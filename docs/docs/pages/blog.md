---
description: A blog with authors, tags, reading time and an Atom feed — from a folder of Markdown files.
---

# Blog

Every Markdown file under `docs/blog/` is a post. Sumi generates the blog index, keeps posts out of the sidebar, and writes an Atom feed. You don't need another plugin.

```filetree
docs/
└── blog/
    ├── .authors.yml          # optional: author names and avatars
    ├── index.md              # optional: the blog's title and intro
    └── posts/
        ├── 2026-11-01-introducing-sumi.md
        └── 2026-11-15-search.md
```

See it on [this site's blog](../../blog/index.md).

## Writing a post

```markdown title="docs/blog/posts/2026-11-01-introducing-sumi.md"
---
date: 2026-11-01
authors: [xianpeng]
tags: [release, design]
description: Sumi 0.1 is out.
---

# Introducing Sumi

The first paragraph is the excerpt shown on the index.

<!-- more -->

The rest of the post.
```

| Key | Type | Description |
| --- | --- | --- |
| `date` | date | Publication date. Defaults to the date of the last Git commit, or the file's modification time. |
| `updated` | date | Shown as "Updated" on the post. |
| `authors` | list | Author ids from `.authors.yml`, or plain names. |
| `tags` | list | Shown on the post and as filters on the index. `categories` is accepted too. |
| `description` | string | The excerpt on the index and the summary in the feed. Without it, the text before `<!-- more -->` is used. |
| `image` | string | A cover image, as a path from `docs/`. Shown at the top of the post, on its card in the card view, and as the preview when the post is shared. Set `hide_cover: true` to keep it off the post itself. |
| `draft` | boolean | Build the page but leave it out of the index and the feed. |
| `series` | list | Series the post belongs to. The post shows the other posts of each series, oldest first, or in `series_order`. |
| `aliases` | list | Old addresses of the page. See [Old addresses](#old-addresses). Works on any page. |
{.fields}

## Page bundles

A post can also be a folder with an `index.md` and its images, the way Hugo calls a page bundle. The post keeps the folder's URL, and an image named `featured` or `cover` (`.jpg`, `.png`, `.webp` or `.svg`) next to it is its cover:

```filetree
docs/
└── posts/
    └── 2026/
        └── introducing-sumi/
            ├── index.md        # → /posts/2026/introducing-sumi/
            ├── featured.jpg    # the cover
            └── screenshot.png  # ![](screenshot.png) in index.md
```

Front matter written for Hugo works as it is: `summary` is used as the `description`, and `cover: {image: …}` as the `image`.

## Several blogs

`blog.dir` takes a list. Each folder is a blog with its own index and its own previous / next links; tag pages, the archive and the feed take the posts of all of them:

```yaml title="mkdocs.yml"
plugins:
  - sumi:
      blog:
        dir: [posts, essays]
```

## Tag pages

Tag filters on the index need no setup. To give each tag a page of its own, which search engines can find, set `blog.tags_dir`:

```yaml title="mkdocs.yml"
plugins:
  - sumi:
      blog:
        tags_dir: tags
```

Sumi then writes `tags/` with every tag and its number of posts, and a page for each tag. Tag URLs are made the way Hugo makes them: `Open Source` is `tags/open-source/`. Tags on posts link to these pages. To add an introduction to the list of tags, create `tags/index.md` with `template: blog-tags.html`. Tags are listed most used first; add `tags_sort: name` to that page to list them A to Z.

## Archive

A page with `template: blog-archive.html` lists every post, newest first, grouped by year:

```markdown title="docs/archive.md"
---
template: blog-archive.html
---

# Archive
```

## Old addresses

When a page moves, list its old addresses in `aliases`, and Sumi writes a page at each one that sends readers and search engines to the new address:

```yaml
---
aliases:
  - /2019/05/hello-world/
---
```

An address starting with `/` is from the root of the site; one without is from the root of the page's language. A redirect never replaces a page, and on a [multi-language site](../customize/i18n.md) the default language's redirects come first.

## Authors

```yaml title="docs/blog/.authors.yml"
authors:
  xianpeng:
    name: Xianpeng Shen
    description: Maintainer
    avatar: https://github.com/shenxianpeng.png
    url: https://github.com/shenxianpeng
```

The format is the same as the Material blog plugin's, so an existing file can be reused.

## The index page

Without `docs/blog/index.md`, Sumi creates one titled "Blog". To add an introduction, create the file; any Markdown in it is shown above the list of posts. Tag filters appear when posts have tags, and a filter can be linked to as `blog/#tag=release`.

Any page can list a selection of posts: give it `template: blog.html` and `blog_tag: release` for the posts with that tag, or `blog_series: Getting started` for the posts of a series.

## List and card views

The index shows posts as a list, or as a grid of cards with cover images. Readers can switch with the buttons next to the tag filters; their choice is remembered. Pick the default with `blog.layout`:

```yaml title="mkdocs.yml"
plugins:
  - sumi:
      blog:
        layout: cards    # or list (the default)
```

A post without an `image` gets a cover drawn from the accent colour and its first tag.

## Feed

An Atom feed is written to `blog/feed.xml` and linked from every page's `<head>`, so feed readers find it from any URL. It needs `site_url` to produce absolute links.

To keep the address and format of an older feed, for example Hugo's RSS feed at `index.xml`, set `feed_path` and `feed_format`. The RSS feed carries each post's description and cover image:

```yaml title="mkdocs.yml"
plugins:
  - sumi:
      blog:
        feed_path: index.xml
        feed_format: rss
        feed_items: 0      # every post
```

## Post footer

To add something under every post, such as a newsletter form or links to your projects, override `partials/post-footer.html` (see [Template overrides](../customize/overrides.md)). It is empty by default and has the post as `sumi.post`.

## Options

```yaml title="mkdocs.yml"
plugins:
  - sumi:
      blog:
        dir: blog        # folder under docs/ that contains posts, or a list of folders
        feed: true
        feed_items: 20   # 0 for every post
        feed_path: blog/feed.xml   # defaults to feed.xml in the first blog folder
        feed_format: atom          # or rss
        tags_dir:        # a folder for tag pages, such as tags; off by default
        layout: list     # or cards
```
