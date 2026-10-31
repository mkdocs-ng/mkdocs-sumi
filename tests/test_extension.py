from __future__ import annotations

import re


def test_callout_types_and_titles(md):
    html = md("""
        > [!WARNING] Back up first
        > This **deletes** data.
        """)
    assert 'sumi-callout--warning' in html
    assert 'Back up first' in html
    assert '<strong>deletes</strong>' in html
    assert '<blockquote' not in html


def test_callout_default_title_follows_language(md):
    assert '>Tip<' in md('> [!TIP]\n> Text')
    assert '>提示<' in md('> [!TIP]\n> Text', language='zh')


def test_material_type_maps_to_family(md):
    assert 'sumi-callout--caution' in md('> [!DANGER]\n> Hot')


def test_foldable_callouts(md):
    closed = md('> [!NOTE]- Folded\n> Body')
    opened = md('> [!NOTE]+ Open\n> Body')
    assert closed.startswith('<details class="sumi-callout sumi-callout--note">')
    assert opened.startswith('<details class="sumi-callout sumi-callout--note" open')


def test_adjacent_callouts_are_split(md):
    html = md('> [!NOTE]\n> One\n>\n> [!TIP]\n> Two')
    assert 'sumi-callout--note' in html and 'sumi-callout--tip' in html
    assert html.count('class="sumi-callout sumi-callout--') == 2


def test_plain_blockquote_untouched(md):
    html = md('> Just a quote')
    assert '<blockquote>' in html and 'sumi-callout' not in html


def test_steps_and_cards(md):
    steps = md('1. One\n2. Two\n{.steps}')
    assert '<ol class="sumi-steps">' in steps
    cards = md('- [A](a.md) First\n- [B](b.md) Second\n{.cards cols=2}')
    assert 'class="sumi-cards"' in cards and '--cols:2' in cards
    assert '{.cards' not in cards


def test_fields(md):
    html = md("""
        | Name | Type | Default | Required | Description |
        | --- | --- | --- | --- | --- |
        | `port` | integer | `8000` | yes | The **port**. |
        {.fields}
        """)
    assert 'class="sumi-fields"' in html and '<table' not in html
    assert 'sumi-chip--required' in html
    assert 'data-key="type"' in html and 'integer' in html
    assert '<strong>port</strong>' in html


def test_table_caption_and_flags(md):
    html = md('| a | b |\n| - | - |\n| 1 | 2 |\n{.wide .striped caption="Numbers"}')
    assert '<caption>Numbers</caption>' in html
    assert 'sumi-table--wide' in html and 'sumi-table--striped' in html


def test_figure_caption_and_lazy_images(md):
    html = md('![Alt](a.png)\n{caption="A figure"}')
    assert '<figure class="sumi-figure">' in html
    assert '<figcaption>A figure</figcaption>' in html
    assert 'loading="lazy"' in html


def test_tabs_group_adjacent_fences(md):
    html = md("""
        ```sh {tab="Linux"}
        apt install x
        ```

        ```powershell {tab="Windows"}
        winget install x
        ```
        """)
    assert html.count('class="sumi-tabs"') == 1
    assert 'data-group="Linux|Windows"' in html
    assert html.count('class="sumi-tab"') == 2
    assert '{tab=' not in html


def test_titled_fence(md):
    html = md('```python title="app.py"\nprint(1)\n```')
    assert 'class="sumi-code"' in html and '<span>app.py</span>' in html
    assert 'highlight' in html


def test_fences_inside_longer_fences_stay_literal(md):
    html = md('````markdown\n```sh {tab="A"}\nx\n```\n````')
    assert 'sumi-tabs' not in html
    assert 'tab=' in html


def test_filetree(md):
    html = md("""
        ```filetree
        site/
        ├── docs/       # sources
        │   └── index.md
        └── mkdocs.yml
        ```
        """)
    assert 'sumi-filetree' in html
    assert 'sources' in html and 'mkdocs.yml' in html
    assert '<details open>' in html


def test_mermaid_can_be_disabled(md):
    on = md('```mermaid\ngraph TD; A-->B\n```')
    off = md('```mermaid\ngraph TD; A-->B\n```', mermaid=False)
    assert '<pre class="mermaid">' in on
    assert '<pre class="mermaid">' not in off


def test_math(md):
    html = md('Euler $e^{i\\pi}+1=0$ costs $5 or $6.\n\n$$\n\\int_0^1 x\\,dx\n$$')
    assert html.count('sumi-math') == 2
    assert '$5 or $6' in html
    assert 'sumi-math' not in md('Code `$x$` here')


def test_keys_and_icons(md):
    html = md('Press ++Ctrl+K++ :lucide-rocket: :brand-github: :lucide-nope:')
    assert html.count('<kbd>') == 2
    assert html.count('<svg') == 2
    assert ':lucide-nope:' in html


def test_attribute_line_inside_code_is_untouched(md):
    html = md('```markdown\n1. a\n{.steps}\n```')
    assert '{.steps}' in html and 'sumi-steps' not in html


def test_no_leftover_placeholders(md):
    html = md("""
        > [!NOTE]
        > ```py title="x.py"
        > print(1)
        > ```
        """)
    assert not re.search(r'\x02|wzxhzdk', html)
