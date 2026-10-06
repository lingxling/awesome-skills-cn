---
name: Zoho Books Automation
description: "通过自然语言命令自动化 Zoho Books 会计工作流，包括开票、账单管理、联系人查找、付款跟踪以及多组织支持"
requires:
  mcp:
    - rube
---

# Zoho Books Automation

自动化 Zoho Books 会计工作流——创建和管理发票、跟踪账单和付款、查找联系人、导出 PDF，并处理多组织设置——全部通过自然语言完成。

**工具包文档：** [composio.dev/toolkits/zoho_books](https://composio.dev/toolkits/zoho_books)

---

## 设置

1. 将 Rube MCP 服务器添加到你的环境中：`https://rube.app/mcp`
2. 按提示连接你的 Zoho Books 账户（通过 Composio 的 OAuth 流程）
3. 开始发出用于 Zoho Books 自动化的自然语言命令

---

## 核心工作流

### 1. 发现组织

获取已认证用户的所有组织。这是一个前提条件，因为几乎所有其他端点都需要 `organization_id`。

**工具：** `ZOHO_BOOKS_LIST_ORGANIZATIONS`

无需参数。返回组织 ID、名称和元数据。

> 始终先调用此工具，以获取所有其他 Zoho Books 工具所需的 `organization_id`。

示例提示：
> "列出我的 Zoho Books 组织"

---

### 2. 创建和管理发票

创建带有明细项的发票、管理现有发票，并将其导出为 PDF。

**创建：** `ZOHO_BOOKS_CREATE_INVOICE`

关键参数：
- `organization_id` —— 目标组织（必需）
- `customer_id` —— 收款对象客户（必需）
- `line_items` —— 明细项数组（必需），每项包含：
  - `item_id` 或 `name` —— 引用现有商品或创建临时明细行
  - `quantity`、`rate` —— 金额明细
  - `description`、`tax_id`、`discount` —— 可选明细
- `date` / `due_date` —— 日期，格式为 `YYYY-MM-DD`
- `invoice_number` —— 自定义编号（需设置 `ignore_auto_number_generation=true`）
- `discount` / `discount_type` —— 发票级折扣（`entity_level` 或 `item_level`）
- `notes` / `terms` —— 打印在发票上的说明
- `send` —— 创建后立即发送发票邮件
- `payment_terms` —— 付款期限天数

**列出：** `ZOHO_BOOKS_LIST_INVOICES`

关键参数：
- `organization_id`（必需）
- `status` —— `sent`、`draft`、`overdue`、`paid`、`void`、`unpaid`、`partially_paid`、`viewed`
- `customer_id` / `customer_name` —— 按客户筛选
- `date_start` / `date_end` —— 日期范围筛选（`YYYY-MM-DD`）
- `search_text` —— 按发票编号、参考号或客户名称搜索
- `sort_column` / `sort_order` —— 按 `date`、`due_date`、`total`、`balance` 等排序
- `page` / `per_page` —— 分页（每页最多 200 条）

**获取详情：** `ZOHO_BOOKS_GET_INVOICE` —— 通过 `invoice_id` 获取，`accept` 格式可为：`json`、`pdf` 或 `html`

**删除：** `ZOHO_BOOKS_DELETE_INVOICE` —— 按 `invoice_id` 删除

**批量导出：** `ZOHO_BOOKS_BULK_EXPORT_INVOICES_PDF` —— 将最多 25 张发票合并为单个 PDF

**批量打印：** `ZOHO_BOOKS_BULK_PRINT_INVOICES` —— 为最多 25 张发票生成合并的可打印 PDF

示例提示：
> "为客户 1234567890 创建一张发票，包含 2 个明细项：10 件 Widget A，单价 25 美元，以及 5 件 Widget B，单价 50 美元，30 天内到期"

---

### 3. 跟踪和管理账单

列出、查看和更新供应商账单，支持全面筛选。

**列出：** `ZOHO_BOOKS_LIST_BILLS`

关键参数：
- `organization_id`（必需）
- `status` —— `paid`、`open`、`overdue`、`void`、`partially_paid`
- `vendor_id` / `vendor_name_contains` —— 按供应商筛选
- `bill_number` / `bill_number_contains` —— 按账单编号筛选
- `date_start` / `date_end` —— 日期范围筛选
- `total_greater_than` / `total_less_than` —— 金额范围筛选
- `sort_column` / `sort_order` —— 按 `vendor_name`、`bill_number`、`date`、`due_date`、`total` 等排序
- `page` / `per_page` —— 分页（最多 200）

**获取详情：** `ZOHO_BOOKS_GET_BILL` —— 通过 `bill_id` 和 `organization_id` 获取完整账单

**更新：** `ZOHO_BOOKS_UPDATE_BILL` —— 修改现有账单（需要 `bill_id`、`organization_id`、`vendor_id`、`bill_number`）

示例提示：
> "列出我组织的所有逾期账单，按到期日排序"

---

### 4. 查找联系人

搜索和筛选联系人（客户和供应商），用于发票和账单。

**工具：** `ZOHO_BOOKS_LIST_CONTACTS`

关键参数：
- `organization_id`（必需）
- `contact_type` —— `customer` 或 `vendor`
- `contact_name_contains` / `contact_name_startswith` —— 名称筛选
- `email_contains` / `email_startswith` —— 邮箱筛选
- `company_name_contains` —— 公司名称筛选
- `filter_by` —— 状态筛选：`Status.Active`、`Status.Inactive`、`Status.Duplicate` 等
- `search_text` —— 按联系人名称或备注搜索（最多 100 字符）
- `sort_column` —— 按 `contact_name`、`email`、`outstanding_receivable_amount`、`created_time` 等排序
- `page` / `per_page` —— 分页（最多 200）

示例提示：
> "查找所有公司名称包含 'Acme' 的活跃客户"

---

### 5. 跟踪发票付款

列出针对特定发票记录的所有付款。

**工具：** `ZOHO_BOOKS_LIST_INVOICE_PAYMENTS`

关键参数：
- `invoice_id` —— 要查询的发票（必需）
- `organization_id` —— 组织（必需）

返回应用于该发票的所有付款交易，包括金额、日期和付款方式。

示例提示：
> "显示发票 451025000000123045 的所有付款记录"

---

### 6. 完整开票工作流

组合多个工具以实现端到端的发票管理：

1. **组织**：`ZOHO_BOOKS_LIST_ORGANIZATIONS` —— 获取 `organization_id`
2. **联系人**：`ZOHO_BOOKS_LIST_CONTACTS` —— 查找或验证 `customer_id`
3. **创建**：`ZOHO_BOOKS_CREATE_INVOICE` —— 创建带明细项的发票
4. **审核**：`ZOHO_BOOKS_GET_INVOICE` —— 获取发票详情或 PDF
5. **跟踪**：`ZOHO_BOOKS_LIST_INVOICE_PAYMENTS` —— 监控付款状态
6. **导出**：`ZOHO_BOOKS_BULK_EXPORT_INVOICES_PDF` —— 批量导出以供存档

示例提示：
> "找到 'Acme Corp' 的客户 ID，为其创建一张包含咨询服务的发票，然后获取 PDF"

---

## 已知陷阱

| 陷阱 | 详情 |
|---------|--------|
| 始终需要组织 ID | 几乎每个端点都需要 `organization_id` —— 始终先调用 `ZOHO_BOOKS_LIST_ORGANIZATIONS` |
| 发票需要明细项 | `ZOHO_BOOKS_CREATE_INVOICE` 需要至少一个明细项，带 `item_id` 或 `name` |
| 发票 ID 格式 | 使用发票对象中的数字 `invoice_id`（例如 `7472322000000264123`），而不是 `invoice_url` 中的编码 ID |
| 批量限制 | `ZOHO_BOOKS_BULK_EXPORT_INVOICES_PDF` 和 `ZOHO_BOOKS_BULK_PRINT_INVOICES` 均最多接受 25 个发票 ID |
| 分页上限 200 | 所有列表端点每页上限为 200 条记录 —— 需要遍历分页以获取完整结果 |
| 账单更新需要所有字段 | 即使是部分更新，`ZOHO_BOOKS_UPDATE_BILL` 也需要 `bill_id`、`organization_id`、`vendor_id` 和 `bill_number` |
| 日期格式 | 所有日期参数均使用 `YYYY-MM-DD` 格式 |
| response_option 未文档化 | `ZOHO_BOOKS_LIST_INVOICES` 有一个未文档化的 `response_option` 参数（0=完整，1=完整+总计，2=仅计数），可能随时变更而无通知 |

---

## 快速参考

| 操作 | 工具标识 | 关键参数 |
|--------|-----------|------------|
| 列出组织 | `ZOHO_BOOKS_LIST_ORGANIZATIONS` | （无） |
| 创建发票 | `ZOHO_BOOKS_CREATE_INVOICE` | `organization_id`、`customer_id`、`line_items` |
| 列出发票 | `ZOHO_BOOKS_LIST_INVOICES` | `organization_id`、`status`、`date_start` |
| 获取发票 | `ZOHO_BOOKS_GET_INVOICE` | `invoice_id`、`organization_id`、`accept` |
| 删除发票 | `ZOHO_BOOKS_DELETE_INVOICE` | `invoice_id`、`organization_id` |
| 批量导出 PDF | `ZOHO_BOOKS_BULK_EXPORT_INVOICES_PDF` | `organization_id`、`invoice_ids` |
| 批量打印 | `ZOHO_BOOKS_BULK_PRINT_INVOICES` | `organization_id`、`invoice_ids` |
| 列出账单 | `ZOHO_BOOKS_LIST_BILLS` | `organization_id`、`status`、`vendor_id` |
| 获取账单 | `ZOHO_BOOKS_GET_BILL` | `bill_id`、`organization_id` |
| 更新账单 | `ZOHO_BOOKS_UPDATE_BILL` | `bill_id`、`organization_id`、`vendor_id` |
| 列出联系人 | `ZOHO_BOOKS_LIST_CONTACTS` | `organization_id`、`contact_type`、`search_text` |
| 列出付款 | `ZOHO_BOOKS_LIST_INVOICE_PAYMENTS` | `invoice_id`、`organization_id` |

---

*由 [Composio](https://composio.dev) 提供支持*
