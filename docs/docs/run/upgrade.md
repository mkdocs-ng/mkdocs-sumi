---
description: Move to a new Sumi release safely, and keep template overrides in step.
---

# Upgrade

Sumi follows [semantic versioning](https://semver.org/). While the version starts with `0.`, a minor release (0.2 → 0.3) can change options or templates; a patch release (0.2.0 → 0.2.1) only fixes bugs. Every change is listed on the [releases page](../../releases.md).

## Steps

1. Read the release notes for every version between yours and the new one. Look for **Changed** and **Removed** entries.
2. Update the package:

    ```sh {tab="pip"}
    pip install --upgrade mkdocs-sumi
    ```

    ```sh {tab="uv"}
    uv lock --upgrade-package mkdocs-sumi
    ```

3. Build with warnings as errors:

    ```sh
    mkdocs build --strict
    ```

4. Look through a few pages with `mkdocs serve`: the home page, a long docs page, the blog, and any page whose templates you override.
5. Update the version pin in `requirements.txt` (or your lock file) and commit it, so your host builds with the same version.
{.steps}

## MkDocs NG

Sumi needs [MkDocs NG](https://github.com/mkdocs-ng/mkdocs) 1.9 or newer, and installs it for you. Some features need a newer MkDocs NG:

| Feature | Needs |
| --- | --- |
| Native translations (`languages:`) and the bilingual view | MkDocs NG 1.11 |
| `llms.txt` and Markdown copies of pages | MkDocs NG 1.9 |
{.compact}

When you upgrade MkDocs NG on its own, read [its release notes](https://mkdocs-ng.org/about/release-notes/) as well.

## Template overrides

An override replaces Sumi's copy of a template. When a release changes that template, your copy does not get the change. After an upgrade:

1. List your overrides: the files in your `custom_dir`.
2. For each, compare it with the new version in Sumi's `theme/` folder, which you can find with `python -c "import mkdocs_sumi, os; print(os.path.dirname(mkdocs_sumi.__file__))"`.
3. Bring over the changes, keeping your own edits.

Overriding a [block](../customize/overrides.md) of `main.html` rather than a whole file keeps this work small.

## Going back

If a release causes trouble, pin the previous version and [open an issue](https://github.com/mkdocs-ng/mkdocs-sumi/issues) with the build output:

```text title="requirements.txt"
mkdocs-sumi==0.2.1
```
