---
name: primekg
description: 查询精准医学知识图谱（PrimeKG）以获取多尺度生物数据，包括基因、药物、疾病、表型等。
license: Unknown
metadata:
    skill-author: K-Dense Inc. (PrimeKG 原始数据来自哈佛 MIMS)
---

# PrimeKG 知识图谱技能

## 概述

PrimeKG 是一个精准医学知识图谱，整合了20多个主要数据库和高质量科学文献到单一资源中。它包含超过100,000个节点和400万条边，涵盖29种关系类型，包括药物-靶点、疾病-基因和表型-疾病关联。

**核心功能：**
- 搜索节点（基因、蛋白质、药物、疾病、表型）
- 检索直接邻居（相关实体和临床证据）
- 分析局部疾病背景（相关基因、药物、表型）
- 识别药物-疾病路径（潜在的药物重定位机会）

**数据访问：** 通过 `query_primekg.py` 进行程序化访问。数据存储在 `C:\Users\eamon\Documents\Data\PrimeKG\kg.csv`。

## 使用场景

本技能适用于以下情况：

- **基于知识的药物发现：** 识别疾病的靶点和机制。
- **药物重定位：** 寻找可能对新适应症有证据的现有药物。
- **表型分析：** 了解症状/表型如何与疾病和基因相关。
- **多尺度生物学：** 弥合分子靶点（基因）和临床结果（疾病）之间的差距。
- **网络药理学：** 研究药物-靶点相互作用的更广泛网络效应。

## 核心工作流程

### 1. 搜索实体

查找基因、药物或疾病的标识符。

```python
from scripts.query_primekg import search_nodes

# 搜索阿尔茨海默病节点
results = search_nodes("Alzheimer", node_type="disease")
# 返回: [{"id": "EFO_0000249", "type": "disease", "name": "Alzheimer's disease", ...}]
```

### 2. 获取邻居（直接关联）

检索所有连接的节点和关系类型。

```python
from scripts.query_primekg import get_neighbors

# 获取特定疾病ID的所有邻居
neighbors = get_neighbors("EFO_0000249")
# 返回: 邻居列表，如 {"neighbor_name": "APOE", "relation": "disease_gene", ...}
```

### 3. 分析疾病背景

一个高级函数，用于总结疾病的关联。

```python
from scripts.query_primekg import get_disease_context

# 疾病的综合总结
context = get_disease_context("Alzheimer's disease")
# 访问: context['associated_genes'], context['associated_drugs'], context['phenotypes']
```

## PrimeKG 中的关系类型

该图谱包含几种关键关系类型：
- `protein_protein`：物理蛋白质-蛋白质相互作用
- `drug_protein`：药物靶点/机制关联
- `disease_gene`：遗传关联
- `drug_disease`：适应症和禁忌症
- `disease_phenotype`：临床体征和症状
- `gwas`：全基因组关联研究证据

## 最佳实践

1. **使用特定ID：** 使用 `get_neighbors` 时，确保从 `search_nodes` 获取正确的ID。
2. **先了解背景：** 在深入研究特定基因或药物之前，使用 `get_disease_context` 获取广泛概述。
3. **过滤关系：** 使用 `get_neighbors` 中的 `relation_type` 过滤器专注于特定证据（例如，仅 `drug_protein`）。
4. **多尺度整合：** 与 `OpenTargets` 结合获取更深入的遗传证据，或与 `Semantic Scholar` 结合获取最新的文献背景。

## 资源

### 脚本
- `scripts/query_primekg.py`：用于搜索和查询知识图谱的核心函数。

### 数据路径
- 数据：`/mnt/c/Users/eamon/Documents/Data/PrimeKG/kg.csv`
- 总节点数：约129,000
- 总边数：约4,000,000
- 数据库：基于CSV，为pandas查询优化。