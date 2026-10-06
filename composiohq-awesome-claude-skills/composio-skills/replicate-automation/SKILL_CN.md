---
name: Replicate Automation
description: "自动化 Replicate AI 模型操作 -- 通过 Composio MCP 集成运行预测、上传文件、检查模型模式、列出版本以及管理预测历史。"
requires:
  mcp:
    - rube
---

# Replicate 自动化

自动化你的 Replicate AI 模型工作流 -- 在任何公开模型（图像生成、LLM、音频、视频）上运行预测、上传输入文件、检查模型模式和文档、列出模型版本以及跟踪预测历史。

**工具包文档:** [composio.dev/toolkits/replicate](https://composio.dev/toolkits/replicate)

---

## 设置

1. 将 Composio MCP 服务器添加到你的客户端：`https://rube.app/mcp`
2. 在提示时连接你的 Replicate 账户（API 令牌认证）
3. 开始使用下面的工作流

---

## 核心工作流

### 1. 获取模型详情和模式

在运行预测之前，使用 `REPLICATE_MODELS_GET` 检查模型的输入/输出模式。

```
Tool: REPLICATE_MODELS_GET
Inputs:
  - model_owner: string (required) -- e.g., "meta", "black-forest-labs", "stability-ai"
  - model_name: string (required) -- e.g., "meta-llama-3-8b-instruct", "flux-1.1-pro"
```

**重要：** 每个模型都有独特的输入键和类型。在构造预测输入之前，请务必检查此响应中的 `openapi_schema`。

### 2. 运行预测

使用 `REPLICATE_MODELS_PREDICTIONS_CREATE` 在任何模型上运行推理，可选择同步等待和 webhook。

```
Tool: REPLICATE_MODELS_PREDICTIONS_CREATE
Inputs:
  - model_owner: string (required) -- e.g., "meta", "black-forest-labs"
  - model_name: string (required) -- e.g., "flux-1.1-pro", "sdxl"
  - input: object (required) -- model-specific inputs, e.g., { "prompt": "A sunset over mountains" }
  - wait_for: integer (1-60 seconds, optional) -- synchronous wait for completion
  - cancel_after: string (optional) -- max execution time, e.g., "300s", "5m"
  - webhook: string (optional) -- HTTPS URL for async completion notifications
  - webhook_events_filter: array (optional) -- ["start", "output", "logs", "completed"]
```

**同步与异步：** 对于快速模型使用 `wait_for`（1-60 秒）。对于长时间运行的任务，请省略它，改用 webhook 或通过 `REPLICATE_PREDICTIONS_LIST` 轮询。

### 3. 上传模型输入文件

使用 `REPLICATE_CREATE_FILE` 上传图像、文档或模型所需的其他二进制输入。

```
Tool: REPLICATE_CREATE_FILE
Inputs:
  - content: string (required) -- base64-encoded file content
  - filename: string (required) -- e.g., "input.png", "audio.wav" (max 255 bytes UTF-8)
  - content_type: string (default "application/octet-stream") -- MIME type
  - metadata: object (optional) -- custom JSON metadata
```

### 4. 阅读模型文档

使用 `REPLICATE_MODELS_README_GET` 以 Markdown 格式获取模型的 README，了解详细的使用说明。

```
Tool: REPLICATE_MODELS_README_GET
Inputs:
  - model_owner: string (required)
  - model_name: string (required)
```

### 5. 列出模型版本

使用 `REPLICATE_MODELS_VERSIONS_LIST` 查看模型的所有可用版本，按最新优先排序。

```
Tool: REPLICATE_MODELS_VERSIONS_LIST
Inputs:
  - model_owner: string (required)
  - model_name: string (required)
```

### 6. 跟踪预测历史和文件

使用 `REPLICATE_PREDICTIONS_LIST` 检索预测历史，并使用 `REPLICATE_FILES_GET`/`REPLICATE_FILES_LIST` 管理已上传的文件。

```
Tool: REPLICATE_PREDICTIONS_LIST
  - Lists all predictions for the authenticated user with pagination

Tool: REPLICATE_FILES_LIST
  - Lists uploaded files, most recent first

Tool: REPLICATE_FILES_GET
  - Get details of a specific file by ID
```

---

## 已知陷阱

| 陷阱 | 详情 |
|---------|--------|
| 模型特定的输入键 | 每个模型都有独特的输入键和类型。使用错误的键会导致验证错误。请务必先调用 `REPLICATE_MODELS_GET` 检查 `openapi_schema`。 |
| 文件上传编码 | `REPLICATE_CREATE_FILE` 需要 base64 编码的内容。被当作文本（UTF-8）处理的二进制文件会因解码错误而失败。 |
| 公开模型与部署路径 | 公开模型必须通过 `REPLICATE_MODELS_PREDICTIONS_CREATE` 运行。使用面向部署的路径会导致 HTTP 404 失败。 |
| 同步等待限制 | `wait_for` 仅支持 1-60 秒。长时间运行的任务需要通过 webhook 或轮询 `REPLICATE_PREDICTIONS_LIST` 进行异步处理。 |
| 图像模型约束 | flux-1.1-pro 等图像模型有特定约束（例如，最大宽/高 1440px、有效的宽高比）。请先检查模型模式。 |
| 过期的文件引用 | 大量使用会产生许多上传文件。请定期检查 `REPLICATE_FILES_LIST`，避免使用过期的 `file_id` 引用。 |

---

## 快速参考

| 工具 Slug | 描述 |
|-----------|-------------|
| `REPLICATE_MODELS_GET` | 获取模型详情、模式和元数据 |
| `REPLICATE_MODELS_PREDICTIONS_CREATE` | 在模型上运行预测 |
| `REPLICATE_CREATE_FILE` | 上传文件作为模型输入 |
| `REPLICATE_MODELS_README_GET` | 获取模型 README 文档 |
| `REPLICATE_MODELS_VERSIONS_LIST` | 列出模型的所有版本 |
| `REPLICATE_PREDICTIONS_LIST` | 列出带分页的预测历史 |
| `REPLICATE_FILES_LIST` | 列出已上传的文件 |
| `REPLICATE_FILES_GET` | 按 ID 获取文件详情 |

---

*由 [Composio](https://composio.dev) 提供支持*
