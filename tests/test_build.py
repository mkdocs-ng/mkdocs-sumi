"""Build small sites with the theme and plugin and check the outputs."""

from __future__ import annotations

import os
import re
import textwrap
from pathlib import Path

import pytest
from mkdocs.commands import build
from mkdocs.config import load_config

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
