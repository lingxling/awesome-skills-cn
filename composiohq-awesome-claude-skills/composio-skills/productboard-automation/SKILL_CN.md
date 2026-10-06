---
name: Productboard Automation
description: "在 Productboard 中自动化产品管理工作流——通过自然语言指令管理功能、笔记、目标、组件和发布。"
requires:
  mcp:
    - rube
---

# Productboard 自动化

直接从 Claude Code 自动化你的 Productboard 产品管理操作。根据客户反馈创建笔记、浏览功能和目标、关联实体并跟踪发布——无需离开终端。

**工具包文档：** [composio.dev/toolkits/productboard](https://composio.dev/toolkits/productboard)

---

## 设置

1. 在你的 Claude Code 配置中添加 Rube MCP 服务器，URL 为：`https://rube.app/mcp`
2. 收到提示时，通过提供的连接链接认证你的 Productboard 账户
3. 开始用自然语言自动化你的产品管理工作流

---

## 核心工作流

### 1. 管理客户笔记

根据客户反馈创建笔记，并用标签、链接和关注者进行组织。

**工具：** `PRODUCTBOARD_CREATE_NOTE`、`PRODUCTBOARD_LIST_NOTES`、`PRODUCTBOARD_ADD_NOTE_TAG`、`PRODUCTBOARD_ADD_NOTE_FOLLOWERS`、`PRODUCTBOARD_CREATE_NOTE_LINK`

```
创建一条标题为 "Mobile app crash report" 的笔记，内容来自客户反馈，标记为 "bug" 并关联到功能 abc-123
```

`PRODUCTBOARD_CREATE_NOTE` 的关键参数：
- `title`（必填）和 `content`（必填） -- 笔记标题和正文
- `customer_email` 或 `user.email` -- 归属到某客户/用户
- `tags` -- 用于分类的标签字符串数组
- `display_url` -- 从笔记标题链接出去的 URL
- `source` -- 来源系统，包含 `origin` 和 `record_id`
- `company` -- 与某公司关联

`PRODUCTBOARD_LIST_NOTES` 的关键参数：
- `createdFrom` / `createdTo` -- ISO 8601 日期范围
- `last` -- 相对时间窗口（例如 `"6m"`、`"10d"`、`"24h"`）
- `term` -- 按标题或内容进行全文搜索
- `allTags` / `anyTag` -- 按标签过滤（两者不能同时使用）
- `featureId`、`companyId`、`ownerEmail`、`source` -- 实体过滤器
- `pageLimit`（最大 100）/ `pageCursor` -- 分页

### 2. 浏览和检索功能

列出所有功能/子功能并检索详细信息。

**工具：** `PRODUCTBOARD_LIST_FEATURES`、`PRODUCTBOARD_RETRIEVE_FEATURE`

```
列出 Productboard 中的前 50 个功能，然后获取功能 abc-def-123 的详情
```

- `PRODUCTBOARD_LIST_FEATURES` 支持 `pageLimit`（默认 100）和 `pageOffset` 进行分页
- `PRODUCTBOARD_RETRIEVE_FEATURE` 需要功能 `id`（UUID）才能获取完整详情

### 3. 目标与关键结果（OKR）

列出目标、查看功能与目标之间的关联，并浏览关键结果。

**工具：** `PRODUCTBOARD_LIST_OBJECTIVES`、`PRODUCTBOARD_LIST_FEATURE_OBJECTIVES`、`PRODUCTBOARD_LIST_KEY_RESULTS`

```
显示 alice@example.com 负责的所有进行中目标
```

`PRODUCTBOARD_LIST_OBJECTIVES` 的关键参数：
- `status.name` -- 按状态过滤（例如 `"In Progress"`）
- `owner.email` -- 按负责人邮箱过滤
- `parent.id` -- 按父级目标过滤
- `archived` -- 按归档状态过滤

`PRODUCTBOARD_LIST_FEATURE_OBJECTIVES`：
- 需要**顶级功能**（非子功能）的 `id`（UUID）
- 支持 `pageCursor` 进行分页

### 4. 组件管理

列出用于组织功能和产品层级结构的产品组件。

**工具：** `PRODUCTBOARD_LIST_COMPONENTS`

```
列出我们 Productboard 工作区中的所有组件
```

- 支持 `page_limit` 和 `page_offset` 进行分页
- 跟随 `links.next` 获取更多页面

### 5. 发布跟踪

查看带有状态和日期过滤条件的功能-发布分配。

**工具：** `PRODUCTBOARD_LIST_FEATURE_RELEASE_ASSIGNMENTS`

```
显示功能 abc-123 的所有活动发布分配
```

- 按 `feature.id`、`release.id`、`release.state`（planned、active、closed）过滤
- 日期范围过滤器：`release.timeframe.endDate.from` 和 `release.timeframe.endDate.to`（YYYY-MM-DD）

### 6. 将笔记关联到功能

将客户反馈笔记关联到产品功能，以便聚合洞察。

**工具：** `PRODUCTBOARD_CREATE_NOTE_LINK`

```
将笔记 3fa85f64-5717 关联到功能 1b6c8c76-8f5d 以便跟踪
```

- 需要 `noteId`（UUID）和 `entityId`（功能、组件或产品的 UUID）
- 在创建笔记后使用，以确保反馈与正确的产品区域相关联

---

## 已知坑点

- **目标仅适用于顶级功能：** `PRODUCTBOARD_LIST_FEATURE_OBJECTIVES` 只适用于顶级功能 ID，不适用于子功能 ID。使用 `PRODUCTBOARD_LIST_FEATURES` 来确定哪些功能是顶级的。
- **标签过滤互斥：** `allTags` 和 `anyTag` 不能在 `PRODUCTBOARD_LIST_NOTES` 中同时使用。每次查询只能选择一种过滤策略。
- **相对日期与绝对日期：** `last` 参数（例如 `"24h"`）不能与 `PRODUCTBOARD_LIST_NOTES` 中的 `createdFrom`/`createdTo` 组合使用。只能使用其中一种方式。
- **基于游标的分页：** 对于多页结果，跟随响应中的 `links.next` 或使用 `pageCursor`。基于偏移量的分页和基于游标的分页用在不同的端点上——请逐一检查各工具。
- **笔记归属：** 在 `PRODUCTBOARD_CREATE_NOTE` 中必须提供 `user.email` 或 `customer_email` 之一来归属反馈。否则该笔记将没有客户关联。
- **需要 UUID 格式：** 所有实体 ID（功能、笔记、组件）都必须是有效的 UUID。传入格式错误的 ID 会导致 400 错误。

---

## 快速参考

| 工具标识 | 描述 |
|---|---|
| `PRODUCTBOARD_CREATE_NOTE` | 创建客户反馈笔记（需要 `title`、`content`） |
| `PRODUCTBOARD_LIST_NOTES` | 列出笔记，支持搜索、日期和标签过滤 |
| `PRODUCTBOARD_ADD_NOTE_TAG` | 为笔记添加标签 |
| `PRODUCTBOARD_ADD_NOTE_FOLLOWERS` | 通过邮箱为笔记添加关注者 |
| `PRODUCTBOARD_CREATE_NOTE_LINK` | 将笔记关联到功能/组件（需要 `noteId`、`entityId`） |
| `PRODUCTBOARD_LIST_FEATURES` | 分页列出所有功能 |
| `PRODUCTBOARD_RETRIEVE_FEATURE` | 按 UUID 获取详细功能信息 |
| `PRODUCTBOARD_LIST_OBJECTIVES` | 按状态/负责人过滤列出目标 |
| `PRODUCTBOARD_LIST_FEATURE_OBJECTIVES` | 列出与某顶级功能关联的目标 |
| `PRODUCTBOARD_LIST_KEY_RESULTS` | 列出目标的关键结果 |
| `PRODUCTBOARD_LIST_COMPONENTS` | 分页列出产品组件 |
| `PRODUCTBOARD_LIST_FEATURE_RELEASE_ASSIGNMENTS` | 按过滤条件列出功能-发布分配 |

---

*Powered by [Composio](https://composio.dev)*
