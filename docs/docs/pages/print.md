---
description: The whole site as one printable page, and clean printing of any single page.
---

# Print edition

Sumi writes the whole site as one long page at `/print/`, in navigation order, with a cover and a table of contents. Open it and print to PDF for an offline manual. Open [this site's print edition](../../print/index.html).

Every page also prints cleanly on its own: the header, sidebars and buttons are hidden, collapsed callouts are expanded, tabs are shown one after another, and links show their address.

## How it works

The print edition is built from the same HTML as the pages, after they are rendered. Links between pages become links within the document; images and assets are rebased so they resolve from `/print/`.

## Options

```yaml title="mkdocs.yml"
plugins:
  - sumi:
      print:
        enabled: true
        path: print/
```

Use the **Print** command in the page actions menu, or press <kbd>⌘</kbd> <kbd>K</kbd> and type `> print`.

> [!TIP]
> To leave a page out of the print edition, add `print: false` to its front matter.
