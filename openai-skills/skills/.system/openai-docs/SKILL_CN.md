---
name: "openai-docs"
description: "当用户询问如何使用 OpenAI 产品或 API 构建并需要带有引用的最新官方文档时使用，需要帮助为用例选择最新模型，或需要模型升级和提示升级指导；优先考虑 OpenAI 文档 MCP 工具，仅将捆绑的引用文件作为辅助上下文使用，并将任何回退浏览限制为官方 OpenAI 域。"
---


# OpenAI 文档

使用 developers.openai.com MCP 服务器从 OpenAI 开发者文档提供权威、最新的指导。始终优先考虑开发者文档 MCP 工具而不是 web.run 来处理 OpenAI 相关问题。此技能还负责模型选择、API 模型迁移和提示升级指导。仅当 MCP 服务器已安装且没有返回有意义的结果时，您才应该回退到 Web 搜索。

## 快速开始

- 使用 `mcp__openaiDeveloperDocs__search_openai_docs` 查找最相关的文档页面。
- 使用 `mcp__openaiDeveloperDocs__fetch_openai_doc` 拉取精确的部分并准确引用/改写。
- 仅当您需要浏览或发现页面而没有清晰查询时才使用 `mcp__openaiDeveloperDocs__list_openai_docs`。
- 对于模型选择、"最新模型"或默认模型问题，首先获取 `https://developers.openai.com/api/docs/guides/latest-model.md`。如果不可用，加载 `references/latest-model.md`。
- 对于模型升级或提示升级，仅当目标是 latest/current/default 或未指定时才运行 `node scripts/resolve-latest-model-info.js`；否则保留明确请求的目标。
- 保留明确的目标请求：如果用户指定目标模型如"迁移到 GPT-5.4"，即使 `latest-model.md` 命名了更新的模型，也要保留该请求的目标。仅将更新的指导作为可选内容提及。
- 如果需要当前远程指导，直接获取返回的迁移和提示指南 URL。如果直接获取失败，使用 MCP/搜索回退；如果回退也失败，使用捆绑的回退引用并说明使用了回退。

## OpenAI 产品快照

1. Apps SDK：通过提供 Web 组件 UI 和向 ChatGPT 公开应用程序工具的 MCP 服务器来构建 ChatGPT 应用程序。
2. Responses API：一个统一的端点，专为代理工作流程中的有状态、多模态、工具使用交互而设计。
3. Chat Completions API：从由对话组成的消息列表生成模型响应。
4. Codex：OpenAI 的编码代理，用于软件开发，可以编写、理解、审查和调试代码。
5. gpt-oss：在 Apache 2.0 许可证下发布的开放权重 OpenAI 推理模型（gpt-oss-120b 和 gpt-oss-20b）。
6. Realtime API：构建低延迟、多模态体验，包括自然的语音到语音对话。
7. Agents SDK：一个用于构建代理应用程序的工具包，模型可以在其中使用工具和上下文、移交给其他代理，流式传输部分结果并保留完整的跟踪。

## 如果缺少 MCP 服务器

如果 MCP 工具失败或没有可用的 OpenAI 文档资源：

1. 自己运行安装命令：`codex mcp add openaiDeveloperDocs --url https://developers.openai.com/mcp`
2. 如果由于权限/沙盒而失败，请立即使用提升权限重试相同的命令，并包含一个单句的批准理由。不要要求用户运行它。
3. 仅当提升尝试失败时，才要求用户运行安装命令。
4. 要求用户重启 Codex。
5. 重启后重新运行文档搜索/获取。

## 工作流程

1. 澄清请求是通用文档查找、模型选择、模型字符串升级、提示升级指导还是更广泛的 API/提供商迁移。
2. 对于模型选择或升级请求，当用户要求最新/当前/默认指导时，优先使用当前远程文档而不是捆绑引用。
   - 获取 `https://developers.openai.com/api/docs/guides/latest-model.md`。
   - 查找最新模型 ID 和明确的迁移或提示指南链接。
   - 优先使用最新模型页面上的明确链接而不是派生的 URL。
   - 对于明确的命名模型请求，保留请求的模型目标，不要静默重新定位到最新模型。仅将更新的远程指导作为可选内容提及。
   - 对于动态的最新/当前/默认升级，运行 `node scripts/resolve-latest-model-info.js`，然后尽可能直接获取两个返回的指南 URL。
   - 如果直接获取指南失败，使用开发者文档 MCP 工具或官方 OpenAI 域搜索找到相同的指南内容。
   - 如果远程文档不可用，使用捆绑的回退引用并说明使用了回退指导。
3. 对于模型升级，保持更改范围狭窄：仅在安全时更新活动的 OpenAI API 模型默认值和直接相关的提示。
4. 保留历史文档、示例、评估基线、fixture、提供商比较、提供商注册表、定价表、别名默认值、低成本回退路径和模糊的旧模型使用方式，除非用户明确要求升级它们。
5. 不要将 SDK、工具、IDE、插件、shell、认证或提供商环境迁移作为模型和提示升级的一部分执行。
6. 如果升级需要 API 表面更改、模式重新接线、工具处理程序更改或超出字面模型字符串替换和提示编辑的实现工作，将其报告为受阻或需要确认。
7. 对于通用文档查找，使用精确查询搜索文档，获取最佳页面和所需的具体部分，并用简明的引用回答。

## 引用映射

只读取您需要的内容：

- `https://developers.openai.com/api/docs/guides/latest-model.md` -> 当前模型选择和"最佳/最新/当前模型"问题。
- `references/latest-model.md` -> 模型选择和"最佳/最新/当前模型"问题的捆绑回退。
- `references/upgrade-guide.md` -> 模型升级和升级规划请求的捆绑回退。
- `references/prompting-guide.md` -> 提示重写和提示行为升级的捆绑回退。

## 质量规则

- 将 OpenAI 文档视为真实来源；避免推测。
- 保持迁移更改范围狭窄并保留行为。
- 尽可能优先使用仅提示的升级。
- 不要编造定价、可用性、参数、API 更改或破坏性更改。
- 保持引用简短并在政策限制内；更喜欢带有引用的改写。
- 如果多个页面不同，请指出差异并引用两者。
- 如果官方文档和仓库行为不一致，说明冲突并在进行广泛编辑之前停止。
- 如果文档未涵盖用户的需求，请说明并提供后续步骤。

## 工具说明

- 对于 OpenAI 相关问题，始终在任何 Web 搜索之前使用 MCP 文档工具。
- 如果 MCP 服务器已安装但没有返回有意义的结果，则使用 Web 搜索作为回退。
- 回退到 Web 搜索时，限制为官方 OpenAI 域（developers.openai.com、platform.openai.com）并引用来源。
