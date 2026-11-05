---
description: 把 Sumi 站点发布到 GitHub Pages、Cloudflare Pages、Netlify 或任何静态托管服务。
---

# 部署 {#deploy}

Sumi 站点就是一个静态文件夹。`mkdocs build` 把它写到 `site/`，任何 Web 服务器或静态托管服务都能直接提供：没有服务端代码，没有数据库，也没有 Node.js 构建步骤。

```sh
mkdocs build --strict
```

`--strict` 会在出现任何警告（比如失效的链接或写错的图表）时停止构建，让问题在读者看到之前暴露出来。在 CI 中请使用它。

## 固定版本 {#pin-your-versions}

托管服务上的构建应该和你本机使用相同的版本。把版本写在 `mkdocs.yml` 旁边的文件里：

```text title="requirements.txt"
mkdocs-sumi==0.2.1
mkdocs-ng==1.11.0
```

[升级](upgrade.md)时记得更新这里的版本号。

## GitHub Pages {#github-pages}

推荐用 GitHub Actions 工作流构建站点，再用 GitHub 官方的 Pages actions 发布。先在仓库的 **Settings → Pages** 中把 **Source** 设为 **GitHub Actions**，然后添加：

```yaml title=".github/workflows/docs.yml"
name: docs
on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
        with:
          fetch-depth: 0          # 完整历史，用于“最后更新”日期
      - uses: actions/setup-python@v7
        with:
          python-version: "3.13"
          cache: pip
      - run: pip install -r requirements.txt
      - run: mkdocs build --strict
      - if: github.event_name == 'push'
        uses: actions/upload-pages-artifact@v5
        with:
          path: site

  deploy:
    if: github.event_name == 'push'
    needs: build
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v5
```

Pull request 只构建和检查，不发布。推送到 `main` 后一两分钟就会上线。

如果你更喜欢 `gh-pages` 分支，`mkdocs gh-deploy` 依然可用：它会构建站点并强制推送到这个分支。这种情况下把 **Source** 设为 **Deploy from a branch**。

## Cloudflare Pages {#cloudflare-pages}

在 Cloudflare 控制台（**Workers & Pages → Create → Pages**）中连接仓库，并使用：

| 设置 | 值 |
| --- | --- |
| Build command | `pip install -r requirements.txt && mkdocs build --strict` |
| Build output directory | `site` |
| 环境变量 | `PYTHON_VERSION` = `3.13` |
{.compact}

每个分支和 pull request 都有自己的预览地址。见[域名与预览](domains.md)。

## Netlify {#netlify}

```toml title="netlify.toml"
[build]
  command = "pip install -r requirements.txt && mkdocs build --strict"
  publish = "site"

[build.environment]
  PYTHON_VERSION = "3.13"
```

Netlify 会为每个 pull request 构建一个预览。

## 其他托管方式 {#any-other-host}

把 `site/` 里的内容上传到网站根目录即可：S3 存储桶、Nginx 或 Caddy 服务器、内网共享目录都可以。有两点需要检查：

- **地址。** 把 `site_url` 设为站点实际的地址，包括子路径，比如 `https://example.com/docs/`。站点地图、订阅源、`llms.txt`、社交分享预览和 canonical 链接都根据它生成。
- **目录式 URL。** 页面写成 `guide/index.html`，链接写成 `guide/`。大多数服务器默认会为文件夹返回 `index.html`。如果你的服务器不会，请打开这个功能，或者在 `mkdocs.yml` 中设置 `use_directory_urls: false`。

## 发布了哪些内容 {#what-gets-published}

| 输出 | 路径 | 说明 |
| --- | --- | --- |
| 页面 | `…/index.html` | 静态 HTML，没有 JavaScript 也能阅读 |
| 主题资源 | `assets/` | 字体、CSS、一个脚本，以及只在用到时才加载的 Mermaid、KaTeX、ECharts 和 Markmap |
| 搜索索引 | `search/search_index.json` | 读者第一次打开 ⌘K 时才下载 |
| Markdown 副本、`llms.txt` | 与 `guide/` 并列的 `guide.md`、`llms.txt`、`llms-full.txt` | 需要 `llms_txt` 插件 |
| 订阅源 | `blog/feed.xml` | 站点有博客时生成 |
| 打印版 | `print/` | 见[打印版](../pages/print.md) |
| 站点地图 | `sitemap.xml` | 完整的地址需要 `site_url` |
{.compact}

所有内容都从你自己的域名提供：Sumi 不从 CDN 加载任何字体、脚本或样式。站点可以拷到 U 盘或隔离网络中继续使用，只有[评论](comments.md)和你打开的[访问统计](analytics.md)除外。
