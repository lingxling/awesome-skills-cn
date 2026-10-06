---
name: Neon Automation
description: "自动化 Neon 无服务器 Postgres 操作 —— 通过 Composio MCP 集成管理项目、分支、数据库、角色和连接 URI。"
requires:
  mcp:
    - rube
---

# Neon Automation

自动化你的 Neon 无服务器 Postgres 工作流 —— 列出项目和分支、检查数据库、获取连接 URI、管理角色，并将 Neon 数据库操作集成到跨应用管道中。

**工具包文档：** [composio.dev/toolkits/neon](https://composio.dev/toolkits/neon)

---

## 设置

1. 将 Composio MCP 服务器添加到你的客户端：`https://rube.app/mcp`
2. 在提示时连接你的 Neon 账户（API 密钥身份验证）
3. 开始使用下面的工作流

---

## 核心工作流

### 1. 列出项目

使用 `NEON_RETRIEVE_PROJECTS_LIST` 发现与已认证用户关联的所有项目。

```
Tool: NEON_RETRIEVE_PROJECTS_LIST
Inputs:
  - org_id: string（使用个人 API 密钥时必填）
  - limit: integer（1-400，默认 10）
  - cursor: string（来自上一响应的分页游标）
  - search: string（按项目名称或 ID 搜索，支持部分匹配）
  - timeout: integer（毫秒；超时时返回部分结果）
```

**重要：** 使用个人 API 密钥时，`org_id` 是必填的。请先通过 `NEON_GET_USER_ORGANIZATIONS` 获取它。

### 2. 获取项目详情

使用 `NEON_ACCESS_PROJECT_DETAILS_BY_ID` 检查项目配置、所有者信息和消耗指标。

```
Tool: NEON_ACCESS_PROJECT_DETAILS_BY_ID
Inputs:
  - project_id: string（必填）—— 格式："形容词-名词-数字"，例如 "dry-smoke-26258271"
```

### 3. 列出项目的分支

使用 `NEON_GET_BRANCHES_FOR_PROJECT` 枚举项目中的分支（开发阶段）。

```
Tool: NEON_GET_BRANCHES_FOR_PROJECT
Inputs:
  - project_id: string（必填）
  - search: string（可选，按分支名称或 ID 搜索）
```

### 4. 列出分支上的数据库

使用 `NEON_FETCH_DATABASE_FOR_BRANCH` 清点特定项目和分支内的数据库。

```
Tool: NEON_FETCH_DATABASE_FOR_BRANCH
Inputs:
  - project_id: string（必填）
  - branch_id: string（必填）
```

### 5. 获取连接 URI

使用 `NEON_GET_PROJECT_CONNECTION_URI` 获取某个项目/分支/数据库的 Postgres 连接字符串。

```
Tool: NEON_GET_PROJECT_CONNECTION_URI
Inputs:
  - project_id: string（必填）
  - database_name: string（必填）—— 例如 "neondb"
  - role_name: string（必填）—— 例如 "neondb_owner"
  - branch_id: string（可选，默认为项目的默认分支）
  - endpoint_id: string（可选，默认为读写端点）
  - pooled: boolean（可选，添加 -pooler 以启用连接池）
```

**安全提示：** 返回的 URI 包含凭证。请将其视为机密 —— 不要记录或分享它。

### 6. 检查数据库详情和角色

使用 `NEON_RETRIEVE_BRANCH_DATABASE_DETAILS` 在连接之前验证数据库，使用 `NEON_GET_BRANCH_ROLES_FOR_PROJECT` 列出可用角色。

```
Tool: NEON_RETRIEVE_BRANCH_DATABASE_DETAILS
Inputs:
  - project_id: string（必填）
  - branch_id: string（必填）
  - database_name: string（必填）

Tool: NEON_GET_BRANCH_ROLES_FOR_PROJECT
Inputs:
  - project_id: string（必填）
  - branch_id: string（必填）
```

---

## 已知坑点

| 坑点 | 详情 |
|---------|--------|
| 需要 org_id | 使用个人 API 密钥时，`NEON_RETRIEVE_PROJECTS_LIST` 会返回 HTTP 400 "org_id is required"。请先调用 `NEON_GET_USER_ORGANIZATIONS`。 |
| 分页不完整 | 如果没有分页，项目列表可能不完整。请使用 `cursor` 迭代直到为空。 |
| 速率限制 | 在密集列出时，`NEON_RETRIEVE_PROJECTS_LIST` 会返回 HTTP 429。请避免冗余调用，并在重试前退避。 |
| 无效的角色/数据库配对 | 当 database_name/role_name 配对无效时，`NEON_GET_PROJECT_CONNECTION_URI` 会返回 401/403。请使用 `NEON_GET_BRANCH_ROLES_FOR_PROJECT` 选择一个允许的角色。 |
| 连接 URI 是机密信息 | 返回的 URI 包含凭证。切勿以明文记录、显示或分享它。 |

---

## 快速参考

| 工具标识 | 描述 |
|-----------|-------------|
| `NEON_RETRIEVE_PROJECTS_LIST` | 列出所有 Neon 项目，支持分页和搜索 |
| `NEON_ACCESS_PROJECT_DETAILS_BY_ID` | 获取项目配置和消耗指标 |
| `NEON_GET_BRANCHES_FOR_PROJECT` | 列出项目中的分支 |
| `NEON_FETCH_DATABASE_FOR_BRANCH` | 列出特定分支上的数据库 |
| `NEON_GET_PROJECT_CONNECTION_URI` | 获取 Postgres 连接 URI（含凭证） |
| `NEON_RETRIEVE_BRANCH_DATABASE_DETAILS` | 检查数据库元数据和设置 |
| `NEON_GET_USER_ORGANIZATIONS` | 列出已认证用户所属的组织 |
| `NEON_CREATE_API_KEY_FOR_ORGANIZATION` | 为组织创建新的 API 密钥 |
| `NEON_GET_BRANCH_ROLES_FOR_PROJECT` | 列出分支上可用的角色 |

---

*Powered by [Composio](https://composio.dev)*
