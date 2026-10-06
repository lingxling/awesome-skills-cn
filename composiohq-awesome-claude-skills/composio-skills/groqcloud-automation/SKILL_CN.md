---
name: GroqCloud Automation
description: "通过 Composio 借助 GroqCloud 的高性能 API 自动化 AI 推理、聊天补全、音频翻译和 TTS 语音管理"
requires:
  mcp:
    - rube
---

# GroqCloud 自动化

使用 GroqCloud 的超高速 API 自动化 AI 推理工作流——聊天补全、模型发现、音频翻译和 TTS 语音选择——全部通过 Composio MCP 集成进行编排。

**工具包文档：** [composio.dev/toolkits/groqcloud](https://composio.dev/toolkits/groqcloud)

---

## 设置

1. 通过 `https://rube.app/mcp` 的 Composio MCP 服务器连接你的 GroqCloud 账户
2. 如果不存在有效连接，智能体会向你提供一个认证链接
3. 连接后，所有 `GROQCLOUD_*` 工具都可用于执行

---

## 核心工作流

### 1. 发现可用模型
列出 GroqCloud 上所有可用的模型，以便在运行推理之前找到有效的模型 ID。

**工具：** `GROQCLOUD_LIST_MODELS`

```
No parameters required -- returns all available models with metadata.
```

在任何聊天补全调用之前，请先使用它，以确保引用的是有效且未被弃用的模型 ID。

---

### 2. 运行聊天补全
使用指定的 GroqCloud 模型为对话式提示生成 AI 响应。

**工具：** `GROQCLOUD_GROQ_CREATE_CHAT_COMPLETION`

| 参数 | 类型 | 必填 | 描述 |
|-----------|------|----------|-------------|
| `model` | string | 是 | 来自 `GROQCLOUD_LIST_MODELS` 的模型 ID |
| `messages` | array | 是 | `{role, content}` 对象的有序列表（`system`、`user`、`assistant`） |
| `temperature` | number | 否 | 采样温度 0-2（默认：1） |
| `max_completion_tokens` | integer | 否 | 生成的最大 token 数 |
| `top_p` | number | 否 | 核采样 0-1（默认：1） |
| `stop` | string/array | 否 | 最多 4 个停止序列 |
| `stream` | boolean | 否 | 启用 SSE 流式传输（默认：false） |

---

### 3. 查看模型详情
检索特定模型的详细元数据，包括上下文窗口和能力。

**工具：** `GROQCLOUD_GROQ_RETRIEVE_MODEL`

| 参数 | 类型 | 必填 | 描述 |
|-----------|------|----------|-------------|
| `model` | string | 是 | 模型标识符（例如 `groq-1-large`） |

---

### 4. 将音频翻译为英文
使用 Whisper 模型将非英语音频文件翻译为英文文本。

**工具：** `GROQCLOUD_GROQ_CREATE_AUDIO_TRANSLATION`

| 参数 | 类型 | 必填 | 描述 |
|-----------|------|----------|-------------|
| `file_path` | string | 是 | 音频的本地路径、HTTP(S) URL 或 base64 data URL |
| `model` | string | 否 | 模型 ID（默认：`whisper-large-v3`）。注意：`whisper-large-v3-turbo` 可能不支持翻译 |
| `response_format` | string | 否 | `json`、`verbose_json` 或 `text`（默认：`json`） |
| `temperature` | number | 否 | 采样温度 0-1（默认：0） |

---

### 5. 列出 TTS 语音
枚举 Groq PlayAI 模型可用的文本转语音语音，以驱动语音选择的用户体验。

**工具：** `GROQCLOUD_LIST_VOICES`

```
Returns the set of supported TTS voices. Note: this is a static list maintained manually.
```

---

## 已知陷阱

| 陷阱 | 详情 |
|---------|---------|
| **嵌套的模型列表** | `GROQCLOUD_LIST_MODELS` 的响应可能嵌套在 `response['data']['data']` 中——不要假设它是扁平的顶层数组 |
| **硬编码的模型 ID 会失效** | 始终通过 `GROQCLOUD_LIST_MODELS` 动态获取模型 ID；当模型被弃用或重命名时，硬编码的名称可能会失效 |
| **音频格式验证** | `GROQCLOUD_GROQ_CREATE_AUDIO_TRANSLATION` 会静默拒绝无效或不受支持的音频格式——调用前请验证输入 |
| **模型元数据会漂移** | `GROQCLOUD_GROQ_RETRIEVE_MODEL` 返回的数据（上下文窗口、功能）会随着模型更新而变化——不要将其视为静态数据 |
| **TTS 语音变化** | `GROQCLOUD_LIST_VOICES` 返回的语音集合可能会随时间缩减或重命名——请妥善处理缺失的语音 |

---

## 快速参考

| 工具 Slug | 用途 |
|-----------|---------|
| `GROQCLOUD_LIST_MODELS` | 列出所有可用模型及元数据 |
| `GROQCLOUD_GROQ_CREATE_CHAT_COMPLETION` | 生成基于聊天的 AI 补全 |
| `GROQCLOUD_GROQ_RETRIEVE_MODEL` | 获取特定模型的详细信息 |
| `GROQCLOUD_GROQ_CREATE_AUDIO_TRANSLATION` | 将非英语音频翻译为英文文本 |
| `GROQCLOUD_LIST_VOICES` | 检索 PlayAI 可用的 TTS 语音 |

---

*由 [Composio](https://composio.dev) 提供支持*
