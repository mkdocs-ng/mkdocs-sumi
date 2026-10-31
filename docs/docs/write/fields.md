---
description: Reference tables for options, parameters and API fields.
---

# Fields

Configuration options and API parameters are usually written as a table, and tables become hard to read once descriptions grow. Add `{.fields}` and Sumi turns each row into a reference entry: the name and its type, default and *required* flag on one line, the description underneath.

```markdown
| Name | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `site_name` | string | | yes | The title of the site, used in the header and in every page title. |
| `site_url` | string | `null` | | The canonical address of the built site. Required for the sitemap, the feed and `llms.txt`. |
| `strict` | boolean | `false` | | Stop the build on any warning, such as a broken link. |
{.fields}
```

| Name | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `site_name` | string | | yes | The title of the site, used in the header and in every page title. |
| `site_url` | string | `null` | | The canonical address of the built site. Required for the sitemap, the feed and `llms.txt`. |
| `strict` | boolean | `false` | | Stop the build on any warning, such as a broken link. |
{.fields}

## Which columns are metadata

The first column is always the name. Columns headed **Type**, **Default** and **Required** (or **类型**, **默认值**, **必填**) become chips next to it. Every other column becomes part of the description.

To choose the metadata columns yourself, list their headings in `meta`:

```markdown
{.fields meta="type since"}
```

| Field | Type | Since | Description |
| --- | --- | --- | --- |
| `id` | integer | 1.0 | Unique identifier of the release. |
| `assets` | list | 1.2 | Files attached to the release, with their size and SHA-256 checksum. |
{.fields meta="type since"}

## Linking to a field

Each entry keeps the content of its name cell, so you can add an anchor with `attr_list`:

```markdown
| `strict`{#strict} | boolean | `false` | Stop on warnings. |
```

The Markdown copy of the page keeps the original table.
