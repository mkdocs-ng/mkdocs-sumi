---
description: 键盘快捷键和 2 000 个行内图标。
---

# 按键与图标

## 键盘快捷键 {#keyboard-shortcuts}

把组合键写在两对加号之间：

```markdown
按 ++Ctrl+Shift+P++ 打开命令面板，按 ++Esc++ 关闭。
```

按 ++Ctrl+Shift+P++ 打开命令面板，按 ++Esc++ 关闭。

正文中的单个按键，也可以直接用 `<kbd>`：<kbd>Enter</kbd>。

## 图标 {#icons}

写 `:lucide-名称:` 可以插入 2 000 个 [Lucide](https://lucide.dev/icons/) 图标中的任意一个，写 `:brand-名称:` 可以插入品牌标志。图标在构建时以 SVG 内联，颜色跟随周围的文字。

```markdown
:lucide-rocket: 发布 · :lucide-shield-check: 安全 · :lucide-languages: 多语言
```

:lucide-rocket: 发布 · :lucide-shield-check: 安全 · :lucide-languages: 多语言

不认识的名称会原样保留为文字，所以拼错了很容易发现。

## 品牌图标 {#brand-icons}

| 图标 | 名称 | 图标 | 名称 |
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

完整的图标集还包括 `bitbucket`、`telegram`、`reddit`、`stackoverflow`、`npm`、`go`、`postgresql`、`markdown`、`readthedocs`、`matrix`、`qq`、`medium`、`devdotto`、`substack`、`facebook` 和 `instagram`。

## 在模板和 front matter 中 {#in-templates-and-front-matter}

凡是 Sumi 接受图标的地方，用的都是同一套名称：首页的功能介绍、按钮、社交链接和卡片。

```yaml
extra:
  social:
    - icon: brand-github
      link: https://github.com/mkdocs-ng/mkdocs-sumi
```
