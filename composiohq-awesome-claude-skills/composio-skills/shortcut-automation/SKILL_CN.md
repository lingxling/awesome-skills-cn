---
name: Shortcut Automation
description: "自动化 Shortcut 中的项目管理工作流——创建故事（stories）、管理任务、跟踪 epics，并通过自然语言命令组织工作流。"
requires:
  mcp:
    - rube
---

# Shortcut Automation

直接从 Claude Code 自动化你的 Shortcut 项目管理操作。创建和列出故事（stories）、添加任务和评论、批量创建故事，并浏览工作流——全部无需离开你的终端。

**工具包文档：** [composio.dev/toolkits/shortcut](https://composio.dev/toolkits/shortcut)

---

## 设置

1. 将 Rube MCP 服务器添加到你的 Claude Code 配置中，URL 为：`https://rube.app/mcp`
2. 按提示通过提供的连接链接验证你的 Shortcut 账户
3. 开始使用自然语言自动化你的项目管理工作流

---

## 核心工作流

### 1. 创建故事（Stories）

向你的 Shortcut 工作区添加具有完整配置的新故事。

**工具：** `SHORTCUT_CREATE_STORY`

```
在工作流状态 500000001 中创建一个名为 "Add dark mode support" 的功能故事，估点为 5，标签为 "frontend"
```

`SHORTCUT_CREATE_STORY` 的关键参数：
- `name`（必填）—— 故事标题
- `workflow_state_id` —— 放置故事所在的工作流状态（推荐优先使用，而非 `project_id`）
- `story_type` —— `"feature"`、`"bug"` 或 `"chore"`
- `description` —— 故事正文/描述
- `estimate` —— 数值点数估计（或 null 表示未估计）
- `epic_id` —— 关联某个 epic
- `iteration_id` —— 关联某个迭代
- `labels` —— 标签对象数组，包含 `name`（以及可选的 `color`、`description`）
- `owner_ids` —— 要指派的成员 UUID 数组
- `deadline` —— ISO 8601 格式的截止日期
- `tasks` —— 内联任务数组，包含 `description` 以及可选的 `complete`、`owner_ids`
- `comments` —— 内联评论数组，包含 `text`
- `story_links` —— 使用 `verb`（`"blocks"`、`"duplicates"`、`"relates to"`）链接故事

**重要：** `workflow_state_id` 或 `project_id` 必须二者选一提供。两者都提供或都不提供都会导致请求被拒绝。推荐使用 `workflow_state_id`，因为 Projects 功能正在被 Shortcut 淘汰。

### 2. 批量创建故事

在单次 API 调用中创建多个故事。

**工具：** `SHORTCUT_CREATE_MULTIPLE_STORIES`

```
创建 3 个缺陷故事："Login page 500 error"、"Cart total rounding issue" 和 "Search results empty state broken"
```

- 需要 `stories` 数组，其中每个元素遵循与 `SHORTCUT_CREATE_STORY` 相同的结构
- 数组中的每个故事都需要 `name`
- 适用于批量导入、冲刺计划，或基于模板的故事创建

### 3. 列出项目中的故事

检索特定项目中的所有故事。

**工具：** `SHORTCUT_LIST_STORIES`

```
列出项目 42 中的所有故事及其描述
```

- 需要 `project__public__id`（整数项目 ID）
- 可选 `includes_description: true`，在响应中包含故事描述
- 返回所有故事及其属性（状态、类型、估点等）

### 4. 管理故事任务

在故事内创建任务（检查清单），用于跟踪子工作。

**工具：** `SHORTCUT_CREATE_TASK`

```
为故事 12345 添加任务 "Write unit tests for dark mode toggle"
```

关键参数：
- `story__public__id`（必填）—— 父故事 ID
- `description`（必填）—— 任务描述
- `complete` —— 布尔值，默认为 false
- `owner_ids` —— 要指派该任务的成员 UUID 数组
- `external_id` —— 如从外部工具导入时的 ID

### 5. 添加故事评论

在故事上发布评论，用于讨论和记录。

**工具：** `SHORTCUT_CREATE_STORY_COMMENT`

```
在故事 12345 上添加评论："已审查实现——看起来不错，但需要进行无障碍测试"
```

关键参数：
- `story__public__id`（必填）—— 故事 ID
- `text`（必填）—— 评论内容
- `author_id` —— 成员 UUID（默认为 API 令牌所有者）
- `parent_id` —— 父评论的 ID，用于线程式回复

### 6. 工作流和项目发现

列出工作流和项目，以解析用于创建故事的 ID。

**工具：** `SHORTCUT_LIST_WORKFLOWS`、`SHORTCUT_LIST_PROJECTS`

```
显示我们 Shortcut 工作区中的所有工作流，以便我找到正确的工作流状态 ID
```

- `SHORTCUT_LIST_WORKFLOWS` 返回所有工作流及其状态（ID、名称、类型）
- `SHORTCUT_LIST_PROJECTS` 返回所有项目及其属性
- 在创建故事之前，使用这些工具发现有效的 `workflow_state_id` 和 `project_id` 值

---

## 常见陷阱

- **`workflow_state_id` 与 `project_id` 的区别：** `SHORTCUT_CREATE_STORY` 恰好需要这两者之一。两者都提供或都不提供都会导致请求被拒绝。优先使用 `workflow_state_id`，因为 Projects 功能正在被淘汰。
- **Projects 功能正在被淘汰：** Shortcut 正在用基于工作流的组织方式取代 Projects。对于新故事，请使用 `workflow_state_id`。
- **标签创建是内联的：** `labels` 数组中的标签如果不存在会被即时创建。每个标签对象都需要 `name` 字段。
- **故事类型的默认值：** 如果省略 `story_type`，默认为 `"feature"`。对于缺陷和杂务，请始终明确设置。
- **批量限制：** `SHORTCUT_CREATE_MULTIPLE_STORIES` 在单次请求中处理所有故事。非常大的批次可能会超时——请将批次保持在 25 个故事以下。
- **故事/项目使用整数 ID：** 故事和项目 ID 是整数，而不是 UUID。成员和组 ID 是 UUID。混用这些格式会导致错误。
- **`move_to` 定位：** `move_to` 字段（`"first"` 或 `"last"`）会在其工作流状态内移动故事，而不是跨状态移动。

---

## 快速参考

| 工具标识 | 描述 |
|---|---|
| `SHORTCUT_CREATE_STORY` | 创建单个故事（需要 `name` + `workflow_state_id` 或 `project_id`） |
| `SHORTCUT_CREATE_MULTIPLE_STORIES` | 批量创建多个故事（需要 `stories` 数组） |
| `SHORTCUT_LIST_STORIES` | 列出项目中的故事（需要 `project__public__id`） |
| `SHORTCUT_CREATE_TASK` | 在故事中创建任务（需要 `story__public__id`、`description`） |
| `SHORTCUT_CREATE_STORY_COMMENT` | 向故事添加评论（需要 `story__public__id`、`text`） |
| `SHORTCUT_CREATE_STORY_FROM_TEMPLATE` | 从模板创建故事 |
| `SHORTCUT_LIST_WORKFLOWS` | 列出所有工作流及其状态 |
| `SHORTCUT_LIST_PROJECTS` | 列出所有项目 |

---

*由 [Composio](https://composio.dev) 提供支持*
