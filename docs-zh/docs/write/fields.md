---
description: 用于配置选项、参数和 API 字段的参考表。
---

# 字段

配置选项和 API 参数通常写成表格，可说明一长，表格就很难读。加上 `{.fields}`，Sumi 会把每一行变成一条参考条目：名称及其类型、默认值和“必填”标记排在同一行，说明放在下面。

```markdown
| 名称 | 类型 | 默认值 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `site_name` | string | | 是 | 站点标题，显示在页眉和每个页面的标题中。 |
| `site_url` | string | `null` | | 构建出的站点的正式地址。站点地图、订阅源和 `llms.txt` 都需要它。 |
| `strict` | boolean | `false` | | 遇到任何警告（例如失效链接）就停止构建。 |
{.fields}
```

| 名称 | 类型 | 默认值 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `site_name` | string | | 是 | 站点标题，显示在页眉和每个页面的标题中。 |
| `site_url` | string | `null` | | 构建出的站点的正式地址。站点地图、订阅源和 `llms.txt` 都需要它。 |
| `strict` | boolean | `false` | | 遇到任何警告（例如失效链接）就停止构建。 |
{.fields}

## 哪些列是元数据 {#which-columns-are-metadata}

第一列始终是名称。表头为 **类型**、**默认值** 和 **必填**（或英文的 **Type**、**Default**、**Required**）的列会变成名称旁边的小标签，其余各列都并入说明。

要自己指定哪些列是元数据，把它们的表头写进 `meta`：

```markdown
{.fields meta="类型 起始版本"}
```

| 字段 | 类型 | 起始版本 | 说明 |
| --- | --- | --- | --- |
| `id` | integer | 1.0 | 发布的唯一标识。 |
| `assets` | list | 1.2 | 发布附带的文件，含大小和 SHA-256 校验和。 |
{.fields meta="类型 起始版本"}

## 链接到某个字段 {#linking-to-a-field}

每个条目都保留名称单元格的内容，所以可以用 `attr_list` 加上锚点：

```markdown
| `strict`{#strict} | boolean | `false` | 遇到警告就停止。 |
```

页面的 Markdown 副本保留原始表格。

## 参考 {#reference}

| 项目 | 说明 |
| --- | --- |
| 输出 | `<div class="sumi-fields">`，每一行一个 `<div class="sumi-field">`，元数据列显示为小标签。 |
| 没有 Sumi 时 | 原始表格。 |
| JavaScript | 不需要。 |
| 限制 | 第一列总是名称。单元格里只能写行内 Markdown。 |
{.compact}
