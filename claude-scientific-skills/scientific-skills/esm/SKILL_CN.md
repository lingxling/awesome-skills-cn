---
name: esm
description: 包括 ESM3（跨序列、结构和功能的生成式多模态蛋白质设计）和 ESM C（高效蛋白质嵌入和表示）的综合蛋白质语言模型工具包。当处理蛋白质序列、结构或功能预测；设计新颖蛋白质；生成蛋白质嵌入；执行反向折叠；或进行蛋白质工程任务时使用此技能。支持本地模型使用和基于云的 Forge API 以实现可扩展的推理。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# ESM：进化尺度建模

## 概述

ESM 提供用于理解、生成和设计蛋白质的最先进蛋白质语言模型。此技能使您能够使用两个模型家族：ESM3 用于跨序列、结构和功能的生成式蛋白质设计，以及 ESM C 用于高效的蛋白质表示学习和嵌入。

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

# 本地加载模型
model: ESM3InferenceClient = ESM3.from_pretrained("esm3-sm-open-v1").to("cuda")

# 创建蛋白质提示
protein = ESMProtein(sequence="MPRT___KEND")  # '_' 代表被屏蔽的位置

# 生成补全
protein = model.generate(protein, GenerationConfig(track="sequence", num_steps=8))
print(protein.sequence)
```

**通过 Forge API 进行远程/云使用：**

```python
from esm.sdk.forge import ESM3ForgeInferenceClient
from esm.sdk.api import ESMProtein, GenerationConfig

# 连接到 Forge
model = ESM3ForgeInferenceClient(model="esm3-medium-2024-08", url="https://forge.evolutionaryscale.ai", token="<token>")

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
from esm.sdk.api import ESMProtein

# 加载 ESM C 模型
model = ESMC.from_pretrained("esmc-300m").to("cuda")

# 获取嵌入
protein = ESMProtein(sequence="MPRTKEINDAGLIVHSP...")
protein_tensor = model.encode(protein)

# 生成嵌入
embeddings = model.forward(protein_tensor)
```

**批处理：**

```python
# 编码多个蛋白质
proteins = [
    ESMProtein(sequence="MPRTKEIND..."),
    ESMProtein(sequence="AGLIVHSPQ..."),
    ESMProtein(sequence="KTEFLNDGR...")
]

embeddings_list = [model.logits(model.forward(model.encode(p))) for p in proteins]
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

使用 Forge 的异步执行器高效处理多个蛋白质。

```python
from esm.sdk.forge import ESM3ForgeInferenceClient
import asyncio

client = ESM3ForgeInferenceClient(model="esm3-medium-2024-08", token="<token>")

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
- `esm3-sm-open-v1` (1.4B) - 开放权重，本地使用，适合实验
- `esm3-medium-2024-08` (7B) - 质量和速度的最佳平衡（仅 Forge）
- `esm3-large-2024-03` (98B) - 最高质量，较慢（仅 Forge）

**ESM C 模型（嵌入）：**
- `esmc-300m` (30 层) - 轻量级，快速推理
- `esmc-600m` (36 层) - 平衡性能
- `esmc-6b` (80 层) - 最大表示质量

**选择标准：**
- **本地开发/测试**：使用 `esm3-sm-open-v1` 或 `esmc-300m`
- **生产质量**：通过 Forge 使用 `esm3-medium-2024-08`
- **最高精度**：使用 `esm3-large-2024-03` 或 `esmc-6b`
- **高吞吐量**：使用带有批处理执行器的 Forge API
- **成本优化**：使用较小的模型，实施缓存策略

## 安装

**基本安装：**

```bash
uv pip install esm
```

**使用 Flash Attention（推荐用于更快的推理）：**

```bash
uv pip install esm
uv pip install flash-attn --no-build-isolation
```

**用于 Forge API 访问：**

```bash
uv pip install esm  # SDK 包括 Forge 客户端
```

无需其他依赖项。在 https://forge.evolutionaryscale.ai 获取 Forge API 令牌。

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
- `references/workflows.md` - 完整示例和常见工作流模式

这些参考包含详细的 API 规范、参数描述和高级使用模式。根据特定任务需要加载它们。

## 最佳实践

**对于生成任务：**
- 从较小的模型开始进行原型设计（`esm3-sm-open-v1`）
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

- **GitHub 仓库**：https://github.com/evolutionaryscale/esm
- **Forge 平台**：https://forge.evolutionaryscale.ai
- **科学论文**：Hayes et al., Science (2025) - https://www.science.org/doi/10.1126/science.ads0018
- **博客文章**：
  - ESM3 发布：https://www.evolutionaryscale.ai/blog/esm3-release
  - ESM C 发布：https://www.evolutionaryscale.ai/blog/esm-cambrian
- **社区**：位于 https://bit.ly/3FKwcWd 的 Slack 社区
- **模型权重**：HuggingFace EvolutionaryScale 组织

## 负责任使用

ESM 旨在用于蛋白质工程、药物发现和科学研究中的有益应用。在设计新颖蛋白质进行实验验证之前，请遵循负责任生物设计框架（https://responsiblebiodesign.ai/）。考虑蛋白质设计的生物安全和伦理影响。
