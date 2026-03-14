---
name: scvi-tools
description: 用于单细胞组学的深度生成模型。当需要概率性批次校正（scVI）、迁移学习、带不确定性的差异表达或多模态整合（TOTALVI、MultiVI）时使用。最适用于高级建模、批次效应、多模态数据。标准分析流程请使用 scanpy。
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# scvi-tools

## 概述

scvi-tools 是一个用于单细胞基因组学中概率模型的综合 Python 框架。它基于 PyTorch 和 PyTorch Lightning 构建，使用变分推断提供深度生成模型，用于分析多种单细胞数据模态。

## 何时使用此技能

当以下情况时使用此技能：
- 分析单细胞 RNA-seq 数据（降维、批次校正、整合）
- 处理单细胞 ATAC-seq 或染色质可及性数据
- 整合多模态数据（CITE-seq、多组学、配对/非配对数据集）
- 分析空间转录组学数据（反卷积、空间映射）
- 对单细胞数据执行差异表达分析
- 进行细胞类型注释或迁移学习任务
- 处理专门的单细胞模态（甲基化、细胞术、RNA 速度）
- 构建用于单细胞分析的自定义概率模型

## 核心功能

scvi-tools 提供按数据模态组织的模型：

### 1. 单细胞 RNA-seq 分析
用于表达分析、批次校正和整合的核心模型。请参阅 `references/models-scrna-seq.md`：
- **scVI**：无监督降维和批次校正
- **scANVI**：半监督细胞类型注释和整合
- **AUTOZI**：零膨胀检测和建模
- **VeloVI**：RNA 速度分析
- **contrastiveVI**：扰动效应隔离

### 2. 染色质可及性（ATAC-seq）
用于分析单细胞染色质数据的模型。请参阅 `references/models-atac-seq.md`：
- **PeakVI**：基于峰的 ATAC-seq 分析和整合
- **PoissonVI**：定量片段计数建模
- **scBasset**：带有基序分析的深度学习方法

### 3. 多模态和多组学整合
多种数据类型的联合分析。请参阅 `references/models-multimodal.md`：
- **totalVI**：CITE-seq 蛋白质和 RNA 联合建模
- **MultiVI**：配对和非配对多组学整合
- **MrVI**：多分辨率跨样本分析

### 4. 空间转录组学
空间解析转录组学分析。请参阅 `references/models-spatial.md`：
- **DestVI**：多分辨率空间反卷积
- **Stereoscope**：细胞类型反卷积
- **Tangram**：空间映射和整合
- **scVIVA**：细胞-环境关系分析

### 5. 专门模态
其他专门分析工具。请参阅 `references/models-specialized.md`：
- **MethylVI/MethylANVI**：单细胞甲基化分析
- **CytoVI**：流式/质谱细胞术批次校正
- **Solo**：双细胞检测
- **CellAssign**：基于标记的细胞类型注释

## 典型工作流

所有 scvi-tools 模型遵循一致的 API 模式：

```python
# 1. 加载和预处理数据（AnnData 格式）
import scvi
import scanpy as sc

adata = scvi.data.heart_cell_atlas_subsampled()
sc.pp.filter_genes(adata, min_counts=3)
sc.pp.highly_variable_genes(adata, n_top_genes=1200)

# 2. 向模型注册数据（指定层、协变量）
scvi.model.SCVI.setup_anndata(
    adata,
    layer="counts",  # 使用原始计数，而非对数标准化
    batch_key="batch",
    categorical_covariate_keys=["donor"],
    continuous_covariate_keys=["percent_mito"]
)

# 3. 创建和训练模型
model = scvi.model.SCVI(adata)
model.train()

# 4. 提取潜在表示和标准化值
latent = model.get_latent_representation()
normalized = model.get_normalized_expression(library_size=1e4)

# 5. 存储在 AnnData 中用于下游分析
adata.obsm["X_scVI"] = latent
adata.layers["scvi_normalized"] = normalized

# 6. 使用 scanpy 进行下游分析
sc.pp.neighbors(adata, use_rep="X_scVI")
sc.tl.umap(adata)
sc.tl.leiden(adata)
```

**关键设计原则：**
- **需要原始计数**：模型期望未标准化的计数数据以获得最佳性能
- **统一 API**：所有模型的一致接口（设置 → 训练 → 提取）
- **以 AnnData 为中心**：与 scanpy 生态系统无缝集成
- **GPU 加速**：自动利用可用的 GPU
- **批次校正**：通过协变量注册处理技术变异

## 常见分析任务

### 差异表达
使用学习到的生成模型进行概率性 DE 分析：

```python
de_results = model.differential_expression(
    groupby="cell_type",
    group1="TypeA",
    group2="TypeB",
    mode="change",  # 使用复合假设检验
    delta=0.25      # 最小效应大小阈值
)
```

请参阅 `references/differential-expression.md` 了解详细方法和解释。

### 模型持久化
保存和加载训练好的模型：

```python
# 保存模型
model.save("./model_directory", overwrite=True)

# 加载模型
model = scvi.model.SCVI.load("./model_directory", adata=adata)
```

### 批次校正和整合
跨批次或研究整合数据集：

```python
# 注册批次信息
scvi.model.SCVI.setup_anndata(adata, batch_key="study")

# 模型自动学习批次校正的表示
model = scvi.model.SCVI(adata)
model.train()
latent = model.get_latent_representation()  # 批次校正后的
```

## 理论基础

scvi-tools 基于：
- **变分推断**：用于可扩展贝叶斯推断的近似后验分布
- **深度生成模型**：学习复杂数据分布的 VAE 架构
- **摊销推断**：跨细胞高效学习的共享神经网络
- **概率建模**：原则性不确定性量化和统计检验

请参阅 `references/theoretical-foundations.md` 了解数学框架的详细背景。

## 其他资源

- **工作流**：`references/workflows.md` 包含常见工作流、最佳实践、超参数调优和 GPU 优化
- **模型参考**：`references/` 目录中每个模型类别的详细文档
- **官方文档**：https://docs.scvi-tools.org/en/stable/
- **教程**：https://docs.scvi-tools.org/en/stable/tutorials/index.html
- **API 参考**：https://docs.scvi-tools.org/en/stable/api/index.html

## 安装

```bash
uv pip install scvi-tools
# 用于 GPU 支持
uv pip install scvi-tools[cuda]
```

## 最佳实践

1. **使用原始计数**：始终向模型提供未标准化的计数数据
2. **过滤基因**：分析前移除低计数基因（例如，`min_counts=3`）
3. **注册协变量**：在 `setup_anndata` 中包含已知的技术因素（批次、供体等）
4. **特征选择**：使用高可变基因以提高性能
5. **模型保存**：始终保存训练好的模型以避免重新训练
6. **GPU 使用**：为大型数据集启用 GPU 加速（`accelerator="gpu"`）
7. **Scanpy 集成**：将输出存储在 AnnData 对象中用于下游分析