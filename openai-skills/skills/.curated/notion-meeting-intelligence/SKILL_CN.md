---
name: notion-meeting-intelligence
description: 使用 Notion 上下文和 Codex 研究准备会议材料；当收集上下文、起草议程/预读以及为与会者定制材料时使用。
metadata:
  short-description: 使用 Notion 上下文和定制的议程准备会议
---

# 会议智能

通过拉取 Notion 上下文、定制议程/预读并使用 Codex 研究来丰富内容，准备会议。

## 快速开始

1) 确认会议目标、与会者、日期/时间以及所需的决策。
2) 收集上下文：使用 `Notion:notion-search` 搜索，然后使用 `Notion:notion-fetch` 获取（先前的笔记、规格、OKR、决策）。
3) 通过 `reference/template-selection-guide.md` 选择正确的模板（状态、决策、规划、回顾、1:1、头脑风暴）。
4) 使用 `Notion:notion-create-pages` 在 Notion 中起草议程/预读，嵌入源链接和所有者/时间框。
5) 使用 Codex 研究丰富（行业洞察、基准、风险）并随着计划的更改使用 `Notion:notion-update-page` 更新页面。

## 工作流程

### 0) 如果任何 MCP 调用由于 Notion MCP 未连接而失败，请暂停并设置它：
1. 添加 Notion MCP：
   - `codex mcp add notion --url https://mcp.notion.com/mcp`
2. 启用远程 MCP 客户端：
   - 在 `config.toml` 中设置 `[features].rmcp_client = true` **或**运行 `codex --enable rmcp_client`
3. 使用 OAuth 登录：
   - `codex mcp login notion`

成功登录后，用户必须重新启动 codex。您应该完成您的回答并告诉他们，当他们再次尝试时可以从步骤 1 继续。

### 1) 收集输入
- 询问目标、预期结果/决策、与会者、持续时间、日期/时间以及先前的材料。
- 搜索 Notion 以获取相关文档、过去的笔记、规格和行动项（`Notion:notion-search`），然后获取关键页面（`Notion:notion-fetch`）。
- 提前捕获阻塞/风险和未决问题。

### 2) 选择格式
- 状态/更新 → 状态模板。
- 决策/批准 → 决策模板。
- 规划（冲刺/项目）→ 规划模板。
- 回顾/反馈 → 回顾模板。
- 1:1 → 一对一模板。
- 头脑风暴 → 头脑风暴模板。
- 使用 `reference/template-selection-guide.md` 确认。

### 3) 构建议程/预读
- 从 `reference/` 中的选定模板开始并调整部分（上下文、目标、议程、每个项目的所有者/时间框、决策、风险、准备询问）。
- 包括到拉取的 Notion 页面的链接以及任何必需的预读。
- 为每个议程项目分配所有者；调用时间框和预期输出。

### 4) 用研究丰富
- 在有帮助的地方添加简明的 Codex 研究：市场/行业事实、基准、风险、最佳实践。
- 保持声明带有源链接的引用；将事实与意见分开。

### 5) 最终确定和分享
- 为后续添加后续步骤和所有者。
- 如果出现任务，请在相关的 Notion 数据库中创建/链接任务。
- 当详细信息更改时通过 `Notion:notion-update-page` 更新页面；如果进行多次编辑，请保持简短的变更日志。

## 参考资料和示例

- `reference/` — 模板选择器和会议模板（例如，`template-selection-guide.md`、`status-update-template.md`、`decision-meeting-template.md`、`sprint-planning-template.md`、`one-on-one-template.md`、`retrospective-template.md`、`brainstorming-template.md`）。
- `examples/` — 端到端的会议准备（例如，`executive-review.md`、`project-decision.md`、`sprint-planning.md`、`customer-meeting.md`）。
