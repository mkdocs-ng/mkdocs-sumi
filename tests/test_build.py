"""Build small sites with the theme and plugin and check the outputs."""

from __future__ import annotations

import os
import re
import textwrap
from pathlib import Path

import jinja2
import pytest
from mkdocs.commands import build
from mkdocs.config import load_config
from mkdocs.exceptions import Abort

ROOT = Path(__file__).resolve().parent.parent

try:
    import mkdocs.contrib.llms_txt  # noqa: F401

    HAS_LLMS_TXT = True
except ImportError:  # MkDocs NG before 1.9
    HAS_LLMS_TXT = False
needs_llms_txt = pytest.mark.skipif(not HAS_LLMS_TXT, reason='needs the llms_txt plugin of MkDocs NG 1.9')


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


def test_social_meta(site):
    html = (site / 'guide' / 'index.html').read_text()
    assert '<meta property="og:type" content="article">' in html
    assert '<meta property="og:locale" content="en_US">' in html
    assert '<meta name="twitter:card" content="summary">' in html
    home = (site / 'index.html').read_text()
    assert '<meta property="og:type" content="website">' in home


def test_landing_page(site):
    html = (site / 'index.html').read_text()
    assert 'sumi-hero' in html and 'Hello<br>world' in html
    assert 'sumi-feature' in html
    md = (site / 'index.md').read_text()
    assert '**Hello world**' in md
    assert '> A test site.' in md
    assert '[**Fast**](guide/): Very fast.' in md


def test_landing_links_to_markdown_files(tmp_path, caplog):
    """`link: page.md` in front matter leads to the built page, as in Markdown."""
    site = _site(tmp_path, {
        'index.md': """
            ---
            template: landing.html
            hero:
              actions:
                - {text: Start, link: getting-started.md, primary: true}
                - {text: Guide, link: guide/README.md}
                - {text: GitHub, link: "https://github.com/x/y"}
            sections:
              - type: features
                items:
                  - {title: Config, text: x, link: "guide/config.md#llmstxt"}
                  - {title: Old style, text: x, link: guide/}
                  - {title: Missing, text: x, link: nope.md}
              - type: cta
                actions:
                  - {text: Start, link: getting-started.md}
            ---
            """,
        'getting-started.md': '# Start\n',
        'guide/README.md': '# Guide\n',
        'guide/config.md': '# Config\n',
        'guide/landing.md': """
            ---
            template: landing.html
            hero:
              actions:
                - {text: Relative, link: config.md}
                - {text: From the root, link: getting-started.md}
            ---
            """,
    }, BASIC)
    html = (site / 'index.html').read_text()
    assert 'href="getting-started/"' in html
    assert 'href="guide/"' in html
    assert 'href="guide/config/#llmstxt"' in html
    assert 'href="https://github.com/x/y"' in html
    assert re.findall(r'href="([^"]*\.md[^"]*)"', html.split('<main', 1)[1]) == ['nope.md']
    assert "links to 'nope.md' in its front matter" in caplog.text
    sub = (site / 'guide' / 'landing' / 'index.html').read_text()
    assert 'href="../config/"' in sub
    assert 'href="../../getting-started/"' in sub
    if HAS_LLMS_TXT:
        # The Markdown copy keeps links to the other Markdown copies.
        assert '[Start](getting-started.md)' in (site / 'index.md').read_text()


def test_landing_text_links_to_markdown_files(tmp_path):
    """`[x](page.md)` inside front-matter text leads to the built page too."""
    site = _site(tmp_path, {
        'index.md': """
            ---
            template: landing.html
            hero:
              text: "Read [the guide](guide/README.md) first."
            sections:
              - type: features
                text: "[All settings](guide/config.md#llmstxt)"
                items:
                  - title: Start
                    text: >-
                      [Begin](getting-started.md)<br>
                      [Site](https://example.com/a.md) · [Here](#top)
              - type: faq
                items:
                  - {q: Where?, a: "See [config](<guide/config.md>)."}
              - type: split
                code: {lang: md, content: "[keep](getting-started.md)"}
            ---
            """,
        'getting-started.md': '# Start\n',
        'guide/README.md': '# Guide\n',
        'guide/config.md': '# Config\n',
        'guide/landing.md': """
            ---
            template: landing.html
            hero:
              text: "[Config](config.md) and [start](getting-started.md)"
            ---
            """,
    }, BASIC)
    html = (site / 'index.html').read_text()
    main = html.split('<main', 1)[1]
    assert 'href="guide/"' in main
    assert 'href="guide/config/#llmstxt"' in main
    assert 'href="getting-started/"' in main
    assert 'href="https://example.com/a.md"' in main
    assert 'href="#top"' in main
    assert 'keep' in main and 'getting-started.md' in main  # code is left alone
    assert re.findall(r'href="([^"]*\.md[^"]*)"', main) == ['https://example.com/a.md']
    if HAS_LLMS_TXT:
        # The Markdown copy keeps .md links.
        assert '](guide/README.md)' in (site / 'index.md').read_text()
    sub = (site / 'guide' / 'landing' / 'index.html').read_text()
    assert 'href="../config/"' in sub
    assert 'href="../../getting-started/"' in sub


def test_blog(site):
    post = site / 'blog' / '2026' / '01' / '02' / 'hello' / 'index.html'
    assert post.is_file()
    index = (site / 'blog' / 'index.html').read_text()
    assert 'Hello' in index and 'data-tags="news"' in index and 'Excerpt.' in index
    assert 'data-view="list"' in index
    assert 'sumi-post-cover--blank' in index and '<span>news</span>' in index
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


def _supports_languages() -> bool:
    from mkdocs.config.defaults import MkDocsConfig

    return any(name == 'languages' for name, _ in MkDocsConfig._schema)


@needs_llms_txt
@pytest.mark.skipif(not _supports_languages(), reason='the docs site needs MkDocs NG 1.11 (`languages`)')
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
    dates = plugin._git_dates([str(tmp_path / 'docs')])
    key = lambda name: os.path.normcase(os.path.join(os.path.realpath(tmp_path), 'docs', name))  # noqa: E731
    assert dates[key('a.md')] == datetime.datetime(2026, 11, 1, 12, 2, 53, tzinfo=datetime.timezone.utc)
    assert dates[key('b.md')].utcoffset() == datetime.timedelta(hours=2)


def test_logo_dark(tmp_path):
    """`logo_dark` adds a second header logo shown only in the dark palette."""
    config = BASIC.replace('      name: sumi\n', '      name: sumi\n      logo: img/logo.svg\n      logo_dark: img/logo-dark.svg\n')
    out = _site(tmp_path, {
        'index.md': '# Home\n',
        'img/logo.svg': '<svg xmlns="http://www.w3.org/2000/svg"/>',
        'img/logo-dark.svg': '<svg xmlns="http://www.w3.org/2000/svg"/>',
    }, config)
    html = (out / 'index.html').read_text(encoding='utf-8')
    assert '<img class="sumi-logo sumi-when-light" src="img/logo.svg"' in html
    assert '<img class="sumi-logo sumi-when-dark" src="img/logo-dark.svg"' in html


def test_material_variables_are_mapped():
    """Plugin CSS written for Material reads --md-* variables; Sumi defines the common ones."""
    css = (ROOT / 'src/mkdocs_sumi/theme/assets/css/sumi.css').read_text(encoding='utf-8')
    for name in ('--md-primary-fg-color', '--md-accent-fg-color', '--md-default-fg-color--lighter',
                 '--md-default-bg-color', '--md-code-bg-color', '--md-typeset-a-color', '--md-code-font-family'):
        assert re.search(rf'^\s*{name}:', css, re.M), name


def test_mkdocstrings_page(tmp_path):
    """An API page built by mkdocstrings gets Sumi's symbol badges and loads its CSS after Sumi's."""
    pytest.importorskip('mkdocstrings_handlers.python')
    (tmp_path / 'src').mkdir()
    (tmp_path / 'src' / 'demo.py').write_text(textwrap.dedent('''
        """Demo module."""

        def add(a: int, b: int = 0) -> int:
            """Add numbers.

            Args:
                a: First.
                b: Second.
            """
            return a + b
        '''), encoding='utf-8')
    out = _site(tmp_path, {'index.md': '# API\n\n::: demo\n'}, BASIC + """
      - mkdocstrings:
          handlers:
            python:
              paths: [src]
              options:
                show_root_heading: true
                show_symbol_type_heading: true
                show_source: true
    """)
    html = (out / 'index.html').read_text(encoding='utf-8')
    assert 'doc-symbol-function' in html
    assert 'class="mkdocstrings-source"' in html
    assert html.index('assets/css/sumi.css') < html.index('assets/_mkdocstrings.css')


def test_social_preview_tags(tmp_path):
    """Shared links get a title, description and image; the home page uses the site name."""
    config = BASIC.replace('site_name: Test\n', 'site_name: Test\n    site_description: A test site.\n').replace(
        '      name: sumi\n', '      name: sumi\n      social_image: img/social.png\n')
    out = _site(tmp_path, {
        'index.md': '# Welcome\n',
        'guide.md': '---\ndescription: How to use it.\nimage: https://cdn.example.com/guide.png\n---\n# Guide\n',
        'img/social.png': '',
    }, config)
    home = (out / 'index.html').read_text(encoding='utf-8')
    assert '<meta property="og:title" content="Test">' in home
    assert '<meta property="og:description" content="A test site.">' in home
    assert '<meta property="og:image" content="https://example.com/img/social.png">' in home
    assert '<meta name="twitter:card" content="summary_large_image">' in home
    guide = (out / 'guide' / 'index.html').read_text(encoding='utf-8')
    assert '<meta property="og:title" content="Guide">' in guide
    assert '<meta property="og:description" content="How to use it.">' in guide
    assert '<meta property="og:image" content="https://cdn.example.com/guide.png">' in guide


def test_social_preview_without_image(tmp_path):
    """Without an image, links still share as a small summary card."""
    out = _site(tmp_path, {'index.md': '# Home\n'}, BASIC)
    home = (out / 'index.html').read_text(encoding='utf-8')
    assert 'og:image' not in home
    assert '<meta name="twitter:card" content="summary">' in home


@pytest.mark.skipif(not _supports_languages(), reason='needs MkDocs NG 1.11 (`languages`)')
def test_multi_language_site(tmp_path):
    """One config builds both languages; untranslated pages say so and pages list their translations."""
    config = BASIC + """
    languages:
      en: English
      zh:
        name: 简体中文
        site_name: 测试
    """
    out = _site(tmp_path, {
        'index.md': '# Home\n',
        'index.zh.md': '# 首页\n',
        'guide.md': '# Guide\n',
    }, config)
    home = (out / 'zh' / 'index.html').read_text(encoding='utf-8')
    assert '<html lang="zh"' in home
    assert 'sumi-untranslated' not in home
    assert '<link rel="alternate" hreflang="en" href="https://example.com/">' in home
    assert '<link rel="alternate" hreflang="zh" href="https://example.com/zh/">' in home
    assert '<link rel="alternate" hreflang="x-default" href="https://example.com/">' in home
    guide = (out / 'zh' / 'guide' / 'index.html').read_text(encoding='utf-8')
    assert 'sumi-untranslated' in guide
    assert '本页还没有翻译，下面是 English 版本。' in guide
    assert 'lang="en"' in guide
    # The language menu links to the same page in the other language.
    assert 'href="../../guide/" hreflang="en"' in guide
    assert 'sumi-untranslated' not in (out / 'guide' / 'index.html').read_text(encoding='utf-8')


def test_theme_env_from_other_plugins(tmp_path):
    """Plugins that render main.html with a fresh `theme.get_env()` (print-site does) get Sumi's helpers."""
    from mkdocs.plugins import BasePlugin

    out = {}

    class RenderLater(BasePlugin):
        def on_post_build(self, *, config):
            env = config.theme.get_env()
            out['html'] = env.get_template('main.html').render(config=config, base_url='.', nav=[], page=None)

    (tmp_path / 'docs').mkdir()
    (tmp_path / 'docs' / 'index.md').write_text('# Home\n', encoding='utf-8')
    (tmp_path / 'mkdocs.yml').write_text(textwrap.dedent(BASIC), encoding='utf-8')
    cfg = load_config(str(tmp_path / 'mkdocs.yml'))
    cfg.plugins['render-later'] = RenderLater()
    build.build(cfg)
    assert 'class="sumi-skip"' in out['html']


def test_section_index_link_is_outside_the_toggle(tmp_path):
    """A section's index link sits next to its <summary>, not inside it (no control inside a control)."""
    out = _site(tmp_path, {
        'index.md': '# Home\n',
        'docs/index.md': '# Docs\n',
        'docs/guide/index.md': '# Guide\n',
        'docs/guide/one.md': '# One\n',
        'docs/more/two.md': '# Two\n',
    }, BASIC)
    html = (out / 'docs' / 'guide' / 'one' / 'index.html').read_text(encoding='utf-8')
    html = html.split('<nav class="sumi-nav">')[1].split('</nav>')[0]
    summaries = re.findall(r'<summary\b.*?</summary>', html, re.S)
    assert summaries and not any('<a ' in s for s in summaries)
    assert re.search(r'<a class="sumi-nav-head" href="\.\./">Guide</a>', html)
    assert '<summary class="sumi-nav-toggle" aria-label="Guide">' in html
    # A section without an index page keeps its title inside the toggle.
    assert re.search(r'<summary><span>More</span>', html)


def test_theme_without_plugin_says_what_is_missing(tmp_path):
    with pytest.raises(jinja2.TemplateNotFound, match='needs its plugin'):
        _site(tmp_path, {'index.md': '# Home\n'}, 'site_name: Test\ntheme: sumi\n')


def test_blog_tags_written_as_one_string(tmp_path):
    out = _site(tmp_path, {
        'blog/index.md': '# Blog\n',
        'blog/posts/2026-01-02-hello.md': """
            ---
            tags: release
            ---
            # Hello
        """,
        'blog/posts/2026-01-03-more.md': """
            ---
            tags: [news, null]
            ---
            # More
        """,
    }, BASIC + '    extra:\n      sumi:\n        blog: blog/index.md\n')
    html = (out / 'blog' / 'index.html').read_text(encoding='utf-8')
    assert re.findall(r'class="sumi-tag" data-tag="([^"]*)"', html) == ['news', 'release']


def test_invalid_date_in_post_name_warns(tmp_path, caplog):
    _site(tmp_path, {
        'blog/index.md': '# Blog\n',
        'blog/posts/2026-13-45-oops.md': '# Oops\n',
    }, BASIC + '    extra:\n      sumi:\n        blog: blog/index.md\n')
    assert 'invalid date in its name: 2026-13-45' in caplog.text


def test_meta_values_are_escaped(tmp_path):
    out = _site(tmp_path, {
        'index.md': '# Home\n',
        'page.md': """
            ---
            description: The "fast" way <b>now</b>
            ---
            # Fish & "chips"
        """,
    }, BASIC)
    html = (out / 'page' / 'index.html').read_text(encoding='utf-8')
    assert '<meta name="description" content="The &#34;fast&#34; way &lt;b&gt;now&lt;/b&gt;">' in html
    assert '<meta property="og:title" content="Fish &amp; &#34;chips&#34;">' in html


@pytest.mark.parametrize(('meta', 'message'), [
    ('template: landing.html\nhero: just a string', "'hero' must be a mapping"),
    ('template: landing.html\nsections: features', "'sections' must be a list"),
    ('template: releases.html\nreleases:\n  - just-a-string', 'must be a mapping'),
])
def test_malformed_front_matter_is_a_clear_error(tmp_path, caplog, meta, message):
    with pytest.raises(Abort):
        _site(tmp_path, {'index.md': f'---\n{meta}\n---\n# Home\n'}, BASIC)
    assert message in caplog.text
    assert 'Traceback' not in caplog.text


def test_every_language_has_every_string():
    """Each interface language translates every key, with the same placeholders as English."""
    import string

    from mkdocs_sumi.i18n import STRINGS

    def fields(text):
        return {f for _, f, _, _ in string.Formatter().parse(text) if f}

    for code, table in STRINGS.items():
        assert set(table) == set(STRINGS['en']), code
        for key, text in table.items():
            assert fields(text) == fields(STRINGS['en'][key]), (code, key)


@pytest.mark.parametrize(('locale', 'lang', 'text'), [
    ('de', 'de', 'Auf dieser Seite'),
    ('ja', 'ja', 'このページの内容'),
    ('pt_BR', 'pt-BR', 'Nesta página'),
])
def test_interface_language(tmp_path, locale, lang, text):
    config = BASIC.replace('      name: sumi\n', f'      name: sumi\n      locale: {locale}\n')
    out = _site(tmp_path, {'index.md': '# Home\n\n## One\n\n## Two\n'}, config)
    html = (out / 'index.html').read_text(encoding='utf-8')
    assert f'<html lang="{lang}" data-palette' in html
    assert text in html


def test_material_language_key_is_honoured(tmp_path):
    """A site moving from Material keeps `theme.language` and gets its interface language."""
    config = BASIC.replace('      name: sumi\n', '      name: sumi\n      language: fr\n')
    out = _site(tmp_path, {'index.md': '# Home\n\n## One\n\n## Two\n'}, config)
    html = (out / 'index.html').read_text(encoding='utf-8')
    assert '<html lang="fr"' in html
    assert 'Sur cette page' in html
    assert '<meta property="og:locale" content="fr_FR">' in html


def test_right_to_left_language(tmp_path):
    config = BASIC.replace('      name: sumi\n', '      name: sumi\n      locale: ar\n')
    out = _site(tmp_path, {'index.md': '# Home\n\n## One\n\n## Two\n'}, config)
    html = (out / 'index.html').read_text(encoding='utf-8')
    assert '<html lang="ar" dir="rtl"' in html
    assert 'في هذه الصفحة' in html


def test_dates_in_the_page_language():
    from mkdocs_sumi.i18n import format_date

    assert format_date(2026, 11, 5, 'en') == 'November 5, 2026'
    assert format_date(2026, 11, 5, 'en', short=True) == 'Nov 5, 2026'
    assert format_date(2026, 11, 5, 'de') == '5. November 2026'
    assert format_date(2026, 11, 5, 'es') == '5 de noviembre de 2026'
    assert format_date(2026, 11, 5, 'ko') == '2026년 11월 5일'
    assert format_date(2026, 11, 5, 'zh_TW') == '2026年11月5日'


def test_bilingual_view_only_on_translated_pages(tmp_path):
    config = BASIC + """
    languages:
      en: English
      zh:
        name: 简体中文
    """
    out = _site(tmp_path, {
        'index.md': '# Home\n',
        'index.zh.md': '# 首页\n',
        'guide.md': '# Guide\n',
    }, config)
    home = (out / 'index.html').read_text(encoding='utf-8')
    assert 'data-sumi-compare' in home
    assert 'class="sumi-compare"' in home
    assert '"href": "zh/", "lang": "zh", "name": "\\u7b80\\u4f53\\u4e2d\\u6587"' in home
    zh_home = (out / 'zh' / 'index.html').read_text(encoding='utf-8')
    assert '"href": "../", "lang": "en"' in zh_home
    # Not translated: no bilingual view in either language.
    assert 'data-sumi-compare' not in (out / 'guide' / 'index.html').read_text(encoding='utf-8')
    assert 'data-sumi-compare' not in (out / 'zh' / 'guide' / 'index.html').read_text(encoding='utf-8')


def test_bilingual_view_can_be_turned_off(tmp_path):
    config = BASIC.replace('      name: sumi\n', '      name: sumi\n      bilingual_view: false\n') + """
    languages:
      en: English
      zh: 简体中文
    """
    out = _site(tmp_path, {'index.md': '# Home\n', 'index.zh.md': '# 首页\n'}, config)
    assert 'data-sumi-compare' not in (out / 'index.html').read_text(encoding='utf-8')


def test_feedback_widget(tmp_path):
    config = BASIC.replace('      name: sumi\n', '      name: sumi\n      feedback: true\n')
    out = _site(tmp_path, {
        'index.md': '# Home\n',
        'quiet.md': '---\nhide: [feedback]\n---\n# Quiet\n',
    }, config)
    html = (out / 'index.html').read_text(encoding='utf-8')
    assert '<form class="sumi-feedback" data-pagefind-ignore hidden>' in html
    assert 'Was this page helpful?' in html
    assert html.count('class="sumi-feedback-btn"') == 2
    assert 'sumi-feedback' not in (out / 'quiet' / 'index.html').read_text(encoding='utf-8')


def test_feedback_reads_material_settings(tmp_path):
    config = BASIC + """
    extra:
      analytics:
        provider: google
        property: G-TEST
        feedback:
          title: Useful?
          ratings:
            - icon: material/emoticon-happy-outline
              name: Helpful
              data: 1
              note: 'Thanks! <a href="https://example.com/?t={title}">Tell us more</a>'
            - icon: material/emoticon-sad-outline
              name: Not helpful
              data: 0
              note: Thanks for telling us.
    """
    out = _site(tmp_path, {'index.md': '# Home\n'}, config)
    html = (out / 'index.html').read_text(encoding='utf-8')
    assert 'Useful?' in html and 'Not helpful' in html
    assert 'data-note="Thanks! &lt;a href=&#34;https://example.com/?t={title}&#34;&gt;Tell us more&lt;/a&gt;"' in html
    # Material's emoticon icons become Lucide thumbs.
    assert 'M15 5.88 14 10h5.83' in html and 'M9 18.12 10 14H4.17' in html
    assert "gtag('config', \"G-TEST\")" in html


def test_giscus_comments(tmp_path):
    config = BASIC.replace('      name: sumi\n', """      name: sumi
      locale: zh
      comments:
        provider: giscus
        repo: acme/docs
        repo_id: R_1
        category: Comments
        category_id: DIC_1
""")
    out = _site(tmp_path, {
        'index.md': '# Home\n',
        'off.md': '---\ncomments: false\n---\n# Off\n',
    }, config)
    html = (out / 'index.html').read_text(encoding='utf-8')
    assert 'class="sumi-giscus" data-repo="acme/docs" data-repo-id="R_1"' in html
    assert 'data-lang="zh-CN"' in html
    assert 'id="__comments"' in html
    assert 'sumi-giscus' not in (out / 'off' / 'index.html').read_text(encoding='utf-8')


def test_giscus_comments_opt_in(tmp_path):
    config = BASIC.replace('      name: sumi\n', """      name: sumi
      comments:
        repo: acme/docs
        opt_in: true
""")
    out = _site(tmp_path, {'index.md': '# Home\n', 'on.md': '---\ncomments: true\n---\n# On\n'}, config)
    assert 'sumi-giscus' not in (out / 'index.html').read_text(encoding='utf-8')
    assert 'sumi-giscus' in (out / 'on' / 'index.html').read_text(encoding='utf-8')


@pytest.mark.parametrize(('analytics', 'expected'), [
    ('provider: plausible\n        domain: docs.example.com', ['"docs.example.com"', 'https://plausible.io/js/script.js']),
    ('provider: umami\n        website_id: abc-123\n        src: https://stats.example.com/script.js',
     ['"abc-123"', '"https://stats.example.com/script.js"']),
])
def test_privacy_friendly_analytics(tmp_path, analytics, expected):
    config = BASIC + f"""
    extra:
      analytics:
        {analytics}
    """
    html = (_site(tmp_path, {'index.md': '# Home\n'}, config) / 'index.html').read_text(encoding='utf-8')
    for text in expected:
        assert text in html
    assert "window.name !== 'sumi-pane'" in html
    assert 'googletagmanager' not in html


def test_expandable_table(tmp_path):
    out = _site(tmp_path, {'index.md': '# Home\n\n| a | b |\n| --- | --- |\n| 1 | 2 |\n{.expand .compact}\n'}, BASIC)
    html = (out / 'index.html').read_text(encoding='utf-8')
    assert 'class="sumi-table sumi-table--compact sumi-table--expand"' in html


def test_gallery_columns_and_style_combine(tmp_path):
    out = _site(tmp_path, {'index.md': '# Home\n\n- ![a](a.png)\n- ![b](b.png)\n{.gallery cols="2" style="--ratio: 16 / 10"}\n'}, BASIC)
    assert 'style="--cols:2;--ratio: 16 / 10"' in (out / 'index.html').read_text(encoding='utf-8')


GITHUB_RELEASES = [
    {'tag_name': 'v0.3.0', 'name': 'v0.3.0', 'draft': True, 'published_at': None, 'body': 'Not out yet.'},
    {'tag_name': 'v0.2.0', 'name': 'v0.2.0', 'published_at': '2026-11-05T16:35:46Z', 'prerelease': False,
     'body': '<!-- Optional: add a release summary here -->\r\nLanguages and comments.\r\n\r\n'
             '## 🚀 New features\r\n\r\n- Ten more languages by @octo-cat in #22\r\n\r\n'
             '**Full Changelog**: https://github.com/o/r/compare/v0.1.0...v0.2.0\r\n',
     'assets': [{'name': 'app.zip', 'browser_download_url': 'https://github.com/o/r/app.zip', 'size': 2_500_000,
                 'digest': 'sha256:' + 'a' * 64}]},
    {'tag_name': 'v0.1.1', 'name': 'Small fixes', 'published_at': '2026-11-02T08:00:00Z', 'prerelease': True,
     'body': '## What\'s Changed\r\n* Fix it by @octo-cat in https://github.com/o/r/pull/5\r\n'},
]
PYPI = {'releases': {
    '0.1.1': [
        {'filename': 'r-0.1.1.tar.gz', 'url': 'https://files/r-0.1.1.tar.gz', 'size': 1200,
         'digests': {'sha256': 'b' * 64}},
        {'filename': 'r-0.1.1-py3-none-any.whl', 'url': 'https://files/r-0.1.1-py3-none-any.whl', 'size': 900,
         'digests': {'sha256': 'c' * 64}},
    ],
    '0.2.0': [{'filename': 'r-0.2.0.tar.gz', 'url': 'https://files/r-0.2.0.tar.gz', 'size': 1,
               'digests': {'sha256': 'd' * 64}}],
}}


@pytest.fixture
def remote(monkeypatch):
    from mkdocs_sumi import releases

    calls = []

    def get_json(url):
        calls.append(url)
        if url.startswith('https://api.github.com/repos/o/r/releases'):
            return GITHUB_RELEASES
        if url == 'https://pypi.org/pypi/r/json':
            return PYPI
        raise OSError('offline')

    monkeypatch.setattr(releases, '_get_json', get_json)
    monkeypatch.setattr(releases, '_cache', {})
    return calls


def test_releases_from_github_and_pypi(tmp_path, remote):
    out = _site(tmp_path, {
        'index.md': '# Home\n',
        'releases.md': """
            ---
            template: releases.html
            releases:
              github: o/r
              pypi: r
              file: releases.yml
            ---
            # Releases
        """,
        'releases.yml': """
            - version: 0.1.1
              summary: Hand-written summary.
            - version: 0.0.9
              date: 2026-10-01
              notes: Only in the file.
        """,
    }, BASIC)
    html = (out / 'releases' / 'index.html').read_text(encoding='utf-8')
    # Drafts are left out; GitHub's order, then file-only versions by date.
    assert 'v0-3-0' not in html
    assert html.index('id="v0-2-0"') < html.index('id="v0-1-1"') < html.index('id="v0-0-9"')
    # The first paragraph is the summary; comments go; headings move down; refs and users link.
    assert '<p class="sumi-release-summary">Languages and comments.</p>' in html
    assert 'Optional: add a release summary' not in html
    assert '<h4>🚀 New features</h4>' in html
    assert '<a href="https://github.com/octo-cat">@octo-cat</a>' in html
    assert '<a href="https://github.com/o/r/issues/22">#22</a>' in html
    assert '<a href="https://github.com/o/r/compare/v0.1.0...v0.2.0">' in html
    # GitHub assets win over PyPI's; PyPI fills in the rest, wheels first.
    assert 'app.zip' in html and 'data-copy="' + 'a' * 64 + '"' in html and '2.5 MB' in html
    assert 'r-0.2.0.tar.gz' not in html
    assert html.index('r-0.1.1-py3-none-any.whl') < html.index('r-0.1.1.tar.gz')
    assert '1.2 KB' in html
    # The file's fields win; a GitHub name that isn't the tag is the title; pre-releases are marked.
    assert 'Hand-written summary.' in html
    assert 'Small fixes' in html
    assert 'sumi-release--prerelease' in html
    assert '<a href="https://github.com/o/r/pull/5">https://github.com/o/r/pull/5</a>' in html


def test_releases_sources_are_read_once(tmp_path, remote):
    page = '---\ntemplate: releases.html\nreleases:\n  github: o/r\n---\n# Releases\n'
    _site(tmp_path, {'index.md': '# Home\n', 'a.md': page, 'b.md': page}, BASIC)
    assert len(remote) == 1


def test_releases_unreachable_source_warns_and_keeps_the_file(tmp_path, remote, caplog):
    out = _site(tmp_path, {
        'index.md': '# Home\n',
        'releases.md': '---\ntemplate: releases.html\nreleases:\n  github: x/offline\n  file: releases.yml\n---\n# R\n',
        'releases.yml': '- version: 1.0.0\n  notes: From the file.\n- version: 0.9.0\n',
    }, BASIC)
    assert "couldn't read the releases of x/offline from GitHub: offline" in caplog.text
    html = (out / 'releases' / 'index.html').read_text(encoding='utf-8')
    assert html.index('id="v1-0-0"') < html.index('id="v0-9-0"')
    assert 'From the file.' in html


def test_releases_unknown_source_is_a_clear_error(tmp_path, caplog):
    with pytest.raises(Abort):
        _site(tmp_path, {'index.md': '---\ntemplate: releases.html\nreleases:\n  gitlab: o/r\n---\n# R\n'}, BASIC)
    assert "Unknown 'releases' keys in 'index.md': gitlab" in caplog.text


def test_landing_docs_and_include_sections(tmp_path):
    (tmp_path / 'overrides' / 'partials').mkdir(parents=True)
    (tmp_path / 'overrides' / 'partials' / 'checker.html').write_text('<div class="my-checker">{{ page.title }}</div>')
    (tmp_path / 'overrides' / 'partials' / 'tools.html').write_text('<p class="my-tools">spec.json</p>')
    site = _site(tmp_path, {
        'index.md': """
            ---
            template: landing.html
            hero: {title: Spec, text: A specification.}
            sections:
              - {type: content, toc: true, id: spec, aside: partials/tools.html}
              - {type: include, template: partials/checker.html, title: Try it, class: is-dark}
            ---
            # Spec 1.0

            ## Summary

            Text.

            ## Rules

            More.
            """,
    }, BASIC.replace('  name: sumi\n', '  name: sumi\n      custom_dir: overrides\n'))
    html = (site / 'index.html').read_text()
    docs = html[html.index('sumi-land-docs'):html.index('sumi-land-include')]
    assert 'id="spec"' in html
    assert 'sumi-rail' in docs and 'sumi-toc-inline' in docs and 'href="#rules"' in docs
    assert '<p class="my-tools">spec.json</p>' in docs
    assert '<h2 id="rules">' in docs and 'data-pagefind-body' in docs
    include = html[html.index('sumi-land-include'):]
    assert 'is-dark' in include and 'Try it' in include
    assert '<div class="my-checker">Spec 1.0</div>' in include


def test_versions_in_folders(tmp_path):
    site = _site(tmp_path, {
        'index.md': '# Latest\n',
        'v1/index.md': '# Old\n',
    }, BASIC.replace('  name: sumi\n', '  name: sumi\n      versions:\n        - {title: "2.0", path: ""}\n        - {title: "1.0", path: v1/}\n'))
    latest = (site / 'index.html').read_text()
    assert 'sumi-version-current">2.0<' in latest
    assert '<div class="sumi-version-banner" hidden></div>' in latest
    old = (site / 'v1' / 'index.html').read_text()
    assert 'sumi-version-current">1.0<' in old
    assert re.search(r'<div class="sumi-version-banner">You are reading [^<]*<a href="\.\./">', old)
    assert 'href="./" aria-current="true">1.0' in old


def test_main_html_override_reaches_every_template(tmp_path):
    (tmp_path / 'overrides').mkdir()
    (tmp_path / 'overrides' / 'main.html').write_text(
        '{% extends "base.html" %}{% block extrahead %}<meta name="x-test" content="1">{% endblock %}')
    site = _site(tmp_path, {
        'index.md': '---\ntemplate: landing.html\nhero: {title: Hi}\n---\n',
        'page.md': '# Page\n',
    }, BASIC.replace('  name: sumi\n', '  name: sumi\n      custom_dir: overrides\n'))
    for path in ('index.html', 'page/index.html', '404.html'):
        assert '<meta name="x-test" content="1">' in (site / path).read_text(), path


def test_navigation_tabs_always(tmp_path):
    site = _site(tmp_path, {
        'index.md': '---\ntemplate: landing.html\nhero: {title: Hi}\n---\n',
        'guide.md': '# Guide\n',
    }, BASIC.replace('  name: sumi\n', '  name: sumi\n      navigation_tabs: always\n'))
    for path in ('index.html', 'guide/index.html'):
        html = (site / path).read_text()
        assert 'class="sumi-tabs-nav"' in html, path
        # The header tabs are hidden on small screens, so the drawer lists them.
        assert 'sumi-sidebar--tabs-only' in html and 'aria-controls="sumi-sidebar"' in html, path
