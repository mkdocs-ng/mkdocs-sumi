---
date: 2026-11-01
authors: [xianpeng]
tags: [release, design]
description: Sumi 0.1 is a local-first documentation theme for MkDocs that keeps your content in plain Markdown and publishes it for people and agents alike.
---

# Introducing Sumi

Today we are releasing Sumi 0.1, a documentation theme for MkDocs NG. It is the first theme built by the MkDocs NG project, and it is meant to be a complete answer to "how should our docs look?" for engineering teams.

<!-- more -->

## Why another theme

MkDocs made documentation easy: write Markdown, run one command, get a site. Over the years, good-looking MkDocs sites came to depend on a long list of extensions, each with its own syntax. Content written for one theme stopped making sense anywhere else.

Sumi goes back to the original promise. It adds twelve components, each written in plain Markdown — a callout is a blockquote, steps are a numbered list, tabs are labelled code fences. Your source still reads well on GitHub and in a terminal.

## What is in 0.1

- :lucide-book-open: **A full docs layout** with tabs, a sidebar, an on-page table of contents and previous / next links.
- :lucide-command: **Search as a command palette**, local and CJK-aware, opened with ++Cmd+K++.
- :lucide-layout-template: **Landing, blog, releases and print** page types sharing one design.
- :lucide-sparkles: **A Markdown copy of every page** and `llms.txt` links for AI agents.
- :lucide-hard-drive: **No CDN**: fonts, icons, Mermaid and KaTeX ship with the theme.

## Try it

```sh
pip install mkdocs-sumi
```

```yaml title="mkdocs.yml"
theme:
  name: sumi
plugins:
  - search
  - sumi
```

Then read [the documentation](../../docs/index.md) — this site is built with Sumi, and every page doubles as an example. Feedback and bug reports are welcome on [GitHub](https://github.com/mkdocs-ng/mkdocs-sumi/issues).

## Thanks

Sumi's principles owe a lot to [Oink](https://github.com/pgsty/oink) by Feng Ruohang, which showed how much a documentation distribution can do with plain Markdown and no external services.
