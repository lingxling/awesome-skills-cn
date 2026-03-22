---
name: pennylane
description: 硬件无关的量子机器学习框架，具有自动微分功能。用于通过梯度训练量子电路、构建混合量子-经典模型，或在IBM/Google/Rigetti/IonQ等设备之间实现可移植性。最适合变分算法（VQE、QAOA）、量子神经网络以及与PyTorch/JAX/TensorFlow的集成。对于硬件特定优化，请使用qiskit（IBM）或cirq（Google）；对于开放量子系统，请使用qutip。
license: Apache-2.0 license
metadata:
    skill-author: K-Dense Inc.
---

# PennyLane

## 概述

PennyLane是一个量子计算库，使训练量子计算机像训练神经网络一样。它提供量子电路的自动微分、设备无关编程以及与经典机器学习框架的无缝集成。

## 安装

使用uv安装：

```bash
uv pip install pennylane
```

对于量子硬件访问，安装设备插件：

```bash
# IBM Quantum
uv pip install pennylane-qiskit

# Amazon Braket
uv pip install amazon-braket-pennylane-plugin

# Google Cirq
uv pip install pennylane-cirq

# Rigetti Forest
uv pip install pennylane-rigetti

# IonQ
uv pip install pennylane-ionq
```

## 快速开始

构建量子电路并优化其参数：

```python
import pennylane as qml
from pennylane import numpy as np

# 创建设备
dev = qml.device('default.qubit', wires=2)

# 定义量子电路
@qml.qnode(dev)
def circuit(params):
    qml.RX(params[0], wires=0)
    qml.RY(params[1], wires=1)
    qml.CNOT(wires=[0, 1])
    return qml.expval(qml.PauliZ(0))

# 优化参数
opt = qml.GradientDescentOptimizer(stepsize=0.1)
params = np.array([0.1, 0.2], requires_grad=True)

for i in range(100):
    params = opt.step(circuit, params)
```

## 核心功能

### 1. 量子电路构建

使用门、测量和状态准备构建电路。请参阅`references/quantum_circuits.md`了解：
- 单量子比特和多量子比特门
- 受控操作和条件逻辑
- 电路中间测量和自适应电路
- 各种测量类型（期望值、概率、样本）
- 电路检查和调试

### 2. 量子机器学习

创建混合量子-经典模型。请参阅`references/quantum_ml.md`了解：
- 与PyTorch、JAX、TensorFlow的集成
- 量子神经网络和变分分类器
- 数据编码策略（角度、振幅、基、IQP）
- 使用反向传播训练混合模型
- 量子电路的迁移学习

### 3. 量子化学

模拟分子并计算基态能量。请参阅`references/quantum_chemistry.md`了解：
- 分子哈密顿量生成
- 变分量子本征求解器（VQE）
- 用于化学的UCCSD ansatz
- 几何优化和解离曲线
- 分子性质计算

### 4. 设备管理

在模拟器或量子硬件上执行。请参阅`references/devices_backends.md`了解：
- 内置模拟器（default.qubit、lightning.qubit、default.mixed）
- 硬件插件（IBM、Amazon Braket、Google、Rigetti、IonQ）
- 设备选择和配置
- 性能优化和缓存
- GPU加速和JIT编译

### 5. 优化

使用各种优化器训练量子电路。请参阅`references/optimization.md`了解：
- 内置优化器（Adam、梯度下降、动量、RMSProp）
- 梯度计算方法（反向传播、参数移位、伴随）
- 变分算法（VQE、QAOA）
- 训练策略（学习率调度、小批量）
- 处理 barren plateaus和局部最小值

### 6. 高级功能

利用模板、变换和编译。请参阅`references/advanced_features.md`了解：
- 电路模板和层
- 变换和电路优化
- 脉冲级编程
- Catalyst JIT编译
- 噪声模型和错误缓解
- 资源估计

## 常见工作流程

### 训练变分分类器

```python
# 1. 定义ansatz
@qml.qnode(dev)
def classifier(x, weights):
    # 编码数据
    qml.AngleEmbedding(x, wires=range(4))

    # 变分层
    qml.StronglyEntanglingLayers(weights, wires=range(4))

    return qml.expval(qml.PauliZ(0))

# 2. 训练
opt = qml.AdamOptimizer(stepsize=0.01)
weights = np.random.random((3, 4, 3))  # 3层，4个量子比特

for epoch in range(100):
    for x, y in zip(X_train, y_train):
        weights = opt.step(lambda w: (classifier(x, w) - y)**2, weights)
```

### 运行VQE计算分子基态

```python
from pennylane import qchem

# 1. 构建哈密顿量
symbols = ['H', 'H']
coords = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.74])
H, n_qubits = qchem.molecular_hamiltonian(symbols, coords)

# 2. 定义ansatz
@qml.qnode(dev)
def vqe_circuit(params):
    qml.BasisState(qchem.hf_state(2, n_qubits), wires=range(n_qubits))
    qml.UCCSD(params, wires=range(n_qubits))
    return qml.expval(H)

# 3. 优化
opt = qml.AdamOptimizer(stepsize=0.1)
params = np.zeros(10, requires_grad=True)

for i in range(100):
    params, energy = opt.step_and_cost(vqe_circuit, params)
    print(f"步骤 {i}: 能量 = {energy:.6f} Ha")
```

### 在设备之间切换

```python
# 相同电路，不同后端
circuit_def = lambda dev: qml.qnode(dev)(circuit_function)

# 在模拟器上测试
dev_sim = qml.device('default.qubit', wires=4)
result_sim = circuit_def(dev_sim)(params)

# 在量子硬件上运行
dev_hw = qml.device('qiskit.ibmq', wires=4, backend='ibmq_manila')
result_hw = circuit_def(dev_hw)(params)
```

## 详细文档

有关特定主题的全面覆盖，请参考参考文件：

- **入门**：`references/getting_started.md` - 安装、基本概念、第一步
- **量子电路**：`references/quantum_circuits.md` - 门、测量、电路模式
- **量子机器学习**：`references/quantum_ml.md` - 混合模型、框架集成、QNN
- **量子化学**：`references/quantum_chemistry.md` - VQE、分子哈密顿量、化学工作流
- **设备**：`references/devices_backends.md` - 模拟器、硬件插件、设备配置
- **优化**：`references/optimization.md` - 优化器、梯度、变分算法
- **高级**：`references/advanced_features.md` - 模板、变换、JIT编译、噪声

## 最佳实践

1. **从模拟器开始** - 在部署到硬件之前在`default.qubit`上测试
2. **对硬件使用参数移位** - 反向传播仅适用于模拟器
3. **选择适当的编码** - 将数据编码与问题结构匹配
4. **仔细初始化** - 使用小随机值避免barren plateaus
5. **监控梯度** - 检查深度电路中的梯度消失
6. **缓存设备** - 重用设备对象以减少初始化开销
7. **分析电路** - 使用`qml.specs()`分析电路复杂性
8. **本地测试** - 在提交到硬件之前在模拟器上验证
9. **使用模板** - 利用内置模板进行常见电路模式
10. **尽可能编译** - 对性能关键代码使用Catalyst JIT

## 资源

- 官方文档：https://docs.pennylane.ai
- 代码手册（教程）：https://pennylane.ai/codebook
- QML演示：https://pennylane.ai/qml/demonstrations
- 社区论坛：https://discuss.pennylane.ai
- GitHub：https://github.com/PennyLaneAI/pennylane