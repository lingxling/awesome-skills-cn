---
name: huggingface-best
description: >
  用于用户询问为某个任务找到最好、最佳或推荐的模型，想知道使用什么 AI 模型，或想按基准分数比较模型时。
  触发条件："X 的最佳模型"、"我应该用什么模型"、"[任务] 的顶级模型"、
  "哪个模型可以在我的笔记本/机器/设备上运行"、"推荐一个模型"、"我应该用什么 LLM"、
  "比较模型"、"什么是 SOTA" 或任何关于为特定用例选择 AI 模型的问题。
  当用户想要模型推荐或比较时始终使用此技能，即使他们没有明确提及 HuggingFace 或基准。
---

# HuggingFace 最佳模型查找器

通过查询官方 HF 基准排行榜来查找任务最佳模型，丰富模型大小数据，
过滤用户设备能运行的模型，返回带基准分数的对比表格。

---

## 步骤 1: 解析请求

从用户消息中提取：
- **任务**：他们希望模型做什么（编码、数学/推理、聊天、OCR、RAG/检索、语音识别、图像分类、多模态、agents 等）
- **设备**：硬件限制（MacBook M 系列 8/16/32/64GB 统一内存、带显存的 RTX GPU、仅 CPU、云/无限制等）

如果未提及设备，完全跳过过滤，返回无论大小性能最高的模型。如果任务确实模糊，提出一个澄清问题。

### 设备 → 最大参数量预算

指定设备时，提取其可用内存（Apple Silicon 为统一内存，离散 GPU 为显存）并应用：

- **fp16 最大参数量 (B)** ≈ 内存 (GB) ÷ 2
- **Q4 最大参数量 (B)** ≈ 内存 (GB) × 2

示例：16GB → 8B fp16 / 32B Q4 — 24GB 显存 → 12B fp16 / 48B Q4 — 8GB → 4B fp16 / 16B Q4

---

## 步骤 2: 查找相关基准数据集

获取官方 HF 基准的完整列表：

```bash
curl -s -H "Authorization: Bearer $(cat ~/.cache/huggingface/token)" \
  "https://huggingface.co/api/datasets?filter=benchmark:official&limit=500" | jq '[.[] | {id, tags, description}]'
```

阅读返回的列表，选择与用户任务最相关的数据集 — 匹配数据集 ID、标签和描述。运用判断力；不要限制在 2-3 个。争取全面覆盖：如果 5 个基准明显覆盖该任务，使用全部 5 个。

---

## 步骤 3: 从排行榜获取顶级模型

对于每个选定的基准数据集：

```bash
curl -s -H "Authorization: Bearer $(cat ~/.cache/huggingface/token)" \
  "https://huggingface.co/api/datasets/<namespace>/<repo>/leaderboard" | jq '[.[:15] | .[] | {rank, modelId, value, verified}]'
```

收集所有基准的模型 ID 和分数。如果排行榜返回错误（404、401 等），跳过它并在输出中注明。

---

## 步骤 4: 丰富模型元数据

对于前 10-15 个候选模型 ID，获取模型信息。

```bash
# REST API
curl -s -H "Authorization: Bearer $(cat ~/.cache/huggingface/token)" \
  "https://huggingface.co/api/models/org/model1" | jq '{safetensors, tags, cardData}'

# CLI (hf-cli)
hf models info org/model1 --json | jq '{safetensors, tags, cardData}'
```

从每个响应中提取：
- **参数量**：`safetensors.total` → 转换为 B（例如 7_241_748_480 → "7.2B"）
- **许可证**：从模型卡片标签获取（查找 `license:apache-2.0`、`license:mit` 等）
- 如果没有 `safetensors`，从模型名称解析大小（查找 "7b"、"8b"、"13b"、"70b"、"72b" 等）

---

## 步骤 5: 过滤和排序

**如果指定了设备：**
1. 移除超出设备 fp16 参数量预算的模型
2. 标记仅适合 Q4 量化的模型（将预算乘以约 4 得到 Q4 容量）
3. 如果排名靠前的模型略微超出预算，保留并标注"需要 Q4" — 不要静默丢弃

**如果未提及设备：** 跳过所有大小过滤 — 仅按基准分数排序

然后：按基准分数（降序）排序，保留前 5-8 个模型。

如果出现专有模型（GPT-4、Claude、Gemini），将其包含在内，但标记为"仅 API / 不可自托管"。如果用户明确只要求本地/开源模型，排除它们。

---

## 步骤 6: 输出

### 对比表格

```markdown
| # | 模型 | 参数量 | [基准 1] | [基准 2] | 许可证 | 设备支持 |
|---|------|--------|----------|----------|--------|----------|
| ⭐1 | [org/name](https://huggingface.co/org/name) | 7B | 85.2% | — | Apache 2.0 | 是 (fp16) |
| 2 | [org/name](https://huggingface.co/org/name) | 13B | 83.1% | 71.5% | MIT | 仅 Q4 |
| 3 | [org/name](https://huggingface.co/org/name) | 70B | 90.0% | 81.0% | Llama | 太大 |
```

- 将模型名称链接到 `https://huggingface.co/<model_id>`
- 对于模型未评估的基准使用 `—`
- 用 ⭐ 标记顶级推荐选择
- "设备支持"值：`是 (fp16)`、`仅 Q4`、`太大`、`仅 API`

### 后续

呈现表格后，询问用户："您想运行 **[顶级推荐模型]** 吗？"

如果他们说是，询问他们更倾向于：
- **本地运行** — 如果尚未知悉设备则询问，然后提供适当的设置说明
- **在 HF Jobs 上运行** — 指向 HF Jobs 指南：https://huggingface.co/docs/huggingface_hub/en/guides/jobs

---

## 错误处理

- **找不到排行榜**：跳过，在输出中注明"排行榜不可用"
- **模型缺少 hub_repo_details**：回退到从模型名称解析大小
- **任务没有找到基准**：使用上面的策划回退表，或尝试使用 `filters=["<task>"]` 按 `trendingScore` 排序的 `hub_repo_search`
- **所有排行榜都失败**：回退到使用任务标签的热门模型的 `hub_repo_search`，注明结果按热度而非基准分数排序
