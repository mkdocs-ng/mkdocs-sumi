---
description: 带文件名、行号和复制按钮的语法高亮代码块。
---

# 代码块

围栏代码块在构建时由 Pygments 高亮。每个代码块都有复制按钮，页面上不附带任何 JavaScript 高亮库。

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

## 文件名 {#file-names}

在语言后面加 `title="…"`，就会在代码上方显示文件名：

````markdown
```toml title="pyproject.toml"
[project]
name = "my-docs"
dependencies = ["mkdocs-sumi"]
```
````

```toml title="pyproject.toml"
[project]
name = "my-docs"
dependencies = ["mkdocs-sumi"]
```

## 行号与高亮行 {#line-numbers-and-highlighted-lines}

这些选项来自 Python-Markdown 的 `codehilite`，如果你用的是 `pymdownx.highlight`，则来自它：

````markdown
```python hl_lines="2 3"
def total(items):
    subtotal = sum(i.price for i in items)
    return subtotal * 1.2
```
````

```python hl_lines="2 3"
def total(items):
    subtotal = sum(i.price for i in items)
    return subtotal * 1.2
```

要让每个代码块都显示行号，请配置扩展：

```yaml title="mkdocs.yml"
markdown_extensions:
  - codehilite:
      linenums: true
```

## 终端会话 {#shell-sessions}

带提示符和输出的终端记录请用 `console`。这样复制按钮只会复制命令，不带 `$` 提示符，也不带输出。

```console
$ mkdocs build
INFO    -  Building documentation to directory: site
INFO    -  Documentation built in 0.42 seconds
```

## 差异 {#diffs}

```diff
 theme:
-  name: mkdocs
+  name: sumi
```

## 行内代码 {#inline-code}

用单个反引号写行内代码：`mkdocs serve`。在正文中，Sumi 会给行内代码加一层浅色背景，浅色和深色模式下都清晰可读。

> [!TIP]
> 如果要按操作系统或语言分别展示多个版本，请看[标签页](tabs.md)。
