---
name: azure-ai-transcription-py
description: Azure AI 转录 SDK for Python。用于实时和批量语音转文本转录，包含时间戳和说话人分离。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure AI Transcription SDK for Python

Azure AI 转录（语音转文本）的客户端库，支持实时和批量转录。

## 安装

```bash
pip install azure-ai-transcription
```

## 环境变量

```bash
TRANSCRIPTION_ENDPOINT=https://<resource>.cognitiveservices.azure.com
TRANSCRIPTION_KEY=<your-key>
```

## 认证

使用订阅密钥认证（该客户端不支持 DefaultAzureCredential）：

```python
import os
from azure.ai.transcription import TranscriptionClient

client = TranscriptionClient(
    endpoint=os.environ["TRANSCRIPTION_ENDPOINT"],
    credential=os.environ["TRANSCRIPTION_KEY"]
)
```

## 转录（批量）

```python
job = client.begin_transcription(
    name="meeting-transcription",
    locale="en-US",
    content_urls=["https://<storage>/audio.wav"],
    diarization_enabled=True
)
result = job.result()
print(result.status)
```

## 转录（实时）

```python
stream = client.begin_stream_transcription(locale="en-US")
stream.send_audio_file("audio.wav")
for event in stream:
    print(event.text)
```

## 最佳实践

1. **启用说话人分离**（当有多个说话人时）
2. **对存储在 blob 存储中的长文件使用批量转录**
3. **捕获时间戳**以生成字幕
4. **指定语言**以提高识别准确性
5. **处理流式传输背压**（用于实时转录）
6. **完成时关闭转录会话**

## 何时使用

该技能适用于执行上述概述中描述的工作流程或操作。

## 限制

- 仅在任务明确符合上述描述的范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
