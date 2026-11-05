---
description: 所有主题选项：颜色、标志、页眉、公告栏、页面元素和页脚。
---

# 主题选项

主题选项写在 `mkdocs.yml` 的 `theme:` 下，全部都是可选的。

```yaml title="mkdocs.yml"
theme:
  name: sumi
  palette: auto
  accent: indigo
  logo: assets/logo.svg
  announcement: 'Sumi 0.1 发布了，<a href="blog/">阅读文章</a>'
```

## 选项 {#options}

| 选项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `palette` | string | `auto` | `light`、`dark` 或 `auto`（跟随操作系统）。读者可以随时切换，选择会被记住。 |
| `accent` | string | `vermilion` | 链接、高亮和当前标签的颜色：`vermilion`、`indigo`、`moss`、`plum`、`ochre`、`teal`、`ink`，或者任意 CSS 颜色。 |
| `locale` | string | `en` | 界面语言，如 `en`、`zh`、`zh_TW`、`ja`、`de`；也认 Material 的 `language`。见[语言](i18n.md)。 |
| `logo` | string | | `docs/` 中用于页眉的图片。不设置时使用 Sumi 标志。 |
| `logo_dark` | string | | 深色配色下的页眉图片。不设置时两种配色都用 `logo`。 |
| `favicon` | string | | `docs/` 中用于浏览器标签页的图片。 |
| `social_image` | string | | 页面分享到 X、Slack、Mastodon 等平台时显示的预览图：`docs/` 中的一张图片（约 1200×630，需要 `site_url`），或者一个完整 URL。页面可以在 front matter 中用 `image:` 指定自己的预览图。 |
| `brand` | string | `site_name` | 页眉品牌名的 HTML，例如 `"MkDocs<b>ng</b>"`。 |
| `announcement` | string | | 页眉上方可关闭的公告栏的 HTML。读者关闭旧公告后，新的公告仍会显示。 |
| `navigation_tabs` | boolean | `true` | 在页眉中把顶层章节显示为标签。设为 `false` 时，整个导航都放在侧边栏中。 |
| `toc_depth` | integer | `3` | 页面目录中最深的标题级别。 |
| `hide` | list | `[]` | 在每个页面上隐藏的部分：`toc`、`sidebar`、`breadcrumbs`、`actions`、`pager`、`footer`、`feedback`、`comments`。 |
| `version_provider` | string | | 设为 `mike` 显示版本菜单。见[导航](navigation.md#versions)。 |
| `bilingual_view` | boolean | `true` | 多语言站点上，提供页面与译文并排阅读的双语对照视图。见[语言](i18n.md#bilingual-view)。 |
| `comments` | mapping | | 文档页和博客文章下方的 Giscus 评论。见[评论](../run/comments.md)。 |
| `feedback` | boolean 或 mapping | | “这页内容对你有帮助吗？”反馈组件。Material 的 `extra.analytics.feedback` 同样有效。见[访问统计与反馈](../run/analytics.md)。 |
| `repo_icon` | string | | 覆盖仓库图标，例如 `brand-gitlab`。默认根据 `repo_url` 识别。 |
| `keyboard` | boolean | `true` | 启用单键快捷键。<kbd>⌘</kbd> <kbd>K</kbd> 始终可用。 |
| `credit` | boolean | `true` | 在页脚显示“由 MkDocs NG 与 Sumi 构建”。 |
{.fields}

## 强调色 {#accent-colours}

| 名称 | 浅色 | 深色 |
| --- | --- | --- |
| `vermilion` | `#c4432b` | `#ef7258` |
| `indigo` | `#2f5d93` | `#86b4ea` |
| `moss` | `#4b6b2f` | `#9ccc6e` |
| `plum` | `#7a3b74` | `#dc93d4` |
| `ochre` | `#9a6512` | `#e7b45a` |
| `teal` | `#1f6f6a` | `#6fd0c6` |
| `ink` | `#2a2926` | `#e8e4dc` |
{.compact}

具名强调色在深色模式下有专门调过的版本。自定义的 CSS 颜色在两种模式下都一样。

## 单页选项 {#per-page-options}

页面的 front matter 可以改变它的布局：

| 键 | 说明 |
| --- | --- |
| `hide` | 和主题选项相同，但只作用于一个页面：`hide: [toc, pager]`。`navigation` 可以作为 `sidebar` 的别名。 |
| `layout` | `wide` 会去掉两侧边栏，使页面占满全宽。 |
| `comments` | `false` 关闭本页的评论；设置了 `comments.opt_in` 时，`true` 为本页打开评论。 |
| `template` | `landing.html`、`blog.html` 或 `releases.html`。见[页面类型](../pages/landing.md)。 |
| `description` | 用于 `<meta name="description">`、链接预览、卡片和博客首页。 |
{.fields}

## 页脚与社交链接 {#footer-and-social-links}

```yaml title="mkdocs.yml"
copyright: © 2026 The MkDocs NG project
extra:
  social:
    - icon: brand-github
      link: https://github.com/mkdocs-ng
      name: GitHub
    - icon: fontawesome/brands/x-twitter   # Material 的图标名也可以用
      link: https://x.com/mkdocs
```

## 自定义 CSS {#custom-css}

所有颜色、字体和尺寸都是 CSS 变量。用 `extra_css` 添加样式表：

```css title="docs/assets/extra.css"
:root {
  --sumi-font: "IBM Plex Sans", system-ui, sans-serif;
  --sumi-content-w: 820px;
}
[data-theme="dark"] {
  --sumi-bg: #0f1115;
}
```

```yaml title="mkdocs.yml"
extra_css:
  - assets/extra.css
```
