---
name: flowkit
description: 使用 FlowKit 分析流式细胞术数据，包括溢出补偿、logicle 和 biexponential 变换、层级门控、GatingML 策略以及受支持的 FlowJo 10 工作区。适用于可复现的门控计数、群体百分比、门控荧光汇总，或在 Python 中复现 FlowJo 分析。若仅需检查 FCS 元数据或修复文件格式，请使用 FlowIO。
license: MIT
compatibility: Requires Python 3.13 with flowkit==1.3.2 for the tested environment. Dependencies include FlowIO, FlowUtils, NumPy, pandas, SciPy, lxml, and Bokeh. Installation needs network access; analysis uses local FCS/XML/WSP files without credentials. FlowUtils needs a C compiler if a compatible wheel is unavailable.
metadata:
  version: "1.1"
  skill-author: K-Dense Inc.
  last-reviewed: "2026-09-30"
---

# FlowKit

## 何时使用

使用 FlowKit 来应用或构建细胞术门控策略、分析批量的 FCS 样本，或复现受支持的 FlowJo 工作区分析。它支持 GatingML 2.0 以及 **FlowJo 10 功能的一个子集**。仅仅导入成功并不能确立与 FlowJo 的一致性。

示例和随附的辅助工具面向 **Python 3.13 上的 FlowKit 1.3.2**。上游支持更多的 Python 版本；这里并未对它们进行测试。辅助工具和示例已在合成的 FCS 数据上测试，包括一个公开的 FlowJo 10.7.1 合成工作区固定数据。它们不是生物学验证。

## 安装

请使用单独的环境；FlowKit 1.3.2 要求 NumPy >2 和 pandas <3：

```bash
uv venv --python 3.13 .venv-flowkit
uv pip install --python .venv-flowkit/bin/python "flowkit==1.3.2"
.venv-flowkit/bin/python -c "import flowkit; print(flowkit.__version__)"
```

该科学软件包采用 BSD-3-Clause 许可；本技能采用 MIT 许可。

## 工作流程

1. **确定分析定义。** 对于编程方式或 GatingML 策略，使用 `Session`；对于 FlowJo 中特定于样本的门、补偿和变换，使用 `Workspace`。当尚未提供生物学阈值时，请索取实际的策略或对照。
2. **检查样本和通道标识。** 将检测器/PnN 标签与补偿矩阵和门的维度相匹配；PnS 标记名称可能为空或重复。请核实样本 ID：默认值是 FCS 的 `$FIL`，它可能与当前文件名不同。在加载批量数据之前，拒绝 ID 冲突。
3. **确立坐标系。** 确定所提供的事件是否已经过补偿。在非线性变换之前应用补偿；使门的阈值与相同的变换后或未变换的坐标相匹配。参见[补偿与门控](references/compensation-and-gating.md)。
4. **检查层级结构。** 保留父门和完整的门路径，包括 `root`。对于一项研究，请根据其面板酌情审阅采集/时间稳定性、碎片排除、单细胞（singlets）、活力和表型门。使用单染对照进行补偿，并使用合适的阴性/FMO 对照来界定阳性；演示用的阈值并不是可移植的生物学结论。
5. **分析并检查。** 对所有事件运行，然后检查门的叠加图和样本层面的质控。图的子采样并不是群体的分母。请审阅警告，并将有代表性的导入结果与 FlowJo 进行比较。
6. **导出带有分母和来源信息的计数。** 保留门路径、样本 ID、总事件数、输入哈希、软件包版本以及分析定义。保持生物学重复可被识别；来自同一标本的事件不是独立的实验重复。

## 应用现有策略

将 `FLOWKIT_SKILL_DIR` 设置为本技能的安装目录。从仓库根目录来看，它是 `skills/flowkit`。以下路径代表用户的本地输入。

```bash
FLOWKIT_SKILL_DIR="skills/flowkit"
uv run --no-project --python 3.13 --with "flowkit==1.3.2" \
  python "$FLOWKIT_SKILL_DIR/scripts/analyze_gates.py" \
  --gatingml gates.xml --fcs sample.fcs --output-dir results-gatingml
```

对于 FlowJo 工作区，请提供所选分组中**的每一个 FCS 文件**：

```bash
uv run --no-project --python 3.13 --with "flowkit==1.3.2" \
  python "$FLOWKIT_SKILL_DIR/scripts/analyze_gates.py" \
  --workspace study.wsp --group "Study" \
  --fcs sample-a.fcs sample-b.fcs --output-dir results-workspace
```

该辅助工具会将 `gate_report.csv` 和 `provenance.json` 写入一个新目录。每一行都包含 `sample_event_count`、`parent_event_count` 和完整的 `population_path`；父群为空时的百分比留空，并以 `relative_percent_defined=False` 标记。它会拒绝重复的样本 ID、缺失/多余的工作区分组样本、零事件样本以及没有门的策略。它使用显式的输入文件，不会跟随工作区中嵌入的路径，并且在运行时不使用多进程或变换后事件缓存。它仍会将每个样本加载到内存中；对于大型研究，请通过 Python API 使用可控规模的批次。

`--filename-as-id` 会有意地从 `$FIL` 切换为文件基本名。仅当这些名称与分析定义相符时才使用它。有关部分分组分析、结果解读和荧光汇总，参见[工作区分析](references/workspaces-and-results.md)。

## 在 Python 中构建策略

这个可运行的示例使用带有 `FSC-A`、`FL1-A` 和 `FL2-A` 的 `sample.fcs`。矩阵、阈值和变换参数都是**合成的教学用数值**。请将其替换为研究中经过验证的设置。

```python
import flowkit as fk
import numpy as np

sample = fk.Sample("sample.fcs")
strategy = fk.GatingStrategy()
strategy.add_comp_matrix(
    "spill", fk.Matrix(
        np.array([[1.0, 0.1], [0.2, 1.0]]), ["FL1-A", "FL2-A"],
        fluorochromes=["FITC", "PE"],
    )
)
logicle = fk.transforms.LogicleTransform(
    param_t=262144, param_w=0.5, param_m=4.5, param_a=0
)
strategy.add_transform("logicle", logicle)
strategy.add_gate(
    fk.gates.RectangleGate("Cells", [
        fk.Dimension("FSC-A", range_min=50, range_max=300)
    ]),
    gate_path=("root",),
)
thresholds = logicle.apply(np.array([50.0, 600.0]))
strategy.add_gate(
    fk.gates.RectangleGate("Positive", [
        fk.Dimension(
            "FL1-A", compensation_ref="spill", transformation_ref="logicle",
            range_min=float(thresholds[0]), range_max=float(thresholds[1]),
        )
    ]),
    gate_path=("root", "Cells"),
)
session = fk.Session(gating_strategy=strategy, fcs_samples=[sample])
session.analyze_samples(use_mp=False)
report = session.get_analysis_report()
print(report[["sample_id", "gate_path", "gate_name", "count",
              "absolute_percent", "relative_percent"]])
with open("gates.xml", "xb") as handle:
    session.export_gml(handle)
```

GatingML 默认导出的是模板。当存在自定义的逐样本门时，请使用 `session.export_gml(handle, sample_id=sample.id)` 导出该样本的策略。单个模板导出并不会保留每一个特定于样本的覆盖设置。

## 解读检查

- `count` 是通过该门及其所有祖先门的事件数。
- `absolute_percent` 是占样本全部事件的百分比；`relative_percent` 是占其直接父群的百分比。这些是百分数，而不是分数。
- 门的名称可以在不同的父门下重复。在该辅助工具的输出中，请使用 `(sample_id, population_path)` 作为标识符。路径是 CSV 单元格内的 JSON 数组。FlowKit 原生报告将象限的所属者单独存储在 `quadrant_parent` 中；仅凭其 `gate_path` 会遗漏该所属者。
- 零事件的父群会使子群的百分比在生物学上无定义；FlowKit 1.3.2 对普通子群报告零，对象限报告 NaN。该辅助工具将两者都导出为空白并带有明确的 false 标志。这不同于其父群包含事件、而该门为空时所定义的 0%。
- 补偿后的负荧光值是合理的。不要仅仅为了使用对数变换而将其截断为零或丢弃这些事件。
- 请定义“MFI”指的是均值还是中位数，并说明事件来源。变换后的显示值并不是原始尺度上的强度。

## 参考资料

- [补偿与门控](references/compensation-and-gating.md)：事件来源、检测器顺序、变换语义、门路径和绘图。
- [工作区与结果](references/workspaces-and-results.md)：样本匹配、缺失的 FCS 文件、FlowJo 的限制以及门控荧光汇总。
- [FlowKit API](https://flowkit.readthedocs.io/en/latest/api.html)和[带版本的源码](https://github.com/whitews/FlowKit/tree/1.3.2)：在超出经测试的发行版时，请查阅其中的签名。
- [FlowKit 论文](https://doi.org/10.3389/fimmu.2021.768541)：在用于分析时，请在科学方法中引用该软件及其版本。
