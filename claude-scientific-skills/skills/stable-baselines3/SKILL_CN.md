---
name: stable-baselines3
description: 使用 Stable Baselines3（PPO、SAC、DQN、TD3、DDPG、A2C）训练和评估单智能体强化学习，涵盖 Gymnasium 自定义环境、向量化 rollout、回调（callback）和检查点归一化。适用于可复现的 RL 实验、连续控制、离散动作，以及 SB3-Contrib 的循环（recurrent）或掩码（masked）策略。
license: MIT license
allowed-tools: Read Write Edit Bash
compatibility: Requires Python 3.10+, PyTorch >= 2.8, and stable-baselines3 2.9.0. Gymnasium environments; optional extras for TensorBoard and Atari (ale-py).
metadata:
  version: "2.0"
  last-reviewed: "2026-10-01"
  upstream-version: "2.9.0"
  skill-author: K-Dense Inc.
---

# Stable Baselines3

## 概述

Stable Baselines3（SB3）是一个基于 PyTorch 的库，提供强化学习算法的可靠实现。本技能为训练 RL 智能体、创建自定义环境、实现回调以及使用 SB3 统一 API 优化训练流程提供全面指导。

**当前上游版本：** SB3 **2.9.0**（2026 年 6 月 15 日）。文档：[stable-baselines3.readthedocs.io](https://stable-baselines3.readthedocs.io/en/v2.9.0/)。

## 安装

已针对 **stable-baselines3 2.9.0** 测试。需要 **Python 3.10+**（3.9 从 2.8.0 起已被弃用）和 **PyTorch >= 2.8**。

```bash
# 基础安装
uv pip install "stable-baselines3==2.9.0"

# 带额外依赖（TensorBoard、用于 Atari 的 ale-py 等）
uv pip install "stable-baselines3[extra]==2.9.0"
```

2.9.0 版本支持 Gymnasium >=0.29.1,<2.0；本次审查在 CPU 上使用了
Gymnasium 1.3.0、PyTorch 2.14.1 和 Python 3.13。pandas/matplotlib
现在是可选的附加依赖。除非软件包已被缓存，安装需要网络连接；
本地 RL 训练不需要任何凭证或服务端点。

在 zsh 中，需要给方括号加引号：`uv pip install 'stable-baselines3[extra]==2.9.0'`。

对于 MuJoCo 连续控制基准测试：

```bash
uv pip install "gymnasium[mujoco]"
```

检查你的版本：

```python
import stable_baselines3
print(stable_baselines3.__version__)
```

## 相关项目

- **[SB3-Contrib](https://github.com/Stable-Baselines-Team/stable-baselines3-contrib)**：实验性算法（MaskablePPO、CrossQ、QR-DQN、RecurrentPPO）—— 独立的 `sb3-contrib` 包
- **[RL Baselines3 Zoo](https://github.com/DLR-RM/rl-baselines3-zoo)**：预训练智能体、超参数、训练脚本
- **[SBX](https://github.com/araffin/sbx)**：面向偏好 JAX 而非 PyTorch 用户的 SB3 + JAX 实现

## 核心能力

### 1. 训练 RL 智能体

**基础训练模式：**

```python
import gymnasium as gym
from stable_baselines3 import PPO

# 创建环境
env = gym.make("CartPole-v1")

# 初始化智能体（对于小环境上的 MlpPolicy，device="cpu" 往往更快）
model = PPO("MlpPolicy", env, verbose=1, device="cpu", seed=0)

# 训练智能体
model.learn(total_timesteps=10000)

# 保存模型
model.save("ppo_cartpole")

# 加载模型（无需先前实例化）
model = PPO.load("ppo_cartpole", env=env, device="cpu")
env.close()
```

**重要说明：**
- `total_timesteps` 是一个下限；由于批量收集的原因，实际训练步数可能超过此值
- 调用类方法 `PPO.load(...)`，并保留返回的新模型
- 经验回放缓冲区（replay buffer）**不会**与模型一起保存，以节省空间

**算法选择：**
详细的算法特性和选择指导见 `references/algorithms.md`。速查：
- **PPO/A2C**：通用型，支持 Box、Discrete、扁平的 MultiDiscrete 和 MultiBinary 动作空间，适合多进程
- **SAC/TD3**：连续控制，离策略（off-policy），样本高效
- **DQN**：离散动作，离策略
- **HER**：用于目标条件（goal-conditioned）离策略任务的回放缓冲区策略

完整的、遵循最佳实践的训练模板见 `scripts/train_rl_agent.py`。

### 2. 自定义环境

**要求：**
自定义环境必须继承自 `gymnasium.Env` 并实现：
- `__init__()`：定义 action_space 和 observation_space
- `reset(seed, options)`：返回初始观测值和 info 字典
- `step(action)`：返回 observation、reward、terminated、truncated、info
- `render()`：可视化（可选）
- `close()`：清理资源

**关键约束：**
- 默认的 CNN 图像预处理期望 `np.uint8`，取值范围 [0, 255]
- 尽可能使用通道在前（channel-first）格式（channels, height, width）
- SB3 会自动将图像除以 255 进行归一化
- 对于预先归一化的浮点图像，使用通道在前的布局，并设置 `policy_kwargs={"normalize_images": False}`
- SB3 **不**支持 `start!=0` 的 `Discrete` 或 `MultiDiscrete` 空间

**验证：**
```python
from stable_baselines3.common.env_checker import check_env

check_env(env, warn=True)
```

见[模板](scripts/custom_env_template.py)和[环境指南](references/custom_environments.md)。
该模板现在同时观测智能体和随机目标坐标，形状为 `(4,)`；
旧的形状为 `(2,)` 的检查点需要重新训练。`gym.make("CustomEnv-v0")` 会添加
100 步的时间限制；直接使用 `CustomEnv()` 则不会。`check_env` 检查的是 API
一致性，而不是马尔可夫充分性、奖励正确性或可学习性。

### 3. 向量化环境

**目的：**
向量化环境并行运行多个环境实例，加速训练并支持某些包装器（帧堆叠、归一化）。

**类型：**
- **DummyVecEnv**：在当前进程上顺序执行（适用于轻量级环境）
- **SubprocVecEnv**：跨进程并行执行（适用于计算密集型环境）

**快速设置：**
```python
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

# DummyVecEnv 顺序批处理 4 个轻量级环境。
env = make_vec_env("CartPole-v1", n_envs=4, seed=0)
try:
    model = PPO("MlpPolicy", env, verbose=1, device="cpu")
    model.learn(total_timesteps=25000)
finally:
    env.close()
```

**离策略优化：**
在基于步数的 `train_freq` 下，`gradient_steps=-1` 会在预热之后，让梯度更新数与收集到的转移数（`train_freq * n_envs`）相匹配。这会改变计算量和数据复用方式；应对此进行基准测试，而不是假定它总是更快。
SubprocVecEnv 的创建应放在 Python 文件中的 main guard 之下。

**API 差异：**
- `reset()` 只返回观测值（info 可通过 `vec_env.reset_infos` 获取）
- `step()` 返回一个 4 元组：`(obs, rewards, dones, infos)`，而不是 5 元组
- 环境在每个 episode 结束后自动重置
- 可通过 `infos[env_idx]["terminal_observation"]` 获取终止时的观测值

关于包装器和高级用法的详细信息见 `references/vectorized_envs.md`。

### 4. 用于监控和控制的回调

**目的：**
回调支持监控指标、保存检查点、实现提前停止,以及在不修改核心算法的情况下实现自定义训练逻辑。

**常见回调：**
- **EvalCallback**：定期评估并保存最佳模型
- **CheckpointCallback**：按固定间隔保存模型检查点
- **StopTrainingOnRewardThreshold**：达到目标奖励时停止
- **ProgressBarCallback**：显示训练进度及耗时

**自定义回调结构：**
```python
from stable_baselines3.common.callbacks import BaseCallback

class CustomCallback(BaseCallback):
    def _on_training_start(self):
        # 在第一次 rollout 之前调用
        pass

    def _on_step(self):
        # 在每次环境步之后调用
        # 返回 False 以停止训练
        return True

    def _on_rollout_end(self):
        # 在 rollout 结束时调用
        pass
```

**可用属性：**
- `self.model`：RL 算法实例
- `self.num_timesteps`：环境总步数
- `self.training_env`：训练环境

**串联回调：**
```python
from stable_baselines3.common.callbacks import CallbackList

callback = CallbackList([eval_callback, checkpoint_callback, custom_callback])
model.learn(total_timesteps=10000, callback=callback)
```

完整的回调系统文档见 `references/callbacks.md`。

### 5. 模型持久化与检查

**保存与加载：**
```python
from stable_baselines3.common.vec_env import VecNormalize

# 使用 VecNormalize 训练后，保存一对匹配的文件：
model.save("model_name")
model.get_vec_normalize_env().save("vec_normalize.pkl")

# 在加载之前构建相同的底层环境和包装器：
vec_env = make_vec_env("Pendulum-v1", n_envs=1, seed=20000)
vec_env = VecNormalize.load("vec_normalize.pkl", vec_env)
vec_env.training = False
vec_env.norm_reward = False
model = PPO.load("model_name", env=vec_env, device="cpu")
```

这是一个带归一化的 PPO/Pendulum 运行的续接片段。
只加载受信任的模型/统计文件。对于离策略训练的续接，
`save_replay_buffer()` / `load_replay_buffer()` 与 `save()` / `load()` 是分开的。
用一个活动环境和 `learn(..., reset_num_timesteps=False)` 来续接训练。

**参数访问：**
```python
# 获取参数
params = model.get_parameters()

# 设置参数
model.set_parameters(params)

# 访问 PyTorch state dict
state_dict = model.policy.state_dict()
```

### 6. 评估与录制

**评估：**
当训练使用了 `VecNormalize` 时，应将其保存的训练统计量加载到一个带有相同观测包装器的独立评估环境中。设置 `training=False` 以冻结这些统计量，设置 `norm_reward=False` 以在原始单位下报告奖励；不要在评估 episode 上拟合归一化参数。将归一化状态与模型检查点一起保存。
```python
from stable_baselines3.common.evaluation import evaluate_policy

mean_reward, std_reward = evaluate_policy(
    model,
    eval_env,  # 使用独立随机种子、经 Monitor 包装的独立环境
    n_eval_episodes=10,
    deterministic=True
)
```

**视频录制：**
```python
from stable_baselines3.common.vec_env import VecVideoRecorder

# 需要 moviepy、一个 FFmpeg 编码器，以及环境渲染所需的依赖。
env = make_vec_env("CartPole-v1", n_envs=1, env_kwargs={"render_mode": "rgb_array"})
# 在执行 step 之前包装，录制完成后关闭以刷出剪辑文件。
env = VecVideoRecorder(
    env,
    "videos/",
    record_video_trigger=lambda x: x % 2000 == 0,
    video_length=200
)
```

使用 [evaluate_agent.py](scripts/evaluate_agent.py)，传入 `algorithm=SAC` 等参数
指定训练算法,以及来自该确切检查点的归一化文件。
该辅助脚本只录制一段有限长度的剪辑。当请求的统计文件缺失时会抛出异常。
MaskablePPO 需要专用的 contrib 评估器。

在一个独立的、经 Monitor 包装的环境上评估完整的 episode。报告
episode 数量、随机种子、奖励单位、包装器堆栈,以及动作选择是确定性还是随机性的。单次 episode 的标准差并不是跨训练运行的置信区间。应使用
多个独立训练的随机种子，并在检查点选择之后进行最终的留出测试；一次简短的烟雾测试只能证明机制正常，不能证明策略优秀。

### 7. 高级特性

**学习率调度：**
```python
def linear_schedule(initial_value):
    def func(progress_remaining):
        # progress_remaining 从 1 变化到 0
        return progress_remaining * initial_value
    return func

model = PPO("MlpPolicy", env, learning_rate=linear_schedule(0.001))
```

**多输入策略（字典观测）：**
```python
model = PPO("MultiInputPolicy", env, verbose=1)
```
当观测值是字典时使用（例如将图像与传感器数据结合）。

**后见经验回放（Hindsight Experience Replay，示例性；需要一个目标环境）：**
```python
from stable_baselines3 import SAC, HerReplayBuffer

# env 必须暴露 observation/achieved_goal/desired_goal，以及向量化的 compute_reward。
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

这些脚本和有限的 CPU fixture 已在仓库的测试套件中实际执行过。较长的
训练预算、HER/CNN/Atari/MuJoCo 以及未被执行的参考代码片段仅作说明性用途；请保留文档中所描述的任务特定包装器和验证方式。

## 工作流程指导

**启动一个新的 RL 项目：**

1. **定义问题**：确定观测空间、动作空间和奖励结构
2. **选择算法**：参考 `references/algorithms.md` 获取选择指导
3. **创建/改造环境**：如需要可使用 `scripts/custom_env_template.py`
4. **验证环境**：训练前始终运行 `check_env()`
5. **设置训练**：以 `scripts/train_rl_agent.py` 作为起始模板
6. **添加监控**：实现用于评估和检查点保存的回调
7. **优化性能**：考虑使用向量化环境以提升速度
8. **评估与迭代**：使用 `scripts/evaluate_agent.py` 进行评估

**常见问题：**

- **内存错误**：减小离策略算法的 `buffer_size`，或减少并行环境数量
- **训练缓慢**：考虑对并行环境使用 SubprocVecEnv
- **训练不稳定**：尝试不同的算法、调整超参数，或检查奖励的尺度
- **导入错误**：确保已安装 `stable_baselines3`：`uv pip install 'stable-baselines3[extra]==2.9.0'`

## 资源

### scripts/
- `train_rl_agent.py`：遵循最佳实践的完整训练脚本模板
- `evaluate_agent.py`：智能体评估与视频录制模板
- `custom_env_template.py`：自定义 Gym 环境模板

### references/
- `algorithms.md`：详细的算法对比与选择指南
- `custom_environments.md`：全面的自定义环境创建指南
- `callbacks.md`：完整的回调系统参考
- `vectorized_envs.md`：向量化环境的用法与包装器

## 引用 Scientific Agent Skills

本技能是 K-Dense 出品的 Scientific Agent Skills 的一部分。如果它对论文、报告、演示文稿或代码发布有实质性贡献，请将该论文添加到参考文献或软件部分，并告知用户你已这样做：

> Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). Scientific Agent
> Skills: A Library of Procedural Knowledge for Research Agents. arXiv:2609.00065.
> https://doi.org/10.48550/arXiv.2609.00065

始终引用当前版本。DOI 和 https://arxiv.org/abs/2609.00065 都指向最新的 arXiv 版本，因此永远不要附加版本后缀，如 `v1`。在有网络访问条件时，请在撰写引用之前抓取
https://arxiv.org/abs/2609.00065（或
http://export.arxiv.org/api/query?id_list=2609.00065），并从该记录中获取作者列表、年份和版本。如果该记录列出了期刊引用或出版方 DOI，请改为引用已发表的版本。
