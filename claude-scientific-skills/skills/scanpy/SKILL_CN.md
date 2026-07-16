---
name: scanpy
description: 标准单细胞RNA-seq分析流程。用于QC、归一化、降维（PCA/UMAP/t-SNE）、聚类、差异表达、可视化，以及将Seurat或SingleCellExperiment RDS文件等R友好型单细胞格式转换为h5ad以供Scanpy使用。最适合使用成熟工作流程的探索性scRNA-seq分析。深度学习模型使用scvi-tools；数据格式问题使用anndata。
license: BSD-3-Clause
metadata: {"version": "1.3", "skill-author": "K-Dense Inc."}
---

# Scanpy：单细胞分析

## 概述

Scanpy是一个基于AnnData构建的可扩展Python工具包，用于分析单细胞RNA-seq数据。应用此技能进行完整的单细胞工作流程，包括质量控制、归一化、降维、聚类、标记基因识别、可视化和轨迹分析。当前稳定版本：**scanpy 1.12.x**（2026年1月）。

## 安装

需要 Python **3.12+**（scanpy 1.12 已停止支持 Python 3.11 及更早版本）以及 anndata **≥0.10**。

```bash
uv pip install "scanpy[leiden]"
```

`[leiden]` 附加包会安装 `python-igraph` 和 `leidenalg`，这是 Leiden 聚类所必需的。为保证环境可复现，建议固定版本号：`uv pip install "scanpy[leiden]==1.12.1"`。

对于大型或核外（out-of-core）数据集，许多函数支持 [Dask](https://docs.dask.org/) 数组（实验性）：

```bash
uv pip install "scanpy[leiden]" dask
```

参见 [在Scanpy中使用dask](https://scanpy.scverse.org/en/stable/tutorials/experimental/dask.html) 教程。对于GPU加速的scanpy风格操作，请使用独立的 [rapids-singlecell](https://rapids-singlecell.readthedocs.io/) 软件包。

如果输入是R原生的单细胞对象（`.rds`、`.RData`、Seurat 或 SingleCellExperiment），请先用R工具将其转换为 `.h5ad`，再用Scanpy加载。有关在 macOS、Linux 和 Windows 上由代理执行的安装和转换说明，请阅读 `references/r_interop.md`。

有关AnnData结构和I/O细节，请使用 **anndata** 技能。有关概率模型和批次校正，请使用 **scvi-tools** 技能。

## 何时使用此技能

当您需要以下操作时，应使用此技能：
- 分析单细胞RNA-seq数据（.h5ad、10X、CSV格式）
- 处理需要转换为 `.h5ad` 的R友好型单细胞数据集（`.rds`、`.RData`、Seurat、SingleCellExperiment）
- 对scRNA-seq数据集执行质量控制
- 创建UMAP、t-SNE或PCA可视化
- 识别细胞簇并寻找标记基因
- 基于基因表达注释细胞类型
- 进行轨迹推断或伪时间分析
- 生成 publication 质量的单细胞图表

## 脚本工具集（优先于从零编写代码）

本技能在 `scripts/` 中为每个常见步骤都内置了可直接运行的CLI脚本。**优先运行这些脚本，而不是手写scanpy代码**——它们能根据扩展名处理文件加载、图表配置、合理的默认值、原始计数的保留以及进度日志记录。每个脚本都读写 `.h5ad`，因此它们可以串联使用，并且各自都有 `--help`。只有在脚本无法覆盖某个任务、或需要非常规定制时，才需要直接编写scanpy代码。

所有脚本共用一个 `scripts/_common.py` 辅助模块（加载、保存、图表配置）——请将它与其他脚本放在一起。从技能目录运行，或传入完整路径；图表默认输出到 `./figures/`。

| 脚本 | 作用 | 典型调用 |
|--------|---------|--------------|
| `run_pipeline.py` | **一条命令完成完整流程**：加载 → QC → 归一化 → HVG → PCA → （批次校正）→ UMAP → Leiden → 标记基因 | `python scripts/run_pipeline.py raw.h5ad -o processed.h5ad` |
| `inspect_data.py` | 汇总未知数据集（形状、obs/var、layers、已计算的内容、原始与归一化状态） | `python scripts/inspect_data.py data.h5ad` |
| `convert.py` | 加载任意格式（10x目录/.h5、csv、loom、mtx）并写出 `.h5ad` | `python scripts/convert.py 10x_dir/ -o data.h5ad` |
| `qc_analysis.py` | QC指标、前后对比图、过滤、可选的Scrublet双细胞检测 | `python scripts/qc_analysis.py raw.h5ad -o qc.h5ad --scrublet` |
| `preprocess.py` | 归一化、log1p、HVG、可选的缩放/回归（保留 `counts` layer + `raw`） | `python scripts/preprocess.py qc.h5ad -o norm.h5ad` |
| `reduce_dimensions.py` | PCA + 方差图、邻域图、UMAP、可选的t-SNE | `python scripts/reduce_dimensions.py norm.h5ad -o red.h5ad` |
| `batch_correct.py` | 整合方法：harmony / bbknn / combat | `python scripts/batch_correct.py red.h5ad -o int.h5ad --method harmony --batch-key sample` |
| `cluster.py` | 单个或多个分辨率下的Leiden（或louvain）聚类 | `python scripts/cluster.py red.h5ad -o clu.h5ad --resolution 0.3 0.6 1.0` |
| `find_markers.py` | `rank_genes_groups` + 分组CSV + 标记基因图 | `python scripts/find_markers.py clu.h5ad --groupby leiden -o clu.h5ad` |
| `annotate.py` | 从JSON/CSV映射簇 → 细胞类型；可选生成标记参考点图 | `python scripts/annotate.py clu.h5ad -o ann.h5ad --mapping map.json` |
| `score_genes.py` | 对基因特征集（JSON）和/或细胞周期阶段进行评分 | `python scripts/score_genes.py ann.h5ad -o scored.h5ad --gene-sets sigs.json` |
| `pseudobulk.py` | 按样本 × 细胞类型聚合计数 → 供pydeseq2使用的矩阵 | `python scripts/pseudobulk.py ann.h5ad --by sample cell_type --out-prefix pb` |
| `subset.py` | 按obs值或基因列表取子集（可选清除过时的嵌入） | `python scripts/subset.py ann.h5ad -o tcells.h5ad --obs cell_type --keep "T cells"` |
| `plot.py` | 从已处理的对象生成umap/tsne/pca/violin/dotplot/heatmap等图 | `python scripts/plot.py ann.h5ad --kind dotplot --genes CD3D CD14 --groupby cell_type` |

### 一键端到端运行

```bash
# 计数矩阵 → 已聚类并标注了标记基因的对象 + 图表 + 标记基因CSV
python scripts/run_pipeline.py raw.h5ad -o processed.h5ad \
    --resolution 0.5 --n-top-genes 2000 --scrublet
# 带多样本整合：
python scripts/run_pipeline.py raw.h5ad -o processed.h5ad --batch-key sample --batch-method harmony
# 通过JSON实现可复现的参数配置（键名与flag名对应，用下划线代替连字符）：
python scripts/run_pipeline.py raw.h5ad -o processed.h5ad --config params.json
```

### 逐步链式调用（需要在各阶段之间检查/迭代时使用）

```bash
python scripts/qc_analysis.py        raw.h5ad  -o qc.h5ad   --scrublet
python scripts/preprocess.py         qc.h5ad   -o norm.h5ad --n-top-genes 2000
python scripts/reduce_dimensions.py  norm.h5ad -o red.h5ad  --n-pcs 40
python scripts/cluster.py            red.h5ad  -o clu.h5ad  --resolution 0.3 0.5 0.8
python scripts/find_markers.py       clu.h5ad  -o clu.h5ad  --groupby leiden --use-raw
# 检查 results/markers/*.csv，确定标签，编写映射JSON，然后：
python scripts/annotate.py           clu.h5ad  -o ann.h5ad  --mapping celltypes.json
```

以下各节记录了每个脚本背后调用的scanpy函数——当需要超出脚本参数范围的定制时请阅读。

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
sc.settings.autosave = True  # 优先于逐图的save=参数（在scanpy 1.12中已弃用）
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

对于R原生文件，不要尝试在Python中直接解析Seurat的 `.rds`。请先进行转换：

```bash
# 有关安装R和转换所需软件包的说明，参见 references/r_interop.md。
Rscript convert_rds_to_h5ad.R input.rds output.h5ad
```

```python
adata = sc.read_h5ad('output.h5ad')
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

**双细胞（doublet）检测（可选，在归一化前对原始计数执行）：**

```python
sc.pp.scrublet(adata)  # 自scanpy 1.10起为核心API（此前位于scanpy.external.pp）
adata = adata[~adata.obs['predicted_doublet'], :].copy()
```

**使用QC脚本进行自动化分析**（从技能目录运行，或传入完整路径）：

```bash
python skills/scanpy/scripts/qc_analysis.py input_file.h5ad --output filtered.h5ad
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

`rank_genes_groups` 仅应用于**探索性的簇标记基因**分析。由于细胞并非独立观测值，逐细胞的统计检验会使p值虚高。对于条件或样本之间严谨的差异表达分析，应先进行伪批量（pseudobulk）处理（见下文），再使用 **pydeseq2** 等工具。

```python
# 为每个簇找到标记基因（探索性）
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

保存图表时优先使用 `sc.settings.autosave` 和 `sc.settings.figdir`。在scanpy 1.12中，逐图的 `save=` 参数已被弃用。

```python
# 设置高质量默认值
sc.settings.set_figure_params(dpi=300, frameon=False, figsize=(5, 5))
sc.settings.file_format_figs = 'pdf'
sc.settings.figdir = './figures/'
sc.settings.autosave = True

# 带有自定义样式的UMAP（通过autosave保存为figures/umap.pdf）
sc.pl.umap(adata, color='cell_type',
           palette='Set2',
           legend_loc='on data',
           legend_fontsize=12,
           legend_fontoutline=2,
           frameon=False)

# 标记基因热图
sc.pl.heatmap(adata, var_names=genes, groupby='cell_type',
              swap_axes=True, show_gene_labels=True)

# 点图
sc.pl.dotplot(adata, var_names=genes, groupby='cell_type')
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

### 条件间的伪批量与差异表达

按样本和细胞类型进行伪批量处理，然后使用规范的差异表达工具（如pydeseq2），而不是逐细胞的 `rank_genes_groups`：

```python
# 按样本和细胞类型聚合计数（scanpy 1.12中兼容dask）
pb = sc.get.aggregate(
    adata,
    by=['sample', 'cell_type'],
    func='sum',
    layer='counts',  # 如果有，使用原始计数layer
)
# 下游：导出pb，使用pydeseq2进行条件比较
```

对于簇内的快速探索性比较，`rank_genes_groups` 是可以接受的，但要谨慎解读p值：

```python
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
3. **使用Leiden聚类**：`sc.tl.louvain` 在scanpy 1.12中已被弃用
4. **尝试多个聚类分辨率**：找到最佳粒度
5. **验证细胞类型注释**：使用多个标记基因
6. **对基因表达图使用`use_raw=True`**：显示来自`.raw`的归一化计数
7. **检查PCA方差比**：确定最佳PC数量
8. **保存中间结果**：长工作流程可能在中途失败
9. **差异表达使用伪批量**：不要将`rank_genes_groups`的p值当作条件间严谨的差异表达结果
10. **通过设置保存图表**：使用`sc.settings.autosave`而不是绘图函数中已弃用的`save=`
11. **在使用Scanpy前转换R对象**：使用R软件包将Seurat或SingleCellExperiment的`.rds`文件转换为`.h5ad`，并保留计数、元数据和基因标识符

## 捆绑资源

### scripts/（CLI工具集）
一套可组合的、以 `.h5ad` 为输入输出的脚本，覆盖整个工作流程，并附带一条命令即可完成的端到端流程。完整的表格和链式调用示例参见上面的**脚本工具集**一节。每个脚本都有 `--help`。文件列表：

- `_common.py` — 供其他脚本导入的共享加载/保存/图表配置辅助模块（不是CLI）
- `run_pipeline.py` — 一条命令完成完整流程（通过flag或`--config` JSON配置）
- `inspect_data.py`、`convert.py` — 探查并加载/转换任意输入格式
- `qc_analysis.py`、`preprocess.py`、`reduce_dimensions.py`、`batch_correct.py`、`cluster.py` — 流程各步骤
- `find_markers.py`、`annotate.py`、`score_genes.py`、`pseudobulk.py` — 标记基因、注释、评分、差异表达准备
- `subset.py`、`plot.py` — 按元数据/基因取子集；生成任意标准图表

**在从零编写scanpy代码之前，优先使用这些脚本。**

### references/standard_workflow.md
完整的逐步工作流程，带有详细解释和代码示例：
- 数据加载和设置
- 带可视化的质量控制
- 归一化和缩放
- 特征选择
- 降维（PCA、UMAP、t-SNE）
- 聚类（Leiden）
- 双细胞检测（scrublet）与伪批量聚合
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

### references/r_interop.md
供代理执行的操作手册，涵盖在 macOS、Linux 和 Windows 上安装R、安装CRAN/Bioconductor转换软件包、检查`.rds`/`.RData`输入、将Seurat或SingleCellExperiment对象转换为`.h5ad`，以及在Scanpy中验证转换结果。

### assets/analysis_template.py
完整的分析模板，提供从数据加载到细胞类型注释的完整工作流程。复制并自定义此模板用于新分析：

```bash
cp assets/analysis_template.py my_analysis.py
# 编辑参数并运行
python my_analysis.py
```

模板包含所有标准步骤，带有可配置参数和有用的注释。

### assets/ JSON模板
可直接编辑并传入使用的模板，无需从零编写配置/映射文件：
- `assets/pipeline_config.json` — 供`run_pipeline.py --config`使用的参数集
- `assets/celltype_mapping.json` — 供`annotate.py --mapping`使用的簇 → 细胞类型映射
- `assets/gene_signatures.json` — 供`score_genes.py --gene-sets`使用的基因集特征

## 其他资源

- **官方scanpy文档**：https://scanpy.scverse.org/en/stable/
- **Scanpy教程**：https://scanpy.scverse.org/en/stable/tutorials/index.html
- **发布说明**：https://scanpy.scverse.org/en/stable/release-notes/index.html
- **scverse生态系统**：https://scverse.org/（相关工具：squidpy、scvi-tools、cellrank）
- **R互操作性**：https://www.bioconductor.org/packages/release/bioc/html/zellkonverter.html 和 https://mojaveazure.github.io/seurat-disk/
- **最佳实践**：Luecken & Theis (2019) "Current best practices in single-cell RNA-seq"

## 有效分析的提示

1. **从模板开始**：使用`assets/analysis_template.py`作为起点
2. **首先运行QC脚本**：使用`scripts/qc_analysis.py`进行初始过滤
3. **根据需要参考**：将工作流程和API参考加载到上下文中
4. **在聚类上迭代**：尝试多种分辨率和可视化方法
5. **生物学验证**：检查标记基因是否与预期细胞类型匹配
6. **记录参数**：记录QC阈值和分析设置
7. **保存检查点**：在关键步骤写入中间结果
