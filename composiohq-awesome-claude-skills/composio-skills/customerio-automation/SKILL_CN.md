---
name: Customer.io Automation
description: "通过 Composio 自动化 Customer.io 中的客户互动工作流，包括广播触发、消息分析、细分管理和新闻通讯跟踪"
requires:
  mcp:
    - rube
---

# Customer.io Automation

自动化客户互动操作 —— 触发定向广播、检索送达指标、管理受众细分、列出新闻通讯和交易模板，并查看触发器执行历史 —— 全部通过 Composio MCP 集成来协调完成。

**工具包文档：** [composio.dev/toolkits/customerio](https://composio.dev/toolkits/customerio)

---

## 设置

1. 通过 `https://rube.app/mcp` 处的 Composio MCP 服务器连接你的 Customer.io 账户
2. 如果不存在有效连接，代理会提示你一个身份验证链接
3. 连接成功后，所有 `CUSTOMERIO_*` 工具即可使用

---

## 核心工作流

### 1. 触发广播
手动向特定受众触发一个预先配置好的广播，并附带个性化数据。

**工具：** `CUSTOMERIO_TRIGGER_BROADCAST`

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| `broadcast_id` | integer | 是 | Customer.io 触发详情中的广播 ID |
| `ids` | array | 否 | 目标客户 ID 列表 |
| `emails` | array | 否 | 目标邮箱地址列表 |
| `recipients` | object | 否 | 带有 `and`/`or`/`not`/`segment` 运算符的复杂过滤器 |
| `per_user_data` | array | 否 | 带 `id`/`email` + `data` 的逐用户个性化数据 |
| `data` | object | 否 | 用于 Liquid 模板个性化的全局键值数据 |
| `data_file_url` | string | 否 | 包含逐行用户数据的 JSON 文件的 URL |
| `email_add_duplicates` | boolean | 否 | 允许重复收件人（默认：false） |
| `email_ignore_missing` | boolean | 否 | 跳过没有邮箱的人（默认：false） |
| `id_ignore_missing` | boolean | 否 | 跳过没有客户 ID 的人（默认：false） |

**重要：** 精确提供以下受众选项中的一种：`recipients`、`ids`、`emails`、`per_user_data` 或 `data_file_url`。速率限制：每个广播每10秒1个请求。

---

### 2. 检索消息送达指标
按活动、类型和时间窗口筛选，获取分页的消息送达指标。

**工具：** `CUSTOMERIO_GET_MESSAGES`

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| `type` | string | 否 | 消息类型：`email`、`webhook`、`twilio`、`slack`、`push`、`in_app` |
| `metric` | string | 否 | 指标：`attempted`、`sent`、`delivered`、`opened`、`clicked`、`converted` |
| `campaign_id` | integer | 否 | 按活动 ID 筛选 |
| `newsletter_id` | integer | 否 | 按新闻通讯 ID 筛选 |
| `action_id` | integer | 否 | 按动作 ID 筛选 |
| `start_ts` | integer | 否 | 时间窗口起点（Unix 时间戳） |
| `end_ts` | integer | 否 | 时间窗口终点（Unix 时间戳） |
| `limit` | integer | 否 | 每页结果数，1-1000（默认：50） |
| `start` | string | 否 | 来自上一次响应 `next` 值的分页令牌 |
| `drafts` | boolean | 否 | 返回草稿消息而不是活动中/已发送的消息 |

---

### 3. 列出受众细分
检索工作区中定义的所有细分，用于受众分析和广播定向。

**工具：** `CUSTOMERIO_GET_SEGMENTS`

```
无需参数 —— 返回所有细分及其 ID 和元数据。
```

在通过 `recipients.segment.id` 过滤器定向广播时，使用细分 ID。

---

### 4. 列出新闻通讯
分页浏览所有新闻通讯的元数据，用于跟踪和分析。

**工具：** `CUSTOMERIO_LIST_NEWSLETTERS`

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| `limit` | integer | 否 | 每页最大数量，1-100 |
| `sort` | string | 否 | `asc`（按时间顺序）或 `desc`（倒序） |
| `start` | string | 否 | 来自上一次响应 `next` 值的分页游标 |

---

### 5. 发现交易消息模板
列出所有交易消息模板，以便找到用于通过 API 发送的 ID。

**工具：** `CUSTOMERIO_LIST_TRANSACTIONAL_MESSAGES`

```
无需参数 —— 返回模板 ID 和触发器名称。
```

---

### 6. 查看广播触发器历史
查看某个广播的所有触发器执行记录，并检查单个触发器的详情。

**工具：** `CUSTOMERIO_GET_TRIGGERS` 和 `CUSTOMERIO_GET_TRIGGER`

**列出某广播的所有触发器：**

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| `broadcast_id` | integer | 是 | 广播/活动 ID |

**获取特定触发器：**

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| `broadcast_id` | integer | 是 | 活动/广播 ID |
| `trigger_id` | string | 是 | 触发器标识符（例如 `456` 或 `5-37`） |

---

## 已知陷阱

| 陷阱 | 详情 |
|---------|---------|
| **互斥的受众参数** | `CUSTOMERIO_TRIGGER_BROADCAST` 要求精确提供 `recipients`、`ids`、`emails`、`per_user_data` 或 `data_file_url` 中的一个 —— 提供多个会导致错误 |
| **广播的速率限制** | 每个广播 ID 限制为每10秒1个触发请求 |
| **Unix 时间戳格式** | `CUSTOMERIO_GET_MESSAGES` 中的 `start_ts` 和 `end_ts` 必须是 Unix 时间戳，而不是 ISO 字符串 |
| **分页令牌** | 消息和新闻通讯使用基于游标的分页，通过 `start` 参数 —— 请使用上一次响应中的 `next` 值 |
| **细分 ID 解析** | 要在广播中定向某个细分，首先通过 `CUSTOMERIO_GET_SEGMENTS` 获取细分 ID，然后在 `recipients.segment.id` 中按 ID 引用 |

---

## 快速参考

| 工具 Slug | 用途 |
|-----------|------|
| `CUSTOMERIO_TRIGGER_BROADCAST` | 向指定受众触发广播 |
| `CUSTOMERIO_GET_MESSAGES` | 带筛选条件检索消息送达指标 |
| `CUSTOMERIO_GET_SEGMENTS` | 列出所有受众细分 |
| `CUSTOMERIO_GET_SEGMENT_DETAILS` | 获取特定细分的详情 |
| `CUSTOMERIO_LIST_NEWSLETTERS` | 分页浏览新闻通讯 |
| `CUSTOMERIO_LIST_TRANSACTIONAL_MESSAGES` | 列出交易消息模板 |
| `CUSTOMERIO_GET_TRIGGERS` | 列出某广播的所有触发器执行记录 |
| `CUSTOMERIO_GET_TRIGGER` | 检查特定触发器执行记录 |

---

*由 [Composio](https://composio.dev) 提供支持*
