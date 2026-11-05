---
description: Publish a Sumi site to GitHub Pages, Cloudflare Pages, Netlify or any static host.
---

# Deploy

A Sumi site is a folder of static files. `mkdocs build` writes it to `site/`, and any web server or static host can serve it: there is no server-side code, no database and no Node.js step.

```sh
mkdocs build --strict
```

`--strict` stops the build on any warning, such as a broken link or an invalid chart, so problems surface before readers see them. Use it in CI.

## Pin your versions

Builds on a host should use the same versions as your machine. Keep them in a file next to `mkdocs.yml`:

```text title="requirements.txt"
mkdocs-sumi==0.2.1
mkdocs-ng==1.11.0
```

Update the pins when you [upgrade](upgrade.md).

## GitHub Pages

The recommended way is a GitHub Actions workflow that builds the site and publishes it with GitHub's own Pages actions. In the repository's **Settings → Pages**, set **Source** to **GitHub Actions**, then add:

```yaml title=".github/workflows/docs.yml"
name: docs
on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
        with:
          fetch-depth: 0          # full history, for "Last updated" dates
      - uses: actions/setup-python@v7
        with:
          python-version: "3.13"
          cache: pip
      - run: pip install -r requirements.txt
      - run: mkdocs build --strict
      - if: github.event_name == 'push'
        uses: actions/upload-pages-artifact@v5
        with:
          path: site

  deploy:
    if: github.event_name == 'push'
    needs: build
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v5
```

Pull requests are built and checked but not published. Pushes to `main` go live a minute or two later.

`mkdocs gh-deploy` still works if you prefer a `gh-pages` branch: it builds the site and force-pushes it to that branch. Set **Source** to **Deploy from a branch** in that case.

## Cloudflare Pages

Connect the repository in the Cloudflare dashboard (**Workers & Pages → Create → Pages**) and use:

| Setting | Value |
| --- | --- |
| Build command | `pip install -r requirements.txt && mkdocs build --strict` |
| Build output directory | `site` |
| Environment variable | `PYTHON_VERSION` = `3.13` |
{.compact}

Every branch and pull request gets its own preview address. See [Domains and previews](domains.md).

## Netlify

```toml title="netlify.toml"
[build]
  command = "pip install -r requirements.txt && mkdocs build --strict"
  publish = "site"

[build.environment]
  PYTHON_VERSION = "3.13"
```

Netlify builds a deploy preview for every pull request.

## Any other host

Upload the contents of `site/` to the web root: an S3 bucket, an Nginx or Caddy server, an intranet share. Two things to check:

- **The address.** Set `site_url` to the address the site is served from, including any sub-path such as `https://example.com/docs/`. The sitemap, the feed, `llms.txt`, social previews and canonical links are built from it.
- **Directory URLs.** Pages are written as `guide/index.html` and linked as `guide/`. Most servers serve `index.html` for a folder by default. If yours does not, turn that on, or set `use_directory_urls: false` in `mkdocs.yml`.

## What gets published

| Output | Path | Notes |
| --- | --- | --- |
| Pages | `…/index.html` | Static HTML, readable without JavaScript |
| Theme assets | `assets/` | Fonts, CSS, one script, and Mermaid, KaTeX, ECharts and Markmap loaded only where used |
| Search index | `search/search_index.json` | Fetched when a reader first opens ⌘K |
| Markdown copies, `llms.txt` | `guide.md` next to `guide/`, `llms.txt`, `llms-full.txt` | With the `llms_txt` plugin |
| Feed | `blog/feed.xml` | When the site has a blog |
| Print edition | `print/` | See [Print edition](../pages/print.md) |
| Sitemap | `sitemap.xml` | Full addresses need `site_url` |
{.compact}

Everything is served from your own domain: Sumi loads no fonts, scripts or styles from a CDN. A site can be copied to a USB stick or an air-gapped network and keeps working, apart from [comments](comments.md) and any [analytics](analytics.md) you turn on.
