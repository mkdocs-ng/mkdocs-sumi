---
description: What Sumi does that Material for MkDocs doesn't, where Material is still ahead, and how to switch.
---

# Sumi and Material for MkDocs

[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) is by far the most widely used MkDocs theme. Sumi is newer: it is built for [MkDocs NG](https://mkdocs-ng.org/) and does several things Material doesn't. This page shows where Sumi is ahead, where Material still is, and how to try Sumi on your site. Your Markdown, `mkdocs.yml` and plugins work with both, and switching [starts with a two-line change](migrate.md).

Facts on this page were checked on 2026-11-06 against Sumi 0.3.1, Material for MkDocs 9.8.0 and `mkdocs-ng-material` 9.8.0. If something here is wrong or out of date, please [open an issue](https://github.com/mkdocs-ng/mkdocs-sumi/issues).

## Where Sumi is ahead

### Actively developed

Sumi gets new features in every minor release and is developed together with MkDocs NG, so it is the first theme to use new MkDocs NG features such as one `mkdocs.yml` for every language. Material for MkDocs is in maintenance mode: its authors provide critical fixes until 2027-05-05 and now build a new generator, [Zensical](https://zensical.org/), instead.

If you want to stay on Material, the MkDocs NG project maintains a fork, [`mkdocs-ng-material`](https://github.com/mkdocs-ng/mkdocs-material), which gets bug fixes and keeps working with new MkDocs NG releases, but no new features.

### Nothing loaded from other servers

Fonts, 2,000 icons, search, Mermaid, ECharts, mind maps and KaTeX are part of the theme and copied into your site. A Sumi site makes no requests to other servers unless you configure them, so it works the same behind a firewall, on an intranet or offline, and readers aren't seen by a font or script CDN. With default settings, Material loads its fonts from Google Fonts and Mermaid from `unpkg.com`, and its docs suggest a CDN for MathJax or KaTeX.

We built the same page — headings, a code block, tabs, a table and two callouts — with each theme's default settings and loaded it in Chromium:

| | Sumi 0.3.1 | Material for MkDocs 9.8.0 |
| --- | --- | --- |
| Requests | 5 | 8 |
| Requests to other servers | 0 | 3, to Google Fonts |
| Transferred, compressed | 128 KB, of which fonts 87 KB | 149 KB, of which fonts 74 KB |
| JavaScript | 17 KB | 46 KB, including the search worker |
{caption="Measured on 2026-11-06. With <code>theme.font: false</code>, Material uses the reader's system fonts instead: 5 requests, 72 KB."}

### Components that are still Markdown

Material adds components through Python-Markdown extensions, with syntax such as `!!! warning` and `=== "Tab"`. On GitHub or in an editor preview, that shows as plain text.

Sumi writes every component in Markdown's own vocabulary — a blockquote, a list, a table or a fence — with at most one line of `{…}` attributes. A callout is a GitHub alert, so it renders on GitHub too:

```markdown
> [!WARNING]
> Back up your data before upgrading.
```

Your pages stay readable wherever they are opened, and they don't lock you into Sumi. Sumi also reads Material's syntax, so existing pages render without changes.

### A whole project site, not only docs

Sumi's plugin builds the pages a project needs besides its docs, in the same design:

- a [home page](../pages/landing.md) described in front matter: hero, features, code, stats, steps and FAQ, with no HTML;
- a [blog](../pages/blog.md) with authors, tags, reading time, card layout and an Atom feed;
- a [releases page](../pages/releases.md) with downloads and SHA-256 checksums, read from a YAML file, GitHub Releases or PyPI;
- a [print edition](../pages/print.md) of the whole site.

Material has a blog plugin; a home page needs template overrides, a feed needs the `mkdocs-rss-plugin`, and printing the whole site needs the `print-site` plugin.

### Built for AI agents

Every Sumi page is also published as Markdown, linked from the HTML page so agents can find it, with a *Copy as Markdown* button and links that open the page in an AI assistant. Together with `llms.txt`, coding agents and assistants read your docs without the navigation and scripts in their way. See [Docs for people and agents](../ai.md). Material has none of this built in; MkDocs NG's `llms_txt` plugin works with both.

### Multi-language sites

With MkDocs NG, one `mkdocs.yml` holds every language. Sumi adds a language menu that links to the same page in each language, `hreflang` links for search engines, a note on pages that aren't translated yet, and a [bilingual view](../customize/i18n.md#bilingual-view) that shows a page and its translation side by side, scrolled together. Chinese, Japanese and Korean get their own typography, and search matches them by substring.

### Faster on large sites

In MkDocs NG's [build benchmark](https://mkdocs-ng.org/about/comparison/#build-speed), a 5,000-page site builds in 67.6 s with Sumi and 134.5 s with Material, because Material writes the whole navigation into every page. At 1,000 pages the two are close: 12.2 s and 11.1 s. `mkdocs serve` shows an edit after 1.8 s with Sumi and 2.7 s with Material.

### More diagrams, loaded only when needed

Next to Mermaid and KaTeX, Sumi has [ECharts charts and Markmap mind maps](../write/charts.md). Each runtime is loaded only on pages that use it, Mermaid only when a diagram scrolls near the viewport, and only the code for that diagram type.

### Search as a command palette

<kbd>⌘</kbd> <kbd>K</kbd> searches every heading, including Chinese and Japanese text, and runs commands: switch language, toggle dark mode, copy the page as Markdown, open the bilingual view. The search index loads only when the palette opens.

### Python 3.10

Sumi supports Python 3.10 and later. Material for MkDocs 9.8.0 requires Python 3.11.

## Where Material is ahead

- **Users.** Material has many times more downloads, and about 84,000 public GitHub repositories depend on it, according to its authors. That means more examples, answers and plugins tested against it. Sumi was first released on 2026-10-31.
- **Breadth.** More than 60 interface languages against Sumi's 15, about 14,000 icons against 2,000, and any Google Font.
- **Features Sumi doesn't have:** code annotations, instant navigation without full page loads, a social card generated for every page, and tags across docs pages (Sumi's tags are for blog posts).

If your site depends on these, Material, or `mkdocs-ng-material` on MkDocs NG, is the better fit today.

## At a glance

| | Sumi | Material for MkDocs |
| --- | --- | --- |
| Development | Active | Maintenance mode, critical fixes until 2027-05-05 |
| Loads from other servers by default | Nothing | Google Fonts; Mermaid from `unpkg.com` |
| Component syntax | Native Markdown, renders on GitHub; also reads Material's | Python-Markdown extensions |
| Project pages | Home page, blog with feed, releases with checksums, print edition | Blog; the rest through overrides and plugins |
| For AI agents | Markdown copy of every page, *Copy as Markdown*, `llms.txt` | `llms.txt` through MkDocs NG |
| Multi-language | Language menu, `hreflang`, untranslated-page note, bilingual view | Language menu |
| Diagrams | Mermaid, ECharts, mind maps, KaTeX, all bundled | Mermaid from a CDN; math added by you |
| Search | Command palette, CJK substring matching | lunr.js with stemming, suggestions, optional Chinese segmentation |
| 5,000-page build | 67.6 s | 134.5 s |
| Python | 3.10+ | 3.11+ (`mkdocs-ng-material`: 3.10+) |
| Interface languages | 15, including right to left | More than 60, including right to left |
| Icons | About 2,000 | About 14,000 |
| Code annotations, instant navigation, generated social cards | No | Yes |
| Runs on | MkDocs NG 1.9+ | MkDocs 1.6, MkDocs NG, ProperDocs |
| First release | 2026-10-31 | 2016-02-09 |
{.wide}

## Plugins

Both themes run ordinary MkDocs plugins: mkdocstrings, macros, glightbox, awesome-nav, redirects, git-revision-date-localized and the rest.

- Plugins that style their output with Material's `--md-*` colours or `[data-md-color-scheme]` follow Sumi's palette and dark mode.
- Scripts that wait for Material's instant navigation (`document$`) need to run on `DOMContentLoaded` instead, because Sumi uses ordinary page loads.
- Material's built-in plugins — `blog`, `tags`, `social`, `privacy`, `offline` and the others — are part of Material and don't run with Sumi. Sumi's own blog reads Material's blog posts and `.authors.yml` as they are, and Sumi doesn't need a privacy plugin because it loads nothing from other servers.

[For plugin authors](../customize/plugin-authors.md) explains how to support both themes.

## Try Sumi

```diff title="mkdocs.yml"
 theme:
-  name: material
+  name: sumi
 plugins:
   - search
+  - sumi
```

Run `mkdocs serve` and look through your site. [Migrate from Material](migrate.md) lists what keeps working and what changes. Sumi is before 1.0, so pin the version you test with and read the [release notes](../../releases.md) before you upgrade.
