---
name: audio-transcriber
description: "使用 LLM 集成将音频记录转换为具有智能摘要的专业 Markdown 文档"
category: content
risk: safe
source: community
tags: "[audio, transcription, whisper, meeting-minutes, speech-to-text]"
date_added: "2026-02-27"
---

## 详细指南

在执行此技能前读取[详细指南](references/detailed-guide.md)。它保留完整程序和参考材料。将其安全、前置条件和验证要求视为强制性。为了专注工作，加载相关部分；为端到端工作，完全读取指南。

## 何时使用

在以下情况调用此技能：

- 用户需要转录音频/视频文件为文本
- 用户想要从记录自动生成会议记录
- 用户在对话中需要说话人识别（说话人分割）
- 用户需要字幕/说明文字（SRT、VTT 格式）
- 用户想要长音频内容的执行摘要
- 用户询问"转录此音频"、"将音频转换为文本"、"从记录生成会议记录"的变体
- 用户有常见格式的音频文件（MP3、WAV、M4A、OGG、FLAC、WEBM）

## 示例用法

### **示例 1：基本转录**

**用户输入：**
```bash
copilot> transcribe audio to markdown: meeting-2026-02-02.mp3
```

**技能输出**

```bash
✅ Faster-Whisper detected (optimized)
✅ ffmpeg available (format conversion enabled)

📂 文件：meeting-2026-02-02.mp3
📊 大小：12.3 MB
⏱️  持续时间：00:45:32

🎙️  处理中...
[████████████████████] 100%

✅ 检测到的语言：Portuguese (pt-BR)
👥 识别的说话人：4
📝 生成 Markdown 输出...

✅ 转录完成！

📊 结果：
  文件：meeting-2026-02-02.md
  语言：pt-BR
  持续时间：00:45:32
  说话人：4
  单词：6,842
  处理时间：127s

📝 生成的：
  - meeting-2026-02-02.md (Markdown 报告)

🎯 后续步骤：
  1. 审查会议记录和行动项
  2. 与参与者分享报告
  3. 跟踪行动项完成情况
```

### **示例 3：批量处理**

**用户输入：**
```bash
copilot> transcreva estes áudios: recordings/*.mp3
```

**技能输出**

```bash
📦 批量模式：5 个文件找到
  1. team-standup.mp3
  2. client-call.mp3
  3. brainstorm-session.mp3
  4. product-demo.mp3
  5. retrospective.mp3

🎙️  处理批次...

[1/5] team-standup.mp3 ✅ (2m 34s)
[2/5] client-call.mp3 ✅ (15m 12s)
[3/5] brainstorm-session.mp3 ✅ (8m 47s)
[4/5] product-demo.mp3 ✅ (22m 03s)
[5/5] retrospective.mp3 ✅ (11m 28s)

✅ 批次完成！
📝 生成 5 个 Markdown 报告
⏱️  总处理时间：6m 15s
```

### **示例 5：大文件警告**

**用户输入：**
```bash
copilot> transcribe audio to markdown: conference-keynote.mp3
```

**技能输出**

```bash
✅ Faster-Whisper detected (optimized)

📂 文件：conference-keynote.mp3
📊 大小：87.2 MB
⏱️  持续时间：02:15:47
⚠️  大文件（87.2 MB）- 处理可能需要几分钟

继续吗？[Y/n]：
```

**用户：** `Y`

```bash
🎙️  处理中...（这可能需要 10-15 分钟）
[████░░░░░░░░░░░░░░░░] 20% - 估计剩余时间：12m
```

此技能**与平台无关**，在任何提供 GitHub Copilot CLI 的终端上下文中工作。它不依赖于特定的项目配置或外部 API，遵循零配置理念。

## 限制

- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
