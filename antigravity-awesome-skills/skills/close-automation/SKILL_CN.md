---
name: close-automation
description: "通过 Rube MCP (Composio) 自动化 Close CRM 任务：创建潜在客户、管理通话/短信、处理任务和跟踪笔记。始终先搜索工具以获取当前模式。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 进行 Close CRM 自动化

通过 Rube MCP 的 Composio Close 工具包自动化 Close CRM 操作。

## 前提条件

- Rube MCP 必须连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用工具包 `close` 的活动 Close 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 以获取当前工具模式

## 设置

**获取 Rube MCP**：将 `https://rube.app/mcp` 添加为客户端配置中的 MCP 服务器。不需要 API 密钥 — 只需添加端点，它就会起作用。


1. 通过确认 `RUBE_SEARCH_TOOLS` 响应验证 Rube MCP 可用
2. 使用工具包 `close` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接不是活动状态，请按照返回的身份验证链接完成 Close API 身份验证
4. 在运行任何工作流前确认连接状态显示为活动

## 核心工作流

### 1. 创建和管理潜在客户

**何时使用**：用户想要创建新潜在客户或管理现有潜在客户记录

**工具序列**：
1. `CLOSE_CREATE_LEAD` - 在 Close 中创建新潜在客户 [必需]

**关键参数**：
- `name`：潜在客户/公司名称
- `contacts`：与潜在客户关联的联系对象数组
- `custom`：自定义字段值作为键值对
- `status_id`：潜在客户状态 ID

**陷阱**：
- Close 中的潜在客户代表公司/组织，而不是个人
- 联系人嵌套在潜在客户中；先创建潜在客户，然后包含联系人
- 自定义字段键使用自定义字段 ID（例如 'custom.cf_XXX'），而不是显示名称
- 重复潜在客户检测不是自动的；创建前先检查

### 2. 记录通话

**何时使用**：用户想要针对潜在客户记录电话通话活动

**工具序列**：
1. `CLOSE_CREATE_CALL` - 记录通话活动 [必需]

**关键参数**：
- `lead_id`：关联潜在客户的 ID
- `contact_id`：被呼叫联系人的 ID
- `direction`：'outbound' 或 'inbound'
- `status`：通话状态（'completed', 'no-answer', 'busy' 等）
- `duration`：通话持续时间（秒）
- `note`：通话笔记

**陷阱**：
- lead_id 是必需的；通话必须与潜在客户关联
- 持续时间以秒为单位，而不是分钟
- 通话方向影响报告和分析
- contact_id 是可选的，但建议用于跟踪

### 3. 发送短信

**何时使用**：用户想要通过 Close 发送或记录短信

**工具序列**：
1. `CLOSE_CREATE_SMS` - 发送或记录短信 [必需]

**关键参数**：
- `lead_id`：关联潜在客户的 ID
- `contact_id`：联系人的 ID
- `direction`：'outbound' 或 'inbound'
- `text`：短信内容
- `status`：消息状态

**陷阱**：
- 短信功能需要配置 Close 电话/短信集成
- 所有短信活动都需要 lead_id
- 出站短信可能需要验证的发送号码
- 消息长度限制可能适用于运营商

### 4. 管理任务

**何时使用**：用户想要创建或管理后续任务

**工具序列**：
1. `CLOSE_CREATE_TASK` - 创建新任务 [必需]

**关键参数**：
- `lead_id`：关联的潜在客户 ID
- `text`：任务描述
- `date`：任务的截止日期
- `assigned_to`：受理人的用户 ID
- `is_complete`：任务是否已完成

**陷阱**：
- 任务与潜在客户关联，而不是联系人
- 日期格式应遵循 ISO 8601
- assigned_to 需要 Close 用户 ID，而不是电子邮件或名称
- 没有日期的任务显示在"无截止日期"部分

### 5. 管理笔记

**何时使用**：用户想要添加或检索潜在客户上的笔记

**工具序列**：
1. `CLOSE_GET_NOTE` - 检索特定笔记 [必需]

**关键参数**：
- `note_id`：要检索的笔记的 ID

**陷阱**：
- 笔记与潜在客户关联
- 检索需要笔记 ID；先搜索潜在客户以查找笔记引用
- 笔记支持纯文本和基本格式

### 6. 删除活动

**何时使用**：用户想要移除通话记录或其他活动

**工具序列**：
1. `CLOSE_DELETE_CALL` - 删除通话活动 [必需]

**关键参数**：
- `call_id`：要删除的通话的 ID

**陷阱**：
- 删除是永久的，无法撤消
- 只有通话创建者或管理员可以删除通话
- 删除通话会从所有报告和时间线中删除它

## 常见模式

### 潜在客户和联系人关系

```
Close 数据模型：
- Lead = 公司/组织
  - Contact = 人员（嵌套在 Lead 中）
  - Activity = 通话、短信、电子邮件、笔记（链接到 Lead）
  - Task = 后续项目（链接到 Lead）
  - Opportunity = 交易（链接到 Lead）
```

### ID 解析

**潜在客户 ID**：
```
1. 使用 Close 搜索 API 搜索潜在客户
2. 从结果中提取 lead_id（格式：'lead_XXXXXXXXXXXXX'）
3. 在所有活动创建调用中使用 lead_id
```

**联系人 ID**：
```
1. 检索潜在客户详情以获取嵌套联系人
2. 提取 contact_id（格式：'cont_XXXXXXXXXXXXX'）
3. 在通话/短信活动中使用以进行准确跟踪
```

### 活动记录模式

```
1. 确定 lead_id 并可选择 contact_id
2. 使用 lead_id 创建活动（通话、短信、笔记）
3. 包括相关元数据（持续时间、方向、状态）
4. 如果需要，创建后续任务
```

## 已知陷阱

**ID 格式**：
- 潜在客户 ID：'lead_XXXXXXXXXXXXX'
- 联系人 ID：'cont_XXXXXXXXXXXXX'
- 活动 ID 因类型而异：'acti_XXXXXXXXXXXXX', 'call_XXXXXXXXXXXXX'
- 自定义字段 ID：'custom.cf_XXXXXXXXXXXXX'
- 始终使用完整 ID 字符串

**速率限制**：
- Close API 的速率限制基于您的计划
- 在批量操作之间实现延迟
- 监控响应头以获取速率限制状态
- 429 响应需要退避

**自定义字段**：
- 自定义字段由其 API ID 引用，而不是显示名称
- 不同的潜在客户状态可能有不同的必需自定义字段
- 自定义字段类型（文本、数字、日期、下拉列表）强制执行值格式

**数据完整性**：
- 潜在客户是主要实体；联系人和活动链接到潜在客户
- 删除潜在客户可能会级联到其联系人和活动
- 批量操作应在执行前验证 ID

## 快速参考

| 任务 | 工具代码 | 关键参数 |
|------|-----------|------------|
| 创建潜在客户 | CLOSE_CREATE_LEAD | name, contacts, custom |
| 记录通话 | CLOSE_CREATE_CALL | lead_id, direction, status, duration |
| 发送短信 | CLOSE_CREATE_SMS | lead_id, text, direction |
| 创建任务 | CLOSE_CREATE_TASK | lead_id, text, date, assigned_to |
| 获取笔记 | CLOSE_GET_NOTE | note_id |
| 删除通话 | CLOSE_DELETE_CALL | call_id |

## 何时使用
此技能适用于执行概览中描述的工作流或操作。

## 限制
- 仅在任务与上述范围匹配时使用此技能。
- 不要将输出视为特定于环境的验证、测试或专家审查的替代品。
- 如果需要的输入、权限、安全边界或成功标准缺失，请停止并寻求澄清。
