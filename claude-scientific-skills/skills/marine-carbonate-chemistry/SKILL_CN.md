---
name: marine-carbonate-chemistry
description: 使用 PyCO2SYS 求解海水碳酸盐化学问题，适用于化学海洋学、海洋酸化和海洋碳循环研究。用于配对的总碱度、溶解无机碳、pH 或海水 pCO2/fCO2 测量值；碳酸盐物种分配；文石和方石灰的饱和度；Revelle 因子；实验室到现场的温度和压力校正；以及测量不确定度传播。适用于碳酸盐系统计算，不适用于一般水化学物种分配或海气气体通量估算。
license: MIT
compatibility: Requires Python 3.13 with PyCO2SYS 1.8.3.4 and NumPy. Network access is needed only to install packages or obtain external data; bundled calculations run locally without credentials.
metadata:
  version: "1.1"
  skill-author: K-Dense Inc.
  upstream-version: "PyCO2SYS 1.8.3.4"
  last-reviewed: "2026-10-01"
---

# Marine Carbonate Chemistry

将两个独立的海水碳酸盐测量值转化为可复现的物种分配表、矿物饱和度估算结果，
以及一份计算假设的记录。目标版本为 **PyCO2SYS 1.8.3.4**，已用 Python 3.13 和
NumPy 2.5.3 测试。截至 2026-10-01 的审查，这仍是 PyPI 上的稳定发布版本。
[v2 文档](https://mvdh.xyz/PyCO2SYS/)针对的是带有破坏性变更的测试版；对于此
固定版本请使用 v1 文档。

## 何时使用

- 分析瓶装样本、船载碳酸盐测量，或酸化实验。
- 根据一对有效的测量值计算总量标尺 pH、海水 pCO2/fCO2、碳酸根离子、文石/
  方石灰饱和状态，或 Revelle 因子。
- 将在实验室条件下确定的系统转换为指定的海洋条件。
- 量化所陈述的测量不确定度如何影响计算结果。

此工作流关注的是海水碳酸盐平衡。淡水、具有大量未表征碱度的孔隙水、超出所选
校准范围的卤水，以及反应/传输模型都需要额外的化学知识和验证。不要仅凭碳酸盐
平衡就推断出海气通量或大气碳清除量。

## 确立测量契约

在运行求解器之前，先确定两个测量变量、它们的单位、质量标志，以及它们的
温度/压力基准。保留一份单独的来源表，其中包含站位、深度、时间戳、方法、
参考材料和原始 QC 代码，并通过样本 ID 关联。不要将缺失值或被拒绝的测量值
当作零处理。

| 量 | 必需的约定 |
|---|---|
| 总碱度 (TA)、DIC、营养盐 | 每**千克海水**微摩尔，不是每升或每千克水 |
| 盐度 | 实用盐度（Practical Salinity），不是以 g/kg 表示的绝对盐度 |
| 温度 | 现场/测量温度，摄氏度，不是位势温度或保守温度 |
| 压力 | 以 dbar 表示的海压；表层样本为 0，不是 1 个大气压 |
| pH | 陈明的总量、海水、自由或 NBS 标尺，在陈明的测量条件下 |
| pCO2 / fCO2 | 以微大气压表示的海水分压/逸度；这两者是不同的量 |

对于封闭样本，TA 和 DIC 在求解器的温度/压力转换过程中保持恒定。pH 和气体
参数会发生变化。在不同条件下测量的两个输入不能简单地共享一个 `temperature`
值。首先要确立一致的测量基准。温度校正不能修复由气体交换、生物活动、蒸发，
或矿物溶解/沉淀所造成的样本变化。

使用两个独立的碳酸盐参数。pCO2 加 fCO2 不构成独立的一对。三个或更多的测量值
可以进行过度确定检验：求解独立的配对，并比较预测与测量的第三个参数（包括其
不确定度）。不要为了掩盖校准或标尺不匹配而对不一致的解取平均。

## 安装

在用户的工作目录中创建一个专用环境：

```bash
uv venv --python 3.13 .venv
uv pip install --python .venv/bin/python "PyCO2SYS==1.8.3.4" "numpy==2.5.3"
```

在 Windows 上，该环境的解释器是 `.venv/Scripts/python.exe`。下面的命令使用
POSIX 解释器路径。将 shell 变量 `SKILL_DIR` 设置为此已安装技能的目录。将输入
和生成的输出保留在工作目录中。

## 工作流程

1. **准备配对测量值。** 使用
   [references/input-and-results.md](references/input-and-results.md) 中的
   模式。在创建输入文件之前解决单位和质量标志问题。明确提供磷酸盐和硅酸盐；
   零值是一个需要证明合理性的假设，而不是缺失数据的代码。
2. **选择平衡常数。** 阅读
   [references/chemistry-decisions.md](references/chemistry-decisions.md)
   了解 pH 标尺、碳酸常数、硼酸盐、饱和度解读和不确定度限制。匹配研究所使用
   的经过验证的约定并报告它。该辅助工具支持碳酸选项 10 和 15；其他体系需要
   单独经过验证的直接 PyCO2SYS 调用。
3. **使用 `scripts/solve_carbonate.py` 求解。** 它会验证完整的输入表，求解
   该配对，检查有限的输出值和 DIC 物种平衡，然后将 `carbonate.csv` 和
   `provenance.json` 写入一个新的输出目录。
4. **检查标志和一致性。** 检查校准范围和气体压力标志、碳酸盐平衡、可用时的
   测量第三参数残差，以及对照项。成功求解并不能验证样本、常数或测量方法的
   正确性。
5. **按预期条件报告。** 以 `_out` 结尾的结果描述的是所提供的输出温度/压力。
   没有后缀的结果描述的是输入条件。气体结果保留该辅助工具未经校正的流体静
   力气体约定（见下文）。将参数配对、pH 标尺、单位、常数、营养盐假设、不确定
   度范围、软件版本，以及被排除/标记的样本一并包含在结果表中。

## 示例分析：封闭样本条件校正

以下数值是合成数据，不是实地观测数据。将其保存为工作目录中的 `samples.csv`。
这两个样本仅在 DIC 上有差异；第二个样本代表固定碱度的 CO2 添加对比。它们的
测量条件为 25 C 和 0 dbar；同时还请求了 10 C 和 1000 dbar 条件下的结果。

```csv
sample_id,par1,par2,salinity,temperature,pressure,total_phosphate,total_silicate,temperature_out,pressure_out,u_par1,u_par2
baseline,2300,2000,35,25,0,0,0,10,1000,2,2
added_co2,2300,2100,35,25,0,0,0,10,1000,2,2
```

从该工作目录运行：

```bash
.venv/bin/python "$SKILL_DIR/scripts/solve_carbonate.py" samples.csv \
  --par1-type alkalinity --par2-type dic --k-carbonic 10 \
  --output-dir carbonate-results
```

对于基线样本，经测试的版本给出输入条件下的总量 pH 为 **8.045886**，pCO2 为
**396.958 微大气压**，文石饱和度为 **3.386201**。在指定的输出条件下，总量
pH 为 **8.241241**，文石饱和度为 **2.605691**。这些四舍五入的数值是针对此
确切设置的回归检验结果，不是通用的海水基准值。仅考虑 TA 和 DIC 独立的 2
微摩尔/千克不确定度时，`u_pH_total` 约为 **0.004580**。这不包括平衡常数和
其他输入的不确定度。两行都带有 `gas_pressure_correction_disabled_output`
标志：输出的 pH 和矿物饱和度包含压力效应，但报告的 pCO2/fCO2 不包含对 CO2
溶解度和逸度的流体静力校正。不要将这些气体值直接与经过压力校正的次表层
传感器测量值进行比较。

对于 TA + 测量的 pH，只有在来源明确标明是总量标尺 pH 时，才使用
`--par2-type ph --ph-scale total`；将 `par2` 和 `u_par2` 替换为测量的 pH
及其绝对标准不确定度。仅名为 `pH` 的列不足以确立其标尺。

## 不确定度与解读

可选的 `u_` 输入列包含绝对的**一个标准偏差**不确定度。它们会在每个所请求的
条件下传播到总量 pH、pCO2 和文石饱和度。该辅助工具假设误差是独立的，并将
未列出的输入/常数视为精确值。对于协方差、常数不确定度或强非线性不确定度，
请遵循决策指南并验证一个定制的传播过程，而不要将这些输出称为一份完整的
不确定度预算。

Omega < 1 表示相对于所命名的矿物处于热力学未饱和状态。它并不能确立溶解速率
或生物的反应。在未配对的样本之间较低的 pH，本身并不能证明存在人为酸化趋势。

## 来源与验证边界

- [PyCO2SYS v1 参数、单位、设置和结果键](https://pyco2sys.readthedocs.io/en/latest/co2sys_nd/)
- [不确定度传播](https://pyco2sys.readthedocs.io/en/latest/uncertainty/)
- [上游验证](https://pyco2sys.readthedocs.io/en/latest/validate/)
- [稳定发布版本](https://github.com/mvdh7/PyCO2SYS/releases/tag/v1.8.3.4)
- [Humphreys et al. (2022), PyCO2SYS v1.8](https://doi.org/10.5194/gmd-15-15-2022)

仓库测试涵盖了固定版本的求解器、独立配对的往返验证、碳平衡、pH 标尺等价性、
条件校正、Revelle 因子导数、气体压力约定、不确定度求和，以及该示例分析。该
辅助工具调用的是本地 `pyco2.sys` Python API；它没有任何 HTTP 端点或身份验证。
测试建立的是软件行为，不是独立的实地数据验证；上游的验证页面也包含历史性
示例，包括一个已移除的 `pyco2.test` 接口。
