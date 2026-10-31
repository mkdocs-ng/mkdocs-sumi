---
description: An overview of every component Sumi adds to Markdown, and the one rule they all follow.
---

# Writing with Sumi

Sumi adds twelve components to Markdown. None of them introduces new syntax that breaks on GitHub: each one is a blockquote, a list, a table, an image or a code fence, sometimes followed by a single attribute line in braces.

```markdown
1. Install the theme
2. Enable the plugin
{.steps}
```

If a renderer does not know Sumi, the reader still sees a numbered list. Sumi sees a procedure.

## Components

| Component | Written as | Page |
| --- | --- | --- |
| Callout | `> [!NOTE]`, `> [!TIP]-` | [Callouts](callouts.md) |
| Code block with title | ```` ```py title="app.py" ```` | [Code blocks](code.md) |
| Tabs | ```` ```sh {tab="Linux"} ```` | [Tabs](tabs.md) |
| Steps | ordered list + `{.steps}` | [Steps](steps.md) |
| Cards | bullet list of links + `{.cards}` | [Cards](cards.md) |
| Fields | table + `{.fields}` | [Fields](fields.md) |
| Table options | table + `{.wide}`, `{caption="…"}` | [Tables](tables.md) |
| Figure | image + `{caption="…"}` | [Images](images.md) |
| File tree | ```` ```filetree ```` | [File trees](filetree.md) |
| Diagram | ```` ```mermaid ```` | [Diagrams](diagrams.md) |
| Math | `$…$`, `$$…$$` | [Math](math.md) |
| Keys and icons | `++Ctrl+K++`, `:lucide-rocket:` | [Keys and icons](keys-icons.md) |
{.wide}

## Attribute lines

An attribute line is a paragraph that contains only `{…}` and sits directly under the block it modifies. It can carry classes, an id and key–value pairs:

```markdown
| Name | Type |
| --- | --- |
| `port` | integer |
{.fields #server-options caption="Server options"}
```

Classes that Sumi does not recognise are kept, so you can style blocks yourself in `extra_css`.

## Markdown extensions

The `sumi` plugin enables these Python-Markdown extensions for you, so they need no configuration:

- `attr_list`, `md_in_html`, `tables`, `toc` (with permalinks), `footnotes`, `def_list`, `admonition`
- `fenced_code` and `codehilite` — unless `pymdownx.superfences` and `pymdownx.highlight` are configured, in which case Sumi leaves code to them

Any other extension in `markdown_extensions` continues to work.

> [!TIP]
> Every page of this site was written with these components. Click **Copy as Markdown** at the top of a page to see its source.
