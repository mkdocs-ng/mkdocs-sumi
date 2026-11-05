---
description: 放在功能名称、版本号或表格单元格旁边的小状态标签。
---

# 徽章

在粗体或斜体文字后面紧跟 `{.badge}`，它就会变成徽章。这是标准的 `attr_list` 语法，所以不认识 Sumi 的渲染器仍然会把这个词显示为粗体。

```markdown
## 命令面板 **新**{.badge .new}

| 选项 | 状态 |
| --- | --- |
| `palette` | **稳定**{.badge .tip} |
| `brand` | **测试版**{.badge .warning} |
| `legacy_nav` | **已弃用**{.badge .deprecated} |
```

| 选项 | 状态 |
| --- | --- |
| `palette` | **稳定**{.badge .tip} |
| `brand` | **测试版**{.badge .warning} |
| `legacy_nav` | **已弃用**{.badge .deprecated} |

## 色调 {#tones}

第二个类名决定颜色。不加的话，徽章是中性的灰色。

| 类名 | 徽章 |
| --- | --- |
| *（无）* | **默认**{.badge} |
| `.note`、`.info` | **注意**{.badge .note} |
| `.tip`、`.success` | **稳定**{.badge .tip} |
| `.important`、`.new` | **新**{.badge .new} |
| `.warning` | **测试版**{.badge .warning} |
| `.caution`、`.danger`、`.deprecated` | **已移除**{.badge .caution} |
| `.accent` | **Sumi**{.badge .accent} |
{.compact}

## 在标题中 {#in-headings}

标题里的徽章会缩小以适应标题，也不会出现在目录的文字里。

## 版本 0.2 **最新**{.badge .tip}

```markdown
## 版本 0.2 **最新**{.badge .tip}
```

## 参考 {#reference}

| 项目 | 说明 |
| --- | --- |
| 输出 | `<strong>`、`<em>`、`<span>` 或 `<code>` 元素，带 `badge` 类，色调是第二个类名。 |
| 没有 Sumi 时 | 粗体或斜体文字：GitHub 和编辑器会忽略 `{…}`。 |
| JavaScript | 不需要。 |
| 限制 | 每个徽章只有一种色调。徽章本身不是链接，需要时可以放在链接里。 |
{.compact}
