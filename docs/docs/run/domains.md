---
description: Serve the site from your own domain, preview changes before they go live, and publish several versions.
---

# Domains and previews

## Your own domain

1. Add a DNS record with your domain provider. For a subdomain such as `docs.example.com`, a `CNAME` record pointing to the host: `<user>.github.io` for GitHub Pages, the `*.pages.dev` address for Cloudflare Pages, or the `*.netlify.app` address for Netlify. For an apex domain such as `example.com`, follow the host's guide: [GitHub](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site), [Cloudflare](https://developers.cloudflare.com/pages/configuration/custom-domains/), [Netlify](https://docs.netlify.com/domains-https/custom-domains/).
2. Enter the domain in the host's settings. On GitHub, that is **Settings → Pages → Custom domain**; turn on **Enforce HTTPS** once the certificate is ready.
3. Set `site_url` to the new address:

```yaml title="mkdocs.yml"
site_url: https://docs.example.com/
```

`site_url` is where the sitemap, the feed, `llms.txt`, social previews and canonical links point. Without it, they are missing or incomplete.

> [!NOTE]
> With `mkdocs gh-deploy`, GitHub reads the domain from a `CNAME` file in the published branch. Put a file named `CNAME` holding the domain in `docs/`, and every build copies it along. A GitHub Actions deployment does not need the file.

### Moving to a new domain

Readers and search engines still have the old links. Most hosts can redirect a whole domain: keep the old domain attached and add a redirect rule to the new one, path included. For moved pages inside one site, the [mkdocs-redirects](https://github.com/mkdocs/mkdocs-redirects) plugin writes small pages that forward to the new address.

## Preview before publishing

| Where | How |
| --- | --- |
| Your machine | `mkdocs serve` rebuilds on every save and reloads the browser. If a page looks different from a full build, `mkdocs serve --clean` turns off the preview server's caches. |
| A built copy | `mkdocs build` and then `python -m http.server -d site`, to see the real output. Opening `site/index.html` from the file system is not enough: browsers block search and fonts on `file://` pages. |
| Pull requests on Cloudflare or Netlify | Every branch and pull request gets its own preview address, posted on the pull request. |
| Pull requests on GitHub Pages | GitHub Pages serves one version of a site. The [workflow](deploy.md#github-pages) still builds pull requests with `--strict`, which catches broken links. To browse a preview, check out the branch and build it locally, or let Cloudflare or Netlify deploy previews. |
{.fields}

Search engines should not index previews. Preview hosts usually add an `X-Robots-Tag: noindex` header to preview addresses; check yours if previews show up in search results.

## Several versions

To keep the documentation of older releases online, publish each version to its own folder with [mike](https://github.com/jimporter/mike). Sumi then shows a version menu in the header and a notice on old versions. See [Navigation](../customize/navigation.md#versions).

## Several languages

A translated site is one build: each language is written to its own folder, such as `/zh/`. See [Languages](../customize/i18n.md). Nothing changes for deployment.
