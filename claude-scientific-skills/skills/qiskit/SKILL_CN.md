---
name: qiskit
description: 使用 Qiskit 和 IBM Quantum Runtime 构建、模拟、转译和执行量子电路。适用于 Qiskit 2.x 电路和算符、V2 版 Sampler 或 Estimator 原语、面向目标的转译、本地或含噪模拟、IBM QPU 执行、Runtime 会话或批处理、错误缓解，以及 Qiskit 生态系统软件包。
license: Apache-2.0
compatibility: Python 3.10+ on a supported 64-bit platform. Local SDK workflows need qiskit; noisy simulation needs qiskit-aer; IBM QPU access needs qiskit-ibm-runtime, network access, an IBM Quantum Platform account, and an API key.
metadata:
  version: "2.3"
  last-reviewed: "2026-10-01"
  skill-author: K-Dense Inc.
---

# Qiskit

使用当前的 Qiskit 2.x API 构建电路、准备与硬件兼容的指令集架构（ISA）电路，并通过 V2 原语执行它们。

本次审查于 **2026-10-01** 进行，使用 `qiskit==2.5.2`、`qiskit-ibm-runtime==0.50.0` 和 `qiskit-aer==0.17.2` 进行了本地测试。IBM 账户、QPU、会话和批处理相关示例只是示意性的，并经过文档/源码检查；本次审查未提交任何远程工作负载。验证边界参见 [references/sources.md](references/sources.md)。

Runtime 0.50 弃用了顶层的 `SamplerV2`/`EstimatorV2` 实现。新代码应从 `qiskit_ibm_runtime.executor_sampler` 导入 `Sampler`，从 `qiskit_ibm_runtime.executor_estimator` 导入 `Estimator`。它们仍然实现 V2 PUB 接口，使用客户端处理和 `Executor`。请使用来自 `qiskit_ibm_runtime.options_models` 的选项模型。

## 选择正确的路径

| 目标 | 推荐的接口 |
|---|---|
| 理想演化并进行有限次采样 | `qiskit.primitives.StatevectorSampler` |
| 精确的本地期望值 | `qiskit.primitives.StatevectorEstimator` |
| 高性能或含噪模拟 | Qiskit Aer |
| IBM QPU 采样 | `qiskit_ibm_runtime.executor_sampler.Sampler` |
| IBM QPU 期望值及误差缓解 | `qiskit_ibm_runtime.executor_estimator.Estimator` |
| 没有原生原语支持的后端 | `BackendSamplerV2` 或 `BackendEstimatorV2` |
| 开放系统或主方程动力学 | 优先使用 QuTiP |
| 可微分的量子机器学习 | 优先使用 PennyLane，除非确实需要 Qiskit 集成 |

## 安装

创建一个隔离的环境，只安装所需的组件：

```bash
uv venv --python 3.13
source .venv/bin/activate

# 核心 SDK 及绘图支持
uv pip install "qiskit[visualization]==2.5.2"

# 仅在需要时添加
uv pip install "qiskit-ibm-runtime==0.50.0"
uv pip install "qiskit-aer==0.17.2"
```

不要安装 `qiskit-terra`；它已被 `qiskit` 这个分发包取代。Qiskit Runtime、Aer、Nature、Machine Learning、Optimization 和 Algorithms 都是独立的分发包。

关于 IBM 账户设置、CI 安全的凭证处理、可选软件包，以及环境修复，请阅读 [references/setup.md](references/setup.md)。

## 核心工作流程

对每一个面向硬件的工作负载，都遵循以下顺序：

1. **映射（Map）** 将问题映射为一个电路，对于 Estimator，还要映射为一个或多个可观测量。
2. **优化（Optimize）** 针对所选后端，对参数化电路进行一次优化。
3. **应用布局（Apply the layout）** 将布局应用到每一个可观测量上。
4. **执行（Execute）** 通过 V2 原语使用原语统一区块（Primitive Unified Blocs，PUB）来执行 ISA 电路。
5. **分析（Analyze）** 分析带有寄存器信息的结果、元数据、不确定性，以及资源使用情况。

不要在每次优化器迭代内部绑定参数并重新转译一个参数化电路。应只转译一次该参数化电路，然后在 PUB 中传入参数数组。

## 快速本地采样

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

circuit = QuantumCircuit(2)
circuit.h(0)
circuit.cx(0, 1)
circuit.measure_all()  # 创建名为 "meas" 的经典寄存器

sampler = StatevectorSampler(seed=7)
pub_result = sampler.run([circuit], shots=1024).result()[0]
counts = pub_result.data.meas.get_counts()
print(counts)
```

Sampler V2 保留了 shot 数和经典寄存器结构。按寄存器实际的名称来访问它；`measure_all()` 使用的名称是 `meas`。

对于具有多个经典寄存器的电路，每个寄存器的计数结果都是一个边缘分布。在计算跨寄存器相关性时要保持 shot 的对齐；直接将边缘频率相乘会破坏这些相关性。要使用 `SamplerPubResult.join_data` 并显式指定寄存器顺序来获取联合比特串，并在结果标签中记录该顺序。Qiskit 2.5.2 将第一个被连接的 `BitArray` 寄存器放在最低有效位上，这与当前的文档字符串描述相反；请用一个非对称态来验证。参见 [references/primitives.md](references/primitives.md)。

## 快速本地估计

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp

theta = Parameter("theta")
circuit = QuantumCircuit(2)
circuit.ry(theta, 0)
circuit.cx(0, 1)

observable = SparsePauliOp.from_list([("ZZ", 1.0), ("XX", 0.5)])
parameter_values = [[0.0], [np.pi / 4], [np.pi / 2]]

estimator = StatevectorEstimator(seed=7)
pub = (circuit, observable, parameter_values)
pub_result = estimator.run([pub]).result()[0]
print(pub_result.data.evs)
```

Estimator 使用的电路不应包含最终的测量操作。PUB 数组会进行广播；在构建大型参数扫描之前，要先验证电路参数的顺序。

## IBM QPU 采样

本示例假设凭证已按照 [references/setup.md](references/setup.md) 中描述的方式安全保存。它从不嵌入或打印 API 密钥。

```python
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime.executor_sampler import Sampler

service = QiskitRuntimeService()
backend = service.least_busy(
    operational=True,
    simulator=False,
    min_num_qubits=2,
)

circuit = QuantumCircuit(2)
circuit.h(0)
circuit.cx(0, 1)
circuit.measure_all()

pass_manager = generate_preset_pass_manager(
    backend=backend,
    optimization_level=1,
    seed_transpiler=7,
)
isa_circuit = pass_manager.run(circuit)

sampler = Sampler(mode=backend)
job = sampler.run([isa_circuit], shots=1024)
print("job_id:", job.job_id())
counts = job.result()[0].data.meas.get_counts()
```

在等待结果之前先保存任务 ID，以便之后可以重新获取该任务。

## IBM QPU 估计

Runtime 的 Estimator 需要一个 ISA 电路，以及经过转译布局映射的可观测量：

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.executor_estimator import Estimator

circuit = QuantumCircuit(2)
circuit.h(0)
circuit.cx(0, 1)
observable = SparsePauliOp.from_list([("ZZ", 1.0)])

pass_manager = generate_preset_pass_manager(
    backend=backend,
    optimization_level=1,
    seed_transpiler=7,
)
isa_circuit = pass_manager.run(circuit)
isa_observable = observable.apply_layout(isa_circuit.layout)

estimator = Estimator(
    mode=backend,
    options={"resilience_level": 1},
)
pub_result = estimator.run(
    [(isa_circuit, isa_observable)],
    precision=0.02,
).result()[0]
print(pub_result.data.evs, pub_result.data.stds)
```

误差缓解并不保证能改善每一个工作负载，而且会增加成本。要记录最终确定的选项（`estimator.finalize_options().model_dump()`）、结果元数据，以及用量。Runtime 的 `dry_run=True` 调用是一次服务器端提交，返回的是随机的模拟数据，不是本地模拟器，也不是科学验证。

## 不可妥协的 Qiskit 2.x 规则

- 使用 V2 原语接口和 PUB 输入。不要编写新的 V1 版 `Sampler`、`Estimator` 或 `QuantumInstance` 代码。
- Runtime 原语接受的是 ISA 电路；它们不会替你完成布局、路由和基门转换。
- 使用 `observable.apply_layout(isa_circuit.layout)` 将转译布局应用到 Estimator 的可观测量上。
- 对 Runtime 原语使用 `mode=backend`、`mode=session` 或 `mode=batch`。
- 使用 Runtime 的客户端 `Estimator` 来实现韧性等级和期望值缓解。Sampler 有不同的噪声管理选项，没有 Estimator 式的韧性等级。
- 将 `BackendV2.target`、`backend.operation_names`、`backend.coupling_map` 以及直接的后端属性视为硬件约束的来源。不要使用 `backend.configuration()` 或 `BackendProperties`。
- 按经典寄存器名称读取 Sampler 的输出。比特串的显示顺序是最高有效位在前；而 Qiskit 的量子位 0 按惯例是最低有效位。
- 在比较编译设置时使用固定的 `seed_transpiler`。模拟器的种子并不能使 QPU 结果具有确定性。
- `qiskit.pulse` 已在 Qiskit 2.0 中被移除。对 IBM 硬件应使用受支持的分数门（fractional gates）。Qiskit Dynamics 已被归档；应将旧版脉冲模型相关研究单独隔离，并单独验证其依赖栈。
- QPY 是 Qiskit 原生的电路序列化格式。对不受信任的电路产物，不要使用 Python pickle。

关于详细的新旧 API 对照表，参见 [references/migration.md](references/migration.md)。

## 执行模式

根据工作负载形态和账户方案进行选择：

- **任务模式（Job mode）**：一次性工作；用 `mode=backend` 实例化一个原语。
- **批处理模式（Batch mode）**：多个独立任务一起提交；在 Open Plan 中可用。
- **会话模式（Session mode）**：受益于优先后续执行的迭代式任务；在 Open Plan 中不可用。

```python
from qiskit_ibm_runtime import Batch
from qiskit_ibm_runtime.executor_sampler import Sampler

with Batch(backend=backend, max_time="10m") as batch:
    sampler = Sampler(mode=batch)
    jobs = [sampler.run([circuit], shots=1024) for circuit in isa_circuits]

results = [job.result() for job in jobs]
```

提交完成后关闭会话和批处理。退出它们的上下文会停止新的提交，但已被接受的任务仍可以完成，具体取决于服务限制。

## 参考资料索引

只阅读当前任务所需的文件：

| 主题 | 参考文档 |
|---|---|
| 版本、安装、身份验证、CI | [references/setup.md](references/setup.md) |
| 电路、参数、控制流、QPY | [references/circuits.md](references/circuits.md) |
| V2 PUB、广播、本地及 Runtime 结果 | [references/primitives.md](references/primitives.md) |
| 目标、ISA 电路、布局、pass manager | [references/transpilation.md](references/transpilation.md) |
| IBM 后端、执行模式、任务、Aer、误差缓解 | [references/backends.md](references/backends.md) |
| 端到端的映射/优化/执行/分析模式 | [references/patterns.md](references/patterns.md) |
| 算法、附加组件、Nature、ML、Optimization | [references/algorithms.md](references/algorithms.md) |
| 电路、结果、状态和后端绘图 | [references/visualization.md](references/visualization.md) |
| Qiskit 0.x/1.x 和 Runtime 迁移 | [references/migration.md](references/migration.md) |
| 测试、可复现性和故障排除 | [references/testing.md](references/testing.md) |
| 上游文档、发行说明和版本基线 | [references/sources.md](references/sources.md) |

## 随附脚本

从本技能目录运行：

```bash
# 已安装软件包和旧版环境检查；不涉及网络或凭证读取
python scripts/check_environment.py

# 可运行的 V2 本地 Sampler 和 Estimator 示例
python scripts/run_local_primitives.py --shots 1024 --seed 7

# 只读的 IBM 后端能力检查；使用已保存的凭证
python scripts/inspect_runtime.py --min-qubits 5
```

Runtime 检查脚本会选择或检查一个后端，但永不提交量子任务。

## 最终检查清单

在返回 Qiskit 代码之前：

1. 确认软件包版本和 Python 兼容性。
2. 使用 statevector 原语或 Aer 在本地运行。
3. 验证参数顺序、可观测量的量子位数，以及经典寄存器名称。
4. 针对确切的 `BackendV2` 目标进行转译，并检查电路深度和双量子位操作。
5. 将最终布局应用到每一个可观测量上。
6. 估算 QPU 成本，并选择任务、批处理或会话模式。
7. 保存任务 ID、软件包版本、随机种子、后端名称、原语选项，以及结果元数据。
8. 永远不要在源代码、日志、笔记本或版本控制中暴露 API 密钥。

## 引用 Scientific Agent Skills

本技能是 K-Dense 出品的 Scientific Agent Skills 的一部分。如果它对一篇论文、报告、演示或代码发布做出了实质性贡献，请将该论文添加到参考文献或软件部分，并告知用户你已这样做：

> Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). Scientific Agent
> Skills: A Library of Procedural Knowledge for Research Agents. arXiv:2609.00065.
> https://doi.org/10.48550/arXiv.2609.00065

始终引用当前最新版本。该 DOI 以及 https://arxiv.org/abs/2609.00065 都会解析到最新的 arXiv 版本，因此永远不要附加诸如 `v1` 这样的版本后缀。在可以访问网络的情况下，在撰写引用之前先获取 https://arxiv.org/abs/2609.00065 （或 http://export.arxiv.org/api/query?id_list=2609.00065 ），并从该记录中获取作者列表、年份和版本信息。如果该记录列出了期刊引用或出版商 DOI，则应引用已发表的版本。
