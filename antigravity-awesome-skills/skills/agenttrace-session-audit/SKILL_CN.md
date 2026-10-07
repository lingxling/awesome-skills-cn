---
name: agenttrace-session-audit
description: "使用 agenttrace 审计本地 AI 编码代理会话，监控成本、工具失败、延迟、异常、健康状态、差异和 CI 门控。"
category: development
risk: safe
source: community
source_repo: luoyuctl/agenttrace
source_type: community
date_added: "2026-05-10"
author: luoyuctl
tags: [ai-coding, observability, cost-tracking, session-analysis]
tools: [claude, cursor, gemini, codex-cli]
license: "MIT"
license_source: "https://github.com/luoyuctl/agenttrace/blob/master/LICENSE"
---

# agenttrace 会话审计

## 概述

使用此技能通过 [agenttrace](https://github.com/luoyuctl/agenttrace) 检查本地 AI 编码代理会话。它重点关注运行背后的过程：令牌和成本峰值、工具失败、重试循环、延迟间隔、异常、健康分数和会话间差异。

agenttrace 采用本地优先的方式，从 Claude Code、Codex CLI、Gemini CLI、Aider、Cursor 导出、OpenCode、Qwen Code、Kimi 和泛型 JSON 或 JSONL 追踪中读取会话日志。

## 何时使用此技能

- 当用户询问 AI 编码运行速度慢、成本高、深度浅或不可靠时使用。
- 在重试失败或可疑任务之前查看本地代理日志时使用。
- 为 AI 辅助编码会话构建轻量级 CI 健康门控时使用。
- 比较两次尝试并查找已更改的工具路径、重试或成本模式时使用。

## 工作原理

### 第 1 步：发现可用会话

当 `agenttrace` 二进制文件在 `PATH` 上可用时，优先使用已安装的 `agenttrace` 二进制文件。如果当前存储库是 `luoyuctl/agenttrace`，请改用 `go run ./cmd/agenttrace`。

```bash
agenttrace --doctor
agenttrace --overview
```

如果未检测到任何会话，请报告 `--doctor` 检查的目录，并要求提供导出的会话文件或日志目录。

### 第 2 步：生成人类可读的审计

当用户希望获得可以检查或共享的简洁报告时，使用 Markdown。

```bash
agenttrace --overview -f markdown -o agenttrace-overview.md
```

在报告中，以风险最高的会话开始，并解释原因：关键异常、重复的工具失败、令牌或成本浪费、长延迟间隔、低健康分数和可疑的浅表会话。

### 第 3 步：检查单个会话或目录

使用最新的会话进行快速检查，或在用户提供一个会话时传递显式导出路径。

```bash
agenttrace --latest
agenttrace --latest -f json
agenttrace path/to/session-or-export.json
agenttrace --overview -d path/to/session-dir
```

### 第 4 步：当语义很重要时比较尝试

即使代理自信地采取了错误的实现路径，令牌和延迟指标也可能看起来很好。当风险是语义偏差时，将追踪审计与针对先前或已知良好尝试的差异进行配对。

查找：

- 与预期任务不同的已更改文件或命令
- 与参考尝试相比缺少的测试或验证步骤
- 围绕相同文件的重复编辑，没有明确的原因
- 来自跳过必要探索的较低成本

### 第 5 步：添加自动化门控

对于 CI 或可重复的团队工作流，使用 JSON 输出或健康阈值。

```bash
agenttrace --overview -f json -o agenttrace-overview.json
agenttrace --overview --fail-under-health 80 --fail-on-critical --max-tool-fail-rate 15
```

根据项目调整阈值。严格的门控对于关键工作流很有用；学习基线时，仅报告命令会更好。

## 示例

### 快速本地审查

```bash
agenttrace --overview
agenttrace --latest
```

在长时间的编码代理运行后使用，以决定下一个提示是否应该拆分任务、避免失败的工具路径、添加缺失的测试或重置上下文。

### CI 健康检查

```bash
agenttrace --overview --fail-under-health 80 --fail-on-critical
```

当代理会话日志在 CI 中可用时使用，团队希望对关键异常或不健康的运行进行简单的保护。

## 最佳实践

- 当会话发现不确定时，从 `--doctor` 开始。
- 明确报告缺失的字段；不要编造成本、模型、延迟或健康数据。
- 将提示、代码和会话内容视为私有本地数据。
- 优先使用 JSON 输出进行自动化，使用 Markdown 输出进行人类审查。
- 使用追踪指标来处理过程失败，使用差异/参考审查来处理语义偏差。

## 限制

- agenttrace 只能分析本地存在或作为导出提供的日志。
- 某些代理不公开足够的字段来推断成本、模型、缓存使用或延迟。
- 健康的追踪指标不能证明最终代码是正确的；仍然要运行测试并审查差异。
- CI 门控应该在团队了解正常基线行为之前作为建议性的。

## 安全与安全性说明

- 除非用户明确批准，否则不要将私有会话日志上传到外部服务。
- 除非用户请求该精确输出路径，否则不要覆盖用户报告。
- 避免打印在提示、工具输出、环境变量或日志中发现的机密。

## 常见陷阱

- **问题：** 找不到任何会话。
  **解决方案：** 运行 `agenttrace --doctor`，然后将 agenttrace 指向导出的文件或日志目录。

- **问题：** 运行看起来成本低、速度快，但产生了错误的重构。
  **解决方案：** 将会话与先前的尝试或已知的良好差异进行比较；仅成本指标会错过语义偏差。

- **问题：** 添加健康门控后 CI 失败过于频繁。
  **解决方案：** 从 JSON 或 Markdown 报告开始，检查正常基线，然后逐步收紧阈值。

## 相关技能

- `@langfuse` - 用于生产 LLM 应用程序追踪和评估。
- `@observability-engineer` - 用于更广泛的服务监控、SLO 和事件工作流。
