---
description: 把现有站点从 Material for MkDocs 或其他主题迁移到 Sumi。
---

# 从 Material 迁移

Sumi 能读取为 Material for MkDocs 编写的内容和大部分配置。先改下面两行，再对照[需要调整的部分](#what-changes)看看你的站点用到了哪些。还在犹豫？看看 [Sumi 与 Material for MkDocs 对比](compare.md)。

```diff title="mkdocs.yml"
 theme:
-  name: material
+  name: sumi
 plugins:
   - search
+  - sumi
```

## 继续可用的部分 {#what-keeps-working}

| 你在用的 | 在 Sumi 中 |
| --- | --- |
| `admonition`、`!!! note` 和 `??? note` | 渲染为提示框，颜色与 `> [!NOTE]` 一致 |
| `pymdownx.details`、`pymdownx.tabbed`（alternate 样式） | 原生样式 |
| `pymdownx.superfences`、`pymdownx.highlight` | 支持；此时 Sumi 把代码高亮交给它们 |
| `pymdownx.arithmatex` | 用内置的 KaTeX 渲染 |
| `pymdownx.keys` | 保留；Sumi 自带的 `++Ctrl+K++` 让位 |
| 网格卡片（`<div class="grid cards" markdown>`）和 `{ .md-button }` 链接 | 显示为 Sumi 的卡片和按钮 |
| `theme.palette` | 按原设置使用浅色、深色或跟随系统；`primary` 颜色成为 Sumi 的[强调色](../customize/theme.md#accent-colours) |
| 不含 `navigation.tabs` 的 `theme.features` | 和 Material 一样，整个导航留在侧边栏 |
| `extra.social`、`extra.alternate`、`extra.analytics` | 原样读取，包括 `fontawesome/brands/…` 图标名 |
| `mkdocstrings` API 页面 | 有样式：签名、符号徽章（`show_symbol_type_heading`）、标签、嵌套成员、反向链接和源码面板。[推荐配置](../customize/plugin-authors.md#mkdocstrings) |
| 使用 Material `--md-*` 颜色或 `[data-md-color-scheme]` 的插件 CSS | 跟随 Sumi 的配色和深色模式。插件作者请看：[面向插件作者](../customize/plugin-authors.md) |
| `print-site` 插件 | 可以正常构建；Sumi 也自带[打印版](../pages/print.md) |
| `mike` 多版本（`extra.version.provider: mike`） | 原样读取；与 `theme.version_provider: mike` 相同 |
| `overrides/main.html` 中的 `announce` 和 `outdated` 块 | 显示在 Sumi 的公告栏和旧版本提示中 |
| 调用 `document$.subscribe(…)` 的脚本 | 在页面加载完成后执行 |
| 博客：`blog/posts/`、`.authors.yml`、`date`、`authors`、`tags`、`<!-- more -->` | 原样读取 |
| front matter 中的 `hide: [toc, navigation]` | 改为 `hide: [toc, sidebar]` |
{.wide}

## 需要调整的部分 {#what-changes}

- `theme.features` 的其他条目会被忽略，Sumi 的[主题选项](../customize/theme.md)提供了对应的设置。
- 用 `emoji_index: !!python/name:material.extensions.emoji.twemoji` 配置的 `pymdownx.emoji` 需要安装 Material，否则构建会中止。请删掉 `emoji_index` 和 `emoji_generator` 两行，图标改写成 `:lucide-name:` 或 `:brand-name:`（见[按键与图标](../write/keys-icons.md)）；之后 `:material-…:` 和 `:octicons-…:` 会显示为文字。
- Material 自带的插件 `blog`、`tags`、`social`、`privacy` 和 `offline` 属于 Material 本身，请从 `plugins` 中删除。Sumi 的[博客](../pages/blog.md)能读取 Material 的文章，Sumi 不从其他服务器加载任何内容，分享链接的图片用 `theme.social_image` 设置。
- 暂不支持代码注释（`# (1)!`）和 `[TAGS]` 标记：注释会显示为代码里的普通注释，后面跟着它的列表。
- Sumi 不使用 Material 的 partial，比如 `partials/copyright.html`。Sumi 的 partial 见[覆盖模板](../customize/overrides.md)。
- 不模拟 Material Insiders 的功能。

> [!NOTE]
> 如果切换后某个页面显示不对，请[提交 issue](https://github.com/mkdocs-ng/mkdocs-sumi/issues)，附上导致问题的 Markdown。
