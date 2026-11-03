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
{.fields}

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

## 选项 {#options}

```yaml title="mkdocs.yml"
plugins:
  - sumi:
      blog:
        dir: blog        # docs/ 下存放文章的文件夹
        feed: true
        feed_items: 20
        layout: list     # 或 cards
```
