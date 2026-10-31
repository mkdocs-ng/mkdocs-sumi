"""Parse `{...}` attribute lines such as `{.steps}` or `{.fields meta="type default"}`."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# A line that holds nothing but an attribute list.
ATTR_LINE_RE = re.compile(r'^\{:?\s*((?:[.#][\w-]+|[\w-]+=(?:"[^"]*"|\'[^\']*\'|[^\s}]+))(?:\s+(?:[.#][\w-]+|[\w-]+=(?:"[^"]*"|\'[^\']*\'|[^\s}]+)))*)\s*\}\s*$')

_TOKEN_RE = re.compile(r'([.#][\w-]+)|([\w-]+)=("[^"]*"|\'[^\']*\'|[^\s}]+)')


@dataclass
class Attrs:
    id: str | None = None
    classes: list[str] = field(default_factory=list)
    values: dict[str, str] = field(default_factory=dict)

    def has(self, cls: str) -> bool:
        return cls in self.classes


def parse_attrs(text: str) -> Attrs:
    """Parse the inside of an attribute list (without the braces)."""
    attrs = Attrs()
    for m in _TOKEN_RE.finditer(text):
        if m.group(1):
            token = m.group(1)
            if token[0] == '.':
                attrs.classes.append(token[1:])
            else:
                attrs.id = token[1:]
        else:
            value = m.group(3)
            if value[:1] in ('"', "'"):
                value = value[1:-1]
            attrs.values[m.group(2)] = value
    return attrs


def match_attr_line(text: str) -> Attrs | None:
    """Return the parsed attributes if `text` is a lone attribute list."""
    m = ATTR_LINE_RE.match(text.strip())
    if not m:
        return None
    return parse_attrs(m.group(1))
