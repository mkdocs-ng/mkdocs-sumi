"""Read the parts of a Material for MkDocs configuration that have a Sumi equivalent.

A site that switches from `theme: material` keeps its `mkdocs.yml`. The keys
below mean the same thing in both themes but are written differently, so they
are translated once, before the build, instead of being ignored.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

# Material's `palette.primary` names, as a link colour that is readable on
# Sumi's light and dark backgrounds (WCAG AA, 4.5:1). Light, yellow and orange
# tones have no readable dark shade, so they use the nearest Sumi accent.
PRIMARY_COLOURS: dict[str, Any] = {
    'red': {'light': '#c62828', 'dark': '#e57373'},
    'pink': {'light': '#ad1457', 'dark': '#f06292'},
    'purple': {'light': '#6a1b9a', 'dark': '#ba68c8'},
    'deep-purple': {'light': '#4527a0', 'dark': '#9575cd'},
    'indigo': {'light': '#283593', 'dark': '#7986cb'},
    'blue': {'light': '#1565c0', 'dark': '#64b5f6'},
    'light-blue': {'light': '#01579b', 'dark': '#4fc3f7'},
    'cyan': {'light': '#006064', 'dark': '#4dd0e1'},
    'teal': {'light': '#00695c', 'dark': '#4db6ac'},
    'green': {'light': '#2e7d32', 'dark': '#81c784'},
    'light-green': {'light': '#33691e', 'dark': '#aed581'},
    'lime': 'moss',
    'yellow': 'ochre',
    'amber': 'ochre',
    'orange': 'ochre',
    'deep-orange': {'light': '#bf360c', 'dark': '#ff8a65'},
    'brown': {'light': '#4e342e', 'dark': '#a1887f'},
    'grey': {'light': '#616161', 'dark': '#bdbdbd'},
    'blue-grey': {'light': '#37474f', 'dark': '#90a4ae'},
    'black': 'ink',
}

DEFAULT_ACCENT = 'vermilion'


def _entries(palette: Any) -> list[Mapping]:
    if isinstance(palette, Mapping):
        palette = [palette]
    if not isinstance(palette, (list, tuple)):
        return []
    return [entry for entry in palette if isinstance(entry, Mapping)]


def palette_mode(palette: Any) -> str:
    """Sumi's `palette` (light, dark or auto) for a Material palette list."""
    if isinstance(palette, str):
        return palette
    entries = _entries(palette)
    if len(entries) != 1 or 'media' in entries[0]:
        # A toggle between schemes, or one that follows `prefers-color-scheme`.
        return 'auto'
    return 'dark' if entries[0].get('scheme') == 'slate' else 'light'


def palette_accent(palette: Any) -> Any:
    """The accent for a Material palette list, from its `primary` or `accent` colour."""
    for entry in _entries(palette):
        for key in ('primary', 'accent'):
            name = str(entry.get(key) or '').strip().lower().replace(' ', '-')
            if name in PRIMARY_COLOURS:
                return PRIMARY_COLOURS[name]
    return None


def adapt_theme(theme: Any, extra: Any) -> None:
    """Translate the Material keys of `theme` (and `extra`) in place."""
    palette = theme.get('palette')
    if not isinstance(palette, str):
        theme['palette'] = palette_mode(palette)
        accent = palette_accent(palette)
        if accent and theme.get('accent') == DEFAULT_ACCENT:
            theme['accent'] = accent

    features = theme.get('features')
    if isinstance(features, (list, tuple)) and theme.get('navigation_tabs') is True:
        # Without `navigation.tabs`, Material lists the whole nav in the sidebar.
        theme['navigation_tabs'] = 'navigation.tabs' in features

    version = extra.get('version') if isinstance(extra, Mapping) else None
    if isinstance(version, Mapping) and version.get('provider') and not theme.get('version_provider'):
        theme['version_provider'] = version['provider']
