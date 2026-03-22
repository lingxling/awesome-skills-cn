---
name: "openai-docs"
description: "当用户询问如何使用 OpenAI 产品或 API 构建并需要带有引用的最新官方文档时使用（例如：Codex、Responses API、Chat Completions、Apps SDK、Agents SDK、Realtime、模型功能或限制），需要帮助为用例选择最新模型，或需要明确的 GPT-5.4 升级和提示升级指导；优先考虑 OpenAI 文档 MCP 工具，仅将捆绑的引用文件作为辅助上下文使用，并将任何回退浏览限制为官方 OpenAI 域。"
---


# OpenAI 文档

使用 developers.openai.com MCP 服务器从 OpenAI 开发者文档提供权威、最新的指导。始终优先考虑开发人员文档 MCP 工具而不是 web.run。此技能还可以从 `references/` 加载针对模型选择和 GPT-5.4 特定请求的文件，但当前 OpenAI 文档仍然是权威的。仅当 MCP 服务器已安装且没有返回有意义的结果时，您才应该回退到 Web 搜索。

## 快速开始

- 使用 `mcp__openaiDeveloperDocs__search_openai_docs` 查找最相关的文档页面。
- 使用 `mcp__openaiDeveloperDocs__fetch_openai_doc` 拉取精确的部分并准确引用/改写。
- 仅当您需要浏览或发现页面而没有清晰查询时才使用 `mcp__openaiDeveloperDocs__list_openai_docs`。
- 仅当问题是关于模型选择或 GPT-5.4 升级时，从 `references/` 加载相关文件。

## OpenAI 产品快照

1. Apps SDK：通过提供 Web 组件 UI 和向 ChatGPT 公开应用程序工具的 MCP 服务器来构建 ChatGPT 应用程序。
2. Responses API：一个统一的端点，专为代理工作流程中的有状态、多模态、工具使用交互而设计。
3. Chat Completions API：从由对话组成的消息列表生成模型响应。
4. Codex：OpenAI 的编码代理，用于软件开发，可以编写、理解、审查和调试代码。
5. gpt-oss：在 Apache 2.0 许可证下发布的开放权重 OpenAI 推理模型（gpt-oss-120b 和 gpt-oss-20b）。
6. Realtime API：构建低延迟、多模态体验，包括自然的语音到语音对话。
7. Agents SDK：一个用于构建代理应用程序的工具包，模型可以在其中使用工具和上下文、移交给其他代理、流式传输部分结果并保留完整的跟踪。

## 如果缺少 MCP 服务器

如果 MCP 工具失败或没有可用的 OpenAI 文档资源：

1. 自己运行安装命令：`codex mcp add openaiDeveloperDocs --url https://developers.openai.com/mcp`
2. 如果由于权限/沙盒而失败，请立即使用提升权限重试相同的命令，并包含一个单句的批准理由。不要要求用户运行它。
3. 仅当提升尝试失败时，才要求用户运行安装命令。
4. 要求用户重启 Codex。
5. 重启后重新运行文档搜索/获取。

## 工作流程

1. 澄清产品范围以及请求是通用文档查找、模型选择、GPT-5.4 升级还是 GPT-5.4 提示升级。
2. 如果是模型选择请求，加载 `references/latest-model.md`。
3. 如果是明确的 GPT-5.4 升级请求，加载 `references/upgrading-to-gpt-5p4.md`。
4. 如果升级可能需要提示更改，或者工作流程是研究密集型、工具密集型、编码导向型、多代理或长时间运行的，还要加载 `references/gpt-5p4-prompting-guide.md`。
5. 使用精确查询搜索文档。
6. 获取最佳页面和所需的具体部分（尽可能使用 `anchor`）。
7. 对于 GPT-5.4 升级审查，始终使每个使用站点的输出明确：目标模型、起始推理建议、相关的 `phase` 评估、提示块和兼容性状态。
8. 用简明的指导回答并引用文档来源，仅将引用文件作为辅助上下文使用。

## 引用映射

只读取您需要的内容：

- `references/latest-model.md` -> 模型选择和"最佳/最新/当前模型"问题；在回答之前根据当前 OpenAI 文档验证每个建议。
- `references/upgrading-to-gpt-5p4.md` -> 仅用于明确的 GPT-5.4 升级和升级规划请求；在回答之前根据当前 OpenAI 文档验证清单和兼容性指导。
- `references/gpt-5p4-prompting-guide.md` -> GPT-5.4 的提示重写和提示行为升级；在回答之前根据当前 OpenAI 文档验证提示指导。

## 质量规则

- 将 OpenAI 文档视为真实来源；避免推测。
- 保持引用简短并在政策限制内；更喜欢带有引用的改写。
- 如果多个页面不同，请指出差异并引用两者。
- 引用文件只是便利指南；对于易变指导（如推荐模型、升级说明或提示建议），当前 OpenAI 文档始终胜出。
- 如果文档未涵盖用户的需求，请说明并提供后续步骤。

## 工具说明

- 对于 OpenAI 相关问题，始终在任何 Web 搜索之前使用 MCP 文档工具。
- 如果 MCP 服务器已安装但没有返回有意义的结果，则使用 Web 搜索作为回退。
- 回退到 Web 搜索时，限制为官方 OpenAI 域（developers.openai.com、platform.openai.com）并引用来源。
