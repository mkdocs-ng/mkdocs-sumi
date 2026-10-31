"""Inline SVG icons: Lucide (ISC) for interface icons, Simple Icons (CC0) for brands."""

from __future__ import annotations

import functools
import json
from importlib import resources

from markupsafe import Markup, escape


@functools.cache
def _lucide() -> dict[str, str]:
    return json.loads(resources.files(__package__).joinpath('vendor/icons/lucide.json').read_text('utf-8'))


@functools.cache
def _brands() -> dict[str, str]:
    return json.loads(resources.files(__package__).joinpath('vendor/icons/brands.json').read_text('utf-8'))


def has_icon(name: str) -> bool:
    name = name.removeprefix('lucide-')
    if name.startswith('brand-'):
        return name[6:] in _brands()
    return name in _lucide()


def icon(name: str, cls: str = '', label: str | None = None) -> Markup:
    """Return the icon as inline SVG, or an empty string for an unknown name.

    `name` is a Lucide icon name (`rocket`, `book-open`) or `brand-<slug>` for
    a Simple Icons brand (`brand-github`).
    """
    name = (name or '').removeprefix('lucide-')
    aria = f' role="img" aria-label="{escape(label)}"' if label else ' aria-hidden="true"'
    classes = f'sumi-icon {cls}'.strip()
    if name.startswith('brand-'):
        path = _brands().get(name[6:])
        if path is None:
            return Markup('')
        return Markup(
            f'<svg class="{classes}" viewBox="0 0 24 24" fill="currentColor"{aria}>'
            f'<path d="{path}"/></svg>'
        )
    body = _lucide().get(name)
    if body is None:
        return Markup('')
    return Markup(
        f'<svg class="{classes}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"{aria}>{body}</svg>'
    )
