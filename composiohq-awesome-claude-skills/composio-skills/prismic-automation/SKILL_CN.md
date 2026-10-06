---
name: Prismic Automation
description: "自动化 Prismic 中的无头 CMS 操作 —— 通过 Composio Prismic 集成查询文档、搜索内容、检索自定义类型，并管理仓库引用。"
requires:
  mcp:
    - rube
---

# Prismic Automation

直接从 Claude Code 管理你的 **Prismic** 无头 CMS。按类型查询文档、对内容进行全文搜索、检查自定义类型，并使用仓库引用（repository refs）进行内容版本管理。

**工具包文档：** [composio.dev/toolkits/prismic](https://composio.dev/toolkits/prismic)

---

## 设置

1. 将 Composio MCP 服务器添加到你的配置中：
   ```
   https://rube.app/mcp
   ```
2. 按提示连接你的 Prismic 账户。智能体会提供一个身份验证链接。
3. 大多数内容查询都需要一个 `ref` 令牌。请始终先调用 `PRISMIC_REPOSITORY_API_GET_REFS` 或 `PRISMIC_REPOSITORY_API_GET_INFO` 以获取 master ref。

---

## 核心工作流

### 1. 获取仓库信息和引用

检索全面的仓库元数据，包括可用的引用（内容版本）、自定义类型、语言、标签和书签。这通常是你的第一个 API 调用。

**工具：** `PRISMIC_REPOSITORY_API_GET_INFO`、`PRISMIC_REPOSITORY_API_GET_REFS`

无需参数 —— 这些端点返回完整的仓库配置。`refs` 字段至关重要，因为所有内容查询都需要引用。

示例提示：*"获取我的 Prismic 仓库信息以及当前的 master ref"*

---

### 2. 使用谓词查询文档

使用 Prismic 的谓词查询语法获取文档，并提供完整的分页和过滤支持。

**工具：** `PRISMIC_CONTENT_API_QUERY_DOCUMENTS`

关键参数：
- `ref`（必填） —— 内容发布版本的引用 ID（通常是 master ref）
- `q` —— 谓词查询，例如 `[[at(document.type, "page")]]`
- `page`（最小 1）和 `pageSize`（1-100） —— 分页
- `lang` —— 语言代码，例如 `en-us`（默认 `*` 表示所有语言）
- `orderings` —— 排序方式，例如 `[my.article.date desc]`
- `fetch` —— 以逗号分隔的要获取的字段，以减小响应体积
- `fetchLinks` —— 内联解析关联文档字段

示例提示：*"在 Prismic 中查询所有已发布的博客文章，按日期降序排列，使用英语"*

---

### 3. 按类型获取文档

检索特定自定义类型的所有文档，并自动解析 master ref。

**工具：** `PRISMIC_GET_DOCUMENTS_BY_TYPE`

关键参数：
- `type`（必填） —— 自定义类型的 API ID，例如 `blog_post`、`article`、`page`
- `page`（默认 1）和 `pageSize`（1-100，默认 20）
- `lang` —— 语言代码过滤
- `orderings` —— 排序方式，例如 `[my.article.date desc]`
- `after` —— 基于游标的分页，用于超过第 50 页的深度分页

示例提示：*"获取 Prismic 中所有 blog_post 文档，每页 20 条"*

---

### 4. 全文搜索

在文档的所有文本字段中搜索指定词汇。不区分大小写，支持词根匹配。

**工具：** `PRISMIC_CONTENT_API_GET_DOCUMENTS_WITH_FULLTEXT_SEARCH`

关键参数：
- `q`（必填） —— 全文谓词，例如 `[[fulltext(document, "machine learning")]]`
- `page`、`pageSize`、`lang`、`orderings` —— 与其他查询相同的分页/过滤选项

示例提示：*"在所有 Prismic 文档中搜索 'machine learning'"*

---

### 5. 按 ID 获取单个文档

按唯一标识符检索特定文档。

**工具：** `PRISMIC_GET_DOCUMENT_BY_ID`

关键参数：
- `document_id`（必填） —— 唯一文档标识符
- `ref`（必填） —— 来自仓库的内容引用
- `lang` —— 可选的语言过滤

示例提示：*"获取 Prismic 文档 Xx2KLhEAAJljVWaA"*

---

### 6. 列出自定义类型

发现仓库中定义的所有自定义类型（内容模型），包括其结构定义。

**工具：** `PRISMIC_TYPES_API_GET_TYPES`

关键参数：
- `limit` —— 每页返回的最大类型数量
- `page` —— 页码（从 1 开始）
- `sort` —— 排序方式，例如 `name`

示例提示：*"列出我的 Prismic 仓库中的所有自定义类型"*

---

## 已知问题

- **所有内容查询都需要 ref：** 在查询任何文档之前，你必须先从 `PRISMIC_REPOSITORY_API_GET_REFS` 或 `PRISMIC_REPOSITORY_API_GET_INFO` 获取一个有效的 `ref`（通常是 master ref）。没有 ref 的查询将会失败。
- **谓词语法需要双括号：** Prismic 查询使用双方括号：`[[at(document.type, "page")]]`。如需多个谓词，可将它们组合：`[[at(document.type, "blog")][at(document.tags, ["featured"])]]`。
- **深度分页限制：** 标准的基于页码的分页在超过第 50 页后可能会失败。要进行深度分页，请使用 `after` 参数并传入上一次结果集中最后一个文档的 ID。
- **pageSize 上限为 100：** 每页请求超过 100 个文档将被拒绝。请使用分页来迭代更大的结果集。
- **语言过滤：** 默认的语言过滤器是 `*`（所有语言）。如果你需要特定区域语言的文档，请始终显式传入 `lang`（例如 `en-us`、`fr-fr`）。
- **集成字段需要单独的 ref：** 在使用 `PRISMIC_CONTENT_API_GET_DOCUMENTS_WITH_INTEGRATION_FIELDS` 时，除标准内容 `ref` 外，还需要一个 `integrationFieldsRef`。

---

## 快速参考

| 工具 Slug | 描述 |
|---|---|
| `PRISMIC_REPOSITORY_API_GET_INFO` | 获取仓库元数据、引用、类型、语言 |
| `PRISMIC_REPOSITORY_API_GET_REFS` | 列出所有引用（master + 发布版本） |
| `PRISMIC_TYPES_API_GET_TYPES` | 列出所有自定义类型/内容模型 |
| `PRISMIC_CONTENT_API_QUERY_DOCUMENTS` | 使用谓词和分页查询文档 |
| `PRISMIC_GET_DOCUMENTS_BY_TYPE` | 按自定义类型过滤获取文档 |
| `PRISMIC_GET_DOCUMENT_BY_ID` | 按 ID 检索单个文档 |
| `PRISMIC_CONTENT_API_GET_DOCUMENTS_WITH_FULLTEXT_SEARCH` | 在所有文档中进行全文搜索 |
| `PRISMIC_CONTENT_API_GET_DOCUMENTS_WITH_PREDICATES` | 使用多个谓词条件过滤文档 |
| `PRISMIC_CONTENT_API_GET_DOCUMENTS_WITH_INTEGRATION_FIELDS` | 获取包含集成字段数据的文档 |
| `PRISMIC_GET_DOCUMENTS_ORDERED` | 按指定字段排序获取文档 |

---

*由 [Composio](https://composio.dev) 提供支持*
