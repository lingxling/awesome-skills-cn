---
name: googledocs-automation
description: "通过 Rube MCP（Composio）自动化 Google Docs 任务：创建、编辑、搜索、导出、复制和更新文档。请始终先搜索工具以获取最新的模式定义。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 实现 Google Docs 自动化

使用 Rube MCP（Composio）以编程方式创建、编辑、搜索、导出和管理 Google Docs 文档。

**工具包文档**：[composio.dev/toolkits/googledocs](https://composio.dev/toolkits/googledocs)

## 前置条件
- 必须已连接 Rube MCP（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 对工具包 `googledocs` 建立活跃连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 以获取最新的工具模式

## 设置
**获取 Rube MCP**：在你的客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——只需添加该端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 是否可用
2. 对工具包 `googledocs` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接未处于 ACTIVE 状态，按返回的身份验证链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 创建新文档
使用 `GOOGLEDOCS_CREATE_DOCUMENT` 创建一个带标题和初始文本内容的新 Google Doc。
```
Tool: GOOGLEDOCS_CREATE_DOCUMENT
Parameters:
  - title (required): Document filename/title
  - text (required): Initial text content to insert into the document
```

### 2. 搜索文档
使用 `GOOGLEDOCS_SEARCH_DOCUMENTS` 按名称、内容、日期或共享状态查找 Google Docs 文档。
```
Tool: GOOGLEDOCS_SEARCH_DOCUMENTS
Parameters:
  - query: Search query string
  - max_results: Limit number of results
  - modified_after / created_after: Filter by date
  - shared_with_me: Filter shared documents
  - starred_only: Filter starred documents
  - include_shared_drives: Search shared drives
  - order_by: Sort results
  - page_token: Pagination token
```

### 3. 用 Markdown 更新文档内容
使用 `GOOGLEDOCS_UPDATE_DOCUMENT_MARKDOWN` 将文档的全部内容替换为 Markdown 格式的文本。
```
Tool: GOOGLEDOCS_UPDATE_DOCUMENT_MARKDOWN
Parameters:
  - id (required): Document ID
  - markdown (required): Markdown content to replace entire document body
```

### 4. 查找并替换文本
使用 `GOOGLEDOCS_REPLACE_ALL_TEXT` 替换文档中某字符串的所有出现位置。
```
Tool: GOOGLEDOCS_REPLACE_ALL_TEXT
Parameters:
  - document_id (required): Target document ID
  - find_text (required): Text to search for
  - replace_text (required): Replacement text
  - match_case: Case-sensitive matching (boolean)
  - search_by_regex: Use regex for find_text
  - tab_ids: Specific tabs to search
```

### 5. 将文档导出为 PDF
使用 `GOOGLEDOCS_EXPORT_DOCUMENT_AS_PDF` 将 Google Doc 导出为 PDF 格式。
```
Tool: GOOGLEDOCS_EXPORT_DOCUMENT_AS_PDF
Parameters:
  - file_id (required): Document file ID
  - filename: Output PDF filename
```

### 6. 复制文档
使用 `GOOGLEDOCS_COPY_DOCUMENT` 复制一份现有的 Google Doc。
```
Tool: GOOGLEDOCS_COPY_DOCUMENT
Parameters:
  - document_id (required): Source document ID to copy
  - title: Title for the new copy
  - include_shared_drives: Search shared drives for the source
```

## 常见模式

- **先搜索再编辑**：使用 `GOOGLEDOCS_SEARCH_DOCUMENTS` 按名称查找文档，然后用返回的文档 ID 配合 `GOOGLEDOCS_UPDATE_DOCUMENT_MARKDOWN` 或 `GOOGLEDOCS_REPLACE_ALL_TEXT` 来修改它。
- **从模板创建**：使用 `GOOGLEDOCS_COPY_DOCUMENT` 复制一个模板，然后用 `GOOGLEDOCS_REPLACE_ALL_TEXT` 填充占位文本。
- **先获取再更新**：使用 `GOOGLEDOCS_GET_DOCUMENT_BY_ID` 读取当前内容，然后用 `GOOGLEDOCS_UPDATE_EXISTING_DOCUMENT` 应用编辑。
- **批量插入文本**：使用 `GOOGLEDOCS_INSERT_TEXT_ACTION` 在特定位置（按索引）插入文本，或追加到文档末尾。
- **共享文档**：与 `GOOGLEDRIVE_ADD_FILE_SHARING_PREFERENCE`（googledrive 工具包）结合使用，在创建后共享文档。

## 常见陷阱

- `GOOGLEDOCS_UPDATE_DOCUMENT_MARKDOWN` 会替换文档的**全部**内容 -- 它不是追加。仅在需要完全重写时使用。
- `GOOGLEDOCS_INSERT_TEXT_ACTION` 需要精确的 `insertion_index`（字符位置）。设置 `append_to_end: true` 可以安全地在末尾添加文本。
- `GOOGLEDOCS_UPDATE_EXISTING_DOCUMENT` 需要构造一个包含原始 Google Docs API 批量更新请求的 `editDocs` 请求体 -- 请查阅该 API 文档以获取正确的结构。
- 对于 Google Docs，文档 ID 和文件 ID 是同一个值，但不同工具中参数名称不同（`id`、`document_id`、`file_id`）。
- `GOOGLEDOCS_SEARCH_DOCUMENTS` 的 `query` 参数使用 Google Drive 的搜索语法（例如 `name contains 'report'`）。

## 快速参考
| 操作 | 工具 | 关键参数 |
|--------|------|----------------|
| 创建文档 | `GOOGLEDOCS_CREATE_DOCUMENT` | `title`, `text` |
| 搜索文档 | `GOOGLEDOCS_SEARCH_DOCUMENTS` | `query`, `max_results`, `modified_after` |
| 按 ID 获取文档 | `GOOGLEDOCS_GET_DOCUMENT_BY_ID` | `id` |
| 用 Markdown 更新 | `GOOGLEDOCS_UPDATE_DOCUMENT_MARKDOWN` | `id`, `markdown` |
| 编程方式编辑 | `GOOGLEDOCS_UPDATE_EXISTING_DOCUMENT` | `document_id`, `editDocs` |
| 插入文本 | `GOOGLEDOCS_INSERT_TEXT_ACTION` | `document_id`, `text_to_insert`, `insertion_index` |
| 查找并替换 | `GOOGLEDOCS_REPLACE_ALL_TEXT` | `document_id`, `find_text`, `replace_text` |
| 导出为 PDF | `GOOGLEDOCS_EXPORT_DOCUMENT_AS_PDF` | `file_id`, `filename` |
| 复制文档 | `GOOGLEDOCS_COPY_DOCUMENT` | `document_id`, `title` |

---
*由 [Composio](https://composio.dev) 提供支持*
