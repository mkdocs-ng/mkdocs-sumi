"""The Sumi Markdown extension: native-Markdown components.

Every component is written in plain Markdown plus at most one `{…}`
attribute line, so the source stays readable on GitHub and in the Markdown
copy that MkDocs publishes for LLMs:

- `> [!NOTE]` blockquotes become callouts;
- `{.steps}` after an ordered list makes a procedure;
- `{.cards}` after a bullet list makes a card grid;
- `{.fields}` after a table makes a parameter reference;
- `{caption="…"}` after an image or table adds a caption;
- adjacent fences with `{tab="…"}` become a tab set;
- `title="…"` on a fence adds a file name header;
- ```` ```filetree ```` and ```` ```mermaid ```` fences become a file tree and a diagram;
- `$…$` and `$$…$$` are math, rendered by KaTeX in the browser;
- `++Ctrl+K++` is a key chord and `:lucide-rocket:` an inline icon.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as etree
from html import escape
from typing import Any

from markdown import Extension, Markdown
from markdown.inlinepatterns import InlineProcessor
from markdown.preprocessors import Preprocessor
from markdown.treeprocessors import Treeprocessor
from markdown.util import AtomicString

from mkdocs_sumi.icons import has_icon, icon
from mkdocs_sumi.markdown import filetree
from mkdocs_sumi.markdown.attrs import Attrs, match_attr_line, parse_attrs

# ---------------------------------------------------------------------------
# Callout vocabulary
# ---------------------------------------------------------------------------

CALLOUT_ICONS = {
    'note': 'info',
    'info': 'info',
    'tip': 'lightbulb',
    'hint': 'lightbulb',
    'important': 'message-square-warning',
    'success': 'circle-check',
    'check': 'circle-check',
    'question': 'circle-help',
    'faq': 'circle-help',
    'warning': 'triangle-alert',
    'attention': 'triangle-alert',
    'caution': 'octagon-alert',
    'failure': 'circle-x',
    'danger': 'zap',
    'error': 'circle-x',
    'bug': 'bug',
    'example': 'flask-conical',
    'quote': 'quote',
    'abstract': 'clipboard-list',
    'summary': 'clipboard-list',
    'tldr': 'clipboard-list',
    'todo': 'list-todo',
}

# The colour family each type belongs to.
CALLOUT_FAMILY = {
    'note': 'note', 'info': 'note', 'todo': 'note',
    'tip': 'tip', 'hint': 'tip', 'success': 'tip', 'check': 'tip',
    'important': 'important', 'question': 'important', 'faq': 'important', 'example': 'important',
    'abstract': 'important', 'summary': 'important', 'tldr': 'important',
    'warning': 'warning', 'attention': 'warning',
    'caution': 'caution', 'danger': 'caution', 'failure': 'caution', 'error': 'caution', 'bug': 'caution',
    'quote': 'quote',
}

CALLOUT_LABELS = {
    'en': {
        'note': 'Note', 'info': 'Info', 'tip': 'Tip', 'hint': 'Hint', 'important': 'Important',
        'success': 'Success', 'check': 'Check', 'question': 'Question', 'faq': 'FAQ',
        'warning': 'Warning', 'attention': 'Attention', 'caution': 'Caution', 'failure': 'Failure',
        'danger': 'Danger', 'error': 'Error', 'bug': 'Bug', 'example': 'Example', 'quote': 'Quote',
        'abstract': 'Abstract', 'summary': 'Summary', 'tldr': 'TL;DR', 'todo': 'To do',
    },
    'zh': {
        'note': '注意', 'info': '信息', 'tip': '提示', 'hint': '提示', 'important': '重要',
        'success': '成功', 'check': '检查', 'question': '问题', 'faq': '常见问题',
        'warning': '警告', 'attention': '注意', 'caution': '小心', 'failure': '失败',
        'danger': '危险', 'error': '错误', 'bug': '缺陷', 'example': '示例', 'quote': '引用',
        'abstract': '摘要', 'summary': '摘要', 'tldr': '太长不看', 'todo': '待办',
    },
}

IMAGE_RE = re.compile(r'^!\[[^\]]*\](?:\([^)]*\)|\[[^\]]*\])$')
CALLOUT_RE = re.compile(r'^\[!(?P<type>[A-Za-z]+)\](?P<fold>[+-]?)[ \t]*(?P<title>[^\n]*)(?:\n|$)')

# ---------------------------------------------------------------------------
# Fences
# ---------------------------------------------------------------------------

FENCE_OPEN_RE = re.compile(r'^(?P<indent>[ \t]*)(?P<fence>`{3,}|~{3,})[ \t]*(?P<info>[^`\n]*?)[ \t]*$')
_KV_RE = r'(?P<key>{key})=(?:"(?P<dq>[^"]*)"|\'(?P<sq>[^\']*)\'|(?P<bare>[^\s}}]+))'


def _take(info: str, key: str) -> tuple[str, str | None]:
    """Remove `key="value"` from a fence info string; return (info, value)."""
    m = re.search(r'(?:^|(?<=[\s{]))' + _KV_RE.format(key=key), info)
    if not m:
        return info, None
    value = m.group('dq') if m.group('dq') is not None else m.group('sq') if m.group('sq') is not None else m.group('bare')
    info = (info[: m.start()] + info[m.end():])
    info = re.sub(r'\{\s*\}', '', info)
    info = re.sub(r'[ \t]{2,}', ' ', info).strip()
    return info, value


def _lang(info: str) -> str:
    m = re.match(r'\{?\s*\.?([\w#.+-]+)', info)
    return m.group(1).lower() if m else ''


class _Fence:
    __slots__ = ('start', 'end', 'indent', 'info', 'lines', 'tab', 'title', 'lang', 'opener', 'closer', 'raw')

    def __init__(self, start, end, indent, opener, info, lines, closer, raw):
        self.start, self.end, self.indent, self.raw = start, end, indent, raw
        self.opener, self.closer = opener, closer
        self.info, self.lines = info, lines
        self.info, self.tab = _take(self.info, 'tab')
        self.info, self.title = _take(self.info, 'title')
        self.lang = _lang(self.info)


class FencePreprocessor(Preprocessor):
    """Group `{tab=…}` fences, add titles, and render filetree / mermaid fences.

    Runs before the fence processor of either `fenced_code` or
    `pymdownx.superfences`, and only rewrites what it recognises.
    """

    def __init__(self, md: Markdown, ext: SumiExtension):
        super().__init__(md)
        self.ext = ext

    def _scan(self, lines: list[str]) -> list[_Fence | str]:
        out: list[_Fence | str] = []
        i = 0
        while i < len(lines):
            m = FENCE_OPEN_RE.match(lines[i])
            if not m:
                out.append(lines[i])
                i += 1
                continue
            fence = m.group('fence')
            close_re = re.compile(r'^[ \t]*' + re.escape(fence[0]) + '{' + str(len(fence)) + r',}[ \t]*$')
            j = i + 1
            while j < len(lines) and not close_re.match(lines[j]):
                j += 1
            if j >= len(lines):  # unclosed: leave it alone
                out.extend(lines[i:])
                break
            out.append(_Fence(i, j, m.group('indent'), fence, m.group('info'), lines[i + 1: j], lines[j], lines[i]))
            i = j + 1
        return out

    def _stash(self, html: str) -> str:
        return self.md.htmlStash.store(html)

    def _emit_code(self, f: _Fence) -> list[str]:
        ind = f.indent
        if f.lang == 'filetree':
            body = [ln[len(ind):] if ln.startswith(ind) else ln for ln in f.lines]
            return ['', ind + self._stash(filetree.render('\n'.join(body), f.title)), '']
        if f.lang == 'mermaid' and self.ext.getConfig('mermaid'):
            body = '\n'.join(ln[len(ind):] if ln.startswith(ind) else ln for ln in f.lines)
            title = f'<figcaption>{escape(f.title)}</figcaption>' if f.title else ''
            html = f'<figure class="sumi-diagram"><pre class="mermaid">{escape(body)}</pre>{title}</figure>'
            return ['', ind + self._stash(html), '']
        if f.tab is None and f.title is None:
            block = [f.raw, *f.lines, f.closer]
        else:
            block = [f'{ind}{f.opener}{f.info}', *f.lines, f.closer]
        if f.title:
            head = (f'<div class="sumi-code" data-title="{escape(f.title)}">'
                    f'<div class="sumi-code-title">{icon("file-code")}<span>{escape(f.title)}</span></div>')
            return ['', ind + self._stash(head), '', *block, '', ind + self._stash('</div>'), '']
        return block

    def run(self, lines: list[str]) -> list[str]:
        items = self._scan(lines)
        if not any(isinstance(it, _Fence) for it in items):
            return lines
        out: list[str] = []
        k = 0
        while k < len(items):
            it = items[k]
            if isinstance(it, str):
                out.append(it)
                k += 1
                continue
            if it.tab is None:
                out.extend(self._emit_code(it))
                k += 1
                continue
            # Collect adjacent tabbed fences at the same indentation.
            group = [it]
            n = k + 1
            while True:
                m = n
                while m < len(items) and isinstance(items[m], str) and not items[m].strip():
                    m += 1
                if m < len(items) and isinstance(items[m], _Fence) and items[m].tab is not None \
                        and items[m].indent == it.indent:
                    group.append(items[m])
                    n = m + 1
                else:
                    break
            ind = it.indent
            labels = [g.tab or str(i + 1) for i, g in enumerate(group)]
            self.ext.tab_groups += 1
            gid = self.ext.tab_groups
            out += ['', ind + self._stash(f'<div class="sumi-tabs" data-group="{escape("|".join(labels))}">'), '']
            for i, g in enumerate(group):
                out += ['', ind + self._stash(
                    f'<div class="sumi-tab" data-label="{escape(labels[i])}" id="tab-{gid}-{i + 1}">'
                    f'<div class="sumi-tab-label">{escape(labels[i])}</div>'), '']
                out += self._emit_code(g)
                out += ['', ind + self._stash('</div>'), '']
            out += ['', ind + self._stash('</div>'), '']
            k = n
        return out


class BlockPreprocessor(Preprocessor):
    """Isolate `{…}` attribute lines and stash `$$` math blocks.

    Runs after fences are stashed, so code is never touched.
    """

    def __init__(self, md: Markdown, ext: SumiExtension):
        super().__init__(md)
        self.ext = ext

    def run(self, lines: list[str]) -> list[str]:
        out: list[str] = []
        math = self.ext.getConfig('math')
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            if math and stripped.startswith('$$'):
                ind = line[: len(line) - len(line.lstrip())]
                rest = stripped[2:]
                if rest.endswith('$$') and len(rest) > 2:
                    tex = rest[:-2].strip()
                    out += ['', ind + self._math(tex), '']
                    i += 1
                    continue
                j = i + 1
                body = [rest] if rest.strip() else []
                while j < len(lines) and not lines[j].strip().endswith('$$'):
                    body.append(lines[j].strip())
                    j += 1
                if j < len(lines):
                    last = lines[j].strip()[:-2].strip()
                    if last:
                        body.append(last)
                    out += ['', ind + self._math('\n'.join(body)), '']
                    i = j + 1
                    continue
            if line[:1] == '{' and match_attr_line(line):
                if out and out[-1].strip():
                    out.append('')
                out.append(line.strip())
                if i + 1 < len(lines) and lines[i + 1].strip():
                    out.append('')
                i += 1
                continue
            out.append(line)
            i += 1
        return out

    def _math(self, tex: str) -> str:
        self.ext.page_features.add('math')
        return self.md.htmlStash.store(f'<div class="sumi-math math-display">{escape(tex)}</div>')


class MathInline(InlineProcessor):
    def __init__(self, pattern: str, md: Markdown, ext: SumiExtension):
        super().__init__(pattern, md)
        self.ext = ext

    def handleMatch(self, m, data):  # type: ignore[override]
        el = etree.Element('span', {'class': 'sumi-math math-inline'})
        el.text = AtomicString(m.group(1))
        self.ext.page_features.add('math')
        return el, m.start(0), m.end(0)


class KeysInline(InlineProcessor):
    def handleMatch(self, m, data):  # type: ignore[override]
        keys = [k.strip() for k in m.group(1).split('+') if k.strip()]
        el = etree.Element('span', {'class': 'sumi-keys'})
        for n, key in enumerate(keys):
            if n:
                sep = etree.SubElement(el, 'span', {'class': 'sumi-keys-sep'})
                sep.text = '+'
            kbd = etree.SubElement(el, 'kbd')
            kbd.text = AtomicString(key)
        return el, m.start(0), m.end(0)


class IconInline(InlineProcessor):
    def handleMatch(self, m, data):  # type: ignore[override]
        name = m.group(1)
        if not has_icon(name):
            return None, None, None
        return self.md.htmlStash.store(str(icon(name, 'sumi-icon-inline'))), m.start(0), m.end(0)


class ComponentTreeprocessor(Treeprocessor):
    """Callouts, attribute lines, fields, captions and table wrappers."""

    def __init__(self, md: Markdown, ext: SumiExtension):
        super().__init__(md)
        self.ext = ext

    def run(self, root: etree.Element) -> None:
        self._walk(root)

    def _walk(self, parent: etree.Element) -> None:
        children = list(parent)
        k = 0
        while k < len(children):
            el = children[k]
            if el.tag == 'p' and len(el) == 0 and el.text and k > 0:
                attrs = match_attr_line(el.text)
                if attrs is not None:
                    prev = children[k - 1]
                    replacement = self._apply(parent, prev, attrs)
                    parent.remove(el)
                    children.pop(k)
                    if replacement is not None:
                        children[k - 1] = replacement
                    continue
            k += 1
        for el in list(parent):
            if el.tag == 'blockquote':
                self._callout(parent, el)
        for el in list(parent):
            if el.tag == 'table':
                self._wrap_table(parent, el)
        for el in parent:
            if el.tag not in ('pre', 'code'):
                self._walk(el)

    # -- attribute lines ---------------------------------------------------

    def _apply(self, parent: etree.Element, el: etree.Element, attrs: Attrs) -> etree.Element | None:
        classes = list(attrs.classes)
        values = dict(attrs.values)
        new = None
        if el.tag == 'ol' and 'steps' in classes:
            classes[classes.index('steps')] = 'sumi-steps'
        if el.tag == 'ul' and 'cards' in classes:
            classes[classes.index('cards')] = 'sumi-cards'
            cols = values.pop('cols', None)
            if cols:
                el.set('style', f'--cols:{int(cols) if cols.isdigit() else 2}')
        if el.tag == 'ul' and 'checklist' in classes:
            classes[classes.index('checklist')] = 'sumi-checklist'
        if el.tag == 'table':
            caption = values.pop('caption', None)
            if caption:
                cap = etree.Element('caption')
                cap.text = caption
                el.insert(0, cap)
            if 'fields' in classes:
                classes.remove('fields')
                new = self._fields(parent, el, values.pop('meta', None))
            for flag in ('wide', 'compact', 'striped', 'center'):
                if flag in classes:
                    classes.remove(flag)
                    el.set('data-' + flag, '')
        if el.tag == 'p' and 'caption' in values and self._is_image_para(el):
            new = self._figure(parent, el, values.pop('caption'))
        target = new if new is not None else el
        if attrs.id:
            target.set('id', attrs.id)
        if classes:
            target.set('class', ' '.join(filter(None, [target.get('class', ''), *classes])))
        for key, value in values.items():
            target.set(key, value)
        return new

    @staticmethod
    def _is_image_para(el: etree.Element) -> bool:
        return len(el) == 0 and bool(IMAGE_RE.match((el.text or '').strip()))

    def _figure(self, parent: etree.Element, p: etree.Element, caption: str) -> etree.Element:
        fig = etree.Element('figure', {'class': 'sumi-figure'})
        fig.text = p.text.strip()
        cap = etree.SubElement(fig, 'figcaption')
        cap.text = caption
        idx = list(parent).index(p)
        parent.remove(p)
        parent.insert(idx, fig)
        return fig

    def _fields(self, parent: etree.Element, table: etree.Element, meta: str | None) -> etree.Element:
        head = table.find('thead')
        body = table.find('tbody')
        names = [(th.text or '').strip() for th in head.iter('th')] if head is not None else []
        lower = [n.lower() for n in names]
        if meta:
            meta_cols = {i for i, n in enumerate(lower) if n in meta.lower().split()}
        else:
            meta_cols = {i for i, n in enumerate(lower) if n in ('type', 'default', 'required', '类型', '默认值', '必填')}
        meta_cols.discard(0)
        box = etree.Element('div', {'class': 'sumi-fields'})
        for tr in (body if body is not None else []):
            cells = list(tr)
            if not cells:
                continue
            item = etree.SubElement(box, 'div', {'class': 'sumi-field'})
            top = etree.SubElement(item, 'div', {'class': 'sumi-field-head'})
            name = etree.SubElement(top, 'span', {'class': 'sumi-field-name'})
            self._move(cells[0], name)
            desc = etree.Element('div', {'class': 'sumi-field-body'})
            for i, cell in enumerate(cells[1:], start=1):
                label = lower[i] if i < len(lower) else ''
                text = (cell.text or '').strip()
                if i in meta_cols:
                    if not text and len(cell) == 0:
                        continue
                    if label in ('required', '必填'):
                        if text.lower() in ('yes', 'true', 'y', '✓', '✔', '是', 'required'):
                            chip = etree.SubElement(top, 'span', {'class': 'sumi-chip sumi-chip--required'})
                            chip.text = names[i] if label != 'required' else 'required'
                        continue
                    chip = etree.SubElement(top, 'span', {'class': 'sumi-chip', 'data-key': label})
                    if label not in ('type', '类型'):
                        k = etree.SubElement(chip, 'span', {'class': 'sumi-chip-key'})
                        k.text = names[i] + ' '
                    holder = etree.SubElement(chip, 'span')
                    self._move(cell, holder)
                else:
                    holder = etree.SubElement(desc, 'div')
                    self._move(cell, holder)
            if len(desc):
                item.append(desc)
        idx = list(parent).index(table)
        parent.remove(table)
        parent.insert(idx, box)
        return box

    @staticmethod
    def _move(src: etree.Element, dst: etree.Element) -> None:
        dst.text = src.text
        for child in list(src):
            dst.append(child)

    def _wrap_table(self, parent: etree.Element, table: etree.Element) -> None:
        if parent.get('class', '').startswith('sumi-table'):
            return
        wrapper = etree.Element('div', {'class': 'sumi-table'})
        for flag in ('wide', 'compact', 'striped', 'center'):
            if table.get('data-' + flag) is not None:
                wrapper.set('class', wrapper.get('class') + ' sumi-table--' + flag)
        idx = list(parent).index(table)
        parent.remove(table)
        wrapper.tail, table.tail = table.tail, None
        wrapper.append(table)
        parent.insert(idx, wrapper)

    # -- callouts ----------------------------------------------------------

    def _callout(self, parent: etree.Element, quote: etree.Element) -> None:
        if not len(quote) or quote[0].tag != 'p' or not quote[0].text or not self._marker(quote[0]):
            return
        # Python-Markdown merges blockquotes separated by a blank line: split
        # them again at every marker paragraph.
        segments: list[list[etree.Element]] = []
        for child in list(quote):
            if child.tag == 'p' and child.text and self._marker(child):
                segments.append([])
            segments[-1].append(child)
        idx = list(parent).index(quote)
        tail = quote.tail
        parent.remove(quote)
        boxes = [self._build_callout(seg) for seg in segments]
        for n, box in enumerate(boxes):
            parent.insert(idx + n, box)
        boxes[-1].tail = tail

    @staticmethod
    def _marker(p: etree.Element) -> re.Match[str] | None:
        m = CALLOUT_RE.match(p.text or '')
        return m if m and m.group('type').lower() in CALLOUT_ICONS else None

    def _build_callout(self, seg: list[etree.Element]) -> etree.Element:
        first = seg[0]
        m = self._marker(first)
        assert m is not None
        kind = m.group('type').lower()
        fold = m.group('fold')
        title = m.group('title').strip()
        labels = CALLOUT_LABELS.get(self.ext.getConfig('language')[:2], CALLOUT_LABELS['en'])
        family = CALLOUT_FAMILY.get(kind, 'note')
        cls = f'sumi-callout sumi-callout--{family}'
        if family != kind:
            cls += f' sumi-callout--{kind}'
        first.text = first.text[m.end():]
        if not first.text.strip() and len(first) == 0:
            seg = seg[1:]
        if fold:
            box = etree.Element('details', {'class': cls})
            if fold == '+':
                box.set('open', '')
            head = etree.SubElement(box, 'summary', {'class': 'sumi-callout-title'})
        else:
            box = etree.Element('div', {'class': cls, 'role': 'note'})
            head = etree.SubElement(box, 'p', {'class': 'sumi-callout-title'})
        head.text = self.md.htmlStash.store(str(icon(CALLOUT_ICONS[kind])))
        label = etree.SubElement(head, 'span')
        label.text = title or labels.get(kind, kind.title())
        content = etree.SubElement(box, 'div', {'class': 'sumi-callout-body'})
        for child in seg:
            content.append(child)
        return box


class ImageTreeprocessor(Treeprocessor):
    """Lazy-load content images once inline images exist."""

    def run(self, root: etree.Element) -> None:
        for img in root.iter('img'):
            img.set('loading', img.get('loading', 'lazy'))
            img.set('decoding', img.get('decoding', 'async'))


class SumiExtension(Extension):
    def __init__(self, **kwargs: Any):
        self.config = {
            'language': ['en', 'Language used for default callout titles.'],
            'math': [True, 'Enable `$…$` and `$$…$$` math.'],
            'mermaid': [True, 'Render ```mermaid fences as diagrams.'],
            'keys': [True, 'Enable `++Ctrl+K++` key chords.'],
            'icons': [True, 'Enable `:lucide-name:` inline icons.'],
        }
        super().__init__(**kwargs)
        self.tab_groups = 0
        self.page_features: set[str] = set()

    def reset(self) -> None:
        self.tab_groups = 0
        self.page_features = set()

    def extendMarkdown(self, md: Markdown) -> None:
        md.registerExtension(self)
        self.reset()
        md.preprocessors.register(FencePreprocessor(md, self), 'sumi_fences', 26)
        md.preprocessors.register(BlockPreprocessor(md, self), 'sumi_blocks', 24)
        names = {type(e).__module__ for e in md.registeredExtensions}
        if self.getConfig('math') and 'pymdownx.arithmatex' not in names:
            md.inlinePatterns.register(
                MathInline(r'(?<![\\$\w])\$(?![\s$])((?:\\\$|[^$\n])+?)(?<![\s\\])\$(?![\w$])', md, self),
                'sumi_math', 185)
        if self.getConfig('keys') and 'pymdownx.keys' not in names:
            md.inlinePatterns.register(KeysInline(r'\+\+([^+\s][^\n]*?[^+\s]|[^+\s])\+\+', md), 'sumi_keys', 186)
        if self.getConfig('icons'):
            md.inlinePatterns.register(IconInline(r':((?:lucide|brand)-[a-z0-9-]+):', md), 'sumi_icons', 184)
        md.treeprocessors.register(ComponentTreeprocessor(md, self), 'sumi_components', 25)
        md.treeprocessors.register(ImageTreeprocessor(md), 'sumi_images', 1)


def makeExtension(**kwargs: Any) -> SumiExtension:
    return SumiExtension(**kwargs)
