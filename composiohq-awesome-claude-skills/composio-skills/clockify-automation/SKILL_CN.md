---
name: Clockify Automation
description: "自动化 Clockify 中的时间跟踪工作流——通过自然语言命令创建和管理时间条目、工作区和用户。"
requires:
  mcp:
    - rube
---

# Clockify Automation

直接从 Claude Code 自动化你的 Clockify 时间跟踪操作。记录时间条目、查询历史数据、管理工作区，并审计团队活动——全部无需离开你的终端。

**工具包文档：** [composio.dev/toolkits/clockify](https://composio.dev/toolkits/clockify)

---

## 设置

1. 将 Rube MCP 服务器添加到你的 Claude Code 配置中，URL 为：`https://rube.app/mcp`
2. 按提示通过提供的连接链接验证你的 Clockify 账户
3. 开始使用自然语言自动化你的时间跟踪工作流

---

## 核心工作流

### 1. 创建时间条目

记录时间，关联项目、任务和标签，并设置计费状态。

**工具：** `CLOCKIFY_CREATE_TIME_ENTRY`

```
在工作区 64a687e3 中记录项目 64a687e2 的 2 小时工作，从今天 UTC 上午 9 点开始，描述为 "API development"
```

关键参数：
- `workspaceId`（必填）—— 创建条目所在的工作区
- `start`（必填）—— ISO 8601 格式的开始时间（例如 `2026-02-11T09:00:00Z`）
- `end` —— ISO 8601 格式的结束时间；省略则创建一个正在运行的计时器
- `projectId` —— 关联某个项目
- `taskId` —— 关联某个任务
- `description` —— 工作描述（0-3000 个字符）
- `tagIds` —— 标签 ID 数组
- `billable` —— 该条目是否计费
- `customFieldValues` —— 自定义字段条目数组，包含 `customFieldId` 和 `value`

### 2. 查询时间条目

检索历史时间条目，用于报告、审计和开具发票。

**工具：** `CLOCKIFY_GET_TIME_ENTRIES`

```
获取工作区 xyz789 中用户 abc123 在 2026 年 1 月的所有时间条目
```

关键参数：
- `workspaceId`（必填）—— 要查询的工作区
- `userId`（必填）—— 要检索其条目的用户
- `start` / `end` —— ISO 8601 日期范围筛选
- `project` —— 按项目 ID 筛选
- `task` —— 按任务 ID 筛选
- `tags` —— 以逗号分隔的标签 ID
- `description` —— 文本筛选（部分匹配）
- `hydrated` —— 设为 `true` 以获取完整的项目/任务/标签对象，而非仅 ID
- `in-progress` —— 设为 `true` 仅返回正在运行的计时器
- `page` / `page-size` —— 分页（默认每页 50 条）

### 3. 删除时间条目

移除错误、重复或已取消的时间条目。

**工具：** `CLOCKIFY_DELETE_TIME_ENTRY`

```
从工作区 64a687e3 中删除时间条目 5b715448
```

- 需要 `workspaceId` 和 `id`（时间条目 ID）
- 用于清理错误导入或重复数据

### 4. 管理工作区

列出经身份验证的用户所属的所有工作区。

**工具：** `CLOCKIFY_GET_ALL_MY_WORKSPACES`

```
显示我所有的 Clockify 工作区
```

- 可选 `roles` 筛选——角色数组，如 `["WORKSPACE_ADMIN", "OWNER"]`
- 在创建或查询条目之前，使用此工具发现工作区 ID

### 5. 用户信息

检索当前用户详情并列出工作区成员。

**工具：** `CLOCKIFY_GET_CURRENTLY_LOGGED_IN_USER_INFO`、`CLOCKIFY_FIND_ALL_USERS_ON_WORKSPACE`

```
我以谁的身份登录？然后列出工作区 64a687e3 中的所有用户
```

- `CLOCKIFY_GET_CURRENTLY_LOGGED_IN_USER_INFO` 返回经身份验证用户的个人资料（无需参数）
- `CLOCKIFY_FIND_ALL_USERS_ON_WORKSPACE` 需要 `workspaceId`；支持 `name`、`email` 筛选和分页（`page`、`page-size` 最多 100）

### 6. 正在运行的计时器管理

通过在创建时省略 `end` 来启动计时器，或检查正在运行的条目。

**工具：** `CLOCKIFY_CREATE_TIME_ENTRY`、`CLOCKIFY_GET_TIME_ENTRIES`

```
在工作区 xyz 中为项目 abc 启动计时器，描述为 "Working on bug fix"
```

- 创建时省略 `end` 即可启动一个正在运行的计时器
- 使用 `CLOCKIFY_GET_TIME_ENTRIES` 配合 `in-progress: true` 来检查是否有计时器在运行

---

## 常见陷阱

- **工作区和用户 ID 是必需的：** 大多数 Clockify 工具都需要 `workspaceId` 和 `userId`。请始终先调用 `CLOCKIFY_GET_ALL_MY_WORKSPACES` 和 `CLOCKIFY_GET_CURRENTLY_LOGGED_IN_USER_INFO` 来解析这些 ID。
- **ISO 8601 时间戳：** 所有时间参数都必须采用带时区的 ISO 8601 格式（例如 `2026-02-11T09:00:00Z`）。省略时区会导致不可预测的行为。
- **正在运行的计时器：** 一次只能运行一个计时器。如果另一个计时器已处于活动状态，创建不带 `end` 的新条目将失败。请先停止现有计时器。
- **分页默认值：** `CLOCKIFY_GET_TIME_ENTRIES` 默认每页 50 条。要完整导出数据，请循环遍历各页，直到不再返回结果。
- **标签 ID 是工作区范围的：** 一个工作区的标签 ID 不能在另一个工作区中使用。请始终在目标工作区的上下文中解析标签。

---

## 快速参考

| 工具标识 | 描述 |
|---|---|
| `CLOCKIFY_CREATE_TIME_ENTRY` | 创建时间条目或启动计时器（需要 `workspaceId`、`start`） |
| `CLOCKIFY_GET_TIME_ENTRIES` | 列出带筛选条件的时间条目（需要 `workspaceId`、`userId`） |
| `CLOCKIFY_DELETE_TIME_ENTRY` | 删除时间条目（需要 `workspaceId`、`id`） |
| `CLOCKIFY_GET_ALL_MY_WORKSPACES` | 列出经身份验证用户的所有工作区 |
| `CLOCKIFY_GET_CURRENTLY_LOGGED_IN_USER_INFO` | 获取当前用户的个人资料信息 |
| `CLOCKIFY_FIND_ALL_USERS_ON_WORKSPACE` | 列出工作区中的所有用户（需要 `workspaceId`） |

---

*由 [Composio](https://composio.dev) 提供支持*
