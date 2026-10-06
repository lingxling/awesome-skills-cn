---
name: Xero Automation
description: "Xero Automation：管理 Xero 中的发票、联系人、付款、银行交易和账户，实现云端记账"
requires:
  mcp: [rube]
---

# Xero Automation

自动化 Xero 会计操作，包括管理发票、联系人、付款、银行交易和会计科目表，服务于小型企业记账。

**工具包文档：** [composio.dev/toolkits/xero](https://composio.dev/toolkits/xero)

---

## 设置

此技能需要连接到 `https://rube.app/mcp` 的 **Rube MCP 服务器**。

在执行任何工具之前，请确保 `xero` 工具包存在有效连接。如果没有活动连接，请通过 `RUBE_MANAGE_CONNECTIONS` 发起一个。

**多租户：** 如果你管理多个 Xero 组织，请先调用 `XERO_GET_CONNECTIONS` 列出活动租户，获取后续调用所需的正确 `tenant_id`。

---

## 核心工作流

### 1. 列出和筛选发票

按状态、联系人、日期范围检索发票，并支持分页。

**工具：** `XERO_LIST_INVOICES`

**关键参数：**
- `Statuses` —— 以逗号分隔的状态筛选：`"DRAFT"`、`"SUBMITTED"`、`"AUTHORISED"`、`"PAID"`
- `ContactIDs` —— 以逗号分隔的联系人 ID，用于筛选
- `InvoiceIDs` —— 以逗号分隔的发票 ID，用于筛选
- `where` —— OData 风格的筛选器，例如 `"Status==\"AUTHORISED\" AND Total>100"`
- `order` —— 排序表达式，例如 `"Date DESC"`、`"InvoiceNumber ASC"`
- `page` —— 分页页码
- `If-Modified-Since` —— UTC 时间戳；仅返回此日期之后被修改的发票
- `tenant_id` —— Xero 组织 ID（省略时使用第一个租户）

**示例：**
```
Tool: XERO_LIST_INVOICES
Arguments:
  Statuses: "AUTHORISED,PAID"
  order: "Date DESC"
  page: 1
```

---

### 2. 管理联系人

检索和搜索用于发票和交易的联系人。

**工具：** `XERO_GET_CONTACTS`

**关键参数：**
- `searchTerm` —— 跨 Name、FirstName、LastName、Email、ContactNumber 的不区分大小写搜索
- `ContactID` —— 按 ID 获取单个联系人
- `where` —— OData 筛选器，例如 `"ContactStatus==\"ACTIVE\""`
- `page`、`pageSize` —— 分页控制
- `order` —— 排序，例如 `"UpdatedDateUTC DESC"`
- `includeArchived` —— 设为 `true` 时包含已归档的联系人
- `summaryOnly` —— 设为 `true` 时返回轻量级响应

**示例：**
```
Tool: XERO_GET_CONTACTS
Arguments:
  searchTerm: "acme"
  page: 1
  pageSize: 25
```

> **注意：** 在高交易量账户中，某些 `where` 筛选条件（例如 `IsCustomer`、`IsSupplier`）可能会被 Xero 拒绝。此时应回退到使用 `searchTerm` 或分页。

---

### 3. 创建付款

通过创建付款记录，将发票与银行账户关联起来。

**工具：** `XERO_CREATE_PAYMENT`

**关键参数：**
- `InvoiceID`（必填）—— 付款所适用的 Xero 发票 ID
- `AccountID`（必填）—— 付款所使用的银行账户 ID
- `Amount`（必填）—— 付款金额（数字）
- `Date` —— 付款日期，格式为 `YYYY-MM-DD`
- `Reference` —— 付款参考或描述
- `CurrencyRate` —— 外币付款的汇率

**示例：**
```
Tool: XERO_CREATE_PAYMENT
Arguments:
  InvoiceID: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
  AccountID: "b2c3d4e5-f6a7-8901-bcde-f12345678901"
  Amount: 1500.00
  Date: "2026-02-11"
  Reference: "Payment for INV-0042"
```

---

### 4. 创建银行交易

记录支出（付款支出）或收入（资金进账）银行交易。

**工具：** `XERO_CREATE_BANK_TRANSACTION`

**关键参数：**
- `Type`（必填）—— `"SPEND"`（付款支出）或 `"RECEIVE"`（资金进账）
- `ContactID`（必填）—— Xero 联系人 ID
- `BankAccountCode`（必填）—— 会计科目表中的银行账户代码
- `LineItems`（必填）—— 行项目数组，每个包含：
  - `Description`（必填）—— 行项目描述
  - `UnitAmount`（必填）—— 单价
  - `AccountCode`（必填）—— 用于分类的账户代码
  - `Quantity` —— 数量（默认 1）
  - `TaxType` —— 税种：`"OUTPUT"`、`"INPUT"`、`"NONE"`
- `Date` —— 交易日期，格式为 `YYYY-MM-DD`
- `Reference` —— 交易参考
- `Status` —— `"AUTHORISED"` 或 `"DELETED"`
- `CurrencyCode` —— 例如 `"USD"`、`"EUR"`

**示例：**
```
Tool: XERO_CREATE_BANK_TRANSACTION
Arguments:
  Type: "SPEND"
  ContactID: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
  BankAccountCode: "090"
  LineItems: [
    {
      "Description": "Office supplies",
      "UnitAmount": 75.00,
      "AccountCode": "429",
      "Quantity": 1,
      "TaxType": "INPUT"
    }
  ]
  Date: "2026-02-11"
  Reference: "Feb office supplies"
```

---

### 5. 列出付款和银行交易

查看现有的付款和银行交易历史。

**工具：**
- `XERO_LIST_PAYMENTS` —— 列出将发票与银行交易关联起来的付款
- `XERO_LIST_BANK_TRANSACTIONS` —— 列出支出/收入银行交易

**通用参数：**
- `where` —— OData 筛选器，例如 `"Status==\"AUTHORISED\""`
- `order` —— 排序表达式，例如 `"Date DESC"`
- `page` —— 分页页码
- `If-Modified-Since` —— 自某时间戳以来的增量更新
- `tenant_id` —— 组织 ID

---

### 6. 查看会计科目表和连接

**工具：**
- `XERO_LIST_ACCOUNTS` —— 检索用于分类交易的所有账户代码
- `XERO_GET_CONNECTIONS` —— 列出活动的 Xero 租户连接
- `XERO_LIST_ATTACHMENTS` —— 列出某个实体（发票、联系人等）上的附件

---

## 常见陷阱

| 陷阱 | 详情 |
|---------|--------|
| **多租户路由** | 如果省略 `tenant_id`，则使用第一个已连接的租户。管理多个组织时，务必使用 `XERO_GET_CONNECTIONS` 验证正确的租户。 |
| **高交易量账户的筛选拒绝** | 在大型账户中，某些 `where` 筛选条件如 `IsCustomer`/`IsSupplier` 可能会被拒绝。此时应回退到使用 `searchTerm` 配合分页。 |
| **OData 筛选语法** | 在 OData 筛选器中使用双等号（`==`），例如 `Status==\"AUTHORISED\"`。单个 `=` 会导致错误。 |
| **需要分页** | 大多数列表端点会对结果分页。务必检查是否存在更多页面，并持续获取直到完整。 |
| **日期格式** | 所有日期必须为 `YYYY-MM-DD` 格式。`If-Modified-Since` 的时间戳必须是完整的 ISO 8601 UTC 日期时间。 |
| **银行账户代码** | 银行交易中的 `BankAccountCode` 必须与会计科目表中的有效代码匹配。使用 `XERO_LIST_ACCOUNTS` 来发现有效代码。 |

---

## 快速参考

| 工具标识 | 描述 |
|-----------|-------------|
| `XERO_LIST_INVOICES` | 列出发票，支持筛选和分页 |
| `XERO_GET_CONTACTS` | 检索和搜索联系人 |
| `XERO_CREATE_PAYMENT` | 创建将发票与银行账户关联的付款 |
| `XERO_CREATE_BANK_TRANSACTION` | 记录支出或收入银行交易 |
| `XERO_LIST_PAYMENTS` | 列出付款记录 |
| `XERO_LIST_BANK_TRANSACTIONS` | 列出银行交易 |
| `XERO_LIST_ACCOUNTS` | 检索会计科目表 |
| `XERO_GET_CONNECTIONS` | 列出活动的 Xero 租户连接 |
| `XERO_LIST_ATTACHMENTS` | 列出某个实体上的附件 |

---

*由 [Composio](https://composio.dev) 提供支持*
