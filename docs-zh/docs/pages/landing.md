---
description: 用 front matter 搭建产品首页：主视觉、功能介绍、代码、数据、步骤、常见问题和行动号召。
---

# 首页

首页就是一个设置了 `template: landing.html` 的 Markdown 文件。它的各个区块写在 front matter 里，所以整个页面都是可以在 diff 中审阅的数据：不写 HTML，也不用导入组件。[本站首页](../../index.md)就是这样做的。

```yaml title="docs/index.md"
---
template: landing.html
hero:
  eyebrow: "v2.0 已发布"
  title: "写出<br>*有人读的*文档。"
  text: 用一句话说明这个产品。
  actions:
    - {text: 开始使用, link: guide/, icon: rocket, primary: true}
    - {text: GitHub, link: "https://github.com/me/project", icon: brand-github}
  install: pip install my-project
sections:
  - type: features
    title: 有什么不同
    items:
      - {icon: zap, title: 快, text: 不到一秒就能构建完。, link: guide/speed/}
      - {icon: lock, title: 私密, text: 完全在你的电脑上运行。}
  - type: cta
    title: 准备好了吗？
    actions:
      - {text: 阅读指南, link: guide/, primary: true}
---
```

指向 Markdown 文件的链接，例如 `guide.md` 或 `guide/speed.md#cache`，会指向由该文件生成的页面。和 Markdown 链接一样，它相对于首页本身，文件不存在时构建会给出警告。其他链接相对于站点根目录，和 `nav` 条目一样。文本字段可以使用行内 Markdown，其中的 Markdown 链接（例如 `[指南](guide.md)`）也按同样的方式处理。

## 主视觉 {#hero}

| 键 | 类型 | 说明 |
| --- | --- | --- |
| `eyebrow` | string | 标题上方的短标签，例如发布公告。 |
| `title` | string | 大标题。`<br>` 用来换行；`*强调*` 会用强调色显示。默认为页面标题。 |
| `text` | string | 标题下方的一两句话。默认为 `site_description`。 |
| `actions` | list | 按钮：`text`、`link`、`icon`、`primary`。 |
| `install` | string | 显示在点击即可复制的框中的命令。 |
| `code` | object | 文字旁边的代码卡片：`title`、`lang`、`content`。 |
| `image` | string | 没有 `code` 时，显示在文字旁边的图片。 |
{.fields}

## 区块 {#sections}

`sections` 中的每个条目都有一个 `type`，以及可选的 `eyebrow`、`title`、`text`、`id` 和 `tone: soft`（带底色的背景）。

| 类型 | 键 | 说明 |
| --- | --- | --- |
| `features` | `items`、`columns` | 功能网格，每项有 `icon`、`title`、`text` 和可选的 `link`。 |
| `split` | `bullets`、`actions`、`code` 或 `image` 或 `markdown`、`reverse` | 一侧是文字，另一侧是插图。 |
| `stats` | `items` | 醒目的数字：`value` 和 `label`。 |
| `steps` | `items` | 带编号的步骤：`title` 和 `text`。 |
| `faq` | `items` | 问题与回答：`q` 和 `a`（Markdown）。 |
| `cta` | `actions` | 收尾的行动号召。 |
| `content` | `toc`、`aside` | 页面的 Markdown 正文。如果省略 `sections`，正文显示在主视觉下方。设 `toc: true` 时按文档页排版，旁边是页面目录；`aside` 在目录下方加入 `custom_dir` 中的一个模板。 |
| `include` | `template` | `custom_dir` 中你自己的模板，例如 `partials/demo.html`，显示在区块标题下方。它和其他覆盖模板一样，能用页面变量和主题的辅助函数。 |
{.fields meta="键"}

每个区块还可以设 `class`，给它的 `<section>` 加 CSS 类，方便在自己的样式表里单独调整。

### 首页就是规范 {#a-specification-on-the-home-page}

如果项目的首页就是文档本身（比如一份规范），可以保留主视觉，正文用文档页排版：

```yaml title="docs/index.md"
---
template: landing.html
hero:
  title: My Spec
  actions:
    - {text: 阅读规范, link: "#spec", primary: true}
sections:
  - {type: content, toc: true, id: spec}
  - {type: include, template: partials/playground.html, title: 试一试}
---
```

> [!TIP]
> 希望智能体和搜索引擎看到的内容，请写在页面正文里。front matter 中的区块是视觉呈现；首页的 Markdown 副本只包含标题、文字和正文。
