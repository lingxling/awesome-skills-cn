---
name: Hunter Automation
description: "通过 Composio MCP 集成，使用自然语言自动化 Hunter.io 邮箱情报——按域名搜索邮箱地址、查找特定联系人、验证邮箱可送达性、管理潜在客户，以及监控账户用量"
category: email-intelligence
requires:
  mcp:
    - rube
---

# Hunter Automation

借助 Hunter.io 提升你的外联效率——按域名发现邮箱地址、查找特定人员的邮箱、验证可送达性、保存潜在客户，并跟踪你的 API 用量——全部通过自然语言命令完成。

**工具包文档：** [composio.dev/toolkits/hunter](https://composio.dev/toolkits/hunter)

---

## 设置

1. 将 Composio MCP 服务器添加到你的客户端配置：
   ```
   https://rube.app/mcp
   ```
2. 按提示连接你的 Hunter.io 账户（API 密钥认证）。
3. 开始发出用于查找和验证邮箱的自然语言命令。

---

## 核心工作流

### 1. 按域名搜索邮箱地址
发现给定域名或公司的所有公开可用邮箱地址，可按部门、职级和类型筛选。

**工具：** `HUNTER_DOMAIN_SEARCH`

**示例提示：**
> "使用 Hunter 查找 stripe.com 的所有高管邮箱地址"

**关键参数：**
- `domain` —— 要搜索的域名（例如 "stripe.com"）。若未提供 `company` 则必需。
- `company` —— 要搜索的公司名称（例如 "Stripe"）。若未提供 `domain` 则必需。
- `type` —— 按 "personal" 或 "generic" 邮箱筛选
- `seniority` —— 按职级筛选："junior"、"senior"、"executive"（数组）
- `department` —— 按部门筛选："executive"、"it"、"finance"、"sales" 等（数组）
- `required_field` —— 要求特定字段："full_name"、"position"、"phone_number"（数组）
- `limit` —— 每次请求的最大结果数（1-100，默认 10；免费/基础计划限制为 10）
- `offset` —— 分页跳过结果数（默认 0）

---

### 2. 查找特定人员的邮箱
根据姓名和域名或公司，推断某人最可能的邮箱地址。

**工具：** `HUNTER_EMAIL_FINDER`

**示例提示：**
> "使用 Hunter 查找 Alexis Ohanian 在 reddit.com 的邮箱"

**关键参数：**
- `domain` —— 目标域名（例如 "reddit.com"）。优先于 `company`。
- `company` —— 公司名称（例如 "Reddit"）。未提供 domain 时使用。
- 姓名（需提供以下组合之一）：
  - `first_name` + `last_name`（例如 "Alexis" + "Ohanian"）
  - `full_name`（例如 "Alexis Ohanian"）
- `max_duration` —— 最大请求时长（秒）（3-20，默认 10）。更长的时长可获得更准确的结果。

---

### 3. 验证邮箱可送达性
检查某个邮箱地址是否有效、可送达且可安全发送。

**工具：** `HUNTER_EMAIL_VERIFIER`

**示例提示：**
> "验证 john.doe@example.com 是否是有效邮箱地址"

**关键参数：**
- `email`（必需） —— 要验证的邮箱地址（例如 "john.doe@example.com"）

**响应包含：** 验证状态、可送达性评分、MX 记录验证和风险评估。

---

### 4. 获取邮箱数量估算
查询 Hunter 针对某个域名或公司拥有多少邮箱地址——此调用免费，不消耗 API 额度。

**工具：** `HUNTER_EMAIL_COUNT`

**示例提示：**
> "Hunter 对 stripe.com 有多少邮箱地址？"

**关键参数：**
- `domain` —— 要查询的域名（例如 "stripe.com"）。若未提供 `company` 则必需。
- `company` —— 公司名称（至少 3 个字符）。若未提供 `domain` 则必需。
- `type` —— 按 "personal" 或 "generic" 邮箱筛选数量

**返回：** 总数以及按类型、部门和职级划分的明细。

---

### 5. 保存和管理潜在客户
通过一次 upsert 调用按邮箱创建或更新潜在客户——无需先检查是否存在。

**工具：** `HUNTER_UPSERT_LEAD`

**示例提示：**
> "在 Hunter 中将 john@stripe.com 保存为潜在客户，姓名 John Doe，职位 CTO"

**关键参数：**
- `email` —— 潜在客户的邮箱地址（upsert 的主标识）
- 姓名、职位、公司及其他潜在客户元数据

---

### 6. 检查账户用量和限额
在执行批量操作之前，查看你的 Hunter 账户计划详情、剩余搜索次数和验证配额。

**工具：** `HUNTER_ACCOUNT_INFORMATION`

**示例提示：**
> "我本月还剩多少 Hunter API 搜索次数？"

**关键参数：** 无需参数。

---

## 已知陷阱

- **HTTP 401 表示凭据无效**：`authentication_failed` 错误表示 API 密钥无效或已过期。在尝试批量操作之前先修复。
- **邮箱数量是估算值**：`HUNTER_EMAIL_COUNT` 返回的是用于估量和优先级排序的近似数字，并不保证可检索到相同数量的邮箱。
- **域名搜索使用偏移分页**：`HUNTER_DOMAIN_SEARCH` 通过 `limit`/`offset` 分页。不要假设第一页就是完整结果——继续获取直到结果为空或达到上限。
- **空结果不是错误**：`HUNTER_DOMAIN_SEARCH` 可能返回 `emails: []` 而不报错。应视为"未找到数据"并继续，而不要当作失败重试。
- **验证状态的细微差别**：`HUNTER_EMAIL_VERIFIER` 返回的 `accept_all` 或 `risky` 状态表示存在不确定性。在严格的可送达性工作流中应排除这些结果，或单独处理。
- **免费/基础计划限制**：免费和基础计划将 `HUNTER_DOMAIN_SEARCH` 限制为每次请求 10 条结果。更高的限额需要付费计划。
- **域名格式很重要**：使用裸域名，如 "stripe.com"——不要包含协议（"https://"）或 "www." 前缀。

---

## 快速参考

| 操作 | 工具标识 | 必需参数 |
|---|---|---|
| 搜索域名邮箱 | `HUNTER_DOMAIN_SEARCH` | `domain` 或 `company` |
| 查找个人邮箱 | `HUNTER_EMAIL_FINDER` | 姓名 + (`domain` 或 `company`) |
| 验证邮箱 | `HUNTER_EMAIL_VERIFIER` | `email` |
| 获取邮箱数量 | `HUNTER_EMAIL_COUNT` | `domain` 或 `company` |
| 保存/更新潜在客户 | `HUNTER_UPSERT_LEAD` | `email` |
| 检查账户 | `HUNTER_ACCOUNT_INFORMATION` | 无 |

---

*由 [Composio](https://composio.dev) 提供支持*
