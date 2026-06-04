---
name: anndata
description: 单细胞分析中注释矩阵的数据结构。当处理.h5ad文件或与scverse生态系统集成时使用。这是数据格式技能——分析工作流请使用scanpy；概率模型请使用scvi-tools；群体规模查询请使用cellxgene-census。
license: BSD-3-Clause license
metadata:
  version: "1.0"
  skill-author: K-Dense Inc.
---






# AnnData

## 概述

AnnData 是一个用于处理注释数据矩阵的 Python 包，存储实验测量值（X）以及观测元数据（obs）、变量元数据（var）和多维注释（obsm、varm、obsp、varp、uns）。最初为单细胞基因组学通过 Scanpy 设计，现在作为通用框架用于任何需要高效存储、操作和分析的注释数据。

## 何时使用此技能

在以下情况下使用此技能：
- 创建、读取或写入 AnnData 对象
- 使用 h5ad、zarr 或其他基因组数据格式
- 执行单细胞 RNA-seq 分析
- 使用稀疏矩阵或后端模式管理大型数据集
- 串联多个数据集或实验批次
- 对注释数据进行子集筛选、过滤或转换
- 与 scanpy、scvi-tools 或其他 scverse 生态系统工具集成

## 安装

需要 Python 3.11+（anndata 0.11+ 放弃了对 3.9 的支持）。当前稳定版本：0.12.x。

```bash
uv pip install anndata

# 惰性 I/O 和 dask 支持的操作
uv pip install "anndata[dask,lazy]"

# 开发/文档（贡献者）
uv pip install "anndata[dev,test,doc]"
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

# 带元数据
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
# 本地格式（read_h5ad/read_zarr 保持在顶层）
adata = ad.read_h5ad('data.h5ad')
adata = ad.read_h5ad('large_data.h5ad', backed='r')  # 大文件的惰性加载
adata = ad.read_zarr('data.zarr')

# 其他格式：优先使用 anndata.io（顶层导入已弃用）
from anndata.io import read_csv, read_loom, read_mtx

adata = read_csv('data.csv')
adata = read_loom('data.loom')

# 10X Genomics：使用 scanpy（不是 anndata）— 参见 scanpy 技能
import scanpy as sc
adata = sc.read_10x_h5('filtered_feature_bc_matrix.h5')
adata = sc.read_10x_mtx('filtered_feature_bc_matrix/')
```

### 写入数据
```python
# 写入 h5ad 文件
adata.write_h5ad('output.h5ad')

# 写入带压缩
adata.write_h5ad('output.h5ad', compression='gzip')

# 写入其他格式
adata.write_zarr('output.zarr')
adata.write_csvs('output_dir/')
```

### 基本操作
```python
# 按条件子集筛选
t_cells = adata[adata.obs['cell_type'] == 'T cell']

# 按索引子集筛选
subset = adata[0:50, 0:100]

# 添加元数据
adata.obs['quality_score'] = np.random.rand(adata.n_obs)
adata.var['highly_variable'] = np.random.rand(adata.n_vars) > 0.8

# 访问维度
print(f"{adata.n_obs} 观测 × {adata.n_vars} 变量")
```

## 核心能力

### 1. 数据结构

了解 AnnData 对象结构，包括 X、obs、var、layers、obsm、varm、obsp、varp、uns 和 raw 组件。

**参见**：`references/data_structure.md` 获取全面信息：
- 核心组件（X、obs、var、layers、obsm、varm、obsp、varp、uns、raw）
- 从各种来源创建 AnnData 对象
- 访问和操作数据组件
- 内存效率实践

### 2. 输入/输出操作

以各种格式读写数据，支持压缩、后端模式和云存储。

**参见**：`references/io_operations.md` 了解详情：
- 本地格式（h5ad、zarr）
- 替代格式（CSV、MTX、Loom、10X、Excel）
- 大数据集的后端模式
- 远程数据访问
- 格式转换
- 性能优化

常用命令：
```python
from anndata.io import read_mtx

# 读写 h5ad
adata = ad.read_h5ad('data.h5ad', backed='r')
adata.write_h5ad('output.h5ad', compression='gzip')

# 10X Genomics（通过 scanpy）
import scanpy as sc
adata = sc.read_10x_h5('filtered_feature_bc_matrix.h5')

# 读取 MTX 格式
adata = read_mtx('matrix.mtx').T
```

### 3. 串联

沿观测或变量灵活连接策略组合多个 AnnData 对象。

**参见**：`references/concatenation.md` 获取全面覆盖：
- 基本串联（axis=0 用于观测，axis=1 用于变量）
- 连接类型（inner、outer）
- 合并策略（same、unique、first、only）
- 使用标签跟踪数据来源
- 惰性串联（AnnCollection）
- 大数据集的磁盘串联

常用命令：
```python
# 串联观测（合并样本）
adata = ad.concat(
    [adata1, adata2, adata3],
    axis=0,
    join='inner',
    label='batch',
    keys=['batch1', 'batch2', 'batch3']
)

# 串联变量（合并模态）
adata = ad.concat([adata_rna, adata_protein], axis=1)

# 惰性串联
from anndata.experimental import AnnCollection
collection = AnnCollection(
    ['data1.h5ad', 'data2.h5ad'],
    join_obs='outer',
    label='dataset'
)
```

### 4. 数据操作

高效地转换、子集筛选、过滤和重组数据。

**参见**：`references/manipulation.md` 获取详细指导：
- 子集筛选（按索引、名称、布尔掩码、元数据条件）
- 转置
- 复制（完整副本 vs 视图）
- 重命名（观测、变量、类别）
- 类型转换（字符串到分类变量、稀疏/密集）
- 添加/删除数据组件
- 重新排序
- 质量控制过滤

常用命令：
```python
# 按元数据子集筛选
filtered = adata[adata.obs['quality_score'] > 0.8]
hv_genes = adata[:, adata.var['highly_variable']]

# 转置
adata_T = adata.T

# 副本 vs 视图
view = adata[0:100, :]  # 视图（轻量级引用）
copy = adata[0:100, :].copy()  # 独立副本

# 字符串转换为分类变量
adata.strings_to_categoricals()
```

### 5. 最佳实践

遵循推荐的模式以提高内存效率、性能和可重现性。

**参见**：`references/best_practices.md` 获取指导：
- 内存管理（稀疏矩阵、分类变量、后端模式）
- 副本 vs 视图
- 数据存储优化
- 性能优化
- 原始数据工作
- 元数据管理
- 可重现性
- 错误处理
- 与其他工具集成
- 常见陷阱和解决方案

关键建议：
```python
# 对稀疏数据使用稀疏矩阵
from scipy.sparse import csr_matrix
adata.X = csr_matrix(adata.X)

# 字符串转换为分类变量
adata.strings_to_categoricals()

# 对大文件使用后端模式
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

# 合并 RNA 和蛋白质数据
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

# 1. 加载数据（10X 通过 scanpy；anndata 原生处理 h5ad/zarr）
adata = sc.read_10x_h5('filtered_feature_bc_matrix.h5')

# 2. 质量控制
adata.obs['n_genes'] = (adata.X > 0).sum(axis=1)
adata.obs['n_counts'] = adata.X.sum(axis=1)
adata = adata[adata.obs['n_genes'] > 200]
adata = adata[adata.obs['n_counts'] < 50000]

# 3. 存储原始数据
adata.raw = adata.copy()

# 4. 归一化和过滤
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)
adata = adata[:, adata.var['highly_variable']]

# 5. 保存处理后的数据
adata.write_h5ad('processed.h5ad')
```

### 批次整合
```python
# 加载多个批次
adata1 = ad.read_h5ad('batch1.h5ad')
adata2 = ad.read_h5ad('batch2.h5ad')
adata3 = ad.read_h5ad('batch3.h5ad')

# 带批次标签串联
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

## 故障排除

### 内存不足错误
- **问题**：处理大型数据集时内存不足
- **解决**：
  - 使用 `adata.to_memory()` 强制将数据加载到内存
  - 处理数据子集
  - 使用 `chunked` 读取大型文件
  - 考虑使用 `vaex` 进行超大型数据

### 文件读取缓慢
- **问题**：读取大型 h5ad 文件很慢
- **解决**：
  - 使用 `adata = adata.copy()` 创建副本
  - 压缩原始数据
  - 使用 `lgbm` 后端进行更快读取

### 索引对齐问题
- **问题**：X 和 obs 的索引不对齐
- **解决**：
  - 使用 `adata.copy()` 确保对齐
  - 显式设置索引：`adata.obs_names = [...]`
  - 检查并修复重复的索引

## 其他资源

- [AnnData 文档](https://anndata.readthedocs.io/)
- [Scanpy 教程](https://scanpy.readthedocs.io/)
- [AnnData API 参考](https://anndata.readthedocs.io/en/latest/api.html)
