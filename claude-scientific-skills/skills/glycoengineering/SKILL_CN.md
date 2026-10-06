---
name: glycoengineering
description: 通过扫描经典 N-糖基化序列基序（sequon）、描述富含 S/T 的区域、检查经整理的糖基证据，并准备 NetNGlyc、NetOGlyc 和 GlycoSHIELD 工作流,来分析和改造蛋白质糖基化。适用于糖蛋白工程、抗体 Fc 糖基化、糖链屏蔽,以及位点特异性糖蛋白质组学的解读。
license: Unknown
compatibility: Local sequence helpers require Python 3.10+. Public GlyTouCan lookup requires requests and network access. DTU predictors use a browser; optional GlycoSHIELD needs a separate source installation, glycan libraries, and GROMACS for SASA analysis.
metadata:
  version: "1.4"
  skill-author: Kuan-lin Huang
  last-reviewed: "2026-10-01"
---

# 糖基化工程

## 何时使用

适用于经典 N-糖基化候选位点分析、O-GalNAc 候选位点筛选、
抗体糖型比较，或结构性糖链屏蔽。应将四类结果分开看待：序列基序、
预测结果、有实验支持的占位情况，以及糖链结构/组成。单独任何一项都不能确立其他几项。

本工作流聚焦于真核生物分泌通路的 N-糖基化,以及黏蛋白型
O-GalNAc。O-GlcNAc、O-甘露糖、O-岩藻糖以及其他 O-连接修饰需要
相应的证据和预测工具；仅凭 S/T 富集并不能确定修饰类型。

## 工作流程

1. 记录蛋白质登录号、同种型/版本、确切序列、表达宿主、
   信号肽/跨膜拓扑结构,以及构建体边界。应保留一份
   从提交序列坐标到成熟蛋白、PDB 链/残基标识符以及（如适用）抗体编号的映射关系。
2. 扫描经典的 N-X-[S/T] 候选位点，其中 X 不是 Pro。应保留重叠位点：`NNST`
   在位置 1 和 2 都有候选位点。缺少经典基序并不能排除
   非常规的 N-糖基化；存在该基序也不能确立占位情况。
3. 利用拓扑结构和经整理的证据，优先考虑分泌/管腔内/细胞外的区域。仅凭序列
   在细胞质区域得出的结果，并不能作为分泌通路糖基化的证据。
4. 对于 O-GalNAc，只将 S/T 密度用作描述性特征，然后检视
   合适的预测工具以及细胞/转移酶背景。**不要排除 SP/TP 基序**：
   相邻的 Pro 可能是有利的，这取决于具体的 GalNAc 转移酶和上下文背景。
   见[GalNAc-T 底物研究](https://doi.org/10.1093/glycob/cwu089)。
5. 提出明确编号的突变，列出每一个被改变的残基，并对整个产物重新扫描，检查丢失/新产生的重叠基序。应独立于糖基化情况评估结构和
   表达方面的影响。
6. 通过实验验证占位情况和糖型，需要有定位证据、
   糖链组成/结构方面的置信度，以及该工程目标所需要的生物学检测方法。对于生物类似药的比较，在比较糖链百分比之前，应先匹配样品处理方式、
   分析覆盖范围和定量方法。

## 本地序列分析

标准库辅助脚本 [scripts/glycoengineering_tools.py](scripts/glycoengineering_tools.py)
取代了零散的代码片段。导入时请将本技能的 `scripts/` 目录加入
`PYTHONPATH`，或从该目录运行 Python。它接受原始的经典
20 种氨基酸序列，会归一化空白字符/大小写，并拒绝 FASTA header、
缺口、未知残基和空输入。应先解析 FASTA 记录；不要移除未知残基，因为那样会改变坐标。坐标是在归一化后提交的序列中以 1 起始计数的。

```python
from glycoengineering_tools import (
    normalize_sequence, find_n_glycosylation_sequons,
    eliminate_glycosite, add_glycosite, find_st_rich_sites,
)

sequence = normalize_sequence("NNST")
sites = find_n_glycosylation_sequons(sequence)
assert [site["position"] for site in sites] == [1, 2]

mutant = eliminate_glycosite(sequence, 1, "Q")
assert mutant == "QNST"  # 位置 2 处的重叠 sequon 依然存在
assert [site["position"] for site in find_n_glycosylation_sequons(mutant)] == [2]

# 三处预期变化：A1N、P2A、A3T。P->A 必须明确指定。
parent = "APA"
product = add_glycosite(parent, 1, "T", allow_proline_substitution=True)
changes = [(i, before, after) for i, (before, after) in
           enumerate(zip(parent, product), 1) if before != after]
assert product == "NAT" and len(changes) == 3

# 密度是残基的比例，不是 O-糖基化概率。
o_candidates = find_st_rich_sites("STPST", window=7, min_st_fraction=0.4)
assert [site["position"] for site in o_candidates] == [1, 2, 4, 5]
```

`eliminate_glycosite` 需要一个完整的经典 sequon，以及一个非 N 的单残基
替换。`add_glycosite` 最多可以改变三个残基；它会保留 +2 位置上已存在的 S/T。两个函数都不预测突变体的折叠方式、糖链占位情况、
功能或耐受性。即使没有糖链方面的影响，N 到 Q 的替换也可能改变蛋白质的行为。

S/T 密度窗口必须是一个正奇数。末端窗口会缩短，
其分母是实际的窗口长度。密集区域可能有助于筛选黏蛋白样序列；孤立的真实 O-GalNAc 位点可能会被漏掉。

对于批量分析，应保留标识符和归一化后的序列长度：

```python
sequences = {"overlap": "NNST", "control": "APAA", "mucin_like": "STPST"}
rows = []
for name, raw_sequence in sequences.items():
    seq = normalize_sequence(raw_sequence)
    positions = [site["position"] for site in find_n_glycosylation_sequons(seq)]
    rows.append({"protein": name, "length": len(seq),
                 "n_sequon_positions": positions,
                 "n_sequons_per_100_residues": 100 * len(positions) / len(seq),
                 "st_rich_positions": [site["position"] for site in find_st_rich_sites(seq)]})
```

## 预测服务

使用官方提供的表单，它们接受 FASTA 格式并返回网页结果；本技能
不提供稳定的提交 API 或任务轮询端点。保存一个 CGI URL 并不等于提交了任务。应将输出、输入和服务版本一起保存。

| 服务 | 当前文档记载的适用范围与解读方式 |
| --- | --- |
| [NetNGlyc 1.0](https://services.healthtech.dtu.dk/services/NetNGlyc-1.0/) | 人类 N-糖基化；报告网络潜力和评审团一致性。默认阈值 0.5；不是经过校准的占位概率。最多 2,000 条序列 / 总计 200,000 个残基 / 每条序列 4,000 个残基。会运行 SignalP，但不检查细胞外拓扑结构。该服务器可能对 N-P-S/T 打分；除非有独立证据值得复核，否则应将这些排除在经典候选集之外。 |
| [NetOGlyc 4.0](https://services.healthtech.dtu.dk/services/NetOGlyc-4.0/) | 哺乳动物黏蛋白型 O-GalNAc；输出 GFF2 置信度分数，分数**大于** 0.5 标记为阳性。最多 50 条序列 / 总计 200,000 个残基 / 每条序列 4,000 个残基。建议使用包含信号肽的完整序列；孤立位点在两侧都需要 15 个残基的侧翼上下文。阳性结果支持的是区域可能性，而不是保证的位点占位，也不代表超出该模型 O-GalNAc 范围之外的糖链类型。 |

本次更新审查了服务文档和示例输出；在本次刷新过程中没有提交新的预测任务。

## 使用 GlycoSHIELD 进行结构屏蔽

[GlycoSHIELD](https://gitlab.mpcdf.mpg.de/dioscuri-biophysics/glycoshield-md/)
将预先模拟好的糖链构象嫁接到蛋白质结构上，并过滤空间位阻冲突。它不预测哪些 sequon 会被占位，也不会为每个查询运行全新的分子
动力学模拟。见 [Tsai et al., 2024](https://doi.org/10.1016/j.cell.2024.01.034)。

关于锚定的源码版本、安装方法、直接 Python API、输入映射和 SASA 分析，见
[references/glycoshield.md](references/glycoshield.md)。**经审查的上游 CLI 会静默忽略若干已解析的选项，包括 `--mode`、
`--threshold` 和 `--dryrun`；应使用文档中记载的直接 API 变通方案。**输出
包括每个位点的 PDB/XTC 集合,以及编码在 PDB B-factor 列中的屏蔽程度；
这些值并不是晶体学温度因子。

## 数据库证据与糖链记法

关于实时的 GlyTouCan SPARQL 查询、GlyConnect 访问限制、经整理的资源和
记法，见[references/glycan_databases.md](references/glycan_databases.md)。查询确切的登录号，并保留数据集/数据来源的日期、物种、
组织/细胞背景以及支持性出版物。记录缺失或服务错误并不能证明某个蛋白质未被糖基化。

像 `Hex:5 HexNAc:4 dHex:1` 这样的单糖组成并不能解析连接方式、
分支位置，也无法区分 GlcNAc 和 GalNAc。没有连接方式的示意图只是图示，并非 IUPAC 简缩记法。应在可能的情况下使用真实序列
（保留不确定性的 WURCS/GlycoCT/IUPAC 记法）和登录号。核心岩藻糖连接在 N-糖链最内侧的 GlcNAc 上，而不是核心甘露糖上。

## 抗体工程决策

应以一套明确的方案（通常是 EU）给 Fc 突变编号，然后将其映射到
实际的构建体上。EU 编号中的 N297 并不是孤立 Fc FASTA 序列中的第 297 个残基。Fc 糖链
和任何 Fab 糖链必须通过分析方法区分开来。

| 目标 | 候选策略 | 所需的解读方式 |
| --- | --- | --- |
| 增强 FcγRIIIa 结合 / ADCC | 在保留糖链的同时降低 Fc 核心岩藻糖化程度 | 效应大小取决于抗体、受体和检测方法；不要假设存在普遍适用的提升幅度。[结构证据](https://pubmed.ncbi.nlm.nih.gov/22023369/)。 |
| 移除经典 Fc N-糖基化位点 | N297Q/A/D，或用 T299A 破坏 +2 位置残基 | 这是对 sequon 的破坏；不能保证其他方面的结构或效应器功能保持不变。应验证实际产物。 |
| 改变血清持久性 | 结合相关蛋白表征糖型特异性的清除情况 | IgG 高甘露糖糖型的清除可能会增加；唾液酸化并不是普遍适用的 IgG 半衰期配方。[人体 PK 研究](https://pubmed.ncbi.nlm.nih.gov/21421994/)。 |
| 研究 Fc 的抗炎活性 | 比较明确定义的唾液酸化糖型 | 连接方式、制备方法和生物学模型都很重要。在特定模型中获得的阳性结果并不能确立一个普遍适用的 IVIG 机制。[明确的 Fc 研究](https://pubmed.ncbi.nlm.nih.gov/18420934/)。 |
| 降低非人源糖链表位 | 测量 α-Gal 和 Neu5Gc 并选择兼容的生产条件 | 仅靠序列编辑并不能控制宿主的糖链加工过程。 |
| 研究表位可及性 | 引入或移除一个已映射的表面 sequon | 确认占位情况、折叠、结合和抗原性；屏蔽计算只是几何学上的假设。 |

像 S298A/E333A/K334A 或包含 F243L 的 Fc 序列变体
可能同时改变受体相互作用和宿主依赖性的糖链加工。不要
将单独的 F243L 标记为一个确定性的去岩藻糖化开关。参见
[2026 年 Fc 变体糖链研究](https://pubmed.ncbi.nlm.nih.gov/41873859/)。

## 实验解读与验证边界

糖肽搜索可以支持肽段身份、组成，有时还可以支持位点定位，
但无法解析出完整的糖链结构。应审查定位片段、相互竞争的归属结果、搜索空间的选择,以及错误控制。在
[Byonic](https://support.proteinmetrics.com/hc/en-us/articles/18139992247060-Byonic-O-Linked-Glycopeptide-Analysis)
中，组成并不能确定拓扑结构；即使识别出一个糖肽，O-糖基化位点的歧义性仍可能存在。检测到的各糖型之间的相对信号并不自动等同于绝对
位点占位；占位计算需要恰当的修饰型和未修饰型分母，以及分析响应方面的考量。

本地序列行为已通过合成测试覆盖。公共登录号查询已实际执行；API 错误处理是模拟的。GlycoSHIELD 的源码/参数处理已经过检查，但完整的构象嫁接、GROMACS SASA、DTU 任务、商业 MS
软件以及生物学性能均未实际执行。支持性参考资料记录了服务/源码审查日期和尚未解决的访问缺口。
