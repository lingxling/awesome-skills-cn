---
name: scvi-tools
description: 拟合单细胞组学的概率模型，包括 scVI 批次整合、scANVI 注释、totalVI CITE-seq、MultiVI RNA/ATAC 整合以及后验差异表达。适用于生成式建模、参考映射、多模态分析或基于模型的不确定性；标准预处理和探索性分析请使用 scanpy。
license: BSD-3-Clause license
compatibility: 需要 Python 3.12+ 以及带有模型特定依赖的 scvi-tools。支持 CPU；加速器要求取决于 PyTorch 和硬件。安装或可选的数据集/基因组下载需要网络访问，本地模型拟合则不需要。
metadata:
  version: "1.4"
  skill-author: K-Dense Inc.
  last-reviewed: "2026-10-01"
  upstream-version: "1.5.1"
---

# scvi-tools

面向 **scvi-tools 1.5.1**，发布于 2026 年 9 月 10 日。以下 API 已对照带标签的源代码和官方文档进行核对。示例是示意性的：
仓库测试执行了针对 SCVI、SCANVI、TOTALVI、MULTIVI、METHYLVI、PEAKVI 和 POISSONVI 的简短 CPU 合成拟合，以及保持计数的预处理、DE 输出契约、保存/加载和最小化（minification）。测试所用的软件栈为 Python 3.13、Scanpy 1.12.4、AnnData 0.13.4、MuData 0.4.1、PyTorch 2.14.1 和 Lightning 2.6.6。长时间训练、特定硬件的路径以及其他专门的工作流仍属示意性；这些检查并不确立收敛性或生物学有效性。

## 选择模型及其输入契约

| 任务 | 类 | 必需的输入 |
| --- | --- | --- |
| RNA 整合 | `scvi.model.SCVI` | 未归一化的 RNA 计数 |
| RNA 注释 | `scvi.model.SCANVI` | 计数和部分标签 |
| CITE-seq | `scvi.model.TOTALVI` | RNA 和蛋白质计数，细胞对齐 |
| RNA + ATAC 整合 | `scvi.model.MULTIVI` | 已注册的 MuData，且模态表示已对齐 |
| ATAC 可及性 | `scvi.model.PEAKVI` | 细胞 × 峰，二值/计数可及性 |
| 定量 ATAC | `scvi.external.POISSONVI` | 区域水平的片段计数 |
| 甲基化 | `scvi.external.METHYLVI`、`METHYLANVI` | 含甲基化和总覆盖度计数的 MuData |
| 细胞术 | `scvi.external.CYTOVI` | 经变换的蛋白质强度 |
| 大型跨系统效应 | `scvi.external.SysVI` | 经归一化、对数变换的表达 |
| RNA 速率 | `scvi.external.VELOVI` | 经预处理的剪接/未剪接丰度 |

计数规则因模型而异：不要将原始 RNA 计数输入 SysVI，也不要用比率替换甲基化覆盖度。同样，切勿通过对数归一化数据取指数来重建计数。请保留实测计数和预处理的来源出处。

在使用专门的模型之前，请阅读相应的参考资料：

- [RNA models](references/models-scrna-seq.md)：SCVI、SCANVI、AUTOZI、VELOVI、
  ContrastiveVI、CellAssign、SOLO、LinearSCVI、AmortizedLDA。
- [ATAC models](references/models-atac-seq.md)：PEAKVI、POISSONVI、SCBASSET。
- [Multimodal models](references/models-multimodal.md)：TOTALVI、TOTALANVI、
  MULTIVI、MRVI、DIAGVI。
- [Spatial models](references/models-spatial.md)：CondSCVI/DestVI、Stereoscope、
  Tangram、GIMVI、SCVIVA、RESOLVI。
- [Specialized models](references/models-specialized.md)：甲基化、
  细胞术、SysVI、Decipher。

**发布边界：** 包括 `JaxSCVI` 在内的 JAX 支持已在 1.5 中移除。
`scvi.model.mlxSCVI` 仍是一个单独的可选 Apple 芯片实现；
PyTorch MPS 和 MLX 是不同的后端。空间模型和 DIAGVI 在 1.5.1 中仍可导入，但上游将其后续维护转交给
[scVIVA-tools](https://scviva-tools.readthedocs.io/en/latest/)。此处固定的兼容性示例仅用于现有的 scvi-tools 工作流。

## 工作流程

1. 确认模态、原始数据的来源出处、唯一的细胞/特征 ID、特征顺序、批次/样本元数据以及预期的生物学比较。
2. 在模型注册之前执行质控和特征选择。对计数层使用感知计数的 HVG 选择，并保留全基因计数对象，以供所选特征集之外的后续分析使用。
3. 使用该模型的 `setup_anndata` 或 `setup_mudata` 注册确切的数据对象；创建并训练模型。Setup 是注册，而不是归一化。
4. 检查验证历史、留出集拟合、种子稳定性、批次混合**以及**已知生物学的保留。仅有混合良好的 UMAP 并不能验证整合。
5. 提取表示或模型特定的归一化输出；保存模型、数据、所选特征顺序、软件版本、种子和训练参数。

### 示意性的 RNA 工作流

假设 `rna_counts.h5ad` 在 `.X` 中包含实测的、未归一化的计数，且 `obs['batch']` 无缺失。请在此代码块之前为该实验选择质控阈值。

```python
import numpy as np
import scanpy as sc
import scvi
from scipy import sparse

scvi.settings.seed = 0
adata = sc.read_h5ad("rna_counts.h5ad")
assert adata.obs_names.is_unique and adata.var_names.is_unique
assert adata.obs["batch"].notna().all()
x = adata.X
values = x.data if sparse.issparse(x) else np.asarray(x)
assert np.isfinite(values).all() and (values >= 0).all()
assert np.allclose(values, np.rint(values))
assert (np.asarray(x.sum(axis=1)).ravel() > 0).all()
adata.layers["counts"] = x.copy()
sc.pp.filter_genes(adata, min_cells=3)
sc.pp.highly_variable_genes(
    adata, layer="counts", flavor="seurat_v3", batch_key="batch",
    n_top_genes=min(2000, adata.n_vars), subset=True,
)
adata = adata.copy()
assert (np.asarray(adata.layers["counts"].sum(axis=1)).ravel() > 0).all()
scvi.model.SCVI.setup_anndata(adata, layer="counts", batch_key="batch")
model = scvi.model.SCVI(adata, n_latent=20, gene_likelihood="nb")
model.train(max_epochs=400, early_stopping=True)
adata.obsm["X_scVI"] = model.get_latent_representation()
sc.pp.neighbors(adata, use_rep="X_scVI")
sc.tl.umap(adata)
sc.tl.leiden(adata, flavor="igraph", n_iterations=2, directed=False)
model.save("scvi_model", save_anndata=True)
```

`seurat_v3` 需要 scikit-misc（通过 scvi-tools 的 Scanpy 依赖一并包含）；
使用 `flavor='igraph'` 的 Leiden 需要 igraph。极小或退化的数据集可能使 HVG 局部回归失败；请降低特征选择的目标，检查数据质量，并且不要通过更改计数层来掩盖该失败。

计数的有效性并不证明计数的来源出处。如果过滤使某个细胞的所有表达都被移除，请在 setup 之前移除该细胞或修订特征选择。不要自动将条件、组织或供体作为干扰协变量加入：它们可能编码了正在研究的生物学信号，而混杂无法仅靠注册来修复。

注册与特征顺序、层和类别编码绑定。请在 setup 之前完成过滤。如果训练对象发生变化，请重新注册并初始化新模型；对于已训练的参考，请使用专用的查询映射方法，而不是就地更改其注册表。

### 输出与差异表达

```python
# SCVI 归一化表达：可能为稠密的细胞 × 基因矩阵。
normalized = model.get_normalized_expression(
    gene_list=adata.var_names[:20].tolist(), library_size=1e4,
    n_samples=25, return_mean=True,
)
# 该比较以拟合的模型和所选基因为条件。
de = model.differential_expression(
    groupby="cell_type", group1="TypeA", group2="TypeB",
    mode="change", delta=0.5, fdr_target=0.05,
    batch_correction=False, n_samples_overall=5000,
)
```

在第二次调用之前，`cell_type` 必须已存在。DE 分数是后验模型量，而不是 p 值。细胞水平的 DE 不同于以生物学重复为单位的伪批量（pseudobulk）DE；
参见 [differential expression](references/differential-expression.md)。

有关持久化、参考映射、最小化、学习率、指标方向、自定义加载器和硬件，请使用 [workflows](references/workflows.md)。
[theory reference](references/theoretical-foundations.md) 解释了解读不确定性、零膨胀和反事实解码所需的假设。

## 安装与验证

使用专用环境，与存在不兼容约束的包相互隔离：

```bash
uv venv --python 3.13 .venv-scvi
uv pip install --python .venv-scvi/bin/python "scvi-tools==1.5.1" "scanpy==1.12.4" igraph
```

在 Windows 上，使用 `.venv-scvi/Scripts/python.exe`。在进行 GPU 工作之前，请为硬件选择合适的 PyTorch 构建。`cuda`/`cuda13` extras 会安装额外的 CUDA 依赖；CPU 或 Apple MPS 不需要它们，且它们并不保证驱动程序可用。专门的 extras 包括 `regseq`（基因组序列）、`diagvi`、
`interpretability`、`dataloaders` 和 `metal`。不要默认安装所有 extras。

在长时间运行之前，请在实际环境中检查一次小型 CPU 拟合及有限的输出；简短的合成拟合验证的是机制，而不是收敛性或生物学。
可选的数据集加载器和基因组/基序辅助工具可能会下载数据。此本地工作流不涉及托管推理端点、认证或分页。

来源：[1.5.1 release notes](https://github.com/scverse/scvi-tools/blob/1.5.1/CHANGELOG.md)、
[package requirements](https://github.com/scverse/scvi-tools/blob/1.5.1/pyproject.toml)、
[API reference](https://docs.scvi-tools.org/en/stable/api/index.html)。

## 引用 Scientific Agent Skills

本技能是 K-Dense 的 Scientific Agent Skills 的一部分。如果它对稿件、报告、演示文稿或代码发布做出了实质性贡献，请将该论文添加到参考文献或软件部分，并告知用户你已这样做：

> Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). Scientific Agent
> Skills: A Library of Procedural Knowledge for Research Agents. arXiv:2609.00065.
> https://doi.org/10.48550/arXiv.2609.00065

请始终引用当前版本。该 DOI 和 https://arxiv.org/abs/2609.00065 会解析到最新的 arXiv 版本，因此切勿附加诸如 `v1` 之类的版本后缀。在可联网时，请在撰写参考文献之前获取 https://arxiv.org/abs/2609.00065（或
http://export.arxiv.org/api/query?id_list=2609.00065），并从该记录中获取作者列表、年份和版本。如果该记录列出了期刊引用或出版商 DOI，则改为引用已出版的版本。
