---
name: scvelo
description: 使用 scVelo 进行 RNA 速度分析。从未剪接/已剪接 mRNA 动力学估计细胞状态转变，推断轨迹方向，计算潜在时间，并在单细胞 RNA-seq 数据中识别驱动基因。补充 Scanpy/scVI-tools 用于轨迹推断。
license: BSD-3-Clause
metadata:
    skill-author: Kuan-lin Huang
---

# scVelo — RNA 速度分析

## 概述

scVelo 是用于单细胞 RNA-seq 数据中 RNA 速度分析的领先 Python 包。它通过建模 mRNA 剪接的动力学来推断细胞状态转变 — 使用未剪接（前体 mRNA）与已剪接（成熟 mRNA）丰度的比率来确定每个细胞中基因是上调还是下调。这允许重建发育轨迹并识别细胞命运决定，而无需时间序列数据。

**安装：** `pip install scvelo`

**关键资源：**
- 文档：https://scvelo.readthedocs.io/
- GitHub：https://github.com/theislab/scvelo
- 论文：Bergen et al. (2020) Nature Biotechnology. PMID: 32747759

## 何时使用此技能

当以下情况时使用 scVelo：

- **从快照数据推断轨迹**：确定细胞分化的方向
- **细胞命运预测**：识别祖细胞及其下游命运
- **驱动基因识别**：找到其动力学最能解释观察到的轨迹的基因
- **发育生物学**：建模造血、神经发生、上皮-间充质转变
- **潜在时间估计**：沿着从剪接动力学导出的伪时间对细胞进行排序
- **补充 Scanpy**：向 UMAP 嵌入添加方向信息

## 前提条件

scVelo 需要**未剪接**和**已剪接** RNA 的计数矩阵。这些由以下工具生成：
1. **STARsolo** 或 **kallisto|bustools**（使用 `lamanno` 模式）
2. **velocyto** CLI：`velocyto run10x` / `velocyto run`
3. **alevin-fry** / **simpleaf**（带剪接/未剪接输出）

数据存储在带有 `layers["spliced"]` 和 `layers["unspliced"]` 的 `AnnData` 对象中。

## 标准 RNA 速度工作流

### 1. 设置和数据加载

```python
import scvelo as scv
import scanpy as sc
import numpy as np
import matplotlib.pyplot as plt

# 配置设置
scv.settings.verbosity = 3       # 显示计算步骤
scv.settings.presenter_view = True
scv.settings.set_figure_params('scvelo')

# 加载数据（带有剪接/未剪接层的 AnnData）
# 选项 A：从 loom 加载（velocyto 输出）
adata = scv.read("cellranger_output.loom", cache=True)

# 选项 B：将 velocyto loom 与 Scanpy 处理的 AnnData 合并
adata_processed = sc.read_h5ad("processed.h5ad")  # 有 UMAP、聚类
adata_velocity = scv.read("velocyto.loom")
adata = scv.utils.merge(adata_processed, adata_velocity)

# 验证层
print(adata)
# obs × var: N × G
# layers: 'spliced', 'unspliced' (必需)
# obsm['X_umap'] (可视化必需)
```

### 2. 预处理

```python
# 过滤和标准化（遵循 Scanpy 约定）
scv.pp.filter_and_normalize(
    adata,
    min_shared_counts=20,   # 剪接+未剪接中的最小计数
    n_top_genes=2000        # 顶部高可变基因
)

# 计算一阶和二阶矩（均值和方差）
# 必须先计算 knn_connectivities
sc.pp.neighbors(adata, n_neighbors=30, n_pcs=30)
scv.pp.moments(
    adata,
    n_pcs=30,
    n_neighbors=30
)
```

### 3. 速度估计 — 随机模型

随机模型速度快，适合探索性分析：

```python
# 随机速度（更快，准确性较低）
scv.tl.velocity(adata, mode='stochastic')
scv.tl.velocity_graph(adata)

# 可视化
scv.pl.velocity_embedding_stream(
    adata,
    basis='umap',
    color='leiden',
    title="RNA Velocity (Stochastic)"
)
```

### 4. 速度估计 — 动力学模型（推荐）

动力学模型拟合完整的剪接动力学，更准确：

```python
# 恢复动力学（计算密集型；10K 细胞约 10-30 分钟）
scv.tl.recover_dynamics(adata, n_jobs=4)

# 从动力学模型计算速度
scv.tl.velocity(adata, mode='dynamical')
scv.tl.velocity_graph(adata)
```

### 5. 潜在时间

动力学模型启用共享潜在时间（伪时间）的计算：

```python
# 计算潜在时间
scv.tl.latent_time(adata)

# 在 UMAP 上可视化潜在时间
scv.pl.scatter(
    adata,
    color='latent_time',
    color_map='gnuplot',
    size=80,
    title='Latent time'
)

# 识别按潜在时间排序的顶部基因
top_genes = adata.var['fit_likelihood'].sort_values(ascending=False).index[:300]
scv.pl.heatmap(
    adata,
    var_names=top_genes,
    sortby='latent_time',
    col_color='leiden',
    n_convolve=100
)
```

### 6. 驱动基因分析

```python
# 识别速度拟合最高的基因
scv.tl.rank_velocity_genes(adata, groupby='leiden', min_corr=0.3)
df = scv.DataFrame(adata.uns['rank_velocity_genes']['names'])
print(df.head(10))

# 速度和一致性
scv.tl.velocity_confidence(adata)
scv.pl.scatter(
    adata,
    c=['velocity_length', 'velocity_confidence'],
    cmap='coolwarm',
    perc=[5, 95]
)

# 特定基因的相位图
scv.pl.velocity(adata, ['Cpe', 'Gnao1', 'Ins2'],
               ncols=3, figsize=(16, 4))
```

### 7. 速度箭头和伪时间

```python
# UMAP 上的箭头图
scv.pl.velocity_embedding(
    adata,
    arrow_length=3,
    arrow_size=2,
    color='leiden',
    basis='umap'
)

# 流图（更清晰的可视化）
scv.pl.velocity_embedding_stream(
    adata,
    basis='umap',
    color='leiden',
    smooth=0.8,
    min_mass=4
)

# 速度伪时间（潜在时间的替代方案）
scv.tl.velocity_pseudotime(adata)
scv.pl.scatter(adata, color='velocity_pseudotime', cmap='gnuplot')
```

### 8. PAGA 轨迹图

```python
# 带速度信息转换的 PAGA 图
scv.tl.paga(adata, groups='leiden')
df = scv.get_df(adata, 'paga/transitions_confidence', precision=2).T
df.style.background_gradient(cmap='Blues').format('{:.2g}')

# 绘制带速度的 PAGA
scv.pl.paga(
    adata,
    basis='umap',
    size=50,
    alpha=0.1,
    min_edge_width=2,
    node_size_scale=1.5
)
```

## 完整工作流脚本

```python
import scvelo as scv
import scanpy as sc

def run_rna_velocity(adata, n_top_genes=2000, mode='dynamical', n_jobs=4):
    """
    完整的 RNA 速度工作流。

    参数：
        adata: 带有 'spliced' 和 'unspliced' 层的 AnnData，UMAP 在 obsm 中
        n_top_genes: 用于速度的顶部 HVG 数量
        mode: 'stochastic'（快速）或 'dynamical'（准确）
        n_jobs: 动力学模型的并行作业数

    返回：
        带有速度信息的处理后 AnnData
    """
    scv.settings.verbosity = 2

    # 1. 预处理
    scv.pp.filter_and_normalize(adata, min_shared_counts=20, n_top_genes=n_top_genes)

    if 'neighbors' not in adata.uns:
        sc.pp.neighbors(adata, n_neighbors=30)

    scv.pp.moments(adata, n_pcs=30, n_neighbors=30)

    # 2. 速度估计
    if mode == 'dynamical':
        scv.tl.recover_dynamics(adata, n_jobs=n_jobs)

    scv.tl.velocity(adata, mode=mode)
    scv.tl.velocity_graph(adata)

    # 3. 下游分析
    if mode == 'dynamical':
        scv.tl.latent_time(adata)
        scv.tl.rank_velocity_genes(adata, groupby='leiden', min_corr=0.3)

    scv.tl.velocity_confidence(adata)
    scv.tl.velocity_pseudotime(adata)

    return adata
```

## AnnData 中的关键输出字段

运行工作流后，添加以下字段：

| 位置 | 键 | 描述 |
|----------|-----|-------------|
| `adata.layers` | `velocity` | 每个细胞每个基因的 RNA 速度 |
| `adata.layers` | `fit_t` | 每个细胞每个基因的拟合潜在时间 |
| `adata.obsm` | `velocity_umap` | UMAP 上的 2D 速度向量 |
| `adata.obs` | `velocity_pseudotime` | 来自速度的伪时间 |
| `adata.obs` | `latent_time` | 来自动力学模型的潜在时间 |
| `adata.obs` | `velocity_length` | 每个细胞的速度 |
| `adata.obs` | `velocity_confidence` | 每个细胞的置信度评分 |
| `adata.var` | `fit_likelihood` | 基因水平模型拟合质量 |
| `adata.var` | `fit_alpha` | 转录率 |
| `adata.var` | `fit_beta` | 剪接率 |
| `adata.var` | `fit_gamma` | 降解率 |
| `adata.uns` | `velocity_graph` | 细胞-细胞转换概率矩阵 |

## 速度模型比较

| 模型 | 速度 | 准确性 | 何时使用 |
|-------|-------|----------|-------------|
| `stochastic` | 快速 | 中等 | 探索性；大型数据集 |
| `deterministic` | 中等 | 中等 | 简单线性动力学 |
| `dynamical` | 缓慢 | 高 | 发表质量；识别驱动基因 |

## 最佳实践

- **从随机模式开始**进行探索；切换到动力学模式进行最终分析
- **需要良好的未剪接读取覆盖**：短读取（< 100 bp）可能错过内含子覆盖
- **最少 2,000 个细胞**：RNA 速度在细胞较少时噪声大
- **速度应一致**：箭头应遵循已知生物学；随机性表明存在问题
- **k-NN 带宽很重要**：邻居太少 → 速度噪声大；太多 → 过度平滑
- **健全性检查**：根细胞（祖细胞）应具有高未剪接/剪接比率的标记基因
- **动力学模型需要不同的动力学状态**：最适合清晰的分化过程

## 故障排除

| 问题 | 解决方案 |
|---------|---------|
| 缺少未剪接层 | 重新运行 velocyto 或使用带有 `--soloFeatures Gene Velocyto` 的 STARsolo |
| 很少的速度基因 | 降低 `min_shared_counts`；检查测序深度 |
| 看起来随机的箭头 | 尝试不同的 `n_neighbors` 或速度模型 |
| 动力学模型的内存错误 | 设置 `n_jobs=1`；减少 `n_top_genes` |
| 到处都是负速度 | 检查剪接/未剪接层是否未交换 |

## 其他资源

- **scVelo 文档**：https://scvelo.readthedocs.io/
- **教程笔记本**：https://scvelo.readthedocs.io/tutorials/
- **GitHub**：https://github.com/theislab/scvelo
- **论文**：Bergen V et al. (2020) Nature Biotechnology. PMID: 32747759
- **velocyto**（预处理）：http://velocyto.org/
- **CellRank**（命运预测，扩展 scVelo）：https://cellrank.readthedocs.io/
- **dynamo**（代谢标记替代方案）：https://dynamo-release.readthedocs.io/