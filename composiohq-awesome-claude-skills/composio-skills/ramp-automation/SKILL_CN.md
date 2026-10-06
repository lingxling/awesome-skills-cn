---
name: Ramp Automation
description: "Ramp Automation：通过 Ramp 平台管理企业卡交易、报销、用户以及费用跟踪"
requires:
  mcp: [rube]
---

# Ramp Automation

自动化 Ramp 企业财务操作，包括检索交易、管理报销、搜索费用、查看卡片详情，以及列出用户，用于费用管理和会计工作流。

**工具包文档：** [composio.dev/toolkits/ramp](https://composio.dev/toolkits/ramp)

---

## 设置

此技能需要连接 **Rube MCP 服务器**，地址为 `https://rube.app/mcp`。

在执行任何工具之前，请确保 `ramp` 工具包存在有效连接。如果没有有效连接，请通过 `RUBE_MANAGE_CONNECTIONS` 发起一个。

---

## 核心工作流

### 1. 列出所有交易

检索所有企业卡交易，并提供全面的过滤选项。

**工具：** `RAMP_GET_ALL_TRANSACTIONS`

**关键参数：**
- `from_date` —— 此日期之后的交易（ISO 8601 日期时间格式）
- `to_date` —— 此日期之前的交易（ISO 8601 日期时间格式，默认：今天）
- `user_id` —— 按用户 UUID 过滤
- `card_id` —— 按实体卡 UUID 过滤
- `department_id` —— 按部门 UUID 过滤
- `merchant_id` —— 按商户 UUID 过滤
- `entity_id` —— 按业务实体 UUID 过滤
- `min_amount` / `max_amount` —— 金额范围过滤（美元）
- `state` —— 交易状态；设为 `"ALL"` 以包含被拒绝的交易
- `approval_status` —— 按审批状态过滤
- `sync_status` —— 按 ERP 同步状态过滤（优先于 `sync_ready` 和 `has_no_sync_commits`）
- `has_no_sync_commits` —— `true` 表示未同步的交易
- `sync_ready` —— `true` 表示准备同步到 ERP 的交易
- `requires_memo` —— `true` 表示缺少必要备注的交易
- `include_merchant_data` —— `true` 表示包含来自商户的完整购买数据
- `page_size` —— 每页结果数（2--100，默认：20）
- `start` —— 分页游标：上一页最后一个实体的 ID
- `order_by_date_desc` / `order_by_date_asc` —— 按日期排序
- `order_by_amount_desc` / `order_by_amount_asc` —— 按金额排序

**示例：**
```
Tool: RAMP_GET_ALL_TRANSACTIONS
Arguments:
  from_date: "2026-02-01T00:00:00Z"
  to_date: "2026-02-11T23:59:59Z"
  page_size: 50
  order_by_date_desc: true
```

---

### 2. 搜索交易

按商户名称、备注或其他交易详情搜索交易。

**工具：** `RAMP_SEARCH_TRANSACTIONS`

**关键参数：**
- `query`（必填） —— 用于搜索商户名称、备注或其他详情的文本
- `RAMP_GET_ALL_TRANSACTIONS` 中的所有过滤参数在此同样可用

**示例：**
```
Tool: RAMP_SEARCH_TRANSACTIONS
Arguments:
  query: "AWS"
  from_date: "2026-01-01T00:00:00Z"
  page_size: 25
```

---

### 3. 获取交易详情

检索特定交易的完整详情，包括商户详情、收据、会计代码以及争议信息。

**工具：** `RAMP_GET_TRANSACTION`

**关键参数：**
- `transaction_id`（必填） —— 交易的 ID

**示例：**
```
Tool: RAMP_GET_TRANSACTION
Arguments:
  transaction_id: "txn_abc123def456"
```

---

### 4. 管理报销

列出并检索报销记录，用于审批工作流和费用分析。

**工具：**
- `RAMP_LIST_REIMBURSEMENTS` —— 列出报销并支持过滤
- `RAMP_GET_REIMBURSEMENT` —— 获取特定报销的完整详情

**`RAMP_LIST_REIMBURSEMENTS` 的关键参数：**
- `user_id` —— 按员工 UUID 过滤
- `entity_id` —— 按业务实体 UUID 过滤
- `from_date` / `to_date` —— 创建日期的日期范围
- `from_submitted_at` / `to_submitted_at` —— 提交日期的日期范围
- `from_transaction_date` / `to_transaction_date` —— 底层交易日期范围
- `awaiting_approval_by_user_id` —— 按等待特定审批人审批的报销过滤
- `sync_status` —— 按 ERP 同步状态过滤
- `has_no_sync_commits` —— `true` 表示未同步的报销
- `sync_ready` —— `true` 表示准备同步的报销
- `direction` —— `"BUSINESS_TO_USER"`（默认）或 `"USER_TO_BUSINESS"`（偿还）
- `page_size` —— 每页结果数（2--100，默认：20）
- `start` —— 分页游标

**示例：**
```
Tool: RAMP_LIST_REIMBURSEMENTS
Arguments:
  from_date: "2026-02-01T00:00:00Z"
  sync_ready: true
  page_size: 50
```

---

### 5. 列出用户并获取我的交易

查看组织用户以及个人交易历史。

**工具：**
- `RAMP_LIST_USERS` —— 按部门、角色、位置、实体列出并过滤用户
- `RAMP_GET_MY_TRANSACTIONS` —— 获取已认证用户的交易

**`RAMP_LIST_USERS` 的关键参数：**
- `department_id` —— 按部门 UUID 过滤
- `role` —— 按用户角色过滤
- `email` —— 按电子邮件地址过滤
- `employee_id` —— 按员工 ID 过滤
- `entity_id` —— 按业务实体 UUID 过滤
- `location_id` —— 按位置 UUID 过滤
- `page_size` —— 每页结果数（2--100，默认：20）

**示例：**
```
Tool: RAMP_LIST_USERS
Arguments:
  role: "ADMIN"
  page_size: 50
```

---

### 6. 查看卡片详情和会计字段

检索卡片信息以及自定义会计字段配置。

**工具：**
- `RAMP_GET_CARD` —— 获取详细的卡片信息（消费限额、持卡人、发卡状态）
- `RAMP_FETCH_CUSTOM_ACCOUNTING_FIELD` —— 获取自定义会计字段定义

---

## 已知问题

| 问题 | 详情 |
|---------|--------|
| **需要分页** | 所有列表端点返回分页结果。使用上一页最后一个实体的 ID 作为 `start` 参数进行迭代。 |
| **日期格式** | 所有日期参数必须是 ISO 8601 日期时间格式（例如 `"2026-02-11T00:00:00Z"`）。纯日期字符串会失败。 |
| **sync_status 优先级** | 设置 `sync_status` 时，它会优先于 `has_no_sync_commits` 和 `sync_ready` 参数。 |
| **金额过滤以美元计** | `min_amount` 和 `max_amount` 以美元计。过滤时请确保货币上下文正确。 |
| **state=ALL 用于已拒绝交易** | 默认情况下，被拒绝的交易会被排除。设置 `state: "ALL"` 以将其包含在结果中。 |
| **page_size 范围限制** | 必须在 2 到 100 之间。默认值为 20。超出此范围的值会导致错误。 |

---

## 快速参考

| 工具 Slug | 描述 |
|-----------|-------------|
| `RAMP_GET_ALL_TRANSACTIONS` | 列出所有交易并支持过滤 |
| `RAMP_SEARCH_TRANSACTIONS` | 按文本查询搜索交易 |
| `RAMP_GET_TRANSACTION` | 获取特定交易的详情 |
| `RAMP_GET_MY_TRANSACTIONS` | 获取已认证用户的交易 |
| `RAMP_LIST_REIMBURSEMENTS` | 列出报销并支持过滤 |
| `RAMP_GET_REIMBURSEMENT` | 获取特定报销的详情 |
| `RAMP_LIST_USERS` | 列出组织用户 |
| `RAMP_GET_CARD` | 获取卡片详情 |
| `RAMP_FETCH_CUSTOM_ACCOUNTING_FIELD` | 获取自定义会计字段配置 |

---

*由 [Composio](https://composio.dev) 提供支持*
