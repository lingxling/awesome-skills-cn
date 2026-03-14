---
name: torchdrug
description: 用于分子和蛋白质的 PyTorch 原生图神经网络。在构建用于药物发现、蛋白质建模或知识图谱推理的自定义 GNN 架构时使用。最适用于自定义模型开发、蛋白质属性预测、逆合成。对于预训练模型和多样化的特征提取器，请使用 deepchem；对于基准数据集，请使用 pytdc。
license: Apache-2.0 license
metadata:
    skill-author: K-Dense Inc.
---

# TorchDrug

## 概述

TorchDrug 是一个基于 PyTorch 的综合机器学习工具箱，用于药物发现和分子科学。将图神经网络、预训练模型和任务定义应用于分子、蛋白质和生物知识图谱，包括分子属性预测、蛋白质建模、知识图谱推理、分子生成、逆合成规划，拥有 40+ 精选数据集和 20+ 模型架构。

## 何时使用此技能

当您处理以下任务时，应使用此技能：

**数据类型：**
- SMILES 字符串或分子结构
- 蛋白质序列或 3D 结构（PDB 文件）
- 化学反应和逆合成
- 生物医学知识图谱
- 药物发现数据集

**任务：**
- 预测分子属性（溶解度、毒性、活性）
- 蛋白质功能或结构预测
- 药物-靶点结合预测
- 生成新的分子结构
- 规划化学合成路线
- 生物医学知识库中的链接预测
- 在科学数据上训练图神经网络

**库和集成：**
- TorchDrug 是主要库
- 通常与 RDKit 一起用于 cheminformatics
- 与 PyTorch 和 PyTorch Lightning 兼容
- 与 AlphaFold 和 ESM 集成用于蛋白质

## 入门

### 安装

```bash
uv pip install torchdrug
# 或带可选依赖项
uv pip install torchdrug[full]
```

### 快速示例

```python
from torchdrug import datasets, models, tasks
from torch.utils.data import DataLoader

# 加载分子数据集
dataset = datasets.BBBP("~/molecule-datasets/")
train_set, valid_set, test_set = dataset.split()

# 定义 GNN 模型
model = models.GIN(
    input_dim=dataset.node_feature_dim,
    hidden_dims=[256, 256, 256],
    edge_input_dim=dataset.edge_feature_dim,
    batch_norm=True,
    readout="mean"
)

# 创建属性预测任务
task = tasks.PropertyPrediction(
    model,
    task=dataset.tasks,
    criterion="bce",
    metric=["auroc", "auprc"]
)

# 使用 PyTorch 训练
optimizer = torch.optim.Adam(task.parameters(), lr=1e-3)
train_loader = DataLoader(train_set, batch_size=32, shuffle=True)

for epoch in range(100):
    for batch in train_loader:
        loss = task(batch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

## 核心功能

### 1. 分子属性预测

从结构预测分子的化学、物理和生物属性。

**用例：**
- 类药性和 ADMET 属性
- 毒性筛选
- 量子化学属性
- 结合亲和力预测

**关键组件：**
- 20+ 分子数据集（BBBP、HIV、Tox21、QM9 等）
- GNN 模型（GIN、GAT、SchNet）
- PropertyPrediction 和 MultipleBinaryClassification 任务

**参考：** 请查看 `references/molecular_property_prediction.md` 了解：
- 完整的数据集目录
- 模型选择指南
- 训练工作流程和最佳实践
- 特征工程详细信息

### 2. 蛋白质建模

处理蛋白质序列、结构和属性。

**用例：**
- 酶功能预测
- 蛋白质稳定性和溶解度
- 亚细胞定位
- 蛋白质-蛋白质相互作用
- 结构预测

**关键组件：**
- 15+ 蛋白质数据集（EnzymeCommission、GeneOntology、PDBBind 等）
- 序列模型（ESM、ProteinBERT、ProteinLSTM）
- 结构模型（GearNet、SchNet）
- 不同预测级别的多种任务类型

**参考：** 请查看 `references/protein_modeling.md` 了解：
- 蛋白质特定数据集
- 序列与结构模型
- 预训练策略
- 与 AlphaFold 和 ESM 的集成

### 3. 知识图谱推理

预测生物知识图谱中缺失的链接和关系。

**用例：**
- 药物重定位
- 疾病机制发现
- 基因-疾病关联
- 多跳生物医学推理

**关键组件：**
- 通用 KG（FB15k、WN18）和生物医学（Hetionet）
- 嵌入模型（TransE、RotatE、ComplEx）
- KnowledgeGraphCompletion 任务

**参考：** 请查看 `references/knowledge_graphs.md` 了解：
- 知识图谱数据集（包括具有 45k 生物医学实体的 Hetionet）
- 嵌入模型比较
- 评估指标和协议
- 生物医学应用

### 4. 分子生成

生成具有所需属性的新型分子结构。

**用例：**
- 从头药物设计
- 先导优化
- 化学空间探索
- 属性引导生成

**关键组件：**
- 自回归生成
- GCPN（基于策略的生成）
- GraphAutoregressiveFlow
- 属性优化工作流程

**参考：** 请查看 `references/molecular_generation.md` 了解：
- 生成策略（无条件、条件、基于支架）
- 多目标优化
- 验证和过滤
- 与属性预测的集成

### 5. 逆合成

预测从目标分子到起始材料的合成路线。

**用例：**
- 合成规划
- 路线优化
- 合成可及性评估
- 多步规划

**关键组件：**
- USPTO-50k 反应数据集
- CenterIdentification（反应中心预测）
- SynthonCompletion（反应物预测）
- 端到端逆合成管道

**参考：** 请查看 `references/retrosynthesis.md` 了解：
- 任务分解（中心 ID → 合成子完成）
- 多步合成规划
- 商业可用性检查
- 与其他逆合成工具的集成

### 6. 图神经网络模型

针对不同数据类型和任务的综合 GNN 架构目录。

**可用模型：**
- 通用 GNN：GCN、GAT、GIN、RGCN、MPNN
- 3D 感知：SchNet、GearNet
- 蛋白质特定：ESM、ProteinBERT、GearNet
- 知识图谱：TransE、RotatE、ComplEx、SimplE
- 生成式：GraphAutoregressiveFlow

**参考：** 请查看 `references/models_architectures.md` 了解：
- 详细的模型描述
- 按任务和数据集的模型选择指南
- 架构比较
- 实现提示

### 7. 数据集

40+ 精选数据集，涵盖化学、生物学和知识图谱。

**类别：**
- 分子属性（药物发现、量子化学）
- 蛋白质属性（功能、结构、相互作用）
- 知识图谱（通用和生物医学）
- 逆合成反应

**参考：** 请查看 `references/datasets.md` 了解：
- 完整的数据集目录，包括大小和任务
- 数据集选择指南
- 加载和预处理
- 分割策略（随机、支架）

## 常见工作流程

### 工作流程 1：分子属性预测

**场景：** 预测药物候选物的血脑屏障穿透性。

**步骤：**
1. 加载数据集：`datasets.BBBP()`
2. 选择模型：GIN 用于分子图
3. 定义任务：`PropertyPrediction` 用于二分类
4. 使用支架分割进行真实评估训练
5. 使用 AUROC 和 AUPRC 评估

**导航：** `references/molecular_property_prediction.md` → 数据集选择 → 模型选择 → 训练

### 工作流程 2：蛋白质功能预测

**场景：** 从序列预测酶功能。

**步骤：**
1. 加载数据集：`datasets.EnzymeCommission()`
2. 选择模型：ESM（预训练）或 GearNet（带结构）
3. 定义任务：`PropertyPrediction` 用于多分类
4. 微调预训练模型或从头训练
5. 使用准确率和每类指标评估

**导航：** `references/protein_modeling.md` → 模型选择（序列 vs 结构）→ 预训练策略

### 工作流程 3：通过知识图谱进行药物重定位

**场景：** 在 Hetionet 中寻找新的疾病治疗方法。

**步骤：**
1. 加载数据集：`datasets.Hetionet()`
2. 选择模型：RotatE 或 ComplEx
3. 定义任务：`KnowledgeGraphCompletion`
4. 使用负采样训练
5. 查询 "Compound-treats-Disease" 预测
6. 按合理性和机制过滤

**导航：** `references/knowledge_graphs.md` → Hetionet 数据集 → 模型选择 → 生物医学应用

### 工作流程 4：从头分子生成

**场景：** 生成为目标结合优化的类药分子。

**步骤：**
1. 在活性数据上训练属性预测器
2. 选择生成方法：GCPN 用于基于 RL 的优化
3. 定义结合亲和力、类药性、可合成性的奖励函数
4. 生成带有属性约束的候选物
5. 验证化学并按类药性过滤
6. 按多目标评分排序

**导航：** `references/molecular_generation.md` → 条件生成 → 多目标优化

### 工作流程 5：逆合成规划

**场景：** 为目标分子规划合成路线。

**步骤：**
1. 加载数据集：`datasets.USPTO50k()`
2. 训练中心识别模型（RGCN）
3. 训练合成子完成模型（GIN）
4. 组合成端到端逆合成管道
5. 递归应用于多步规划
6. 检查构建块的商业可用性

**导航：** `references/retrosynthesis.md` → 任务类型 → 多步规划

## 集成模式

### 与 RDKit 集成

在 TorchDrug 分子和 RDKit 之间转换：
```python
from torchdrug import data
from rdkit import Chem

# SMILES → TorchDrug 分子
smiles = "CCO"
mol = data.Molecule.from_smiles(smiles)

# TorchDrug → RDKit
tdkit_mol = mol.to_molecule()

# RDKit → TorchDrug
tdkit_mol = Chem.MolFromSmiles(smiles)
mol = data.Molecule.from_molecule(tdkit_mol)
```

### 与 AlphaFold/ESM 集成

使用预测结构：
```python
from torchdrug import data

# 加载 AlphaFold 预测结构
protein = data.Protein.from_pdb("AF-P12345-F1-model_v4.pdb")

# 构建带空间边的图
graph = protein.residue_graph(
    node_position="ca",
    edge_types=["sequential", "radius"],
    radius_cutoff=10.0
)
```

### 与 PyTorch Lightning 集成

包装任务用于 Lightning 训练：
```python
import pytorch_lightning as pl

class LightningTask(pl.LightningModule):
    def __init__(self, torchdrug_task):
        super().__init__()
        self.task = torchdrug_task

    def training_step(self, batch, batch_idx):
        return self.task(batch)

    def validation_step(self, batch, batch_idx):
        pred = self.task.predict(batch)
        target = self.task.target(batch)
        return {"pred": pred, "target": target}

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-3)
```

## 技术细节

深入了解 TorchDrug 的架构：

**核心概念：** 请查看 `references/core_concepts.md` 了解：
- 架构理念（模块化、可配置）
- 数据结构（Graph、Molecule、Protein、PackedGraph）
- 模型接口和前向函数签名
- 任务接口（predict、target、forward、evaluate）
- 训练工作流程和最佳实践
- 损失函数和指标
- 常见陷阱和调试

## 快速参考速查表

**选择数据集：**
- 分子属性 → `references/datasets.md` → 分子部分
- 蛋白质任务 → `references/datasets.md` → 蛋白质部分
- 知识图谱 → `references/datasets.md` → 知识图谱部分

**选择模型：**
- 分子 → `references/models_architectures.md` → GNN 部分 → GIN/GAT/SchNet
- 蛋白质（序列）→ `references/models_architectures.md` → 蛋白质部分 → ESM
- 蛋白质（结构）→ `references/models_architectures.md` → 蛋白质部分 → GearNet
- 知识图谱 → `references/models_architectures.md` → KG 部分 → RotatE/ComplEx

**常见任务：**
- 属性预测 → `references/molecular_property_prediction.md` 或 `references/protein_modeling.md`
- 生成 → `references/molecular_generation.md`
- 逆合成 → `references/retrosynthesis.md`
- KG 推理 → `references/knowledge_graphs.md`

**理解架构：**
- 数据结构 → `references/core_concepts.md` → 数据结构
- 模型设计 → `references/core_concepts.md` → 模型接口
- 任务设计 → `references/core_concepts.md` → 任务接口

## 常见问题排查

**问题：维度不匹配错误**
→ 检查 `model.input_dim` 与 `dataset.node_feature_dim` 匹配
→ 查看 `references/core_concepts.md` → 基本属性

**问题：分子任务性能差**
→ 使用支架分割，而非随机分割
→ 尝试 GIN 而非 GCN
→ 查看 `references/molecular_property_prediction.md` → 最佳实践

**问题：蛋白质模型不学习**
→ 对序列任务使用预训练的 ESM
→ 检查结构模型的边构建
→ 查看 `references/protein_modeling.md` → 训练工作流程

**问题：大图内存错误**
→ 减少批量大小
→ 使用梯度累积
→ 查看 `references/core_concepts.md` → 内存效率

**问题：生成的分子无效**
→ 添加有效性约束
→ 使用 RDKit 验证后处理
→ 查看 `references/molecular_generation.md` → 验证和过滤

## 资源

**官方文档：** https://torchdrug.ai/docs/
**GitHub：** https://github.com/DeepGraphLearning/torchdrug
**论文：** TorchDrug: A Powerful and Flexible Machine Learning Platform for Drug Discovery

## 总结

根据您的任务导航到相应的参考文件：

1. **分子属性预测** → `molecular_property_prediction.md`
2. **蛋白质建模** → `protein_modeling.md`
3. **知识图谱** → `knowledge_graphs.md`
4. **分子生成** → `molecular_generation.md`
5. **逆合成** → `retrosynthesis.md`
6. **模型选择** → `models_architectures.md`
7. **数据集选择** → `datasets.md`
8. **技术细节** → `core_concepts.md`

每个参考都提供了其领域的全面覆盖，包括示例、最佳实践和常见用例。