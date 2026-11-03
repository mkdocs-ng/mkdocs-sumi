---
description: 把现有站点从 Material for MkDocs 或其他主题迁移到 Sumi。
---

# 从 Material 迁移

Sumi 能读取为 Material for MkDocs 编写的内容和大部分配置。切换通常只需改两行。

```diff title="mkdocs.yml"
 theme:
-  name: material
+  name: sumi
 plugins:
   - search
+  - sumi
```

## 继续可用的部分

| 你在用的 | 在 Sumi 中 |
| --- | --- |
| `admonition`、`!!! note` 和 `??? note` | 渲染为提示框，颜色与 `> [!NOTE]` 一致 |
| `pymdownx.details`、`pymdownx.tabbed`（alternate 样式） | 原生样式 |
| `pymdownx.superfences`、`pymdownx.highlight` | 支持；此时 Sumi 把代码高亮交给它们 |
| `pymdownx.arithmatex` | 用内置的 KaTeX 渲染 |
| `pymdownx.keys` | 保留；Sumi 自带的 `++Ctrl+K++` 让位 |
| 网格卡片（`<div class="grid cards" markdown>`）和 `{ .md-button }` 链接 | 显示为 Sumi 的卡片和按钮 |
| `extra.social`、`extra.alternate`、`extra.analytics` | 原样读取，包括 `fontawesome/brands/…` 图标名 |
| `mkdocstrings` API 页面 | 有样式：签名、符号徽章（`show_symbol_type_heading`）、标签、嵌套成员、反向链接和源码面板。[推荐配置（英文）](https://sumi.mkdocs-ng.org/docs/customize/plugin-authors/#mkdocstrings) |
| 使用 Material `--md-*` 颜色或 `[data-md-color-scheme]` 的插件 CSS | 跟随 Sumi 的配色和深色模式。插件作者请看：[让插件适配 Sumi（英文）](https://sumi.mkdocs-ng.org/docs/customize/plugin-authors/) |
| `print-site` 插件 | 可以正常构建；Sumi 也自带[打印版](../pages/print.md) |
| `mike` 多版本 | `theme.version_provider: mike` |
| 博客：`blog/posts/`、`.authors.yml`、`date`、`authors`、`tags`、`<!-- more -->` | 原样读取 |
| front matter 中的 `hide: [toc, navigation]` | 改为 `hide: [toc, sidebar]` |
{.wide}

## 需要调整的部分

- Material 的 `theme.features` 和 `theme.palette` 列表会被忽略，请改用[主题选项（英文）](https://sumi.mkdocs-ng.org/docs/customize/theme/)。
- 写成 `:material-…:` 或 `:octicons-…:` 的图标仍需 `pymdownx.emoji` 扩展。Sumi 自带的行内图标是 `:lucide-name:` 和 `:brand-name:`。
- 不模拟 Material Insiders 的功能。

> [!NOTE]
> 如果切换后某个页面显示不对，请[提交 issue](https://github.com/mkdocs-ng/mkdocs-sumi/issues)，附上导致问题的 Markdown。
