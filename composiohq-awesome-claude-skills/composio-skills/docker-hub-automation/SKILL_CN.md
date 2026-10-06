---
name: Docker Hub Automation
description: "自动化 Docker Hub 操作 -- 通过 Composio MCP 集成管理组织、仓库、团队、成员和 webhook。"
requires:
  mcp:
    - rube
---

# Docker Hub Automation

自动化你的 Docker Hub 工作流 -- 创建和管理组织、仓库、团队，添加成员，设置镜像推送 webhook，以及列出容器镜像。

**工具包文档：** [composio.dev/toolkits/docker_hub](https://composio.dev/toolkits/docker_hub)

---

## 设置

1. 将 Composio MCP 服务器添加到你的客户端：`https://rube.app/mcp`
2. 按提示连接你的 Docker Hub 账户（JWT/令牌认证）
3. 开始使用下面的工作流

---

## 核心工作流

### 1. 列出组织

使用 `DOCKER_HUB_LIST_ORGANIZATIONS` 查看已认证用户所属的组织。

```
Tool: DOCKER_HUB_LIST_ORGANIZATIONS
Inputs:
  - page: integer (从 1 开始，默认 1)
  - page_size: integer (1-100，默认 25)
```

### 2. 创建组织

使用 `DOCKER_HUB_CREATE_ORGANIZATION` 以编程方式创建新的 Docker Hub 组织。

```
Tool: DOCKER_HUB_CREATE_ORGANIZATION
Inputs:
  - orgname: string（必填） -- 小写，仅允许字母/数字/._-，至少 2 个字符
  - company: string（可选） -- 与该组织关联的公司名称
```

**注意：** 需要通过 `/v2/users/login` 获取的 JWT 认证，并可能存在访问限制。

### 3. 获取组织详情和仓库

使用 `DOCKER_HUB_GET_ORGANIZATION` 获取命名空间信息及其仓库。适用于任何公开的命名空间。

```
Tool: DOCKER_HUB_GET_ORGANIZATION
Inputs:
  - organization: string（必填） -- 例如 "docker"、"bitnami"、"library"
```

### 4. 创建仓库

使用 `DOCKER_HUB_CREATE_REPOSITORY` 在命名空间下创建公开或私有仓库。

```
Tool: DOCKER_HUB_CREATE_REPOSITORY
Inputs:
  - namespace: string（必填） -- Docker Hub 用户名或组织名
  - name: string（必填） -- 小写；允许字母、数字、._-
  - description: string（可选） -- 最多 100 个字符
  - full_description: string（可选） -- Markdown 格式的 README 内容
  - is_private: boolean（默认 false） -- 私有仓库需要付费套餐
```

### 5. 带筛选条件列出仓库

使用 `DOCKER_HUB_LIST_REPOSITORIES` 枚举命名空间内的仓库，支持排序和按内容类型筛选。

```
Tool: DOCKER_HUB_LIST_REPOSITORIES
Inputs:
  - namespace: string（必填） -- 例如 "library"、"myorg"
  - ordering: "name" | "last_updated" | "pull_count"（加 - 前缀表示降序）
  - page: integer（默认 1）
  - page_size: integer（1-100，默认 25）
  - content_types: string（逗号分隔，例如 "image,artifact"）
```

### 6. 管理团队、成员和 Webhook

使用 `DOCKER_HUB_LIST_TEAMS` 列出组织内的团队，使用 `DOCKER_HUB_ADD_ORG_MEMBER` 邀请用户，使用 `DOCKER_HUB_CREATE_WEBHOOK` 设置推送通知。

```
Tool: DOCKER_HUB_LIST_TEAMS
  - 列出 Docker Hub 组织内的所有团队/小组

Tool: DOCKER_HUB_ADD_ORG_MEMBER
  - 通过 Docker ID 或邮箱邀请用户加入组织
  - 需要所有者或管理员权限

Tool: DOCKER_HUB_CREATE_WEBHOOK
  - 在仓库上创建用于镜像推送通知的 webhook
  - 分两步进行：先创建 webhook，再添加 hook URL
  - 需要对该仓库拥有管理员权限
```

---

## 常见陷阱

| 陷阱 | 详情 |
|---------|--------|
| JWT 认证 | `DOCKER_HUB_CREATE_ORGANIZATION` 需要来自 `/v2/users/login` 的 JWT 认证 -- 标准 API 令牌可能不够用。 |
| 私有仓库限制 | 创建私有仓库（`is_private: true`）需要付费的 Docker Hub 套餐。 |
| 组织名称限制 | 组织名称必须为小写，至少 2 个字符，且只能包含字母、数字、`.`、`_` 或 `-`。 |
| Webhook 分两步 | `DOCKER_HUB_CREATE_WEBHOOK` 是一个两步过程：先用名称创建 webhook，再为其添加 hook URL。 |
| 分页 | 所有列表接口都使用基于页码的分页 -- 需逐页遍历直至结果耗尽。 |

---

## 快速参考

| 工具标识 | 描述 |
|-----------|-------------|
| `DOCKER_HUB_LIST_ORGANIZATIONS` | 列出用户所属的组织 |
| `DOCKER_HUB_CREATE_ORGANIZATION` | 创建新的 Docker Hub 组织 |
| `DOCKER_HUB_GET_ORGANIZATION` | 获取组织详情和仓库列表 |
| `DOCKER_HUB_CREATE_REPOSITORY` | 在命名空间下创建仓库 |
| `DOCKER_HUB_LIST_REPOSITORIES` | 带筛选和排序列出仓库 |
| `DOCKER_HUB_LIST_TEAMS` | 列出组织内的团队/小组 |
| `DOCKER_HUB_ADD_ORG_MEMBER` | 邀请用户加入组织 |
| `DOCKER_HUB_CREATE_WEBHOOK` | 在仓库上创建推送通知 webhook |

---

*由 [Composio](https://composio.dev) 提供支持*
