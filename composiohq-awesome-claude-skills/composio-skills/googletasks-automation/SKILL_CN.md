---
name: googletasks-automation
description: "Automate Google Tasks via Rube MCP (Composio): create, list, update, delete, move, and bulk-insert tasks and task lists. Always search tools first for current schemas."
requires:
  mcp: [rube]
---

# Google Tasks Automation via Rube MCP

Create, manage, organize, and bulk-operate on Google Tasks and task lists using Rube MCP (Composio).

**Toolkit docs**: [composio.dev/toolkits/googletasks](https://composio.dev/toolkits/googletasks)

## 前置条件
- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- Active connection via `RUBE_MANAGE_CONNECTIONS` with toolkit `googletasks`
- 始终首先调用 `RUBE_SEARCH_TOOLS` 以获取当前工具架构

## 设置
**获取 Rube MCP**: 在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 响应来验证 Rube MCP 可用
2. Call `RUBE_MANAGE_CONNECTIONS` with toolkit `googletasks`
3. 如果连接未处于 ACTIVE 状态，请按照返回的授权链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## Core Workflows

### 1. List All Task Lists
Use `GOOGLETASKS_LIST_TASK_LISTS` to fetch all available task lists for the authenticated user.
```
Tool: GOOGLETASKS_LIST_TASK_LISTS
Parameters:
  - maxResults: Maximum task lists to return
  - pageToken: Pagination token for next page
```

### 2. Create a New Task
Use `GOOGLETASKS_INSERT_TASK` to add a new task to a specific task list.
```
Tool: GOOGLETASKS_INSERT_TASK
Parameters:
  - tasklist_id (required): ID of the target task list
  - title (required): Task title
  - notes: Task description/notes
  - due: Due date in RFC3339 format (e.g., "2025-01-20T00:00:00.000Z")
  - status: "needsAction" or "completed"
  - task_parent: Parent task ID (to create subtask)
  - task_previous: Previous task ID (for ordering)
```

### 3. List All Tasks Across Lists
Use `GOOGLETASKS_LIST_ALL_TASKS` to fetch tasks across all task lists with optional filters.
```
Tool: GOOGLETASKS_LIST_ALL_TASKS
Parameters:
  - max_tasks_total: Maximum total tasks to return
  - showCompleted: Include completed tasks
  - showDeleted: Include deleted tasks
  - showHidden: Include hidden tasks
  - dueMin / dueMax: Filter by due date range
  - completedMin / completedMax: Filter by completion date
  - updatedMin: Filter by last update time
  - showAssigned: Include assigned tasks
```

### 4. Update an Existing Task
Use `GOOGLETASKS_UPDATE_TASK` to modify a task's title, notes, due date, or status.
```
Tool: GOOGLETASKS_UPDATE_TASK
Parameters:
  - tasklist_id (required): Task list ID
  - task_id (required): Task ID to update
  - title: New title
  - notes: Updated notes
  - due: New due date (RFC3339)
  - status: "needsAction" or "completed"
```

### 5. Bulk Insert Tasks
Use `GOOGLETASKS_BULK_INSERT_TASKS` to create multiple tasks at once in a single operation.
```
Tool: GOOGLETASKS_BULK_INSERT_TASKS
Parameters:
  - tasklist_id (required): Target task list ID
  - tasks (required): Array of task objects (each with title, notes, due, status)
  - batch_size: Number of tasks per batch request
```

### 6. Delete or Clear Tasks
Use `GOOGLETASKS_DELETE_TASK` to remove a specific task, or `GOOGLETASKS_CLEAR_TASKS` to permanently remove all completed tasks from a list.
```
Tool: GOOGLETASKS_DELETE_TASK
Parameters:
  - tasklist_id (required): Task list ID
  - task_id (required): Task ID to delete

Tool: GOOGLETASKS_CLEAR_TASKS
Parameters:
  - tasklist (required): Task list ID to clear completed tasks from
```

## Common Patterns

- **Get task list ID first**: Always start with `GOOGLETASKS_LIST_TASK_LISTS` to discover available task lists and their IDs before creating or listing tasks.
- **List then update**: Use `GOOGLETASKS_LIST_ALL_TASKS` or `GOOGLETASKS_LIST_TASKS` to find task IDs, then use `GOOGLETASKS_UPDATE_TASK` to modify them.
- **Mark complete**: Update a task with `status: "completed"` using `GOOGLETASKS_UPDATE_TASK`.
- **Create subtasks**: Use `GOOGLETASKS_INSERT_TASK` with the `task_parent` parameter set to the parent task's ID.
- **Reorder tasks**: Use `GOOGLETASKS_MOVE_TASK` to change a task's position within its list or reparent it.
- **Batch creation**: Use `GOOGLETASKS_BULK_INSERT_TASKS` for creating many tasks at once (e.g., importing from another system).

## 已知陷阱

- Both `tasklist_id` and `task_id` are **required** for `GOOGLETASKS_UPDATE_TASK`, `GOOGLETASKS_DELETE_TASK`, and `GOOGLETASKS_GET_TASK`. You cannot operate on a task without knowing which list it belongs to.
- All date/time strings must be in **RFC3339 format** (e.g., `2025-01-20T00:00:00.000Z`). Other formats will be rejected.
- `GOOGLETASKS_CLEAR_TASKS` permanently deletes all **completed** tasks from a list. This action is irreversible.
- `GOOGLETASKS_LIST_ALL_TASKS` fetches across all lists but results may be paginated -- check for pagination tokens.
- Task list IDs are not the same as task list names. Always resolve names to IDs using `GOOGLETASKS_LIST_TASK_LISTS`.
- The default task list is typically named "My Tasks" but its ID is an opaque string, not "default" or "primary".

## 快速参考
| Action | Tool | Key Parameters |
|--------|------|----------------|
| List task lists | `GOOGLETASKS_LIST_TASK_LISTS` | `maxResults`, `pageToken` |
| List all tasks | `GOOGLETASKS_LIST_ALL_TASKS` | `max_tasks_total`, `showCompleted`, `dueMin` |
| List tasks in a list | `GOOGLETASKS_LIST_TASKS` | `tasklist_id`, `maxResults`, `showCompleted` |
| Get single task | `GOOGLETASKS_GET_TASK` | `tasklist_id`, `task_id` |
| Create task | `GOOGLETASKS_INSERT_TASK` | `tasklist_id`, `title`, `notes`, `due` |
| Bulk create tasks | `GOOGLETASKS_BULK_INSERT_TASKS` | `tasklist_id`, `tasks` |
| Update task | `GOOGLETASKS_UPDATE_TASK` | `tasklist_id`, `task_id`, `title`, `status` |
| Delete task | `GOOGLETASKS_DELETE_TASK` | `tasklist_id`, `task_id` |
| Move/reorder task | `GOOGLETASKS_MOVE_TASK` | `tasklist_id`, `task_id` |
| Clear completed | `GOOGLETASKS_CLEAR_TASKS` | `tasklist` |

---
*由 [Composio](https://composio.dev) 提供支持*
