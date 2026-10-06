---
name: Mistral AI Automation
description: "自动化 Mistral AI 操作——管理文件和库、上传文档用于微调、批处理和 OCR、跟踪微调任务，并通过 Composio MCP 集成构建 RAG 管道。"
requires:
  mcp:
    - rube
---

# Mistral AI 自动化

自动化你的 Mistral AI 工作流——上传文件用于微调、批处理和 OCR，管理支持 RAG 的智能体所用的文档库，列出并检索文件，跟踪微调任务，并将 Mistral AI 集成到跨应用的数据管道中。

**工具包文档：** [composio.dev/toolkits/mistral_ai](https://composio.dev/toolkits/mistral_ai)

---

## 设置

1. 将 Composio MCP 服务器添加到你的客户端：`https://rube.app/mcp`
2. 在提示时连接你的 Mistral AI 账户（API 密钥认证）
3. 开始使用下面的工作流

---

## 核心工作流

### 1. 将文件上传到 Mistral AI

使用 `MISTRAL_AI_UPLOAD_FILE` 上传文件，用于微调、批处理或 OCR。

```
Tool: MISTRAL_AI_UPLOAD_FILE
Inputs:
  - file: object (required)
    - name: string -- destination filename (e.g., "training_data.jsonl")
    - mimetype: string -- MIME type (e.g., "application/pdf", "application/jsonl")
    - s3key: string -- S3 key of a previously downloaded/stored file
  - purpose: "fine-tune" | "batch" | "ocr" (default "fine-tune")
```

**限制：** 最大文件大小为 512 MB。对于微调，仅支持 `.jsonl` 文件。

### 2. 列出并检索文件

使用 `MISTRAL_AI_LIST_FILES` 分页浏览已上传的文件，使用 `MISTRAL_AI_RETRIEVE_FILE` 获取特定文件的元数据。

```
Tool: MISTRAL_AI_LIST_FILES
Inputs:
  - limit: integer (optional, min 1)
  - after: string (file ID cursor for next page)
  - order: "asc" | "desc" (default "desc")

Tool: MISTRAL_AI_RETRIEVE_FILE
Inputs:
  - file_id: string (required) -- UUID obtained from List Files
```

### 3. 创建文档库

使用 `MISTRAL_AI_CREATE_LIBRARY` 将文档分组到库中，供支持 RAG 的 Mistral AI 智能体使用。

```
Tool: MISTRAL_AI_CREATE_LIBRARY
Inputs:
  - name: string (required) -- e.g., "Project Documents"
  - description: string (optional)
```

### 4. 将文档上传到库

使用 `MISTRAL_AI_UPLOAD_LIBRARY_DOCUMENT` 向库中添加文档，供 Mistral AI 智能体进行 RAG 检索。

```
Tool: MISTRAL_AI_UPLOAD_LIBRARY_DOCUMENT
  - Requires library_id and file details
  - Call RUBE_GET_TOOL_SCHEMAS for full input schema before use
```

### 5. 列出库并下载文件

使用 `MISTRAL_AI_LIST_LIBRARIES` 发现可用的文档库，使用 `MISTRAL_AI_DOWNLOAD_FILE` 检索文件内容。

```
Tool: MISTRAL_AI_LIST_LIBRARIES
  - Lists all document libraries with metadata (id, name, document counts)
  - Call RUBE_GET_TOOL_SCHEMAS for full input schema

Tool: MISTRAL_AI_DOWNLOAD_FILE
  - Downloads raw binary content of a previously uploaded file
  - Call RUBE_GET_TOOL_SCHEMAS for full input schema
```

### 6. 跟踪微调任务

使用 `MISTRAL_AI_GET_FINE_TUNING_JOBS` 按模型、状态和创建时间列出并过滤微调任务。

```
Tool: MISTRAL_AI_GET_FINE_TUNING_JOBS
  - Supports filtering by model, status, creation time, and W&B integration
  - Call RUBE_GET_TOOL_SCHEMAS for full input schema
```

---

## 已知陷阱

| 陷阱 | 详情 |
|---------|--------|
| 微调文件格式 | 微调上传仅支持 `.jsonl` 文件。其他格式将被拒绝。 |
| 文件大小限制 | 每个文件的最大上传大小为 512 MB。 |
| 文件对象结构 | `MISTRAL_AI_UPLOAD_FILE` 需要一个引用先前存储文件的 `s3key`，而不是原始二进制内容。请先使用下载操作将文件暂存到 S3。 |
| 分页游标 | `MISTRAL_AI_LIST_FILES` 通过 `after` 参数（文件 ID）使用基于游标的分页。持续获取直到不再返回结果。 |
| 库文档处理 | 上传的库文档是异步处理的。上传后它们可能无法立即用于 RAG 查询。 |
| Schema 引用 | 若干工具（`MISTRAL_AI_UPLOAD_LIBRARY_DOCUMENT`、`MISTRAL_AI_LIST_LIBRARIES`、`MISTRAL_AI_GET_FINE_TUNING_JOBS`、`MISTRAL_AI_DOWNLOAD_FILE`）需要在执行前调用 `RUBE_GET_TOOL_SCHEMAS` 来加载完整的输入 schema。 |

---

## 快速参考

| 工具 Slug | 描述 |
|-----------|-------------|
| `MISTRAL_AI_UPLOAD_FILE` | 上传文件用于微调、批处理或 OCR |
| `MISTRAL_AI_LIST_FILES` | 列出已上传的文件，支持分页 |
| `MISTRAL_AI_RETRIEVE_FILE` | 按 ID 获取特定文件的元数据 |
| `MISTRAL_AI_DOWNLOAD_FILE` | 下载已上传文件的内容 |
| `MISTRAL_AI_CREATE_LIBRARY` | 为 RAG 创建文档库 |
| `MISTRAL_AI_LIST_LIBRARIES` | 列出所有文档库及元数据 |
| `MISTRAL_AI_UPLOAD_LIBRARY_DOCUMENT` | 将文档添加到库中用于 RAG |
| `MISTRAL_AI_GET_FINE_TUNING_JOBS` | 列出并过滤微调任务 |

---

*由 [Composio](https://composio.dev) 提供支持*
