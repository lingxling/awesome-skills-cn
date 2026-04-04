---
name: Apollo Automation
description: "自动化 Apollo.io 潜在客户生成 -- 搜索组织、发现联系人、丰富潜在客户数据、管理联系人阶段，并构建定向外联列表 -- 通过 Composio MCP 集成使用自然语言。"
category: sales-intelligence
requires:
  mcp:
    - rube
---

# Apollo 自动化

使用 Apollo.io 提升您的销售潜在客户开发 — 搜索公司、发现决策者、用电子邮件和电话号码丰富联系人数据，并管理您的销售管道阶段 — 全部通过自然语言命令。

**工具包文档:** [composio.dev/toolkits/apollo](https://composio.dev/toolkits/apollo)

---

## 设置

1. 将 Composio MCP 服务器添加到您的客户端配置：
   ```
   https://rube.app/mcp
   ```
2. 在提示时连接您的 Apollo.io 账户（API 密钥认证）。
3. 开始发出自然语言命令以开发潜在客户和丰富数据。

---

## 核心工作流

### 1. 搜索组织

使用名称、位置、员工数量和行业关键词等过滤器查找目标公司。

**工具：** `APOLLO_ORGANIZATION_SEARCH`

**示例提示：**
> "在 Apollo 上查找德克萨斯州拥有 50-500 名员工的 SaaS 公司"

**关键参数：**
- `q_organization_name` -- 部分名称匹配（例如，"Apollo" 匹配 "Apollo Inc."）
- `organization_locations` -- 要包含的总部位置（例如，"texas"、"tokyo"）
- `organization_not_locations` -- 要排除的总部位置
- `organization_num_employees_ranges` -- "min,max" 格式的员工范围（例如，"50,500"）
- `q_organization_keyword_tags` -- 行业关键词（例如，"software"、"healthcare"）
- `page` / `per_page` -- 分页（每页最多 100，最多 500 页）

---

### 2. 在公司中发现人员

在 Apollo 的联系人数据库中搜索匹配职位、资历、位置和公司标准的人员。

**工具：** `APOLLO_PEOPLE_SEARCH`

**示例提示：**
> "在 microsoft.com 和 apollo.io 上查找销售副总裁"

**关键参数：**
- `person_titles` -- 职位（例如，"VP of Sales"、"CTO"）
- `person_seniorities` -- 资历级别（例如，"director"、"vp"、"senior"）
- `person_locations` -- 人员的地理位置
- `q_organization_domains` -- 公司域名（例如，"apollo.io" — 排除 "www."）
- `organization_ids` -- 来自组织搜索的 Apollo 公司 ID
- `contact_email_status` -- 按电子邮件状态过滤："verified"、"unverified"、"likely to engage"
- `page` / `per_page` -- 分页（每页最多 100）

---

### 3. 丰富个人联系人

使用电子邮件、LinkedIn URL 或姓名 + 公司为单个人员获取全面数据（电子邮件、电话、LinkedIn、公司信息）。

**工具：** `APOLLO_PEOPLE_ENRICHMENT`

**示例提示：**
> "在 Apollo 上丰富 Apollo.io 的 Tim Zheng"

**关键参数（至少需要一个标识符）：**
- `email` -- 人员的电子邮件地址
- `linkedin_url` -- 完整的 LinkedIn 个人资料 URL
- `first_name` + `last_name` + (`organization_name` 或 `domain`) -- 基于名称的匹配
- `domain` -- 不带协议的纯主机名（例如，"apollo.io"，而不是 "https://apollo.io"）
- `reveal_personal_emails` -- 设置为 true 以获取个人电子邮件（可能使用额外积分）
- `reveal_phone_number` -- 设置为 true 以获取电话号码（需要 `webhook_url`）

---

### 4. 批量丰富潜在客户

同时丰富多达 10 人，以实现高效的批量处理。

**工具：** `APOLLO_BULK_PEOPLE_ENRICHMENT`

**示例提示：**
> "使用他们的 Apollo 数据批量丰富这 5 个潜在客户：[姓名/电子邮件列表]"

**关键参数：**
- `details`（必需）-- 1-10 个人员对象的数组，每个都包含 `email`、`linkedin_url`、`first_name`、`last_name`、`domain`、`company_name` 等标识符
- `reveal_personal_emails` -- 包含个人电子邮件（额外积分）
- `reveal_phone_number` -- 包含电话号码（需要 `webhook_url`）

---

### 5. 管理联系人管道阶段

列出可用阶段并通过您的销售漏斗更新联系人。

**工具：** `APOLLO_LIST_CONTACT_STAGES`、`APOLLO_UPDATE_CONTACT_STAGE`

**示例提示：**
> "将联系人 X 和 Y 移至 Apollo 中的'合格'阶段"

**列出阶段的关键参数：** 无需必需参数。

**更新阶段的关键参数：**
- `contact_ids`（必需）-- 要更新的联系人 ID 数组
- `contact_stage_id`（必需）-- 目标阶段 ID（来自列出联系人阶段）

---

### 6. 创建和搜索保存的联系人

创建新的联系人记录并搜索您现有的 Apollo 联系人数据库。

**工具：** `APOLLO_CREATE_CONTACT`、`APOLLO_SEARCH_CONTACTS`

**示例提示：**
> "在 Apollo 中搜索 Stripe 的任何联系人"

**搜索的关键参数：**
- 关键词搜索、阶段 ID 过滤、排序选项
- `page` / `per_page` -- 分页

**创建的关键参数：**
- `first_name`、`last_name`、`email`、`organization_name`
- `account_id` -- 链接到组织
- `contact_stage_id` -- 初始销售阶段

---

## 已知陷阱

- **组织域名可能为空**：来自 `APOLLO_ORGANIZATION_SEARCH` 的某些组织返回缺失或空的域名字段。在依赖它们之前，请使用 `APOLLO_ORGANIZATION_ENRICHMENT` 验证域名。
- **HTTP 403 表示配置问题**：403 响应表示 API 密钥或计划访问问题 — 请勿重试。首先修复您的凭据或计划。
- **人员搜索返回混淆数据**：`APOLLO_PEOPLE_SEARCH` 可能显示 `has_email`/`has_direct_phone` 标志或混淆字段，而不是完整的联系人详细信息。请使用 `APOLLO_PEOPLE_ENRICHMENT` 获取完整信息。
- **分页限制严格**：人员搜索支持每页最多 100，最多 500 页。提前停止可能会遗漏结果集的大部分。
- **批量丰富的小批量限制**：`APOLLO_BULK_PEOPLE_ENRICHMENT` 每次调用仅接受 10 个项目。当标识符不足时，它可能返回 `status='success'` 且 `missing_records > 0` — 请使用 `APOLLO_PEOPLE_ENRICHMENT` 重试单个记录。
- **无自动去重**：`APOLLO_CREATE_CONTACT` 不会去重。请首先使用 `APOLLO_SEARCH_CONTACTS` 检查现有联系人。
- **域名格式很重要**：始终使用纯主机名（例如，"apollo.io"），不带协议前缀（"https://"）或 "www." 前缀。

---

## 快速参考

| 操作 | 工具标识符 | 必需参数 |
|---|---|---|
| 搜索组织 | `APOLLO_ORGANIZATION_SEARCH` | 无（可选过滤器） |
| 丰富组织 | `APOLLO_ORGANIZATION_ENRICHMENT` | `domain` |
| 批量丰富组织 | `APOLLO_BULK_ORGANIZATION_ENRICHMENT` | `domains` |
| 搜索人员 | `APOLLO_PEOPLE_SEARCH` | 无（可选过滤器） |
| 丰富人员 | `APOLLO_PEOPLE_ENRICHMENT` | 以下之一：`email`、`linkedin_url` 或姓名+公司 |
| 批量丰富人员 | `APOLLO_BULK_PEOPLE_ENRICHMENT` | `details`（1-10 个人员对象） |
| 列出联系人阶段 | `APOLLO_LIST_CONTACT_STAGES` | 无 |
| 更新联系人阶段 | `APOLLO_UPDATE_CONTACT_STAGE` | `contact_ids`、`contact_stage_id` |
| 创建联系人 | `APOLLO_CREATE_CONTACT` | 姓名 + 标识符 |
| 搜索联系人 | `APOLLO_SEARCH_CONTACTS` | 无（可选过滤器） |

---

*由 [Composio](https://composio.dev) 提供支持*
