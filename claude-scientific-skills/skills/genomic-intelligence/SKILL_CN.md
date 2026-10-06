---
name: genomic-intelligence
description: "使用 Genomic Intelligence 托管的 Transformer DNA 语言模型，直接从 DNA 序列预测调控特征、基因结构和表达——无需本地 GPU 或模型权重。通过 REST API 和托管 MCP 服务器（免密钥公共演示）提供六项任务：启动子区域、剪接供体/受体位点、增强子活性、染色质状态、序列到表达（log TPM）以及从头基因注释，另有“先找基因再预测表达”的复合工作流。当用户拥有基因符号、基因组区域或 DNA/FASTA 序列并需要上述任何预测，或提及 Genomic Intelligence、genomicintelligence.ai、api.genomicintelligence.ai 或 mcp.genomicintelligence.ai 时使用。"
license: MIT
compatibility: Python 3.10+ with the `requests` library for the REST examples. Network access required. The REST `/v1` API needs a `GI_API_KEY` (a `gi_` bearer); the hosted MCP server at mcp.genomicintelligence.ai/mcp works keyless against a rate- and concurrency-limited public demo tier, key optional.
metadata:
  version: "1.4"
  last-reviewed: "2026-10-01"
  skill-author: Genomic Intelligence
  trigger-keywords: DNA sequence prediction, regulatory genomics, promoter prediction, splice site prediction, enhancer activity, chromatin state, gene expression prediction, sequence to expression, log TPM, gene annotation, transcript prediction, DNA language model, genomic intelligence, hosted inference, Ensembl sequence, FASTA prediction, cis-regulatory, TSS window, DeepSEA, DeepSTARR, BigBird splice, MCP genomics
  openclaw:
    primaryEnv: GI_API_KEY
    envVars:
    - name: GI_API_KEY
      required: false
      description: Optional gi_ bearer key for the REST /v1 API and higher MCP rate and concurrency limits. The hosted MCP demo runs keyless; request a key at contact@genomicintelligence.ai.
---

# Genomic Intelligence — DNA 序列模型

Genomic Intelligence（GI）在托管 GPU 上提供 Transformer DNA 语言模型，覆盖六项
序列分析任务。给它一个**基因符号**、一个**基因组区域**或一段 **DNA/FASTA 序列**，
它会返回结构化预测——启动子区域、剪接位点、增强子活性、染色质状态、表达量
（log TPM）以及从头基因注释。没有任何东西在本地运行：不需要模型权重、
不需要 GPU，也不需要庞大的 Python 软件栈。它只是托管的、带版本的推理 API
之上的一个轻量客户端。

**官方文档：** [docs.genomicintelligence.ai](https://docs.genomicintelligence.ai) ·
REST 契约见 [api.genomicintelligence.ai/v1/openapi.json](https://api.genomicintelligence.ai/v1/openapi.json) ·
托管 MCP 服务器位于 `https://mcp.genomicintelligence.ai/mcp`

## 何时使用此技能

当用户拥有 DNA 并需要模型预测时使用 GI：

- 在基因组区域中**查找启动子**（`promoter`）
- **预测剪接**供体/受体位点（`splice`）
- **为增强子活性打分**——发育型与管家型（`enhancer`）
- 跨数百条轨道**注释染色质状态**（`chromatin`）
- 根据序列 + 细胞类型上下文**预测表达量**，以 log(TPM+1) 表示（`expression`）
- 从头**注释基因/转录本**，无需参考（`annotation`）
- **找出区域中的基因并预测每个基因的表达量**（复合工作流）

不适用于局部比对、变异检测或文件 I/O——这些请使用本地工具
（BioPython、bcftools）。GI 用于**基于序列的模型推理**。

> 仅供研究与开发使用。不得用于临床或诊断决策。

## 调用 GI 的两种方式

### 托管 MCP 服务器（免密钥；在 MCP 宿主上首选）

GI 在 `https://mcp.genomicintelligence.ai/mcp`（Streamable HTTP）托管了一个 MCP
服务器。当你的智能体宿主支持 MCP 时，优先使用它：它可以**免密钥**访问一个
受速率和并发限制的公共演示层级，可选的 `gi_` bearer 密钥可提高这些限制。
它提供返回**序列句柄**（`sequence_ref`）的获取工具，以及接收该句柄的
`predict_*` 工具，从而让大型序列不进入上下文。参见下文的
[MCP 工作流](#mcp-workflow-handle-based)以及 `references/mcp.md`。

### REST API（通用）

使用 `requests` 对 `https://api.genomicintelligence.ai/v1` 发起普通 HTTP 请求。
REST 路径**需要** `GI_API_KEY`（一个 `gi_` bearer）。可在任何宿主、脚本中使用，
或在需要原始信封（envelope）时使用。参见[核心 REST 工作流](#core-rest-workflow)。

## 访问与认证

1. **托管 MCP 演示免密钥**——什么都不设置即可试用。
2. REST 预测和作业操作需要密钥，以 `Authorization: Bearer <key>` 发送。
   公共的 `GET /v1/tasks/{task}/models` 发现接口无需密钥，按来源 IP 限速；
   在申请访问之前可先查看模型窗口和边界。
   参见[当前认证契约](https://docs.genomicintelligence.ai/)。
   在 [contact@genomicintelligence.ai](mailto:contact@genomicintelligence.ai) 申请预测密钥。
3. **切勿硬编码密钥。** 从 `GI_API_KEY` 环境变量读取
   （或通过 `python-dotenv` 读取 `.env`）。切勿提交密钥。

```bash
export GI_API_KEY="gi_yourkeyhere"     # MCP 可选；REST 必需
export GI_BASE_URL="https://api.genomicintelligence.ai"   # 用于预发布环境时覆盖
```

密钥绑定到某个合作伙伴层级，带有并发和每分钟上限。`429` 表示你触及了上限——
退避后重试，或请 GI 提升你的层级。

## 六项任务

每项任务都是**独立发布的操作**，拥有自己的请求 schema、自己的最小长度以及自己的
封闭 `options` 对象——`POST
/v1/tasks/promoter/predict`、`/v1/tasks/splice/predict`、
`/v1/tasks/enhancer/predict`、`/v1/tasks/chromatin/predict`、
`/v1/tasks/annotation/predict`、`/v1/tasks/expression/predict`。每个路径都是
字面字符串，因此无需拼接构造，也不存在共享的 `PredictRequest` schema。请求体为
`{sequence, sequence_name?, model?,
options?}`，返回 `{data, meta}` 信封。各任务的差异如下：

| 任务 | 推荐模式 | 可接受长度 | `context_window_bp` | 说明 |
|---|---|---|---|---|
| `promoter` | 同步 | 300–500,000 bp | 2,000 bp | 滑动窗口启动子区域 |
| `splice` | 同步 | 100–500,000 bp | 15,000 bp | 供体/受体位点（长上下文 BigBird）；具有链特异性——请输入转录本方向的序列 |
| `enhancer` | 同步 | 50–500,000 bp | 249 bp | 发育型 + 管家型得分（DeepSTARR，*Drosophila*） |
| `chromatin` | 同步 | 200–500,000 bp | 1,000 bp | 数百条轨道（DeepSEA） |
| `expression` | 同步 | **9,198–500,000 bp** | 不适用（`trained_window_bp` 9,198） | log(TPM+1)；除非恰好为 9,198 bp，否则需要 `tss_index`，另需细胞类型 `description` |
| `annotation` | 异步 | 1,000–500,000 bp | 不适用 | 从头转录本；提交 + 轮询；超过 200,000 bp 的同步 JSON 请求返回 `413 sync_too_large` |

`推荐模式`是指导而非约束——每项任务都同时接受两种模式。省略 `Prefer` 可获得同步的 `200`；发送 `Prefer: respond-async` 则得到 `202` 并配合 `GET /v1/tasks/jobs/{job_id}`。唯一强制执行的限制按操作而定：凡是 `/v1/openapi.json` 在某个 `POST` 上发布了 `x-sync-limit-bp` 的，超过该长度的同步 JSON 请求即为 `413 sync_too_large`——在契约修订版 16 中，`annotation` 为 200,000 bp，复合工作流为 50,000 bp。请读取该字段，而不要死记这些数字。Annotation 的 BED/GFF3 输出在任何被接受的长度下都保持同步，可能超时；其余五项预测任务没有硬性同步上限。

**最小长度是准入控制，而非工作区间。** 高于下限但短于所选模型
`bio_spec.context_window_bp` 的请求会被*接受并打分*——针对一个被填充至上下文窗口
大小的窗口。增强子是典型例子：下限为 50 bp，但上下文窗口为 249 bp，因此
50–248 bp 的序列大部分是基于填充内容打分的。将你的长度与
`GET /v1/tasks/{task}/models` 返回的 `context_window_bp` 进行比较，即可知道模型是否
看到了真实序列。超过上下文长度的输入没有问题——扫描器每次步进一个预测窗口，
只填充最后一个不完整的窗口。

低于下限和超过 500,000 bp 上限**都返回 `422 validation_failed`**，
位于 `loc ["body","sequence"]`；超长*不是* `413`。所有长度都在去除空白字符后
计算，因此可以原样粘贴按行折叠的 FASTA 正文（但 `>` 标题行仍会无法通过字母表检查）。

`options` 按任务有类型定义且是**封闭的**（`additionalProperties: false`）——未知键
会导致硬性的 `422 validation_failed`，`type: "extra_forbidden"`，
绝不会被忽略：

| 任务 | `options` 键 |
|---|---|
| promoter | `threshold`（0–1，默认 0.5） |
| splice | `threshold`（0–1，默认 0.5），`site_types`（`["donor","acceptor"]` 的子集，默认两者都有） |
| enhancer | *（无）* |
| chromatin | `threshold`（0–1，默认 0.5） |
| annotation | `batch_size`（1–128，默认 8），`shift_coordinates`，`reverse_complement`（默认 true） |
| expression | `description`——**必需**，且是唯一的键 |

`Prefer: respond-async` 是在**全部六个**预测操作以及复合工作流上都声明了的请求头，
而不仅限于 `annotation`——参见[异步](#async-any-task-recommended-for-annotation)。

**省略 `model`，API 就会使用该任务的默认模型**——这是推荐的调用方式。
此处有意**不**记录默认模型 ID：默认值会变化，而已退役的 ID 会直接失败，因此切勿
硬编码。若要固定某个模型，或选择非人类模型（多项任务提供果蝇、酵母和拟南芥模型），
请在调用时通过 `GET /v1/tasks/{task}/models`（REST）或
`list_models`（MCP）发现 ID——并且**切勿自行编造**。各任务完整的输出结构见
`references/tasks.md`。

`expression` 是六项任务中最严格的：只有它的 schema 同时要求
`options` 和 `sequence`。它强制执行三条硬性规则——任何违规都是 `422`，
不会进行填充或截断，也没有任何可关闭的标志、请求头或查询参数：

- **它始终只对一个以 TSS 为中心的 9,198 bp 窗口打分**——
  `sequence[tss_index-4599 : tss_index+4599]`。端点本身接受
  **9,198–500,000 bp**；低于 9,198 bp 的任何输入都会被直接拒绝。
- **除非序列恰好为 9,198 bp，否则 `tss_index` 是必需的。** 它是 TSS 在
  **去除空白后**序列中的 0 起始偏移，范围为
  `4599 ≤ tss_index ≤ len(sequence) − 4599`。恰好为 9,198 bp 时默认为
  4,599，这也是此时唯一合法的值。因此你可以提交整个基因座（最多
  500 kb），由服务器切出窗口——但服务器**不会**为你寻找 TSS
  （那是复合工作流的工作），也**不会**进行反向互补：请提交基因正义链序列。
- **`options.description`**——细胞类型 / 实验检测字符串（例如 `"K562 cells"`）——
  是必需的，并且是 `expression` 在 `options` 中接受的**唯一**键。
  未知的顶层请求体字段同样会被拒绝。

> 注意：合法的 `tss_index` 范围很宽，因此一个仅仅是*错误*的偏移
> （按包含换行符的原始 FASTA 字符计数，或相对于基因座起点而非所提交片段计算）
> 并不会报错——它会针对错误的窗口返回一个看似可信的 `200`。请在响应中对
> `meta.task_specific_counts.scored_window` / `.tss_index` 进行断言。
> 提交的长度为 `meta.sequence_length`；打分宽度始终为
> 9,198，即 `scored_window[1] - scored_window[0]`。在修订版 16 中，
> `data.input` 仅包含 `sequence_name`、`description` 和 `tss_index`；
> 不包含提交的长度或打分窗口。
>
> 两种 `tss_index` 违规——“除非恰好 9,198 bp 否则必需”以及范围检查——都来自
> 整个模型级别的校验器，因此它们出现在请求体级别，而不是 `tss_index` 之下。
> 请匹配 `error.code == "validation_failed"`，消息仅用于显示。本技能中引用的任何
> `loc` 元组只是对该结构的示意，并不属于契约：它未在 schema 中发布，不得据此分支。

## 序列获取

你很少会从一条原始的 9,198 bp 字符串开始。请先获取序列：

- **从基因符号** → MCP `fetch_ensembl_sequence(gene=...)`；**从
  坐标** → `fetch_region(region=...)`。两者都会获取公共参考序列（无需密钥），使用内置坐标
  目录、缓存、UCSC 或 Ensembl；请保留返回的来源信息（provenance）。REST 用户可直接查询 Ensembl REST。（`find_genes` 是
  注释任务，而不是获取工具。）
- **用于 `expression`** → 使用以 TSS 为中心的获取方式，使窗口恰好为
  9,198 bp。MCP：`fetch_gene_for_expression`（会处理居中）。否则
  获取更宽的基因座，并将 TSS 作为 `tss_index` 传入，由服务器切出
  窗口——但该偏移要在去除空白后的核苷酸字符串上计算，而不是在文件字符上计算。
- **从本地 FASTA** → MCP `store_inline_sequence`，或在使用 REST 时自行读取文件。
  （`load_local_fasta` 仅存在于本地部署中，托管服务器上没有。）
- **演示序列** → MCP `load_demo_sequence(name=...)` 返回一个可直接使用的句柄，
  用于免密钥冒烟测试；`name` 为必需参数。

确切的 Ensembl 调用和表达窗口的计算方法见 `references/sequence-acquisition.md`。

## 核心 REST 工作流

以下传输示例是用模拟响应测试的，而非经过认证的真实推理。调用前请提供适合任务的
`seq`。比较预测结果时，请始终使用完全一致的表达上下文措辞。

```python
import os
import time
import requests

BASE = os.environ.get("GI_BASE_URL", "https://api.genomicintelligence.ai").rstrip("/")
HEADERS = {"Authorization": f"Bearer {os.environ['GI_API_KEY']}"}
TASKS = {"promoter", "splice", "enhancer", "chromatin", "annotation", "expression"}

def predict(task, sequence, sequence_name, model=None, options=None, tss_index=None):
    if task not in TASKS:
        raise ValueError("Unknown GI task")
    body = {"sequence": sequence, "sequence_name": sequence_name}
    if model is not None:
        body["model"] = model
    if options is not None:
        body["options"] = options
    if tss_index is not None:
        if task != "expression":
            raise ValueError("tss_index is expression-only")
        body["tss_index"] = tss_index
    r = requests.post(f"{BASE}/v1/tasks/{task}/predict", headers=HEADERS,
                      json=body, timeout=(10, 300))
    r.raise_for_status()
    if r.status_code != 200:
        raise RuntimeError(f"Unexpected prediction status {r.status_code}")
    return r.json()

# 在获取并检查了合适的启动子序列之后：
# out = predict("promoter", seq, "TP53_region")
# print(out["meta"]["task_specific_counts"]["regions_found"])

# 一个经过验证的基因正义链表达窗口，或已知 TSS 的更长基因座：
# out = predict("expression", locus_seq, "HBB", tss_index=tss_offset,
#               options={"description": "polyA plus RNA-seq; Homo sapiens K562"})
# assert out["meta"]["sequence_length"] == len("".join(locus_seq.split()))
# assert out["meta"]["task_specific_counts"]["scored_window"] == [tss_offset-4599, tss_offset+4599]
# print(out["data"]["prediction"]["expression_log_tpm"])
```

`data.summary` 仅用于显示：其键可能在没有契约修订的情况下变化。
计算时请使用 `data` 和 `meta.task_specific_counts` 中声明的字段。
超时或代理错误可能带有非 JSON 的响应体；这并不能证明推理从未运行。
请保留请求 ID，避免盲目重新提交 POST。

### 异步（任何任务；推荐用于 annotation）

在六项任务中的任意一项或复合工作流上发送 `Prefer: respond-async`。`202`
的内容为 `{data: {job_id, status: "accepted", links}, meta}`。`Content-Location` 和
`X-Job-Id` 标识同一个作业。异步仅支持 JSON；文本格式加异步会返回
`400`。轮询前请保存作业 ID。下面这个有界轮询示例会将
HTTP 失败（包括 `429` 和 `410`）抛给调用方处理：

```python
def submit_annotation(sequence, sequence_name):
    r = requests.post(f"{BASE}/v1/tasks/annotation/predict",
                      headers={**HEADERS, "Prefer": "respond-async"},
                      json={"sequence": sequence, "sequence_name": sequence_name},
                      timeout=(10, 30))
    r.raise_for_status()
    if r.status_code != 202:
        raise RuntimeError(f"Unexpected submission status {r.status_code}")
    return r.json()["data"]["job_id"]

def wait_for_job(job_id, max_polls=120):
    if max_polls < 1:
        raise ValueError("max_polls must be positive")
    for attempt in range(max_polls):
        r = requests.get(f"{BASE}/v1/tasks/jobs/{job_id}", headers=HEADERS,
                         timeout=(10, 30))
        r.raise_for_status()  # 失败的作业 -> 返回其底层的 4xx/5xx，而不是 200
        if r.status_code == 200:
            return r.json()
        if r.status_code != 202:
            raise RuntimeError(f"Unexpected polling status {r.status_code}")
        if attempt + 1 < max_polls:
            time.sleep(5)
    raise TimeoutError(f"Polling stopped; resume this job rather than resubmit: {job_id}")

# job_id = submit_annotation(seq, "TP53_region")  # 持久化保存此 ID
# result = wait_for_job(job_id)
# assert result["data"]["task"] == "annotation"
# transcripts = result["data"]["transcripts"]
```

`200` 表示完成；`202` 包含 `data.status` 和 `data.progress`。
未知/不属于你的作业返回 `404`；过期作业返回 `410 job_expired`。
文档说明结果自最后一次活动起保留 24 小时；请在本地保存结果。
作业列表是近期的有界列表，而不是可分页的归档。

## MCP 工作流（基于句柄）

在 MCP 宿主上，先获取句柄，再针对句柄进行预测——序列不会进入上下文：

```
# 1. 获取序列句柄（每个都返回 data.ref，作为 sequence_ref 传入）：
load_demo_sequence(name="promoter_tp53")  # 免密钥冒烟测试；name 为必需参数
fetch_ensembl_sequence(gene="TP53", flank_bp=5000)  # 包含调控上下文
fetch_region(region="chr11:5,225,000-5,235,000")   # 坐标 -> 句柄
fetch_gene_for_expression(gene="HBB")     # 用于表达预测的以 TSS 为中心的 9,198 bp 句柄

# 2. 针对句柄进行预测：
predict_promoter(sequence_ref=<ref>)
predict_expression(sequence_ref=<ref>, description="K562 cells")
predict_splice(sequence_ref=<ref>)        # + predict_enhancer / predict_chromatin

# 3. MCP 上的注释是 `find_genes`（没有 predict_annotation）。
#    它接收句柄而非区域，并在内部异步运行：
find_genes(sequence_ref=<ref>)            # wait=True（默认）返回结果
find_genes(sequence_ref=<ref>, wait=False)  # 仅限自有密钥 -> job_id；轮询 get_job(job_id)

# 获取工具返回 data.ref；将该值用作 sequence_ref。
# 用 list_models(task) 发现模型；参考上下文位于
# gi://models、gi://docs/tasks 和 gi://account 这些 MCP 资源中。
```

共享演示禁用了 `get_job`、`list_jobs` 和分离式的 `wait=False`。
在演示环境中请保持 `wait=True`；等待超时是一个错误，而不是可恢复的作业句柄。
资源、结果信封及其生命周期参见 [MCP 详情](references/mcp.md)。

## 复合工作流：先找基因，再预测表达

要回答“这个区域里有哪些基因、它们的表达情况如何？”，请使用复合工作流：

- **MCP：** `find_genes_and_predict_expression(sequence_ref=..., description=...)`
  ——接收**句柄而非区域**（先用 `fetch_region` 获取一个句柄）；
  `description` 为必需。它在序列中查找基因，并为每个基因返回
  表达预测。
- **REST：** 一次调用——`POST /v1/workflows/find-genes-and-predict-expression`，
  请求体 `{sequence, options}`，其中 `sequence` 为 1,000–500,000 bp，且
  `options.description`（细胞类型 / 实验检测）为必需；缺失或为空的
  description 返回 `422 validation_failed`。它先进行注释，然后以每个发现基因的 TSS
  为中心取 9,198 bp 窗口（在边缘处用 `N` 填充最多半个窗口，
  而不是丢弃边缘基因），并为每个基因返回预测。
  `meta.task_specific_counts` = `{genes_found, genes_predicted, genes_skipped}`，
  满足 `genes_predicted + genes_skipped == genes_found`；每个基因的跳过原因在
  `data.expression_predictions[].skip_reason` 中。超过 **50,000 bp**（其 `x-sync-limit-bp`）时强制
  异步：超过该大小的同步请求返回 `413 sync_too_large`，
  `error.details = {sequence_length, threshold}`——请用相同的请求体加上
  `Prefer: respond-async` 重试。

API 还发布了一个单独的、仍在开发中的 VCF 工作流。当 `meta.model` 缺失时，
其输出并不是已确立的模型结果；参见
[有界契约说明](references/api-and-auth.md#vcf-workflow-boundary)。

## 错误

| 状态码 | `error.code` | 含义 | 处理方式 |
|---|---|---|---|
| 400 | `bad_request` | 请求格式错误 | 检查请求体结构 |
| 401 / 403 | `unauthorized` / `forbidden` | 缺失/无效密钥（REST） | 设置 `GI_API_KEY`；或使用免密钥 MCP 演示 |
| 404 | `not_found` | **未知任务**（`/v1/tasks/bogus/predict`）或未知作业 | 检查任务名称——无法识别的任务返回 404，而不是 422 |
| 413 | `payload_too_large` | 原始请求体超过 **16 MiB** | 拆分输入——这是请求体上限，而不是序列上限 |
| 410 | `job_expired` | 结果保留期已过 | 恢复已保存的结果，或有意识地提交新任务 |
| 413 | `sync_too_large` | 同步 JSON 请求超过该操作的 `x-sync-limit-bp`（`annotation` 为 200,000 bp，复合工作流为 50,000 bp） | 使用 `Prefer: respond-async` 重试 |
| 415 | `unsupported_format` | 不支持的 `format` 查询值 | 使用该任务支持的格式；不会静默回退到 JSON |
| 422 | `validation_failed` | 最常见的失败：序列**低于任务下限或超过 500,000 bp**、表达序列低于 9,198 bp、`tss_index` 缺失/越界、缺少 `options.description`，或出现**任何未知的请求体或 `options` 键**；也包括剪接响应上限 | 阅读消息；修正请求体 |
| 429 | `rate_limited` / `too_many_requests` | 速率 / 并发上限 | 退避（遵循 `Retry-After`）；请 GI 提升你的层级 |
| 5xx | `internal_error` / `service_unavailable` / `model_loading` / `timeout` | 服务器错误 | 保留请求/作业 ID；带退避地重试轮询，避免盲目重新提交 POST |

`error.code` 是一个封闭的 21 值枚举（`bad_request`、`unauthorized`、
`forbidden`、`not_found`、`conflict`、`job_expired`、`payload_too_large`、
`sync_too_large`、`unsupported_format`、`validation_failed`、
`too_many_requests`、`rate_limited`、`internal_error`、`timeout`、
`insufficient_memory`、`model_not_found`、`task_not_supported_by_model`、
`model_loading`、`service_unavailable`、`http_error`、`unknown`）；遇到未列出的值时，
应将其视为一般性失败，而不是解析错误。

**首先依据 `code` 分支，绝不依据消息文本或 `loc`。** Pydantic 请求
失败通常带有 `details.errors`；剪接响应上限则带有
`record_count`、`maximum_records`、`sequence_length` 和 `threshold`。请将
这些作为不同的可选 details 结构分别处理。超过 20,000 条剪接记录会导致
`422 validation_failed`，而不是返回截断的结果；请提高阈值，并记录
这一被更改的分析设置。参见[任务注意事项](references/tasks.md)。

为了关联追踪，API 响应中同时记录了 `error.request_id` 和 `X-Request-Id` **请求头**，
成功信封中带有 `meta.request_id`。优先读取该请求头仍是稳妥的默认做法。
API 响应记录了 `RateLimit-Limit`、`RateLimit-Remaining`、
`RateLimit-Reset`、`RateLimit-Policy`；`429` 还会附加 `Retry-After`。该限制是
突发桶（burst bucket），而不是每分钟请求数：已发布的 `x-rate-limit-burst-divisor` 为 6，因此
持续的每分钟配额是该请求头值的六倍。代理故障可能会省略
这些请求头以及常规的 JSON 错误信封。

于 2026-10-01 对照线上 OpenAPI `info.version` **2026.09.22.2
(af902d84)**、`x-contract-revision: 16` 以及 `gi-mcp` **0.1.0a21** 进行了审查。
请将契约修订版、解析后的模型 ID、基因组组装版本、链/TSS
来源、选项以及实验描述与结果一并记录。在可能时对确切提交的碱基计算哈希。
仅返回句柄的 MCP 获取只返回预览，而不是完整碱基或校验和：请保留其获取参数和来源
发布版本元数据，不要编造哈希或声称进行了字节级验证。
[审查证据与局限](references/review.md)区分了公共发现、
源码审查和模拟示例与推理验证。

## 参考文件

- `references/tasks.md`——各任务的输出结构、模型注册表、异步
  注释契约。
- `references/api-and-auth.md`——REST 端点、`{data, meta}` 信封、
  认证、基础 URL 覆盖、层级。
- `references/mcp.md`——托管 MCP 工具列表、基于句柄的流程，以及
  `gi://` 资源。
- `references/sequence-acquisition.md`——Ensembl 获取调用以及
  表达窗口（9,198 bp，以 TSS 为中心）的计算，包括 `tss_index`。
