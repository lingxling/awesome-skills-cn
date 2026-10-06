---
name: SharePoint Automation
description: "SharePoint 自动化：管理 SharePoint 和 OneDrive 中的站点、列表、文档、文件夹、页面并搜索内容"
requires:
  mcp: [rube]
---

# SharePoint Automation

自动化 SharePoint 操作，包括管理站点、列表、文档和文件夹。通过 SharePoint REST API 以及基于 OneDrive 的 Microsoft Graph 进行集成。

**工具包文档：** [composio.dev/toolkits/share_point](https://composio.dev/toolkits/share_point)

---

## 设置

本技能需要连接 **Rube MCP 服务器**，地址为 `https://rube.app/mcp`。

在执行任何工具之前，请确保 `share_point` 和 `one_drive` 工具包存在有效连接。如果没有活动连接，请通过 `RUBE_MANAGE_CONNECTIONS` 发起连接。

> **注意：** 许多 OneDrive/SharePoint 工具仅适用于组织的 Microsoft 365 账户（Azure AD/Entra ID）。不支持个人 Microsoft 账户。

---

## 核心工作流

### 1. 列出并浏览站点

获取站点详情并列举子站点，以发现 SharePoint 拓扑结构。

**工具：**
- `ONE_DRIVE_GET_SITE_DETAILS` —— 按 ID 获取特定站点的元数据
- `ONE_DRIVE_LIST_SITE_SUBSITES` —— 列出父站点下的所有子站点

**关键参数：**
- `site_id`（必需）—— 组合格式：`hostname,site-collection-guid,web-guid`（例如 `"contoso.sharepoint.com,da60e844-...,712a596e-..."`）

**示例：**
```
Tool: ONE_DRIVE_GET_SITE_DETAILS
Arguments:
  site_id: "contoso.sharepoint.com,2C712604-1370-44E7-A1F5-426573FDA80A,2D2244C3-251A-49EA-93A8-39E1C3A060FE"
```

---

### 2. 管理列表

创建列表、列举现有列表并检索列表项。

**工具：**
- `SHARE_POINT_LIST_ALL_LISTS` —— 检索站点上的所有列表（支持 OData 的 filter、select、orderby、top）
- `SHARE_POINT_SHAREPOINT_CREATE_LIST` —— 使用指定模板创建新列表
- `ONE_DRIVE_LIST_SITE_LISTS` —— 通过 Microsoft Graph 列出站点下的所有列表
- `ONE_DRIVE_GET_SHAREPOINT_LIST_ITEMS` —— 从特定列表中检索项目

**`SHARE_POINT_SHAREPOINT_CREATE_LIST` 的关键参数：**
- `name`（必需）—— 列表名称
- `template`（必需）—— 模板类型：`"genericList"`、`"documentLibrary"`、`"tasks"` 等
- `description` —— 可选描述

**`SHARE_POINT_LIST_ALL_LISTS` 的关键参数：**
- `filter` —— OData 过滤条件，例如 `"Hidden eq false"`
- `select` —— 要返回的属性，例如 `"Title,Id"`
- `orderby` —— 排序表达式，例如 `"Title desc"`
- `top` —— 限制结果数量

**示例：**
```
Tool: SHARE_POINT_SHAREPOINT_CREATE_LIST
Arguments:
  name: "Project Tasks"
  template: "tasks"
  description: "Task tracking for Q1 deliverables"
```

---

### 3. 管理文件夹和文件

创建文件夹、列出文件夹中的文件，并浏览文档库。

**工具：**
- `SHARE_POINT_SHAREPOINT_CREATE_FOLDER` —— 在文档库中创建新文件夹
- `SHARE_POINT_LIST_FILES_IN_FOLDER` —— 通过服务器相对 URL 列出文件夹中的文件
- `SHARE_POINT_GET_FOLDER_BY_SERVER_RELATIVE_URL` —— 按路径获取文件夹元数据

**`SHARE_POINT_SHAREPOINT_CREATE_FOLDER` 的关键参数：**
- `folder_name`（必需）—— 要创建的文件夹名称
- `document_library` —— 目标库（默认：`"Shared Documents"`）
- `relative_path` —— 库内的额外路径

**`SHARE_POINT_LIST_FILES_IN_FOLDER` 的关键参数：**
- `folder_name`（必需）—— 服务器相对 URL，例如 `"/Shared Documents"`
- `select` —— 逗号分隔的属性，例如 `"Name,ServerRelativeUrl,Length"`
- `top` —— 限制结果数量
- `orderby` —— 排序表达式，例如 `"Name desc"`

**示例：**
```
Tool: SHARE_POINT_LIST_FILES_IN_FOLDER
Arguments:
  folder_name: "/Shared Documents/Reports"
  select: "Name,ServerRelativeUrl,Length"
  top: 50
```

---

### 4. 搜索 SharePoint 内容

使用关键字查询语言（KQL）搜索站点上的文档、列表项和其他内容。

**工具：** `SHARE_POINT_SEARCH_QUERY`

**关键参数：**
- `querytext`（必需）—— KQL 查询，例如 `"project report"`、`"FileType:docx"`、`"Author:\"John Doe\""`
- `rowlimit` —— 每次请求的最大结果数（默认约 50，最大 500）
- `startrow` —— 用于分页的从零开始的偏移量
- `selectproperties` —— 要返回的属性，例如 `"Title,Author,Path"`
- `refinementfilters` —— 缩小结果范围，例如 `"FileType:equals(\"docx\")"`

**示例：**
```
Tool: SHARE_POINT_SEARCH_QUERY
Arguments:
  querytext: "IsDocument:1 FileType:pdf"
  rowlimit: 25
  selectproperties: "Title,Author,Path,LastModifiedTime"
```

---

### 5. 跟踪列表变更（增量查询）

使用增量查询来获取增量变化（新建、更新、删除的项），而不必读取整个列表。

**工具：** `ONE_DRIVE_LIST_SHAREPOINT_LIST_ITEMS_DELTA`

**关键参数：**
- `site_id`（必需）—— 组合站点 ID
- `list_id`（必需）—— 列表 GUID
- `token` —— 初次同步时省略；传入 `"latest"` 可获得带 token 的空响应；传入之前的 token 可获取自那以后的变化
- `expand` —— 例如 `"fields($select=ColumnA,ColumnB)"`
- `top` —— 每次响应的最大项数

---

### 6. 检索站点页面内容

读取现代 SharePoint 站点页面内容，包括画布网页部件。

**工具：** `SHARE_POINT_GET_SITE_PAGE_CONTENT`

**关键参数：**
- `page_file_name` —— 带 `.aspx` 扩展名的文件名，例如 `"Home.aspx"`
- `item_id` —— 备选方式：页面的列表项 ID
- `render_as` —— `"raw"`（默认）、`"text"` 或 `"html"`
- `site` —— 可选的站点名称范围

---

## 已知问题

| 问题 | 详情 |
|---------|--------|
| **站点 ID 格式** | 必须是组合格式：`hostname,site-collection-guid,web-guid`。格式不正确会导致 400 错误。 |
| **不支持个人账户** | `ONE_DRIVE_LIST_SITE_LISTS` 和基于 Graph 的工具仅适用于组织的 M365 账户，不适用于个人 MSA/Outlook.com 账户。 |
| **OData 过滤器语法** | SharePoint OData 过滤器使用特定语法。请逐步测试过滤条件；不支持的表达式可能会悄无声息地返回空结果。 |
| **分页** | 在列表操作中使用 `skiptoken` 进行服务器端分页。分页设置不完整可能导致遗漏结果。 |
| **文件夹路径** | 必须使用服务器相对 URL（例如 `/Shared Documents`），而不是绝对 URL。 |

---

## 快速参考

| 工具标识 | 描述 |
|-----------|-------------|
| `ONE_DRIVE_GET_SITE_DETAILS` | 获取 SharePoint 站点的元数据 |
| `ONE_DRIVE_LIST_SITE_SUBSITES` | 列出父站点的子站点 |
| `ONE_DRIVE_LIST_SITE_LISTS` | 列出站点下的所有列表（Graph API） |
| `ONE_DRIVE_LIST_SHAREPOINT_LIST_ITEMS_DELTA` | 跟踪列表的增量变化 |
| `ONE_DRIVE_GET_SHAREPOINT_LIST_ITEMS` | 从列表中检索项 |
| `ONE_DRIVE_LIST_DRIVES` | 列出用户/站点/组可用的驱动器 |
| `ONE_DRIVE_LIST_SITE_COLUMNS` | 列出站点的列定义 |
| `SHARE_POINT_LIST_ALL_LISTS` | 检索站点上的所有列表（REST API） |
| `SHARE_POINT_SHAREPOINT_CREATE_LIST` | 创建新的 SharePoint 列表 |
| `SHARE_POINT_SHAREPOINT_CREATE_FOLDER` | 在文档库中创建文件夹 |
| `SHARE_POINT_LIST_FILES_IN_FOLDER` | 列出文件夹中的文件 |
| `SHARE_POINT_SEARCH_QUERY` | 使用 KQL 搜索内容 |
| `SHARE_POINT_GET_SITE_PAGE_CONTENT` | 检索站点页面内容 |
| `SHARE_POINT_GET_FOLDER_BY_SERVER_RELATIVE_URL` | 按路径获取文件夹元数据 |

---

*Powered by [Composio](https://composio.dev)*
