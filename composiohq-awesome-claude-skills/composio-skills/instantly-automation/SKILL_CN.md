---
name: Instantly Automation
description: "通过 Composio MCP 集成，用自然语言自动化 Instantly 冷邮件外联 —— 管理活动、发件账户、潜客名单、批量导入潜客以及活动分析。"
category: email-outreach
requires:
  mcp:
    - rube
---

# Instantly Automation

使用 Instantly 自动化你的冷邮件外联 —— 创建和管理带有多步序列的活动、配置发送计划、批量导入潜客、管理发件账户，并跟踪活动表现 —— 全部通过自然语言指令完成。

**工具包文档：** [composio.dev/toolkits/instantly](https://composio.dev/toolkits/instantly)

---

## 设置

1. 将 Composio MCP 服务器添加到你的客户端配置中：
   ```
   https://rube.app/mcp
   ```
2. 按提示连接你的 Instantly 账户（API 密钥身份验证）。
3. 开始使用自然语言指令管理你的外联活动。

---

## 核心工作流

### 1. 列出发件账户
检索你 Instantly 工作区中配置的所有邮件账户，可按状态和服务商进行筛选。

**工具：** `INSTANTLY_LIST_ACCOUNTS`

**示例提示：**
> "显示我 Instantly 工作区中所有处于活动状态的发件账户"

**关键参数：**
- `status` —— 按状态筛选：`1`（活动）、`2`（已暂停）、`-1`（连接错误）、`-2`（软退信错误）、`-3`（发送错误）
- `provider_code` —— 按服务商筛选：`1`（自定义 IMAP/SMTP）、`2`（Google）、`3`（Microsoft）、`4`（AWS）
- `search` —— 按邮箱子字符串或域名搜索
- `limit` —— 最大条目数（1-100）
- `starting_after` —— 来自上一次响应的分页游标
- `tag_ids` —— 逗号分隔的标签 UUID

---

### 2. 创建活动
启动一个带有调度、邮件序列、A/B 测试变体和发送配置的新外联活动。

**工具：** `INSTANTLY_CREATE_CAMPAIGN`

**示例提示：**
> "创建一个名为 'Q1 Outreach' 的 Instantly 活动，按中部时间周一至周五上午9点到下午5点发送，包含一个3步邮件序列"

**关键参数：**
- `name`（必填）—— 活动名称
- `campaign_schedule`（必填）—— 调度配置：
  - `schedules`（必填）—— 调度对象数组，每个对象包含：
    - `name` —— 调度名称
    - `timing` —— `{from: "09:00", to: "17:00"}`（HH:mm 格式）
    - `days` —— 星期索引字符串 "0"（周日）到 "6"（周六）到布尔值的映射
    - `timezone` —— 支持的值包括 "America/Chicago"、"America/Detroit"、"America/Boise"、"America/Anchorage"
  - `start_date` / `end_date` —— ISO 8601 日期
- `email_list` —— 发件账户邮箱地址数组（必须是预先配置好的账户；使用 `INSTANTLY_LIST_ACCOUNTS` 查找有效地址）
- `sequences` —— 数组（只使用第一个元素），包含：
  - `steps` —— 步骤对象数组，每个对象包含：
    - `type` —— 必须为 "email"
    - `delay` —— 距下一封邮件的天数（整数，最小为 0）
    - `variants` —— 用于 A/B 测试的 `{subject, body}` 对象数组
- `daily_limit` —— 每日发送上限
- `email_gap` —— 邮件之间的间隔分钟数
- `stop_on_reply` —— 当潜客回复时停止活动（布尔值）
- `stop_on_auto_reply` —— 在自动回复时停止（布尔值）
- `open_tracking` / `link_tracking` —— 启用跟踪（布尔值）

**时区说明：**
- 验证可用："America/Chicago"（中部）、"America/Detroit"（东部）、"America/Boise"（山地）
- 自动映射："America/New_York" 映射到 "America/Detroit"，"America/Denver" 映射到 "America/Boise"
- 不支持："America/Los_Angeles"、"US/Pacific" —— 请使用 "America/Anchorage" 或 "America/Dawson" 作为替代

---

### 3. 更新活动设置
修改现有活动的调度、发送限制、序列或跟踪设置。

**工具：** `INSTANTLY_UPDATE_CAMPAIGN`

**示例提示：**
> "更新我的 Instantly 活动，将每日限制提高到100并启用打开跟踪"

**关键参数：**
- `id`（必填）—— 活动 UUID
- 以下任意组合：`name`、`campaign_schedule`、`email_list`、`sequences`、`daily_limit`、`email_gap`、`stop_on_reply`、`open_tracking`、`link_tracking` 等
- 将任意参数设为 `null` 以取消设置

---

### 4. 管理潜客名单与批量导入
创建专用的潜客名单，并批量导入潜在客户以用于活动定向。

**工具：** `INSTANTLY_CREATE_LEAD_LIST`、`INSTANTLY_ADD_LEADS_BULK`

**示例提示：**
> "创建一个名为 'Q1 Prospects' 的潜客名单，并向我的 Instantly 活动添加50个潜客"

**创建潜客名单的关键参数：**
- 名单名称和配置

**批量导入潜客的关键参数：**
- 要导入的活动或名单 ID
- 包含邮箱和元数据的潜客对象数组
- 重复项处理选项
- 潜客验证设置

---

### 5. 查看活动详情
检索完整的活动配置，以验证设置、检查序列或为更新做准备。

**工具：** `INSTANTLY_GET_CAMPAIGN`

**示例提示：**
> "显示我 Instantly 活动的完整详情"

**关键参数：**
- `id`（必填）—— 活动 UUID

---

### 6. 列出所有活动
枚举工作区中的所有活动，支持可选的筛选和分页。

**工具：** `INSTANTLY_LIST_CAMPAIGNS`

**示例提示：**
> "列出我所有的 Instantly 活动"

**关键参数：**
- 可选的筛选和分页参数

---

## 已知陷阱

- **时区支持有限**：Instantly API 只接受一组受限的时区字符串。不支持太平洋时间（"America/Los_Angeles"）。请使用 "America/Anchorage"（UTC-9/UTC-8）或 "America/Dawson"（全年 UTC-7）作为替代。
- **无效的调度负载会导致 400 错误**：格式错误的 `campaign_schedule`（缺少 `days`、`from`、`to` 或 `schedules`）会触发 HTTP 400。反复出现 400 表示负载存在问题，而不是临时性故障。
- **序列必须完整**：每个序列步骤都需要有效的 `type`（"email"）、`delay`，以及至少一个同时包含 `subject` 和 `body` 的变体。不完整的变体会阻止活动创建。
- **仅使用第一个序列元素**：API 只处理 `sequences[0]`。额外的序列会被忽略。
- **email_list 必须引用已存在的账户**：`email_list` 字段需要你 Instantly 工作区中预先配置好的发件账户的邮箱地址，而不是任意的收件人地址。请始终使用 `INSTANTLY_LIST_ACCOUNTS` 查找有效的发件地址。
- **创建活动时的 401 作用域错误**：创建活动可能会因 "Invalid scope. Required: campaigns:create" 而失败。在重试写操作之前，请更新你的 API 密钥权限。
- **回读字段可能有所不同**：`INSTANTLY_GET_CAMPAIGN` 响应中的字段名可能与创建负载不同（例如 `timing.from_` 对比 `timing.from`）。解析时要留有余地。

---

## 快速参考

| 操作 | 工具 Slug | 必填参数 |
|---|---|---|
| 列出发件账户 | `INSTANTLY_LIST_ACCOUNTS` | 无（可选筛选条件） |
| 创建活动 | `INSTANTLY_CREATE_CAMPAIGN` | `name`、`campaign_schedule` |
| 更新活动 | `INSTANTLY_UPDATE_CAMPAIGN` | `id` |
| 获取活动详情 | `INSTANTLY_GET_CAMPAIGN` | `id` |
| 列出活动 | `INSTANTLY_LIST_CAMPAIGNS` | 无（可选筛选条件） |
| 创建潜客名单 | `INSTANTLY_CREATE_LEAD_LIST` | 名单名称 |
| 批量导入潜客 | `INSTANTLY_ADD_LEADS_BULK` | 活动/名单 ID、潜客 |

---

*由 [Composio](https://composio.dev) 提供支持*
