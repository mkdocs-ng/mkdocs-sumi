---
description: Local full-text search, CJK support, and the command palette.
---

# Search

Press <kbd>⌘</kbd> <kbd>K</kbd>, <kbd>Ctrl</kbd> <kbd>K</kbd> or <kbd>/</kbd> anywhere to search. Search runs in the browser against an index built by MkDocs' `search` plugin; nothing is sent to a server.

```yaml title="mkdocs.yml"
plugins:
  - search
  - sumi
```

## How results are ranked

- Every page and every section heading is a result, so a match takes you straight to the right place.
- Matches in titles rank above matches in text; a title that starts with your query ranks highest.
- All words must match. Matching words are highlighted in the result and in a snippet of the text.

The index is loaded the first time the palette opens, not with the page.

## Chinese, Japanese and Korean

Text in CJK scripts has no spaces between words, so word-based search finds nothing. Sumi matches CJK text as substrings: searching for `安装` finds *安装指南* and *如何安装*. Mixed queries such as `mkdocs 主题` are split into a Latin term and a CJK term.

## Commands

The palette is also a command launcher. Type `>` (or press <kbd>></kbd> on a page) to list commands only:

| Command | Action |
| --- | --- |
| Toggle dark mode | Switch between light and dark (<kbd>t</kbd>) |
| Copy page as Markdown | Copy the Markdown source of the page |
| View page as Markdown | Open the Markdown copy in a new tab |
| Edit this page | Open the page in your repository |
| Print | Print the current page |
| Go to top / Go home | Navigate |
| Switch language / version | When `extra.alternate` or versions are configured |
| Open llms.txt | When the `llms_txt` plugin is enabled |

Press <kbd>?</kbd> to see every keyboard shortcut.

## Excluding pages

Use the standard `search` front matter to keep a page out of the index:

```yaml
---
search:
  exclude: true
---
```
