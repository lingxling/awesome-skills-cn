---
name: Gong Automation
description: "通过 Composio MCP 集成，使用自然语言自动化 Gong 对话智能 -- 获取通话录音、转录文本、详细分析数据、发言人统计信息以及工作区数据。"
category: conversation-intelligence
requires:
  mcp:
    - rube
---

# Gong Automation

从销售通话中挖掘洞见 -- 获取转录文本、按日期范围分析通话数据、访问带有主题和追踪器的详细对话分析，并管理工作区 -- 全部通过自然语言命令完成。

**工具包文档：** [composio.dev/toolkits/gong](https://composio.dev/toolkits/gong)

---

## 设置

1. 将 Composio MCP 服务器添加到你的客户端配置中：
   ```
   https://rube.app/mcp
   ```
2. 按提示连接你的 Gong 账户（OAuth / Bearer token 身份验证）。
3. 开始使用自然语言命令分析你的通话数据。

---

## 核心工作流

### 1. 按日期范围获取通话转录文本
获取指定时间段内所有通话的转录文本，可选按特定通话 ID 或工作区进行筛选。

**工具：** `GONG_RETRIEVE_TRANSCRIPTS_OF_CALLS_V2_CALLS_TRANSCRIPT`

**示例提示：**
> "获取 2025 年 2 月 1 日至 10 日所有通话的 Gong 转录文本"

**关键参数：**
- `filter__fromDateTime` -- ISO-8601 起始日期（例如 `2025-02-01T00:00:00Z`）
- `filter__toDateTime` -- ISO-8601 结束日期（例如 `2025-02-10T23:59:59Z`）
- `filter__callIds` -- 可选的特定通话 ID 数组筛选
- `filter__workspaceId` -- 可选的工作区 ID 筛选
- `cursor` -- 来自上一个响应的分页游标

**所需权限范围：** `api:calls:read:transcript`

---

### 2. 获取特定通话的转录文本
使用 filter 对象获取包含发言人信息、时间戳和主题分类的转录文本。

**工具：** `GONG_GET_CALL_TRANSCRIPT`

**示例提示：**
> "获取通话 ID 555785916001072125 的 Gong 转录文本"

**关键参数（filter 为必填）：**
- `filter.callIds` -- 特定通话 ID 数组（例如 `["555785916001072125"]`）
- `filter.fromDateTime` -- ISO-8601 起始日期
- `filter.toDateTime` -- ISO-8601 结束日期
- `filter.workspaceId` -- 可选的工作区筛选
- `cursor` -- 分页游标

---

### 3. 按日期范围列出通话
获取指定日期范围内通话的基本元数据（参与者、时长、时间信息）。

**工具：** `GONG_RETRIEVE_CALL_DATA_BY_DATE_RANGE_V2_CALLS`

**示例提示：**
> "列出上周所有的 Gong 通话"

**关键参数（均为必填）：**
- `fromDateTime` -- ISO-8601 起始日期（例如 `2025-02-03T00:00:00Z`）
- `toDateTime` -- ISO-8601 结束日期（例如 `2025-02-10T00:00:00Z`）
- `workspaceId` -- 可选的工作区筛选
- `cursor` -- 分页游标

**所需权限范围：** `api:calls:read:basic`

---

### 4. 获取详细的通话分析数据
获取广泛的通话详情，包括亮点、要点、主题、追踪器、发言人统计、问题以及媒体 URL。

**工具：** `GONG_RETRIEVE_FILTERED_CALL_DETAILS`

**示例提示：**
> "获取本周 Gong 通话的详细分析，包括主题、要点和发言人统计"

**关键参数：**
- `filter__fromDateTime` / `filter__toDateTime` -- 日期范围筛选
- `filter__callIds` -- 特定通话 ID
- `filter__primaryUserIds` -- 按主持人用户 ID 筛选
- 内容选择器（均为布尔值）：
  - `contentSelector__exposedFields__content__keyPoints` -- 通话要点
  - `contentSelector__exposedFields__content__topics` -- 主题时长
  - `contentSelector__exposedFields__content__highlights` -- 通话亮点
  - `contentSelector__exposedFields__content__outline` -- 通话大纲
  - `contentSelector__exposedFields__content__brief` -- Spotlight 通话简报
  - `contentSelector__exposedFields__content__callOutcome` -- 通话结果
  - `contentSelector__exposedFields__content__trackers` -- 智能/关键词追踪器
  - `contentSelector__exposedFields__content__trackerOccurrences` -- 追踪器出现时间与发言人（需 trackers=true）
  - `contentSelector__exposedFields__interaction__speakers` -- 每位参与者的发言时长
  - `contentSelector__exposedFields__interaction__questions` -- 问题数量
  - `contentSelector__exposedFields__interaction__personInteractionStats` -- 主持人统计信息
  - `contentSelector__exposedFields__media` -- 音频/视频 URL（有效期 8 小时）
  - `contentSelector__exposedFields__parties` -- 参与方信息
  - `contentSelector__exposedFields__collaboration__publicComments` -- 公开评论
- `contentSelector__context` -- "Basic"、"Extended" 或 "None"，用于 CRM/外部系统关联

**所需权限范围：** `api:calls:read:extensive`（如需媒体则还需 `api:calls:read:media-url`）

---

### 5. 按 ID 获取特定通话
使用其唯一的 Gong ID 获取单次通话的基本数据。

**工具：** `GONG_RETRIEVE_DATA_FOR_A_SPECIFIC_CALL_V2_CALLS_ID`

**示例提示：**
> "获取 Gong 通话 1223781272986876929 的详情"

**关键参数（必填）：**
- `id` -- Gong 为该通话分配的唯一数字标识符（最多 20 位）

**所需权限范围：** `api:calls:read:basic`

---

### 6. 列出公司工作区
获取你 Gong 组织中的所有工作区，以便获取用于筛选的工作区 ID。

**工具：** `GONG_LIST_ALL_COMPANY_WORKSPACES_V2_WORKSPACES`

**示例提示：**
> "列出我公司的所有 Gong 工作区"

**关键参数：** 无需任何参数。

**所需权限范围：** `api:workspaces:read`

---

## 常见陷阱

- **ISO-8601 日期格式是必须的**：所有日期参数都必须使用带时区的 ISO-8601 格式：`2025-02-01T00:00:00Z` 或 `2025-02-01T02:30:00-07:00`。普通日期格式将会失败。
- **日期范围在 toDateTime 上是排他的**：`toDateTime` 参数返回的是在指定时间之前（但不包括该时间）开始的通话。要包含某一天的通话，请将 `toDateTime` 设置为次日。
- **大结果集需要分页**：所有列表端点都返回分页结果。使用上一个响应中的 `cursor` 值来获取下一页。持续获取直到不再返回 cursor。
- **权限范围要求因端点而异**：不同端点需要不同的 API 权限范围。转录文本访问需要 `api:calls:read:transcript`，基本通话数据需要 `api:calls:read:basic`，详细分析需要 `api:calls:read:extensive`。
- **媒体 URL 8 小时后过期**：详细通话端点返回的音频和视频 URL 是临时的，8 小时后会过期。
- **追踪器出现数据的可用性**：追踪器出现数据（时间和发言人 ID）仅适用于 2023 年 1 月 1 日之后录制的通话。如需回填，请联系 Gong 支持。
- **网络会议通话与常规通话的区别**：对于 Gong 录制的网络会议通话，日期代表的是预定时间。对于其他通话，代表的是实际开始时间。

---

## 快速参考

| 操作 | 工具 Slug | 必填参数 |
|---|---|---|
| 按日期获取转录文本 | `GONG_RETRIEVE_TRANSCRIPTS_OF_CALLS_V2_CALLS_TRANSCRIPT` | 无（建议提供日期范围） |
| 获取通话转录文本 | `GONG_GET_CALL_TRANSCRIPT` | `filter` 对象 |
| 按日期列出通话 | `GONG_RETRIEVE_CALL_DATA_BY_DATE_RANGE_V2_CALLS` | `fromDateTime`、`toDateTime` |
| 获取详细通话分析 | `GONG_RETRIEVE_FILTERED_CALL_DETAILS` | 无（建议提供日期范围或通话 ID） |
| 获取特定通话 | `GONG_RETRIEVE_DATA_FOR_A_SPECIFIC_CALL_V2_CALLS_ID` | `id` |
| 列出工作区 | `GONG_LIST_ALL_COMPANY_WORKSPACES_V2_WORKSPACES` | 无 |

---

*由 [Composio](https://composio.dev) 提供支持*
