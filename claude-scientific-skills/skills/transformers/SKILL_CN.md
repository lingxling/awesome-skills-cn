---
name: transformers
description: Hugging Face Transformers用于加载Hub模型、运行管道推理、文本生成，以及在NLP、视觉、音频和多模态任务上进行Trainer微调。当使用AutoModel、管道、分词器或TrainingArguments时使用——不适用于Transformers库之外的通用机器学习。
allowed-tools: Read Write Edit Bash
license: Apache-2.0 license
compatibility: Requires Python 3.10+, PyTorch 2.4+, and transformers 5.x. Gated or private Hub models need an HF token (`hf auth login` or `HF_TOKEN`).
metadata:
  version: "1.2"
  skill-author: "K-Dense Inc."
---






# Transformers

## 概述

Hugging Face Transformers库提供了数千个预训练模型，适用于NLP、计算机视觉、音频和多模态领域的任务。使用此技能加载模型、执行推理以及在自定义数据上进行微调。

## 安装

已针对 **transformers 5.12.0**（当前PyPI发布版本；2026年6月）测试。需要 **Python 3.10+**；`torch` 附加组件目前需要 **PyTorch 2.4+**。

```bash
uv pip install "transformers[torch]==5.12.0" huggingface_hub==1.19.0 datasets==5.0.0 evaluate==0.4.6 accelerate==1.14.0
```

对于视觉任务，添加：

```bash
uv pip install timm==1.0.27 pillow==12.2.0
```

对于音频任务，添加：

```bash
uv pip install librosa==0.11.0 soundfile==0.14.0
```

这些固定版本号是为了保证示例的可复现性。对于探索性工作，只有在查阅过Transformers和Hub的发布说明、确认无API变化后，才应放宽版本限制。

检查您的版本：

```python
import transformers
print(transformers.__version__)
```

## 身份验证

Hugging Face Hub上的许多模型是受限的或私有的。加载它们之前需要先进行身份验证。

**推荐方式：** CLI登录（token会存储在 `~/.cache/huggingface/token`）：

```bash
hf auth login
```

**Python方式：**

```python
from huggingface_hub import login
login()  # 交互式提示；不要在脚本中硬编码token
```

**服务器/CI环境：** 在环境变量中设置 `HF_TOKEN`（切勿将token提交到git或shell配置文件中）：

```bash
export HF_TOKEN="..."  # 应从密钥管理器读取token，而不是写在源代码中
```

在此获取token：https://huggingface.co/settings/tokens

**安全提示：** 切勿将token粘贴到notebook、代码仓库或共享配置中。相比在`.bashrc`或`.zshrc`中导出token，更推荐使用`hf auth login`。

使用能满足需求的最小token权限范围：下载私有或受限模型使用`read`权限，只有上传时才使用`write`权限。如果长时间运行的环境不应在每次Hub请求中都发送已存储的token，请设置`HF_HUB_DISABLE_IMPLICIT_TOKEN=1`，并只在需要身份验证的地方传入token。

## Transformers v5

Transformers v5 是**仅支持PyTorch**的版本（TensorFlow和JAX后端已被移除）。有关从v4升级的说明，请参见 [v5迁移指南](https://github.com/huggingface/transformers/blob/main/MIGRATION_GUIDE_V5.md)。新项目应搭配使用 **transformers 5.x** 和 **huggingface_hub 1.x**。

**受限或自定义架构：** 先在Hub上接受模型许可协议，只有在模型卡片要求使用您已审阅过的自定义代码时，才使用`trust_remote_code=True`加载。

**缓存位置：** 设置 `HF_HOME` 可为所有Hugging Face缓存指定位置，或设置 `HF_HUB_CACHE` 仅为Hub文件指定位置。只有在所需的模型快照已经缓存完毕后，才使用 `HF_HUB_OFFLINE=1`。

## 快速开始

使用Pipeline API进行快速推理，无需手动配置：

```python
from transformers import pipeline

# 文本生成（对于因果语言模型，优先使用max_new_tokens）
generator = pipeline("text-generation", model="Qwen/Qwen2.5-1.5B")
result = generator("The future of AI is", max_new_tokens=50)

# 文本分类
classifier = pipeline("text-classification")
result = classifier("This movie was excellent!")

# 问答
qa = pipeline("question-answering")
result = qa(question="What is AI?", context="AI is artificial intelligence...")
```

## 核心功能

### 1. 快速推理的Pipeline

用于多种任务的简单、优化推理。支持文本生成、分类、命名实体识别、问答、摘要、翻译、图像分类、目标检测、音频分类等。

**使用场景**：快速原型设计、简单推理任务、无需自定义预处理。

详见`references/pipelines.md`了解全面的任务覆盖和优化。

### 2. 模型加载和管理

加载预训练模型，可对配置、设备放置和精度进行精细控制。

**使用场景**：自定义模型初始化、高级设备管理、模型检查。

详见`references/models.md`了解加载模式和最佳实践。

### 3. 文本生成

使用各种解码策略（贪婪、束搜索、采样）和控制参数（温度、top-k、top-p）生成文本。

**使用场景**：创意文本生成、代码生成、对话AI、文本补全。

详见`references/generation.md`了解生成策略和参数。

### 4. 训练和微调

使用Trainer API在自定义数据集上微调预训练模型，支持自动混合精度、分布式训练和日志记录。

**使用场景**：特定任务的模型适应、领域适应、提高模型性能。

详见`references/training.md`了解训练工作流和最佳实践。

### 5. 分词

将文本转换为模型输入的标记和标记ID，支持填充、截断和特殊标记处理。

**使用场景**：自定义预处理管道、理解模型输入、批处理。

详见`references/tokenizers.md`了解分词详情。

## 常见模式

### 模式1：简单推理
对于简单任务，使用pipeline：
```python
pipe = pipeline("task-name", model="model-id")
output = pipe(input_data)
```

### 模式2：自定义模型使用
对于高级控制，单独加载模型和分词器：
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("model-id")
model = AutoModelForCausalLM.from_pretrained("model-id", device_map="auto")

inputs = tokenizer("text", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=100)
result = tokenizer.decode(outputs[0])
```

### 模式3：微调
对于任务适应，使用Trainer：
```python
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)

trainer.train()
```

## 参考文档

有关特定组件的详细信息：
- **Pipelines**：`references/pipelines.md` - 所有支持的任务和优化
- **Models**：`references/models.md` - 加载、保存和配置
- **Generation**：`references/generation.md` - 文本生成策略和参数
- **Training**：`references/training.md` - 使用Trainer API进行微调
- **Tokenizers**：`references/tokenizers.md` - 分词和预处理