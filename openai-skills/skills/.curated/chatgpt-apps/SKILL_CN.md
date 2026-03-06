---
name: chatgpt-apps
description: 构建、脚手架、重构和故障排除 ChatGPT Apps SDK 应用程序，这些应用程序结合了 MCP 服务器和小组件 UI。当 Codex 需要设计工具、注册 UI 资源、连接 MCP Apps 桥或 ChatGPT 兼容性 API、应用 Apps SDK 元数据或 CSP 或域设置，或生成与文档一致的项目脚手架时使用。通过首先调用 openai-docs 技能或 OpenAI 开发者文档 MCP 工具来生成代码，优先使用文档优先的工作流程。
---

# ChatGPT Apps

## 概述

使用文档优先、示例优先的工作流程脚手架 ChatGPT Apps SDK 实现，然后生成遵循当前 Apps SDK 和 MCP Apps 桥模式的代码。

使用此技能生成：

- 主要应用程序原型分类和仓库形状决策
- 工具计划（名称、架构、注释、输出）
- 上游起点建议（官方示例、ext-apps 示例或本地回退脚手架）
- MCP 服务器脚手架（资源注册、工具处理程序、元数据）
- 小组件脚手架（MCP Apps 桥优先，`window.openai` 兼容性/扩展其次）
- 可重用的 Node + `@modelcontextprotocol/ext-apps` 启动脚手架，用于低依赖性回退
- 针对最小工作仓库合同的验证报告
- 本地开发和连接器设置步骤
- 应用程序功能的简短利益相关者摘要（当请求时）

## 强制文档优先工作流程

在构建或更改 ChatGPT Apps SDK 应用程序时，首先使用 `$openai-docs`。

1. 调用 `$openai-docs`（首选）或直接调用 OpenAI 文档 MCP 服务器。
2. 在编写代码之前获取当前 Apps SDK 文档，特别是（基线页面）：
   - `apps-sdk/build/mcp-server`
   - `apps-sdk/build/chatgpt-ui`
   - `apps-sdk/build/examples`
   - `apps-sdk/plan/tools`
   - `apps-sdk/reference`
3. 在脚手架新应用程序或生成首次实现时获取 `apps-sdk/quickstart`，并在从头发明脚手架之前检查官方示例仓库/页面。
4. 当任务包括本地 ChatGPT 测试、托管或公开发布时，获取部署/提交文档：
   - `apps-sdk/deploy`
   - `apps-sdk/deploy/submission`
   - `apps-sdk/app-submission-guidelines`
5. 在解释设计选择或生成的脚手架时，引用您使用的文档 URL。
6. 当它们不同时，优先考虑当前文档指导而不是较旧的仓库模式，并明确调用兼容性别名。
7. 如果文档搜索超时或返回较差的匹配项，则通过 URL 直接获取规范的 Apps SDK 页面并继续；不要让搜索失败阻止脚手架。

如果 `$openai-docs` 不可用，请使用：

- `mcp__openaiDeveloperDocs__search_openai_docs`
- `mcp__openaiDeveloperDocs__fetch_openai_doc`

阅读 `references/apps-sdk-docs-workflow.md` 以获取建议的文档查询和紧凑清单。
阅读 `references/app-archetypes.md` 以在选择示例或脚手架之前将请求分类为少量支持的应用程序形状。
阅读 `references/repo-contract-and-validation.md` 以在生成或审查仓库时使输出保持在稳定的"工作应用程序"合同内。
阅读 `references/search-fetch-standard.md` 以在应用程序是连接器类型、仅数据、同步导向或旨在与公司知识或深度研究良好工作时使用。
阅读 `references/upstream-example-workflow.md` 以在启动绿地应用程序或决定是否调整上游示例或使用本地回退脚手架时使用。
阅读 `references/window-openai-patterns.md` 以在任务需要 ChatGPT 特定的小组件行为或翻译使用包装器特定 `app.*` 助手的仓库示例时使用。

## 提示指导

使用明确将此技能与 `$openai-docs` 配对的提示，以便生成的脚手架建立在当前文档的基础上。

首选提示模式：

- `Use $chatgpt-apps with $openai-docs to scaffold a ChatGPT app for <use case> with a <TS/Python> MCP server and <React/vanilla> widget.`
- `Use $chatgpt-apps with $openai-docs to adapt the closest official Apps SDK example into a ChatGPT app for <use case>.`
- `Use $chatgpt-apps and $openai-docs to refactor this Apps SDK demo into a production-ready structure with tool annotations, CSP, and URI versioning.`
- `Use $chatgpt-apps with $openai-docs to plan tools first, then generate MCP server and widget code.`

响应时，在编码之前询问或推断这些输入：

- 用例和主要用户流程
- 只读与变异工具
- 演示与生产目标
- 私有/内部使用与公共目录提交
- 后端语言和 UI 堆栈
- 身份验证要求
- CSP 允许列表的外部 API 域
- 托管目标和本地开发方法
- 组织所有权/验证准备情况（用于提交任务）

## 在选择代码之前对应用程序进行分类

在选择示例、仓库形状或脚手架之前，将请求分类为一个主要原型并说明它。

- `tool-only`
- `vanilla-widget`
- `react-widget`
- `interactive-decoupled`
- `submission-ready`

推断原型，除非缺少的细节真正阻止。使用原型来选择：

- 是否需要 UI
- 是否保留拆分的 `server/` + `web/` 布局
- 是否优先考虑官方 OpenAI 示例、ext-apps 示例或本地回退脚手架
- 哪些验证检查最重要
- `search` 和 `fetch` 是否应为默认的只读工具表面

阅读 `references/app-archetypes.md` 以获取决策规则。

## 默认起点顺序

对于绿地应用程序，按顺序优先考虑这些起点：

1. **官方 OpenAI 示例**，当接近的示例已经匹配请求的堆栈或交互模式时。
2. **版本匹配的 `@modelcontextprotocol/ext-apps` 示例**，当用户需要更低级别或更可移植的 MCP Apps 基线时。
3. **`scripts/scaffold_node_ext_apps.mjs`**，仅当没有接近的示例适合时，用户想要一个微小的 Node + 原生启动器，或网络访问/示例检索不可取时。

如果接近的上游示例已经存在，不要从头生成大型自定义脚手架。
复制最小的匹配示例，删除不相关的演示代码，然后将其修补为当前文档和用户请求。

## 构建工作流程

### 0. 对应用程序原型进行分类

在规划工具或选择起点之前，选择一个主要原型。

- 优先考虑单个主要原型而不是混合几个。
- 如果请求广泛，推断仍然可以满足它的最小原型。
- 仅当用户要求公开发布、目录提交或审查就绪的部署时，才升级到 `submission-ready`。
- 在响应中调用所选原型，以便用户可以在需要时早期纠正它。

### 1. 在代码之前规划工具

从用户意图定义工具表面区域。

- 每个工具使用一个作业。
- 编写以"Use this when..."行为提示开头的工具描述。
- 使输入明确且对机器友好（枚举、必填字段、边界）。
- 决定每个工具是仅数据、仅渲染还是两者。
- 准确设置注释（`readOnlyHint`、`destructiveHint`、`openWorldHint`；当为 true 时添加 `idempotentHint`）。
- 如果应用程序是连接器类型、仅数据、同步导向或旨在用于公司知识或深度研究，则默认为标准的 `search` 和 `fetch` 工具，而不是发明自定义的只读等效项。
- 对于教育/演示应用程序，每个工具优先考虑一个概念，以便模型可以干净地选择正确的示例。
- 按学习目标对演示工具进行分组：数据进入小组件、小组件操作返回到对话或工具、主机/布局环境信号以及生命周期/流式传输行为。

当 `search` 和 `fetch` 可能相关时，阅读 `references/search-fetch-standard.md`。

### 2. 选择应用程序架构

选择适合目标的最简单结构。

- 对快速原型、研讨会或概念证明使用**最小演示模式**。
- 对生产 UX 使用**解耦的数据/渲染模式**，以便小组件不会在每次工具调用时重新渲染。

对非平凡应用程序优先考虑解耦模式：

- 数据工具返回可重用的 `structuredContent`。
- 渲染工具附加 `_meta.ui.resourceUri` 和可选的 `_meta["openai/outputTemplate"]`。
- 渲染工具描述说明先决条件（例如，"Call `search` first"）。

### 2a. 当适合时从上游示例开始

当它们接近请求的应用程序时，默认对绿地工作使用上游示例。

- 首先检查官方 OpenAI 示例以获取面向 ChatGPT 的应用程序、经过优化的 UI 模式、React 组件、文件上传流程、模态流程或类似于文档示例的应用程序。
- 当请求更接近原始 MCP Apps 桥/服务器接线或版本匹配的包模式比 ChatGPT 特定优化更重要时，使用 `@modelcontextprotocol/ext-apps` 示例。
- 选择最小的匹配示例并仅复制相关文件；不要原样移植整个展示应用程序。
- 复制后，将示例与您获取的当前文档协调：工具名称/描述、注释、`_meta.ui.*`、CSP、URI 版本控制和本地运行说明。
- 用一句话说明您选择了哪个示例以及为什么。

阅读 `references/upstream-example-workflow.md` 以获取选择和调整规则。

### 2b. 当低依赖性回退有帮助时使用启动器脚本

仅当用户想要快速的绿地 Node 启动器且 vanilla HTML 小组件可接受，并且没有上游示例是更好的起点时，才使用 `scripts/scaffold_node_ext_apps.mjs`。

- 仅在获取当前文档后运行它，然后将生成的文件与您获取的文档协调。
- 如果您选择脚本而不是上游示例，请说明为什么回退对该请求更好。
- 当存在接近的官方示例、用户已有现有的应用程序结构、他们需要非 Node 堆栈、他们明确想要 React 优先或他们只想要计划/审查而不是代码时，跳过它。
- 该脚本生成最小的 `@modelcontextprotocol/ext-apps` 服务器以及默认使用 MCP Apps 桥的 vanilla HTML 小组件。
- 生成的小组件将后续消息保留在标准 `ui/message` 桥上，并且仅对可选的主机信号/扩展使用 `window.openai`。
- 运行它后，将生成的输出修补为匹配当前文档和用户请求：调整工具名称/描述、注释、资源元数据、URI 版本控制和 README/运行说明。

### 3. 脚手架 MCP 服务器

生成一个服务器，该服务器：

- 使用 MCP Apps UI MIME 类型（`text/html;profile=mcp-app`）或 SDK 常量（`RESOURCE_MIME_TYPE`）注册小组件资源/模板，当使用 `@modelcontextprotocol/ext-apps/server` 时
- 注册具有清晰名称、架构、标题和描述的工具
- 有意返回 `structuredContent`（模型 + 小组件）、`content`（模型叙述）和 `_meta`（仅小组件数据）
- 保持处理程序等幂或明确记录非等幂行为
- 在 ChatGPT 中有帮助时包含工具状态字符串（`openai/toolInvocation/*`）

保持 `structuredContent` 简洁。将大型或敏感的小组件仅有效负载移动到 `_meta`。

### 4. 脚手架小组件 UI

首先使用 MCP Apps 桥以实现可移植性，然后当它们实质性地改善 UX 时添加 ChatGPT 特定的 `window.openai` API。

- 监听 `ui/notifications/tool-result`（通过 `postMessage` 的 JSON-RPC）
- 从 `structuredContent` 渲染
- 对组件发起的工具调用使用 `tools/call`
- 仅当 UI 状态应更改模型看到的内容时才使用 `ui/update-model-context`

对兼容性和扩展（文件上传、模态、显示模式等）使用 `window.openai`，而不是作为新应用程序的唯一集成路径。

#### API 表面防护栏

- 一些示例用 `app` 对象包装桥（例如，`@modelcontextprotocol/ext-apps/react`）并公开辅助名称，如 `app.sendMessage()`、`app.callServerTool()`、`app.openLink()` 或主机 getter 方法。
- 将这些包装器视为实现细节或便利层，而不是默认要教授的规范公共 API。
- 对于面向 ChatGPT 的指导，优先考虑当前记录的表面：`window.openai.callTool(...)`、`window.openai.sendFollowUpMessage(...)`、`window.openai.openExternal(...)`、`window.openai.requestDisplayMode(...)` 和直接全局变量，如 `window.openai.theme`、`window.openai.locale`、`window.openai.displayMode`、`window.openai.toolInput`、`window.openai.toolOutput`、`window.openai.toolResponseMetadata` 和 `window.openai.widgetState`。
- 如果您从仓库示例引用包装器辅助，请将它们映射回记录的 `window.openai` 或 MCP Apps 桥原语，并调用包装器不是规范 API 表面。
- 对包装器到规范的映射和 React 辅助提取模式使用 `references/window-openai-patterns.md`。

### 5. 添加资源元数据和安全性

在小组件资源/模板上故意设置资源元数据：

- `_meta.ui.csp` 具有精确的 `connectDomains` 和 `resourceDomains`
- `_meta.ui.domain` 用于应用提交就绪的部署
- `_meta.ui.prefersBorder`（或在需要时使用 OpenAI 兼容性别名）
- 可选的 `openai/widgetDescription` 以减少冗余叙述

除非 iframe 嵌入是产品的核心，否则避免 `frameDomains`。

### 5a. 强制执行最小工作仓库合同

每个生成的仓库在您认为完成之前都应满足一个小而稳定的合同。

- 仓库形状匹配所选原型。
- MCP 服务器和工具连接到可访问的 `/mcp` 端点。
- 工具具有清晰的描述、准确的注释和需要的 UI 元数据。
- 连接器类型、仅数据、同步导向和公司知识风格的应用程序在相关时使用标准的 `search` 和 `fetch` 工具形状。
- 小组件在存在 UI 时正确使用 MCP Apps 桥。
- 仓库包含足够的脚本或命令，以便用户可以在本地运行和检查它。
- 响应明确说明运行了什么验证以及没有运行什么。

阅读 `references/repo-contract-and-validation.md` 以获取详细清单和验证阶梯。

### 6. 验证本地循环

针对最小工作仓库合同进行验证，而不仅仅是"是否创建了文件"。

- 首先运行最低成本的检查：
  - 静态合同审查
  - 语法或编译检查（当可行时）
  - 本地 `/mcp` 健康检查（当可行时）
- 然后向上移动到运行时检查：
  - 在 MCP Inspector 中验证工具描述符和小组件渲染
  - 通过 HTTPS 隧道在 ChatGPT 开发者模式中测试应用程序
  - 练习重试和重复的工具调用以确认等幂行为
  - 检查主机事件和后续工具调用后的小组件更新
- 如果您只交付脚手架并且不安装依赖项，仍然运行低成本检查并明确说明您没有运行什么。

阅读 `references/repo-contract-and-validation.md` 以获取验证阶梯。

### 7. 在 ChatGPT 中连接和测试（开发者模式）

对于本地开发，包括明确的 ChatGPT 设置步骤（不仅仅是代码/运行命令）。

- 在 `http://localhost:<port>/mcp` 上本地运行 MCP 服务器
- 使用公共 HTTPS 隧道（例如 `ngrok http <port>`）暴露本地服务器
- 从 ChatGPT 连接时使用隧道的 HTTPS URL 加上 `/mcp` 路径
- 在 ChatGPT 中，在 **设置 → 应用程序和连接器 → 高级设置** 下启用开发者模式
- 在 ChatGPT 应用程序设置中，为远程 MCP 服务器创建新应用程序并粘贴公共 MCP URL
- 告诉用户在 MCP 工具/元数据更改后刷新应用程序，以便 ChatGPT 重新加载最新的描述符

注意：一些文档/屏幕截图仍然使用较旧的"连接器"术语。在给出分步说明时优先考虑当前产品措辞（"应用程序"），同时承认两个标签。

### 8. 规划生产托管和部署

当用户要求部署或准备启动时，为 MCP 服务器（以及如果单独托管的小组件资产）生成托管指导。

- 在稳定的公共 HTTPS 端点（不是隚道）后面托管，并具有可靠的 TLS
- 在 `/mcp` 上保留低延迟流式传输行为
- 在仓库外部配置机密（环境变量 / 机密管理器）
- 为工具调用添加日志记录、请求延迟跟踪和错误可见性
- 添加基本可观察性（CPU、内存、请求量）和故障排除路径
- 在提交之前在 ChatGPT 开发者模式中重新测试托管端点

### 9. 准备提交和发布（仅公共应用程序）

仅当用户打算公共目录列表时包括这些步骤。

- 使用 `apps-sdk/deploy/submission` 获取提交流程，使用 `apps-sdk/app-submission-guidelines` 获取审查要求
- 将私有/内部应用程序保留在开发者模式中而不是提交
- 在提交工作之前确认组织验证和所有者角色先决条件
- 确保 MCP 服务器使用公共生产端点（没有 localhost/测试 URL）并配置了提交就绪的 CSP
- 准备提交工件：应用程序元数据、徽标/屏幕截图、隐私策略 URL、支持联系人、测试提示/响应、本地化信息
- 如果需要身份验证，包括审查安全的演示凭据并端到端测试登录路径
- 在平台仪表板中提交审查，监控审查状态，并仅在批准后发布

## 交互状态指导

当应用程序具有长生命周期小组件状态、重复交互或组件发起的工具调用（例如，游戏、棋盘、地图、仪表板、编辑器）时，阅读 `references/interactive-state-sync-patterns.md`。

使用它来选择以下内容的模式：

- 状态快照加上单调事件令牌（`stateVersion`、`resetCount` 等）
- 等幂重试安全处理程序
- `structuredContent` 与 `_meta` 分区
- 首先使用 MCP Apps 桥更新流程并具有可选的 `window.openai` 兼容性
- 用于更复杂的交互应用程序的解耦数据/渲染工具架构

## 输出期望

使用此技能脚手架代码时，除非用户另有要求，否则按此顺序生成输出：

- 对于直接脚手架请求，不要停在计划：给出简短计划，然后立即创建文件。

1. 选择的主要应用程序原型以及为什么
2. 工具计划和架构选择（最小与解耦）
3. 选择的上游起点（官方示例、ext-apps 示例或本地回退脚手架）以及为什么
4. 从 `$openai-docs` 使用的文档页面/URL
5. 要创建或修改的文件树
6. 实现（服务器 + 小组件）
7. 针对最小工作仓库合同执行的验证
8. 本地运行/测试说明（包括隚道 + ChatGPT 开发者模式应用程序设置）
9. 托管/托管指导（如果请求或暗示）
10. 提交就绪清单（用于公开发布请求）
11. 风险、差距和后续改进

## 引用

- `references/app-archetypes.md` 用于将请求分类为少量支持的应用程序形状
- `references/apps-sdk-docs-workflow.md` 用于文档查询、页面目标和代码生成清单
- `references/interactive-state-sync-patterns.md` 用于有状态或高度交互的小组件应用程序的可重用模式
- `references/repo-contract-and-validation.md` 用于最小工作仓库合同和轻量级验证阶梯
- `references/search-fetch-standard.md` 用于何时以及如何默认为标准的 `search` 和 `fetch` 工具
- `references/upstream-example-workflow.md` 用于在官方示例、ext-apps 示例和本地回退脚手架之间选择
- `references/window-openai-patterns.md` 用于 ChatGPT 特定扩展、包装器 API 翻译和 React 辅助模式
- `scripts/scaffold_node_ext_apps.mjs` 用于最小的 Node + `@modelcontextprotocol/ext-apps` 回退启动脚手架
