"""Release lists for `template: releases.html`, from a YAML file, GitHub Releases and PyPI.

A releases page can name its sources in the front matter:

    releases:
      github: owner/repo     # versions, dates and notes from GitHub Releases
      pypi: package-name     # downloads with sizes and SHA-256 checksums
      file: releases.yml     # hand-written entries; their fields win

The remote sources are read once per build process and cached, so `mkdocs serve`
doesn't refetch them on every change. When one can't be reached, the build warns
and goes on with what it has.
"""

from __future__ import annotations

import json
import logging
import os
import re
import urllib.request
from collections.abc import Callable
from typing import Any

log = logging.getLogger('mkdocs.plugins.sumi')

_cache: dict[str, Any] = {}

_COMMENT_RE = re.compile(r'<!--.*?-->', re.DOTALL)
_HEADING_RE = re.compile(r'^(#{1,4})(?=\s)', re.MULTILINE)
_URL_RE = re.compile(r'(?<![<(\w])(https?://[^\s<>()]+[^\s<>().,;:!?\'"])')
_REF_RE = re.compile(r'(?<![\w/&\[#])#(\d+)\b(?!\])')
_USER_RE = re.compile(r'(?<![\w/@.\[`])@([A-Za-z0-9](?:[A-Za-z0-9-]{0,38}))\b(?!\])')


def _get_json(url: str) -> Any:
    headers = {'Accept': 'application/json', 'User-Agent': 'mkdocs-sumi'}
    if url.startswith('https://api.github.com/'):
        headers['Accept'] = 'application/vnd.github+json'
        token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
        if token:
            headers['Authorization'] = f'Bearer {token}'
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=20) as resp:
        return json.load(resp)


def _fetch(key: str, fetch: Callable[[], Any], what: str) -> Any:
    if key not in _cache:
        try:
            _cache[key] = fetch()
        except (OSError, ValueError, TypeError, KeyError) as e:  # network, HTTP or bad data: still build
            log.warning(f"sumi: couldn't read {what}: {e}")
            return None
    return _cache[key]


def github_releases(repo: str) -> list[dict[str, Any]]:
    """Published releases of `owner/repo`, newest first, as release entries."""

    def fetch() -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for n in range(1, 11):
            batch = _get_json(f'https://api.github.com/repos/{repo}/releases?per_page=100&page={n}')
            out.extend(batch)
            if len(batch) < 100:
                break
        return out

    data = _fetch(f'github:{repo}', fetch, f'the releases of {repo} from GitHub') or []
    return [from_github(rel, repo) for rel in data if not rel.get('draft')]


def pypi_assets(package: str) -> dict[str, list[dict[str, str]]]:
    """Downloads of each version of a PyPI package: name, url, size and sha256."""
    data = _fetch(f'pypi:{package}', lambda: _get_json(f'https://pypi.org/pypi/{package}/json'),
                  f'the files of {package} from PyPI') or {}
    assets: dict[str, list[dict[str, str]]] = {}
    for version, files in (data.get('releases') or {}).items():
        assets[version] = [{
            'name': f['filename'],
            'url': f['url'],
            'size': format_size(f.get('size') or 0),
            'sha256': (f.get('digests') or {}).get('sha256', ''),
        } for f in sorted(files, key=lambda f: f['filename'].endswith('.tar.gz'))]
    return assets


def format_size(size: int) -> str:
    for unit in ('B', 'KB', 'MB'):
        if size < 1000 or unit == 'MB':
            return f'{size} B' if unit == 'B' else f'{size:.1f} {unit}'
        size /= 1000
    return ''  # pragma: no cover


def version_of(tag: str) -> str:
    return tag[1:] if re.match(r'v\d', tag) else tag


def from_github(rel: dict[str, Any], repo: str) -> dict[str, Any]:
    """A release entry from a GitHub release: the first paragraph is the summary, the rest the notes."""
    tag = rel.get('tag_name') or ''
    version = version_of(tag)
    entry: dict[str, Any] = {'version': version}
    name = (rel.get('name') or '').strip()
    if name and name not in (tag, version):
        entry['title'] = name
    if rel.get('published_at'):
        entry['date'] = rel['published_at'][:10]
    if rel.get('prerelease'):
        entry['status'] = 'prerelease'
    body = _COMMENT_RE.sub('', (rel.get('body') or '').replace('\r\n', '\n')).strip()
    first, _, rest = body.partition('\n\n')
    if first and not re.match(r'\s*(#|[-*+] |\d+\. |```|\||>|\*\*)', first):
        entry['summary'] = ' '.join(first.split())
        body = rest.strip()
    if body:
        entry['notes'] = github_markdown(body, repo)
    assets = [{
        'name': a['name'],
        'url': a['browser_download_url'],
        'size': format_size(a.get('size') or 0),
        'sha256': (a.get('digest') or '').removeprefix('sha256:'),
    } for a in rel.get('assets') or [] if a.get('browser_download_url')]
    if assets:
        entry['assets'] = assets
    return entry


def github_markdown(text: str, repo: str) -> str:
    """Release notes written for GitHub, made to read well on a releases page."""
    text = _HEADING_RE.sub(lambda m: '#' * min(len(m.group(1)) + 2, 6), text)
    text = _URL_RE.sub(r'<\1>', text)
    text = _REF_RE.sub(lambda m: f'[#{m.group(1)}](https://github.com/{repo}/issues/{m.group(1)})', text)
    text = _USER_RE.sub(lambda m: f'[@{m.group(1)}](https://github.com/{m.group(1)})', text)
    return text


def merge(base: list[dict[str, Any]], extra: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """`base` with the fields of `extra` laid over it by version; new versions sorted in by date."""
    if not base:
        return list(extra)
    by_version = {str(rel.get('version')): rel for rel in extra}
    out = [{**rel, **by_version.pop(str(rel.get('version')), {})} for rel in base]
    if by_version:
        out += by_version.values()
        out.sort(key=lambda rel: str(rel.get('date') or ''), reverse=True)
    return out
