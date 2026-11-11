---
description: Move an existing site from Material for MkDocs or another theme to Sumi.
---

# Migrate from Material

Sumi reads the content and most of the configuration written for Material for MkDocs. Start with a two-line change, then check [what changes](#what-changes) for anything your site uses. Still deciding? See [Sumi and Material for MkDocs](compare.md) for how the two differ.

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
| Grid cards (`<div class="grid cards" markdown>`) and `{ .md-button }` links | Drawn as Sumi cards and buttons |
| `theme.palette` | Light, dark or following the system, as set; the `primary` colour becomes Sumi's [accent](../customize/theme.md#accent-colours) |
| `theme.features` without `navigation.tabs` | The whole nav stays in the sidebar, as in Material |
| `extra.social`, `extra.alternate`, `extra.analytics` | Read as-is, including `fontawesome/brands/…` icon names |
| `mkdocstrings` API pages | Styled: signatures, symbol badges (`show_symbol_type_heading`), labels, nested members, backlinks and source panels. [Recommended options](../customize/plugin-authors.md#mkdocstrings) |
| Plugin CSS that uses Material's `--md-*` colours or `[data-md-color-scheme]` | Follows Sumi's palette and dark mode. Authors: [make your plugin work with Sumi](../customize/plugin-authors.md) |
| `print-site` plugin | Builds; Sumi also has its own [print edition](../pages/print.md) |
| `mike` versions (`extra.version.provider: mike`) | Read as-is; `theme.version_provider: mike` is the same |
| `announce` and `outdated` blocks in `overrides/main.html` | Shown in Sumi's announcement bar and old-version banner |
| Scripts that call `document$.subscribe(…)` | Run once the page has loaded |
| Blog: `blog/posts/`, `.authors.yml`, `date`, `authors`, `tags`, `<!-- more -->` | Read as-is |
| `hide: [toc, navigation]` front matter | `hide: [toc, sidebar]` |
{.wide}

## What changes

- Other `theme.features` entries are ignored. Sumi's [theme options](../customize/theme.md) cover the same ground.
- `pymdownx.emoji` set up with `emoji_index: !!python/name:material.extensions.emoji.twemoji` needs Material installed, or the build stops. Remove the `emoji_index` and `emoji_generator` lines and write icons as `:lucide-name:` or `:brand-name:` ([keys and icons](../write/keys-icons.md)); `:material-…:` and `:octicons-…:` then show as text.
- Material's own plugins, `blog`, `tags`, `social`, `privacy` and `offline`, are part of Material: remove them from `plugins`. Sumi's [blog](../pages/blog.md) reads Material's posts, Sumi loads nothing from other servers, and `theme.social_image` sets the image for shared links.
- Code annotations (`# (1)!`) and the `[TAGS]` marker are not supported yet: an annotation shows as a code comment followed by its list.
- Material's partials, such as `partials/copyright.html`, aren't used by Sumi. See [overriding templates](../customize/overrides.md) for Sumi's.
- Material Insiders features are not emulated.

> [!NOTE]
> If a page looks wrong after switching, [open an issue](https://github.com/mkdocs-ng/mkdocs-sumi/issues) with the Markdown that causes it.
