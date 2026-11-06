---
description: How Sumi and Material for MkDocs differ — writing, features, plugins, speed, privacy, languages and maintenance — so you can choose between them.
---

# Sumi and Material for MkDocs

[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) is the most widely used MkDocs theme, and many ideas in Sumi were first made popular by it. This page sets out where the two differ, so you can choose the one that fits your project. Both are MkDocs themes: your Markdown, `mkdocs.yml` and plugins work with either, and switching in either direction is a [two-line change](migrate.md).

Facts on this page were checked on 2026-11-06 against Sumi 0.3.1, Material for MkDocs 9.8.0 and `mkdocs-ng-material` 9.8.0. If something here is wrong or out of date, please [open an issue](https://github.com/mkdocs-ng/mkdocs-sumi/issues).

## In short

- **Choose Material** if you need its breadth: more than 60 interface languages, about 14,000 icons, code annotations, instant navigation, generated social cards, and ten years of examples, answers and plugins built around it. It is in maintenance mode, with critical fixes until 2027-05-05.
- **Choose Sumi** if you want a theme that is actively developed with [MkDocs NG](https://mkdocs-ng.org/), loads nothing from other servers, keeps components readable as plain Markdown, builds a whole project site — home page, blog, releases, print edition — in one design, and publishes every page for AI agents too.
- **Not sure?** Try Sumi on a branch: change two lines, run `mkdocs serve` and compare. Your content doesn't need to change.

## At a glance

| | Sumi | Material for MkDocs |
| --- | --- | --- |
| Package | `mkdocs-sumi` | `mkdocs-material`, or the [`mkdocs-ng-material`](https://github.com/mkdocs-ng/mkdocs-material) fork maintained for MkDocs NG |
| First release | 2026-10-31 | 2016-02-09 |
| Development | Active: new features in every minor release | Maintenance mode: critical fixes until 2027-05-05, while its authors build [Zensical](https://zensical.org/) |
| Runs on | MkDocs NG 1.9 or later | MkDocs 1.6, MkDocs NG, ProperDocs |
| Python | 3.10+ | 3.11+ (`mkdocs-ng-material`: 3.10+) |
| Components | Native Markdown: `> [!NOTE]`, numbered lists with `{.steps}`, fences with `{tab="…"}`. Also reads Material's syntax. | Python-Markdown extensions: `!!! note`, `=== "Tab"`, `<div class="grid cards" markdown>` |
| Interface languages | 13, including Arabic and Hebrew right to left | More than 60, including right to left |
| Icons | About 2,000 (Lucide and brand icons) | About 14,000 (Material Design, Font Awesome, Octicons, Simple Icons) |
| Fonts | Inter and JetBrains Mono, bundled | Any Google Font, loaded from Google by default |
| Diagrams and math | Mermaid, ECharts, mind maps and KaTeX, bundled and loaded only on pages that use them | Mermaid, loaded from `unpkg.com`; MathJax or KaTeX added by you, usually from a CDN |
| Search | A command palette with CJK substring matching; the index loads when the palette opens | lunr.js in a web worker, with word stemming for many languages, optional Chinese word segmentation (jieba), suggestions and highlighting |
| Page loads | Ordinary page loads | Optional instant navigation, which swaps pages without a full reload |
| Code blocks | Build-time highlighting, titles, line numbers, copy button (console blocks copy only the commands) | The same, plus code annotations |
| Project pages | Data-driven home page, blog with Atom feed, releases page with checksums, whole-site print edition | Blog and tags plugins; a home page through template overrides; print through the `print-site` plugin |
| Link previews | One image for the site, or one per page | The social plugin draws a card for every page |
| For AI agents | A Markdown copy of every page, linked from its HTML; *Copy as Markdown*; `llms.txt` | `llms.txt` through MkDocs NG's plugin, which works with any theme |
| Multi-language sites | MkDocs NG `languages:` with a language menu, `hreflang` links, a note on untranslated pages and a side-by-side bilingual view | A language menu through `extra.alternate`, and MkDocs NG `languages:` |
| Versions | `mike` | `mike` |
| Users | A handful of sites so far, listed in the [showcase](../../showcase.md) | About 84,000 public GitHub repositories depend on it, according to its authors |
{.wide}

## Writing

Material adds components through Python-Markdown extensions, so a page uses syntax such as `!!! warning` and `=== "Tab"`. That syntax is compact, but on GitHub or in an editor preview it shows as plain text.

Sumi writes components in Markdown's own vocabulary — a blockquote, a list, a table or a fence — with at most one line of `{…}` attributes. A callout in Sumi is a GitHub alert, so it also renders on GitHub:

```markdown
> [!WARNING]
> Back up your data before upgrading.
```

Sumi also reads Material's syntax: admonitions, `pymdownx` tabs and details, grid cards and buttons render without changes. See [What keeps working](migrate.md#what-keeps-working).

## Features only Material has

- **Code annotations**: numbered markers in a code block that open notes.
- **Instant navigation**: pages swap in place, with prefetching and a progress bar.
- **Generated social cards**: an image with the page title for every page.
- **Tags across the docs**: Sumi's tags are for blog posts only.
- **Privacy and offline plugins**: they download external assets into the site, or make it browsable from the file system. Sumi has no privacy plugin because it loads nothing from other servers to begin with.
- **More languages and icons**: more than 60 interface languages against Sumi's 13, about 14,000 icons against 2,000, and any Google Font.

## Features only Sumi has

- **A command palette**: <kbd>⌘</kbd> <kbd>K</kbd> searches every heading and runs commands such as switching language, toggling dark mode or copying the page as Markdown.
- **Project pages**: a [home page](../pages/landing.md) described in front matter, a [releases page](../pages/releases.md) with downloads and checksums read from GitHub Releases or PyPI, and a [print edition](../pages/print.md) of the whole site.
- **Docs for agents**: every page has a [Markdown copy](../ai.md) linked from its HTML, a *Copy as Markdown* button and links that open the page in an AI assistant.
- **More diagrams, all local**: ECharts charts and Markmap mind maps next to Mermaid and KaTeX, each loaded only when a page needs it.
- **Bilingual view**: a page and its translation side by side, scrolled together. See [Languages](../customize/i18n.md#bilingual-view).

## Plugins

Both themes run ordinary MkDocs plugins: mkdocstrings, macros, glightbox, awesome-nav, redirects, git-revision-date-localized and the rest.

- Plugins that style their output with Material's `--md-*` colours or `[data-md-color-scheme]` follow Sumi's palette and dark mode.
- Scripts that wait for Material's instant navigation (`document$`) need to run on `DOMContentLoaded` instead, because Sumi uses ordinary page loads.
- Material's built-in plugins — `blog`, `tags`, `social`, `privacy`, `offline`, `optimize` and the others — are part of Material and don't run with Sumi. Sumi's plugin has its own [blog](../pages/blog.md), and it reads Material's blog posts and `.authors.yml` as they are.

[For plugin authors](../customize/plugin-authors.md) explains how to support both themes.

## Speed and page weight

**Building.** In MkDocs NG's [build benchmark](https://mkdocs-ng.org/about/comparison/#build-speed), a 1,000-page site builds in 12.2 s with Sumi 0.2.0 and 11.1 s with Material. At 5,000 pages Sumi takes 67.6 s and Material 134.5 s, because Material writes the whole navigation into every page. `mkdocs serve` shows an edit after 1.8 s with Sumi and 2.7 s with Material.

**Reading.** We built the same page — headings, a code block, tabs, a table and two callouts — with each theme's default settings and loaded it in Chromium:

| | Sumi 0.3.1 | Material for MkDocs 9.8.0 |
| --- | --- | --- |
| Requests | 5 | 8 |
| Requests to other servers | 0 | 3, to Google Fonts |
| Transferred, compressed | 127 KB, of which fonts 87 KB | 149 KB, of which fonts 74 KB |
| JavaScript | 16 KB | 46 KB, including the search worker |
{caption="Measured on 2026-11-06. With <code>theme.font: false</code>, Material uses the reader's system fonts instead: 5 requests, 72 KB."}

Both are light. The difference that matters more is where the requests go: a Sumi site works the same behind a firewall or on an intranet, and readers aren't seen by a font or script CDN.

## Maintenance

Material for MkDocs is in maintenance mode: its authors have announced critical fixes until 2027-05-05 and recommend their new generator, Zensical, after that. The MkDocs NG project maintains [`mkdocs-ng-material`](https://github.com/mkdocs-ng/mkdocs-material), a fork that gets bug fixes and keeps working with new MkDocs NG releases, so existing Material sites can stay as they are.

Sumi is where new theme work in MkDocs NG happens, and it ships features that need MkDocs NG, such as one `mkdocs.yml` for every language. It is also young: it was first released on 2026-10-31 and is before 1.0, so pin the version you test with and read the [release notes](../../releases.md) before you upgrade.

## Trying Sumi

```diff title="mkdocs.yml"
 theme:
-  name: material
+  name: sumi
 plugins:
   - search
+  - sumi
```

Run `mkdocs serve` and look through your site. [Migrate from Material](migrate.md) lists what keeps working and what changes. Switching back is the same two lines: Sumi's components are plain Markdown, so a page written for Sumi still reads well with Material.
