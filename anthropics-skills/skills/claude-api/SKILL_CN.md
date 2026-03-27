---
name: claude-api
description: "使用 Claude API 或 Anthropic SDK 构建应用。触发条件：代码导入 `anthropic`/`@anthropic-ai/sdk`/`claude_agent_sdk`，或用户要求使用 Claude API、Anthropic SDK 或 Agent SDK。不要触发：代码导入 `openai`/其他 AI SDK、通用编程或 ML/数据科学任务。"
license: 完整条款见 LICENSE.txt
---

# 使用 Claude 构建 LLM 驱动的应用

此技能帮助您使用 Claude 构建 LLM 驱动的应用。根据您的需求选择合适的接口，检测项目语言，然后阅读相关的语言特定文档。

## 默认设置

除非用户另有要求：

对于 Claude 模型版本，请使用 Claude Opus 4.6，您可以通过精确的模型字符串 `claude-opus-4-6` 访问。对于任何稍微复杂的任务，请默认使用自适应思考（`thinking: {type: "adaptive"}`）。最后，对于任何可能涉及长输入、长输出或高 `max_tokens` 的请求，请默认使用流式传输——这样可以避免请求超时。如果您不需要处理单个流事件，请使用 SDK 的 `.get_final_message()` / `.finalMessage()` 辅助方法获取完整响应

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

| 语言   | 工具运行器 | Agent SDK | 备注                                 |
| ---------- | ----------- | --------- | ------------------------------------- |
| Python     | 是（测试版）  | 是       | 完全支持 — `@beta_tool` 装饰器 |
| TypeScript | 是（测试版）  | 是       | 完全支持 — `betaZodTool` + Zod    |
| Java       | 是（测试版）  | 否        | 使用带注释类的测试版工具使用  |
| Go         | 是（测试版）  | 否        | `toolrunner` 包中的 `BetaToolRunner`  |
| Ruby       | 是（测试版）  | 否        | 测试版中的 `BaseTool` + `tool_runner`    |
| cURL       | 不适用         | 不适用       | 原始 HTTP，无 SDK 功能             |
| C#         | 否          | 否        | 官方 SDK                          |
| PHP        | 是（测试版）  | 否        | `BetaRunnableTool` + `toolRunner()`   |

---

## 我应该使用哪个接口？

> **从简单开始。** 默认使用满足您需求的最简单层级。单个 API 调用和工作流处理大多数用例——只有当任务真正需要开放式、模型驱动的探索时才使用 agent。

| 用例                                        | 层级            | 推荐接口       | 原因                                     |
| ----------------------------------------------- | --------------- | ------------------------- | --------------------------------------- |
| 分类、摘要、提取、问答  | 单个 LLM 调用 | **Claude API**            | 一个请求，一个响应               |
| 批处理或嵌入                  | 单个 LLM 调用 | **Claude API**            | 专用端点                   |
| 带代码控制逻辑的多步骤管道 | 工作流        | **Claude API + 工具使用** | 您编排循环                |
| 使用自己的工具的自定义 agent                | Agent           | **Claude API + 工具使用** | 最大灵活性                     |
| 具有文件/网络/终端访问权限的 AI agent          | Agent           | **Agent SDK**             | 内置工具、安全性和 MCP 支持 |
| Agentic 编程助手                        | Agent           | **Agent SDK**             | 专为此用例设计              |
| 需要内置权限和护栏        | Agent           | **Agent SDK**             | 包含安全功能                |

> **注意：** Agent SDK 适用于您需要内置文件/网络/终端工具、权限和 MCP 的情况。如果您想使用自己的工具构建 agent，Claude API 是正确的选择——使用工具运行器进行自动循环处理，或手动循环进行细粒度控制（审批门、自定义日志、条件执行）。

### 决策树

```
您的应用需要什么？

1. 单个 LLM 调用（分类、摘要、提取、问答）
   └── Claude API — 一个请求，一个响应

2. Claude 是否需要读取/写入文件、浏览网页或运行 shell 命令
   作为其工作的一部分？（不是：您的应用读取文件并将其交给 Claude——
   Claude 本身是否需要发现和访问文件/网络/shell？）
   └── 是 → Agent SDK — 内置工具，不要重新实现它们
       示例："扫描代码库查找 bug"、"总结目录中的每个文件"、"使用子 agent 查找 bug"、"通过网络搜索研究主题"

3. 工作流（多步骤、代码编排、使用自己的工具）
   └── Claude API + 工具使用 — 您控制循环

4. 开放式 agent（模型决定自己的轨迹、自己的工具）
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

## 当前模型（缓存：2026-02-17）

| 模型             | 模型 ID            | 上下文        | 输入 $/1M | 输出 $/1M |
| ----------------- | ------------------- | -------------- | ---------- | ----------- |
| Claude Opus 4.6   | `claude-opus-4-6`   | 200K (1M 测试版) | $5.00      | $25.00      |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 200K (1M 测试版) | $3.00      | $15.00      |
| Claude Haiku 4.5  | `claude-haiku-4-5`  | 200K           | $1.00      | $5.00       |

**始终使用 `claude-opus-4-6`，除非用户明确指定不同的模型。** 这是不可协商的。不要使用 `claude-sonnet-4-6`、`claude-sonnet-4-5` 或任何其他模型，除非用户字面上说"使用 sonnet"或"使用 haiku"。永远不要为了降低成本而降级——这是用户的决定，不是您的决定。

**关键：仅使用上表中精确的模型 ID 字符串——它们原样完整。不要附加日期后缀。** 例如，使用 `claude-sonnet-4-5`，永远不要使用 `claude-sonnet-4-5-20250514` 或您可能从训练数据中回忆起的任何其他带日期后缀的变体。如果用户请求表中未列出的较旧模型（例如，"opus 4.5"、"sonnet 3.7"），请阅读 `shared/models.md` 以获取精确 ID——不要自己构造一个。

注意：如果上述任何模型字符串对您来说看起来不熟悉，那是意料之中的——这只是意味着它们是在您的训练数据截止日期之后发布的。请放心，它们是真实的模型；我们不会那样戏弄您。

**实时能力查询：** 上表是缓存的。当用户询问"X 的上下文窗口是多少"、"X 是否支持视觉/思考/努力"或"哪些模型支持 Y"时，请查询 Models API（`client.models.retrieve(id)` / `client.models.list()`）——有关字段参考和能力过滤示例，请参阅 `shared/models.md`。

---

## 思考与努力（快速参考）

**Opus 4.6 — 自适应思考（推荐）：** 使用 `thinking: {type: "adaptive"}`。Claude 动态决定何时以及思考多少。不需要 `budget_tokens` — `budget_tokens` 在 Opus 4.6 和 Sonnet 4.6 上已弃用，绝不能使用。自适应思考还会自动启用交错思考（不需要测试版标头）。**当用户要求"扩展思考"、"思考预算"或 `budget_tokens` 时：始终使用 Opus 4.6 配合 `thinking: {type: "adaptive"}`。固定令牌预算进行思考的概念已弃用——自适应思考取代了它。不要使用 `budget_tokens` 并且不要切换到较旧的模型。**

**努力参数（正式版，无需测试版标头）：** 通过 `output_config: {effort: "low"|"medium"|"high"|"max"}`（在 `output_config` 内，不在顶层）控制思考深度和整体令牌开销。默认为 `high`（相当于省略它）。`max` 仅适用于 Opus 4.6。适用于 Opus 4.5、Opus 4.6 和 Sonnet 4.6。在 Sonnet 4.5 / Haiku 4.5 上会出错。与自适应思考结合使用以获得最佳成本-质量权衡。对子 agent 或简单任务使用 `low`；对最深推理使用 `max`。

**Sonnet 4.6：** 支持自适应思考（`thinking: {type: "adaptive"}`）。`budget_tokens` 在 Sonnet 4.6 上已弃用——改用自适应思考。

**较旧的模型（仅在明确请求时）：** 如果用户特别要求 Sonnet 4.5 或另一个较旧的模型，请使用 `thinking: {type: "enabled", budget_tokens: N}`。`budget_tokens` 必须小于 `max_tokens`（最少 1024）。永远不要仅仅因为用户提到 `budget_tokens` 就选择较旧的模型——改用 Opus 4.6 配合自适应思考。

---

## 压缩（快速参考）

**测试版，适用于 Opus 4.6 和 Sonnet 4.6。** 对于可能超过 200K 上下文窗口的长时间运行的对话，启用服务器端压缩。当接近触发阈值（默认：150K 令牌）时，API 会自动汇总较早的上下文。需要测试版标头 `compact-2026-01-12`。

关键：在每一轮中将 `response.content`（不仅仅是文本）追加回您的消息。响应中的压缩块必须保留——API 使用它们在下一个请求中替换压缩的历史记录。仅提取文本字符串并追加该字符串将静默丢失压缩状态。

有关代码示例，请参阅 `{lang}/claude-api/README.md`（压缩部分）。通过 `shared/live-sources.md` 中的 WebFetch 获取完整文档。

---

## 提示缓存（快速参考）

**前缀匹配。** 前缀中的任何字节更改都会使其后的所有内容失效。渲染顺序为 `tools` → `system` → `messages`。将稳定内容放在前面（冻结的系统提示、确定性工具列表），将易变内容（时间戳、每个请求的 ID、不同的问题）放在最后一个 `cache_control` 断点之后。

**顶层自动缓存**（在 `messages.create()` 上使用 `cache_control: {type: "ephemeral"}`）是不需要细粒度放置时的最简单选项。每个请求最多 4 个断点。最小可缓存前缀约为 1024 个令牌——较短的前缀不会静默缓存。

**使用 `usage.cache_read_input_tokens` 验证** — 如果在重复请求中它为零，则存在静默无效器（系统提示中的 `datetime.now()`、未排序的 JSON、变化的工具集）。

有关放置模式、架构指导和静默无效器审计清单：请阅读 `shared/prompt-caching.md`。语言特定语法：`{lang}/claude-api/README.md`（提示缓存部分）。

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

**提示缓存 / 优化缓存 / "为什么我的缓存命中率低"：**
→ 阅读 `shared/prompt-caching.md` + `{lang}/claude-api/README.md`（提示缓存部分）

**函数调用 / 工具使用 / agents：**
→ 阅读 `{lang}/claude-api/README.md` + `shared/tool-use-concepts.md` + `{lang}/claude-api/tool-use.md`

**批处理（非延迟敏感）：**
→ 阅读 `{lang}/claude-api/README.md` + `{lang}/claude-api/batches.md`

**跨多个请求的文件上传：**
→ 阅读 `{lang}/claude-api/README.md` + `{lang}/claude-api/files-api.md`

**具有内置工具的 agent（文件/网络/终端）：**
→ 阅读 `{lang}/agent-sdk/README.md` + `{lang}/agent-sdk/patterns.md`

### Claude API（完整文件参考）

阅读**语言特定的 Claude API 文件夹**（`{language}/claude-api/`）：

1. **`{language}/claude-api/README.md`** — **首先阅读此文件。** 安装、快速入门、常见模式、错误处理。
2. **`shared/tool-use-concepts.md`** — 当用户需要函数调用、代码执行、内存或结构化输出时阅读。涵盖概念基础。
3. **`{language}/claude-api/tool-use.md`** — 阅读以获取语言特定的工具使用代码示例（工具运行器、手动循环、代码执行、内存、结构化输出）。
4. **`{language}/claude-api/streaming.md`** — 构建聊天 UI 或增量显示响应的接口时阅读。
5. **`{language}/claude-api/batches.md`** — 处理许多离线请求（非延迟敏感）时阅读。以 50% 的成本异步运行。
6. **`{language}/claude-api/files-api.md`** — 在多个请求中发送相同文件而无需重新上传时阅读。
7. **`shared/prompt-caching.md`** — 添加或优化提示缓存时阅读。涵盖前缀稳定性设计、断点放置和会静默使缓存无效的反模式。
8. **`shared/error-codes.md`** — 调试 HTTP 错误或实现错误处理时阅读。
9. **`shared/live-sources.md`** — 用于获取最新官方文档的 WebFetch URL。

> **注意：** 对于 Java、Go、Ruby、C#、PHP 和 cURL——这些各有一个文件涵盖所有基础知识。阅读该文件以及根据需要阅读 `shared/tool-use-concepts.md` 和 `shared/error-codes.md`。

### Agent SDK

阅读**语言特定的 Agent SDK 文件夹**（`{language}/agent-sdk/`）。Agent SDK 仅适用于 **Python 和 TypeScript**。

1. **`{language}/agent-sdk/README.md`** — 安装、快速入门、内置工具、权限、MCP、钩子。
2. **`{language}/agent-sdk/patterns.md`** — 自定义工具、钩子、子 agent、MCP 集成、会话恢复。
3. **`shared/live-sources.md`** — 用于当前 Agent SDK 文档的 WebFetch URL。

---

## 何时使用 WebFetch

在以下情况下使用 WebFetch 获取最新文档：

- 用户要求"最新"或"当前"信息
- 缓存数据似乎不正确
- 用户询问此处未涵盖的功能

实时文档 URL 在 `shared/live-sources.md` 中。

## 常见陷阱

- 将文件或内容传递给 API 时不要截断输入。如果内容太长而无法放入上下文窗口，请通知用户并讨论选项（分块、摘要等），而不是静默截断。
- **Opus 4.6 / Sonnet 4.6 思考：** 使用 `thinking: {type: "adaptive"}` — 不要使用 `budget_tokens`（在 Opus 4.6 和 Sonnet 4.6 上已弃用）。对于较旧的模型，`budget_tokens` 必须小于 `max_tokens`（最少 1024）。如果弄错了，这将抛出错误。
- **Opus 4.6 预填充已移除：** 助手消息预填充（最后一轮助手预填充）在 Opus 4.6 上返回 400 错误。改用结构化输出（`output_config.format`）或系统提示指令来控制响应格式。
- **`max_tokens` 默认值：** 不要低估 `max_tokens` — 达到上限会在思考中途截断输出并需要重试。对于非流式请求，默认为 `~16000`（保持响应在 SDK HTTP 超时以下）。对于流式请求，默认为 `~64000`（超时不是问题，所以给模型留出空间）。只有在有充分理由时才降低：分类（`~256`）、成本上限或故意简短的输出。
- **128K 输出令牌：** Opus 4.6 支持高达 128K `max_tokens`，但对于大 `max_tokens`，SDK 需要流式传输以避免 HTTP 超时。使用 `.stream()` 配合 `.get_final_message()` / `.finalMessage()`。
- **工具调用 JSON 解析（Opus 4.6）：** Opus 4.6 可能在工具调用 `input` 字段中产生不同的 JSON 字符串转义（例如，Unicode 或反斜杠转义）。始终使用 `json.loads()` / `JSON.parse()` 解析工具输入——永远不要对序列化输入进行原始字符串匹配。
- **结构化输出（所有模型）：** 在 `messages.create()` 上使用 `output_config: {format: {...}}` 而不是已弃用的 `output_format` 参数。这是一个通用的 API 更改，不是 4.6 特定的。
- **不要重新实现 SDK 功能：** SDK 提供高级辅助——使用它们而不是从头开始构建。具体来说：使用 `stream.finalMessage()` 而不是将 `.on()` 事件包装在 `new Promise()` 中；使用类型化异常类（`Anthropic.RateLimitError` 等）而不是字符串匹配错误消息；使用 SDK 类型（`Anthropic.MessageParam`、`Anthropic.Tool`、`Anthropic.Message` 等）而不是重新定义等效接口。
- **不要为 SDK 数据结构定义自定义类型：** SDK 导出所有 API 对象的类型。使用 `Anthropic.MessageParam` 表示消息，`Anthropic.Tool` 表示工具定义，`Anthropic.ToolUseBlock` / `Anthropic.ToolResultBlockParam` 表示工具结果，`Anthropic.Message` 表示响应。定义自己的 `interface ChatMessage { role: string; content: unknown }` 重复了 SDK 已经提供的内容并失去类型安全性。
- **报告和文档输出：** 对于生成报告、文档或可视化的任务，代码执行沙箱预安装了 `python-docx`、`python-pptx`、`matplotlib`、`pillow` 和 `pypdf`。Claude 可以生成格式化文件（DOCX、PDF、图表）并通过 Files API 返回它们——对于"报告"或"文档"类型的请求，请考虑这一点，而不是纯标准输出文本。
