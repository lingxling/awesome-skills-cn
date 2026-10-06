---
name: scvelo
description: 使用 scVelo 对剪接和未剪接的单细胞RNA计数进行RNA速率分析。拟合确定性或动态模型，检查基因相位图，构建速率图，估计相对潜伏时间，并对速率相关基因进行排序。用于在Scanpy基础上进行方向性轨迹假设和动态模型诊断；仅凭速率无法确立细胞命运或因果驱动因素。
license: BSD-3-Clause
compatibility: Requires Python 3.13 for the tested stack with scvelo 0.3.4, scanpy 1.12.4, anndata 0.13.4, numpy 2.5.3 and pandas 2.3.3. Loom import requires loompy. Local H5AD analysis needs no network or credentials. The default stochastic solver is incompatible with NumPy 2.
metadata:
  version: "2.0"
  skill-author: Kuan-lin Huang
  last-reviewed: "2026-10-01"
---

# scVelo RNA 速率分析

## 何时使用

用于对齐后的剪接/未剪接RNA计数进行动态学分析、方向性轨迹假设、
基因级相位图，以及动态潜伏时间分析。有关假设、转移概率以及可选的
CellRank交接，请使用[模型参考文档](references/velocity_models.md)。

RNA速率是在某个模型下估计的表达量导数。平滑的箭头并不是观测到的
细胞运动、谱系追踪、因果驱动因素，或未来命运的证明。动态估计器在
每一个数据集上都不会自动比稳态估计器更准确。

## 经过测试的环境与兼容性

维护中的工作流针对的是在Python 3.13上的scVelo **0.3.4**、Scanpy
**1.12.4**、AnnData **0.13.4**、NumPy **2.5.3**、pandas **2.3.3**、
SciPy **1.18.1**、Matplotlib **3.11.2** 以及loompy **3.0.8**。使用
一个隔离的环境：

```bash
uv venv --python 3.13 .venv-velocity
uv pip install --python .venv-velocity/bin/python \
  scvelo==0.3.4 scanpy==1.12.4 anndata==0.13.4 numpy==2.5.3 \
  pandas==2.3.3 scipy==1.18.1 matplotlib==3.11.2 loompy==3.0.8
```

以上软件包是从缓存解析并在一个隔离的 `uv` 环境中测试的；上面的
shell路径使用POSIX语法。安装需要网络访问，除非软件包已被缓存。
不需要API密钥。

- **确定性模型和动态模型：** 原生合成拟合、图谱、相对时间、绘图
  以及H5AD往返读写均已在此技术栈上测试。
- **随机模型：** scVelo 0.3.4默认的GLS标量赋值在NumPy 2下会失败。
  Scanpy 1.12需要NumPy 2，因此在当前Scanpy旁安装 `numpy<2` 并不是
  一个解决方案。需要一个单独经过验证的旧版Scanpy/NumPy环境；该旧
  版技术栈在本次审查中未被执行。该辅助工具会在修改数据之前拒绝
  这种组合，而不会改变模型本身。
- **pandas 3：** scVelo 0.3.4的动态拟合和一些绘图使用的操作已不再
  受pandas 3支持。请保持显式的pandas版本固定。
- 上游稳定版教程中仍包含已被移除的 `scv.read` 和更旧的预处理调用。
  当教程与已安装的API不一致时，请检查
  [0.3.4源代码](https://github.com/theislab/scvelo/tree/v0.3.4)。

## 输入契约

1. 从一个支持速率分析的量化工具获取剪接和未剪接计数。保留量化
   工具/版本、参考注释、计数模式、样本ID以及细胞条码映射关系。
   上游量化过程不在本随附脚本的范围内。
2. 在 `adata.layers['spliced']` 和 `adata.layers['unspliced']` 中
   提供**细胞x基因**矩阵，两者要有相同的细胞/基因顺序和唯一的ID。
   计数必须是有限且非负的；允许分数形式的计数估计值。永远不要将
   对数化、缩放、残差化或批次校正后的数值当作计数使用。仅凭数值
   检查无法确立数据是原始数据。
3. 在拟合之前检查每个文库/聚类的覆盖度、双细胞、环境RNA、零计数
   细胞以及注释兼容性。保留原始的完整基因计数文件。保留部分基因
   的备份文件无法保留被过滤掉的基因。
4. 在合并文件时明确解析条码前缀和基因标识符。不要悄悄地剥离文库
   ID、交集掉大多数细胞，或者在不理解重复原因的情况下将重复的
   生物学ID变为唯一。

通过AnnData读取H5AD。scVelo 0.3.4没有 `scv.read` 或
`scv.DataFrame`：

```python
import anndata as ad
adata = ad.read_h5ad("velocity_counts.h5ad")
```

对于遗留的loom输入，使用 `ad.io.read_loom('counts.loom',
X_name='spliced', sparse=True)`。AnnData 0.13已弃用loom；进一步
处理请转换为H5AD。它的 `layers[None]` 是 `X` 的别名：不要删除它，
也不要像每个键都是字符串那样遍历所有layers。该辅助工具只访问具名
的速率layers。原生loom读取以及精确的、重新排序后的元数据对齐已
被测试覆盖；未使用AnnData 0.13的 `write_loom`。

## 运行维护中的工作流

[随附脚本](scripts/rna_velocity_workflow.py)接受本地文件，启动时
从不下载演示数据集：

```bash
MPLBACKEND=Agg .venv-velocity/bin/python scripts/rna_velocity_workflow.py \
  velocity_counts.h5ad --mode dynamical --groupby clusters \
  --n-top-genes 2000 --n-neighbors 30 --n-jobs 1 --output-dir velocity_results

# 导入一个loom文件，并将其原始计数与一个已有的注释文件对齐：
MPLBACKEND=Agg .venv-velocity/bin/python scripts/rna_velocity_workflow.py \
  counts.loom --processed-h5ad annotated.h5ad --groupby clusters \
  --mode deterministic --output-dir velocity_check
```

从技能目录下运行这些命令。输入文件名和生物学注释均为示意性内容；
相同的CLI和函数已在小型生成的动态学测试数据上进行了测试。当没有
注释可用时，省略 `--groupby`。使用 `--no-plots` 可在不计算UMAP的
情况下进行分析。

该辅助工具执行以下步骤：

1. 验证layers、ID、模型兼容性和分组；拒绝先前已生成的moments/
   velocity，以防止预处理悄悄地运行两次。
2. 将保留的原始layers备份为 `spliced_counts` 和
   `unspliced_counts`，并从原始剪接计数重建 `X`。过滤基因，并在
   线性尺度上对 `X` 和这两个计数layers进行归一化。
3. 对 `X` **且仅对X**应用 `sc.pp.log1p`，用Scanpy选择高变异基因，
   并在子集化之后重建PCA和邻居图。重复使用来自不相关特征集的过时
   PCA/邻居图可能会悄悄改变速率模型。
4. 从显式的Scanpy图中，用
   `scv.pp.moments(adata, n_neighbors=None)` 计算 `Ms` 和
   `Mu`。Moments是稠密的：要为多个细胞x基因数组预留内存预算，而
   不仅仅是稀疏的输入数据。
5. 对于动态模式，在对选定基因调用
   `velocity(mode='dynamical')` 之前，先对其调用
   `recover_dynamics(var_names='all')`；否则拟合所选的模型。要求
   有可用的基因以及一个非空的速率图。
6. 计算速率一致性和速率伪时间；只为动态拟合添加潜伏时间。只有
   当存在至少两个组且每组至少两个细胞时，才对速率相关基因进行
   排序。在 `uns['velocity_workflow']['diagnostics']` 中记录/
   警告非有限或恒定的时间/一致性输出；恒定的伪时间不支持轨迹
   排序。排序是探索性的。
7. 对于绘图，从重建后的图重新计算UMAP，投影速率，将PNG直接保存到
   请求的目录，然后保存带有软件包版本和所选参数的H5AD文件。现有
   的标签仍然只是注释，不是经过验证的细胞身份。

这个Python函数会就地修改其参数；如果要保留原始对象，请传入
`adata.copy()`。CLI会写入 `output_dir/adata_velocity.h5ad`。版本2
有意改变了先前辅助工具的行为：重建了原始layer的几何结构，缺失的
请求标签会报错，并且可以显式控制绘图和并行度。运行时取决于细胞
数、基因数和拟合难度；并不存在一个通用的10–30分钟预期值。

## 在解读之前检查证据

在一次动态运行之后（数据集特定的基因选择为示意性内容）：

```python
import pandas as pd
import scvelo as scv

# 候选动态学基因，不是经实验证实的驱动因素。
candidates = adata.var['fit_likelihood'].dropna().nlargest(6).index.tolist()
scv.pl.velocity(adata, var_names=candidates, basis='umap', show=False)

# 这是对组相关速率的排序，不是因果影响或条件差异表达。
scv.tl.rank_velocity_genes(adata, groupby='clusters', min_corr=0.3)
ranked = pd.DataFrame(adata.uns['rank_velocity_genes']['names'])

scv.tl.velocity_confidence(adata)
scv.pl.scatter(adata, color=['velocity_length', 'velocity_confidence'], show=False)
```

检查剪接与未剪接的相位图、诱导和抑制阶段的覆盖情况、拟合参数、
失败/NaN拟合，以及分支特异性动态学。检查对基因集、邻居数、子
抽样以及模型假设的敏感性。在可用的情况下，使用时间序列标签、
扰动、谱系追踪或标记实验作为独立的方向性证据。仅凭一个看起来合理
的UMAP无法验证一次拟合，而调参直到箭头符合某个预期叙事，也不是
一种验证策略。

不存在一个通用的2,000细胞最小值、通用的未剪接比例，或"根细胞必须
具有最高未剪接/剪接比例"的规则。相关动态学状态的覆盖情况和测量
质量才是重要的。负速率可能代表抑制或模型错误指定；它本身并不是
layers被调换的证据。

## 输出解读

| 字段 | 解读 |
| --- | --- |
| `layers['velocity']` | 在处理后的基因表达空间中由模型估计的导数 |
| `var['velocity_genes']` | 被选中用于速率图的基因；与所有HVG不同 |
| `layers['Ms']`、`layers['Mu']` | 邻居平均后的线性尺度剪接/未剪接表达量 |
| `layers['fit_t']` | 基因特异的拟合时间坐标，仅动态模型 |
| `var['fit_alpha/beta/gamma']` | 模型推断尺度上的拟合速率；不是经过校准的物理速率 |
| `var['fit_likelihood']` | 相对的模型拟合诊断值；不是生物学真实性的后验概率 |
| `uns['velocity_graph']` | 候选转移的稀疏正余弦相关值；不是行随机的 |
| `obsm['velocity_umap']` | 投影后的向量，只有在计算/绘制嵌入之后才存在 |
| `obs['velocity_pseudotime']` | 基于图的相对排序 |
| `obs['latent_time']` | 耦合的动态排序；通常缩放到0–1，不是实际经过的小时数 |
| `obs['velocity_length']` | 处理后空间中的向量大小；不是物理细胞速度 |
| `obs['velocity_confidence']` | 邻居速率一致性，不是经过校准的不确定性 |

对于命运概率，使用一个显式归一化的转移核以及一个经过验证的终末
状态定义；参见参考文档中可选的CellRank示例。PAGA需要可选的igraph
和兼容的Scanpy内部实现；它不是经过测试的核心工作流的一部分，也不
能替代命运推断。

## 故障排查

| 问题 | 操作 |
| --- | --- |
| Layers缺失或不匹配 | 重新检查量化过程和显式的ID对齐；X不能替代未剪接计数 |
| 速率基因非常少 | 在更改阈值之前检查深度、状态覆盖和相位图 |
| 箭头平滑但不合理 | 检查模型假设、批次几何结构和单个基因；与独立证据对比 |
| 拟合结果非有限或图为空 | 停止解读并调查退化的特征/覆盖情况 |
| 内存或拟合时间过高 | 使用一个经论证的基因集和`n_jobs=1`；考虑稠密moments和拟合数组的开销 |
| NumPy 2上的随机模型失败 | 使用一个单独经过验证的兼容旧版技术栈，或明确重新考虑模型选择 |
| 拟合/绘图时的pandas `unique`错误 | 使用经过测试的pandas 2.3.3固定版本 |

## 来源与验证范围

于2026-10-01针对[已发布的源代码](https://github.com/theislab/scvelo/tree/v0.3.4)、
[API](https://scvelo.readthedocs.io/en/latest/api.html)、
[动态模型注意事项](https://scvelo.readthedocs.io/en/latest/perspectives/Perspectives.html)
以及[AnnData loom读取器](https://anndata.readthedocs.io/en/stable/generated/anndata.io.read_loom.html)
进行了复核。主要论文是
[Bergen et al., 2020](https://doi.org/10.1038/s41587-020-0591-3)。
合成执行测试验证的是软件契约以及文件/图表生成；它们不能确立生物
学准确性、可辨识性，或特定数据集的参数恢复能力。可选的CellRank/
PAGA分析仍然是经过源代码审查的示意性扩展。未使用任何经过认证的
远程服务。
