---
name: routerbase-api-integration
description: 将应用接入 RouterBase 的 OpenAI 兼容模型网关。适用于迁移 OpenAI SDK 调用、配置 RouterBase API key、实现 chat completions、流式输出、工具调用、JSON mode、视觉输入、错误处理，或为 Python、JavaScript、curl、LangChain、LlamaIndex、Vercel AI SDK、Cursor、Continue 等 OpenAI 兼容客户端编写 RouterBase 设置文档。
---

# RouterBase API 集成

## 概览

使用 [routerbase](https://routerbase.com/) 作为 GPT、Claude、Gemini 等模型的 OpenAI 兼容网关。这个技能帮助 agent 迁移现有 OpenAI 兼容代码，保护 API key，并产出简洁、可测试的 RouterBase 集成示例。

当需要精确端点、请求头或完整示例时，应查阅原仓库的参考文档。

## 集成流程

1. 先判断用户是在做迁移、新集成、调试还是写文档。
2. 不要把凭据放在浏览器端或移动端代码里，优先使用服务端环境配置或密钥管理系统。
3. 尽量复用用户已有的 OpenAI 兼容客户端，把 base URL 改为 `https://routerbase.com/v1`，再替换 `model`。
4. 默认保留标准 OpenAI 请求结构，除非 RouterBase 文档或具体模型要求额外字段。
5. 如果有 API key，可以查询实时模型目录；否则只把文档中的模型 ID 当作起点，并提醒用户上线前确认可用性。
6. 增加最小 smoke test，但只有在用户明确期望并提供凭据时才执行真实调用。

## 常见模式

### Python

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["ROUTERBASE_API_KEY"],
    base_url="https://routerbase.com/v1",
)

response = client.chat.completions.create(
    model="google/gemini-2.5-flash",
    messages=[{"role": "user", "content": "用一句话解释模型路由。"}],
)

print(response.choices[0].message.content)
```

### JavaScript

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.ROUTERBASE_API_KEY,
  baseURL: "https://routerbase.com/v1",
});

const response = await client.chat.completions.create({
  model: "google/gemini-2.5-flash",
  messages: [{ role: "user", content: "用一句话解释模型路由。" }],
});

console.log(response.choices[0].message.content);
```

### curl

```bash
curl -X POST https://routerbase.com/v1/chat/completions \
  -H "Authorization: Bearer $ROUTERBASE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/gemini-2.5-flash",
    "messages": [{"role": "user", "content": "2+2 等于多少？"}]
  }'
```

## 实施护栏

- 不要粘贴、记录或提交真实 API key。
- 不要把 RouterBase key 放进浏览器、移动端或公开仓库。
- 除非用户要求框架适配层，否则保持 OpenAI 兼容写法。
- 流式输出使用 `stream: true` 并处理 SDK stream chunk 或 SSE。
- 工具调用和 JSON mode 继续使用标准 OpenAI 字段 `tools` 和 `response_format`。
- 多模态 chat 使用 OpenAI content parts，例如 `text` 和 `image_url`。
- 调用失败时先检查 headers、model ID、endpoint path、rate limit 和账号权限，再改应用逻辑。

## 输出检查清单

- 写清楚 base URL 的变化。
- 写清楚 `ROUTERBASE_API_KEY` 应配置在哪里。
- 提供一个最小请求示例。
- 提醒模型 ID 和价格要以实时目录为准。
- 提供测试命令或 dry-run 验证路径。
