---
name: Webex Automation
description: "通过自然语言命令自动化 Cisco Webex 的消息、房间、团队、Webhook 和人员管理"
requires:
  mcp:
    - rube
---

# Webex Automation

自动化 Cisco Webex 协作工作流——发送消息、管理房间和团队、配置 Webhook、查找人员——全部通过自然语言完成。

**工具包文档：** [composio.dev/toolkits/webex](https://composio.dev/toolkits/webex)

---

## 设置

1. 将 Rube MCP 服务器添加到你的环境中：`https://rube.app/mcp`
2. 按提示连接你的 Webex 账户（通过 Composio 的 OAuth 流程）
3. 开始使用自然语言命令进行 Webex 自动化

---

## 核心工作流

### 1. 向房间或个人发送消息

向任意 Webex 房间或直接向某个人发布纯文本、Markdown、文件附件或 Adaptive Card。

**工具：** `WEBEX_MESSAGING_CREATE_MESSAGE`

关键参数：
- `roomId` -- 目标房间 ID（使用 `WEBEX_MESSAGING_LIST_ROOMS` 查找）
- `toPersonEmail` -- 改为发送私人 1:1 消息（与 `roomId` 互斥）
- `text` -- 纯文本内容（最大 7439 字节）
- `markdown` -- Markdown 格式的内容（优先于 `text`）
- `files` -- 文件附件的公开 URL 列表（每条消息仅一个文件）
- `attachments` -- Adaptive Card JSON（每条消息一张卡片）
- `parentId` -- 以线程回复的形式回复特定消息

示例提示词：
> “向房间 Y2lz... 发送一条 Markdown 消息，内容为 **部署已完成**，并附上发布说明链接”

---

### 2. 列出和发现房间

浏览你所属的所有房间，可按类型、团队筛选或按活动排序。

**工具：** `WEBEX_MESSAGING_LIST_ROOMS`

关键参数：
- `type` -- 按 `direct`（1:1）或 `group` 筛选
- `teamId` -- 限定为特定团队的房间
- `sortBy` -- 按 `id`、`lastactivity` 或 `created` 排序
- `max` -- 限制结果数量（1-1000，默认 100）

后续可用 `WEBEX_MESSAGING_GET_ROOM_DETAILS` 获取特定房间的完整元数据，包括标题、类型、锁定状态、创建者和时间戳。

示例提示词：
> “列出我最近活跃的 10 个群组房间”

---

### 3. 管理用于事件驱动自动化的 Webhook

创建 Webhook，以便在 Webex 资源发生变化时实时接收 HTTP POST 通知。

**工具：** `WEBEX_WEBHOOKS_CREATE_WEBHOOK`

关键参数：
- `name` -- 便于识别的 Webhook 名称（必填）
- `targetUrl` -- 接收 POST 通知的 URL（必填）
- `resource` -- 要监控的内容：`messages`、`rooms`、`memberships`、`meetings`、`recordings`、`meetingParticipants`、`telephony_calls` 等（必填）
- `event` -- 触发类型：`created`、`updated`、`deleted`、`started`、`ended`、`joined`、`left`（必填）
- `filter` -- 限定通知范围（例如 `roomId=<id>` 或 `hostEmail=<email>`）
- `secret` -- 用于负载签名验证的可选 HMAC 密钥
- `ownedBy` -- 个人 Webhook 用 `creator`，组织范围 Webhook 用 `org`

辅助工具：
- `WEBEX_LIST_WEBHOOKS` -- 列出所有已注册的 Webhook，支持可选的 `max` 和 `ownedBy` 过滤
- `WEBEX_WEBHOOKS_GET_WEBHOOK` -- 按 `webhookId` 查看特定 Webhook

示例提示词：
> “创建一个名为 'New Messages' 的 Webhook，在房间 Y2lz... 中有新消息创建时 POST 到 https://my-app.com/hook”

---

### 4. 管理团队成员资格

将人员添加到 Webex 团队，并可选择授予协调员（moderator）权限。

**工具：** `WEBEX_MESSAGING_CREATE_TEAM_MEMBERSHIP`

关键参数：
- `teamId` -- 要添加人员的团队（必填）
- `personEmail` -- 要添加人员的邮箱
- `personId` -- Webex 人员 ID（邮箱的替代方案）
- `isModerator` -- 设为 `true` 以授予协调员权限（默认 `false`）

请先使用 `WEBEX_LIST_TEAMS` 发现可用团队。

示例提示词：
> “将 alice@example.com 添加为团队 Y2lz... 的协调员”

---

### 5. 审计房间成员资格

查看房间中有哪些成员、验证特定人员的成员资格，或列出跨团队的成员资格。

**工具：** `WEBEX_MESSAGING_LIST_MEMBERSHIPS`

关键参数：
- `roomId` -- 列出特定房间的所有成员
- `personEmail` -- 检查某人是否为成员（需要 `roomId`）
- `personId` -- 按 Webex 人员 ID 检查（需要 `roomId`）
- `teamId` -- 按团队关联筛选
- `max` -- 限制结果数量

示例提示词：
> “列出房间 Y2lz... 的所有成员，并告诉我谁是协调员”

---

### 6. 搜索和查找人员

按邮箱、显示名称或 ID 在你的 Webex 组织中查找人员。

**工具：** `WEBEX_PEOPLE_LIST_PEOPLE`

用于在发送直接消息或添加团队成员之前，将姓名解析为人员 ID。

示例提示词：
> “查找 bob@company.com 的 Webex 人员 ID”

---

## 常见陷阱

| 陷阱 | 详情 |
|---------|---------|
| Webhook 自动禁用 | 目标 URL 必须响应 HTTP 2xx；5 分钟内失败 100 次会自动禁用该 Webhook |
| 消息大小限制 | `text` 和 `markdown` 的最大值均为 7439 字节 |
| 每条消息仅一个文件 | `files` 数组可以接受一个列表，但每条消息实际上只支持一个附件 |
| 每条消息仅一张卡片 | 每条消息只支持一个 Adaptive Card 附件 |
| 目标互斥 | 发送消息时 `roomId` 与 `toPersonEmail`/`toPersonId` 不能同时使用 |
| 更新房间需要标题 | `WEBEX_UPDATE_ROOM` 始终要求提供 `title` 参数，即使只是更改锁定状态或团队 |
| orgPublicSpaces 冲突 | 列出房间时，`orgPublicSpaces` 不能与 `teamId`、`type` 或 `sortBy` 组合使用 |
| Webhook 读取范围 | 创建 Webhook 需要对所监控资源类型具有 `read` 权限范围 |
| 成员筛选需要 roomId | 在列出成员资格时，`personEmail` 和 `personId` 过滤器需要 `roomId`，除非你是合规官（Compliance Officer） |

---

## 快速参考

| 操作 | 工具 Slug | 关键参数 |
|--------|-----------|------------|
| 发送消息 | `WEBEX_MESSAGING_CREATE_MESSAGE` | `roomId`、`text`/`markdown`、`toPersonEmail` |
| 列出房间 | `WEBEX_MESSAGING_LIST_ROOMS` | `type`、`sortBy`、`max` |
| 获取房间详情 | `WEBEX_MESSAGING_GET_ROOM_DETAILS` | `roomId` |
| 更新房间 | `WEBEX_UPDATE_ROOM` | `roomId`、`title` |
| 删除消息 | `WEBEX_MESSAGING_DELETE_MESSAGE` | `messageId` |
| 获取消息详情 | `WEBEX_MESSAGING_GET_MESSAGE_DETAILS` | `messageId` |
| 创建 Webhook | `WEBEX_WEBHOOKS_CREATE_WEBHOOK` | `name`、`targetUrl`、`resource`、`event` |
| 列出 Webhook | `WEBEX_LIST_WEBHOOKS` | `max`、`ownedBy` |
| 获取 Webhook | `WEBEX_WEBHOOKS_GET_WEBHOOK` | `webhookId` |
| 添加团队成员 | `WEBEX_MESSAGING_CREATE_TEAM_MEMBERSHIP` | `teamId`、`personEmail`、`isModerator` |
| 列出成员资格 | `WEBEX_MESSAGING_LIST_MEMBERSHIPS` | `roomId`、`personEmail`、`max` |
| 列出人员 | `WEBEX_PEOPLE_LIST_PEOPLE` | 邮箱、displayName、ID 过滤器 |
| 列出团队 | `WEBEX_LIST_TEAMS` | `max` |

---

*由 [Composio](https://composio.dev) 提供支持*
