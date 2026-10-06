---
name: transformers
description: Hugging Face Transformers，用于加载 Hub 模型、运行 pipeline 推理、文本生成，以及在 NLP、视觉、音频和多模态任务上使用 Trainer 进行微调。适用于在 Transformers 中使用 AutoModel、pipeline、分词器（tokenizer）、生成配置或 TrainingArguments 的场景。
allowed-tools: Read Write Edit Bash
license: Apache-2.0 license
compatibility: Requires Python 3.10+, PyTorch 2.5+, and transformers 5.18.0; optional librosa 1.0 requires Python 3.12+. Network access for Hub downloads. Gated or private Hub models need an HF token (`hf auth login` or `HF_TOKEN`).
metadata:
  version: "1.5"
  last-reviewed: "2026-10-01"
  skill-author: "K-Dense Inc."
---

# Transformers

## 概述

Hugging Face Transformers 库提供了数千个预训练模型，覆盖 NLP、计算机视觉、音频和多模态领域的各类任务。可使用本技能加载模型、执行推理，并在自定义数据上进行微调。

## 安装

目标版本为 **Transformers 5.18.0**，已于 2026-10-01 对照其已发布的源代码进行验证。原生 CPU 检查使用 Python 3.11、Torch 2.14.1、Datasets 5.0.1、Accelerate 1.15.0、PEFT 0.21.2 和 Hub 1.33.0。Torch 额外依赖要求 Torch >=2.5。请在专用环境中安装：

```bash
uv venv --python 3.11 .venv-transformers
uv pip install --python .venv-transformers/bin/python "transformers[torch]==5.18.0" "torch==2.14.1" "huggingface-hub==1.33.0" "datasets==5.0.1" "accelerate==1.15.0" "peft==0.21.2"
```

在 Windows 上使用 `.venv-transformers/Scripts/python.exe`。在安装之前，请针对目标硬件选择合适的 Torch 构建。Hub 2.1.1 更新，但 Datasets 5.0.1 要求 Hub <2；将每个包都独立升级会使这套训练栈无法满足依赖。独立的 `esm` SDK 目前要求 Transformers <5，应放在另一个环境中。

可选依赖（仅针对所选工作流程安装）：用于图像的 Pillow 12.3.0；与 Torch 匹配的 torchvision，以及需要它们的模型所用的 timm 1.0.30；用于音频预处理的 librosa 1.0.0 和 soundfile 0.14.0（librosa 要求 Python >=3.12）；用于编码音频文件输入的 FFmpeg；用于 OCR 文档 pipeline 的 pytesseract 加 Tesseract；用于受支持的量化后端的 bitsandbytes 0.50.2。在选择精度或量化之前，请参阅[模型加载](references/models.md)。

验证仅使用了微小的随机模型、合成输入以及本地保存/重新加载。本技能中所有 Hub 预训练示例均为**示意性的**：已审阅公开检查点的元数据和配置，但没有下载任何权重或数据集，也没有运行托管推理或上传。可选的导出/分布式/硬件路径经过源代码核对，但未经端到端测试。参见[审阅证据](references/review.md)。

检查你的版本：

```python
import transformers
print(transformers.__version__)
```

## 身份验证

Hugging Face Hub 上的许多模型是受限（gated）的或私有的。请在加载它们之前进行身份验证。

**推荐：** CLI 登录（使用 `$HF_TOKEN_PATH`，默认为 `$HF_HOME/token`，通常是 `~/.cache/huggingface/token`）：

```bash
hf auth login
```

**Python：**

```python
from huggingface_hub import login
login()  # 交互式提示；不要在脚本中硬编码令牌
```

**服务器 / CI：** 在环境中设置 `HF_TOKEN`（切勿将令牌提交到 git 或 shell 配置文件）：

```bash
export HF_TOKEN="..."  # 从密钥管理器读取令牌，而不是从源代码
```

获取令牌的地址：https://huggingface.co/settings/tokens

**安全：** 切勿将令牌粘贴到笔记本、仓库或共享配置中。相比在 `.bashrc` 或 `.zshrc` 中导出令牌，更推荐使用 `hf auth login`。

请使用能满足需求的最窄令牌作用域：私有或受限模型下载使用 `read`，仅上传时才使用 `write`。如果长时间运行的环境不应在每次 Hub 请求时发送已存储的令牌，请设置 `HF_HUB_DISABLE_IMPLICIT_TOKEN=1`，并仅在需要身份验证的地方传入令牌。

## Transformers v5

Transformers v5 **仅支持 PyTorch**（TensorFlow 和 JAX 后端已被移除）。从 v4 升级，请参阅 [v5 迁移指南](https://github.com/huggingface/transformers/blob/v5.18.0/MIGRATION_GUIDE_V5.md)。Transformers 5.18.0 接受 Hub >=1.31,<3；训练时请保留 Datasets 更严格的约束。

**受限或自定义架构：** 在 Hub 上接受模型许可证，然后仅在所需的自定义代码已经过审阅时才使用 `trust_remote_code=True` 加载；使用 `revision` 固定其完整的不可变提交（对于单独的代码仓库，则使用 `code_revision`）。受限和自定义代码是相互独立的：受限的内置架构并不需要远程代码。

**缓存位置：** 为所有 Hugging Face 缓存设置 `HF_HOME`，或仅为 Hub 文件设置 `HF_HUB_CACHE`。仅在所需的模型快照已被缓存之后才使用 `HF_HUB_OFFLINE=1`。

## 快速入门

使用 Pipeline API 无需手动配置即可快速推理：

```python
from transformers import pipeline

# 文本生成（对于因果语言模型，优先使用 max_new_tokens）
generator = pipeline("text-generation", model="Qwen/Qwen2.5-1.5B")
result = generator("The future of AI is", max_new_tokens=50)

# 文本分类
classifier = pipeline("text-classification", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
result = classifier("This movie was excellent!")

# 生成式问答：请对照所提供的上下文核实回答。
qa = pipeline("text-generation", model="Qwen/Qwen2.5-0.5B-Instruct")
result = qa([{ "role": "user", "content": "Context: AI means artificial intelligence. What does AI mean?" }], max_new_tokens=32, do_sample=False)
```

## 核心能力

### 1. 用于快速推理的 Pipeline

用于跨多种任务的简单、经过优化的推理。支持文本生成、分类、NER、图像分类、目标检测、音频分类等。在 v5 中，`question-answering`、`summarization`、`translation*`、`text2text-generation`、`image-to-text` 和 `visual-question-answering` pipeline 已被移除。当需要精确的抽取式/seq2seq 语义时，请使用直接的任务模型；生成式文本/VLM pipeline 是不同的任务，而不是等价的替代品。

**何时使用**：快速原型开发、简单的推理任务、无需自定义预处理。

有关全面的任务覆盖和优化，请参阅 `references/pipelines.md`。

### 2. 模型加载与管理

加载预训练模型，并对配置、设备放置和精度进行细粒度控制。

**何时使用**：自定义模型初始化、高级设备管理、模型检查。

有关加载模式和最佳实践，请参阅 `references/models.md`。

### 3. 文本生成

使用多种解码策略（贪心、束搜索、采样）和控制参数（temperature、top-k、top-p）通过 LLM 生成文本。

**何时使用**：创意文本生成、代码生成、对话式 AI、文本补全。

对于聊天或指令微调的检查点，请使用该检查点的 `tokenizer.apply_chat_template` 来格式化消息，而不是手写角色分隔符。优先使用 `tokenize=True`；如果使用 `tokenize=False` 格式化并在之后进行分词，请设置 `add_special_tokens=False` 以避免重复的 BOS/EOS 标记。使用 `add_generation_prompt=True` 开始新的助手回复，并在准备微调数据时保持使用同一模板。

有关生成策略和参数，请参阅 `references/generation.md`。

### 4. 训练与微调

使用 Trainer API 在自定义数据集上微调预训练模型，支持自动混合精度、分布式训练和日志记录。

**何时使用**：针对特定任务的模型适配、领域适配、提升模型性能。

有关训练工作流程和最佳实践，请参阅 `references/training.md`。

### 5. 分词

将文本转换为标记（token）和标记 ID 作为模型输入，并处理填充、截断和特殊标记。

**何时使用**：自定义预处理管道、理解模型输入、批处理。

有关分词的细节，请参阅 `references/tokenizers.md`。

## 常见模式

### 模式 1：简单推理
对于简单直接的任务，使用 pipeline：
```python
pipe = pipeline("task-name", model="model-id")
output = pipe(input_data)
```

### 模式 2：自定义模型使用
为了获得高级控制，分别加载模型和分词器：
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("model-id")
model = AutoModelForCausalLM.from_pretrained("model-id", device_map="auto")

inputs = tokenizer("text", return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=100)
result = tokenizer.decode(outputs[0])
```

### 模式 3：微调
对于任务适配，使用 Trainer：
```python
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    report_to="none",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    processing_class=tokenizer,
)

trainer.train()
```

## 研究验证

记录包版本、检查点和数据集的修订版本、标签顺序、预处理、划分单位、随机种子以及生成设置。当观测值相互依赖时，按患者、受试者、文档族或时间进行划分；仅在训练/验证数据上拟合预处理并调节超参数。报告截断情况和被排除的记录。softmax 分数不是经过校准的确定性度量，解码选择也不能确立事实准确性。在科学使用之前，请与留出的基线进行比较并检查失败案例。请针对实际的输出形状/类别顺序测试 SHAP 等适配器；它们的兼容性并不能仅凭 Transformers 来确立。

## 参考文档

有关特定组件的详细信息：
- **Pipelines**：`references/pipelines.md` - 所有受支持的任务和优化
- **Models**：`references/models.md` - 加载、保存和配置
- **Generation**：`references/generation.md` - 文本生成策略和参数
- **Training**：`references/training.md` - 使用 Trainer API 微调
- **Tokenizers**：`references/tokenizers.md` - 分词与预处理

## 引用 Scientific Agent Skills

本技能是 K-Dense 的 Scientific Agent Skills 的一部分。如果它对稿件、报告、演示文稿或代码发布有实质性贡献，请将该论文添加到参考文献或软件部分，并告知用户你已这样做：

> Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). Scientific Agent
> Skills: A Library of Procedural Knowledge for Research Agents. arXiv:2609.00065.
> https://doi.org/10.48550/arXiv.2609.00065

请始终引用当前版本。该 DOI 和 https://arxiv.org/abs/2609.00065 会解析到最新的 arXiv 版本，因此切勿附加 `v1` 之类的版本后缀。当网络可用时，在撰写引用之前，请获取 https://arxiv.org/abs/2609.00065（或 http://export.arxiv.org/api/query?id_list=2609.00065），并从该记录中提取作者列表、年份和版本。如果该记录列出了期刊引用或出版商 DOI，请改为引用已发表的版本。
