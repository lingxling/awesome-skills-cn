---
name: Cloudinary Automation
description: "通过自然语言命令自动化 Cloudinary 媒体管理，包括文件夹整理、上传预设、资源查找、转换以及用量监控"
requires:
  mcp:
    - rube
---

# Cloudinary Automation

自动化 Cloudinary 媒体管理工作流 —— 创建文件夹、配置上传预设、查找资源、管理转换、搜索文件夹，以及监控用量 —— 全部通过自然语言完成。

**工具包文档：** [composio.dev/toolkits/cloudinary](https://composio.dev/toolkits/cloudinary)

---

## 设置

1. 将 Rube MCP 服务器添加到你的环境中：`https://rube.app/mcp`
2. 按提示连接你的 Cloudinary 账户（通过 Composio 进行 API 密钥认证）
3. 开始使用自然语言命令进行 Cloudinary 自动化操作

---

## 核心工作流

### 1. 使用文件夹整理资源

创建文件夹结构以整理托管的图片、视频和原始文件。

**工具：** `CLOUDINARY_CREATE_FOLDER`

关键参数：
- `folder` —— 新资源文件夹的完整路径（必填），例如 `images/events/2023`

辅助工具：
- `CLOUDINARY_SEARCH_FOLDERS` —— 使用类似 Lucene 的表达式按名称、路径或创建日期搜索文件夹
  - `expression` —— 搜索过滤条件（例如 `name:sample AND path:events`）
  - `max_results` —— 1-500 条结果（默认 50）
  - `sort_by` —— 排序对象列表（例如 `[{"created_at": "desc"}]`）
  - `next_cursor` —— 分页游标
- `CLOUDINARY_GET_RESOURCES_BY_ASSET_FOLDER` —— 列出指定文件夹内的资源

示例提示：
> "在 Cloudinary 中创建一个名为 'marketing/campaigns/spring-2026' 的文件夹"

---

### 2. 配置上传预设

定义集中式上传行为，包括目标文件夹、允许的格式、转换、标签以及覆盖规则。

**工具：** `CLOUDINARY_CREATE_UPLOAD_PRESET`

关键参数：
- `name` —— 预设名称（若省略则自动生成）
- `folder` —— 上传的目标文件夹路径（例如 `samples/`）
- `allowed_formats` —— 以逗号分隔的格式列表（例如 `jpg,png,webp`）
- `tags` —— 以逗号分隔的要应用的标签（例如 `marketing,thumbnail`）
- `transformation` —— 传入时的转换（例如 `c_limit,w_500`）
- `eager` —— 上传时要预先生成的转换（例如 `c_fill,g_face,h_150,w_150`）
- `unsigned` —— 是否允许未签名上传（`true`/`false`）
- `overwrite` —— 以相同 public_id 覆盖已有资源（当 `unsigned=true` 时不能为 `true`）
- `resource_type` —— `image`、`video` 或 `raw`（默认 `image`）
- `unique_filename` —— 追加随机后缀以避免冲突（默认 `true`）
- `use_filename` —— 使用原始文件名（默认 `false`）
- `moderation` —— 审核类型：`manual`、`webpurify`、`aws_rek` 等
- `auto_tagging` —— AI 自动打标签的置信度阈值 0.0-1.0
- `notification_url` —— 上传通知的 webhook URL

示例提示：
> "创建一个名为 'product-images' 的上传预设，仅允许 JPG 和 PNG，存储在 'products/' 文件夹中，并以 0.7 的置信度自动打标签"

---

### 3. 查找资源详情

按 public ID 检索特定资源的完整详情，包括元数据、派生资源以及相关资源。

**工具：** `CLOUDINARY_GET_RESOURCE_BY_PUBLIC_ID`

关键参数：
- `public_id` —— 资源的 public ID（必填）
- `resource_type` —— `image`、`video` 或 `raw`（必填）
- `type` —— 交付类型：`upload`、`private`、`authenticated`、`fetch` 等（必填）
- `colors` —— 包含颜色直方图和主要颜色
- `faces` —— 包含检测到的面部坐标
- `media_metadata` —— 包含 IPTC、XMP 及详细元数据
- `quality_analysis` —— 包含质量分析分数
- `phash` —— 包含用于相似度检测的感知哈希
- `versions` —— 包含已备份的版本
- `related` —— 包含相关资源
- `max_results` —— 返回的派生/相关资源最大数量（1-500）

示例提示：
> "获取图片 'products/hero-banner' 的完整详情，包括颜色分析和质量分数"

---

### 4. 管理转换和派生资源

列出现有转换，对已上传的资源应用预生成转换，并清理派生资源。

**工具：**
- `CLOUDINARY_GET_TRANSFORMATIONS` —— 列出所有具名和匿名转换
  - `max_results` —— 1-500（默认 10）
  - `next_cursor` —— 分页游标
- `CLOUDINARY_EXPLICIT_RESOURCE` —— 更新现有资源：预生成转换、更新元数据、移动到新文件夹，或修改标签
  - `public_id` —— 目标资源（必填）
  - `eager` —— 要预生成的转换字符串列表（例如 `["c_fill,w_300,h_200", "c_thumb,w_100,h_100,g_face"]`）
  - `eager_async` —— 异步生成转换
  - `tags` —— 替换现有标签
  - `asset_folder` —— 将资源移动到新文件夹
  - `display_name` —— 设置显示名称
  - `context` —— 键值元数据（例如 `{"alt": "Mountain view"}`）
  - `invalidate` —— 使 CDN 缓存失效（最多需要 1 小时生效）
- `CLOUDINARY_DELETE_DERIVED_RESOURCES` —— 按 ID 删除指定的派生资源（每次调用最多 100 个）

示例提示：
> "为资源 'products/hero-banner' 预生成一个 300x200 的填充裁剪和一个 100x100 的人脸检测缩略图"

---

### 5. 监控用量和配置

检查账户级别的用量限制、环境配置以及标签清单。

**工具：**
- `CLOUDINARY_GET_USAGE` —— 监控存储、带宽、请求以及配额限制
- `CLOUDINARY_GET_CONFIG` —— 获取环境配置详情
  - `settings` —— 设为 `true` 以包含如 `folder_mode` 等配置设置
- `CLOUDINARY_GET_TAGS` —— 列出某资源类型的所有标签

示例提示：
> "显示我的 Cloudinary 账户用量和剩余配额"

---

### 6. 设置 Webhook 触发器

为特定 Cloudinary 事件创建 webhook 通知。

**工具：** `CLOUDINARY_CREATE_TRIGGER`

用于在上传完成、转换完成或其他事件发生时接收回调。

示例提示：
> "创建一个在上传事件发生时通知 https://my-app.com/hook 的 webhook 触发器"

---

## 已知问题

| 问题 | 详情 |
|---------|---------|
| 文件夹创建幂等性 | 如果路径已存在，`CLOUDINARY_CREATE_FOLDER` 可能会报错或无操作 —— 请设计幂等的文件夹命名方式 |
| 预设与上传的一致性 | 上传预设中的 `allowed_formats`、`folder` 和 `unsigned` 等选项必须与实际上传方式匹配，否则上传会被拒绝 |
| 严格的资源查找 | 若 `resource_type`、`type` 或 `public_id` 中任一项不正确，即使资源存在，`CLOUDINARY_GET_RESOURCE_BY_PUBLIC_ID` 也会失败 |
| 文件夹路径的敏感性 | `CLOUDINARY_GET_RESOURCES_BY_ASSET_FOLDER` 仅列出指定确切文件夹中的资源；拼写错误会返回空结果 |
| 配额阻塞 | `CLOUDINARY_GET_USAGE` 反映账户级别的限制 —— 达到上限会在检查和处理用量之前静默阻塞上传 |
| CDN 失效延迟 | 在 `CLOUDINARY_EXPLICIT_RESOURCE` 上设置 `invalidate=true` 最多需要 1 小时才能生效传播 |
| 未签名与覆盖的冲突 | 在上传预设中，当 `unsigned=true` 时不能设置 `overwrite=true` |

---

## 快速参考

| 操作 | 工具 Slug | 关键参数 |
|--------|-----------|------------|
| 创建文件夹 | `CLOUDINARY_CREATE_FOLDER` | `folder` |
| 搜索文件夹 | `CLOUDINARY_SEARCH_FOLDERS` | `expression`, `max_results` |
| 列出文件夹资源 | `CLOUDINARY_GET_RESOURCES_BY_ASSET_FOLDER` | 文件夹路径 |
| 创建上传预设 | `CLOUDINARY_CREATE_UPLOAD_PRESET` | `name`, `folder`, `allowed_formats`, `tags` |
| 获取资源详情 | `CLOUDINARY_GET_RESOURCE_BY_PUBLIC_ID` | `public_id`, `resource_type`, `type` |
| 列出转换 | `CLOUDINARY_GET_TRANSFORMATIONS` | `max_results`, `next_cursor` |
| 更新/转换资源 | `CLOUDINARY_EXPLICIT_RESOURCE` | `public_id`, `eager`, `tags` |
| 删除派生资源 | `CLOUDINARY_DELETE_DERIVED_RESOURCES` | `derived_resource_ids` |
| 获取用量 | `CLOUDINARY_GET_USAGE` | （无） |
| 获取配置 | `CLOUDINARY_GET_CONFIG` | `settings` |
| 列出标签 | `CLOUDINARY_GET_TAGS` | resource_type |
| 创建 webhook | `CLOUDINARY_CREATE_TRIGGER` | 事件类型、URL |

---

*由 [Composio](https://composio.dev) 提供支持*
