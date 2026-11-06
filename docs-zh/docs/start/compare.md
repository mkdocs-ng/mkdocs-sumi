---
description: Sumi 与 Material for MkDocs 有哪些不同：写作方式、功能、插件、速度、隐私、语言和维护状态，帮你做出选择。
---

# Sumi 与 Material for MkDocs 对比

[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) 是使用最广的 MkDocs 主题，Sumi 的不少想法也是它最先带火的。本页列出两者的区别，帮你选出适合自己项目的那一个。两者都是 MkDocs 主题：你的 Markdown、`mkdocs.yml` 和插件在两边都能用，来回切换都只需[改两行](migrate.md)。

本页内容于 2026-11-06 对照 Sumi 0.3.1、Material for MkDocs 9.8.0 和 `mkdocs-ng-material` 9.8.0 核实。如有错误或过时之处，请[提交 issue](https://github.com/mkdocs-ng/mkdocs-sumi/issues)。

## 一句话总结 {#in-short}

- **选 Material**：如果你需要它的广度——60 多种界面语言、约 14,000 个图标、代码注释、即时导航、自动生成的社交卡片，以及十年积累下来的示例、问答和围绕它开发的插件。它目前处于维护模式，关键修复持续到 2027-05-05。
- **选 Sumi**：如果你想要一个随 [MkDocs NG](https://mkdocs-ng.org/) 持续开发的主题——不从其他服务器加载任何东西，组件保持为可读的纯 Markdown，用同一套设计做出完整的项目站点（首页、博客、发布页、打印版），并且每个页面也为 AI 智能体发布一份。
- **还拿不准？** 在一个分支上试试 Sumi：改两行，运行 `mkdocs serve` 对比一下。你的内容不需要改动。

## 总览 {#at-a-glance}

| | Sumi | Material for MkDocs |
| --- | --- | --- |
| 包名 | `mkdocs-sumi` | `mkdocs-material`，或为 MkDocs NG 维护的分支 [`mkdocs-ng-material`](https://github.com/mkdocs-ng/mkdocs-material) |
| 首次发布 | 2026-10-31 | 2016-02-09 |
| 开发状态 | 活跃：每个次版本都有新功能 | 维护模式：关键修复持续到 2027-05-05，作者转向开发 [Zensical](https://zensical.org/) |
| 运行于 | MkDocs NG 1.9 及以上 | MkDocs 1.6、MkDocs NG、ProperDocs |
| Python | 3.10+ | 3.11+（`mkdocs-ng-material`：3.10+） |
| 组件写法 | 原生 Markdown：`> [!NOTE]`、带 `{.steps}` 的有序列表、带 `{tab="…"}` 的代码围栏；也能读取 Material 的写法 | Python-Markdown 扩展：`!!! note`、`=== "Tab"`、`<div class="grid cards" markdown>` |
| 界面语言 | 13 种，包括从右到左的阿拉伯语和希伯来语 | 60 多种，包括从右到左的语言 |
| 图标 | 约 2,000 个（Lucide 和品牌图标） | 约 14,000 个（Material Design、Font Awesome、Octicons、Simple Icons） |
| 字体 | Inter 和 JetBrains Mono，随主题打包 | 任意 Google 字体，默认从 Google 加载 |
| 图表与公式 | Mermaid、ECharts、思维导图和 KaTeX，随主题打包，只在用到的页面加载 | Mermaid，从 `unpkg.com` 加载；MathJax 或 KaTeX 需自行添加，通常来自 CDN |
| 搜索 | 命令面板，中日韩文本按子串匹配；打开面板时才加载索引 | 在 Web Worker 中运行的 lunr.js，支持多种语言的词干提取、可选的中文分词（jieba）、搜索建议和高亮 |
| 页面加载 | 普通的页面加载 | 可选的即时导航，切换页面时不整页刷新 |
| 代码块 | 构建时高亮、标题、行号、复制按钮（console 代码块只复制命令） | 同样具备，另有代码注释 |
| 项目页面 | 数据驱动的首页、带 Atom 订阅的博客、带校验和的发布页、整站打印版 | 博客和标签插件；首页通过模板覆盖实现；打印通过 `print-site` 插件 |
| 链接预览图 | 全站一张，或每页一张 | 社交插件为每个页面生成一张卡片 |
| 面向 AI 智能体 | 每个页面都有 Markdown 副本并在 HTML 中链接；*复制为 Markdown*；`llms.txt` | 通过 MkDocs NG 的插件生成 `llms.txt`，该插件适用于任何主题 |
| 多语言站点 | MkDocs NG 的 `languages:`，带语言菜单、`hreflang` 链接、未翻译页面提示和左右对照的双语视图 | 通过 `extra.alternate` 的语言菜单，以及 MkDocs NG 的 `languages:` |
| 多版本 | `mike` | `mike` |
| 使用者 | 目前只有少量站点，见[案例](../../showcase.md) | 据其作者统计，约 84,000 个公开 GitHub 仓库依赖它 |
{.wide}

## 写作方式 {#writing}

Material 通过 Python-Markdown 扩展提供组件，所以页面里会用到 `!!! warning`、`=== "Tab"` 这样的语法。写起来很简洁，但在 GitHub 或编辑器预览里只会显示成普通文本。

Sumi 用 Markdown 自己的词汇来写组件——引用块、列表、表格或代码围栏——最多再加一行 `{…}` 属性。Sumi 的提示框就是 GitHub 的 alert 语法，所以在 GitHub 上也能正常渲染：

```markdown
> [!WARNING]
> 升级前请先备份数据。
```

Sumi 也能读取 Material 的语法：admonition、`pymdownx` 的标签页和折叠块、网格卡片和按钮都无需修改即可渲染。见[继续可用的部分](migrate.md#what-keeps-working)。

## 只有 Material 有的功能 {#features-only-material-has}

- **代码注释**：代码块中的编号标记，点击后展开说明。
- **即时导航**：页面原地切换，带预加载和进度条。
- **自动生成社交卡片**：为每个页面生成一张带标题的图片。
- **整站文档标签**：Sumi 的标签只用于博客文章。
- **隐私和离线插件**：把外部资源下载到站点里，或让站点可以直接从文件系统浏览。Sumi 没有隐私插件，因为它本来就不从其他服务器加载任何东西。
- **更多语言和图标**：60 多种界面语言对 Sumi 的 13 种，约 14,000 个图标对 2,000 个，并可使用任意 Google 字体。

## 只有 Sumi 有的功能 {#features-only-sumi-has}

- **命令面板**：<kbd>⌘</kbd> <kbd>K</kbd> 搜索所有标题，还能执行命令，例如切换语言、切换深色模式或把页面复制为 Markdown。
- **项目页面**：用 front matter 描述的[首页](../pages/landing.md)，从 GitHub Releases 或 PyPI 读取、带下载和校验和的[发布页](../pages/releases.md)，以及整站[打印版](../pages/print.md)。
- **面向智能体的文档**：每个页面都有一份在 HTML 中链接的 [Markdown 副本](../ai.md)、*复制为 Markdown* 按钮，以及在 AI 助手中打开本页的链接。
- **更多图表，全部本地**：除了 Mermaid 和 KaTeX，还有 ECharts 图表和 Markmap 思维导图，都只在页面需要时加载。
- **双语视图**：页面和它的译文左右对照，滚动同步。见[语言](../customize/i18n.md#bilingual-view)。

## 插件 {#plugins}

两个主题都能运行普通的 MkDocs 插件：mkdocstrings、macros、glightbox、awesome-nav、redirects、git-revision-date-localized 等等。

- 用 Material 的 `--md-*` 颜色或 `[data-md-color-scheme]` 设置样式的插件，会跟随 Sumi 的配色和深色模式。
- 等待 Material 即时导航（`document$`）的脚本需要改为在 `DOMContentLoaded` 时运行，因为 Sumi 使用普通的页面加载。
- Material 的内置插件——`blog`、`tags`、`social`、`privacy`、`offline`、`optimize` 等——是 Material 的一部分，不能和 Sumi 一起运行。Sumi 的插件自带[博客](../pages/blog.md)，并能原样读取 Material 的博客文章和 `.authors.yml`。

[面向插件作者](../customize/plugin-authors.md)介绍了如何同时支持两个主题。

## 速度与页面体积 {#speed-and-page-weight}

**构建。** 在 MkDocs NG 的[构建基准测试](https://mkdocs-ng.org/about/comparison/#build-speed)中，1,000 页的站点用 Sumi 0.2.0 构建需要 12.2 秒，用 Material 需要 11.1 秒。5,000 页时 Sumi 需要 67.6 秒，Material 需要 134.5 秒，因为 Material 会把整个导航写进每一个页面。`mkdocs serve` 中保存修改后，Sumi 1.8 秒、Material 2.7 秒就能看到更新。

**阅读。** 我们用两个主题的默认设置构建同一个页面——包含标题、代码块、标签页、表格和两个提示框——并在 Chromium 中加载：

| | Sumi 0.3.1 | Material for MkDocs 9.8.0 |
| --- | --- | --- |
| 请求数 | 5 | 8 |
| 发往其他服务器的请求 | 0 | 3，发往 Google Fonts |
| 传输量（压缩后） | 127 KB，其中字体 87 KB | 149 KB，其中字体 74 KB |
| JavaScript | 16 KB | 46 KB，含搜索 Worker |
{caption="测于 2026-11-06。设置 <code>theme.font: false</code> 后，Material 改用读者的系统字体：5 个请求，72 KB。"}

两者都很轻。更重要的区别在于请求发往哪里：Sumi 站点在防火墙后或内网中表现完全一样，读者也不会被字体或脚本 CDN 看到。

## 维护状态 {#maintenance}

Material for MkDocs 处于维护模式：作者宣布关键修复持续到 2027-05-05，之后推荐使用他们的新生成器 Zensical。MkDocs NG 项目维护着分支 [`mkdocs-ng-material`](https://github.com/mkdocs-ng/mkdocs-material)，它会接收 bug 修复，并保持与新版 MkDocs NG 兼容，所以现有的 Material 站点可以保持原样。

Sumi 是 MkDocs NG 新主题工作的所在，它会率先提供依赖 MkDocs NG 的功能，例如用一个 `mkdocs.yml` 管理所有语言。它也很年轻：2026-10-31 才首次发布，尚未到 1.0，所以请固定你测试过的版本，并在升级前阅读[发布记录](../../releases.md)。

## 试用 Sumi {#trying-sumi}

```diff title="mkdocs.yml"
 theme:
-  name: material
+  name: sumi
 plugins:
   - search
+  - sumi
```

运行 `mkdocs serve`，浏览一遍你的站点。[从 Material 迁移](migrate.md)列出了哪些继续可用、哪些需要调整。切换回去也是同样的两行：Sumi 的组件都是纯 Markdown，所以为 Sumi 写的页面在 Material 下依然好读。
