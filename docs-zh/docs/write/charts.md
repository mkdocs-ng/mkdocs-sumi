---
description: 用 YAML 和 Apache ECharts 画数据图，用 Markdown 大纲画思维导图。
---

# 数据图与思维导图

还有两种代码块也能把文字画成图。和[图表](diagrams.md)一样，它们的脚本随 Sumi 附带，只在数据图或思维导图即将滚入视野时才加载。

## 数据图 {#charts}

`echarts` 代码块里写的是一份 [Apache ECharts](https://echarts.apache.org/zh/option.html) 配置项，可以用 YAML 或 JSON。Sumi 在构建站点时会检查它：不是有效 YAML 或 JSON 的代码块会原样保留为代码块，构建时输出一条警告。

````markdown
```echarts title="构建 1 000 个页面的耗时（秒）"
xAxis:
  type: category
  data: [MkDocs 1.6, MkDocs NG, NG + Sumi]
yAxis:
  type: value
series:
  - type: bar
    data: [18.1, 8.4, 12.0]
```
````

```echarts title="构建 1 000 个页面的耗时（秒）"
xAxis:
  type: category
  data: [MkDocs 1.6, MkDocs NG, NG + Sumi]
yAxis:
  type: value
series:
  - type: bar
    data: [18.1, 8.4, 12.0]
```

数据图优先使用站点的强调色，跟随配色切换，并在页面尺寸变化时重新绘制。在代码块上设置 `height` 可以修改高度，单位是像素（默认为 360）：

````markdown
```echarts height="240"
series:
  - type: pie
    radius: ["45%", "70%"]
    data:
      - {name: Markdown, value: 60}
      - {name: 模板, value: 15}
      - {name: 搜索索引, value: 16}
      - {name: 其他, value: 9}
```
````

```echarts height="240"
tooltip: {}
series:
  - type: pie
    radius: ["45%", "70%"]
    data:
      - {name: Markdown, value: 60}
      - {name: 模板, value: 15}
      - {name: 搜索索引, value: 16}
      - {name: 其他, value: 9}
```

没有 JavaScript 时，以及在页面的 Markdown 副本中，读者看到的是 YAML 源码。

> [!NOTE]
> 配置项是数据，不是代码：自定义 `formatter` 回调这样的函数没法用 YAML 或 JSON 写。请改用 `formatter: "{b}: {c}"` 这样的模板字符串。

## 思维导图 {#mind-maps}

`markmap` 代码块用标题和嵌套列表画出思维导图。点击节点可以折叠或展开分支；拖动可以平移，滚动可以缩放。

````markdown
```markmap height="360"
# Sumi
## 写作
- 提示框
- 标签页和步骤
- 图表和数据图
## 发布
- 首页
- 博客
- 发布记录
## 阅读
- ⌘K 搜索
- 深色模式
- 打印版
```
````

```markmap height="360"
# Sumi
## 写作
- 提示框
- 标签页和步骤
- 图表和数据图
## 发布
- 首页
- 博客
- 发布记录
## 阅读
- ⌘K 搜索
- 深色模式
- 打印版
```

大纲在构建站点时就转换成了树。没有 JavaScript 时、打印时以及在 Markdown 副本中，读者看到的是一个嵌套列表。

## 关闭这两个功能 {#turning-them-off}

如果已经有别的插件处理 `echarts` 或 `markmap` 代码块，可以关闭 Sumi 的处理：

```yaml title="mkdocs.yml"
plugins:
  - sumi:
      echarts: false
      markmap: false
```
