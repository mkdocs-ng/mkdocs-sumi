"""Build-time handling of ```` ```echarts ```` and ```` ```markmap ```` fences.

Both are parsed in Python so that mistakes surface as build warnings and
readers without JavaScript still see something useful: the chart's source
and the mind map as a nested list.
"""

from __future__ import annotations

import json
import logging
import re
from html import escape
from typing import Any

import markdown
import yaml

log = logging.getLogger('mkdocs.plugins.sumi')

_HEADING_RE = re.compile(r'^(#{1,6})\s+(.*?)\s*#*\s*$')
_ITEM_RE = re.compile(r'^(?P<indent>[ \t]*)(?:[-*+]|\d+[.)])\s+(?P<text>.*)$')


def _script_json(data: Any) -> str:
    """JSON that is safe inside a <script> element."""
    return json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


def _height(value: str | None, default: int) -> int:
    try:
        return max(120, min(1600, int(str(value).rstrip('px')))) if value else default
    except ValueError:
        return default


def _caption(title: str | None) -> str:
    return f'<figcaption>{escape(title)}</figcaption>' if title else ''


def echarts(body: str, title: str | None, height: str | None) -> str | None:
    """Return the figure for an ECharts option written in YAML or JSON, or None if it is invalid."""
    try:
        option = json.loads(body)
    except ValueError:
        try:
            option = yaml.safe_load(body)
        except yaml.YAMLError as e:
            log.warning("Sumi: an echarts fence is neither valid JSON nor YAML: %s", str(e).splitlines()[0])
            return None
    if not isinstance(option, dict):
        log.warning("Sumi: an echarts fence must contain an option object (a mapping), got %s.", type(option).__name__)
        return None
    h = _height(height, 360)
    return (
        f'<figure class="sumi-chart">'
        f'<div class="sumi-chart-canvas" style="height:{h}px" role="img"'
        f'{f" aria-label={chr(34)}{escape(title)}{chr(34)}" if title else ""}></div>'
        f'<script type="application/json" class="sumi-chart-option">{_script_json(option)}</script>'
        f'<pre class="sumi-chart-source"><code>{escape(body)}</code></pre>'
        f'{_caption(title)}</figure>'
    )


def _inline(md: markdown.Markdown, text: str) -> str:
    html = md.reset().convert(text).strip()
    if html.startswith('<p>') and html.endswith('</p>') and html.count('<p>') == 1:
        html = html[3:-4]
    return html


def outline(body: str) -> dict[str, Any]:
    """Parse headings and nested list items into a markmap tree."""
    md = markdown.Markdown(extensions=['attr_list'])
    root: dict[str, Any] = {'content': '', 'children': []}
    stack: list[tuple[int, dict[str, Any]]] = [(0, root)]
    heading_depth = 0
    unit = 0
    for line in body.splitlines():
        if not line.strip():
            continue
        m = _HEADING_RE.match(line)
        if m:
            depth = len(m.group(1))
            heading_depth = depth
            text = m.group(2)
        else:
            m = _ITEM_RE.match(line)
            if not m:
                continue
            width = len(m.group('indent').expandtabs(4))
            if width and not unit:
                unit = width
            depth = heading_depth + 1 + (width // unit if unit else 0)
            text = m.group('text')
        node = {'content': _inline(md, text), 'children': []}
        while stack[-1][0] >= depth:
            stack.pop()
        stack[-1][1]['children'].append(node)
        stack.append((depth, node))
    if len(root['children']) == 1:
        return root['children'][0]
    return root


def _nested_list(node: dict[str, Any]) -> str:
    if not node['children']:
        return ''
    items = ''.join(f'<li>{c["content"]}{_nested_list(c)}</li>' for c in node['children'])
    return f'<ul>{items}</ul>'


def markmap(body: str, title: str | None, height: str | None) -> str:
    """Return the figure for a mind map written as a Markdown outline."""
    tree = outline(body)
    h = _height(height, 420)
    fallback = (f'<p>{tree["content"]}</p>' if tree['content'] else '') + _nested_list(tree)
    return (
        f'<figure class="sumi-markmap" style="--h:{h}px">'
        f'<div class="sumi-markmap-outline">{fallback}</div>'
        f'<script type="application/json" class="sumi-markmap-data">{_script_json(tree)}</script>'
        f'{_caption(title)}</figure>'
    )
