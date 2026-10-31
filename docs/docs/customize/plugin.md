---
description: Options of the sumi plugin — components, blog, print edition, Git dates and AI links.
---

# Plugin options

The `sumi` plugin adds the Markdown components, the blog, the print edition, the Markdown copy button and Git dates. The theme needs it; you can use it without options.

```yaml title="mkdocs.yml"
plugins:
  - search
  - llms_txt
  - sumi:
      git_dates: true
      assistant_links: [claude, chatgpt]
```

## Options

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `language` | string | `theme.locale` | Language of default callout titles and generated text. |
| `math` | boolean | `true` | Parse `$…$` and `$$…$$` and load KaTeX on pages that use them. |
| `mermaid` | boolean | `true` | Render `mermaid` fences and load Mermaid on pages that use them. |
| `markdown_copy` | boolean | `true` | Show **Copy as Markdown** and **View as Markdown** when a Markdown copy of the page exists. |
| `assistant_links` | list | `[]` | Add "Open in Claude" or "Open in ChatGPT" to the page menu: `claude`, `chatgpt`. Off by default, because they send the page address to a third party. |
| `git_dates` | boolean | `false` | Show "Last updated" from the last Git commit that touched each page. One `git log` runs per build. |
| `blog.enabled` | boolean | `true` | Treat files under `blog.dir` as posts. |
| `blog.dir` | string | `blog` | The blog folder under `docs/`. |
| `blog.feed` | boolean | `true` | Write an Atom feed to `blog/feed.xml`. |
| `blog.feed_items` | integer | `20` | Number of posts in the feed. |
| `blog.authors` | mapping | `{}` | Authors, if you prefer not to use `.authors.yml`. |
| `print.enabled` | boolean | `true` | Write the [print edition](../pages/print.md). |
| `print.path` | string | `print/` | Where to write it. |
{.fields}

## Markdown extensions

The plugin enables a small set of Python-Markdown extensions that the components rely on. They are listed in [Writing](../write/index.md#markdown-extensions). Your own `markdown_extensions` entries take precedence: if you configure one of them with options, your options are used.

## Git dates in CI

Shallow clones only contain the last commit, which makes every page look updated today. Fetch the full history before building:

```yaml title=".github/workflows/docs.yml"
- uses: actions/checkout@v5
  with:
    fetch-depth: 0
```
