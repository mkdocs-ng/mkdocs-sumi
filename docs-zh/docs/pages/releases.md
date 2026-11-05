---
description: 由 YAML、GitHub Releases 或 PyPI 生成的下载与发布说明页面，带校验和。
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

`releases` 可以是 front matter 中的一个列表、一个 YAML 文件的路径（相对于 `docs/`），也可以是[要读取的来源](#remote)，比如 GitHub Releases。

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

## 来自 GitHub Releases 和 PyPI {#remote}

不必手写每个版本，可以让页面在构建站点时自己读取：

```yaml title="docs/releases.md"
---
template: releases.html
releases:
  github: owner/repo     # 版本、日期和说明来自 GitHub Releases
  pypi: package-name     # 下载文件，带大小和 SHA-256 校验和
  file: releases.yml     # 可选：手写的字段优先
---
```

| 键 | 说明 |
| --- | --- |
| `github` | 仓库所有已发布的版本，从新到旧。草稿不会列出，标为预发布的版本状态为 `prerelease`。发布说明的第一段成为 `summary`，其余部分成为 `notes`；标题降两级，`#123` 和 `@user` 变成链接。附加在 release 上的文件成为 `assets`。 |
| `pypi` | 每个版本在 PyPI 上的文件，用于自身没有 `assets` 的版本。 |
| `file` | 按 `version` 匹配的条目会覆盖对应字段，可以为某个版本写更好的概要或说明。只在文件里出现的版本按 `date` 排入列表。 |
{.fields}

在 CI 中构建时设置 `GITHUB_TOKEN`（或 `GH_TOKEN`），以免触发 GitHub 未认证时每小时 60 次请求的限制。每个来源在一次构建进程中只读取一次，所以 `mkdocs serve` 不会在每次修改时重新读取。某个来源无法访问时，构建会给出警告，并显示已有的内容。

想在发布新版本时刷新页面，就在发布流程里重新构建站点。本站的 [`release.yml`](https://github.com/mkdocs-ng/mkdocs-sumi/blob/main/.github/workflows/release.yml) 会在包上传到 PyPI 后启动文档构建。
