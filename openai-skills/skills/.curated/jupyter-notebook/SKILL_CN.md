---
name: "jupyter-notebook"
description: "当用户要求创建、搭建或编辑 Jupyter 笔记本（`.ipynb`）用于实验、探索或教程时使用；更喜欢捆绑的模板并运行辅助脚本 `new_notebook.py` 生成一个干净的起始笔记本。"
---


# Jupyter 笔记本技能

为两种主要模式创建干净、可重现的 Jupyter 笔记本：

- 实验和探索性分析
- 教程和面向教学的演练

更喜欢捆绑的模板和辅助脚本以获得一致的结构和更少的 JSON 错误。

## 何时使用
- 从头创建新的 `.ipynb` 笔记本。
- 将粗略的笔记或脚本转换为结构化的笔记本。
- 重构现有笔记本以更具可重现性和可浏览性。
- 构建将被其他人阅读或重新运行的实验或教程。

## 决策树
- 如果请求是探索性的、分析性的或假设驱动的，请选择 `experiment`。
- 如果请求是指示性的、分步的或特定于受众的，请选择 `tutorial`。
- 如果编辑现有笔记本，请将其视为重构：保留意图并改进结构。

## 技能路径（设置一次）

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export JUPYTER_NOTEBOOK_CLI="$CODEX_HOME/skills/jupyter-notebook/scripts/new_notebook.py"
```

用户范围的技能安装在 `$CODEX_HOME/skills` 下（默认：`~/.codex/skills`）。

## 工作流程
1. 锁定意图。
确定笔记本类型：`experiment` 或 `tutorial`。
捕获目标、受众以及"完成"的样子。

2. 从模板搭建。
使用辅助程序以避免手动编写原始笔记本 JSON。

```bash
uv run --python 3.12 python "$JUPYTER_NOTEBOOK_CLI" \
  --kind experiment \
  --title "Compare prompt variants" \
  --out output/jupyter-notebook/compare-prompt-variants.ipynb
```

```bash
uv run --python 3.12 python "$JUPYTER_NOTEBOOK_CLI" \
  --kind tutorial \
  --title "Intro to embeddings" \
  --out output/jupyter-notebook/intro-to-embeddings.ipynb
```

3. 用小的、可运行的步骤填充笔记本。
保持每个代码单元格专注于一个步骤。
添加解释目的和预期结果的简短 markdown 单元格。
当简短摘要有效时，避免大的、嘈杂的输出。

4. 应用正确的模式。
对于实验，请遵循 `references/experiment-patterns.md`。
对于教程，请遵循 `references/tutorial-patterns.md`。

5. 使用现有笔记本时安全编辑。
保留笔记本结构；除非它改进从上到下的故事，否则避免重新排序单元格。
更喜欢有针对性的编辑而不是完全重写。
如果必须编辑原始 JSON，请先查看 `references/notebook-structure.md`。

6. 验证结果。
当环境允许时，从上到下运行笔记本。
如果执行不可能，请明确说明并说明如何在本地验证。
使用 `references/quality-checklist.md` 中的最终通过检查清单。

## 模板和辅助脚本
- 模板位于 `assets/experiment-template.ipynb` 和 `assets/tutorial-template.ipynb` 中。
- 辅助脚本加载模板、更新标题单元格并写入笔记本。

脚本路径：
- `$JUPYTER_NOTEBOOK_CLI`（安装默认：`$CODEX_HOME/skills/jupyter-notebook/scripts/new_notebook.py`）

## 临时和输出约定
- 使用 `tmp/jupyter-notebook/` 作为中间文件；完成后删除。
- 在此仓库中工作时，将最终工件写入 `output/jupyter-notebook/`。
- 使用稳定的、描述性的文件名（例如，`ablation-temperature.ipynb`）。

## 依赖项（仅在需要时安装）
更喜欢 `uv` 进行依赖管理。

用于本地笔记本执行的可选 Python 包：

```bash
uv pip install jupyterlab ipykernel
```

捆绑的搭建脚本仅使用 Python 标准库，不需要额外的依赖项。

## 环境
没有必需的环境变量。

## 参考地图
- `references/experiment-patterns.md`：实验结构和启发式方法。
- `references/tutorial-patterns.md`：教程结构和教学流程。
- `references/notebook-structure.md`：笔记本 JSON 形状和安全编辑规则。
- `references/quality-checklist.md`：最终验证检查清单。
