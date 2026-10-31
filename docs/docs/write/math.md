---
description: Inline and display formulas typeset by a bundled copy of KaTeX.
---

# Math

Write TeX between dollar signs. Sumi typesets it with a bundled copy of [KaTeX](https://katex.org/), loaded only on pages that contain a formula.

## Inline formulas

```markdown
Euler's identity, $e^{i\pi} + 1 = 0$, links five constants.
```

Euler's identity, $e^{i\pi} + 1 = 0$, links five constants.

A dollar sign followed by a space, or preceded by a letter or digit, is not math — so prices such as $5 or $10 stay as written. Escape a literal dollar sign as `\$`.

## Display formulas

```markdown
$$
\hat{f}(\xi) = \int_{-\infty}^{\infty} f(x)\, e^{-2\pi i x \xi}\, dx
$$
```

$$
\hat{f}(\xi) = \int_{-\infty}^{\infty} f(x)\, e^{-2\pi i x \xi}\, dx
$$

Multi-line environments work too:

$$
\begin{aligned}
\nabla \cdot \mathbf{E} &= \frac{\rho}{\varepsilon_0} \\
\nabla \times \mathbf{B} &= \mu_0 \mathbf{J} + \mu_0 \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}
\end{aligned}
$$

## Compatibility

If `pymdownx.arithmatex` is configured with `generic: true`, Sumi renders its output with the same KaTeX and turns its own `$` parsing off. To disable math entirely, set `math: false` on the [plugin](../customize/plugin.md).
