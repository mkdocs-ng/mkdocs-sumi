---
description: Create a new site with Sumi, from an empty folder to a deployed build.
---

# Your first site

This page builds a small site from scratch: a home page, two guide pages and a blog post.

1. Create the project

    ```sh
    mkdocs new my-docs
    cd my-docs
    ```

2. Lay out the files

    ```filetree
    my-docs/
    ├── docs/
    │   ├── index.md            # Home page
    │   ├── guide/
    │   │   ├── index.md        # Section landing, linked from the sidebar title
    │   │   └── install.md
    │   └── blog/
    │       └── posts/
    │           └── hello.md    # Any page under blog/ is a post
    └── mkdocs.yml              # Site configuration
    ```

3. Configure the site

    ```yaml title="mkdocs.yml"
    site_name: My Docs
    site_url: https://example.com/
    repo_url: https://github.com/me/my-docs

    theme:
      name: sumi

    plugins:
      - search
      - sumi
    ```

4. Preview and build

    ```sh
    mkdocs serve        # live preview
    mkdocs build        # writes static files to site/
    ```
{.steps}

## How navigation is built

Top-level sections become **tabs** in the header. Pages inside the active tab appear in the **sidebar**. A section whose first page is `index.md` uses that page as its landing: the section title links to it.

> [!TIP]
> Without a `nav:` key, MkDocs builds the navigation from your folders. Blog posts are kept out of the sidebar automatically.

## Deploy

`mkdocs build` writes plain HTML, CSS and JavaScript to `site/`. Upload that folder to any static host — GitHub Pages, Cloudflare Pages, Netlify, an S3 bucket or an Nginx server. Nothing needs to run after deployment.

```sh
mkdocs gh-deploy      # build and push to the gh-pages branch
```
