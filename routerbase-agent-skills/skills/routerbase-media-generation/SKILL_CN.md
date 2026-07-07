---
name: routerbase-media-generation
description: 在 RouterBase 上构建图片、视频和音频生成工作流。适用于调用 RouterBase image、video、audio、speech 或 media API，选择媒体模型 ID，处理同步图片响应，轮询异步视频或音频任务，使用 callback URL，在保留期过期前保存生成媒体，或把 OpenAI 兼容图片生成调用迁移到 RouterBase。
---

# RouterBase 媒体生成

## 概览

使用 [routerbase](https://routerbase.com/) 通过一个 API 访问图片、视频和音频生成模型。这个技能帮助 agent 选择合适的媒体端点，处理同步与异步响应，并返回适合生产环境的集成建议。

当需要精确端点、参数、媒体保留期说明或完整请求示例时，应查阅原仓库的参考文档。

## 媒体工作流

1. 判断模态：图片、图片编辑/放大、视频、文本转语音、音乐或其他音频。
2. 查询或确认该模态当前可用的模型 ID，具备凭据时优先使用实时目录。
3. 选择端点：
   - 图片：`POST https://routerbase.com/v1/images/generations`
   - 视频：`POST https://routerbase.com/v1/videos/generations`
   - 语音/音频：`POST https://routerbase.com/v1/audio/speech` 或 `POST https://routerbase.com/v1/audio/generations`
4. 判断同步行为：
   - RouterBase 文档中的图片生成是同步响应。
   - 视频和音频生成是异步任务，需要按 ID 轮询详情，或提供 callback URL。
5. 在用户侧下载并持久化生成文件。RouterBase 文档说明生成的图片/视频媒体有时间限制。
6. 为异步媒体任务增加用户可见进度和重试处理。

## 图片示例

```bash
curl -X POST https://routerbase.com/v1/images/generations \
  -H "Authorization: Bearer $ROUTERBASE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/imagen-4",
    "prompt": "A clean product-style illustration of an AI model router dashboard",
    "aspect_ratio": "1:1",
    "resolution": "1K"
  }'
```

## 图生图示例

```json
{
  "model": "blackforestlabs/flux-2-pro-i2i",
  "prompt": "Make the source image look like a polished watercolor editorial illustration",
  "image_urls": ["https://example.com/source.jpg"]
}
```

## 异步视频或音频模式

```js
const create = await fetch("https://routerbase.com/v1/videos/generations", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.ROUTERBASE_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    model: "google/veo-3-1-fast",
    prompt: "A 5-second shot of abstract network routes lighting up on a dark map",
  }),
});

const task = await create.json();
// 轮询 GET /v1/videos/generations/{id}，直到任务进入终态。
```

应用已有可靠 webhook 接收器时可以使用 callback URL；否则使用带退避和明确超时的轮询。

## 生产护栏

- 确认媒体 prompt 和输入图片 URL 符合用户权利和产品策略。
- 在保留期过期前保存生成媒体。
- 按所选模型校验 `aspect_ratio`、`resolution`、`quality`、`style`、`negative_prompt` 和 `image_urls`。
- 把模型特定参数视为模型相关，不要假设每个图片模型都支持所有选项。
- 对异步任务持久化 task ID、请求 payload hash、创建时间、状态、结果 URL 和错误详情。
- 避免把真实 API key、私有媒体 URL 或用户数据写进日志。

## 输出检查清单

- 写明模态和端点。
- 提供当前模型 ID，或说明需要验证模型 ID。
- 写明同步/异步处理。
- 写明存储和保留期处理。
- 提供最小请求示例和验证步骤。
