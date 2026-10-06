---
name: Harvest Automation
description: "自动化 Harvest 中的工时跟踪、项目管理和开票工作流 —— 通过自然语言命令记录工时，管理项目、客户和任务。"
requires:
  mcp:
    - rube
---

# Harvest Automation

直接从 Claude Code 自动化你的 Harvest 工时跟踪操作。记录工时条目、管理项目和客户、创建任务，并提取报告数据 —— 全程无需离开终端。

**工具包文档：** [composio.dev/toolkits/harvest](https://composio.dev/toolkits/harvest)

---

## 设置

1. 将 Rube MCP 服务器添加到你的 Claude Code 配置中，URL 为：`https://rube.app/mcp`
2. 在提示时，通过提供的连接链接认证你的 Harvest 账户
3. 开始用自然语言自动化你的工时跟踪工作流

---

## 核心工作流

### 1. 记录和管理工时条目

创建、列出、更新和获取工时条目，以进行准确的计费和报告。

**工具：** `HARVEST_CREATE_TIME_ENTRY`、`HARVEST_LIST_TIME_ENTRIES`、`HARVEST_GET_TIME_ENTRY`、`HARVEST_UPDATE_TIME_ENTRY`

```
为项目 12345 的任务 67890 记录今天 3.5 小时的开发工作
```

`HARVEST_CREATE_TIME_ENTRY` 的关键参数：
- `project_id`（必填）—— 要记录工时的项目
- `task_id`（必填）—— 该任务必须已分配给该项目
- `spent_date`（必填）—— YYYY-MM-DD 格式的日期
- `hours` —— 总工时（用于基于时长的账户）
- `started_time` / `ended_time` —— 用于基于时间戳的账户
- `notes` —— 工作内容描述

`HARVEST_LIST_TIME_ENTRIES` 的关键参数：
- `from_date` / `to` —— 日期范围过滤（YYYY-MM-DD）
- `project_id`、`client_id`、`task_id`、`user_id` —— 实体过滤
- `is_billed` / `is_running` —— 状态过滤
- `page` / `per_page`（最大 2000）—— 分页

### 2. 管理项目

创建新项目并列出现有项目，包含客户和计费配置。

**工具：** `HARVEST_CREATE_PROJECT`、`HARVEST_LIST_PROJECTS`、`HARVEST_GET_PROJECT`

```
为客户 456 创建一个名为“Website Redesign”的可计费项目，按任务计费并设置项目预算
```

`HARVEST_CREATE_PROJECT` 的关键参数：
- `name`、`client_id`、`is_billable`、`bill_by`、`budget_by`（均为必填）
- `bill_by` 选项：`"Project"`、`"Tasks"`、`"People"`、`"none"`
- `budget_by` 选项：`"project"`、`"project_cost"`、`"task"`、`"task_fees"`、`"person"`、`"none"`
- 可选：`budget`、`hourly_rate`、`starts_on`、`ends_on`、`is_fixed_fee`

### 3. 管理客户

创建和列出项目所归属的客户。

**工具：** `HARVEST_CREATE_CLIENT`、`HARVEST_LIST_CLIENTS`

```
列出我们 Harvest 账户中所有的活跃客户
```

- `HARVEST_CREATE_CLIENT` 需要 `name`；可接受 `address`、`currency`、`is_active`
- `HARVEST_LIST_CLIENTS` 支持 `is_active` 过滤和分页（`per_page` 最大 2000）

### 4. 管理任务

创建和列出可复用的任务类型，用于工时跟踪。

**工具：** `HARVEST_CREATE_TASK`、`HARVEST_LIST_TASKS`

```
创建一个名为“Code Review”的新可计费任务，默认费率为每小时 150 美元
```

- `HARVEST_CREATE_TASK` 需要 `name`；可接受 `billable_by_default`、`default_hourly_rate`、`is_active`、`is_default`
- `HARVEST_LIST_TASKS` 支持 `is_active`、`is_default` 过滤和分页（`per_page` 最大 100）
- 任务名称在所有任务（活跃和归档的）中必须唯一

### 5. 工时条目报告

按日期范围和过滤条件提取工时条目，用于计费汇总和利用率报告。

**工具：** `HARVEST_LIST_TIME_ENTRIES`、`HARVEST_GET_TIME_ENTRY`

```
显示 2026 年 1 月项目 789 的所有未结算工时条目
```

- 使用 `from_date` 和 `to` 划定日期窗口
- 使用 `is_billed: false` 过滤未结算条目
- 组合 `project_id`、`user_id`、`client_id` 进行多维度报告
- 使用 `page` 和 `per_page` 分页以获取完整数据集

### 6. 更新和修正工时条目

修改现有工时条目以修正工时、重新分配项目或更新备注。

**工具：** `HARVEST_UPDATE_TIME_ENTRY`

```
将工时条目 123456 的工时改为 4.0，并添加备注“Completed API integration”
```

- 需要 `time_entry_id`
- 支持部分更新 —— 仅需包含要修改的字段
- 可更新 `hours`、`notes`、`project_id`、`task_id`、`spent_date`、`started_time`、`ended_time`

---

## 已知坑点

- **任务分配很重要：** 创建工时条目时，`task_id` 必须对应实际已分配给指定 `project_id` 的任务。请用项目任务分配端点验证，而不仅仅依赖 `HARVEST_LIST_TASKS`（该接口返回的是全局任务）。
- **时长 vs. 时间戳跟踪：** Harvest 账户被配置为基于时长或基于时间戳两种跟踪方式之一。在基于时间戳的账户中 `hours` 会被忽略；在基于时长的账户中 `started_time`/`ended_time` 会被忽略。
- **分页限制各不相同：** `HARVEST_LIST_TIME_ENTRIES` 和 `HARVEST_LIST_CLIENTS` 每页最多支持 2000 条，但 `HARVEST_LIST_PROJECTS` 和 `HARVEST_LIST_TASKS` 每页上限为 100 条。
- **日期格式一致性：** 所有日期参数必须使用 `YYYY-MM-DD` 格式。`updated_since` 过滤器使用带时区的 ISO 8601 格式。
- **项目必填字段：** `HARVEST_CREATE_PROJECT` 需要五个字段：`name`、`client_id`、`is_billable`、`bill_by` 和 `budget_by`。缺少任何一个都会导致校验错误。

---

## 快速参考

| 工具标识 | 描述 |
|---|---|
| `HARVEST_LIST_TIME_ENTRIES` | 按日期、项目、客户、用户过滤列出工时条目 |
| `HARVEST_CREATE_TIME_ENTRY` | 记录新的工时条目（需要 `project_id`、`task_id`、`spent_date`） |
| `HARVEST_GET_TIME_ENTRY` | 按 ID 获取特定工时条目 |
| `HARVEST_UPDATE_TIME_ENTRY` | 更新现有工时条目（需要 `time_entry_id`） |
| `HARVEST_LIST_PROJECTS` | 列出项目，可选客户过滤 |
| `HARVEST_CREATE_PROJECT` | 创建带计费配置的新项目 |
| `HARVEST_GET_PROJECT` | 按 ID 获取特定项目 |
| `HARVEST_LIST_CLIENTS` | 按活跃/非活跃状态列出客户 |
| `HARVEST_CREATE_CLIENT` | 创建新客户（需要 `name`） |
| `HARVEST_LIST_TASKS` | 列出可复用的任务类型 |
| `HARVEST_CREATE_TASK` | 创建新任务类型（需要 `name`） |

---

*Powered by [Composio](https://composio.dev)*
