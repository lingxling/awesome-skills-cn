---
name: huggingface-llm-trainer
description: 当用户想要在 Hugging Face Jobs 基础设施上使用 TRL（Transformer 强化学习）训练或微调语言模型时，应使用此技能。涵盖 SFT、DPO、GRPO 和奖励模型训练方法，以及用于本地部署的 GGUF 转换。包括 TRL Jobs 包、带有 PEP 723 格式的 UV 脚本、数据集准备和验证、硬件选择、成本估算、Trackio 监控、Hub 认证和模型持久化的指导。当涉及云 GPU 训练、GGUF 转换或用户提及在 Hugging Face Jobs 上训练而无需本地 GPU 设置时，应调用此技能。
license: 完整条款见 LICENSE.txt
---

# 在 Hugging Face Jobs 上进行 TRL 训练

## 概述

使用 TRL（Transformer 强化学习）在完全托管的 Hugging Face 基础设施上训练语言模型。无需本地 GPU 设置——模型在云 GPU 上训练，结果自动保存到 Hugging Face Hub。

**TRL 提供多种训练方法：**
- **SFT**（监督微调）- 标准指令调优
- **DPO**（直接偏好优化）- 来自偏好数据的对齐
- **GRPO**（组相对策略优化）- 在线 RL 训练
- **奖励模型** - 为 RLHF 训练奖励模型

**有关详细的 TRL 方法文档：**
```python
hf_doc_search("your query", product="trl")
hf_doc_fetch("https://huggingface.co/docs/trl/sft_trainer")  # SFT
hf_doc_fetch("https://huggingface.co/docs/trl/dpo_trainer")  # DPO
# 等等
```

**另请参阅：** `references/training_methods.md` 了解方法概述和选择指南

## 何时使用此技能

当用户想要：
- 在没有本地基础设施的情况下在云 GPU 上微调语言模型
- 使用 TRL 方法（SFT、DPO、GRPO 等）进行训练
- 在 Hugging Face Jobs 基础设施上运行训练作业
- 将训练的模型转换为 GGUF 以用于本地部署（Ollama、LM Studio、llama.cpp）
- 确保训练的模型永久保存到 Hub
- 使用具有优化默认值的现代工作流程

### 何时使用 Unsloth

当以下情况时，使用 **Unsloth**（`references/unsloth.md`）而不是标准 TRL：
- **有限的 GPU 内存** - Unsloth 使用约 60% 更少的 VRAM
- **速度重要** - Unsloth 速度快约 2 倍
- 训练 **大型模型 (>13B)** - 内存效率至关重要
- 训练 **视觉-语言模型 (VLM)** - Unsloth 支持 `FastVisionModel`

有关完整的 Unsloth 文档，请参阅 `references/unsloth.md`，有关生产就绪的训练脚本，请参阅 `scripts/unsloth_sft_example.py`。

## 关键指令

在协助训练作业时：

1. **始终使用 `hf_jobs()` MCP 工具** - 使用 `hf_jobs("uv", {...})` 提交作业，而不是 bash `trl-jobs` 命令。`script` 参数直接接受 Python 代码。除非用户明确要求，否则不要保存到本地文件。将脚本内容作为字符串传递给 `hf_jobs()`。如果用户要求"训练模型"、"微调"或类似请求，你必须创建训练脚本并立即使用 `hf_jobs()` 提交作业。

2. **始终包含 Trackio** - 每个训练脚本都应包含 Trackio 以进行实时监控。使用 `scripts/` 中的示例脚本作为模板。

3. **提交后提供作业详细信息** - 提交后，提供作业 ID、监控 URL、估计时间，并注意用户可以稍后请求状态检查。

4. **使用示例脚本作为模板** - 参考 `scripts/train_sft_example.py`、`scripts/train_dpo_example.py` 等作为起点。

## 本地脚本执行

仓库脚本使用 PEP 723 内联依赖。使用 `uv run` 运行它们：
```bash
uv run scripts/estimate_cost.py --help
uv run scripts/dataset_inspector.py --help
```

## 先决条件检查清单

在开始任何训练作业之前，验证：

### ✅ **账户和认证**
- 具有 [Pro](https://hf.co/pro)、[Team](https://hf.co/enterprise) 或 [Enterprise](https://hf.co/enterprise) 计划的 Hugging Face 账户（Jobs 需要付费计划）
- 已认证登录：使用 `hf_whoami()` 检查
- **用于 Hub 推送的 HF_TOKEN** ⚠️ 关键 - 训练环境是临时的，必须推送到 Hub，否则所有训练结果都会丢失
- 令牌必须具有写入权限
- **必须在作业配置中传递 `secrets={"HF_TOKEN": "$HF_TOKEN"}`** 以使令牌可用（`$HF_TOKEN` 语法引用您的实际令牌值）

### ✅ **数据集要求**
- 数据集必须存在于 Hub 上或可通过 `datasets.load_dataset()` 加载
- 格式必须与训练方法匹配（SFT："messages"/text/prompt-completion；DPO：chosen/rejected；GRPO：prompt-only）
- **在 GPU 训练前始终验证未知数据集** 以防止格式失败（见下文数据集验证部分）
- 大小适合硬件（演示：t4-small 上 50-100 个示例；生产：a10g-large/a100-large 上 1K-10K+）

### ⚠️ **关键设置**
- **超时必须超过预期训练时间** - 默认 30 分钟对于大多数训练来说太短。建议最小值：1-2 小时。如果超时，作业失败并丢失所有进度。
- **必须启用 Hub 推送** - 配置：`push_to_hub=True`，`hub_model_id="username/model-name"`；作业：`secrets={"HF_TOKEN": "$HF_TOKEN"}`

## 异步作业指南

**⚠️ 重要：训练作业异步运行，可能需要数小时**

### 所需操作

**当用户请求训练时：**
1. **创建包含 Trackio 的训练脚本**（使用 `scripts/train_sft_example.py` 作为模板）
2. **立即使用 `hf_jobs()` MCP 工具提交**，脚本内容内联 - 除非用户要求，否则不要保存到文件
3. **报告提交情况**，包括作业 ID、监控 URL 和估计时间
4. **等待用户** 请求状态检查 - 不要自动轮询

### 基本规则
- **作业在后台运行** - 提交立即返回；训练独立继续
- **初始日志延迟** - 日志可能需要 30-60 秒才会出现
- **用户检查状态** - 等待用户请求状态更新
- **避免轮询** - 仅在用户请求时检查日志；提供监控链接

### 提交后

**提供给用户：**
- ✅ 作业 ID 和监控 URL
- ✅ 预计完成时间
- ✅ Trackio 仪表板 URL
- ✅ 注意用户可以稍后请求状态检查

**示例响应：**
```
✅ 作业提交成功！

作业 ID: abc123xyz
监控: https://huggingface.co/jobs/username/abc123xyz

预计时间: ~2 小时
估计成本: ~$10

作业在后台运行。准备好时请让我检查状态/日志！
```

## 快速开始：三种方法

**💡 演示提示：** 对于在较小 GPU（t4-small）上的快速演示，省略 `eval_dataset` 和 `eval_strategy` 以节省约 40% 的内存。您仍会看到训练损失和学习进度。

### 序列长度配置

**TRL 配置类使用 `max_length`（不是 `max_seq_length`）** 来控制标记化序列长度：

```python
# ✅ 正确 - 如果需要设置序列长度
SFTConfig(max_length=512)   # 将序列截断为 512 个标记
DPOConfig(max_length=2048)  # 更长的上下文（2048 个标记）

# ❌ 错误 - 此参数不存在
SFTConfig(max_seq_length=512)  # 类型错误！
```

**默认行为：** `max_length=1024`（从右侧截断）。这对大多数训练效果良好。

**何时覆盖：**
- **更长的上下文**：设置更高（例如，`max_length=2048`）
- **内存约束**：设置更低（例如，`max_length=512`）
- **视觉模型**：设置 `max_length=None`（防止裁剪图像标记）

**通常您根本不需要设置此参数** - 下面的示例使用合理的默认值。

### 方法 1：UV 脚本（推荐—默认选择）

UV 脚本使用 PEP 723 内联依赖进行干净、自包含的训练。**这是 Claude Code 的主要方法。**

```python
hf_jobs("uv", {
    "script": """
# /// script
# dependencies = ["trl>=0.12.0", "peft>=0.7.0", "trackio"]
# ///

from datasets import load_dataset
from peft import LoraConfig
from trl import SFTTrainer, SFTConfig
import trackio

dataset = load_dataset("trl-lib/Capybara", split="train")

# 为监控创建训练/评估分割
dataset_split = dataset.train_test_split(test_size=0.1, seed=42)

trainer = SFTTrainer(
    model="Qwen/Qwen2.5-0.5B",
    train_dataset=dataset_split["train"],
    eval_dataset=dataset_split["test"],
    peft_config=LoraConfig(r=16, lora_alpha=32),
    args=SFTConfig(
        output_dir="my-model",
        push_to_hub=True,
        hub_model_id="username/my-model",
        num_train_epochs=3,
        eval_strategy="steps",
        eval_steps=50,
        report_to="trackio",
        project="meaningful_prject_name", # 训练名称的项目名称（trackio）
        run_name="meaningful_run_name",   # 特定训练运行的描述性名称（trackio）
    )
)

trainer.train()
trainer.push_to_hub()
""",
    "flavor": "a10g-large",
    "timeout": "2h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}
})
```

**优势：** 直接使用 MCP 工具，代码干净，依赖内联声明（PEP 723），无需保存文件，完全控制
**何时使用：** Claude Code 中所有训练任务的默认选择，自定义训练逻辑，任何需要 `hf_jobs()` 的场景

#### 使用脚本

⚠️ **重要：** `script` 参数接受内联代码（如上所示）或 URL。**本地文件路径不起作用。**

**为什么本地路径不起作用：**
作业在隔离的 Docker 容器中运行，无法访问您的本地文件系统。脚本必须是：
- 内联代码（推荐用于自定义训练）
- 可公开访问的 URL
- 私有仓库 URL（带 HF_TOKEN）

**常见错误：**
```python
# ❌ 这些都会失败
hf_jobs("uv", {"script": "train.py"})
hf_jobs("uv", {"script": "./scripts/train.py"})
hf_jobs("uv", {"script": "/path/to/train.py"})
```

**正确方法：**
```python
# ✅ 内联代码（推荐）
hf_jobs("uv", {"script": "# /// script\n# dependencies = [...]
# ///\n\n<your code>"})

# ✅ 从 Hugging Face Hub
hf_jobs("uv", {"script": "https://huggingface.co/user/repo/resolve/main/train.py"})

# ✅ 从 GitHub
hf_jobs("uv", {"script": "https://raw.githubusercontent.com/user/repo/main/train.py"})

# ✅ 从 Gist
hf_jobs("uv", {"script": "https://gist.githubusercontent.com/user/id/raw/train.py"})
```

**要使用本地脚本：** 首先上传到 HF Hub：
```bash
hf repos create my-training-scripts --type model
hf upload my-training-scripts ./train.py train.py
# 使用: https://huggingface.co/USERNAME/my-training-scripts/resolve/main/train.py
```

### 方法 2：TRL 维护的脚本（官方示例）

TRL 为所有方法提供经过实战测试的脚本。可以从 URL 运行：

```python
hf_jobs("uv", {
    "script": "https://github.com/huggingface/trl/blob/main/trl/scripts/sft.py",
    "script_args": [
        "--model_name_or_path", "Qwen/Qwen2.5-0.5B",
        "--dataset_name", "trl-lib/Capybara",
        "--output_dir", "my-model",
        "--push_to_hub",
        "--hub_model_id", "username/my-model"
    ],
    "flavor": "a10g-large",
    "timeout": "2h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}
})
```

**优势：** 无需编写代码，由 TRL 团队维护，经过生产测试
**何时使用：** 标准 TRL 训练，快速实验，不需要自定义代码
**可用：** 脚本可从 https://github.com/huggingface/trl/tree/main/examples/scripts 获取

### 在 Hub 上查找更多 UV 脚本

`uv-scripts` 组织在 Hugging Face Hub 上提供现成的 UV 脚本，存储为数据集：

```python
# 发现可用的 UV 脚本集合
dataset_search({"author": "uv-scripts", "sort": "downloads", "limit": 20})

# 浏览特定集合
hub_repo_details(["uv-scripts/classification"], repo_type="dataset", include_readme=True)
```

**流行集合：** ocr, classification, synthetic-data, vllm, dataset-creation

### 方法 3：HF Jobs CLI（直接终端命令）

当 `hf_jobs()` MCP 工具不可用时，直接使用 `hf jobs` CLI。

**⚠️ 关键：CLI 语法规则**

```bash
# ✅ 正确语法 - 标记在脚本 URL 之前
hf jobs uv run --flavor a10g-large --timeout 2h --secrets HF_TOKEN "https://example.com/train.py"

# ❌ 错误 - "run uv" 而不是 "uv run"
hf jobs run uv "https://example.com/train.py" --flavor a10g-large

# ❌ 错误 - 标记在脚本 URL 之后（将被忽略！）
hf jobs uv run "https://example.com/train.py" --flavor a10g-large

# ❌ 错误 - "--secret" 而不是 "--secrets"（复数）
hf jobs uv run --secret HF_TOKEN "https://example.com/train.py"
```

**关键语法规则：**
1. 命令顺序是 `hf jobs uv run`（不是 `hf jobs run uv`）
2. 所有标记（`--flavor`、`--timeout`、`--secrets`）必须在脚本 URL 之前
3. 使用 `--secrets`（复数），不是 `--secret`
4. 脚本 URL 必须是最后一个位置参数

**完整 CLI 示例：**
```bash
hf jobs uv run \
  --flavor a10g-large \
  --timeout 2h \
  --secrets HF_TOKEN \
  "https://huggingface.co/user/repo/resolve/main/train.py"
```

**通过 CLI 检查作业状态：**
```bash
hf jobs ps                        # 列出所有作业
hf jobs logs <job-id>             # 查看日志
hf jobs inspect <job-id>          # 作业详情
hf jobs cancel <job-id>           # 取消作业
```

### 方法 4：TRL Jobs 包（简化训练）

`trl-jobs` 包提供优化的默认值和一行式训练。

```bash
uvx trl-jobs sft \
  --model_name Qwen/Qwen2.5-0.5B \
  --dataset_name trl-lib/Capybara

```

**优势：** 预配置设置，自动 Trackio 集成，自动 Hub 推送，一行命令
**何时使用：** 用户直接在终端工作（不在 Claude Code 上下文中），快速本地实验
**仓库：** https://github.com/huggingface/trl-jobs

⚠️ **在 Claude Code 上下文中，当可用时，优先使用 `hf_jobs()` MCP 工具（方法 1）。**

## 硬件选择

| 模型大小 | 推荐硬件 | 成本（约/小时） | 用例 |
|------------|---------------------|------------------|----------|
| <1B 参数 | `t4-small` | ~$0.75 | 演示，仅快速测试，无评估步骤 |
| 1-3B 参数 | `t4-medium`, `l4x1` | ~$1.50-2.50 | 开发 |
| 3-7B 参数 | `a10g-small`, `a10g-large` | ~$3.50-5.00 | 生产训练 |
| 7-13B 参数 | `a10g-large`, `a100-large` | ~$5-10 | 大型模型（使用 LoRA） |
| 13B+ 参数 | `a100-large`, `a10g-largex2` | ~$10-20 | 非常大（使用 LoRA） |

**GPU 类型：** cpu-basic/upgrade/performance/xl, t4-small/medium, l4x1/x4, a10g-small/large/largex2/largex4, a100-large, h100/h100x8

**指南：**
- 对于 >7B 的模型使用 **LoRA/PEFT** 以减少内存
- 多 GPU 由 TRL/Accelerate 自动处理
- 从小型硬件开始测试

**参见：** `references/hardware_guide.md` 了解详细规格

## 关键：将结果保存到 Hub

**⚠️ 临时环境—必须推送到 Hub**

Jobs 环境是临时的。作业结束时所有文件都会被删除。如果模型未推送到 Hub，**所有训练都将丢失**。

### 所需配置

**在训练脚本/配置中：**
```python
SFTConfig(
    push_to_hub=True,
    hub_model_id="username/model-name",  # 必须指定
    hub_strategy="every_save",  # 可选：推送检查点
)
```

**在作业提交中：**
```python
{
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}  # 启用认证
}
```

### 验证清单

提交前：
- [ ] `push_to_hub=True` 在配置中设置
- [ ] `hub_model_id` 包含 username/repo-name
- [ ] `secrets` 参数包含 HF_TOKEN
- [ ] 用户对目标仓库有写入权限

**参见：** `references/hub_saving.md` 了解详细故障排除

## 超时管理

**⚠️ 默认：30 分钟—对训练来说太短**

### 设置超时

```python
{
    "timeout": "2h"   # 2 小时（格式："90m"、"2h"、"1.5h" 或秒作为整数）
}
```

### 超时指南

| 场景 | 推荐 | 注意 |
|----------|-------------|-------|
| 快速演示（50-100 个示例） | 10-30 分钟 | 验证设置 |
| 开发训练 | 1-2 小时 | 小型数据集 |
| 生产（3-7B 模型） | 4-6 小时 | 完整数据集 |
| 带 LoRA 的大型模型 | 3-6 小时 | 取决于数据集 |

**始终添加 20-30% 的缓冲区** 用于模型/数据集加载、检查点保存、Hub 推送操作和网络延迟。

**超时后：** 作业立即终止，所有未保存的进度丢失，必须从头开始重新启动

## 成本估算

**当使用已知参数规划作业时，提供成本估算。** 使用 `scripts/estimate_cost.py`：

```bash
uv run scripts/estimate_cost.py \
  --model meta-llama/Llama-2-7b-hf \
  --dataset trl-lib/Capybara \
  --hardware a10g-large \
  --dataset-size 16000 \
  --epochs 3
```

输出包括估计时间、成本、推荐超时（带缓冲区）和优化建议。

**何时提供：** 用户规划作业，询问成本/时间，选择硬件，作业运行时间 >1 小时或成本 >$5

## 示例训练脚本

**具有所有最佳实践的生产就绪模板：**

正确加载这些脚本：

- **`scripts/train_sft_example.py`** - 完整的 SFT 训练，带有 Trackio、LoRA、检查点
- **`scripts/train_dpo_example.py`** - 用于偏好学习的 DPO 训练
- **`scripts/train_grpo_example.py`** - 用于在线 RL 的 GRPO 训练

这些脚本展示了正确的 Hub 保存、Trackio 集成、检查点管理和优化参数。将它们的内容内联传递给 `hf_jobs()` 或用作自定义脚本的模板。

## 监控和跟踪

**Trackio** 提供实时指标可视化。有关完整设置指南，请参阅 `references/trackio_guide.md`。

**关键点：**
- 将 `trackio` 添加到依赖项
- 使用 `report_to="trackio" 和 run_name="meaningful_name"` 配置训练器

### Trackio 配置默认值

**除非用户指定，否则使用合理的默认值。** 当生成带有 Trackio 的训练脚本时：

**默认配置：**
- **空间 ID**：`{username}/trackio`（使用 "trackio" 作为默认空间名称）
- **运行命名**：除非另有说明，否则以用户可识别的方式命名运行（例如，描述任务、模型或目的）
- **配置**：保持最小 - 仅包括超参数和模型/数据集信息
- **项目名称**：使用项目名称将运行与特定项目关联

**用户覆盖：** 如果用户请求特定的 trackio 配置（自定义空间、运行命名、分组或附加配置），应用他们的偏好而不是默认值。

这对于管理具有相同配置的多个作业或保持训练脚本可移植性很有用。

有关完整文档，包括为实验分组运行，请参阅 `references/trackio_guide.md`。

### 检查作业状态

```python
# 列出所有作业
hf_jobs("ps")

# 检查特定作业
hf_jobs("inspect", {"job_id": "your-job-id"})

# 查看日志
hf_jobs("logs", {"job_id": "your-job-id"})
```

**记住：** 等待用户请求状态检查。避免重复轮询。

## 数据集验证

**在启动 GPU 训练之前验证数据集格式，以防止训练失败的 #1 原因：格式不匹配。**

### 为什么验证

- 50%+ 的训练失败是由于数据集格式问题
- DPO 特别严格：需要确切的列名（`prompt`、`chosen`、`rejected`）
- 失败的 GPU 作业浪费 $1-10 和 30-60 分钟
- 在 CPU 上验证成本约 $0.01，耗时 <1 分钟

### 何时验证

**始终验证：**
- 未知或自定义数据集
- DPO 训练（关键 - 90% 的数据集需要映射）
- 任何未明确兼容 TRL 的数据集

**跳过已知 TRL 数据集的验证：**
- `trl-lib/ultrachat_200k`、`trl-lib/Capybara`、`HuggingFaceH4/ultrachat_200k` 等

### 用法

```python
hf_jobs("uv", {
    "script": "https://huggingface.co/datasets/mcp-tools/skills/raw/main/dataset_inspector.py",
    "script_args": ["--dataset", "username/dataset-name", "--split", "train"]
})
```

脚本速度快，通常会同步完成。

### 阅读结果

输出显示每种训练方法的兼容性：

- **`✓ READY`** - 数据集兼容，直接使用
- **`✗ NEEDS MAPPING`** - 兼容但需要预处理（提供映射代码）
- **`✗ INCOMPATIBLE`** - 不能用于此方法

当需要映射时，输出包含带有可复制粘贴 Python 代码的 **"MAPPING CODE"** 部分。

### 示例工作流

```python
# 1. 检查数据集（成本约 $0.01，CPU 上 <1 分钟）
hf_jobs("uv", {
    "script": "https://huggingface.co/datasets/mcp-tools/skills/raw/main/dataset_inspector.py",
    "script_args": ["--dataset", "argilla/distilabel-math-preference-dpo", "--split", "train"]
})

# 2. 检查输出标记：
#    ✓ READY → 继续训练
#    ✗ NEEDS MAPPING → 应用下面的映射代码
#    ✗ INCOMPATIBLE → 选择不同的方法/数据集

# 3. 如果需要映射，在训练前应用：
def format_for_dpo(example):
    return {
        'prompt': example['instruction'],
        'chosen': example['chosen_response'],
        'rejected': example['rejected_response'],
    }
dataset = dataset.map(format_for_dpo, remove_columns=dataset.column_names)

# 4. 自信地启动训练作业
```

### 常见场景：DPO 格式不匹配

大多数 DPO 数据集使用非标准列名。示例：

```
数据集有：instruction, chosen_response, rejected_response
DPO 期望：prompt, chosen, rejected
```

验证器检测到这一点并提供确切的映射代码来修复它。

## 将模型转换为 GGUF

训练后，将模型转换为 **GGUF 格式**，用于 llama.cpp、Ollama、LM Studio 和其他本地推理工具。

**什么是 GGUF：**
- 为 llama.cpp 的 CPU/GPU 推理优化
- 支持量化（4 位、5 位、8 位）以减少模型大小
- 与 Ollama、LM Studio、Jan、GPT4All、llama.cpp 兼容
- 7B 模型通常为 2-8GB（vs 未量化的 14GB）

**何时转换：**
- 使用 Ollama 或 LM Studio 在本地运行模型
- 通过量化减少模型大小
- 部署到边缘设备
- 分享用于本地优先使用的模型

**参见：** `references/gguf_conversion.md` 了解完整的转换指南，包括生产就绪的转换脚本、量化选项、硬件要求、使用示例和故障排除。

**快速转换：**
```python
hf_jobs("uv", {
    "script": "<参见 references/gguf_conversion.md 获取完整脚本>",
    "flavor": "a10g-large",
    "timeout": "45m",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"},
    "env": {
        "ADAPTER_MODEL": "username/my-finetuned-model",
        "BASE_MODEL": "Qwen/Qwen2.5-0.5B",
        "OUTPUT_REPO": "username/my-model-gguf"
    }
})
```

## 常见训练模式

有关详细示例，请参阅 `references/training_patterns.md`，包括：
- 快速演示（5-10 分钟）
- 带检查点的生产
- 多 GPU 训练
- DPO 训练（偏好学习）
- GRPO 训练（在线 RL）

## 常见失败模式

### 内存不足 (OOM)

**修复（按顺序尝试）：**
1. 减少批处理大小：`per_device_train_batch_size=1`，增加 `gradient_accumulation_steps=8`。有效批处理大小为 `per_device_train_batch_size` x `gradient_accumulation_steps`。为获得最佳性能，保持有效批处理大小接近 128。
2. 启用：`gradient_checkpointing=True`
3. 升级硬件：t4-small → l4x1, a10g-small → a10g-large 等

### 数据集格式错误

**修复：**
1. 首先使用数据集检查器验证：
   ```bash
   uv run https://huggingface.co/datasets/mcp-tools/skills/raw/main/dataset_inspector.py \
     --dataset name --split train
   ```
2. 检查输出的兼容性标记（✓ READY, ✗ NEEDS MAPPING, ✗ INCOMPATIBLE）
3. 如果需要，应用检查器输出中的映射代码

### 作业超时

**修复：**
1. 检查实际运行时间的日志：`hf_jobs("logs", {"job_id": "..."})`
2. 增加超时并添加缓冲区：`"timeout": "3h"`（在估计时间上增加 30%）
3. 或减少训练：降低 `num_train_epochs`，使用更小的数据集，启用 `max_steps`
4. 保存检查点：`save_strategy="steps"`，`save_steps=500`，`hub_strategy="every_save"`

**注意：** 默认 30 分钟对实际训练来说是不够的。最少 1-2 小时。

### Hub 推送失败

**修复：**
1. 添加到作业：`secrets={"HF_TOKEN": "$HF_TOKEN"}`
2. 添加到配置：`push_to_hub=True`，`hub_model_id="username/model-name"`
3. 验证认证：`mcp__huggingface__hf_whoami()`
4. 检查令牌是否有写入权限，仓库是否存在（或设置 `hub_private_repo=True`）

### 缺少依赖项

**修复：**
添加到 PEP 723 头部：
```python
# /// script
# dependencies = ["trl>=0.12.0", "peft>=0.7.0", "trackio", "missing-package"]
# ///
```

## 故障排除

**常见问题：**
- 作业超时 → 增加超时，减少轮数/数据集，使用更小的模型/LoRA
- 模型未保存到 Hub → 检查 push_to_hub=True，hub_model_id，secrets=HF_TOKEN
- 内存不足 (OOM) → 减少批处理大小，增加梯度累积，启用 LoRA，使用更大的 GPU
- 数据集格式错误 → 使用数据集检查器验证（见数据集验证部分）
- 导入/模块错误 → 添加带有依赖项的 PEP 723 头部，验证格式
- 认证错误 → 检查 `mcp__huggingface__hf_whoami()`，令牌权限，secrets 参数

**参见：** `references/troubleshooting.md` 了解完整的故障排除指南

## 资源

### 参考（在此技能中）
- `references/training_methods.md` - SFT、DPO、GRPO、KTO、PPO、奖励模型的概述
- `references/training_patterns.md` - 常见训练模式和示例
- `references/unsloth.md` - 用于快速 VLM 训练的 Unsloth（速度快 2 倍，VRAM 少 60%）
- `references/gguf_conversion.md` - 完整的 GGUF 转换指南
- `references/trackio_guide.md` - Trackio 监控设置
- `references/hardware_guide.md` - 硬件规格和选择
- `references/hub_saving.md` - Hub 认证故障排除
- `references/troubleshooting.md` - 常见问题和解决方案
- `references/local_training_macos.md` - 在 macOS 上本地训练

### 脚本（在此技能中）
- `scripts/train_sft_example.py` - 生产 SFT 模板
- `scripts/train_dpo_example.py` - 生产 DPO 模板
- `scripts/train_grpo_example.py` - 生产 GRPO 模板
- `scripts/unsloth_sft_example.py` - Unsloth 文本 LLM 训练模板（更快，更少 VRAM）
- `scripts/estimate_cost.py` - 估计时间和成本（在适当情况下提供）
- `scripts/convert_to_gguf.py` - 完整的 GGUF 转换脚本

### 外部脚本
- [数据集检查器](https://huggingface.co/datasets/mcp-tools/skills/raw/main/dataset_inspector.py) - 在训练前验证数据集格式（通过 `uv run` 或 `hf_jobs` 使用）

### 外部链接
- [TRL 文档](https://huggingface.co/docs/trl)
- [TRL Jobs 训练指南](https://huggingface.co/docs/trl/en/jobs_training)
- [TRL Jobs 包](https://github.com/huggingface/trl-jobs)
- [HF Jobs 文档](https://huggingface.co/docs/huggingface_hub/guides/jobs)
- [TRL 示例脚本](https://github.com/huggingface/trl/tree/main/examples/scripts)
- [UV 脚本指南](https://docs.astral.sh/uv/guides/scripts/)
- [UV 脚本组织](https://huggingface.co/uv-scripts)

## 关键要点

1. **内联提交脚本** - `script` 参数直接接受 Python 代码；除非用户要求，否则无需保存文件
2. **作业是异步的** - 不要等待/轮询；让用户在准备好时检查
3. **始终设置超时** - 默认 30 分钟不足；推荐最少 1-2 小时
4. **始终启用 Hub 推送** - 环境是临时的；没有推送，所有结果都将丢失
5. **包含 Trackio** - 使用示例脚本作为实时监控的模板
6. **提供成本估算** - 当参数已知时，使用 `scripts/estimate_cost.py`
7. **使用 UV 脚本（方法 1）** - 默认为带有内联脚本的 `hf_jobs("uv", {...})`；标准训练使用 TRL 维护的脚本；在 Claude Code 中避免使用 bash `trl-jobs` 命令
8. **使用 hf_doc_fetch/hf_doc_search** 获取最新的 TRL 文档
9. **在训练前验证数据集格式** 使用数据集检查器（见数据集验证部分）
10. **选择适合模型大小的硬件**；对 >7B 的模型使用 LoRA