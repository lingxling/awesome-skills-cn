---
name: arrowspace
description: "使用图拉普拉斯特征结构的谱向量搜索。当余弦/L2 相似度在你的嵌入中遗漏潜在结构时使用。"
category: data
risk: safe
source: community
source_repo: Genefold/arrowspace-skills
source_type: community
date_added: "2026-06-25"
author: Genefold AI
license: Apache-2.0
license_source: "https://github.com/Genefold/arrowspace-skills/blob/main/LICENSE"
tags: [vector-search, spectral-analysis, graph-laplacian, embeddings, lambda-tau]
tools: [claude, cursor, codex, gemini, opencode]
---

# ArrowSpace

用图拉普拉斯特征增强最近邻搜索的谱向量搜索。计算项图上的拉普拉斯矩阵，并使用 Rayleigh 商为每个项产生 λτ（lambda-tau）分数，使搜索既能尊重语义相似性又能尊重结构角色。

## 何时使用此技能

- 余弦或 L2 相似度在你的嵌入中遗漏潜在结构
- 你想要具有谱感知的基于图的检索
- 你需要表征嵌入空间的谱属性
- 你正在构建 RAG 管道，其中上下文角色与语义内容同样重要

## 工作原理

### 步骤 1：安装和导入

```bash
pip install arrowspace
```

```python
from arrowspace import ArrowSpaceBuilder
import numpy as np
```

### 步骤 2：准备数据

传递一个 (N, d) float64 NumPy 嵌入向量数组：

```python
items = np.array([[0.1, 0.2, 0.3],
                  [0.0, 0.5, 0.1],
                  [0.9, 0.1, 0.0]], dtype=np.float64)
```

### 步骤 3：配置图参数

```python
graph_params = {"eps": 0.2, "k": 6, "topk": 3, "p": 2.0, "sigma": 1.0}
builder = ArrowSpaceBuilder(items, graph_params=graph_params)
aspace = builder.build()
```

### 步骤 4：查询

```python
lambdas = aspace.lambdas()           # 按插入顺序索引的数组
sorted_res = aspace.lambdas_sorted()  # (分数, 索引) 对，升序排列
```

较高的 λτ 值表示既语义接近又结构上中心的项。

## 示例

### 示例 1：基本谱检索

```python
items = np.random.randn(100, 64).astype(np.float64)
builder = ArrowSpaceBuilder(items, graph_params={"eps": 0.5, "k": 10, "topk": 5, "p": 2.0, "sigma": None})
aspace = builder.build()
scores = aspace.lambdas()
top_indices = np.argsort(scores)[-5:]
```

### 示例 2：比较谱排序与余弦排序

```python
from sklearn.metrics.pairwise import cosine_similarity
cos_sim = cosine_similarity(items)
cosine_order = np.argsort(cos_sim[0])[::-1]
spectral_order = np.argsort(aspace.lambdas())[::-1]
```

## 最佳实践

- ✅ 在传递给 ArrowSpace 前将嵌入归一化到单位范数
- ✅ 从与 1/sqrt(dim) 成比例的 eps 开始，从那里调整
- ✅ 根据数据集大小在 3 到 25 之间使用 k（规则：N/50）
- ✅ 设置 sigma=None 以从距离分布自动选择内核宽度
- ❌ 不要与少于 10 个项一起使用（图结构没有意义）
- ❌ 不要用于实时流数据（ArrowSpace 是批量导向的）

## 限制

- 此技能不会替代特定环境的验证、测试或专家审查。
- ArrowSpace 是批量导向的，不设计用于流数据的实时索引。

## 常见陷阱

- **问题**：eps 过小，产生断开的图
  **解决方案**：增加 eps，或将其设置为与 1/sqrt(embedding_dim) 成比例

- **问题**：k 太大，产生密集图且谱特征淡化
  **解决方案**：对大多数数据集保持 k ≤ 25

## 相关技能

- `vector-database-engineer` — 一般向量数据库专业知识
- `embedding-strategies` — 嵌入模型选择和分块
- `similarity-search-patterns` — 语义搜索实现模式
- `hybrid-search-implementation` — 组合语义 + 关键词搜索
