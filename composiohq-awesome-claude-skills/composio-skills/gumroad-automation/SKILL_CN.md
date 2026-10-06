---
name: Gumroad Automation
description: "通过 Composio MCP 集成，使用自然语言自动化 Gumroad 产品管理、销售跟踪、许可证验证以及 webhook 订阅。"
category: e-commerce
requires:
  mcp:
    - rube
---

# Gumroad Automation

自动化你的 Gumroad 店铺 —— 列出产品、跟踪销售、验证许可证，以及管理实时 webhook —— 全部通过自然语言命令完成。

**工具包文档：** [composio.dev/toolkits/gumroad](https://composio.dev/toolkits/gumroad)

---

## 设置

1. 将 Composio MCP 服务器添加到你的客户端配置中：
   ```
   https://rube.app/mcp
   ```
2. 按提示连接你的 Gumroad 账户（API 密钥认证）。
3. 开始使用自然语言命令管理你的 Gumroad 店铺。

---

## 核心工作流

### 1. 列出所有产品
检索你已认证的 Gumroad 账户中的每一个产品，以获取用于后续操作的产品 ID。

**工具：** `GUMROAD_LIST_PRODUCTS`

**示例提示：**
> "列出我所有的 Gumroad 产品"

**参数：** 无需参数 —— 返回已认证账户的所有产品。

---

### 2. 使用过滤器跟踪销售
检索成功的销售记录，支持按电子邮件、日期范围、产品或分页进行可选过滤。

**工具：** `GUMROAD_GET_SALES`

**示例提示：**
> "显示 2025 年 1 月产品 prod_ABC123 的所有 Gumroad 销售记录"

**关键参数：**
- `after` —— ISO8601 日期/时间，用于过滤该时间之后的销售（例如 `2025-01-01T00:00:00Z`）
- `before` —— ISO8601 日期/时间，用于过滤该时间之前的销售
- `email` —— 按客户电子邮件地址过滤
- `product_id` —— 按特定产品 ID 过滤
- `page` —— 分页结果的页码（最小 1）

---

### 3. 验证许可证密钥
检查许可证密钥是否对特定产品有效，查看使用次数，或验证会员资格权限。

**工具：** `GUMROAD_VERIFY_LICENSE`

**示例提示：**
> "验证产品 prod_ABC123 的许可证密钥 ABCD-EFGH-IJKL-MNOP"

**关键参数（均为必填）：**
- `product_id` —— 用于验证的产品 ID（对于 2023 年 1 月 9 日及以后创建的产品为必填）
- `license_key` —— 许可证密钥字符串（例如 `ABCD-EFGH-IJKL-MNOP`）
- `increment_uses_count` —— 是否增加使用次数计数（默认为 true）

---

### 4. 订阅 Webhook 事件
通过将你的端点 URL 订阅到特定的 Gumroad 资源事件，设置实时事件通知。

**工具：** `GUMROAD_SUBSCRIBE_TO_RESOURCE`

**示例提示：**
> "将我的 webhook https://example.com/hook 订阅到 Gumroad 的销售事件"

**关键参数（均为必填）：**
- `resource_name` —— 以下之一：`sale`、`refund`、`dispute`、`dispute_won`、`cancellation`、`subscription_updated`、`subscription_ended`、`subscription_restarted`
- `post_url` —— 你用于接收 HTTP POST 通知的端点 URL

---

### 5. 列出活跃的 Webhook 订阅
在添加新订阅之前，先查看给定资源类型的现有 webhook 订阅，以避免重复。

**工具：** `GUMROAD_GET_RESOURCE_SUBSCRIPTIONS`

**示例提示：**
> "显示我所有针对销售事件的活跃 Gumroad webhook 订阅"

**关键参数（必填）：**
- `resource_name` —— 八种受支持事件类型之一（例如 `sale`、`refund`）

---

## 已知问题

- **许可证验证需要产品 ID**：2023 年 1 月 9 日及以后创建的产品需要 `product_id` 参数。较旧的产品可能无需此参数即可工作，但仍建议提供。
- **销售记录的分页**：销售结果是分页的。请始终通过递增 `page` 参数来检查是否还有更多页。
- **Webhook 去重**：在订阅某个资源之前，请使用 `GUMROAD_GET_RESOURCE_SUBSCRIPTIONS` 检查是否已存在订阅，以避免重复的 webhook。
- **ISO8601 日期格式**：销售记录的日期过滤必须使用 ISO8601 格式（例如 `2025-01-01T00:00:00Z`），而非纯日期。

---

## 快速参考

| 操作 | 工具 Slug | 必填参数 |
|---|---|---|
| 列出产品 | `GUMROAD_LIST_PRODUCTS` | 无 |
| 获取销售记录 | `GUMROAD_GET_SALES` | 无（均为可选过滤条件） |
| 验证许可证 | `GUMROAD_VERIFY_LICENSE` | `product_id`、`license_key` |
| 订阅事件 | `GUMROAD_SUBSCRIBE_TO_RESOURCE` | `resource_name`、`post_url` |
| 列出 webhook 订阅 | `GUMROAD_GET_RESOURCE_SUBSCRIPTIONS` | `resource_name` |

---

*由 [Composio](https://composio.dev) 提供支持*
