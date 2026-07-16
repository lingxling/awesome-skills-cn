---
name: esm
description: 当直接使用 `esm` Python SDK、ESM3 或 ESMC 模型 ID、Forge/Biohub 推理客户端或 ESMFold2 折叠工作流时使用。
license: MIT license
metadata: {"version": "1.1", "skill-author": "K-Dense Inc."}
---

# ESM：进化尺度建模

## 概述

ESM 提供用于理解、生成和设计蛋白质的蛋白质语言模型。此技能用于当前的 EvolutionaryScale/Biohub 工作流:ESM3 用于生成式设计,ESMC 用于表示学习和嵌入,托管的 Forge/Biohub 推理,以及 ESMFold2 全原子结构预测。

## 核心能力

### 1. 使用 ESM3 进行蛋白质序列生成

使用多模态生成建模生成具有所需属性的新颖蛋白质序列。

**何时使用：**
- 设计具有特定功能属性的蛋白质
- 完成部分蛋白质序列
- 生成现有蛋白质的变体
- 创建具有所需结构特征的蛋白质

**基本用法：**

```python
from esm.models.esm3 import ESM3
from esm.sdk.api import ESM3InferenceClient, ESMProtein, GenerationConfig

# 在 Hugging Face 上接受许可协议后加载本地开放权重。
model: ESM3InferenceClient = ESM3.from_pretrained("esm3-open").to("cuda")

# 创建蛋白质提示
protein = ESMProtein(sequence="MPRT___KEND")  # '_' 代表被屏蔽的位置

# 生成补全
protein = model.generate(protein, GenerationConfig(track="sequence", num_steps=8))
print(protein.sequence)
```

**通过 Forge API 进行远程/云使用：**

```python
import os
import esm
from esm.sdk.api import ESMProtein, GenerationConfig

# 与本地 ESM3 接口相同;令牌来自 ESM_API_KEY(参见"身份验证"）
model = esm.sdk.client("esm3-medium-2024-08", token=os.environ["ESM_API_KEY"])

# 生成
protein = model.generate(protein, GenerationConfig(track="sequence", num_steps=8))
```

有关详细的 ESM3 模型规范、高级生成配置和多模态提示示例，请参阅 `references/esm3-api.md`。

### 2. 结构预测和反向折叠

使用 ESM3 的结构轨道进行从序列的结构预测或反向折叠（从结构设计序列）。

**结构预测：**

```python
from esm.sdk.api import ESM3InferenceClient, ESMProtein, GenerationConfig

# 从序列预测结构
protein = ESMProtein(sequence="MPRTKEINDAGLIVHSP...")
protein_with_structure = model.generate(
    protein,
    GenerationConfig(track="structure", num_steps=protein.sequence.count("_"))
)

# 访问预测的结构
coordinates = protein_with_structure.coordinates  # 3D 坐标
pdb_string = protein_with_structure.to_pdb()
```

**反向折叠（从结构设计序列）：**

```python
# 为目标结构设计序列
protein_with_structure = ESMProtein.from_pdb("target_structure.pdb")
protein_with_structure.sequence = None  # 移除序列

# 生成折叠到此结构的序列
designed_protein = model.generate(
    protein_with_structure,
    GenerationConfig(track="sequence", num_steps=50, temperature=0.7)
)
```

### 3. 使用 ESM C 进行蛋白质嵌入

为下游任务（如功能预测、分类或相似性分析）生成高质量嵌入。

**何时使用：**
- 为机器学习提取蛋白质表示
- 计算序列相似性
- 用于蛋白质分类的特征提取
- 用于蛋白质相关任务的迁移学习

**基本用法：**

```python
from esm.models.esmc import ESMC
from esm.sdk.api import ESMProtein, LogitsConfig

# 加载 ESM C 模型
model = ESMC.from_pretrained("esmc_300m").to("cuda")

# 获取嵌入
protein = ESMProtein(sequence="MPRTKEINDAGLIVHSP...")
protein_tensor = model.encode(protein)
logits_output = model.logits(
    protein_tensor,
    LogitsConfig(sequence=True, return_embeddings=True),
)
embeddings = logits_output.embeddings
```

**批处理：**

```python
# 编码多个蛋白质
proteins = [
    ESMProtein(sequence="MPRTKEIND..."),
    ESMProtein(sequence="AGLIVHSPQ..."),
    ESMProtein(sequence="KTEFLNDGR...")
]

embeddings_list = [
    model.logits(
        model.encode(p),
        LogitsConfig(sequence=True, return_embeddings=True),
    ).embeddings
    for p in proteins
]
```

有关 ESM C 模型详细信息、效率比较和高级嵌入策略，请参阅 `references/esm-c-api.md`。

### 4. 功能条件和注释

使用 ESM3 的功能轨道生成具有特定功能注释的蛋白质或从序列预测功能。

**功能条件生成：**

```python
from esm.sdk.api import ESMProtein, FunctionAnnotation, GenerationConfig

# 创建具有所需功能的蛋白质
protein = ESMProtein(
    sequence="_" * 200,  # 生成 200 个残基的蛋白质
    function_annotations=[
        FunctionAnnotation(label="fluorescent_protein", start=50, end=150)
        ]
)

# 生成具有指定功能的序列
functional_protein = model.generate(
    protein,
    GenerationConfig(track="sequence", num_steps=200)
)
```

### 5. 思维链生成

使用 ESM3 的思维链生成方法迭代优化蛋白质设计。

```python
from esm.sdk.api import GenerationConfig

# 多步细化
protein = ESMProtein(sequence="MPRT" + "_" * 100 + "KEND")

# 步骤 1：生成初始结构
config = GenerationConfig(track="structure", num_steps=50)
protein = model.generate(protein, config)

# 步骤 2：基于结构细化序列
config = GenerationConfig(track="sequence", num_steps=50, temperature=0.5)
protein = model.generate(protein, config)

# 步骤 3：预测功能
config = GenerationConfig(track="function", num_steps=20)
protein = model.generate(protein, config)
```

### 6. 使用 Forge API 进行批处理

使用 Forge 的异步方法高效处理多个蛋白质。

```python
import os
import asyncio
import esm
from esm.sdk.api import ESMProtein, GenerationConfig

client = esm.sdk.client("esm3-medium-2024-08", token=os.environ["ESM_API_KEY"])

# 异步批处理
async def batch_generate(proteins_list):
    tasks = [
        client.async_generate(protein, GenerationConfig(track="sequence"))
        for protein in proteins_list
    ]
    return await asyncio.gather(*tasks)

# 执行
proteins = [ESMProtein(sequence=f"MPRT{'_' * 50}KEND") for _ in range(10)]
results = asyncio.run(batch_generate(proteins))
```

有关详细的 Forge API 文档、身份验证、速率限制和批处理模式，请参阅 `references/forge-api.md`。

## 模型选择指南

**ESM3 模型（生成式）：**
- `esm3-open` (1.4B) - 开放权重,在 Hugging Face 上接受许可协议后可本地使用
- `esm3-medium-2024-08` (7B) - 质量和速度的最佳平衡（仅 Forge）
- `esm3-large-2024-03` (98B) - 最高质量，较慢（仅 Forge）

**ESM C 模型（嵌入）：**
- `esmc_300m` / `esmc-300m-2024-12` (30 层) - 轻量级,快速推理（开放权重,本地）
- `esmc_600m` / `esmc-600m-2024-12` (36 层) - 平衡性能（开放权重,本地）
- `esmc-6b-2024-12` (80 层) - 最大质量（Forge API;本地 6B 权重需要 Forge 或 SageMaker）

本地 `ESMC.from_pretrained()` 示例使用带下划线的别名（`esmc_300m`、`esmc_600m`）。托管 API 客户端使用带日期的模型 ID,例如 `esmc-600m-2024-12`。

**选择标准：**
- **本地开发/测试**：使用 `esm3-open` 或 `esmc_300m`
- **生产质量**：通过 Forge 使用 `esm3-medium-2024-08`
- **最高精度**：通过 Forge 使用 `esm3-large-2024-03` 或 `esmc-6b-2024-12`
- **高吞吐量**：使用带有明确异步并发限制的 Forge 或 Biohub API
- **成本优化**：使用较小的模型，实施缓存策略

## 安装

从 PyPI 安装（EvolutionaryScale 发布的 [`esm`](https://pypi.org/project/esm/)）。当前 PyPI 版本:**3.2.3**(2025 年 10 月 14 日）。需要 **Python >=3.12,<3.13**。

**基本安装：**

```bash
uv pip install "esm==3.2.3"
```

**使用 Flash Attention（推荐用于 NVIDIA GPU 上更快的推理）：**

```bash
uv pip install "esm==3.2.3"
uv pip install flash-attn --no-build-isolation
```

Forge 客户端随 `esm` 包一起提供 - ESM3 或 ESMC 的 Forge 推理无需额外安装。

## 身份验证

Forge API 访问需要 API 密钥。切勿在脚本中硬编码令牌或将其提交到版本控制。

1. 检查环境中是否已设置 `ESM_API_KEY`。
2. 如果未设置,只在本地 `.env` 中检查 `ESM_API_KEY`(不要加载不相关的机密信息）。
3. 如果仍然缺失,在 [Biohub 开发者控制台](https://biohub.ai/developer-console/api-keys)为 Biohub API 创建密钥,或在 [Forge](https://forge.evolutionaryscale.ai) 为旧版 Forge 托管的 ESM3/ESMC 访问创建密钥。

```python
import os

token = os.environ["ESM_API_KEY"]  # 如果未设置则抛出 KeyError
```

当省略 `token` 参数时,`esm.sdk.client()` 会自动读取 `ESM_API_KEY`。将端点 URL 固定为可信主机,例如 `https://forge.evolutionaryscale.ai` 或 `https://biohub.ai`;不要从不可信的用户输入中获取 API 主机地址。

**Biohub 平台：** EvolutionaryScale 和 Forge 现在通过 [biohub.ai](https://biohub.ai) 提供当前的托管模型。SDK 类名可能仍引用 "Forge"。有关 ESMFold2 和 Biohub 特定的设置，请参阅 `references/biohub-platform.md`。

## 常见工作流

有关详细示例和完整工作流，请参阅 `references/workflows.md`，其中包括：
- 使用思维链的新颖 GFP 设计
- 蛋白质变体生成和筛选
- 基于结构的序列优化
- 功能预测管道
- 基于嵌入的聚类和分析

## 参考

此技能包含全面的参考文档：

- `references/esm3-api.md` - ESM3 模型架构、API 参考、生成参数和多模态提示
- `references/esm-c-api.md` - ESM C 模型详细信息、嵌入策略和性能优化
- `references/forge-api.md` - Forge 平台文档、身份验证、批处理和部署
- `references/biohub-platform.md` - Biohub API 迁移、ESMFold2 结构预测以及开发者控制台身份验证
- `references/workflows.md` - 完整示例和常见工作流模式

这些参考包含详细的 API 规范、参数描述和高级使用模式。根据特定任务需要加载它们。

## 最佳实践

**对于生成任务：**
- 从较小的模型开始进行原型设计（`esm3-open`）
- 使用温度参数控制多样性（0.0 = 确定性，1.0 = 多样化）
- 使用思维链进行复杂设计的迭代细化
- 使用结构预测或湿实验室实验验证生成的序列

**对于嵌入任务：**
- 尽可能批处理序列以提高效率
- 为重复分析缓存嵌入
- 计算相似性时归一化嵌入
- 根据下游任务要求使用适当的模型大小

**对于生产部署：**
- 使用 Forge API 以实现可扩展性和最新模型
- 为 API 调用实施错误处理和重试逻辑
- 监控令牌使用并实施速率限制
- 考虑使用 AWS SageMaker 进行专用基础设施部署

## 资源和文档

- **GitHub 仓库：** https://github.com/Biohub/esm（当前 ESMC/ESMFold2/Biohub 文档;ESM3 文档仍从该仓库链接）
- **Forge 平台：** https://forge.evolutionaryscale.ai
- **Biohub 平台：** https://biohub.ai
- **科学论文：** Hayes et al., Science (2025) - https://www.science.org/doi/10.1126/science.ads0018
- **博客文章：**
  - ESM3 发布：https://www.evolutionaryscale.ai/blog/esm3-release
  - ESM C 发布：https://www.evolutionaryscale.ai/blog/esm-cambrian
- **社区：** 位于 https://bit.ly/3FKwcWd 的 Slack 社区
- **模型权重：** Hugging Face 上的 EvolutionaryScale 和 Biohub 组织

## 负责任使用

ESM 旨在用于蛋白质工程、药物发现和科学研究中的有益应用。在设计新颖蛋白质进行实验验证之前，请遵循负责任生物设计框架（https://responsiblebiodesign.ai/）以及 Biohub 可接受使用政策（https://biohub.org/acceptable-use-policy/）。考虑蛋白质设计的生物安全和伦理影响。
