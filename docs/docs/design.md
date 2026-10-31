---
description: The principles behind Sumi, and the trade-offs they lead to.
---

# Design principles

*Sumi* (墨) is the ink of East Asian painting and calligraphy. One ink, ground to different strengths, produces every shade on the page. The theme follows the same idea: warm paper, black ink, a single vermilion accent like a seal, and nothing that does not carry information.

## Content stays Markdown

Documentation outlives the tools that render it. A page written for Sumi must still make sense on GitHub, in an editor and in a terminal, so every component is written in Markdown's own vocabulary — blockquotes, lists, tables, images and fences — with at most one `{…}` line of attributes. If you leave Sumi tomorrow, your content leaves with you.

This rules out shortcodes, MDX and inline HTML widgets, and it is why the component set is small. Each component exists because technical documentation needs it often: warnings, procedures, alternatives, references, layouts and diagrams.

## Everything is local

A built Sumi site makes no network requests that you did not configure. Fonts (Inter and JetBrains Mono), 2 000 icons, the search index, Mermaid and KaTeX are part of the theme and copied into your site. That means:

- the site works behind a firewall, on an intranet and from a USB stick;
- readers are not tracked by a font or script CDN;
- a build today and a build in five years produce the same page.

## Pay only for what you use

The core of the theme is one stylesheet and one script with no framework. Heavier runtimes are loaded on demand: Mermaid only on pages with a diagram, KaTeX only on pages with a formula, the search index only when the palette is opened. Vendor files are copied into the site only if some page uses them.

## Degrade gracefully

Every page is readable without JavaScript: navigation is links, collapsible sections are `<details>`, tabs show one after another, file trees are nested lists. JavaScript adds convenience — search, tab sync, copy buttons, scroll spy — never content.

## People and agents are both readers

Every page is published as HTML for people and as Markdown for programs, and each HTML page links to its Markdown twin. See [Docs for people and agents](ai.md).

## One design language

Docs, blog, landing page, release downloads and print share one set of tokens: type scale, spacing, colours and components. A project site built with Sumi looks like one product, not a docs theme with a marketing page bolted on.

## Credits

Sumi's principles were inspired by [Oink](https://github.com/pgsty/oink), a documentation distribution for Hugo by Feng Ruohang, and by the long tradition of MkDocs themes — especially [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), whose configuration Sumi reads so that existing sites can switch. Sumi's code and design are its own.
