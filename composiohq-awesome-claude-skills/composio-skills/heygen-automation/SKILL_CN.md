---
name: HeyGen Automation
description: "通过 Composio 在 HeyGen 平台上自动化 AI 视频生成、头像浏览、基于模板的视频创建以及视频状态跟踪"
requires:
  mcp:
    - rube
---

# HeyGen 自动化

自动化 AI 驱动的视频创作工作流——浏览头像和模板、基于模板生成个性化视频、跟踪处理状态并获取可分享的 URL——全部通过 Composio MCP 集成进行编排。

**工具包文档：** [composio.dev/toolkits/heygen](https://composio.dev/toolkits/heygen)

---

## 设置

1. 通过 Composio MCP 服务器 `https://rube.app/mcp` 连接你的 HeyGen 账户
2. 如果不存在有效连接，代理会向你提供一个认证链接
3. 连接后，所有 `HEYGEN_*` 工具即可用于执行

---

## 核心工作流

### 1. 浏览可用模板
从 HeyGen 库中检索预先设计的头像模板，用于视频创建。

**工具：** `HEYGEN_V2_TEMPLATES`

```
No parameters required -- returns template IDs, names, preview images, and customization options.
```

在生成视频之前使用此工具发现模板。每个模板都有生成时所需的唯一 ID。

---

### 2. 查看模板详情与变量
检索模板的完整结构，包括所有变量、场景映射和自定义选项。

**工具：** `HEYGEN_RETRIEVE_TEMPLATE_DETAILS_V3`

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `template_id` | string | 是 | 来自 `HEYGEN_V2_TEMPLATES` 或 HeyGen 控制台的模板 ID |

这是生成视频之前的**必要前置步骤**——它会准确告诉你哪些变量必须填写。

---

### 3. 浏览可用头像
列出所有可用于视频创建的逼真头像，便于将角色映射到场景。

**工具：** `HEYGEN_V2_AVATARS`

```
No parameters required -- returns avatar identifiers, names, and preview images.
The list may be paginated; additional calls might be needed for the full set.
```

---

### 4. 基于模板生成视频
通过向模板填充你的变量和内容来创建自定义视频。

**工具：** `HEYGEN_V2_TEMPLATE_GENERATE`

提供视频标题以及通过 `HEYGEN_RETRIEVE_TEMPLATE_DETAILS_V3` 发现的所有模板变量。每个必填变量都必须以准确的名称和类型提供。

---

### 5. 检查视频处理状态
轮询正在生成的视频的处理状态并检索其元数据。

**工具：** `HEYGEN_RETRIEVE_VIDEO_STATUS_DETAILS`

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `video_id` | string | 是 | 生成 API 返回的视频 ID |

返回的 URL 在 7 天后过期，但可以通过再次调用此端点重新生成。

---

### 6. 获取可分享的视频 URL
生成一个公开的可分享链接，任何人无需认证即可观看该视频。

**工具：** `HEYGEN_RETRIEVE_SHARABLE_VIDEO_URL`

提供 `video_id` 即可获得用于分发的公开 URL。

---

## 已知陷阱

| 陷阱 | 详情 |
|------|------|
| **所有模板变量均为必填** | `HEYGEN_V2_TEMPLATE_GENERATE` 要求提供来自 `HEYGEN_RETRIEVE_TEMPLATE_DETAILS_V3` 的每个变量，且名称和类型必须准确——缺失或命名错误的字段会破坏场景或导致生成失败 |
| **始终先检查模板** | 生成之前切勿跳过 `HEYGEN_RETRIEVE_TEMPLATE_DETAILS_V3`——多场景模板具有复杂的变量结构 |
| **视频 URL 会过期** | 来自 `HEYGEN_RETRIEVE_VIDEO_STATUS_DETAILS` 的 URL 在 7 天后过期；再次调用该端点即可重新生成 |
| **头像列表分页** | `HEYGEN_V2_AVATARS` 可能返回分页结果——可能需要额外调用才能获取完整的库 |
| **处理时间不定** | 视频生成是异步的；在使用输出 URL 之前，请轮询 `HEYGEN_RETRIEVE_VIDEO_STATUS_DETAILS`，直到状态为完成 |

---

## 快速参考

| 工具 Slug | 用途 |
|-----------|------|
| `HEYGEN_V2_TEMPLATES` | 列出可用的视频模板 |
| `HEYGEN_RETRIEVE_TEMPLATE_DETAILS_V3` | 获取模板变量和场景结构 |
| `HEYGEN_V2_AVATARS` | 浏览可用的 AI 头像 |
| `HEYGEN_V2_TEMPLATE_GENERATE` | 基于模板生成视频 |
| `HEYGEN_RETRIEVE_VIDEO_STATUS_DETAILS` | 检查视频处理状态并获取 URL |
| `HEYGEN_RETRIEVE_SHARABLE_VIDEO_URL` | 获取公开的可分享视频链接 |

---

*由 [Composio](https://composio.dev) 提供支持*
