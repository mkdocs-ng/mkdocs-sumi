---
description: Sumi 背后的原则，以及由此带来的取舍。
---

# 设计原则

*Sumi*（墨）是东亚书画所用的墨。一种墨，研磨出不同的浓淡，就能画出纸上所有的层次。这个主题遵循同样的思路：暖色的纸、黑色的墨、一点像印章一样的朱红，此外不放任何不传达信息的东西。

## 内容始终是 Markdown {#content-stays-markdown}

文档比渲染它的工具活得更久。为 Sumi 写的页面，在 GitHub、编辑器和终端里都必须讲得通，所以每个组件都用 Markdown 自己的词汇来写：引用块、列表、表格、图片和代码块，最多再加一行 `{…}` 属性。哪天你不用 Sumi 了，内容也能原封不动地带走。

这就排除了短代码、MDX 和内联 HTML 小部件，也是组件数量不多的原因。每个组件之所以存在，是因为技术文档经常需要它：警示、操作步骤、多选一、参考信息、布局和图表。

## 一切都在本地 {#everything-is-local}

构建好的 Sumi 站点不会发出任何你没有配置的网络请求。字体（Inter 和 JetBrains Mono）、2 000 个图标、搜索索引、Mermaid 和 KaTeX 都是主题的一部分，会被复制到你的站点中。这意味着：

- 站点在防火墙后、内网里、U 盘上都能用；
- 读者不会被字体或脚本 CDN 追踪；
- 今天构建和五年后构建，得到的是同样的页面。

## 用到什么才加载什么 {#pay-only-for-what-you-use}

主题的核心是一个样式表和一个脚本，不依赖任何框架。较重的运行时按需加载：Mermaid 只在图表接近视口时加载，而且只加载该图表类型所需的代码；KaTeX 只在有公式的页面上加载；搜索索引只在打开命令面板时加载。只有当某个页面用到时，相应的第三方文件才会被复制进站点。

## 优雅降级 {#degrade-gracefully}

每个页面在没有 JavaScript 时都能阅读：导航是链接，折叠区是 `<details>`，标签页依次排开，文件树是嵌套列表。JavaScript 只增加便利，比如搜索、标签同步、复制按钮和目录高亮，从不承载内容。

## 人和智能体都是读者 {#people-and-agents-are-both-readers}

每个页面都以 HTML 发布给人，以 Markdown 发布给程序，每个 HTML 页面都链接到它的 Markdown 副本。详见[面向人和智能体的文档](ai.md)。

## 一套设计语言 {#one-design-language}

文档、博客、首页、发布下载页和打印版共用一套设计令牌：字号、间距、颜色和组件。用 Sumi 搭建的项目站点看起来是一个完整的产品，而不是一个文档主题外面再拼一个营销页。

## 致谢 {#credits}

Sumi 的原则受到了 [Oink](https://github.com/pgsty/oink)（冯若航为 Hugo 打造的文档发行版）的启发，也受益于 MkDocs 主题的悠久传统，尤其是 [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)。Sumi 能读取 Material 的配置，方便现有站点切换过来。Sumi 的代码和设计均为原创。
