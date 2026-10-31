---
description: How tabs, the sidebar, section index pages, breadcrumbs, versions and languages are built.
---

# Navigation

Sumi builds its navigation from MkDocs' `nav`, or from your folders when there is no `nav`.

```yaml title="mkdocs.yml"
nav:
  - Home: index.md
  - Guide:
      - guide/index.md          # section landing page
      - Install: guide/install.md
      - Configure: guide/configure.md
  - Reference:
      - reference/index.md
      - CLI: reference/cli.md
  - Blog: blog/index.md
```

## Tabs and sidebar

- Each **top-level section** is a tab in the header. The sidebar shows the pages of the active tab only.
- **Top-level pages**, such as *Home* and *Blog* above, are tabs as well.
- A section whose first entry is an `index.md` without a title uses that page as its landing: the tab, the sidebar heading and the section name all link to it.
- Nested sections are collapsible. The section containing the current page is open.

On small screens, the tabs and the sidebar move into a drawer opened from the menu button.

With `navigation_tabs: false`, the whole navigation is shown in the sidebar.

## Table of contents

Headings up to `toc_depth` (level 3 by default) are listed on the right, with the current section highlighted as you scroll. On narrow screens the list is folded at the top of the page.

## Previous and next

Links to the previous and next page follow the navigation order. <kbd>[</kbd> and <kbd>]</kbd> move between pages; <kbd>j</kbd> and <kbd>k</kbd> move between headings.

## Versions

Sumi reads the `versions.json` file that [mike](https://github.com/jimporter/mike) writes, shows a version menu in the header and a notice on old versions.

```yaml title="mkdocs.yml"
theme:
  name: sumi
  version_provider: mike
```

```sh
mike deploy --push --update-aliases 0.2 latest
mike set-default --push latest
```

## Languages

For a site published in several languages, list them under `extra.alternate`. A language menu appears in the header and in the command palette.

```yaml title="mkdocs.yml"
extra:
  alternate:
    - name: English
      link: /en/
      lang: en
    - name: 简体中文
      link: /zh/
      lang: zh
```

## Edit links

With `repo_url` and `edit_uri`, each page shows **Edit this page** at the bottom and in the page menu.

```yaml title="mkdocs.yml"
repo_url: https://github.com/me/project
edit_uri: edit/main/docs/
```
