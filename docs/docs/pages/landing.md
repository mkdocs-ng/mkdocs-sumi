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

A link to a Markdown file, such as `guide.md` or `guide/speed.md#cache`, leads to the page built from it. Like a Markdown link, it is relative to the landing page, and the build warns when the file doesn't exist. Other links are relative to the site root, like `nav` entries. Text fields accept inline Markdown, and a Markdown link in them, such as `[the guide](guide.md)`, works the same way.

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
| `badges` | list | Small labels under the text: a string, or `text` and `tone` (`tip`, `note`, `warning`, `caution`, `important`, `accent`). |
{.fields}

## Sections

Every entry in `sections` has a `type` and optional `eyebrow`, `title`, `text`, `id` and `tone`: `soft` for a tinted background, `dark` for a dark band. Any section can also take `markdown`, shown below it, and `actions`, buttons below that.

| Type | Keys | Description |
| --- | --- | --- |
| `features` | `items`, `columns` | A grid of features, each with `icon`, `title`, `text` and an optional `link`. See [Product cards](#product-cards) for badges, check lists and buttons. |
| `split` | `bullets`, `actions`, `code` or `image` or `markdown`, `reverse` | Text on one side, an illustration on the other. |
| `stats` | `items` | Big numbers: `value`, `label` and an optional `link`. |
| `steps` | `items` | A numbered sequence: `title` and `text`. |
| `faq` | `items` | Questions and answers: `q` and `a` (Markdown). |
| `cta` | `actions` | A closing call to action. |
| `pricing` | `items` | Plans or services: `name`, `price`, `note`, `text`, `bullets`, `actions` and `featured: true` for the one to highlight. |
| `posts` | `limit` | The latest posts of the [blog](blog.md), 3 by default. |
| `markdown` | `markdown` | Any Markdown: a table, a picture, a callout. |
| `content` | `toc`, `aside` | The Markdown body of the page. If `sections` is omitted, the body is shown under the hero. With `toc: true` it is laid out like a docs page, beside its table of contents; `aside` adds a template from your `custom_dir` under that table of contents. |
| `include` | `template` | A template of your own from `custom_dir`, such as `partials/demo.html`, under the section's heading. It sees the page and the theme's helpers, like any override. |
{.fields meta="keys"}

Every section also takes `class`, extra CSS classes for its `<section>`, to style one section from your own stylesheet.

### A specification on the home page

A project whose home page is its document, such as a specification, keeps the hero and gets the docs layout for the body:

```yaml title="docs/index.md"
---
template: landing.html
hero:
  title: My Spec
  actions:
    - {text: Read the specification, link: "#spec", primary: true}
sections:
  - {type: content, toc: true, id: spec}
  - {type: include, template: partials/playground.html, title: Try it}
---
```

## Product cards

A product or service site needs more than an icon and a sentence per card. A `features` item can also carry:

| Key | Description |
| --- | --- |
| `mark` | Short text in the icon tile instead of an icon, such as `"8"` or `AIX`. |
| `meta` | A line under the title in monospace, such as the repository and licence. |
| `badges` | Status labels, like the hero's `badges`. |
| `bullets` | A check list. |
| `actions` | Buttons. A card with buttons is not itself a link. |
{.fields}

```yaml
sections:
  - type: features
    columns: 2
    items:
      - title: Agent8 for Jenkins
        mark: "8"
        meta: keelinfra/agent8 · MIT
        badges: [{text: Available, tone: tip}, Free]
        text: Run Jenkins agents on hosts stuck on Java 8.
        bullets: [Tested in CI on Linux, One install script]
        actions:
          - {text: Explore, link: jenkins/index.md, primary: true}
          - {text: GitHub, link: "https://github.com/keelinfra/agent8", icon: brand-github}
  - type: pricing
    title: Find out before you roll out
    items:
      - name: Plugin check
        price: $1,500
        note: fixed price
        bullets: [A written report within ten business days]
        actions: [{text: Ask for a check, link: "mailto:hello@example.com"}]
  - type: steps
    tone: dark
    title: How every product works
    items:
      - {title: Open source first, text: The code and tests are public.}
  - type: posts
    title: From the blog
    actions: [{text: All posts, link: blog/index.md}]
```

[keelinfra.io](https://keelinfra.io/) is built this way.

> [!TIP]
> Keep the page body for content that agents and search should see. The front-matter sections are visual; the Markdown copy of a landing page contains its title, text and body.
