"""Browser tests against the built documentation site.

Run with `pytest tests/test_browser.py` after `pip install playwright` and
`playwright install chromium`. Skipped when Playwright is not installed.
Set SUMI_CHROMIUM to use an existing Chromium binary.
"""

from __future__ import annotations

import functools
import http.server
import os
import threading
from pathlib import Path

import pytest

sync_api = pytest.importorskip('playwright.sync_api')

from mkdocs.commands import build  # noqa: E402
from mkdocs.config import load_config  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
pytest.importorskip('mkdocs.contrib.llms_txt', reason='the docs site needs MkDocs NG 1.9')
pytest.importorskip('mkdocs.languages', reason='the docs site needs MkDocs NG 1.11')


@pytest.fixture(scope='module')
def base_url(tmp_path_factory):
    site = tmp_path_factory.mktemp('site')
    cfg = load_config(str(ROOT / 'mkdocs.yml'), site_dir=str(site))
    build.build(cfg)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(site))
    handler.log_message = lambda *a: None
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f'http://127.0.0.1:{server.server_address[1]}/', site
    server.shutdown()


@pytest.fixture(scope='module')
def browser():
    with sync_api.sync_playwright() as p:
        exe = os.environ.get('SUMI_CHROMIUM')
        b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        yield b
        b.close()


@pytest.fixture
def page(browser):
    ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
    pg = ctx.new_page()
    pg.errors = []
    pg.on('pageerror', lambda e: pg.errors.append(str(e)))
    pg.on('console', lambda m: m.type == 'error' and pg.errors.append(m.text))
    yield pg
    ctx.close()


def test_every_page_loads_without_errors(base_url, page):
    url, site = base_url
    pages = sorted(p.relative_to(site).parent.as_posix() for p in site.rglob('index.html'))
    assert len(pages) > 30
    for rel in pages:
        page.goto(url + ('' if rel == '.' else rel + '/'), wait_until='networkidle')
        assert page.errors == [], f'{rel}: {page.errors}'


def test_palette_searches_cjk_and_runs_commands(base_url, page):
    url, _ = base_url
    page.goto(url + 'docs/', wait_until='networkidle')
    page.keyboard.press('Control+k')
    dialog = page.locator('.sumi-palette')
    sync_api.expect(dialog).to_be_visible()
    page.keyboard.type('安装')
    sync_api.expect(page.locator('.sumi-palette-item').first).to_contain_text('Search')
    page.keyboard.press('Escape')
    sync_api.expect(dialog).to_be_hidden()
    theme = page.evaluate('document.documentElement.dataset.theme')
    page.keyboard.press('Control+k')
    sync_api.expect(dialog).to_be_visible()
    page.keyboard.type('>dark')
    sync_api.expect(page.locator('.sumi-palette-item')).to_have_count(1)
    page.evaluate("document.addEventListener('sumi:theme', e => { window.sumiTheme = e.detail.theme; })")
    page.keyboard.press('Enter')
    new = page.evaluate('document.documentElement.dataset.theme')
    assert new != theme
    # Plugins can follow the switch through the event or Material's attribute.
    assert page.evaluate('window.sumiTheme') == new
    scheme = page.evaluate('document.documentElement.dataset.mdColorScheme')
    assert scheme == ('slate' if new == 'dark' else 'default')


def test_palette_highlights_without_breaking_the_markup(base_url, page):
    url, _ = base_url
    page.goto(url + 'docs/', wait_until='networkidle')
    page.keyboard.press('Control+k')
    # "t" and "q" sit inside "&quot;", and "mark" inside the <mark> of an earlier term.
    page.keyboard.type('a t q mark')
    results = page.locator('.sumi-palette-results')
    sync_api.expect(page.locator('.sumi-palette-item').first).to_be_visible()
    text = results.inner_text()
    for broken in ('&quot;', '&amp;', '&lt;', 'mark>'):
        assert broken not in text
    assert page.locator('.sumi-palette-results mark mark').count() == 0


def test_tabs_sync_and_persist(base_url, page):
    url, _ = base_url
    page.goto(url + 'docs/write/tabs/', wait_until='networkidle')
    page.locator('.sumi-tablist [role=tab]', has_text='Windows').first.click()
    active = page.locator('.sumi-tabs .sumi-tab.is-active .sumi-tab-label').all_inner_texts()
    assert active[:2] == ['Windows', 'Windows']
    page.goto(url + 'docs/start/install/', wait_until='networkidle')
    page.goto(url + 'docs/write/tabs/', wait_until='networkidle')
    assert page.locator('.sumi-tabs .sumi-tab.is-active').first.get_attribute('data-label') == 'Windows'


def test_mermaid_and_math_render(base_url, page):
    url, _ = base_url
    page.goto(url + 'docs/write/diagrams/', wait_until='networkidle')
    sync_api.expect(page.locator('.sumi-diagram svg').first).to_be_visible()
    page.goto(url + 'docs/write/math/', wait_until='networkidle')
    sync_api.expect(page.locator('.katex').first).to_be_visible()


def test_charts_and_mind_maps_render(base_url, page):
    url, _ = base_url
    page.goto(url + 'docs/write/charts/', wait_until='networkidle')
    chart = page.locator('.sumi-chart').first
    chart.scroll_into_view_if_needed()
    sync_api.expect(chart.locator('.sumi-chart-canvas svg')).to_be_visible()
    mm = page.locator('.sumi-markmap').first
    mm.scroll_into_view_if_needed()
    sync_api.expect(mm.locator('svg.sumi-markmap-svg g.markmap-node').first).to_be_attached()
    sync_api.expect(mm.locator('.sumi-markmap-outline')).to_be_hidden()


def test_copy_as_markdown(base_url, browser):
    url, _ = base_url
    ctx = browser.new_context(permissions=['clipboard-read', 'clipboard-write'])
    page = ctx.new_page()
    page.goto(url + 'docs/write/steps/', wait_until='networkidle')
    page.get_by_role('button', name='Copy as Markdown').click()
    page.wait_for_timeout(500)
    assert '{.steps}' in page.evaluate('navigator.clipboard.readText()')
    ctx.close()


def test_mobile_drawer(base_url, browser):
    url, _ = base_url
    ctx = browser.new_context(viewport={'width': 390, 'height': 844})
    page = ctx.new_page()
    page.goto(url + 'docs/write/callouts/', wait_until='networkidle')
    sidebar = page.locator('#sumi-sidebar')
    assert not sidebar.is_visible() or sidebar.bounding_box()['x'] < 0
    page.locator('.sumi-menu-btn, [aria-controls="sumi-sidebar"]').first.click()
    page.wait_for_timeout(400)
    assert sidebar.bounding_box()['x'] >= 0
    ctx.close()


def test_mobile_drawer_fits_the_screen_and_lists_the_tabs(base_url, browser):
    url, _ = base_url
    # A short screen, so the docs nav is taller than the drawer.
    ctx = browser.new_context(viewport={'width': 320, 'height': 500})
    page = ctx.new_page()
    page.goto(url + 'docs/write/callouts/', wait_until='networkidle')
    page.locator('.sumi-menu-btn').click()
    page.wait_for_timeout(400)
    header = page.locator('.sumi-header').bounding_box()
    box = page.locator('#sumi-sidebar').bounding_box()
    # The drawer starts below the header and ends at the bottom of the screen.
    assert abs(box['y'] - (header['y'] + header['height'])) < 2
    assert abs(box['y'] + box['height'] - 500) < 2
    inner = page.locator('.sumi-sidebar-inner')
    assert inner.evaluate('e => e.scrollHeight > e.clientHeight')
    # The header tabs are hidden on small screens, so the drawer lists them.
    tabs = page.locator('.sumi-sidebar-tabs')
    assert tabs.is_visible()
    assert tabs.locator('a.is-active').inner_text() == 'Docs'
    # The menu button keeps its size next to a long site name.
    assert page.locator('.sumi-menu-btn').bounding_box()['width'] >= 35
    ctx.close()


def test_mobile_drawer_on_a_page_outside_the_tabs(base_url, browser):
    url, _ = base_url
    ctx = browser.new_context(viewport={'width': 390, 'height': 844})
    page = ctx.new_page()
    page.goto(url + 'releases/', wait_until='networkidle')
    page.locator('.sumi-menu-btn').click()
    page.wait_for_timeout(400)
    assert page.locator('.sumi-sidebar-tabs').is_visible()
    ctx.close()


def test_bilingual_view_scrolls_both_languages_together(base_url, page):
    url, _ = base_url
    page.goto(url + 'docs/write/code/', wait_until='networkidle')
    page.get_by_role('button', name='Open bilingual view').click()
    dialog = page.locator('.sumi-compare')
    sync_api.expect(dialog).to_be_visible()
    left, right = page.frame_locator('.sumi-compare iframe').nth(0), page.frame_locator('.sumi-compare iframe').nth(1)
    sync_api.expect(right.locator('html.sumi-pane')).to_be_attached()
    sync_api.expect(right.locator('html')).to_have_attribute('lang', 'zh')
    # The pane shows the content only.
    sync_api.expect(left.locator('.sumi-header')).to_be_hidden()
    left.locator('#diffs').evaluate('h => h.scrollIntoView()')
    page.wait_for_timeout(400)
    top = right.locator('#diffs').evaluate('h => h.getBoundingClientRect().top')
    assert 0 <= top < 80
    page.keyboard.press('Escape')
    sync_api.expect(dialog).to_be_hidden()
    assert page.url.endswith('/docs/write/code/')
    assert not page.errors


def test_bilingual_view_lines_up_blocks_and_follows_either_side(base_url, page):
    url, _ = base_url
    page.goto(url + 'docs/write/tables/', wait_until='networkidle')
    page.keyboard.press('b')
    sync_api.expect(page.locator('.sumi-compare')).to_be_visible()
    frames = page.locator('.sumi-compare iframe')
    right = page.frame_locator('.sumi-compare iframe').nth(1)
    sync_api.expect(right.locator('html.sumi-pane')).to_be_attached()
    page.wait_for_timeout(500)
    # Headings and blocks match, so no "approximate" note.
    sync_api.expect(page.locator('.sumi-compare-approx')).to_be_hidden()

    def blocks(n):
        return frames.nth(n).evaluate(
            """f => [...f.contentDocument.querySelectorAll('.sumi-content > *')]
                 .filter(e => e.offsetHeight).map(e => e.getBoundingClientRect().top)"""
        )

    # Scroll the right side with the wheel: the left side follows it, and the
    # block at the reading line (a third of the way down) is the same block.
    box = frames.nth(1).bounding_box()
    page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
    for _ in range(12):
        page.mouse.wheel(0, 120)
        page.wait_for_timeout(50)
    page.wait_for_timeout(300)
    line = box['height'] / 3
    left, right_tops = blocks(0), blocks(1)
    assert len(left) == len(right_tops)
    k = min(range(len(right_tops)), key=lambda i: abs(right_tops[i] - line))
    assert abs(left[k] - right_tops[k]) < 40
    # Both sides reach the end together.
    for _ in range(80):
        page.mouse.wheel(0, 400)
    page.wait_for_timeout(500)
    ends = [
        frames.nth(n).evaluate(
            'f => f.contentDocument.documentElement.scrollHeight - f.contentWindow.innerHeight - f.contentWindow.scrollY'
        )
        for n in (0, 1)
    ]
    assert ends[0] < 2 and ends[1] < 2
    # Turning sync off is remembered.
    page.locator('.sumi-compare-sync input').uncheck()
    assert page.evaluate("localStorage.getItem('sumi.compare-sync')") == '0'
    assert not page.errors


def test_bilingual_view_notes_sections_that_differ(base_url, page):
    url, _ = base_url
    # The Chinese page has a section the English one lacks.
    page.goto(url + 'docs/customize/i18n/', wait_until='networkidle')
    page.keyboard.press('b')
    sync_api.expect(page.locator('.sumi-compare-approx')).to_be_visible()
    assert not page.errors


def test_wide_table_opens_full_screen(base_url, page):
    url, _ = base_url
    page.goto(url + 'docs/write/tables/', wait_until='networkidle')
    # The table marked {.expand} gets the button; tables that fit do not.
    buttons = page.get_by_role('button', name='Expand table')
    sync_api.expect(buttons).to_have_count(1)
    buttons.click()
    view = page.locator('.sumi-table-view')
    sync_api.expect(view).to_be_visible()
    sync_api.expect(view.locator('table th').first).to_have_text('Option')
    page.keyboard.press('Escape')
    sync_api.expect(view).to_be_hidden()
    assert not page.errors


def test_wide_table_moves_the_toc_aside(base_url, page):
    url, _ = base_url
    page.set_viewport_size({'width': 1440, 'height': 900})
    page.goto(url + 'docs/start/migrate/', wait_until='networkidle')
    rail = page.locator('.sumi-rail')
    sync_api.expect(rail).to_be_visible()
    # The {.wide} table reaches into the table-of-contents column, so the
    # table of contents steps aside while the table is beside it.
    page.locator('.sumi-table--wide').evaluate(
        'el => window.scrollTo(0, el.getBoundingClientRect().top + scrollY - 100)'
    )
    sync_api.expect(rail).to_be_hidden()
    page.evaluate('window.scrollTo(0, 0)')
    sync_api.expect(rail).to_be_visible()
    assert not page.errors


def test_diagram_view_pans_and_zooms(base_url, page):
    url, _ = base_url
    page.goto(url + 'docs/write/diagrams/', wait_until='networkidle')
    fig = page.locator('.sumi-diagram').first
    sync_api.expect(fig.locator('svg').first).to_be_visible()
    fig.hover()
    fig.get_by_role('button', name='Expand diagram').click()
    view = page.locator('.sumi-diagram-view')
    sync_api.expect(view).to_be_visible()
    canvas = view.locator('.sumi-diagram-view-canvas')

    def scale():
        return canvas.evaluate('c => new DOMMatrix(getComputedStyle(c).transform).a')

    view.get_by_role('button', name='Zoom in').click()
    assert abs(scale() - 1.5) < 0.01
    page.keyboard.press('-')
    assert abs(scale() - 1) < 0.01
    box = view.locator('.sumi-diagram-view-body').bounding_box()
    page.mouse.move(box['x'] + 200, box['y'] + 200)
    page.mouse.wheel(0, -300)
    assert scale() > 1.2
    before = canvas.evaluate('c => new DOMMatrix(getComputedStyle(c).transform).e')
    page.mouse.down()
    page.mouse.move(box['x'] + 260, box['y'] + 200, steps=4)
    page.mouse.up()
    after = canvas.evaluate('c => new DOMMatrix(getComputedStyle(c).transform).e')
    assert abs(after - before - 60) < 2
    page.keyboard.press('0')
    assert abs(scale() - 1) < 0.01
    assert not page.errors


def test_feedback_widget_sends_the_rating(tmp_path, page):
    docs = tmp_path / 'docs'
    docs.mkdir()
    (docs / 'index.md').write_text('# Home\n\nText.\n', encoding='utf-8')
    (tmp_path / 'mkdocs.yml').write_text(
        'site_name: Test\ntheme:\n  name: sumi\nplugins: [sumi]\nextra:\n  analytics:\n    feedback:\n'
        '      title: Useful?\n      ratings:\n        - {icon: thumbs-up, name: "Yes", data: 1, note: "Thanks, <b>{title}</b>"}\n'
        '        - {icon: thumbs-down, name: "No", data: 0, note: Sorry}\n', encoding='utf-8')
    build.build(load_config(str(tmp_path / 'mkdocs.yml')))
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(tmp_path / 'site'))
    handler.log_message = lambda *a: None
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    page.goto(f'http://127.0.0.1:{server.server_address[1]}/', wait_until='networkidle')
    page.evaluate("document.addEventListener('sumi:feedback', e => { window.rated = e.detail.value; })")
    form = page.locator('.sumi-feedback')
    sync_api.expect(form).to_be_visible()
    form.get_by_role('button', name='Yes').click()
    assert page.evaluate('window.rated') == 1
    sync_api.expect(form.locator('.sumi-feedback-note b')).to_have_text('Test')
    sync_api.expect(form.get_by_role('button', name='No')).to_be_disabled()
    assert not page.errors
    server.shutdown()
