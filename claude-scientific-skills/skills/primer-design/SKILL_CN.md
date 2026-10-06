---
name: primer-design
description: 使用 Primer3、明确的热力学条件、基于参考序列的脱靶扩增搜索以及可追溯的序列坐标来设计和审核 PCR 与 RT-qPCR 引物。用于设计引物对、检查现有引物、外显子连接处或异构体特异性检测、变异位点屏蔽、克隆尾巴、多重兼容性以及解读 Primer-BLAST 结果。包含有界的本地电子 PCR（in-silico PCR）和 BLAST 筛选；区分计算得到的候选引物与经过实验验证的检测方法。
license: MIT
compatibility: Requires Python 3.11+ and primer3-py 2.3.1 for design and thermodynamics. Local exhaustive screening uses the standard library; BLAST screening additionally needs blastn and makeblastdb on PATH. Network access is needed only for installation, reference retrieval, or external Primer-BLAST.
metadata:
  version: "1.1"
  skill-author: K-Dense Inc.
  last-reviewed: "2026-10-01"
---

# 引物设计与特异性

以 5' 到 3' 方向生成候选寡核苷酸，并为每个结论附上确切的模板、
化学条件、预期产物和搜索范围。使用所提供的工具计算
依赖序列的量。熟悉的基因名称、良好的
Primer3 罚分或单个 BLAST 比对都无法确立引物的特异性。

## 选择工作流

| 需求 | 从这里开始 |
| --- | --- |
| 新的基因组 PCR 或 RT-qPCR 引物对 | 定义检测和参考序列；设计；评估热力学；筛选产物。 |
| 检查现有引物对 | 准备引物对 TSV；评估完整寡核苷酸和退火核心；使用明确的预期坐标进行筛选。 |
| 外显子连接处、转录本异构体、等位基因区分 | 阅读 [design-workflows.md](references/design-workflows.md)；在施加约束之前提供序列注释。 |
| 克隆/带接头尾巴的引物 | 设计退火核心，附加声明的 5' 尾巴，重新评估完整寡核苷酸，重建最终产物。 |
| 多重检测组合 | 在热力学和特异性工具中都启用 `--multiplex`，以评估寡核苷酸相互作用和跨引物对产物。 |
| 简并、亚硫酸氢盐、探针或修饰碱基检测 | 使用 [design-workflows.md](references/design-workflows.md) 中的专门工作流；内置的普通 DNA 模型不足以应对。 |

本地工具支持具有明确 ACGT 核心的成对引物。高级检测
类型有实质性的设计和验证指导，但不会被静默简化
为普通 PCR。本技能负责设计检测；表达量归一化、实验性
诊断验证和向导 RNA 设计是独立的任务。

## 确立检测契约

获取会改变结果的信息；对于探索性设计使用明确的临时假设，
并在报告中标明它们：

- **目的和模板：** 基因组 DNA、cDNA、质粒或其他明确定义的底物；
  目标生物、**带版本号的**登录号、基因组组装/转录本发布版本、链方向、
  所需异构体以及产物大小范围。列出需要的和不需要的模板。
- **序列证据：** 本地 FASTA 及其来源/获取日期和 SHA-256 哈希值。
  基因座摘录使用局部坐标；记录其与完整参考序列的映射关系。
  在相应的筛选中包含相关的旁系同源基因、假基因、替代 contig、转录本异构体、
  载体骨架和宿主序列。
- **反应条件：** 聚合酶/缓冲液、一价盐、二价盐总量、
  dNTP 总量以及寡核苷酸浓度。Primer3 对盐/dNTP 使用 mM，对 DNA 使用 nM。
  将初始反应浓度与 Primer3 的有效退火寡核苷酸浓度参数分开记录。
  引擎默认值属于假设。
- **约束条件：** 目标区间、允许/排除的结合区域、连接处、
  变异排除及其来源、固定引物、尾巴或多重组合成员身份。
  不要猜测外显子边界，也不要静默替换为另一个基因组组装。
- **可接受结果的定义：** 相关的脱靶参考序列、扩增子
  长度、错配搜索限制、对照，以及适合该检测的实验验证。
  不存在能验证所有 PCR 的通用热力学阈值。

使用 [input-contract.md](references/input-contract.md) 获取文件模式和坐标
示例。将 [assay-report-template.md](assets/assay-report-template.md) 复制到
分析目录中以收集证据。参考序列的获取可以手动进行，也可以通过
成熟的序列 API 进行；保留登录号/版本号并验证返回的
序列。所提供的脚本使用本地文件，不会在线提交序列。

## 安装与验证

将 `SKILL_DIR` 设置为本技能实际的安装目录。在单独的分析
目录中工作，使环境、参考数据库和结果不会进入技能目录。

```bash
uv venv --python 3.13 .venv-primer
uv pip install --python .venv-primer/bin/python -r "$SKILL_DIR/assets/requirements.txt"
.venv-primer/bin/python "$SKILL_DIR/scripts/design_primers.py" --help
```

在 Windows 上使用环境中的 `Scripts/python.exe`。设计/热力学
示例针对 primer3-py **2.3.1**，并在 Python **3.13** 下测试。对于可选的
BLAST 引擎，请从官方发行渠道安装 NCBI BLAST+ 并检查：

```bash
blastn -version
makeblastdb -version
```

本地集成检查还覆盖了 BLAST+ 2.17.0；其他版本在声称具有同等覆盖范围之前，
需要检查其输出和搜索行为。

在更新依赖或 API 假设时阅读 [sources.md](references/sources.md)。
脚本会在其 JSON 报告中记录引擎版本和有效设置。

## 1. 设计候选引物

对于初步的功能演示，使用内置的合成序列。它是
非生物学的示例输入，而不是经过实验验证的检测：

```bash
.venv-primer/bin/python "$SKILL_DIR/scripts/design_primers.py" \
  --template "$SKILL_DIR/assets/demo-template.fasta" \
  --preset qpcr --config "$SKILL_DIR/assets/qpcr-config.json" \
  --output design.json --pairs-out pairs.tsv --expected-out expected.tsv
```

在实际工作中，替换为经过审核的目标 FASTA 和约束条件。多记录
FASTA 需要使用 `--record` 指定其确切 ID。`pcr` 预设要求 100–1000 bp；
`qpcr` 要求 70–200 bp。可在配置中覆盖这些起始范围。
示例将其范围覆盖为 90–180 bp，并包含一个特定的目标区间。
多个 `SEQUENCE_TARGET` 区间互为备选：Primer3 至少会侧翼覆盖其中一个。
若要求覆盖每个区间，请提供一个包含所有区间的目标并验证
返回的产物；独立的检测需要独立的设计运行。

该工具：

- 将经过验证的 `sequence_args` 和 `global_args` 传递给 Primer3。不受支持或
  拼写错误的标签会导致失败，而不是静默改变任务。
- 将模板中的模糊位置转换为 `N`，并禁止引物中出现模糊碱基。
  它不会将小写序列解释为重复序列掩码；请使用明确的排除区间。
- 可选地以**所提供模板的坐标**导入 `--mask-bed` 排除区间。
  仅在验证参考序列映射之后，才使用 BED 区间进行变异/重复序列屏蔽；
  它不会推断等位基因频率，也不会转换任意的 VCF。
- 根据模板验证返回的正向和反向序列，并检查
  产物长度。Primer3 的右引物位置会被转换为半开的
  结合区间；反向引物已经是订购方向。
- 可选地将 `--forward-tail` 和 `--reverse-tail` 附加到核心上。设计评分
  和核心 Tm 不包含这些尾巴；第 2 步会检查完整的寡核苷酸。

当找不到候选引物时，检查 `engine_explanations`。修改一个在生物学上
有依据的约束并重新运行；不要静默放宽所有约束，也不要返回
编造的序列。在比较参数选择时保留之前的报告。

`expected.tsv` 描述的是**设计模板上**的预期产物。如果筛选
另一个参考序列，请将这些坐标映射到其确切的记录 ID 和方向。
cDNA 产物不能被重新标注为跨越内含子的基因组区间。

## 2. 评估热力学

使用**与设计相同的化学条件**。以下明确的数值与
内置的设计默认值一致；当实际条件不同时，请一并替换：

```bash
.venv-primer/bin/python "$SKILL_DIR/scripts/check_thermodynamics.py" \
  --pairs pairs.tsv --mv-conc 50 --dv-conc 1.5 --dntp-conc 0.6 \
  --dna-conc 50 --temp-c 37 --output thermodynamics.json
```

报告包含核心 Tm、核心和完整寡核苷酸的发夹结构/同源二聚体、完整寡核苷酸的
异源二聚体、自身 3' 端稳定性，以及寡核苷酸之间两个方向的 3'
端稳定性计算。Delta-G 和
delta-H 以 kcal/mol 报告；delta-S 以 cal/(mol K) 报告。`--temp-c` 控制
计算 delta-G 的温度，**而不是**推荐的 PCR 退火温度。

如果设计时使用了不同的 Tm/盐模型，也要设置 `--tm-method` 和
`--salt-corrections-method` 以保持一致；参见输入契约中的映射。

对于检测组合，添加 `--multiplex` 以检查所有无序的寡核苷酸组合，包括
不同引物对之间的正向/正向和反向/反向组合。要区分将被合并使用的组合
与将被分别测试的备选候选引物。

在解读这些数值之前阅读 [thermodynamics.md](references/thermodynamics.md)。
长于 60 个碱基的完整寡核苷酸会被报告为未解析；它们永远不会被
静默截断。修饰碱基和简并混合物需要合适的模型。
热力学预测支持排序和实验规划，而不能笼统地
宣称引物质量良好。
非有限的 Tm 或等于/低于绝对零度的 Tm 会作为计算/输入
失败被拒绝；这样的结果不能被当作普通的低 Tm 引物进行排序。

## 3. 筛选扩增产物

在做出特异性声明之前阅读 [specificity.md](references/specificity.md)。
在两条链上搜索每条引物，并将朝内的结合位点配对。单独的结合
命中并不是扩增子；没有报告命中并不能证明不存在。

### 穷举式有界本地搜索

```bash
.venv-primer/bin/python "$SKILL_DIR/scripts/screen_specificity.py" \
  --pairs pairs.tsv --reference "$SKILL_DIR/assets/demo-template.fasta" \
  --expected expected.tsv --engine exhaustive \
  --min-product 40 --max-product 1000 --max-mismatches 2 \
  --three-prime-bases 5 --max-three-prime-mismatches 0 \
  --output specificity.json
```

该命令在**有界的本地参考序列**中枚举全长、无空位的结合位点，
并检查每个引物对的 F/R、R/F、F/F 和 R/R 产物。参考序列中的模糊碱基
会被保守地视为未解析序列；它无法确立一个干净的结果。
错配限制是一种搜索模型，而不是经过验证的聚合酶区分
规则。严格的 3' 端阈值可能会排除可扩增的错配位点；在评估这种不确定性时
请放宽搜索范围。

对于环状分子使用 `--circular RECORD_ID`。跨越环接点的产物使用规范的
起始坐标，其未展开的终点大于参考序列长度；只考虑
跨越至多一个分子的产物。对比较次数、命中数
和产物数的上限可防止无界的工作量；触及上限会使结果不完整。

### BLAST 辅助的本地搜索

```bash
.venv-primer/bin/python "$SKILL_DIR/scripts/screen_specificity.py" \
  --pairs pairs.tsv --reference "$SKILL_DIR/assets/demo-template.fasta" \
  --expected expected.tsv --engine blast \
  --min-product 40 --max-product 1000 --max-mismatches 2 \
  --three-prime-bases 5 --max-three-prime-mismatches 0 \
  --output specificity-blast.json
```

该脚本会构建一个临时的本地 BLAST 数据库，运行短查询比对，
重新检查完整引物长度的候选位点，并记录命令和版本。
它会检查配置的命中上限和工具失败情况。BLAST 发现是启发式的：
执行成功且未达到上限并不能确立穷举式的覆盖。
参考序列会被加载到内存中；对于大型基因组，请规划内存和搜索边界。
该小型示例验证的是执行过程，而不是对人类基因组的灵敏度或可扩展性。

对于更广泛的公共参考序列筛选，请遵循 [specificity.md](references/specificity.md) 中
NCBI Primer-BLAST 的官方工作流，审慎地选择物种、
数据库、预期模板、最大产物长度和错配策略。
提交序列会将其发送给 NCBI；仅限本地的工作应保留在本地。Primer-BLAST
不是这些脚本所实现的有文档的 REST API。

### 解读结果

- `potential_off_target`：检查每个意外产物，包括其方向、
  长度、错配位置和参考序列身份；重新设计或论证其相关性。
- `intended_target_not_found`：在得出特异性结论之前，解决映射、参考序列、
  序列和搜索方面的问题。
- `no_expected_target`：结果只是一份产物清单，没有针对特定目标的
  结论。请提供该检测所有预期产物的区间。
- `incomplete`：参考序列的不确定性、资源限制或计算失败使
  结论悬而未决。检查报告的原因并适当地重复执行。
- `no_off_target_found_within_search_scope`：说明确切的参考序列和搜索
  模型。检查报告中的穷举/启发式标志；这并不是经验性验证。

对于多重反应，在特异性命令以及
热力学命令中都添加 `--multiplex`。然后特异性工具会搜索每一种跨引物对的
寡核苷酸组合，并保留原始的寡核苷酸身份和尾巴。它将
跨引物对产物视为非预期产物；有意共享引物的设计需要
明确的独立组合以及经过审核的预期产物。
`--max-panel-combinations` 上限默认为 10,000，并在展开之前进行检查。
热力学 `--multiplex` 检查结构；特异性 `--multiplex` 检查
参考序列上的产物。两者对于该组合评估都是必需的。

## 4. 验证检测并交付证据

根据检测目的、覆盖范围、特异性证据和化学条件来选择候选引物，
而不仅仅是看最低的 Primer3 罚分。当仍存在不确定性时，保留多个候选引物。
遵循 [design-workflows.md](references/design-workflows.md) 进行相关的
实验检查：预期产物的身份/大小、阴性对照和无模板对照、
RT-qPCR 的基因组污染对照，以及在打算定量时进行效率/动态范围评估。
单一的熔解峰本身并不能证明产物身份。

交付填写完整的[报告模板](assets/assay-report-template.md)、引物对 TSV、
设计/热力学/特异性 JSON 以及来源清单。包括：

1. 确切的订购序列、分开列出的退火核心和尾巴、引物长度、
   预期产物的坐标/大小，以及任何相关的转录本/连接处映射。
2. 化学条件和模型设置；引擎版本；参考序列的登录号/发布版本、来源、
   获取日期和文件哈希值；明确的排除项及其理由。
3. 预期产物和潜在的非预期产物；来自未知碱基、
   不完整参考序列、启发式搜索、上限以及不受支持的检测化学的不确定性。
4. 实际获得的实验证据、尚待进行的验证，以及推荐每个候选引物的
   理由。准确标注未经测试的候选引物。

## 本实现的验证与局限

位于 `tests/primer-design/` 的仓库测试套件覆盖了实际的 Primer3 计算、
方向和坐标重建、屏蔽、尾巴、浓度处理、
脱靶产物几何结构、错配/模糊碱基行为、失败状态，以及在安装了可执行文件时的本地
BLAST 集成。合成测试夹具确立的是软件行为；它们不能验证生物学检测，也不能证明全基因组范围的召回率。

工具在计算完成时返回 0，在设计完成但没有
候选引物或长寡核苷酸热力学不完整时返回 1，在输入无效或工具
失败时返回 2。即使退出码为 0，也要读取 JSON 中的科学状态：发现脱靶
是一次成功完成的计算。有关筛选特有的退出码，请参见输入契约。

## 引用 Scientific Agent Skills

如果在已发表的工作中使用，请引用 [sources.md](references/sources.md) 中的上游方法
以及 [Scientific Agent Skills](https://arxiv.org/abs/2609.00065)。报告重现实际分析
所需的软件版本和检测特定的设置。
