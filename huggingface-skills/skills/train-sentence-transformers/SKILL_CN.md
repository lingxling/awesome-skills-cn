---
name: train-sentence-transformers
description: 训练或微调 sentence-transformers 模型，涵盖 `SentenceTransformer`（双编码器；稠密或静态嵌入模型；用于检索、相似度、聚类、分类、复述挖掘、去重、多模态）、`CrossEncoder`（重排序器；两阶段检索/成对分类的成对打分）和 `SparseEncoder`（SPLADE，稀疏嵌入模型；用于学习稀疏检索）。涵盖损失函数选择、难负样本挖掘、评估器、蒸馏、LoRA、Matryoshka 和 Hugging Face Hub 发布。用于任何 sentence-transformers 训练任务。
---

# 训练 sentence-transformers 模型

**本 SKILL.md 是一个路由器，而非手册。** 它告诉你需要为你的任务加载哪些参考文档和示例脚本。实际内容——推荐的损失函数、评估器、训练脚本结构、模型选择、训练参数调节、故障排查——位于 `references/` 和 `scripts/` 中。

**不要仅根据本文件综合生成训练脚本。** 打开对应类型的生产模板（`scripts/train_<type>_example.py`）并将其复制为起点。这些模板包含关键脚手架（autocast 辅助函数、模型卡片类、日志静默列表、`force=True`、`seed`、TF32、版本兼容的导入、命名评估器的指标处理），之前的 agent 运行在自己拼凑代码时反复遗漏这些内容。

## 1. 识别模型类型

| 标签 | 类 | 功能 | 适用场景 |
|---|---|---|---|
| **[SentenceTransformer]** | `SentenceTransformer`（双编码器） | 将每个输入映射为固定维度的稠密向量 | 检索、相似度、聚类、分类、复述挖掘、去重 |
| **[CrossEncoder]** | `CrossEncoder`（重排序器） | 联合为 `(query, passage)` 对打分 | 两阶段检索（对双编码器的 top-100 结果重排序）、成对分类 |
| **[SparseEncoder]** | `SparseEncoder`（SPLADE） | 基于词表的稀疏向量 | 学习稀疏检索、倒排索引后端（Elasticsearch / OpenSearch / Lucene） |

请求模糊时的判断规则："embedding model" / "vector search" / "similarity" → **[SentenceTransformer]**。"rerank" / "ranker" / "two-stage" → **[CrossEncoder]**。"SPLADE" / "sparse" / "inverted index" → **[SparseEncoder]**。如果仍不清楚，请询问。

## 2. 必读内容

**在编写任何代码之前完整阅读以下内容。不要按自认为的相关性进行筛选。**

### 按类型 — 始终必需

**[SentenceTransformer]**
- `references/losses_sentence_transformer.md` — 损失函数到数据形状的映射；MNRL 家族的 `BatchSamplers.NO_DUPLICATES` 要求；`Cached*` 与 `gradient_checkpointing` 的不兼容性。
- `references/evaluators_sentence_transformer.md` — 评估器到任务的映射；`metric_for_best_model` 键的构造（命名 vs 未命名）；每个评估器的 `primary_metric` 值。
- `references/model_architectures.md` — 编码器 vs 解码器 vs 静态 vs Router 流水线；池化规则（mean / cls / lasttoken）；从头开始的 MLM 基模型的自动 mean pooling 行为。
- `scripts/train_sentence_transformer_example.py` — 生产模板；复制此文件作为起点。

**[CrossEncoder]**
- `references/losses_cross_encoder.md` — pointwise / pairwise / listwise / distillation；`pos_weight` 推导；非 BCE 损失必须设置 `activation_fn=Identity()`（否则会导致静默的评估排名崩溃）。
- `references/evaluators_cross_encoder.md` — `CrossEncoderRerankingEvaluator` 配方；命名评估器键格式 `eval_{name}_{primary_metric}`。
- `scripts/train_cross_encoder_example.py` — 生产模板；复制此文件作为起点。

**[SparseEncoder]**
- `references/losses_sparse_encoder.md` — `SpladeLoss` 包装器要求；FLOPS 正则化权重；活跃维度攀升行为的冒烟测试。
- `references/evaluators_sparse_encoder.md` — `SparseNanoBEIREvaluator`（仅限英文）和领域内替代方案；`eval_{name}_{primary_metric}` 键格式。
- `scripts/train_sparse_encoder_example.py` — 生产模板；复制此文件作为起点。

### 跨类型 — 始终必需（无论任务如何）

- `references/training_args.md` — `TrainingArguments` 参数、精度规则（加载 fp32 + autocast bf16/fp16；绝不使用 `torch_dtype=bfloat16`）、`warmup_steps`（float）vs 已弃用的 `warmup_ratio`、`save_steps` 必须是 `eval_steps` 的倍数才能使用 `load_best_model_at_end`、调度器、HPO、tracker、恢复、Hub 推送变体。
- `references/dataset_formats.md` — 列匹配规则（标签名自动检测；列顺序而非列名）；reshape 配方；难负样本挖掘选项。
- `references/base_model_selection.md` — 发现命令；每类型模型命名空间；ModernBERT 家族 `max_seq_length=8192` 陷阱；`datasets >= 4` 脚本加载器拒绝；非英文起始点快捷方式。
- `references/troubleshooting.md` — 按症状索引的故障处理方案。每次运行时浏览章节标题，即使是健康运行；"Metrics don't improve" 和 "Hub push fails" 条目涵盖经常出现的 bug，在发生前识别比事后调试更划算。

### 跨类型 — 适用时加载

- `references/hardware_guide.md` — VRAM 容量估算、多 GPU、FSDP / DeepSpeed、HF Jobs 类型。>24GB 模型、多 GPU 或 HF Jobs 运行时必需。
- `references/hf_jobs_execution.md` — 在 HF Jobs 上运行时必需。
- `references/prompts_and_instructions.md` — 使用 prompt-tuned 基模型（E5、BGE、GTE、Qwen3-Embedding、Instructor、Nomic 等）或添加 `query: ` / `passage: ` 风格前缀时必需。

### 变体脚本（任务匹配时打开）
- **[SentenceTransformer]** `scripts/train_sentence_transformer_<matryoshka|multi_dataset|with_lora|distillation|make_multilingual|static_embedding>_example.py`。
- **[CrossEncoder]** `scripts/train_cross_encoder_<distillation|listwise>_example.py`。
- **[SparseEncoder]** `scripts/train_sparse_encoder_distillation_example.py`。
- 难负样本挖掘 CLI — `scripts/mine_hard_negatives.py`。

## 3. 默认值

仅在用户另有说明时覆盖：
- **本地执行。** 仅当本地硬件无法容纳任务时才推荐使用 HF Jobs。
- **单次运行。** 完成后，如果用户会受益，则建议进行实验（弱/边际结果、"看看能推到多高" 的框架等）。迭代规则见 `references/training_args.md`（Experimentation 部分）。
- **运行结束时推送到公开 Hub，用 try-except 包裹。** 在 HF Jobs 上（临时环境）同时启用 trainer 内推送（`push_to_hub=True` + `hub_strategy="every_save"`）；详情见 `references/hf_jobs_execution.md`。

## 4. 生成的脚本必须满足的约束

这些是不可协商的契约。实现位于生产模板和参考文档中 — 不要重新发明。

- 在 `trainer.train()` **之前** 将预训练评估器分数捕获为 `baseline_eval`。
- 输出单行运行结束信息：`VERDICT: WIN|MARGINAL|REGRESSION | score=... | baseline=... | delta=...`。监控程序会抓取此行。
- 将 `httpx`、`httpcore`、`huggingface_hub`、`urllib3`、`filelock`、`fsspec` 静默为 WARNING（否则 HF 下载 URL 会淹没 agent 的上下文）。
- 将日志同时输出到 `logs/{RUN_NAME}.log`。
- 以 `try/except` 包裹的 `model.push_to_hub(...)` 结束。
- 任何长运行前进行冒烟测试（`max_steps=1` + 极小数据集切片）。生产模板展示了一种常见模式（`SMOKE_TEST` 环境变量）。
- **[CrossEncoder]** 包含 `EarlyStoppingCallback(patience>=3)` — CE 重排序器经常在训练中达到峰值后衰退。
- **[SparseEncoder]** 在 verdict 行中记录 `query_active_dims` / `corpus_active_dims`；高 nDCG 但稀疏性坍塌不是胜利。键会带名称前缀返回（例如 `..._query_active_dims`）；使用后缀匹配来提取它们 — 参见 SPARSE 生产模板中的确切模式。

## 5. 工作流程

1. 识别模型类型（§1）。如有歧义请询问。
2. 加载该类型的 §2 必读文件。
3. 打开 `scripts/train_<type>_example.py` 并将其复制为起点。
4. 将 `MODEL_NAME`、`DATASET_NAME`、`RUN_NAME`、损失函数和评估器替换为用户的任务。对照 `references/losses_<type>.md` 交叉检查损失/数据形状匹配；对照 `references/evaluators_<type>.md` 交叉检查 `metric_for_best_model` 键（命名评估器将键格式化为 `eval_{name}_{primary_metric}`）。
5. 冒烟测试（`max_steps=1`）。
6. 运行。
7. 运行后，追加到 `logs/experiments.md`，如果结果是弱/边际则建议迭代。

## 前置条件

```bash
pip install "sentence-transformers[train]>=5.0"        # 对于 [SentenceTransformer] 多模态，添加 [train,image] / [audio] / [video]
pip install trackio                                    # 可选 tracker；或 wandb / tensorboard / mlflow
hf auth login                                          # 或设置具有写入权限的 HF_TOKEN（用于 Hub 推送）
```

强烈推荐使用 GPU。CPU 仅适用于演示和 `[SentenceTransformer]` `StaticEmbedding`。
