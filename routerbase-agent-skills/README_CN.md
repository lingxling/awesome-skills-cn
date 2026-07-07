# RouterBase Agent Skills 中文学习版

本目录翻译自 [zenlee123/routerbase-agent-skills](https://github.com/zenlee123/routerbase-agent-skills)，用于学习如何把 AI 应用接入 [routerbase](https://routerbase.com/)：通过一个 OpenAI 兼容入口完成模型路由、API 迁移和多媒体生成调用。

## 技能列表

- [routerbase-api-integration](skills/routerbase-api-integration/SKILL_CN.md) - RouterBase API 集成与 OpenAI 兼容迁移
- [routerbase-model-routing](skills/routerbase-model-routing/SKILL_CN.md) - 模型选择、路由策略与 fallback 设计
- [routerbase-media-generation](skills/routerbase-media-generation/SKILL_CN.md) - 图片、视频和音频生成工作流

## 学习重点

- 将 OpenAI SDK 的 base URL 切换为 `https://routerbase.com/v1`
- 用服务端环境变量或密钥管理系统保存 RouterBase API key
- 按任务类型选择模型：对话、视觉、图片、视频、音频、embedding
- 设计主模型和备用模型，避免把价格、模型列表和能力假设写死
- 区分同步图片生成和异步视频/音频任务，并保留轮询、回调和结果持久化步骤

## 原始仓库

- GitHub: [zenlee123/routerbase-agent-skills](https://github.com/zenlee123/routerbase-agent-skills)
- RouterBase: [routerbase](https://routerbase.com/)
