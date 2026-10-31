---
description: A downloads and release notes page with checksums, generated from YAML.
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

`releases` is either a list in the front matter or a path to a YAML file relative to `docs/`.

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
