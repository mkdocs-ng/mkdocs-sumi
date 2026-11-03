---
description: 本地全文搜索、中日韩文字支持，以及命令面板。
---

# 搜索与命令

在任何地方按 <kbd>⌘</kbd> <kbd>K</kbd>、<kbd>Ctrl</kbd> <kbd>K</kbd> 或 <kbd>/</kbd> 即可搜索。搜索在浏览器中运行，使用的是 MkDocs `search` 插件构建的索引，不会向服务器发送任何内容。

```yaml title="mkdocs.yml"
plugins:
  - search
  - sumi
```

## 结果如何排序 {#how-results-are-ranked}

- 每个页面和每个小节标题都是一条结果，所以点击匹配项会直接跳到对应的位置。
- 标题中的匹配排在正文匹配之前；以查询词开头的标题排在最前。
- 所有词都必须匹配。匹配的词会在结果和正文摘要中高亮。

索引在第一次打开面板时才加载，不随页面一起加载。

## 中文、日文和韩文 {#chinese-japanese-and-korean}

中日韩文字的词与词之间没有空格，按词搜索什么也找不到。Sumi 按子串匹配中日韩文字：搜索 `安装` 能找到*安装指南*和*如何安装*。`mkdocs 主题` 这样的混合查询会被拆成一个拉丁文词和一个中文词。

## 命令 {#commands}

面板同时也是命令启动器。输入 `>`（或者在页面上按 <kbd>></kbd>）只列出命令：

| 命令 | 作用 |
| --- | --- |
| 切换浅色 / 深色 | 在浅色和深色之间切换（<kbd>t</kbd>） |
| 复制本页 Markdown | 复制页面的 Markdown 源码 |
| 以 Markdown 打开本页 | 在新标签页中打开 Markdown 副本 |
| 编辑本页 | 在你的仓库中打开这个页面 |
| 打印本页 | 打印当前页面 |
| 回到顶部 / 回到首页 | 页面跳转 |
| 切换语言 / 切换版本 | 配置了 `extra.alternate` 或多版本时可用 |
| 打开 llms.txt | 启用 `llms_txt` 插件时可用 |

按 <kbd>?</kbd> 可以查看所有键盘快捷键。

## 排除页面 {#excluding-pages}

用标准的 `search` front matter 让某个页面不进入索引：

```yaml
---
search:
  exclude: true
---
```
