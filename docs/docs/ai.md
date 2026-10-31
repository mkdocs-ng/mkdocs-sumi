---
description: How Sumi publishes every page for AI agents — Markdown copies, llms.txt, discovery links and one-click copying.
---

# Docs for people and agents

More and more readers of documentation are not people. Coding agents, assistants and search tools read your pages to answer questions about your project, and they read HTML badly: navigation, scripts and styling are noise to them. Sumi publishes every page twice — as a page for people and as plain Markdown for programs.

## What Sumi publishes

| Output | Where | For |
| --- | --- | --- |
| HTML page | `guide/install/` | People |
| Markdown copy | `guide/install.md` | Agents reading one page |
| `llms.txt` | site root | Agents discovering the site |
| `llms-full.txt` | site root | Agents loading everything at once (opt-in) |
| Atom feed | `blog/feed.xml` | Feed readers |
| Print edition | `print/` | Paper, PDF, offline reading |
{caption="Every output is a static file. None requires a server."}

The Markdown copy and `llms.txt` come from the `llms_txt` plugin that ships with [MkDocs-ng](https://github.com/mkdocs-ng/mkdocs). Enable it next to `sumi`:

```yaml title="mkdocs.yml"
site_url: https://example.com/docs/   # needed for absolute links in llms.txt

plugins:
  - search
  - llms_txt:
      full_output: true   # also write llms-full.txt
  - sumi
```

Try it on this site: open [llms.txt](https://mkdocs-ng.github.io/mkdocs-sumi/llms.txt), or choose **View as Markdown** in the menu at the top of this page.

## Discovery

Each HTML page announces its Markdown copy in `<head>`:

```html
<link rel="alternate" type="text/markdown" href="ai.md" title="Markdown">
<link rel="alternate" type="text/plain" href="../llms.txt" title="llms.txt">
```

An agent that lands on any page can find the clean version without guessing URLs.

## Copy as Markdown

The **Copy as Markdown** button at the top of each page copies the page source — the same text an agent reads — so you can paste it into a chat. The menu next to it can also open the Markdown copy, print the page and, if you enable it, open the page in an assistant:

```yaml title="mkdocs.yml"
plugins:
  - sumi:
      assistant_links: [claude, chatgpt]
```

> [!NOTE]
> Assistant links are off by default: they send the page address to a third-party service when clicked.

## Why native Markdown matters here

Components written in a private syntax — MDX, shortcodes, HTML widgets — reach an agent either as raw markup it has to interpret or not at all. Sumi's components are ordinary Markdown with an attribute line, so the Markdown copy reads naturally: a callout is a quote, steps are a numbered list, tabs are consecutive code blocks with labels.

Landing pages are the one place where content lives in front matter. For those pages, Sumi writes a Markdown copy that lists the hero, features, steps and questions as headings and lists.
