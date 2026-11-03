---
description: 把有序列表变成分步操作说明。
---

# 步骤

在有序列表下面加一行 `{.steps}`，它就会显示为操作步骤：编号由一条线串起来，每一步的第一行就是这一步的标题。

````markdown
1. 创建虚拟环境

    ```sh
    python -m venv .venv
    ```

2. 安装 Sumi

    ```sh
    pip install mkdocs-sumi
    ```

3. 启动预览服务器

    运行 `mkdocs serve`，然后打开它输出的地址。
{.steps}
````

1. 创建虚拟环境

    ```sh
    python -m venv .venv
    ```

2. 安装 Sumi

    ```sh
    pip install mkdocs-sumi
    ```

3. 启动预览服务器

    运行 `mkdocs serve`，然后打开它输出的地址。
{.steps}

## 简短的步骤 {#short-steps}

步骤不一定要有正文：

1. 写作
2. 预览
3. 发布
{.steps}

## 写法建议 {#guidelines}

- 每一步都以动词开头。
- 每一步只做一件事。如果某一步还需要自己的列表，它多半应该拆成两步。
- 步骤内容缩进四个空格，这样它才会留在这一步里。
