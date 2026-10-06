---
name: Lemlist Automation
description: "自动化 Lemlist 多渠道外联 -- 通过 Composio MCP 集成管理营销活动、注册潜在客户、添加个性化变量、导出活动数据以及处理退订。"
requires:
  mcp:
    - rube
---

# Lemlist Automation

自动化你的 Lemlist 多渠道外联工作流 -- 管理营销活动、大规模注册潜在客户、用自定义变量进行丰富、导出活动数据，以及清理退订名单。

**工具包文档：** [composio.dev/toolkits/lemlist](https://composio.dev/toolkits/lemlist)

---

## 设置

1. 将 Composio MCP 服务器添加到你的客户端：`https://rube.app/mcp`
2. 按提示连接你的 Lemlist 账户（API 密钥身份验证）
3. 开始使用下面的工作流

---

## 核心工作流

### 1. 列出并发现营销活动

使用 `LEMLIST_GET_LIST_CAMPAIGNS` 按状态枚举所有营销活动，支持分页。

```
Tool: LEMLIST_GET_LIST_CAMPAIGNS
Inputs:
  - status: "running" | "draft" | "archived" | "ended" | "paused" | "errors" (optional)
  - limit: integer (max 100, default 100)
  - offset: integer (pagination offset)
  - sortBy: "createdAt"
  - sortOrder: "asc" | "desc"
```

**重要提示：** 响应可能被包装为 `{campaigns: [...], pagination: {...}}`，而不是扁平列表。始终从 `campaigns` 键中提取数据。

### 2. 获取营销活动详情

使用 `LEMLIST_GET_CAMPAIGN_BY_ID` 在写入前验证营销活动配置。

```
Tool: LEMLIST_GET_CAMPAIGN_BY_ID
Inputs:
  - campaignId: string (required) -- e.g., "cam_A1B2C3D4E5F6G7H8I9"
```

### 3. 将潜在客户注册到营销活动

使用 `LEMLIST_POST_CREATE_LEAD_IN_CAMPAIGN` 添加潜在客户，可选邮箱查找、电话查找和 LinkedIn 信息丰富。

```
Tool: LEMLIST_POST_CREATE_LEAD_IN_CAMPAIGN
Inputs:
  - campaignId: string (required)
  - email: string (required)
  - firstName, lastName, companyName, companyDomain: string (optional)
  - jobTitle, phone, linkedinUrl, icebreaker: string (optional)
  - deduplicate: boolean (prevents cross-campaign duplicates)
  - findEmail, findPhone, verifyEmail, linkedinEnrichment: boolean (optional)
  - timezone: string (IANA format, e.g., "America/New_York")
```

**批量模式：** 将潜在客户按约 50 条分批处理，并在批次之间设置检查点以记录进度。

### 4. 为潜在客户添加自定义变量

使用 `LEMLIST_POST_ADD_VARIABLES_TO_LEAD` 在注册后为潜在客户丰富个性化字段。

```
Tool: LEMLIST_POST_ADD_VARIABLES_TO_LEAD
Inputs:
  - leadId: string (required) -- internal Lemlist lead ID (NOT email)
  - company: string (required) -- must match your company name in Lemlist
  - variables: object (required) -- key-value pairs, e.g., {"score": "42", "color": "yellow"}
```

**重要提示：** 这不是一个 upsert 操作 -- 尝试添加已存在的变量会失败。如果你只有邮箱地址，请先通过 `LEMLIST_GET_RETRIEVE_LEAD_BY_EMAIL` 解析出内部的 `leadId`。

### 5. 导出营销活动的潜在客户

使用 `LEMLIST_GET_EXPORT_CAMPAIGN_LEADS` 按状态过滤下载潜在客户，用于报告或质检。

```
Tool: LEMLIST_GET_EXPORT_CAMPAIGN_LEADS
Inputs:
  - campaignId: string (required)
  - (supports state filtering and JSON/CSV output)
```

### 6. 将潜在客户从营销活动中退订

使用 `LEMLIST_DELETE_UNSUBSCRIBE_LEAD_FROM_CAMPAIGN` 通过将潜在客户从营销活动中移除来停止外联。

```
Tool: LEMLIST_DELETE_UNSUBSCRIBE_LEAD_FROM_CAMPAIGN
Inputs:
  - campaignId: string (required)
  - leadId or email: string (required)
```

---

## 常见陷阱

| 陷阱 | 详情 |
|---------|--------|
| 被包装的营销活动列表 | `LEMLIST_GET_LIST_CAMPAIGNS` 可能返回 `{campaigns: [...], pagination: {...}}`，而不是扁平数组。始终从 `campaigns` 键中提取数据。 |
| 跨活动去重 | 启用去重的 `LEMLIST_POST_CREATE_LEAD_IN_CAMPAIGN` 会因 "Lead already in other campaign" 返回 HTTP 500 失败 -- 对于有意的跨活动注册，请关闭去重功能。 |
| 批量导入失败 | 将批量导入按约 50 条一批进行分块，并设置检查点，以避免在间歇性失败时丢失部分进度。 |
| 无效的 leadId | 如果将邮箱当作 leadId 使用，`LEMLIST_POST_ADD_VARIABLES_TO_LEAD` 会返回 HTTP 400 "Invalid leadId" -- 请先通过 `LEMLIST_GET_RETRIEVE_LEAD_BY_EMAIL` 解析出内部 ID。 |
| 变量冲突 | `LEMLIST_POST_ADD_VARIABLES_TO_LEAD` 不是 upsert 操作。添加已存在的键会返回 HTTP 400 "Variables X already exist"。 |

---

## 快速参考

| 工具标识 | 说明 |
|-----------|-------------|
| `LEMLIST_GET_LIST_CAMPAIGNS` | 列出所有营销活动，支持状态过滤和分页 |
| `LEMLIST_GET_CAMPAIGN_BY_ID` | 按 ID 获取营销活动的详细信息 |
| `LEMLIST_POST_CREATE_LEAD_IN_CAMPAIGN` | 创建潜在客户并注册到营销活动 |
| `LEMLIST_POST_ADD_VARIABLES_TO_LEAD` | 为潜在客户添加自定义个性化变量 |
| `LEMLIST_GET_RETRIEVE_LEAD_BY_EMAIL` | 按邮箱地址查找潜在客户 |
| `LEMLIST_GET_EXPORT_CAMPAIGN_LEADS` | 按状态过滤导出营销活动中的潜在客户 |
| `LEMLIST_DELETE_UNSUBSCRIBE_LEAD_FROM_CAMPAIGN` | 将潜在客户从营销活动中移除 |

---

*由 [Composio](https://composio.dev) 提供支持*
