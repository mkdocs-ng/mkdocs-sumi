---
description: 把不同选项（操作系统、编程语言、包管理器）显示为标签页。
---

# 标签页

连续的几个代码块，每个都带 `{tab="…"}`，就会合成一组标签页。没有 Sumi 时，它们只是几个连续的代码块，各自标明了用途。

````markdown
```sh {tab="macOS"}
brew install python
```

```sh {tab="Ubuntu"}
sudo apt install python3
```

```powershell {tab="Windows"}
winget install Python.Python.3.12
```
````

```sh {tab="macOS"}
brew install python
```

```sh {tab="Ubuntu"}
sudo apt install python3
```

```powershell {tab="Windows"}
winget install Python.Python.3.12
```

## 同步切换 {#synchronised-tabs}

标签相同的几组标签页会同步切换：选一次 **Windows**，所有页面上标签相同的标签页都会跟着切换。浏览器会记住这个选择。

```sh {tab="macOS"}
python3 -m venv .venv && source .venv/bin/activate
```

```sh {tab="Ubuntu"}
python3 -m venv .venv && source .venv/bin/activate
```

```powershell {tab="Windows"}
py -m venv .venv; .venv\Scripts\Activate.ps1
```

## 标签页中的标题 {#titles-inside-tabs}

`title` 和 `tab` 可以一起用：

````markdown
```yaml {tab="YAML" title="mkdocs.yml"}
theme: sumi
```

```toml {tab="TOML" title="pyproject.toml"}
[tool.mkdocs]
theme = "sumi"
```
````

```yaml {tab="YAML" title="mkdocs.yml"}
theme:
  name: sumi
```

```toml {tab="TOML" title="pyproject.toml"}
[tool.mkdocs]
theme = "sumi"
```

## 包含正文的标签页 {#tabs-with-prose}

如果标签页里不只是代码，请使用 `pymdownx.tabbed` 并设置 `alternate_style: true`。Sumi 会给它配上一致的样式：

```yaml title="mkdocs.yml"
markdown_extensions:
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
```

打印时以及在 Markdown 副本中，所有标签页会依次显示在各自的标签下。
