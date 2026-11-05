---
description: 用随主题附带的 KaTeX 排版行内公式和独立公式。
---

# 数学公式

把 TeX 写在美元符号之间。Sumi 用随主题附带的 [KaTeX](https://katex.org/) 排版公式，只在含有公式的页面上加载。

## 行内公式 {#inline-formulas}

```markdown
欧拉恒等式 $e^{i\pi} + 1 = 0$ 把五个常数联系在了一起。
```

欧拉恒等式 $e^{i\pi} + 1 = 0$ 把五个常数联系在了一起。

后面跟空格的美元符号，或者前面紧挨字母或数字的美元符号，都不算公式，所以 $5 或 $10 这样的价格会原样显示。要写一个字面上的美元符号，请转义成 `\$`。

## 独立公式 {#display-formulas}

```markdown
$$
\hat{f}(\xi) = \int_{-\infty}^{\infty} f(x)\, e^{-2\pi i x \xi}\, dx
$$
```

$$
\hat{f}(\xi) = \int_{-\infty}^{\infty} f(x)\, e^{-2\pi i x \xi}\, dx
$$

多行环境也可以用：

$$
\begin{aligned}
\nabla \cdot \mathbf{E} &= \frac{\rho}{\varepsilon_0} \\
\nabla \times \mathbf{B} &= \mu_0 \mathbf{J} + \mu_0 \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}
\end{aligned}
$$

## 兼容性 {#compatibility}

如果配置了 `pymdownx.arithmatex` 并设置 `generic: true`，Sumi 会用同一个 KaTeX 渲染它的输出，并关闭自己的 `$` 解析。要完全关闭数学公式，在[插件](../customize/plugin.md)上设置 `math: false`。

## 参考 {#reference}

| 项目 | 说明 |
| --- | --- |
| 输出 | `<span class="sumi-math">` 和 `<div class="sumi-math">` 保存 TeX，在浏览器中排版。 |
| 没有 Sumi 时 | 美元符号之间的 TeX。GitHub 也会排版。 |
| JavaScript | KaTeX，随主题打包，只在有公式的页面加载。 |
| 限制 | KaTeX 支持大部分 LaTeX 数学语法，但不是所有宏包。 |
{.compact}
