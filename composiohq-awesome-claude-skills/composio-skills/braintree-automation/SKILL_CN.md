---
name: Braintree Automation
description: "Braintree 自动化：通过兼容 Stripe 的工具管理客户、订阅、支付方式和交易的支付处理"
requires:
  mcp: [rube]
---

# Braintree 自动化

通过兼容 Stripe 的工具自动化支付处理操作，包括管理客户、订阅、支付方式、余额交易和客户搜索。Composio 平台通过 Stripe 工具包路由 Braintree 支付工作流，实现统一的支付管理。

**工具包文档：** [composio.dev/toolkits/braintree](https://composio.dev/toolkits/braintree)

---

## 设置

此技能需要连接到 `https://rube.app/mcp` 的 **Rube MCP 服务器**。

在执行任何工具之前，请确保 `stripe` 工具包存在活动连接。如果没有活动连接，请通过 `RUBE_MANAGE_CONNECTIONS` 发起一个。

---

## 核心工作流

### 1. 创建和管理客户

创建新客户并检索现有客户详情。

**工具：**
- `STRIPE_CREATE_CUSTOMER` -- 创建新客户
- `STRIPE_GET_CUSTOMERS_CUSTOMER` -- 按 ID 检索客户
- `STRIPE_POST_CUSTOMERS_CUSTOMER` -- 更新现有客户
- `STRIPE_LIST_CUSTOMERS` -- 分页列出客户
- `STRIPE_GET_V1_CUSTOMERS_SEARCH_CUSTOMERS` -- 按邮箱、姓名、元数据搜索客户

**`STRIPE_CREATE_CUSTOMER` 的关键参数：**
- `email` -- 客户的主要邮箱地址
- `name` -- 全名或企业名称
- `phone` -- 带国家代码的电话号码
- `description` -- 内部参考备注
- `address` -- 账单地址对象，包含 `line1`、`city`、`state`、`postal_code`、`country`

**`STRIPE_GET_V1_CUSTOMERS_SEARCH_CUSTOMERS` 的关键参数：**
- `query`（必填） -- Stripe 搜索查询语言。必须使用 `field:value` 语法：
  - `email:'user@example.com'` -- 精确匹配（不区分大小写）
  - `name~'John'` -- 子字符串匹配（最少 3 个字符）
  - `metadata['key']:'value'` -- 元数据搜索
  - `created>1609459200` -- 时间戳比较
  - 可用 `AND` 或 `OR` 组合（最多 10 个子句，不能混用）
- `limit` -- 每页结果数（1--100，默认 10）

**示例：**
```
Tool: STRIPE_CREATE_CUSTOMER
Arguments:
  email: "jane@example.com"
  name: "Jane Doe"
  description: "Enterprise plan customer"
  address: {
    "line1": "123 Main St",
    "city": "San Francisco",
    "state": "CA",
    "postal_code": "94105",
    "country": "US"
  }
```

---

### 2. 管理订阅

创建订阅并查看客户的订阅详情。

**工具：**
- `STRIPE_CREATE_SUBSCRIPTION` -- 为现有客户创建新订阅
- `STRIPE_GET_CUSTOMERS_CUSTOMER_SUBSCRIPTIONS` -- 列出某客户的所有订阅
- `STRIPE_GET_CUSTOMERS_CUSTOMER_SUBS_SUB_EXPOSED_ID` -- 获取特定订阅

**`STRIPE_CREATE_SUBSCRIPTION` 的关键参数：**
- `customer`（必填） -- 客户 ID，例如 `"cus_xxxxxxxxxxxxxx"`
- `items`（必填） -- 订阅项目数组，每项包含：
  - `price` -- 价格 ID，例如 `"price_xxxxxxxxxxxxxx"`（与 `price_data` 二选一）
  - `price_data` -- 内联价格定义，包含 `currency`、`product`、`unit_amount`、`recurring`
  - `quantity` -- 项目数量
- `default_payment_method` -- 支付方式 ID（在试用期或按发票计费时非必填）
- `trial_period_days` -- 试用天数（试用期内无需支付）
- `collection_method` -- `"charge_automatically"`（默认）或 `"send_invoice"`
- `cancel_at_period_end` -- 在计费周期结束时取消（布尔值）

**`STRIPE_GET_CUSTOMERS_CUSTOMER_SUBSCRIPTIONS` 的关键参数：**
- `customer`（必填） -- 客户 ID
- `status` -- 过滤条件：`"active"`、`"all"`、`"canceled"`、`"trialing"`、`"past_due"` 等
- `limit` -- 每页结果数（1--100，默认 10）

**示例：**
```
Tool: STRIPE_CREATE_SUBSCRIPTION
Arguments:
  customer: "cus_abc123"
  items: [{"price": "price_xyz789", "quantity": 1}]
  trial_period_days: 14
```

---

### 3. 管理支付方式

列出并将支付方式附加到客户。

**工具：**
- `STRIPE_GET_CUSTOMERS_CUSTOMER_PAYMENT_METHODS` -- 列出客户的支付方式
- `STRIPE_ATTACH_PAYMENT_METHOD` -- 将支付方式附加到客户

**`STRIPE_GET_CUSTOMERS_CUSTOMER_PAYMENT_METHODS` 的关键参数：**
- `customer`（必填） -- 客户 ID
- `type` -- 按类型过滤：`"card"`、`"sepa_debit"`、`"us_bank_account"` 等
- `limit` -- 每页结果数（1--100，默认 10）

**示例：**
```
Tool: STRIPE_GET_CUSTOMERS_CUSTOMER_PAYMENT_METHODS
Arguments:
  customer: "cus_abc123"
  type: "card"
  limit: 10
```

---

### 4. 查看余额交易

检索客户余额变动的历史记录。

**工具：** `STRIPE_GET_CUSTOMERS_CUSTOMER_BALANCE_TRANSACTIONS`

**关键参数：**
- `customer`（必填） -- 客户 ID
- `created` -- 按创建日期过滤，支持比较运算符：`{"gte": 1609459200}` 或 `{"gt": 1609459200, "lt": 1640995200}`
- `invoice` -- 按相关发票 ID 过滤
- `limit` -- 每页结果数（1--100）
- `starting_after` / `ending_before` -- 分页游标

**示例：**
```
Tool: STRIPE_GET_CUSTOMERS_CUSTOMER_BALANCE_TRANSACTIONS
Arguments:
  customer: "cus_abc123"
  limit: 25
  created: {"gte": 1704067200}
```

---

## 已知坑点

| 坑点 | 详情 |
|---------|--------|
| **搜索查询语法** | `STRIPE_GET_V1_CUSTOMERS_SEARCH_CUSTOMERS` 需要带字段前缀的查询（例如 `email:'x'`）。没有字段前缀的裸字符串无效，会报错。 |
| **订阅的支付方式** | 如果使用 `trial_period_days` 或 `collection_method='send_invoice'`，则不需要 `default_payment_method`。否则，订阅可能无法激活。 |
| **支付方式绑定** | `PaymentMethod` 在绑定到客户之前必须处于未绑定状态。已绑定的支付方式会报错。 |
| **分页游标** | 使用 `starting_after`/`ending_before` 配合对象 ID，而不是页码。从每次响应中提取最后/第一个对象 ID。 |
| **余额金额以分计** | 所有金额均以最小货币单位表示（例如美元的分）。1000 = $10.00。 |
| **订阅状态默认值** | `GET_CUSTOMERS_CUSTOMER_SUBSCRIPTIONS` 默认排除已取消的订阅。传入 `status: "all"` 以包含它们。 |

---

## 快速参考

| 工具标识 | 描述 |
|-----------|-------------|
| `STRIPE_CREATE_CUSTOMER` | 创建新客户 |
| `STRIPE_GET_CUSTOMERS_CUSTOMER` | 按 ID 检索客户 |
| `STRIPE_POST_CUSTOMERS_CUSTOMER` | 更新现有客户 |
| `STRIPE_LIST_CUSTOMERS` | 分页列出客户 |
| `STRIPE_GET_V1_CUSTOMERS_SEARCH_CUSTOMERS` | 按属性搜索客户 |
| `STRIPE_CREATE_SUBSCRIPTION` | 为客户创建订阅 |
| `STRIPE_GET_CUSTOMERS_CUSTOMER_SUBSCRIPTIONS` | 列出客户订阅 |
| `STRIPE_GET_CUSTOMERS_CUSTOMER_SUBS_SUB_EXPOSED_ID` | 获取特定订阅 |
| `STRIPE_GET_CUSTOMERS_CUSTOMER_PAYMENT_METHODS` | 列出客户支付方式 |
| `STRIPE_ATTACH_PAYMENT_METHOD` | 将支付方式附加到客户 |
| `STRIPE_GET_CUSTOMERS_CUSTOMER_BALANCE_TRANSACTIONS` | 列出客户余额交易 |

---

*Powered by [Composio](https://composio.dev)*
