---
description: Charts from YAML with Apache ECharts, and mind maps from a Markdown outline.
---

# Charts and mind maps

Two more fences draw pictures from text. Like [diagrams](diagrams.md), their scripts ship with Sumi and load only when a chart or mind map is about to scroll into view.

## Charts

An `echarts` fence holds an [Apache ECharts](https://echarts.apache.org/en/option.html) option, written in YAML or JSON. Sumi checks it when the site is built: a fence that is not valid YAML or JSON is left as a code block and the build prints a warning.

````markdown
```echarts title="Build time for 1 000 pages (seconds)"
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

```echarts title="Build time for 1 000 pages (seconds)"
xAxis:
  type: category
  data: [MkDocs 1.6, MkDocs NG, NG + Sumi]
yAxis:
  type: value
series:
  - type: bar
    data: [18.1, 8.4, 12.0]
```

Charts use the site's accent colour first, follow the colour scheme, and redraw when the page is resized. Set `height` on the fence to change the height in pixels (the default is 360):

````markdown
```echarts height="240"
series:
  - type: pie
    radius: ["45%", "70%"]
    data:
      - {name: Markdown, value: 60}
      - {name: Templates, value: 15}
      - {name: Search index, value: 16}
      - {name: Other, value: 9}
```
````

```echarts height="240"
tooltip: {}
series:
  - type: pie
    radius: ["45%", "70%"]
    data:
      - {name: Markdown, value: 60}
      - {name: Templates, value: 15}
      - {name: Search index, value: 16}
      - {name: Other, value: 9}
```

Without JavaScript, and in the Markdown copy of the page, readers see the YAML source.

> [!NOTE]
> Options are data, not code: functions such as custom `formatter` callbacks cannot be written in YAML or JSON. Use template strings like `formatter: "{b}: {c}"` instead.

## Mind maps

A `markmap` fence draws a mind map from headings and nested lists. Click a node to fold or unfold its branch; drag to pan and scroll to zoom.

````markdown
```markmap height="360"
# Sumi
## Write
- Callouts
- Tabs and steps
- Diagrams and charts
## Publish
- Landing page
- Blog
- Releases
## Read
- ⌘K search
- Dark mode
- Print edition
```
````

```markmap height="360"
# Sumi
## Write
- Callouts
- Tabs and steps
- Diagrams and charts
## Publish
- Landing page
- Blog
- Releases
## Read
- ⌘K search
- Dark mode
- Print edition
```

The outline is turned into a tree when the site is built. Without JavaScript, in print and in the Markdown copy, readers see it as a nested list.

## Turning them off

If another plugin already handles `echarts` or `markmap` fences, switch Sumi's handling off:

```yaml title="mkdocs.yml"
plugins:
  - sumi:
      echarts: false
      markmap: false
```
