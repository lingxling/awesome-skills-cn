---
name: notion-knowledge-capture
description: 将对话和决策捕获到结构化的 Notion 页面中；当将聊天/笔记转换为 wiki 条目、操作指南、决策或带有适当链接的 FAQ 时使用。
metadata:
  short-description: 将对话捕获到结构化的 Notion 页面中
---

# 知识捕获

将对话和笔记转换为结构化的、可链接的 Notion 页面，以便于重用。

## 快速开始
1) 澄清要捕获的内容（决策、操作指南、FAQ、学习、文档）和目标受众。
2) 在 `reference/` 中识别正确的数据库/模板（团队 wiki、操作指南、FAQ、决策日志、学习、文档）。
3) 使用 `Notion:notion-search` → `Notion:notion-fetch` 从 Notion 拉取任何先前的上下文（要更新/链接的现有页面）。
4) 使用 `Notion:notion-create-pages` 使用数据库的架构起草页面；包括摘要、上下文、源链接和标签/所有者。
5) 从中心页面和相关记录进行链接；随着源的演变，使用 `Notion:notion-update-page` 更新状态/所有者。

## 工作流程

### 0) 如果任何 MCP 调用由于 Notion MCP 未连接而失败，请暂停并设置它：
1. 添加 Notion MCP：
   - `codex mcp add notion --url https://mcp.notion.com/mcp`
2. 启用远程 MCP 客户端：
   - 在 `config.toml` 中设置 `[features].rmcp_client = true` **或**运行 `codex --enable rmcp_client`
3. 使用 OAuth 登录：
   - `codex mcp login notion`

成功登录后，用户必须重新启动 codex。您应该完成您的回答并告诉他们，当他们再次尝试时可以从步骤 1 继续。

### 1) 定义捕获
- 询问目的、受众、新鲜度以及这是新的还是更新。
- 确定内容类型：决策、操作指南、FAQ、概念/wiki 条目、学习/笔记、文档页面。

### 2) 定位目标
- 使用 `reference/*-database.md` 指南选择正确的数据库；确认必需的属性（标题、标签、所有者、状态、日期、关系）。
- 如果有多个候选数据库，请询问用户使用哪一个；否则，在主 wiki/文档 DB 中创建。

### 3) 提取和结构化
- 从对话中提取事实、决策、行动和理由。
- 对于决策，记录替代方案、理由和结果。
- 对于操作指南/文档，捕获步骤、前置要求、到资产/代码的链接和边缘情况。
- 对于 FAQ，将其表述为带有简明答案和到更深层文档链接的问答。

### 4) 在 Notion 中创建/更新
- 使用正确的 `data_source_id` 通过 `Notion:notion-create-pages`；设置属性（标题、标签、所有者、状态、日期、关系）。
- 使用 `reference/` 中的模板来结构化内容（部分标题、检查清单）。
- 如果更新现有页面，请先获取然后通过 `Notion:notion-update-page` 编辑。

### 5) 链接和展示
- 添加关系到中心页面、相关规格/文档和团队。
- 为未来的读者添加简短的摘要/变更日志。
- 如果存在后续任务，请在相关数据库中创建任务并链接它们。

## 参考资料和示例

- `reference/` — 数据库架构和模板（例如，`team-wiki-database.md`、`how-to-guide-database.md`、`faq-database.md`、`decision-log-database.md`、`documentation-database.md`、`learning-database.md`、`database-best-practices.md`）。
- `examples/` — 实践中的捕获模式（例如，`decision-capture.md`、`how-to-guide.md`、`conversation-to-faq.md`）。
