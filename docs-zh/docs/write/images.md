---
description: 图片、带图注的插图、放大查看，以及分别用于浅色和深色模式的图片。
---

# 图片与插图

图片使用标准 Markdown 语法。路径相对于当前页面，所以图片在编辑器、GitHub 和站点上都能显示。

```markdown
![Sumi 标志](../../assets/sumi-mark.svg)
```

## 插图 {#figures}

在图片下一行加 `{caption="…"}`，它就会变成带图注的插图：

```markdown
![Sumi 标志](../../assets/sumi-mark.svg)
{caption="Sumi 标志：一笔墨迹，一方朱印。"}
```

![Sumi 标志](../../assets/sumi-mark.svg)
{caption="Sumi 标志：一笔墨迹，一方朱印。"}

## 放大查看 {#zoom}

点击正文中的图片可以全屏查看；按 <kbd>Esc</kbd> 或再点一次即可关闭。链接和卡片中的图片不能放大。要让某张图片不可放大，给它加上 `no-zoom` 类：

```markdown
![流程图](flow.png){.no-zoom}
```

## 浅色与深色版本 {#light-and-dark-variants}

在图片地址后面加 `#only-light` 或 `#only-dark`，图片就只在对应的配色下显示：

```markdown
![架构](arch-light.png#only-light)
![架构](arch-dark.png#only-dark)
```

## 尺寸与位置 {#size-and-placement}

借助 `attr_list`，可以设置图片宽度或让图片浮动：

```markdown
![标志](logo.png){width="120"}
![截图](shot.png){.left width="320"}
```

> [!NOTE]
> 图片会延迟加载。请给大图写上明确的 `width` 和 `height` 属性，以免页面布局跳动。

## 参考 {#reference}

| 项目 | 说明 |
| --- | --- |
| 输出 | `<img loading="lazy">`；设置 `caption` 时是带 `<figcaption>` 的 `<figure class="sumi-figure">`。 |
| 没有 Sumi 时 | 普通图片。`#only-light` 和 `#only-dark` 两张图都会显示。 |
| JavaScript | 只有放大查看时需要。 |
| 限制 | 放大时显示的是图片本身的尺寸，不会加载更大的文件。 |
{.compact}
