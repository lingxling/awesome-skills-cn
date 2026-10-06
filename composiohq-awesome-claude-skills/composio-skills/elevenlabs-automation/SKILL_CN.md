---
name: ElevenLabs Automation
description: "通过 Composio MCP 集成自动化 ElevenLabs 文本转语音工作流——从文本生成语音、浏览和检查语音、查看订阅额度、列出模型、流式传输音频，以及检索历史记录。"
requires:
  mcp:
    - rube
---

# ElevenLabs Automation

自动化你的 ElevenLabs 文本转语音工作流——将文本转换为自然语音、浏览语音库、检查语音详情、查看订阅额度、选择 TTS 模型、以低延迟方式流式传输音频，并从历史记录中检索之前生成的音频。

**工具包文档：** [composio.dev/toolkits/elevenlabs](https://composio.dev/toolkits/elevenlabs)

---

## 设置

1. 将 Composio MCP 服务器添加到你的客户端：`https://rube.app/mcp`
2. 按提示连接你的 ElevenLabs 账户（API 密钥认证）
3. 开始使用下面的工作流

---

## 核心工作流

### 1. 从文本生成语音

使用 `ELEVENLABS_TEXT_TO_SPEECH` 将文本转换为可下载的音频文件。

```
工具：ELEVENLABS_TEXT_TO_SPEECH
输入：
  - voice_id：字符串（必需） —— 从 ELEVENLABS_GET_VOICES 获取
  - text：字符串（必需） —— 最多约 10,000 字符（大多数模型）、30,000（Flash/Turbo v2）、40,000（v2.5）
  - model_id：字符串（默认 "eleven_monolingual_v1"） —— 例如 "eleven_multilingual_v2"
  - output_format：字符串（默认 "mp3_44100_128"） —— 见下方格式
  - optimize_streaming_latency：整数（0-4；eleven_v3 不支持）
  - seed：整数（可选，用于可重复性——不保证）
  - pronunciation_dictionary_locators：数组（可选，最多 3 个词典）
```

**输出格式：**
- MP3：`mp3_22050_32`、`mp3_44100_32`、`mp3_44100_64`、`mp3_44100_96`、`mp3_44100_128`、`mp3_44100_192`（Creator 及以上）
- PCM：`pcm_16000`、`pcm_22050`、`pcm_24000`、`pcm_44100`（Pro 及以上）
- uLaw：`ulaw_8000`（适用于 Twilio）

**重要：** 输出是一个文件对象，带有位于 `data.file.s3url` 的预签名下载链接（约 1 小时后过期）。请及时下载。

### 2. 浏览可用语音

使用 `ELEVENLABS_GET_VOICES` 列出所有语音及其属性和设置。

```
工具：ELEVENLABS_GET_VOICES
输入：（无）
```

返回位于 `data.voices[]` 的数组，包含 `voice_id`、`name`、`labels`（性别、口音、使用场景）和设置。

### 3. 检查特定语音

在合成之前，使用 `ELEVENLABS_GET_VOICE` 获取候选语音的详细元数据。

```
工具：ELEVENLABS_GET_VOICE
输入：
  - voice_id：字符串（必需） —— 例如 "21m00Tcm4TlvDq8ikWAM"
  - with_settings：布尔值（默认 false） —— 是否包含详细的语音设置
```

### 4. 检查订阅和额度

在批量生成之前，使用 `ELEVENLABS_GET_USER_SUBSCRIPTION_INFO` 验证计划限额和剩余额度。

```
工具：ELEVENLABS_GET_USER_SUBSCRIPTION_INFO
输入：（无）
```

### 5. 列出可用的 TTS 模型

使用 `ELEVENLABS_GET_MODELS` 发现兼容的模型，并按 `can_do_text_to_speech: true` 筛选。

```
工具：ELEVENLABS_GET_MODELS
输入：（无）
```

### 6. 流式传输音频并检索历史记录

使用 `ELEVENLABS_TEXT_TO_SPEECH_STREAM` 实现低延迟流式传输，使用 `ELEVENLABS_GET_AUDIO_FROM_HISTORY_ITEM` 重新下载之前生成的音频。

```
工具：ELEVENLABS_TEXT_TO_SPEECH_STREAM
  - 与 TEXT_TO_SPEECH 的核心输入相同，但返回用于低延迟播放的流

工具：ELEVENLABS_GET_AUDIO_FROM_HISTORY_ITEM
  - history_item_id：字符串（必需） —— 来自先前生成的 ID
```

---

## 已知陷阱

| 陷阱 | 详情 |
|---------|--------|
| 文本长度限制 | 大多数模型每次请求上限约为 10,000-20,000 字符。超大输入会返回 HTTP 400。将长文本拆分为多个块（约 5000 字符）并逐块生成。 |
| 输出是预签名链接 | `ELEVENLABS_TEXT_TO_SPEECH` 返回的 `data.file.s3url` 有效期约 1 小时（X-Amz-Expires=3600）。请及时下载音频文件。 |
| 配额和额度错误 | HTTP 401 伴随 `quota_exceeded`，或 HTTP 402 `payment_required`，表示额度不足或受套餐限制。在批量任务前用 `ELEVENLABS_GET_USER_SUBSCRIPTION_INFO` 检查。 |
| 语音权限 | HTTP 401 伴随 `missing_permissions` 表示 API 密钥缺少 `voices_read` 权限范围。请验证密钥权限。 |
| 模型兼容性 | 并非所有模型都支持 TTS。使用 `ELEVENLABS_GET_MODELS` 并按 `can_do_text_to_speech: true` 筛选。`optimize_streaming_latency` 参数不支持 `eleven_v3`。 |
| 大型语音列表被截断 | `ELEVENLABS_GET_VOICES` 可能返回很长的列表。请从完整的 `data.voices[]` 负载中进行选择——预览内容可能显示被截断。 |

---

## 快速参考

| 工具标识 | 描述 |
|-----------|-------------|
| `ELEVENLABS_TEXT_TO_SPEECH` | 将文本转换为语音，返回可下载的音频文件 |
| `ELEVENLABS_GET_VOICES` | 列出所有可用语音及其属性 |
| `ELEVENLABS_GET_VOICE` | 获取特定语音的详细信息 |
| `ELEVENLABS_GET_USER_SUBSCRIPTION_INFO` | 查看订阅计划和剩余额度 |
| `ELEVENLABS_GET_MODELS` | 列出可用的 TTS 模型及其能力 |
| `ELEVENLABS_TEXT_TO_SPEECH_STREAM` | 以低延迟方式流式传输音频 |
| `ELEVENLABS_GET_AUDIO_FROM_HISTORY_ITEM` | 从生成历史记录中重新下载音频 |

---

*由 [Composio](https://composio.dev) 提供支持*
