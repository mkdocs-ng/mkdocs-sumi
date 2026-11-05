---
description: Giscus comments backed by GitHub Discussions, loaded only when readers scroll to them.
---

# Comments

Sumi can show [Giscus](https://giscus.app/) comments under docs pages and blog posts. Giscus stores each page's thread in a GitHub Discussion of your repository, so there is no database to run and no ads.

## Set up

1. Turn on Discussions in your repository's settings, and install the [Giscus app](https://github.com/apps/giscus) on it.
2. Open [giscus.app](https://giscus.app/), enter the repository and pick a discussion category (*Announcements* is a good choice: only maintainers and Giscus can start threads in it). The page shows the `data-repo-id` and `data-category-id` values.
3. Copy them into `mkdocs.yml`:

```yaml title="mkdocs.yml"
theme:
  name: sumi
  comments:
    provider: giscus
    repo: acme/docs
    repo_id: R_kgDOxxxxxx
    category: Announcements
    category_id: DIC_kwDOxxxxxx
```

## Options

| Option | Default | Description |
| --- | --- | --- |
| `repo` | | The repository that holds the discussions, `owner/name`. Required. |
| `repo_id`, `category`, `category_id` | | From giscus.app. |
| `mapping` | `pathname` | How a page finds its discussion: `pathname`, `url`, `title`, `og:title` or `specific`. With `specific`, a page's `comments_term` front matter names its discussion, so pages keep their threads when their URL changes. |
| `strict` | `false` | Match discussion titles exactly instead of by search. |
| `reactions` | `true` | Show reactions on the main post. |
| `input_position` | `bottom` | `top` puts the comment box above the comments. |
| `lang` | the site language | The Giscus interface language. |
| `theme_light`, `theme_dark` | `light`, `dark` | The Giscus themes for each palette. |
| `opt_in` | `false` | Show comments only on pages with `comments: true` in their front matter. |
{.fields}

## Per page

```yaml title="docs/changelog.md"
---
comments: false
---
```

`comments: false` turns comments off on one page. With `opt_in: true`, `comments: true` turns them on.

## What readers get

| Output | Details |
| --- | --- |
| Markup | A **Comments** heading and an empty box after the article, before the previous/next links |
| Loading | Giscus' script is fetched only when the reader scrolls within 400 pixels of the box, so pages without readers at the bottom never load it |
| Theme | Follows the light/dark switch without reloading |
| Without JavaScript | A link to the repository's Discussions |
{.compact}

## Limits

- Readers need a GitHub account to comment. Everyone can read the comments.
- Comments load from giscus.app. Apart from an analytics provider you turn on, this is the only Sumi feature that talks to a third-party service. Leave `comments` unset for a site that must work offline.
- Landing pages and the blog index have no comments.
- Changing `mapping` later can disconnect pages from their existing discussions.
