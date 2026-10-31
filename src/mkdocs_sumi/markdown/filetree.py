"""Render a ```filetree fence as an interactive, JavaScript-free tree.

Both box-drawing trees (as printed by `tree`) and plain indentation work:

    my-site/
    ├── docs/            # Markdown sources
    │   └── index.md
    └── mkdocs.yml       # Site configuration
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from html import escape

from mkdocs_sumi.icons import icon

_PREFIX_CHARS = set(' \t│├└─|`+│├└─ ')
_NOTE_RE = re.compile(r'\s+#\s?(.*)$')

_EXT_ICONS = {
    'file-code': {'py', 'js', 'ts', 'tsx', 'jsx', 'go', 'rs', 'c', 'h', 'cpp', 'java', 'rb', 'php',
                  'sh', 'bash', 'zsh', 'sql', 'html', 'css', 'scss', 'vue', 'svelte', 'lua', 'kt', 'swift'},
    'file-text': {'md', 'markdown', 'txt', 'rst', 'adoc'},
    'file-json': {'json', 'jsonc', 'json5'},
    'file-cog': {'yml', 'yaml', 'toml', 'ini', 'cfg', 'conf', 'env', 'lock'},
    'file-image': {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp', 'avif', 'ico'},
    'file-archive': {'zip', 'gz', 'tgz', 'tar', 'xz', 'bz2', '7z', 'whl'},
}


@dataclass
class Node:
    name: str
    note: str = ''
    is_dir: bool = False
    depth: int = 0
    children: list[Node] = field(default_factory=list)


def _file_icon(name: str) -> str:
    lower = name.lower()
    if lower in ('dockerfile', 'makefile', 'justfile'):
        return 'file-cog'
    if lower.startswith('license') or lower.startswith('readme'):
        return 'file-text'
    ext = lower.rsplit('.', 1)[-1] if '.' in lower else ''
    for icon_name, exts in _EXT_ICONS.items():
        if ext in exts:
            return icon_name
    return 'file'


def parse(source: str) -> list[Node]:
    rows: list[tuple[int, str, str]] = []
    for raw in source.splitlines():
        if not raw.strip():
            continue
        col = 0
        while col < len(raw) and raw[col] in _PREFIX_CHARS:
            col += 1
        text = raw[col:]
        note = ''
        m = _NOTE_RE.search(text)
        if m:
            note = m.group(1).strip()
            text = text[: m.start()]
        elif text.startswith('#'):
            continue
        rows.append((col, text.strip(), note))
    columns = sorted({col for col, _, _ in rows})
    roots: list[Node] = []
    stack: list[Node] = []
    for col, name, note in rows:
        depth = columns.index(col)
        node = Node(name=name.rstrip('/') if name not in ('/', './') else name, note=note,
                    is_dir=name.endswith('/'), depth=depth)
        while stack and stack[-1].depth >= depth:
            stack.pop()
        if stack:
            parent = stack[-1]
            parent.is_dir = True
            node.depth = parent.depth + 1
            parent.children.append(node)
        else:
            node.depth = 0
            roots.append(node)
        stack.append(node)
    return roots


def _width(nodes: list[Node]) -> int:
    best = 0
    for node in nodes:
        best = max(best, node.depth * 3 + len(node.name) + (1 if node.is_dir else 0), _width(node.children))
    return best


def _row(node: Node) -> str:
    name = escape(node.name) + ('<span class="sumi-ft-slash">/</span>' if node.is_dir else '')
    note = f'<span class="sumi-ft-note">{escape(node.note)}</span>' if node.note else ''
    if node.is_dir:
        icons = icon('folder', 'sumi-ft-closed') + icon('folder-open', 'sumi-ft-open')
    else:
        icons = icon(_file_icon(node.name))
    return (f'<span class="sumi-ft-row" style="--d:{node.depth}">{icons}'
            f'<span class="sumi-ft-name">{name}</span>{note}</span>')


def _render(nodes: list[Node]) -> str:
    out = ['<ul>']
    for node in nodes:
        cls = 'sumi-ft-dir' if node.is_dir else 'sumi-ft-file'
        if node.is_dir and node.children:
            out.append(f'<li class="{cls}"><details open><summary>{_row(node)}</summary>'
                       f'{_render(node.children)}</details></li>')
        else:
            out.append(f'<li class="{cls}">{_row(node)}</li>')
    out.append('</ul>')
    return ''.join(out)


def render(source: str, title: str | None = None) -> str:
    nodes = parse(source)
    has_notes = "true" if any(_has_note(n) for n in nodes) else "false"
    head = f'<div class="sumi-ft-title">{escape(title)}</div>' if title else ''
    return (f'<div class="sumi-filetree" data-notes="{has_notes}" style="--ft-col:{_width(nodes) + 4}ch">'
            f'{head}{_render(nodes)}</div>')


def _has_note(node: Node) -> bool:
    return bool(node.note) or any(_has_note(c) for c in node.children)
