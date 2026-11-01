"""The Sumi plugin: Markdown components, blog, print edition and AI-friendly outputs.

The theme needs this plugin. Enable both:

    theme:
      name: sumi
    plugins:
      - search
      - sumi
"""

from __future__ import annotations

import datetime
import json
import logging
import os
import posixpath
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from importlib import resources
from typing import TYPE_CHECKING, Any
from urllib.parse import quote, urlsplit

import yaml
from jinja2 import pass_context
from markupsafe import Markup

from mkdocs import utils
from mkdocs.config import base
from mkdocs.config import config_options as c
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin, CombinedEvent, event_priority
from mkdocs.structure.files import File, Files
from mkdocs.structure.nav import Navigation, Section
from mkdocs.structure.pages import Page

from mkdocs_sumi.i18n import STRINGS, translator
from mkdocs_sumi.icons import icon

if TYPE_CHECKING:
    from jinja2 import Environment

    from mkdocs.config.defaults import MkDocsConfig

log = logging.getLogger('mkdocs.plugins.sumi')

_CJK_RE = re.compile(r'[぀-ヿ㐀-䶿一-鿿가-힯]')
_WORD_RE = re.compile(r'[A-Za-z0-9_\'-]+')
_MORE_RE = re.compile(r'<!--\s*more\s*-->', re.I)
_TAG_RE = re.compile(r'<[^>]+>')
_URL_ATTR_RE = re.compile(r'(?P<attr>\s(?:href|src))="(?P<url>[^"]*)"')


class _BlogConfig(base.Config):
    enabled = c.Type(bool, default=True)
    dir = c.Type(str, default='blog')
    feed = c.Type(bool, default=True)
    feed_items = c.Type(int, default=20)
    authors = c.Type(dict, default={})


class _PrintConfig(base.Config):
    enabled = c.Type(bool, default=True)
    path = c.Type(str, default='print/')


class SumiConfig(base.Config):
    language = c.Optional(c.Type(str))
    math = c.Type(bool, default=True)
    mermaid = c.Type(bool, default=True)
    markdown_copy = c.Type(bool, default=True)
    assistant_links = c.ListOfItems(c.Choice(['chatgpt', 'claude']), default=[])
    git_dates = c.Type(bool, default=False)
    blog = c.SubConfig(_BlogConfig)
    print = c.SubConfig(_PrintConfig)


@dataclass
class Post:
    page: Page
    date: datetime.datetime
    updated: datetime.datetime | None = None
    authors: list[dict[str, str]] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    excerpt: str = ''
    reading_time: int = 1

    @property
    def title(self) -> str:
        return self.page.title or ''

    @property
    def url(self) -> str:
        return self.page.url


def _parse_date(value: Any) -> datetime.datetime | None:
    if isinstance(value, dict):
        value = value.get('created') or next(iter(value.values()), None)
    if isinstance(value, datetime.datetime):
        return value
    if isinstance(value, datetime.date):
        return datetime.datetime(value.year, value.month, value.day)
    if isinstance(value, str):
        try:
            return datetime.datetime.fromisoformat(value.strip())
        except ValueError:
            return None
    return None


def reading_minutes(text: str) -> int:
    """Estimate reading time: 230 Latin words or 400 CJK characters per minute."""
    cjk = len(_CJK_RE.findall(text))
    words = len(_WORD_RE.findall(_CJK_RE.sub(' ', text)))
    return max(1, round(words / 230 + cjk / 400))


class SumiPlugin(BasePlugin[SumiConfig]):
    supports_multiple_instances = False

    def __init__(self) -> None:
        super().__init__()
        self.features: dict[str, set[str]] = {}
        self.contents: dict[str, str] = {}
        self.posts: list[Post] = []
        self.git_dates: dict[str, datetime.datetime] = {}
        self.nav: Navigation | None = None
        self.files: Files | None = None
        self.language = 'en'
        self.authors: dict[str, dict[str, str]] = {}
        self.blog_index: str | None = None

    # -- configuration -------------------------------------------------------

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig:
        if config.theme.name != 'sumi':
            log.warning("The 'sumi' plugin is meant to be used with 'theme: sumi'.")
        self.language = self.config.language or str(config.theme.get('locale') or 'en')
        exts = config.markdown_extensions
        names = set(exts)
        for name in ('attr_list', 'admonition', 'footnotes', 'def_list', 'md_in_html', 'tables', 'toc'):
            if name not in names and f'markdown.extensions.{name}' not in names:
                exts.append(name)
        highlighters = {'pymdownx.highlight', 'pymdownx.superfences', 'codehilite', 'markdown.extensions.codehilite'}
        if not names & highlighters:
            exts.append('codehilite')
            config.mdx_configs.setdefault('codehilite', {}).update(
                {'css_class': 'highlight', 'guess_lang': False, 'pygments_lang_class': True})
        if 'fenced_code' not in names and 'pymdownx.superfences' not in names:
            exts.append('fenced_code')
        toc = config.mdx_configs.setdefault('toc', {})
        toc.setdefault('permalink', '#')
        if 'mkdocs_sumi.markdown.extension' not in exts:
            exts.append('mkdocs_sumi.markdown.extension')
        config.mdx_configs['mkdocs_sumi.markdown.extension'] = {
            'language': self.language, 'math': self.config.math, 'mermaid': self.config.mermaid}
        if self.config.git_dates:
            self.git_dates = _git_dates(config.docs_dir)
        self.authors = dict(self.config.blog.authors)
        return config

    def on_pre_build(self, *, config: MkDocsConfig) -> None:
        self.features.clear()
        self.contents.clear()
        self.posts.clear()
        self.blog_index = None

    # -- blog ------------------------------------------------------------------

    def _blog_dir(self) -> str:
        return self.config.blog.dir.strip('/')

    def _is_post(self, file: File) -> bool:
        d = self._blog_dir()
        return (self.config.blog.enabled and file.is_documentation_page()
                and file.src_uri.startswith(d + '/') and file.src_uri != f'{d}/index.md'
                and not posixpath.basename(file.src_uri).startswith(('index.', 'README.')))

    def on_files(self, files: Files, *, config: MkDocsConfig) -> Files:
        self.files = files
        if self.config.print.enabled:
            # A placeholder, so pages can link to the print edition; written in on_post_build.
            target = self.config.print.path.strip('/') + '/index.html'
            if files.get_file_from_path(target) is None:
                files.append(File.generated(config, target, content=''))
        if not self.config.blog.enabled or not any(self._is_post(f) for f in files):
            return files
        d = self._blog_dir()
        from mkdocs.structure.files import InclusionLevel

        for f in files:
            if self._is_post(f) and f.inclusion == InclusionLevel.INCLUDED:
                f.inclusion = InclusionLevel.NOT_IN_NAV
            if self._is_post(f):
                # posts/2026-11-01-hello.md -> blog/2026/11/01/hello/
                m = _POST_NAME_RE.match(posixpath.basename(f.src_uri))
                if m:
                    slug = posixpath.join(d, m['y'], m['m'], m['d'], m['slug'])
                    f.dest_uri = slug + ('/index.html' if config.use_directory_urls else '.html')
                    f.__dict__.pop('url', None)
                    f.__dict__.pop('abs_dest_path', None)
        authors_file = os.path.join(config.docs_dir, d, '.authors.yml')
        if os.path.isfile(authors_file):
            with open(authors_file, encoding='utf-8') as fh:
                data = yaml.safe_load(fh) or {}
            self.authors.update(data.get('authors', data))
        self.blog_index = f'{d}/index.md'
        if files.get_file_from_path(self.blog_index) is None:
            title = translator(self.language)('blog')
            files.append(File.generated(config, self.blog_index,
                                        content=f'---\ntemplate: blog.html\n---\n\n# {title}\n'))
        return files

    def on_nav(self, nav: Navigation, *, config: MkDocsConfig, files: Files) -> Navigation:
        self.nav = nav
        self._nav_json: str | None = None
        if self.blog_index and config.nav is None:
            # Keep posts out of the sidebar: the blog section shows its index only.
            def prune(items: list) -> list:
                out = []
                for item in items:
                    if isinstance(item, Section):
                        index = next((ch for ch in item.children if isinstance(ch, Page)
                                      and ch.file.src_uri == self.blog_index), None)
                        if index is not None:
                            index.parent = item.parent
                            out.append(index)
                            continue
                        item.children = prune(item.children)
                    out.append(item)
                return out

            nav.items = prune(nav.items)
            pages = _pages_in(nav.items)
            for i, page in enumerate(pages):
                page.previous_page = pages[i - 1] if i else None
                page.next_page = pages[i + 1] if i + 1 < len(pages) else None
        return nav

    def on_page_markdown(self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files) -> str:
        template = page.meta.get('template')
        if template in ('landing.html', 'blog.html'):
            page.meta.setdefault('layout', template[:-5])
        if self.blog_index and page.file.src_uri == self.blog_index:
            page.meta.setdefault('template', 'blog.html')
            page.meta.setdefault('layout', 'blog')
        elif self.blog_index and self._is_post(page.file):
            page.meta.setdefault('template', 'blog-post.html')
            date = _parse_date(page.meta.get('date')) or _file_date(page.file)
            meta_authors = page.meta.get('authors') or page.meta.get('author') or []
            if isinstance(meta_authors, str):
                meta_authors = [meta_authors]
            authors = []
            for a in meta_authors:
                info = self.authors.get(a, {'name': a}) if isinstance(a, str) else a
                authors.append({'id': a if isinstance(a, str) else info.get('name', ''), **info})
            tags = page.meta.get('tags') or page.meta.get('categories') or []
            if not page.meta.get('draft'):
                self.posts.append(Post(page=page, date=date, updated=_parse_date(page.meta.get('updated')),
                                       authors=authors, tags=[str(t) for t in tags],
                                       reading_time=reading_minutes(markdown)))
        page.meta.setdefault('reading_time', reading_minutes(markdown))
        return markdown

    # -- content ---------------------------------------------------------------

    @event_priority(50)
    def _on_page_content_early(self, html: str, *, page: Page, config: MkDocsConfig, files: Files) -> None:
        # Before `llms_txt` writes the page's Markdown copy.
        if page.meta.get('template') == 'landing.html' and page.markdown is not None:
            from mkdocs_sumi.landing import landing_markdown

            body = re.sub(r'^\s*#\s+[^\n]*\n', '', page.markdown, count=1) if getattr(page, 'content_title', None) else page.markdown
            page.markdown = landing_markdown(page.meta, body, getattr(page, 'content_title', None))

    def _on_page_content(self, html: str, *, page: Page, config: MkDocsConfig, files: Files) -> str:
        feats = set()
        if 'class="mermaid"' in html:
            feats.add('mermaid')
        if 'sumi-math' in html or 'class="arithmatex"' in html:
            feats.add('math')
        if 'sumi-tabs' in html or 'tabbed-set' in html:
            feats.add('tabs')
        self.features[page.file.src_uri] = feats
        self.contents[page.file.src_uri] = html
        for post in self.posts:
            if post.page is page:
                m = _MORE_RE.search(html)
                if m:
                    post.excerpt = html[: m.start()]
                else:
                    para = re.search(r'<p>.*?</p>', html, re.S)
                    post.excerpt = para.group(0) if para else ''
        if (self.config.markdown_copy and 'llms_txt' not in config.plugins
                and not page.file.inclusion.is_excluded() and page.markdown is not None):
            try:
                from mkdocs.contrib.llms_txt import markdown_path, page_markdown
            except ImportError:  # MkDocs NG before 1.9
                markdown_path, page_markdown = _markdown_path, _page_markdown

            utils.write_file(page_markdown(page).encode('utf-8'),
                             os.path.join(config.site_dir, markdown_path(page)))
        return html

    on_page_content = CombinedEvent(_on_page_content_early, _on_page_content)

    def _markdown_url(self, page: Page, config: MkDocsConfig) -> str | None:
        if 'llms_txt' not in config.plugins and not self.config.markdown_copy:
            return None
        if page.file.generated_by:
            return None
        return quote(posixpath.splitext(page.file.src_uri)[0] + '.md')

    def on_page_context(self, context: dict, *, page: Page, config: MkDocsConfig, nav: Navigation) -> dict:
        ctx: dict[str, Any] = {
            'features': sorted(self.features.get(page.file.src_uri, set())),
            'markdown_url': self._markdown_url(page, config),
            'llms_txt': 'llms_txt' in config.plugins,
            'assistant_links': self.config.assistant_links,
            'last_updated': self.git_dates.get(page.file.src_uri),
            'reading_time': page.meta.get('reading_time'),
            'print_url': self.config.print.path if self.config.print.enabled else None,
            'is_post': False,
        }
        if self.blog_index:
            posts = sorted(self.posts, key=lambda p: p.date, reverse=True)
            ctx['posts'] = posts
            index = self.files.get_file_from_path(self.blog_index) if self.files else None
            ctx['blog_index_url'] = index.url if index else None
            tags: dict[str, int] = {}
            for p in posts:
                for tag in p.tags:
                    tags[tag] = tags.get(tag, 0) + 1
            ctx['tags'] = sorted(tags.items(), key=lambda kv: (-kv[1], kv[0].lower()))
            for i, p in enumerate(posts):
                if p.page is page:
                    ctx['is_post'] = True
                    ctx['post'] = p
                    ctx['newer'] = posts[i - 1] if i > 0 else None
                    ctx['older'] = posts[i + 1] if i + 1 < len(posts) else None
            ctx['feed_url'] = f'{self._blog_dir()}/feed.xml' if self.config.blog.feed else None
        if page.meta.get('template') == 'releases.html':
            ctx['releases'] = self._releases(page, config)
        ctx['nav_json'] = Markup(self._nav_index())
        ctx['strings_json'] = Markup(self._strings())
        context['sumi'] = ctx
        return context

    def _nav_index(self) -> str:
        """Every page in the nav, with its section path, for the command palette."""
        if getattr(self, '_nav_json', None):
            return self._nav_json
        entries: list[dict[str, Any]] = []

        def walk(items: list, path: list[str]) -> None:
            for item in items:
                if isinstance(item, Section):
                    walk(item.children, [*path, item.title or ''])
                elif isinstance(item, Page):
                    entries.append({'t': item.title or item.file.name, 'u': item.url, 's': ' / '.join(path)})
                elif getattr(item, 'is_link', False):
                    entries.append({'t': item.title, 'u': item.url, 's': ' / '.join(path), 'x': 1})

        walk(self.nav.items if self.nav else [], [])
        if self.blog_index:
            for post in sorted(self.posts, key=lambda p: p.date, reverse=True):
                entries.append({'t': post.title, 'u': post.url, 's': translator(self.language)('blog')})
        self._nav_json = _json_html(entries)
        return self._nav_json

    def _strings(self) -> str:
        t = translator(self.language)
        return _json_html({k: t(k) for k in STRINGS['en']})

    @event_priority(-50)
    def on_env(self, env: Environment, *, config: MkDocsConfig, files: Files) -> Environment:
        self.files = files
        env.globals['icon'] = icon
        env.globals['t'] = translator(self.language)
        env.globals['sumi_language'] = self.language
        env.filters['sumi_date'] = _format_date
        env.filters['sumi_md'] = _inline_markdown
        env.filters['sumi_strip_tags'] = lambda s: Markup(_TAG_RE.sub('', str(s or ''))).unescape()
        env.filters['sumi_links'] = _site_links
        return env

    def _releases(self, page: Page, config: MkDocsConfig) -> list[dict[str, Any]]:
        data = page.meta.get('releases')
        if isinstance(data, str):
            path = os.path.normpath(os.path.join(config.docs_dir, data))
            if not os.path.isfile(path):
                raise PluginError(f"Releases file '{data}' referenced by '{page.file.src_uri}' does not exist.")
            with open(path, encoding='utf-8') as fh:
                data = yaml.safe_load(fh) or []
        import markdown as md_lib

        releases = []
        for n, rel in enumerate(data or []):
            rel = dict(rel)
            if rel.get('notes'):
                rel['notes_html'] = Markup(md_lib.markdown(str(rel['notes']), extensions=['fenced_code', 'tables']))
            rel['date'] = _parse_date(rel.get('date'))
            rel.setdefault('status', 'latest' if n == 0 else 'stable')
            releases.append(rel)
        return releases

    # -- outputs ---------------------------------------------------------------

    def on_post_build(self, *, config: MkDocsConfig) -> None:
        used = set().union(*self.features.values()) if self.features else set()
        vendor = resources.files('mkdocs_sumi').joinpath('vendor')
        dest = os.path.join(config.site_dir, 'assets', 'sumi', 'vendor')
        wanted = {'mermaid': 'mermaid', 'math': 'katex'}
        for feature, name in wanted.items():
            if feature in used:
                with resources.as_file(vendor.joinpath(name)) as src:
                    shutil.copytree(src, os.path.join(dest, name), dirs_exist_ok=True)
        if self.config.print.enabled and self.nav is not None:
            self._write_print(config)
        if self.blog_index and self.config.blog.feed and self.posts:
            self._write_feed(config)

    def _write_print(self, config: MkDocsConfig) -> None:
        from mkdocs.commands.build import get_context

        env = config.theme.get_env()
        self.on_env(env, config=config, files=self.files or Files([]))
        path = self.config.print.path.strip('/') + '/'
        sections = []
        for page in _pages_in(self.nav.items if self.nav else []):
            html = self.contents.get(page.file.src_uri)
            if html is None or page.meta.get('print') is False:
                continue
            if page.meta.get('template') in ('landing.html', 'blog.html') and not _strip_tags(html).strip():
                continue
            anchor = 'p-' + (re.sub(r'[^a-z0-9]+', '-', page.url.lower()).strip('-') or 'home')
            sections.append({'page': page, 'anchor': anchor,
                             'html': Markup(_rebase(html, page.url, path, anchor))})
        context = get_context(self.nav, self.files or Files([]), config,
                              base_url=utils.get_relative_url('.', path))
        context['sumi'] = {'features': sorted(set().union(*self.features.values())) if self.features else [],
                           'print_sections': sections, 'print_url': path, 'is_print': True}
        output = env.get_template('print.html').render(context)
        utils.write_file(output.encode('utf-8'), os.path.join(config.site_dir, path, 'index.html'))

    def _write_feed(self, config: MkDocsConfig) -> None:
        site = (config.site_url or '').rstrip('/') + '/'
        posts = sorted(self.posts, key=lambda p: p.date, reverse=True)[: self.config.blog.feed_items]
        updated = max(p.updated or p.date for p in posts)

        def esc(s: str) -> str:
            return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

        def iso(d: datetime.datetime) -> str:
            return (d if d.tzinfo else d.replace(tzinfo=datetime.timezone.utc)).isoformat()

        entries = []
        for p in posts:
            url = site + p.url
            authors = ''.join(f'<author><name>{esc(a.get("name", ""))}</name></author>' for a in p.authors)
            content = _rebase(p.excerpt, p.url, '', None, absolute=site)
            entries.append(
                f'<entry><title>{esc(p.title)}</title><link href="{esc(url)}"/><id>{esc(url)}</id>'
                f'<published>{iso(p.date)}</published><updated>{iso(p.updated or p.date)}</updated>{authors}'
                + ''.join(f'<category term="{esc(t)}"/>' for t in p.tags)
                + f'<summary type="html">{esc(content)}</summary></entry>')
        feed_url = site + self._blog_dir() + '/feed.xml'
        xml = ('<?xml version="1.0" encoding="utf-8"?>\n<feed xmlns="http://www.w3.org/2005/Atom">'
               f'<title>{esc(config.site_name)}</title><id>{esc(feed_url)}</id>'
               f'<link rel="self" href="{esc(feed_url)}"/><link href="{esc(site)}"/>'
               f'<updated>{iso(updated)}</updated>' + ''.join(entries) + '</feed>\n')
        utils.write_file(xml.encode('utf-8'), os.path.join(config.site_dir, self._blog_dir(), 'feed.xml'))


@pass_context
def _site_links(context: Any, html: Any) -> Markup:
    """Resolve relative `href`/`src` in site-wide HTML (e.g. the announcement) from the site root."""
    base = str(context.get('base_url') or '.').rstrip('/') + '/'

    def sub(m: re.Match[str]) -> str:
        url = m.group(2)
        if re.match(r'^(?:[a-z][a-z0-9+.-]*:|/|#)', url, re.I):
            return m.group(0)
        return f'{m.group(1)}{base}{url}{m.group(3)}'

    return Markup(re.sub(r'(\b(?:href|src)=")([^"]*)(")', sub, str(html or '')))


def _markdown_path(page: Page) -> str:
    return posixpath.splitext(page.file.src_uri)[0] + '.md'


def _page_markdown(page: Page) -> str:
    markdown = page.markdown or ''
    if getattr(page, 'content_title', None) is None and page.title and not re.match(r'\s*#\s', markdown):
        markdown = f'# {page.title}\n\n{markdown}'
    return markdown.strip() + '\n'


_POST_NAME_RE = re.compile(r'^(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})-(?P<slug>.+)\.md$')


def _strip_tags(html: str) -> str:
    return re.sub(r'<[^>]+>', '', html)


def _json_html(data: Any) -> str:
    """JSON that is safe inside a <script> element."""
    return (json.dumps(data, ensure_ascii=False, separators=(',', ':'))
            .replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026'))


def _pages_in(items: list) -> list[Page]:
    pages: list[Page] = []
    for item in items:
        if isinstance(item, Section):
            pages.extend(_pages_in(item.children))
        elif isinstance(item, Page):
            pages.append(item)
    return pages


def _rebase(html: str, page_url: str, target: str, anchor: str | None, absolute: str | None = None) -> str:
    """Rewrite relative URLs in `html`, written for `page_url`, so they work from `target`.

    With `anchor`, ids and same-page fragments are prefixed so several pages
    can share one document (the print edition).
    """
    page_dir = page_url if page_url.endswith('/') or not page_url else posixpath.dirname(page_url) + '/'

    def sub(m: re.Match[str]) -> str:
        url = m.group('url')
        parts = urlsplit(url)
        if parts.scheme or parts.netloc or url.startswith(('/', 'data:', 'mailto:')):
            return m.group(0)
        if url.startswith('#'):
            if anchor and m.group('attr').strip() == 'href':
                return f'{m.group("attr")}="#{anchor}--{url[1:]}"'
            return m.group(0)
        resolved = posixpath.normpath(posixpath.join(page_dir, parts.path)) if parts.path else page_dir.rstrip('/')
        if resolved == '.':
            resolved = ''
        if (parts.path.endswith('/') or not parts.path) and resolved:
            resolved += '/'
        if absolute is not None:
            new = absolute + resolved
        else:
            new = utils.get_relative_url(resolved or '.', target or '.')
            if resolved.endswith('/') and not new.endswith('/'):
                new += '/'
        if parts.query:
            new += '?' + parts.query
        if parts.fragment:
            new += '#' + parts.fragment
        return f'{m.group("attr")}="{new}"'

    html = _URL_ATTR_RE.sub(sub, html)
    if anchor:
        html = re.sub(r'\sid="([^"]+)"', lambda m: f' id="{anchor}--{m.group(1)}"', html)
    return html


def _git_dates(docs_dir: str) -> dict[str, datetime.datetime]:
    """Map each docs file (relative path) to its last commit date, in one `git log` call."""
    try:
        root = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=docs_dir, capture_output=True,
                              text=True, check=True).stdout.strip()
        out = subprocess.run(['git', 'log', '--format=@%cI', '--name-only', '--', '.'], cwd=docs_dir,
                             capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        log.info('sumi: git_dates is enabled but git history is unavailable.')
        return {}
    prefix = os.path.relpath(os.path.realpath(docs_dir), os.path.realpath(root)).replace(os.sep, '/')
    prefix = '' if prefix == '.' else prefix + '/'
    dates: dict[str, datetime.datetime] = {}
    current = None
    for line in out.splitlines():
        if line.startswith('@'):
            current = datetime.datetime.fromisoformat(line[1:])
        elif line and current is not None and line.startswith(prefix):
            dates.setdefault(line[len(prefix):], current)
    return dates


def _file_date(file: File) -> datetime.datetime:
    m = re.search(r'(\d{4})-(\d{2})-(\d{2})', file.src_uri)
    if m:
        return datetime.datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    if file.abs_src_path and os.path.exists(file.abs_src_path):
        return datetime.datetime.fromtimestamp(os.path.getmtime(file.abs_src_path))
    return datetime.datetime.now()


_MONTHS_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
              'October', 'November', 'December']


def _format_date(value: Any, language: str = 'en', short: bool = False) -> str:
    d = value if isinstance(value, datetime.datetime) else _parse_date(value)
    if d is None:
        return ''
    if language.startswith(('zh', 'ja')):
        return f'{d.year}年{d.month}月{d.day}日'
    month = _MONTHS_EN[d.month - 1]
    return f'{month[:3] if short else month} {d.day}, {d.year}'


def _inline_markdown(text: Any, block: bool = False) -> Markup:
    """Render a short Markdown string from front matter (hero text, feature blurbs)."""
    import markdown as md_lib

    html = md_lib.markdown(
        str(text or ''),
        extensions=['attr_list', 'tables', 'fenced_code', 'codehilite', 'mkdocs_sumi.markdown.extension'],
        extension_configs={'codehilite': {'css_class': 'highlight', 'guess_lang': False, 'pygments_lang_class': True}})
    if not block and html.startswith('<p>') and html.endswith('</p>') and html.count('<p>') == 1:
        html = html[3:-4]
    return Markup(html)
