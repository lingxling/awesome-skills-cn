---
name: bdistill-behavioral-xray
description: X-ray 任何 AI 模型的行为模式 — 拒绝边界、幻觉倾向、推理风格、格式化默认值。不需要 API 密钥。
category: ai-testing
risk: safe
source: community
date_added: "2026-03-20"
author: FrancyJGLisboa
tags: [ai, testing, behavioral-analysis, model-evaluation, red-team, compliance, mcp]
tools: [claude, cursor, codex, copilot]
---

# 行为 X 射线

系统地探测 AI 模型的行为模式并生成可视化报告。AI 代理探测*自己* — 不需要 API 密钥或外部设置。

## 概述

bdistill 的行为 X 射线在 6 个维度上运行 30 个精心设计的探测问题，用行为元数据自动标记每个响应，并将结果编译成带有雷达图和可操作见解的样式化 HTML 报告。

使用它来在使用前了解您的模型、为任务选择比较模型或跟踪行为漂移随时间。

## 何时使用此技能

- 当您想了解 AI 模型的实际行为方式（而非其声称的行为）时使用
- 当为特定任务在模型之间选择时使用
- 当调试意外拒绝、幻觉或格式化问题时使用
- 用于合规性审计 — 在部署边界处记录模型行为
- 用于红队评估 — 跨安全维度的系统边界映射

## 工作原理

### 步骤 1：安装

```bash
pip install bdistill
claude mcp add bdistill -- bdistill-mcp   # Claude Code
```

对于其他工具，在项目配置中将 bdistill-mcp 添加为 MCP 服务器。

### 步骤 2：运行探测

在 Claude Code 中：
```
/xray                          # 完整行为探测（30 个问题）
/xray --dimensions refusal     # 仅探测一个维度
/xray-report                   # 从已完成的探测生成报告
```

在任何配备 MCP 的工具中：
```
"X-ray your behavioral patterns"
"Test your refusal boundaries"
"Generate a behavioral report"
```

## 探测维度

| 维度 | 其测量内容 |
|-----------|-----------------|
| **tool_use** | 何时调用工具与从知识库回答？ |
| **refusal** | 它在哪里绘制安全边界？它是否过度拒绝？ |
| **formatting** | 列表 vs 散文？代码块？长度校准？ |
| **reasoning** | 它是否显示思维链？处理技巧性问题？ |
| **persona** | 身份、语气匹配、在敌意下的镇定 |
| **grounding** | 幻觉抵抗、制造陷阱、知识限制 |

## 输出

一份样式化的 HTML 报告显示：
- 拒绝率、对冲率、思维链使用情况
- 每个维度的分解与条形图
- 带有行为标签的示例响应
- 可操作的见解（例如，"您已经显示 CoT 使用率 85%，无需提示"）

## 最佳实践

- 诚实回答探测问题 — 价值在于真实的行为数据
- 定期在相同模型上运行探测以跟踪行为漂移
- 比较模型间的报告来做出知情的选择决定
- 与行为探测一起使用对抗性知识提取（`/distill --adversarial`）以进行完整的模型分析

## 相关技能

- `@bdistill-knowledge-extraction` - 从任何 AI 模型提取结构化领域知识

## 限制

- 仅在任务明确符合上述范围时使用此技能。
- 不要将输出作为特定于环境的验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并要求澄清。
