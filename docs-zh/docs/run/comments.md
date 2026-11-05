---
description: 基于 GitHub Discussions 的 Giscus 评论，读者滚动到附近时才加载。
---

# 评论 {#comments}

Sumi 可以在文档页和博客文章下方显示 [Giscus](https://giscus.app/) 评论。Giscus 把每个页面的评论存放在你仓库的一个 GitHub Discussion 里，不需要运行数据库，也没有广告。

## 配置 {#set-up}

1. 在仓库设置中打开 Discussions，并为仓库安装 [Giscus 应用](https://github.com/apps/giscus)。
2. 打开 [giscus.app](https://giscus.app/)，填入仓库并选择一个讨论分类（推荐 *Announcements*：只有维护者和 Giscus 能在其中新建讨论）。页面会给出 `data-repo-id` 和 `data-category-id` 的值。
3. 把它们复制到 `mkdocs.yml`：

```yaml title="mkdocs.yml"
theme:
  name: sumi
  comments:
    provider: giscus
    repo: acme/docs
    repo_id: R_kgDOxxxxxx
    category: Announcements
    category_id: DIC_kwDOxxxxxx
```

## 选项 {#options}

| 选项 | 默认值 | 说明 |
| --- | --- | --- |
| `repo` | | 存放讨论的仓库，格式为 `owner/name`。必填。 |
| `repo_id`、`category`、`category_id` | | 从 giscus.app 获取。 |
| `mapping` | `pathname` | 页面如何找到对应的讨论：`pathname`、`url`、`title`、`og:title` 或 `specific`。 |
| `strict` | `false` | 按讨论标题精确匹配，而不是搜索匹配。 |
| `reactions` | `true` | 在主帖上显示表情回应。 |
| `input_position` | `bottom` | 设为 `top` 时，评论框放在评论列表上方。 |
| `lang` | 站点语言 | Giscus 界面的语言。 |
| `theme_light`、`theme_dark` | `light`、`dark` | 浅色和深色模式下使用的 Giscus 主题。 |
| `opt_in` | `false` | 只在 front matter 写了 `comments: true` 的页面上显示评论。 |
{.fields}

## 单个页面 {#per-page}

```yaml title="docs/changelog.md"
---
comments: false
---
```

`comments: false` 关闭某一页的评论。设置了 `opt_in: true` 时，用 `comments: true` 为某一页打开评论。

## 读者看到什么 {#what-readers-get}

| 输出 | 说明 |
| --- | --- |
| 结构 | 正文之后、上一页/下一页链接之前，一个“评论”标题和一个空白区域 |
| 加载 | 读者滚动到距离评论区 400 像素以内时才请求 Giscus 的脚本，没人读到底的页面永远不会加载它 |
| 主题 | 跟随浅色/深色切换，无需刷新 |
| 没有 JavaScript 时 | 一个指向仓库 Discussions 的链接 |
{.compact}

## 限制 {#limits}

- 读者需要 GitHub 账号才能发表评论，所有人都可以阅读评论。
- 评论从 giscus.app 加载。除了你自己打开的统计服务，这是 Sumi 唯一会连接第三方服务的功能。站点需要离线可用时，请不要设置 `comments`。
- 首页（落地页）和博客索引页没有评论。
- 之后再修改 `mapping`，页面可能会和已有的讨论对应不上。
