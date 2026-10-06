---
name: FreshBooks Automation
description: "FreshBooks 自动化：在 FreshBooks 云会计中管理企业、项目、时间跟踪和计费"
requires:
  mcp: [rube]
---

# FreshBooks Automation

自动化 FreshBooks 操作，包括列出企业、管理项目、跟踪时间，以及为中小型企业会计监控预算。

**工具包文档：** [composio.dev/toolkits/freshbooks](https://composio.dev/toolkits/freshbooks)

---

## 设置

此技能需要连接到 `https://rube.app/mcp` 的**Rube MCP 服务器**。

在执行任何工具之前，请确保 `freshbooks` 工具包存在有效连接。如果没有有效连接，请通过 `RUBE_MANAGE_CONNECTIONS` 发起连接。

---

## 核心工作流

### 1. 列出企业

获取与已认证用户关联的所有企业。此响应中的 `business_id` 是大多数其他 FreshBooks API 调用所必需的。

**工具：** `FRESHBOOKS_LIST_BUSINESSES`

**参数：** 无需参数。

**示例：**
```
工具：FRESHBOOKS_LIST_BUSINESSES
参数：{}
```

**输出：** 返回企业成员资格信息，包括用户有权访问的所有企业，以及其在每个企业中的角色。

> **重要：** 在执行特定项目的操作之前，始终先调用此工具以获取有效的 `business_id`。

---

### 2. 列出和筛选项目

获取某个企业的所有项目，支持全面的筛选和排序选项。

**工具：** `FRESHBOOKS_LIST_PROJECTS`

**关键参数：**
- `business_id`（必需） —— 从 `FRESHBOOKS_LIST_BUSINESSES` 获取的企业 ID
- `active` —— 按活跃状态筛选：`true`（仅活跃）、`false`（仅非活跃），不传则返回全部
- `complete` —— 按完成状态筛选：`true`（已完成）、`false`（未完成），不传则返回全部
- `sort_by` —— 排序方式："created_at"、"due_date" 或 "title"
- `updated_since` —— RFC3339 格式的 UTC 日期时间，例如 "2026-01-01T00:00:00Z"
- `include_logged_duration` —— `true` 表示包含每个项目的总记录时长（以秒为单位）
- `skip_group` —— `true` 表示省略团队成员/邀请数据（缩小响应体积）

**示例：**
```
工具：FRESHBOOKS_LIST_PROJECTS
参数：
  business_id: 123456
  active: true
  complete: false
  sort_by: "due_date"
  include_logged_duration: true
```

**使用场景：**
- 获取所有项目以进行时间跟踪或开票
- 按客户、状态或日期范围查找项目
- 监控项目完成情况和预算跟踪
- 获取团队分配和项目分组

---

### 3. 监控活跃项目

通过筛选活跃且未完成的项目来跟踪项目进度和预算。

**步骤：**
1. 调用 `FRESHBOOKS_LIST_BUSINESSES` 获取 `business_id`
2. 以 `active: true`、`complete: false`、`include_logged_duration: true` 调用 `FRESHBOOKS_LIST_PROJECTS`
3. 分析每个项目的已记录时长与预算的对比

---

### 4. 查看最近更新的项目

使用 `updated_since` 筛选条件检查最近的项目活动。

**步骤：**
1. 调用 `FRESHBOOKS_LIST_BUSINESSES` 获取 `business_id`
2. 以设置了截止日期时间的 `updated_since` 调用 `FRESHBOOKS_LIST_PROJECTS`
3. 查看返回的项目以了解最近的变更

**示例：**
```
工具：FRESHBOOKS_LIST_PROJECTS
参数：
  business_id: 123456
  updated_since: "2026-02-01T00:00:00Z"
  sort_by: "created_at"
```

---

## 推荐执行计划

1. **获取企业 ID**，调用 `FRESHBOOKS_LIST_BUSINESSES`
2. **列出项目**，使用获取到的 `business_id` 调用 `FRESHBOOKS_LIST_PROJECTS`
3. **按需筛选**，使用 `active`、`complete`、`updated_since` 和 `sort_by` 参数

---

## 已知陷阱

| 陷阱 | 详情 |
|---------|--------|
| **需要 business_id** | 大多数 FreshBooks 操作都需要 `business_id`。始终先调用 `FRESHBOOKS_LIST_BUSINESSES` 来获取它。 |
| **日期格式** | `updated_since` 参数必须是 RFC3339 格式："2026-01-01T00:00:00Z"。其他格式将导致失败。 |
| **分页结果** | 项目列表响应是分页的。请检查响应中是否有更多页面。 |
| **空结果** | 如果不存在项目或没有项目匹配应用的筛选条件，将返回空列表。这不是错误。 |
| **已记录时长单位** | 当 `include_logged_duration` 为 true 时，时长以秒为单位返回。显示时需转换为小时（除以 3600）。 |

---

## 快速参考

| 工具标识 | 描述 |
|-----------|-------------|
| `FRESHBOOKS_LIST_BUSINESSES` | 列出已认证用户的所有企业 |
| `FRESHBOOKS_LIST_PROJECTS` | 列出某个企业的项目，支持筛选和排序 |

---

*由 [Composio](https://composio.dev) 提供支持*
