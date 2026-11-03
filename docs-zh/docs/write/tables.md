---
description: 带图注的表格，以及全宽、紧凑和斑马纹等样式。
---

# 表格

表格就是标准的 GitHub 风格 Markdown。Sumi 给它们加上边框和吸顶表头，在窄屏上可以横向滚动。

| 命令 | 用途 |
| --- | --- |
| `mkdocs new` | 新建项目 |
| `mkdocs serve` | 启动自动刷新的预览服务器 |
| `mkdocs build` | 构建站点 |
| `mkdocs gh-deploy` | 构建并部署到 GitHub Pages |

## 图注 {#captions}

```markdown
| 方案 | 价格 |
| --- | --- |
| 开源 | 免费 |
{caption="Sumi 采用 Apache 2.0 许可证。"}
```

| 方案 | 价格 |
| --- | --- |
| 开源 | 免费 |
{caption="Sumi 采用 Apache 2.0 许可证。"}

## 样式 {#variants}

在属性行上加一个或多个类名：

| 类名 | 效果 |
| --- | --- |
| `.wide` | 表格占满内容区的全部宽度 |
| `.compact` | 减小单元格内边距，适合密集数据 |
| `.striped` | 隔行加底色 |
| `.center` | 所有单元格居中 |
{.compact .striped}

```markdown
{.compact .striped caption="样式"}
```

## 对齐 {#alignment}

列对齐使用标准的冒号语法：

```markdown
| 左对齐 | 居中 | 右对齐 |
| :--- | :---: | ---: |
| a | b | 1.00 |
```

| 左对齐 | 居中 | 右对齐 |
| :--- | :---: | ---: |
| a | b | 1.00 |
| 较长的文字 | c | 120.50 |

> [!TIP]
> 列出选项和参数时，请用[字段](fields.md)，而不是很宽的表格。
