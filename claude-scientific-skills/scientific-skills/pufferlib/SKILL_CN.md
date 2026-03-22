---
name: pufferlib
description: 高性能强化学习框架，针对速度和规模进行了优化。当您需要快速并行训练、向量化环境、多智能体系统或与游戏环境（Atari、Procgen、NetHack）集成时使用。实现比标准实现快2-10倍的速度。对于快速原型设计或具有广泛文档的标准算法实现，请使用stable-baselines3。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# PufferLib - 高性能强化学习

## 概述

PufferLib是一个高性能强化学习库，专为快速并行环境模拟和训练而设计。它通过优化的向量化、原生多智能体支持和高效的PPO实现（PuffeRL）实现每秒数百万步的训练。该库提供Ocean套件的20+环境，并与Gymnasium、PettingZoo和专业RL框架无缝集成。

## 使用场景

本技能适用于以下情况：
- **训练RL智能体** 在任何环境（单智能体或多智能体）上使用PPO
- **创建自定义环境** 使用PufferEnv API
- **优化性能** 用于并行环境模拟（向量化）
- **集成现有环境** 来自Gymnasium、PettingZoo、Atari、Procgen等
- **开发策略** 使用CNN、LSTM或自定义架构
- **扩展RL** 到每秒数百万步以加快实验速度
- **多智能体RL** 具有原生多智能体环境支持

## 核心功能

### 1. 高性能训练（PuffeRL）

PuffeRL是PufferLib的优化PPO+LSTM训练算法，实现1M-4M步/秒。

**快速开始训练：**
```bash
# CLI训练
puffer train procgen-coinrun --train.device cuda --train.learning-rate 3e-4

# 分布式训练
torchrun --nproc_per_node=4 train.py
```

**Python训练循环：**
```python
import pufferlib
from pufferlib import PuffeRL

# 创建向量化环境
env = pufferlib.make('procgen-coinrun', num_envs=256)

# 创建训练器
trainer = PuffeRL(
    env=env,
    policy=my_policy,
    device='cuda',
    learning_rate=3e-4,
    batch_size=32768
)

# 训练循环
for iteration in range(num_iterations):
    trainer.evaluate()  # 收集轨迹
    trainer.train()     # 在批次上训练
    trainer.mean_and_log()  # 记录结果
```

**有关全面的训练指导**，请阅读`references/training.md`以获取：
- 完整的训练工作流程和CLI选项
- 使用Protein进行超参数调优
- 分布式多GPU/多节点训练
- 日志记录器集成（Weights & Biases，Neptune）
- 检查点和恢复训练
- 性能优化技巧
- 课程学习模式

### 2. 环境开发（PufferEnv）

使用PufferEnv API创建自定义高性能环境。

**基本环境结构：**
```python
import numpy as np
from pufferlib import PufferEnv

class MyEnvironment(PufferEnv):
    def __init__(self, buf=None):
        super().__init__(buf)

        # 定义空间
        self.observation_space = self.make_space((4,))
        self.action_space = self.make_discrete(4)

        self.reset()

    def reset(self):
        # 重置状态并返回初始观察
        return np.zeros(4, dtype=np.float32)

    def step(self, action):
        # 执行动作，计算奖励，检查完成
        obs = self._get_observation()
        reward = self._compute_reward()
        done = self._is_done()
        info = {}

        return obs, reward, done, info
```

**使用模板脚本：** `scripts/env_template.py` 提供完整的单智能体和多智能体环境模板，包括：
- 不同的观察空间类型（向量、图像、字典）
- 动作空间变体（离散、连续、多离散）
- 多智能体环境结构
- 测试工具

**有关完整的环境开发**，请阅读`references/environments.md`以获取：
- PufferEnv API详细信息和原地操作模式
- 观察和动作空间定义
- 多智能体环境创建
- Ocean套件（20+预构建环境）
- 性能优化（Python到C工作流程）
- 环境包装器和最佳实践
- 调试和验证技术

### 3. 向量化和性能

通过优化的并行模拟实现最大吞吐量。

**向量化设置：**
```python
import pufferlib

# 自动向量化
env = pufferlib.make('environment_name', num_envs=256, num_workers=8)

# 性能基准：
# - 纯Python环境：100k-500k SPS
# - C基环境：100M+ SPS
# - 带训练：400k-4M总SPS
```

**关键优化：**
- 共享内存缓冲区用于零拷贝观察传递
- 忙等待标志代替管道/队列
- 用于异步返回的多余环境
- 每个工作者多个环境

**有关向量化优化**，请阅读`references/vectorization.md`以获取：
- 架构和性能特征
- 工作者和批处理大小配置
- 串行vs多处理vs异步模式
- 共享内存和零拷贝模式
- 大规模分层向量化
- 多智能体向量化策略
- 性能分析和故障排除

### 4. 策略开发

将策略构建为标准PyTorch模块，可选实用程序。

**基本策略结构：**
```python
import torch.nn as nn
from pufferlib.pytorch import layer_init

class Policy(nn.Module):
    def __init__(self, observation_space, action_space):
        super().__init__()

        # 编码器
        self.encoder = nn.Sequential(
            layer_init(nn.Linear(obs_dim, 256)),
            nn.ReLU(),
            layer_init(nn.Linear(256, 256)),
            nn.ReLU()
        )

        # 演员和评论家头部
        self.actor = layer_init(nn.Linear(256, num_actions), std=0.01)
        self.critic = layer_init(nn.Linear(256, 1), std=1.0)

    def forward(self, observations):
        features = self.encoder(observations)
        return self.actor(features), self.critic(features)
```

**有关完整的策略开发**，请阅读`references/policies.md`以获取：
- 用于图像观察的CNN策略
- 带优化LSTM的递归策略（3倍更快的推理）
- 用于复杂观察的多输入策略
- 连续动作策略
- 多智能体策略（共享vs独立参数）
- 高级架构（注意力、残差）
- 观察归一化和梯度裁剪
- 策略调试和测试

### 5. 环境集成

无缝集成来自流行RL框架的环境。

**Gymnasium集成：**
```python
import gymnasium as gym
import pufferlib

# 包装Gymnasium环境
gym_env = gym.make('CartPole-v1')
env = pufferlib.emulate(gym_env, num_envs=256)

# 或直接使用make
env = pufferlib.make('gym-CartPole-v1', num_envs=256)
```

**PettingZoo多智能体：**
```python
# 多智能体环境
env = pufferlib.make('pettingzoo-knights-archers-zombies', num_envs=128)
```

**支持的框架：**
- Gymnasium / OpenAI Gym
- PettingZoo（并行和AEC）
- Atari（ALE）
- Procgen
- NetHack / MiniHack
- Minigrid
- Neural MMO
- Crafter
- GPUDrive
- MicroRTS
- Griddly
- 等等...

**有关集成详情**，请阅读`references/integration.md`以获取：
- 每个框架的完整集成示例
- 自定义包装器（观察、奖励、帧堆叠、动作重复）
- 空间展平和反展平
- 环境注册
- 兼容性模式
- 性能考虑
- 集成调试

## 快速开始工作流程

### 训练现有环境

1. 从Ocean套件或兼容框架中选择环境
2. 使用`scripts/train_template.py`作为起点
3. 为您的任务配置超参数
4. 使用CLI或Python脚本运行训练
5. 使用Weights & Biases或Neptune监控
6. 参考`references/training.md`进行优化

### 创建自定义环境

1. 从`scripts/env_template.py`开始
2. 定义观察和动作空间
3. 实现`reset()`和`step()`方法
4. 本地测试环境
5. 使用`pufferlib.emulate()`或`make()`向量化
6. 参考`references/environments.md`获取高级模式
7. 如果需要，使用`references/vectorization.md`进行优化

### 策略开发

1. 根据观察选择架构：
   - 向量观察 → MLP策略
   - 图像观察 → CNN策略
   - 顺序任务 → LSTM策略
   - 复杂观察 → 多输入策略
2. 使用`layer_init`进行正确的权重初始化
3. 遵循`references/policies.md`中的模式
4. 在全面训练前用环境测试

### 性能优化

1. 分析当前吞吐量（每秒步数）
2. 检查向量化配置（num_envs, num_workers）
3. 优化环境代码（原地操作，numpy向量化）
4. 考虑关键路径的C实现
5. 使用`references/vectorization.md`进行系统优化

## 资源

### scripts/

**train_template.py** - 完整的训练脚本模板，包括：
- 环境创建和配置
- 策略初始化
- 日志记录器集成（WandB, Neptune）
- 带检查点的训练循环
- 命令行参数解析
- 多GPU分布式训练设置

**env_template.py** - 环境实现模板：
- 单智能体PufferEnv示例（网格世界）
- 多智能体PufferEnv示例（协作导航）
- 多种观察/动作空间模式
- 测试工具

### references/

**training.md** - 综合训练指南：
- 训练工作流程和CLI选项
- 超参数配置
- 分布式训练（多GPU，多节点）
- 监控和日志记录
- 检查点
- Protein超参数调优
- 性能优化
- 常见训练模式
- 故障排除

**environments.md** - 环境开发指南：
- PufferEnv API和特性
- 观察和动作空间
- 多智能体环境
- Ocean套件环境
- 自定义环境开发工作流程
- Python到C优化路径
- 第三方环境集成
- 包装器和最佳实践
- 调试

**vectorization.md** - 向量化优化：
- 架构和关键优化
- 向量化模式（串行，多处理，异步）
- 工作者和批处理配置
- 共享内存和零拷贝模式
- 高级向量化（分层，自定义）
- 多智能体向量化
- 性能监控和分析
- 故障排除和最佳实践

**policies.md** - 策略架构指南：
- 基本策略结构
- 用于图像的CNN策略
- 带优化的LSTM策略
- 多输入策略
- 连续动作策略
- 多智能体策略
- 高级架构（注意力，残差）
- 观察处理和反展平
- 初始化和归一化
- 调试和测试

**integration.md** - 框架集成指南：
- Gymnasium集成
- PettingZoo集成（并行和AEC）
- 第三方环境（Procgen, NetHack, Minigrid等）
- 自定义包装器（观察，奖励，帧堆叠等）
- 空间转换和反展平
- 环境注册
- 兼容性模式
- 性能考虑
- 调试集成

## 成功提示

1. **从简单开始**：在创建自定义环境之前，先从Ocean环境或Gymnasium集成开始

2. **早期分析**：从一开始就测量每秒步数，以识别瓶颈

3. **使用模板**：`scripts/train_template.py`和`scripts/env_template.py`提供了坚实的起点

4. **按需阅读参考**：每个参考文件都是自包含的，专注于特定能力

5. **逐步优化**：从Python开始，分析，然后在需要时用C优化关键路径

6. **利用向量化**：PufferLib的向量化是实现高吞吐量的关键

7. **监控训练**：使用WandB或Neptune跟踪实验并及早识别问题

8. **测试环境**：在扩大训练规模之前验证环境逻辑

9. **检查现有环境**：Ocean套件提供20+预构建环境

10. **使用适当的初始化**：始终使用`pufferlib.pytorch`中的`layer_init`用于策略

## 常见用例

### 在标准基准上训练
```python
# Atari
env = pufferlib.make('atari-pong', num_envs=256)

# Procgen
env = pufferlib.make('procgen-coinrun', num_envs=256)

# Minigrid
env = pufferlib.make('minigrid-empty-8x8', num_envs=256)
```

### 多智能体学习
```python
# PettingZoo
env = pufferlib.make('pettingzoo-pistonball', num_envs=128)

# 所有智能体共享策略
policy = create_policy(env.observation_space, env.action_space)
trainer = PuffeRL(env=env, policy=policy)
```

### 自定义任务开发
```python
# 创建自定义环境
class MyTask(PufferEnv):
    # ... 实现环境 ...

# 向量化并训练
env = pufferlib.emulate(MyTask, num_envs=256)
trainer = PuffeRL(env=env, policy=my_policy)
```

### 高性能优化
```python
# 最大化吞吐量
env = pufferlib.make(
    'my-env',
    num_envs=1024,      # 大批量
    num_workers=16,     # 许多工作者
    envs_per_worker=64  # 优化每个工作者
)
```

## 安装

```bash
uv pip install pufferlib
```

## 文档

- 官方文档：https://puffer.ai/docs.html
- GitHub：https://github.com/PufferAI/PufferLib
- Discord：提供社区支持