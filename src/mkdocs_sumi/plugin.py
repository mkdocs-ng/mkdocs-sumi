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
from html import escape
from urllib.parse import quote, unquote, urlsplit

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

from mkdocs_sumi.i18n import STRINGS, format_date, is_rtl, og_locale, translator
from mkdocs_sumi.icons import has_icon, icon

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
    dir = c.Type((str, list), default='blog')
    feed = c.Type(bool, default=True)
    feed_items = c.Type(int, default=20)
    feed_path = c.Optional(c.Type(str))
    feed_format = c.Choice(['atom', 'rss'], default='atom')
    tags_dir = c.Optional(c.Type(str))
    authors = c.Type(dict, default={})
    layout = c.Choice(['list', 'cards'], default='list')


class _PrintConfig(base.Config):
    enabled = c.Type(bool, default=True)
    path = c.Type(str, default='print/')


class SumiConfig(base.Config):
    language = c.Optional(c.Type(str))
    math = c.Type(bool, default=True)
    mermaid = c.Type(bool, default=True)
    echarts = c.Type(bool, default=True)
    markmap = c.Type(bool, default=True)
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
    blog: str = ''
    series: list[str] = field(default_factory=list)

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
        self.blog_indexes: dict[str, str] = {}
        self.tag_pages: dict[str, str] = {}
        self.tags_index: str | None = None
        self.covers: dict[str, str] = {}
        self.aliases: list[tuple[str, Page]] = []

    # -- configuration -------------------------------------------------------

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig:
        if config.theme.name != 'sumi':
            log.warning("The 'sumi' plugin is meant to be used with 'theme: sumi'.")
        # `theme.language` is what Material calls it: honour it so a site that
        # switches themes keeps its interface language. On a multi-language
        # site MkDocs NG sets `locale` for each language, so that one wins.
        material = None if config.get('languages') else config.theme.get('language')
        self.language = str(self.config.language or material or config.theme.get('locale') or 'en')
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
            'language': self.language, 'math': self.config.math, 'mermaid': self.config.mermaid,
            'echarts': self.config.echarts, 'markmap': self.config.markmap}
        if self.config.git_dates:
            # On a multi-language site (MkDocs NG 1.11+), untranslated pages come
            # from the default language's docs_dir.
            languages = config.get('languages') or ()
            dirs = [config.docs_dir] + [lang.docs_dir for lang in languages if getattr(lang, 'docs_dir', None)]
            self.git_dates = _git_dates(list(dict.fromkeys(dirs)))
        self.authors = dict(self.config.blog.authors)
        return config

    def on_pre_build(self, *, config: MkDocsConfig) -> None:
        self.features.clear()
        self.contents.clear()
        self.posts.clear()
        self.blog_index = None
        self.blog_indexes = {}
        self.tag_pages = {}
        self.tags_index = None
        self.covers = {}
        self.aliases = []

    # -- blog ------------------------------------------------------------------

    def _blog_dirs(self) -> list[str]:
        dirs = self.config.blog.dir
        dirs = [dirs] if isinstance(dirs, str) else list(dirs)
        return [str(d).strip('/') for d in dirs if str(d).strip('/')]

    def _blog_dir(self) -> str:
        dirs = self._blog_dirs()
        return dirs[0] if dirs else 'blog'

    def _blog_of(self, file: File) -> str | None:
        """The blog folder `file` is a post of, or None.

        A post is any page under a blog folder except the folder's own
        `index.md`: `posts/2026-11-01-hello.md` as well as a page bundle,
        `posts/2026/hello/index.md` next to its images.
        """
        if not self.config.blog.enabled or not file.is_documentation_page():
            return None
        for d in self._blog_dirs():
            if file.src_uri.startswith(d + '/') and file.src_uri not in (f'{d}/index.md', f'{d}/README.md'):
                return d
        return None

    def _is_post(self, file: File) -> bool:
        return self._blog_of(file) is not None

    def on_files(self, files: Files, *, config: MkDocsConfig) -> Files:
        self.files = files
        if self.config.print.enabled:
            # A placeholder, so pages can link to the print edition; written in on_post_build.
            target = self.config.print.path.strip('/') + '/index.html'
            if files.get_file_from_path(target) is None:
                files.append(File.generated(config, target, content=''))
        posts = [f for f in files if self._is_post(f)]
        if not posts:
            return files
        from mkdocs.structure.files import InclusionLevel

        for f in posts:
            if f.inclusion == InclusionLevel.INCLUDED:
                f.inclusion = InclusionLevel.NOT_IN_NAV
            # posts/2026-11-01-hello.md -> blog/2026/11/01/hello/
            m = _POST_NAME_RE.match(posixpath.basename(f.src_uri))
            if m:
                slug = posixpath.join(self._blog_of(f), m['y'], m['m'], m['d'], m['slug'])
                f.dest_uri = slug + ('/index.html' if config.use_directory_urls else '.html')
                f.__dict__.pop('url', None)
                f.__dict__.pop('abs_dest_path', None)
            elif posixpath.basename(f.src_uri).startswith(('index.', 'README.')):
                # A page bundle: its cover is the `featured` or `cover` image next to it (Hugo's convention).
                folder = posixpath.dirname(f.src_uri)
                for name in _COVER_NAMES:
                    if files.get_file_from_path(f'{folder}/{name}') is not None:
                        self.covers[f.src_uri] = f'{folder}/{name}'
                        break
        for d in self._blog_dirs():
            authors_file = _source_path(files, config, posixpath.join(d, '.authors.yml'))
            if os.path.isfile(authors_file):
                with open(authors_file, encoding='utf-8') as fh:
                    data = yaml.safe_load(fh) or {}
                self.authors.update(data.get('authors', data))
        for d in dict.fromkeys(self._blog_of(f) for f in posts):
            index = f'{d}/index.md'
            self.blog_indexes[d] = index
            if files.get_file_from_path(index) is None:
                title = translator(self.language)('blog')
                files.append(File.generated(config, index, content=f'---\ntemplate: blog.html\n---\n\n# {title}\n'))
        self.blog_index = self.blog_indexes.get(self._blog_dir()) or next(iter(self.blog_indexes.values()))
        if self.config.blog.tags_dir:
            self._tag_files(files, config, posts)
        return files

    def _tag_files(self, files: Files, config: MkDocsConfig, posts: list[File]) -> None:
        """Generate a page for each tag, and an index of the tags, under `blog.tags_dir`."""
        from mkdocs.structure.files import InclusionLevel
        from mkdocs.utils.meta import get_data

        tags: dict[str, None] = {}
        for f in posts:
            try:
                meta = get_data(f.content_string)[1]
            except (OSError, UnicodeDecodeError):
                continue
            if not meta.get('draft'):
                for tag in _tag_list(meta.get('tags') or meta.get('categories')):
                    tags.setdefault(tag)
        root = self.config.blog.tags_dir.strip('/')
        self.tags_index = f'{root}/index.md'
        existing = files.get_file_from_path(self.tags_index)
        if existing is None:
            t = translator(self.language)
            files.append(File.generated(config, self.tags_index,
                                        content=f'---\ntemplate: blog-tags.html\n---\n\n# {t("tags")}\n'))
        slugs: dict[str, str] = {}
        for tag in sorted(tags, key=str.lower):
            slug = _slugify_tag(tag)
            if not slug or slugs.get(slug, tag) != tag:
                log.warning("Sumi: tag '%s' has the same URL as tag '%s'; it gets no page of its own.", tag, slugs[slug])
                continue
            slugs[slug] = tag
            uri = f'{root}/{slug}/index.md'
            if files.get_file_from_path(uri) is None:
                title = tag.replace('\\', '\\\\').replace('"', '\\"')
                f = File.generated(config, uri, content=f'---\ntemplate: blog.html\nblog_tag: "{title}"\n---\n\n# {tag}\n')
                f.inclusion = InclusionLevel.NOT_IN_NAV
                files.append(f)
            self.tag_pages[tag] = uri

    def on_nav(self, nav: Navigation, *, config: MkDocsConfig, files: Files) -> Navigation:
        self.nav = nav
        self._nav_json: str | None = None
        if self.blog_indexes and config.nav is None:
            indexes = set(self.blog_indexes.values())

            # Keep posts out of the sidebar: the blog section shows its index only.
            def prune(items: list) -> list:
                out = []
                for item in items:
                    if isinstance(item, Section):
                        index = next((ch for ch in item.children if isinstance(ch, Page)
                                      and ch.file.src_uri in indexes), None)
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
        self._files = files
        template = page.meta.get('template')
        if template in ('landing.html', 'blog.html'):
            page.meta.setdefault('layout', template[:-5])
        if template in ('blog-tags.html', 'blog-archive.html'):
            page.meta.setdefault('layout', 'blog')
        # Hugo's `summary` is the page description.
        if not page.meta.get('description') and isinstance(page.meta.get('summary'), str):
            page.meta['description'] = ' '.join(page.meta['summary'].split())
        if isinstance(page.meta.get('aliases'), (list, str)):
            aliases = page.meta['aliases']
            for alias in [aliases] if isinstance(aliases, str) else aliases:
                if isinstance(alias, str) and alias.strip('/'):
                    self.aliases.append((alias, page))
        blog = self._blog_of(page.file)
        if self.blog_indexes and page.file.src_uri in self.blog_indexes.values():
            page.meta.setdefault('template', 'blog.html')
            page.meta.setdefault('layout', 'blog')
        elif self.blog_indexes and blog is not None:
            page.meta.setdefault('template', 'blog-post.html')
            if not page.meta.get('image'):
                cover = page.meta.get('cover')
                if isinstance(cover, dict):  # Hugo themes write `cover: {image: …}`
                    cover = cover.get('image')
                if isinstance(cover, str) and cover:
                    page.meta['image'] = cover if '/' in cover or cover.startswith('http') else \
                        posixpath.join(posixpath.dirname(page.file.src_uri), cover)
                elif page.file.src_uri in self.covers:
                    page.meta['image'] = self.covers[page.file.src_uri]
            date = _parse_date(page.meta.get('date')) or _file_date(page.file)
            meta_authors = page.meta.get('authors') or page.meta.get('author') or []
            if isinstance(meta_authors, str):
                meta_authors = [meta_authors]
            authors = []
            for a in meta_authors:
                info = self.authors.get(a, {'name': a}) if isinstance(a, str) else a
                authors.append({'id': a if isinstance(a, str) else info.get('name', ''), **info})
            tags = _tag_list(page.meta.get('tags') or page.meta.get('categories'))
            if not page.meta.get('draft'):
                self.posts.append(Post(page=page, date=date, updated=_parse_date(page.meta.get('updated')),
                                       authors=authors, tags=tags,
                                       reading_time=reading_minutes(markdown), blog=blog,
                                       series=_tag_list(page.meta.get('series'))))
        page.meta.setdefault('reading_time', reading_minutes(markdown))
        return markdown

    # -- content ---------------------------------------------------------------

    @event_priority(50)
    def _on_page_content_early(self, html: str, *, page: Page, config: MkDocsConfig, files: Files) -> None:
        # Before `llms_txt` writes the page's Markdown copy.
        if page.meta.get('template') == 'landing.html' and page.markdown is not None:
            from mkdocs_sumi.landing import landing_markdown

            for key, kind in (('hero', dict), ('sections', list)):
                if page.meta.get(key) is not None and not isinstance(page.meta[key], kind):
                    raise PluginError(
                        f"Landing page '{page.file.src_uri}': '{key}' must be a "
                        f"{'mapping' if kind is dict else 'list'}, got: {page.meta[key]!r}")

            body = re.sub(r'^\s*#\s+[^\n]*\n', '', page.markdown, count=1) if getattr(page, 'content_title', None) else page.markdown
            page.markdown = landing_markdown(page.meta, body, getattr(page, 'content_title', None))

    def _on_page_content(self, html: str, *, page: Page, config: MkDocsConfig, files: Files) -> str:
        feats = set()
        if 'class="mermaid"' in html:
            feats.add('mermaid')
        if 'sumi-math' in html or 'class="arithmatex"' in html:
            feats.add('math')
        if 'class="sumi-chart"' in html:
            feats.add('echarts')
        if 'class="sumi-markmap"' in html:
            feats.add('markmap')
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

    def _landing_links(self, page: Page) -> None:
        """Point `link: guide.md` in landing front matter at the page built from it.

        Runs after the page's Markdown copy is written, so that copy keeps the
        `.md` links, which lead to the other Markdown copies.
        """
        files = getattr(self, '_files', None)
        if files is None or page.meta.get('template') != 'landing.html':
            return
        hero = page.meta.get('hero')
        groups = [hero.get('actions')] if isinstance(hero, dict) else []
        for s in page.meta.get('sections') or []:
            if isinstance(s, dict):
                groups += [s.get('actions'), s.get('items')]
        for group in groups:
            for item in group if isinstance(group, list) else []:
                if isinstance(item, dict) and isinstance(item.get('link'), str):
                    item['link'] = _doc_link(item['link'], page, files)
        # Markdown links inside text fields (`[Guide](guide.md)`) are rendered
        # without MkDocs' link resolution, so resolve them here as well.
        for key in ('hero', 'sections'):
            if key in page.meta:
                page.meta[key] = _text_links(page.meta[key], page, files)

    def on_page_context(self, context: dict, *, page: Page, config: MkDocsConfig, nav: Navigation) -> dict:
        self._landing_links(page)
        ctx: dict[str, Any] = {
            'features': sorted(self.features.get(page.file.src_uri, set())),
            'markdown_url': self._markdown_url(page, config),
            'llms_txt': 'llms_txt' in config.plugins,
            'assistant_links': self.config.assistant_links,
            'last_updated': self.git_dates.get(os.path.normcase(os.path.realpath(page.file.abs_src_path)))
            if page.file.abs_src_path else None,
            'reading_time': page.meta.get('reading_time'),
            'print_url': self.config.print.path if self.config.print.enabled else None,
            'is_post': False,
        }
        if self.blog_index:
            ctx.update(self._blog_context(page))
        if page.meta.get('template') == 'releases.html':
            ctx['releases'] = self._releases(page, config)
        ctx['translations'] = self._translations(page, config, context.get('i18n'))
        ctx['feedback'] = self._feedback(page, config)
        ctx['comments'] = self._comments(page, config)
        ctx['nav_json'] = Markup(self._nav_index())
        ctx['strings_json'] = Markup(self._strings())
        context['sumi'] = ctx
        return context

    def _url_of(self, src_uri: str | None) -> str | None:
        f = self.files.get_file_from_path(src_uri) if self.files and src_uri else None
        return f.url if f else None

    def _blog_context(self, page: Page) -> dict[str, Any]:
        """The posts a page lists, and where it sits among them."""
        ctx: dict[str, Any] = {}
        all_posts = sorted(self.posts, key=lambda p: p.date, reverse=True)
        current = next((p for p in all_posts if p.page is page), None)
        blog = current.blog if current else next(
            (d for d, uri in self.blog_indexes.items() if uri == page.file.src_uri), None)
        tag = page.meta.get('blog_tag')
        if tag is not None:
            posts = [p for p in all_posts if str(tag) in p.tags]
        elif blog is not None:
            posts = [p for p in all_posts if p.blog == blog]
        else:
            posts = all_posts
        ctx['posts'] = posts
        ctx['all_posts'] = all_posts
        ctx['blog_tag'] = str(tag) if tag is not None else None
        ctx['blog_index_url'] = self._url_of(self.blog_indexes.get(blog or '') or self.blog_index)
        tag_urls = {t: self._url_of(uri) for t, uri in self.tag_pages.items()}
        ctx['tag_urls'] = {t: u for t, u in tag_urls.items() if u}
        ctx['tags_url'] = self._url_of(self.tags_index)
        counts: dict[str, int] = {}
        for p in posts if tag is None else all_posts:
            for t in p.tags:
                counts[t] = counts.get(t, 0) + 1
        ctx['tags'] = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0].lower()))
        years: dict[int, list[Post]] = {}
        for p in posts:
            years.setdefault(p.date.year, []).append(p)
        ctx['years'] = list(years.items())
        if current is not None:
            siblings = [p for p in all_posts if p.blog == current.blog]
            i = siblings.index(current)
            ctx['is_post'] = True
            ctx['post'] = current
            ctx['newer'] = siblings[i - 1] if i > 0 else None
            ctx['older'] = siblings[i + 1] if i + 1 < len(siblings) else None
            ctx['series'] = []
            for name in current.series:
                members = [p for p in all_posts if name in p.series]
                members.sort(key=lambda p: (_series_order(p), p.date))
                ctx['series'].append({'name': name, 'posts': members})
        if self.config.blog.feed:
            ctx['feed_url'] = self._feed_path()
            ctx['feed_type'] = 'application/rss+xml' if self.config.blog.feed_format == 'rss' else 'application/atom+xml'
        ctx['blog_layout'] = page.meta.get('blog_layout') or self.config.blog.layout
        return ctx

    def _feed_path(self) -> str:
        return (self.config.blog.feed_path or f'{self._blog_dir()}/feed.xml').lstrip('/')

    def _feedback(self, page: Page, config: MkDocsConfig) -> dict[str, Any] | None:
        """The "Was this page helpful?" widget: Material's `extra.analytics.feedback`, or `theme.feedback`."""
        analytics = (config.extra or {}).get('analytics') or {}
        conf = analytics.get('feedback') if isinstance(analytics, dict) else None
        if conf is None:
            conf = config.theme.get('feedback')
        if not conf or _hidden(page, config, 'feedback') or page.meta.get('template') in _LIST_TEMPLATES:
            return None
        conf = conf if isinstance(conf, dict) else {}
        t = translator(self.language)
        ratings = conf.get('ratings') or [
            {'icon': 'thumbs-up', 'name': t('feedback_yes'), 'data': 1, 'note': t('feedback_thanks')},
            {'icon': 'thumbs-down', 'name': t('feedback_no'), 'data': 0, 'note': t('feedback_thanks')},
        ]
        out = []
        for i, r in enumerate(ratings):
            if not isinstance(r, dict):
                continue
            out.append({'icon': _feedback_icon(str(r.get('icon') or ''), i), 'name': str(r.get('name') or ''),
                        'data': r.get('data', 1 - i), 'note': str(r.get('note') or t('feedback_thanks'))})
        return {'title': str(conf.get('title') or t('feedback_title')), 'ratings': out}

    def _comments(self, page: Page, config: MkDocsConfig) -> dict[str, Any] | None:
        """Giscus comments under the page, from `theme.comments`."""
        conf = config.theme.get('comments')
        if not isinstance(conf, dict) or not conf.get('repo'):
            return None
        wanted = page.meta.get('comments')
        if wanted is False or _hidden(page, config, 'comments') or page.meta.get('template') in _LIST_TEMPLATES:
            return None
        if conf.get('opt_in') and wanted is not True:
            return None
        term = page.meta.get('comments_term')
        return {
            'term': str(term) if term is not None else '',
            'repo': conf['repo'], 'repo_id': conf.get('repo_id', ''), 'category': conf.get('category', ''),
            'category_id': conf.get('category_id', ''), 'mapping': conf.get('mapping', 'pathname'),
            'strict': '1' if conf.get('strict') else '0', 'reactions': '0' if conf.get('reactions') is False else '1',
            'input_position': conf.get('input_position', 'bottom'),
            'lang': conf.get('lang') or _giscus_lang(self.language),
            'theme_light': conf.get('theme_light', 'light'), 'theme_dark': conf.get('theme_dark', 'dark'),
        }

    def _translations(self, page: Page, config: MkDocsConfig, i18n: dict | None) -> list[dict[str, str]]:
        """The other languages that have their own version of this page, for the bilingual view."""
        if not i18n or i18n.get('fallback') or config.theme.get('bilingual_view') is False:
            return []
        out = []
        for lang in i18n.get('languages') or []:
            if lang.get('current') or not lang.get('available'):
                continue
            if page.file.src_uri in self._translated_pages(config, lang['code']):
                out.append({'lang': lang['code'], 'name': lang['name'], 'link': lang['link']})
        return out

    def _translated_pages(self, config: MkDocsConfig, code: str) -> set[str]:
        """The pages a language has its own source for, not borrowed from the default language."""
        cache = self.__dict__.setdefault('_translated_cache', {})
        if code in cache:
            return cache[code]
        pages: set[str] = set()
        try:
            from mkdocs import languages as ng_languages

            skipped = ng_languages.docs_dirs(config)

            def walk(src_dir: str):
                for source_dir, dirnames, filenames in os.walk(src_dir, followlinks=True):
                    dirnames[:] = sorted(d for d in dirnames
                                         if os.path.abspath(os.path.join(source_dir, d)) not in skipped)
                    for name in filenames:
                        yield os.path.relpath(os.path.join(source_dir, name), src_dir).replace(os.sep, '/')

            for lang in config.get('languages') or []:
                if lang.code == code:
                    for source in ng_languages.select_sources(config, lang, walk):
                        if not source.is_fallback and utils.is_markdown_file(source.src_uri):
                            pages.add(source.src_uri)
        except (ImportError, AttributeError):  # MkDocs NG before 1.11
            pass
        cache[code] = pages
        return pages

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
        self._install(env)
        # Some plugins (print-site, for one) render the theme's templates with
        # a fresh `theme.get_env()` after the build: give that env Sumi's
        # helpers too, or base.html fails on `t` and `icon`.
        theme = config.theme
        if not getattr(theme, '_sumi_env_patched', False):
            get_env = theme.get_env

            def sumi_get_env() -> Environment:
                return self._install(get_env())

            theme.get_env = sumi_get_env  # type: ignore[method-assign]
            theme._sumi_env_patched = True  # type: ignore[attr-defined]
        return env

    def _install(self, env: Environment) -> Environment:
        env.globals['icon'] = icon
        env.globals['t'] = translator(self.language)
        env.globals['sumi_language'] = self.language
        env.globals['sumi_dir'] = 'rtl' if is_rtl(self.language) else 'ltr'
        env.globals['sumi_og_locale'] = og_locale(self.language)
        env.filters['sumi_date'] = _format_date
        env.filters['sumi_md'] = _inline_markdown
        env.filters['sumi_strip_tags'] = lambda s: Markup(_TAG_RE.sub('', str(s or ''))).unescape()
        env.filters['sumi_links'] = _site_links
        return env

    def _releases(self, page: Page, config: MkDocsConfig) -> list[dict[str, Any]]:
        from mkdocs_sumi import releases as sources

        data = page.meta.get('releases')
        remote: dict[str, Any] = {}
        if isinstance(data, dict):
            unknown = set(data) - {'file', 'github', 'pypi'}
            if unknown:
                raise PluginError(f"Unknown 'releases' keys in '{page.file.src_uri}': {', '.join(sorted(unknown))}. "
                                  "Use 'file', 'github' or 'pypi'.")
            remote, data = data, data.get('file')
        if isinstance(data, str):
            path = _source_path(self.files, config, data)
            if not os.path.isfile(path):
                raise PluginError(f"Releases file '{data}' referenced by '{page.file.src_uri}' does not exist.")
            with open(path, encoding='utf-8') as fh:
                data = yaml.safe_load(fh) or []
        import markdown as md_lib

        releases = []
        if data is not None and not isinstance(data, list):
            raise PluginError(f"Releases of '{page.file.src_uri}' must be a list, got: {data!r}")
        for n, rel in enumerate(data or []):
            if not isinstance(rel, dict):
                raise PluginError(f"Release {n + 1} of '{page.file.src_uri}' must be a mapping, got: {rel!r}")
        data = list(data or [])
        if remote.get('github'):
            data = sources.merge(sources.github_releases(str(remote['github'])), data)
        if remote.get('pypi'):
            files = sources.pypi_assets(str(remote['pypi']))
            data = [rel if rel.get('assets') or str(rel.get('version')) not in files
                    else {**rel, 'assets': files[str(rel.get('version'))]} for rel in data]
        for n, rel in enumerate(data):
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
        wanted = {'mermaid': 'mermaid', 'math': 'katex', 'echarts': 'echarts', 'markmap': 'markmap'}
        for feature, name in wanted.items():
            if feature in used:
                with resources.as_file(vendor.joinpath(name)) as src:
                    shutil.copytree(src, os.path.join(dest, name), dirs_exist_ok=True)
        if self.config.print.enabled and self.nav is not None:
            self._write_print(config)
        if self.blog_index and self.config.blog.feed and self.posts:
            self._write_feed(config)
        if self.aliases:
            self._write_aliases(config)

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
        posts = sorted(self.posts, key=lambda p: p.date, reverse=True)
        if self.config.blog.feed_items > 0:
            posts = posts[: self.config.blog.feed_items]
        updated = max(p.updated or p.date for p in posts)
        feed_url = site + self._feed_path()

        def esc(s: str) -> str:
            return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

        def iso(d: datetime.datetime) -> str:
            return (d if d.tzinfo else d.replace(tzinfo=datetime.timezone.utc)).isoformat()

        def rfc822(d: datetime.datetime) -> str:
            from email.utils import format_datetime

            return format_datetime(d if d.tzinfo else d.replace(tzinfo=datetime.timezone.utc))

        def summary(p: Post) -> str:
            if p.page.meta.get('description'):
                return str(p.page.meta['description'])
            return _rebase(p.excerpt, p.url, '', None, absolute=site)

        def cover(p: Post) -> str | None:
            image = p.page.meta.get('image')
            if not isinstance(image, str) or not image:
                return None
            return image if image.startswith(('http://', 'https://')) else site + image.lstrip('/')

        if self.config.blog.feed_format == 'rss':
            items = []
            for p in posts:
                url = site + p.url
                image = cover(p)
                items.append(
                    f'<item><title>{esc(p.title)}</title><link>{esc(url)}</link>'
                    f'<pubDate>{rfc822(p.date)}</pubDate><guid>{esc(url)}</guid>'
                    + ''.join(f'<category>{esc(t)}</category>' for t in p.tags)
                    + f'<description>{esc(summary(p))}</description>'
                    + (f'<media:content url="{esc(image)}" medium="image"/>' if image else '')
                    + '</item>')
            xml = ('<?xml version="1.0" encoding="utf-8"?>\n<rss version="2.0" '
                   'xmlns:atom="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/"><channel>'
                   f'<title>{esc(config.site_name)}</title><link>{esc(site)}</link>'
                   f'<description>{esc(config.site_description or config.site_name)}</description>'
                   f'<language>{esc(self.language.replace("_", "-").lower())}</language>'
                   f'<lastBuildDate>{rfc822(updated)}</lastBuildDate>'
                   f'<atom:link href="{esc(feed_url)}" rel="self" type="application/rss+xml"/>'
                   + ''.join(items) + '</channel></rss>\n')
        else:
            entries = []
            for p in posts:
                url = site + p.url
                authors = ''.join(f'<author><name>{esc(a.get("name", ""))}</name></author>' for a in p.authors)
                entries.append(
                    f'<entry><title>{esc(p.title)}</title><link href="{esc(url)}"/><id>{esc(url)}</id>'
                    f'<published>{iso(p.date)}</published><updated>{iso(p.updated or p.date)}</updated>{authors}'
                    + ''.join(f'<category term="{esc(t)}"/>' for t in p.tags)
                    + f'<summary type="html">{esc(_rebase(p.excerpt, p.url, "", None, absolute=site))}</summary></entry>')
            xml = ('<?xml version="1.0" encoding="utf-8"?>\n<feed xmlns="http://www.w3.org/2005/Atom">'
                   f'<title>{esc(config.site_name)}</title><id>{esc(feed_url)}</id>'
                   f'<link rel="self" href="{esc(feed_url)}"/><link href="{esc(site)}"/>'
                   f'<updated>{iso(updated)}</updated>' + ''.join(entries) + '</feed>\n')
        utils.write_file(xml.encode('utf-8'), os.path.join(config.site_dir, *self._feed_path().split('/')))

    def _write_aliases(self, config: MkDocsConfig) -> None:
        """A redirect page at each of a page's old addresses (front matter `aliases`).

        `old/path/` is from the root of the page's language, `/old/path/` from
        the root of the whole site. A redirect never replaces a page, and on a
        multi-language site the default language's redirects win.
        """
        lang_path, is_default = '', True
        try:
            from mkdocs import languages

            lang = languages.current(config)
            if lang is not None:
                lang_path, is_default = lang.path, lang.default
        except ImportError:  # MkDocs NG before 1.11
            pass
        root = config.site_dir
        if lang_path:
            root = os.path.normpath(os.path.join(config.site_dir, *(['..'] * len(lang_path.split('/')))))
        for alias, page in self.aliases:
            path = alias if alias.startswith('/') else posixpath.join(lang_path, alias)
            path = posixpath.normpath('/' + unquote(path.split('#')[0].split('?')[0])).lstrip('/')
            if not path or path.startswith('..'):
                continue
            file = path if path.endswith(('.html', '.htm')) else posixpath.join(path, 'index.html')
            dest = os.path.join(root, *file.split('/'))
            target = posixpath.join(lang_path, page.url) if lang_path else page.url
            if posixpath.normpath(target or '.') == posixpath.normpath(posixpath.dirname(file) or '.'):
                continue  # the page itself
            if os.path.exists(dest):
                with open(dest, encoding='utf-8', errors='replace') as fh:
                    is_redirect = _REDIRECT_MARK in fh.read(600)
                if not is_redirect or not is_default:
                    continue
            href = posixpath.relpath(target or '.', posixpath.dirname(file) or '.')
            if target.endswith('/') or not target:
                href = href.rstrip('/') + '/'
            canonical = page.canonical_url or href
            html = ('<!doctype html><html><head><meta charset="utf-8">' + _REDIRECT_MARK
                    + f'<title>{escape(page.title or "")}</title><link rel="canonical" href="{escape(canonical)}">'
                    + '<meta name="robots" content="noindex">'
                    + f'<meta http-equiv="refresh" content="0; url={escape(href)}"></head>'
                    + f'<body><a href="{escape(href)}">{escape(page.title or href)}</a></body></html>\n')
            utils.write_file(html.encode('utf-8'), dest)


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


_COVER_NAMES = ('featured.jpg', 'featured.jpeg', 'featured.png', 'featured.webp', 'featured.svg',
                'cover.jpg', 'cover.jpeg', 'cover.png', 'cover.webp', 'cover.svg')
_LIST_TEMPLATES = ('landing.html', 'blog.html', 'blog-tags.html', 'blog-archive.html')
_REDIRECT_MARK = '<meta name="generator" content="sumi-redirect">'


def _slugify_tag(tag: str) -> str:
    """A tag's URL path, as Hugo makes it: `Open Source` -> `open-source`, `CI/CD` -> `ci/cd`."""
    slug = re.sub(r'\s+', '-', tag.strip().lower())
    slug = re.sub(r'[^\w/.+#-]', '', slug)
    slug = '/'.join(part for part in slug.split('/') if part not in ('', '.', '..'))
    return slug


def _series_order(post: Post) -> float:
    try:
        return float(post.page.meta.get('series_order'))
    except (TypeError, ValueError):
        return float('inf')


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


def _doc_link(link: str, page: Page, files: Files) -> str:
    """Turn a link to a Markdown source file into the URL of its page.

    Like a Markdown link, the path is relative to the page; a path from the
    docs root works too. Other links are returned unchanged.
    """
    parts = urlsplit(link)
    if parts.scheme or parts.netloc or link.startswith('/') or not utils.is_markdown_file(parts.path):
        return link
    path = unquote(parts.path)
    for candidate in (posixpath.join(posixpath.dirname(page.file.src_uri), path), path):
        target = files.get_file_from_path(posixpath.normpath(candidate))
        if target is not None and target.is_documentation_page():
            return target.url + (f'?{parts.query}' if parts.query else '') + (f'#{parts.fragment}' if parts.fragment else '')
    log.warning("Doc file '%s' links to '%s' in its front matter, but the target is not found "
                'among documentation files.', page.file.src_uri, link)
    return link


_MD_LINK_RE = re.compile(r'(\]\()(<[^>\n]+>|[^)\s]+)')


def _text_links(value: Any, page: Page, files: Files, key: str | None = None) -> Any:
    """Resolve `.md` targets of Markdown links in landing front-matter text.

    `link` fields are handled by `_doc_link` itself and `code` blocks are left
    alone. A resolved target is made relative to the page, as MkDocs does.
    """
    if key in ('link', 'code', 'icon', 'image'):
        return value
    if isinstance(value, dict):
        return {k: _text_links(v, page, files, k) for k, v in value.items()}
    if isinstance(value, list):
        return [_text_links(v, page, files, key) for v in value]
    if not isinstance(value, str) or '](' not in value:
        return value

    def sub(m: re.Match[str]) -> str:
        target = m.group(2)
        bare = target[1:-1] if target.startswith('<') else target
        resolved = _doc_link(bare, page, files)
        if resolved == bare:
            return m.group(0)
        return m.group(1) + utils.get_relative_url(resolved, page.url)

    return _MD_LINK_RE.sub(sub, value)


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


def _source_path(files: Files | None, config: MkDocsConfig, rel: str) -> str:
    """The file at `rel` in the docs, wherever it really is (a language's own or the default one)."""
    file = files.get_file_from_path(rel) if files is not None else None
    if file is not None and file.abs_src_path:
        return file.abs_src_path
    return os.path.normpath(os.path.join(config.docs_dir, rel))


def _git_dates(docs_dirs: list[str]) -> dict[str, datetime.datetime]:
    """Map each docs file (absolute, real path) to its last commit date, in one `git log` call."""
    try:
        root = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=docs_dirs[0], capture_output=True,
                              text=True, check=True).stdout.strip()
        out = subprocess.run(['git', 'log', '--format=@%cI', '--name-only', '--', *docs_dirs], cwd=root,
                             capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        log.info('sumi: git_dates is enabled but git history is unavailable.')
        return {}
    root = os.path.realpath(root)
    dates: dict[str, datetime.datetime] = {}
    current = None
    for line in out.splitlines():
        if line.startswith('@'):
            stamp = line[1:]
            if stamp.endswith('Z'):  # newer Git writes UTC as "Z", which Python 3.10 can't parse
                stamp = stamp[:-1] + '+00:00'
            current = datetime.datetime.fromisoformat(stamp)
        elif line and current is not None:
            dates.setdefault(os.path.normcase(os.path.join(root, line)), current)
    return dates


def _tag_list(tags: Any) -> list[str]:
    """Front matter tags as a list: `tags: release` is one tag, not seven."""
    if tags is None:
        return []
    if not isinstance(tags, (list, tuple)):
        tags = [tags]
    return [str(t) for t in tags if t is not None and str(t).strip()]


def _file_date(file: File) -> datetime.datetime:
    m = re.search(r'(\d{4})-(\d{2})-(\d{2})', file.src_uri)
    if m:
        try:
            return datetime.datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            log.warning(f"Sumi: '{file.src_uri}' has an invalid date in its name: {m.group(0)}.")
    if file.abs_src_path and os.path.exists(file.abs_src_path):
        return datetime.datetime.fromtimestamp(os.path.getmtime(file.abs_src_path))
    return datetime.datetime.now()



def _hidden(page: Page, config: MkDocsConfig, part: str) -> bool:
    """Whether `hide:` in the page's front matter or in the theme options lists `part`."""
    for hide in (page.meta.get('hide'), config.theme.get('hide')):
        if isinstance(hide, list) and part in hide:
            return True
    return False


def _feedback_icon(name: str, index: int) -> str:
    """A Lucide icon for a feedback rating, also for Material's `material/emoticon-happy-outline` and the like."""
    name = name.rsplit('/', 1)[-1]
    if any(k in name for k in ('happy', 'thumb-up', 'thumbs-up', 'heart', 'smile')):
        return 'thumbs-up'
    if any(k in name for k in ('sad', 'thumb-down', 'thumbs-down', 'frown', 'neutral')):
        return 'thumbs-down'
    if name and has_icon(name):
        return name
    return 'thumbs-up' if index == 0 else 'thumbs-down'


def _giscus_lang(language: str) -> str:
    norm = language.replace('_', '-')
    if norm.lower() in ('zh-tw', 'zh-hk', 'zh-hant'):
        return 'zh-TW'
    base = norm.split('-')[0].lower()
    return {'zh': 'zh-CN', 'pt': 'pt'}.get(base, base)


def _format_date(value: Any, language: str = 'en', short: bool = False) -> str:
    d = value if isinstance(value, datetime.datetime) else _parse_date(value)
    if d is None:
        return ''
    return format_date(d.year, d.month, d.day, language, short)


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
