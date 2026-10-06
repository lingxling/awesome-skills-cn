---
name: LaunchDarkly Automation
description: "自动化 LaunchDarkly 功能开关管理 -- 列出项目和环境、创建和删除触发器工作流，并通过 Composio MCP 集成跟踪代码引用。"
requires:
  mcp:
    - rube
---

# LaunchDarkly 自动化

自动化你的 LaunchDarkly 功能开关工作流 -- 枚举项目和环境、创建由 webhook 驱动的开关触发器、管理触发器生命周期，并跨代码仓库审计代码引用。

**工具包文档：** [composio.dev/toolkits/launch_darkly](https://composio.dev/toolkits/launch_darkly)

---

## 设置

1. 将 Composio MCP 服务器添加到你的客户端：`https://rube.app/mcp`
2. 在提示时连接你的 LaunchDarkly 账户（API 密钥认证）
3. 开始使用下面的工作流

---

## 核心工作流

### 1. 列出项目

使用 `LAUNCH_DARKLY_LIST_PROJECTS` 发现所有项目及其 key，以供后续操作使用。

```
Tool: LAUNCH_DARKLY_LIST_PROJECTS
Inputs:
  - filter: string (e.g., "query:myproject" or "keys:proj1,proj2" or "tags:mytag")
  - expand: string (e.g., "environments" to include env list per project)
  - limit: integer (default 20)
  - offset: integer (pagination start index)
  - sort: string (e.g., "name" or "-name" for descending)
```

### 2. 获取项目的环境

使用 `LAUNCH_DARKLY_GET_ENVIRONMENTS` 列出项目内的所有环境（production、staging、test 等）。

```
Tool: LAUNCH_DARKLY_GET_ENVIRONMENTS
Inputs:
  - project_key: string (required) -- e.g., "my-project", "default"
  - filter: string (e.g., "query:production")
  - limit: integer (default 20)
  - offset: integer (pagination)
  - sort: string (e.g., "name" or "-name")
```

### 3. 创建开关触发器工作流

使用 `LAUNCH_DARKLY_CREATE_TRIGGER_WORKFLOW` 设置由外部事件（webhook、Datadog 告警等）触发的自动开关切换。

```
Tool: LAUNCH_DARKLY_CREATE_TRIGGER_WORKFLOW
Inputs:
  - project_key: string (required)
  - feature_flag_key: string (required) -- e.g., "new-feature", "enable-dark-mode"
  - environment_key: string (required) -- e.g., "production", "staging"
  - integration_key: string (default "generic-trigger") -- or "datadog", "honeycomb", "dynatrace"
  - instructions: array of objects (optional):
      - kind: "flag_action" (fixed)
      - action: "turnFlagOn" | "turnFlagOff"
  - comment: string (optional) -- description of the trigger purpose
```

该触发器会生成一个唯一的 webhook URL，调用它即可执行已配置的开关操作。

### 4. 删除开关触发器工作流

使用 `LAUNCH_DARKLY_DELETE_TRIGGER_WORKFLOW` 永久移除触发器及其 URL。

```
Tool: LAUNCH_DARKLY_DELETE_TRIGGER_WORKFLOW
Inputs:
  - project_key: string (required)
  - feature_flag_key: string (required)
  - environment_key: string (required)
  - id: string (required) -- the trigger ID returned during creation
```

**警告：** 删除不可逆。触发器及其 URL 无法恢复。

### 5. 列出代码引用仓库

使用 `LAUNCH_DARKLY_LIST_CODE_REFERENCE_REPOSITORIES` 跟踪功能开关在你的代码库中的使用位置。

```
Tool: LAUNCH_DARKLY_LIST_CODE_REFERENCE_REPOSITORIES
Inputs:
  - projKey: string (optional) -- filter by project key
  - flagKey: string (optional) -- filter by feature flag key
  - withBranches: string (any value to include branch data)
  - withReferencesForDefaultBranch: string (any value to include code refs for default branch)
```

**注意：** 代码引用是企业版功能，需要 `code-reference-repository` 写入权限。

---

## 已知陷阱

| 陷阱 | 详情 |
|---------|--------|
| 项目 key 发现 | 在调用其他工具之前，始终先使用 `LAUNCH_DARKLY_LIST_PROJECTS` 查找有效的项目 key。 |
| 环境 key 格式 | 环境 key 是小写 slug（例如 "production"、"test"），而不是显示名称。 |
| 触发器删除是永久的 | 一旦通过 `LAUNCH_DARKLY_DELETE_TRIGGER_WORKFLOW` 删除，触发器 URL 将无法恢复。 |
| 仅限企业版的代码引用 | `LAUNCH_DARKLY_LIST_CODE_REFERENCE_REPOSITORIES` 需要企业版套餐和写入权限。 |
| 触发器指令格式 | 每个指令对象都需要 `kind: "flag_action"`（固定常量），并且 `action` 为 `turnFlagOn` 或 `turnFlagOff`。 |

---

## 快速参考

| 工具 Slug | 描述 |
|-----------|-------------|
| `LAUNCH_DARKLY_LIST_PROJECTS` | 列出所有项目，支持过滤和分页 |
| `LAUNCH_DARKLY_GET_ENVIRONMENTS` | 列出项目内的环境 |
| `LAUNCH_DARKLY_CREATE_TRIGGER_WORKFLOW` | 创建由 webhook 驱动的开关触发器 |
| `LAUNCH_DARKLY_DELETE_TRIGGER_WORKFLOW` | 永久删除开关触发器 |
| `LAUNCH_DARKLY_LIST_CODE_REFERENCE_REPOSITORIES` | 列出包含开关代码引用的仓库 |

---

*由 [Composio](https://composio.dev) 提供支持*
