---
name: qiime2-amplicon
description: 将双端 16S 扩增子测序读段处理为 QIIME 2 的 ASV 和分类学结果，并保留制品溯源信息。检查配对的 FASTQ 清单、引物方向诊断、预测的修剪后重叠、样本 ID、运行时版本和读段保留情况，并指导选择兼容的分类学分类器。
license: MIT
compatibility: Python 3.10+ for the standard-library validation helper; QIIME 2 2026.7 distribution with cutadapt, dada2, demux, feature-table, feature-classifier, taxa and types plugins for execution. Install through the official conda/container distribution, not PyPI. Requires a compatible trusted classifier and network for installation/reference downloads.
metadata:
  version: "1.1"
  skill-author: K-Dense Inc.
  upstream-version: "2026.7"
  last-reviewed: "2026-10-01"
---

# QIIME 2 双端 16S 扩增子

适用于已拆分样本（demultiplexed）的双端 16S 检测，且已知引物、质量编码、预期插入片段长度和样本元数据。这一有界的工作流程导入读段、去除 5′ 引物、使用 DADA2 去噪、使用明确提供的分类器对 ASV 进行分类，并保留 `.qza`/`.qzv` 溯源信息。不要将读段计数视为绝对细胞计数，也不要将分类学注释视为菌株鉴定。

## 运行前确定检测方案

- 确认 Phred+33、读段方向、正向/反向读段中**实际测序出的**引物序列，以及引物是否已被去除。内置运行器要求引物仍存在于 5′ 端；它锚定 Cutadapt 匹配，并丢弃未修剪的配对读段。已修剪的读段需要使用直接导入 → DADA2 的工作流程，并在溯源信息中记录这一省略。
- 根据实际的逐碱基质量和错误谱选择截断位置。`trunc-f/r` 是**引物去除之后**的位置。预期的最大插入片段长度同样不包括引物。要求 `trunc_f + trunc_r - maximum_insert_length >= 12`；请为长度变异留出余量。该检查预测的是几何重叠，而不是生物学上成功的合并。
- 选择一个其参考数据库、分类学覆盖范围、方向和训练方式都适合该检测的分类器。支持全长分类器；针对引物区域的专门训练并非必须。其 scikit-learn 版本必须与已安装的环境完全匹配（官方 2026.7 发行版固定为 1.7.1）。记录来源 URL、数据库版本和校验和。QIIME 当前的数据资源页面链接了适用于 2026.4 及更高版本的外部托管分类器；其较旧的下载并不自动兼容。不要自动获取任意的"最新"分类器，也不要重用不兼容的序列化 sklearn 模型。仅从可信来源加载 sklearn 分类器制品：QZA 格式验证并不会使不可信的序列化模型变得安全。
- 在可用时包含提取空白对照、PCR 阴性对照和模拟群落（mock community）。运行器会拒绝空的 FASTQ；请单独保留空对照的 ID 并加以报告，而不是悄悄删除对照证据。在进行生态学解释之前评估污染情况。

## 输入文件

清单是一个**以制表符分隔**的 `PairedEndFastqManifestPhred33V2` 文件，表头必须与下面完全一致：

```text
sample-id	forward-absolute-filepath	reverse-absolute-filepath
sample1	/data/sample1_R1.fastq.gz	/data/sample1_R2.fastq.gz
```

这是辅助工具有意设计得较窄的清单配置。请使用真实的制表符、运行时可见的字面绝对路径（在调用此辅助工具之前先展开环境变量），并且每个样本一行；此清单中不得有注释/指令行或额外的列。不要对 R2 文件做反向互补。样本元数据是以制表符分隔的文件，第一列为 `sample-id`，ID 唯一且与清单匹配，并可附带可选的 `#q2:types` 注解。请包含下游所需的协变量和生物学重复 ID。辅助工具检查元数据 ID 和行结构；QIIME 在执行期间进行完整的元数据类型/指令验证。动作所使用的元数据会保留在制品溯源信息中，因此请使用去标识化的生物学重复 ID。

## 执行

辅助工具位于 [scripts/amplicon_workflow.py](scripts/amplicon_workflow.py)。以下命令假定技能目录为工作目录。首先在不使用 QIIME 的情况下验证。这些示例引物和长度仅为**示意**，并非通用的检测设置：

```bash
python scripts/amplicon_workflow.py validate \
  --manifest manifest.tsv --metadata sample-metadata.tsv \
  --primer-f GTGYCAGCMGCCGCGGTAA --primer-r GGACTACNVGGGTWTCTAAT \
  --trunc-f 220 --trunc-r 200 --amplicon-max 300
```

然后在 QIIME 2 2026.7 环境中，配合兼容的分类器运行。此针对具体研究的调用仅为示意；请根据事先的质量检查或预试验来选择长度：

```bash
python scripts/amplicon_workflow.py run \
  --manifest manifest.tsv --metadata sample-metadata.tsv \
  --primer-f GTGYCAGCMGCCGCGGTAA --primer-r GGACTACNVGGGTWTCTAAT \
  --trunc-f 220 --trunc-r 200 --amplicon-max 300 \
  --classifier compatible-classifier.qza --threads 4 --output run01
```

`run` 会立即执行，仅写入全新的输出目录，并在 QIIME 命令失败时停止。它会遍历每一条配对的 FASTQ 记录，以捕获不匹配的 ID/顺序/计数，检查序列/质量的一致性和样本对齐，并对前 1,000 个读段对分析其与 IUPAC 引物的精确匹配。较低的精确匹配率属于警告：Cutadapt 允许错配，但较低的比率也可能表明方向不正确、存在接头，或数据已被修剪。每个样本至少有一个完整的读段对必须达到名义上的引物后截断长度。这些长度估计会减去所述的引物长度；它们不会模拟 Cutadapt 的插入缺失或质量过滤，也不能证明任何读段对确实会合并。

运行器对输出集不断演变的插件方法使用 `--output-dir`，并在发行版提供时保留 Cutadapt 统计数据和 DADA2 碱基转换制品。2026.7 的表格摘要还会在 `table.qzv` 旁边生成 `feature-frequencies.qza` 和 `sample-frequencies.qza`。它记录 `qiime-info.txt`、`commands.json`、`workflow.log`、输入质控、分类器校验和以及输出制品的校验和。在报告完成之前，它会运行最高级别的 QIIME 制品验证。有关发行版固定的运行时、实际的验证范围、重启处理和科学解释，参见 [references/runtime-and-interpretation.md](references/runtime-and-interpretation.md)。

## 分析前检查结果

请在本地的 QIIME 可视化环境或 [QIIME 2 View](https://view.qiime2.org/) 中（视数据而定）打开 `trimmed.qzv`、`table.qzv` 和 `taxa.qzv`。检查质量/长度谱、各样本深度和优势类群。请保留原始制品，而不是用 CSV/BIOM 导出文件替代它们：导出文件不保留原始的溯源图。

`retention-qc.json` 将原始读段对与 DADA2 输入及非嵌合读段进行比较，因此修剪造成的损失依然可见。保留比例 <50% 是一个审查启发式标准，而不是通用的拒绝规则。请检查 `stats/stats.tsv` 中的各个阶段：过滤阶段的损失提示质量/期望错误设置有问题；正向去噪之后的损失包括反向去噪和合并失败；嵌合体损失则值得审查文库质量和参数。在进行稀释、多样性或差异丰度分析之前，请调查缺失/为零的样本以及对照的表现。这些下游分析需要单独的设计决策；本技能不会自动选择稀释深度。独立的 `retention stats.tsv` 子命令只知道 DADA2 的输入计数：它报告 `raw_pairs: null`，并明确指出该分母。它支持仅合并的双端 DADA2 统计（即本运行器所生成的）；它会拒绝保留未合并/拼接读段的统计。

## 主要参考资料

- [当前的安装入口](https://library.qiime2.org/quickstart/qiime2)和[扩增子文档](https://amplicon-docs.qiime2.org/en/latest/)。
- [导入格式](https://amplicon-docs.qiime2.org/en/latest/how-to-guides/how-to-import/)。
- [Cutadapt 动作](https://amplicon-docs.qiime2.org/en/latest/references/plugins/cutadapt/)和
  [DADA2 动作](https://amplicon-docs.qiime2.org/en/latest/references/plugins/dada2/)。
- [分类器数据资源](https://library.qiime2.org/data-resources)。

滚动更新的文档可能描述的是开发版。在将固定版本的运行器改用于后续发行版之前，请在确切的已安装环境中检查 `qiime info` 和各动作的 `--help`。
