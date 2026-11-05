---
description: A downloads and release notes page with checksums, generated from YAML, GitHub Releases or PyPI.
---

# Releases

A page with `template: releases.html` lists versions with their notes and downloadable assets. Each asset shows its size and a SHA-256 checksum that copies on click. See [this site's releases](../../releases.md).

```markdown title="docs/releases.md"
---
template: releases.html
releases: releases.yml
---

# Releases

Download the latest version, or browse the history.
```

`releases` is a list in the front matter, a path to a YAML file relative to `docs/`, or [sources to read](#remote) such as GitHub Releases.

```yaml title="docs/releases.yml"
- version: 0.2.0
  date: 2026-12-01
  summary: Versioned docs and a Japanese interface.
  notes: |
    - **New:** `version_provider: mike`.
    - **Fixed:** tabs no longer jump when switching.
  assets:
    - name: mkdocs_sumi-0.2.0-py3-none-any.whl
      url: https://example.com/mkdocs_sumi-0.2.0-py3-none-any.whl
      size: 1.9 MB
      sha256: 9f2c0a…
- version: 0.1.0
  date: 2026-11-01
  notes: First release.
```

## Fields

| Key | Type | Description |
| --- | --- | --- |
| `version` | string | Version number; also the anchor, so `releases/#v0-2-0` links to it. |
| `title` | string | Shown instead of the version, if set. |
| `date` | date | Release date. |
| `status` | string | `latest`, `stable`, `prerelease` or `archived`. The first release defaults to `latest`. |
| `summary` | string | One line under the heading. |
| `notes` | string | Release notes in Markdown. |
| `assets` | list | Downloads: `name`, `url`, `size`, `sha256`. |
{.fields}

The page's own Markdown is shown above the list, so you can add installation instructions or a support policy.

## From GitHub Releases and PyPI {#remote}

Instead of writing every release by hand, let the page read them when the site builds:

```yaml title="docs/releases.md"
---
template: releases.html
releases:
  github: owner/repo     # versions, dates and notes from GitHub Releases
  pypi: package-name     # downloads with sizes and SHA-256 checksums
  file: releases.yml     # optional: hand-written fields that win
---
```

| Key | Description |
| --- | --- |
| `github` | Every published release of the repository, newest first. Drafts are left out, and a release marked as a pre-release gets the `prerelease` status. The first paragraph of the release text becomes the `summary`, the rest the `notes`; headings move down two levels, and `#123` and `@user` become links. Files attached to the release become `assets`. |
| `pypi` | The files of each version on PyPI, for releases that have no `assets` of their own. |
| `file` | Entries matched to the same `version` replace its fields, so you can give a release a better summary or notes. Versions only in the file are sorted in by `date`. |
{.fields}

Set `GITHUB_TOKEN` (or `GH_TOKEN`) when building in CI to avoid GitHub's limit of 60 requests an hour without one. Each source is read once per build process, so `mkdocs serve` doesn't refetch it on every change. When a source can't be reached the build warns and shows what it has.

To refresh the page when you publish a release, rebuild the site from your release workflow. This site's [`release.yml`](https://github.com/mkdocs-ng/mkdocs-sumi/blob/main/.github/workflows/release.yml) starts the docs workflow once the package is on PyPI.
