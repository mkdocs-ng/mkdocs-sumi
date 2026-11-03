---
date: 2026-11-01
authors: [xianpeng]
tags: [release, design]
image: assets/screens/home-light.jpg
hide_cover: true
description: Sumi 0.1 是一个本地优先的 MkDocs 文档主题：内容始终是纯 Markdown，发布出来的页面人能读，智能体也能读。
---

# Sumi 来了

今天我们发布 Sumi 0.1，一个面向 MkDocs NG 的文档主题。它是 MkDocs NG 项目打造的第一个主题，目标是为工程团队完整回答“我们的文档应该长什么样”这个问题。

<!-- more -->

## 为什么还要一个主题 {#why-another-theme}

MkDocs 让写文档变得简单：写 Markdown，运行一条命令，得到一个网站。这些年来，好看的 MkDocs 站点越来越依赖一长串扩展，每个扩展都有自己的语法。为一个主题写的内容，换个地方就没法读了。

Sumi 回到最初的承诺。它增加了十二个组件，每一个都用原生 Markdown 书写：提示框是引用块，步骤是编号列表，标签页是带标签的代码块。你的源文件在 GitHub 上和终端里依然好读。

## 0.1 包含什么 {#what-is-in-01}

- :lucide-book-open: **完整的文档布局**：顶部标签、侧边栏、页内目录，以及上一页 / 下一页链接。
- :lucide-command: **搜索即命令面板**：本地运行，支持中日韩文字，按 ++Cmd+K++ 打开。
- :lucide-layout-template: **首页、博客、发布页和打印版**：几种页面类型共用一套设计。
- :lucide-sparkles: **每个页面都有 Markdown 副本**，并为 AI 智能体提供 `llms.txt` 链接。
- :lucide-hard-drive: **不依赖 CDN**：字体、图标、Mermaid 和 KaTeX 都随主题附带。

## 试一试 {#try-it}

```sh
pip install mkdocs-sumi
```

```yaml title="mkdocs.yml"
theme:
  name: sumi
plugins:
  - search
  - sumi
```

然后阅读[文档](../../docs/index.md)。本站就是用 Sumi 构建的，每个页面同时也是一个示例。欢迎在 [GitHub](https://github.com/mkdocs-ng/mkdocs-sumi/issues) 上反馈意见、报告问题。

## 致谢 {#thanks}

Sumi 的设计原则很大程度上受益于冯若航的 [Oink](https://github.com/pgsty/oink)。它展示了一个文档发行版只靠纯 Markdown、不依赖任何外部服务，能做到多少事。
