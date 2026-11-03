---
description: 由 YAML 生成的下载与发布说明页面，带校验和。
---

# 发布与下载

设置了 `template: releases.html` 的页面会列出各个版本的说明和可下载的文件。每个文件都显示大小和 SHA-256 校验和，点击即可复制校验和。可以看看[本站的发布记录](../../releases.md)。

```markdown title="docs/releases.md"
---
template: releases.html
releases: releases.yml
---

# 发布记录

下载最新版本，或者浏览历史版本。
```

`releases` 可以是 front matter 中的一个列表，也可以是一个 YAML 文件的路径（相对于 `docs/`）。

```yaml title="docs/releases.yml"
- version: 0.2.0
  date: 2026-12-01
  summary: 多版本文档和日文界面。
  notes: |
    - **新增：** `version_provider: mike`。
    - **修复：** 切换标签页时不再跳动。
  assets:
    - name: mkdocs_sumi-0.2.0-py3-none-any.whl
      url: https://example.com/mkdocs_sumi-0.2.0-py3-none-any.whl
      size: 1.9 MB
      sha256: 9f2c0a…
- version: 0.1.0
  date: 2026-11-01
  notes: 首个版本。
```

## 字段 {#fields}

| 键 | 类型 | 说明 |
| --- | --- | --- |
| `version` | string | 版本号，同时也是锚点，所以 `releases/#v0-2-0` 会链接到它。 |
| `title` | string | 设置后代替版本号显示。 |
| `date` | date | 发布日期。 |
| `status` | string | `latest`、`stable`、`prerelease` 或 `archived`。第一个版本默认为 `latest`。 |
| `summary` | string | 标题下方的一行概要。 |
| `notes` | string | 发布说明，使用 Markdown。 |
| `assets` | list | 下载文件：`name`、`url`、`size`、`sha256`。 |
{.fields}

页面自身的 Markdown 显示在列表上方，可以在这里写安装说明或支持策略。
