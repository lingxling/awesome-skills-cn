---
name: stable-baselines3
description: 生产就绪的强化学习算法（PPO、SAC、DQN、TD3、DDPG、A2C），具有类 scikit-learn API。用于标准 RL 实验、快速原型设计和文档完善的算法实现。最适用于带有 Gymnasium 环境的单智能体 RL。对于高性能并行训练、多智能体系统或自定义向量化环境，请使用 pufferlib。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# Stable Baselines3

## 概述

Stable Baselines3 (SB3) 是一个基于 PyTorch 的库，提供可靠的强化学习算法实现。此技能提供全面的指导，用于使用 SB3 的统一 API 训练 RL 智能体、创建自定义环境、实现回调以及优化训练工作流。

## 核心功能

### 1. 训练 RL 智能体

**基本训练模式：**

```python
import gymnasium as gym
from stable_baselines3 import PPO

# 创建环境
env = gym.make("CartPole-v1")

# 初始化智能体
model = PPO("MlpPolicy", env, verbose=1)

# 训练智能体
model.learn(total_timesteps=10000)

# 保存模型
model.save("ppo_cartpole")

# 加载模型（无需先实例化）
model = PPO.load("ppo_cartpole", env=env)
```

**重要说明：**
- `total_timesteps` 是下限；实际训练可能会因批次收集而超过此值
- 使用 `model.load()` 作为静态方法，而不是在现有实例上使用
- 为节省空间，模型不会保存回放缓冲区

**算法选择：**
使用 `references/algorithms.md` 获取详细的算法特性和选择指南。快速参考：
- **PPO/A2C**：通用，支持所有动作空间类型，适合多处理
- **SAC/TD3**：连续控制，离策略，样本高效
- **DQN**：离散动作，离策略
- **HER**：目标条件任务

有关完整的训练模板和最佳实践，请参阅 `scripts/train_rl_agent.py`。

### 2. 自定义环境

**要求：**
自定义环境必须继承自 `gymnasium.Env` 并实现：
- `__init__()`：定义 action_space 和 observation_space
- `reset(seed, options)`：返回初始观察和信息字典
- `step(action)`：返回观察、奖励、terminated、truncated、信息
- `render()`：可视化（可选）
- `close()`：清理资源

**关键约束：**
- 图像观察必须是 `np.uint8` 类型，范围 [0, 255]
- 尽可能使用通道优先格式（通道, 高度, 宽度）
- SB3 会自动通过除以 255 来标准化图像
- 如果已预标准化，在 policy_kwargs 中设置 `normalize_images=False`
- SB3 不支持 `start!=0` 的 `Discrete` 或 `MultiDiscrete` 空间

**验证：**
```python
from stable_baselines3.common.env_checker import check_env

check_env(env, warn=True)
```

有关完整的自定义环境模板，请参阅 `scripts/custom_env_template.py`，有关综合指导，请参阅 `references/custom_environments.md`。

### 3. 向量化环境

**目的：**
向量化环境并行运行多个环境实例，加速训练并启用某些包装器（帧堆叠、标准化）。

**类型：**
- **DummyVecEnv**：在当前进程中顺序执行（适用于轻量级环境）
- **SubprocVecEnv**：跨进程并行执行（适用于计算密集型环境）

**快速设置：**
```python
from stable_baselines3.common.env_util import make_vec_env

# 创建 4 个并行环境
env = make_vec_env("CartPole-v1", n_envs=4, vec_env_cls=SubprocVecEnv)

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=25000)
```

**离策略优化：**
当使用多个环境与离策略算法（SAC、TD3、DQN）时，设置 `gradient_steps=-1` 以在每个环境步骤执行一次梯度更新，平衡墙钟时间和样本效率。

**API 差异：**
- `reset()` 仅返回观察（信息可在 `vec_env.reset_infos` 中获取）
- `step()` 返回 4 元组：`(obs, rewards, dones, infos)` 而不是 5 元组
- 环境在 episodes 后自动重置
- 终端观察可通过 `infos[env_idx]["terminal_observation"]` 获取

有关包装器和高级用法的详细信息，请参阅 `references/vectorized_envs.md`。

### 4. 用于监控和控制的回调

**目的：**
回调启用监控指标、保存检查点、实现早停和自定义训练逻辑，而无需修改核心算法。

**常见回调：**
- **EvalCallback**：定期评估并保存最佳模型
- **CheckpointCallback**：按间隔保存模型检查点
- **StopTrainingOnRewardThreshold**：当达到目标奖励时停止
- **ProgressBarCallback**：显示带有计时的训练进度

**自定义回调结构：**
```python
from stable_baselines3.common.callbacks import BaseCallback

class CustomCallback(BaseCallback):
    def _on_training_start(self):
        # 在第一次 rollout 之前调用
        pass

    def _on_step(self):
        # 在每个环境步骤后调用
        # 返回 False 以停止训练
        return True

    def _on_rollout_end(self):
        # 在 rollout 结束时调用
        pass
```

**可用属性：**
- `self.model`：RL 算法实例
- `self.num_timesteps`：总环境步骤
- `self.training_env`：训练环境

**链接回调：**
```python
from stable_baselines3.common.callbacks import CallbackList

callback = CallbackList([eval_callback, checkpoint_callback, custom_callback])
model.learn(total_timesteps=10000, callback=callback)
```

有关综合回调文档，请参阅 `references/callbacks.md`。

### 5. 模型持久化和检查

**保存和加载：**
```python
# 保存模型
model.save("model_name")

# 保存标准化统计信息（如果使用 VecNormalize）
vec_env.save("vec_normalize.pkl")

# 加载模型
model = PPO.load("model_name", env=env)

# 加载标准化统计信息
vec_env = VecNormalize.load("vec_normalize.pkl", vec_env)
```

**参数访问：**
```python
# 获取参数
params = model.get_parameters()

# 设置参数
model.set_parameters(params)

# 访问 PyTorch 状态字典
state_dict = model.policy.state_dict()
```

### 6. 评估和记录

**评估：**
```python
from stable_baselines3.common.evaluation import evaluate_policy

mean_reward, std_reward = evaluate_policy(
    model,
    env,
    n_eval_episodes=10,
    deterministic=True
)
```

**视频录制：**
```python
from stable_baselines3.common.vec_env import VecVideoRecorder

# 用视频录制器包装环境
env = VecVideoRecorder(
    env,
    "videos/",
    record_video_trigger=lambda x: x % 2000 == 0,
    video_length=200
)
```

有关完整的评估和记录模板，请参阅 `scripts/evaluate_agent.py`。

### 7. 高级功能

**学习率调度：**
```python
def linear_schedule(initial_value):
    def func(progress_remaining):
        # progress_remaining 从 1 变为 0
        return progress_remaining * initial_value
    return func

model = PPO("MlpPolicy", env, learning_rate=linear_schedule(0.001))
```

**多输入策略（字典观察）：**
```python
model = PPO("MultiInputPolicy", env, verbose=1)
```
当观察是字典时使用（例如，结合图像和传感器数据）。

**事后经验回放：**
```python
from stable_baselines3 import SAC, HerReplayBuffer

model = SAC(
    "MultiInputPolicy",
    env,
    replay_buffer_class=HerReplayBuffer,
    replay_buffer_kwargs=dict(
        n_sampled_goal=4,
        goal_selection_strategy="future",
    ),
)
```

**TensorBoard 集成：**
```python
model = PPO("MlpPolicy", env, tensorboard_log="./tensorboard/")
model.learn(total_timesteps=10000)
```

## 工作流指导

**开始新的 RL 项目：**

1. **定义问题**：识别观察空间、动作空间和奖励结构
2. **选择算法**：使用 `references/algorithms.md` 获取选择指南
3. **创建/适配环境**：必要时使用 `scripts/custom_env_template.py`
4. **验证环境**：训练前始终运行 `check_env()`
5. **设置训练**：使用 `scripts/train_rl_agent.py` 作为起始模板
6. **添加监控**：实现评估和检查点的回调
7. **优化性能**：考虑使用向量化环境提高速度
8. **评估和迭代**：使用 `scripts/evaluate_agent.py` 进行评估

**常见问题：**

- **内存错误**：为离策略算法减少 `buffer_size` 或使用更少的并行环境
- **训练缓慢**：考虑使用 SubprocVecEnv 进行并行环境
- **训练不稳定**：尝试不同的算法，调整超参数，或检查奖励缩放
- **导入错误**：确保安装了 `stable_baselines3`：`uv pip install stable-baselines3[extra]`

## 资源

### scripts/
- `train_rl_agent.py`：带有最佳实践的完整训练脚本模板
- `evaluate_agent.py`：智能体评估和视频录制模板
- `custom_env_template.py`：自定义 Gym 环境模板

### references/
- `algorithms.md`：详细的算法比较和选择指南
- `custom_environments.md`：综合的自定义环境创建指南
- `callbacks.md`：完整的回调系统参考
- `vectorized_envs.md`：向量化环境使用和包装器

## 安装

```bash
# 基本安装
uv pip install stable-baselines3

# 带有额外依赖（Tensorboard 等）
uv pip install stable-baselines3[extra]
```