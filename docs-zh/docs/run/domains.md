---
description: 用自己的域名提供站点，上线前预览改动，并发布多个版本。
---

# 域名与预览 {#domains-and-previews}

## 自己的域名 {#your-own-domain}

1. 在域名服务商处添加 DNS 记录。对于 `docs.example.com` 这样的子域名，添加一条指向托管服务的 `CNAME` 记录：GitHub Pages 是 `<user>.github.io`，Cloudflare Pages 是 `*.pages.dev` 地址，Netlify 是 `*.netlify.app` 地址。对于 `example.com` 这样的根域名，请按托管服务的说明操作：[GitHub](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)、[Cloudflare](https://developers.cloudflare.com/pages/configuration/custom-domains/)、[Netlify](https://docs.netlify.com/domains-https/custom-domains/)。
2. 在托管服务的设置中填入域名。GitHub 上是 **Settings → Pages → Custom domain**；证书就绪后打开 **Enforce HTTPS**。
3. 把 `site_url` 设为新地址：

```yaml title="mkdocs.yml"
site_url: https://docs.example.com/
```

站点地图、订阅源、`llms.txt`、社交分享预览和 canonical 链接都指向 `site_url`。不设置的话，它们会缺失或不完整。

> [!NOTE]
> 使用 `mkdocs gh-deploy` 时，GitHub 从发布分支里的 `CNAME` 文件读取域名。在 `docs/` 中放一个名为 `CNAME`、内容是域名的文件，每次构建都会把它一起复制过去。用 GitHub Actions 部署时不需要这个文件。

### 迁移到新域名 {#moving-to-a-new-domain}

读者和搜索引擎手里还是旧链接。大多数托管服务可以重定向整个域名：保留旧域名，添加一条带路径重定向到新域名的规则。站内移动过的页面，可以用 [mkdocs-redirects](https://github.com/mkdocs/mkdocs-redirects) 插件生成跳转到新地址的小页面。

## 发布前预览 {#preview-before-publishing}

| 在哪里 | 怎么做 |
| --- | --- |
| 本机 | `mkdocs serve` 在每次保存后重新构建并刷新浏览器。如果页面和完整构建的结果不一样，用 `mkdocs serve --clean` 关闭预览服务器的缓存。 |
| 构建好的副本 | 先 `mkdocs build`，再 `python -m http.server -d site`，查看真实的输出。直接从文件系统打开 `site/index.html` 不行：浏览器会在 `file://` 页面上拦截搜索和字体。 |
| Cloudflare 或 Netlify 上的 pull request | 每个分支和 pull request 都有自己的预览地址，并会贴在 pull request 上。 |
| GitHub Pages 上的 pull request | GitHub Pages 一个站点只提供一个版本。[工作流](deploy.md#github-pages)仍会用 `--strict` 构建 pull request，能发现失效的链接。要浏览预览，请检出分支在本地构建，或者让 Cloudflare 或 Netlify 部署预览。 |
{.fields}

搜索引擎不应该收录预览。预览地址通常会带上 `X-Robots-Tag: noindex` 响应头；如果预览出现在搜索结果里，请检查你的托管服务。

## 多个版本 {#several-versions}

要让旧版本的文档继续在线，用 [mike](https://github.com/jimporter/mike) 把每个版本发布到各自的文件夹。Sumi 会在页头显示版本菜单，并在旧版本上显示提示。见[导航](../customize/navigation.md#versions)。

## 多种语言 {#several-languages}

多语言站点只需一次构建：每种语言写到各自的文件夹，比如 `/zh/`。见[语言](../customize/i18n.md)。部署方式不用改。
