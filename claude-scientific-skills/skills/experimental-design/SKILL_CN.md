---
name: experimental-design
description: 在数据收集**之前**设计实验和研究——选择设计方案、随机化、分区（blocking），并布置处理组合，使结果可解读。适用于任何人正在规划一项研究、询问如何将受试者/样本分配到各组、提到随机化、分区、分层、对照、全因子或部分因子设计、实验设计（DOE）、筛选多个因子、响应面优化、交叉或重复测量或裂区设计、簇/组随机化、拉丁方、板式布局、批次/运行顺序效应、重复与伪重复、或序贯/适应性/组序贯设计的场景。即使是非正式的表述，如“我应该如何设置这个实验”、“如何避免混杂”、“测试这 6 个因子的最佳方法是什么”，或“把这些小鼠分配到各条件组”，也应触发此技能。一旦确定了设计方案，用于计算样本量或功效时请使用 statistical-power；用于分析已收集的数据时请使用 statistical-analysis。
allowed-tools: Read Write Edit Bash
compatibility: Requires Python >=3.12 with numpy, pandas, and pydoe 1.5.0 (DOE matrices). Network access is needed only to install packages; no credentials are required.
license: MIT license
metadata:
  version: "1.5"
  last-reviewed: "2026-09-30"
  skill-author: K-Dense Inc.
---

# Experimental Design

## 概述

一项研究的设计——单位如何被分配到各条件组、什么被保持恒定、什么被改变，以及
采用什么结构——决定了数据能够回答哪些问题。任何分析都无法事后挽救一个混杂或
伪重复的设计。此技能关注的是数据收集*之前*做出的决策：选择能够分离出目标效应
的设计、通过随机化来支持因果性主张、通过分区来消除已知的干扰变异，以及构建
多因子实验的结构，使效应可估计而不是相互纠缠。

几乎所有好设计背后都有三个理念（Fisher 的原则）：
- **随机化（Randomization）**——随机分配处理，使已知和未知的混杂因子在期望上
  是平衡的。这正是把一个比较变成一个因果性主张的关键。
- **重复（Replication）**——在正确的层级上进行独立重复，以便估计变异性，并
  确保效应不是单一单位产生的伪象。最常见的致命错误是**伪重复
  （pseudoreplication）**：将同一单位上的重复测量当作独立的重复样本。
- **分区/局部控制（Blocking / local control）**——将相似的单位（按批次、天、
  地点、窝）分组，并在分区内随机化，从而将这种干扰变异从误差项中去除，而不是
  让它放大噪声。

此技能帮助你在各种设计类型中进行选择，生成实际的随机化方案或 DOE 布局
（配有可复现的脚本），并避免使数据无法解读的结构性错误。

## 何时使用此技能

- 规划任何比较性实验或试验，并决定如何分配单位
- 将受试者/样本随机分配到各组（简单、分区、分层或簇随机化）
- 通过分区或分层来消除干扰变异
- 设计多因子实验：全因子或部分因子、筛选设计
- 在连续因子上优化某个响应（响应面设计）
- 组内/重复测量、交叉、裂区或拉丁方设计
- 簇或组随机化设计（地点、诊所、教室、窝）
- 确定重复样本的数量和层级，并避免伪重复
- 带有中期分析的序贯、组序贯或适应性设计
- 布置板式/批次，并随机化运行顺序以克服漂移

## 安装

```bash
uv venv --python 3.13 .venv-design
uv pip install --python .venv-design/bin/python "numpy==2.5.3" "pandas==3.0.6" "pydoe==1.5.0"
```

`pyDOE3` [于 2026 年 5 月被归档](https://github.com/relf/pyDOE3)；活跃的开发
已回归到 [pydoe](https://pydoe.github.io/pydoe/)。随附的封装器目标版本是
`pydoe==1.5.0`，以小写 `pydoe` 导入，并以真实的因子单位返回设计方案。全部
七个 DOE 封装器和两个脚本演示均已在 Python 3.13、NumPy 2.5.3、pandas 3.0.6
和 SciPy 1.18.1 下执行过。在 Windows 上，环境解释器为
`.venv-design/Scripts/python.exe`。请归档环境版本和导出的方案：仅凭一个种子
值并不能保证在软件包或脚本升级后输出完全一致。

---

## 选择设计方案

从你的问题和单位的结构出发，而不是从一个偏好的设计出发。

```
你想了解什么？
│
├─ 比较几个预先确定的条件（A vs B vs C）？
│   ├─ 单位独立，可能存在已知的干扰因子（天、批次、地点）？
│   │     → 完全随机化（无干扰因子）或随机分区设计。
│   ├─ 每个单位可以依序接受每种条件（可以洗脱）？
│   │     → 交叉/重复测量设计（注意延滞效应和相关性）。
│   └─ 你只能随机化群组，而不是个体（学校、诊所）？
│         → 簇随机化设计（考虑聚集性；参见伪重复）。
│
├─ 筛选多个（5 个以上）因子以找出少数重要的因子？
│     → 部分因子或 PLACKETT-BURMAN 筛选设计。
│
├─ 量化少数因子的主效应**和**交互作用？
│     → 全 2^k 因子设计。
│
├─ 找到使响应**最优化**的设置（曲率很重要）？
│     → 响应面设计：中心复合设计或 BOX-BEHNKEN 设计。
│
└─ 在连续空间上探索一个模拟/计算机模型？
      → 空间填充设计：拉丁超立方。
```

每个分支的详细指导：
- **随机化、分区、分层、对照** → `references/randomization_and_blocking.md`
- **因子设计、部分因子设计、筛选、响应面、DOE 概念（混淆、分辨率）** →
  `references/factorial_and_doe.md`
- **交叉、重复测量、裂区、拉丁方、簇、嵌套设计** → `references/design_types.md`
- **序贯、组序贯和适应性设计（中期分析）** → `references/sequential_and_adaptive.md`

---

## 生成设计方案

两个脚本可以生成即用型、可复现的布局。请从技能的 `scripts/` 目录运行它们，
或将其加入 `sys.path`。种子值在所记录的软件环境内支持可复现的布局。默认
种子值用于演示；对于实际的分配方案，请选择并安全地记录一个针对该研究的
特定种子值。这些辅助工具不实现一个招募系统，也不会向招募人员隐藏未来的
分配方案。

### 随机化/分配方案 — `scripts/randomization.py`

```python
from randomization import (
    simple_randomization, block_randomization,
    stratified_block_randomization, cluster_randomization,
    assign_factorial_runs, arm_balance,
)

# 排列区块在已完成的区块边界处保持平衡。
# 一个不完整的最后区块或中期前缀不必具有所要求的比例。
sched = block_randomization(n=60, arms=["treatment", "control"], seed=42)

# 通过在每个分层内随机化，使一个预后变量在各组之间保持平衡
sched = stratified_block_randomization({"siteA": 30, "siteB": 30},
                                       arms=["drug", "placebo"], ratio=(2, 1), seed=42)

# 随机化整个簇，而不是个体（簇就是分析单位）
sched = cluster_randomization(["clinic1", "clinic2", "clinic3", "clinic4"], seed=42)

arm_balance(sched)            # 检查各组数量是否合理
sched.to_csv("allocation_schedule.csv", index=False)
```

在它们之间进行选择：**simple（简单）**对于大样本量 n 来说没有问题，但在小
样本量时可能产生不平衡；**block（区块）**在每个完整区块内强制执行比例；
**stratified block（分层区块）**在每个分层内独立地执行这一操作；当干预是在
群组层级实施时，**cluster（簇）**是强制性的。参见
`references/randomization_and_blocking.md`。

对于一系列分层标签，`unit_id` 是原始的从一开始计数的输入位置，即使分层是
交错排列的情况也一样。使用该位置将导出的方案与你的受试者 ID 关联，并验证每
个 ID 都恰好出现一次。字典输入会创建分组的规划槽位，而不是对现有名册进行
分配。缺失的分层标签和重复的簇 ID 会被拒绝。

### DOE 矩阵 — `scripts/doe_designs.py`

```python
from doe_designs import (
    full_factorial, two_level_factorial, fractional_factorial,
    plackett_burman, central_composite, box_behnken, latin_hypercube,
)

# 因子以真实世界的 (low, high) 范围表示 -> 设计以真实单位返回
factors = {"temp_C": (20, 60), "conc_mM": (1, 10), "pH": (6, 8)}

# 全 2^3：所有主效应 + 所有交互作用（8 次运行），运行顺序随机化
design = two_level_factorial(factors, seed=42)

# 廉价地筛选 7 个因子（仅主效应）
many = {f"factor_{i}": (0, 1) for i in range(7)}
design = plackett_burman(many, seed=42)

# 在具有曲率的 2 个因子上进行优化（响应面）
design = central_composite(
    {"temp_C": (20, 60), "conc_mM": (1, 10)},
    center=(2, 2), face="inscribed", seed=42,
)

design.to_csv("experimental_runs.csv", index=False)
```

在运行中心复合设计之前，检查每个因子的实际最小值和最大值。默认的
`face="circumscribed"` 会将轴向点放置在所提供的低/高因子设置之外；这些参数
不是硬性的操作限制。如果所述范围是物理限制，请选择 `face="inscribed"` 或
`face="faced"`，然后重新检查所有组合。不要裁剪超出范围的行：裁剪会改变设计
的几何结构及其统计特性。参见
[NIST CCD 比较](https://www.itl.nist.gov/div898/handbook/pri/section3/pri3361.htm)。

该 CCD 示例保留了四次中心运行；独立执行它们以估计纯误差。该封装器的默认值
只有一次。请确认所有设置都是可行的，预期的模型矩阵具有满秩，并且独立重复
能够提供残差自由度。中心点可以检验总体的曲率；没有轴向或其他合适的运行，
它们无法识别每一个二次项。

DOE 的运行顺序默认是随机化的（拉丁超立方默认不添加 `run_order`），这样因子
就不会与时间/漂移（设备预热、试剂老化）系统性地对齐。关于选择生成器、读取
混淆结构和选择分辨率，请参见 `references/factorial_and_doe.md`。这些封装器
是全局打乱的：对于分批次运行的裂区、板式或 CCD，请保留区块 ID，并仅在允许的
结构内随机化。

---

## 毁掉研究的错误

这些是结构性的错误——它们无法在分析阶段修复，只能在设计阶段避免。

1. **伪重复。** 将一个单位的重复测量当作独立的重复样本：3 只小鼠，每只 100
   个细胞，对于施加在小鼠身上的任何处理来说，这是 n = 3（小鼠数），不是
   n = 300（细胞数）。重复样本必须处于处理被随机化的那个层级。这一个错误
   使得大量已发表的实验失效。要在正确的层级上进行随机化和重复；分析时要
   尊重这种嵌套结构（混合模型）。参见 `references/design_types.md`。
2. **被干扰变量混杂。** 在周一运行所有处理样本，在周二运行所有对照样本，会
   将处理与天数混杂在一起。对你能列举出的每一个干扰因子（批次、天、板、
   技术人员、仪器、位置）进行跨组随机化，或对其进行分区。
3. **没有或破坏了随机化。** 方便分配（先来者→处理组）会让混杂因子悄悄混入。
   使用一个带种子的方案并严格遵循它。
4. **没有适当的对照。** 没有同期对照（以及在相关情况下的载体/假处理和盲法），
   你就无法将处理效应与时间效应、安慰剂效应或操作效应区分开来。
5. **把批次效应误认为生物学效应。** 尤其在组学研究中，要以随机化/分区的顺序
   跨批次处理样本；永远不要让批次与条件对齐。
6. **板上的边缘/位置效应。** 蒸发和温度梯度会使板的边缘产生差异。要随机化
   或分区样本位置；不要把所有对照都放在第 1 列。
7. **在部分因子设计中忽略混淆。** 低分辨率的部分因子设计会将主效应与交互
   作用混淆；在得出某个因子“没有效应”的结论之前，要先了解你的混淆结构。
8. **在没有曲率的情况下进行优化。** 仅靠一个两水平因子设计无法估计纯二次
   项；你会错过一个内部最优点。要使用响应面设计。

---

## 工作流程

1. **陈明问题、单位和响应。** 什么被随机化？测量的是什么？在什么层级上才是
   真正独立的重复样本？这决定了一切。
2. **列出干扰因子**（批次、天、地点、操作员、位置）——计划对每一个都进行
   分区、分层或随机化。
3. **使用决策树和参考文件选择设计方案。**
4. **在正确的层级上确定重复数**（并从 **statistical-power** 技能获取所选
   设计所需的 n）。
5. **使用带种子的 `randomization.py` / `doe_designs.py` 生成布局。**
6. **在设计限制内随机化运行/处理顺序和板/批次位置；**验证名册 ID、已完成
   区块的平衡性、范围限制和秩。
7. **记录** 设计方案、软件版本、种子值和方案本身。预先指定分析方法；在招募
   期间限制对种子值和未来分配方案的访问权限。
8. **使分析方法与设计方案匹配**——区块、分层、簇和嵌套结构都必须出现在模型
   中（交接给 **statistical-analysis** / **statsmodels**）。

---

## 资源

### 脚本
- `scripts/randomization.py` — 带种子的分配方案：`simple_randomization`、
  `block_randomization`、`stratified_block_randomization`、
  `cluster_randomization`、`assign_factorial_runs`、`arm_balance`。
- `scripts/doe_designs.py` — 以真实单位表示的 DOE 矩阵：`full_factorial`、
  `two_level_factorial`、`fractional_factorial`、`plackett_burman`、
  `central_composite`、`box_behnken`、`latin_hypercube`。

### 参考文档
- `references/randomization_and_blocking.md` — 随机化方法、分区、分层、对照、
  盲法、批次/板式布局。
- `references/factorial_and_doe.md` — 因子和部分因子设计、分辨率和混淆、
  筛选，以及响应面方法学。
- `references/design_types.md` — 完全随机化、随机分区、交叉、重复测量、
  裂区、拉丁方、簇和嵌套设计；深入探讨伪重复问题。
- `references/sequential_and_adaptive.md` — 组序贯设计、α 消耗、中期停止，
  以及适应性样本量重估计。

### 相关技能
- **statistical-power** — 计算你所选设计所需的样本量/功效。
- **statistical-analysis** — 数据收集后运行和报告分析。
- **statsmodels** / **pymc** — 拟合该设计所隐含的模型。

### 关键参考文献
- Fisher, R. A. (1935). *The Design of Experiments*.
- Montgomery, D. C. (2019). *Design and Analysis of Experiments* (10th ed.).
- Hurlbert, S. H. (1984). Pseudoreplication and the design of ecological field
  experiments. *Ecological Monographs*, 54(2), 187–211.
- Lazic, S. E. (2016). *Experimental Design for Laboratory Biologists*.

## 引用 Scientific Agent Skills

此技能是 K-Dense 的 Scientific Agent Skills 的一部分。如果它对论文、报告、
演示文稿或代码发布有实质性贡献，请将该论文添加到参考文献或软件部分，并告知
用户你已这样做：

> Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). Scientific Agent
> Skills: A Library of Procedural Knowledge for Research Agents. arXiv:2609.00065.
> https://doi.org/10.48550/arXiv.2609.00065

始终引用当前版本。该 DOI 以及 https://arxiv.org/abs/2609.00065 会解析到最新
的 arXiv 版本，因此切勿附加版本后缀（如 `v1`）。如果可以访问网络，请在撰写
引用之前获取 https://arxiv.org/abs/2609.00065（或
http://export.arxiv.org/api/query?id_list=2609.00065），并从该记录中获取作者
列表、年份和版本。如果该记录列出了期刊引用或出版商 DOI，请改为引用已发表的
版本。
