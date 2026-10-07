---
name: bdistill-knowledge-extraction
description: 从 AI 模型中提取结构化领域知识 — 从会话中或通过 Ollama 从本地开源模型提取。不需要 API 密钥。
category: ai-research
risk: safe
source: community
date_added: "2026-03-20"
author: FrancyJGLisboa
tags: [ai, knowledge-extraction, domain-specific, data-moat, mcp, reference-data]
tools: [claude, cursor, codex, copilot]
---

# 知识提取

从任何 AI 模型中提取结构化、质量评分的领域知识 — 从会话中的闭源模型（无需 API 密钥）或本地通过 Ollama 的开源模型。

## 概述

bdistill 将您的 AI 订阅会话转变为复合知识库。代理回答有针对性的领域问题，bdistill 对响应进行结构化和质量评分，输出累积成可搜索、可导出的参考数据集。

对抗模式挑战代理的声明 — 强制提供证据、纠正和承认的限制 — 产生验证的知识条目。

## 何时使用此技能

- 当您需要任何领域（医学、法律、金融、网络安全）的结构化参考数据时使用
- 当构建查询表、Q&A 数据集或研究语料库时使用
- 当为传统 ML 模型生成训练数据时使用（回归、分类 — 不是竞争 LLMs）
- 当您想要跨模型的领域知识比较时使用

## 工作原理

### 步骤 1：安装

```bash
pip install bdistill
claude mcp add bdistill -- bdistill-mcp   # Claude Code
```

### 步骤 2：在会话中提取知识

```
/distill medical cardiology                    # 预设领域
/distill --custom kubernetes docker helm       # 自定义术语
/distill --adversarial medical                 # 带对抗验证
```

### 步骤 3：搜索、导出、复合

```bash
bdistill kb list                               # 显示所有领域
bdistill kb search "atrial fibrillation"       # 关键词搜索
bdistill kb export -d medical -f csv           # 导出为电子表格
bdistill kb export -d medical -f markdown      # 可读的知识文档
```

## 输出格式

结构化参考 JSONL — 不是训练数据：

```json
{
  "question": "What causes myocardial infarction?",
  "answer": "Myocardial infarction results from acute coronary artery occlusion...",
  "domain": "medical",
  "category": "cardiology",
  "tags": ["mechanistic", "evidence-based"],
  "quality_score": 0.73,
  "confidence": 1.08,
  "validated": true,
  "source_model": "Claude Sonnet 4"
}
```

## 表格 ML 数据生成

为传统 ML 模型生成结构化训练数据：

```
/schema sepsis | hr:float, bp:float, temp:float, wbc:float | risk:category[low,moderate,high,critical]
```

导出为 CSV 格式，可用于 pandas/sklearn。每一行都跟踪 source_model 以进行跨模型分析。

## 本地模型提取 (Ollama)

对于在本地运行的开源模型：

```bash
# 从 https://ollama.com 安装 Ollama
ollama serve
ollama pull qwen3:4b

bdistill extract --domain medical --model qwen3:4b
```

## 安全性和安全注意事项

- 会话内提取使用您现有的订阅 — 无需额外的 API 密钥
- 本地提取完全在您的机器上通过 Ollama 运行
- 没有数据发送到外部服务
- 输出是参考数据，不是 LLM 训练格式

## 相关技能

- `@bdistill-behavioral-xray` - X-ray 模型的行为模式

## 限制

- 仅在任务明确符合上述范围时使用此技能。
- 不要将输出作为特定于环境的验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并要求澄清。
