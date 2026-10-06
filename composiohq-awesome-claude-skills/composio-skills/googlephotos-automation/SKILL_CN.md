---
name: googlephotos-automation
description: "通过 Rube MCP（Composio）自动化 Google Photos 任务：上传媒体文件、管理相册、搜索照片、批量添加项目、创建和更新相册。务必先搜索工具以获取最新的模式定义。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 实现 Google Photos 自动化

使用 Rube MCP（Composio）上传照片、管理相册、搜索媒体项目，并在 Google Photos 中批量整理内容。

**工具包文档**：[composio.dev/toolkits/googlephotos](https://composio.dev/toolkits/googlephotos)

## 前置条件
- 必须已连接 Rube MCP（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 对工具包 `googlephotos` 建立有效连接
- 务必先调用 `RUBE_SEARCH_TOOLS` 以获取最新的工具模式定义

## 设置
**获取 Rube MCP**：将 `https://rube.app/mcp` 作为 MCP 服务器添加到你的客户端配置中。无需 API 密钥——只需添加端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 是否可用
2. 对工具包 `googlephotos` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接未处于 ACTIVE 状态，请按返回的身份验证链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 列出相册
使用 `GOOGLEPHOTOS_LIST_ALBUMS` 获取用户相册标签页中可见的所有相册。
```
Tool: GOOGLEPHOTOS_LIST_ALBUMS
Parameters:
  - pageSize: Number of albums per page
  - pageToken: Pagination token
  - excludeNonAppCreatedData: Only show albums created by this app
```

### 2. 创建新相册
使用 `GOOGLEPHOTOS_CREATE_ALBUM` 在 Google Photos 中创建新相册。
```
Tool: GOOGLEPHOTOS_CREATE_ALBUM
Parameters:
  - title (required): Album title
```

### 3. 上传媒体文件
使用 `GOOGLEPHOTOS_UPLOAD_MEDIA` 将图片或视频文件上传到 Google Photos。
```
Tool: GOOGLEPHOTOS_UPLOAD_MEDIA
Parameters:
  - file_to_upload: Local file path to upload
  - url: URL of file to upload (alternative to file_to_upload)
  - file_name: Name for the uploaded file
  - description: Description/caption for the media item
```

### 4. 批量上传并创建媒体项目
使用 `GOOGLEPHOTOS_BATCH_CREATE_MEDIA_ITEMS` 一次操作上传多个文件并创建媒体项目。
```
Tool: GOOGLEPHOTOS_BATCH_CREATE_MEDIA_ITEMS
Parameters:
  - files: Local file paths to upload
  - urls: URLs of files to upload
  - media_files: Mixed input (files and URLs)
  - albumId: Album to add items to
  - albumPosition: Position within the album
```

### 5. 搜索媒体项目
使用 `GOOGLEPHOTOS_SEARCH_MEDIA_ITEMS` 带筛选条件搜索用户的照片库。
```
Tool: GOOGLEPHOTOS_SEARCH_MEDIA_ITEMS
Parameters:
  - albumId: Filter by album
  - filters: Search filters (date ranges, content categories, media types)
  - orderBy: Sort order
  - pageSize: Results per page
  - pageToken: Pagination token
```

### 6. 将项目添加到相册
使用 `GOOGLEPHOTOS_BATCH_ADD_MEDIA_ITEMS` 将现有媒体项目添加到相册中。
```
Tool: GOOGLEPHOTOS_BATCH_ADD_MEDIA_ITEMS
Parameters:
  - albumId (required): Target album ID
  - mediaItemIds (required): Array of media item IDs to add
```

## 常见模式

- **先创建相册再上传**：使用 `GOOGLEPHOTOS_CREATE_ALBUM` 创建相册，然后用该相册 ID 调用 `GOOGLEPHOTOS_BATCH_CREATE_MEDIA_ITEMS`，一步完成照片的上传与整理。
- **先列出再整理**：使用 `GOOGLEPHOTOS_SEARCH_MEDIA_ITEMS` 或 `GOOGLEPHOTOS_LIST_MEDIA_ITEMS` 查找媒体项目 ID，然后使用 `GOOGLEPHOTOS_BATCH_ADD_MEDIA_ITEMS` 将它们添加到相册中。
- **更新相册元数据**：使用 `GOOGLEPHOTOS_UPDATE_ALBUM` 修改相册的标题或封面照片。
- **获取相册详情**：使用相册 ID 调用 `GOOGLEPHOTOS_GET_ALBUM` 获取完整的相册信息。
- **添加丰富内容**：使用 `GOOGLEPHOTOS_ADD_ENRICHMENT` 在相册的某个位置添加文字叠层、位置或地图丰富内容。
- **从 URL 上传**：在 `GOOGLEPHOTOS_UPLOAD_MEDIA` 中使用 `url` 参数，或在 `GOOGLEPHOTOS_BATCH_CREATE_MEDIA_ITEMS` 中使用 `urls` 参数，可直接从网络 URL 上传图片。

## 常见陷阱

- `GOOGLEPHOTOS_LIST_MEDIA_ITEMS` 已被**弃用**——建议使用 `GOOGLEPHOTOS_SEARCH_MEDIA_ITEMS` 来列出和筛选媒体文件。
- `GOOGLEPHOTOS_UPLOAD_MEDIA` 支持最大 **200MB** 的图片以及更大限制的视频。超出这些限制会导致失败。
- 相册 ID 必须从 `GOOGLEPHOTOS_LIST_ALBUMS` 或 `GOOGLEPHOTOS_CREATE_ALBUM` 的响应中获取——它们是不透明的字符串。
- `GOOGLEPHOTOS_BATCH_ADD_MEDIA_ITEMS` 只能将项目添加到**应用创建**的相册或用户自己拥有的相册中。
- `GOOGLEPHOTOS_SEARCH_MEDIA_ITEMS` 中的 `filters` 参数使用特定的 Google Photos API 筛选结构——请查阅模式定义以了解日期范围和内容分类的格式。
- 由于处理延迟，通过 API 创建的媒体项目可能不会立即出现在 Google Photos 网页界面中。

## 快速参考
| 操作 | 工具 | 关键参数 |
|--------|------|----------------|
| 列出相册 | `GOOGLEPHOTOS_LIST_ALBUMS` | `pageSize`、`pageToken` |
| 创建相册 | `GOOGLEPHOTOS_CREATE_ALBUM` | `title` |
| 获取相册 | `GOOGLEPHOTOS_GET_ALBUM` | `albumId` |
| 更新相册 | `GOOGLEPHOTOS_UPDATE_ALBUM` | `albumId`、`title`、`coverPhotoMediaItemId` |
| 上传媒体文件 | `GOOGLEPHOTOS_UPLOAD_MEDIA` | `file_to_upload` 或 `url`、`description` |
| 批量上传 | `GOOGLEPHOTOS_BATCH_CREATE_MEDIA_ITEMS` | `files` 或 `urls`、`albumId` |
| 搜索媒体文件 | `GOOGLEPHOTOS_SEARCH_MEDIA_ITEMS` | `albumId`、`filters`、`pageSize` |
| 列出媒体项目 | `GOOGLEPHOTOS_LIST_MEDIA_ITEMS` | `pageSize`、`pageToken` |
| 向相册添加项目 | `GOOGLEPHOTOS_BATCH_ADD_MEDIA_ITEMS` | `albumId`、`mediaItemIds` |
| 添加丰富内容 | `GOOGLEPHOTOS_ADD_ENRICHMENT` | `albumId`、`newEnrichmentItem`、`albumPosition` |

---
*由 [Composio](https://composio.dev) 提供支持*
