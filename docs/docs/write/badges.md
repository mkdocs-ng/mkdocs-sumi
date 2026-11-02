---
description: Small status labels next to a feature name, a version or a table cell.
---

# Badges

Put `{.badge}` right after bold or italic text to turn it into a badge. This is the standard `attr_list` syntax, so a renderer that does not know Sumi still shows the word in bold.

```markdown
## Command palette **New**{.badge .new}

| Option | Status |
| --- | --- |
| `palette` | **Stable**{.badge .tip} |
| `brand` | **Beta**{.badge .warning} |
| `legacy_nav` | **Deprecated**{.badge .deprecated} |
```

| Option | Status |
| --- | --- |
| `palette` | **Stable**{.badge .tip} |
| `brand` | **Beta**{.badge .warning} |
| `legacy_nav` | **Deprecated**{.badge .deprecated} |

## Tones

A second class picks the colour. Without one, a badge is neutral grey.

| Class | Badge |
| --- | --- |
| *(none)* | **Default**{.badge} |
| `.note`, `.info` | **Note**{.badge .note} |
| `.tip`, `.success` | **Stable**{.badge .tip} |
| `.important`, `.new` | **New**{.badge .new} |
| `.warning` | **Beta**{.badge .warning} |
| `.caution`, `.danger`, `.deprecated` | **Removed**{.badge .caution} |
| `.accent` | **Sumi**{.badge .accent} |
{.compact}

## In headings

A badge in a heading shrinks to fit, and stays out of the table of contents text.

## Version 0.2 **Latest**{.badge .tip}

```markdown
## Version 0.2 **Latest**{.badge .tip}
```
