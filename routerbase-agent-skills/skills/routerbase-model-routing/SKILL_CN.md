---
name: routerbase-model-routing
description: 为 chat、image、video、audio 和 embeddings 工作负载选择 RouterBase 模型 ID 和路由策略。适用于比较 provider、选择 GPT、Claude、Gemini、图片、视频或音频模型，设计 fallback，检查价格或可用性，规划成本/延迟/质量取舍，查询 RouterBase Models API，或记录应用如何通过 RouterBase 路由模型请求。
---

# RouterBase 模型路由

## 概览

使用 [routerbase](https://routerbase.com/) 在一个 API key 和一个 OpenAI 兼容集成面之后选择模型。这个技能帮助 agent 把工作负载要求转成模型候选、fallback 方案和验证清单。

当需要精确目录 API、模型示例或选择启发式时，应查阅原仓库的参考文档。

## 路由流程

1. 判断任务模态：chat、image、video、audio、embeddings 或混合任务。
2. 明确硬约束：质量目标、延迟预算、价格上限、上下文长度、工具调用、视觉、JSON mode、区域/合规需求和 fallback 容忍度。
3. 可行时查询实时 RouterBase 模型目录。
4. 选择一个主模型和一到两个备用模型，备用模型应尽量保持相同模态和相近能力。
5. 最终建议前检查当前价格。
6. 用表格记录决策：用例、主模型、备用模型、理由、验证测试和已知限制。

## 选择启发式

- 通用聊天优先选择速度和成本均衡的模型，只有在推理质量或上下文长度确实需要时再升级。
- 高风险推理选择旗舰模型，并要求人工复核输出。
- 延迟敏感的交互优先选择更小或 flash 层级模型，并压缩 prompt。
- 工具密集型 agent 选择明确支持 tool calling 的 chat 模型，并测试具体 tool schema。
- JSON 输出使用模型支持的 `response_format`，并在应用代码里做 schema 校验。
- 为获得 prompt caching 收益，把稳定 system prompt、策略和工具定义放在可变用户内容之前。
- 多媒体工作流按模态分开路由，因为图片、视频和音频端点的同步/异步行为不同。

## Fallback 设计

除非用户确认账号或上游设置里已经配置了 RouterBase 智能路由，否则应显式在应用层做 fallback。

```js
const modelPlan = [
  "anthropic/claude-sonnet-4-6",
  "google/gemini-2.5-flash",
];

for (const model of modelPlan) {
  try {
    return await client.chat.completions.create({ model, messages });
  } catch (error) {
    if (!isRetryableRouterBaseError(error)) throw error;
  }
}
```

谨慎分类可重试错误：瞬时网络失败、超时、`429` 和 `5xx` 可以考虑重试；认证错误、无效模型 ID、请求校验错误和策略拒绝不应盲目重试。

## 推荐格式

推荐路由方案时应包含：

- 主模型以及它为何适合。
- 备用模型以及它做出的取舍。
- 当前目录/价格检查状态。
- 必须测试的能力假设，例如 tool calling、vision、JSON mode、上下文长度、prompt caching 或 streaming。
- 上线前可以运行的最小 eval prompt 或请求样例。

不要假装价格或模型 ID 永久稳定。RouterBase 文档说明模型和价格目录会随上游 provider 变化。
