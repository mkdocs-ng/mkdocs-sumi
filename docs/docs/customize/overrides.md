---
description: Override templates and blocks with MkDocs' custom_dir.
---

# Template overrides

Sumi is a standard MkDocs theme, so any template can be overridden with `custom_dir`:

```yaml title="mkdocs.yml"
theme:
  name: sumi
  custom_dir: overrides
```

```filetree
overrides/
├── main.html                 # extend blocks for every page
└── partials/
    └── footer.html           # replace one partial
```

## Extending blocks

Create `overrides/main.html` and extend `base.html`:

```jinja title="overrides/main.html"
{% extends "base.html" %}

{% block extrahead %}
  <meta name="robots" content="noindex">
{% endblock %}
```

| Block | Contains |
| --- | --- |
| `site_meta` | `<meta>` and `<link>` tags in `<head>` |
| `htmltitle` | The `<title>` element |
| `styles` | Stylesheets |
| `analytics` | The analytics snippet |
| `extrahead` | Empty; for your own tags |
| `header` | The site header |
| `layout` | Sidebar, article and table of contents |
| `content` | The article |
| `page_content` | The rendered Markdown |
| `article_footer` | Last updated, edit link, previous / next |
| `footer` | The site footer |
| `scripts` | Scripts at the end of `<body>` |
{.compact}

## Partials

| Partial | Purpose |
| --- | --- |
| `partials/header.html` | Logo, tabs, search button, menus |
| `partials/logo.html` | The logo only |
| `partials/breadcrumbs.html` | The path above the title |
| `partials/page-actions.html` | Copy as Markdown and the page menu |
| `partials/toc.html` | Table of contents |
| `partials/article-footer.html` | Below the article |
| `partials/footer.html` | Site footer |
| `partials/palette.html` | Search and command palette |
| `partials/analytics.html` | Analytics |
{.compact}

## Analytics

Google Analytics is supported with the same keys as Material:

```yaml title="mkdocs.yml"
extra:
  analytics:
    provider: google
    property: G-XXXXXXXXXX
```

For another provider, add its snippet to the `analytics` block in `overrides/main.html`.

> [!NOTE]
> Analytics is the one feature that contacts a third party. It is off unless configured.
