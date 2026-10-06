---
name: tellurium
description: 使用 Tellurium 和 libRoadRunner 模拟来自 SBML 或 Antimony 的生化动力学模型，检查模型单位，比较确定性的参数扰动，并导出和重放 SBML 加 SED-ML 的 COMBINE 归档。适用于反应网络时间过程、动力学参数、浓度动态和可复现的模拟实验；稳态的基于约束的代谢通量分析属于 cobrapy。
license: MIT
compatibility: 需要 Python 3.11，以及 Tellurium 2.2.13.1、libRoadRunner 2.10.0、Antimony 3.2.0、python-libsbml 5.21.2、python-libsedml 2.0.34 和 python-libcombine 0.2.20。仅安装时需要网络。原生 wheel 已在 macOS ARM64 上测试。无需凭据或外部服务。
metadata:
  version: "1.1"
  skill-author: K-Dense Inc.
  upstream-version: "2.2.13.1"
  last-reviewed: "2026-10-01"
---

# Tellurium 动力学实验

## 何时使用

使用此技能处理来自本地模型的确定性反应网络轨迹以及相互独立的参数条件。辅助脚本会执行 SBML 一致性检查、CVODE 积分以及真正的 COMBINE 归档重放。它会导出每个条件的确切 SBML 以及 SED-ML 实验，而不是交出一个未经记录的 notebook 状态。

## 运行时

```bash
uv venv --python 3.11 kinetic-env
uv pip install --python kinetic-env/bin/python tellurium==2.2.13.1 libroadrunner==2.10.0 \
  antimony==3.2.0 python-libsbml==5.21.2 python-libsedml==2.0.34 python-libcombine==0.2.20
```

完整工作流已在 macOS ARM64 上使用这些包运行过。它使用 libSEDML 构建 SED-ML，并使用 Tellurium/libCombine 构建归档；此辅助脚本不需要 PhraSEDML。无界面运行可以设置 `MPLBACKEND=Agg`。辅助脚本不会打开任何绘图窗口。

这六个固定版本已于 2026-10-01 对照官方 PyPI 元数据重新核对。RoadRunner 的文档站点仍然显示旧版本横幅；下面的求解器设置也已对照已发布的 2.10.0 源码和已安装的原生运行时进行了核对。

## 工作流程

1. 检查所提供模型的隔室（compartment）、物种、初始条件、边界物种、反应、参数定义以及规则/事件。明确科学问题，并区分机理动力学模型与通量平衡重建。记录源模型、版本以及任何文献参数；不要把示例模型当作经过实验校准的模型。
2. 在解读轨迹之前先检查单位。SBML 反应速率具有量/时间的单位；物种可能具有浓度或量的语义。在体积固定的一级模型中，`k*A*cell` 会把对浓度的依赖转换为量/时间。辅助脚本会检查 SBML 一致性并保留每一条警告，包括未定义的单位。未定义的单位会被报告为空/无法确定，而不是默默地假定其为 SI 单位。
3. 按照 [references/experiments.md](references/experiments.md) 中描述的 JSON 格式选择浓度输出和实验。时间值使用模型自己的时间单位。经测试的辅助脚本对 `hasOnlySubstanceUnits=false` 的物种输出浓度；它会拒绝仅按量选择的情况，以避免在 SED-ML 重放时改变其含义。零维隔室和速率规则模型也会被拒绝；后者需要单独的容差工作流，因为 RoadRunner 2.10.0 对标量容差与状态的排序方式可能不同。
4. 运行基线以及所需的常量全局参数变化。每个情景都从全新的 SBML 模型开始，因此前一个情景的最终浓度不会泄漏到下一个条件中。对物种初始值、隔室体积、赋值规则或随时间变化的输入所做的更改，需要显式的模型修改以及相应的测试；它们不是此辅助脚本中隐藏的参数突变。
5. 检查输出是否有限、符号、相关的守恒关系以及时间尺度。当科学解读取决于微小差异时，通过在更严格的容差下重复运行来检查求解器敏感性。一条平滑的曲线或归档重放误差为零，并不能证明模型有效或参数可识别。绝不要为了掩盖求解器或模型问题而把负浓度截断为零。
6. 查看 `report.json` 中的 COMBINE 重放比较、模型警告和单位。辅助脚本会重放它自己生成的归档，并将每个选定的值与直接轨迹进行比较。交付归档、报告、源模型、实验配置和 CSV 曲线。

## 运行可执行的参考示例

[assets/first-order.ant](assets/first-order.ant) 在一个恒定的 1 升隔室中定义了封闭反应 A → B，初始 A=1、B=0 mol/L，k=0.2 每秒。[assets/experiment.json](assets/experiment.json) 在 0 到 10 秒内运行基线和 k=0.4 每秒两个条件。在技能目录下，将解释器指向上面创建的环境：

```bash
MPLBACKEND=Agg kinetic-env/bin/python scripts/kinetic_experiment.py \
  --model assets/first-order.ant --format antimony --experiment assets/experiment.json \
  --output kinetic-reference

# SBML 分支也已测试过；请将这些文件名替换为实际的用户输入。
MPLBACKEND=Agg kinetic-env/bin/python scripts/kinetic_experiment.py \
  --model model.xml --format sbml --experiment experiment.json --output kinetic-analysis
```

输出目录必须是新的。该参考示例已被执行，包括 Antimony 到 SBML 的转换、libSBML 检查、两次直接积分、SED-ML 创建和 COMBINE 重放。两个条件都与解析解 `A(t)=exp(-k*t)`、`B(t)=1-A(t)` 吻合，绝对/相对容差在 2e-8 以内；A+B 守恒在 1e-10 以内，并且在所测试的软件栈上，归档重放与直接输出完全一致。额外的检查使用了 5 升隔室和 10 mol 的初始量（2 mol/L），将每个 SED-ML 物种的 XPath 对照其实际的 SBML 文件进行解析，并验证求解器容差的缩放。这验证的是这个受控示例；任意 SBML 包、事件、延迟或随机模型不在这些测试的覆盖范围之内。

## 产出物

| 文件 | 内容 |
| --- | --- |
| `baseline.csv`、其他情景的 CSV | 时间和选定的浓度，物种表头带方括号 |
| `model_<scenario>.xml` | 两条执行路径共同使用的确切、独立的 SBML 条件 |
| `experiment.sedml` | 均匀时间过程、CVODE/容差、模型、任务和输出选择 |
| `experiment.omex` | 上述 SBML 文件加上主 SED-ML 和归档清单 |
| `report.json` | 版本、输入/归档校验和、参数、单位、验证发现、初始状态容差向量、最小浓度以及重放差异 |

报告中的 libSEDML 发现属于**解析诊断**。成功执行和结果相等，为这个生成的均匀过程实验能够在 Tellurium 中运行提供了额外证据；它们并不能证明所有 SED-ML 功能或所有模拟器的兼容性。

在 RoadRunner 2.10.0 中，JSON 里的 `absolute_tolerance` 值是对状态/量容差的**标量调整因子**，而不是统一的浓度误差界。归档把这一含义记录为 `KISAO:0000571`；请查看 `initial_state_absolute_tolerances` 以及 [references/experiments.md](references/experiments.md) 中的详细说明。声明的 SBML XPath 命名空间以及显式的刚性/均匀输出设置，可以避免 Tellurium 重放成功时掩盖归档中缺失的上下文。

## 主要参考资料

- [Tellurium 模型加载与导出方法](https://tellurium.readthedocs.io/en/latest/tellurium_methods.html)
- [Antimony 单位与反应语义](https://tellurium.readthedocs.io/en/latest/antimony.html)
- [Tellurium 的 SED-ML 实现](https://tellurium.readthedocs.io/en/latest/_modules/tellurium/sedml/tesedml.html)
- [SED-ML Level 1 Version 3 规范](https://sed-ml.org/documents/sed-ml-L1V3.pdf)
- [RoadRunner 2.10.0 CVODE 实现](https://github.com/sys-bio/roadrunner/blob/v2.10.0/source/CVODEIntegrator.cpp)
- [KiSAO 算法与参数定义](https://github.com/SED-ML/KiSAO/blob/master/kisao.owl)
