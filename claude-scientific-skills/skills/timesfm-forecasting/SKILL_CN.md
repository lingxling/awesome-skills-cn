---
name: timesfm-forecasting
description: 使用谷歌的 TimesFM 执行零样本时间序列预测，包括规则网格 CSV 准备、分位数预测、XReg 协变量以及留出集评估。默认使用 Apache 许可的 TimesFM 2.5 检查点，并记录了不同的 TimesFM 3.0 多变量 API 及其权重许可要求。
allowed-tools: Read Write Edit Bash
license: Apache-2.0 license
compatibility: Requires Python 3.10+ and timesfm 3.0.2 with PyTorch; CSV tooling also needs NumPy and pandas. Network access and cache space are needed for initial Hugging Face checkpoint download. Optional XReg needs JAX and scikit-learn; current JAX requires Python 3.12+.
metadata:
  version: "3.0"
  skill-author: Clayton Young / Superior Byte Works, LLC (@borealBytes)
  last-reviewed: "2026-10-01"
  tested-package: "timesfm 3.0.2"
---

# TimesFM 预测

## 先选择模型/API

**Python 软件包版本为 3.0.2**；检查点版本是独立编号的。

| 检查点 | 接口 | 分位数输出 | 使用条款 |
| --- | --- | --- | --- |
| 2.5, 2 亿参数 | `timesfm.TimesFM_2p5_200M_torch`, `compile`, `forecast` | 均值 + 9 个十分位数，中位数索引为 5 | Apache-2.0 权重；捆绑 CLI 的默认选项 |
| 3.0, 约 3.3 亿参数 | `timesfm3.TimesFM3Forecaster`, `predict` / `predict_batch` | 9 个十分位数，中位数索引为 4 | 下载的权重仅限非商业、非生产用途 |

上游将 3.0 标识为最新模型。本技能仍将 2.5 作为默认的本地工作流，
因为其 Apache 许可的权重具有不同的使用条款。
若需使用 3.0 的多变量目标、仅过去协变量或 Apple MLX，
请在改写代码前阅读 [references/timesfm3.md](references/timesfm3.md)。
经授权的 Google Cloud 服务拥有独立条款；拥有 Cloud 权限
并不会改变下载权重的许可证。参见[上游许可声明](https://github.com/google-research/timesfm#license-notice-for-pretrained-weights)。

将 TimesFM 用于对有序时间目标进行预测，而无需针对任务进行模型训练。
它不是因果效应估计器、临床检测器，也不是基于物理的气候模型。
"零样本"描述的是拟合方式；它并不说明预训练中不存在基准重叠，
也不说明在新领域中具有良好的准确性。

## 工作流程

1. 确定节奏（cadence）、单位、预测起点、预测时长（horizon）、起点已知的协变量、
   评估截止点，以及朴素/季节性朴素基线。
2. 验证一个已排序、唯一且规则的时间网格。不要对内部缺口执行 `dropna()`：
   那会改变时间间距。拒绝非有限的输入，或在每段训练历史内部明确进行插补。
   永远不要使用留出的未来目标值进行填充。
3. 在下载/加载权重之前运行 `python scripts/check_system.py`。
   它关于可用内存和缓存空间的阈值只是经验法则，并不能保证不发生 OOM。
   先从批大小 1 开始；实测真实的峰值使用量。
4. 使用记录下来的不可变版本（revision）加载所选检查点。对于 2.5，
   要编译明确的正数上下文/预测时长设置；0 并**不**意味着"使用最大值"。
   当使用连续分位数头时，保持经过补丁对齐（patch-rounded）的
   上下文 + 预测时长 <=16,384，且预测时长 <=1,024。
5. 执行预测，验证形状/有限值/分位数顺序，并导出预测起点、
   频率、配置和检查点版本。
6. 跨多个滚动起点进行评估，每个起点独立拟合预处理。
   按预测时长报告准确度、区间覆盖率和区间宽度；
   在根据相关数据校准之前，将分位数区间标注为**名义上的（nominal）**。

## 安装

在独立的环境中运行。以下命令针对的是已评审过的版本。
Shell 的 extras 和版本约束必须加引号，尤其是在 zsh 中。

```bash
uv venv .venv-timesfm
uv pip install --python .venv-timesfm/bin/python "timesfm[torch]==3.0.2" numpy pandas
.venv-timesfm/bin/python scripts/check_system.py
```

请使用当前的 [PyTorch 安装选择器](https://pytorch.org/get-started/locally/)
以获得与主机匹配的 CUDA wheel。本版本中的 2.5 加载器会在存在 CUDA 时
选择 `cuda:0`，否则选择 CPU；检测到 MPS **并不**会启用 MPS 推理。
不要在该封装器上使用 `model.to(...)`，就好像它是一个 `nn.Module` 一样。
若需仅在 CPU 上使用 XReg，请在 PyTorch 环境中额外安装 `jax` 和
`scikit-learn`；上游的 `[xreg]` extra 会请求 `jax[cuda]`，
这在 macOS 上并不合适。Flax 是一个独立的可选后端；捆绑脚本并不需要它。

```python
from importlib.metadata import version
import timesfm
print(version("timesfm"))  # package has no guaranteed timesfm.__version__
assert hasattr(timesfm, "TimesFM_2p5_200M_torch")
```

## TimesFM 2.5 快速入门

检查点加载示例仅为说明性质：本次更新的验证使用的是
原生软件包代码，搭配微小的随机模型和受控的解码测试数据，
并未下载预训练权重。这验证的是机制，而非准确性。

```python
import numpy as np
import timesfm

model = timesfm.TimesFM_2p5_200M_torch.from_pretrained(
    "google/timesfm-2.5-200m-pytorch",
    revision="1d952420fba87f3c6dee4f240de0f1a0fbc790e3",
    torch_compile=False,  # avoid compilation startup during an initial smoke run
)
model.compile(timesfm.ForecastConfig(
    max_context=512, max_horizon=128, per_core_batch_size=1,
    normalize_inputs=True, use_continuous_quantile_head=True,
    force_flip_invariance=True, infer_is_positive=False,
    fix_quantile_crossing=True,
))
histories = [np.sin(np.linspace(0, 20, 200)).astype(np.float32)]
# 2.5 may append dummy series to its input list during batching; pass a fresh list.
point, q = model.forecast(horizon=24, inputs=list(histories))
assert point.shape == (1, 24) and q.shape == (1, 24, 10)
assert np.isfinite(q).all() and np.all(np.diff(q[..., 1:], axis=-1) >= 0)
assert np.allclose(point, q[..., 5])
lower_80, upper_80 = q[..., 1], q[..., 9]  # q10-q90: nominal 80% PI
lower_60, upper_60 = q[..., 2], q[..., 8]  # q20-q80: nominal 60% PI
```

只有在目标领域确实非负时，才将 `infer_is_positive=True`。
观测窗口为正值并不能证明温度异常、收益率或残差不可能变为负值。
分位数的单调性和连续分位数头都不能证明区间已经过校准。

## CSV 辅助工具

```bash
python scripts/forecast_csv.py monthly_sales.csv \
  --date-col date --freq MS --value-cols sales,revenue \
  --horizon 12 --batch-size 1 --nonnegative --output forecasts.csv
```

`forecast_csv.py` 在加载之前进行验证，对日期排序，拒绝重复的
表头/日期，检查完整的规则网格并保留缺失位置。
默认情况下缺失值会导致失败；`--missing interpolate` 只填充内部缺口，
绝不填充起始/末尾的缺失值。若未指定 `--date-col`，则假定行顺序即为
规则网格，输出将使用步数（steps）。必须使用 `--value-cols` 排除数值型 ID 列。
`--max-context` 控制历史截断长度；在该分位数头工作流中，
`--horizon` 的取值范围限制为 1 到 1,024。

输出保留 `forecast`、`median`、`lower_80`、`upper_80`、`lower_60`、`upper_60`
这些字段。一个 `.metadata.json` 附属文件会记录起点、节奏、模型版本和配置。
旧版技能发布曾将 q10-q90/q20-q80 错误地标注为 90%/80%；请同时将
旧的外层 `*_90` 迁移为 `*_80`，旧的内层 `*_80` 迁移为 `*_60`。
之前生成的示例预测已被移除，因为其映射关系/来源无效。

## 协变量与异常筛查

对于 2.5 的 XReg，编译时要设置 `return_backcast=True`，
将目标和协变量保持在相同的网格上，并在上下文**和**预测时长内都提供
动态协变量。`"xreg + timesfm"` 先对目标进行回归拟合，然后对回归残差进行预测。
`"timesfm + xreg"` 先进行预测，然后对回测（backcast）残差进行回归拟合。
后者需要超过一个输入补丁（32 个观测值）。在 3.0.2 软件包中，
该实现返回的是**组合点预测和分位数预测的列表**；
继承下来的文档字符串错误地将第二个返回值描述为仅限 XReg。
完整调用方式请参见 [references/api_reference.md](references/api_reference.md)。

分位数超限可用于筛查异常观测值，但即便是经过校准的 80% 区间，
也会在边际上排除大约 20% 的普通观测值。它们并不提供异常概率、
族系误差控制（familywise control）或经过验证的告警严重程度。
回溯性的去趋势 Z 分数也与前瞻性异常检测不同。

## 参考资料与示例

- [API 参考](references/api_reference.md)：2.5 的加载器、compile、forecast 以及 XReg 调用约定。
- [输出/配置](references/output_and_config.md)：所有真实的 ForecastConfig 字段及区间索引方式。
- [数据准备](references/data_preparation.md)：网格、缺失值、协变量时序及格式方案。
- [工作流](references/workflows.md)：留出集和滚动起点验证、基线对比。
- [系统要求](references/system_requirements.md)：资源检查与后端要求。
- [性能调优](references/performance_tuning.md)：经过实测的批大小/上下文调优。
- [示例与验证](references/examples_and_validation.md)：示例命令和测试范围。
- [TimesFM 3.0](references/timesfm3.md)：多变量 API、9 分位数布局以及使用边界。

主要评审来源：[官方源代码](https://github.com/google-research/timesfm)，
[3.0.2 发行版](https://pypi.org/project/timesfm/3.0.2/)，
[2.5 模型卡](https://huggingface.co/google/timesfm-2.5-200m-pytorch)，
[3.0 模型卡](https://huggingface.co/google/timesfm-3.0-pytorch)。
