---
description: Sumi 能做到哪些 Material for MkDocs 做不到的事，Material 在哪些方面仍然领先，以及如何切换。
---

# Sumi 与 Material for MkDocs 对比

[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) 是目前使用最广的 MkDocs 主题，遥遥领先。Sumi 更年轻：它为 [MkDocs NG](https://mkdocs-ng.org/) 打造，能做到不少 Material 做不到的事。本页介绍 Sumi 领先的地方、Material 仍然领先的地方，以及如何在你的站点上试用 Sumi。你的 Markdown、`mkdocs.yml` 和插件在两边都能用，切换只需[改两行](migrate.md)。

本页内容于 2026-11-06 对照 Sumi 0.3.1、Material for MkDocs 9.8.0 和 `mkdocs-ng-material` 9.8.0 核实。如有错误或过时之处，请[提交 issue](https://github.com/mkdocs-ng/mkdocs-sumi/issues)。

## Sumi 领先的地方 {#where-sumi-is-ahead}

### 持续开发 {#actively-developed}

Sumi 每个次版本都有新功能，并与 MkDocs NG 一起开发，所以它总是第一个用上 MkDocs NG 新功能的主题，例如用一个 `mkdocs.yml` 管理所有语言。Material for MkDocs 已进入维护模式：作者只提供关键修复，持续到 2027-05-05，现在转而开发新的生成器 [Zensical](https://zensical.org/)。

如果你想继续使用 Material，MkDocs NG 项目维护着分支 [`mkdocs-ng-material`](https://github.com/mkdocs-ng/mkdocs-material)，它会接收 bug 修复并保持与新版 MkDocs NG 兼容，但不再增加新功能。

### 不从其他服务器加载任何东西 {#nothing-loaded-from-other-servers}

字体、2,000 个图标、搜索、Mermaid、ECharts、思维导图和 KaTeX 都随主题打包，并复制到你的站点里。除非你自己配置，Sumi 站点不会向其他服务器发出任何请求，所以在防火墙后、内网或离线环境中表现完全一样，读者也不会被字体或脚本 CDN 看到。默认设置下，Material 从 Google Fonts 加载字体、从 `unpkg.com` 加载 Mermaid，它的文档也建议从 CDN 引入 MathJax 或 KaTeX。

我们用两个主题的默认设置构建同一个页面——包含标题、代码块、标签页、表格和两个提示框——并在 Chromium 中加载：

| | Sumi 0.3.1 | Material for MkDocs 9.8.0 |
| --- | --- | --- |
| 请求数 | 5 | 8 |
| 发往其他服务器的请求 | 0 | 3，发往 Google Fonts |
| 传输量（压缩后） | 128 KB，其中字体 87 KB | 149 KB，其中字体 74 KB |
| JavaScript | 17 KB | 46 KB，含搜索 Worker |
{caption="测于 2026-11-06。设置 <code>theme.font: false</code> 后，Material 改用读者的系统字体：5 个请求，72 KB。"}

### 组件依然是 Markdown {#components-that-are-still-markdown}

Material 通过 Python-Markdown 扩展提供组件，语法是 `!!! warning`、`=== "Tab"` 这样的写法。在 GitHub 或编辑器预览里，它们只会显示成普通文本。

Sumi 的每个组件都用 Markdown 自己的词汇来写——引用块、列表、表格或代码围栏——最多再加一行 `{…}` 属性。提示框就是 GitHub 的 alert 语法，所以在 GitHub 上也能正常渲染：

```markdown
> [!WARNING]
> 升级前请先备份数据。
```

你的页面在哪里打开都好读，也不会被 Sumi 锁定。Sumi 同样能读取 Material 的语法，现有页面无需修改即可渲染。

### 完整的项目站点，而不只是文档 {#a-whole-project-site-not-only-docs}

除了文档，Sumi 的插件还能用同一套设计构建项目需要的其他页面：

- 用 front matter 描述的[首页](../pages/landing.md)：主视觉、功能、代码、数据、步骤和常见问题，不用写 HTML；
- 带作者、标签、阅读时长、卡片布局和 Atom 订阅的[博客](../pages/blog.md)；
- 带下载和 SHA-256 校验和的[发布页](../pages/releases.md)，数据来自 YAML 文件、GitHub Releases 或 PyPI；
- 整站[打印版](../pages/print.md)。

Material 有博客插件；首页需要覆盖模板，订阅源需要 `mkdocs-rss-plugin`，整站打印需要 `print-site` 插件。

### 为 AI 智能体而生 {#built-for-ai-agents}

Sumi 的每个页面也会发布一份 Markdown，并在 HTML 页面中链接，方便智能体找到；页面上还有*复制为 Markdown* 按钮，以及在 AI 助手中打开本页的链接。再加上 `llms.txt`，编程智能体和 AI 助手读你的文档时就不会被导航和脚本干扰。见[面向 AI 与智能体](../ai.md)。Material 没有内置这些功能；MkDocs NG 的 `llms_txt` 插件两边都能用。

### 多语言站点 {#multi-language-sites}

在 MkDocs NG 中，一个 `mkdocs.yml` 就能管理所有语言。Sumi 在此之上提供：链接到同一页面其他语言版本的语言菜单、供搜索引擎使用的 `hreflang` 链接、未翻译页面的提示，以及左右对照、同步滚动的[双语视图](../customize/i18n.md#bilingual-view)。中文、日文和韩文有专门的排版，搜索也按子串匹配。

### 大型站点更快 {#faster-on-large-sites}

在 MkDocs NG 的[构建基准测试](https://mkdocs-ng.org/about/comparison/#build-speed)中，5,000 页的站点用 Sumi 构建需要 67.6 秒，用 Material 需要 134.5 秒，因为 Material 会把整个导航写进每一个页面。1,000 页时两者接近：12.2 秒和 11.1 秒。`mkdocs serve` 中保存修改后，Sumi 1.8 秒、Material 2.7 秒就能看到更新。

### 更多图表，按需加载 {#more-diagrams-loaded-only-when-needed}

除了 Mermaid 和 KaTeX，Sumi 还提供 [ECharts 图表和 Markmap 思维导图](../write/charts.md)。每种运行库只在用到它的页面加载；Mermaid 只在图表滚动到视口附近时才加载，而且只加载该图表类型所需的代码。

### 命令面板式搜索 {#search-as-a-command-palette}

<kbd>⌘</kbd> <kbd>K</kbd> 搜索所有标题，包括中文和日文，还能执行命令：切换语言、切换深色模式、把页面复制为 Markdown、打开双语视图。搜索索引在打开面板时才加载。

### 支持 Python 3.10 {#python-310}

Sumi 支持 Python 3.10 及以上版本。Material for MkDocs 9.8.0 要求 Python 3.11。

## Material 领先的地方 {#where-material-is-ahead}

- **用户量。** Material 的下载量是 Sumi 的许多倍，据其作者统计，约 84,000 个公开 GitHub 仓库依赖它。这意味着更多的示例、问答，以及针对它测试过的插件。Sumi 2026-10-31 才首次发布。
- **广度。** 60 多种界面语言对 Sumi 的 13 种，约 14,000 个图标对 2,000 个，并可使用任意 Google 字体。
- **Sumi 没有的功能：** 代码注释、无需整页刷新的即时导航、为每个页面自动生成的社交卡片，以及跨文档页面的标签（Sumi 的标签只用于博客文章）。

如果你的站点依赖这些功能，目前 Material（或在 MkDocs NG 上使用 `mkdocs-ng-material`）更合适。

## 总览 {#at-a-glance}

| | Sumi | Material for MkDocs |
| --- | --- | --- |
| 开发状态 | 活跃 | 维护模式，关键修复持续到 2027-05-05 |
| 默认从其他服务器加载 | 无 | Google Fonts；从 `unpkg.com` 加载 Mermaid |
| 组件语法 | 原生 Markdown，可在 GitHub 上渲染；也能读取 Material 的语法 | Python-Markdown 扩展 |
| 项目页面 | 首页、带订阅源的博客、带校验和的发布页、打印版 | 博客；其余需通过模板覆盖和插件 |
| 面向 AI 智能体 | 每页的 Markdown 副本、*复制为 Markdown*、`llms.txt` | 通过 MkDocs NG 提供 `llms.txt` |
| 多语言 | 语言菜单、`hreflang`、未翻译提示、双语视图 | 语言菜单 |
| 图表 | Mermaid、ECharts、思维导图、KaTeX，全部打包 | Mermaid 来自 CDN；公式需自行添加 |
| 搜索 | 命令面板，中日韩文本按子串匹配 | lunr.js，支持词干提取、搜索建议、可选的中文分词 |
| 5,000 页构建 | 67.6 秒 | 134.5 秒 |
| Python | 3.10+ | 3.11+（`mkdocs-ng-material`：3.10+） |
| 界面语言 | 13 种，包括从右到左的语言 | 60 多种，包括从右到左的语言 |
| 图标 | 约 2,000 个 | 约 14,000 个 |
| 代码注释、即时导航、自动生成社交卡片 | 无 | 有 |
| 运行于 | MkDocs NG 1.9+ | MkDocs 1.6、MkDocs NG、ProperDocs |
| 首次发布 | 2026-10-31 | 2016-02-09 |
{.wide}

## 插件 {#plugins}

两个主题都能运行普通的 MkDocs 插件：mkdocstrings、macros、glightbox、awesome-nav、redirects、git-revision-date-localized 等等。

- 用 Material 的 `--md-*` 颜色或 `[data-md-color-scheme]` 设置样式的插件，会跟随 Sumi 的配色和深色模式。
- 等待 Material 即时导航（`document$`）的脚本需要改为在 `DOMContentLoaded` 时运行，因为 Sumi 使用普通的页面加载。
- Material 的内置插件——`blog`、`tags`、`social`、`privacy`、`offline` 等——是 Material 的一部分，不能和 Sumi 一起运行。Sumi 自带的博客能原样读取 Material 的博客文章和 `.authors.yml`；Sumi 也不需要隐私插件，因为它本来就不从其他服务器加载任何东西。

[面向插件作者](../customize/plugin-authors.md)介绍了如何同时支持两个主题。

## 试用 Sumi {#try-sumi}

```diff title="mkdocs.yml"
 theme:
-  name: material
+  name: sumi
 plugins:
   - search
+  - sumi
```

运行 `mkdocs serve`，浏览一遍你的站点。[从 Material 迁移](migrate.md)列出了哪些继续可用、哪些需要调整。Sumi 尚未到 1.0，请固定你测试过的版本，并在升级前阅读[发布记录](../../releases.md)。
