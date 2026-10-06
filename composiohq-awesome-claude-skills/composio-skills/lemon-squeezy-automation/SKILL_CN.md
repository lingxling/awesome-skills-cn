---
name: Lemon Squeezy Automation
description: "通过 Composio MCP 集成，使用自然语言自动化 Lemon Squeezy 店铺管理——产品、订单、订阅、客户、折扣，以及结账跟踪。"
category: e-commerce
requires:
  mcp:
    - rube
---

# Lemon Squeezy Automation

管理你的 Lemon Squeezy 数字产品业务——跟踪订单、监控订阅、分析客户、审查折扣，并审计结账——全部通过自然语言命令完成。

**工具包文档：** [composio.dev/toolkits/lemon_squeezy](https://composio.dev/toolkits/lemon_squeezy)

---

## 设置

1. 将 Composio MCP 服务器添加到你的客户端配置中：
   ```
   https://rube.app/mcp
   ```
2. 按提示连接你的 Lemon Squeezy 账户（API 密钥身份验证）。
3. 开始发出自然语言命令来管理你的店铺。

---

## 核心工作流

### 1. 发现店铺和产品
列出所有店铺以获取店铺 ID，然后检索特定店铺的产品和变体。

**工具：** `LEMON_SQUEEZY_LIST_ALL_STORES`、`LEMON_SQUEEZY_LIST_ALL_PRODUCTS`、`LEMON_SQUEEZY_LIST_ALL_VARIANTS`

**示例提示：**
> "列出我所有的 Lemon Squeezy 店铺及其产品"

**关键参数：**
- `LEMON_SQUEEZY_LIST_ALL_STORES` —— 无需参数
- `LEMON_SQUEEZY_LIST_ALL_PRODUCTS` —— 按 `filter[store_id]` 筛选
- `LEMON_SQUEEZY_LIST_ALL_VARIANTS` —— 按 `filter[product_id]`、`filter[status]`（pending/draft/published）筛选

---

### 2. 跟踪订单和订单项目
检索所有订单，可选按店铺、用户邮箱或订单号筛选，并深入查看单个订单项目。

**工具：** `LEMON_SQUEEZY_LIST_ALL_ORDERS`、`LEMON_SQUEEZY_LIST_ALL_ORDER_ITEMS`

**示例提示：**
> "显示我 Lemon Squeezy 店铺中来自 johndoe@example.com 的所有订单"

**订单的关键参数：**
- `filter[store_id]` —— 按店铺 ID 筛选
- `filter[user_email]` —— 按客户邮箱筛选
- `filter[order_number]` —— 按特定订单号筛选
- `page[number]` / `page[size]` —— 分页（每页最多 100 条）

**订单项目的关键参数：**
- `filter[order_id]`、`filter[product_id]`、`filter[variant_id]` —— 按关联实体筛选

---

### 3. 监控订阅
列出所有订阅，提供丰富的筛选选项，用于跟踪经常性收入。

**工具：** `LEMON_SQUEEZY_LIST_ALL_SUBSCRIPTIONS`

**示例提示：**
> "显示我 Lemon Squeezy 店铺中所有活跃的订阅"

**关键参数：**
- `filter[status]` —— 按状态筛选（例如 `active`、`cancelled`）
- `filter[store_id]` —— 按店铺筛选
- `filter[product_id]` —— 按产品筛选
- `filter[user_email]` —— 按订阅者邮箱筛选
- `filter[variant_id]` —— 按变体筛选
- `page[number]` / `page[size]` —— 分页（每页最多 100 条）

---

### 4. 管理客户
检索客户记录，包括邮箱、月经常性收入（MRR）、总收入和客户门户 URL 等详细信息。

**工具：** `LEMON_SQUEEZY_LIST_ALL_CUSTOMERS`

**示例提示：**
> "查找邮箱为 johndoe@example.com 的 Lemon Squeezy 客户"

**关键参数：**
- `filter[email]` —— 按确切邮箱地址筛选
- `filter[store_id]` —— 按店铺 ID 筛选
- `page[number]` / `page[size]` —— 分页（每页最多 100 条）

---

### 5. 审计折扣和兑换记录
列出所有折扣码，并跟踪它们在各订单中的兑换情况。

**工具：** `LEMON_SQUEEZY_LIST_ALL_DISCOUNTS`、`LEMON_SQUEEZY_LIST_ALL_DISCOUNT_REDEMPTIONS`

**示例提示：**
> "显示店铺 12345 的所有折扣及其兑换历史"

**折扣的关键参数：**
- `filter[store_id]` —— 按店铺筛选
- `page[number]` / `page[size]` —— 分页

**兑换记录的关键参数：**
- `filter[discount_id]` —— 按折扣筛选
- `filter[order_id]` —— 按订单筛选

---

### 6. 审查结账
列出所有结账会话，可选按店铺或变体筛选。

**工具：** `LEMON_SQUEEZY_LIST_ALL_CHECKOUTS`

**示例提示：**
> "显示我 Lemon Squeezy 店铺中变体 42 的所有结账记录"

**关键参数：**
- `filter[store_id]` —— 按店铺 ID 筛选
- `filter[variant_id]` —— 按变体 ID 筛选

---

## 常见陷阱

- **店铺 ID 是基础**：大多数筛选条件都需要 `store_id`。在筛选其他资源之前，请始终先调用 `LEMON_SQUEEZY_LIST_ALL_STORES` 来发现有效的店铺 ID。
- **大型数据集必须分页**：所有列表端点都使用 `page[number]` / `page[size]` 分页（每页最多 100 条）。不要假设第一页就是完整数据。
- **筛选参数命名**：Lemon Squeezy 使用方括号表示法进行筛选（例如 `filter[store_id]`、`page[number]`）。请确保使用准确的参数名称。
- **订阅发票与订单的区别**：订阅发票（`LEMON_SQUEEZY_LIST_ALL_SUBSCRIPTION_INVOICES`）与一次性订单是分开的。请根据使用场景选用合适的端点。

---

## 快速参考

| 操作 | 工具标识 | 必填参数 |
|---|---|---|
| 列出店铺 | `LEMON_SQUEEZY_LIST_ALL_STORES` | 无 |
| 列出产品 | `LEMON_SQUEEZY_LIST_ALL_PRODUCTS` | 无（可选筛选条件） |
| 列出变体 | `LEMON_SQUEEZY_LIST_ALL_VARIANTS` | 无（可选筛选条件） |
| 列出订单 | `LEMON_SQUEEZY_LIST_ALL_ORDERS` | 无（可选筛选条件） |
| 列出订单项目 | `LEMON_SQUEEZY_LIST_ALL_ORDER_ITEMS` | 无（可选筛选条件） |
| 列出订阅 | `LEMON_SQUEEZY_LIST_ALL_SUBSCRIPTIONS` | 无（可选筛选条件） |
| 列出客户 | `LEMON_SQUEEZY_LIST_ALL_CUSTOMERS` | 无（可选筛选条件） |
| 列出折扣 | `LEMON_SQUEEZY_LIST_ALL_DISCOUNTS` | 无（可选筛选条件） |
| 列出折扣兑换记录 | `LEMON_SQUEEZY_LIST_ALL_DISCOUNT_REDEMPTIONS` | 无（可选筛选条件） |
| 列出结账记录 | `LEMON_SQUEEZY_LIST_ALL_CHECKOUTS` | 无（可选筛选条件） |

---

*由 [Composio](https://composio.dev) 提供支持*
