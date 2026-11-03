---
date: 2026-11-02
authors: [xianpeng]
tags: [performance, design]
image: assets/screens/docs-dark.jpg
hide_cover: true
description: 一个只有一张 Mermaid 图表的页面，曾经让手机上的读者等上十秒。下面是我们做了哪些改动，以及改动前后的数据。
---

# 让图表不再拖慢页面

Sumi 承诺，重量级脚本只在用到的地方加载。对 Mermaid 来说这一点虽然做到了，但还不够：一个只有一张图表的页面在 Lighthouse 移动端测试中只得了 45 分，最大内容绘制要等 10 秒以后才出现。

<!-- more -->

## 慢在哪里 {#what-was-slow}

Mermaid 过去是一个 5.5 MB 的脚本（压缩后 1.5 MB）。在有图表的页面上，Sumi 一打开页面就去下载它。在被限速的手机 CPU 上解析这么多 JavaScript，会阻塞其他一切；而图表本身的文字又是屏幕上最大的元素，所以要等 Mermaid 跑完，页面才算“加载完成”。

## 改了什么 {#what-changed}

1. **Mermaid 按图表类型拆分。** Sumi 现在附带的是 Mermaid 的 ES 模块版本。有流程图的页面只下载 Mermaid 的核心和流程图代码；甘特图、思维导图以及其他二十种图表类型的代码都留在服务器上。
2. **图表接近视野之前什么都不加载。** 每张图表都会被监视，第一张图表进入视口 400 像素范围内时才下载 Mermaid。长页面底部的图表，在读者滚动到它之前不产生任何开销。
3. **一次只画一张图表。** 图表依次渲染，而不是同时渲染，这样主线程在两次渲染之间可以喘口气。
{.steps}

图表画出来之前，读者看到的是它的源码文本，这也是没有 JavaScript 的读者看到的内容。

## 改动前后 {#before-and-after}

| 图表页面，Lighthouse 移动端 | 改动前 | 改动后 |
| --- | --- | --- |
| 性能得分 | 35 | 73 |
| 最大内容绘制 | 31.0 s | 2.3 s |
| 下载的 JavaScript | 5.4 MB | 2.4 MB |
{caption="在本地构建上测量，服务时未启用压缩。在启用压缩的 GitHub Pages 上，改动前的得分是 45。"}

没有图表的页面本来就在 94–100 分之间，没有变化。

## 顺便做的事 {#while-we-were-there}

现在每张画好的图表都有三个按钮：全屏查看、复制 Mermaid 源码、下载为 SVG 文件。另外还新增了两种把文字画成图的代码块，做法相同：用 Apache ECharts 画的[数据图](../../docs/write/charts.md)和用 Markmap 画的[思维导图](../../docs/write/charts.md#mind-maps)。

> [!NOTE]
> `file://` 页面无法加载 ES 模块。要看到图表，请通过服务器打开构建好的站点，在本地也可以用 `python -m http.server`。
