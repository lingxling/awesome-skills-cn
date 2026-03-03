---
name: notion-research-documentation
description: 研究跨 Notion 并综合为结构化文档；当从多个 Notion 来源收集信息以生成简报、比较或带有引用的报告时使用。
metadata:
  short-description: 研究 Notion 内容并生成简报/报告
---

# 研究与文档

拉取相关的 Notion 页面，综合发现，并发布清晰的简报或报告（带有引用和到源的链接）。

## 快速开始

1) 使用 `Notion:notion-search` 通过有针对性的查询查找来源；与用户确认范围。
2) 通过 `Notion:notion-fetch` 获取页面；注意关键部分并捕获引用（`reference/citations.md`）。
3) 使用 `reference/format-selection-guide.md` 选择输出格式（简报、摘要、比较、综合报告）。
4) 使用 `Notion:notion-create-pages` 在 Notion 中起草，使用匹配的模板（快速、摘要、比较、综合）。
5) 链接来源并添加引用/参考部分；随着新信息的到达，使用 `Notion:notion-update-page` 更新。

## 工作流程

### 0) 如果任何 MCP 调用由于 Notion MCP 未连接而失败，请暂停并设置它：
1. 添加 Notion MCP：
   - `codex mcp add notion --url https://mcp.notion.com/mcp`
2. 启用远程 MCP 客户端：
   - 在 `config.toml` 中设置 `[features].rmcp_client = true` **或**运行 `codex --enable rmcp_client`
3. 使用 OAuth 登录：
   - `codex mcp login notion`

成功登录后，用户必须重新启动 codex。您应该完成您的回答并告诉他们，当他们再次尝试时可以从步骤 1 继续。

### 1) 收集来源
- 首先搜索（`Notion:notion-search`）；优化查询，如果出现多个结果，请要求用户确认。
- 获取相关页面（`Notion:notion-fetch`），浏览事实、指标、声明、约束和日期。
- 跟踪每个源 URL/ID 以便稍后引用；对于关键事实更喜欢直接引用。

### 2) 选择格式
- 快速阅读 → 快速简报。
- 单主题深入 → 研究摘要。
- 选项权衡 → 比较。
- 深入/执行就绪 → 综合报告。
- 何时选择每一个，请参阅 `reference/format-selection-guide.md`。

### 3) 综合
- 写入之前先概述；按主题/问题分组发现。
- 使用源 ID 注明证据；标记缺口或矛盾。
- 保持用户目标在视野中（决策、摘要、计划、建议）。

### 4) 创建文档
- 在 `reference/` 中选择匹配的模板（简报、摘要、比较、综合）并调整它。
- 使用 `Notion:notion-create-pages` 创建页面；包括标题、摘要、关键发现、支持证据以及相关时的建议/后续步骤。
- 内联添加引用和参考部分；链接回源页面。

### 5) 最终确定和交接
- 添加亮点、风险和未决问题。
- 如果用户需要后续，请在页面中创建任务或检查清单；如果适用，链接任何任务数据库条目。
- 更新时使用 `Notion:notion-update-page` 分享简短的变更日志或状态。

## 参考资料和示例

- `reference/` — 搜索策略、格式选择、模板和引用规则（例如，`advanced-search.md`、`format-selection-guide.md`、`research-summary-template.md`、`comparison-template.md`、`citations.md`）。
- `examples/` — 端到端的演练（例如，`competitor-analysis.md`、`technical-investigation.md`、`market-research.md`、`trip-planning.md`）。
