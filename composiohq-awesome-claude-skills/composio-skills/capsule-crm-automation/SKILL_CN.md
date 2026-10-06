---
name: Capsule CRM Automation
description: "通过 Composio MCP 集成，使用自然语言自动化 Capsule CRM 操作——管理联系人（parties）、运行结构化筛选查询、跟踪任务和项目、记录条目，并处理组织。"
category: crm
requires:
  mcp:
    - rube
---

# Capsule CRM Automation

管理你的 Capsule CRM——创建和更新联系人、对 parties/opportunities/cases 运行强大的筛选查询、跟踪任务和项目、浏览活动条目，并组织团队关系——全部通过自然语言命令完成。

**工具包文档：** [composio.dev/toolkits/capsule_crm](https://composio.dev/toolkits/capsule_crm)

---

## 设置

1. 将 Composio MCP 服务器添加到你的客户端配置中：
   ```
   https://rube.app/mcp
   ```
2. 按提示连接你的 Capsule CRM 账户（OAuth 身份验证）。
3. 开始发出自然语言命令来管理你的 CRM。

---

## 核心工作流

### 1. 运行结构化筛选查询
使用多个筛选条件、操作符和排序规则查询 parties、opportunities 或 cases（项目）。

**工具：** `CAPSULE_CRM_RUN_FILTER_QUERY`

**示例提示：**
> "查找加利福尼亚州所有标记为 'VIP' 的 Capsule CRM 联系人，按名称排序"

**关键参数：**
- `entity`（必填）—— 以下之一：`parties`、`opportunities`、`kases`
- `filter`（必填）—— 筛选对象，包含：
  - `conditions` —— 条件数组，每个条件包含：
    - `field` —— 字段名（例如 "name"、"email"、"state"、"country"、"tag"、"owner"、"jobTitle"、"addedOn"）
    - `operator` —— 以下之一："is"、"is not"、"starts with"、"ends with"、"contains"、"is greater than"、"is less than"、"is after"、"is before"、"is older than"、"is within last"、"is within next"
    - `value` —— 要比较的值
  - `orderBy` —— 排序对象数组，包含 `field` 和 `direction`（"ascending"/"descending"）
- `embed` —— 要包含在响应中的附加数据
- `page` / `perPage` —— 分页（每页最多 100 条）

**重要字段说明：**
- 地址字段（`city`、`state`、`country`、`zip`）是顶层字段，而不是嵌套在 "address" 之下
- 国家必须是 ISO 3166-1 alpha-2 代码（例如 "US"、"GB"、"CA"）
- 自定义字段使用 `custom:{fieldId}` 格式
- 组织字段使用 `org.` 前缀（例如 `org.name`、`org.tag`）

---

### 2. 列出和管理联系人（Parties）
检索所有联系人，可选按修改日期筛选并嵌入相关数据。

**工具：** `CAPSULE_CRM_LIST_PARTIES`

**示例提示：**
> "列出自 2025 年 1 月以来修改过的所有 Capsule CRM 联系人，附带其标签和组织"

**关键参数：**
- `since` —— ISO8601 日期，用于筛选在此日期之后发生变更的联系人
- `embed` —— 附加数据："tags"、"fields"、"organisation"、"missingImportantFields"
- `page` / `perPage` —— 分页（每页最多 100 条，默认 50）

---

### 3. 创建新联系人
将个人或组织添加到你的 Capsule CRM 中，包含完整的详细信息，如电子邮件、电话、地址、标签和自定义字段。

**工具：** `CAPSULE_CRM_CREATE_PARTY`

**示例提示：**
> "在 Capsule CRM 中创建一个新的人物：John Smith，Acme Corp 的销售副总裁，john@acme.com"

**关键参数：**
- `type`（必填）—— "person" 或 "organisation"
- 对于个人：`firstName`、`lastName`、`jobTitle`、`title`
- 对于组织：`name`
- `emailAddresses` —— `{address, type}` 对象数组
- `phoneNumbers` —— `{number, type}` 对象数组
- `addresses` —— 地址对象数组，包含 `street`、`city`、`state`、`country`、`zip`、`type`（Home/Postal/Office/Billing/Shipping）
- `organisation` —— 通过 `{id}` 或 `{name}` 关联组织（如未找到则创建）
- `tags` —— 通过 `{name}` 或 `{id}` 指定的标签数组
- `fields` —— 自定义字段值，格式为 `{definition, value}`
- `websites` —— `{address, service, type}` 对象数组
- `owner` —— 指定所属用户 `{id}`

---

### 4. 更新现有联系人
修改 party 记录的任何方面，包括添加/删除电子邮件、电话、标签和自定义字段。

**工具：** `CAPSULE_CRM_UPDATE_PARTY`

**示例提示：**
> "更新 Capsule CRM 中 party 11587：添加工作邮箱 john.new@acme.com 并移除标签 'prospect'"

**关键参数：**
- `partyId`（必填）—— 要更新的 party 的整数 ID
- `party`（必填）—— 包含待更新字段的对象。支持：
  - 所有创建字段（name、emails、phones、addresses 等）
  - 在子项上设置 `_delete: true` 以移除它们（需要该子项的 `id`）
  - 标签：通过 `{name}` 添加，或通过 `{id, _delete: true}` 移除

---

### 5. 跟踪任务
列出任务，可按状态筛选并嵌入相关数据。

**工具：** `CAPSULE_CRM_LIST_TASKS`

**示例提示：**
> "显示 Capsule CRM 中所有待处理任务，附带其关联的 parties 和所属人"

**关键参数：**
- `status` —— 按状态筛选："open"、"completed"、"pending"（数组）
- `embed` —— 附加数据："party"、"opportunity"、"kase"、"owner"、"nextTask"
- `page` / `perPage` —— 分页（每页最多 100 条，默认 50）

---

### 6. 浏览项目和活动条目
列出项目（cases）以及近期活动条目，包括备注、电子邮件和已完成的任务。

**工具：** `CAPSULE_CRM_LIST_PROJECTS`、`CAPSULE_CRM_LIST_ENTRIES_BY_DATE`

**示例提示：**
> "显示 Capsule CRM 中所有进行中的项目" / "显示带有 party 详情的近期活动条目"

**项目的关键参数：**
- `status` —— 按 "OPEN" 或 "CLOSED" 筛选
- `search` —— 用于搜索项目名称/描述的搜索词
- `since` —— ISO8601 日期，用于筛选此日期之后的修改
- `embed` —— "tags,fields,party,opportunity,missingImportantFields"

**条目的关键参数：**
- `embed` —— "party"、"kase"、"opportunity"、"creator"、"activityType"
- `page` / `perPage` —— 分页（每页最多 100 条）

---

## 常见陷阱

- **地址字段是顶层字段**：筛选时直接使用 `state`、`city`、`country`、`zip`——而不是 `address.state` 或嵌套语法。
- **国家代码是 ISO alpha-2 格式**：按 "US"、"GB"、"CA" 筛选——而不是 "United States" 或 "United Kingdom"。
- **自定义字段使用特殊语法**：在筛选条件中将自定义字段引用为 `custom:{fieldId}`。对于组织级自定义字段，使用 `org.custom:{fieldId}`。
- **项目在 API 中称为 "kases"**：尽管在 UI 中称为 "projects"，但 API 实体类型是 `kases`。在筛选查询中使用 `kases`。
- **删除操作需要条目 ID**：更新 party 以移除子项（emails、phones、tags）时，必须连同 `_delete: true` 一起提供该条目的 `id`。请先列出该 party 以获取子项 ID。
- **分页默认为 50**：所有列表端点默认每页 50 条，最多 100 条。为获取完整数据，请务必实现分页。
- **嵌入值因实体而异**：并非所有嵌入选项都适用于所有实体。请查阅文档以了解每个端点支持的嵌入值。

---

## 快速参考

| 操作 | 工具标识 | 必填参数 |
|---|---|---|
| 运行筛选查询 | `CAPSULE_CRM_RUN_FILTER_QUERY` | `entity`、`filter` |
| 列出联系人 | `CAPSULE_CRM_LIST_PARTIES` | 无（可选筛选条件） |
| 创建联系人 | `CAPSULE_CRM_CREATE_PARTY` | `type` |
| 更新联系人 | `CAPSULE_CRM_UPDATE_PARTY` | `partyId`、`party` |
| 删除联系人 | `CAPSULE_CRM_DELETE_PARTY` | `party_id` |
| 列出任务 | `CAPSULE_CRM_LIST_TASKS` | 无（可选筛选条件） |
| 列出项目 | `CAPSULE_CRM_LIST_PROJECTS` | 无（可选筛选条件） |
| 列出活动条目 | `CAPSULE_CRM_LIST_ENTRIES_BY_DATE` | 无（可选筛选条件） |
| 列出组织员工 | `CAPSULE_CRM_LIST_ORG_EMPLOYEES` | 组织 ID |
| 列出已删除的 opportunities | `CAPSULE_CRM_LIST_DELETED_OPPORTUNITIES` | `since` |

---

*由 [Composio](https://composio.dev) 提供支持*
