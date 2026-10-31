---
description: Install Sumi and enable it in an MkDocs project.
---

# Install

Sumi is a Python package. It depends on [MkDocs-ng](https://github.com/mkdocs-ng/mkdocs), so installing Sumi installs MkDocs too.

## Requirements

- Python 3.10 or newer
- An MkDocs project, or an empty folder

## Install the package

```sh {tab="pip"}
pip install mkdocs-sumi
```

```sh {tab="uv"}
uv add --dev mkdocs-sumi
```

```sh {tab="pipx"}
pipx install mkdocs-ng --include-deps
pipx inject mkdocs-ng mkdocs-sumi
```

## Enable the theme and the plugin

Sumi has two halves: the **theme** draws the page and the **plugin** adds the Markdown components, the blog and the extra outputs. Enable both:

```yaml title="mkdocs.yml"
theme:
  name: sumi

plugins:
  - search    # powers ⌘K search
  - llms_txt  # optional: llms.txt and a Markdown copy of every page
  - sumi
```

> [!IMPORTANT]
> When you add a `plugins:` list, MkDocs no longer enables `search` for you. List it explicitly, as above.

## Preview

```sh
mkdocs serve
```

Open <http://127.0.0.1:8000/>. Press <kbd>⌘</kbd> <kbd>K</kbd> (or <kbd>Ctrl</kbd> <kbd>K</kbd>) to search.

## Next

Continue with [Your first site](first-site.md), or jump to [Writing](../write/index.md).
