---
name: qiskit
description: IBM量子计算框架。适用于目标为IBM Quantum硬件、使用Qiskit Runtime处理生产工作负载，或需要IBM优化工具的场景。最适合IBM硬件执行、量子误差缓解和企业量子计算。对于Google硬件使用cirq；对于基于梯度的量子机器学习使用pennylane；对于开放量子系统模拟使用qutip。
license: Apache-2.0 license
metadata:
    skill-author: K-Dense Inc.
---

# Qiskit

## 概述

Qiskit是世界上最流行的开源量子计算框架，下载量超过1300万次。用于构建量子电路、针对硬件进行优化、在模拟器或真实量子计算机上执行，以及分析结果。支持IBM Quantum（100+量子比特系统）、IonQ、Amazon Braket等提供商。

**主要特性：**
- 比竞争对手快83倍的转译速度
- 优化电路中两量子比特门数量减少29%
- 与后端无关的执行（本地模拟器或云硬件）
- 用于优化、化学和机器学习的综合算法库

## 快速开始

### 安装

```bash
uv pip install qiskit
uv pip install "qiskit[visualization]" matplotlib
```

### 第一个电路

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

# 创建Bell态（纠缠量子比特）
qc = QuantumCircuit(2)
qc.h(0)           # 对量子比特0应用Hadamard门
qc.cx(0, 1)       # 从量子比特0到1的CNOT门
qc.measure_all()  # 测量两个量子比特

# 本地运行
sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()
counts = result[0].data.meas.get_counts()
print(counts)  # {'00': ~512, '11': ~512}
```

### 可视化

```python
from qiskit.visualization import plot_histogram

qc.draw('mpl')           # 电路图
plot_histogram(counts)   # 结果直方图
```

## 核心功能

### 1. 设置和安装
关于详细的安装、认证和IBM Quantum账户设置：
- **参见 `references/setup.md`**

涵盖主题：
- 使用uv进行安装
- Python环境设置
- IBM Quantum账户和API令牌配置
- 本地与云端执行

### 2. 构建量子电路
关于使用门、测量和组合构建量子电路：
- **参见 `references/circuits.md`**

涵盖主题：
- 使用QuantumCircuit创建电路
- 单量子比特门（H、X、Y、Z、旋转、相位门）
- 多量子比特门（CNOT、SWAP、Toffoli）
- 测量和屏障
- 电路组合和属性
- 变分算法的参数化电路

### 3. 原语（Sampler和Estimator）
关于执行量子电路和计算结果：
- **参见 `references/primitives.md`**

涵盖主题：
- **Sampler**：获取比特串测量和概率分布
- **Estimator**：计算可观测量的期望值
- V2接口（StatevectorSampler、StatevectorEstimator）
- 用于硬件的IBM Quantum Runtime原语
- Session和Batch模式
- 参数绑定

### 4. 转译和优化
关于优化电路并为硬件执行做准备：
- **参见 `references/transpilation.md`**

涵盖主题：
- 为什么需要转译
- 优化级别（0-3）
- 六个转译阶段（初始化、布局、路由、转换、优化、调度）
- 高级特性（虚拟置换消除、门抵消）
- 常用参数（initial_layout、approximation_degree、seed）
- 高效电路的最佳实践

### 5. 可视化
关于显示电路、结果和量子态：
- **参见 `references/visualization.md`**

涵盖主题：
- 电路绘制（文本、matplotlib、LaTeX）
- 结果直方图
- 量子态可视化（布洛赫球、状态城市、QSphere）
- 后端拓扑和误差图
- 自定义和样式
- 保存 publication 质量的图形

### 6. 硬件后端
关于在模拟器和真实量子计算机上运行：
- **参见 `references/backends.md`**

涵盖主题：
- IBM Quantum后端和认证
- 后端属性和状态
- 使用Runtime原语在真实硬件上运行
- 作业管理和排队
- Session模式（迭代算法）
- Batch模式（并行作业）
- 本地模拟器（StatevectorSampler、Aer）
- 第三方提供商（IonQ、Amazon Braket）
- 误差缓解策略

### 7. Qiskit Patterns工作流
关于实现四步量子计算工作流：
- **参见 `references/patterns.md`**

涵盖主题：
- **映射**：将问题转换为量子电路
- **优化**：为硬件转译
- **执行**：使用原语运行
- **后处理**：提取和分析结果
- 完整的VQE示例
- Session与Batch执行
- 常见工作流模式

### 8. 量子算法和应用
关于实现特定的量子算法：
- **参见 `references/algorithms.md`**

涵盖主题：
- **优化**：VQE、QAOA、Grover算法
- **化学**：分子基态、激发态、哈密顿量
- **机器学习**：量子核、VQC、QNN
- **算法库**：Qiskit Nature、Qiskit ML、Qiskit Optimization
- 物理模拟和基准测试

## 工作流决策指南

**如果您需要：**

- 安装Qiskit或设置IBM Quantum账户 → `references/setup.md`
- 构建新的量子电路 → `references/circuits.md`
- 了解门和电路操作 → `references/circuits.md`
- 运行电路并获取测量结果 → `references/primitives.md`
- 计算期望值 → `references/primitives.md`
- 优化电路以适应硬件 → `references/transpilation.md`
- 可视化电路或结果 → `references/visualization.md`
- 在IBM Quantum硬件上执行 → `references/backends.md`
- 连接到第三方提供商 → `references/backends.md`
- 实现端到端量子工作流 → `references/patterns.md`
- 构建特定算法（VQE、QAOA等） → `references/algorithms.md`
- 解决化学或优化问题 → `references/algorithms.md`

## 最佳实践

### 开发工作流

1. **从模拟器开始**：在使用硬件前先在本地测试
   ```python
   from qiskit.primitives import StatevectorSampler
   sampler = StatevectorSampler()
   ```

2. **始终转译**：在执行前优化电路
   ```python
   from qiskit import transpile
   qc_optimized = transpile(qc, backend=backend, optimization_level=3)
   ```

3. **使用适当的原语**：
   - Sampler用于比特串（优化算法）
   - Estimator用于期望值（化学、物理）

4. **选择执行模式**：
   - Session：迭代算法（VQE、QAOA）
   - Batch：独立并行作业
   - 单个作业：一次性实验

### 性能优化

- 生产环境使用optimization_level=3
- 最小化两量子比特门（主要误差源）
- 在使用硬件前用噪声模拟器测试
- 保存并重用转译后的电路
- 监控变分算法的收敛

### 硬件执行

- 提交前检查后端状态
- 测试时使用least_busy()
- 保存作业ID以便以后检索
- 应用误差缓解（resilience_level）
- 从较少的shots开始，最终运行时增加

## 常见模式

### 模式1：简单电路执行

```python
from qiskit import QuantumCircuit, transpile
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()
counts = result[0].data.meas.get_counts()
```

### 模式2：带转译的硬件执行

```python
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit import transpile

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

qc_optimized = transpile(qc, backend=backend, optimization_level=3)

sampler = Sampler(backend)
job = sampler.run([qc_optimized], shots=1024)
result = job.result()
```

### 模式3：变分算法（VQE）

```python
from qiskit_ibm_runtime import Session, EstimatorV2 as Estimator
from scipy.optimize import minimize

with Session(backend=backend) as session:
    estimator = Estimator(session=session)

    def cost_function(params):
        bound_qc = ansatz.assign_parameters(params)
        qc_isa = transpile(bound_qc, backend=backend)
        result = estimator.run([(qc_isa, hamiltonian)]).result()
        return result[0].data.evs

    result = minimize(cost_function, initial_params, method='COBYLA')
```

## 额外资源

- **官方文档**：https://quantum.ibm.com/docs
- **Qiskit教科书**：https://qiskit.org/learn
- **API参考**：https://docs.quantum.ibm.com/api/qiskit
- **模式指南**：https://quantum.cloud.ibm.com/docs/en/guides/intro-to-patterns