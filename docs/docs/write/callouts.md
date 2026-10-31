---
description: Notes, tips and warnings written as GitHub-style blockquotes.
---

# Callouts

A callout draws attention to information that should not be missed. Sumi uses the syntax GitHub introduced for alerts, so callouts render on GitHub, in your editor's preview and in Sumi alike.

```markdown
> [!NOTE]
> Sumi reads the same syntax GitHub does.
```

> [!NOTE]
> Sumi reads the same syntax GitHub does.

## The five types

> [!NOTE]
> Useful information that users should know, even when skimming.

> [!TIP]
> Helpful advice for doing things better or more easily.

> [!IMPORTANT]
> Key information users need to achieve their goal.

> [!WARNING]
> Urgent information that needs immediate attention to avoid problems.

> [!CAUTION]
> Advises about risks or negative outcomes of certain actions.

```markdown
> [!NOTE]
> [!TIP]
> [!IMPORTANT]
> [!WARNING]
> [!CAUTION]
```

Sumi also accepts the type names used by Material for MkDocs — `info`, `success`, `question`, `failure`, `danger`, `bug`, `example`, `quote`, `abstract` and `todo` — each mapped to the closest colour.

## Custom titles

Text after the marker replaces the default title:

```markdown
> [!WARNING] Back up first
> `mkdocs gh-deploy --force` replaces the whole `gh-pages` branch.
```

> [!WARNING] Back up first
> `mkdocs gh-deploy --force` replaces the whole `gh-pages` branch.

## Collapsible callouts

Add `-` after the marker for a callout that starts closed, or `+` for one that starts open but can be closed.

```markdown
> [!TIP]- Why is it called Sumi?
> *Sumi* (墨) is the ink of East Asian calligraphy: one colour, many shades.
```

> [!TIP]- Why is it called Sumi?
> *Sumi* (墨) is the ink of East Asian calligraphy: one colour, many shades.

Collapsed callouts are printed open.

## Rich content

A callout can hold anything a blockquote can — lists, code, tables, even other callouts.

> [!IMPORTANT] Before you upgrade
> 1. Read the [release notes](../../releases.md).
> 2. Pin the version in `requirements.txt`:
>
>     ```text
>     mkdocs-sumi==0.1.0
>     ```

## Admonitions

If your pages already use the `admonition` extension, they keep working and look the same:

```markdown
!!! warning "Deprecated"
    Use `theme.palette` instead.
```

!!! warning "Deprecated"
    Use `theme.palette` instead.

`??? note` and `???+ note` from `pymdownx.details` are styled as collapsible callouts.
