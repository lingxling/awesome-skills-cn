---
name: googlephotos-automation
description: "Automate Google Photos tasks via Rube MCP (Composio): upload media, manage albums, search photos, batch add items, create and update albums. Always search tools first for current schemas."
requires:
  mcp: [rube]
---

# Google Photos Automation via Rube MCP

Upload photos, manage albums, search media items, and batch-organize content in Google Photos using Rube MCP (Composio).

**Toolkit docs**: [composio.dev/toolkits/googlephotos](https://composio.dev/toolkits/googlephotos)

## 前置条件
- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- Active connection via `RUBE_MANAGE_CONNECTIONS` with toolkit `googlephotos`
- 始终首先调用 `RUBE_SEARCH_TOOLS` 以获取当前工具架构

## 设置
**获取 Rube MCP**: 在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 响应来验证 Rube MCP 可用
2. Call `RUBE_MANAGE_CONNECTIONS` with toolkit `googlephotos`
3. 如果连接未处于 ACTIVE 状态，请按照返回的授权链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## Core Workflows

### 1. List Albums
Use `GOOGLEPHOTOS_LIST_ALBUMS` to retrieve all albums visible in the user's Albums tab.
```
Tool: GOOGLEPHOTOS_LIST_ALBUMS
Parameters:
  - pageSize: Number of albums per page
  - pageToken: Pagination token
  - excludeNonAppCreatedData: Only show albums created by this app
```

### 2. Create a New Album
Use `GOOGLEPHOTOS_CREATE_ALBUM` to create a new album in Google Photos.
```
Tool: GOOGLEPHOTOS_CREATE_ALBUM
Parameters:
  - title (required): Album title
```

### 3. Upload Media
Use `GOOGLEPHOTOS_UPLOAD_MEDIA` to upload an image or video file to Google Photos.
```
Tool: GOOGLEPHOTOS_UPLOAD_MEDIA
Parameters:
  - file_to_upload: Local file path to upload
  - url: URL of file to upload (alternative to file_to_upload)
  - file_name: Name for the uploaded file
  - description: Description/caption for the media item
```

### 4. Batch Upload and Create Media Items
Use `GOOGLEPHOTOS_BATCH_CREATE_MEDIA_ITEMS` to upload multiple files and create media items in one operation.
```
Tool: GOOGLEPHOTOS_BATCH_CREATE_MEDIA_ITEMS
Parameters:
  - files: Local file paths to upload
  - urls: URLs of files to upload
  - media_files: Mixed input (files and URLs)
  - albumId: Album to add items to
  - albumPosition: Position within the album
```

### 5. Search Media Items
Use `GOOGLEPHOTOS_SEARCH_MEDIA_ITEMS` to search the user's photo library with filters.
```
Tool: GOOGLEPHOTOS_SEARCH_MEDIA_ITEMS
Parameters:
  - albumId: Filter by album
  - filters: Search filters (date ranges, content categories, media types)
  - orderBy: Sort order
  - pageSize: Results per page
  - pageToken: Pagination token
```

### 6. Add Items to an Album
Use `GOOGLEPHOTOS_BATCH_ADD_MEDIA_ITEMS` to add existing media items to an album.
```
Tool: GOOGLEPHOTOS_BATCH_ADD_MEDIA_ITEMS
Parameters:
  - albumId (required): Target album ID
  - mediaItemIds (required): Array of media item IDs to add
```

## Common Patterns

- **Create album then upload**: Use `GOOGLEPHOTOS_CREATE_ALBUM` to create an album, then `GOOGLEPHOTOS_BATCH_CREATE_MEDIA_ITEMS` with the album ID to upload and organize photos in one step.
- **List then organize**: Use `GOOGLEPHOTOS_SEARCH_MEDIA_ITEMS` or `GOOGLEPHOTOS_LIST_MEDIA_ITEMS` to find media item IDs, then `GOOGLEPHOTOS_BATCH_ADD_MEDIA_ITEMS` to add them to albums.
- **Update album metadata**: Use `GOOGLEPHOTOS_UPDATE_ALBUM` to change an album's title or cover photo.
- **Get album details**: Use `GOOGLEPHOTOS_GET_ALBUM` with an album ID to retrieve full album information.
- **Add enrichments**: Use `GOOGLEPHOTOS_ADD_ENRICHMENT` to add text overlays, locations, or map enrichments to album positions.
- **Upload from URLs**: Use the `url` parameter in `GOOGLEPHOTOS_UPLOAD_MEDIA` or `urls` in `GOOGLEPHOTOS_BATCH_CREATE_MEDIA_ITEMS` to upload images directly from web URLs.

## 已知陷阱

- `GOOGLEPHOTOS_LIST_MEDIA_ITEMS` is **deprecated** -- prefer `GOOGLEPHOTOS_SEARCH_MEDIA_ITEMS` for listing and filtering media.
- `GOOGLEPHOTOS_UPLOAD_MEDIA` supports images up to **200MB** and videos up to a larger limit. Exceeding these will fail.
- Album IDs must be obtained from `GOOGLEPHOTOS_LIST_ALBUMS` or `GOOGLEPHOTOS_CREATE_ALBUM` responses -- they are opaque strings.
- `GOOGLEPHOTOS_BATCH_ADD_MEDIA_ITEMS` can only add items to albums **created by the app** or albums the user owns.
- The `filters` parameter in `GOOGLEPHOTOS_SEARCH_MEDIA_ITEMS` uses a specific Google Photos API filter structure -- consult the schema for date range and content category formats.
- Media items created via the API may not immediately appear in the Google Photos web UI due to processing delays.

## 快速参考
| Action | Tool | Key Parameters |
|--------|------|----------------|
| List albums | `GOOGLEPHOTOS_LIST_ALBUMS` | `pageSize`, `pageToken` |
| Create album | `GOOGLEPHOTOS_CREATE_ALBUM` | `title` |
| Get album | `GOOGLEPHOTOS_GET_ALBUM` | `albumId` |
| Update album | `GOOGLEPHOTOS_UPDATE_ALBUM` | `albumId`, `title`, `coverPhotoMediaItemId` |
| Upload media | `GOOGLEPHOTOS_UPLOAD_MEDIA` | `file_to_upload` or `url`, `description` |
| Batch upload | `GOOGLEPHOTOS_BATCH_CREATE_MEDIA_ITEMS` | `files` or `urls`, `albumId` |
| Search media | `GOOGLEPHOTOS_SEARCH_MEDIA_ITEMS` | `albumId`, `filters`, `pageSize` |
| List media items | `GOOGLEPHOTOS_LIST_MEDIA_ITEMS` | `pageSize`, `pageToken` |
| Add items to album | `GOOGLEPHOTOS_BATCH_ADD_MEDIA_ITEMS` | `albumId`, `mediaItemIds` |
| Add enrichment | `GOOGLEPHOTOS_ADD_ENRICHMENT` | `albumId`, `newEnrichmentItem`, `albumPosition` |

---
*由 [Composio](https://composio.dev) 提供支持*
