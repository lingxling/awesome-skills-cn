---
name: Toggl Automation
description: "自动化 Toggl Track 的时间追踪工作流——通过自然语言命令创建时间记录，管理项目、客户、标签和工作区。"
requires:
  mcp:
    - rube
---

# Toggl Automation

直接从 Claude Code 自动化你的 Toggl Track 时间追踪操作。记录时间、管理项目和客户、用标签组织、控制工作区——全部无需离开终端。

**工具包文档：** [composio.dev/toolkits/toggl](https://composio.dev/toolkits/toggl)

---

## 设置

1. 将 Rube MCP 服务器添加到你的 Claude Code 配置中，URL 为：`https://rube.app/mcp`
2. 按提示通过提供的连接链接验证你的 Toggl Track 账户
3. 开始使用自然语言自动化你的时间追踪工作流

---

## 核心工作流

### 1. 创建和停止时间记录

记录带有项目、任务和标签关联的时间，或启动/停止计时器。

**工具：** `TOGGL_CREATE_TIME_ENTRY`、`TOGGL_PATCH_STOP_TIME_ENTRY`

```
在工作区 123456 中为项目 78910 启动一条时间记录，标签为 "meeting" 和 "design"，描述为 "设计评审会议"
```

`TOGGL_CREATE_TIME_ENTRY` 的关键参数：
- `workspace_id`（必填）-- 目标工作区
- `created_with`（必填）-- 客户端应用名称（例如 `"api_client"`）
- `start`（必填）-- ISO 8601 时间戳
- `stop` -- ISO 8601 结束时间；若要让记录保持运行则省略
- `duration` -- 时长（秒）；运行中的记录可省略
- `project_id` -- 关联项目
- `task_id` -- 关联任务
- `tags` -- 标签名称字符串组成的数组
- `description` -- 工作描述
- `billable` -- 是否可计费

`TOGGL_PATCH_STOP_TIME_ENTRY` 的关键参数：
- `workspace_id`（必填）和 `time_entry_id`（必填）

### 2. 管理项目

创建新项目，并列出带有客户详情和分页的现有项目。

**工具：** `TOGGL_CREATE_PROJECT`、`TOGGL_GET_PROJECTS`、`TOGGL_GET_PROJECT_DETAILS`

```
在工作区 123456 中为客户 78910 创建一个名为 "Q1 Marketing Campaign" 的私有可计费项目
```

`TOGGL_CREATE_PROJECT` 的关键参数：
- `workspace_id`（必填）和 `name`（必填）
- `client_id`、`billable`、`is_private`、`active`、`color`
- `estimated_hours`、`rate`、`fixed_fee`、`currency`（高级功能）

`TOGGL_GET_PROJECTS` 的关键参数：
- `workspace_id`（必填）
- `page` / `page_size`（1-200）用于分页
- `since` / `until` -- 用于筛选修改时间的 Unix 时间戳（仅限最近 3 个月）
- `clients: true` 以包含完整的客户详情

### 3. 管理客户

在工作区内创建和列出客户。

**工具：** `TOGGL_CREATE_CLIENT`、`TOGGL_GET_LIST_CLIENTS`

```
列出工作区 123456 中所有活跃客户，然后创建一个名为 "Acme Corp" 的新客户
```

- `TOGGL_CREATE_CLIENT` 需要 `workspace_id` 和 `name`；接受 `notes`、`external_reference`
- `TOGGL_GET_LIST_CLIENTS` 需要 `workspace_id`；支持 `status`（`"active"`、`"archived"`、`"both"`）和 `name`（不区分大小写的搜索）

### 4. 标签和工作区偏好设置

检索用于分类的标签，并检查工作区设置。

**工具：** `TOGGL_GET_TAGS`、`TOGGL_GET_WORKSPACE_PREFERENCES`

```
显示工作区 123456 中的所有标签以及工作区偏好设置
```

- `TOGGL_GET_TAGS` 需要 `workspace_id`；返回标签 ID 和名称
- `TOGGL_GET_WORKSPACE_PREFERENCES` 需要 `workspace_id`；返回定价方案和显示设置

### 5. 工作区发现

列出已认证用户所属的所有工作区。

**工具：** `TOGGL_GET_USER_WORKSPACES`

```
我有权访问哪些 Toggl 工作区？
```

- 不需要参数
- 返回所有工作区及其 ID、名称和元数据
- 使用此工具首先发现其他操作所需的工作区 ID

### 6. 用户项目可见性

列出已认证用户可见的项目。

**工具：** `TOGGL_GET_USER_PROJECTS`

```
显示我所有工作区中我能看到的所有项目
```

- 返回已认证用户有权访问的项目
- 可与 `TOGGL_GET_PROJECTS` 搭配使用，查看工作区范围内的视图

---

## 常见陷阱

- **标签使用名称而非 ID：** `TOGGL_CREATE_TIME_ENTRY` 在 `tags` 数组中接受字符串形式的标签名称，不同于许多使用 ID 的 API。使用 `TOGGL_GET_TAGS` 验证可用的标签名称。
- **`created_with` 为必填项：** 每条时间记录都必须包含 `created_with`（例如 `"api_client"`）。缺失此字段会导致静默失败。
- **时长以秒为单位：** 时间记录上的 `duration` 参数以秒为单位，而不是小时。1 小时 = 3600 秒。
- **`since` 时间戳限制：** `TOGGL_GET_PROJECTS` 上的 `since` 过滤器仅允许最近 3 个月内的时间戳。更早的查询会被拒绝。
- **高级功能受限：** 项目的自定义颜色、模板、固定费用和小时费率需要 Toggl 高级方案。非高级账户使用这些字段时会报错。
- **几乎处处需要工作区 ID：** 几乎所有 Toggl 工具都需要 `workspace_id`。请始终先调用 `TOGGL_GET_USER_WORKSPACES` 来获取它。

---

## 快速参考

| 工具 Slug | 描述 |
|---|---|
| `TOGGL_CREATE_TIME_ENTRY` | 创建时间记录或正在运行的计时器（需要 `workspace_id`、`created_with`、`start`） |
| `TOGGL_PATCH_STOP_TIME_ENTRY` | 停止正在运行的时间记录（需要 `workspace_id`、`time_entry_id`） |
| `TOGGL_GET_PROJECTS` | 分页列出工作区中的项目 |
| `TOGGL_GET_PROJECT_DETAILS` | 获取特定项目的详情 |
| `TOGGL_CREATE_PROJECT` | 创建新项目（需要 `workspace_id`、`name`） |
| `TOGGL_GET_LIST_CLIENTS` | 列出客户，支持 status/name 过滤（需要 `workspace_id`） |
| `TOGGL_CREATE_CLIENT` | 创建新客户（需要 `workspace_id`、`name`） |
| `TOGGL_GET_TAGS` | 列出工作区中的所有标签（需要 `workspace_id`） |
| `TOGGL_GET_WORKSPACE_PREFERENCES` | 获取工作区设置（需要 `workspace_id`） |
| `TOGGL_GET_USER_WORKSPACES` | 列出已认证用户的所有工作区 |
| `TOGGL_GET_USER_PROJECTS` | 列出已认证用户可见的项目 |

---

*由 [Composio](https://composio.dev) 提供支持*
