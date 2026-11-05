---
description: sumi 插件的选项：组件、博客、打印版、Git 日期和 AI 链接。
---

# 插件选项

`sumi` 插件提供 Markdown 组件、博客、打印版、复制为 Markdown 按钮和 Git 日期。主题依赖这个插件；不加任何选项也能用。

```yaml title="mkdocs.yml"
plugins:
  - search
  - llms_txt
  - sumi:
      git_dates: true
      assistant_links: [claude, chatgpt]
```

## 选项 {#options}

| 选项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `language` | string | `theme.locale` | 提示框默认标题和自动生成文字所用的语言。 |
| `math` | boolean | `true` | 解析 `$…$` 和 `$$…$$`，并在用到它们的页面上加载 KaTeX。 |
| `mermaid` | boolean | `true` | 渲染 `mermaid` 代码块，并在用到它们的页面上加载 Mermaid。 |
| `echarts` | boolean | `true` | 把 `echarts` 代码块（YAML 或 JSON 配置项）渲染为数据图。见[数据图](../write/charts.md)。 |
| `markmap` | boolean | `true` | 把 `markmap` 代码块（Markdown 大纲）渲染为思维导图。见[思维导图](../write/charts.md#mind-maps)。 |
| `markdown_copy` | boolean | `true` | 当页面有 Markdown 副本时，显示 **复制为 Markdown** 和 **查看 Markdown**。 |
| `assistant_links` | list | `[]` | 在页面菜单中加入“在 Claude 中打开”或“在 ChatGPT 中打开”：`claude`、`chatgpt`。默认关闭，因为它们会把页面地址发送给第三方。 |
| `git_dates` | boolean | `false` | 根据最后一次修改该页面的 Git 提交显示“最后更新”。每次构建只运行一次 `git log`。 |
| `date_format` | string | 无 | 主题显示的所有日期使用的 `strftime` 格式，例如 `"%Y-%m-%d"`。默认按页面语言写出日期：“November 5, 2026”、“2026年11月5日”。 |
| `blog.enabled` | boolean | `true` | 把 `blog.dir` 下的文件当作文章。 |
| `blog.dir` | string 或 list | `blog` | `docs/` 下的博客文件夹，也可以是多个文件夹的列表。 |
| `blog.layout` | string | `list` | `list` 或 `cards`。 |
| `blog.tags_dir` | string | 无 | 在这个文件夹下为每个标签生成页面，并生成标签列表。 |
| `blog.feed` | boolean | `true` | 把 Atom 订阅源写到 `blog/feed.xml`。 |
| `blog.feed_items` | integer | `20` | 订阅源中的文章数；`0` 表示全部文章。 |
| `blog.feed_path` | string | 无 | 订阅源的写入位置，例如 `index.xml`。 |
| `blog.feed_format` | string | `atom` | `atom` 或 `rss`。 |
| `blog.authors` | mapping | `{}` | 作者信息，如果你不想用 `.authors.yml`。 |
| `print.enabled` | boolean | `true` | 生成[打印版](../pages/print.md)。 |
| `print.path` | string | `print/` | 打印版的输出位置。 |
{.fields}

## Markdown 扩展 {#markdown-extensions}

插件会启用组件所依赖的一小组 Python-Markdown 扩展，列表见[写作](../write/index.md#markdown-extensions)。你自己在 `markdown_extensions` 中的配置优先：如果你给其中某个扩展配置了选项，就用你的选项。

## 在 CI 中使用 Git 日期 {#git-dates-in-ci}

浅克隆只包含最后一次提交，这会让每个页面看起来都是今天更新的。构建前请拉取完整历史：

```yaml title=".github/workflows/docs.yml"
- uses: actions/checkout@v5
  with:
    fetch-depth: 0
```
