"""A Markdown version of a landing page, for its `.md` copy and `llms.txt` readers.

A landing page keeps its content in front matter, so its Markdown body is
often empty. This turns the hero and sections into headings and lists.
"""

from __future__ import annotations

import re
from typing import Any

_TAG_RE = re.compile(r'<br\s*/?>|<[^>]+>')


def _text(value: Any) -> str:
    text = _TAG_RE.sub(lambda m: ' ' if m.group(0).lower().startswith('<br') else '', str(value or ''))
    return ' '.join(text.split())


def _link(text: str, link: Any) -> str:
    return f'[{text}]({link})' if link else text


def _actions(items: Any) -> list[str]:
    return [f'- {_link(_text(a.get("text")), a.get("link"))}' for a in items or [] if isinstance(a, dict) and a.get('text')]


def _code(code: Any) -> list[str]:
    if not isinstance(code, dict) or not code.get('content'):
        return []
    body = str(code['content']).rstrip('\n')
    fence = '`' * max(3, max((len(m) for m in re.findall(r'`+', body)), default=0) + 1)
    title = f' title="{code["title"]}"' if code.get('title') else ''
    return [f'{fence}{code.get("lang") or "text"}{title}', body, fence, '']


def landing_markdown(meta: dict[str, Any], body: str, h1: str | None) -> str:
    """`h1` is the page's own heading; without one, MkDocs adds the page title."""
    hero = meta.get('hero') or {}
    out: list[str] = [f'# {h1}', ''] if h1 else []
    if hero.get('title') and _text(hero['title']) != h1:
        out += [f'**{_text(hero["title"])}**', '']
    if hero.get('text'):
        out += [f'> {_text(hero["text"])}', '']
    if hero.get('install'):
        out += ['```sh', str(hero['install']), '```', '']
    out += _code(hero.get('code'))
    if hero.get('actions'):
        out += [*_actions(hero['actions']), '']
    for s in meta.get('sections') or []:
        if not isinstance(s, dict):
            continue
        kind = s.get('type') or 'content'
        if kind == 'content':
            if body.strip():
                out += [body.strip(), '']
            continue
        if s.get('title'):
            out += [f'## {_text(s["title"])}', '']
        if s.get('text'):
            out += [_text(s['text']), '']
        items = s.get('items') or []
        if kind == 'features':
            for f in items:
                name = _link(f'**{_text(f.get("title"))}**', f.get('link'))
                out.append(f'- {name}: {_text(f.get("text"))}')
            out.append('')
        elif kind == 'stats':
            out += [f'- **{_text(st.get("value"))}** {_text(st.get("label"))}' for st in items] + ['']
        elif kind == 'steps':
            out += [f'{n}. **{_text(st.get("title"))}**: {_text(st.get("text"))}' for n, st in enumerate(items, 1)] + ['']
        elif kind == 'faq':
            for f in items:
                out += [f'### {_text(f.get("q"))}', '', str(f.get('a') or '').strip(), '']
        elif kind == 'split':
            out += [f'- {_text(b)}' for b in s.get('bullets') or []] + ([''] if s.get('bullets') else [])
            out += _code(s.get('code'))
            if s.get('markdown'):
                out += [str(s['markdown']).strip(), '']
        if s.get('actions'):
            out += [*_actions(s['actions']), '']
    if not any((s or {}).get('type', 'content') == 'content' for s in meta.get('sections') or []) and body.strip():
        out += [body.strip(), '']
    return '\n'.join(out).strip() + '\n'
