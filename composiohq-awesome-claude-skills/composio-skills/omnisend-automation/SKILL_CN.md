---
name: Omnisend Automation
description: "通过 Composio 自动化 Omnisend 的电商营销工作流，包括联系人管理、批量操作和订阅者细分"
requires:
  mcp:
    - rube
---

# Omnisend Automation

自动化电商营销操作 —— 创建和更新联系人、通过游标分页管理订阅者列表、运行批量操作，并对受众进行细分 —— 全部通过 Composio MCP 集成编排完成。

**工具包文档：** [composio.dev/toolkits/omnisend](https://composio.dev/toolkits/omnisend)

---

## 设置

1. 通过 `https://rube.app/mcp` 的 Composio MCP 服务器连接你的 Omnisend 账户
2. 如果不存在活动连接，代理会提示一个身份验证链接
3. 连接完成后，所有 `OMNISEND_*` 工具即可供执行

---

## 核心工作流

### 1. 创建或更新联系人
通过邮箱标识符更新插入（upsert）联系人，设置订阅状态、资料字段以及可选的欢迎消息。

**工具：** `OMNISEND_CREATE_OR_UPDATE_CONTACT`

| 参数 | 类型 | 必填 | 描述 |
|-----------|------|----------|-------------|
| `identifiers` | array | 是 | 至少一个标识符对象，包含 `id`（邮箱）、`type`（`email`）、可选的 `channels.email.status`（`subscribed`、`nonSubscribed`、`unsubscribed`）以及 `sendWelcomeMessage`（布尔值） |
| `firstName` | string | 否 | 联系人的名 |
| `lastName` | string | 否 | 联系人的姓 |
| `gender` | string | 否 | `m` 或 `f` |
| `birthdate` | string | 否 | 格式：`YYYY-MM-DD` |
| `country` | string | 否 | 完整国家名称 |
| `countryCode` | string | 否 | ISO 3166-1 alpha-2 代码（例如 `US`） |
| `city` | string | 否 | 城市名称 |
| `address` | string | 否 | 街道地址 |
| `postalCode` | string | 否 | 邮政编码 |

---

### 2. 分页列出联系人
分批检索联系人，并可选按邮箱、电话、状态、细分或标签进行过滤。

**工具：** `OMNISEND_LIST_CONTACTS`

| 参数 | 类型 | 必填 | 描述 |
|-----------|------|----------|-------------|
| `limit` | integer | 否 | 每页结果数（默认：100，最大：250） |
| `after` | string | 否 | 下一页的游标（base64 编码的 ContactID） |
| `before` | string | 否 | 上一页的游标 |
| `email` | string | 否 | 按精确邮箱地址过滤 |
| `phone` | string | 否 | 按含国家代码的完整电话号码过滤 |
| `status` | string | 否 | 按以下值过滤：`subscribed`、`nonSubscribed`、`unsubscribed` |
| `segmentID` | integer | 否 | 按细分 ID 过滤 |
| `tag` | string | 否 | 按标签过滤（例如 `VIP`） |

---

### 3. 获取联系人详情
当已有联系人 ID 时，检索单个联系人的完整资料。

**工具：** `OMNISEND_GET_CONTACT`

| 参数 | 类型 | 必填 | 描述 |
|-----------|------|----------|-------------|
| `contactId` | string | 是 | 唯一联系人标识符（例如 `60e7412b1234567890abcdef`） |

---

### 4. 更新现有联系人
按 ID 修补联系人的特定字段，而不覆盖整条记录。

**工具：** `OMNISEND_UPDATE_CONTACT`

需要 `contactId` 以及要更新的字段。请先通过 `OMNISEND_LIST_CONTACTS` 或 `OMNISEND_GET_CONTACT` 获取联系人 ID。

---

### 5. 批量操作
在单次调用中异步处理大量记录 —— 联系人、产品、订单、事件或分类。

**工具：** `OMNISEND_CREATE_BATCH`

| 参数 | 类型 | 必填 | 描述 |
|-----------|------|----------|-------------|
| `method` | string | 是 | `POST` 或 `PUT` |
| `endpoint` | string | 是 | 目标：`contacts`、`orders`、`products`、`events`、`categories` |
| `items` | array | 是 | 每个操作对应的负载对象数组 |
| `eventID` | string | 条件必填 | 当 endpoint 为 `events` 时必填 |

使用批量操作可在处理大数据集时避免触发速率限制。

---

## 已知坑点

| 坑点 | 详情 |
|---------|---------|
| **需要标识符** | `OMNISEND_CREATE_OR_UPDATE_CONTACT` 要求 `identifiers` 数组中至少有一个标识符 —— 仅支持 `email` 类型 |
| **基于游标的分页** | `OMNISEND_LIST_CONTACTS` 使用 base64 编码的 `after`/`before` 游标，而不是页码 —— 请沿游标继续获取，避免数据不完整 |
| **联系人 ID 解析** | `OMNISEND_UPDATE_CONTACT` 需要 `contactId` —— 请始终先通过列表或获取操作解析出该 ID |
| **批量方法限制** | `OMNISEND_CREATE_BATCH` 只接受 `POST` 或 `PUT` 方法 —— 不支持 `DELETE` 或 `PATCH` |
| **事件 ID 依赖** | 批量处理事件时，`eventID` 参数是必填的 —— 省略它会导致批处理失败 |

---

## 快速参考

| 工具标识 | 用途 |
|-----------|---------|
| `OMNISEND_CREATE_OR_UPDATE_CONTACT` | 按邮箱创建或更新插入联系人 |
| `OMNISEND_LIST_CONTACTS` | 带过滤和游标分页列出联系人 |
| `OMNISEND_GET_CONTACT` | 按 ID 获取单个联系人的完整资料 |
| `OMNISEND_UPDATE_CONTACT` | 修补现有联系人的特定字段 |
| `OMNISEND_CREATE_BATCH` | 针对联系人、产品、订单、事件的批量异步操作 |

---

*Powered by [Composio](https://composio.dev)*
