---
name: OpenAI Automation
description: "自动化 OpenAI API 操作 -- 通过 Composio MCP 集成生成响应（支持多模态和结构化输出）、创建嵌入向量、生成图像以及列出模型。"
requires:
  mcp:
    - rube
---

# OpenAI Automation

自动化你的 OpenAI API 工作流 -- 使用 Responses API 生成文本（包括多模态图像+文本输入和结构化 JSON 输出）、为搜索和聚类创建嵌入向量、用 DALL-E 和 GPT Image 模型生成图像，并列出可用模型。

**工具包文档：** [composio.dev/toolkits/openai](https://composio.dev/toolkits/openai)

---

## 设置

1. 将 Composio MCP 服务器添加到你的客户端：`https://rube.app/mcp`
2. 按提示连接你的 OpenAI 账户（API 密钥身份验证）
3. 开始使用下面的工作流

---

## 核心工作流

### 1. 生成响应（文本、多模态、结构化）

使用 `OPENAI_CREATE_RESPONSE` 获取一次性的模型响应，包括文本、图像分析、OCR 以及结构化 JSON 输出。

```
Tool: OPENAI_CREATE_RESPONSE
Inputs:
  - model: string (required) -- e.g., "gpt-5", "gpt-4o", "o3-mini"
  - input: string | array (required)
    Simple: "Explain quantum computing"
    Multimodal: [
      { role: "user", content: [
        { type: "input_text", text: "What is in this image?" },
        { type: "input_image", image_url: { url: "https://..." } }
      ]}
    ]
  - temperature: number (0-2, optional -- not supported with reasoning models)
  - max_output_tokens: integer (optional)
  - reasoning: { effort: "none" | "minimal" | "low" | "medium" | "high" }
  - text: object (structured output config)
    - format: { type: "json_schema", name: "...", schema: {...}, strict: true }
  - tools: array (function, code_interpreter, file_search, web_search)
  - tool_choice: "auto" | "none" | "required" | { type: "function", function: { name: "..." } }
  - store: boolean (false to opt out of model distillation)
  - stream: boolean
```

**结构化输出示例：** 将 `text.format` 设置为 `{ type: "json_schema", name: "person", schema: { type: "object", properties: { name: { type: "string" }, age: { type: "integer" } }, required: ["name", "age"], additionalProperties: false }, strict: true }`。

### 2. 创建嵌入向量

使用 `OPENAI_CREATE_EMBEDDINGS` 实现向量搜索、聚类、推荐和 RAG 流水线。

```
Tool: OPENAI_CREATE_EMBEDDINGS
Inputs:
  - input: string | string[] | int[] | int[][] (required) -- max 8192 tokens, max 2048 items
  - model: string (required) -- "text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"
  - dimensions: integer (optional, only for text-embedding-3 and later)
  - encoding_format: "float" | "base64" (default "float")
  - user: string (optional, end-user ID for abuse monitoring)
```

### 3. 生成图像

使用 `OPENAI_CREATE_IMAGE` 通过 GPT Image 或 DALL-E 模型根据文本提示创建图像。

```
Tool: OPENAI_CREATE_IMAGE
Inputs:
  - model: string (required) -- "gpt-image-1", "gpt-image-1.5", "dall-e-3", "dall-e-2"
  - prompt: string (required) -- max 32000 chars (GPT Image), 4000 (DALL-E 3), 1000 (DALL-E 2)
  - size: "1024x1024" | "1536x1024" | "1024x1536" | "auto" | "256x256" | "512x512" | "1792x1024" | "1024x1792"
  - quality: "standard" | "hd" | "auto" | "high" | "medium" | "low"
  - n: integer (1-10; DALL-E 3 supports n=1 only)
  - background: "transparent" | "opaque" | "auto" (GPT Image models only)
  - style: "vivid" | "natural" (DALL-E 3 only)
  - user: string (optional)
```

### 4. 列出可用模型

使用 `OPENAI_LIST_MODELS` 查看你的 API 密钥可以访问哪些模型。

```
Tool: OPENAI_LIST_MODELS
Inputs: (none)
```

---

## 常见陷阱

| 陷阱 | 详情 |
|---------|--------|
| DALL-E 已被弃用 | DALL-E 2 和 DALL-E 3 已被弃用，将于 2026 年 5 月 12 日停止支持。请优先使用 GPT Image 模型。 |
| DALL-E 3 仅支持单图 | 使用 DALL-E 3 的 `OPENAI_CREATE_IMAGE` 仅支持 `n=1`。若需生成多张图像，请使用 GPT Image 模型或 DALL-E 2。 |
| 嵌入向量的 token 限制 | 对于嵌入模型，每项输入不得超过 8192 个 token，每批不得超过 2048 项。 |
| 推理模型的限制 | 推理模型（o3-mini 等）不支持 `temperature` 和 `top_p`。请改用 `reasoning.effort`。 |
| 结构化输出的严格模式 | 当 json_schema 格式中 `strict: true` 时，所有 schema 属性必须都列在 `required` 数组中。 |
| 提示长度因模型而异 | 图像提示的最大长度各不相同：32000（GPT Image）、4000（DALL-E 3）、1000（DALL-E 2）。 |

---

## 快速参考

| 工具标识 | 说明 |
|-----------|-------------|
| `OPENAI_CREATE_RESPONSE` | 生成文本/多模态响应，支持结构化输出 |
| `OPENAI_CREATE_EMBEDDINGS` | 创建用于搜索、聚类和 RAG 的文本嵌入向量 |
| `OPENAI_CREATE_IMAGE` | 根据文本提示生成图像 |
| `OPENAI_LIST_MODELS` | 列出你的 API 密钥可用的所有模型 |

---

*由 [Composio](https://composio.dev) 提供支持*
