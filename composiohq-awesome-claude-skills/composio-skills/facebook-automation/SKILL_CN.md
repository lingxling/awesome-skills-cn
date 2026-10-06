---
name: Facebook Automation
description: "通过 Composio 自动化 Facebook 主页管理，包括帖子创建、排期、视频上传、Messenger 对话和受众互动"
requires:
  mcp:
    - rube
---

# Facebook Automation

自动化 Facebook 主页操作 —— 创建和排期帖子、上传视频、管理 Messenger 对话、获取主页数据分析，以及处理已排期的内容 —— 全部通过 Composio MCP 集成进行编排。

**工具包文档：** [composio.dev/toolkits/facebook](https://composio.dev/toolkits/facebook)

---

## 设置

1. 通过 Composio MCP 服务器连接你的 Facebook 账户，地址为 `https://rube.app/mcp`
2. 如果没有活动连接，智能体会向你提供身份验证链接
3. 连接完成后，所有 `FACEBOOK_*` 工具即可使用
4. **注意：** 该工具包仅支持 Facebook 主页，不支持个人 Facebook 账户

---

## 核心工作流

### 1. 发现所管理的主页
列出你所管理的所有 Facebook 主页，获取后续操作所需的主页 ID 和访问令牌。

**工具：** `FACEBOOK_LIST_MANAGED_PAGES`

| 参数 | 类型 | 是否必需 | 描述 |
|-----------|------|----------|-------------|
| `fields` | string | 否 | 逗号分隔的字段（默认：`id,name,access_token,category,tasks,about,link,picture`） |
| `limit` | integer | 否 | 每次请求的最大主页数（默认：25） |
| `user_id` | string | 否 | 用户 ID（默认：`me`） |

**务必首先运行此工具**以缓存 `page_id` 值。避免重复进行发现调用 —— 缓存结果。

---

### 2. 创建与排期帖子
在 Facebook 主页上发布或排期带可选链接的文本帖子。

**工具：** `FACEBOOK_CREATE_POST`

| 参数 | 类型 | 是否必需 | 描述 |
|-----------|------|----------|-------------|
| `page_id` | string | 是 | 来自已管理主页的数字主页 ID |
| `message` | string | 是 | 帖子的文本内容 |
| `published` | boolean | 否 | `true` 立即发布，`false` 为草稿/排期（默认：true） |
| `scheduled_publish_time` | integer | 否 | Unix UTC 时间戳；必须至少晚于当前时间 10 分钟 |
| `link` | string | 否 | 帖子中包含的 URL |
| `targeting` | object | 否 | 受众定向规格 |

**排期时：** 将 `published` 设为 `false`，并以 Unix UTC 时间戳形式提供 `scheduled_publish_time`。

---

### 3. 创建与排期视频帖子
在 Facebook 主页上上传并排期视频内容。

**工具：** `FACEBOOK_CREATE_VIDEO_POST`

| 参数 | 类型 | 是否必需 | 描述 |
|-----------|------|----------|-------------|
| `page_id` | string | 是 | 数字主页 ID |
| `file_url` | string | 条件必需 | 视频文件的 URL（提供 `file_url` 或 `video` 二者之一） |
| `video` | object | 条件必需 | 本地文件上传，包含 `name`、`mimetype`、`s3key` |
| `title` | string | 否 | 视频标题 |
| `description` | string | 否 | 视频描述 |
| `published` | boolean | 否 | 是否立即发布（默认：true） |
| `scheduled_publish_time` | integer | 否 | 排期发布的 Unix 时间戳 |

---

### 4. 管理已排期帖子
查看、重新排期、更新或立即发布已排期内容。

**工具：**

- **`FACEBOOK_GET_SCHEDULED_POSTS`** —— 列出主页的已排期/未发布帖子
  - `page_id`（必需）、`fields`、`limit`（最大 100）
- **`FACEBOOK_RESCHEDULE_POST`** —— 更改排期发布时间
- **`FACEBOOK_UPDATE_POST`** —— 编辑现有帖子的文案/文本
- **`FACEBOOK_PUBLISH_SCHEDULED_POST`** —— 立即发布已排期的帖子

---

### 5. 读取主页 Messenger 对话
检索用户与你主页之间的收件箱对话和消息线程。

**工具：** `FACEBOOK_GET_PAGE_CONVERSATIONS`

| 参数 | 类型 | 是否必需 | 描述 |
|-----------|------|----------|-------------|
| `page_id` | string | 是 | Facebook 主页 ID |
| `fields` | string | 否 | 要返回的字段（默认：`participants,updated_time,id`） |
| `limit` | integer | 否 | 要返回的对话数，最大 25 |

然后检索完整的消息线程：

**工具：** `FACEBOOK_GET_CONVERSATION_MESSAGES`

| 参数 | 类型 | 是否必需 | 描述 |
|-----------|------|----------|-------------|
| `page_id` | string | 是 | 拥有该对话的主页 ID |
| `conversation_id` | string | 是 | `t_` 格式的对话 ID（例如 `t_3638640842939952`） |
| `fields` | string | 否 | 默认：`id,created_time,from,to,message` |
| `limit` | integer | 否 | 要返回的消息数，最大 25 |

---

### 6. 发送消息并标记为已读
通过 Messenger 回复用户，并将消息标记为已读。

**工具：**

- **`FACEBOOK_SEND_MESSAGE`** —— 从主页通过 Messenger 向用户发送文本消息
- **`FACEBOOK_MARK_MESSAGE_SEEN`** —— 将用户的消息标记为主页已读

**警告：** 这两个工具都会产生用户可见的副作用。仅在获得明确确认后才可调用。

---

## 已知问题

| 问题 | 详情 |
|---------|---------|
| **排期时间过于接近当前时间** | `FACEBOOK_CREATE_POST` 的 `scheduled_publish_time` 距当前时间不足约 10 分钟时会返回 HTTP 400 —— 批量操作时应留出更大的缓冲时间 |
| **需要 Unix UTC 时间戳** | `scheduled_publish_time` 必须是 Unix UTC —— 时区转换错误会导致排期时间偏差数小时或验证失败 |
| **基于游标的分页** | `FACEBOOK_GET_SCHEDULED_POSTS` 和 `FACEBOOK_GET_PAGE_CONVERSATIONS` 返回的是子集 —— 需跟随分页游标以获取完整数据 |
| **大型对话负载** | 在对话中请求嵌入的消息会产生巨大的负载 —— 应改用 `FACEBOOK_GET_CONVERSATION_MESSAGES` 获取完整线程 |
| **视频处理延迟** | 已上传的视频可能仍处于处理状态 —— 只有在上传内容可用后，才能通过 `FACEBOOK_CREATE_VIDEO_POST` 进行排期 |
| **缓存主页 ID** | 重复调用 `FACEBOOK_LIST_MANAGED_PAGES` 会增加延迟 —— 应按工作区/运行缓存 `page_id` |
| **仅支持主页** | 该工具包不支持个人 Facebook 账户 —— 仅支持 Facebook 主页 |
| **写操作需要确认** | `FACEBOOK_SEND_MESSAGE` 和 `FACEBOOK_MARK_MESSAGE_SEEN` 会产生用户可见的副作用 —— 仅在获得用户明确确认后才可调用 |

---

## 快速参考

| 工具标识 | 用途 |
|-----------|---------|
| `FACEBOOK_LIST_MANAGED_PAGES` | 列出你所管理的主页及其访问令牌 |
| `FACEBOOK_GET_PAGE_DETAILS` | 获取特定主页的详细信息 |
| `FACEBOOK_CREATE_POST` | 创建或排期文本/链接帖子 |
| `FACEBOOK_CREATE_VIDEO_POST` | 创建或排期视频帖子 |
| `FACEBOOK_GET_SCHEDULED_POSTS` | 列出已排期/未发布的帖子 |
| `FACEBOOK_RESCHEDULE_POST` | 更改排期发布时间 |
| `FACEBOOK_UPDATE_POST` | 编辑现有帖子 |
| `FACEBOOK_PUBLISH_SCHEDULED_POST` | 立即发布已排期的帖子 |
| `FACEBOOK_UPLOAD_VIDEO` | 向主页上传视频文件 |
| `FACEBOOK_GET_PAGE_CONVERSATIONS` | 列出 Messenger 收件箱对话 |
| `FACEBOOK_GET_CONVERSATION_MESSAGES` | 检索某对话中的消息 |
| `FACEBOOK_SEND_MESSAGE` | 从主页发送 Messenger 消息 |
| `FACEBOOK_MARK_MESSAGE_SEEN` | 将消息标记为已读 |
| `FACEBOOK_GET_PAGE_POSTS` | 检索主页动态中的帖子 |
| `FACEBOOK_GET_USER_PAGES` | 列出带任务和令牌的主页 |

---

*Powered by [Composio](https://composio.dev)*
