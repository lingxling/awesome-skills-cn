---
name: googleslides-automation
description: "通过 Rube MCP（Composio）自动化 Google Slides 任务：创建演示文稿、从 Markdown 添加幻灯片、批量更新、从模板复制、获取缩略图。请始终先搜索工具以获取最新模式。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 实现 Google Slides 自动化

使用 Rube MCP（Composio）以编程方式创建、编辑和管理 Google Slides 演示文稿。

**工具包文档**：[composio.dev/toolkits/googleslides](https://composio.dev/toolkits/googleslides)

## 前置条件
- 必须已连接 Rube MCP（`RUBE_SEARCH_TOOLS` 可用）
- 已通过 `RUBE_MANAGE_CONNECTIONS` 为工具包 `googleslides` 建立活动连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 以获取当前工具模式

## 设置
**获取 Rube MCP**：在你的客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——只需添加该端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 是否可用
2. 对工具包 `googleslides` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接未处于 ACTIVE 状态，请按返回的授权链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 创建空白演示文稿
使用 `GOOGLESLIDES_PRESENTATIONS_CREATE` 初始化一个新的空白演示文稿。
```
Tool: GOOGLESLIDES_PRESENTATIONS_CREATE
Parameters:
  - title（必填）: 新演示文稿的标题
  - presentationId（可选）: 要指定的特定 ID（通常自动生成）
```

### 2. 从 Markdown 创建幻灯片
使用 `GOOGLESLIDES_CREATE_SLIDES_MARKDOWN` 从 Markdown 文本生成完整的演示文稿。内容会自动拆分为多张幻灯片。
```
Tool: GOOGLESLIDES_CREATE_SLIDES_MARKDOWN
Parameters:
  - title（必填）: 演示文稿标题
  - markdown_text（必填）: Markdown 内容（自动拆分为幻灯片）
```

### 3. 批量更新演示文稿
使用 `GOOGLESLIDES_PRESENTATIONS_BATCH_UPDATE`，通过 Markdown 或原始 API 请求对现有演示文稿应用更新。
```
Tool: GOOGLESLIDES_PRESENTATIONS_BATCH_UPDATE
Parameters:
  - presentationId（必填）: 目标演示文稿 ID
  - markdown_text: 用于更新幻灯片的 Markdown 内容
  - requests: 原始 Google Slides API 批量更新请求
  - writeControl: 写入控制设置
```

### 4. 从模板复制
使用 `GOOGLESLIDES_PRESENTATIONS_COPY_FROM_TEMPLATE` 将现有演示文稿复制为模板。
```
Tool: GOOGLESLIDES_PRESENTATIONS_COPY_FROM_TEMPLATE
Parameters:
  - template_presentation_id（必填）: 源模板演示文稿 ID
  - new_title（必填）: 新副本的标题
  - parent_folder_id（可选）: 用于存放副本的 Google Drive 文件夹
```

### 5. 获取演示文稿详情
使用 `GOOGLESLIDES_PRESENTATIONS_GET` 检索某演示文稿的当前状态，包括所有幻灯片和元素。
```
Tool: GOOGLESLIDES_PRESENTATIONS_GET
Parameters:
  - presentationId（必填）: 要检索的演示文稿 ID
  - fields（可选）: 要返回的特定字段
```

### 6. 生成幻灯片缩略图
使用 `GOOGLESLIDES_PRESENTATIONS_PAGES_GET_THUMBNAIL` 为特定幻灯片生成缩略图图像 URL。
```
Tool: GOOGLESLIDES_PRESENTATIONS_PAGES_GET_THUMBNAIL
Parameters:
  - presentationId（必填）: 演示文稿 ID
  - pageObjectId（必填）: 页面/幻灯片对象 ID
  - thumbnailProperties.mimeType: 图像格式（例如 PNG）
  - thumbnailProperties.thumbnailSize: 缩略图大小
```

## 常见模式

- **以 Markdown 为先的工作流**：使用 `GOOGLESLIDES_CREATE_SLIDES_MARKDOWN` 从结构化文本快速生成演示文稿。该工具会自动将内容拆分为多张幻灯片。
- **基于模板的生成**：使用 `GOOGLESLIDES_PRESENTATIONS_COPY_FROM_TEMPLATE` 复制一个带样式的模板，然后使用 `GOOGLESLIDES_PRESENTATIONS_BATCH_UPDATE` 填充内容。
- **先检索再修改**：使用 `GOOGLESLIDES_PRESENTATIONS_GET` 检查幻灯片结构和对象 ID，然后使用 `GOOGLESLIDES_PRESENTATIONS_BATCH_UPDATE` 进行有针对性的修改。
- **导出缩略图**：使用 `GOOGLESLIDES_PRESENTATIONS_PAGES_GET` 列出页面对象 ID，然后使用 `GOOGLESLIDES_PRESENTATIONS_PAGES_GET_THUMBNAIL` 生成预览图像。
- **分享演示文稿**：创建完成后，结合 `GOOGLEDRIVE_ADD_FILE_SHARING_PREFERENCE`（googledrive 工具包）进行分享。

## 已知坑点

- `GOOGLESLIDES_CREATE_SLIDES_MARKDOWN` 每次都会创建一个全新的演示文稿——它不能追加到现有的演示文稿中。
- 使用原始 `requests` 的 `GOOGLESLIDES_PRESENTATIONS_BATCH_UPDATE` 需要了解 Google Slides API 的请求格式。对于更简单的更新，优先使用 `markdown_text`。
- 页面对象 ID 必须先通过 `GOOGLESLIDES_PRESENTATIONS_GET` 获取，然后才能使用缩略图或页面获取工具。
- `presentationId` 是 Google Slides URL 中那段较长的字母数字字符串（位于 `/d/` 和 `/edit` 之间）。
- 从模板复制要求经过身份验证的用户至少对该模板演示文稿拥有读取权限。

## 快速参考
| 操作 | 工具 | 关键参数 |
|--------|------|----------------|
| 创建空白演示文稿 | `GOOGLESLIDES_PRESENTATIONS_CREATE` | `title` |
| 从 Markdown 创建 | `GOOGLESLIDES_CREATE_SLIDES_MARKDOWN` | `title`、`markdown_text` |
| 批量更新幻灯片 | `GOOGLESLIDES_PRESENTATIONS_BATCH_UPDATE` | `presentationId`、`markdown_text` 或 `requests` |
| 从模板复制 | `GOOGLESLIDES_PRESENTATIONS_COPY_FROM_TEMPLATE` | `template_presentation_id`、`new_title` |
| 获取演示文稿 | `GOOGLESLIDES_PRESENTATIONS_GET` | `presentationId` |
| 获取页面详情 | `GOOGLESLIDES_PRESENTATIONS_PAGES_GET` | `presentationId`、`pageObjectId` |
| 获取幻灯片缩略图 | `GOOGLESLIDES_PRESENTATIONS_PAGES_GET_THUMBNAIL` | `presentationId`、`pageObjectId` |

---
*Powered by [Composio](https://composio.dev)*
