# Sumi

**Markdown in. Beautiful docs out.**

Sumi is a documentation theme for [MkDocs-ng](https://github.com/mkdocs-ng/mkdocs). It turns a folder of plain Markdown into a complete project site — docs, landing page, blog, release downloads and a print edition — without Node.js, a CDN or a hosted service.

[Documentation](https://mkdocs-ng.github.io/mkdocs-sumi/) · [Components](https://mkdocs-ng.github.io/mkdocs-sumi/docs/write/) · [Releases](https://mkdocs-ng.github.io/mkdocs-sumi/releases/)

## Quick start

```sh
pip install mkdocs-sumi
```

```yaml
# mkdocs.yml
theme:
  name: sumi

plugins:
  - search
  - llms_txt   # optional: llms.txt and a Markdown copy of every page
  - sumi
```

```sh
mkdocs serve
```

## Highlights

- **Components in native Markdown.** Callouts are `> [!NOTE]`, steps are a numbered list with `{.steps}`, tabs are fences with `{tab="…"}`. Your source still reads well on GitHub.
- **Local-first.** Fonts, 2 000 icons, search, Mermaid and KaTeX ship with the theme. Mermaid and KaTeX load only on pages that use them.
- **Search as a command palette.** <kbd>⌘</kbd> <kbd>K</kbd> searches every heading, including Chinese and Japanese, and runs commands.
- **Written for agents too.** Every page has a Markdown twin announced in `<head>`, plus `llms.txt` and *Copy as Markdown*.
- **One design for the whole project site.** Data-driven landing pages, a blog with tags and an Atom feed, a releases page with checksums, and a whole-site print edition.
- **Keeps your MkDocs content.** Admonitions, `pymdownx` tabs and details, `mike` versions and Material's `extra` keys keep working.

## Development

```sh
pip install -e ".[test]"
pytest                       # unit and build tests
pip install playwright && playwright install chromium
pytest tests/test_browser.py # browser tests against the docs site
mkdocs serve                 # the docs site is the visual regression suite
```

## License

Apache 2.0. See [NOTICE](NOTICE) for the licenses of bundled fonts, icons and libraries.
