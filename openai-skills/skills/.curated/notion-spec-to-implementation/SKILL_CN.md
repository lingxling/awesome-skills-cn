---
name: notion-spec-to-implementation
description: 将 Notion 规格转换为实施计划、任务和进度跟踪；当实施 PRD/功能规格并从它们创建 Notion 计划 + 任务时使用。
metadata:
  short-description: 将 Notion 规格转换为实施计划、任务和进度跟踪
---

# 规格到实施

将 Notion 规格转换为链接的实施计划、任务和持续的状态更新。

## 快速开始

1) 使用 `Notion:notion-search` 定位规格，然后使用 `Notion:notion-fetch` 获取它。
2) 使用 `reference/spec-parsing.md` 解析需求和歧义。
3) 使用 `Notion:notion-create-pages` 创建计划页面（选择一个模板：快速 vs 完整）。
4) 查找任务数据库，确认架构，然后使用 `Notion:notion-create-pages` 创建任务。
5) 链接规格 ↔ 计划 ↔ 任务；使用 `Notion:notion-update-page` 保持状态当前。

## 工作流程

### 0) 如果任何 MCP 调用由于 Notion MCP 未连接而失败，请暂停并设置它：
1. 添加 Notion MCP：
   - `codex mcp add notion --url https://mcp.notion.com/mcp`
2. 启用远程 MCP 客户端：
   - 在 `config.toml` 中设置 `[features].rmcp_client = true` **或**运行 `codex --enable rmcp_client`
3. 使用 OAuth 登录：
   - `codex mcp login notion`

成功登录后，用户必须重新启动 codex。您应该完成您的回答并告诉他们，当他们再次尝试时可以从步骤 1 继续。

### 1) 定位和阅读规格
- 首先搜索（`Notion:notion-search`）；如果有多个命中，请询问用户使用哪一个。
- 获取页面（`Notion:notion-fetch`）并扫描需求、验收标准、约束和优先级。有关提取模式，请参阅 `reference/spec-parsing.md`。
- 在继续之前在澄清块中捕获缺口/假设。

### 2) 选择计划深度
- 简单更改 → 使用 `reference/quick-implementation-plan.md`。
- 多阶段功能/迁移 → 使用 `reference/standard-implementation-plan.md`。
- 通过 `Notion:notion-create-pages` 创建计划，包括：概述、链接的规格、需求摘要、阶段、依赖/风险和成功标准。链接回规格。

### 3) 创建任务
- 查找任务数据库（`Notion:notion-search` → `Notion:notion-fetch` 以确认数据源和必需的属性）。`reference/task-creation.md` 中的模式。
- 将任务调整为 1–2 天。使用 `reference/task-creation-template.md` 获取内容（上下文、目标、验收标准、依赖、资源）。
- 设置属性：标题/行动动词、状态、优先级、到规格 + 计划的关系、截止日期/故事点（如果提供）或受让人。
- 使用数据库的 `data_source_id` 通过 `Notion:notion-create-pages` 创建页面。

### 4) 链接工件
- 计划链接到规格；任务链接到计划和规格。
- 可选地使用简短的"实施"部分更新规格，该部分指向使用 `Notion:notion-update-page` 的计划和任务。

### 5) 跟踪进度
- 使用 `reference/progress-tracking.md` 中的节奏。
- 使用 `reference/progress-update-template.md` 发布更新；使用 `reference/milestone-summary-template.md` 关闭阶段。
- 保持计划/任务中的检查清单和状态字段同步；注意阻塞和决策。

## 参考资料和示例

- `reference/` — 解析模式、计划/任务模板、进度节奏（例如，`spec-parsing.md`、`standard-implementation-plan.md`、`task-creation.md`、`progress-tracking.md`）。
- `examples/` — 端到端的演练（例如，`ui-component.md`、`api-feature.md`、`database-migration.md`）。
