---
template: landing.html
title: Sumi
description: A modern, local-first documentation theme for MkDocs.
hero:
  eyebrow: "Sumi 0.1 · local-first · for MkDocs"
  title: "Markdown in.<br>*Beautiful docs* out."
  text: "Sumi is a documentation theme for MkDocs that keeps your content plain Markdown, ships every asset with your site, and writes pages that people *and* AI agents can read."
  actions:
    - {text: Get started, link: docs/start/install/, icon: rocket, primary: true}
    - {text: See the components, link: docs/write/, icon: blocks}
  install: pip install mkdocs-sumi
  code:
    title: mkdocs.yml
    lang: yaml
    content: |
      site_name: My Project

      theme:
        name: sumi          # paper, ink and a vermilion seal

      plugins:
        - search            # ⌘K search, CJK-aware
        - llms_txt          # a Markdown copy of every page
        - sumi              # components, blog, print edition
sections:
  - type: features
    eyebrow: Why Sumi
    title: Everything engineering docs need. Nothing they don't.
    text: Built in, kept local, and loaded only on the pages that use it.
    items:
      - icon: file-text
        title: Components in plain Markdown
        text: "Callouts are `> [!NOTE]`, steps are a list with `{.steps}`, tabs are fences with `{tab=…}`. Your source still reads well on GitHub."
        link: docs/write/
      - icon: hard-drive
        title: Local-first, no CDN
        text: Fonts, icons, search, Mermaid and KaTeX ship with the theme. Build offline, host anywhere, keep working behind a firewall.
        link: docs/design/
      - icon: sparkles
        title: Written for agents too
        text: "Every page has a clean `.md` twin, announced in its `<head>`. The site has an `llms.txt`. One click copies a page as Markdown."
        link: docs/ai/
      - icon: command
        title: Search that is also a command palette
        text: "Press ⌘K to search every heading — including Chinese and Japanese — or type `>` to switch theme, copy, print and more."
        link: docs/customize/search/
      - icon: layout-template
        title: Docs, blog, landing, releases
        text: One design language for the whole project site, from a data-driven home page to an RSS-ready blog and a download page.
        link: docs/pages/landing/
      - icon: puzzle
        title: Keeps your MkDocs content
        text: "Admonitions, `pymdownx` tabs and details, `mike` versions and Material's `extra` keys all keep working."
        link: docs/start/migrate/
  - type: split
    eyebrow: Native Markdown
    title: Write it once. Read it anywhere.
    text: "Sumi never asks you to write a private dialect. Each component is a blockquote, a list, a table or a fence with one attribute line — so the same file renders in Sumi, on GitHub, and in the Markdown copy an agent reads."
    bullets:
      - "No MDX, no shortcodes, no imports in your pages."
      - "Every component degrades to readable Markdown and prints fully expanded."
      - "Mermaid and KaTeX load only on pages that contain a diagram or a formula."
    code:
      title: docs/install.md
      lang: markdown
      content: |
        > [!TIP]
        > Use a virtual environment.

        1. Install the theme
        2. Enable the plugin
        3. Run `mkdocs serve`
        {.steps}

        ```sh {tab="Linux"}
        pip install mkdocs-sumi
        ```

        ```powershell {tab="Windows"}
        py -m pip install mkdocs-sumi
        ```
  - type: stats
    items:
      - {value: "0", label: "runtime services or CDNs"}
      - {value: "12", label: "native-Markdown components"}
      - {value: "9 KB", label: "core script, gzipped. No framework."}
      - {value: "2", label: "interface languages: English, 中文"}
  - type: steps
    eyebrow: Three minutes
    title: From empty folder to a published site.
    items:
      - title: Install
        text: "`pip install mkdocs-sumi` — it brings MkDocs with it."
      - title: Configure
        text: "Set `theme: sumi` and add the `sumi` plugin to `mkdocs.yml`."
      - title: Write
        text: "Run `mkdocs serve` and write Markdown. Sumi takes care of the rest."
      - title: Publish
        text: "`mkdocs build` produces plain static files for any host."
  - type: cta
    title: Your docs deserve good paper.
    text: Sumi is free and open source under the Apache 2.0 license.
    actions:
      - {text: Read the docs, link: docs/, primary: true}
      - {text: Star on GitHub, link: "https://github.com/mkdocs-ng/mkdocs-sumi", icon: brand-github}
---
