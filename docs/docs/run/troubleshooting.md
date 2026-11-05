---
description: Fixes for the problems people run into most often with Sumi.
---

# Troubleshooting

Start with `mkdocs build --strict`. It prints every warning and stops on the first one, which usually names the file at fault. Add `--verbose` for more detail.

## Search finds nothing

The ⌘K palette opens but lists no pages.

- **`search` is missing from `plugins`.** Once `plugins:` is in `mkdocs.yml`, MkDocs no longer adds `search` by itself. List it before `sumi`, as in [Install](../start/install.md#enable-the-theme-and-the-plugin).
- **The site is opened from the file system.** Browsers do not let a `file://` page fetch the search index. Serve the folder instead: `python -m http.server -d site`.

## The page looks unstyled, or fonts are missing

- **Opened from the file system.** As above, browsers block fonts on `file://` pages. Serve the folder over HTTP.
- **Served from a sub-path.** If the site lives at `https://example.com/docs/`, set `site_url` to that address. Links between pages are relative and keep working; the address matters for canonical links, the sitemap and social previews.
- **A strict Content Security Policy.** Sumi uses a few small inline scripts, for the colour scheme and the page data. A policy without `'unsafe-inline'` for scripts blocks them. Allow them with a hash or a nonce in your server's policy.

## Components show as plain Markdown

Callouts appear as blockquotes, `{.cards}` lines are visible, or `mermaid` fences stay code.

- **The attribute line is not directly under the block.** `{.cards}` must be the line right after the list, with no blank line in between. See [Attribute lines](../write/index.md#attribute-lines).
- **Another plugin handles the fence.** If a Mermaid or ECharts plugin is also enabled, turn one off, for example `mermaid: false` on the [Sumi plugin](../customize/plugin.md).

## "The Sumi theme needs its plugin"

The build stops with this message when `theme: name: sumi` is set but `sumi` is not under `plugins:`. The theme draws the page and the plugin turns Markdown into components, so both are needed:

```yaml title="mkdocs.yml"
theme:
  name: sumi
plugins:
  - search
  - sumi
```

## "The 'sumi' plugin is meant to be used with 'theme: sumi'"

The opposite case: the plugin is enabled, but the theme is another one. Set `theme: name: sumi`, or remove `sumi` from `plugins`.

## "An echarts fence is neither valid JSON nor YAML"

A chart's option could not be read. The message gives the first parse error. Common causes are tabs used for indentation, an unquoted string with a `:` in it, or a JavaScript function, which options cannot contain. See [Charts](../write/charts.md).

## Every page says "Last updated" today

With `git_dates: true`, dates come from Git. CI services usually clone only the last commit, which makes every page look new. Fetch the full history first, with `fetch-depth: 0` on `actions/checkout`. If there is no Git history at all, the build logs `git_dates is enabled but git history is unavailable` and shows no dates.

## `locale` is rejected

MkDocs accepts letters and underscores in `theme.locale`: write `pt_BR` or `zh_TW`, not `pt-BR`. The page's `lang` attribute is still written as `pt-BR`. See [Languages](../customize/i18n.md).

## The bilingual view button is missing

It appears only on a multi-language site, and only on pages that have a translation: a page shown in the default language because its translation is missing does not offer it. Check that the translated file exists, and that `bilingual_view` is not `false`.

## Comments do not appear

- Check `repo`, `repo_id`, `category` and `category_id` against [giscus.app](https://giscus.app/).
- The repository must be public, have Discussions turned on and have the Giscus app installed.
- Comments load when the reader scrolls near them. A privacy extension can block giscus.app.

## A page breaks after an upgrade

Usually a [template override](../customize/overrides.md) that predates the release. Move the override aside, build again, and compare. See [Upgrade](upgrade.md#template-overrides).

## Still stuck

[Open an issue](https://github.com/mkdocs-ng/mkdocs-sumi/issues) with the output of `mkdocs build --strict --verbose`, your `mkdocs.yml`, and the versions from `pip show mkdocs-sumi mkdocs-ng`.
