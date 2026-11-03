---
description: 用 Sumi 从空文件夹开始搭建并部署一个新站点。
---

# 第一个站点

本页从零搭建一个小站点：一个首页、两个指南页面和一篇博客文章。

> [!TIP]
> 想更快？[sumi-starter](https://github.com/mkdocs-ng/sumi-starter) 是一个现成的模板仓库，包含中英文两套内容和 GitHub Pages 部署流程，点 **Use this template** 即可开始。

1. 创建项目

    ```sh
    mkdocs new my-docs
    cd my-docs
    ```

2. 规划文件

    ```filetree
    my-docs/
    ├── docs/
    │   ├── index.md            # 首页
    │   ├── guide/
    │   │   ├── index.md        # 分区首页，侧边栏标题链接到这里
    │   │   └── install.md
    │   └── blog/
    │       └── posts/
    │           └── hello.md    # blog/ 下的页面都是博客文章
    └── mkdocs.yml              # 站点配置
    ```

3. 配置站点

    ```yaml title="mkdocs.yml"
    site_name: 我的文档
    site_url: https://example.com/
    repo_url: https://github.com/me/my-docs

    theme:
      name: sumi
      locale: zh

    plugins:
      - search
      - sumi
    ```

4. 预览并构建

    ```sh
    mkdocs serve        # 实时预览
    mkdocs build        # 把静态文件写入 site/
    ```
{.steps}

## 导航如何生成 {#how-navigation-is-built}

顶层分区会成为页眉中的**标签**，当前标签内的页面显示在**侧边栏**中。如果一个分区的第一页是 `index.md`，它就是该分区的首页，点击分区标题会打开它。

> [!TIP]
> 不写 `nav:` 时，MkDocs 会按文件夹结构生成导航。博客文章会自动从侧边栏中排除。

## 部署 {#deploy}

`mkdocs build` 会把纯 HTML、CSS 和 JavaScript 写入 `site/`。把这个文件夹上传到任意静态托管服务即可：GitHub Pages、Cloudflare Pages、Netlify、对象存储或 Nginx 服务器都行。部署后不需要运行任何程序。

```sh
mkdocs gh-deploy      # 构建并推送到 gh-pages 分支
```
