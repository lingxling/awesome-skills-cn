---
name: transformers
description: 当你需要处理自然语言处理、计算机视觉、音频或多模态任务的预训练Transformer模型时，应使用此技能。适用于文本生成、分类、问答、翻译、摘要、图像分类、目标检测、语音识别以及在自定义数据集上微调模型。
license: Apache-2.0 license
compatibility: 某些功能需要Huggingface token
metadata:
    skill-author: K-Dense Inc.
---

# Transformers

## 概述

Hugging Face Transformers库提供了数千个预训练模型，适用于NLP、计算机视觉、音频和多模态领域的任务。使用此技能加载模型、执行推理以及在自定义数据上进行微调。

## 安装

安装transformers和核心依赖：

```bash
uv pip install torch transformers datasets evaluate accelerate
```

对于视觉任务，添加：
```bash
uv pip install timm pillow
```

对于音频任务，添加：
```bash
uv pip install librosa soundfile
```

## 身份验证

Hugging Face Hub上的许多模型需要身份验证。设置访问权限：

```python
from huggingface_hub import login
login()  # 按照提示输入token
```

或设置环境变量：
```bash
export HUGGINGFACE_TOKEN="your_token_here"
```

在以下位置获取token：https://huggingface.co/settings/tokens

## 快速开始

使用Pipeline API进行快速推理，无需手动配置：

```python
from transformers import pipeline

# 文本生成
generator = pipeline("text-generation", model="gpt2")
result = generator("The future of AI is", max_length=50)

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