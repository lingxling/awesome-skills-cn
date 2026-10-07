---
name: clarvia-aeo-check
description: "使用 Clarvia AEO（Agent Experience Optimization）对任何 MCP 服务器、API 或 CLI 进行 Agent 就绪性评分。在将工具添加到工作流之前，搜索 15,400+ 个索引工具。"
category: tool-quality
risk: safe
source: community
date_added: "2026-03-27"
author: digitamaz
tags: [mcp, aeo, tool-quality, agent-readiness, api-scoring, clarvia]
tools: [claude, cursor, windsurf, cline]
---

# Clarvia AEO 检查

## 概述

在向 Agent 工作流添加任何 MCP 服务器、API 或 CLI 工具之前，使用 Clarvia 对其 Agent 就绪性进行评分。Clarvia 在四个 AEO 维度上评估 15,400+ 个 AI 工具：API 可访问性、数据结构化、Agent 兼容性和信任信号。

## 先决条件

将 Clarvia MCP 服务器添加到你的配置：

```json
{
  "mcpServers": {
    "clarvia": {
      "command": "npx",
      "args": ["-y", "clarvia-mcp-server"]
    }
  }
}
```

## 何时使用此技能

- 在将新 MCP 服务器添加到配置之前评估它时使用
- 在为同一工作比较两个工具时使用
- 在构建动态选择工具的 Agent 时使用
- 当你想找到类别中质量最高的工具时使用

## 工作原理

### 步骤 1：对特定工具进行评分

要求 Claude 按 URL 或名称对任何工具进行评分：

```
Score https://github.com/example/my-mcp-server for agent-readiness
```

Clarvia 返回一个 0-100 的 AEO 分数，以及四个维度的细分。

### 步骤 2：按类别搜索工具

```
Find the top-rated database MCP servers using Clarvia
```

从 15,400+ 个索引工具中返回排序结果。

### 步骤 3：工具间对比

```
Compare supabase-mcp vs firebase-mcp using Clarvia
```

返回并排的评分细分以及建议。

### 步骤 4：查看排行榜

```
Show me the top 10 MCP servers for authentication using Clarvia
```

## 示例

### 示例 1：安装前评估

```
Before I add this MCP server to my config, score it:
https://github.com/example/new-tool

Use the clarvia aeo_score tool and tell me if it's agent-ready.
```

### 示例 2：找到类别中最佳工具

```
I need an MCP server for web scraping. Use Clarvia to find the 
top-rated options and compare the top 3.
```

### 示例 3：CI/CD 质量门

添加到你的 CI 管道中，使用 GitHub Action：

```yaml
- uses: clarvia-project/clarvia-action@v1
  with:
    url: https://your-api.com
    fail-under: 70
```

## AEO 分数解释

| 分数 | 评分 | 含义 |
|-------|--------|---------|
| 90-100 | Agent 原生 | 专为 Agent 使用而构建 |
| 70-89 | Agent 友好 | 工作良好、细微差距 |
| 50-69 | Agent 兼容 | 工作但需要改进 |
| 30-49 | Agent 部分 | 重大限制 |
| 0-29 | 非 Agent 就绪 | 避免用于 Agent 工作流 |

## 最佳实践

- ✅ 在向长期运行的 Agent 工作流添加工具前对其进行评分
- ✅ 使用 Clarvia 排行榜发现你未曾考虑的替代方案
- ✅ 定期重新检查分数 — 工具会随时间改进
- ❌ 不要跳过"众所周知"工具的评分 — 即使受欢迎的工具也可能评分较低
- ❌ 不要在生产 Agent 管道中使用评分低于 50 的工具，除非理解限制

## 常见陷阱

- **问题**：Clarvia 返回工具"未找到"
  **解决方案**：尝试直接通过 `aeo_score` 按 URL 扫描 — Clarvia 会按需对其进行评分

- **问题**：我信任的工具分数似乎很低
  **解决方案**：使用 `get_score_breakdown` 查看哪些维度较弱，并决定它们是否对你的用例重要

## 相关技能

- `@mcp-builder` - 构建在 AEO 中评分良好的新 MCP 服务器
- `@agent-evaluation` - 更广泛的 Agent 质量评估框架

## 限制
- 仅当任务明确与上述范围相符时，才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并要求澄清。
