"""Build small sites with the theme and plugin and check the outputs."""

from __future__ import annotations

import os
import textwrap
from pathlib import Path

import pytest
from mkdocs.commands import build
from mkdocs.config import load_config

ROOT = Path(__file__).resolve().parent.parent

try:
    import mkdocs.contrib.llms_txt  # noqa: F401

    HAS_LLMS_TXT = True
except ImportError:  # MkDocs-ng before 1.9
    HAS_LLMS_TXT = False
needs_llms_txt = pytest.mark.skipif(not HAS_LLMS_TXT, reason='needs the llms_txt plugin of MkDocs-ng 1.9')


def _site(tmp_path: Path, files: dict[str, str], config: str) -> Path:
    for name, content in files.items():
        path = tmp_path / 'docs' / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(content).lstrip('\n'), encoding='utf-8')
    (tmp_path / 'mkdocs.yml').write_text(textwrap.dedent(config), encoding='utf-8')
    cfg = load_config(str(tmp_path / 'mkdocs.yml'))
    build.build(cfg)
    return tmp_path / 'site'


BASIC = """
    site_name: Test
    site_url: https://example.com/
    theme:
      name: sumi
      announcement: 'New: <a href="blog/">the blog</a>'
    plugins:
      - search
      - sumi
""" + ('      - llms_txt\n' if HAS_LLMS_TXT else '')


@pytest.fixture
def site(tmp_path):
    return _site(tmp_path, {
        'index.md': """
            ---
            template: landing.html
            hero:
              title: "Hello<br>world"
              text: A test site.
            sections:
              - type: features
                title: Features
                items:
                  - {icon: zap, title: Fast, text: Very fast., link: guide/}
            ---
            """,
        'guide/index.md': '# Guide\n\nSee [the post](../blog/posts/2026-01-02-hello.md).\n',
        'guide/math.md': '# Math\n\n$x^2$\n',
        'blog/.authors.yml': 'authors:\n  me: {name: Me}\n',
        'blog/posts/2026-01-02-hello.md': """
            ---
            date: 2026-01-02
            authors: [me]
            tags: [news]
            ---
            # Hello

            Excerpt.

            <!-- more -->

            Rest.
            """,
    }, BASIC)


def test_pages_and_assets(site):
    assert (site / 'index.html').is_file()
    assert (site / 'assets' / 'css' / 'sumi.css').is_file()
    # Vendor runtimes are copied only when a page uses them.
    assert (site / 'assets' / 'sumi' / 'vendor' / 'katex').is_dir()
    assert not (site / 'assets' / 'sumi' / 'vendor' / 'mermaid').exists()


def test_landing_page(site):
    html = (site / 'index.html').read_text()
    assert 'sumi-hero' in html and 'Hello<br>world' in html
    assert 'sumi-feature' in html
    md = (site / 'index.md').read_text()
    assert '**Hello world**' in md
    assert '> A test site.' in md
    assert '[**Fast**](guide/): Very fast.' in md


def test_blog(site):
    post = site / 'blog' / '2026' / '01' / '02' / 'hello' / 'index.html'
    assert post.is_file()
    index = (site / 'blog' / 'index.html').read_text()
    assert 'Hello' in index and 'data-tags="news"' in index and 'Excerpt.' in index
    feed = (site / 'blog' / 'feed.xml').read_text()
    assert '<feed' in feed and 'https://example.com/blog/2026/01/02/hello/' in feed
    guide = (site / 'guide' / 'index.html').read_text()
    assert 'href="../blog/2026/01/02/hello/"' in guide
    # Posts stay out of the navigation.
    nav = guide.split('<nav class="sumi-nav">')[1].split('</nav>')[0]
    assert 'hello' not in nav


def test_markdown_discovery_and_llms(site):
    html = (site / 'guide' / 'index.html').read_text()
    assert '<link rel="alternate" type="text/markdown" href="../index.md"' not in html
    assert 'type="text/markdown"' in html
    if HAS_LLMS_TXT:
        assert (site / 'llms.txt').read_text().startswith('# Test')


def test_announcement_links_are_rebased(site):
    html = (site / 'guide' / 'math' / 'index.html').read_text()
    assert 'href="../../blog/"' in html


def test_print_edition(site):
    html = (site / 'print' / 'index.html').read_text()
    assert 'sumi-print' in html
    assert 'Guide' in html and 'Math' in html


@needs_llms_txt
def test_docs_site_builds_without_warnings(tmp_path, caplog):
    """The documentation of Sumi is its own regression suite."""
    cfg = load_config(str(ROOT / 'mkdocs.yml'), site_dir=str(tmp_path / 'site'))
    cfg['strict'] = True
    build.build(cfg)
    assert (tmp_path / 'site' / 'docs' / 'write' / 'callouts' / 'index.html').is_file()
    assert not [r for r in caplog.records if r.levelname == 'WARNING']


def test_git_dates_parse_utc_written_as_z(tmp_path, monkeypatch):
    """Newer Git writes UTC commit dates with a "Z" suffix; Python 3.10 must still parse them."""
    import datetime
    import subprocess

    from mkdocs_sumi import plugin

    outputs = iter([f'{tmp_path}\n', '@2026-11-01T12:02:53Z\n\ndocs/a.md\n@2026-10-31T23:18:41+02:00\n\ndocs/b.md\n'])

    def fake_run(*args, **kwargs):
        return subprocess.CompletedProcess(args, 0, stdout=next(outputs))

    monkeypatch.setattr(plugin.subprocess, 'run', fake_run)
    (tmp_path / 'docs').mkdir()
    dates = plugin._git_dates(str(tmp_path / 'docs'))
    assert dates['a.md'] == datetime.datetime(2026, 11, 1, 12, 2, 53, tzinfo=datetime.timezone.utc)
    assert dates['b.md'].utcoffset() == datetime.timedelta(hours=2)
