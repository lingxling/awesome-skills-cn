---
name: mageck
description: 使用 MAGeCK 分析池化（pooled）CRISPR 筛选的 FASTQ 读段和 guide 计数矩阵，验证 guide 文库和对比组，评估重复样本和文库质控（QC），并生成带效应量和 FDR 的基因打击（hit）排序。适用于新的敲除（knockout）、CRISPRi 或 CRISPRa 筛选分析、富集或耗竭对比,以及 MAGeCK count/test 工作流；现有的公开依赖性分数查询属于 DepMap 的范畴。
license: MIT
compatibility: Requires Python 3.10+ for the helper and MAGeCK 0.5.9.5 with its compiled RRA executable for analysis. Tested runtime uses Python 3.11, NumPy 1.26.4 and SciPy 1.13.1. Source installation needs a C++ compiler; network is needed only for installation. No credentials.
metadata:
  version: "1.1"
  skill-author: K-Dense Inc.
  upstream-version: "0.5.9.5"
  last-reviewed: "2026-10-01"
---

# MAGeCK 池化筛选分析

## 何时使用

使用本技能对现有的测序读段按提供的 guide 文库进行计数，或比较
已经完成计数的池化筛选结果。应提供计数矩阵、QC、guide 和基因层面的结果、对比组的
溯源信息，以及对富集/耗竭情况的简要解读。本工作流分析的是筛选结果；
它不设计 guide，也不会仅凭一个打击结果就推断基因功能。

## 运行环境

经测试的源码安装方式和外部运行时的注意事项见
[references/runtime.md](references/runtime.md)。在分析之前，应验证 `mageck --version` 和
`mageck test --help` 两者。内置的 Python 辅助脚本只依赖标准库。
MAGeCK 本身还需要 NumPy、SciPy，以及 `RRA` 二进制程序。PDF/R 报告是可选的，辅助脚本不需要它。

[官方发布目录](https://sourceforge.net/projects/mageck/files/0.5/)仍将
0.5.9.5 列为其最新的 MAGeCK 发布版本。上游现在链接到独立的
[MAGeCK2 项目](https://github.com/davidliwei/mageck2）；这些命令和辅助脚本针对的是
MAGeCK 0.5.9.5，而不是可互换使用的 MAGeCK2 安装。这是一个本地 CLI 工作流，
没有服务 API 或身份验证。

## 工作流程

1. 确定文库版本、扰动模式、样本名称、选择方向、
   生物学重复样本、基线材料、时间点和批次。应将测序通道（lane）
   与独立的生物学重复样本区分开来。质粒基线和细胞的第 0 天基线
   回答的是不同的问题。要求明确指定处理组/对照组的对比；辅助脚本
   绝不会悄悄地把所有未使用的样本都归入对照组。
2. 验证一份**无表头的 TSV 文库**文件，包含 guide ID、DNA 序列、基因。ID 和
   序列必须唯一。辅助脚本要求计数表的表头以 `sgRNA`、`Gene` 开头，
   后面跟着唯一的非数字样本名，例如 `c1`。MAGeCK 可能把数字名称
   解释为列索引或计数值；分析之前应先重命名它们。guide/基因 ID 不能包含
   空白字符。辅助脚本会拒绝有歧义的序列，以及任何计数/文库 ID 或基因不匹配的情况；
   对于有意设计的多靶点 guide，应在上游明确处理。这些都是辅助脚本有意设置的
   限制；原生 MAGeCK 也接受其他输入变体。
3. 对于 FASTQ，应检查读段结构和已知的 guide 序列，以确定裁剪和
   方向。使用 MAGeCK 的 `count`，每个生物学样本对应一个以空格分隔的参数；
   只有当多个测序通道是同一样本的技术重复时，才用逗号把它们连接起来。当比对效果较差时，应保留未映射读段和计数汇总方面的证据。零计数的 guide
   仍应保留在文库中；不要为了改善 QC 而删掉它。
4. 在进行统计检验之前先做 QC。审查文库代表性、每个 guide 的读段中位数、
   零值比例、Gini 系数，以及同一条件内重复样本间的相关性。辅助脚本中
   10% 零值和 0.8 相关性的提示阈值只是用于审查的提示，不是普遍适用的接受标准。高相关性可能与系统性的
   伪影同时存在。读取深度不等于实验细胞覆盖度。该辅助脚本使用的是基于原始计数总体的 Gini 系数；MAGeCK 原生的
   计数汇总 Gini 系数使用的是 log(count + 1) 并带有限样本校正。不要把它们的
   数值或阈值当作同一个统计量来比较。
5. 根据筛选情况选择归一化方法。中位数归一化假定大多数 guide 是
   稳定的。对于较强的全局偏移，提供经验证的阴性对照 guide 可能支持使用
   `--normalization control`。这些必须是**guide ID**，每行一个；基因列表不能互换使用。生物学对照样本和阴性对照 guide 承担的是不同的
   角色。必须至少存在两个对照，并且分配给某个对照基因的每一个 guide
   都必须被标记为对照。提供 `--control-guides` 也会改变 RRA 的零分布，
   即使同时使用中位数归一化也是如此。应记录它们的来源并检查其计数分布。
   当某个选定样本的中位数为零，或超过 45% 的 guide 为零值时，MAGeCK 0.5.9.5
   会将中位数归一化切换为总计数缩放；对于对照归一化，它会评估
   对照 guide 子集。应检查报告中实际应用的方法、规模因子（size factor）和警告信息。
6. 使用 `test` 进行两组比较。`--paired` 要求两个列表按对应的
   生物学顺序排列，且长度相等；仅凭长度匹配并不能确立配对关系。
   辅助脚本会按请求的 FDR 报告两个方向上的基因，并保留完整的排序结果。
   对于多因素设计，见[references/design.md](references/design.md)；不要把
   批次或时间序列数据不加论证地压缩成一个两组检验。
7. 检查主要基因的 guide 一致性、适用情况下的必需基因（essential-gene）
   恢复情况、阴性对照、重复样本一致性,以及核酸酶敲除
   筛选中的拷贝数伪影。应把效应量和 FDR 一起报告。一个富集的 guide
   可能表示抗性、生长优势，或取决于选择条件的采样伪影；耗竭也不一定意味着
   普遍的必需性。缺乏重复或低计数的 guide 会削弱推断力度。

## 命令

运行路径相对于已安装的技能目录。输入和输出路径指的是用户的
分析目录。该辅助脚本拒绝复用一个已存在的结果目录。

```bash
# 单端 guide 读段；裁剪和方向必须与用户的文库制备方式相匹配。
mageck count -l library.tsv --fastq c1.fastq.gz c2.fastq.gz t1.fastq.gz t2.fastq.gz \
  --sample-label c1,c2,t1,t2 --trim-5 0 --norm-method none -n counts

python scripts/screen_analysis.py qc --counts counts.count.txt --library library.tsv \
  --control c1 c2 --treatment t1 t2 --output qc.json

python scripts/screen_analysis.py test --counts counts.count.txt --library library.tsv \
  --control c1 c2 --treatment t1 t2 --normalization median --fdr 0.05 --output result
```

该 FASTQ 命令结构已使用一个合成的双 guide 文库进行了测试：精确恢复了
30 和 12 的计数值。一个单独的、经过裁剪和反向互补处理的双通道 fixture 恢复了
15、7 和 0 条读段。两组比较辅助脚本已使用每个条件 500 个 guide、两个重复样本的数据，在非配对和配对模式下进行了测试；已知的耗竭和富集基因在各自的方向上都排在首位，
并通过了 FDR 0.05 的检验。稀疏 fixture 验证了总计数归一化的回退机制。
这些测试确立的是执行情况和信号方向，而不是真实筛选的统计校准。
上文中真实的文件路径仅作说明性用途。

`result/report.json` 记录了计数/文库/对照 guide 的 SHA-256、对照 guide ID、MAGeCK 版本、
实际使用的参数、QC、应用的归一化方法、警告信息、打击方向、FDR、log2 倍数变化和排名。
该辅助脚本明确选择了基于中位数的 guide LFC 聚合方式和 `--remove-zero both`：全零
guide 会保留在输入/QC 中，但会从排序结果中排除。原生 MAGeCK 默认也会跳过 `NA`/`na`
基因标签。该辅助脚本的 `--fdr` 过滤的是已完成的基因结果；它设置的不是 MAGeCK 的
`--gene-test-fdr-threshold`，后者控制的是 RRA guide 选择的截断值。阴性和阳性
FDR 是两个独立的族；它们的并集并不能确立跨方向或跨多个对比组的联合 FDR 控制。`screen.gene_summary.txt`、`screen.sgrna_summary.txt`、归一化后的
计数以及执行日志保留了完整的证据。在分析交接时应包含原始文库、样本表
和阴性对照列表；仅凭计数校验和无法重建它们。

## 主要参考资料

- [MAGeCK 用法与命令语义](https://sourceforge.net/p/mageck/wiki/usage/)
- [官方安装指导](https://sourceforge.net/p/mageck/wiki/install/)
- [输入格式](https://sourceforge.net/p/mageck/wiki/input/)
- [输出字段含义](https://sourceforge.net/p/mageck/wiki/output/)
