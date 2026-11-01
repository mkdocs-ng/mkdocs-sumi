---
description: Move an existing site from Material for MkDocs or another theme to Sumi.
---

# Migrate from Material

Sumi reads the content and most of the configuration written for Material for MkDocs. Switching is usually a two-line change.

```diff title="mkdocs.yml"
 theme:
-  name: material
+  name: sumi
 plugins:
   - search
+  - sumi
```

## What keeps working

| You use | In Sumi |
| --- | --- |
| `admonition`, `!!! note` and `??? note` | Styled as callouts, same colours as `> [!NOTE]` |
| `pymdownx.details`, `pymdownx.tabbed` (alternate style) | Styled natively |
| `pymdownx.superfences`, `pymdownx.highlight` | Supported; Sumi then leaves highlighting to them |
| `pymdownx.arithmatex` | Rendered with the bundled KaTeX |
| `pymdownx.keys` | Kept; Sumi's own `++Ctrl+K++` steps aside |
| `extra.social`, `extra.alternate`, `extra.analytics` | Read as-is, including `fontawesome/brands/…` icon names |
| `mkdocstrings` API pages | Styled: signatures, symbol badges (`show_symbol_type_heading`), labels and nested members |
| `mike` versions | `theme.version_provider: mike` |
| Blog: `blog/posts/`, `.authors.yml`, `date`, `authors`, `tags`, `<!-- more -->` | Read as-is |
| `hide: [toc, navigation]` front matter | `hide: [toc, sidebar]` |
{.wide}

## What changes

- Material's `theme.features` and `theme.palette` lists are ignored. Use [theme options](../customize/theme.md) instead.
- Icons written as `:material-…:` or `:octicons-…:` need the `pymdownx.emoji` extension as before. Sumi's own inline icons are `:lucide-name:` and `:brand-name:`.
- Material Insiders features are not emulated.

> [!NOTE]
> If a page looks wrong after switching, [open an issue](https://github.com/mkdocs-ng/mkdocs-sumi/issues) with the Markdown that causes it.
