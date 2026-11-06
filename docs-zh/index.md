---
template: landing.html
title: Sumi
description: 一个现代、本地优先的 MkDocs 文档主题。
hero:
  eyebrow: "本地优先 · 为 MkDocs NG 打造"
  title: "写 Markdown，<br>*出好文档*。"
  text: "Sumi 是 MkDocs 的文档主题：内容始终是纯 Markdown，所有资源随站点一起发布，生成的页面人能读，AI 智能体也能读。"
  actions:
    - {text: 开始使用, link: docs/start/install/, icon: rocket, primary: true}
    - {text: 查看组件, link: docs/write/, icon: blocks}
  install: pip install mkdocs-sumi
  code:
    title: mkdocs.yml
    lang: yaml
    content: |
      site_name: 我的项目

      theme:
        name: sumi          # 纸、墨与一方朱印
        locale: zh          # 中文界面

      plugins:
        - search            # ⌘K 搜索，支持中文
        - llms_txt          # 每页一份 Markdown 副本
        - sumi              # 组件、博客、打印版
sections:
  - type: features
    eyebrow: 为什么选 Sumi
    title: 工程文档需要的都有，用不上的一概不加。
    text: 功能内置、资源本地，只在用到的页面上加载。
    items:
      - icon: file-text
        title: 组件就是 Markdown
        text: "提示框是 `> [!NOTE]`，步骤是带 `{.steps}` 的列表，标签页是带 `{tab=…}` 的代码块。源文件在 GitHub 上一样好读。"
        link: docs/write/
      - icon: hard-drive
        title: 本地优先，不依赖 CDN
        text: 字体、图标、搜索、Mermaid 和 KaTeX 都随主题发布。离线构建，随处托管，内网照常可用。
        link: docs/design/
      - icon: sparkles
        title: 也为智能体而写
        text: "每个页面都有一份干净的 `.md` 副本，并在 `<head>` 中声明；站点有 `llms.txt`；一键即可把页面复制为 Markdown。"
        link: docs/ai/
      - icon: command
        title: 搜索即命令面板
        text: "按 ⌘K 搜索所有标题，中文、日文同样可搜；输入 `>` 可切换主题、复制、打印等。"
        link: docs/customize/search/
      - icon: layout-template
        title: 文档、博客、首页、发布页
        text: 整个项目站点共用一套设计语言，从数据驱动的首页到带订阅源的博客和下载页。
        link: docs/pages/landing/
      - icon: puzzle
        title: 保留你的 MkDocs 内容
        text: "Admonition、`pymdownx` 标签页与折叠块、`mike` 多版本以及 Material 的 `extra` 配置都能继续使用。"
        link: docs/start/migrate/
  - type: split
    eyebrow: 原生 Markdown
    title: 写一次，到处都能读。
    text: "Sumi 从不要求你写私有方言。每个组件都是引用块、列表、表格或代码块，最多再加一行属性。同一个文件在 Sumi、GitHub 和智能体读取的 Markdown 副本中都能正常显示。"
    bullets:
      - "没有 MDX，没有短代码，页面里不需要 import。"
      - "每个组件都能退化为可读的 Markdown，打印时全部展开。"
      - "Mermaid 和 KaTeX 只在含有图表或公式的页面上加载。"
    code:
      title: docs/install.md
      lang: markdown
      content: |
        > [!TIP]
        > 建议使用虚拟环境。

        1. 安装主题
        2. 启用插件
        3. 运行 `mkdocs serve`
        {.steps}

        ```sh {tab="Linux"}
        pip install mkdocs-sumi
        ```

        ```powershell {tab="Windows"}
        py -m pip install mkdocs-sumi
        ```
  - type: stats
    items:
      - {value: "0", label: "运行时服务或 CDN"}
      - {value: "16", label: "原生 Markdown 组件"}
      - {value: "17 KB", label: "核心脚本（gzip），不依赖框架"}
      - {value: "13", label: "种界面语言，支持从右到左"}
  - type: steps
    eyebrow: 三分钟
    title: 从空文件夹到上线的站点。
    items:
      - title: 安装
        text: "`pip install mkdocs-sumi`，会一并装好 MkDocs。"
      - title: 配置
        text: "在 `mkdocs.yml` 中设置 `theme: sumi` 并添加 `sumi` 插件。"
      - title: 写作
        text: "运行 `mkdocs serve`，专心写 Markdown，其余交给 Sumi。"
      - title: 发布
        text: "`mkdocs build` 生成纯静态文件，可部署到任何托管服务。"
  - type: cta
    title: 好文档，值得一张好纸。
    text: Sumi 免费开源，采用 Apache 2.0 许可证。
    actions:
      - {text: 阅读文档, link: docs/, primary: true}
      - {text: 在 GitHub 上加星, link: "https://github.com/mkdocs-ng/mkdocs-sumi", icon: brand-github}
---
