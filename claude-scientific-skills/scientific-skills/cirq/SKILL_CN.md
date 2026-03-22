---
name: cirq
description: Google 量子计算框架。当针对 Google Quantum AI 硬件、设计噪声感知电路或运行量子表征实验时使用。最适合 Google 硬件、噪声建模和低级电路设计。对于 IBM 硬件使用 qiskit; 对于具有自动微分的量子 ML 使用 pennylane; 对于物理模拟使用 qutip。
license: Apache-2.0 许可证
metadata:
    skill-author: K-Dense Inc.
---

# Cirq - Python 量子计算

Cirq 是 Google Quantum AI 的开源框架,用于在量子计算机和模拟器上设计、模拟和运行量子电路。

## 安装

```bash
uv pip install cirq
```

对于硬件集成:
```bash
# Google Quantum Engine
uv pip install cirq-google

# IonQ
uv pip install cirq-ionq

# AQT (Alpine Quantum Technologies)
uv pip install cirq-aqt

# Pasqal
uv pip install cirq-pasqal

# Azure Quantum
uv pip install azure-quantum cirq
```

## 快速开始

### 基本电路

```python
import cirq
import numpy as np

# 创建量子比特
q0, q1 = cirq.LineQubit.range(2)

# 构建电路
circuit = cirq.Circuit(
    cirq.H(q0),              # 在 q0 上应用 Hadamard 门
    cirq.CNOT(q0, q1),       # CNOT 门,q0 为控制,q1 为目标
    cirq.measure(q0, q1, key='result')
)

print(circuit)

# 模拟
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=1000)

# 显示结果
print(result.histogram(key='result'))
```

### 参数化电路

```python
import sympy

# 定义符号参数
theta = sympy.Symbol('theta')

# 创建参数化电路
circuit = cirq.Circuit(
    cirq.ry(theta)(q0),
    cirq.measure(q0, key='m')
)

# 扫描参数值
sweep = cirq.Linspace('theta', start=0, stop=2*np.pi, length=20)
results = simulator.run_sweep(circuit, params=sweep, repetitions=1000)

# 处理结果
for params, result in zip(sweep, results):
    theta_val = params['theta']
    counts = result.histogram(key='m')
    print(f"θ={theta_val:.2f}: {counts}")
```

## 核心功能

### 电路构建

关于构建量子电路的全面信息,包括量子比特、门、操作、自定义门和电路模式,请参阅:
- **[references/building.md](references/building.md)** - 电路构建完整指南

常见主题:
- 量子比特类型(GridQubit、LineQubit、NamedQubit)
- 单量子比特和双量子比特门
- 参数化门和操作
- 自定义门分解
- 使用时刻组织电路
- 标准电路模式(Bell 态、GHZ、QFT)
- 导入/导出(OpenQASM、JSON)
- 使用量子位和可观测量

### 模拟

关于模拟量子电路的详细信息,包括精确模拟、噪声模拟、参数扫描和量子虚拟机,请参阅:
- **[references/simulation.md](references/simulation.md)** - 量子模拟完整指南

常见主题:
- 精确模拟(态矢量、密度矩阵)
- 采样和测量
- 参数扫描(单个和多个参数)
- 噪声模拟
- 态直方图和可视化
- 量子虚拟机(QVM)
- 期望值和可观测量
- 性能优化

### 电路变换

关于优化、编译和操作量子电路的信息,请参阅:
- **[references/transformation.md](references/transformation.md)** - 电路变换完整指南

常见主题:
- 变换器框架
- 门分解
- 电路优化(合并门、弹出 Z 门、丢弃可忽略操作)
- 硬件电路编译
- 量子比特路由和 SWAP 插入
- 自定义变换器
- 变换流水线

### 硬件集成

关于在各种提供商的真实量子硬件上运行电路的信息,请参阅:
- **[references/hardware.md](references/hardware.md)** - 硬件集成完整指南

支持的提供商:
- **Google Quantum AI**(cirq-google) - Sycamore、Weber 处理器
- **IonQ**(cirq-ionq) - 离子阱量子计算机
- **Azure Quantum**(azure-quantum) - IonQ 和 Honeywell 后端
- **AQT**(cirq-aqt) - Alpine Quantum Technologies
- **Pasqal**(cirq-pasqal) - 中性原子量子计算机

主题包括设备表示、量子比特选择、身份验证、作业管理和硬件电路优化。

### 噪声建模

关于建模噪声、噪声模拟、表征和错误缓解的信息,请参阅:
- **[references/noise.md](references/noise.md)** - 噪声建模完整指南

常见主题:
- 噪声信道(去极化、振幅衰减、相位衰减)
- 噪声模型(常数、门特定、量子比特特定、热)
- 向电路添加噪声
- 读出噪声
- 噪声表征(随机基准测试、XEB)
- 噪声可视化(热图)
- 错误缓解技术

### 量子实验

关于设计实验、参数扫描、数据收集和使用 ReCirq 框架的信息,请参阅:
- **[references/experiments.md](references/experiments.md)** - 量子实验完整指南

常见主题:
- 实验设计模式
- 参数扫描和数据收集
- ReCirq 框架结构
- 常见算法(VQE、QAOA、QPE)
- 数据分析和可视化
- 统计分析和保真度估计
- 并行数据收集

## 常见模式

### 变分算法模板

```python
import scipy.optimize

def variational_algorithm(ansatz, cost_function, initial_params):
    """变分量子算法模板。"""

    def objective(params):
        circuit = ansatz(params)
        simulator = cirq.Simulator()
        result = simulator.simulate(circuit)
        return cost_function(result)

    # 优化
    result = scipy.optimize.minimize(
        objective,
        initial_params,
        method='COBYLA'
    )

    return result

# 定义 ansatz
def my_ansatz(params):
    q = cirq.LineQubit(0)
    return cirq.Circuit(
        cirq.ry(params[0])(q),
        cirq.rz(params[1])(q)
    )

# 定义代价函数
def my_cost(result):
    state = result.final_state_vector
    # 基于态计算代价
    return np.real(state[0])

# 运行优化
result = variational_algorithm(my_ansatz, my_cost, [0.0, 0.0])
```

### 硬件执行模板

```python
def run_on_hardware(circuit, provider='google', device_name='weber', repetitions=1000):
    """在量子硬件上运行的模板。"""

    if provider == 'google':
        import cirq_google
        engine = cirq_google.get_engine()
        processor = engine.get_processor(device_name)
        job = processor.run(circuit, repetitions=repetitions)
        return job.results()[0]

    elif provider == 'ionq':
        import cirq_ionq
        service = cirq_ionq.Service()
        result = service.run(circuit, repetitions=repetitions, target='qpu')
        return result

    elif provider == 'azure':
        from azure.quantum.cirq import AzureQuantumService
        # 设置工作区...
        service = AzureQuantumService(workspace)
        result = service.run(circuit, repetitions=repetitions, target='ionq.qpu')
        return result

    else:
        raise ValueError(f"未知提供商: {provider}")
```

### 噪声研究模板

```python
def noise_comparison_study(circuit, noise_levels):
    """比较不同噪声水平下的电路性能。"""

    results = {}

    for noise_level in noise_levels:
        # 创建噪声电路
        noisy_circuit = circuit.with_noise(cirq.depolarize(p=noise_level))

        # 模拟
        simulator = cirq.DensityMatrixSimulator()
        result = simulator.run(noisy_circuit, repetitions=1000)

        # 分析
        results[noise_level] = {
            'histogram': result.histogram(key='result'),
            'dominant_state': max(
                result.histogram(key='result').items(),
                key=lambda x: x[1]
            )
        }

    return results

# 运行研究
noise_levels = [0.0, 0.001, 0.01, 0.05, 0.1]
results = noise_comparison_study(circuit, noise_levels)
```

## 最佳实践

1. **电路设计**
   - 为您的拓扑结构使用适当的量子比特类型
   - 保持电路模块化和可重用
   - 使用描述性键标记测量
   - 执行前根据设备约束验证电路

2. **模拟**
   - 对纯态使用态矢量模拟(更高效)
   - 仅在需要时使用密度矩阵模拟(混合态、噪声)
   - 利用参数扫描而不是单独运行
   - 监控大型系统的内存使用量(2^n 增长很快)

3. **硬件执行**
   - 始终先在模拟器上测试
   - 使用校准数据选择最佳量子比特
   - 针对目标硬件门集优化电路
   - 为生产运行实施错误缓解
   - 立即存储昂贵的硬件结果

4. **电路优化**
   - 从高级内置变换器开始
   - 按顺序链接多个优化
   - 跟踪深度和门数减少
   - 变换后验证正确性

5. **噪声建模**
   - 使用来自校准数据的现实噪声模型
   - 包括所有错误源(门、退相干、读出)
   - 在缓解之前表征
   - 保持电路浅以最小化噪声积累

6. **实验**
   - 用清晰的分离构建实验(数据生成、收集、分析)
   - 使用 ReCirq 模式以确保可重现性
   - 频繁保存中间结果
   - 并行化独立任务
   - 使用元数据彻底记录

## 其他资源

- **官方文档**: https://quantumai.google/cirq
- **API 参考**: https://quantumai.google/reference/python/cirq
- **教程**: https://quantumai.google/cirq/tutorials
- **示例**: https://github.com/quantumlib/Cirq/tree/master/examples
- **ReCirq**: https://github.com/quantumlib/ReCirq

## 常见问题

**电路对于硬件来说太深:**
- 使用电路优化变换器减少深度
- 参见 `transformation.md` 了解优化技术

**模拟内存问题:**
- 从密度矩阵切换到态矢量模拟器
- 减少量子比特数量或对 Clifford 电路使用稳定器模拟器

**设备验证错误:**
- 使用 device.metadata.nx_graph 检查量子比特连通性
- 将门分解为设备原生门集
- 参见 `hardware.md` 了解设备特定编译

**噪声模拟太慢:**
- 密度矩阵模拟是 O(2^2n) - 考虑减少量子比特
- 选择性地仅在关键操作上使用噪声模型
- 参见 `simulation.md` 了解性能优化
