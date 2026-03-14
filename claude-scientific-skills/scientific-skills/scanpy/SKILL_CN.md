---
name: scanpy
description: 标准单细胞RNA-seq分析流程。用于质量控制、归一化、降维（PCA/UMAP/t-SNE）、聚类、差异表达和可视化。最适合使用已建立工作流程的探索性scRNA-seq分析。对于深度学习模型使用scvi-tools；对于数据格式问题使用anndata。
license: SD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# Scanpy：单细胞分析

## 概述

Scanpy是一个基于AnnData构建的可扩展Python工具包，用于分析单细胞RNA-seq数据。应用此技能进行完整的单细胞工作流程，包括质量控制、归一化、降维、聚类、标记基因识别、可视化和轨迹分析。

## 何时使用此技能

当您需要以下操作时，应使用此技能：
- 分析单细胞RNA-seq数据（.h5ad、10X、CSV格式）
- 对scRNA-seq数据集执行质量控制
- 创建UMAP、t-SNE或PCA可视化
- 识别细胞簇并寻找标记基因
- 基于基因表达注释细胞类型
- 进行轨迹推断或伪时间分析
- 生成 publication 质量的单细胞图表

## 快速开始

### 基本导入和设置

```python
import scanpy as sc
import pandas as pd
import numpy as np

# 配置设置
sc.settings.verbosity = 3
sc.settings.set_figure_params(dpi=80, facecolor='white')
sc.settings.figdir = './figures/'
```

### 加载数据

```python
# 从10X Genomics
adata = sc.read_10x_mtx('path/to/data/')
adata = sc.read_10x_h5('path/to/data.h5')

# 从h5ad（AnnData格式）
adata = sc.read_h5ad('path/to/data.h5ad')

# 从CSV
adata = sc.read_csv('path/to/data.csv')
```

### 理解AnnData结构

AnnData对象是scanpy中的核心数据结构：

```python
adata.X          # 表达矩阵（细胞 × 基因）
adata.obs        # 细胞元数据（DataFrame）
adata.var        # 基因元数据（DataFrame）
adata.uns        # 非结构化注释（字典）
adata.obsm       # 多维细胞数据（PCA、UMAP）
adata.raw        # 原始数据备份

# 访问细胞和基因名称
adata.obs_names  # 细胞条形码
adata.var_names  # 基因名称
```

## 标准分析工作流程

### 1. 质量控制

识别并过滤低质量细胞和基因：

```python
# 识别线粒体基因
adata.var['mt'] = adata.var_names.str.startswith('MT-')

# 计算QC指标
sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], inplace=True)

# 可视化QC指标
sc.pl.violin(adata, ['n_genes_by_counts', 'total_counts', 'pct_counts_mt'],
             jitter=0.4, multi_panel=True)

# 过滤细胞和基因
sc.pp.filter_cells(adata, min_genes=200)
sc.pp.filter_genes(adata, min_cells=3)
adata = adata[adata.obs.pct_counts_mt < 5, :]  # 移除高MT%细胞
```

**使用QC脚本进行自动化分析：**
```bash
python scripts/qc_analysis.py input_file.h5ad --output filtered.h5ad
```

### 2. 归一化和预处理

```python
# 归一化到每个细胞10,000计数
sc.pp.normalize_total(adata, target_sum=1e4)

# 对数转换
sc.pp.log1p(adata)

# 保存原始计数供以后使用
adata.raw = adata

# 识别高可变基因
sc.pp.highly_variable_genes(adata, n_top_genes=2000)
sc.pl.highly_variable_genes(adata)

# 子集到高可变基因
adata = adata[:, adata.var.highly_variable]

# 回归掉不需要的变异
sc.pp.regress_out(adata, ['total_counts', 'pct_counts_mt'])

# 缩放数据
sc.pp.scale(adata, max_value=10)
```

### 3. 降维

```python
# PCA
sc.tl.pca(adata, svd_solver='arpack')
sc.pl.pca_variance_ratio(adata, log=True)  # 检查肘图

# 计算邻域图
sc.pp.neighbors(adata, n_neighbors=10, n_pcs=40)

# UMAP可视化
sc.tl.umap(adata)
sc.pl.umap(adata, color='leiden')

# 替代方案：t-SNE
sc.tl.tsne(adata)
```

### 4. 聚类

```python
# Leiden聚类（推荐）
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color='leiden', legend_loc='on data')

# 尝试多个分辨率以找到最佳粒度
for res in [0.3, 0.5, 0.8, 1.0]:
    sc.tl.leiden(adata, resolution=res, key_added=f'leiden_{res}')
```

### 5. 标记基因识别

```python
# 为每个簇找到标记基因
sc.tl.rank_genes_groups(adata, 'leiden', method='wilcoxon')

# 可视化结果
sc.pl.rank_genes_groups(adata, n_genes=25, sharey=False)
sc.pl.rank_genes_groups_heatmap(adata, n_genes=10)
sc.pl.rank_genes_groups_dotplot(adata, n_genes=5)

# 获取结果为DataFrame
markers = sc.get.rank_genes_groups_df(adata, group='0')
```

### 6. 细胞类型注释

```python
# 为已知细胞类型定义标记基因
marker_genes = ['CD3D', 'CD14', 'MS4A1', 'NKG7', 'FCGR3A']

# 可视化标记
sc.pl.umap(adata, color=marker_genes, use_raw=True)
sc.pl.dotplot(adata, var_names=marker_genes, groupby='leiden')

# 手动注释
cluster_to_celltype = {
    '0': 'CD4 T cells',
    '1': 'CD14+ Monocytes',
    '2': 'B cells',
    '3': 'CD8 T cells',
}
adata.obs['cell_type'] = adata.obs['leiden'].map(cluster_to_celltype)

# 可视化注释类型
sc.pl.umap(adata, color='cell_type', legend_loc='on data')
```

### 7. 保存结果

```python
# 保存处理后的数据
adata.write('results/processed_data.h5ad')

# 导出元数据
adata.obs.to_csv('results/cell_metadata.csv')
adata.var.to_csv('results/gene_metadata.csv')
```

## 常见任务

### 创建Publication质量的图表

```python
# 设置高质量默认值
sc.settings.set_figure_params(dpi=300, frameon=False, figsize=(5, 5))
sc.settings.file_format_figs = 'pdf'

# 带有自定义样式的UMAP
sc.pl.umap(adata, color='cell_type',
           palette='Set2',
           legend_loc='on data',
           legend_fontsize=12,
           legend_fontoutline=2,
           frameon=False,
           save='_publication.pdf')

# 标记基因热图
sc.pl.heatmap(adata, var_names=genes, groupby='cell_type',
              swap_axes=True, show_gene_labels=True,
              save='_markers.pdf')

# 点图
sc.pl.dotplot(adata, var_names=genes, groupby='cell_type',
              save='_dotplot.pdf')
```

请参考`references/plotting_guide.md`获取全面的可视化示例。

### 轨迹推断

```python
# PAGA（基于分区的图抽象）
sc.tl.paga(adata, groups='leiden')
sc.pl.paga(adata, color='leiden')

# 扩散伪时间
adata.uns['iroot'] = np.flatnonzero(adata.obs['leiden'] == '0')[0]
sc.tl.dpt(adata)
sc.pl.umap(adata, color='dpt_pseudotime')
```

### 条件间的差异表达

```python
# 比较细胞类型内的处理组与对照组
adata_subset = adata[adata.obs['cell_type'] == 'T cells']
sc.tl.rank_genes_groups(adata_subset, groupby='condition',
                         groups=['treated'], reference='control')
sc.pl.rank_genes_groups(adata_subset, groups=['treated'])
```

### 基因集评分

```python
# 对基因集表达进行细胞评分
gene_set = ['CD3D', 'CD3E', 'CD3G']
sc.tl.score_genes(adata, gene_set, score_name='T_cell_score')
sc.pl.umap(adata, color='T_cell_score')
```

### 批次校正

```python
# ComBat批次校正
sc.pp.combat(adata, key='batch')

# 替代方案：使用Harmony或scVI（单独的包）
```

## 关键参数调整

### 质量控制
- `min_genes`：每个细胞的最小基因数（通常为200-500）
- `min_cells`：每个基因的最小细胞数（通常为3-10）
- `pct_counts_mt`：线粒体阈值（通常为5-20%）

### 归一化
- `target_sum`：每个细胞的目标计数（默认1e4）

### 特征选择
- `n_top_genes`：HVG数量（通常为2000-3000）
- `min_mean`, `max_mean`, `min_disp`：HVG选择参数

### 降维
- `n_pcs`：主成分数量（检查方差比图）
- `n_neighbors`：邻居数量（通常为10-30）

### 聚类
- `resolution`：聚类粒度（0.4-1.2，越高=更多簇）

## 常见陷阱和最佳实践

1. **始终保存原始计数**：在过滤基因前使用`adata.raw = adata`
2. **仔细检查QC图**：根据数据集质量调整阈值
3. **使用Leiden而非Louvain**：更高效且结果更好
4. **尝试多个聚类分辨率**：找到最佳粒度
5. **验证细胞类型注释**：使用多个标记基因
6. **对基因表达图使用`use_raw=True`**：显示原始计数
7. **检查PCA方差比**：确定最佳PC数量
8. **保存中间结果**：长工作流程可能在中途失败

## 捆绑资源

### scripts/qc_analysis.py
自动化质量控制脚本，计算指标、生成图表并过滤数据：

```bash
python scripts/qc_analysis.py input.h5ad --output filtered.h5ad \
    --mt-threshold 5 --min-genes 200 --min-cells 3
```

### references/standard_workflow.md
完整的逐步工作流程，带有详细解释和代码示例：
- 数据加载和设置
- 带可视化的质量控制
- 归一化和缩放
- 特征选择
- 降维（PCA、UMAP、t-SNE）
- 聚类（Leiden、Louvain）
- 标记基因识别
- 细胞类型注释
- 轨迹推断
- 差异表达

从头执行完整分析时阅读此参考。

### references/api_reference.md
按模块组织的scanpy函数快速参考指南：
- 读取/写入数据（`sc.read_*`、`adata.write_*`）
- 预处理（`sc.pp.*`）
- 工具（`sc.tl.*`）
- 绘图（`sc.pl.*`）
- AnnData结构和操作
- 设置和实用程序

用于快速查找函数签名和常见参数。

### references/plotting_guide.md
全面的可视化指南，包括：
- 质量控制图
- 降维可视化
- 聚类可视化
- 标记基因图（热图、点图、小提琴图）
- 轨迹和伪时间图
- Publication质量定制
- 多面板图
- 颜色 palette 和样式

创建 publication 就绪图表时参考。

### assets/analysis_template.py
完整的分析模板，提供从数据加载到细胞类型注释的完整工作流程。复制并自定义此模板用于新分析：

```bash
cp assets/analysis_template.py my_analysis.py
# 编辑参数并运行
python my_analysis.py
```

模板包含所有标准步骤，带有可配置参数和有用的注释。

## 其他资源

- **官方scanpy文档**：https://scanpy.readthedocs.io/
- **Scanpy教程**：https://scanpy-tutorials.readthedocs.io/
- **scverse生态系统**：https://scverse.org/（相关工具：squidpy、scvi-tools、cellrank）
- **最佳实践**：Luecken & Theis (2019) "Current best practices in single-cell RNA-seq"

## 有效分析的提示

1. **从模板开始**：使用`assets/analysis_template.py`作为起点
2. **首先运行QC脚本**：使用`scripts/qc_analysis.py`进行初始过滤
3. **根据需要参考**：将工作流程和API参考加载到上下文中
4. **在聚类上迭代**：尝试多种分辨率和可视化方法
5. **生物学验证**：检查标记基因是否与预期细胞类型匹配
6. **记录参数**：记录QC阈值和分析设置
7. **保存检查点**：在关键步骤写入中间结果