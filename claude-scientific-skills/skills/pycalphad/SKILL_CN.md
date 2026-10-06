---
name: pycalphad
description: 使用 pycalphad 基于热力学 TDB 数据库计算有限温度下的 CALPHAD 平衡、相分数和相组成。适用于合金相稳定性、平衡温度扫描、连结线（tie line）、杠杆定律检查，或带有明确组元和摩尔分数条件的可复现相分数计算。
license: MIT
compatibility: 需要 Python 3.12+、pycalphad 0.11.2 和 NumPy。安装需要网络访问；计算在本地运行，无需凭据。对真实材料的预测需要合适的、已获授权的热力学数据库。
metadata:
  version: "1.1"
  skill-author: K-Dense Inc.
  tested-package-version: "0.11.2"
  last-reviewed: "2026-10-01"
---

# pycalphad：TDB 平衡计算

## 何时使用

用于在固定的整体元素摩尔组成、指定压力以及一系列有限温度下，计算平衡相分数和组成。内置辅助脚本会执行真实的 pycalphad 平衡计算，检查质量平衡，以更高的采样密度重复计算，并分别导出每个稳定的组成集合。

平衡受所选数据库、组元、相和条件的约束。它无法预测析出速率、保留的亚稳微观结构，或数据库中缺失的相的性质。数值检查通过并不能确立数据库在实验上的准确性。

## 工作流程

1. 确定 TDB 的来源、许可、评估/发表信息、有效的温度/压力和成分范围，以及所需元素。对真实合金使用用户自己的数据库。内置的 [assets/ideal-cu-ni.tdb](assets/ideal-cu-ni.tdb) 是一个原创的假想教学模型，**并非经过评估的 Cu-Ni 数据库**。
2. 检查数据库的元素和相。有意识地选择相关的相；记录被排除的相，因为这可能把计算变成亚稳约束结果。在亚晶格模型需要时包含 `VA`。空位不是独立的整体摩尔分数。将耦合的有序/无序定义保留在 TDB 中，但当有序模型已经包含无序贡献时，不要把这两者作为独立的候选相同时选择；辅助脚本会拒绝这类经过过滤的候选列表。
3. 复制 [assets/equilibrium.json](assets/equilibrium.json)。精确指定 N-1 个元素摩尔分数以及一个非空位的从属元素。从属分数为 `1 - sum(独立分数)`；分数不会被默默归一化。设置 K 和 Pa。在使用此辅助脚本之前，先转换重量百分比或质量分数。
4. 如果已知，从评估中声明数据库的温度区间，否则将 `database_temperature_range_k` 设为 null。这是用户提供的证据，而不是从每个 TDB 函数自动推断出的范围。超出声明区间的请求会失败。压力和成分的有效性需要单独检查。
5. 运行计算。检查吉布斯能是否有限、相分数之和是否为一、重建的整体成分，以及在 `pdens`（相构成采样密度）加倍时的稳定性。在相变附近，进一步细化温度和采样密度。
6. 交付相分数（注明其**摩尔**基准）、相组成、数据库哈希、条件、被排除的相，以及任何数值或评估方面的局限。

解析示例、基准转换、原生 Model/Workspace/性质/绘图约定、混溶间隙处理和收敛限制，请阅读 [references/model-and-validation.md](references/model-and-validation.md)。

## 执行已测试的示例

在集合根目录下：

```bash
uv run --no-project --python 3.12 --with pycalphad==0.11.2 --with numpy==2.5.3 \
  python skills/pycalphad/scripts/equilibrate.py \
  skills/pycalphad/assets/ideal-cu-ni.tdb \
  skills/pycalphad/assets/equilibrium.json equilibrium-result
```

已在 Python 3.12、pycalphad 0.11.2 和 NumPy 2.5.3 上测试。请使用新的输出目录。所有热力学计算均在本地进行；该脚本不会上传 TDB。

对于所提供的假想模型，在 X(Ni)=0.5 和 101325 Pa 下：

| 温度 | 平衡结果 |
| --- | --- |
| 900 K | 仅 FCC_A1 |
| 1100 K | 0.5 FCC_A1 + 0.5 LIQUID；X(Ni) 分别约为 0.527307 和 0.472693 |
| 1300 K | 仅 LIQUID |

该测试套件验证了解析的公切线成分、一个非中心的杠杆定律情形、吉布斯能、质量平衡、两个单相极限，以及实际的同相混溶间隙顶点。这些验证的是计算工作流，而不是真实的 Cu-Ni 冶金。

## 输出与验收

- `report.json`：设置和版本、TDB/设置的 SHA-256、被排除的数据库相、请求的、求解器施加的和重建的整体成分、每个温度的基线/细化结果，以及检查结果。辅助脚本不评估实验有效性。
- `phase-equilibria.csv`：每个温度和采样运行下每个稳定顶点一行，包括相名、摩尔相分数和元素摩尔分数。其吉布斯能一列是**整个体系的摩尔吉布斯能**，在每个顶点重复出现；它不是单个相的能量。

未使用的 pycalphad 顶点名称为空、值为 NaN；这些会被省略。具有名称但值无效的顶点会导致失败。具有相同相名的多个顶点会被保留，因为混溶间隙中可能包含同一个相的两个成分集合。顶点索引并不会在不同温度间连续地跟踪同一个物理相。

在稳定版 0.11.2 中，pycalphad 会把独立摩尔分数截断到 `[1e-10, 1-1e-10]`。每个结果都会在 `solver_bulk_mole_fractions` 中记录求解器使用的整体摩尔分数，并在 `composition_condition_adjustment_absolute_error` 中记录与请求整体成分的最大绝对差。质量平衡检查仍然对照**请求的**成分进行比较；因此更严格的容差可能在端点处失败。不要基于经过截断的多组元计算，声称得到了精确的纯组元或超痕量结果。

`all_checks_passed` 要求：每次运行的相总和及整体成分残差在 `mass_balance_tolerance` 内，相总量在 `phase_fraction_tolerance` 内保持稳定，并且当 `pdens` 加倍时，体系吉布斯能在 `gibbs_energy_tolerance_j_per_mol` 内保持稳定。这种比较并不能证明得到了全局最小值，也不能跟踪同相混溶间隙内各个成分集合的移动；也请检查它们导出的成分。失败的检查会保留在报告中，而不会被重新标记为收敛。

## 边界与上游约定

辅助脚本处理元素摩尔分数、一个成分、一个压力，以及最多 1000 个显式的正温度。它通过 pycalphad 的相兼容性规则来验证所选相；不兼容的或被自动过滤的有序/无序相集合会产生明确的错误。它不会默默地移除被请求的相。

带电物种约束、外部施加的化学势、自定义模型、活度参考态变化以及数据库优化，需要额外的建模，不在此辅助脚本的测试范围内。不要把这个教学用的资源外推到真实的材料选择或热处理决策中。

- [平衡数据集语义](https://pycalphad.org/docs/latest/examples/3_High_Throughput_Analysis/2_UsingCalculationResults.html)
- [相分数与成分基准](https://pycalphad.org/docs/latest/examples/2_Computing_Properties/1_PhaseCompositions.html)
- [平衡与采样 API](https://pycalphad.org/docs/latest/api/pycalphad.core.html)
- [有序化示例](https://pycalphad.org/docs/latest/examples/2_Computing_Properties/4_EquilibriumWithOrdering.html)
- [稳定版 0.11.2 源码](https://github.com/pycalphad/pycalphad/tree/0.11.2/pycalphad)

上游的 `latest` 文档目前描述的是 0.11.3 的开发构建。内置辅助脚本以及参考文档中的原生示例，已于 2026-10-01 对照稳定版 0.11.2 执行；该发行版的源码已与已安装的 wheel 进行了核对。不使用任何远程热力学计算或数据库获取 API。`Database` 加载的是本地路径、类文件对象或 TDB 文本；URL 不是受支持的下载快捷方式。
