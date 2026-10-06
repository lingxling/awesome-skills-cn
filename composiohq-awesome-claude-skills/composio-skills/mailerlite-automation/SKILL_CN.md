---
name: MailerLite Automation
description: "通过 Composio 借助 MailerLite 自动化电子邮件营销工作流，包括订阅者管理、活动分析、分组细分和账户监控"
requires:
  mcp:
    - rube
---

# MailerLite 自动化

自动化电子邮件营销操作——管理订阅者、分析活动表现、组织分组和细分，以及监控账户健康状况——全部通过 Composio MCP 集成进行编排。

**工具包文档：** [composio.dev/toolkits/mailerlite](https://composio.dev/toolkits/mailerlite)

---

## 设置

1. 通过 `https://rube.app/mcp` 的 Composio MCP 服务器连接你的 MailerLite 账户
2. 如果不存在有效连接，智能体会向你提供一个认证链接
3. 连接后，所有 `MAILERLITE_*` 工具都可用于执行

---

## 核心工作流

### 1. 验证账户并获取元数据
检索账户详情，包括套餐限制和时区，以确保报告一致。

**工具：** `MAILERLITE_GET_ACCOUNT_INFO`

```
No parameters required -- returns account metadata, plan details, and timezone configuration.
```

请始终首先运行此工具，以确定套餐限制和时区，从而保证基于时间窗口的查询一致。

---

### 2. 获取账户范围的表现统计
检索订阅者总数、已发送邮件总数和互动指标的汇总数据，以获得健康状况快照。

**工具：** `MAILERLITE_GET_ACCOUNT_STATS`

```
No parameters required -- returns overall subscriber counts, sent emails, and performance metrics.
```

---

### 3. 列出并分页遍历订阅者
检索订阅者，支持可选的状态过滤和基于游标的分页。

**工具：** `MAILERLITE_GET_SUBSCRIBERS`

| 参数 | 类型 | 必填 | 描述 |
|-----------|------|----------|-------------|
| `filter[status]` | string | 否 | 按以下状态过滤：`active`、`unsubscribed`、`unconfirmed`、`bounced`、`junk` |
| `limit` | integer | 否 | 每页订阅者数（默认：25） |
| `cursor` | string | 否 | 来自上一次响应 `meta.cursor` 的分页游标 |
| `include` | string | 否 | 设置为 `groups` 以包含分组成员关系 |

**重要：** 使用 `meta.next_cursor` 循环直到其为 `null`，以构建完整的订阅者列表。

---

### 4. 列出并分析活动
检索活动，支持可选的状态/类型过滤和基于页码的分页。

**工具：** `MAILERLITE_GET_CAMPAIGNS`

| 参数 | 类型 | 必填 | 描述 |
|-----------|------|----------|-------------|
| `filter[status]` | string | 否 | 按以下状态过滤：`sent`、`draft`、`ready` |
| `filter[type]` | string | 否 | 按以下类型过滤：`regular`、`ab`、`resend`、`rss` |
| `limit` | integer | 否 | 每页条目数（默认：25） |
| `page` | integer | 否 | 页码（默认：1） |

**重要：** 使用 `meta.last_page` 进行分页，以避免在历史分析中遗漏活动。

---

### 5. 管理订阅者分组
列出、过滤和排序订阅者分组，用于受众组织。

**工具：** `MAILERLITE_GET_GROUPS`

| 参数 | 类型 | 必填 | 描述 |
|-----------|------|----------|-------------|
| `filter[name]` | string | 否 | 名称部分匹配过滤 |
| `limit` | integer | 否 | 返回的最大分组数 |
| `page` | integer | 否 | 页码（从 1 开始） |
| `sort` | string | 否 | 排序依据：`name`、`total`、`open_rate`、`click_rate`、`created_at`（加前缀 `-` 表示降序） |

---

### 6. 检索受众细分和自定义字段
获取细分和自定义字段定义，用于高级受众分析。

**工具：** `MAILERLITE_GET_SEGMENTS` 和 `MAILERLITE_GET_FIELDS`

**细分：**

| 参数 | 类型 | 必填 | 描述 |
|-----------|------|----------|-------------|
| `limit` | integer | 否 | 返回的最大细分数（最多 250） |
| `page` | integer | 否 | 页码（从 1 开始） |

**字段：** 无需参数——返回所有自定义字段定义。

---

## 已知陷阱

| 陷阱 | 详情 |
|---------|---------|
| **订阅者分页基于游标** | `MAILERLITE_GET_SUBSCRIBERS` 使用 `meta.next_cursor`——你必须循环直到其为 `null`，否则计数将不完整 |
| **活动分页基于页码** | `MAILERLITE_GET_CAMPAIGNS` 使用 `page`/`limit` 配合 `meta.last_page`——过早停止会遗漏活动并扭曲趋势 |
| **抽样偏差** | 仅根据第一页计算互动指标会引入偏差；请始终汇总所有页面 |
| **嵌套的响应结构** | MailerLite 的载荷嵌套在 `results[i].response.data` 之下，包含 `data` 和 `meta` 子键，而不是扁平的 `data` 键——请相应地解析 |
| **API 配额** | 订阅者列表受 MailerLite Connect API 配额限制——请据此规划批量操作 |

---

## 快速参考

| 工具 Slug | 用途 |
|-----------|---------|
| `MAILERLITE_GET_ACCOUNT_INFO` | 验证认证并查看账户元数据 |
| `MAILERLITE_GET_ACCOUNT_STATS` | 获取汇总的表现指标 |
| `MAILERLITE_GET_SUBSCRIBERS` | 列出订阅者，支持过滤和分页 |
| `MAILERLITE_GET_CAMPAIGNS` | 列出活动，支持状态/类型过滤 |
| `MAILERLITE_GET_GROUPS` | 列出并排序订阅者分组 |
| `MAILERLITE_GET_SEGMENTS` | 列出受众细分 |
| `MAILERLITE_GET_FIELDS` | 检索自定义字段定义 |

---

*由 [Composio](https://composio.dev) 提供支持*
