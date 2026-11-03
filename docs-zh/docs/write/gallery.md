---
description: 用一个普通的图片列表生成带图注的响应式图片网格。
---

# 图集

由图片组成的无序列表，后面跟一行 `{.gallery}`，就会变成图片网格。图片后面的文字是图注。点击图片可以查看原图。

```markdown
- ![首页，浅色](../../assets/screens/home-light.jpg)
  首页
- ![首页，深色](../../assets/screens/home-dark.jpg)
  深色模式
- ![文档页](../../assets/screens/docs-light.jpg)
  文档
- ![深色模式下的文档页](../../assets/screens/docs-dark.jpg)
  文档，深色
- ![博客](../../assets/screens/blog-light.jpg)
  博客
- ![发布页](../../assets/screens/releases-light.jpg)
  发布与下载
{.gallery}
```

- ![首页，浅色](../../assets/screens/home-light.jpg)
  首页
- ![首页，深色](../../assets/screens/home-dark.jpg)
  深色模式
- ![文档页](../../assets/screens/docs-light.jpg)
  文档
- ![深色模式下的文档页](../../assets/screens/docs-dark.jpg)
  文档，深色
- ![博客](../../assets/screens/blog-light.jpg)
  博客
- ![发布页](../../assets/screens/releases-light.jpg)
  发布与下载
{.gallery}

在 GitHub 上和页面的 Markdown 副本中，它仍然是一个带图注的图片列表。

## 列数与比例 {#columns-and-shape}

网格会排成放得下的尽可能多的列，最多三列，用 `cols` 可以修改。图片默认裁成 4:3；要用别的比例，在 `style` 中设置 `--ratio`：

```markdown
- ![](a.png)
- ![](b.png)
{.gallery cols="2" style="--ratio: 16 / 10"}
```

- ![首页，浅色](../../assets/screens/home-light.jpg)
  浅色
- ![首页，深色](../../assets/screens/home-dark.jpg)
  深色
{.gallery cols="2" style="--ratio: 16 / 10"}

## 链接 {#links}

把图片包在链接里，点击时就会打开对应页面，而不是显示原图：

```markdown
- [![博客](blog.png)](../pages/blog.md)
  博客布局
{.gallery}
```
