---
description: 把整个站点变成一个可打印的页面，任何单个页面也都能干净地打印。
---

# 打印版

Sumi 会把整个站点按导航顺序写成一个长页面，放在 `/print/`，带封面和目录。打开它，打印为 PDF，就得到一本离线手册。打开[本站的打印版](../../print/index.html)。

每个页面单独打印也很干净：页眉、侧边栏和按钮会隐藏，折叠的提示框会展开，标签页依次显示，链接会显示出地址。

## 工作原理 {#how-it-works}

打印版在页面渲染完成后，由和页面相同的 HTML 生成。页面之间的链接变成文档内部的链接；图片和其他资源的路径会重新调整，使它们从 `/print/` 也能正确加载。

## 选项 {#options}

```yaml title="mkdocs.yml"
plugins:
  - sumi:
      print:
        enabled: true
        path: print/
```

使用页面操作菜单中的 **打印** 命令，或者按 <kbd>⌘</kbd> <kbd>K</kbd> 后输入 `> print`。

> [!TIP]
> 要让某个页面不出现在打印版中，在它的 front matter 中加上 `print: false`。
