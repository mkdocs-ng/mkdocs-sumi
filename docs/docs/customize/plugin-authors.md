---
description: How to make an MkDocs plugin, or CSS and templates written for Material for MkDocs, work well with Sumi.
---

# For plugin authors

Material for MkDocs is in maintenance mode, with critical fixes through 2027-05-05. Many plugins were written and tested only against it. This page is for their authors: what already works in Sumi, what needs a small change, and how to get your plugin listed.

Sumi is a standard MkDocs theme. A plugin that only uses MkDocs events and writes plain HTML into the page works without changes.

## Does my plugin need changes?

| Your plugin… | In Sumi |
| --- | --- |
| Uses MkDocs events and writes HTML into `page.content` | Works. |
| Ships CSS that reads `--md-*` variables | Works: Sumi maps the common ones to its own colours, in both palettes. |
| Switches its dark CSS on `[data-md-color-scheme="slate"]` | Works: Sumi sets that attribute next to its own `data-theme`. |
| Writes `!!! note` admonitions, `<details>`, tables or highlighted code | Works: Sumi styles them like its own callouts and code blocks. |
| Scopes CSS to `.md-typeset` | Change: add `.sumi-prose`, the class of Sumi's content container. |
| Runs JavaScript on `document$` (Material's instant loading) | Change: Sumi loads every page normally; run on `DOMContentLoaded`. |
| Checks `config.theme.name == "material"` | Change: accept `"sumi"` as well, or test for the feature you need. |
| Imports from the `material` package or overrides Material partials | Change: see [Templates](#templates). |

## Detect the theme

```python title="plugin.py"
def on_config(self, config):
    self.is_sumi = config.theme.name == "sumi"
```

Prefer this over checking for installed packages: a site can have Material installed and still build with Sumi.

## Styles

Rendered Markdown lives in `<div class="sumi-content sumi-prose">`. Scope your CSS to it the same way you scoped it to `.md-typeset`:

```css title="my-plugin.css"
:is(.md-typeset, .sumi-prose) .my-widget { margin: 1em 0; }
```

Use Sumi's tokens when you want an exact match, and keep Material's as the fallback so one stylesheet serves both themes:

```css
.my-widget {
  border: 1px solid var(--sumi-line, var(--md-default-fg-color--lightest));
  background: var(--sumi-bg-elev, var(--md-default-bg-color));
  color: var(--sumi-fg-2, var(--md-default-fg-color--light));
}
```

| Token | Use |
| --- | --- |
| `--sumi-fg`, `--sumi-fg-2`, `--sumi-fg-3` | Text: body, secondary, muted |
| `--sumi-bg`, `--sumi-bg-elev`, `--sumi-bg-soft`, `--sumi-bg-sunken` | Page, raised panels, subtle fills, wells |
| `--sumi-line`, `--sumi-line-2` | Borders: hairline and stronger |
| `--sumi-accent` | The accent colour chosen with `theme.accent` |
| `--sumi-link` | Links |
| `--c-note`, `--c-tip`, `--c-important`, `--c-warning`, `--c-caution` | Status colours, the same as callouts |
| `--sumi-code-bg`, `--sumi-code-inline` | Code block and inline code backgrounds |
| `--sumi-font`, `--sumi-font-mono` | Text and code fonts |
| `--sumi-radius`, `--sumi-radius-sm` | Corner radii |
{.compact}

All tokens change with the palette, so CSS that uses them needs no dark-mode rules. If you write your own, key them on `[data-theme="dark"]`.

To add your stylesheet, append it to `config.extra_css` in `on_config` and copy the file in `on_post_build`, as you would for Material. Sumi loads `extra_css` after its own CSS.

## Scripts

Sumi has no instant loading: each link is a normal page load, so a script that runs on `DOMContentLoaded` runs on every page. When the reader switches between light and dark, Sumi updates `data-theme` on `<html>` and fires an event:

```js
document.addEventListener("sumi:theme", (event) => {
  redraw(event.detail.theme);  // "light" or "dark"
});
```

`data-theme` is set before the page is drawn, so a script can read it at any time. Don't rely on Sumi's own script having run first: it is deferred.

In the [bilingual view](i18n.md#bilingual-view) a page is loaded a second time inside a frame named `sumi-pane`, with the class `sumi-pane` on `<html>`. A script that counts visits or opens a popup should skip it: `if (window.name === 'sumi-pane') return;`.

## Templates

Sumi has the usual MkDocs blocks. A plugin or user override that extends Material's `main.html` maps like this:

| Material block | In Sumi |
| --- | --- |
| `extrahead`, `htmltitle`, `site_meta`, `styles`, `analytics` | Same name |
| `scripts`, `content`, `header`, `footer` | Same name |
| `announce` | The `theme.announcement` option |
| `outdated` | Built in with `theme.version_provider: mike` |
| `tabs`, `hero` | Header tabs are built in; use a [landing page](../pages/landing.md) for a hero |
{.compact}

Sumi's partials have different names and contents from Material's; see [Template overrides](overrides.md). If your plugin replaces a Material partial, such as the "last updated" line, write the information into the page instead, or ask for a hook in an issue.

## Features Sumi already has

Some plugins exist to fill a gap that Sumi covers itself. If yours is one of them, document how it fits next to Sumi's version rather than duplicating it.

| Material plugin | In Sumi |
| --- | --- |
| `blog` | The [blog](../pages/blog.md) reads the same folder, front matter and `.authors.yml` |
| `tags` | Tags on blog posts, with filters on the index |
| `search` | MkDocs' `search` plugin, shown in Sumi's command palette |
| `privacy`, `offline` | Not needed: fonts, icons and scripts are bundled, nothing is fetched at read time |
| `social` | Not built in. Sumi writes `og:title`, `og:description` and `twitter:card`, and writes `og:image` only when `social_image` or a page `image:` is set, so a social card plugin can add its own image without duplicates |
{.compact}

## Test against Sumi

1. Build a small site with `theme: sumi` and `plugins: [search, sumi, your-plugin]`, using `mkdocs build --strict`.
2. Check the output in both palettes and on a narrow screen.
3. Open `/print/`, the [print edition](../pages/print.md), if your plugin adds content to pages.

## Get listed

[Open an issue](https://github.com/mkdocs-ng/mkdocs-sumi/issues) with your plugin's name and a screenshot of it in Sumi. Plugins that work are added to the [migration guide](../start/migrate.md#what-keeps-working). If something in Sumi stands in your way, say so in the same issue: a missing block or token is easier for us to add than for you to work around.

## Plugins Sumi styles

These plugins write HTML that Sumi styles to match the rest of the site.

### mkdocstrings

API pages from [mkdocstrings](https://mkdocstrings.github.io/) get Sumi's code font and colours: signatures, symbol badges (`mod`, `class`, `func`, `meth`, `attr`, `type`, `param`), labels, nested members, section tables and lists, parameter headings, backlinks and a quiet "Source code" panel. These options suit Sumi well:

```yaml title="mkdocs.yml"
plugins:
  - search
  - sumi
  - mkdocstrings:
      handlers:
        python:
          options:
            show_root_heading: true
            show_symbol_type_heading: true
            show_symbol_type_toc: true
            separate_signature: true
            show_signature_annotations: true
            signature_crossrefs: true
```
