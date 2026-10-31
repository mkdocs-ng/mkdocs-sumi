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
| `draft` | boolean | Build the page but leave it out of the index and the feed. |
{.fields}

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

## Feed

An Atom feed is written to `blog/feed.xml` and linked from every page's `<head>`, so feed readers find it from any URL. It needs `site_url` to produce absolute links.

## Options

```yaml title="mkdocs.yml"
plugins:
  - sumi:
      blog:
        dir: blog        # folder under docs/ that contains posts
        feed: true
        feed_items: 20
```
