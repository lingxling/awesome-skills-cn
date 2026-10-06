---
name: trl-training
description: 使用 TRL（Transformers Reinforcement Learning）对 LLM 进行后训练——SFT、DPO、GRPO、KTO 以及奖励模型训练。在使用 TRL Python API 或 trl CLI 编写或调试训练代码时使用。
license: Apache-2.0
metadata:
  author: huggingface
  documentation: https://huggingface.co/docs/trl
---

# TRL

每种方法都由一个 `*Trainer` 类与一个 `*Config` 数据类配对组成。Config 继承自 `transformers.TrainingArguments`，因此其所有参数都可在任何 trainer 配置中使用。

| Trainer | 数据集类型 |
|---|---|
| `SFTTrainer` | 语言建模或提示-补全（prompt-completion） |
| `DPOTrainer` | 偏好数据（chosen/rejected 对） |
| `GRPOTrainer` | 仅提示 + 奖励函数 |
| `DistillationTrainer` | 仅提示 + 教师模型（在线策略蒸馏，on-policy distillation） |
| `KTOTrainer` | 非成对偏好数据（每个样本一个布尔标签） |
| `RewardTrainer` | 偏好数据（chosen/rejected 对）；训练的是标量奖励模型，而非策略 |

更多 trainer（OnlineDPO、ORPO、CPO、GKD……）位于 `trl.experimental` 中，其 API 尚不稳定：https://huggingface.co/docs/trl/experimental_overview

```python
from datasets import load_dataset
from trl import SFTConfig, SFTTrainer

trainer = SFTTrainer(
    model="Qwen/Qwen2.5-0.5B",  # 模型 ID 或 PreTrainedModel 实例
    args=SFTConfig(output_dir="Qwen2.5-0.5B-SFT"),
    train_dataset=load_dataset("trl-lib/Capybara", split="train"),
)
trainer.train()
```

将 `model` 以字符串形式传入，并通过 `model_init_kwargs` 传递加载参数（例如 `{"dtype": "bfloat16", "attn_implementation": "kernels-community/flash-attn2"}`），而不要自己调用 `from_pretrained`。tokenizer/processor 会从模型中自动推断；仅当二者不同时才传入 `processing_class`。若使用 LoRA，请传入 `peft_config=LoraConfig(...)`。

## 数据集格式

对话格式：`{"messages": [{"role": ..., "content": ...}]}`（语言建模）或 `{"prompt": [...], "completion": [...]}`。聊天模板会被自动应用——切勿自行应用。允许存在额外列；GRPO 会将其转发给奖励函数。参考：https://huggingface.co/docs/trl/dataset_formats

## SFT：关键字段

```python
SFTConfig(
    max_length=1024,        # 截断长度；None 表示禁用截断
    packing=True,           # 将序列打包为 max_length 大小的块：填充 token 更少，吞吐量更高
    padding_free=True,      # 展平批次，不做填充；需要 FlashAttention；packing 时隐式启用
    use_liger_kernel=True,  # 融合的 Liger 内核，降低峰值显存
    assistant_only_loss=True,  # 仅在助手轮次上计算损失（对话数据集）
)
```

## GRPO：在线强化学习

```python
def reward_len(completions, **kwargs):
    return [-abs(20 - len(c[0]["content"])) for c in completions]

trainer = GRPOTrainer(
    model="Qwen/Qwen2.5-0.5B-Instruct",
    reward_funcs=reward_len,  # 或传入列表；各奖励会被求和
    args=GRPOConfig(output_dir="Qwen2.5-0.5B-GRPO", max_completion_length=512),
    train_dataset=load_dataset("trl-lib/DeepMath-103K", split="train"),
)
```

奖励函数以关键字参数 `prompts`、`completions`、`completion_ids`、`trainer_state` 以及数据集的每个额外列被调用——对于不需要的参数，请用 `**kwargs` 接收。返回 `list[float]`，每个补全对应一个奖励。对于对话数据，`completions` 是消息列表的列表，而不是字符串。

生成批次大小为 `per_device_train_batch_size × num_processes × steps_per_generation`（或直接设置 `generation_batch_size`），且必须能被 `num_generations`（默认 8）整除。生成通常是瓶颈——可通过 `use_vllm=True` 启用 vLLM：`vllm_mode="colocate"` 与训练共享 GPU（用 `vllm_gpu_memory_utilization` 控制占用）；`vllm_mode="server"` 则使用单独的 `trl vllm-serve --model <model_id>`。

`AsyncGRPOTrainer`（`trl.experimental.async_grpo`）实现了相同的算法，但将生成与训练解耦：后台 worker 从 vLLM 服务器流式获取补全，同时训练循环消费这些补全，从而使二者重叠进行，而不是交替执行。

## CLI

命令行标志与配置字段一一对应：`trl sft --model_name_or_path Qwen/Qwen2.5-0.5B --dataset_name trl-lib/Capybara`。可通过 `--config` 使用 YAML；通过 `--accelerate_config zero3` 使用分布式预设（Python 脚本：`accelerate launch train.py`）。
