---
name: Uploadcare Automation
description: "通过自然语言命令自动化 Uploadcare 文件管理，包括列出、存储、检查、下载文件以及组织文件组"
requires:
  mcp:
    - rube
---

# Uploadcare Automation

自动化 Uploadcare 文件处理工作流——列出项目文件、永久存储上传内容、获取文件元数据、获取下载链接，以及管理文件组——全部通过自然语言完成。

**工具包文档：** [composio.dev/toolkits/uploadcare](https://composio.dev/toolkits/uploadcare)

---

## 设置

1. 将 Rube MCP 服务器添加到你的环境中：`https://rube.app/mcp`
2. 按提示连接你的 Uploadcare 账户（通过 Composio 的 API 密钥认证）
3. 开始发出用于 Uploadcare 自动化的自然语言命令

---

## 核心工作流

### 1. 列出项目文件

浏览 Uploadcare 项目中已上传的文件，支持筛选、排序和分页。

**工具：** `UPLOADCARE_LIST_FILES`

关键参数：
- `stored` —— 按存储状态筛选：`"true"` 表示已存储，`"false"` 表示未存储
- `removed` —— 按移除状态筛选：`"true"` 表示已移除，`"false"` 表示有效
- `ordering` —— 按 `datetime_uploaded`（升序）或 `-datetime_uploaded`（降序）排序
- `limit` —— 每页文件数，1-1000（默认 100）
- `offset` —— 从零开始的分页偏移量
- `from_date` —— ISO 8601 时间戳，筛选在此日期之后上传的文件
- `to_date` —— ISO 8601 时间戳，筛选在此日期之前上传的文件
- `include` —— 设置为 `"total"` 可在响应中包含文件总数

示例提示：
> "列出我 Uploadcare 项目中最近上传的 50 个已存储文件"

---

### 2. 永久存储文件

将已上传的文件标记为永久存储。默认情况下，Uploadcare 文件是临时的，除非被存储，否则将在 24 小时后被删除。

**工具：** `UPLOADCARE_STORE_FILE`

关键参数：
- `uuid` —— 要存储的文件的 UUID（必需）；必须是 `8-4-4-4-12` 十六进制格式（例如 `3e55317b-23d1-4f35-9b4c-b9accb7b53f4`）

> 上传后始终存储文件，以防止自动删除。

示例提示：
> "永久存储 UUID 为 3e55317b-23d1-4f35-9b4c-b9accb7b53f4 的文件"

---

### 3. 获取文件元数据

获取特定文件的详细信息，包括大小、MIME 类型、CDN 链接、图像尺寸等。

**工具：** `UPLOADCARE_GET_FILE_INFO`

关键参数：
- `uuid` —— 要检查的文件的 UUID（必需）；格式：`8-4-4-4-12` 十六进制

返回：文件名、大小、MIME 类型、CDN 链接、上传日期、存储状态、图像信息（尺寸、颜色模式）等。

示例提示：
> "获取文件 3e0923f2-e05a-4b37-9f0d-343b981c9d70 的元数据和尺寸"

---

### 4. 获取临时下载链接

获取特定文件的临时直接下载链接。

**工具：** `UPLOADCARE_GET_FILE_DOWNLOAD_URL`

关键参数：
- `file_id` —— 唯一的文件标识符（必需）

返回一个限时链接，可用于直接下载文件。

示例提示：
> "获取文件 3e0923f2-e05a-4b37-9f0d-343b981c9d70 的下载链接"

---

### 5. 浏览文件组

列出项目中的文件组。组是一起上传的文件集合。

**工具：** `UPLOADCARE_LIST_GROUPS`

关键参数：
- `limit` —— 每页组数，1-1000（默认 20）
- `offset` —— 从零开始的分页偏移量（默认 0）
- `ordering` —— 按 `datetime_created`（升序）或 `-datetime_created`（降序）排序

示例提示：
> "列出我最近的 10 个文件组"

---

### 6. 文件生命周期工作流

组合多个工具以实现端到端的文件管理：

1. **上传**：文件通过 Uploadcare 的上传 API 或小部件上传（不在本工具包范围内）
2. **存储**：`UPLOADCARE_STORE_FILE` —— 将文件标记为永久，以防止自动删除
3. **检查**：`UPLOADCARE_GET_FILE_INFO` —— 验证元数据，检查尺寸和 MIME 类型
4. **分享**：`UPLOADCARE_GET_FILE_DOWNLOAD_URL` —— 生成临时下载链接
5. **浏览**：`UPLOADCARE_LIST_FILES` —— 通过状态和日期筛选审计所有文件
6. **组**：`UPLOADCARE_LIST_GROUPS` —— 查看批量上传

示例提示：
> "存储文件 abc-123，然后获取其元数据和下载链接"

---

## 已知陷阱

| 陷阱 | 详情 |
|---------|--------|
| 未存储文件会自动删除 | 上传的文件默认是临时的，24 小时后会被删除——始终调用 `UPLOADCARE_STORE_FILE` 来持久化保存 |
| UUID 格式严格 | 文件 UUID 必须严格符合 `8-4-4-4-12` 十六进制格式（例如 `3e55317b-23d1-4f35-9b4c-b9accb7b53f4`）；格式无效将被拒绝 |
| 筛选值是字符串 | `stored` 和 `removed` 参数接受字符串值 `"true"` 或 `"false"`，而不是布尔值 |
| 临时下载链接 | 来自 `UPLOADCARE_GET_FILE_DOWNLOAD_URL` 的链接是限时的，会过期 |
| 分页基于偏移量 | 使用 `offset` + `limit` 进行分页；没有基于游标的分页令牌 |
| 没有上传工具 | 文件上传通过 Uploadcare 的上传 API 或小部件完成，而不是通过本工具包——这些工具管理的是已上传的文件 |

---

## 快速参考

| 操作 | 工具标识 | 关键参数 |
|--------|-----------|------------|
| 列出文件 | `UPLOADCARE_LIST_FILES` | `stored`、`ordering`、`limit`、`offset` |
| 存储文件 | `UPLOADCARE_STORE_FILE` | `uuid` |
| 获取文件信息 | `UPLOADCARE_GET_FILE_INFO` | `uuid` |
| 获取下载链接 | `UPLOADCARE_GET_FILE_DOWNLOAD_URL` | `file_id` |
| 列出组 | `UPLOADCARE_LIST_GROUPS` | `limit`、`offset`、`ordering` |

---

*由 [Composio](https://composio.dev) 提供支持*
