---
name: Dynamics 365 Automation
description: "Dynamics 365 自动化：通过 Dynamics CRM Web API 管理 CRM 联系人、客户、潜在客户、商机、销售订单、发票和案例"
requires:
  mcp: [rube]
---

# Dynamics 365 Automation

自动化 Microsoft Dynamics 365 CRM 操作，包括创建和更新联系人、客户、潜在客户、商机、销售订单、发票以及支持案例。

**工具包文档：** [composio.dev/toolkits/dynamics365](https://composio.dev/toolkits/dynamics365)

---

## 设置

此技能需要连接 **Rube MCP 服务器**，地址为 `https://rube.app/mcp`。

在执行任何工具之前，请确保 `dynamics365` 工具包存在有效连接。如果没有有效连接，请通过 `RUBE_MANAGE_CONNECTIONS` 发起连接。

---

## 核心工作流

### 1. 管理潜在客户（Leads）

创建、更新、获取和列出潜在客户记录。

**工具：**
- `DYNAMICS365_DYNAMICSCRM_CREATE_LEAD` -- 创建新的潜在客户
- `DYNAMICS365_DYNAMICSCRM_UPDATE_LEAD` -- 更新现有潜在客户
- `DYNAMICS365_DYNAMICSCRM_GET_A_LEAD` -- 通过 GUID 获取潜在客户
- `DYNAMICS365_DYNAMICSCRM_GET_ALL_LEADS` -- 列出/筛选所有潜在客户

**`DYNAMICS365_DYNAMICSCRM_CREATE_LEAD` 的关键参数：**
- `firstname` -- 潜在客户的名字
- `lastname` -- 潜在客户的姓氏
- `emailaddress1` -- 主邮箱地址
- `telephone1` -- 主电话号码
- `companyname` -- 关联的公司名称
- `subject` -- 简要标题/描述

**`DYNAMICS365_DYNAMICSCRM_GET_ALL_LEADS` 的关键参数：**
- `filter` -- OData 筛选条件，例如 `"contains(fullname,'John')"`
- `select` -- 要返回的字段，例如 `"fullname,emailaddress1"`
- `orderby` -- 排序表达式，例如 `"createdon desc"`
- `top` -- 最大结果数量

**示例：**
```
Tool: DYNAMICS365_DYNAMICSCRM_CREATE_LEAD
Arguments:
  firstname: "Jane"
  lastname: "Smith"
  emailaddress1: "jane.smith@example.com"
  companyname: "Acme Corp"
  subject: "Interested in Enterprise plan"
```

---

### 2. 管理客户（Accounts）

在 CRM 中创建和整理客户（公司）记录。

**工具：** `DYNAMICS365_DYNAMICSCRM_CREATE_ACCOUNT`

**关键参数：**
- `name` -- 客户/公司名称
- `description` -- 客户描述
- `revenue` -- 收入金额（数字）
- `accountcategorycode` -- 分类代码（整数，默认值：1）
- `creditonhold` -- 该客户是否处于信用冻结状态（布尔值）

**示例：**
```
Tool: DYNAMICS365_DYNAMICSCRM_CREATE_ACCOUNT
Arguments:
  name: "Contoso Ltd"
  description: "Strategic partner for cloud services"
  revenue: 5000000
  creditonhold: false
```

---

### 3. 管理联系人（Contacts）

创建包含地址和电话信息的详细联系人记录。

**工具：** `DYNAMICS365_DYNAMICSCRM_CREATE_CONTACT`

**关键参数：**
- `firstname`、`lastname` -- 联系人姓名
- `emailaddress1` -- 主邮箱
- `telephone1` -- 主电话
- `mobilephone` -- 手机号码
- `jobtitle` -- 职位
- `address1_city`、`address1_stateorprovince`、`address1_postalcode`、`address1_country` -- 地址字段

**示例：**
```
Tool: DYNAMICS365_DYNAMICSCRM_CREATE_CONTACT
Arguments:
  firstname: "Bob"
  lastname: "Johnson"
  emailaddress1: "bob.johnson@example.com"
  jobtitle: "VP of Engineering"
  address1_city: "Seattle"
  address1_stateorprovince: "WA"
```

---

### 4. 管理商机（Opportunities）

创建和更新带有预估金额及预计成交日期的销售商机。

**工具：**
- `DYNAMICS365_DYNAMICSCRM_CREATE_OPPORTUNITY` -- 创建新商机
- `DYNAMICS365_DYNAMICSCRM_UPDATE_OPPORTUNITY` -- 更新现有商机

**`DYNAMICS365_DYNAMICSCRM_CREATE_OPPORTUNITY` 的关键参数：**
- `name`（必填） -- 商机标题
- `description` -- 简要描述
- `estimatedvalue` -- 预估收入（数字）
- `estimatedclosedate` -- 预计成交日期，格式为 `YYYY-MM-DD`
- `customer_account_id` -- 关联客户的 GUID（不含花括号）
- `customer_contact_id` -- 关联联系人的 GUID（不含花括号）

**`DYNAMICS365_DYNAMICSCRM_UPDATE_OPPORTUNITY` 的关键参数：**
- `opportunity_id`（必填） -- 商机的 GUID
- `opportunityratingcode` -- 1（冷）、2（温）、3（热）
- `salesstagecode` -- 1（资格审查）、2（深入了解）、3（提案）

**示例：**
```
Tool: DYNAMICS365_DYNAMICSCRM_CREATE_OPPORTUNITY
Arguments:
  name: "Enterprise Cloud Migration"
  estimatedvalue: 250000
  estimatedclosedate: "2026-06-30"
  description: "Full cloud migration project for Contoso"
```

---

### 5. 管理销售订单和发票

创建和更新销售订单；生成用于计费的发票。

**工具：**
- `DYNAMICS365_DYNAMICSCRM_CREATE_SALES_ORDER` -- 创建新的销售订单
- `DYNAMICS365_DYNAMICSCRM_UPDATE_SALES_ORDER` -- 更新现有销售订单
- `DYNAMICS365_DYNAMICSCRM_CREATE_INVOICE` -- 创建新发票

**`DYNAMICS365_DYNAMICSCRM_CREATE_SALES_ORDER` 的关键参数：**
- `name` -- 销售订单名称
- `description` -- 描述
- `account_id` -- 客户引用，格式：`"/accounts(GUID)"`
- `currency_id` -- 货币引用，格式：`"/transactioncurrencies(GUID)"`
- `price_level_id` -- 价目表引用，格式：`"/pricelevels(GUID)"`

**`DYNAMICS365_DYNAMICSCRM_UPDATE_SALES_ORDER` 的关键参数：**
- `salesorder_id`（必填） -- 销售订单的 GUID
- `name` -- 更新后的名称
- `discountamount` -- 更新后的折扣
- `freightamount` -- 更新后的运费

**`DYNAMICS365_DYNAMICSCRM_CREATE_INVOICE` 的关键参数：**
- `name` -- 发票名称/编号，例如 `"Invoice #12345"`
- `description` -- 发票描述
- `account_id` -- 关联客户引用
- `currency_id` -- 货币引用
- `price_level_id` -- 价目表引用

---

### 6. 创建支持案例

为客户支持跟踪创建事件/案例记录。

**工具：** `DYNAMICS365_DYNAMICSCRM_CREATE_CASE`

**关键参数：**
- `title` -- 案例的主题/标题
- `description` -- 详细描述
- `prioritycode` -- 1（低）、2（普通）、3（高）
- `caseorigincode` -- 1（电话）、2（邮件）、3（网页）
- `account_id` -- 关联客户，格式：`"/accounts(GUID)"`
- `contact_id` -- 关联联系人，格式：`"/contacts(GUID)"`

**示例：**
```
Tool: DYNAMICS365_DYNAMICSCRM_CREATE_CASE
Arguments:
  title: "Login issue reported by customer"
  description: "Customer unable to access portal since Feb 10"
  prioritycode: 3
  caseorigincode: 2
```

---

## 常见陷阱

| 陷阱 | 详情 |
|---------|--------|
| **GUID 格式** | 所有实体 ID 都是 GUID（例如 `"00000000-0000-0000-0000-000000000000"`）。商机/联系人引用不要包含花括号。 |
| **引用格式** | 关联实体引用使用 `"/entityset(GUID)"` 格式（例如 `"/accounts(abc-123)"`）。缺少前导斜杠或括号会导致错误。 |
| **OData 筛选语法** | `filter` 需使用 Dynamics 365 的 OData 语法（例如 `contains(fullname,'John')`）。语法不正确会返回空结果或错误响应。 |
| **user_id 默认值** | 大多数工具的 `user_id` 默认是已认证用户的 `"me"`。只有在代表其他用户操作时才覆盖此值。 |
| **必填字段** | `CREATE_OPPORTUNITY` 要求必须提供 `name`。其他创建工具没有严格的必填字段，但如果不填数据会创建空记录。 |

---

## 快速参考

| 工具标识 | 描述 |
|-----------|-------------|
| `DYNAMICS365_DYNAMICSCRM_CREATE_LEAD` | 创建新的潜在客户记录 |
| `DYNAMICS365_DYNAMICSCRM_UPDATE_LEAD` | 更新现有潜在客户 |
| `DYNAMICS365_DYNAMICSCRM_GET_A_LEAD` | 通过 GUID 获取潜在客户 |
| `DYNAMICS365_DYNAMICSCRM_GET_ALL_LEADS` | 列出/筛选所有潜在客户 |
| `DYNAMICS365_DYNAMICSCRM_CREATE_ACCOUNT` | 创建新客户 |
| `DYNAMICS365_DYNAMICSCRM_CREATE_CONTACT` | 创建新联系人 |
| `DYNAMICS365_DYNAMICSCRM_CREATE_OPPORTUNITY` | 创建新商机 |
| `DYNAMICS365_DYNAMICSCRM_UPDATE_OPPORTUNITY` | 更新现有商机 |
| `DYNAMICS365_DYNAMICSCRM_CREATE_SALES_ORDER` | 创建新的销售订单 |
| `DYNAMICS365_DYNAMICSCRM_UPDATE_SALES_ORDER` | 更新现有销售订单 |
| `DYNAMICS365_DYNAMICSCRM_CREATE_INVOICE` | 创建新发票 |
| `DYNAMICS365_DYNAMICSCRM_CREATE_CASE` | 创建支持案例/事件 |

---

*由 [Composio](https://composio.dev) 提供支持*
