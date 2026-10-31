---
description: Keyboard shortcuts and 2 000 inline icons.
---

# Keys and icons

## Keyboard shortcuts

Wrap a key combination in double plus signs:

```markdown
Press ++Ctrl+Shift+P++ to open the command palette, or ++Esc++ to close it.
```

Press ++Ctrl+Shift+P++ to open the command palette, or ++Esc++ to close it.

For a single key in running text, plain `<kbd>` also works: <kbd>Enter</kbd>.

## Icons

Write `:lucide-name:` to insert any of the 2 000 [Lucide](https://lucide.dev/icons/) icons, or `:brand-name:` for a brand logo. Icons are inlined as SVG at build time and take the colour of the surrounding text.

```markdown
:lucide-rocket: Launch · :lucide-shield-check: Secure · :lucide-languages: Translated
```

:lucide-rocket: Launch · :lucide-shield-check: Secure · :lucide-languages: Translated

Unknown names are left as text, so a typo is easy to spot.

## Brand icons

| Icon | Name | Icon | Name |
| :---: | --- | :---: | --- |
| :brand-github: | `brand-github` | :brand-gitlab: | `brand-gitlab` |
| :brand-gitee: | `brand-gitee` | :brand-codeberg: | `brand-codeberg` |
| :brand-python: | `brand-python` | :brand-pypi: | `brand-pypi` |
| :brand-docker: | `brand-docker` | :brand-rust: | `brand-rust` |
| :brand-x: | `brand-x` | :brand-mastodon: | `brand-mastodon` |
| :brand-bluesky: | `brand-bluesky` | :brand-discord: | `brand-discord` |
| :brand-wechat: | `brand-wechat` | :brand-zhihu: | `brand-zhihu` |
| :brand-bilibili: | `brand-bilibili` | :brand-xiaohongshu: | `brand-xiaohongshu` |
| :brand-youtube: | `brand-youtube` | :brand-rss: | `brand-rss` |
{.compact}

The full set also includes `bitbucket`, `telegram`, `reddit`, `stackoverflow`, `npm`, `go`, `postgresql`, `markdown`, `readthedocs`, `matrix`, `qq`, `medium`, `devdotto`, `substack`, `facebook` and `instagram`.

## In templates and front matter

The same names are used everywhere Sumi accepts an icon: landing page features, buttons, social links and cards.

```yaml
extra:
  social:
    - icon: brand-github
      link: https://github.com/mkdocs-ng/mkdocs-sumi
```
