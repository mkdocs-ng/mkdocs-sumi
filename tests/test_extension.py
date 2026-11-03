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


def test_echarts_fence_yaml_and_json(md):
    html = md('```echarts title="Sales" height="240"\nseries:\n  - type: bar\n    data: [1, 2]\n```')
    assert '<figure class="sumi-chart">' in html
    assert 'style="height:240px"' in html
    assert '"series":[{"type":"bar","data":[1,2]}]' in html
    assert '<figcaption>Sales</figcaption>' in html
    assert 'class="sumi-chart"' in md('```echarts\n{"series": []}\n```')


def test_echarts_fence_invalid_stays_code(md, caplog):
    html = md('```echarts\n- just\n- a list\n```')
    assert 'sumi-chart' not in html
    assert 'option object' in caplog.text


def test_echarts_option_cannot_close_script(md):
    html = md('```echarts\ntitle: {text: "</script><b>x"}\n```')
    assert '</script><b>' not in html


def test_markmap_outline():
    from mkdocs_sumi.markdown.charts import outline

    tree = outline('# Root\n## A\n- a1\n  - a11\n- a2\n## B\n')
    assert tree['content'] == 'Root'
    assert [c['content'] for c in tree['children']] == ['A', 'B']
    a = tree['children'][0]
    assert [c['content'] for c in a['children']] == ['a1', 'a2']
    assert a['children'][0]['children'][0]['content'] == 'a11'
    assert outline('- **x**\n- y')['children'][0]['content'] == '<strong>x</strong>'


def test_markmap_fence_has_list_fallback(md):
    html = md('```markmap\n# Root\n- one\n- two\n```')
    assert 'class="sumi-markmap"' in html
    assert '<ul><li>one</li><li>two</li></ul>' in html


def test_gallery(md):
    html = md('- ![a](a.png)\n  First\n- ![b](b.png)\n{.gallery cols="2"}')
    assert '<ul class="sumi-gallery" style="--cols:2">' in html


def test_badge_is_plain_attr_list(md):
    assert '<strong class="badge tip">Stable</strong>' in md('**Stable**{.badge .tip}')


def test_fence_inside_a_list_item_is_a_code_block(md):
    html = md('1. Install\n\n    ```sh\n    pip install x\n    ```\n\n2. Run\n{.steps}')
    assert '<code>sh' not in html
    assert '<div class="highlight"><pre>' in html and 'pip' in html
    titled = md('- Step\n\n    ```py title="app.py"\n    print(1)\n    ```\n')
    assert 'data-title="app.py"' in titled and '<pre>' in titled


def test_echarts_canvas_is_named_for_screen_readers(md):
    assert 'role="img" aria-label="Sales"' in md('```echarts title="Sales"\nseries: []\n```')
    # Without a fence title, the chart's own title names it.
    assert 'role="img" aria-label="Build time"' in md('```echarts\ntitle: {text: Build time}\nseries: []\n```')
    # With no name at all, the canvas is not announced as an unnamed image.
    assert 'role="img"' not in md('```echarts\nseries: []\n```')
