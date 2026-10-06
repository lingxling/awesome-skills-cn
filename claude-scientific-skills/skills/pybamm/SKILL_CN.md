---
name: pybamm
description: 使用 PyBaMM 模拟锂离子电池的充电、放电和静置实验，记录参数集的来源，检查网格和求解器的敏感性，并将预测的电压曲线与实测循环数据进行对比。适用于 SPM 或 DFN 电化学电池建模、C 倍率协议、电压截止、参数研究以及电池仿真的数值验证。
license: MIT
compatibility: Requires Python 3.12 with PyBaMM 26.9.0.0 and pybammsolvers 0.10.0 (IDAKLU). NumPy and CasADi are supplied by PyBaMM. Network is needed for installation and optional upstream dataset retrieval; bundled simulations and CSV comparisons run locally without credentials.
metadata:
  version: "1.1"
  skill-author: K-Dense Inc.
  upstream-version: "26.9.0.0"
  last-reviewed: "2026-10-01"
---

# PyBaMM 电池实验

## 何时使用

使用此技能对单电芯恒流充放电和静置进行建模，检查电压和电荷轨迹，
或将 SPM/DFN 的预测结果与循环测量数据进行对比。该辅助脚本运行的是
真实的 PyBaMM 实验，并进行三种数值分辨率的计算；它不控制电池循环仪，
也不为硬件建立运行边界。

## 运行环境与测试案例

```bash
uv venv --python 3.12 battery-env
uv pip install --python battery-env/bin/python pybamm==26.9.0.0 pybammsolvers==0.10.0
```

此发行版要求 `pybammsolvers>=0.10.0`、NumPy 2 或更新版本，以及
CasADi 3.8.1。测试环境使用的是 Python 3.12.10、NumPy 2.5.3 和
SciPy 1.18.1。IDAKLU 是推荐的求解器；`CasadiSolver` 和 `ScipySolver`
在此发行版中已被弃用。请参阅下方的 **26.9.0.0** 版手册，因为
`latest` 可能描述的是尚未发布的 API。

所附带的 [assets/chen2020-protocol.json](assets/chen2020-protocol.json)
是一个合成的等温 298.15 K SPM 案例：初始 SOC 为 80%，以 0.5C 放电
600 秒，静置 120 秒，再以 0.5C 充电 600 秒。Chen2020 提供了一个
标称容量为 5 Ah 的 LG M50 参数化方案；此处 0.5C 意味着 2.5 A。
这是一个可执行的参考示例，并不代表任意用户的电芯都具有这些参数。
除非调用方已经显式配置过该变量，否则该辅助脚本会禁用 PyBaMM
的使用遥测功能。

## 工作流程

1. 确定电芯化学体系、几何结构、标称容量、初始状态、温度以及
   电流符号约定。使用合适的参数集并说明其来源。要区分某篇论文
   的拟合参数与这一特定电芯的实测数据。切勿在未检查其含义和
   适用条件的情况下直接移植老化参数。
2. 将所请求的协议转换为
   [references/protocol-and-comparison.md](references/protocol-and-comparison.md)
   中所述的 JSON 契约。模拟中正电流表示放电；负电流表示充电。
   每一步都有一个有限的持续时间。指定的电压截止值可以提前结束
   该步骤；报告中会记录实际的终止时间。C 倍率使用所选参数集的
   标称容量。该容量发生变化会改变电流。
3. 当其简化的传输假设足够适用时选择 SPM；当需要解析电解液/电极
   传输过程时则使用 DFN。该辅助脚本经过测试的模型都是等温的，
   不包括老化、力学、析锂以及电池组控制。即便数值收敛情况良好，
   提高倍率仍可能使 SPM 的预测失效。
4. 运行该辅助脚本。它会验证协议字段，拒绝未知或被协议覆盖的
   参数输入，使用 IDAKLU，并**在 SOC 初始化之后**对基础参数进行
   快照。要将该协议与该快照一起保留：实验步骤会提供各自的电流。
   不可行或被跳过的步骤会被视为错误，而不会被当作完整协议悄悄呈现。
5. 分别解读两种数值对比：基线与更严格容差的对比用于分离求解器
   误差；原始网格与加倍网格（均使用严格容差）的对比用于分离离散化
   误差。将电压差异和事件时间差异与问题所需的精度进行比较。
   当这些差异过大时需要再次精细化；一次网格加倍并不能证明收敛性。
6. 如果有实测数据，在解读残差之前请先检查电流、时间原点、温度、
   SOC 和容量。提供匹配的秒、伏特和安培单位数据。该辅助脚本会报告
   电压 RMSE/MAE/偏差以及电流 RMSE，并保留残差。在输入电流不匹配的
   情况下出现较小的电压误差，并不能验证该模型。本工作流比较的是
   曲线；它并不宣称能仅凭电压就识别出唯一的动力学参数。

## 运行与检查

在该技能目录下，将 `battery-env/bin/python` 指向上面创建的环境：

```bash
battery-env/bin/python scripts/simulate_battery.py assets/chen2020-protocol.json \
  --output battery-reference

# measured.csv is user data with time_s,voltage_V,current_A columns.
battery-env/bin/python scripts/simulate_battery.py protocol.json \
  --measured measured.csv --mesh-points 30 --output battery-comparison
```

第一条命令已按原样配合外部输出位置执行过。第二条命令使用的是示例性
的用户文件名；该测量路径在测试中是针对一条固定的合成参考曲线进行
验证的。输出目录必须是全新的。

| 产物 | 解读 |
| --- | --- |
| `curve.csv` | 基线的时间、步骤、电压、电流以及**净**放电容量 |
| `tight-tolerance.csv` | 相同网格，更严格的求解器容差 |
| `refined-mesh.csv` | 加倍网格，配合更严格的求解器容差 |
| `parameters.json` | SOC 初始化之后的基础参数；各步骤电流仍保留在协议中 |
| `report.json` | 协议/校验和、软件包版本、参数来源、数值对比及终止情况 |
| `measurement-residuals.csv` | 当提供了实测数据时，预测值减去实测值以及电流不匹配情况 |

该参考案例保持了积分电荷的守恒：在 2.5 A 下运行 600 秒产生了
0.4166667 Ah，随后等量的充电使净放电容量恢复为零。在此案例中，
电压始终保持在 Chen2020 的限制范围内。收紧容差使电压改变了约
1 微伏；将网格从 20 点加倍到 40 点使其改变了约 **2.17 mV**，
因此宣称达到亚毫伏级的网格精度是没有根据的。另一个独立的真实 DFN
测试在所请求的 3.9 V 事件处停止，并验证了其电荷积分。原生测试
还涵盖了充电截止、不可行放电、容量到电流的转换，以及在不重新
初始化 SOC 的情况下对已导出的 SOC 调整参数进行重放。该固定参考
结果是数值回归方面的证据，而不是针对实测电芯的验证。

## 主要参考资料

- [PyBaMM 实验 API 示例](https://docs.pybamm.org/en/pybamm-v26.9.0.0/source/examples/notebooks/getting_started/tutorial-5-run-experiments.html)
- [网格精细化工作流](https://docs.pybamm.org/en/pybamm-v26.9.0.0/source/examples/notebooks/getting_started/tutorial-9-changing-the-mesh.html)
- [IDAKLU 求解器选项](https://docs.pybamm.org/en/pybamm-v26.9.0.0/source/api/solvers/idaklu_solver.html)
- [发行版源码与变更记录](https://github.com/pybamm-team/PyBaMM/blob/pybamm-v26.9.0.0/CHANGELOG.md)

参考资料中所链接的发行版手册、捆绑的辅助脚本、参数序列化以及
可选的 DataLoader 方案均已针对 PyBaMM 26.9.0.0 进行过验证。
