---
name: Spotify Automation
description: "通过 Composio 自动化 Spotify 工作流，包括播放列表管理、音乐搜索、播放控制和用户资料访问"
requires:
  mcp:
    - rube
---

# Spotify Automation

自动化 Spotify 操作 —— 管理播放列表、搜索音乐目录、控制播放、浏览专辑和曲目，以及访问用户资料 —— 全部通过 Composio MCP 集成来协调完成。

**工具包文档：** [composio.dev/toolkits/spotify](https://composio.dev/toolkits/spotify)

---

## 设置

1. 通过 `https://rube.app/mcp` 处的 Composio MCP 服务器连接你的 Spotify 账户
2. 如果不存在有效连接，代理会提示你一个身份验证链接
3. 连接成功后，所有 `SPOTIFY_*` 工具即可使用
4. **注意：** 部分功能（播放控制）需要 Spotify Premium 订阅

---

## 核心工作流

### 1. 获取当前用户资料
检索已通过身份验证的 Spotify 用户的完整资料信息。

**工具：** `SPOTIFY_GET_CURRENT_USER_S_PROFILE`

```
无需参数。
返回：显示名称、邮箱、国家、订阅等级（premium/free）、
露骨内容设置、头像、关注者数量，以及 Spotify URI。
所需作用域：user-read-private、user-read-email。
```

---

### 2. 搜索 Spotify 目录
按关键词查找专辑、艺术家、播放列表、曲目、节目、单集或有声书。

**工具：** `SPOTIFY_SEARCH_FOR_ITEM`

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| `q` | string | 是 | 搜索关键词 |
| `type` | array | 是 | 条目类型：`album`、`artist`、`playlist`、`track`、`show`、`episode`、`audiobook` |
| `limit` | integer | 否 | 返回结果数（默认：20） |
| `offset` | integer | 否 | 分页偏移量（默认：0） |
| `market` | string | 否 | ISO 3166-1 alpha-2 国家代码 |
| `include_external` | string | 否 | 设为 `audio` 以包含外部内容 |

**注意：** 有声书仅在美国、英国、加拿大、爱尔兰、新西兰和澳大利亚可用。

---

### 3. 管理播放列表
浏览、创建、修改并填充播放列表。

**获取某用户的播放列表：**

**工具：** `SPOTIFY_GET_USER_S_PLAYLISTS`

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| `user_id` | string | 是 | Spotify 用户 ID |
| `limit` | integer | 否 | 最大播放列表数，1-50（默认：20） |
| `offset` | integer | 否 | 分页偏移量，0-100000（默认：0） |

**获取当前用户的播放列表：**

**工具：** `SPOTIFY_GET_CURRENT_USER_S_PLAYLISTS`

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| `limit` | integer | 否 | 最大播放列表数，1-50（默认：20） |
| `offset` | integer | 否 | 分页偏移量，0-100000（默认：0） |

**获取播放列表详情：**

**工具：** `SPOTIFY_GET_PLAYLIST`

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| `playlist_id` | string | 是 | Spotify 播放列表 ID（例如 `3cEYpjA9oz9GiPac4AsH4n`） |
| `fields` | string | 否 | 逗号分隔的字段过滤器，用于缩减响应大小 |
| `market` | string | 否 | ISO 国家代码，用于按市场获取内容 |
| `additional_types` | string | 否 | `track,episode`，用于包含播客单集 |

**更新播放列表详情：**

**工具：** `SPOTIFY_CHANGE_PLAYLIST_DETAILS`

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| `playlist_id` | string | 是 | 播放列表 ID（必须归当前用户所有） |
| `name` | string | 否 | 新的播放列表名称 |
| `description` | string | 否 | 新的播放列表描述 |
| `public` | boolean | 否 | 公开/私密切换 |
| `collaborative` | boolean | 否 | 协作模式（仅适用于非公开播放列表） |

---

### 4. 浏览播放列表项并添加曲目
查看播放列表中的曲目并添加新项目。

**工具：** `SPOTIFY_GET_PLAYLIST_ITEMS`

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| `playlist_id` | string | 是 | Spotify 播放列表 ID |
| `limit` | integer | 否 | 每页项目数，1-50（默认：20） |
| `offset` | integer | 否 | 分页偏移量（默认：0） |
| `fields` | string | 否 | 字段过滤器（例如 `items(track(name,id))`） |
| `market` | string | 否 | ISO 国家代码 |
| `additional_types` | string | 否 | `track,episode`，用于播客单集 |

**工具：** `SPOTIFY_ADD_ITEMS_TO_PLAYLIST`

使用 Spotify URI 将曲目或单集添加到播放列表。

---

### 5. 获取曲目和专辑详情
检索单个曲目和专辑的目录信息。

**工具：** `SPOTIFY_GET_TRACK` —— 按 Spotify ID 获取单个曲目的详情。

**工具：** `SPOTIFY_GET_ALBUM` —— 获取包含曲目列表、艺术家信息、封面图和热度的完整专辑数据。

---

### 6. 控制播放
在用户的活动设备上开始、恢复或更改播放。

**工具：** `SPOTIFY_START_RESUME_PLAYBACK`

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| `context_uri` | string | 否 | 专辑、艺术家或播放列表的 Spotify URI（不能与 `uris` 同时使用） |
| `uris` | array | 否 | 要播放的曲目 URI 列表（不能与 `context_uri` 同时使用） |
| `offset` | object | 否 | 起始位置：`{position: 5}` 或 `{uri: 'spotify:track:...'}` |
| `position_ms` | integer | 否 | 以毫秒表示的起始位置 |
| `device_id` | string | 否 | 目标设备 ID（默认为活动设备） |

**要求：** Spotify Premium 订阅，以及至少一个活动设备。

---

## 已知陷阱

| 陷阱 | 详情 |
|---------|---------|
| **播放需要 Premium** | 如果用户没有 Spotify Premium，`SPOTIFY_START_RESUME_PLAYBACK` 会返回 403 |
| **需要活动设备** | 如果没有活动的 Spotify 设备（移动端、桌面端、网页端、音箱），播放控制会返回 404 |
| **context_uri 与 uris 互斥** | 同一次播放调用中不能同时使用 `context_uri` 和 `uris` |
| **协作播放列表** | `collaborative` 只能在非公开播放列表上设为 `true`（`public` 必须为 `false`） |
| **播放列表所属权** | `SPOTIFY_CHANGE_PLAYLIST_DETAILS` 仅适用于已通过身份验证的用户所拥有的播放列表 |
| **有声书的市场限制** | 通过搜索获取的有声书仅在美国、英国、加拿大、爱尔兰、新西兰和澳大利亚可用 |
| **最多 11000 个播放列表** | 通过 `SPOTIFY_CREATE_PLAYLIST`，用户最多可创建约 11,000 个播放列表 |

---

## 快速参考

| 工具 Slug | 用途 |
|-----------|------|
| `SPOTIFY_GET_CURRENT_USER_S_PROFILE` | 获取已通过身份验证用户的资料 |
| `SPOTIFY_SEARCH_FOR_ITEM` | 在目录中搜索曲目、专辑、艺术家等 |
| `SPOTIFY_GET_USER_S_PLAYLISTS` | 获取任意用户的播放列表 |
| `SPOTIFY_GET_CURRENT_USER_S_PLAYLISTS` | 获取当前用户的播放列表 |
| `SPOTIFY_GET_PLAYLIST` | 获取详细的播放列表信息 |
| `SPOTIFY_GET_PLAYLIST_ITEMS` | 列出播放列表中的曲目/单集 |
| `SPOTIFY_CHANGE_PLAYLIST_DETAILS` | 更新播放列表名称、描述、可见性 |
| `SPOTIFY_CREATE_PLAYLIST` | 创建新的播放列表 |
| `SPOTIFY_ADD_ITEMS_TO_PLAYLIST` | 向播放列表添加曲目/单集 |
| `SPOTIFY_GET_TRACK` | 按 ID 获取曲目详情 |
| `SPOTIFY_GET_ALBUM` | 按 ID 获取专辑详情 |
| `SPOTIFY_START_RESUME_PLAYBACK` | 在设备上开始或恢复播放 |

---

*由 [Composio](https://composio.dev) 提供支持*
