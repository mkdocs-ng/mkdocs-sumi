---
description: 用 tree 的输出画出项目结构，带图标和注释。
---

# 文件树

`filetree` 代码块会把目录列表变成一棵可浏览的树，带文件夹和文件图标。可以直接粘贴 `tree` 的输出，也可以用普通缩进写出结构。

````markdown
```filetree
my-docs/
├── docs/                 # Markdown 源文件
│   ├── index.md
│   ├── guide/
│   │   ├── install.md
│   │   └── usage.md
│   └── assets/
│       └── logo.svg
├── overrides/            # 模板覆盖（可选）
│   └── main.html
├── pyproject.toml
└── mkdocs.yml            # 站点配置
```
````

```filetree
my-docs/
├── docs/                 # Markdown 源文件
│   ├── index.md
│   ├── guide/
│   │   ├── install.md
│   │   └── usage.md
│   └── assets/
│       └── logo.svg
├── overrides/            # 模板覆盖（可选）
│   └── main.html
├── pyproject.toml
└── mkdocs.yml            # 站点配置
```

## 规则 {#rules}

- 以 `/` 结尾的名称，或者带有子项的名称，是文件夹。点击文件夹可以折叠。
- ` # ` 后面的文字是注释，会对齐成一列。
- 文件图标按扩展名区分：代码、文本、配置、数据、图片和压缩包。
- 用空格缩进和用 `├──` 这类框线字符效果一样。

## 普通缩进 {#plain-indentation}

````markdown
```filetree title="包结构"
src/
  mkdocs_sumi/
    plugin.py      # MkDocs 插件
    theme/         # Jinja 模板和静态资源
tests/
```
````

```filetree title="包结构"
src/
  mkdocs_sumi/
    plugin.py      # MkDocs 插件
    theme/         # Jinja 模板和静态资源
tests/
```

这棵树在构建时用普通的 HTML `<details>` 元素生成，所以不需要 JavaScript，打印时会完全展开。
