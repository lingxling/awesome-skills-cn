---
name: anndata
description: 单细胞分析中注释矩阵的数据结构。在处理 .h5ad 文件或与 scverse 生态系统集成时使用。这是数据格式技能——用于分析工作流程使用 scanpy；用于概率模型使用 scvi-tools；用于群体规模查询使用 cellxgene-census。
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# AnnData

## 概述

AnnData 是一个用于处理注释数据矩阵的 Python 包，存储实验测量值（X）以及观察元数据（obs）、变量元数据（var）和多维注释（obsm、varm、obsp、varp、uns）。最初通过 Scanpy 为单细胞基因组学设计，现在作为任何需要高效存储、操作和分析的注释数据的通用框架。

## 何时使用此技能

在以下情况下使用此技能：
- 创建、读取或写入 AnnData 对象
- 处理 h5ad、zarr 或其他基因组学数据格式
- 执行单细胞 RNA-seq 分析
- 使用稀疏矩阵或支持模式管理大型数据集
- 连接多个数据集或实验批次
- 子集化、过滤或转换注释数据
- 与 scanpy、scvi-tools 或其他 scverse 生态系统工具集成

## 安装

```bash
uv pip install anndata

# 使用可选依赖项
uv pip install anndata[dev,test,doc]
```

## 快速开始

### 创建 AnnData 对象
```python
import anndata as ad
import numpy as np
import pandas as pd

# 最小创建
X = np.random.rand(100, 2000)  # 100 个细胞 × 2000 个基因
adata = ad.AnnData(X)

# 使用元数据
obs = pd.DataFrame({
    'cell_type': ['T cell', 'B cell'] * 50,
    'sample': ['A', 'B'] * 50
}, index=[f'cell_{i}' for i in range(100)])

var = pd.DataFrame({
    'gene_name': [f'Gene_{i}' for i in range(2000)]
}, index=[f'ENSG{i:05d}' for i in range(2000)])

adata = ad.AnnData(X=X, obs=obs, var=var)
```

### 读取数据
```python
# 读取 h5ad 文件
adata = ad.read_h5ad('data.h5ad')

# 使用支持模式读取（用于大文件）
adata = ad.read_h5ad('large_data.h5ad', backed='r')

# 读取其他格式
adata = ad.read_csv('data.csv')
adata = ad.read_loom('data.loom')
adata = ad.read_10x_h5('filtered_feature_bc_matrix.h5')
```

### 写入数据
```python
# 写入 h5ad 文件
adata.write_h5ad('output.h5ad')

# 使用压缩写入
adata.write_h5ad('output.h5ad', compression='gzip')

# 写入其他格式
adata.write_zarr('output.zarr')
adata.write_csvs('output_dir/')
```

### 基本操作
```python
# 按条件子集化
t_cells = adata[adata.obs['cell_type'] == 'T cell']

# 按索引子集化
subset = adata[0:50, 0:100]

# 添加元数据
adata.obs['quality_score'] = np.random.rand(adata.n_obs)
adata.var['highly_variable'] = np.random.rand(adata.n_vars) > 0.8

# 访问维度
print(f"{adata.n_obs} 个观察 × {adata.n_vars} 个变量")
```

## 核心功能

### 1. 数据结构

了解 AnnData 对象结构，包括 X、obs、var、layers、obsm、varm、obsp、varp、uns 和 raw 组件。

**请参阅**：`references/data_structure.md` 获取关于以下内容的全面信息：
- 核心组件（X、obs、var、layers、obsm、varm、obsp、varp、uns、raw）
- 从各种来源创建 AnnData 对象
- 访问和操作数据组件
- 内存高效实践

### 2. 输入/输出操作

以各种格式读取和写入数据，支持压缩、支持模式和云存储。

**请参阅**：`references/io_operations.md` 获取以下内容的详细信息：
- 本机格式（h5ad、zarr）
- 替代格式（CSV、MTX、Loom、10X、Excel）
- 大型数据集的支持模式
- 远程数据访问
- 格式转换
- 性能优化

常用命令：
```python
# 读取/写入 h5ad
adata = ad.read_h5ad('data.h5ad', backed='r')
adata.write_h5ad('output.h5ad', compression='gzip')

# 读取 10X 数据
adata = ad.read_10x_h5('filtered_feature_bc_matrix.h5')

# 读取 MTX 格式
adata = ad.read_mtx('matrix.mtx').T
```

### 3. 连接

使用灵活的连接策略沿观察或变量连接多个 AnnData 对象。

**请参阅**：`references/concatenation.md` 获取以下内容的全面覆盖：
- 基本连接（axis=0 用于观察，axis=1 用于变量）
- 连接类型（内连接、外连接）
- 合并策略（相同、唯一、第一个、仅）
- 使用标签跟踪数据源
- 延迟连接（AnnCollection）
- 大型数据集的磁盘连接

常用命令：
```python
# 连接观察（组合样本）
adata = ad.concat(
    [adata1, adata2, adata3],
    axis=0,
    join='inner',
    label='batch',
    keys=['batch1', 'batch2', 'batch3']
)

# 连接变量（组合模态）
adata = ad.concat([adata_rna, adata_protein], axis=1)

# 延迟连接
from anndata.experimental import AnnCollection
collection = AnnCollection(
    ['data1.h5ad', 'data2.h5ad'],
    join_obs='outer',
    label='dataset'
)
```

### 4. 数据操作

高效地转换、子集化、过滤和重新组织数据。

**请参阅**：`references/manipulation.md` 获取以下内容的详细指导：
- 子集化（按索引、名称、布尔掩码、元数据条件）
- 转置
- 复制（完整副本 vs 视图）
- 重命名（观察、变量、类别）
- 类型转换（字符串到分类、稀疏/密集）
- 添加/删除数据组件
- 重新排序
- 质量控制过滤

常用命令：
```python
# 按元数据子集化
filtered = adata[adata.obs['quality_score'] > 0.8]
hv_genes = adata[:, adata.var['highly_variable']]

# 转置
adata_T = adata.T

# 复制 vs 视图
view = adata[0:100, :]  # 视图（轻量级引用）
copy = adata[0:100, :].copy()  # 独立副本

# 将字符串转换为分类
adata.strings_to_categoricals()
```

### 5. 最佳实践

遵循推荐的模式以实现内存效率、性能和可重复性。

**请参阅**：`references/best_practices.md` 获取以下内容的指南：
- 内存管理（稀疏矩阵、分类、支持模式）
- 视图 vs 副本
- 数据存储优化
- 性能优化
- 使用原始数据
- 元数据管理
- 可重复性
- 错误处理
- 与其他工具集成
- 常见陷阱和解决方案

关键建议：
```python
# 对稀疏数据使用稀疏矩阵
from scipy.sparse import csr_matrix
adata.X = csr_matrix(adata.X)

# 将字符串转换为分类
adata.strings_to_categoricals()

# 对大文件使用支持模式
adata = ad.read_h5ad('large.h5ad', backed='r')

# 过滤前存储原始数据
adata.raw = adata.copy()
adata = adata[:, adata.var['highly_variable']]
```

## 与 Scverse 生态系统集成

AnnData 作为 scverse 生态系统的基础数据结构：

### Scanpy（单细胞分析）
```python
import scanpy as sc

# 预处理
sc.pp.filter_cells(adata, min_genes=200)
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)

# 降维
sc.pp.pca(adata, n_comps=50)
sc.pp.neighbors(adata, n_neighbors=15)
sc.tl.umap(adata)
sc.tl.leiden(adata)

# 可视化
sc.pl.umap(adata, color=['cell_type', 'leiden'])
```

### Muon（多模态数据）
```python
import muon as mu

# 组合 RNA 和蛋白质数据
mdata = mu.MuData({'rna': adata_rna, 'protein': adata_protein})
```

### PyTorch 集成
```python
from anndata.experimental import AnnLoader

# 为深度学习创建 DataLoader
dataloader = AnnLoader(adata, batch_size=128, shuffle=True)

for batch in dataloader:
    X = batch.X
    # 训练模型
```

## 常见工作流程

### 单细胞 RNA-seq 分析
```python
import anndata as ad
import scanpy as sc

# 1. 加载数据
adata = ad.read_10x_h5('filtered_feature_bc_matrix.h5')

# 2. 质量控制
adata.obs['n_genes'] = (adata.X > 0).sum(axis=1)
adata.obs['n_counts'] = adata.X.sum(axis=1)
adata = adata[adata.obs['n_genes'] > 200]
adata = adata[adata.obs['n_counts'] < 50000]

# 3. 存储原始数据
adata.raw = adata.copy()

# 4. 标准化和过滤
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)
adata = adata[:, adata.var['highly_variable']]

# 5. 保存处理后的数据
adata.write_h5ad('processed.h5ad')
```

### 批次集成
```python
# 加载多个批次
adata1 = ad.read_h5ad('batch1.h5ad')
adata2 = ad.read_h5ad('batch2.h5ad')
adata3 = ad.read_h5ad('batch3.h5ad')

# 使用批次标签连接
adata = ad.concat(
    [adata1, adata2, adata3],
    label='batch',
    keys=['batch1', 'batch2', 'batch3'],
    join='inner'
)

# 应用批次校正
import scanpy as sc
sc.pp.combat(adata, key='batch')

# 继续分析
sc.pp.pca(adata)
sc.pp.neighbors(adata)
sc.tl.umap(adata)
```

### 处理大型数据集
```python
# 以支持模式打开
adata = ad.read_h5ad('100GB_dataset.h5ad', backed='r')

# 基于元数据过滤（无数据加载）
high_quality = adata[adata.obs['quality_score'] > 0.8]

# 加载过滤后的子集
adata_subset = high_quality.to_memory()

# 处理子集
process(adata_subset)

# 或分块处理
chunk_size = 1000
for i in range(0, adata.n_obs, chunk_size):
    chunk = adata[i:i+chunk_size, :].to_memory()
    process(chunk)
```

## 故障排除

### 内存不足错误
使用支持模式或转换为稀疏矩阵：
```python
# 支持模式
adata = ad.read_h5ad('file.h5ad', backed='r')

# 稀疏矩阵
from scipy.sparse import csr_matrix
adata.X = csr_matrix(adata.X)
```

### 文件读取缓慢
使用压缩和适当的格式：
```python
# 优化存储
adata.strings_to_categoricals()
adata.write_h5ad('file.h5ad', compression='gzip')

# 使用 Zarr 进行云存储
adata.write_zarr('file.zarr', chunks=(1000, 1000))
```

### 索引对齐问题
始终在索引上对齐外部数据：
```python
# 错误
adata.obs['new_col'] = external_data['values']

# 正确
adata.obs['new_col'] = external_data.set_index('cell_id').loc[adata.obs_names, 'values']
```

## 其他资源

- **官方文档**：https://anndata.readthedocs.io/
- **Scanpy 教程**：https://scanpy.readthedocs.io/
- **Scverse 生态系统**：https://scverse.org/
- **GitHub 存储库**：https://github.com/scverse/anndata
