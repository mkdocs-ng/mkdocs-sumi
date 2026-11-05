---
description: 如何让 MkDocs 插件，以及为 Material for MkDocs 写的 CSS 和模板，在 Sumi 中好好工作。
---

# 面向插件作者

Material for MkDocs 已进入维护模式，关键修复持续到 2027-05-05。许多插件只针对它编写和测试过。本页写给这些插件的作者：哪些在 Sumi 中已经能用，哪些需要小改动，以及怎样让你的插件被列入推荐名单。

Sumi 是标准的 MkDocs 主题。只使用 MkDocs 事件、往页面里写普通 HTML 的插件，不用改就能用。

## 我的插件需要改吗？ {#does-my-plugin-need-changes}

| 你的插件…… | 在 Sumi 中 |
| --- | --- |
| 使用 MkDocs 事件，把 HTML 写进 `page.content` | 能用。 |
| 自带读取 `--md-*` 变量的 CSS | 能用：Sumi 会把常用的变量映射到自己的颜色，两种配色下都有效。 |
| 用 `[data-md-color-scheme="slate"]` 切换深色 CSS | 能用：Sumi 在自己的 `data-theme` 旁边也会设置这个属性。 |
| 输出 `!!! note` 提示、`<details>`、表格或高亮代码 | 能用：Sumi 会给它们配上和自身提示框、代码块一致的样式。 |
| CSS 限定在 `.md-typeset` 下 | 需要改：加上 `.sumi-prose`，它是 Sumi 内容容器的类名。 |
| 在 `document$`（Material 的即时加载）上运行 JavaScript | 需要改：Sumi 每个页面都正常加载，请在 `DOMContentLoaded` 时运行。 |
| 检查 `config.theme.name == "material"` | 需要改：也接受 `"sumi"`，或者直接检测你需要的功能。 |
| 从 `material` 包导入，或覆盖 Material 的局部模板 | 需要改：见[模板](#templates)。 |

## 检测主题 {#detect-the-theme}

```python title="plugin.py"
def on_config(self, config):
    self.is_sumi = config.theme.name == "sumi"
```

优先用这种方式，而不是检查装了哪些包：一个站点可能装了 Material，却仍然用 Sumi 构建。

## 样式 {#styles}

渲染后的 Markdown 位于 `<div class="sumi-content sumi-prose">` 中。像以前把 CSS 限定在 `.md-typeset` 下那样，把它限定在这里：

```css title="my-plugin.css"
:is(.md-typeset, .sumi-prose) .my-widget { margin: 1em 0; }
```

想要完全一致时，使用 Sumi 的变量，并保留 Material 的变量作为后备，这样一份样式表就能同时服务两个主题：

```css
.my-widget {
  border: 1px solid var(--sumi-line, var(--md-default-fg-color--lightest));
  background: var(--sumi-bg-elev, var(--md-default-bg-color));
  color: var(--sumi-fg-2, var(--md-default-fg-color--light));
}
```

| 变量 | 用途 |
| --- | --- |
| `--sumi-fg`、`--sumi-fg-2`、`--sumi-fg-3` | 文字：正文、次要、弱化 |
| `--sumi-bg`、`--sumi-bg-elev`、`--sumi-bg-soft`、`--sumi-bg-sunken` | 页面、浮起的面板、浅色填充、凹陷区域 |
| `--sumi-line`、`--sumi-line-2` | 边框：细线和较深的线 |
| `--sumi-accent` | 用 `theme.accent` 选定的强调色 |
| `--sumi-link` | 链接 |
| `--c-note`、`--c-tip`、`--c-important`、`--c-warning`、`--c-caution` | 状态色，与提示框相同 |
| `--sumi-code-bg`、`--sumi-code-inline` | 代码块和行内代码的背景 |
| `--sumi-font`、`--sumi-font-mono` | 正文字体和代码字体 |
| `--sumi-radius`、`--sumi-radius-sm` | 圆角半径 |
{.compact}

所有变量都会随配色变化，所以使用它们的 CSS 不需要额外的深色模式规则。如果你要自己写，请以 `[data-theme="dark"]` 为条件。

要添加样式表，就像在 Material 中那样，在 `on_config` 里把它追加到 `config.extra_css`，并在 `on_post_build` 里复制文件。Sumi 会在自身 CSS 之后加载 `extra_css`。

## 脚本 {#scripts}

Sumi 没有即时加载：每次点击链接都是一次普通的页面加载，所以在 `DOMContentLoaded` 时运行的脚本在每个页面上都会运行。读者在浅色和深色之间切换时，Sumi 会更新 `<html>` 上的 `data-theme`，并触发一个事件：

```js
document.addEventListener("sumi:theme", (event) => {
  redraw(event.detail.theme);  // "light" 或 "dark"
});
```

`data-theme` 在页面绘制之前就已设置好，所以脚本随时都能读取它。不要假定 Sumi 自己的脚本已经先运行：它是延迟加载的。

在[双语对照](i18n.md#bilingual-view)里，页面会在名为 `sumi-pane` 的 frame 中再加载一次，`<html>` 上带有 `sumi-pane` 类。统计访问或弹出窗口的脚本应当跳过它：`if (window.name === 'sumi-pane') return;`。

## 模板 {#templates}

Sumi 提供常见的 MkDocs 模板块。继承 Material `main.html` 的插件或用户覆盖可以这样对应：

| Material 模板块 | 在 Sumi 中 |
| --- | --- |
| `extrahead`、`htmltitle`、`site_meta`、`styles`、`analytics` | 名称相同 |
| `scripts`、`content`、`header`、`footer` | 名称相同 |
| `announce` | `theme.announcement` 选项 |
| `outdated` | 设置 `theme.version_provider: mike` 后内置 |
| `tabs`、`hero` | 页眉标签是内置的；主视觉请用[首页](../pages/landing.md) |
{.compact}

Sumi 的局部模板和 Material 的名称、内容都不同，见[覆盖模板](overrides.md)。如果你的插件替换了 Material 的某个局部模板（例如“最后更新”那一行），请改为把信息写进页面，或者在 issue 中请求加一个钩子。

## Sumi 已经具备的功能 {#features-sumi-already-has}

有些插件是为了填补 Sumi 本身已经覆盖的空白。如果你的插件属于这类，请在文档里说明它如何与 Sumi 的版本共存，而不是重复实现。

| Material 插件 | 在 Sumi 中 |
| --- | --- |
| `blog` | [博客](../pages/blog.md)读取相同的文件夹、front matter 和 `.authors.yml` |
| `tags` | 博客文章上的标签，以及博客首页的标签筛选 |
| `search` | MkDocs 的 `search` 插件，显示在 Sumi 的命令面板中 |
| `privacy`、`offline` | 不需要：字体、图标和脚本都随主题附带，阅读时不从网络获取任何内容 |
| `social` | 未内置。Sumi 会写出 `og:title`、`og:description` 和 `twitter:card`，只有设置了 `social_image` 或页面 `image:` 时才写出 `og:image`，所以社交卡片插件可以加上自己的图片而不会重复 |
{.compact}

## 在 Sumi 上测试 {#test-against-sumi}

1. 用 `theme: sumi` 和 `plugins: [search, sumi, your-plugin]` 构建一个小站点，使用 `mkdocs build --strict`。
2. 在两种配色下和窄屏上检查输出。
3. 如果你的插件会往页面里加内容，打开 `/print/`，也就是[打印版](../pages/print.md)看一看。

## 列入推荐名单 {#get-listed}

[提交一个 issue](https://github.com/mkdocs-ng/mkdocs-sumi/issues)，写上你的插件名称，附一张它在 Sumi 中的截图。能正常工作的插件会被加到[迁移指南](../start/migrate.md#what-keeps-working)中。如果 Sumi 有什么地方妨碍了你，也请在同一个 issue 里说明：缺少的模板块或变量，由我们来加，比你绕过去容易得多。

## Sumi 已适配样式的插件 {#plugins-sumi-styles}

这些插件输出的 HTML 会被 Sumi 配上与站点其余部分一致的样式。

### mkdocstrings {#mkdocstrings}

[mkdocstrings](https://mkdocstrings.github.io/) 生成的 API 页面会使用 Sumi 的代码字体和颜色：签名、符号徽章（`mod`、`class`、`func`、`meth`、`attr`、`type`、`param`）、标签、嵌套成员、小节表格和列表、参数标题、反向链接，以及一个低调的“源代码”面板。下面这些选项和 Sumi 很搭：

```yaml title="mkdocs.yml"
plugins:
  - search
  - sumi
  - mkdocstrings:
      handlers:
        python:
          options:
            show_root_heading: true
            show_symbol_type_heading: true
            show_symbol_type_toc: true
            separate_signature: true
            show_signature_annotations: true
            signature_crossrefs: true
```
