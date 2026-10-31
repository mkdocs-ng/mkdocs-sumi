---
description: Draw a project layout from the output of tree, with icons and comments.
---

# File trees

A `filetree` fence turns a directory listing into a navigable tree with folder and file icons. Paste the output of `tree`, or write the structure with plain indentation.

````markdown
```filetree
my-docs/
├── docs/                 # Markdown sources
│   ├── index.md
│   ├── guide/
│   │   ├── install.md
│   │   └── usage.md
│   └── assets/
│       └── logo.svg
├── overrides/            # Template overrides (optional)
│   └── main.html
├── pyproject.toml
└── mkdocs.yml            # Site configuration
```
````

```filetree
my-docs/
├── docs/                 # Markdown sources
│   ├── index.md
│   ├── guide/
│   │   ├── install.md
│   │   └── usage.md
│   └── assets/
│       └── logo.svg
├── overrides/            # Template overrides (optional)
│   └── main.html
├── pyproject.toml
└── mkdocs.yml            # Site configuration
```

## Rules

- A name ending in `/`, or a name with children, is a folder. Click a folder to fold it.
- Text after ` # ` is a comment and is aligned in a column.
- File icons follow the extension: code, text, configuration, data, images and archives.
- Indentation by spaces works as well as box-drawing characters.

## Plain indentation

````markdown
```filetree title="Package layout"
src/
  mkdocs_sumi/
    plugin.py      # The MkDocs plugin
    theme/         # Jinja templates and assets
tests/
```
````

```filetree title="Package layout"
src/
  mkdocs_sumi/
    plugin.py      # The MkDocs plugin
    theme/         # Jinja templates and assets
tests/
```

The tree is built at build time from plain HTML `<details>` elements, so it needs no JavaScript and prints fully expanded.
