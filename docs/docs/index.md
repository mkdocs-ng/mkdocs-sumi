---
description: What Sumi is, what it includes, and where to start.
---

# Sumi documentation

Sumi is a documentation theme for [MkDocs](https://github.com/mkdocs-ng/mkdocs). It turns a folder of plain Markdown into a complete, searchable, printable website — with a home page, a blog and release notes — without Node.js, a CDN or a hosted service.

- :lucide-rocket: [Install](start/install.md)
  Add Sumi to an existing MkDocs project in two lines of configuration.
- :lucide-pen-line: [Write](write/index.md)
  Twelve components, all written in native Markdown.
- :lucide-layout-template: [Pages](pages/landing.md)
  Landing pages, a blog, release downloads and a print edition.
- :lucide-sliders-horizontal: [Customize](customize/theme.md)
  Colours, navigation, search, languages, versions and template overrides.
{.cards}

## What you get

| Area | Included |
| --- | --- |
| Reading | Top tabs, collapsible sidebar, breadcrumbs, table of contents with scroll spy, previous / next |
| Discovery | Local full-text search with CJK support, merged with a command palette (<kbd>⌘</kbd> <kbd>K</kbd>) |
| Authoring | Callouts, tabs, steps, cards, fields, captions, file trees, Mermaid, KaTeX, keys, 1 900+ icons |
| Pages | Data-driven landing page, blog with tags and Atom feed, releases with checksums, whole-site print edition |
| Outputs | HTML, print, a Markdown copy of every page, `llms.txt`, Atom |
| Operations | Dark mode, mike versions, language switcher, edit links, Git "last updated" dates, analytics |
{caption="Everything listed here ships with the theme. Nothing is fetched from the network at build or read time."}

## Principles

Sumi follows four rules. They are explained in [Design principles](design.md).

1. **Content stays Markdown.** A component is a blockquote, a list, a table or a fence with one attribute line.
2. **Everything is local.** Every font, icon and script is part of your built site.
3. **Pay only for what you use.** Diagrams and formulas load their runtime on the pages that contain them.
4. **People and agents are both readers.** Every page is published as HTML and as Markdown.
