---
description: 用 Google Analytics、Plausible 或 Umami 统计访问量，并询问读者这一页有没有帮助。
---

# 访问统计与反馈 {#analytics-and-feedback}

Sumi 本身不做任何追踪。你可以在 `extra.analytics` 下打开一个统计服务，还可以在每页末尾加一个“这页内容对你有帮助吗？”反馈组件。

## 统计服务 {#analytics-providers}

```yaml {tab="Plausible" title="mkdocs.yml"}
extra:
  analytics:
    provider: plausible
    domain: docs.example.com   # 默认是页面所在的域名
    src: https://plausible.io/js/script.js   # 自建 Plausible 时改成自己的地址
```

```yaml {tab="Umami" title="mkdocs.yml"}
extra:
  analytics:
    provider: umami
    website_id: 4f3c1e2a-0000-0000-0000-000000000000
    src: https://cloud.umami.is/script.js    # 自建 Umami 时改成自己的地址
    domains: [docs.example.com]              # 可选：只统计这些域名
```

```yaml {tab="Google Analytics" title="mkdocs.yml"}
extra:
  analytics:
    provider: google
    property: G-XXXXXXXXXX
```

旧版 MkDocs 的 `google_analytics` 设置同样有效。

| 输出 | 说明 |
| --- | --- |
| 位置 | 每个页面 `<head>` 中的一个 `<script>`，由 `partials/analytics.html` 加入 |
| 加载方式 | 使用 `defer` 或 `async` 加载，不会阻塞页面 |
| 不统计 | [双语对照](../customize/i18n.md#bilingual-view)里显示的页面，避免一次访问被算两次 |
{.compact}

Plausible 和 Umami 不使用 Cookie，大多数站点不需要弹出同意提示。Google Analytics 会设置 Cookie，打开之前请先确认读者所在地区的法律要求。

要接入其他统计服务，请[覆盖](../customize/overrides.md) `main.html` 中的 `analytics` 块。

## 这页内容对你有帮助吗？ {#was-this-page-helpful}

```yaml title="mkdocs.yml"
theme:
  name: sumi
  feedback: true
```

这会在每个文档页和博客文章的正文后面加一个小表单，带有“有帮助”和“没帮助”两个按钮，文字跟随站点语言。读者点了其中一个之后，Sumi 会：

1. 向页面上的统计服务发送一个 `feedback` 事件：Google Analytics（`event_label` 是页面路径，`value` 是评分）、Plausible（一个名为 `Feedback` 的目标，带 `page` 和 `rating` 两个属性）或 Umami（一个 `feedback` 事件，数据相同）；
2. 在 `document` 上派发一个 `sumi:feedback` 事件，带 `detail.page` 和 `detail.value`，方便接入其他服务；
3. 显示这个评分的感谢语。

```js title="docs/assets/feedback.js"
document.addEventListener('sumi:feedback', (e) => {
  navigator.sendBeacon('https://example.com/feedback', JSON.stringify(e.detail));
});
```

在 Plausible 中，添加一个名为 `Feedback` 的自定义事件目标就能看到结果。

### 自定义文字 {#your-own-wording}

Material 的设置会原样读取，所以迁移过来的站点会保留原来的反馈组件：

```yaml title="mkdocs.yml"
extra:
  analytics:
    provider: plausible
    feedback:
      title: 这页内容对你有帮助吗？
      ratings:
        - icon: thumbs-up        # material/emoticon-happy-outline 也可以
          name: 有帮助
          data: 1
          note: 感谢你的反馈！
        - icon: thumbs-down
          name: 还可以改进
          data: 0
          note: >-
            谢谢！欢迎<a href="https://github.com/acme/docs/issues/new?title=[Feedback]+{title}+-+{url}" target="_blank" rel="noopener">提一个 issue</a> 告诉我们怎么改进。
```

`note` 可以包含 HTML，其中的 `{title}` 和 `{url}` 会替换成页面标题和地址。不用 Material 的写法时，同样的键也可以写在 `theme.feedback` 下。

### 限制 {#limits}

- 每次打开页面，读者只能评一次分。评分不会保存在浏览器里。
- 没有 JavaScript 时表单保持隐藏，因为它什么也发不出去。
- 首页（落地页）和博客索引页没有反馈组件。在某一页的 front matter 里写 `hide: [feedback]` 可以隐藏它，用 `theme.hide` 可以在所有页面上隐藏。
