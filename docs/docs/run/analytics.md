---
description: Count visits with Google Analytics, Plausible or Umami, and ask readers whether a page helped.
---

# Analytics and feedback

Sumi adds no tracking of its own. Turn on one analytics provider under `extra.analytics`, and optionally a "Was this page helpful?" widget at the end of each page.

## Analytics providers

```yaml {tab="Plausible" title="mkdocs.yml"}
extra:
  analytics:
    provider: plausible
    domain: docs.example.com   # defaults to the domain the page is served from
    src: https://plausible.io/js/script.js   # change it for a self-hosted Plausible
```

```yaml {tab="Umami" title="mkdocs.yml"}
extra:
  analytics:
    provider: umami
    website_id: 4f3c1e2a-0000-0000-0000-000000000000
    src: https://cloud.umami.is/script.js    # change it for a self-hosted Umami
    domains: [docs.example.com]              # optional: only count these hosts
```

```yaml {tab="Google Analytics" title="mkdocs.yml"}
extra:
  analytics:
    provider: google
    property: G-XXXXXXXXXX
```

The `google_analytics` setting of older MkDocs versions works too.

| Output | Details |
| --- | --- |
| Where | One `<script>` in the `<head>` of every page, added by `partials/analytics.html` |
| When | Loaded with `defer` or `async`, so it never blocks the page |
| Not counted | Pages shown inside the [bilingual view](../customize/i18n.md#bilingual-view), so one visit is not counted twice |
{.compact}

Plausible and Umami do not use cookies, so most sites can use them without a consent banner. Google Analytics sets cookies: check what your readers' laws require before turning it on.

To use another provider, [override](../customize/overrides.md) the `analytics` block in `main.html`.

## Was this page helpful?

```yaml title="mkdocs.yml"
theme:
  name: sumi
  feedback: true
```

This adds a small form after the content of each docs page and blog post, with **Yes** and **No** buttons in the site's language. When a reader picks one, Sumi:

1. sends a `feedback` event to the analytics provider on the page: Google Analytics (`event_label` is the page path, `value` the rating), Plausible (a `Feedback` goal with `page` and `rating` properties) or Umami (a `feedback` event with the same data);
2. dispatches a `sumi:feedback` event on `document`, with `detail.page` and `detail.value`, for anything else;
3. thanks the reader with the rating's note.

```js title="docs/assets/feedback.js"
document.addEventListener('sumi:feedback', (e) => {
  navigator.sendBeacon('https://example.com/feedback', JSON.stringify(e.detail));
});
```

In Plausible, add a custom event goal named `Feedback` to see the results.

### Your own wording

Material's settings are read as they are, so a migrated site keeps its feedback widget:

```yaml title="mkdocs.yml"
extra:
  analytics:
    provider: plausible
    feedback:
      title: Was this page helpful?
      ratings:
        - icon: thumbs-up        # material/emoticon-happy-outline works too
          name: This page was helpful
          data: 1
          note: Thanks for your feedback!
        - icon: thumbs-down
          name: This page could be improved
          data: 0
          note: >-
            Thanks! Help us improve it by
            <a href="https://github.com/acme/docs/issues/new?title=[Feedback]+{title}+-+{url}" target="_blank" rel="noopener">opening an issue</a>.
```

`note` may hold HTML. `{title}` and `{url}` in it are replaced by the page title and address. The same keys work under `theme.feedback` when you do not use Material's layout.

### Limits

- A reader can rate a page once per visit. Ratings are not stored in the browser.
- Without JavaScript the form stays hidden, since it could not send anything.
- Landing pages and the blog index have no widget. Hide it on one page with `hide: [feedback]` in its front matter, or on every page with `theme.hide`.
