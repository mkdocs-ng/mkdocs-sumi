---
description: Turn a numbered list into a step-by-step procedure.
---

# Steps

Put `{.steps}` under an ordered list to draw it as a procedure: numbered markers joined by a line, with each step's first line as its heading.

````markdown
1. Create a virtual environment

    ```sh
    python -m venv .venv
    ```

2. Install Sumi

    ```sh
    pip install mkdocs-sumi
    ```

3. Start the preview server

    Run `mkdocs serve` and open the address it prints.
{.steps}
````

1. Create a virtual environment

    ```sh
    python -m venv .venv
    ```

2. Install Sumi

    ```sh
    pip install mkdocs-sumi
    ```

3. Start the preview server

    Run `mkdocs serve` and open the address it prints.
{.steps}

## Short steps

Steps do not need bodies:

1. Write
2. Preview
3. Publish
{.steps}

## Guidelines

- Start each step with a verb.
- Keep one action per step. If a step needs a list of its own, it is probably two steps.
- Indent step content by four spaces so it stays inside the step.
