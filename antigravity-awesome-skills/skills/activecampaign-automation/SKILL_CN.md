---
name: activecampaign-automation
description: "通过 Rube MCP（Composio）自动化 ActiveCampaign 任务：管理联系人、标签、名单订阅、自动化注册和任务。请始终先搜索工具以获取最新的模式定义。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 ActiveCampaign 自动化

通过 Composio 的 ActiveCampaign 工具包（经由 Rube MCP）自动化 ActiveCampaign CRM 与市场营销自动化操作。

## 前提条件

- 必须已连接 Rube MCP（`RUBE_SEARCH_TOOLS` 可用）
- 已通过 `RUBE_MANAGE_CONNECTIONS` 使用工具包 `active_campaign` 建立有效的 ActiveCampaign 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 以获取最新的工具模式定义

## 设置

**获取 Rube MCP**：在你的客户端配置中把 `https://rube.app/mcp` 添加为一个 MCP 服务器。无需 API 密钥——只需添加该端点即可使用。


1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 是否可用
2. 使用工具包 `active_campaign` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的授权链接完成 ActiveCampaign 身份验证
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 创建和查找联系人

**何时使用**：用户想要创建新联系人或查找现有联系人

**工具调用顺序**：
1. `ACTIVE_CAMPAIGN_FIND_CONTACT` - 搜索现有联系人 [可选]
2. `ACTIVE_CAMPAIGN_CREATE_CONTACT` - 创建新联系人 [必需]

**查找的关键参数**：
- `email`：按电子邮件地址搜索
- `id`：按 ActiveCampaign 联系人 ID 搜索
- `phone`：按电话号码搜索

**创建的关键参数**：
- `email`：联系人电子邮件地址（必填）
- `first_name`：联系人名
- `last_name`：联系人姓
- `phone`：联系人电话号码
- `organization_name`：联系人所属机构
- `job_title`：联系人职位
- `tags`：要应用的标签，以逗号分隔的列表

**注意事项**：
- `email` 是创建联系人时唯一必填的字段
- 电话搜索在内部使用通用的搜索参数；可能返回部分匹配的结果
- 在 FIND_CONTACT 中同时提供 `email` 和 `phone` 时，结果会在客户端进行过滤
- 创建时提供的标签会立即生效
- 使用已存在的邮箱创建联系人，可能会更新已有的联系人

### 2. 管理联系人标签

**何时使用**：用户想要为联系人添加或移除标签

**工具调用顺序**：
1. `ACTIVE_CAMPAIGN_FIND_CONTACT` - 按邮箱或 ID 查找联系人 [前提条件]
2. `ACTIVE_CAMPAIGN_MANAGE_CONTACT_TAG` - 添加或移除标签 [必需]

**关键参数**：
- `action`：'Add' 或 'Remove'（必填）
- `tags`：标签名称，以逗号分隔的字符串或字符串数组形式提供（必填）
- `contact_id`：联系人 ID（提供此项或 contact_email）
- `contact_email`：联系人电子邮件地址（可替代 contact_id）

**注意事项**：
- `action` 的取值首字母大写：'Add' 或 'Remove'（不是小写）
- 标签可以是逗号分隔的字符串（'tag1, tag2'）或数组（['tag1', 'tag2']）
- 必须提供 `contact_id` 或 `contact_email` 之一；`contact_id` 优先
- 添加一个不存在的标签会自动创建它
- 移除一个不存在的标签是无操作（不会报错）

### 3. 管理名单订阅

**何时使用**：用户想要为联系人订阅或取消订阅名单

**工具调用顺序**：
1. `ACTIVE_CAMPAIGN_FIND_CONTACT` - 查找该联系人 [前提条件]
2. `ACTIVE_CAMPAIGN_MANAGE_LIST_SUBSCRIPTION` - 订阅或取消订阅 [必需]

**关键参数**：
- `action`：'subscribe' 或 'unsubscribe'（必填）
- `list_id`：数字形式的名单 ID 字符串（必填）
- `email`：联系人电子邮件地址（提供此项或 contact_id）
- `contact_id`：数字形式的联系人 ID 字符串（可替代 email）

**注意事项**：
- `action` 的取值为小写：'subscribe' 或 'unsubscribe'
- `list_id` 是数字字符串（例如 '2'），不是名单名称
- 名单 ID 可通过 GET /api/3/lists 端点获取（该端点未作为 Composio 工具提供；请使用 ActiveCampaign 界面）
- 如果同时提供了 `email` 和 `contact_id`，`contact_id` 优先
- 取消订阅会把状态改为 '2'（已取消订阅），但该关系记录仍会保留

### 4. 把联系人添加到自动化流程

**何时使用**：用户想要把一个联系人注册进某个自动化工作流

**工具调用顺序**：
1. `ACTIVE_CAMPAIGN_FIND_CONTACT` - 验证该联系人存在 [前提条件]
2. `ACTIVE_CAMPAIGN_ADD_CONTACT_TO_AUTOMATION` - 把联系人注册进自动化流程 [必需]

**关键参数**：
- `contact_email`：要注册的联系人邮箱（必填）
- `automation_id`：目标自动化流程的 ID（必填）

**注意事项**：
- 该联系人必须已经存在于 ActiveCampaign 中
- 自动化流程只能通过 ActiveCampaign 界面创建，不能通过 API 创建
- `automation_id` 必须引用一个已存在、处于激活状态的自动化流程
- 该工具会执行两步流程：先按邮箱查找联系人，然后再注册
- 自动化流程 ID 可在 ActiveCampaign 界面中找到，或通过 GET /api/3/automations 获取

### 5. 创建联系人任务

**何时使用**：用户想要创建与联系人关联的跟进任务

**工具调用顺序**：
1. `ACTIVE_CAMPAIGN_FIND_CONTACT` - 查找要关联任务的联系人 [前提条件]
2. `ACTIVE_CAMPAIGN_CREATE_CONTACT_TASK` - 创建该任务 [必需]

**关键参数**：
- `relid`：要关联任务的联系人 ID（必填）
- `duedate`：带时区的 ISO 8601 格式到期日期（必填，例如 '2025-01-15T14:30:00-05:00'）
- `dealTasktype`：基于可用类型的任务类型 ID（必填）
- `title`：任务标题
- `note`：任务描述/内容
- `assignee`：该任务指派给的用户 ID
- `edate`：ISO 8601 格式的结束日期（必须晚于 duedate）
- `status`：0 表示未完成，1 表示已完成

**注意事项**：
- `duedate` 必须是带时区偏移的合法 ISO 8601 日期时间；不要使用占位值
- `edate` 必须晚于 `duedate`
- `dealTasktype` 是引用 ActiveCampaign 中已配置任务类型的字符串 ID
- `relid` 是数字形式的联系人 ID，不是电子邮件地址
- `assignee` 是用户 ID；通过 ActiveCampaign 界面把用户名称解析为 ID

## 常见模式

### 联系人查找流程

```
1. Call ACTIVE_CAMPAIGN_FIND_CONTACT with email
2. If found, extract contact ID for subsequent operations
3. If not found, create contact with ACTIVE_CAMPAIGN_CREATE_CONTACT
4. Use contact ID for tags, subscriptions, or automations
```

### 批量联系人打标签

```
1. For each contact, call ACTIVE_CAMPAIGN_MANAGE_CONTACT_TAG
2. Use contact_email to avoid separate lookup calls
3. Batch with reasonable delays to respect rate limits
```

### ID 解析

**联系人邮箱 -> 联系人 ID**：
```
1. Call ACTIVE_CAMPAIGN_FIND_CONTACT with email
2. Extract id from the response
```

## 已知注意事项

**操作值的大小写**：
- 标签操作：'Add'、'Remove'（首字母大写）
- 订阅操作：'subscribe'、'unsubscribe'（小写）
- 混淆大小写会导致错误

**ID 类型**：
- 联系人 ID：数字字符串（例如 '123'）
- 名单 ID：数字字符串
- 自动化流程 ID：数字字符串
- 所有 ID 都应作为字符串传递，而不是整数

**自动化流程**：
- 自动化流程不能通过 API 创建；只能进行注册
- 自动化流程必须处于激活状态才能接受新联系人
- 把已经在该自动化流程中的联系人再次注册可能没有效果

**速率限制**：
- ActiveCampaign API 对每个账户都有速率限制
- 在收到 429 响应时实施退避策略
- 批量操作之间应保持适当的间隔

**响应解析**：
- 响应数据可能嵌套在 `data` 或 `data.data` 之下
- 使用带回退模式的防御性解析
- 联系人搜索可能返回多个结果；为确保准确，按邮箱匹配

## 快速参考

| 任务 | 工具 Slug | 关键参数 |
|------|-----------|------------|
| 查找联系人 | ACTIVE_CAMPAIGN_FIND_CONTACT | email, id, phone |
| 创建联系人 | ACTIVE_CAMPAIGN_CREATE_CONTACT | email, first_name, last_name, tags |
| 添加/移除标签 | ACTIVE_CAMPAIGN_MANAGE_CONTACT_TAG | action, tags, contact_email |
| 订阅/取消订阅 | ACTIVE_CAMPAIGN_MANAGE_LIST_SUBSCRIPTION | action, list_id, email |
| 添加到自动化流程 | ACTIVE_CAMPAIGN_ADD_CONTACT_TO_AUTOMATION | contact_email, automation_id |
| 创建任务 | ACTIVE_CAMPAIGN_CREATE_CONTACT_TASK | relid, duedate, dealTasktype, title |

## 何时使用
本技能适用于执行概述中所述的工作流或操作。

## 局限性
- 仅在任务明确符合上述范围时使用本技能。
- 不要把输出当作针对特定环境验证、测试或专家评审的替代品。
- 如果所需的输入、权限、安全边界或成功标准缺失，请停下来请求澄清。
