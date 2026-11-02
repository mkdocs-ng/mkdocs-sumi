---
description: Sumi 为 Markdown 增加的所有组件概览，以及它们共同遵循的一条规则。
---

# 用 Sumi 写作

Sumi 为 Markdown 增加了十六个组件。它们都没有引入会在 GitHub 上失效的新语法：每个组件都是引用块、列表、表格、图片或代码块，有时下面再跟一行花括号里的属性。

```markdown
1. 安装主题
2. 启用插件
{.steps}
```

不认识 Sumi 的渲染器看到的是一个编号列表；Sumi 看到的是一组操作步骤。

## 组件

各组件的详细说明目前只有英文版，下表链接到英文页面。

| 组件 | 写法 | 说明页 |
| --- | --- | --- |
| 提示框 | `> [!NOTE]`、`> [!TIP]-` | [Callouts](https://sumi.mkdocs-ng.org/docs/write/callouts/) |
| 带标题的代码块 | ```` ```py title="app.py" ```` | [Code blocks](https://sumi.mkdocs-ng.org/docs/write/code/) |
| 标签页 | ```` ```sh {tab="Linux"} ```` | [Tabs](https://sumi.mkdocs-ng.org/docs/write/tabs/) |
| 步骤 | 有序列表 + `{.steps}` | [Steps](https://sumi.mkdocs-ng.org/docs/write/steps/) |
| 卡片 | 链接组成的无序列表 + `{.cards}` | [Cards](https://sumi.mkdocs-ng.org/docs/write/cards/) |
| 字段表 | 表格 + `{.fields}` | [Fields](https://sumi.mkdocs-ng.org/docs/write/fields/) |
| 表格选项 | 表格 + `{.wide}`、`{caption="…"}` | [Tables](https://sumi.mkdocs-ng.org/docs/write/tables/) |
| 图片与图注 | 图片 + `{caption="…"}` | [Images](https://sumi.mkdocs-ng.org/docs/write/images/) |
| 图集 | 图片列表 + `{.gallery}` | [Galleries](https://sumi.mkdocs-ng.org/docs/write/gallery/) |
| 文件树 | ```` ```filetree ```` | [File trees](https://sumi.mkdocs-ng.org/docs/write/filetree/) |
| 图表（Mermaid） | ```` ```mermaid ```` | [Diagrams](https://sumi.mkdocs-ng.org/docs/write/diagrams/) |
| 数据图表 | ```` ```echarts ````（YAML 或 JSON） | [Charts](https://sumi.mkdocs-ng.org/docs/write/charts/) |
| 思维导图 | ```` ```markmap ```` | [Mind maps](https://sumi.mkdocs-ng.org/docs/write/charts/#mind-maps) |
| 数学公式 | `$…$`、`$$…$$` | [Math](https://sumi.mkdocs-ng.org/docs/write/math/) |
| 按键与图标 | `++Ctrl+K++`、`:lucide-rocket:` | [Keys and icons](https://sumi.mkdocs-ng.org/docs/write/keys-icons/) |
| 徽章 | `**新**{.badge}` | [Badges](https://sumi.mkdocs-ng.org/docs/write/badges/) |
{.wide}

## 属性行

属性行是一个只包含 `{…}` 的段落，紧跟在它所修饰的块下方。它可以带类名、id 和键值对：

```markdown
| 名称 | 类型 |
| --- | --- |
| `port` | integer |
{.fields #server-options caption="服务器选项"}
```

Sumi 不认识的类名会原样保留，你可以在 `extra_css` 中自己给这些块加样式。

## 一个例子

下面三个组件就是用上面的写法渲染出来的。

> [!TIP]
> 提示框是一个以 `[!TIP]` 开头的引用块。在 GitHub 上它同样显示为提示。

1. 写一个有序列表
2. 在下面加一行 `{.steps}`
3. 它就变成了步骤
{.steps}

| 选项 | 类型 | 说明 |
| --- | --- | --- |
| `locale` | string | 界面语言：`en`、`zh`、`zh_TW` |
| `palette` | string | `auto`、`light` 或 `dark` |
{.fields}

## Markdown 扩展

`sumi` 插件会替你启用以下 Python-Markdown 扩展，无需额外配置：

- `attr_list`、`md_in_html`、`tables`、`toc`（带永久链接）、`footnotes`、`def_list`、`admonition`
- `fenced_code` 和 `codehilite`。如果配置了 `pymdownx.superfences` 和 `pymdownx.highlight`，Sumi 会把代码交给它们处理

`markdown_extensions` 中的其他扩展照常工作。

> [!TIP]
> 本站每个页面都是用这些组件写的。点击页面顶部的 **复制为 Markdown** 即可查看源码。
