---
name: huggingface-community-evals
description: 使用 inspect-ai 和 lighteval 在本地硬件上运行 Hugging Face Hub 模型的评估。用于后端选择、本地 GPU 评估以及在 vLLM / Transformers / accelerate 之间进行选择。不适用于 HF Jobs 编排、模型卡片 PR、.eval_results 发布或社区评估自动化。
---

# 概述

此技能用于**在本地硬件上对 Hugging Face Hub 上的模型进行评估**。

它涵盖：
- 带本地推理的 `inspect-ai`
- 带本地推理的 `lighteval`
- 在 `vllm`、Hugging Face Transformers 和 `accelerate` 之间进行选择
- 冒烟测试、任务选择和后端回退策略

它**不**涵盖：
- Hugging Face Jobs 编排
- 模型卡片或 `model-index` 编辑
- README 表格提取
- Artificial Analysis 导入
- `.eval_results` 生成或发布
- PR 创建或社区评估自动化

如果用户希望**在 Hugging Face Jobs 上远程运行相同的评估**，请切换到 `hugging-face-jobs` 技能并将此技能中的本地脚本传递给它。

如果用户希望**将结果发布到社区评估工作流**，请在生成评估运行后停止，并将该发布步骤交给 `~/code/community-evals`。

> 以下所有路径均相对于包含此 `SKILL.md` 的目录。

# 何时使用哪个脚本

| 用例 | 脚本 |
|---|---|
| 通过推理提供商对 Hub 模型进行本地 `inspect-ai` 评估 | `scripts/inspect_eval_uv.py` |
| 使用 `vllm` 或 Transformers 通过 `inspect-ai` 进行本地 GPU 评估 | `scripts/inspect_vllm_uv.py` |
| 使用 `vllm` 或 `accelerate` 通过 `lighteval` 进行本地 GPU 评估 | `scripts/lighteval_vllm_uv.py` |
| 额外命令模式 | `examples/USAGE_EXAMPLES.md` |

# 先决条件

- 优先使用 `uv run` 进行本地执行。
- 为 gated/私有模型设置 `HF_TOKEN`。
- 对于本地 GPU 运行，在开始前验证 GPU 访问：

```bash
uv --version
printenv HF_TOKEN >/dev/null
nvidia-smi
```

如果 `nvidia-smi` 不可用，请选择：
- 使用 `scripts/inspect_eval_uv.py` 进行更轻量级的提供商支持的评估，或
- 如果用户需要远程计算，交给 `hugging-face-jobs` 技能。

# 核心工作流程

1. 选择评估框架。
   - 当您需要明确的任务控制和 inspect 原生流程时，使用 `inspect-ai`。
   - 当基准测试自然地表示为 lighteval 任务字符串时，尤其是排行榜样式的任务，使用 `lighteval`。
2. 选择推理后端。
   - 对于支持的架构，优先使用 `vllm` 以获得吞吐量。
   - 使用 Hugging Face Transformers (`--backend hf`) 或 `accelerate` 作为兼容性回退。
3. 从冒烟测试开始。
   - `inspect-ai`：添加 `--limit 10` 或类似参数。
   - `lighteval`：添加 `--max-samples 10`。
4. 仅在冒烟测试通过后扩大规模。
5. 如果用户需要远程执行，使用相同的脚本 + 参数交给 `hugging-face-jobs`。

# 快速开始

## 选项 A：使用本地推理提供商路径的 inspect-ai

当模型已经被 Hugging Face 推理提供商支持，并且您希望本地设置开销最小时最佳。

```bash
uv run scripts/inspect_eval_uv.py \
  --model meta-llama/Llama-3.2-1B \
  --task mmlu \
  --limit 20
```

当以下情况时使用此路径：
- 您需要快速的本地冒烟测试
- 您不需要直接的 GPU 控制
- 任务已经存在于 `inspect-evals` 中

## 选项 B：本地 GPU 上的 inspect-ai

当您需要直接加载 Hub 模型、使用 `vllm` 或为不支持的架构回退到 Transformers 时最佳。

本地 GPU：

```bash
uv run scripts/inspect_vllm_uv.py \
  --model meta-llama/Llama-3.2-1B \
  --task gsm8k \
  --limit 20
```

Transformers 回退：

```bash
uv run scripts/inspect_vllm_uv.py \
  --model microsoft/phi-2 \
  --task mmlu \
  --backend hf \
  --trust-remote-code \
  --limit 20
```

## 选项 C：本地 GPU 上的 lighteval

当任务自然地表示为 `lighteval` 任务字符串时最佳，尤其是 Open LLM 排行榜样式的基准测试。

本地 GPU：

```bash
uv run scripts/lighteval_vllm_uv.py \
  --model meta-llama/Llama-3.2-3B-Instruct \
  --tasks "leaderboard|mmlu|5,leaderboard|gsm8k|5" \
  --max-samples 20 \
  --use-chat-template
```

`accelerate` 回退：

```bash
uv run scripts/lighteval_vllm_uv.py \
  --model microsoft/phi-2 \
  --tasks "leaderboard|mmlu|5" \
  --backend accelerate \
  --trust-remote-code \
  --max-samples 20
```

# 远程执行边界

此技能有意在**本地执行和后端选择**处停止。

如果用户希望：
- 在 Hugging Face Jobs 上运行这些脚本
- 选择远程硬件
- 向远程作业传递密钥
- 安排定期运行
- 检查 / 取消 / 监控作业

则切换到 **`hugging-face-jobs`** 技能，并将这些脚本之一及其选择的参数传递给它。

# 任务选择

`inspect-ai` 示例：
- `mmlu`
- `gsm8k`
- `hellaswag`
- `arc_challenge`
- `truthfulqa`
- `winogrande`
- `humaneval`

`lighteval` 任务字符串使用 `suite|task|num_fewshot`：
- `leaderboard|mmlu|5`
- `leaderboard|gsm8k|5`
- `leaderboard|arc_challenge|25`
- `lighteval|hellaswag|0`

多个 `lighteval` 任务可以在 `--tasks` 中用逗号分隔。

# 后端选择

- 对于支持的架构，优先使用 `inspect_vllm_uv.py --backend vllm` 进行快速 GPU 推理。
- 当 `vllm` 不支持模型时，使用 `inspect_vllm_uv.py --backend hf`。
- 对于支持的模型，优先使用 `lighteval_vllm_uv.py --backend vllm` 以获得吞吐量。
- 使用 `lighteval_vllm_uv.py --backend accelerate` 作为兼容性回退。
- 当推理提供商已经覆盖模型且您不需要直接 GPU 控制时，使用 `inspect_eval_uv.py`。

# 硬件指导

| 模型大小 | 建议的本地硬件 |
|---|---|
| `< 3B` | 消费级 GPU / Apple Silicon / 小型开发 GPU |
| `3B - 13B` | 更强的本地 GPU |
| `13B+` | 高内存本地 GPU 或交给 `hugging-face-jobs` |

对于冒烟测试，优先使用更便宜的本地运行加上 `--limit` 或 `--max-samples`。

# 故障排除

- CUDA 或 vLLM OOM：
  - 减少 `--batch-size`
  - 减少 `--gpu-memory-utilization`
  - 切换到较小的模型进行冒烟测试
  - 如有必要，交给 `hugging-face-jobs`
- 模型不被 `vllm` 支持：
  - 切换到 `--backend hf` 用于 `inspect-ai`
  - 切换到 `--backend accelerate` 用于 `lighteval`
- Gated/私有存储库访问失败：
  - 验证 `HF_TOKEN`
- 需要自定义模型代码：
  - 添加 `--trust-remote-code`

# 示例

请参阅：
- `examples/USAGE_EXAMPLES.md` 了解本地命令模式
- `scripts/inspect_eval_uv.py`
- `scripts/inspect_vllm_uv.py`
- `scripts/lighteval_vllm_uv.py`