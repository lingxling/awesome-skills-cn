---
name: Attio Automation
description: "自动化 Attio CRM 操作 -- 搜索记录、用高级过滤器查询联系人和公司、管理笔记、列出属性，并浏览你的关系数据 -- 全程通过 Composio MCP 集成以自然语言完成。"
category: crm
requires:
  mcp:
    - rube
---

# Attio Automation

管理你的 Attio CRM 工作区 -- 跨人员和公司进行模糊搜索、运行复杂的过滤查询、浏览笔记、发现对象结构，以及列出记录 -- 全部通过自然语言命令完成。

**工具包文档：** [composio.dev/toolkits/attio](https://composio.dev/toolkits/attio)

---

## 设置

1. 将 Composio MCP 服务器添加到你的客户端配置中：
   ```
   https://rube.app/mcp
   ```
2. 按提示连接你的 Attio 账户（OAuth 身份验证）。
3. 开始发出自然语言命令来管理你的 CRM 数据。

---

## 核心工作流

### 1. 跨记录模糊搜索
按姓名、域名、邮箱、电话或社交账号搜索人员、公司、交易或任意对象。

**工具：** `ATTIO_SEARCH_RECORDS`

**示例提示：**
> "在 Attio 中搜索名为 Alan Mathis 的人"

**关键参数（均为必填）：**
- `query` -- 搜索字符串（最多 256 个字符）。空字符串返回默认结果。
- `objects` -- 要搜索的对象 slug 数组（例如 `["people"]`、`["people", "companies"]`、`["deals"]`）
- `request_as` -- 上下文：使用 `{"type": "workspace"}` 进行全工作区搜索，或指定某个工作区成员

---

### 2. 高级过滤查询
通过服务端过滤、排序和复杂条件查询记录 -- 比模糊搜索更强大得多。

**工具：** `ATTIO_QUERY_RECORDS`

**示例提示：**
> "查找 Attio 中 2025 年 1 月之后创建的所有公司，按名称排序"

**关键参数：**
- `object`（必填）-- 对象 slug 或 UUID（例如 "people"、"companies"、"deals"）
- `filter` -- Attio 过滤器对象，支持 `$eq`、`$contains`、`$gte`、`$and`、`$or` 等操作符
- `sorts` -- 排序规格数组，包含 `direction`（"asc"/"desc"）和 `attribute`
- `limit` -- 最多返回的记录数（最多 500）
- `offset` -- 分页偏移量

**过滤器示例：**
```json
{"name": {"first_name": {"$contains": "John"}}}
{"email_addresses": {"$contains": "@example.com"}}
{"created_at": {"$gte": "2025-01-01T00:00:00.000Z"}}
```

---

### 3. 按 ID 或属性查找记录
通过唯一 ID 或按唯一属性值搜索特定记录。

**工具：** `ATTIO_FIND_RECORD`

**示例提示：**
> "查找域名为 example.com 的 Attio 公司"

**关键参数：**
- `object_id`（必填）-- 对象类型 slug："people"、"companies"、"deals"、"users"、"workspaces"
- `record_id` -- 通过 UUID 直接查找（可选）
- `attributes` -- 属性过滤条件字典（例如 `{"email_addresses": "john@example.com"}`）
- `limit` -- 最多记录数（最多 1000）
- `offset` -- 分页偏移量

---

### 4. 浏览与筛选笔记
列出整个工作区的笔记，或按特定父对象和记录过滤。

**工具：** `ATTIO_LIST_NOTES`

**示例提示：**
> "显示 Attio 中 Acme Corp 公司记录的最后 10 条笔记"

**关键参数：**
- `parent_object` -- 对象 slug（例如 "people"、"companies"、"deals"）-- 需要同时提供 `parent_record_id`
- `parent_record_id` -- 父记录的 UUID -- 需要同时提供 `parent_object`
- `limit` -- 最多返回的笔记数（1-50，默认 10）
- `offset` -- 要跳过的结果数

---

### 5. 发现对象结构与属性
通过列出对象及其属性定义来了解你的工作区结构。

**工具：** `ATTIO_GET_OBJECT`、`ATTIO_LIST_ATTRIBUTES`

**示例提示：**
> "Attio 中 companies 对象有哪些属性？"

**Get Object 的关键参数：**
- `object_id` -- 对象 slug 或 UUID

**List Attributes 的关键参数：**
- `target` -- "objects" 或 "lists"
- `identifier` -- 对象或列表的 ID/slug

---

### 6. 列出所有记录
通过简单分页从特定对象类型检索记录，按创建顺序返回。

**工具：** `ATTIO_LIST_RECORDS`

**示例提示：**
> "列出 Attio 中前 100 条 people 记录"

**关键参数：**
- 对象类型标识符
- 分页参数

---

## 常见陷阱

- **时间戳格式至关重要**：所有时间戳比较（`created_at`、`updated_at`、自定义时间戳）必须使用 ISO8601 字符串格式（例如 `2025-01-01T00:00:00.000Z`）。使用 Unix 时间戳或数值会导致 "Invalid timestamp value" 错误。
- **name 属性必须嵌套**：`name` 属性有子属性（`first_name`、`last_name`、`full_name`），必须嵌套在 `name` 之下。正确写法：`{"name": {"first_name": {"$contains": "John"}}}`。错误写法：`{"first_name": {...}}` -- 这会因 "unknown_filter_attribute_slug" 而失败。
- **邮箱操作符有限制**：`email_addresses` 支持 `$eq`、`$contains`、`$starts_with`、`$ends_with`，但不支持 `$not_empty`。
- **记录引用类属性需要路径过滤**：对于引用其他记录的属性（例如 "team"、"company"），应使用基于路径的过滤，而不是嵌套语法。示例：`{"path": [["companies", "team"], ["people", "name"]], "constraints": {"first_name": {"$eq": "John"}}}`。
- **"lists" 不是对象类型**：不要将 "lists" 用作 `object_id`。请为列表操作使用专门的列表相关操作。
- **搜索是最终一致的**：`ATTIO_SEARCH_RECORDS` 返回的是最终一致的结果。如需保证结果为最新，请改用 `ATTIO_QUERY_RECORDS`。
- **属性 slug 因工作区而异**：系统属性（例如 "email_addresses"、"name"）是一致的，但自定义属性会有所不同。使用 `ATTIO_LIST_ATTRIBUTES` 来发现你工作区中有效的 slug。

---

## 快速参考

| 操作 | 工具标识 | 必填参数 |
|---|---|---|
| 模糊搜索记录 | `ATTIO_SEARCH_RECORDS` | `query`, `objects`, `request_as` |
| 带过滤器查询 | `ATTIO_QUERY_RECORDS` | `object` |
| 按 ID/属性查找记录 | `ATTIO_FIND_RECORD` | `object_id` |
| 列出笔记 | `ATTIO_LIST_NOTES` | None (optional filters) |
| 获取对象结构 | `ATTIO_GET_OBJECT` | `object_id` |
| 列出属性 | `ATTIO_LIST_ATTRIBUTES` | `target`, `identifier` |
| 列出记录 | `ATTIO_LIST_RECORDS` | Object type |

---

*由 [Composio](https://composio.dev) 提供支持*
