---
description: 用一个装满 Markdown 文件的文件夹生成博客，带作者、标签、阅读时长和 Atom 订阅源。
---

# 博客

`docs/blog/` 下的每个 Markdown 文件都是一篇文章。Sumi 会生成博客首页，让文章不出现在侧边栏中，并输出一个 Atom 订阅源。不需要再装别的插件。

```filetree
docs/
└── blog/
    ├── .authors.yml          # 可选：作者姓名和头像
    ├── index.md              # 可选：博客标题和简介
    └── posts/
        ├── 2026-11-01-introducing-sumi.md
        └── 2026-11-15-search.md
```

可以看看[本站的博客](../../blog/index.md)。

## 写一篇文章 {#writing-a-post}

```markdown title="docs/blog/posts/2026-11-01-introducing-sumi.md"
---
date: 2026-11-01
authors: [xianpeng]
tags: [release, design]
description: Sumi 0.1 发布了。
---

# Sumi 来了

第一段是显示在博客首页上的摘要。

<!-- more -->

文章的其余部分。
```

| 键 | 类型 | 说明 |
| --- | --- | --- |
| `date` | date | 发布日期。默认为最后一次 Git 提交的日期，或者文件的修改时间。 |
| `updated` | date | 在文章中显示为“更新于”。 |
| `authors` | list | `.authors.yml` 中的作者 id，或者直接写姓名。 |
| `tags` | list | 显示在文章中，并作为博客首页的筛选条件。也可以写 `categories`。 |
| `description` | string | 博客首页上的摘要，也是订阅源中的概要。不写的话，使用 `<!-- more -->` 之前的文字。 |
| `image` | string | 封面图片，路径相对于 `docs/`。显示在文章顶部、卡片视图中的文章卡片上，也作为分享文章时的预览图。设置 `hide_cover: true` 可以不在文章本身显示封面。 |
| `draft` | boolean | 生成页面，但不放进博客首页和订阅源。 |
| `series` | list | 文章所属的系列。文章里会列出同一系列的其他文章，按时间从早到晚，或按 `series_order` 排序。 |
| `aliases` | list | 页面的旧地址，见[旧地址](#old-addresses)。任何页面都可以用。 |
{.fields}

## 页面包 {#page-bundles}

文章也可以是一个文件夹，里面放 `index.md` 和它用到的图片，也就是 Hugo 说的页面包（page bundle）。文章沿用文件夹的地址，旁边名为 `featured` 或 `cover` 的图片（`.jpg`、`.png`、`.webp` 或 `.svg`）就是封面：

```filetree
docs/
└── posts/
    └── 2026/
        └── introducing-sumi/
            ├── index.md        # → /posts/2026/introducing-sumi/
            ├── featured.jpg    # 封面
            └── screenshot.png  # 在 index.md 中写 ![](screenshot.png)
```

为 Hugo 写的前置元数据可以直接用：`summary` 当作 `description`，`cover: {image: …}` 当作 `image`。

## 多个博客 {#several-blogs}

`blog.dir` 可以是一个列表。每个文件夹是一个博客，有自己的首页和上一篇 / 下一篇；标签页、归档和订阅源包含所有博客的文章：

```yaml title="mkdocs.yml"
plugins:
  - sumi:
      blog:
        dir: [posts, essays]
```

## 标签页 {#tag-pages}

博客首页的标签筛选不需要配置。要让每个标签有自己的页面，方便搜索引擎收录，设置 `blog.tags_dir`：

```yaml title="mkdocs.yml"
plugins:
  - sumi:
      blog:
        tags_dir: tags
```

Sumi 会生成 `tags/`，列出所有标签和文章数，并为每个标签生成一个页面。标签地址和 Hugo 的生成方式相同：`Open Source` 对应 `tags/open-source/`。文章上的标签会链接到这些页面。想在标签列表上方加一段介绍，就创建 `tags/index.md` 并设置 `template: blog-tags.html`。

## 归档 {#archive}

设置了 `template: blog-archive.html` 的页面会按年份列出所有文章，最新的在前：

```markdown title="docs/archive.md"
---
template: blog-archive.html
---

# 归档
```

## 旧地址 {#old-addresses}

页面换了地址时，把旧地址写进 `aliases`，Sumi 会在每个旧地址生成一个跳转页，把读者和搜索引擎带到新地址：

```yaml
---
aliases:
  - /2019/05/hello-world/
---
```

以 `/` 开头的地址从整个站点的根目录算起，不以 `/` 开头的从页面所在语言的根目录算起。跳转页不会覆盖已有页面；在[多语言站点](../customize/i18n.md)上，默认语言的跳转页优先。

## 作者 {#authors}

```yaml title="docs/blog/.authors.yml"
authors:
  xianpeng:
    name: Xianpeng Shen
    description: Maintainer
    avatar: https://github.com/shenxianpeng.png
    url: https://github.com/shenxianpeng
```

格式和 Material 博客插件的相同，现有的文件可以直接沿用。

## 博客首页 {#the-index-page}

没有 `docs/blog/index.md` 时，Sumi 会创建一个标题为“博客”的首页。要加一段介绍，就创建这个文件，其中的 Markdown 会显示在文章列表上方。文章带标签时会出现标签筛选，筛选可以用 `blog/#tag=release` 这样的地址直接链接。

任何页面都可以列出一部分文章：设置 `template: blog.html`，再用 `blog_tag: release` 列出带这个标签的文章，或用 `blog_series: 入门` 列出一个系列的文章。

## 列表视图与卡片视图 {#list-and-card-views}

博客首页可以把文章显示为列表，或者显示为带封面图的卡片网格。读者可以用标签筛选旁边的按钮切换，选择会被记住。用 `blog.layout` 设置默认视图：

```yaml title="mkdocs.yml"
plugins:
  - sumi:
      blog:
        layout: cards    # 或 list（默认）
```

没有 `image` 的文章会得到一张用强调色和第一个标签画出的封面。

## 订阅源 {#feed}

Atom 订阅源写到 `blog/feed.xml`，并在每个页面的 `<head>` 中声明，所以订阅阅读器从任何地址都能找到它。它需要 `site_url` 才能生成绝对链接。

要沿用旧订阅源的地址和格式，比如 Hugo 在 `index.xml` 的 RSS，设置 `feed_path` 和 `feed_format`。RSS 中带有每篇文章的摘要和封面图：

```yaml title="mkdocs.yml"
plugins:
  - sumi:
      blog:
        feed_path: index.xml
        feed_format: rss
        feed_items: 0      # 全部文章
```

## 文章页脚 {#post-footer}

想在每篇文章下面加点内容，比如订阅表单或你的项目链接，就覆盖 `partials/post-footer.html`（见[覆盖模板](../customize/overrides.md)）。它默认是空的，可以用 `sumi.post` 拿到当前文章。

## 选项 {#options}

```yaml title="mkdocs.yml"
plugins:
  - sumi:
      blog:
        dir: blog        # docs/ 下存放文章的文件夹，也可以是文件夹列表
        feed: true
        feed_items: 20   # 0 表示全部文章
        feed_path: blog/feed.xml   # 默认是第一个博客文件夹下的 feed.xml
        feed_format: atom          # 或 rss
        tags_dir:        # 标签页所在的文件夹，比如 tags；默认不生成
        layout: list     # 或 cards
```
