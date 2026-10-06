---
name: Eventbrite Automation
description: "通过自然语言命令自动化 Eventbrite 的活动管理、参会者追踪、组织发现和分类浏览"
requires:
  mcp:
    - rube
---

# Eventbrite Automation

自动化 Eventbrite 活动管理工作流——列出组织活动、追踪参会者、浏览分类和形式、管理组织——全部通过自然语言完成。

**工具包文档：** [composio.dev/toolkits/eventbrite](https://composio.dev/toolkits/eventbrite)

---

## 设置

1. 将 Rube MCP 服务器添加到你的环境中：`https://rube.app/mcp`
2. 按提示连接你的 Eventbrite 账户（通过 Composio 的 OAuth 流程）
3. 开始使用自然语言命令进行 Eventbrite 自动化

---

## 核心工作流

### 1. 发现你的组织

获取已认证用户所属的组织。由于大多数其他 Eventbrite 操作都需要 `organization_id`，这是其前提条件。

**工具：** `EVENTBRITE_LIST_USER_ORGANIZATIONS`

不需要参数。返回组织 ID、名称和元数据。

> 请始终先调用此工具，以获取活动和参会者相关接口所需的 `organization_id`。

示例提示词：
> “列出我的 Eventbrite 组织”

---

### 2. 列出和搜索组织活动

浏览特定组织拥有的活动，支持按状态、时间段筛选和分页。

**工具：** `EVENTBRITE_LIST_ORGANIZATION_EVENTS`

关键参数：
- `organization_id` -- 要列出其活动的组织（必填；从 `EVENTBRITE_LIST_USER_ORGANIZATIONS` 获取）
- `status` -- 按 `live`、`draft`、`canceled`、`started`、`ended`、`completed` 或 `all` 筛选
- `time_filter` -- 按 `current_future` 或 `past` 筛选
- `order_by` -- 按 `start_asc`、`start_desc`、`created_asc`、`created_desc`、`name_asc`、`name_desc` 排序
- `page_size` -- 每页活动数量
- `continuation` -- 来自上一响应的分页令牌
- `expand` -- 以逗号分隔的待展开字段：`organizer`、`venue`、`ticket_classes`

示例提示词：
> “显示我组织的所有 live 活动，按开始日期排序”

---

### 3. 追踪活动参会者

检索任意活动的参会者列表，支持可选的状态筛选和分页。

**工具：** `EVENTBRITE_LIST_EVENT_ATTENDEES`

关键参数：
- `event_id` -- 要检索参会者的活动（必填）
- `status` -- 按 `attending`、`not_attending` 或 `cancelled` 筛选
- `changed_since` -- ISO 8601 时间戳，仅获取近期有变化的参会者
- `continuation` -- 用于获取后续页面的分页令牌

示例提示词：
> “获取活动 123456789 中自 1 月 1 日以来有变动的所有 attending 参会者”

---

### 4. 浏览活动分类

获取用于创建或筛选活动时可用的活动分类。

**工具：** `EVENTBRITE_GET_EVENT_CATEGORIES`

关键参数：
- `locale` -- 用于本地化名称的 BCP-47 语言区域（例如 `en_US`、`es_ES`）

接着可使用 `EVENTBRITE_GET_EVENT_SUBCATEGORIES` 获取所选分类下的子分类。

示例提示词：
> “列出所有英文的 Eventbrite 活动分类”

---

### 5. 列出活动形式

获取所有可用的活动形式类型（会议、研讨会、工作坊等）。

**工具：** `EVENTBRITE_GET_EVENT_FORMATS`

不需要参数。返回形式 ID 和显示名称。

示例提示词：
> “Eventbrite 上有哪些可用的活动形式？”

---

### 6. 浏览活动子分类

获取更细粒度的活动分类子项。

**工具：** `EVENTBRITE_GET_EVENT_SUBCATEGORIES`

关键参数：
- `locale` -- 用于本地化名称的 BCP-47 语言区域（例如 `en_US`）

示例提示词：
> “列出所有 Eventbrite 活动子分类”

---

## 常见陷阱

| 陷阱 | 详情 |
|---------|---------|
| 需要组织 ID | 大多数活动操作都需要 `organization_id` —— 请始终先调用 `EVENTBRITE_LIST_USER_ORGANIZATIONS` |
| 通过 continuation 分页 | 结果使用 continuation 令牌分页，而非页码——需将上一响应中的 `continuation` 值传入以获取下一页 |
| 需先发现活动 ID | 你需要先通过 `EVENTBRITE_LIST_ORGANIZATION_EVENTS` 列出活动，才能获取用于参会者查询的 `event_id` 值 |
| 状态值需精确 | 活动状态值（`live`、`draft`、`canceled`、`started`、`ended`、`completed`）必须完全匹配 |
| expand 字段以逗号分隔 | `expand` 参数接受的是以逗号分隔的字符串，而非数组（例如 `"organizer,venue"`） |
| changed_since 的格式 | `changed_since` 参数必须为 ISO 8601 格式（例如 `2024-01-01T00:00:00Z`） |

---

## 快速参考

| 操作 | 工具 Slug | 关键参数 |
|--------|-----------|------------|
| 列出组织 | `EVENTBRITE_LIST_USER_ORGANIZATIONS` | （无） |
| 列出活动 | `EVENTBRITE_LIST_ORGANIZATION_EVENTS` | `organization_id`、`status`、`time_filter` |
| 列出参会者 | `EVENTBRITE_LIST_EVENT_ATTENDEES` | `event_id`、`status`、`changed_since` |
| 获取分类 | `EVENTBRITE_GET_EVENT_CATEGORIES` | `locale` |
| 获取子分类 | `EVENTBRITE_GET_EVENT_SUBCATEGORIES` | `locale` |
| 获取形式 | `EVENTBRITE_GET_EVENT_FORMATS` | （无） |

---

*由 [Composio](https://composio.dev) 提供支持*
