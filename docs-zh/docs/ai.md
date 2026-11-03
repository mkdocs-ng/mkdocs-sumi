---
description: Sumi 如何为 AI 智能体发布每个页面：Markdown 副本、llms.txt、发现链接和一键复制。
---

# 面向人和智能体的文档

越来越多的文档读者不是人。编程智能体、AI 助手和搜索工具会读你的页面来回答关于项目的问题，而它们并不擅长读 HTML：导航、脚本和样式对它们来说都是噪音。Sumi 把每个页面发布两次：一份给人看的网页，一份给程序读的纯 Markdown。

## Sumi 发布的内容 {#what-sumi-publishes}

| 输出 | 位置 | 读者 |
| --- | --- | --- |
| HTML 页面 | `guide/install/` | 人 |
| Markdown 副本 | `guide/install.md` | 读取单个页面的智能体 |
| `llms.txt` | 站点根目录 | 探索站点的智能体 |
| `llms-full.txt` | 站点根目录 | 一次加载全部内容的智能体（需开启） |
| Atom 订阅 | `blog/feed.xml` | 订阅阅读器 |
| 打印版 | `print/` | 纸张、PDF、离线阅读 |
{caption="每种输出都是静态文件，都不需要服务器。"}

Markdown 副本和 `llms.txt` 由 [MkDocs NG](https://github.com/mkdocs-ng/mkdocs) 自带的 `llms_txt` 插件生成。把它和 `sumi` 一起启用：

```yaml title="mkdocs.yml"
site_url: https://example.com/docs/   # llms.txt 中的绝对链接需要它

plugins:
  - search
  - llms_txt:
      full_output: true   # 同时生成 llms-full.txt
  - sumi
```

可以在本站试试：打开 [llms.txt](https://sumi.mkdocs-ng.org/zh/llms.txt)，或在本页顶部的菜单中选择 **查看 Markdown**。

## 发现机制 {#discovery}

每个 HTML 页面都会在 `<head>` 中声明它的 Markdown 副本：

```html
<link rel="alternate" type="text/markdown" href="ai.md" title="Markdown">
<link rel="alternate" type="text/plain" href="../llms.txt" title="llms.txt">
```

智能体落在任何一个页面上，都能直接找到干净的版本，不用去猜 URL。

## 复制为 Markdown {#copy-as-markdown}

每页顶部的 **复制为 Markdown** 按钮会复制页面源码，也就是智能体读到的同一份文本，方便你粘贴到对话中。旁边的菜单还可以打开 Markdown 副本、打印页面，以及（如果你启用）在 AI 助手中打开本页：

```yaml title="mkdocs.yml"
plugins:
  - sumi:
      assistant_links: [claude, chatgpt]
```

> [!NOTE]
> 助手链接默认关闭：点击时会把页面地址发送给第三方服务。

## 为什么原生 Markdown 在这里很重要 {#why-native-markdown-matters-here}

用私有语法写的组件，比如 MDX、短代码或 HTML 小部件，到了智能体那里要么是一堆需要解读的原始标记，要么干脆丢失。Sumi 的组件是普通 Markdown 加一行属性，所以 Markdown 副本读起来很自然：提示框是引用，步骤是编号列表，标签页是带标签的连续代码块。

首页是唯一把内容放在 front matter 里的地方。对这类页面，Sumi 会生成一份 Markdown 副本，把主视觉、特性、步骤和常见问题写成标题和列表。
