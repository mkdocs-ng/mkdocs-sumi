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
pytest.importorskip('mkdocs.contrib.llms_txt', reason='the docs site needs MkDocs-ng 1.9')


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
    page.keyboard.press('Enter')
    assert page.evaluate('document.documentElement.dataset.theme') != theme


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
