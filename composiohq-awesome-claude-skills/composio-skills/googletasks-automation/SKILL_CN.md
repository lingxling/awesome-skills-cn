---
name: googletasks-automation
description: "通过 Rube MCP（Composio）自动化 Google Tasks：创建、列出、更新、删除、移动和批量插入任务及任务列表。始终先搜索工具以获取最新的模式定义。"
requires:
  mcp: [rube]
---

# Google Tasks Automation via Rube MCP

使用 Rube MCP（Composio）创建、管理、整理并批量操作 Google Tasks 及任务列表。

**工具包文档**：[composio.dev/toolkits/googletasks](https://composio.dev/toolkits/googletasks)

## 前置条件
- 必须已连接 Rube MCP（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 对 `googletasks` 工具包建立有效连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 以获取当前的工具模式定义

## 设置
**获取 Rube MCP**：在你的客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。不需要任何 API 密钥 -- 只需添加该端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 能正常响应来验证 Rube MCP 是否可用
2. 对工具包 `googletasks` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接未处于 ACTIVE 状态，按返回的认证链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 列出所有任务列表
使用 `GOOGLETASKS_LIST_TASK_LISTS` 获取已认证用户的所有可用任务列表。
```
Tool: GOOGLETASKS_LIST_TASK_LISTS
Parameters:
  - maxResults: 返回的最大任务列表数量
  - pageToken: 用于下一页的分页令牌
```

### 2. 创建新任务
使用 `GOOGLETASKS_INSERT_TASK` 向指定任务列表添加新任务。
```
Tool: GOOGLETASKS_INSERT_TASK
Parameters:
  - tasklist_id（必填）: 目标任务列表的 ID
  - title（必填）: 任务标题
  - notes: 任务描述/备注
  - due: 截止日期，RFC3339 格式（例如 "2025-01-20T00:00:00.000Z"）
  - status: "needsAction" 或 "completed"
  - task_parent: 父任务 ID（用于创建子任务）
  - task_previous: 前一个任务的 ID（用于排序）
```

### 3. 列出所有列表中的所有任务
使用 `GOOGLETASKS_LIST_ALL_TASKS` 获取所有任务列表中的任务，并可选加过滤条件。
```
Tool: GOOGLETASKS_LIST_ALL_TASKS
Parameters:
  - max_tasks_total: 返回的最大任务总数
  - showCompleted: 是否包含已完成的任务
  - showDeleted: 是否包含已删除的任务
  - showHidden: 是否包含隐藏的任务
  - dueMin / dueMax: 按截止日期范围筛选
  - completedMin / completedMax: 按完成日期筛选
  - updatedMin: 按最后更新时间筛选
  - showAssigned: 是否包含被分配的任务
```

### 4. 更新现有任务
使用 `GOOGLETASKS_UPDATE_TASK` 修改任务的标题、备注、截止日期或状态。
```
Tool: GOOGLETASKS_UPDATE_TASK
Parameters:
  - tasklist_id（必填）: 任务列表 ID
  - task_id（必填）: 要更新的任务 ID
  - title: 新标题
  - notes: 更新后的备注
  - due: 新的截止日期（RFC3339）
  - status: "needsAction" 或 "completed"
```

### 5. 批量插入任务
使用 `GOOGLETASKS_BULK_INSERT_TASKS` 在单次操作中创建多个任务。
```
Tool: GOOGLETASKS_BULK_INSERT_TASKS
Parameters:
  - tasklist_id（必填）: 目标任务列表 ID
  - tasks（必填）: 任务对象数组（每个对象包含 title、notes、due、status）
  - batch_size: 每批请求处理的任务数量
```

### 6. 删除或清空任务
使用 `GOOGLETASKS_DELETE_TASK` 删除特定任务，或使用 `GOOGLETASKS_CLEAR_TASKS` 永久移除列表中所有已完成的任务。
```
Tool: GOOGLETASKS_DELETE_TASK
Parameters:
  - tasklist_id（必填）: 任务列表 ID
  - task_id（必填）: 要删除的任务 ID

Tool: GOOGLETASKS_CLEAR_TASKS
Parameters:
  - tasklist（必填）: 要清空已完成任务的任务列表 ID
```

## 常见模式

- **先获取任务列表 ID**：在创建或列出任务之前，始终先使用 `GOOGLETASKS_LIST_TASK_LISTS` 发现可用的任务列表及其 ID。
- **先列出再更新**：使用 `GOOGLETASKS_LIST_ALL_TASKS` 或 `GOOGLETASKS_LIST_TASKS` 查找任务 ID，然后使用 `GOOGLETASKS_UPDATE_TASK` 修改它们。
- **标记完成**：使用 `GOOGLETASKS_UPDATE_TASK` 将任务的 `status` 更新为 `"completed"`。
- **创建子任务**：使用 `GOOGLETASKS_INSERT_TASK` 并将 `task_parent` 参数设为父任务的 ID。
- **重新排序任务**：使用 `GOOGLETASKS_MOVE_TASK` 更改任务在其列表中的位置，或将其重新归父。
- **批量创建**：使用 `GOOGLETASKS_BULK_INSERT_TASKS` 一次性创建多个任务（例如从其他系统导入）。

## 常见陷阱

- `GOOGLETASKS_UPDATE_TASK`、`GOOGLETASKS_DELETE_TASK` 和 `GOOGLETASKS_GET_TASK` 都**必须**提供 `tasklist_id` 和 `task_id`。在不知道任务所属列表的情况下，无法对任务进行操作。
- 所有日期/时间字符串都必须是 **RFC3339 格式**（例如 `2025-01-20T00:00:00.000Z`）。其他格式会被拒绝。
- `GOOGLETASKS_CLEAR_TASKS` 会永久删除列表中所有**已完成**的任务。此操作不可逆。
- `GOOGLETASKS_LIST_ALL_TASKS` 会跨所有列表获取任务，但结果可能分页 -- 请检查分页令牌。
- 任务列表 ID 与任务列表名称并不相同。始终使用 `GOOGLETASKS_LIST_TASK_LISTS` 将名称解析为 ID。
- 默认任务列表通常名为 "My Tasks"，但其 ID 是一个不透明的字符串，不是 "default" 或 "primary"。

## 快速参考
| 操作 | 工具 | 关键参数 |
|--------|------|----------------|
| 列出任务列表 | `GOOGLETASKS_LIST_TASK_LISTS` | `maxResults`、`pageToken` |
| 列出所有任务 | `GOOGLETASKS_LIST_ALL_TASKS` | `max_tasks_total`、`showCompleted`、`dueMin` |
| 列出列表中的任务 | `GOOGLETASKS_LIST_TASKS` | `tasklist_id`、`maxResults`、`showCompleted` |
| 获取单个任务 | `GOOGLETASKS_GET_TASK` | `tasklist_id`、`task_id` |
| 创建任务 | `GOOGLETASKS_INSERT_TASK` | `tasklist_id`、`title`、`notes`、`due` |
| 批量创建任务 | `GOOGLETASKS_BULK_INSERT_TASKS` | `tasklist_id`、`tasks` |
| 更新任务 | `GOOGLETASKS_UPDATE_TASK` | `tasklist_id`、`task_id`、`title`、`status` |
| 删除任务 | `GOOGLETASKS_DELETE_TASK` | `tasklist_id`、`task_id` |
| 移动/重排任务 | `GOOGLETASKS_MOVE_TASK` | `tasklist_id`、`task_id` |
| 清空已完成 | `GOOGLETASKS_CLEAR_TASKS` | `tasklist` |

---
*由 [Composio](https://composio.dev) 提供支持*
