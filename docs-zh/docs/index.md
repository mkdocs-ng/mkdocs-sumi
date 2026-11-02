---
description: Sumi 是什么、包含哪些功能，以及从哪里开始。
---

# Sumi 文档

Sumi 是 [MkDocs](https://github.com/mkdocs-ng/mkdocs) 的文档主题。它把一个装满纯 Markdown 的文件夹变成完整、可搜索、可打印的网站，包括首页、博客和发布记录，而且不需要 Node.js、CDN 或任何托管服务。

- :lucide-rocket: [安装](start/install.md)
  两行配置，把 Sumi 加到现有的 MkDocs 项目中。
- :lucide-pen-line: [写作](write/index.md)
  十六个组件，全部用原生 Markdown 书写。
- :lucide-layout-template: [页面类型](https://mkdocs-ng.github.io/mkdocs-sumi/docs/pages/landing/)
  首页、博客、发布下载页和打印版（英文）。
- :lucide-sliders-horizontal: [自定义](https://mkdocs-ng.github.io/mkdocs-sumi/docs/customize/theme/)
  颜色、导航、搜索、语言、版本和模板覆盖（英文）。
{.cards}

## 包含什么

| 方面 | 内置功能 |
| --- | --- |
| 阅读 | 顶部标签、可折叠侧边栏、面包屑、随滚动高亮的目录、上一页 / 下一页 |
| 查找 | 支持中日韩文字的本地全文搜索，与命令面板合二为一（<kbd>⌘</kbd> <kbd>K</kbd>） |
| 写作 | 提示框、标签页、步骤、卡片、字段表、图注、图集、徽章、文件树、Mermaid、ECharts、思维导图、KaTeX、按键、1 900 多个图标 |
| 页面 | 数据驱动的首页、带标签和 Atom 订阅的博客、带校验和的发布页、整站打印版 |
| 输出 | HTML、打印版、每页一份 Markdown 副本、`llms.txt`、Atom |
| 运维 | 深色模式、mike 多版本、语言切换、编辑链接、Git“最后更新”日期、统计分析 |
{caption="以上功能均随主题发布。无论构建还是阅读，都不会从网络获取任何内容。"}

## 原则

Sumi 遵循四条规则，详见[设计原则](design.md)。

1. **内容始终是 Markdown。** 组件就是引用块、列表、表格或代码块，加一行属性。
2. **一切都在本地。** 每个字体、图标和脚本都是你构建出的站点的一部分。
3. **用到什么才加载什么。** 图表和公式只在包含它们的页面上加载运行时。
4. **人和智能体都是读者。** 每个页面都同时以 HTML 和 Markdown 发布。
