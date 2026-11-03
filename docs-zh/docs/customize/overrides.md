---
description: 用 MkDocs 的 custom_dir 覆盖模板和模板块。
---

# 覆盖模板

Sumi 是标准的 MkDocs 主题，所以任何模板都可以用 `custom_dir` 覆盖：

```yaml title="mkdocs.yml"
theme:
  name: sumi
  custom_dir: overrides
```

```filetree
overrides/
├── main.html                 # 为所有页面扩展模板块
└── partials/
    └── footer.html           # 替换一个局部模板
```

## 扩展模板块 {#extending-blocks}

创建 `overrides/main.html`，继承 `base.html`：

```jinja title="overrides/main.html"
{% extends "base.html" %}

{% block extrahead %}
  <meta name="robots" content="noindex">
{% endblock %}
```

| 模板块 | 内容 |
| --- | --- |
| `site_meta` | `<head>` 中的 `<meta>` 和 `<link>` 标签 |
| `htmltitle` | `<title>` 元素 |
| `styles` | 样式表 |
| `analytics` | 统计分析代码 |
| `extrahead` | 空块，用来放你自己的标签 |
| `header` | 站点页眉 |
| `layout` | 侧边栏、正文和目录 |
| `content` | 正文 |
| `page_content` | 渲染后的 Markdown |
| `article_footer` | 最后更新时间、编辑链接、上一页 / 下一页 |
| `footer` | 站点页脚 |
| `scripts` | `<body>` 末尾的脚本 |
{.compact}

## 局部模板 {#partials}

| 局部模板 | 用途 |
| --- | --- |
| `partials/header.html` | 标志、标签、搜索按钮、菜单 |
| `partials/logo.html` | 只有标志 |
| `partials/breadcrumbs.html` | 标题上方的路径 |
| `partials/page-actions.html` | 复制为 Markdown 和页面菜单 |
| `partials/toc.html` | 页面目录 |
| `partials/article-footer.html` | 正文下方 |
| `partials/footer.html` | 站点页脚 |
| `partials/palette.html` | 搜索和命令面板 |
| `partials/analytics.html` | 统计分析 |
{.compact}

## 统计分析 {#analytics}

支持 Google Analytics，配置键和 Material 相同：

```yaml title="mkdocs.yml"
extra:
  analytics:
    provider: google
    property: G-XXXXXXXXXX
```

如果用别的统计服务，把它的代码加到 `overrides/main.html` 的 `analytics` 块中。

> [!NOTE]
> 统计分析是唯一会联系第三方的功能，不配置就不会开启。
