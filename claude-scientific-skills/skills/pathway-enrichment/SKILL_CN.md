---
name: pathway-enrichment
description: 对基因列表或排序基因数据进行通路和基因集富集分析，然后解释结果。当用户有一组基因（来自PyDESeq2/Scanpy的差异表达基因、CRISPR筛选命中、聚类标记基因、蛋白质组学命中）并想知道哪些生物通路、GO术语或基因集被过度代表或富集时使用。涵盖超几何检验（ORA/Enrichr/Fisher）、排序基因集富集分析（GSEA/preranked）、单样本评分（ssGSEA/GSVA）以及通过gseapy、g:Profiler、Enrichr库、MSigDB、GO、KEGG、Reactome和WikiPathways进行功能分析——加上基因ID映射、选择正确的背景 Universe、多重检验校正、冗余减少、点图/富集图和出版级表格。将此用于"通路分析"、"富集分析"、"GO富集"、"KEGG/Reactome通路"、"GSEA"、"超几何检验"、"功能注释"或"我的基因在哪些通路中"。
license: MIT
metadata:
  version: "1.0"
  skill-author: K-Dense Inc.
---






# 通路富集

## 概述

富集分析回答"我的基因中哪些生物学被过度代表？"它是差异表达、筛选或聚类后的标准最后一步。有两种核心方法，正确选择是最重要的决定：

- **ORA（过度代表分析）** — 取一个*阈值化*的基因列表（例如 padj < 0.05），使用 Fisher 精确检验/超几何检验测试哪些基因集比随机重叠更多。工具：Enrichr、g:Profiler。
- **GSEA（基因集富集分析）** — 取*完整排名*的基因列表（无阈值），测试每个基因集是否集中于顶部或底部。预排名 GSEA 使用每个基因的分数（例如 DESeq2 `stat`）。当效果广泛且微妙时更好。

此技能编排这些分析、背后的基因集数据库，以及使结果错误或无法发表的解释陷阱。

## 何时使用此技能

当用户想要以下操作时使用此技能：
- 在基因列表中查找富集的 GO 术语 / KEGG / Reactome / WikiPathways / MSigDB Hallmark 集合。
- 在 DESeq2、edgeR、limma 或 Scanpy `rank_genes_groups` 输出上运行 GSEA / 预排名 GSEA。
- 对每个样本/细胞进行通路活性评分（ssGSEA、GSVA）。
- 解释、去重和可视化富集结果，或构建发表表格/图表。
- 在 ORA 和 GSEA 之间选择，选择基因集库，选择背景，或修复基因 ID 问题。

对于快速一次性 Enrichr 查询，`gget` 技能（`gget enrichr`）更轻量；对于原始通路/交互 API（Reactome、KEGG、STRING），见 `database-lookup` 技能。使用**此技能**进行完整、可辩护的富集工作流程。

## 选择正确的方法

| 情况 | 方法 | 工具/入口点 |
|--------|------|-------------|
| 您有一个离散的命中列表（DE 基因、筛选命中、聚类标记） | **ORA** | `gp.enrichr(...)` 或 g:Profiler |
| 您有一个完整排名列表（每个测试的基因 + 分数） | **预排名 GSEA** | `gp.prerank(...)` |
| 您有表达矩阵 + 类别标签 | **GSEA** | `gp.gsea(...)` |
| 您想要每个样本/细胞的通路分数 | **ssGSEA / GSVA** | `gp.ssgsea(...)`、`gp.gsva(...)` |
| 您需要自定义背景或 500+ 生物体 | **自定义域的 ORA** | g:Profiler (`domain_scope='custom'`) |
| 您想要 TF / 信号*活性*（PROGENy、DoRothEA） | 活性推断 | 见 `references/databases-and-gene-sets.md`（decoupler） |

不确定时：阈值化列表 → ORA；带分数的排名表 → GSEA。永远不要阈值化列表然后喂给 GSEA — 那会丢弃 GSEA 依赖的排名。

## 设置

```bash
uv pip install gseapy gprofiler-official
# gseapy 依赖 pandas、numpy、scipy、matplotlib。需要网络访问以下载
# Enrichr、g:Profiler 和 MSigDB。对于完全离线的 ORA，使用本地
# GMT 文件和 gp.enrich()（见 references/gseapy.md）。
```

验证并列出可用的基因集库（名称随时间变化 — 永远不要盲目硬编码）：

```python
import gseapy as gp
names = gp.get_library_name(organism="human")   # 200+ Enrichr 库
print([n for n in names if "Reactome" in n or "KEGG" in n or "Hallmark" in n])
```

## 快速开始

### 对命中列表进行 ORA（gseapy + Enrichr）

```python
import gseapy as gp

# Enrichr 库期望 HGNC 基因 SYMBOLS（人类：大写）。如需要先映射 ID。
genes = [g.strip() for g in open("deg_symbols.txt") if g.strip()]

enr = gp.enrichr(
    gene_list=genes,
    gene_sets=["MSigDB_Hallmark_2020", "GO_Biological_Process_2023",
               "KEGG_2021_Human", "Reactome_2022"],
    organism="human",
    outdir=None,            # 内存中；设置路径也写入表格/图表
)
res = enr.results
sig = res[res["Adjusted P-value"] < 0.05].sort_values("Adjusted P-value")
print(sig[["Gene_set", "Term", "Overlap", "Adjusted P-value", "Combined Score", "Genes"]].head(20))
```

### 从 DESeq2 结果进行预排名 GSEA

```python
import gseapy as gp
import pandas as pd

res = pd.read_csv("deseq2_results.csv", index_col=0)   # 索引 = 基因符号
# 按检验统计量排名（符号 = 方向，幅度 = 证据）。这比按 log2FoldChange
# 排名更稳定，后者对低计数基因有噪声。
rnk = res["stat"].dropna().sort_values(ascending=False)
rnk.index = rnk.index.str.upper()
rnk = rnk[~rnk.index.duplicated(keep="first")]

pre = gp.prerank(
    rnk=rnk,
    gene_sets=["MSigDB_Hallmark_2020", "GO_Biological_Process_2023"],
    min_size=15, max_size=500,        # 丢弃微小/庞大的集合（有噪声或通用）
    permutation_num=1000, seed=123,   # seed = 可重现的 p 值
    threads=4, outdir=None,
)
out = pre.res2d.sort_values("FDR q-val")
print(out[["Term", "ES", "NES", "NOM p-val", "FDR q-val", "Lead_genes"]].head(20))
```

如果您没有 `stat` 列，从 `sign(log2FoldChange) * -log10(pvalue)` 构建排名。

## 核心工作流程

对于可辩护的分析，请完成这些步骤。中间步骤（ID 类型、背景）是结果最容易静默出错的地方。

### 步骤 1 — 确定输入并选择方法
确认：哪些基因、什么生物体、是否有每个基因的分数（→ GSEA）还是只是一个列表（→ ORA），以及它们代表什么比较（方向对解释很重要）。

### 步骤 2 — 将基因 ID 放入正确的命名空间
Enrichr/MSigDB 库按**基因符号**键入（人类大写，鼠标首字母大写）。如果您有 Ensembl/Entrez ID，先进行转换。详见 `references/databases-and-gene-sets.md` 中的 `gp.Biomart`、g:Profiler `g:Convert` 和 `mygene`。静默 ID 不匹配是"没有显著结果"的 #1 原因。

### 步骤 3 — 选择基因集库以匹配问题
Hallmark（广泛主题）→ GO:BP（机制）→ KEGG/Reactome/WikiPathways（精选通路）→ C7（免疫）等。不要运行 50 个库；选择 2-4 个符合生物学的。目录和选择指南：`references/databases-and-gene-sets.md`。

### 步骤 4 — 设置背景宇宙（仅 ORA）
背景必须是您的检测中*可能*被检测到的基因（例如所有表达/测试的基因），而不是整个基因组。错误的背景会膨胀显著性。Enrichr 使用固定背景；当背景重要时，使用 g:Profiler 的 `domain_scope='custom'` + 您的 `background`，或使用明确背景的 `gp.enrich()`。原理见 `references/interpretation.md`。

### 步骤 5 — 运行分析
使用快速开始模式或捆绑的 `scripts/run_enrichment.py`。对于 GSEA 始终设置 `seed` 并报告 `permutation_num`。

### 步骤 6 — 按调整后 p 值过滤
使用 `Adjusted P-value`（ORA，Benjamini-Hochberg）或 `FDR q-val`（GSEA），而非原始 p 值。典型截止值 0.05；还要检查重叠/基因数量，使"命中"不是 2000 基因集中的 1 个基因。

### 步骤 7 — 可视化
点图、条形图、富集图和 GSEA 运行分数图内置于 gseapy（`gp.dotplot`、`gp.barplot`、`gp.enrichment_map`、`gp.gseaplot`）。详见 `references/gseapy.md`。

### 步骤 8 — 减少冗余并解释
GO 尤其返回许多近乎重复的术语。用富集图（术语-术语相似性）、前沿重叠或父术语进行折叠，并报告代表性术语。解释框架和发表表格格式在 `references/interpretation.md` 中。

## 辅助脚本

`scripts/run_enrichment.py` 端到端运行 ORA 或 GSEA 并写入结果表和点图，处理样板（符号清理、去重、NA 移除、从 DESeq2 表构建排名、每个库的 FDR 过滤）。

```bash
# 从命中列表进行 ORA（每行一个基因符号）
python scripts/run_enrichment.py ora \
  --genes deg_symbols.txt \
  --libraries MSigDB_Hallmark_2020 GO_Biological_Process_2023 KEGG_2021_Human \
  --organism human --outdir results/

# 从 DESeq2 结果 CSV 进行预排名 GSEA（从 `stat` 自动构建排名）
python scripts/run_enrichment.py gsea \
  --deseq2 deseq2_results.csv \
  --libraries MSigDB_Hallmark_2020 GO_Biological_Process_2023 \
  --organism human --outdir results/ --seed 123

# 从显式 2 列排名文件进行预排名 GSEA（基因、分数）
python scripts/run_enrichment.py gsea --rnk ranked_genes.csv --outdir results/
```

运行 `python scripts/run_enrichment.py --help` 获取所有选项（背景文件、FDR 截止值、最小/最大集合大小、排列数）。

## 常见陷阱

这些导致大多数错误或不可重现的结果：

1. **基因 ID / 生物体不匹配** — 符号 vs Ensembl、人类 vs 鼠标大小写。正确映射 ID 和设置 `organism`，否则匹配静默降至接近零。
2. **错误的背景（ORA）** — 使用整个基因组而非测试/表达的基因集会膨胀 p 值。当重要时设置自定义背景。
3. **GSEA 前阈值化** — GSEA 需要*完整*排名列表；只有 ORA 使用切割列表。
4. **仅按 log2FoldChange 排名 GSEA** — 对低计数基因不稳定；优先使用 `stat` 或 `sign(LFC) * -log10(p)`。
5. **跨库多重检验** — FDR 在库*内*计算；运行许多库会增加测试次数。报告每个库的 FDR 并保持保守。
6. **冗余 GO 术语** — 不要报告同一术语的 40 个变体；折叠并显示代表。
7. **显著性 ≠ 相关性** — 检查重叠数量和基因集大小；微小集合 trivial 地达到显著。
8. **列表对 ORA 太短/太长** — <10 基因功效不足；>2000 失去特异性（考虑改用 GSEA）。
9. **无可重现性元数据** — Enrichr/GO 库有版本并随时间漂移。记录库名称+日期并设置 GSEA `seed`。

## 与其他技能的集成

- **上游（基因来源）：** `pydeseq2`（DE 基因 + GSEA 的 `stat`）、`scanpy`（`rank_genes_groups` 标记/分数）、`depmap`/`pytdc`（筛选命中）、蛋白质组学技能（`pyopenms`、`matchms`）。
- **数据库/ID：** `database-lookup`（Reactome、KEGG、STRING、Gene Ontology API）、`gget`（`gget enrichr` 快速路径、`gget info` 用于 ID 映射）、`bioservices`。
- **下游：** `scientific-visualization`（自定义图表）、`networkx`（富集图图）、`scientific-writing` / `literature-review`（解释和引用）、`statistical-analysis`（多重检验详情）。

## 参考文件

需要深度时阅读相关文件：

- `references/gseapy.md` — 完整 gseapy API：`enrichr`、离线 `enrich`、`prerank`、`gsea`、`ssgsea`、`gsva`、`Msigdb`、`Biomart`、`get_library_name`/`read_gmt`、每个图表、结果列含义、GMT/离线用法和故障排除（速率限制、空结果）。
- `references/databases-and-gene-sets.md` — GO、KEGG、Reactome、WikiPathways、MSigDB 集合、Enrichr 库命名、g:Profiler 源、生物体处理、基因 ID 转换、按问题选择库，以及指向 Reactome/STRING API 和 decoupler 活性推断的指针。
- `references/interpretation.md` — ORA vs GSEA 统计、背景宇宙选择、多重检验方法（BH vs g:SCS vs Bonferroni）、前沿基因、冗余减少、效应 vs 显著性、发表表格模板和可重现性检查清单。

## 资源

- gseapy 文档：https://gseapy.readthedocs.io/ · 仓库：https://github.com/zqfang/GSEApy
- g:Profiler：https://biit.cs.ut.ee/gprofiler/ · Python 客户端：https://pypi.org/project/gprofiler-official/
- Enrichr：https://maayanlab.cloud/Enrichr/ · MSigDB：https://www.gsea-msigdb.org/gsea/msigdb/
- GSEA 方法：Subramanian et al. (2005) PNAS, DOI: 10.1073/pnas.0506580102
