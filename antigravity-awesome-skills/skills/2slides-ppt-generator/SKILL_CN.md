---
name: 2slides-ppt-generator
description: "通过2slides API进行AI驱动的演示文稿生成 — 从文本创建幻灯片、匹配参考图像样式、将文档汇总为演示文稿、添加AI语音旁白和导出页面/音频。用于任何"制作幻灯片"、"创建演示文稿"或"从该文档生成幻灯片"的请求。"
category: api-integration
risk: safe
source: community
source_repo: 2slides/slides-generation-2slides-skills
source_type: community
date_added: "2026-06-05"
author: 2slides
tags: [presentations, slides, powerpoint, ai, api-integration, pdf, narration, document-summarization]
tools: [claude, cursor, gemini, codex, antigravity]
plugin:
  setup:
    type: manual
    summary: "在运行生成脚本之前安装Python依赖项并配置2slides API密钥。"
    docs: SKILL.md
---

# 2slides演示文稿生成

## 详细指南

在执行此技能之前，请阅读[详细指南](references/detailed-guide.md)。它保留了完整的程序和参考资料。将其安全性、先决条件和验证要求视为强制性的。对于重点工作，加载相关部分；对于端到端的工作，完全阅读指南。

## 何时使用此技能

- 当用户要求"创建演示文稿"、"制作幻灯片"或"从文本或大纲生成演示文稿"时使用。
- 当用户希望幻灯片匹配参考图像的样式（"创建像这张图像一样的幻灯片"）时使用。
- 当用户想要没有参考图像的自定义设计PDF幻灯片时使用。
- 当用户上传文档并要求"从此文档创建幻灯片"时使用。
- 当用户想要向生成的幻灯片添加AI语音旁白或将幻灯片导出为PNG图像和旁白作为WAV音频时使用。
- 当用户提问"有哪些主题可用？"或想要浏览/选择主题时使用。

## 安全和安全说明

- **凭据**：此技能从 `SLIDES_2SLIDES_API_KEY` 环境变量读取API密钥。永远不要在命令中硬编码密钥、提交或向用户回显。脚本仅通过HTTPS将其作为bearer/`apikey`值发送到 `https://2slides.com`。
- **网络+付费突变**：每次生成调用都会向2slides API发出出站网络请求，并**花费用户的积分**（每页10-210积分，具体取决于模式）。将生成、参考图像、自定义PDF和旁白调用视为可计费的操作 — 在生成大型或高分辨率（4K）演示文稿之前确认意图，并在非平凡情况下显示预期的页数/成本。
- **无破坏性本地操作**：脚本仅读取用户指向的内容/文件，并将生成的输出（例如下载的ZIP）写入用户指定的路径。它们不会修改或删除无关文件。
- **输入处理**：参考图像和文档输入被发送到2slides服务进行处理。不要提交用户未授权用于第三方处理的机密材料。
- **下载URL在1小时内过期** — 及时获取工件，不要将URL视为持久存储。

## 限制

- 需要有效的2slides帐户、API密钥和充足的积分；此技能不提供或支付积分。
- 结果是AI生成的草稿，旨在作为起点，而不是最终的、事实检查的可交付成果 — 使用前请审查内容。
- 此技能不替代环境特定的验证或专家审查。如果缺少API密钥、必需的输入或预期的成本/范围，请停止并请求澄清。
- 速率限制适用（Fast PPT 10/分钟，Nano Banana 6/分钟）；每20-30秒轮询一次异步作业，而不是紧密循环。
