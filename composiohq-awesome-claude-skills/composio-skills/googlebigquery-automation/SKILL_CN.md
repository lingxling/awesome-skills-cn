---
name: googlebigquery-automation
description: "通过 Rube MCP（Composio）自动化 Google BigQuery 任务：运行 SQL 查询、探索数据集和元数据、通过 Metabase 集成执行 MBQL 查询。务必先搜索工具以获取最新的模式。"
requires:
  mcp: [rube]
---

# Google BigQuery Automation via Rube MCP

通过 Rube MCP（Composio）利用 Metabase 集成来运行 SQL 查询、探索数据库模式并分析数据集。

**工具包文档**：[composio.dev/toolkits/googlebigquery](https://composio.dev/toolkits/googlebigquery)

## 前置条件
- 必须已连接 Rube MCP（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 对 `metabase` 工具包建立活动连接
- 一个已连接到你 BigQuery 数据源的 Metabase 实例
- 务必先调用 `RUBE_SEARCH_TOOLS` 以获取最新的工具模式

## 设置
**获取 Rube MCP**：在你的客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥 —— 只需添加该端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 对工具包 `metabase` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接未处于 ACTIVE 状态，请按返回的身份验证链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

> **注意**：BigQuery 数据是通过 Metabase（一款连接到 BigQuery 作为数据源的商业智能工具）访问的。以下工具通过 Metabase 的 API 执行查询并检索元数据。

## 核心工作流

### 1. 运行原生 SQL 查询
使用类型为 `native` 的 `METABASE_POST_API_DATASET` 对 BigQuery 数据库执行原始 SQL 查询。
```
Tool: METABASE_POST_API_DATASET
Parameters:
  - database (required): Metabase database ID (integer)
  - type (required): "native" for SQL queries
  - native (required): Object with "query" string
    - query: Raw SQL string (e.g., "SELECT * FROM users LIMIT 10")
    - template_tags: Parameterized query variables (optional)
  - constraints: { "max-results": 1000 } (optional)
```

### 2. 运行结构化 MBQL 查询
使用类型为 `query` 的 `METABASE_POST_API_DATASET`，执行带有内置聚合和筛选的 Metabase 查询语言查询。
```
Tool: METABASE_POST_API_DATASET
Parameters:
  - database (required): Metabase database ID
  - type (required): "query" for MBQL
  - query (required): Object with:
    - source-table: Table ID (integer)
    - aggregation: e.g., [["count"]] or [["sum", ["field", 5, null]]]
    - breakout: Group-by fields
    - filter: Filter conditions
    - limit: Max rows
    - order-by: Sort fields
```

### 3. 获取查询元数据
使用 `METABASE_POST_API_DATASET_QUERY_METADATA` 来检索可用于查询的数据库、表和字段的元数据。
```
Tool: METABASE_POST_API_DATASET_QUERY_METADATA
Parameters:
  - database (required): Metabase database ID
  - type (required): "query" or "native"
  - query (required): Query object (e.g., {"source-table": 1})
```

### 4. 将查询转换为原生 SQL
使用 `METABASE_POST_API_DATASET_NATIVE` 将 MBQL 查询转换为其原生 SQL 表示形式。
```
Tool: METABASE_POST_API_DATASET_NATIVE
Parameters:
  - database (required): Metabase database ID
  - type (required): "native"
  - native (required): Object with "query" and optional "template_tags"
  - parameters: Query parameter values (optional)
```

### 5. 列出可用数据库
使用 `METABASE_GET_API_DATABASE` 来发现 Metabase 中配置的所有数据库连接。
```
Tool: METABASE_GET_API_DATABASE
Description: Retrieves a list of all Database instances configured in Metabase.
Note: Call RUBE_SEARCH_TOOLS to get the full schema for this tool.
```

### 6. 获取数据库模式元数据
使用 `METABASE_GET_API_DATABASE_ID_METADATA` 来检索特定数据库的完整表和字段信息。
```
Tool: METABASE_GET_API_DATABASE_ID_METADATA
Description: Retrieves complete metadata for a specific database including
  all tables and fields.
Note: Call RUBE_SEARCH_TOOLS to get the full schema for this tool.
```

## 常见模式

- **先发现再查询**：使用 `METABASE_GET_API_DATABASE` 查找数据库 ID，然后使用 `METABASE_GET_API_DATABASE_ID_METADATA` 探索表和字段，最后使用 `METABASE_POST_API_DATASET` 运行查询。
- **SQL 优先方式**：使用类型为 `"native"` 的 `METABASE_POST_API_DATASET`，编写标准 SQL 查询以获得最大灵活性。
- **参数化查询**：在原生查询中使用 `template_tags` 进行安全的参数化（例如 `SELECT * FROM users WHERE id = {{user_id}}`）。
- **模式探索**：在构建复杂查询之前，使用 `METABASE_POST_API_DATASET_QUERY_METADATA` 来理解表结构。
- **获取参数值**：使用 `METABASE_POST_API_DATASET_PARAMETER_VALUES` 来检索筛选下拉列表的可能取值。

## 已知问题

- `database` 参数是 Metabase 内部的**整数 ID**，不是 BigQuery 的项目名或数据集名。请先使用 `METABASE_GET_API_DATABASE` 查找有效的数据库 ID。
- MBQL 查询中的 `source-table` 同样是 Metabase 内部的整数，不是 BigQuery 的表名。应通过元数据工具发现表 ID。
- 原生 SQL 查询使用 BigQuery SQL 方言（标准 SQL）。请确保语法与 BigQuery 兼容。
- `constraints` 中的 `max-results` 默认值可能限制返回的行数。对于大结果集，应显式设置该值。
- `METABASE_POST_API_DATASET` 的响应结果嵌套在 `data` 字段下 —— 请仔细解析，因为结构可能嵌套很深。
- MBQL 的 `aggregation`、`breakout` 和 `filter` 数组中使用的 Metabase 字段 ID 必须是从元数据响应中获取的整数。

## 快速参考
| 操作 | 工具 | 关键参数 |
|--------|------|----------------|
| 运行 SQL 查询 | `METABASE_POST_API_DATASET` | `database`, `type: "native"`, `native.query` |
| 运行 MBQL 查询 | `METABASE_POST_API_DATASET` | `database`, `type: "query"`, `query` |
| 获取查询元数据 | `METABASE_POST_API_DATASET_QUERY_METADATA` | `database`, `type`, `query` |
| 转换为 SQL | `METABASE_POST_API_DATASET_NATIVE` | `database`, `type`, `native` |
| 获取参数值 | `METABASE_POST_API_DATASET_PARAMETER_VALUES` | `parameter`, `field_ids` |
| 列出数据库 | `METABASE_GET_API_DATABASE` | （通过 RUBE_SEARCH_TOOLS 查看完整模式） |
| 获取数据库元数据 | `METABASE_GET_API_DATABASE_ID_METADATA` | （通过 RUBE_SEARCH_TOOLS 查看完整模式） |

---
*Powered by [Composio](https://composio.dev)*
