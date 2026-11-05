---
description: Sumi 最常见问题的解决办法。
---

# 常见问题 {#troubleshooting}

先运行 `mkdocs build --strict`。它会打印所有警告并在第一个警告处停止，警告里通常会写出出问题的文件。加上 `--verbose` 能看到更多细节。

## 搜索什么也找不到 {#search-finds-nothing}

⌘K 面板能打开，但没有列出任何页面。

- **`plugins` 中缺少 `search`。** 一旦 `mkdocs.yml` 里写了 `plugins:`，MkDocs 就不再自动加入 `search`。请把它列在 `sumi` 前面，参见[安装](../start/install.md#enable-the-theme-and-the-plugin)。
- **站点是从文件系统打开的。** 浏览器不允许 `file://` 页面下载搜索索引。请用 HTTP 提供这个文件夹：`python -m http.server -d site`。

## 页面没有样式，或者字体缺失 {#the-page-looks-unstyled-or-fonts-are-missing}

- **从文件系统打开。** 同上，浏览器会在 `file://` 页面上拦截字体。请用 HTTP 提供这个文件夹。
- **部署在子路径下。** 如果站点在 `https://example.com/docs/`，请把 `site_url` 设为这个地址。页面之间的链接是相对的，不受影响；这个地址影响的是 canonical 链接、站点地图和社交分享预览。
- **严格的内容安全策略（CSP）。** Sumi 用了几段很小的内联脚本，用于配色方案和页面数据。脚本策略中没有 `'unsafe-inline'` 时，它们会被拦截。请在服务器的策略中用 hash 或 nonce 放行它们。

## 组件显示为普通 Markdown {#components-show-as-plain-markdown}

提示框显示成引用块，能看到 `{.cards}` 这一行，或者 `mermaid` 代码块没有变成图。

- **属性行没有紧贴在块的下面。** `{.cards}` 必须是列表之后紧接着的一行，中间不能有空行。见[属性行](../write/index.md#attribute-lines)。
- **另一个插件也在处理这类代码块。** 如果同时启用了 Mermaid 或 ECharts 插件，请关掉其中一个，比如在 [Sumi 插件](../customize/plugin.md)上设置 `mermaid: false`。

## “The Sumi theme needs its plugin” {#the-sumi-theme-needs-its-plugin}

设置了 `theme: name: sumi`，但 `plugins:` 下没有 `sumi` 时，构建会带着这条消息停止。主题负责绘制页面，插件负责把 Markdown 变成组件，两者缺一不可：

```yaml title="mkdocs.yml"
theme:
  name: sumi
plugins:
  - search
  - sumi
```

## “The 'sumi' plugin is meant to be used with 'theme: sumi'” {#the-sumi-plugin-is-meant-to-be-used-with-theme-sumi}

和上面相反：启用了插件，但主题是别的。请设置 `theme: name: sumi`，或者从 `plugins` 中删掉 `sumi`。

## “An echarts fence is neither valid JSON nor YAML” {#an-echarts-fence-is-neither-valid-json-nor-yaml}

某个图表的配置读不出来，消息中会给出第一个解析错误。常见原因是用 Tab 缩进、含有 `:` 的字符串没有加引号，或者写了 JavaScript 函数（配置里不能有函数）。见[数据图](../write/charts.md)。

## 每一页都显示今天“最后更新” {#every-page-says-last-updated-today}

设置 `git_dates: true` 后，日期来自 Git。CI 服务通常只克隆最后一次提交，于是每一页看起来都是新的。请先获取完整历史，比如在 `actions/checkout` 上设置 `fetch-depth: 0`。如果完全没有 Git 历史，构建会记录 `git_dates is enabled but git history is unavailable`，并且不显示日期。

## `locale` 被拒绝 {#locale-is-rejected}

MkDocs 的 `theme.locale` 只接受字母和下划线：请写 `pt_BR` 或 `zh_TW`，不要写 `pt-BR`。页面的 `lang` 属性仍然会写成 `pt-BR`。见[语言](../customize/i18n.md)。

## 没有双语对照按钮 {#the-bilingual-view-button-is-missing}

它只出现在多语言站点上，而且只出现在有译文的页面上：因为缺少译文而显示默认语言的页面不会提供它。请检查译文文件是否存在，以及 `bilingual_view` 是否被设成了 `false`。

## 评论没有出现 {#comments-do-not-appear}

- 对照 [giscus.app](https://giscus.app/) 检查 `repo`、`repo_id`、`category` 和 `category_id`。
- 仓库必须是公开的，打开了 Discussions，并且安装了 Giscus 应用。
- 评论在读者滚动到附近时才加载。隐私类浏览器扩展可能会拦截 giscus.app。

## 升级之后页面坏了 {#a-page-breaks-after-an-upgrade}

通常是新版本发布之前写的[模板覆盖](../customize/overrides.md)。先把覆盖移开，重新构建，再对比。见[升级](upgrade.md#template-overrides)。

## 还是没解决 {#still-stuck}

请[提一个 issue](https://github.com/mkdocs-ng/mkdocs-sumi/issues)，附上 `mkdocs build --strict --verbose` 的输出、你的 `mkdocs.yml`，以及 `pip show mkdocs-sumi mkdocs-ng` 显示的版本。
