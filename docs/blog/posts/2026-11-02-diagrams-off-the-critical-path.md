---
date: 2026-11-02
authors: [xianpeng]
tags: [performance, design]
image: assets/screens/docs-dark.jpg
hide_cover: true
description: A page with one Mermaid diagram used to make readers wait ten seconds on a phone. Here is what we changed, and the numbers before and after.
---

# Keeping diagrams off the critical path

Sumi's promise is that heavy scripts load only where they are used. For Mermaid that was true, but not enough: a page with one diagram scored 45 in Lighthouse's mobile test, and its largest paint arrived after 10 seconds.

<!-- more -->

## What was slow

Mermaid shipped as one 5.5 MB script (1.5 MB compressed). On a page with a diagram, Sumi fetched it as soon as the page opened. Parsing that much JavaScript on a throttled phone CPU blocks everything else, and the diagram's own text was the largest element on screen, so the page "finished" only once Mermaid did.

## What changed

1. **Mermaid is split by diagram type.** Sumi now ships Mermaid's ES module build. A page with a flowchart fetches Mermaid's core and the flowchart code; the code for Gantt charts, mind maps and the other twenty diagram types stays on the server.
2. **Nothing loads until a diagram is near.** Each diagram is watched, and Mermaid is fetched when the first one comes within 400 pixels of the viewport. A diagram at the bottom of a long page costs nothing until the reader scrolls to it.
3. **One diagram at a time.** Diagrams render in sequence instead of all at once, so the main thread gets breaks in between.
{.steps}

Until a diagram is drawn, readers see its source text, which is also what readers without JavaScript see.

## Before and after

| Diagrams page, Lighthouse mobile | Before | After |
| --- | --- | --- |
| Performance score | 35 | 73 |
| Largest contentful paint | 31.0 s | 2.3 s |
| JavaScript downloaded | 5.4 MB | 2.4 MB |
{caption="Measured on a local build served without compression. On GitHub Pages, with compression, the page scored 45 before."}

Pages without diagrams were already at 94–100 and are unchanged.

## While we were there

Every drawn diagram now has three buttons: open it full screen, copy its Mermaid source, and download it as an SVG file. And two more text-to-picture fences arrived, built the same way: [charts](../../docs/write/charts.md) with Apache ECharts and [mind maps](../../docs/write/charts.md#mind-maps) with Markmap.

> [!NOTE]
> ES modules cannot be loaded from `file://` pages. Serve the built site, even locally with `python -m http.server`, to see diagrams.
