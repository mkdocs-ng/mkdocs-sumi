---
description: Show alternatives — operating systems, languages, package managers — as tabs.
---

# Tabs

Consecutive code fences that each carry `{tab="…"}` become one tab set. Without Sumi, they are simply consecutive code blocks with a hint of what each one is for.

````markdown
```sh {tab="macOS"}
brew install python
```

```sh {tab="Ubuntu"}
sudo apt install python3
```

```powershell {tab="Windows"}
winget install Python.Python.3.12
```
````

```sh {tab="macOS"}
brew install python
```

```sh {tab="Ubuntu"}
sudo apt install python3
```

```powershell {tab="Windows"}
winget install Python.Python.3.12
```

## Synchronised tabs

Tab sets with the same labels stay in sync: choose **Windows** once and every matching tab set on every page follows. The choice is remembered in the browser.

```sh {tab="macOS"}
python3 -m venv .venv && source .venv/bin/activate
```

```sh {tab="Ubuntu"}
python3 -m venv .venv && source .venv/bin/activate
```

```powershell {tab="Windows"}
py -m venv .venv; .venv\Scripts\Activate.ps1
```

## Titles inside tabs

`title` and `tab` combine:

````markdown
```yaml {tab="YAML" title="mkdocs.yml"}
theme: sumi
```

```toml {tab="TOML" title="pyproject.toml"}
[tool.mkdocs]
theme = "sumi"
```
````

```yaml {tab="YAML" title="mkdocs.yml"}
theme:
  name: sumi
```

```toml {tab="TOML" title="pyproject.toml"}
[tool.mkdocs]
theme = "sumi"
```

## Tabs with prose

For tabs that contain more than code, use `pymdownx.tabbed` with `alternate_style: true`. Sumi styles it to match:

```yaml title="mkdocs.yml"
markdown_extensions:
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
```

In print and in the Markdown copy, every tab is shown one after another under its label.
