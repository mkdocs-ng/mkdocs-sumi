---
description: 安装 Sumi，并在 MkDocs 项目中启用它。
---

# 安装

Sumi 是一个 Python 包。它依赖 [MkDocs NG](https://github.com/mkdocs-ng/mkdocs)，所以安装 Sumi 时会一并安装 MkDocs。

## 环境要求 {#requirements}

- Python 3.10 或更高版本
- 一个 MkDocs 项目，或者一个空文件夹

## 安装软件包 {#install-the-package}

```sh {tab="pip"}
pip install mkdocs-sumi
```

```sh {tab="uv"}
uv add --dev mkdocs-sumi
```

```sh {tab="pipx"}
pipx install mkdocs-ng --include-deps
pipx inject mkdocs-ng mkdocs-sumi
```

> [!TIP]
> 在国内网络环境下，可以加上镜像源，例如 `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple mkdocs-sumi`。Sumi 安装后不再访问任何外部网络。

## 启用主题和插件 {#enable-the-theme-and-the-plugin}

Sumi 分为两部分：**主题**负责绘制页面，**插件**负责 Markdown 组件、博客和额外的输出。两者都要启用：

```yaml title="mkdocs.yml"
theme:
  name: sumi
  locale: zh  # 中文界面；默认是 en

plugins:
  - search    # 提供 ⌘K 搜索
  - llms_txt  # 可选：生成 llms.txt 和每页的 Markdown 副本
  - sumi
```

> [!IMPORTANT]
> 一旦写了 `plugins:` 列表，MkDocs 就不会再自动启用 `search`。请像上面那样显式列出。

## 预览 {#preview}

```sh
mkdocs serve
```

打开 <http://127.0.0.1:8000/>，按 <kbd>⌘</kbd> <kbd>K</kbd>（或 <kbd>Ctrl</kbd> <kbd>K</kbd>）即可搜索。

## 下一步 {#next}

继续阅读[第一个站点](first-site.md)，或直接跳到[写作](../write/index.md)。
