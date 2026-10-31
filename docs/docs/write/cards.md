---
description: A grid of linked cards for section landing pages.
---

# Cards

A bullet list of links followed by `{.cards}` becomes a grid. The link is the card title; the text after it is the description; an inline icon at the start becomes the card icon.

```markdown
- :lucide-rocket: [Install](../start/install.md)
  Add Sumi to a project.
- :lucide-pen-line: [Write](index.md)
  Components in plain Markdown.
- :lucide-palette: [Customize](../customize/theme.md)
  Colours, fonts and layout.
{.cards}
```

- :lucide-rocket: [Install](../start/install.md)
  Add Sumi to a project.
- :lucide-pen-line: [Write](index.md)
  Components in plain Markdown.
- :lucide-palette: [Customize](../customize/theme.md)
  Colours, fonts and layout.
{.cards}

## Columns

Cards fill as many columns as fit, up to three. Set `cols` to fix the number:

```markdown
{.cards cols=2}
```

- :brand-github: [Source code](https://github.com/mkdocs-ng/mkdocs-sumi)
  Report a bug or send a pull request.
- :brand-python: [PyPI](https://pypi.org/project/mkdocs-sumi/)
  Release history and downloads.
{.cards cols=2}

## Cards without links

Items without a link render as static cards — useful for a list of features:

- :lucide-hard-drive: **Local-first**
  Every asset ships with your site.
- :lucide-zap: **Fast**
  No framework; one small script.
- :lucide-printer: **Printable**
  A whole-site print edition.
{.cards}
