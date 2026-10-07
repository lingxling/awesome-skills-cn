---
name: amplitude-automation
description: "通过 Rube MCP (Composio) 自动化处理 Amplitude 任务:事件、用户活动、群组(cohort)、用户识别。请始终先搜索工具以获取最新的模式(schema)。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 自动化 Amplitude

通过 Rube MCP 使用 Composio 的 Amplitude 工具包,自动化处理 Amplitude 产品分析相关任务。

## Prerequisites

- 必须已连接 Rube MCP(`RUBE_SEARCH_TOOLS` 可用)
- 通过 `RUBE_MANAGE_CONNECTIONS` 并指定工具包 `amplitude` 建立的活跃 Amplitude 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 以获取最新的工具模式(schema)

## Setup

**获取 Rube MCP**:在你的客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——只需添加该端点即可使用。


1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 是否可用
2. 调用 `RUBE_MANAGE_CONNECTIONS` 并指定工具包 `amplitude`
3. 如果连接未处于 ACTIVE 状态,按返回的认证链接完成 Amplitude 身份验证
4. 在运行任何工作流之前,确认连接状态显示为 ACTIVE

## Core Workflows

### 1. 发送事件

**使用场景**:用户想要追踪事件或将事件数据发送到 Amplitude

**工具调用顺序**:
1. `AMPLITUDE_SEND_EVENTS` —— 向 Amplitude 发送一个或多个事件【必需】

**关键参数**:
- `events`:事件对象数组,每个对象包含:
  - `event_type`:事件名称(例如 'page_view'、'purchase')
  - `user_id`:唯一用户标识符(如果没有 `device_id` 则必填)
  - `device_id`:设备标识符(如果没有 `user_id` 则必填)
  - `event_properties`:包含自定义事件属性的对象
  - `user_properties`:要设置的用户属性对象
  - `time`:事件时间戳,自纪元起的毫秒数

**注意事项**:
- 每个事件至少需要 `user_id` 或 `device_id` 之一
- 每个事件都必须有 `event_type`;不能为空
- `time` 必须以毫秒为单位(13 位纪元时间),而不是秒
- 存在批次限制;请查看模式以确定每个请求的最大事件数
- 事件是异步处理的;API 响应成功并不意味着数据立即可查询

### 2. 获取用户活动

**使用场景**:用户想要查看特定用户的事件历史

**工具调用顺序**:
1. `AMPLITUDE_FIND_USER` —— 按 ID 或属性查找用户【前置条件】
2. `AMPLITUDE_GET_USER_ACTIVITY` —— 检索该用户的事件流【必需】

**关键参数**:
- `user`:Amplitude 内部用户 ID(来自 FIND_USER)
- `offset`:事件列表的分页偏移量
- `limit`:返回的最大事件数

**注意事项**:
- `user` 参数需要 Amplitude 的内部用户 ID,**而不是**你应用程序的 user_id
- 必须先调用 FIND_USER,将你的 user_id 解析为 Amplitude 的内部 ID
- 默认按时间倒序返回活动
- 大量的活动历史需要通过 `offset` 进行分页

### 3. 查找并识别用户

**使用场景**:用户想要查找用户或设置用户属性

**工具调用顺序**:
1. `AMPLITUDE_FIND_USER` —— 通过各种标识符搜索用户【必需】
2. `AMPLITUDE_IDENTIFY` —— 设置或更新用户属性【可选】

**关键参数**:
- 对于 FIND_USER:
  - `user`:搜索词(user_id、邮箱或 Amplitude ID)
- 对于 IDENTIFY:
  - `user_id`:你应用程序的用户标识符
  - `device_id`:设备标识符(可替代 user_id)
  - `user_properties`:包含 `$set`、`$unset`、`$add`、`$append` 操作的对象

**注意事项**:
- FIND_USER 会在 user_id、device_id 和 Amplitude ID 范围内搜索
- IDENTIFY 使用特殊的属性操作(`$set`、`$unset`、`$add`、`$append`)
- `$set` 会覆盖已有值;`$setOnce` 只在尚未设置时才设置
- IDENTIFY 至少需要 `user_id` 或 `device_id` 之一
- 用户属性变更是最终一致的;不是立即生效的

### 4. 管理群组(Cohort)

**使用场景**:用户想要列出群组、查看群组详情,或更新群组成员

**工具调用顺序**:
1. `AMPLITUDE_LIST_COHORTS` —— 列出所有已保存的群组【必需】
2. `AMPLITUDE_GET_COHORT` —— 获取详细的群组信息【可选】
3. `AMPLITUDE_UPDATE_COHORT_MEMBERSHIP` —— 向群组中添加/移除用户【可选】
4. `AMPLITUDE_CHECK_COHORT_STATUS` —— 检查异步群组操作的状态【可选】

**关键参数**:
- 对于 LIST_COHORTS:无必填参数
- 对于 GET_COHORT:`cohort_id`(来自列表结果)
- 对于 UPDATE_COHORT_MEMBERSHIP:
  - `cohort_id`:目标群组 ID
  - `memberships`:包含 `add` 和/或 `remove` 用户 ID 数组的对象
- 对于 CHECK_COHORT_STATUS:来自更新响应的 `request_id`

**注意事项**:
- 所有群组相关操作都需要群组 ID
- UPDATE_COHORT_MEMBERSHIP 是异步的;使用 CHECK_COHORT_STATUS 来验证
- 状态检查需要更新响应中的 `request_id`
- 每个请求的成员变更数量可能有限制;大批量更新需分块处理
- 只有行为型群组支持通过 API 更新成员

### 5. 浏览事件分类

**使用场景**:用户想要发现 Amplitude 中可用的事件类型和分类

**工具调用顺序**:
1. `AMPLITUDE_GET_EVENT_CATEGORIES` —— 列出所有事件分类【必需】

**关键参数**:
- 无必填参数;返回所有已配置的事件分类

**注意事项**:
- 分类在 Amplitude UI 中配置;API 提供只读访问
- 分类内的事件名称区分大小写
- 在发送事件之前,使用这些分类来验证 event_type 的取值

## Common Patterns

### ID 解析

**应用程序 user_id -> Amplitude 内部 ID**:
```
1. Call AMPLITUDE_FIND_USER with user=your_user_id
2. Extract Amplitude's internal user ID from response
3. Use internal ID for GET_USER_ACTIVITY
```

**群组名称 -> 群组 ID**:
```
1. Call AMPLITUDE_LIST_COHORTS
2. Find cohort by name in results
3. Extract id for cohort operations
```

### 用户属性操作

Amplitude 的 IDENTIFY 支持以下属性操作:
- `$set`:设置属性值(覆盖已有值)
- `$setOnce`:仅在属性尚未设置时才设置
- `$add`:对数值属性做递增
- `$append`:追加到列表属性
- `$unset`:彻底移除属性

示例结构:
```json
{
  "user_properties": {
    "$set": {"plan": "premium", "company": "Acme"},
    "$add": {"login_count": 1}
  }
}
```

### 异步操作模式

对于群组成员更新:
```
1. Call AMPLITUDE_UPDATE_COHORT_MEMBERSHIP -> get request_id
2. Call AMPLITUDE_CHECK_COHORT_STATUS with request_id
3. Repeat step 2 until status is 'complete' or 'error'
```

## Known Pitfalls

**用户 ID**:
- Amplitude 有自己独立于你应用程序的内部用户 ID
- FIND_USER 会将你的 ID 解析为 Amplitude 的内部 ID
- GET_USER_ACTIVITY 需要 Amplitude 的内部 ID,而不是你的 user_id

**事件时间戳**:
- 必须是自纪元起的毫秒数(13 位)
- 秒级(10 位)会被解读为非常久远的日期
- 省略时间戳将使用服务器接收时间

**速率限制**:
- 事件摄入对每个项目有吞吐量限制
- 尽可能批量发送事件以减少 API 调用
- 群组成员更新有异步处理限制

**响应解析**:
- 响应数据可能嵌套在 `data` 键下
- 用户活动按时间倒序返回事件
- 群组列表可能包含已归档的群组;检查 status 字段
- 对可选字段要进行防御性解析,设置回退值

## Quick Reference

| 任务 | 工具标识(Tool Slug) | 关键参数 |
|------|-----------|------------|
| 发送事件 | AMPLITUDE_SEND_EVENTS | events (array) |
| 查找用户 | AMPLITUDE_FIND_USER | user |
| 获取用户活动 | AMPLITUDE_GET_USER_ACTIVITY | user, offset, limit |
| 识别用户 | AMPLITUDE_IDENTIFY | user_id, user_properties |
| 列出群组 | AMPLITUDE_LIST_COHORTS | (none) |
| 获取群组 | AMPLITUDE_GET_COHORT | cohort_id |
| 更新群组成员 | AMPLITUDE_UPDATE_COHORT_MEMBERSHIP | cohort_id, memberships |
| 检查群组状态 | AMPLITUDE_CHECK_COHORT_STATUS | request_id |
| 列出事件分类 | AMPLITUDE_GET_EVENT_CATEGORIES | (none) |

## When to Use
该技能适用于执行概述中所描述的工作流或操作。

## Limitations
- 仅在任务明确符合上述范围时使用该技能。
- 不要将输出当作特定环境验证、测试或专家审查的替代品。
- 如果所需的输入、权限、安全边界或成功标准缺失,请停下来寻求澄清。
