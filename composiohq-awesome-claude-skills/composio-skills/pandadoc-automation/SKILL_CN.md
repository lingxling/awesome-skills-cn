---
name: PandaDoc Automation
description: "通过 Composio 的 PandaDoc 集成自动化文档工作流 —— 从文件创建文档、管理联系人、整理文件夹、设置 webhook、创建模板，并追踪文档状态。"
requires:
  mcp:
    - rube
---

# PandaDoc Automation

直接从 Claude Code 管理 **PandaDoc** 文档工作流。从已上传的文件创建文档、管理收件人和联系人、用文件夹整理内容、设置事件 webhook、创建模板，并追踪文档状态，全程无需离开终端。

**工具包文档：** [composio.dev/toolkits/pandadoc](https://composio.dev/toolkits/pandadoc)

---

## 设置

1. 将 Composio MCP 服务器添加到你的配置中：
   ```
   https://rube.app/mcp
   ```
2. 在提示时连接你的 PandaDoc 账户。代理会提供一个 OAuth 链接用于身份验证。
3. 确保你的 PandaDoc 工作区拥有所需功能对应的套餐（例如电子签名、模板、webhook）。

---

## 核心工作流

### 1. 从文件创建文档

上传 PDF、DOCX 或 RTF 文件以创建一个新的 PandaDoc 文档，并指定用于签署和追踪的收件人。

**工具：** `PANDADOC_CREATE_DOCUMENT_FROM_FILE`

关键参数：
- `name`（必填）—— 文档名称
- `recipients`（必填）—— 收件人对象数组，每个对象包含：
  - `email`（必填）—— 收件人邮箱
  - `first_name`、`last_name` —— 收件人姓名
  - `role` —— `signer`（默认）、`approver` 或 `cc`（每个收件人必须唯一）
  - `signing_order` —— 数字顺序（若为一人设置，则必须为所有人设置）
- `file` —— 上传的文件对象，包含 `name`、`mimetype` 和 `s3key`
- `url` —— 或者，提供一个可公开访问的 HTTPS 文件链接
- `parse_form_fields`（默认 false）—— 解析 PDF 表单字段
- `tags` —— 用于分类的字符串数组
- `owner` —— 文档所有者（邮箱或 membership_id）

示例提示：*“根据 contract.pdf 创建一个 PandaDoc 文档，john@example.com 作为签署人，jane@example.com 作为审批人”*

---

### 2. 获取文档详情

获取文档的完整元数据，包括收件人、字段、令牌、定价、标签以及内容块引用。

**工具：** `PANDADOC_GET_DOCUMENT_DETAILS`

关键参数：
- `id`（必填）—— 文档唯一标识符（例如 `BhVzRcxH9Z2LgfPPGXFUqa`）

用于检查文档状态、查看收件人完成情况、审阅字段值，或为报告收集元数据。

示例提示：*“获取 PandaDoc 文档 BhVzRcxH9Z2LgfPPGXFUqa 的完整详情和状态”*

---

### 3. 管理联系人

在 PandaDoc 中创建新联系人或更新现有联系人。联系人按邮箱匹配 —— 如果给定邮箱的联系人已存在，则更新；否则创建新联系人。

**工具：** `PANDADOC_CREATE_OR_UPDATE_CONTACT`

关键参数：
- `email`（必填）—— 联系人邮箱地址
- `first_name`、`last_name` —— 联系人姓名
- `company` —— 公司名称
- `job_title` —— 职位/头衔
- `phone` —— 电话号码
- `street_address`、`city`、`state`、`postal_code`、`country` —— 地址字段

示例提示：*“为 Acme Corp 的软件工程师 john.doe@example.com 创建一个 PandaDoc 联系人”*

---

### 4. 用文件夹整理内容

创建文件夹并移动文档，以整理你的 PandaDoc 工作区。

**工具：** `PANDADOC_CREATE_FOLDER`、`PANDADOC_LIST_DOCUMENT_FOLDERS`、`PANDADOC_MOVE_DOCUMENT_TO_FOLDER`

创建文件夹时：
- `name`（必填）—— 文件夹名称
- `parent_uuid` —— 用于嵌套结构的父文件夹 UUID

示例提示：*“在 PandaDoc 中创建一个‘Q1 2026 Contracts’文件夹，并将文档 BhVzRcxH9Z 移动到其中”*

---

### 5. 设置 Webhook

创建 webhook 订阅，以在文档事件发生时接收实时通知。

**工具：** `PANDADOC_CREATE_WEBHOOK`

关键参数：
- `name`（必填）—— webhook 的描述性名称
- `url`（必填）—— 接收通知的终端点 URL
- `triggers`（必填）—— 事件类型：`document_state_changed`、`recipient_completed`、`document_updated` 等
- `active`（默认 true）—— 启用/禁用该 webhook
- `payload` —— 要包含的附加数据：`fields`、`products`、`metadata`、`tokens`、`pricing`

示例提示：*“设置一个 PandaDoc webhook，在文档状态变化或收件人完成时通知 https://api.example.com/hooks”*

---

### 6. 创建模板

从 PDF 文件创建可复用模板，或使用结构化内容块从零创建。

**工具：** `PANDADOC_CREATE_TEMPLATE`

关键参数：
- `name`（必填）—— 模板名称
- `file_path` —— 用于创建模板的 PDF 文件路径
- `content` —— 包含 `title` 和 `blocks` 数组的结构化内容对象，用于从零构建
- `description` —— 模板描述
- `tags` —— 分类标签

示例提示：*“根据 nda-template.pdf 文件创建一个名为‘Standard NDA’的 PandaDoc 模板”*

---

## 已知坑点

- **收件人角色唯一性：** PandaDoc API 不允许单个文档中出现重复角色。每个收件人必须有唯一的 `role` 值（例如 `signer`、`signer_2`、`approver`、`cc`）。
- **签署顺序一致性：** 如果为任意收件人指定了 `signing_order`，则必须为文档中的所有收件人都指定。部分设置顺序会导致错误。
- **文件上传要求：** 创建文档时必须提供 `file`（含 `s3key`）或 `url` 二者之一，不能同时提供。URL 必须是可公开访问的 HTTPS 链接。
- **联系人 upsert 行为：** `PANDADOC_CREATE_OR_UPDATE_CONTACT` 按邮箱匹配。如果需要更新联系人自身的邮箱，必须创建一个新联系人并单独处理旧的那个。
- **文档 ID 格式：** 文档 ID 是字母数字字符串（例如 `BhVzRcxH9Z2LgfPPGXFUqa`）。文档创建时会返回该 ID，也可以在 PandaDoc 仪表盘中找到。
- **Webhook 事件命名：** 触发事件名称必须完全匹配（例如 `document_state_changed`，而不是 `stateChanged` 或 `state_changed`）。请查阅 PandaDoc API 文档获取完整列表。
- **文件夹操作需要 UUID：** 移动文档需要同时提供文档 ID 和目标文件夹的 UUID。请先列出文件夹以获取正确的 UUID。
- **模板内容块：** 从零创建模板时，`blocks` 数组必须包含符合 PandaDoc 架构的有效内容块对象。请查阅其 API 文档了解支持的块类型。

---

## 快速参考

| 工具标识 | 描述 |
|---|---|
| `PANDADOC_CREATE_DOCUMENT_FROM_FILE` | 从 PDF/DOCX/RTF 创建带收件人的文档 |
| `PANDADOC_GET_DOCUMENT_DETAILS` | 获取完整文档元数据、状态和字段 |
| `PANDADOC_CREATE_OR_UPDATE_CONTACT` | 按邮箱创建或更新联系人 |
| `PANDADOC_CREATE_FOLDER` | 创建用于文档整理的文件夹 |
| `PANDADOC_LIST_DOCUMENT_FOLDERS` | 列出所有文档文件夹 |
| `PANDADOC_MOVE_DOCUMENT_TO_FOLDER` | 将文档移动到指定文件夹 |
| `PANDADOC_CREATE_WEBHOOK` | 设置事件通知 webhook |
| `PANDADOC_CREATE_TEMPLATE` | 创建可复用的文档模板 |

---

*Powered by [Composio](https://composio.dev)*
