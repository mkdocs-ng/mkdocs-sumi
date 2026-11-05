---
description: 安全地升级到新的 Sumi 版本，并让模板覆盖跟上变化。
---

# 升级 {#upgrade}

Sumi 遵循[语义化版本](https://semver.org/lang/zh-CN/)。版本号以 `0.` 开头期间，次版本（0.2 → 0.3）可能会改动选项或模板；修订版本（0.2.0 → 0.2.1）只修复问题。所有改动都列在[发布记录](../../releases.md)中。

## 步骤 {#steps}

1. 阅读从你当前版本到新版本之间每个版本的发布说明，留意 **Changed** 和 **Removed** 条目。
2. 更新软件包：

    ```sh {tab="pip"}
    pip install --upgrade mkdocs-sumi
    ```

    ```sh {tab="uv"}
    uv lock --upgrade-package mkdocs-sumi
    ```

3. 把警告当作错误来构建：

    ```sh
    mkdocs build --strict
    ```

4. 用 `mkdocs serve` 看几页：首页、一篇长文档、博客，以及你覆盖过模板的页面。
5. 更新 `requirements.txt`（或锁文件）中的版本号并提交，让托管服务用同样的版本构建。
{.steps}

## MkDocs NG {#mkdocs-ng}

Sumi 需要 [MkDocs NG](https://github.com/mkdocs-ng/mkdocs) 1.9 或更新版本，安装 Sumi 时会自动安装它。有些功能需要更新的 MkDocs NG：

| 功能 | 需要 |
| --- | --- |
| 原生多语言（`languages:`）和双语对照 | MkDocs NG 1.11 |
| `llms.txt` 和页面的 Markdown 副本 | MkDocs NG 1.9 |
{.compact}

单独升级 MkDocs NG 时，也请阅读[它的发布说明](https://mkdocs-ng.org/about/release-notes/)。

## 模板覆盖 {#template-overrides}

覆盖会替换 Sumi 自带的模板。新版本修改了这个模板时，你的副本不会自动得到这些修改。升级之后：

1. 列出你的覆盖：`custom_dir` 中的文件。
2. 逐个和 Sumi `theme/` 文件夹中的新版本对比。这个文件夹的位置可以用 `python -c "import mkdocs_sumi, os; print(os.path.dirname(mkdocs_sumi.__file__))"` 查到。
3. 把改动合并过来，同时保留你自己的修改。

覆盖 `main.html` 中的某个[块](../customize/overrides.md)，而不是整个文件，可以让这项工作少很多。

## 回退 {#going-back}

如果新版本出了问题，先固定回上一个版本，再带着构建输出[提一个 issue](https://github.com/mkdocs-ng/mkdocs-sumi/issues)：

```text title="requirements.txt"
mkdocs-sumi==0.2.1
```
