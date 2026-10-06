---
name: google-admin-automation
description: "通过 Rube MCP（Composio）自动化 Google Workspace 管理任务：管理用户、群组、成员资格、暂停账户、创建用户、添加别名。请始终先搜索工具以获取最新的模式。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 自动化 Google Workspace 管理

使用 Rube MCP（Composio）以编程方式管理 Google Workspace 用户、群组、成员资格和组织设置。

**工具包文档**：[composio.dev/toolkits/google_admin](https://composio.dev/toolkits/google_admin)

## 前置条件
- 必须已连接 Rube MCP（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 对工具包 `google_admin` 建立有效连接
- 已认证账户需具有 Google Workspace 管理员权限
- 始终先调用 `RUBE_SEARCH_TOOLS` 以获取当前的工具模式

## 设置
**获取 Rube MCP**：将 `https://rube.app/mcp` 作为 MCP 服务器添加到你的客户端配置中。无需 API 密钥——只需添加端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 是否可用
2. 对工具包 `google_admin` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接未处于 ACTIVE 状态，请按返回的认证链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 列出所有用户
使用 `GOOGLE_ADMIN_LIST_USERS` 检索 Google Workspace 用户，支持可选的筛选和分页。
```
工具：GOOGLE_ADMIN_LIST_USERS
参数：
  - customer：客户 ID 或 "my_customer"（默认）
  - domain：要列出用户的域
  - query：筛选字符串（例如 "orgName=Engineering"、"isSuspended=false"）
  - max_results：最大结果数（1-500，默认 100）
  - order_by：按 "email"、"givenName" 或 "familyName" 排序
  - sort_order："ASCENDING" 或 "DESCENDING"
  - page_token：分页令牌
```

### 2. 创建新用户
使用 `GOOGLE_ADMIN_CREATE_USER` 配置新的 Google Workspace 账户。
```
工具：GOOGLE_ADMIN_CREATE_USER
参数：
  - primary_email（必需）：用户邮箱（例如 "john.doe@company.com"）
  - given_name（必需）：名
  - family_name（必需）：姓
  - password（必需）：符合域要求的密码
  - org_unit_path：组织单位（默认："/"）
  - change_password_at_next_login：强制下次登录时更改密码（默认：true）
  - recovery_email：恢复邮箱地址
  - recovery_phone：恢复电话号码
  - suspended：账户是否以暂停状态开始（默认：false）
```

### 3. 列出和管理群组
使用 `GOOGLE_ADMIN_LIST_GROUPS` 列出群组，使用 `GOOGLE_ADMIN_CREATE_GROUP` 创建新群组。
```
工具：GOOGLE_ADMIN_LIST_GROUPS
参数：
  - customer："my_customer"（默认）
  - domain：按域筛选
  - query：筛选条件（例如 "name=Engineering*"）
  - max_results：最大结果数（1-200）
  - order_by：按 "email" 排序
  - page_token：分页令牌

工具：GOOGLE_ADMIN_CREATE_GROUP
参数：
  - email（必需）：群组邮箱地址（例如 "engineering@company.com"）
  - name（必需）：显示名称（例如 "Engineering Team"）
  - description：群组用途描述
```

### 4. 将用户添加到群组
使用 `GOOGLE_ADMIN_ADD_USER_TO_GROUP` 管理群组成员资格。
```
工具：GOOGLE_ADMIN_ADD_USER_TO_GROUP
参数：
  - group_key（必需）：群组邮箱或 ID
  - user_key（必需）：要添加的用户邮箱或 ID
  - role："MEMBER"（默认）、"MANAGER" 或 "OWNER"
```

### 5. 暂停或取消暂停用户
使用 `GOOGLE_ADMIN_SUSPEND_USER` 切换用户账户的暂停状态。
```
工具：GOOGLE_ADMIN_SUSPEND_USER
参数：
  - user_key（必需）：用户的邮箱或唯一 ID
  - suspended：true 表示暂停，false 表示取消暂停（默认：true）
  - suspension_reason：暂停原因（可选）
```

### 6. 获取用户或群组详情
使用 `GOOGLE_ADMIN_GET_USER` 或 `GOOGLE_ADMIN_GET_GROUP` 获取详细信息。
```
工具：GOOGLE_ADMIN_GET_USER
参数：
  - user_key（必需）：用户的邮箱或唯一 ID

工具：GOOGLE_ADMIN_GET_GROUP
参数：
  - group_key（必需）：群组的邮箱或唯一 ID
```

## 常见模式

- **入职工作流**：使用 `GOOGLE_ADMIN_CREATE_USER` 配置账户，然后使用 `GOOGLE_ADMIN_ADD_USER_TO_GROUP` 将其添加到相关群组。
- **离职工作流**：使用 `GOOGLE_ADMIN_SUSPEND_USER` 禁用访问权限，或使用 `GOOGLE_ADMIN_DELETE_USER` 进行永久移除。
- **审计群组成员资格**：使用 `GOOGLE_ADMIN_LIST_GROUPS` 查找群组，然后使用 `GOOGLE_ADMIN_LIST_GROUP_MEMBERS` 查看成员。
- **批量用户管理**：使用 `GOOGLE_ADMIN_LIST_USERS` 列出用户并筛选查询，然后迭代执行更新。
- **添加邮箱别名**：使用 `GOOGLE_ADMIN_ADD_USER_ALIAS` 为用户添加备用邮箱地址。
- **查找用户详情**：在进行更改之前，使用 `GOOGLE_ADMIN_GET_USER` 获取完整的档案信息。

## 已知陷阱

- **需要管理员权限**：所有工具都要求已认证用户具有 Google Workspace 管理员权限。非管理员账户将收到权限错误。
- **删除是永久性的**：`GOOGLE_ADMIN_DELETE_USER` 会永久删除用户账户。此操作无法撤销。
- **user_key 接受邮箱或 ID**：`user_key` 参数既接受用户的主邮箱地址，也接受其唯一的数字用户 ID。
- **群组成员资格会被替换**：添加到群组时，`role` 参数控制成员的角色。没有"更新角色"的操作——要更改角色需移除后重新添加。
- **客户 ID**：对已认证用户的组织使用 `"my_customer"` 作为 `customer` 参数。特定的客户 ID 形如 `C01abc123`。
- **分页**：用户和群组列表端点都可能返回分页结果。始终检查响应中的 `page_token` 以获取完整结果。
- **密码要求**：`GOOGLE_ADMIN_CREATE_USER` 要求密码符合域的密码策略。弱密码将被拒绝。

## 快速参考
| 操作 | 工具 | 关键参数 |
|--------|------|----------------|
| 列出用户 | `GOOGLE_ADMIN_LIST_USERS` | `customer`、`domain`、`query`、`max_results` |
| 获取用户详情 | `GOOGLE_ADMIN_GET_USER` | `user_key` |
| 创建用户 | `GOOGLE_ADMIN_CREATE_USER` | `primary_email`、`given_name`、`family_name`、`password` |
| 删除用户 | `GOOGLE_ADMIN_DELETE_USER` | `user_key` |
| 暂停用户 | `GOOGLE_ADMIN_SUSPEND_USER` | `user_key`、`suspended` |
| 添加用户别名 | `GOOGLE_ADMIN_ADD_USER_ALIAS` | （通过 RUBE_SEARCH_TOOLS 查看完整模式） |
| 列出群组 | `GOOGLE_ADMIN_LIST_GROUPS` | `customer`、`domain`、`query` |
| 获取群组详情 | `GOOGLE_ADMIN_GET_GROUP` | `group_key` |
| 创建群组 | `GOOGLE_ADMIN_CREATE_GROUP` | `email`、`name`、`description` |
| 添加到群组 | `GOOGLE_ADMIN_ADD_USER_TO_GROUP` | `group_key`、`user_key`、`role` |
| 列出群组成员 | `GOOGLE_ADMIN_LIST_GROUP_MEMBERS` | （通过 RUBE_SEARCH_TOOLS 查看完整模式） |

---
*由 [Composio](https://composio.dev) 提供支持*
