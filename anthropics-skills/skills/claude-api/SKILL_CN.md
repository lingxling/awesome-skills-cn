---
name: claude-api
description: "构建、调试和优化 Claude API / Anthropic SDK 应用。使用此技能构建的应用应包括提示缓存。还处理现有 Claude API 代码在 Claude 模型版本之间的迁移（4.5 → 4.6, 4.6 → 4.7, 已停用模型替换）。触发条件：代码导入 `anthropic`/`@anthropic-ai/sdk`；用户要求使用 Claude API、Anthropic SDK 或托管 Agents；用户在文件中添加/修改/调整 Claude 功能（缓存、思考、压缩、工具使用、批处理、文件、引用、记忆）或模型（Opus/Sonnet/Haiku）；关于 Anthropic SDK 项目中提示缓存/缓存命中率的问题。跳过：文件导入 `openai`/其他提供商 SDK、文件名如 `*-openai.py`/`*-generic.py`、提供商中性代码、通用编程/ML。"
license: 完整条款见 LICENSE.txt
---

# 使用 Claude 构建 LLM 驱动的应用

此技能帮助您使用 Claude 构建 LLM 驱动的应用。根据您的需求选择合适的接口，检测项目语言，然后阅读相关的语言特定文档。

## 开始之前

扫描目标文件（或如果没有目标文件，则扫描提示和项目）以查找非 Anthropic 提供商标记 — `import openai`、`from openai`、`langchain_openai`、`OpenAI(`、`gpt-4`、`gpt-5`、文件名如 `agent-openai.py` 或 `*-generic.py`，或任何明确指示保持代码提供商中立的指令。如果找到任何这些，请停止并告诉用户此技能生成 Claude/Anthropic SDK 代码；询问他们是否要将文件切换到 Claude 或想要非 Claude 实现。不要使用 Anthropic SDK 调用编辑非 Anthropic 文件。

## 输出要求

当用户要求您添加、修改或实现 Claude 功能时，您的代码必须通过以下方式之一调用 Claude：

1. **项目语言的官方 Anthropic SDK**（`anthropic`、`@anthropic-ai/sdk`、`com.anthropic.*` 等）。这是项目存在支持的 SDK 时的默认选项。
2. **原始 HTTP**（`curl`、`requests`、`fetch`、`httpx` 等）—— 仅当用户明确要求 cURL/REST/原始 HTTP、项目是 shell/cURL 项目或语言没有官方 SDK 时使用。

永远不要混合使用两者 — 不要在 Python 或 TypeScript 项目中使用 `requests`/`fetch`，仅仅因为它感觉更轻量。永远不要回退到 OpenAI 兼容的 shim。

**永远不要猜测 SDK 使用方式。** 函数名、类名、命名空间、方法签名和导入路径必须来自明确的文档 — 要么是此技能中的 `{lang}/` 文件，要么是 `shared/live-sources.md` 中列出的官方 SDK 存储库或文档链接。如果技能文件中未明确记录您需要的绑定，请在编写代码之前从 `shared/live-sources.md` WebFetch 相关的 SDK 存储库。不要从 cURL 形状或另一种语言的 SDK 推断 Ruby/Java/Go/PHP/C# API。

## 默认设置

除非用户另有要求：

对于 Claude 模型版本，请使用 Claude Opus 4.7，您可以通过精确的模型字符串 `claude-opus-4-7` 访问。对于任何稍微复杂的任务，请默认使用自适应思考（`thinking: {type: "adaptive"}`）。最后，对于任何可能涉及长输入、长输出或高 `max_tokens` 的请求，请默认使用流式传输——这样可以避免请求超时。如果您不需要处理单个流事件，请使用 SDK 的 `.get_final_message()` / `.finalMessage()` 辅助方法获取完整响应

---

## 子命令

如果此提示底部的用户请求是一个纯子命令字符串（无散文），请搜索本文档中的所有**子命令**表——包括下面附加部分中的任何表——并直接遵循匹配的操作列。这允许用户通过 `/claude-api <子命令>` 调用特定流程。如果文档中没有表匹配，则将请求视为普通散文。

<!-- 子命令表在下面按部分定义；此标题块仅包含调度规则，以便功能门控部分可以添加自己的表而不会将字符串泄漏到非门控构建中。 -->

---

## 语言检测

在阅读代码示例之前，确定用户正在使用的语言：

1. **查看项目文件**以推断语言：

   - `*.py`, `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile` → **Python** — 从 `python/` 阅读
   - `*.ts`, `*.tsx`, `package.json`, `tsconfig.json` → **TypeScript** — 从 `typescript/` 阅读
   - `*.js`, `*.jsx`（没有 `.ts` 文件）→ **TypeScript** — JS 使用相同的 SDK，从 `typescript/` 阅读
   - `*.java`, `pom.xml`, `build.gradle` → **Java** — 从 `java/` 阅读
   - `*.kt`, `*.kts`, `build.gradle.kts` → **Java** — Kotlin 使用 Java SDK，从 `java/` 阅读
   - `*.scala`, `build.sbt` → **Java** — Scala 使用 Java SDK，从 `java/` 阅读
   - `*.go`, `go.mod` → **Go** — 从 `go/` 阅读
   - `*.rb`, `Gemfile` → **Ruby** — 从 `ruby/` 阅读
   - `*.cs`, `*.csproj` → **C#** — 从 `csharp/` 阅读
   - `*.php`, `composer.json` → **PHP** — 从 `php/` 阅读

2. **如果检测到多种语言**（例如，同时有 Python 和 TypeScript 文件）：

   - 检查用户当前文件或问题与哪种语言相关
   - 如果仍然模棱两可，询问："我检测到了 Python 和 TypeScript 文件。您使用哪种语言进行 Claude API 集成？"

3. **如果无法推断语言**（空项目、没有源文件或不支持的语言）：

   - 使用 AskUserQuestion 提供选项：Python、TypeScript、Java、Go、Ruby、cURL/原始 HTTP、C#、PHP
   - 如果 AskUserQuestion 不可用，默认使用 Python 示例并注明："显示 Python 示例。如果您需要不同的语言，请告诉我。"

4. **如果检测到不支持的语言**（Rust、Swift、C++、Elixir 等）：

   - 建议从 `curl/` 使用 cURL/原始 HTTP 示例，并说明可能存在社区 SDK
   - 提供显示 Python 或 TypeScript 示例作为参考实现

5. **如果用户需要 cURL/原始 HTTP 示例**，从 `curl/` 阅读。

### 语言特定功能支持

| 语言   | 工具运行器 | 托管 Agents | 备注                                 |
| ---------- | ----------- | -------------- | ------------------------------------- |
| Python     | 是（测试版）  | 是（测试版）     | 完全支持 — `@beta_tool` 装饰器 |
| TypeScript | 是（测试版）  | 是（测试版）     | 完全支持 — `betaZodTool` + Zod    |
| Java       | 是（测试版）  | 是（测试版）     | 测试版工具使用带注释类  |
| Go         | 是（测试版）  | 是（测试版）     | `toolrunner` 包中的 `BetaToolRunner`  |
| Ruby       | 是（测试版）  | 是（测试版）     | 测试版中的 `BaseTool` + `tool_runner`    |
| C#         | 否          | 否             | 官方 SDK                          |
| PHP        | 是（测试版）  | 是（测试版）     | `BetaRunnableTool` + `toolRunner()`   |
| cURL       | 不适用         | 是（测试版）     | 原始 HTTP，无 SDK 功能             |

> **托管 Agents 代码示例**：为 Python、TypeScript、Go、Ruby、PHP、Java 和 cURL 提供了专门的语言特定 README（`{lang}/managed-agents/README.md`、`curl/managed-agents.md`）。阅读您语言的 README 以及语言无关的 `shared/managed-agents-*.md` 概念文件。**Agents 是持久的 — 创建一次，通过 ID 引用。** 存储 `agents.create` 返回的 agent ID 并将其传递给每个后续的 `sessions.create`；不要在请求路径中调用 `agents.create`。Anthropic CLI 是一种从版本控制的 YAML 创建 agents 和环境的便捷方式 — 其 URL 在 `shared/live-sources.md` 中。如果您需要的绑定未在 README 中显示，请从 `shared/live-sources.md` WebFetch 相关条目，而不是猜测。C# 目前没有托管 Agents 支持；使用针对 API 的 cURL 风格原始 HTTP 请求。

---

## 我应该使用哪个接口？

> **从简单开始。** 默认使用满足您需求的最简单层级。单个 API 调用和工作流处理大多数用例——只有当任务真正需要开放式、模型驱动的探索时才使用 agent。

| 用例                                        | 层级            | 推荐接口       | 原因                                     |
| ----------------------------------------------- | --------------- | ------------------------- | --------------------------------------- |
| 分类、摘要、提取、问答  | 单个 LLM 调用 | **Claude API**            | 一个请求，一个响应               |
| 批处理或嵌入                  | 单个 LLM 调用 | **Claude API**            | 专用端点                   |
| 带代码控制逻辑的多步骤管道 | 工作流        | **Claude API + 工具使用** | 您编排循环                |
| 使用自己的工具的自定义 agent                | Agent           | **Claude API + 工具使用** | 最大灵活性                     |
| 服务器管理的带工作区的有状态 agent          | Agent           | **托管 Agents**        | Anthropic 运行循环并托管工具执行沙箱 |
| 持久化、版本化的 agent 配置              | Agent           | **托管 Agents**        | Agents 是存储对象；会话固定到版本         |
| 带文件挂载的长时间运行多轮 agent         | Agent           | **托管 Agents**        | 每会话容器、SSE 事件流、Skills + MCP       |

> **注意：** 托管 Agents 是当您希望 Anthropic 运行 agent 循环 *并且* 托管工具执行的容器时的正确选择 — 文件操作、bash、代码执行都在每会话工作区中运行。如果您想自己托管计算或运行自己的自定义工具运行时，Claude API + 工具使用是正确的选择 — 使用工具运行器进行自动循环处理，或手动循环进行细粒度控制（审批门、自定义日志、条件执行）。

> **第三方提供商（Amazon Bedrock、Google Vertex AI、Microsoft Foundry）：** 托管 Agents **不可用**于 Bedrock、Vertex 或 Foundry。如果您通过任何第三方提供商部署，请对所有用例使用 **Claude API + 工具使用** — 包括托管 Agents 否则会是推荐表面的情况。

### 决策树

```
您的应用需要什么？

0. 您是否通过 Amazon Bedrock、Google Vertex AI 或 Microsoft Foundry 部署？
   └── 是 → Claude API（+ 工具使用用于 agents）— 托管 Agents 仅适用于第一方。
   否 → 继续。

1. 单个 LLM 调用（分类、摘要、提取、问答）
   └── Claude API — 一个请求，一个响应

2. 您是否希望 Anthropic 运行 agent 循环并托管每会话
   容器，Claude 在其中执行工具（bash、文件操作、代码）？
   └── 是 → 托管 Agents — 服务器管理的会话，持久化 agent 配置，
       SSE 事件流，Skills + MCP，文件挂载。
       示例："每个任务带工作区的有状态编码 agent"、
             "向 UI 流式传输事件的长时间运行研究 agent"、
             "跨多个会话使用的持久化、版本化配置的 agent"

3. 工作流（多步骤、代码编排、使用自己的工具）
   └── Claude API + 工具使用 — 您控制循环

4. 开放式 agent（模型决定自己的轨迹、使用自己的工具、自己托管计算）
   └── Claude API agentic 循环（最大灵活性）
```

### 我应该构建 Agent 吗？

在选择 agent 层级之前，检查所有四个标准：

- **复杂性** — 任务是否多步骤且难以完全提前指定？（例如，"将此设计文档转换为 PR" 与 "从此 PDF 中提取标题"）
- **价值** — 结果是否证明更高的成本和延迟是合理的？
- **可行性** — Claude 是否能够完成此类任务？
- **错误成本** — 错误是否可以被捕获和恢复？（测试、审查、回滚）

如果对其中任何一项的答案是"否"，则保持在更简单的层级（单个调用或工作流）。

---

## 架构

所有内容都通过 `POST /v1/messages`。工具和输出约束是此单个端点的功能——不是单独的 API。

**用户定义的工具** — 您定义工具（通过装饰器、Zod 模式或原始 JSON），SDK 的工具运行器处理调用 API、执行您的函数并循环直到 Claude 完成。对于完全控制，您可以手动编写循环。

**服务器端工具** — 在 Anthropic 基础设施上运行的 Anthropic 托管工具。代码执行完全在服务器端（在 `tools` 中声明，Claude 自动运行代码）。计算机使用可以是服务器托管或自托管。

**结构化输出** — 约束 Messages API 响应格式（`output_config.format`）和/或工具参数验证（`strict: true`）。推荐的方法是 `client.messages.parse()`，它会根据您的模式自动验证响应。注意：旧的 `output_format` 参数已弃用；在 `messages.create()` 上使用 `output_config: {format: {...}}`。

**支持端点** — 批处理（`POST /v1/messages/batches`）、文件（`POST /v1/files`）、令牌计数和模型（`GET /v1/models`、`GET /v1/models/{id}` — 实时能力/上下文窗口发现）输入或支持 Messages API 请求。

---

## 当前模型（缓存：2026-04-15）

| 模型             | 模型 ID            | 上下文        | 输入 $/1M | 输出 $/1M |
| ----------------- | ------------------- | -------------- | ---------- | ----------- |
| Claude Opus 4.7   | `claude-opus-4-7`   | 1M             | $5.00      | $25.00      |
| Claude Opus 4.6   | `claude-opus-4-6`   | 1M             | $5.00      | $25.00      |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 1M             | $3.00      | $15.00      |
| Claude Haiku 4.5  | `claude-haiku-4-5`  | 200K           | $1.00      | $5.00       |

**始终使用 `claude-opus-4-7`，除非用户明确指定不同的模型。** 这是不可协商的。不要使用 `claude-sonnet-4-6`、`claude-sonnet-4-5` 或任何其他模型，除非用户字面上说"使用 sonnet"或"使用 haiku"。永远不要为了降低成本而降级——这是用户的决定，不是您的决定。

**关键：仅使用上表中精确的模型 ID 字符串——它们原样完整。不要附加日期后缀。** 例如，使用 `claude-sonnet-4-5`，永远不要使用 `claude-sonnet-4-5-20250514` 或您可能从训练数据中回忆起的任何其他带日期后缀的变体。如果用户请求表中未列出的较旧模型（例如，"opus 4.5"、"sonnet 3.7"），请阅读 `shared/models.md` 以获取精确 ID——不要自己构造一个。

注意：如果上述任何模型字符串对您来说看起来不熟悉，那是意料之中的——这只是意味着它们是在您的训练数据截止日期之后发布的。请放心，它们是真实的模型；我们不会那样戏弄您。

**实时能力查询：** 上表是缓存的。当用户询问"X 的上下文窗口是多少"、"X 是否支持视觉/思考/努力"或"哪些模型支持 Y"时，请查询 Models API（`client.models.retrieve(id)` / `client.models.list()`）——有关字段参考和能力过滤示例，请参阅 `shared/models.md`。

---

## 思考与努力（快速参考）

**Opus 4.7 — 仅支持自适应思考：** 使用 `thinking: {type: "adaptive"}`。`thinking: {type: "enabled", budget_tokens: N}` 在 Opus 4.7 上会返回 400 错误 — 自适应是唯一的开启模式。`{type: "disabled"}` 和省略 `thinking` 都可以正常工作。采样参数（`temperature`、`top_p`、`top_k`）也已删除，会返回 400 错误。请参阅 `shared/model-migration.md` → 迁移到 Opus 4.7 获取完整的破坏性更改列表。

**Opus 4.6 — 自适应思考（推荐）：** 使用 `thinking: {type: "adaptive"}`。Claude 动态决定何时以及思考多少。不需要 `budget_tokens` — `budget_tokens` 在 Opus 4.6 和 Sonnet 4.6 上已弃用，不应该用于新代码。自适应思考还会自动启用交错思考（不需要测试版标头）。**当用户要求"扩展思考"、"思考预算"或 `budget_tokens` 时：始终使用 Opus 4.7 或 4.6 配合 `thinking: {type: "adaptive"}`。固定令牌预算进行思考的概念已弃用——自适应思考取代了它。不要使用 `budget_tokens` 并且不要切换到较旧的模型。** *渐进式迁移豁免：* `budget_tokens` 在 Opus 4.6 和 Sonnet 4.6 上仍然可用作为过渡性逃生舱 — 如果您正在迁移现有代码并在调整 `effort` 之前需要硬性令牌上限，请参阅 `shared/model-migration.md` → 过渡性逃生舱。请注意，此豁免不适用于 Opus 4.7 — `budget_tokens` 在该版本中已完全移除。

**努力参数（正式版，无需测试版标头）：** 通过 `output_config: {effort: "low"|"medium"|"high"|"max"}`（在 `output_config` 内，不在顶层）控制思考深度和整体令牌开销。默认为 `high`（相当于省略它）。`max` 仅适用于 Opus 层（Opus 4.6 及更高版本 — 不适用于 Sonnet 或 Haiku）。Opus 4.7 添加了 `"xhigh"`（介于 `high` 和 `max` 之间）— 这是 4.7 上大多数编码和 agentic 用例的最佳设置，也是 Claude Code 中的默认设置；对于大多数智能敏感工作，请至少使用 `high`。适用于 Opus 4.5、Opus 4.6、Opus 4.7 和 Sonnet 4.6。在 Sonnet 4.5 / Haiku 4.5 上会出错。在 Opus 4.7 上，努力比以前的任何 Opus 版本都更重要 — 迁移时请重新调整它。结合自适应思考以获得最佳成本-质量权衡。较低的努力意味着更少和更集中的工具调用、更少的前言和更简洁的确认 — `high` 通常是平衡质量和令牌效率的最佳选择；当正确性比成本更重要时使用 `max`；对子 agent 或简单任务使用 `low`。

**Opus 4.7 — 思考内容默认省略：** `thinking` 块仍然流式传输，但其文本为空，除非您使用 `thinking: {type: "adaptive", display: "summarized"}` 选择加入（默认是 `"omitted"`）。静默更改 — 无错误。如果您向用户流式传输推理，默认看起来像输出前的长时间暂停；设置 `"summarized"` 以恢复可见进度。

**任务预算（测试版，Opus 4.7）：** `output_config: {task_budget: {type: "tokens", total: N}}` 告诉模型它有多少令牌用于完整的 agentic 循环 — 它看到倒计时并进行自我调节（最少 20,000；测试版标头 `task-budgets-2026-03-13`）。与 `max_tokens` 不同，后者是模型不知道的强制每响应上限。请参阅 `shared/model-migration.md` → 任务预算。

**Sonnet 4.6：** 支持自适应思考（`thinking: {type: "adaptive"}`）。`budget_tokens` 在 Sonnet 4.6 上已弃用——改用自适应思考。

**较旧的模型（仅在明确请求时）：** 如果用户特别要求 Sonnet 4.5 或另一个较旧的模型，请使用 `thinking: {type: "enabled", budget_tokens: N}`。`budget_tokens` 必须小于 `max_tokens`（最少 1024）。永远不要仅仅因为用户提到 `budget_tokens` 就选择较旧的模型——改用 Opus 4.7 配合自适应思考。

---

## 压缩（快速参考）

**测试版，适用于 Opus 4.6、Opus 4.7 和 Sonnet 4.6。** 对于可能超过 1M 上下文窗口的长时间运行的对话，启用服务器端压缩。当接近触发阈值（默认：150K 令牌）时，API 会自动汇总较早的上下文。需要测试版标头 `compact-2026-01-12`。

关键：在每一轮中将 `response.content`（不仅仅是文本）追加回您的消息。响应中的压缩块必须保留——API 使用它们在下一个请求中替换压缩的历史记录。仅提取文本字符串并追加该字符串将静默丢失压缩状态。

有关代码示例，请参阅 `{lang}/claude-api/README.md`（压缩部分）。通过 `shared/live-sources.md` 中的 WebFetch 获取完整文档。

---

## 提示缓存（快速参考）

**前缀匹配。** 前缀中的任何字节更改都会使其后的所有内容失效。渲染顺序为 `tools` → `system` → `messages`。将稳定内容放在前面（冻结的系统提示、确定性工具列表），将易变内容（时间戳、每个请求的 ID、不同的问题）放在最后一个 `cache_control` 断点之后。

**顶层自动缓存**（在 `messages.create()` 上使用 `cache_control: {type: "ephemeral"}`）是不需要细粒度放置时的最简单选项。每个请求最多 4 个断点。最小可缓存前缀约为 1024 个令牌——较短的前缀不会静默缓存。

**使用 `usage.cache_read_input_tokens` 验证** — 如果在重复请求中它为零，则存在静默无效器（系统提示中的 `datetime.now()`、未排序的 JSON、变化的工具集）。

有关放置模式、架构指导和静默无效器审计清单：请阅读 `shared/prompt-caching.md`。语言特定语法：`{lang}/claude-api/README.md`（提示缓存部分）。

---

## 托管 Agents（测试版）

**托管 Agents** 是第三个表面：服务器管理的有状态 agents，带有 Anthropic 托管的工具执行。您创建一个持久化、版本化的 Agent 配置（`POST /v1/agents`），然后启动引用它的会话。每个会话都为 agent 的工作区提供一个容器 — bash、文件操作和代码执行在那里运行；agent 循环本身在 Anthropic 的编排层上运行，并通过工具在容器上操作。会话流式传输事件；您发送消息和工具结果回去。

**托管 Agents 仅适用于第一方。** 它不适用于 Amazon Bedrock、Google Vertex AI 或 Microsoft Foundry。对于第三方提供商上的 agents，请使用 Claude API + 工具使用。

**强制流程：** Agent（一次）→ 会话（每次运行）。`model`/`system`/`tools` 存在于 agent 上，永远不存在于会话上。有关完整阅读指南、测试版标头和陷阱，请参阅 `shared/managed-agents-overview.md`。

**测试版标头：** `managed-agents-2026-04-01` — SDK 会自动为所有 `client.beta.{agents,environments,sessions,vaults}.*` 调用设置此标头。Skills API 使用 `skills-2025-10-02`，Files API 使用 `files-api-2025-04-14`，但除了 `/v1/skills` 和 `/v1/files` 之外的端点，您不需要明确传递这些。

**子命令** — 使用 `/claude-api <subcommand>` 直接调用：

| 子命令 | 操作 |
|---|---|
| `managed-agents-onboard` | 引导用户从头设置托管 Agent。**立即阅读 `shared/managed-agents-onboarding.md`** 并按照其访谈脚本执行：心理模型 → 了解或探索分支 → 模板配置 → 会话设置 → 生成代码。不要总结 — 运行访谈。 |

**阅读指南：** 从 `shared/managed-agents-overview.md` 开始，然后阅读主题 `shared/managed-agents-*.md` 文件（核心、环境、工具、事件、客户端模式、入门、API 参考）。对于 Python、TypeScript、Go、Ruby、PHP 和 Java，请阅读 `{lang}/managed-agents/README.md` 获取代码示例。对于 cURL，请阅读 `curl/managed-agents.md`。**Agents 是持久的 — 创建一次，通过 ID 引用。** 存储 `agents.create` 返回的 agent ID 并将其传递给每个后续的 `sessions.create`；不要在请求路径中调用 `agents.create`。Anthropic CLI 是一种从版本控制的 YAML 创建 agents 和环境的便捷方式（URL 在 `shared/live-sources.md` 中）。如果您需要的绑定未在语言 README 中显示，请从 `shared/live-sources.md` WebFetch 相关条目，而不是猜测。C# 目前不支持托管 Agents；使用 `curl/managed-agents.md` 中的原始 HTTP 作为参考。

**当用户想要从头设置托管 Agent 时**（例如 "如何开始"、"引导我创建一个"、"设置新 agent"）：阅读 `shared/managed-agents-onboarding.md` 并运行其访谈 — 与 `managed-agents-onboard` 子命令相同的流程。

**当用户询问 "如何为 X 编写客户端代码" 时：** 参考 `shared/managed-agents-client-patterns.md` — 涵盖无损流重新连接、`processed_at` 排队/处理门、中断、`tool_confirmation` 往返、正确的空闲/终止中断门、空闲后状态竞争、流优先排序、文件挂载陷阱、通过自定义工具保持凭据在主机端等。

---

## 阅读指南

检测语言后，根据用户需求阅读相关文件：

### 快速任务参考

**单个文本分类/摘要/提取/问答：**
→ 仅阅读 `{lang}/claude-api/README.md`

**聊天 UI 或实时响应显示：**
→ 阅读 `{lang}/claude-api/README.md` + `{lang}/claude-api/streaming.md`

**长时间运行的对话（可能超过上下文窗口）：**
→ 阅读 `{lang}/claude-api/README.md` — 见压缩部分

**迁移到较新模型（Opus 4.7 / Opus 4.6 / Sonnet 4.6）或替换已停用模型：**
→ 阅读 `shared/model-migration.md`

**提示缓存 / 优化缓存 / "为什么我的缓存命中率低"：**
→ 阅读 `shared/prompt-caching.md` + `{lang}/claude-api/README.md`（提示缓存部分）

**函数调用 / 工具使用 / agents：**
→ 阅读 `{lang}/claude-api/README.md` + `shared/tool-use-concepts.md` + `{lang}/claude-api/tool-use.md`

**Agent 设计（工具表面、上下文管理、缓存策略）：**
→ 阅读 `shared/agent-design.md`

**批处理（非延迟敏感）：**
→ 阅读 `{lang}/claude-api/README.md` + `{lang}/claude-api/batches.md`

**跨多个请求的文件上传：**
→ 阅读 `{lang}/claude-api/README.md` + `{lang}/claude-api/files-api.md`

**托管 Agents（服务器管理的带工作区的有状态 agents）：**
→ 阅读 `shared/managed-agents-overview.md` + 其余 `shared/managed-agents-*.md` 文件。对于 Python、TypeScript、Go、Ruby、PHP 和 Java，请阅读 `{lang}/managed-agents/README.md` 获取代码示例。对于 cURL，请阅读 `curl/managed-agents.md`。**Agents 是持久的 — 创建一次，通过 ID 引用。** 存储 `agents.create` 返回的 agent ID 并将其传递给每个后续的 `sessions.create`；不要在请求路径中调用 `agents.create`。Anthropic CLI 是一种从版本控制的 YAML 创建 agents 和环境的便捷方式（URL 在 `shared/live-sources.md` 中）。如果您需要的绑定未在语言 README 中显示，请从 `shared/live-sources.md` WebFetch 相关条目，而不是猜测。C# 目前不支持托管 Agents；使用 `curl/managed-agents.md` 中的原始 HTTP 作为参考。

### Claude API（完整文件参考）

阅读**语言特定的 Claude API 文件夹**（`{language}/claude-api/`）：

1. **`{language}/claude-api/README.md`** — **首先阅读此文件。** 安装、快速入门、常见模式、错误处理。
2. **`shared/tool-use-concepts.md`** — 当用户需要函数调用、代码执行、内存或结构化输出时阅读。涵盖概念基础。
3. **`shared/agent-design.md`** — 设计 agent 时阅读：bash vs. 专用工具、编程工具调用、工具搜索/技能、上下文编辑 vs. 压缩 vs. 内存、缓存原则。
4. **`{language}/claude-api/tool-use.md`** — 阅读以获取语言特定的工具使用代码示例（工具运行器、手动循环、代码执行、内存、结构化输出）。
5. **`{language}/claude-api/streaming.md`** — 构建聊天 UI 或增量显示响应的接口时阅读。
6. **`{language}/claude-api/batches.md`** — 处理许多离线请求（非延迟敏感）时阅读。以 50% 的成本异步运行。
7. **`{language}/claude-api/files-api.md`** — 在多个请求中发送相同文件而无需重新上传时阅读。
8. **`shared/prompt-caching.md`** — 添加或优化提示缓存时阅读。涵盖前缀稳定性设计、断点放置和会静默使缓存无效的反模式。
9. **`shared/error-codes.md`** — 调试 HTTP 错误或实现错误处理时阅读。
10. **`shared/live-sources.md`** — 用于获取最新官方文档的 WebFetch URL。

> **注意：** 对于 Java、Go、Ruby、C#、PHP 和 cURL——这些各有一个文件涵盖所有基础知识。阅读该文件以及根据需要阅读 `shared/tool-use-concepts.md` 和 `shared/error-codes.md`。

> **注意：** 对于托管 Agents 文件参考，请参阅上面的 `## 托管 Agents（测试版）` 部分 — 它列出了所有 `shared/managed-agents-*.md` 文件和语言特定的 README。

---

## 何时使用 WebFetch

在以下情况下使用 WebFetch 获取最新文档：

- 用户要求"最新"或"当前"信息
- 缓存数据似乎不正确
- 用户询问此处未涵盖的功能

实时文档 URL 在 `shared/live-sources.md` 中。

## 常见陷阱

- 将文件或内容传递给 API 时不要截断输入。如果内容太长而无法放入上下文窗口，请通知用户并讨论选项（分块、摘要等），而不是静默截断。
- **Opus 4.7 思考：** 自适应思考仅支持。`thinking: {type: "enabled", budget_tokens: N}` 在 Opus 4.7 上返回 400 — `budget_tokens` 在该版本已完全移除（以及 `temperature`、`top_p`、`top_k`）。使用 `thinking: {type: "adaptive"}`。
- **Opus 4.6 / Sonnet 4.6 思考：** 使用 `thinking: {type: "adaptive"}` — 新代码不要使用 `budget_tokens`（在 Opus 4.6 和 Sonnet 4.6 上已弃用；有关现有代码的渐进迁移，请参阅 `shared/model-migration.md` 中的过渡性逃生舱 — 注意此豁免不适用于 Opus 4.7）。对于较旧的模型，`budget_tokens` 必须小于 `max_tokens`（最少 1024）。如果弄错了，这将抛出错误。
- **4.6/4.7 系列预填充已移除：** 助手消息预填充（最后一轮助手预填充）在 Opus 4.6、Opus 4.7 和 Sonnet 4.6 上返回 400 错误。改用结构化输出（`output_config.format`）或系统提示指令来控制响应格式。
- **编辑前确认迁移范围：** 当用户要求将代码迁移到较新的 Claude 模型但未指定文件、目录或文件列表时，**请先询问要应用的范围** — 整个工作目录、特定的子目录或特定的文件集。在用户确认之前不要开始编辑。像"迁移我的代码库"、"将我的项目移到 X"、"升级到 Sonnet 4.6"或简单的"迁移到 Opus 4.7"这样的祈使语气仍然**是模糊的** — 它们告诉您要做什么但不告诉在哪里，所以请询问。只有当提示命名了确切的文件、特定的目录或明确的文件列表时，才可以不询问就继续（"迁移 `app.py`"、"迁移 `services/` 下的所有内容"、"更新 `a.py` 和 `b.py`）。请参阅 `shared/model-migration.md` 步骤 0。
- **`max_tokens` 默认值：** 不要低估 `max_tokens` — 达到上限会在思考中途截断输出并需要重试。对于非流式请求，默认为 `~16000`（保持响应在 SDK HTTP 超时以下）。对于流式请求，默认为 `~64000`（超时不是问题，所以给模型留出空间）。只有在有充分理由时才降低：分类（`~256`）、成本上限或故意简短的输出。
- **128K 输出令牌：** Opus 4.6 和 Opus 4.7 支持高达 128K `max_tokens`，但对于大 `max_tokens`，SDK 需要流式传输以避免 HTTP 超时。使用 `.stream()` 配合 `.get_final_message()` / `.finalMessage()`。
- **工具调用 JSON 解析（4.6/4.7 系列）：** Opus 4.6、Opus 4.7 和 Sonnet 4.6 可能在工具调用 `input` 字段中产生不同的 JSON 字符串转义（例如，Unicode 或反斜杠转义）。始终使用 `json.loads()` / `JSON.parse()` 解析工具输入——永远不要对序列化输入进行原始字符串匹配。
- **结构化输出（所有模型）：** 在 `messages.create()` 上使用 `output_config: {format: {...}}` 而不是已弃用的 `output_format` 参数。这是一个通用的 API 更改，不是 4.6 特定的。
- **不要重新实现 SDK 功能：** SDK 提供高级辅助——使用它们而不是从头开始构建。具体来说：使用 `stream.finalMessage()` 而不是将 `.on()` 事件包装在 `new Promise()` 中；使用类型化异常类（`Anthropic.RateLimitError` 等）而不是字符串匹配错误消息；使用 SDK 类型（`Anthropic.MessageParam`、`Anthropic.Tool`、`Anthropic.Message` 等）而不是重新定义等效接口。
- **不要为 SDK 数据结构定义自定义类型：** SDK 导出所有 API 对象的类型。使用 `Anthropic.MessageParam` 表示消息，`Anthropic.Tool` 表示工具定义，`Anthropic.ToolUseBlock` / `Anthropic.ToolResultBlockParam` 表示工具结果，`Anthropic.Message` 表示响应。定义自己的 `interface ChatMessage { role: string; content: unknown }` 重复了 SDK 已经提供的内容并失去类型安全性。
- **报告和文档输出：** 对于生成报告、文档或可视化的任务，代码执行沙箱预安装了 `python-docx`、`python-pptx`、`matplotlib`、`pillow` 和 `pypdf`。Claude 可以生成格式化文件（DOCX、PDF、图表）并通过 Files API 返回它们——对于"报告"或"文档"类型的请求，请考虑这一点，而不是纯标准输出文本。
