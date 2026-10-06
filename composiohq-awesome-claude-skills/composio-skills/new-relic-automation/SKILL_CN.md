---
name: New Relic Automation
description: "自动化 New Relic 可观测性工作流 —— 通过 Composio MCP 集成管理告警策略、通知渠道、告警条件，并监控应用程序和浏览器应用。"
requires:
  mcp:
    - rube
---

# New Relic Automation

自动化你的 New Relic 可观测性工作流 —— 创建和管理告警策略，配置通知渠道（电子邮件、Slack、webhook、PagerDuty），监控 APM 应用程序，检查告警条件，并将 New Relic 告警集成到跨应用管道中。

**工具包文档：** [composio.dev/toolkits/new_relic](https://composio.dev/toolkits/new_relic)

---

## 设置

1. 将 Composio MCP 服务器添加到你的客户端：`https://rube.app/mcp`
2. 按提示连接你的 New Relic 账户（API 密钥认证）
3. 开始使用下面的工作流

---

## 核心工作流

### 1. 列出告警策略

使用 `NEW_RELIC_GET_ALERT_POLICIES` 发现现有的告警策略，支持可选过滤。

```
Tool: NEW_RELIC_GET_ALERT_POLICIES
Inputs:
  - name: string (optional, partial match supported)
  - incident_preference: "PER_POLICY" | "PER_CONDITION" | "PER_CONDITION_AND_TARGET"
  - page: integer (1-indexed pagination)
```

### 2. 创建告警策略

使用 `NEW_RELIC_CREATE_ALERT_POLICY` 为告警条件创建一个新的策略容器。

```
Tool: NEW_RELIC_CREATE_ALERT_POLICY
Inputs:
  - name: string (required) -- must be unique within the account
  - incident_preference: "PER_POLICY" | "PER_CONDITION" | "PER_CONDITION_AND_TARGET" (default: PER_POLICY)
```

**事件偏好说明：**
- `PER_POLICY` —— 每个策略产生一个问题（大多数场景推荐使用）
- `PER_CONDITION` —— 每个告警条件产生一个问题
- `PER_CONDITION_AND_TARGET` —— 每个条件和信号/目标产生一个问题

### 3. 创建告警通知渠道

使用 `NEW_RELIC_CREATE_ALERT_CHANNEL` 注册用于告警投递的通知端点。

```
Tool: NEW_RELIC_CREATE_ALERT_CHANNEL
Inputs:
  - type: "email" | "slack" | "webhook" | "pagerduty" | "opsgenie" | "victorops" (required)
  - name: string (required) -- human-readable channel name
  - configuration: object (required) -- varies by type:
    Email:     { recipients: "devops@example.com,oncall@example.com" }
    Slack:     { url: "<slack_webhook_url>", channel: "alerts" }
    Webhook:   { url: "https://hooks.example.com/alerts", auth_username, auth_password }
    PagerDuty: { service_key: "<integration_key>" }
    OpsGenie:  { api_key, recipients, tags, teams }
    VictorOps: { key: "<api_key>", route_key: "<routing_key>" }
```

### 4. 获取策略的告警条件

使用 `NEW_RELIC_GET_ALERT_CONDITIONS` 检查附加到特定策略上的条件。

```
Tool: NEW_RELIC_GET_ALERT_CONDITIONS
Inputs:
  - policy_id: integer (required)
```

### 5. 监控应用程序

使用 `NEW_RELIC_GET_APPLICATIONS` 和 `NEW_RELIC_GET_BROWSER_APPLICATIONS` 列出 APM 应用和浏览器监控的应用。

```
Tool: NEW_RELIC_GET_APPLICATIONS
Inputs:
  - name: string (optional, case-insensitive partial match)
  - host: string (optional, case-insensitive partial match)
  - ids: string (optional, comma-separated list of app IDs)
  - page: integer (1-indexed)

Tool: NEW_RELIC_GET_BROWSER_APPLICATIONS
Inputs:
  - filter[name]: string (optional, case-insensitive partial match)
  - page: integer (1-indexed)
```

### 6. 管理渠道和策略

使用 `NEW_RELIC_UPDATE_ALERT_CHANNEL` 修改现有渠道，使用 `NEW_RELIC_DELETE_ALERT_POLICY` 删除策略。

```
Tool: NEW_RELIC_UPDATE_ALERT_CHANNEL
Inputs:
  - alert_channel_id: integer (required)
  - name: string (optional)
  - type: string (optional, only to change type)
  - configuration: object (optional, fields vary by type)

Tool: NEW_RELIC_DELETE_ALERT_POLICY
Inputs:
  - policy_id: string (required) -- ID of the policy to delete
```

---

## 已知问题

| 问题 | 详情 |
|---------|--------|
| 策略名称唯一性 | `NEW_RELIC_CREATE_ALERT_POLICY` 要求名称在账户内唯一。 |
| 渠道配置因类型而异 | `NEW_RELIC_CREATE_ALERT_CHANNEL` 的 `configuration` 对象在不同渠道类型下所需字段不同（例如电子邮件需要 `recipients`，PagerDuty 需要 `service_key`）。 |
| 需要分页 | 所有列表端点返回分页结果。请遍历各页直至结果用尽。 |
| policy_id 类型不一致 | `NEW_RELIC_GET_ALERT_CONDITIONS` 要求 `policy_id` 为整数，而 `NEW_RELIC_DELETE_ALERT_POLICY` 要求其为字符串。 |
| 渠道-策略关联 | 创建渠道后，你必须单独将其与策略关联，才能让告警流向该渠道。 |

---

## 快速参考

| 工具 Slug | 描述 |
|-----------|-------------|
| `NEW_RELIC_GET_ALERT_POLICIES` | 列出告警策略，支持可选过滤 |
| `NEW_RELIC_CREATE_ALERT_POLICY` | 创建新的告警策略 |
| `NEW_RELIC_DELETE_ALERT_POLICY` | 按 ID 删除告警策略 |
| `NEW_RELIC_CREATE_ALERT_CHANNEL` | 创建通知渠道（电子邮件、Slack、webhook 等） |
| `NEW_RELIC_GET_ALERT_CHANNELS` | 列出所有已配置的告警渠道 |
| `NEW_RELIC_UPDATE_ALERT_CHANNEL` | 更新现有告警渠道 |
| `NEW_RELIC_GET_ALERT_CONDITIONS` | 获取策略的告警条件 |
| `NEW_RELIC_GET_APPLICATIONS` | 列出 APM 应用程序 |
| `NEW_RELIC_GET_BROWSER_APPLICATIONS` | 列出浏览器监控的应用程序 |

---

*由 [Composio](https://composio.dev) 提供支持*
