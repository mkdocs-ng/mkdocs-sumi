---
description: 用 GitHub 风格的引用块书写注释、提示和警告。
---

# 提示框

提示框用来突出不容错过的信息。Sumi 采用 GitHub 为 alert 引入的语法，所以提示框在 GitHub、编辑器预览和 Sumi 中都能正常显示。

```markdown
> [!NOTE]
> Sumi 读取的语法和 GitHub 一样。
```

> [!NOTE]
> Sumi 读取的语法和 GitHub 一样。

## 五种类型 {#the-five-types}

> [!NOTE]
> 用户应当知道的有用信息，即使只是快速浏览也不该错过。

> [!TIP]
> 帮助用户把事情做得更好、更轻松的建议。

> [!IMPORTANT]
> 用户达成目标所必需的关键信息。

> [!WARNING]
> 需要立即注意、以免出问题的紧急信息。

> [!CAUTION]
> 提醒某些操作可能带来的风险或不良后果。

```markdown
> [!NOTE]
> [!TIP]
> [!IMPORTANT]
> [!WARNING]
> [!CAUTION]
```

Sumi 也接受 Material for MkDocs 使用的类型名：`info`、`success`、`question`、`failure`、`danger`、`bug`、`example`、`quote`、`abstract` 和 `todo`，每个都映射到最接近的颜色。

## 自定义标题 {#custom-titles}

标记后面的文字会替换默认标题：

```markdown
> [!WARNING] 先备份
> `mkdocs gh-deploy --force` 会替换整个 `gh-pages` 分支。
```

> [!WARNING] 先备份
> `mkdocs gh-deploy --force` 会替换整个 `gh-pages` 分支。

## 可折叠的提示框 {#collapsible-callouts}

在标记后加 `-`，提示框默认折叠；加 `+`，默认展开但可以折叠。

```markdown
> [!TIP]- 为什么叫 Sumi？
> *Sumi*（墨）是东亚书法用的墨：一种颜色，万千浓淡。
```

> [!TIP]- 为什么叫 Sumi？
> *Sumi*（墨）是东亚书法用的墨：一种颜色，万千浓淡。

折叠的提示框在打印时会展开。

## 丰富的内容 {#rich-content}

引用块里能放的内容，提示框里都能放：列表、代码、表格，甚至别的提示框。

> [!IMPORTANT] 升级之前
> 1. 阅读[发布记录](../../releases.md)。
> 2. 在 `requirements.txt` 中固定版本：
>
>     ```text
>     mkdocs-sumi==0.1.0
>     ```

## Admonition {#admonitions}

如果你的页面已经在用 `admonition` 扩展，它们照常工作，外观也一样：

```markdown
!!! warning "已弃用"
    请改用 `theme.palette`。
```

!!! warning "已弃用"
    请改用 `theme.palette`。

`pymdownx.details` 的 `??? note` 和 `???+ note` 会显示为可折叠的提示框。
