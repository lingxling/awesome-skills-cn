---
name: Kommo Automation
description: "通过 Composio MCP 集成，用自然语言自动化 Kommo CRM 操作 —— 管理潜客、销售流程、流程阶段、任务和自定义字段。"
category: crm
requires:
  mcp:
    - rube
---

# Kommo Automation

管理你的 Kommo CRM 销售流程 —— 列出并筛选潜客、浏览流程阶段、创建和更新交易、分配任务，并使用自定义字段 —— 全部通过自然语言指令完成。

**工具包文档：** [composio.dev/toolkits/kommo](https://composio.dev/toolkits/kommo)

---

## 设置

1. 将 Composio MCP 服务器添加到你的客户端配置中：
   ```
   https://rube.app/mcp
   ```
2. 按提示连接你的 Kommo 账户（OAuth 身份验证）。
3. 开始使用自然语言指令管理你的 CRM。

---

## 核心工作流

### 1. 浏览流程与阶段
列出所有潜客流程，然后深入查看特定流程阶段，以了解你的销售漏斗结构。

**工具：** `KOMMO_LIST_LEADS_PIPELINES`、`KOMMO_LIST_PIPELINE_STAGES`

**示例提示：**
> "显示我所有的 Kommo 流程，以及我主销售流程中的各个阶段"

**列出流程的关键参数：** 无需任何参数。

**列出阶段的关键参数：**
- `pipeline_id`（必填）—— 要列出阶段的流程 ID
- `with_description` —— 在响应中包含阶段描述（布尔值）

---

### 2. 列出并筛选潜客
检索潜客，支持按流程、状态、日期范围、负责人、价格等进行强大的筛选。

**工具：** `KOMMO_LIST_LEADS`

**示例提示：**
> "显示流程 12345 中本周创建的所有潜客，按最新排序"

**关键参数：**
- `query` —— 跨所有已填写字段的自由文本搜索
- `filter_pipeline_ids` —— 按流程 ID 筛选（整数数组）
- `filter_status` —— 按流程内的状态筛选：`{"pipeline_id": 123, "status_id": 456}`
- `filter_responsible_user_ids` —— 按指派用户 ID 筛选
- `filter_names` —— 按潜客名称筛选
- `filter_price` —— 按交易金额筛选
- `filter_created_at` —— 日期范围：`{"from": <unix_timestamp>, "to": <unix_timestamp>}`
- `filter_updated_at` —— 最后更新的日期范围
- `filter_closed_at` —— 结束的日期范围
- `order_by_created_at` —— 排序："asc" 或 "desc"
- `order_by_updated_at` —— 按更新日期排序
- `limit` —— 每页最多250条
- `page` —— 分页的页码
- `with_params` —— 附加数据："contacts"、"loss_reason"、"catalog_elements"、"source_id"

---

### 3. 创建新潜客
向你的 Kommo 流程中添加新交易，包含自定义字段、标签和流程位置。

**工具：** `KOMMO_CREATE_LEAD`

**示例提示：**
> "在流程 12345 中创建一个名为 'Acme Corp Deal' 的新潜客，价值50,000美元"

**关键参数：**
- `name`（必填）—— 潜客/交易的名称
- `price` —— 交易金额（整数）
- `pipeline_id` —— 要添加潜客的流程
- `status_id` —— 流程内的阶段（默认为主流程的第一个阶段）
- `responsible_user_id` —— 指派的用户 ID
- `custom_fields_values` —— 自定义字段值对象数组
- `tags_to_add` —— 标签数组（按名称或 ID）
- `created_by` —— 创建者的用户 ID（0 表示机器人）
- `loss_reason_id` —— 流失原因（如适用）

---

### 4. 更新现有潜客
修改潜客属性，包括名称、价格、流程阶段、负责人、标签和自定义字段。

**工具：** `KOMMO_UPDATE_LEAD`

**示例提示：**
> "将潜客789移动到流程123中的阶段456，并将价格更新为75,000美元"

**关键参数：**
- 潜客 ID（必填）
- 以下任意组合：`name`、`price`、`pipeline_id`、`status_id`、`responsible_user_id`、`tags_to_add`、`tags_to_delete`、`custom_fields_values`

---

### 5. 创建任务
分配与潜客、联系人或公司相关联的跟进任务。

**工具：** `KOMMO_CREATE_TASK`

**示例提示：**
> "为潜客789创建一个明天到期的跟进电话任务，指派给用户42"

**关键参数：**
- 任务文本/描述
- 实体类型和 ID（潜客、联系人、公司）
- 负责人用户 ID
- 到期日期（Unix 时间戳）
- 任务类型

---

### 6. 发现自定义字段
列出潜客、联系人或公司的所有自定义字段，以了解你的 CRM 结构。

**工具：** `KOMMO_LIST_CUSTOM_FIELDS`

**示例提示：**
> "Kommo 中潜客有哪些自定义字段可用？"

**关键参数：**
- 实体类型（潜客、联系人、公司）

---

## 已知陷阱

- **日期过滤器使用 Unix 时间戳**：所有日期范围过滤器（`filter_created_at`、`filter_updated_at`、`filter_closed_at`）要求使用 `{"from": <timestamp>, "to": <timestamp>}` 结构的 Unix 时间戳格式，而不是 ISO8601 字符串。
- **需要流程和阶段 ID**：要按状态筛选潜客，你需要同时提供 `pipeline_id` 和 `status_id`。请始终先调用 `KOMMO_LIST_LEADS_PIPELINES` 和 `KOMMO_LIST_PIPELINE_STAGES` 来查找有效的 ID。
- **每页最多250个潜客**：`limit` 参数的上限为250。对于大数据集，请使用 `page` 参数实现分页。
- **自定义字段值的格式**：自定义字段使用特定的嵌套对象格式。在设置值之前，请使用 `KOMMO_LIST_CUSTOM_FIELDS` 查找字段 ID 和预期的值格式。
- **状态筛选需要两个 ID**：`filter_status` 参数要求将 `pipeline_id` 和 `status_id` 作为一个组合对象提供 —— 你不能仅按状态单独筛选。
- **Created_by 为 0 表示机器人**：将 `created_by` 或 `updated_by` 设为 0 时，该操作会被归因于机器人/自动化，而不是人工用户。

---

## 快速参考

| 操作 | 工具 Slug | 必填参数 |
|---|---|---|
| 列出流程 | `KOMMO_LIST_LEADS_PIPELINES` | 无 |
| 列出流程阶段 | `KOMMO_LIST_PIPELINE_STAGES` | `pipeline_id` |
| 列出潜客 | `KOMMO_LIST_LEADS` | 无（可选筛选条件） |
| 创建潜客 | `KOMMO_CREATE_LEAD` | `name` |
| 更新潜客 | `KOMMO_UPDATE_LEAD` | 潜客 ID |
| 创建任务 | `KOMMO_CREATE_TASK` | 任务详情 |
| 列出自定义字段 | `KOMMO_LIST_CUSTOM_FIELDS` | 实体类型 |

---

*由 [Composio](https://composio.dev) 提供支持*
