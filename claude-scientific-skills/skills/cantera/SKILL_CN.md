---
name: cantera
description: 运行 Cantera 均相化学反应器并评估点火延迟，同时追溯机理来源、进行守恒检验以及数值精细化。适用于燃烧化学动力学、封闭绝热理想气体定容或定压点火、温度历程，或特定机理的点火延迟对比。
license: MIT
compatibility: Requires Python 3.12-3.14, Cantera 3.2.0, and NumPy. Installation needs network access; simulations run locally without credentials. Custom mechanisms must be available as Cantera YAML files.
metadata:
  version: "1.1"
  skill-author: K-Dense Inc.
  tested-package-version: "3.2.0"
  last-reviewed: "2026-09-30"
---

# Cantera：均相点火计算

## 何时使用

适用于具有已知动力学机理、初始温度、压力和摩尔组成的封闭、绝热、
均相理想气体反应器。捆绑的辅助脚本可运行定容和定压两种情况，
并报告一个精确定义的基于温度的延迟值。它不是火焰求解器，
也不是通用的反应器网络构建工具。

计算成功完成只能证明数值执行成功，并不能证明该机理对于所用燃料、
压力、温度、稀释剂或所测量的点火可观测量是有效的。在选择机理、
与实验对比，或解读未分辨/两阶段点火现象时，请阅读
[references/interpretation.md](references/interpretation.md)。

## 工作流程

1. 确定机理及其经过验证的条件范围。保留其来源、版本、引用，
   以及任何修改记录。检查其相态是否为 `ideal-gas`，并确认每种
   反应物、稀释剂和被追踪的物种都存在。对于带有导入的自定义 YAML，
   既要保留原始依赖文件，也要保留生成的相态快照。自定义 Python
   速率扩展还需要保留其原始代码和环境以便重现。
2. 根据实际物理实验选择定容或定压。显式提供 K、Pa、秒以及摩尔量。
   `mole_amounts` 会被归一化为摩尔分数；它不是质量分数的映射。
   报告中会包含归一化后的初始组成。
3. 复制 [assets/hydrogen-ignition.json](assets/hydrogen-ignition.json) 并修改其条件。
   所提供的 H2/O2/Ar 案例使用 Cantera 捆绑的 `h2o2.yaml`，
   作为一个可执行的数值示例；它并非适用于所有氢气实验的推荐方案。
4. 设定一个足够长的时间范围，以观察温度上升及加热率峰值的下降。
   选择足够精细的输出间隔以定位该峰值。设定一个最小温度升高值，
   以区分点火与可忽略的加热或数值噪声。
5. 运行该辅助脚本并检查全部四条历程曲线及报告。如果延迟发生明显
   变化、最大值接近时间边界，或守恒检验未通过，则需再次进行精细化。
   将温度和被追踪物种的历程与实际点火定义进行对比。
6. 将条件集合、机理哈希值、反应器约束、延迟定义、输出间隔、
   数值变化及科学局限性与延迟结果一并报告。

## 执行已测试的示例

从集合根目录运行：

```bash
uv run --no-project --python 3.12 --with cantera==3.2.0 --with numpy==2.5.3 \
  python skills/cantera/scripts/ignition_delay.py \
  skills/cantera/assets/hydrogen-ignition.json hydrogen-result
```

已在 Python 3.12、Cantera 3.2.0 和 NumPy 2.5.3 上测试通过。无需任何
外部求解器可执行文件或凭据。本地相对机理路径会先相对配置文件所在
目录进行解析，然后才使用 Cantera 内置的数据搜索路径。每次运行请使用
新的输出目录。

在 1000 K、101325 Pa、H2:O2:Ar = 2:1:7 的定容示例中，按所述的
`max(dT/dt)` 定义给出的结果约为 **0.313 毫秒**。在 3 毫秒时其温度
约为 2920.67 K，与一次独立的 `UV` 平衡计算结果一致。这些是软件包的
回归测试值，而非实验验证数据。

## 精确延迟与精细化约定

延迟是在均匀输出网格上，`numpy.gradient(T, time, edge_order=2)`
全局最大值所对应的时间。只有当最大温升达到
`minimum_temperature_rise_k`，且该最大值与边界的距离至少为
两个采样点索引时，才会报告该值。否则 `delay_s` 为空（null），
并附带状态说明原因。不会对超出模拟时间范围的延迟进行外推。

该辅助脚本明确使用 Cantera 3.2 的 `clone=True`，并从 `reactor.phase`
中读取随时间演化的属性。原始的 `Solution` 对象保留的是初始状态；
不要将其当作反应器的最终状态来读取。`ReactorNet.advance(t)`
请求的是一个绝对时间，并且没有配置推进限制，因此输出网格保持均匀。

它会运行四个相互独立的全新反应器：

| 运行 | 相对于配置条件的变化 |
| --- | --- |
| baseline（基线） | 原始设置 |
| finer_output（更细输出） | 输出间隔减半，时间范围和求解器控制保持不变 |
| tighter_solver（更严求解器） | 两个求解器容差都除以十；最大内部时间步长减半 |
| longer_horizon（更长范围） | 时间范围加倍，输出间隔保持原始值 |

`numerically_resolved` 要求所有运行都得出延迟值，且相对延迟变化
在 `delay_relative_tolerance` 范围内，并且所有守恒检验均通过。
在离散网格上的一致性并不等同于统计误差范围：还需报告输出间隔。
基线样本数必须在 11 到 50000 之间，以留出精细化的空间。运行时长
会随机理规模、刚性程度以及所选时间范围增长；积分失败时会保留
Cantera 的错误文本。

## 输出与检查

- `report.json`：所有输入设置、软件包版本、配置与机理哈希值、
  归一化后的初始组成、四个延迟估计值、数值变化、守恒情况，
  以及机理热力学温度范围。
- `baseline.csv`、`finer_output.csv`、`tighter_solver.csv`、
  `longer_horizon.csv`：时间、温度、压力、体积、质量、总内能、
  总焓，以及所请求物种的摩尔分数。
- `mechanism.yaml`：由 Cantera 写出的已加载相态、物种及反应的快照。
  该辅助脚本请求 `write_yaml(precision=17)`，并保存其计算哈希值所用
  的精确 UTF-8 字节，不进行平台换行符转换。该报告还会对定位到的
  原始机理文件计算哈希值。导入的源依赖项不会被单独计算哈希；
  该快照捕获的是已加载的模型。其生成的文件头包含日期，因此该快照
  哈希值标识的是所保存的产物本身，在其他方面相同的重复运行之间
  不必保持一致。

封闭反应器会保持质量和元素质量分数的守恒。定容情形检验总内能；
定压情形检验总焓。能量误差会除以
`max(abs(initial_energy_J), 1 J)`。诊断容差为：质量相对漂移
<1e-8，元素绝对漂移 <1e-8，能量缩放漂移 <1e-6，物种质量分数
总和误差 <1e-8，以及物种质量分数 >-1e-10。这些检查用于发现
数值问题，并不衡量动力学模型的不确定性。

请单独检查 `within_thermo_temperature_range`：它检查的是已保存的
输出状态，而不是每一个内部积分状态。数值上已被分辨并不意味着
物种热力学拟合始终保持在其温度范围之内。该辅助脚本无法根据这些
范围来评估压力依赖的动力学有效性。

## 适用范围与上游参考资料

该测试套件涵盖两种反应器约束、守恒检验、与独立 Cantera 平衡计算的
最终状态一致性、不点火条件、未分辨的边界最大值、精细化、快照重现，
以及无效的组成/条件。它不验证激波管热损失、真实气体效应、表面反应、
流动装置、火焰，或多阶段实验点火定义。构建那些模型时，只应配备
必要的物理模型及其自身的检验；不要将该辅助脚本的结果误标为其中
任何一种。

- [反应器模型方程](https://cantera.org/stable/reference/reactors/index.html)
- [Python 反应器 API](https://cantera.org/stable/python/zerodim.html)
- [热力学属性与平衡](https://cantera.org/stable/python/thermo.html)
- [相态序列化 API](https://cantera.org/stable/python/importing.html#cantera.Solution.write_yaml)
- [自定义扩展注册](https://cantera.org/stable/python/utilities.html#cantera.extension)
- [Cantera 3.2 发行说明](https://cantera.org/stable/reference/releasenotes/v3.2.html)
- [上游点火示例](https://cantera.org/stable/examples/python/reactors/non_ideal_shock_tube.html)
  使用的是物种质量分数峰值；其延迟定义与本辅助脚本的 dT/dt 峰值不同。
