---
name: googlemeet-automation
description: "通过 Rube MCP（Composio）自动化 Google Meet 任务：创建 Meet 会议空间，通过 Calendar 事件安排视频会议，管理会议访问权限。务必先搜索工具以获取当前架构。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 实现 Google Meet 自动化

使用 Rube MCP（Composio）创建 Google Meet 视频会议、安排带有 Meet 链接的会议，并管理会议空间。

**工具包文档**：[composio.dev/toolkits/googlemeet](https://composio.dev/toolkits/googlemeet)

## 前置条件
- 必须已连接 Rube MCP（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 对 `googlemeet` 工具包建立活动连接
- 若要安排带与会者的会议，还需连接 `googlecalendar` 工具包
- 务必先调用 `RUBE_SEARCH_TOOLS` 以获取当前的工具架构

## 设置
**获取 Rube MCP**：在你的客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——只需添加该端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 可用
2. 针对工具包 `googlemeet` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如需安排带日历事件的会议，可选择同时连接 `googlecalendar`
4. 如果连接状态不是 ACTIVE，按返回的身份验证链接完成设置
5. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 创建独立的 Meet 会议空间
使用 `GOOGLEMEET_CREATE_MEET` 创建一个新的 Google Meet 会议空间，并可选择配置其访问类型和接入点。
```
Tool: GOOGLEMEET_CREATE_MEET
Description: 创建一个新的 Google Meet 空间，可选择配置
  其访问类型和接入点。
Note: 调用 RUBE_SEARCH_TOOLS 以获取该工具的完整架构。
```

### 2. 安排带有 Google Meet 链接的会议
使用 `GOOGLECALENDAR_CREATE_EVENT` 创建一个日历事件，该事件会自动生成 Google Meet 链接（默认启用）。
```
Tool: GOOGLECALENDAR_CREATE_EVENT
Parameters:
  - start_datetime (必填): ISO 8601 格式（例如 "2025-01-16T13:00:00"）
  - summary: 会议标题
  - attendees: 邮箱地址列表
  - timezone: IANA 时区（例如 "America/New_York"）
  - event_duration_hour: 时长（小时，默认：0）
  - event_duration_minutes: 时长（分钟，默认：30，最大：59）
  - create_meeting_room: true（默认）—— 生成 Meet 链接
  - description: 会议议程/备注
  - location: 实体或虚拟地点
```

### 3. 查找可用时间段
在安排会议之前，使用 `GOOGLECALENDAR_FIND_FREE_SLOTS` 查找参与者何时有空。
```
Tool: GOOGLECALENDAR_FIND_FREE_SLOTS
Parameters:
  - items: 要检查的日历 ID 列表（例如 ["primary", "user@example.com"]）
  - time_min: 时间窗口的起始（ISO 格式）
  - time_max: 时间窗口的结束（ISO 格式）
  - timezone: IANA 时区
```

### 4. 更新现有会议
使用 `GOOGLECALENDAR_PATCH_EVENT` 修改会议详情、重新安排时间或更新与会者。
```
Tool: GOOGLECALENDAR_PATCH_EVENT
Parameters:
  - calendar_id (必填): 日历 ID（使用 "primary"）
  - event_id (必填): 事件 ID（来自搜索/列表）
  - summary: 更新后的标题
  - start_time / end_time: 重新安排的时间
  - attendees: 更新后的与会者列表（会替换现有列表）
  - send_updates: 通知偏好（"all"、"externalOnly"、"none"）
```

## 常见模式

- **快速会议链接**：使用 `GOOGLEMEET_CREATE_MEET` 创建即时会议空间，而无需日历事件。
- **带与会者的已安排会议**：使用 `GOOGLECALENDAR_CREATE_EVENT` 并设置 `create_meeting_room: true`（默认）来创建一个带嵌入式 Meet 链接的日历事件。Workspace 账户会自动获得 Meet 链接。
- **先检查可用性**：在使用 `GOOGLECALENDAR_CREATE_EVENT` 安排会议之前，用 `GOOGLECALENDAR_FIND_FREE_SLOTS` 查找空闲时间段。
- **将姓名解析为邮箱**：在添加与会者之前，使用 `GMAIL_SEARCH_PEOPLE`（gmail 工具包）根据姓名查找邮箱地址。
- **获取当前时间**：使用带时区的 `GOOGLECALENDAR_GET_CURRENT_DATE_TIME` 获取当前日期/时间，以便相对于“现在”进行排期。

## 已知坑点

- **与会者必须是邮箱地址**：`GOOGLECALENDAR_CREATE_EVENT` 的 attendees 字段只接受邮箱地址，不接受姓名。请先用 `GMAIL_SEARCH_PEOPLE` 将姓名解析为邮箱。
- **个人 Gmail 与 Workspace 的差异**：`create_meeting_room` 功能在 Google Workspace 账户上效果最佳。个人 Gmail 账户会优雅地回退为创建一个没有 Meet 链接的事件。
- **start_datetime 格式**：必须是精确的 ISO 8601 格式（例如 `2025-01-16T13:00:00`）。不支持“明天下午 3 点”之类的自然语言。
- **时长限制**：`event_duration_minutes` 最大为 59。对于 1 小时以上的会议，请结合使用 `event_duration_hour` 和 `event_duration_minutes`。
- **时区至关重要**：务必将 `timezone` 设置为有效的 IANA 标识符（例如 `America/New_York`）。像“EST”或“PST”这样的缩写是无效的。
- **事件 ID 是不透明的**：要更新或删除事件，必须先通过搜索或列表工具获取事件 ID。

## 快速参考
| 操作 | 工具 | 关键参数 |
|--------|------|----------------|
| 创建 Meet 空间 | `GOOGLEMEET_CREATE_MEET` | （通过 RUBE_SEARCH_TOOLS 查看完整架构） |
| 安排会议 | `GOOGLECALENDAR_CREATE_EVENT` | `start_datetime`、`summary`、`attendees`、`timezone` |
| 查找空闲时间段 | `GOOGLECALENDAR_FIND_FREE_SLOTS` | `items`、`time_min`、`time_max`、`timezone` |
| 更新会议 | `GOOGLECALENDAR_PATCH_EVENT` | `calendar_id`、`event_id`、`summary`、`start_time` |
| 获取当前时间 | `GOOGLECALENDAR_GET_CURRENT_DATE_TIME` | `timezone` |
| 查找联系人 | `GMAIL_SEARCH_PEOPLE` | `query` |

---
*Powered by [Composio](https://composio.dev)*
