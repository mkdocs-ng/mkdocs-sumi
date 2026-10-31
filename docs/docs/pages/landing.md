---
description: Build a product home page from front matter — hero, features, code, stats, steps, FAQ and call to action.
---

# Landing pages

A landing page is a Markdown file with `template: landing.html`. Its sections are described in front matter, so the page stays data you can review in a diff — no HTML, no components to import. The [home page of this site](../../index.md) is one.

```yaml title="docs/index.md"
---
template: landing.html
hero:
  eyebrow: "v2.0 is out"
  title: "Ship docs<br>*people read*."
  text: One sentence that explains the product.
  actions:
    - {text: Get started, link: guide/, icon: rocket, primary: true}
    - {text: GitHub, link: "https://github.com/me/project", icon: brand-github}
  install: pip install my-project
sections:
  - type: features
    title: Why it is different
    items:
      - {icon: zap, title: Fast, text: Builds in under a second., link: guide/speed/}
      - {icon: lock, title: Private, text: Runs entirely on your machine.}
  - type: cta
    title: Ready?
    actions:
      - {text: Read the guide, link: guide/, primary: true}
---
```

Links are relative to the site root, like `nav` entries. Text fields accept inline Markdown.

## Hero

| Key | Type | Description |
| --- | --- | --- |
| `eyebrow` | string | A short label above the title, such as a release announcement. |
| `title` | string | The headline. `<br>` breaks lines; `*emphasis*` is drawn in the accent colour. Defaults to the page title. |
| `text` | string | One or two sentences under the title. Defaults to `site_description`. |
| `actions` | list | Buttons: `text`, `link`, `icon`, `primary`. |
| `install` | string | A command shown in a click-to-copy box. |
| `code` | object | A code card beside the text: `title`, `lang`, `content`. |
| `image` | string | An image beside the text, if there is no `code`. |
{.fields}

## Sections

Every entry in `sections` has a `type` and optional `eyebrow`, `title`, `text`, `id` and `tone: soft` (a tinted background).

| Type | Keys | Description |
| --- | --- | --- |
| `features` | `items`, `columns` | A grid of features, each with `icon`, `title`, `text` and an optional `link`. |
| `split` | `bullets`, `actions`, `code` or `image` or `markdown`, `reverse` | Text on one side, an illustration on the other. |
| `stats` | `items` | Big numbers: `value` and `label`. |
| `steps` | `items` | A numbered sequence: `title` and `text`. |
| `faq` | `items` | Questions and answers: `q` and `a` (Markdown). |
| `cta` | `actions` | A closing call to action. |
| `content` | | The Markdown body of the page. If `sections` is omitted, the body is shown under the hero. |
{.fields meta="keys"}

> [!TIP]
> Keep the page body for content that agents and search should see. The front-matter sections are visual; the Markdown copy of a landing page contains its title, text and body.
