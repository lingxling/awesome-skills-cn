---
name: molfeat
description: 用于化学信息学的分子表示和特征工程库。提供统一的接口用于计算分子描述符、指纹、图嵌入和物理化学性质。支持RDKit、Mordred、DGL-LifeSci、DeepChem等后端。适用于分子性质预测、虚拟筛选、QSAR建模、药物发现和化学信息学研究。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# MolFeat

## 概述

MolFeat是一个用于化学信息学的分子表示和特征工程库。它提供了统一的接口，用于计算分子描述符、指纹、图嵌入和物理化学性质。该库支持多个后端，包括RDKit、Mordred、DGL-LifeSci、DeepChem等，适用于分子性质预测、虚拟筛选、QSAR建模、药物发现和化学信息学研究。

## 核心能力

### 1. 分子描述符

计算各种分子描述符，包括：
- **物理化学性质**：分子量、LogP、TPSA、氢键供体/受体
- **拓扑描述符**：Wiener指数、Zagreb指数、Balaban指数
- **电子描述符**：部分电荷、电负性、极化率
- **几何描述符**：分子体积、表面积、形状指数
- **量子化学描述符**：HOMO/LUMO能级、偶极矩

### 2. 分子指纹

生成多种分子指纹，包括：
- **基于子结构的指纹**：MACCS密钥、PubChem指纹
- **基于路径的指纹**：Morgan指纹（ECFP）、RDKit指纹
- **基于拓扑的指纹**：拓扑指纹、原子对指纹
- **基于药效团的指纹**：药效团指纹、Tanimoto相似性

### 3. 图嵌入

使用图神经网络生成分子嵌入：
- **图卷积网络（GCN）**：基于图的卷积操作
- **图注意力网络（GAT）**：基于注意力的图神经网络
- **消息传递神经网络（MPNN）**：基于消息传递的神经网络
- **预训练模型**：使用预训练的分子表示模型

### 4. 物理化学性质

计算分子的物理化学性质：
- **脂溶性**：LogP、LogD
- **溶解度**：LogS、水溶性
- **渗透性**：Caco-2渗透性、血脑屏障渗透性
- **极性**：TPSA（拓扑极性表面积）
- **反应性**：反应性基团、代谢稳定性

## 何时使用此技能

在以下情况下使用此技能：
- 计算分子描述符和指纹
- 进行分子性质预测
- 执行虚拟筛选
- 构建QSAR模型
- 进行药物发现研究
- 执行化学信息学分析
- 生成分子嵌入用于机器学习
- 比较分子相似性

## 安装

```bash
# 基本安装
pip install molfeat

# 带有所有依赖项的安装
pip install molfeat[all]

# 带有特定后端的安装
pip install molfeat[rdkit,mordred,dgl]
```

## 使用示例

### 计算分子描述符

```python
from molfeat.calc import FPCalculator
from rdkit import Chem

# 创建分子
mol = Chem.MolFromSmiles("CCO")

# 计算描述符
calc = FPCalculator("desc2d")
descriptors = calc(mol)

print(f"分子量: {descriptors['MolWt']}")
print(f"LogP: {descriptors['MolLogP']}")
print(f"TPSA: {descriptors['TPSA']}")
```

### 生成分子指纹

```python
from molfeat.calc import FPCalculator

# 创建分子
mol = Chem.MolFromSmiles("CCO")

# 生成Morgan指纹（ECFP）
calc = FPCalculator("ecfp:4")
fingerprint = calc(mol)

print(f"指纹长度: {len(fingerprint)}")
print(f"指纹: {fingerprint}")
```

### 计算图嵌入

```python
from molfeat.trans.graph import GraphTransformer

# 创建分子
mol = Chem.MolFromSmiles("CCO")

# 创建图转换器
transformer = GraphTransformer("gin_supervised")

# 计算图嵌入
embedding = transformer(mol)

print(f"嵌入维度: {embedding.shape}")
```

### 批量计算

```python
from molfeat.calc import FPCalculator
from rdkit import Chem

# 创建分子列表
smiles_list = ["CCO", "CC(C)O", "c1ccccc1"]
mols = [Chem.MolFromSmiles(smi) for smi in smiles_list]

# 计算指纹
calc = FPCalculator("ecfp:4")
fingerprints = [calc(mol) for mol in mols]

print(f"指纹数量: {len(fingerprints)}")
```

## 支持的后端

### RDKit
- 描述符：2D和3D描述符
- 指纹：Morgan、RDKit、MACCS、AtomPair
- 性质：物理化学性质

### Mordred
- 描述符：1800+分子描述符
- 覆盖：物理化学、拓扑、电子、几何

### DGL-LifeSci
- 图嵌入：GCN、GAT、MPNN
- 预训练模型：ChemBERTa、MolBERT

### DeepChem
- 图神经网络：GraphConv、Weave、MPNN
- 分子表示：分子图、分子指纹

## 最佳实践

1. **选择合适的描述符**：根据任务选择最相关的描述符
2. **标准化分子**：在使用前标准化分子结构
3. **处理缺失值**：处理缺失或无效的描述符值
4. **特征缩放**：对描述符进行标准化或归一化
5. **验证结果**：验证计算结果的准确性
6. **批量处理**：使用批量处理提高效率
7. **缓存结果**：缓存计算结果以避免重复计算

## 常见问题

**Q: 如何选择合适的指纹？**
A: 根据任务选择。ECFP适用于相似性搜索，MACCS适用于快速筛选。

**Q: 如何处理缺失的描述符？**
A: 使用插值、删除或填充方法处理缺失值。

**Q: MolFeat支持哪些分子格式？**
A: 支持SMILES、SDF、MOL等多种格式。

**Q: 如何计算3D描述符？**
A: 需要先生成3D构象，然后计算3D描述符。

## 资源

- **MolFeat文档**：https://molfeat-docs.datamol.io
- **GitHub**：https://github.com/datamol-io/molfeat
- **RDKit文档**：https://www.rdkit.org/docs
- **Mordred文档**：https://mordred-descriptor.github.io
