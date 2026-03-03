---
name: hugging-face-evaluation
description: 在 Hugging Face 模型卡片中添加和管理评估结果。支持从 README 内容中提取评估表、从 Artificial Analysis API 导入分数,以及使用 vLLM/lighteval 运行自定义模型评估。与 model-index 元数据格式兼容。
---

# 概述
此技能提供工具来向 Hugging Face 模型卡片添加结构化的评估结果。它支持多种添加评估数据的方法:
- 从 README 内容中提取现有评估表
- 从 Artificial Analysis 导入基准测试分数
- 使用 vLLM 或 accelerate 后端(lighteval/inspect-ai)运行自定义模型评估

## 与 HF 生态系统的集成
- **模型卡片**: 更新 model-index 元数据以进行排行榜集成
- **Artificial Analysis**: 直接 API 集成以进行基准测试导入
- **Papers with Code**: 与其 model-index 规范兼容
- **Jobs**: 使用 `uv` 集成直接在 Hugging Face Jobs 上运行评估
- **vLLM**: 用于自定义模型评估的高效 GPU 推理
- **lighteval**: HuggingFace 的评估库,具有 vLLM/accelerate 后端
- **inspect-ai**: 英国 AI 安全研究所的评估框架

# 版本
1.3.0

# 依赖项

## 核心依赖项
- huggingface_hub>=0.26.0
- markdown-it-py>=3.0.0
- python-dotenv>=1.2.1
- pyyaml>=6.0.3
- requests>=2.32.5
- re(内置)

## 推理提供商评估
- inspect-ai>=0.3.0
- inspect-evals
- openai

## vLLM 自定义模型评估(需要 GPU)
- lighteval[accelerate,vllm]>=0.6.0
- vllm>=0.4.0
- torch>=2.0.0
- transformers>=4.40.0
- accelerate>=0.30.0

注意: 使用 `uv run` 时,通过 PEP 723 脚本标头自动安装 vLLM 依赖项。

# 重要: 使用此技能

## ⚠️ 关键: 在创建新 PR 之前检查现有 PR

**在使用 `--create-pr` 创建任何拉取请求之前,您必须检查现有的开放 PR:**

```bash
uv run scripts/evaluation_manager.py get-prs --repo-id "username/model-name"
```

**如果存在开放 PR:**
1. **不要创建新 PR** - 这会为维护者创建重复工作
2. **警告用户** 已存在开放 PR
3. **向用户显示** 现有 PR URL 以便他们可以查看
4. 仅当用户明确确认他们想要创建另一个 PR 时才继续

这可以防止使用重复的评估 PR 垃圾邮件模型存储库。

---
> **所有路径都是相对于包含此 SKILL.md 文件的目录。**
> 在运行任何脚本之前,首先 `cd` 到该目录或使用完整路径。


**使用 `--help` 获取最新的工作流程指南。** 适用于普通 Python 或 `uv run`:
```bash
uv run scripts/evaluation_manager.py --help
uv run scripts/evaluation_manager.py inspect-tables --help
uv run scripts/evaluation_manager.py extract-readme --help
```
关键工作流程(匹配 CLI 帮助):

1) `get-prs` → 首先检查现有开放 PR
2) `inspect-tables` → 查找表编号/列
3) `extract-readme --table N` → 默认打印 YAML
4) 添加 `--apply`(推送)或 `--create-pr` 以写入更改

# 核心功能

## 1. 检查和从 README 提取评估表
- **检查表**: 使用 `inspect-tables` 查看 README 中的所有表及其结构、列和示例行
- **解析 Markdown 表**: 使用 markdown-it-py 准确解析(忽略代码块和示例)
- **表选择**: 使用 `--table N` 从特定表提取(当存在多个表时需要)
- **格式检测**: 识别常见格式(基准测试作为行、列或具有多个模型的比较表)
- **列匹配**: 自动识别模型列/行;首选 `--model-column-index`(从检查输出的索引)。仅在列标题文本完全匹配时使用 `--model-name-override`。
- **YAML 生成**: 将选定的表转换为 model-index YAML 格式
- **任务类型**: `--task-type` 在 model-index 输出中设置 `task.type` 字段(例如,`text-generation`、`summarization`)

## 2. 从 Artificial Analysis 导入
- **API 集成**: 直接从 Artificial Analysis 获取基准测试分数
- **自动格式化**: 将 API 响应转换为 model-index 格式
- **元数据保留**: 维护源归属和 URL
- **PR 创建**: 使用评估更新自动创建拉取请求

## 3. Model-Index 管理
- **YAML 生成**: 创建正确格式的 model-index 条目
- **合并支持**: 将评估添加到现有模型卡片而不覆盖
- **验证**: 确保符合 Papers with Code 规范
- **批处理操作**: 高效处理多个模型

## 4. 在 HF Jobs 上运行评估(推理提供商)
- **Inspect-AI 集成**: 使用 `inspect-ai` 库运行标准评估
- **UV 集成**: 在 HF 基础设施上无缝运行具有临时依赖项的 Python 脚本
- **零配置**: 无需 Dockerfiles 或 Space 管理
- **硬件选择**: 为评估作业配置 CPU 或 GPU 硬件
- **安全执行**: 通过 CLI 传递的机密安全处理 API 令牌

## 5. 使用 vLLM 运行自定义模型评估(新增)

⚠️ **重要:** 此方法仅在安装了 `uv` 且具有足够 GPU 内存的设备上才可能。
**优点:** 无需使用 `hf_jobs()` MCP 工具,可以直接在终端中运行脚本
**何时使用:** 用户直接在本地设备上工作时,当 GPU 可用时

### 运行脚本之前

- 检查脚本路径
- 检查是否安装了 uv
- 使用 `nvidia-smi` 检查 gpu 是否可用

### 运行脚本

```bash
uv run scripts/train_sft_example.py
```
### 功能

- **vLLM 后端**: 高性能 GPU 推理(比标准 HF 方法快 5-10 倍)
- **lighteval 框架**: HuggingFace 的评估库,具有 Open LLM 排行榜任务
- **inspect-ai 框架**: 英国 AI 安全研究所的评估库
- **独立或 Jobs**: 本地运行或提交到 HF Jobs 基础设施

# 使用说明

该技能在 `scripts/` 中包含用于执行操作的 Python 脚本。

### 先决条件
- 首选: 使用 `uv run`(PEP 723 标头自动安装依赖项)
- 或手动安装: `pip install huggingface-hub markdown-it-py python-dotenv pyyaml requests`
- 设置 `HF_TOKEN` 环境变量,使用写访问令牌
- 对于 Artificial Analysis: 设置 `AA_API_KEY` 环境变量
- 如果安装了 `python-dotenv`,`.env` 会自动加载

### 方法 1: 从 README 提取(CLI 工作流程)

推荐流程(匹配 `--help`):
```bash
# 1) 检查表以获取表编号和列提示
uv run scripts/evaluation_manager.py inspect-tables --repo-id "username/model"

# 2) 提取特定表(默认打印 YAML)
uv run scripts/evaluation_manager.py extract-readme \
  --repo-id "username/model" \
  --table 1 \
  [--model-column-index <inspect-tables 显示的列索引>] \
  [--model-name-override "<列标题/模型名称>"]  # 如果无法使用索引,请使用精确的列标题文本

# 3) 应用更改(推送或 PR)
uv run scripts/evaluation_manager.py extract-readme \
  --repo-id "username/model" \
  --table 1 \
  --apply       # 直接推送
# 或
uv run scripts/evaluation_manager.py extract-readme \
  --repo-id "username/model" \
  --table 1 \
  --create-pr   # 打开 PR
```

验证检查表:
- 默认打印 YAML;在应用之前与 README 表进行比较。
- 首选 `--model-column-index`;如果使用 `--model-name-override`,列标题文本必须完全匹配。
- 对于转置表(模型作为行),确保只提取一行。

### 方法 2: 从 Artificial Analysis 导入

从 Artificial Analysis API 获取基准测试分数并将它们添加到模型卡片。

**基本用法:**
```bash
AA_API_KEY="your-api-key" uv run scripts/evaluation_manager.py import-aa \
  --creator-slug "anthropic" \
  --model-name "claude-sonnet-4" \
  --repo-id "username/model-name"
```

**使用环境文件:**
```bash
# 创建 .env 文件
echo "AA_API_KEY=your-api-key" >> .env
echo "HF_TOKEN=your-hf-token" >> .env

# 运行导入
uv run scripts/evaluation_manager.py import-aa \
  --creator-slug "anthropic" \
  --model-name "claude-sonnet-4" \
  --repo-id "username/model-name"
```

**创建拉取请求:**
```bash
uv run scripts/evaluation_manager.py import-aa \
  --creator-slug "anthropic" \
  --model-name "claude-sonnet-4" \
  --repo-id "username/model-name" \
  --create-pr
```

### 方法 3: 运行评估作业

使用 `hf jobs uv run` CLI 在 Hugging Face 基础设施上提交评估作业。

**直接 CLI 用法:**
```bash
HF_TOKEN=$HF_TOKEN \
hf jobs uv run hf-evaluation/scripts/inspect_eval_uv.py \
  --flavor cpu-basic \
  --secret HF_TOKEN=$HF_TOKEN \
  -- --model "meta-llama/Llama-2-7b-hf" \
     --task "mmlu"
```

**GPU 示例(A10G):**
```bash
HF_TOKEN=$HF_TOKEN \
hf jobs uv run hf-evaluation/scripts/inspect_eval_uv.py \
  --flavor a10g-small \
  --secret HF_TOKEN=$HF_TOKEN \
  -- --model "meta-llama/Llama-2-7b-hf" \
     --task "gsm8k"
```

**Python 帮助器(可选):**
```bash
uv run scripts/run_eval_job.py \
  --model "meta-llama/Llama-2-7b-hf" \
  --task "mmlu" \
  --hardware "t4-small"
```

### 方法 4: 使用 vLLM 运行自定义模型评估

使用 vLLM 或 accelerate 后端直接在 GPU 上评估自定义 HuggingFace 模型。这些脚本与推理提供商脚本是**分开的**,并在作业的硬件上本地运行模型。

#### 何时使用 vLLM 评估(与推理提供商相比)

| 功能 | vLLM 脚本 | 推理提供商脚本 |
|---------|-------------|---------------------------|
| 模型访问 | 任何 HF 模型 | 具有 API 端点的模型 |
| 硬件 | 您的 GPU(或 HF Jobs GPU) | 提供商的基础设施 |
| 成本 | HF Jobs 计算成本 | API 使用费用 |
| 速度 | vLLM 优化 | 取决于提供商 |
| 离线 | 是(下载后) | 否 |

#### 选项 A: 使用 vLLM 后端的 lighteval

lighteval 是 HuggingFace 的评估库,支持 Open LLM 排行榜任务。

**独立(本地 GPU):**
```bash
# 使用 vLLM 运行 MMLU 5-shot
uv run scripts/lighteval_vllm_uv.py \
  --model meta-llama/Llama-3.2-1B \
  --tasks "leaderboard|mmlu|5"

# 运行多个任务
uv run scripts/lighteval_vllm_uv.py \
  --model meta-llama/Llama-3.2-1B \
  --tasks "leaderboard|mmlu|5,leaderboard|gsm8k|5"

# 使用 accelerate 后端代替 vLLM
uv run scripts/lighteval_vllm_uv.py \
  --model meta-llama/Llama-3.2-1B \
  --tasks "leaderboard|mmlu|5" \
  --backend accelerate

# 聊天/指令调整模型
uv run scripts/lighteval_vllm_uv.py \
  --model meta-llama/Llama-3.2-1B-Instruct \
  --tasks "leaderboard|mmlu|5" \
  --use-chat-template
```

**通过 HF Jobs:**
```bash
hf jobs uv run scripts/lighteval_vllm_uv.py \
  --flavor a10g-small \
  --secrets HF_TOKEN=$HF_TOKEN \
  -- --model meta-llama/Llama-3.2-1B \
     --tasks "leaderboard|mmlu|5"
```

**lighteval 任务格式:**
任务使用格式 `suite|task|num_fewshot`:
- `leaderboard|mmlu|5` - 带有 5-shot 的 MMLU
- `leaderboard|gsm8k|5` - 带有 5-shot 的 GSM8K
- `lighteval|hellaswag|0` - HellaSwag zero-shot
- `leaderboard|arc_challenge|25` - 带有 25-shot 的 ARC-Challenge

**查找可用任务:**
可用 lighteval 任务的完整列表可在以下位置找到:
https://github.com/huggingface/lighteval/blob/main/examples/tasks/all_tasks.txt

此文件包含所有支持的任务,格式为 `suite|task|num_fewshot|0`(尾随的 `0` 是版本标志,可以忽略)。常见套件包括:
- `leaderboard` - Open LLM 排行榜任务(MMLU、GSM8K、ARC、HellaSwag 等)
- `lighteval` - 额外的 lighteval 任务
- `bigbench` - BigBench 任务
- `original` - 原始基准测试任务

要从列表中使用任务,提取 `suite|task|num_fewshot` 部分(不带尾随的 `0`)并将其传递给 `--tasks` 参数。例如:
- 从文件: `leaderboard|mmlu|0` → 使用: `leaderboard|mmlu|0`(或更改为 `5` 以进行 5-shot)
- 从文件: `bigbench|abstract_narrative_understanding|0` → 使用: `bigbench|abstract_narrative_understanding|0`
- 从文件: `lighteval|wmt14:hi-en|0` → 使用: `lighteval|wmt14:hi-en|0`

可以指定多个任务为逗号分隔的值: `--tasks "leaderboard|mmlu|5,leaderboard|gsm8k|5"`

#### 选项 B: 使用 vLLM 后端的 inspect-ai

inspect-ai 是英国 AI 安全研究所的评估框架。

**独立(本地 GPU):**
```bash
# 使用 vLLM 运行 MMLU
uv run scripts/inspect_vllm_uv.py \
  --model meta-llama/Llama-3.2-1B \
  --task mmlu

# 使用 HuggingFace Transformers 后端
uv run scripts/inspect_vllm_uv.py \
  --model meta-llama/Llama-3.2-1B \
  --task mmlu \
  --backend hf

# 使用张量并行进行多 GPU
uv run scripts/inspect_vllm_uv.py \
  --model meta-llama/Llama-3.2-70B \
  --task mmlu \
  --tensor-parallel-size 4
```

**通过 HF Jobs:**
```bash
hf jobs uv run scripts/inspect_vllm_uv.py \
  --flavor a10g-small \
  --secrets HF_TOKEN=$HF_TOKEN \
  -- --model meta-llama/Llama-3.2-1B \
     --task mmlu
```

**可用的 inspect-ai 任务:**
- `mmlu` - 大规模多任务语言理解
- `gsm8k` - 小学数学
- `hellaswag` - 常识推理
- `arc_challenge` - AI2 推理挑战
- `truthfulqa` - TruthfulQA 基准测试
- `winogrande` - Winograd 模式挑战
- `humaneval` - 代码生成

#### 选项 C: Python 帮助器脚本

帮助器脚本自动选择硬件并简化作业提交:

```bash
# 基于模型大小自动检测硬件
uv run scripts/run_vllm_eval_job.py \
  --model meta-llama/Llama-3.2-1B \
  --task "leaderboard|mmlu|5" \
  --framework lighteval

# 显式硬件选择
uv run scripts/run_vllm_eval_job.py \
  --model meta-llama/Llama-3.2-70B \
  --task mmlu \
  --framework inspect \
  --hardware a100-large \
  --tensor-parallel-size 4

# 使用 HF Transformers 后端
uv run scripts/run_vllm_eval_job.py \
  --model microsoft/phi-2 \
  --task mmlu \
  --framework inspect \
  --backend hf
```

**硬件推荐:**
| 模型大小 | 推荐硬件 |
|------------|---------------------|
| < 3B 参数 | `t4-small` |
| 3B - 13B | `a10g-small` |
| 13B - 34B | `a10g-large` |
| 34B+ | `a100-large` |

### 命令参考

**顶级帮助和版本:**
```bash
uv run scripts/evaluation_manager.py --help
uv run scripts/evaluation_manager.py --version
```

**检查表(从这里开始):**
```bash
uv run scripts/evaluation_manager.py inspect-tables --repo-id "username/model-name"
```

**从 README 提取:**
```bash
uv run scripts/evaluation_manager.py extract-readme \
  --repo-id "username/model-name" \
  --table N \
  [--model-column-index N] \
  [--model-name-override "精确的列标题或模型名称"] \
  [--task-type "text-generation"] \
  [--dataset-name "Custom Benchmarks"] \
  [--apply | --create-pr]
```

**从 Artificial Analysis 导入:**
```bash
AA_API_KEY=... uv run scripts/evaluation_manager.py import-aa \
  --creator-slug "creator-name" \
  --model-name "model-slug" \
  --repo-id "username/model-name" \
  [--create-pr]
```

**查看/验证:**
```bash
uv run scripts/evaluation_manager.py show --repo-id "username/model-name"
uv run scripts/evaluation_manager.py validate --repo-id "username/model-name"
```

**检查开放 PR(在 --create-pr 之前始终运行):**
```bash
uv run scripts/evaluation_manager.py get-prs --repo-id "username/model-name"
```
列出模型存储库的所有开放拉取请求。显示 PR 编号、标题、作者、日期和 URL。

**运行评估作业(推理提供商):**
```bash
hf jobs uv run scripts/inspect_eval_uv.py \
  --flavor "cpu-basic|t4-small|..." \
  --secret HF_TOKEN=$HF_TOKEN \
  -- --model "model-id" \
     --task "task-name"
```

或使用 Python 帮助器:

```bash
uv run scripts/run_eval_job.py \
  --model "model-id" \
  --task "task-name" \
  --hardware "cpu-basic|t4-small|..."
```

**运行 vLLM 评估(自定义模型):**
```bash
# 使用 vLLM 的 lighteval
hf jobs uv run scripts/lighteval_vllm_uv.py \
  --flavor "a10g-small" \
  --secrets HF_TOKEN=$HF_TOKEN \
  -- --model "model-id" \
     --tasks "leaderboard|mmlu|5"

# 使用 vLLM 的 inspect-ai
hf jobs uv run scripts/inspect_vllm_uv.py \
  --flavor "a10g-small" \
  --secrets HF_TOKEN=$HF_TOKEN \
  -- --model "model-id" \
     --task "mmlu"

# 帮助器脚本(自动硬件选择)
uv run scripts/run_vllm_eval_job.py \
  --model "model-id" \
  --task "leaderboard|mmlu|5" \
  --framework lighteval
```

### Model-Index 格式

生成的 model-index 遵循此结构:

```yaml
model-index:
  - name: Model Name
    results:
      - task:
          type: text-generation
        dataset:
          name: Benchmark Dataset
          type: benchmark_type
        metrics:
          - name: MMLU
            type: mmlu
            value: 85.2
          - name: HumanEval
            type: humaneval
            value: 72.5
        source:
          name: Source Name
          url: https://source-url.com
```

警告: 不要在模型名称中使用 markdown 格式。使用表中的精确名称。仅在 source.url 字段中使用 URL。

### 错误处理
- **表未找到**: 脚本将报告是否未检测到评估表
- **无效格式**: 格式错误的表的清晰错误消息
- **API 错误**: 瞬态 Artificial Analysis API 失败的重试逻辑
- **令牌问题**: 尝试更新之前的验证
- **合并冲突**: 添加新条目时保留现有 model-index 条目
- **Space 创建**: 优雅地处理命名冲突和硬件请求失败

### 最佳实践

1. **首先检查现有 PR**: 在创建任何新 PR 之前运行 `get-prs` 以避免重复
2. **始终从 `inspect-tables` 开始**: 查看表结构并获取正确的提取命令
3. **使用 `--help` 获取指导**: 运行 `inspect-tables --help` 以查看完整的工作流程
4. **首先预览**: 默认行为打印 YAML;在使用 `--apply` 或 `--create-pr` 之前进行审查
5. **验证提取的值**: 手动将 YAML 输出与 README 表进行比较
6. **对于多表 README 使用 `--table N`**: 当存在多个评估表时需要
7. **对于比较表使用 `--model-name-override`**: 从 `inspect-tables` 输出中复制精确的列标题
8. **为其他人创建 PR**: 在更新您不拥有的模型时使用 `--create-pr`
9. **每个存储库一个模型**: 仅将主模型的结果添加到 model-index
10. **YAML 名称中无 markdown**: YAML 中的模型名称字段应该是纯文本

### 模型名称匹配

当提取具有多个模型(作为列或行)的评估表时,脚本使用 **精确的规范化令牌匹配**:

- 删除 markdown 格式(粗体 `**`、链接 `[]()` )
- 规范化名称(小写,用空格替换 `-` 和 `_`)
- 比较令牌集: `"OLMo-3-32B"` → `{"olmo", "3", "32b"}` 匹配 `"**Olmo 3 32B**"` 或 `"[Olmo-3-32B](...)"`
- 仅在令牌完全匹配时提取(处理不同的单词顺序和分隔符)
- 如果未找到精确匹配则失败(而不是从相似的名称猜测)

**对于基于列的表**(基准测试作为行,模型作为列):
- 查找与模型名称匹配的列标题
- 仅从该列提取分数

**对于转置表**(模型作为行,基准测试作为列):
- 在第一列中查找与模型名称匹配的行
- 仅从该行提取所有基准测试分数

这确保只提取正确模型的分数,从不提取不相关的模型或训练检查点。

### 常见模式

**更新您自己的模型:**
```bash
# 从 README 提取并直接推送
uv run scripts/evaluation_manager.py extract-readme \
  --repo-id "your-username/your-model" \
  --task-type "text-generation"
```

**更新其他人的模型(完整工作流程):**
```bash
# 步骤 1: 始终首先检查现有 PR
uv run scripts/evaluation_manager.py get-prs \
  --repo-id "other-username/their-model"

# 步骤 2: 如果不存在开放 PR,则继续创建一个
uv run scripts/evaluation_manager.py extract-readme \
  --repo-id "other-username/their-model" \
  --create-pr

# 如果存在开放 PR:
# - 警告用户有关现有 PR
# - 向他们显示 PR URL
# - 除非用户明确确认,否则不要创建新 PR
```

**导入新基准测试:**
```bash
# 步骤 1: 检查现有 PR
uv run scripts/evaluation_manager.py get-prs \
  --repo-id "anthropic/claude-sonnet-4"

# 步骤 2: 如果没有 PR,则从 Artificial Analysis 导入
AA_API_KEY=... uv run scripts/evaluation_manager.py import-aa \
  --creator-slug "anthropic" \
  --model-name "claude-sonnet-4" \
  --repo-id "anthropic/claude-sonnet-4" \
  --create-pr
```

### 故障排除

**问题**: "README 中未找到评估表"
- **解决方案**: 检查 README 是否包含带有数字分数的 markdown 表

**问题**: "在转置表中未找到模型 'X'"
- **解决方案**: 脚本将显示可用的模型。使用 `--model-name-override` 和列表中的精确名称
- **示例**: `--model-name-override "**Olmo 3-32B**"`

**问题**: "未设置 AA_API_KEY"
- **解决方案**: 设置环境变量或添加到 .env 文件

**问题**: "令牌没有写访问权限"
- **解决方案**: 确保 HF_TOKEN 对存储库具有写权限

**问题**: "在 Artificial Analysis 中未找到模型"
- **解决方案**: 验证 creator-slug 和 model-name 与 API 值匹配

**问题**: "硬件需要付费"
- **解决方案**: 向您的 Hugging Face 帐户添加付款方式以使用非 CPU 硬件

**问题**: "vLLM 内存不足"或 CUDA OOM
- **解决方案**: 使用更大的硬件类型,减少 `--gpu-memory-utilization`,或使用 `--tensor-parallel-size` 进行多 GPU

**问题**: "vLLM 不支持的模型架构"
- **解决方案**: 对 HuggingFace Transformers 使用 `--backend hf`(inspect-ai)或 `--backend accelerate`(lighteval)

**问题**: "需要信任远程代码"
- **解决方案**: 为具有自定义代码的模型(例如,Phi-2、Qwen)添加 `--trust-remote-code` 标志

**问题**: "未找到聊天模板"
- **解决方案**: 仅对包含聊天模板的指令调整模型使用 `--use-chat-template`

### 集成示例

**Python 脚本集成:**
```python
import subprocess
import os

def update_model_evaluations(repo_id, readme_content):
    """使用 README 中的评估更新模型卡片。"""
    result = subprocess.run([
        "python", "scripts/evaluation_manager.py",
        "extract-readme",
        "--repo-id", repo_id,
        "--create-pr"
    ], capture_output=True, text=True)

    if result.returncode == 0:
        print(f"Successfully updated {repo_id}")
    else:
        print(f"Error: {result.stderr}")
```
