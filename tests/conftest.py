from __future__ import annotations

import textwrap

import markdown
import pytest


@pytest.fixture
def md():
    """Render Markdown the way the sumi plugin configures it."""

    def render(text: str, **config) -> str:
        return markdown.markdown(
            textwrap.dedent(text),
            extensions=['attr_list', 'admonition', 'md_in_html', 'tables', 'toc', 'fenced_code', 'codehilite',
                        'mkdocs_sumi.markdown.extension'],
            extension_configs={
                'codehilite': {'css_class': 'highlight', 'guess_lang': False},
                'mkdocs_sumi.markdown.extension': config,
            },
        )

    return render
