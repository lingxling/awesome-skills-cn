---
name: Gorgias Automation
description: "自动化 Gorgias 中的电商客户支持工作流 -- 通过自然语言命令管理工单、客户、标签和团队。"
requires:
  mcp:
    - rube
---

# Gorgias Automation

直接从 Claude Code 自动化你的 Gorgias 工单系统操作。创建、更新和分类支持工单，管理客户，组织你的支持团队 -- 全部无需离开终端。

**工具包文档：** [composio.dev/toolkits/gorgias](https://composio.dev/toolkits/gorgias)

---

## 设置

1. 在 Claude Code 配置中添加 Rube MCP 服务器，地址：`https://rube.app/mcp`
2. 收到提示时，通过提供的连接链接认证你的 Gorgias 账户
3. 开始使用自然语言自动化你的支持工作流

---

## 核心工作流

### 1. 列出和筛选工单

获取工单，并可按状态、渠道、受理人、日期范围等进行筛选。

**工具：** `GORGIAS_LIST_TICKETS`

```
List all open tickets from the email channel created in the last 7 days
```

关键参数：
- `status` -- 按工单状态筛选（例如 "open"、"closed"）
- `channel` -- 按渠道筛选（例如 "email"、"chat"）
- `assignee_user_id` / `assignee_team_id` -- 按受理代理或团队筛选
- `created_from` / `created_to` -- ISO 日期范围筛选
- `limit`（最大 100） / `offset` -- 分页控制
- `order_by` / `order_dir` -- 排序选项

### 2. 创建和更新工单

创建新工单，或对现有工单进行受理人、优先级和状态变更的更新。

**工具：** `GORGIAS_CREATE_TICKET`、`GORGIAS_UPDATE_TICKET`、`GORGIAS_GET_TICKET`

```
Create a high-priority ticket for customer 12345 about a missing order with subject "Order #9876 not delivered"
```

- `GORGIAS_CREATE_TICKET` 需要 `customer_id`；支持 `subject`、`status`、`priority`、`channel`、`messages`、`tags`
- `GORGIAS_UPDATE_TICKET` 需要 `ticket_id`；其他字段均为可选的部分更新
- `GORGIAS_GET_TICKET` 通过 `ticket_id` 获取完整的工单详情

### 3. 管理工单标签

为工单添加标签，用于分类、路由和报告。

**工具：** `GORGIAS_ADD_TICKET_TAGS`、`GORGIAS_LIST_TICKET_TAGS`

```
Add tags 101 and 202 to ticket 5678, then show me all tags on that ticket
```

- `GORGIAS_ADD_TICKET_TAGS` 需要 `ticket_id` 和 `tag_ids`（整数数组）
- `GORGIAS_LIST_TICKET_TAGS` 需要 `ticket_id` 来获取当前标签

### 4. 客户管理

创建新客户或合并重复的客户记录。

**工具：** `GORGIAS_CREATE_CUSTOMER`、`GORGIAS_MERGE_CUSTOMERS`、`GORGIAS_LIST_CUSTOMERS`

```
Create a new customer named "Jane Doe" with email jane@example.com and phone channel
```

- `GORGIAS_CREATE_CUSTOMER` 需要 `name`；支持 `email`、`channels`（包含 `type` 和 `value` 的数组）、`external_id`、`address`、`data`
- `GORGIAS_MERGE_CUSTOMERS` 需要 `source_customer_id` 和 `target_customer_id` -- 源客户会被合并进目标客户
- `GORGIAS_LIST_CUSTOMERS` 支持带筛选条件获取客户列表

### 5. 团队和账户操作

列出团队、获取账户信息，并查看工单自定义字段。

**工具：** `GORGIAS_LIST_TEAMS`、`GORGIAS_GET_TEAM`、`GORGIAS_GET_ACCOUNT`、`GORGIAS_LIST_TICKET_FIELD_VALUES`

```
Show me all support teams in our Gorgias account
```

- `GORGIAS_GET_ACCOUNT` 返回账户级别的指标和配置
- `GORGIAS_LIST_TEAMS` / `GORGIAS_GET_TEAM` 管理团队查找
- `GORGIAS_LIST_TICKET_FIELD_VALUES` 返回指定工单的自定义字段值

### 6. 活动和事件跟踪

监控工单活动和客户事件历史。

**工具：** `GORGIAS_LIST_EVENTS`

```
List recent events to see what activity has happened across our support queue
```

- `GORGIAS_LIST_EVENTS` 提供带筛选选项的活动时间线

---

## 常见陷阱

- **需要分页：**`GORGIAS_LIST_TICKETS` 使用 `limit`/`offset` 分页。未循环遍历所有页面会遗漏较早的工单，导致数据不完整。
- **筛选条件要具体：**`GORGIAS_LIST_TICKETS` 的筛选条件缺失或过于宽泛，会导出过多数据或遗漏所需的报告时间窗口。进行限定时间范围的查询时，务必设置 `created_from`/`created_to`。
- **自定义字段是独立的：**关键业务 KPI 可能只存在于自定义字段中。必须显式查询 `GORGIAS_LIST_TICKET_FIELD_VALUES` 才能将其包含进来。
- **速率限制：**`GORGIAS_LIST_TICKETS` 及相关接口的高频导出可能触发 Gorgias 速率限制。请添加退避重试机制，并从上次的 offset 处继续。
- **认证错误：**任何 Gorgias 工具返回 401/403 响应都表明令牌或权限存在问题。不要把部分数据当作完整数据集处理。

---

## 快速参考

| 工具标识 | 描述 |
|---|---|
| `GORGIAS_LIST_TICKETS` | 带筛选条件（状态、渠道、日期、受理人）列出工单 |
| `GORGIAS_GET_TICKET` | 通过 ID 获取特定工单 |
| `GORGIAS_CREATE_TICKET` | 创建新工单（需要 `customer_id`） |
| `GORGIAS_UPDATE_TICKET` | 更新工单字段（需要 `ticket_id`） |
| `GORGIAS_ADD_TICKET_TAGS` | 为工单添加标签 |
| `GORGIAS_LIST_TICKET_TAGS` | 列出工单上的所有标签 |
| `GORGIAS_LIST_TICKET_FIELD_VALUES` | 列出工单的自定义字段值 |
| `GORGIAS_CREATE_CUSTOMER` | 创建新客户（需要 `name`） |
| `GORGIAS_MERGE_CUSTOMERS` | 合并两个客户记录 |
| `GORGIAS_LIST_CUSTOMERS` | 带筛选条件列出客户 |
| `GORGIAS_LIST_TEAMS` | 列出所有团队 |
| `GORGIAS_GET_TEAM` | 获取特定团队 |
| `GORGIAS_GET_ACCOUNT` | 获取账户信息 |
| `GORGIAS_LIST_EVENTS` | 带筛选条件列出活动事件 |

---

*由 [Composio](https://composio.dev) 提供支持*
