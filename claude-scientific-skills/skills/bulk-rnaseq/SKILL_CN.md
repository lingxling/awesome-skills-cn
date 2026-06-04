---
name: bulk-rnaseq
description: 端到端bulk RNA-seq编排器——将原始FASTQ读段通过QC和修剪（FastQC、fastp/Trim Galore）、比对和定量（STAR、Salmon、featureCounts）组装基因水平计数矩阵，然后移交到差异表达（pydeseq2）、通路/GSEA富集（pathway-enrichment）和出版图（scientific-visualization）。当用户有bulk RNA-seq读段或定量输出并想要完整、可重复的差异表达工作流时使用——例如"分析我的RNA-seq"、"FASTQ到DESeq2"、"运行nf-core/rnaseq"、"STAR/Salmon定量"、"为DESeq2构建计数矩阵"或"从读段到差异表达基因和富集通路"。在nf-core/rnaseq（Nextflow）路径和独立STAR/Salmon路径之间路由，涵盖实验设计、链特异性和QC门控。单细胞RNA-seq请改用scanpy技能。
license: MIT
metadata:
  version: "1.0"
  skill-author: K-Dense Inc.
---






# 批量 RNA-seq

## 概述

此技能编排一个完整、可辩护的批量 RNA-seq 差异表达研究，从原始测序 reads 到富集通路和图表。它是一个路由器，而不是重新实现：大多数阶段已经有了专门的技能，此技能以正确的顺序连接它们，填补一个真正的空白（原始 reads → 基因水平计数矩阵），并强制执行决定最终结果可信度的设计和质控决策。

"可辩护"意味着三件事，贯穿始终：
- **可重复** — 固定的管道/工具版本，尽可能使用容器，记录参数，固定随机种子。
- **有质控门控** — 质控在定量之前、期间和之后都被检查和采取行动，而不是跳过。
- **统计合理** — 充分的重复、与生物学匹配的设计、正确处理计数，以及 FDR 控制的检验。

管道是：**FastQC/修剪 → 比对/定量 (STAR/Salmon) → 计数 → DE (pydeseq2) → 富集 (pathway-enrichment) → 图表**。

## 何时使用此技能

当用户想要以下操作时使用此技能：
- 从 FASTQ 文件（或测序运行）到差异表达基因和通路。
- 运行或配置 `nf-core/rnaseq`，或使用 STAR、Salmon 或 featureCounts 进行比对/定量。
- 将 Salmon/STAR/featureCounts 输出转换为可供 DESeq2/PyDESeq2 使用的计数矩阵。
- 在提交计算之前，设计或检查批量 RNA-seq 实验（重复、批次、链方向性）。
- 规划端到端 RNA-seq 分析并决定链接哪些工具和技能。

这是**批量** RNA-seq（样本 = 生物样本）。对于单细胞/细胞核数据使用 `scanpy`；仅用于 DE 统计使用 `pydeseq2`；仅用于富集使用 `pathway-enrichment`。

## 管道概览

```mermaid
flowchart TD
    fastq["原始 FASTQ + 样本表"] --> qc["FastQC + MultiQC"]
    qc --> trim["修剪：fastp / Trim Galore"]
    trim --> align["比对 + 定量：STAR 和/或 Salmon"]
    align --> counts["基因水平计数矩阵"]
    counts --> de["差异表达"]
    de --> enrich["通路 / GSEA 富集"]
    de --> fig["图表"]
    enrich --> fig
    nfcore["通过 nextflow 技能的 nf-core/rnaseq"] -.->|"路径 A"| align
    manual["独立配方（本技能）"] -.->|"路径 B"| align
    bridge["build_counts_matrix.py（本技能）"] -.-> counts
    pydeseq2skill["pydeseq2 技能"] -.-> de
    pwskill["pathway-enrichment 技能"] -.-> enrich
    vizskill["scientific-visualization 技能"] -.-> fig
```

## 两条上游路径 — 选择一条

reads → 计数阶段可以通过两种方式运行。它们产生等效的基因计数；根据上下文选择，然后保持在该路径上。

| 当…时使用**路径 A — `nf-core/rnaseq`** | 当…时使用**路径 B — 独立工具** |
|------------------------------------------|----------------------------------|
| 您想要一个领域标准的、经过审计的、可引用的管道，一键运行 | 您有几个样本想要学习/检查每个步骤 |
| 多个样本，或将扩展到 HPC/云 | 没有 Nextflow/容器可用，或环境受限 |
| 可重复性和完整的 MultiQC 报告最重要 | 您需要管道未公开的非标准步骤 |
| → 通过 **`nextflow`** 技能驱动 | → 遵循 `references/upstream-manual.md` |

不确定时，优先选择**路径 A**：`nf-core/rnaseq` 已经将 FastQC → 修剪 → STAR/Salmon → 定量 → tximport → MultiQC 用合理、经过审查的默认值连接起来，这是最可辩护的选项。路径 B 存在是为了透明度和受限设置。

两条路径都收敛到**基因水平计数矩阵**，之后工作流程相同。

## 设置

```bash
# 此技能的粘合剂（桥接 + 交接）— Python
uv pip install pytximport pandas

# 下游技能安装自己的依赖：
#   pydeseq2 技能           -> uv pip install pydeseq2
#   pathway-enrichment 技能 -> uv pip install gseapy gprofiler-official

# 路径 A (nf-core)：只需要 Nextflow + 容器引擎 — 见 `nextflow` 技能。
```

# 路径 B (独立工具)：通过 bioconda 安装。固定版本以确保可重复性。
conda create -n rnaseq -c bioconda -c conda-forge \
  fastqc fastp trim-galore "star=2.7.11b" "salmon=1.10.3" subread multiqc
```

记录您使用的确切版本（管道修订版、工具版本、参考基因组 + 注释版本）— 它们属于方法部分并使分析可重复。

## 快速开始

### 路径 A — nf-core/rnaseq（推荐）

```bash
# 0. 首先验证样本表（及早发现最常见的失败）
python scripts/validate_samplesheet.py --samplesheet samplesheet.csv

# 1. 用小型捆绑数据对环境进行冒烟测试
nextflow run nf-core/rnaseq -r 3.26.0 -profile test,docker --outdir test_results

# 2. 实际运行：固定修订版，选择比对器，传递样本表 + 参考
nextflow run nf-core/rnaseq -r 3.26.0 \
  -profile docker \
  --input samplesheet.csv \
  --genome GRCh38 \
  --aligner star_salmon \
  --outdir results \
  -resume
```

`nf-core/rnaseq` 内部运行 tximport，因此基因计数已经**合并**输出 — 不需要桥接脚本。对 DE 使用 `results/star_salmon/salmon.merged.gene_counts_length_scaled.tsv`。样本表格式、比选择和输出：`references/upstream-nfcore.md`。有关引擎/HPC/云/容器详情，使用 **`nextflow`** 技能。

### 路径 B — 独立 STAR/Salmon（简略）

```bash
fastqc -o qc/ reads/*.fastq.gz                      # 1. 质控原始 reads
fastp -i s1_R1.fq.gz -I s1_R2.fq.gz \
      -o s1_R1.trim.fq.gz -O s1_R2.trim.fq.gz \
      --thread 4 -j s1.fastp.json                   # 2. 修剪接头/低质量
salmon quant -i salmon_index -l A \
      -1 s1_R1.trim.fq.gz -2 s1_R2.trim.fq.gz \
      --gcBias --seqBias -p 8 -o quant/s1            # 3. 定量（每个样本）
```

完整配方（FastQC、fastp/Trim Galore、STAR 索引+比对+`--quantMode GeneCounts`、Salmon 解码感知索引、featureCounts、链方向性）：`references/upstream-manual.md`。

### 计数 → DE → 富集（两条路径）

```bash
# 仅路径 B：组装基因 x 样本计数矩阵 + PyDESeq2 的元数据模板
python scripts/build_counts_matrix.py --from salmon \
  --quant-dir quant/ --tx2gene tx2gene.tsv --output-dir counts/

# 然后交接（见专门的技能）：
#   pydeseq2:           counts.csv + metadata.csv -> DE 表 (log2FC, padj, stat)
#   pathway-enrichment: 按 `stat` 排序 (GSEA) 或 padj+|LFC| 命中列表 (ORA)
#   scientific-visualization / matplotlib: 火山图、MA 图、热图、PCA、富集点图
```

## 逐阶段工作流程

自上而下工作。每个阶段命名拥有详情的技能或文件。不要跳过设计/质控阶段 — 批量 RNA-seq 研究最容易在那里出错。

1. **设计 & 样本表。** 确认每组≥3 个生物重复，识别批次/混杂因素，选择比较。构建样本表并用 `scripts/validate_samplesheet.py` 验证。原理和规则：`references/design-and-qc.md`。
2. **原始 reads 质控。** 每个文件运行 FastQC；用 MultiQC 聚合。检查每碱基质量、接头内容、重复和过表达。阈值：`references/design-and-qc.md`。
3. **修剪。** 移除接头和低质量尾（通过 `fastp` 或 Trim Galore）。重新运行 FastQC 确认。配方：`references/upstream-manual.md`（路径 A 为您完成此步骤）。
4. **比对/定量。** STAR（基因组比对 + `--quantMode GeneCounts`）和/或 Salmon（转录本准映射、解码感知）。确定链方向性 — 这很容易出错并且会静默减半您的计数。详情：`references/upstream-manual.md`；管道参数：`references/upstream-nfcore.md`。
5. **构建计数矩阵。** 将定量输出转换为基因 × 样本整数矩阵和元数据模板（`scripts/build_counts_matrix.py`）。关于估计计数和基因 ID 映射的细微差别在 `references/counts-and-handoff.md` 中。
6. **差异表达 → `pydeseq2` 技能。** 加载 `counts.csv` + `metadata.csv`，设置设计（如 `~batch + condition`），拟合，用 FDR 控制检验。作为质控检查 PCA 和 p 值直方图。
7. **富集 → `pathway-enrichment` 技能。** 对于 GSEA，按 DESeq2 `stat` 对*完整*基因列表排序；对于 ORA，传递阈值化命中列表（padj < 0.05，可选 |log2FC| > 1）。首先将基因 ID 映射到符号。
8. **图表 → `scientific-visualization` 技能。** 火山图、MA 图、样本距离热图、PCA 和富集点图，加上 MultiQC 报告作为质控叙述。

## 计数 → DE 桥接（关键粘合剂）

这是没有上游/下游技能的阶段，因此此技能拥有它。`scripts/build_counts_matrix.py` 将定量输出转换为 `pydeseq2` 期望的格式：

- **Salmon**（`--from salmon`）：使用 `pytximport` 将每个样本的 `quant.sf` 聚合到基因水平，使用 `counts_from_abundance="length_scaled_tpm"`（基因水平 DE 的正确选择），需要 `tx2gene` 映射。
- **STAR**（`--from star`）：读取每个 `ReadsPerGene.out.tab`，为您的 `--strandedness`（无链/正向/反向）选择列。
- **featureCounts**（`--from featurecounts`）：解析组合的 `featureCounts` 矩阵。

它写入 `counts.csv`（基因 × 样本，整数）和 `metadata_template.csv`（每样本一行）供您填写。**Salmon/RSEM 计数是估计值（非整数）；它们被四舍五入为整数**，因为 PyDESeq2 需要整数计数 — 见 `references/counts-and-handoff.md` 了解为什么使用 `length_scaled_tpm` 是可接受的，以及它与基于偏移量的 DESeq2+tximport 路由的区别。该参考还涵盖 Ensembl→符号映射（富集前需要）和 PyDESeq2 期望的确切方向。

## 常见陷阱

这些导致大多数错误或不可重复的批量 RNA-seq 结果：

1. **重复太少。** 每组 <3 个生物重复几乎没有功效和不稳定的离散估计。更多重复胜过更深测序。
2. **批次和条件混淆。** 如果每个处理样本在不同于对照样本的日期/泳道上处理，效果无法恢复。随机化，并建模已知批次（`~batch + condition`）。见 `references/design-and-qc.md`。
3. **错误的链方向性。** 选择错误的 STAR 列或 featureCounts `-s`/Salmon 库类型会静默丢弃约一半的 reads。使用 Salmon `-l A` 或推断链方向性，并验证分配 reads 的比例。
4. **将 TPM/FPKM 喂给 DESeq2。** DESeq2 需要原始（或长度缩放）**计数**，而不是 TPM/FPKM/归一化值。桥接处理这个问题。
5. **非整数计数。** PyDESeq2 需要整数；四舍五入 Salmon 估计值（桥接这样做）。
6. **富集的基因 ID 不匹配。** DESeq2 输出通常是 Ensembl ID；Enrichr/MSigDB 期望符号。在 `pathway-enrichment` 之前映射 ID，否则"没有显著结果"。
7. **跳过定量后质控。** 在信任 DE 之前，始终查看 PCA 和样本距离热图 — 它们揭示标签混淆、异常值和隐藏批次。
8. **混合比对器跨样本。** 使用相同的工具、版本、参考和参数对每个样本进行定量。
9. **未固定版本。** "最新"管道/基因组使结果不可重复；固定 `-r`、工具版本和基因组/注释版本。

## 与其他技能的集成

- **上游执行：** `nextflow`（运行 `nf-core/rnaseq`，路径 A；HPC/云/容器）。
- **参考数据 / 基因 ID：** `gget`（`gget ref` 获取基因组+GTF，`gget info`/`gget search` 用于 ID 映射）、`database-lookup`（Ensembl/NCBI）、`biopython`/`pysam`（FASTA/BAM 处理）。
- **差异表达：** `pydeseq2`（此技能交接计数的 DE 引擎）。
- **富集：** `pathway-enrichment`（ORA + GSEA；其 `scripts/run_enrichment.py` 直接读取 DESeq2 结果 CSV）。
- **图表和报告：** `scientific-visualization`、`matplotlib`、`seaborn`；`scientific-writing` 用于方法/结果叙述。
- **相关但不同：** `scanpy`（单细胞）、`statistical-analysis`（多重检验深度）。

## 参考文件

需要深度时阅读相关文件 — 每个都是独立的：

- `references/upstream-nfcore.md` — 路径 A：样本表格式、`--aligner`/`--pseudo_aligner` 选择、关键参数、`salmon.merged.gene_counts*.tsv` 输出、MultiQC，以及交给 `pydeseq2` 的内容。
- `references/upstream-manual.md` — 路径 B：FastQC、fastp/Trim Galore、STAR 基因组索引 + 比对 + `--quantMode GeneCounts`、Salmon 解码感知索引 + `quant`、featureCounts，以及如何确定链方向性。
- `references/counts-and-handoff.md` — 将定量输出转换为 PyDESeq2 就绪的 `counts.csv`/`metadata.csv`（pytximport、STAR 列选择、featureCounts）、整数/估计计数的细微差别、Ensembl→符号映射，以及 DE→富集排序/命中列表配方。
- `references/design-and-qc.md` — 实验设计（重复、批次、混杂、设计公式）和质控指标解释（比对率、重复、rRNA、复杂度、PCA/异常值）— 可辩护管道的支柱。

## 资源

- nf-core/rnaseq: https://nf-co.re/rnaseq · STAR: https://github.com/alexdobin/STAR · Salmon: https://salmon.readthedocs.io
- fastp: https://github.com/OpenGene/fastp · Trim Galore: https://github.com/FelixKrueger/TrimGalore · MultiQC: https://multiqc.info
- pytximport: https://pytximport.complextissue.com · featureCounts (Subread): https://subread.sourceforge.net
- 方法背景：Love et al. 2014 (DESeq2) DOI 10.1186/s13059-014-0550-8 · Soneson et al. 2015 (tximport) DOI 10.12688/f1000research.7563.2
