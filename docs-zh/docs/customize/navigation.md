---
description: 标签、侧边栏、章节首页、面包屑、版本和语言是如何生成的。
---

# 导航

Sumi 根据 MkDocs 的 `nav` 生成导航；没有 `nav` 时，根据文件夹结构生成。

```yaml title="mkdocs.yml"
nav:
  - 首页: index.md
  - 指南:
      - guide/index.md          # 章节首页
      - 安装: guide/install.md
      - 配置: guide/configure.md
  - 参考:
      - reference/index.md
      - 命令行: reference/cli.md
  - 博客: blog/index.md
```

## 标签与侧边栏 {#tabs-and-sidebar}

- 每个**顶层章节**都是页眉中的一个标签。侧边栏只显示当前标签下的页面。
- **顶层页面**，例如上面的“首页”和“博客”，也是标签。
- 如果一个章节的第一项是没有标题的 `index.md`，这个页面就是该章节的首页：标签、侧边栏标题和章节名都链接到它。
- 嵌套章节可以折叠。当前页面所在的章节是展开的。

在小屏幕上，标签和侧边栏会移进一个由菜单按钮打开的抽屉。

设置 `navigation_tabs: false` 后，整个导航都显示在侧边栏中。

## 页面目录 {#table-of-contents}

不超过 `toc_depth`（默认第 3 级）的标题会列在右侧，滚动时当前小节会高亮。在窄屏上，目录折叠在页面顶部。

## 上一页与下一页 {#previous-and-next}

上一页和下一页的链接按导航顺序排列。<kbd>[</kbd> 和 <kbd>]</kbd> 在页面间跳转；<kbd>j</kbd> 和 <kbd>k</kbd> 在标题间跳转。

## 版本 {#versions}

Sumi 读取 [mike](https://github.com/jimporter/mike) 写出的 `versions.json` 文件，在页眉中显示版本菜单，并在旧版本上显示提示。

```yaml title="mkdocs.yml"
theme:
  name: sumi
  version_provider: mike
```

```sh
mike deploy --push --update-aliases 0.2 latest
mike set-default --push latest
```

## 语言 {#languages}

在多语言站点上，页眉会显示语言菜单，命令面板也会为每种语言加一条“切换语言：……”命令。使用 MkDocs NG 1.11 或更高版本时，把各语言列在 `languages` 下，菜单就会把每个页面链接到其他语言中的同一页面；见[语言](i18n.md#multilingual-sites)。

使用较旧的 MkDocs，或者要链接到其他站点时，自己把它们列在 `extra.alternate` 下：

```yaml title="mkdocs.yml"
extra:
  alternate:
    - name: English
      link: /en/
      lang: en
    - name: 简体中文
      link: /zh/
      lang: zh
```

## 编辑链接 {#edit-links}

设置了 `repo_url` 和 `edit_uri` 后，每个页面底部和页面菜单中都会显示 **编辑此页**。

```yaml title="mkdocs.yml"
repo_url: https://github.com/me/project
edit_uri: edit/main/docs/
```
