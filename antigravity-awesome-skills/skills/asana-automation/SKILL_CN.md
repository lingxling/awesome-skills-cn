---
name: asana-automation
description: "通过 Rube MCP (Composio) 自动化 Asana 任务：任务、项目、部分、团队、工作空间。始终先搜索工具以获取当前架构。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 的 Asana 自动化

通过 Rube MCP 的 Composio Asana 工具包自动化 Asana 操作。

## 前置条件

- Rube MCP 必须连接（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用工具包 `asana` 的活跃 Asana 连接
- 始终首先调用 `RUBE_SEARCH_TOOLS` 以获取当前工具架构

## 设置

**获取 Rube MCP**：在你的客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。不需要 API 密钥 — 只需添加端点，它就能工作。

1. 通过确认 `RUBE_SEARCH_TOOLS` 响应验证 Rube MCP 可用
2. 使用工具包 `asana` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接不是活跃的，请按照返回的授权链接完成 Asana OAuth
4. 在运行任何工作流前确认连接状态显示为活跃

## 核心工作流

### 1. 管理任务

**何时使用**：用户想要创建、搜索、列表或组织任务

**工具序列**：
1. `ASANA_GET_MULTIPLE_WORKSPACES` - 获取工作空间 ID [必需]
2. `ASANA_SEARCH_TASKS_IN_WORKSPACE` - 搜索任务 [可选]
3. `ASANA_GET_TASKS_FROM_A_PROJECT` - 列表项目任务 [可选]
4. `ASANA_CREATE_A_TASK` - 创建新任务 [可选]
5. `ASANA_GET_A_TASK` - 获取任务详情 [可选]
6. `ASANA_CREATE_SUBTASK` - 创建子任务 [可选]
7. `ASANA_GET_TASK_SUBTASKS` - 列表子任务 [可选]

**关键参数**：
- `workspace`：工作空间 GID（搜索/创建需要）
- `projects`：要添加任务到的项目 GID 数组
- `name`：任务名称
- `notes`：任务说明
- `assignee`：被分配者（用户 GID 或邮件）
- `due_on`：截止日期（YYYY-MM-DD）

**陷阱**：
- 工作空间 GID 对大多数操作需要；先获取它
- 任务 GID 作为字符串返回，不是整数
- 搜索是工作空间范围的，不是项目范围的

### 2. 管理项目和部分

**何时使用**：用户想要创建项目、管理部分或组织任务

**工具序列**：
1. `ASANA_GET_WORKSPACE_PROJECTS` - 列表工作空间项目 [可选]
2. `ASANA_GET_A_PROJECT` - 获取项目详情 [可选]
3. `ASANA_CREATE_A_PROJECT` - 创建新项目 [可选]
4. `ASANA_GET_SECTIONS_IN_PROJECT` - 列表部分 [可选]
5. `ASANA_CREATE_SECTION_IN_PROJECT` - 创建新部分 [可选]
6. `ASANA_ADD_TASK_TO_SECTION` - 将任务移到部分 [可选]
7. `ASANA_GET_TASKS_FROM_A_SECTION` - 列表部分中的任务 [可选]

**关键参数**：
- `project_gid`：项目 GID
- `name`：项目或部分名称
- `workspace`：创建时的工作空间 GID
- `task`：部分分配的任务 GID
- `section`：部分 GID

**陷阱**：
- 项目属于工作空间；创建时需要工作空间 GID
- 部分在项目中排序
- `DUPLICATE_PROJECT` 创建一个可选包含任务的副本

### 3. 管理团队和用户

**何时使用**：用户想要列表团队、团队成员或工作空间用户

**工具序列**：
1. `ASANA_GET_TEAMS_IN_WORKSPACE` - 列表工作空间团队 [可选]
2. `ASANA_GET_USERS_FOR_TEAM` - 列表团队成员 [可选]
3. `ASANA_GET_USERS_FOR_WORKSPACE` - 列表所有工作空间用户 [可选]
4. `ASANA_GET_CURRENT_USER` - 获取已认证用户 [可选]
5. `ASANA_GET_MULTIPLE_USERS` - 获取多个用户详情 [可选]

**关键参数**：
- `workspace_gid`：工作空间 GID
- `team_gid`：团队 GID

**陷阱**：
- 用户是工作空间范围的
- 团队成员需要团队 GID

### 4. 平行操作

**何时使用**：用户需要有效地执行批量操作

**工具序列**：
1. `ASANA_SUBMIT_PARALLEL_REQUESTS` - 并行执行多个 API 调用 [必需]

**关键参数**：
- `actions`：带有方法、路径和数据的操作对象数组

**陷阱**：
- 每个操作必须是有效的 Asana API 调用
- 失败的单个请求不会回滚成功的

## 常见模式

### ID 解析

**工作空间名称 -> GID**：
```
1. 调用 ASANA_GET_MULTIPLE_WORKSPACES
2. 按名称查找工作空间
3. 提取 gid 字段
```

**项目名称 -> GID**：
```
1. 用工作空间 GID 调用 ASANA_GET_WORKSPACE_PROJECTS
2. 按名称查找项目
3. 提取 gid 字段
```

### 分页

- Asana 使用带 `offset` 参数的基于光标的分页
- 检查响应中的 `next_page`
- 从 `next_page.offset` 为下一请求传递 `offset`

## 已知陷阱

**GID 格式**：
- 所有 Asana ID 都是字符串（GID），不是整数
- GID 是全局唯一标识符

**工作空间范围**：
- 大多数操作需要工作空间上下文
- 任务、项目和用户是工作空间范围的

## 快速参考

| 任务 | 工具 Slug | 关键参数 |
|------|-----------|------------|
| 列表工作空间 | ASANA_GET_MULTIPLE_WORKSPACES | (无) |
| 搜索任务 | ASANA_SEARCH_TASKS_IN_WORKSPACE | workspace、text |
| 创建任务 | ASANA_CREATE_A_TASK | workspace、name、projects |
| 获取任务 | ASANA_GET_A_TASK | task_gid |
| 创建子任务 | ASANA_CREATE_SUBTASK | parent、name |
| 列表子任务 | ASANA_GET_TASK_SUBTASKS | task_gid |
| 项目任务 | ASANA_GET_TASKS_FROM_A_PROJECT | project_gid |
| 列表项目 | ASANA_GET_WORKSPACE_PROJECTS | workspace |
| 创建项目 | ASANA_CREATE_A_PROJECT | workspace、name |
| 获取项目 | ASANA_GET_A_PROJECT | project_gid |
| 复制项目 | ASANA_DUPLICATE_PROJECT | project_gid |
| 列表部分 | ASANA_GET_SECTIONS_IN_PROJECT | project_gid |
| 创建部分 | ASANA_CREATE_SECTION_IN_PROJECT | project_gid、name |
| 添加到部分 | ASANA_ADD_TASK_TO_SECTION | section、task |
| 部分任务 | ASANA_GET_TASKS_FROM_A_SECTION | section_gid |
| 列表团队 | ASANA_GET_TEAMS_IN_WORKSPACE | workspace_gid |
| 团队成员 | ASANA_GET_USERS_FOR_TEAM | team_gid |
| 工作空间用户 | ASANA_GET_USERS_FOR_WORKSPACE | workspace_gid |
| 当前用户 | ASANA_GET_CURRENT_USER | (无) |
| 平行请求 | ASANA_SUBMIT_PARALLEL_REQUESTS | actions |

## 何时使用

此技能适用于执行概述中描述的工作流或操作。

## 限制

- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
