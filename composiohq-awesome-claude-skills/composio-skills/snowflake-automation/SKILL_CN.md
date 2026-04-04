---
name: Snowflake Automation
description: "自动化 Snowflake 数据仓库操作 -- 列出数据库、架构和表，执行 SQL 语句，并通过 Composio MCP 集成管理数据工作流。"
requires:
  mcp:
    - rube
---

# Snowflake 自动化

自动化您的 Snowflake 数据仓库工作流 -- 发现数据库、浏览架构和表、执行任意 SQL（SELECT、DDL、DML），并将 Snowflake 数据操作集成到跨应用程序管道中。

**工具包文档:** [composio.dev/toolkits/snowflake](https://composio.dev/toolkits/snowflake)

---

## 设置

1. 将 Composio MCP 服务器添加到您的客户端：`https://rube.app/mcp`
2. 在提示时连接您的 Snowflake 账户（帐户凭据或密钥对认证）
3. 开始使用以下工作流

---

## 核心工作流

### 1. 列出数据库

使用 `SNOWFLAKE_SHOW_DATABASES` 发现可用数据库，支持可选过滤和时间旅行功能。

```
工具：SNOWFLAKE_SHOW_DATABASES
输入：
  - like_pattern: string (SQL 通配符，例如 "%test%") -- 不区分大小写
  - starts_with: string (例如 "PROD") -- 区分大小写
  - limit: integer (最大 10000)
  - history: boolean (包括时间旅行保留期内已删除的数据库)
  - terse: boolean (返回列的子集：created_on, name, kind, database_name, schema_name)
  - role: string (用于执行的角色)
  - warehouse: string (可选，SHOW DATABASES 不需要)
  - timeout: integer (秒)
```

### 2. 浏览架构

使用 `SNOWFLAKE_SHOW_SCHEMAS` 列出数据库内或跨账户的架构。

```
工具：SNOWFLAKE_SHOW_SCHEMAS
输入：
  - database: string (数据库上下文)
  - in_scope: "ACCOUNT" | "DATABASE" | "<specific_database_name>"
  - like_pattern: string (SQL 通配符过滤器)
  - starts_with: string (区分大小写的前缀)
  - limit: integer (最大 10000)
  - history: boolean (包括已删除的架构)
  - terse: boolean (仅子集列)
  - role, warehouse, timeout: string/integer (可选)
```

### 3. 列出表

使用 `SNOWFLAKE_SHOW_TABLES` 发现表及其元数据，包括行数、大小和聚类键。

```
工具：SNOWFLAKE_SHOW_TABLES
输入：
  - database: string (数据库上下文)
  - schema: string (架构上下文)
  - in_scope: "ACCOUNT" | "DATABASE" | "SCHEMA" | "<specific_name>"
  - like_pattern: string (例如 "%customer%")
  - starts_with: string (例如 "FACT", "DIM", "TEMP")
  - limit: integer (最大 10000)
  - history: boolean (包括已删除的表)
  - terse: boolean (仅子集列)
  - role, warehouse, timeout: string/integer (可选)
```

### 4. 执行 SQL 语句

使用 `SNOWFLAKE_EXECUTE_SQL` 执行 SELECT 查询、DDL（CREATE/ALTER/DROP）和 DML（INSERT/UPDATE/DELETE），支持参数化绑定。

```
工具：SNOWFLAKE_EXECUTE_SQL
输入：
  - statement: string (必需) -- SQL 语句，多语句用分号分隔
  - database: string (区分大小写，回退到 DEFAULT_NAMESPACE)
  - schema_name: string (区分大小写)
  - warehouse: string (区分大小写，计算密集型查询必需)
  - role: string (区分大小写，回退到 DEFAULT_ROLE)
  - bindings: object (参数化查询值以防止 SQL 注入)
  - parameters: object (Snowflake 会话级参数)
  - timeout: integer (秒；0 = 最大 604800s)
```

**示例：**
- `"SELECT * FROM my_table LIMIT 100;"`
- `"CREATE TABLE test (id INT, name STRING);"`
- `"ALTER SESSION SET QUERY_TAG='mytag'; SELECT COUNT(*) FROM my_table;"`

---

## 已知陷阱

| 陷阱 | 详情 |
|---------|--------|
| 大小写敏感性 | 数据库、架构、仓库和角色名称在 `SNOWFLAKE_EXECUTE_SQL` 中区分大小写。 |
| 计算需要仓库 | SELECT 和 DML 查询需要运行中的仓库。SHOW 命令不需要。 |
| 多语句执行 | 用分号分隔的多个语句会自动按顺序执行。 |
| SQL 注入防护 | 始终使用 `bindings` 参数处理用户提供的值以防止注入攻击。 |
| 使用 LIMIT 分页 | `SHOW` 命令支持 `limit`（最大 10000）和 `from_name` 进行基于游标的分页。 |
| 时间旅行 | 设置 `history: true` 以包括仍在保留期内的已删除对象。 |

---

## 快速参考

| 工具标识符 | 描述 |
|-----------|-------------|
| `SNOWFLAKE_SHOW_DATABASES` | 列出数据库，支持过滤和时间旅行 |
| `SNOWFLAKE_SHOW_SCHEMAS` | 列出数据库内或账户范围的架构 |
| `SNOWFLAKE_SHOW_TABLES` | 列出表及其元数据（行数、大小、聚类） |
| `SNOWFLAKE_EXECUTE_SQL` | 执行 SQL：SELECT、DDL、DML，支持参数化绑定 |

---

*由 [Composio](https://composio.dev) 提供支持*
