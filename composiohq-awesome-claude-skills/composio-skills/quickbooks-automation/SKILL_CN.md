---
name: QuickBooks Automation
description: "QuickBooks Automation：在 QuickBooks Online 中管理发票、客户、账户以及付款，以简化记账流程"
requires:
  mcp: [rube]
---

# QuickBooks Automation

自动化 QuickBooks Online 操作，包括创建发票、管理客户、查询账户，以及为财务报告列出发票。

**工具包文档：** [composio.dev/toolkits/quickbooks](https://composio.dev/toolkits/quickbooks)

---

## 设置

此技能需要连接 **Rube MCP 服务器**，地址为 `https://rube.app/mcp`。

在执行任何工具之前，请确保 `quickbooks` 工具包存在有效连接。如果没有有效连接，请通过 `RUBE_MANAGE_CONNECTIONS` 发起一个。

---

## 核心工作流

### 1. 创建发票

为客户创建包含明细行项目的新发票。

**工具：** `QUICKBOOKS_CREATE_INVOICE`

**关键参数：**
- `customer_id`（必填） —— 客户的 ID（CustomerRef.value）
- `lines`（必填） —— 行项目对象数组。每个对象必须包含：
  - `DetailType` —— 例如 `"SalesItemLineDetail"`
  - `Amount` —— 行项目总额
  - `SalesItemLineDetail` —— 包含 `ItemRef` 的对象，其中含有 `value`（项目 ID）
- `minorversion` —— 可选的 API 版本参数

**示例：**
```
Tool: QUICKBOOKS_CREATE_INVOICE
Arguments:
  customer_id: "21"
  lines: [
    {
      "DetailType": "SalesItemLineDetail",
      "Amount": 150.00,
      "SalesItemLineDetail": {
        "ItemRef": {"value": "1", "name": "Services"}
      }
    }
  ]
```

**前置条件：** 使用 `QUICKBOOKS_READ_CUSTOMER` 解析客户 ID，或使用 `QUICKBOOKS_CREATE_CUSTOMER` 创建客户。使用 `QUICKBOOKS_QUERY_ACCOUNT` 解析项目/账户 ID。

---

### 2. 管理客户

创建和读取客户记录。

**工具：**
- `QUICKBOOKS_CREATE_CUSTOMER` —— 创建新客户
- `QUICKBOOKS_READ_CUSTOMER` —— 按 ID 读取客户

**`QUICKBOOKS_CREATE_CUSTOMER` 的关键参数：**
- `display_name` —— 显示名称（在客户、供应商、员工之间必须唯一；最多 500 字符）
- `given_name` —— 名（最多 100 字符）
- `family_name` —— 姓（最多 100 字符）
- `middle_name` —— 中间名（最多 100 字符）
- `title` —— 称谓，例如 `"Mr."`、`"Dr."`（最多 16 字符）
- `suffix` —— 名称后缀，例如 `"Jr."`（最多 16 字符）

> `display_name`、`title`、`given_name`、`middle_name`、`family_name` 或 `suffix` 中至少需要提供一项。

**`QUICKBOOKS_READ_CUSTOMER` 的关键参数：**
- `customer_id`（必填） —— 要读取的客户 ID

**示例：**
```
Tool: QUICKBOOKS_CREATE_CUSTOMER
Arguments:
  display_name: "Acme Corporation"
  given_name: "John"
  family_name: "Doe"
```

---

### 3. 查询和读取账户

检索账户信息，用于发票行项目和财务报告。

**工具：**
- `QUICKBOOKS_QUERY_ACCOUNT` —— 对账户执行查询
- `QUICKBOOKS_READ_ACCOUNT` —— 按 ID 读取特定账户

**`QUICKBOOKS_QUERY_ACCOUNT` 的关键参数：**
- `query`（必填） —— 类似 SQL 的查询字符串，例如 `"SELECT * FROM Account WHERE AccountType = 'Income'"`

**示例：**
```
Tool: QUICKBOOKS_QUERY_ACCOUNT
Arguments:
  query: "SELECT * FROM Account WHERE AccountType = 'Income' MAXRESULTS 10"
```

---

### 4. 列出和过滤发票

检索发票，支持可选的分页和过滤。

**工具：** `QUICKBOOKS_LIST_INVOICES`

**步骤：**
1. 使用分页参数调用 `QUICKBOOKS_LIST_INVOICES`
2. 使用 `start_position` 和 `max_results` 对结果进行分页
3. 根据需要按特定条件过滤

---

## 推荐执行方案

1. **解析客户**：使用 `QUICKBOOKS_READ_CUSTOMER`（如果已有客户 ID）或使用 `QUICKBOOKS_CREATE_CUSTOMER` 创建客户
2. **解析项目/收入账户**：使用 `QUICKBOOKS_QUERY_ACCOUNT` 和 `QUICKBOOKS_READ_ACCOUNT` 获取发票行项目所需的账户或项目 ID
3. **创建发票**：使用 `QUICKBOOKS_CREATE_INVOICE`，传入已解析的 `customer_id` 和格式正确的行项目
4. **验证创建结果**：使用 `QUICKBOOKS_LIST_INVOICES` 按 ID 或 DocNumber 找到新发票

---

## 已知问题

| 问题 | 详情 |
|---------|--------|
| **无效引用** | 如果 `customer_id` 或 `ItemRef.value` 指向不存在或非活动的记录，`QUICKBOOKS_CREATE_INVOICE` 会失败。请始终先解析 ID。 |
| **行项目校验** | 错误的 `DetailType` 或缺失的 `SalesItemLineDetail` 字段会在创建发票时导致模式/校验错误。 |
| **分页** | `QUICKBOOKS_LIST_INVOICES` 使用 `start_position` 和 `max_results`。分页设置不完整可能会在较大的账本中遗漏发票。 |
| **同步令牌** | 任何后续编辑都需要来自最新发票读取结果的 `SyncToken`。过期的同步令牌会导致更新被拒绝。 |
| **速率限制** | QuickBooks 强制执行每分钟和每日的 API 上限。高频运行时应包含退避策略以避免限流错误。 |
| **DisplayName 唯一性** | 客户的 `display_name` 在所有 Customer、Vendor 和 Employee 对象之间必须唯一。重复会导致创建失败。 |

---

## 快速参考

| 工具 Slug | 描述 |
|-----------|-------------|
| `QUICKBOOKS_CREATE_INVOICE` | 创建包含行项目的新发票 |
| `QUICKBOOKS_READ_CUSTOMER` | 按 ID 读取客户记录 |
| `QUICKBOOKS_CREATE_CUSTOMER` | 创建新客户记录 |
| `QUICKBOOKS_QUERY_ACCOUNT` | 使用类似 SQL 的语法查询账户 |
| `QUICKBOOKS_READ_ACCOUNT` | 按 ID 读取特定账户 |
| `QUICKBOOKS_LIST_INVOICES` | 列出发票并支持分页 |

---

*由 [Composio](https://composio.dev) 提供支持*
