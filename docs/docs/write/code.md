---
description: Syntax-highlighted code blocks with file names, line numbers and a copy button.
---

# Code blocks

Fenced code blocks are highlighted at build time by Pygments. Every block gets a copy button; no JavaScript highlighter is shipped.

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

## File names

Add `title="…"` after the language to show a file name above the code:

````markdown
```toml title="pyproject.toml"
[project]
name = "my-docs"
dependencies = ["mkdocs-sumi"]
```
````

```toml title="pyproject.toml"
[project]
name = "my-docs"
dependencies = ["mkdocs-sumi"]
```

## Line numbers and highlighted lines

These options come from Python-Markdown's `codehilite`, or from `pymdownx.highlight` if you use it:

````markdown
```python hl_lines="2 3"
def total(items):
    subtotal = sum(i.price for i in items)
    return subtotal * 1.2
```
````

```python hl_lines="2 3"
def total(items):
    subtotal = sum(i.price for i in items)
    return subtotal * 1.2
```

To show line numbers on every block, configure the extension:

```yaml title="mkdocs.yml"
markdown_extensions:
  - codehilite:
      linenums: true
```

## Shell sessions

Use `console` for transcripts with prompts and output. The copy button then copies only the commands — without the `$` prompts and without the output.

```console
$ mkdocs build
INFO    -  Building documentation to directory: site
INFO    -  Documentation built in 0.42 seconds
```

## Diffs

```diff
 theme:
-  name: mkdocs
+  name: sumi
```

## Inline code

Write inline code with single backticks: `mkdocs serve`. In prose, Sumi gives inline code a quiet background that works in light and dark mode.

> [!TIP]
> To show tabs with one variant per operating system or language, see [Tabs](tabs.md).
