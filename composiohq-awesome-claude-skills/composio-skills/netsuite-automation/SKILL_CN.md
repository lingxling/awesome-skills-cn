---
name: NetSuite Automation
description: "NetSuite 自动化：通过 Oracle NetSuite ERP 管理客户、销售订单、发票、库存和记录，并支持 SuiteQL 查询"
requires:
  mcp: [rube]
---

# NetSuite Automation

自动化 Oracle NetSuite ERP 操作，包括创建客户和销售订单、运行 SuiteQL 查询、按外部 ID 进行更新插入（upsert），以及检查记录元数据，以实现全面的业务管理。

**工具包文档：** [composio.dev/toolkits/netsuite](https://composio.dev/toolkits/netsuite)

---

## 设置

本技能需要连接 **Rube MCP 服务器**，地址为 `https://rube.app/mcp`。

在执行任何工具之前，请确保 `netsuite` 工具包已存在有效连接。如果没有活动连接，请通过 `RUBE_MANAGE_CONNECTIONS` 发起连接。

---

## 核心工作流

### 1. 创建销售订单

创建包含商品引用、数量和定价等明细行的客户订单。

**工具：** `NETSUITE_CREATE_SALES_ORDER`

**关键参数：**
- `entity`（必填）-- 客户引用：`{"id": "<internal_id>"}`
- `item`（必填）-- 包含 `items` 数组的容器，数组中每个元素包含：
  - `item`（必填）-- 商品引用：`{"id": "<internal_id>"}`
  - `quantity`（必填）-- 订购数量（非负数）
  - `rate` -- 单价（如果商品有默认定价则可选）
  - `amount` -- 行总金额（`rate` 的替代方案）
  - `taxcode` -- 税码引用：`{"id": "<internal_id>"}`（启用 SuiteTax 时必填）
  - `description` -- 明细行备注
- `tranDate` -- 交易日期，`YYYY-MM-DD` 格式
- `memo` -- 表头备注
- `orderStatus` -- `"A"`（待审批）或 `"B"`（待履行）
- `otherrefnum` -- 外部引用或采购订单号

**示例：**
```
Tool: NETSUITE_CREATE_SALES_ORDER
Arguments:
  entity: {"id": "1234"}
  item: {
    "items": [
      {"item": {"id": "56"}, "quantity": 10, "rate": 25.00},
      {"item": {"id": "78"}, "quantity": 5, "rate": 50.00}
    ]
  }
  tranDate: "2026-02-11"
  memo: "Q1 bulk order"
  orderStatus: "B"
```

---

### 2. 运行 SuiteQL 查询

对 NetSuite 数据执行带服务端分页的临时 SQL 查询。

**工具：** `NETSUITE_RUN_SUITEQL_QUERY`

**关键参数：**
- `q`（必填）-- SuiteQL SELECT 语句
- `limit` -- 每页行数（默认值不同）
- `offset` -- 首行的从零开始的索引（必须是 `limit` 的倍数）

**示例：**
```
Tool: NETSUITE_RUN_SUITEQL_QUERY
Arguments:
  q: "SELECT id, companyname, email FROM customer WHERE isinactive = 'F' ORDER BY companyname"
  limit: 100
  offset: 0
```

```
Tool: NETSUITE_RUN_SUITEQL_QUERY
Arguments:
  q: "SELECT id, entitystatus, total FROM transaction WHERE type = 'SalesOrd' AND trandate >= '2026-01-01'"
  limit: 50
```

---

### 3. 创建和管理客户

创建带有子公司分配和联系方式的新客户记录。

**工具：**
- `NETSUITE_CREATE_CUSTOMER` -- 创建新客户
- `NETSUITE_GET_CUSTOMER` -- 按内部 ID 获取客户
- `NETSUITE_UPDATE_CUSTOMER` -- 更新现有客户（PATCH 语义）

**`NETSUITE_CREATE_CUSTOMER` 的关键参数：**
- `body`（必填）-- 包含客户数据的 JSON 对象。必填字段：
  - `subsidiary` -- 包含 `id`（子公司内部 ID）的对象
  - 要么填写 `companyName`（企业客户），要么填写 `firstName` + `lastName`（个人客户）
  - 可选：`email`、`phone`、`isPerson`（个人客户设为 `"T"`）、`comments`
- `replace` -- 需要完全替换的子列表名称，以逗号分隔（如 `"contacts,addressbook"`）

**示例：**
```
Tool: NETSUITE_CREATE_CUSTOMER
Arguments:
  body: {
    "companyName": "Acme Corp",
    "subsidiary": {"id": "1"},
    "email": "info@acme.com",
    "phone": "555-0100"
  }
```

---

### 4. 按外部 ID 更新插入记录

使用外部标识符幂等地创建或更新记录。这对同步工作流至关重要。

**工具：** `NETSUITE_UPSERT_RECORD_BY_EXTERNAL_ID`

**关键参数：**
- `record_type`（必填）-- 记录类型名称，例如 `"customer"`、`"salesorder"`、`"customrecord_myrec"`
- `external_id`（必填）-- 外部 ID 值（仅限字母、数字、下划线、连字符）
- `body`（必填）-- 符合记录架构的 JSON 对象；创建记录时需包含必填字段

**示例：**
```
Tool: NETSUITE_UPSERT_RECORD_BY_EXTERNAL_ID
Arguments:
  record_type: "customer"
  external_id: "CRM-CUST-42"
  body: {
    "companyName": "Acme Corp",
    "subsidiary": {"id": "1"},
    "email": "updated@acme.com"
  }
```

> **警告：** 幂等性依赖于外部 ID 使用的一致性。ID 不匹配会悄悄创建额外记录，而不是进行更新。

---

### 5. 检查记录元数据

在创建或更新记录之前，发现可用字段、数据类型、约束条件和必填要求。

**工具：** `NETSUITE_GET_RECORD_METADATA`

**关键参数：**
- `record_type`（必填）-- 例如 `"customer"`、`"salesorder"`、`"invoice"`、`"vendor"`、`"employee"`、`"item"`
- `accept` -- `"application/schema+json"`（默认，JSON Schema）或 `"application/swagger+json"`（OpenAPI 3.0）

**示例：**
```
Tool: NETSUITE_GET_RECORD_METADATA
Arguments:
  record_type: "salesorder"
```

---

### 6. 列出和筛选记录

检索多条记录，并支持可选的筛选和分页。

**工具：** `NETSUITE_LIST_RECORDS`

**关键参数：**
- `recordType`（必填）-- 例如 `"customer"`、`"salesorder"`
- `q` -- 使用 N/query 运算符的过滤表达式，例如 `"email START_WITH \"barbara\""`
- `limit` -- 每页最大记录数（1--1000，默认 1000）
- `offset` -- 从零开始的索引（必须能被 limit 整除）

**辅助工具：**
- `NETSUITE_FILTER_RECORD_COLLECTION` -- 替代性过滤方式（次于 SuiteQL）
- `NETSUITE_GET_RECORD_SELECTED_FIELDS` -- 仅检索特定字段（减小负载）

---

## 推荐执行计划

1. **检查记录架构**，使用 `NETSUITE_GET_RECORD_METADATA` 发现必填字段
2. **搜索现有记录**，使用 `NETSUITE_RUN_SUITEQL_QUERY` 以避免重复
3. **按邮箱查找客户**，使用 SuiteQL；若找到则用 `NETSUITE_GET_CUSTOMER` 获取详情
4. **如有需要则创建客户**，使用 `NETSUITE_CREATE_CUSTOMER`（确保设置了 `subsidiary`）
5. **验证商品内部 ID**，使用 `NETSUITE_LIST_RECORDS` 或 SuiteQL
6. **创建销售订单**，使用 `NETSUITE_CREATE_SALES_ORDER` 并使用已验证的引用
7. **可选地按外部 ID 更新插入**，使用 `NETSUITE_UPSERT_RECORD_BY_EXTERNAL_ID` 用于同步工作流
8. **验证结果**，使用 `NETSUITE_GET_RECORD_SELECTED_FIELDS` 确认定价/总额

---

## 常见陷阱

| 陷阱 | 详情 |
|---------|--------|
| **无效的商品 ID** | 当商品内部 ID 无效时，`NETSUITE_CREATE_SALES_ORDER` 会抛出 USER_ERROR。请先通过 `NETSUITE_LIST_RECORDS` 或 `NETSUITE_RUN_SUITEQL_QUERY` 预先验证。 |
| **缺少必填字段** | 当必填字段（如 `subsidiary`）缺失时，`NETSUITE_CREATE_CUSTOMER` 会返回 400。请始终先用 `NETSUITE_GET_RECORD_METADATA` 检查。 |
| **SuiteQL 字段名** | 不同账户间的查询差异可能导致结果为空。当结果看起来不对时，请通过 `NETSUITE_GET_RECORD_METADATA` 确认字段名。 |
| **过滤表达式的限制** | 如果过滤语法不受支持，`NETSUITE_FILTER_RECORD_COLLECTION` 可能会失败。应将其视为 SuiteQL 的次要备选方案。 |
| **外部 ID 幂等性** | `NETSUITE_UPSERT_RECORD_BY_EXTERNAL_ID` 依赖于外部 ID 的一致性。不匹配会悄悄创建重复记录，而不是进行更新。 |
| **SuiteTax 明细行** | 启用了 SuiteTax 的账户要求每个明细行都填写 `taxcode`。遗漏会导致创建失败。 |

---

## 快速参考

| 工具 Slug | 描述 |
|-----------|-------------|
| `NETSUITE_CREATE_SALES_ORDER` | 创建带明细行的新销售订单 |
| `NETSUITE_RUN_SUITEQL_QUERY` | 执行带分页的临时 SuiteQL 查询 |
| `NETSUITE_CREATE_CUSTOMER` | 创建新客户记录 |
| `NETSUITE_GET_CUSTOMER` | 按内部 ID 获取客户 |
| `NETSUITE_UPDATE_CUSTOMER` | 更新现有客户（PATCH） |
| `NETSUITE_UPSERT_RECORD_BY_EXTERNAL_ID` | 按外部 ID 创建或更新记录 |
| `NETSUITE_GET_RECORD_METADATA` | 检查记录架构和字段定义 |
| `NETSUITE_LIST_RECORDS` | 列出并筛选、分页记录 |
| `NETSUITE_FILTER_RECORD_COLLECTION` | 替代性记录筛选 |
| `NETSUITE_GET_RECORD_SELECTED_FIELDS` | 从记录中检索特定字段 |

---

*由 [Composio](https://composio.dev) 提供支持*
