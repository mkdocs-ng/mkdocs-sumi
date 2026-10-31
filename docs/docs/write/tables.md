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
{.compact .striped}

```markdown
{.compact .striped caption="Variants"}
```

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
