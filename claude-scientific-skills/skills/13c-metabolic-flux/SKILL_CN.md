---
name: 13c-metabolic-flux
description: 使用经过验证的原子映射、mfapy同位素模拟、受约束的多起点拟合以及通量谱诊断，从稳态碳-13同位素追踪测量数据中估计细胞内代谢通量。用于13C-MFA、碳追踪、质量同位素分布（MDV/MID）、位置同位素体、平行示踪剂实验，以及判断标记数据是否能约束某条通路的通量。将基于测量标记的推断与COBRA通量平衡分析区分开，并标记出需要非稳态MFA的实验。
license: MIT
compatibility: Python 3.12 with uv and Git for installation. Tested with mfapy 0.6.3 at a10433af16682386548b360297e2476152d46ede, NumPy 2.5.3, SciPy 1.18.1, and NLopt 2.11.0. Network access is needed only to install public dependencies. Inference runs locally without credentials; inputs are JSON.
metadata:
  version: "1.2"
  skill-author: K-Dense Inc.
  last-reviewed: "2026-09-30"
---

# 碳-13代谢通量推断

将经过审查的碳映射、明确的示踪剂混合物以及经过校正的标记测量值，转化为
可行的通量估计以及关于实验能约束哪些通量的证据。请使用内置的求解器，而不要
重新构建同位素平衡或独立拟合每个反应。它运行mfapy的EMU前向模拟器，并用
SciPy在质量平衡的可行空间内拟合通量。它不使用FBA目标函数。

## 范围与所需证据

本实现支持**代谢和同位素稳态**、跨一个或多个示踪剂实验的单一共享
通量状态、非负的单向反应通量，以及碳子集的质量分布。可逆反应被分别
映射为两个方向。测量误差为高斯分布，使用提供的协方差或一个明确声明的
对角近似。

拟合之前，请获取：

- 碳网络以及每个原子分配的来源。仅凭化学计量关系并不能确定标记的
  原子去向何处。将隔室记录为独立的代谢物ID。
- 对两个稳态假设的证据。代谢物丰度稳定并不能确立同位素稳态。
  时间序列标记需要带有池大小和初始标记的INST-MFA；不要将其
  平均化后输入此求解器。
- 每个碳输入的位置同位素体分布，包括未标记的补充物、
  被同化的碳酸氢盐/CO2，以及示踪剂的杂质。
- 片段碳的分配、自然丰度校正历史，以及**报告均值**的
  不确定性。原始峰强度、衍生化光谱和MS/MS转变需要经过
  验证的预处理，才能构建这些输入。
- 通量单位、细胞外速率测量值或一个声明的相对通量参考，以及
  有生物学依据的边界。仅凭标记分数无法设定绝对速率。

如果缺少必要信息，请指明并准备输入模板；不要
编造片段分配、原子映射、同位素校正或测量误差。
准备输入时请阅读 [references/input-contract.md](references/input-contract.md)。
在解读实际拟合结果之前请阅读 [references/inference.md](references/inference.md)。

## 安装经过测试的引擎

在用户的分析目录中运行。将 `SKILL_DIR` 设为此技能的已安装目录，
使用实际解析后的路径。将环境和生成的结果保存在技能目录之外。

```bash
uv venv --python 3.12 .venv-mfa
uv pip install --python .venv-mfa/bin/python -r "$SKILL_DIR/assets/requirements.txt"
```

以下命令使用 `.venv-mfa/bin/python`；在Windows上使用该环境的
`Scripts/python.exe`。mfapy是从一个不可变的Git修订版本安装的，因为它
没有发布在PyPI上。安装过程会执行依赖构建代码；模型输入
是数据，不是用户提供的Python代码。该适配器会在标识符和原子映射
语法到达mfapy内部生成的数值函数之前对其进行限制。

被固定的提交在2026-09-30时与上游 `master` 分支一致。其README将
最新的更改标记为"064"，但其安装后的发行版仍报告为 `0.6.3`；请在
分析记录中同时保留该Git提交和包版本号。刷新后的
NumPy/SciPy固定版本需要Python 3.12或更高版本；上面的命令使用了经测试的3.12
环境。参见 [references/inference.md](references/inference.md) 中经审查的前向模型契约。

## 工作流程

1. **准备明确的输入。** 将相关的模型资产复制到分析目录中，
   然后仅根据经过审查的证据替换其科学内容。内置的模型
   是示范用途，不是经过验证的物种特定重建模型。为每个生物学条件
   使用一个单独的数据集；只有在示踪剂重复实验的生物学通量状态
   有充分理由可共享时，才联合拟合它们。
2. **检查契约和可行性。**

   ```bash
   .venv-mfa/bin/python "$SKILL_DIR/scripts/mfa.py" check \
     --model model.json --data measurements.json --output input-check.json
   ```

   这会检查原子数和守恒性、片段、示踪剂总和、不确定性
   矩阵、边界以及稳态质量平衡的可行性。它无法验证一个
   化学上一致的原子映射在生物学上是否正确，也无法验证样本是否达到了稳态。
3. **运行前向模型。** 以声明的单位提供一个质量平衡的通量向量。
   将预测的标记结果与一个参考值或独立推导的极限值进行比较。

   ```bash
   .venv-mfa/bin/python "$SKILL_DIR/scripts/mfa.py" simulate \
     --model model.json --data measurements.json --fluxes fluxes.json \
     --output simulated-mdvs.json
   ```

4. **拟合并剖析与问题相关的通量。**

   ```bash
   .venv-mfa/bin/python "$SKILL_DIR/scripts/mfa.py" fit \
     --model model.json --data measurements.json --starts 12 --seed 2026 \
     --profile v3 --profile v7 --profile-points 31 --profile-starts 6 \
     --output fit.json
   ```

   将 `v3` 和 `v7` 替换为实际的反应ID。每个剖析点会固定该反应
   并重新优化干扰通量。对于非线性网络，在解读一个剖析之前，
   请用不同的随机种子和更多的起点重复此过程。一个小的残差不等于
   一个可辨识性结果。
5. **检视证据。** 检查失败的起点、残差模式、质量平衡、
   活跃的边界、局部敏感性秩以及剖析状态。按实际的网格
   分辨率报告阈值穿越区间。如果网格过于粗糙，请细化网格。
   每个请求的剖析在给定的误差模型下给出的是单一通量的一个区间；
   多个95%剖析并不构成整个网络的同时95%置信区域。
   如果某个剖析找到了比基线更优的解，请重新运行拟合；不要发布
   过时的区间。一个失败的剖析点是未知的，而不是被数据排除的。
6. **交付一个有边界的科学结果。** 包括模型和数据的哈希值、包
   版本、来源/校正溯源、单位和参考通量、拟合预测值、
   残差诊断、剖析图或表格，以及未解决的通量组合。
   保留该JSON文件。将数据支持的点估计与沿某个平坦方向的
   任意优化器选择区分开。只有在测试了沿该方向预测标记的
   变化之后，才建议进行额外的测量。

## 示例

这些可运行的示例使用合成的、仅含示踪剂的数据。没有隐藏的自然
丰度校正，且示踪剂比例已经包含了未标记的材料。

### 恢复一个通路分支比例；然后移除有信息量的测量值

该解析性的双路径模型让一个两碳底物通过碳保留路径或碳交换
路径。摄取量固定为100。一个80%碳-1标记的进料以及一个M+1 = 0.56
的碳-1片段，确定了保留路径为70，交换路径为30。

```bash
.venv-mfa/bin/python "$SKILL_DIR/scripts/mfa.py" fit \
  --model "$SKILL_DIR/assets/branch-model.json" \
  --data "$SKILL_DIR/assets/branch-identifiable.json" \
  --profile straight --profile-points 41 --output branch-fit.json

.venv-mfa/bin/python "$SKILL_DIR/scripts/mfa.py" fit \
  --model "$SKILL_DIR/assets/branch-model.json" \
  --data "$SKILL_DIR/assets/branch-unresolved.json" \
  --profile straight --output unresolved-fit.json
```

第一次拟合恢复出大约70/30的比例。在其声明的高斯误差模型下，
`straight` 的解析95%区间大约为67.55–72.45；该脚本报告的是
包含阈值穿越点的网格区间。第二次拟合只有整个分子的分布，
而这对两条路径来说是相同的。预期局部秩为零，以及
`unresolved_within_bounds`；其返回的分割比例是一个任意的最优解。

`assets/branch-fluxes.json` 提供了70/30的前向模拟向量。

### 重现一个已发表的循环网络计算

```bash
.venv-mfa/bin/python "$SKILL_DIR/scripts/mfa.py" simulate \
  --model "$SKILL_DIR/assets/tca-model.json" \
  --data "$SKILL_DIR/assets/tca-tracer.json" \
  --fluxes "$SKILL_DIR/assets/tca-fluxes.json" --output tca-simulation.json

.venv-mfa/bin/python "$SKILL_DIR/scripts/mfa.py" fit \
  --model "$SKILL_DIR/assets/tca-model.json" \
  --data "$SKILL_DIR/assets/tca-reference-mdv.json" \
  --profile v3 --profile v7 --output tca-fit.json
```

第一个命令重现了已发表的、四舍五入后的谷氨酸MDV
`[0.3464, 0.2695, 0.2708, 0.0807, 0.0286, 0.0039]`。
第二个命令使用合成的参考测量值，恢复出接近50的谷氨酸支路
通量，同时也认识到这种标记无法解析富马酸/草酰乙酸
交换。一个由约束引起的上边界并不是测量确定的交换区间的证据。

## 解读边界

- 位置同位素体字符串的书写顺序是**从左到右，从碳1到碳N**。
  `"100000"` 表示碳-1标记的葡萄糖。仅凭质量分布无法确定
  该位置混合物。该适配器处理了mfapy反转的整数位序。
- 自然丰度校正和示踪剂纯度校正是不同的操作。
  输入必须处于文档说明的仅含示踪剂的基准下，且示踪剂杂质必须在
  源混合物中以一致的方式表示。不要对同一贡献进行两次校正。
- 一个N碳的质量分布最多只有N个独立成分，因为它的总和为一。
  该工具移除一个分箱并使用缩减后的协方差。在可用时请保留
  跨分箱的相关性。对角SEM拟合明确是近似的。
- `symmetric` 标志表示身份变换和**完全的碳序反转**的等权平均，
  正如内置的富马酸/琥珀酸映射所示。它不是任意的分子
  对称性。其他置换需要一个明确支持的模型表示方式。
- 此CLI不支持：非稳态MFA、反应速率上的同位素效应、
  未建模的池或隔室、MS/MS联合分布、多元素同位素
  校正、分数碳化学计量/伪反应，以及物种规模的
  性能保证。对于这些情形，请使用一个经过验证的专用模型/引擎，
  并保持相同的输入/溯源和可辨识性规范。

## 实现与验证

`scripts/mfa.py` 是该CLI。`scripts/_mfa_model.py` 验证输入并将其适配到
mfapy的EMU模拟器；`scripts/_mfa_fit.py` 处理可行通量坐标、
多起点优化、诊断秩以及剖析计算。
该引擎被固定在 [assets/requirements.txt](assets/requirements.txt) 中。

位于 `tests/13c-metabolic-flux/` 的仓库测试套件检查了已发表的参考值、
解析性分支恢复和似然剖析、未解析的路径和交换、
带相关误差的省略分箱不变性、平行示踪剂、绝对速率
锚定、重复底物的缩合、对称性、无效的映射以及CLI行为。
这些检查确立的是经过测试的数值行为，而不是对用户模型的生物学
验证，也不是相对于任何特定语言模型的测得优势。

## 来源

- [经测试修订版本的mfapy源码](https://github.com/fumiomatsuda/mfapy/tree/a10433af16682386548b360297e2476152d46ede)，版本0.6.3；[API文档](https://fumiomatsuda.github.io/mfapy-document/mfapy.html)。
- Matsuda et al. (2021), [mfapy: An open-source Python package for 13C-based metabolic flux analysis](https://doi.org/10.1016/j.mec.2021.e00177)。
- Antoniewicz, Kelleher, and Stephanopoulos (2007), [Elementary metabolite units (EMU): A novel framework for modeling isotopic distributions](https://doi.org/10.1016/j.ymben.2006.09.001)。
- TCA网络改编自mfapy中MIT许可的示例文件；归属说明
  和完整声明见 [assets/mfapy-license.txt](assets/mfapy-license.txt)。
