---
description: Every theme option — colours, logo, header, announcement bar, page chrome and footer.
---

# Theme options

Theme options are set under `theme:` in `mkdocs.yml`. All of them are optional.

```yaml title="mkdocs.yml"
theme:
  name: sumi
  palette: auto
  accent: indigo
  logo: assets/logo.svg
  announcement: 'Sumi 0.1 is out — <a href="blog/">read the post</a>'
```

## Options

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `palette` | string | `auto` | `light`, `dark` or `auto` (follow the operating system). Readers can switch at any time; their choice is remembered. |
| `accent` | string | `vermilion` | The colour of links, highlights and the active tab: `vermilion`, `indigo`, `moss`, `plum`, `ochre`, `teal`, `ink`, or any CSS colour. |
| `locale` | string | `en` | The interface language: `en`, `zh`, `zh_TW`. See [Languages](i18n.md). |
| `logo` | string | | An image in `docs/` for the header. The Sumi mark is used if unset. |
| `favicon` | string | | An image in `docs/` for the browser tab. |
| `brand` | string | `site_name` | HTML for the header brand, e.g. `"MkDocs<b>ng</b>"`. |
| `announcement` | string | | HTML for a dismissible bar above the header. A new message reappears for readers who dismissed an older one. |
| `navigation_tabs` | boolean | `true` | Show top-level sections as tabs in the header. When `false`, the whole navigation is in the sidebar. |
| `toc_depth` | integer | `3` | The deepest heading level in the page table of contents. |
| `hide` | list | `[]` | Parts to hide on every page: `toc`, `sidebar`, `breadcrumbs`, `actions`, `pager`, `footer`. |
| `version_provider` | string | | `mike` to show a version menu. See [Navigation](navigation.md#versions). |
| `repo_icon` | string | | Override the repository icon, e.g. `brand-gitlab`. Detected from `repo_url` by default. |
| `keyboard` | boolean | `true` | Enable single-key shortcuts. <kbd>⌘</kbd> <kbd>K</kbd> always works. |
| `credit` | boolean | `true` | Show "Built with MkDocs and Sumi" in the footer. |
{.fields}

## Accent colours

| Name | Light | Dark |
| --- | --- | --- |
| `vermilion` | `#c4432b` | `#ef7258` |
| `indigo` | `#2f5d93` | `#86b4ea` |
| `moss` | `#4b6b2f` | `#9ccc6e` |
| `plum` | `#7a3b74` | `#dc93d4` |
| `ochre` | `#9a6512` | `#e7b45a` |
| `teal` | `#1f6f6a` | `#6fd0c6` |
| `ink` | `#2a2926` | `#e8e4dc` |
{.compact}

A named accent has a tuned variant for dark mode. A custom CSS colour is used in both modes.

## Per-page options

Front matter on a page can change its layout:

| Key | Description |
| --- | --- |
| `hide` | Like the theme option, for one page: `hide: [toc, pager]`. `navigation` is accepted as an alias for `sidebar`. |
| `layout` | `wide` removes both sidebars for a full-width page. |
| `template` | `landing.html`, `blog.html` or `releases.html`. See [Pages](../pages/landing.md). |
| `description` | Used for the `<meta name="description">`, link previews, cards and the blog index. |
{.fields}

## Footer and social links

```yaml title="mkdocs.yml"
copyright: © 2026 The MkDocs NG project
extra:
  social:
    - icon: brand-github
      link: https://github.com/mkdocs-ng
      name: GitHub
    - icon: fontawesome/brands/x-twitter   # Material names work too
      link: https://x.com/mkdocs
```

## Custom CSS

Every colour, font and size is a CSS variable. Add a stylesheet with `extra_css`:

```css title="docs/assets/extra.css"
:root {
  --sumi-font: "IBM Plex Sans", system-ui, sans-serif;
  --sumi-content-w: 820px;
}
[data-theme="dark"] {
  --sumi-bg: #0f1115;
}
```

```yaml title="mkdocs.yml"
extra_css:
  - assets/extra.css
```
