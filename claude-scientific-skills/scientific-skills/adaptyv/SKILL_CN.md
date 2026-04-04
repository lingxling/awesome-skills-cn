---
name: adaptyv
author: "K-Dense, Inc."
description: "如何使用 Adaptyv Bio Foundry API 和 Python SDK 进行蛋白质实验设计、提交和结果检索。当用户提到 Adaptyv、Foundry API、蛋白质结合测定、蛋白质筛选实验、BLI/SPR 测定、热稳定性测定，或希望提交蛋白质序列进行实验表征时使用此技能。当代码导入 `adaptyv`、`adaptyv_sdk` 或 `FoundryClient`，或引用 `foundry-api-public.adaptyvbio.com` 时也会触发。"
---

# Adaptyv Bio Foundry API

Adaptyv Bio 是一个将蛋白质序列转化为实验数据的云实验室。用户通过 API 或 UI 提交氨基酸序列；Adaptyv 的自动化实验室运行测定（结合、热稳定性、表达、荧光）并在约 21 天内交付结果。

## 快速开始

**基础 URL：** `https://foundry-api-public.adaptyvbio.com/api/v1`

**认证：** 在 `Authorization` 头中使用 Bearer 令牌。令牌可从 [foundry.adaptyvbio.com](https://foundry.adaptyvbio.com/) 侧边栏获取。

编写代码时，始终从环境变量 `ADAPTYV_API_KEY` 或 `.env` 文件中读取 API 密钥 — 切勿硬编码令牌。首先检查项目根目录中是否存在 `.env` 文件；如果存在，使用 `python-dotenv` 等库加载它。

```bash
export FOUNDRY_API_TOKEN="abs0_..."
curl https://foundry-api-public.adaptyvbio.com/api/v1/targets?limit=3 \
  -H "Authorization: Bearer $FOUNDRY_API_TOKEN"
```

除 `GET /openapi.json` 外的所有请求都需要认证。将令牌存储在环境变量或 `.env` 文件中 — 切勿将它们提交到源代码控制。

## Python SDK

安装：`uv add adaptyv-sdk`（如果不存在 `pyproject.toml`，会回退到 `uv pip install adaptyv-sdk`）

**环境变量**（在 shell 或 `.env` 文件中设置）：
```bash
ADAPTYV_API_KEY=your_api_key
ADAPTYV_API_URL=https://foundry-api-public.adaptyvbio.com/api/v1
```

### 装饰器模式

```python
from adaptyv import lab

@lab.experiment(target="PD-L1", experiment_type="screening", method="bli")
def design_binders():
    return {"design_a": "MVKVGVNG...", "design_b": "MKVLVAG..."}

result = design_binders()
print(f"Experiment: {result.experiment_url}")
```

### 客户端模式

```python
from adaptyv import FoundryClient

client = FoundryClient(api_key="...", base_url="https://foundry-api-public.adaptyvbio.com/api/v1")

# 浏览靶点
targets = client.targets.list(search="EGFR", selfservice_only=True)

# 估算成本
iestimate = client.experiments.cost_estimate({
    "experiment_spec": {
        "experiment_type": "screening",
        "method": "bli",
        "target_id": "target-uuid",
        "sequences": {"seq1": "EVQLVESGGGLVQ..."},
        "n_replicates": 3
    }
})

# 创建并提交
exp = client.experiments.create({...})
client.experiments.submit(exp.experiment_id)

# 稍后：检索结果
results = client.experiments.get_results(exp.experiment_id)
```

## 实验类型

| 类型 | 方法 | 测量内容 | 需要靶点 |
|---|---|---|---|
| `affinity` | `bli` 或 `spr` | KD、kon、koff 动力学 | 是 |
| `screening` | `bli` 或 `spr` | 有/无结合 | 是 |
| `thermostability` | — | 熔解温度 (Tm) | 否 |
| `expression` | — | 表达产量 | 否 |
| `fluorescence` | — | 荧光强度 | 否 |

## 实验生命周期

```
Draft → WaitingForConfirmation → QuoteSent → WaitingForMaterials → InQueue → InProduction → DataAnalysis → InReview → Done
```

| 状态 | 谁操作 | 描述 |
|---|---|---|
| `Draft` | 您 | 可编辑，无成本承诺 |
| `WaitingForConfirmation` | Adaptyv | 审核中，正在准备报价 |
| `QuoteSent` | 您 | 审核并确认报价 |
| `WaitingForMaterials` | Adaptyv | 基因片段和靶点已订购 |
| `InQueue` | Adaptyv | 材料已到达，等待实验室处理 |
| `InProduction` | Adaptyv | 测定正在运行 |
| `DataAnalysis` | Adaptyv | 原始数据处理和质量控制 |
| `InReview` | Adaptyv | 最终验证 |
| `Done` | 您 | 结果可用 |
| `Canceled` | 任意一方 | 实验已取消 |

实验上的 `results_status` 字段跟踪：`none`、`partial` 或 `all`。

## 常见工作流程

### 1. 提交结合筛选（分步）

```python
# 1. 查找靶点
targets = client.targets.list(search="EGFR", selfservice_only=True)
target_id = targets.items[0].id

# 2. 预览成本
iestimate = client.experiments.cost_estimate({
    "experiment_spec": {
        "experiment_type": "screening",
        "method": "bli",
        "target_id": target_id,
        "sequences": {"seq1": "EVQLVESGGGLVQ...", "seq2": "MKVLVAG..."},
        "n_replicates": 3
    }
})

# 3. 创建实验（开始为 Draft 状态）
exp = client.experiments.create({
    "name": "EGFR binder screen batch 1",
    "experiment_spec": {
        "experiment_type": "screening",
        "method": "bli",
        "target_id": target_id,
        "sequences": {"seq1": "EVQLVESGGGLVQ...", "seq2": "MKVLVAG..."},
        "n_replicates": 3
    }
})

# 4. 提交审核
client.experiments.submit(exp.experiment_id)

# 5. 轮询或使用 webhook 直到 Done
# 6. 检索结果
results = client.experiments.get_results(exp.experiment_id)
```

### 2. 自动化管道（跳过 Draft + 自动接受报价）

```python
exp = client.experiments.create({
    "name": "Auto pipeline run",
    "experiment_spec": {...},
    "skip_draft": True,
    "auto_accept_quote": True,
    "webhook_url": "https://my-server.com/webhook"
})
# Webhook 在每次状态转换时触发；轮询或等待 Done
```

### 3. 使用 Webhook

创建实验时传递 `webhook_url`。Adaptyv 在每次状态转换时都会向该 URL 发送 POST 请求，包含实验 ID、先前状态和新状态。

## 序列

- 简单格式：`{"seq1": "EVQLVESGGGLVQPGGSLRLSCAAS"}`
- 丰富格式：`{"seq1": {"aa_string": "EVQLVESGGGLVQ...", "control": false, "metadata": {"type": "scfv"}}}`
- 多链：使用冒号分隔 — `"MVLS:EVQL"`
- 有效氨基酸：A、C、D、E、F、G、H、I、K、L、M、N、P、Q、R、S、T、V、W、Y（不区分大小写，存储为大写）
- 序列只能添加到 `Draft` 状态的实验中

## 过滤、排序和分页

所有列表端点都支持分页（`limit` 1-100，默认 50；`offset`）、搜索（名称字段的自由文本）和排序。

**过滤** 使用 s-expression 语法通过 `filter` 查询参数：
- 比较：`eq(field,value)`、`neq`、`gt`、`gte`、`lt`、`lte`、`contains(field,substring)`
- 范围/集合：`between(field,lo,hi)`、`in(field,v1,v2,...)`
- 逻辑：`and(expr1,expr2,...)`、`or(...)`、`not(expr)`
- 空值：`is_null(field)`、`is_not_null(field)`
- JSONB：`at(field,key)` — 例如，`eq(at(metadata,score),42)`
- 类型转换：`float()`、`int()`、`text()`、`timestamp()`、`date()`

**排序** 使用 `asc(field)` 或 `desc(field)`，逗号分隔（最多 8 个）：
```
sort=desc(created_at),asc(name)
```

**示例：** `filter=and(gte(created_at,2026-01-01),eq(status,done))`

## 错误处理

所有错误返回：
```json
{
  "error": "人类可读的描述",
  "request_id": "req_019462a4-b1c2-7def-8901-23456789abcd"
}
```
`request_id` 也在 `x-request-id` 响应头中 — 联系支持时请包含它。

## 令牌管理

令牌使用基于 Biscuit 的加密衰减。您可以通过 `POST /tokens/attenuate` 创建受限制的令牌，按组织、资源类型、操作（读取/创建/更新）和过期时间进行范围限定。撤销令牌（`POST /tokens/revoke`）会撤销它及其所有子令牌。

## 详细 API 参考

有关所有 32 个端点的完整列表以及请求/响应模式，请阅读 `references/api-endpoints.md`。