---
description: Tables with captions, full width, compact and striped variants.
---

# Tables

Tables are standard GitHub-flavoured Markdown. Sumi gives them a frame, sticky headers and horizontal scrolling on narrow screens.

| Command | Purpose |
| --- | --- |
| `mkdocs new` | Create a new project |
| `mkdocs serve` | Start a live-reloading preview |
| `mkdocs build` | Build the site |
| `mkdocs gh-deploy` | Build and deploy to GitHub Pages |

## Captions

```markdown
| Plan | Price |
| --- | --- |
| Open source | Free |
{caption="Sumi is licensed under Apache 2.0."}
```

| Plan | Price |
| --- | --- |
| Open source | Free |
{caption="Sumi is licensed under Apache 2.0."}

## Variants

Add one or more of these classes on the attribute line:

| Class | Effect |
| --- | --- |
| `.wide` | Let the table use the full width of the content area |
| `.compact` | Reduce cell padding for dense data |
| `.striped` | Shade alternate rows |
| `.center` | Centre all cells |
| `.expand` | Always offer the full-screen reader (see below) |
{.compact .striped}

```markdown
{.compact .striped caption="Variants"}
```

## Wide tables

A table wider than the column scrolls sideways, and an **Expand table** button appears under it. The button opens the table full screen, where it has the whole window and its header stays in view. Add `.expand` to offer the button on a table that fits too, like this one:

| Option | Type | Default | Applies to | Since | Description |
| --- | --- | --- | --- | --- | --- |
| `palette` | string | `auto` | every page | 0.1 | `light`, `dark` or `auto`, following the operating system until the reader picks one |
| `accent` | string | `vermilion` | links, highlights, the active tab | 0.1 | A named accent with a tuned dark variant, or any CSS colour used in both modes |
| `bilingual_view` | boolean | `true` | translated pages | 0.3 | A side-by-side view of a page and its translation, with scrolling kept in step |
| `comments` | mapping | | docs pages and blog posts | 0.3 | Giscus comments under the page, loaded only when the reader scrolls near them |
{.compact .expand}

## Alignment

Column alignment uses the standard colon syntax:

```markdown
| Left | Centre | Right |
| :--- | :---: | ---: |
| a | b | 1.00 |
```

| Left | Centre | Right |
| :--- | :---: | ---: |
| a | b | 1.00 |
| longer text | c | 120.50 |

> [!TIP]
> For option and parameter references, use [fields](fields.md) instead of a wide table.

## Reference

| What | Details |
| --- | --- |
| Output | `<div class="sumi-table">` around the `<table>`, with the variants as classes. |
| Without Sumi | A plain table. |
| JavaScript | Only for the full-screen reader. |
| Limits | Cells hold inline Markdown only. Very wide tables scroll sideways. |
{.compact}
