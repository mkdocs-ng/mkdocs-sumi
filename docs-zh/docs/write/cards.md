---
description: 用于章节首页的链接卡片网格。
---

# 卡片

由链接组成的无序列表，后面跟一行 `{.cards}`，就会变成卡片网格。链接是卡片标题，链接后的文字是说明，开头的行内图标会成为卡片图标。

```markdown
- :lucide-rocket: [安装](../start/install.md)
  把 Sumi 加到项目中。
- :lucide-pen-line: [写作](index.md)
  用原生 Markdown 书写的组件。
- :lucide-palette: [自定义](../customize/theme.md)
  颜色、字体和布局。
{.cards}
```

- :lucide-rocket: [安装](../start/install.md)
  把 Sumi 加到项目中。
- :lucide-pen-line: [写作](index.md)
  用原生 Markdown 书写的组件。
- :lucide-palette: [自定义](../customize/theme.md)
  颜色、字体和布局。
{.cards}

## 列数 {#columns}

卡片会排成尽可能多的列，最多三列。用 `cols` 可以固定列数：

```markdown
{.cards cols=2}
```

- :brand-github: [源代码](https://github.com/mkdocs-ng/mkdocs-sumi)
  报告问题或提交 Pull Request。
- :brand-python: [PyPI](https://pypi.org/project/mkdocs-sumi/)
  版本历史和下载。
{.cards cols=2}

## 不带链接的卡片 {#cards-without-links}

没有链接的列表项会显示为静态卡片，适合用来列出功能：

- :lucide-hard-drive: **本地优先**
  所有资源都随站点一起发布。
- :lucide-zap: **快速**
  不用框架，只有一个小脚本。
- :lucide-printer: **可打印**
  整站打印版。
{.cards}

## 参考 {#reference}

| 项目 | 说明 |
| --- | --- |
| 输出 | `<ul class="sumi-cards">`，每张卡片一个 `<li>`，整张卡片都可点击。 |
| 没有 Sumi 时 | 一个带说明的链接列表。 |
| JavaScript | 不需要。 |
| 限制 | 每张卡片一个链接，作为卡片标题。说明控制在一两句话，卡片才能对齐。 |
{.compact}
