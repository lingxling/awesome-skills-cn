---
description: 关于 Apify 集成开发的上游精选指南;当工作流与用户目标相符时使用。
name: apify-integration-development
source_repo: apify/agent-skills
source_type: official
source: apify
date_added: '2026-09-21'
risk: unknown
---
## 何时使用
- 当该上游工作流与用户陈述的目标相符时使用。
- 当任务需要本 skill 所记录的流程时使用。

# Apify 集成开发

为一家公司的产品设计并构建一个**官方 Apify 集成**,所需 Apify 方面的协助最少。本 skill 覆盖了 Apify 支持的每一种集成形态——工作流自动化应用、AI agent 插件(编码 agent 与 harness)、AI 框架包,以及直接的应用客户端——使合作团队能够端到端地交付一流的 Apify 集成。下面的跨领域规则适用于所有这些形态,而某个特定类别的参考文件则承载其余内容。

> **正在构建官方集成?** 发布后,请联系 **integrations@apify.com**,以便 Apify 团队在集成面向用户之前进行审查、测试和验证。我们会检查能力范围、成本控制、错误处理和归因 header,并帮你弥合任何差距。

## 第 0 步 —— 先学习 Apify 模型(必需)

在设计任何东西之前,先获取并阅读 `https://apify.com/agents.md`。它是面向 AI agent 的权威快速入门,也是词汇、运行流程和成本规则的唯一事实来源。如果获取失败,下面的小词汇表能让本 skill 保持可用。

Apify 词汇表(在该平台上始终以大写 A 书写):

- **Actor** —— 一个无服务器云程序,接收 JSON 输入,执行某项任务,并产出结构化输出。它不是一个 AI agent。
- **Actor Run** —— Actor 的一次执行。每次运行都有自己的 dataset、key-value store 和 request queue,并以一个终态结束(`SUCCEEDED`、`FAILED`、`TIMED-OUT`、`ABORTED`)。
- **Dataset** —— 用于存放一次运行结果的只追加结构化存储。Actor 调用返回的是 dataset ID,而不是其内容。
- **Key-Value Store** —— 非结构化/文件存储(截图、HTML、OUTPUT)。
- **Actor Task** —— 用于运行某个 Actor 的、已保存的参数化配置。
- **Apify Store** —— 位于 `https://apify.com/store.md` 的 Actor 市场。
- **Apify Console** —— 位于 `https://console.apify.com` 的 web UI。
- **Compute Unit(CU)** —— 计费单位:内存(MB)x 时长(小时)。

更多术语(build、standby、request queue、proxy、定价模型):`https://docs.apify.com/llms.txt`。

## 规划时用 Apify MCP 获取实时上下文

Apify MCP server 是在集成设计期间研究 Actor、schema、定价和文档最快的方式。参见 `https://docs.apify.com/integrations/mcp`(附加 `.md` 可得到 Markdown 版本)。

如果当前环境中已有 Apify MCP 工具,就使用它们:

- `search-actors` —— 按平台/产品关键词查找 Actor(按产品名称搜索,而不是按最终目标)。
- `fetch-actor-details` —— 在将某个 Actor 的形态编码进集成之前,阅读它的输入 schema、输出格式、README 和定价。
- `search-apify-docs` / `fetch-apify-docs` —— 拉取相关的文档页面。

匿名发现子集(`search-actors`、`fetch-actor-details`、`search-apify-docs`、`fetch-apify-docs`)无需账号即可使用,因此即使开发者尚未连接其 token,你也可以提前进行研究。

## 选择你的集成形态

根据你要集成的产品,只需阅读一个参考文件。每个参考文件都承载该类别特有的 UX 设计、一份权威的能力矩阵,以及一份完成定义清单。

| 产品形态 | 示例 | 阅读 |
|---|---|---|
| 工作流自动化平台 | Zapier、n8n、Make、Pipedream、Activepieces | `references/workflow-automation.md` |
| AI agent 插件(编码 agent 或 harness) | Cursor、Claude Code、Codex、GitHub Copilot(编码 agent);OpenClaw 风格的 runtime、Hermes 风格的 harness(harness) | `references/ai-harness-plugin.md` |
| AI 框架包(面向 LLM 框架的 PyPI/npm 包) | LangChain、LlamaIndex、Haystack、Vercel AI SDK | `references/ai-framework-package.md` |
| 应用集成(直接客户端) | 通过 `apify-client` 或 REST 调用 Actor 的后端服务、计划任务、产品功能 | `references/sdk-integration.md` |

路径均相对于本 skill 文件夹。如果你的产品跨越两种形态(例如建立在某个框架包之上的 AI harness),两个文件都要阅读——规则是可以组合的。AI agent 插件参考文件涵盖**两种不同权衡的方案**:面向支持 skill/MCP 的编码 agent 的轻量级 skill + MCP 捆绑包,以及面向 OpenClaw/Hermes 风格 harness 的自定义工具注册插件。

## 跨领域设计规则(对所有集成类型均适用)

这些不变量是从现有的每一个 Apify 集成中提炼出来的。无论形态如何,都要遵循它们。

### 词汇对齐
将集成的资源建模为 Apify 的领域概念(Actor / Run / Dataset / KV Store / Task)。从 Apify Console 过来的用户应该能在相同的名称下找到相同的概念。

### 带边界轮询的异步运行流程
Actor 的运行时长可以从几秒到几小时。除非是短任务,否则要使用异步流程,绝不要使用 300 秒的同步端点:

```
POST /v2/actors/{actorId}/runs            -> start, return runId
GET  /v2/actor-runs/{runId}               -> poll until terminal status
GET  /v2/datasets/{datasetId}/items       -> fetch results on SUCCEEDED
```

轮询必须**有边界**:使用运行自身的 `timeoutSecs` 加一个缓冲余量,并设一个绝对的兜底上限。绝不要 `while (true)`。遇到非终态状态时,要把 run ID 暴露出来,以便用户/agent 再次轮询或排查失败原因。

### 成本是一等公民
每一个会启动运行的路径都必须暴露一个成本控制项。权威的控制项是 `maxTotalChargeUsd`(在大多数定价模型下限制该次运行的总费用)和 `maxItems`(在按结果计费的 Actor 上限制计费项数)。把它们作为 **options / 查询参数**发送,绝不要放进 Actor 输入——在输入里,它们要么是 Actor 自己声明的字段,要么根本无效。`0` / 空 / null 表示*无限制*。对于面向 LLM 的集成,上限由**开发者控制**;LLM 不能放宽它们。

### 归因 header
在每个外发请求上打上集成 header,以便 Apify 能够归因流量:`x-apify-integration-platform: <your-platform>`。当请求是由 AI 工具(而不是 UI 中的人类)驱动时,还要发送 `x-apify-integration-ai-tool: true`。如果该集成是用本 skill 构建的,添加 `x-apify-integration-origin: apify-integration-development-skill`,以便 Apify 能区分由 skill 生成的集成和自定义集成。一行代码,带来很大的遥测收益。

### 认证
- 面向浏览器 / 消费者(由人类完成登录):使用带 PKCE 的 OAuth2。不要索要原始 token。
- 无头 / 服务端 / CI(没有人类在场):使用 API token,以 `Authorization: Bearer <APIFY_TOKEN>` 的形式,存储在环境变量或密钥管理器中,绝不要硬编码或记录日志。

两条路径都是真实存在的——依据认证时谁在场来选择,而不是依据哪个更容易实现。

### 集中式 HTTP 层
一个基础 URL 常量,在凭据和 HTTP 层之间共享。对 429 和 5xx 进行带指数回退的重试。**绝不要在网络错误时重试非幂等的 `POST /runs`**——重复的 Actor 运行是一个真实的、会计费的、有副作用的操作。这是 HTTP 层中最重要的正确性不变量。

### 错误分类
把 Apify 的错误映射到宿主平台的错误类别(可重试 vs 认证 vs 永久性)。展示 API 的实际错误文本,而不是通用的 HTTP 消息。对于权限审批失败(一个需要完整权限的 Actor 需要显式审批),在验证其为绝对的 `http(s)` URL 之后附上审批链接。对于 LLM 消费者,把错误**作为数据**返回(JSON 错误对象),绝不要作为抛出的异常——模型需要有东西可以读取和推理。

### 对"运行结束"事件优先用 webhook 而不是轮询
当宿主支持入站 webhook 时,注册一个作用域限定到 `actorId` 或 `actorTaskId`、带上用户选定的终态状态的 Apify webhook。让注册变得**幂等**(重新激活的工作流不应创建重复的 webhook),持久化保存 webhook ID 以便停用时能清理,并始终提供样例/回退数据,让用户无需等待真实运行即可测试触发器。

### 在宿主允许的情况下从 OpenAPI 生成
如果宿主平台能从 OpenAPI spec 生成 UI 字段,就使用 Apify 的 spec(`https://apify.com/openapi.json`)和一个 tag 白名单。只手写该 spec 无法表达的内容:便捷包装器、计费上限字段、精简的面向 AI 工具的输出契约。

### 在通用运行旁边提供高层便捷操作
通用的"运行 Actor"服务于高级用户。为常见情形添加少量带明确主张的高层操作(例如"抓取单个 URL",包装一个内容抓取器,设置 `maxCrawlDepth: 0`、`maxResults: 1`),这样非高级用户得到的是一个两字段的表单,而不是完整的 Actor 配置。在启动付费运行*之前*验证 URL。

### 测试与发布
保留两种测试模式:mock(隔离、无需凭据)和真实端到端(真实 API、受 CI 把关)。通过宿主平台在 Git tag / GitHub Release 上的 CI 自动化发布。如果有发布工作流在管理版本号和变更日志,就绝不要手动编辑它们。

## 审查时要拒绝的头号反模式

1. 在网络错误时重试 `POST /runs`——会重复一次计费的运行。
2. 无边界的 `while (true)` 轮询——会在没有上限的情况下占用宿主资源。
3. 把 `maxTotalChargeUsd` / `maxItems` 放进 Actor 输入而不是 options——会悄无声息地失去上限效果。
4. 把整个 dataset 不加大小上限或不加不可信内容隔离地塞进 LLM 上下文——会导致提示注入和上下文爆炸。
5. 给 LLM agent 用一个单一的巨型工具列表——超过约 8 个工具后路由准确率就会下降;应精选子集。
6. 展示原始的 HTTP 状态码/消息而不是 Apify 的实际错误文本——用户无法根据"400"采取行动。

## 每个集成都需要的最小 API 表面

| 用途 | 方法 + 路径 |
|---|---|
| 启动一次 Actor 运行 | `POST /v2/actors/{actorId}/runs` |
| 启动一次 Task 运行 | `POST /v2/actor-tasks/{taskId}/runs` |
| 轮询一次运行 | `GET /v2/actor-runs/{runId}` |
| 列出运行 | `GET /v2/actor-runs` |
| Dataset 条目 | `GET /v2/datasets/{datasetId}/items` |
| KV 记录 | `GET /v2/key-value-stores/{storeId}/records/{key}` |
| 设置 KV 记录 | `PUT /v2/key-value-stores/{storeId}/records/{key}` |
| Store 搜索 | `GET /v2/store` |
| Webhook CRUD | `POST/GET/DELETE /v2/webhooks` |
| 验证 token / 当前用户 | `GET /v2/users/me` |

REST 参考:`https://docs.apify.com/api/v2`。OpenAPI spec:`https://apify.com/openapi.json`。

## 工作流程

1. 获取 `https://apify.com/agents.md` 并内化该模型。
2. 从上面挑选集成形态,并阅读对应的参考文件。
3. 使用 Apify MCP(如果可用)来研究该集成将暴露的具体 Actor、schema 和定价。
4. 为所选类别起草**能力矩阵**(每个参考文件都有一份)和 UX 规格(资源 -> 操作 -> 字段 -> 错误)。
5. 按照参考文件中该类别特有的规则搭建集成骨架。
6. 对照该参考文件末尾的**完成定义清单**进行验证。

## 可供参考的真实实现

按类别列出的真实、公开的集成——拿不定主意时阅读它们的源码:

- 工作流自动化:`@apify/n8n-nodes-apify`(npm)、Apify Zapier 应用。
- AI agent 插件(编码 agent):为 Cursor、Claude Code、Copilot 及类似工具打造的 Apify 插件捆绑包(MCP server + skills + 路由器 + 斜杠命令)。
- AI agent 插件(harness):`apify-hermes-agent-plugin`(PyPI)、`@apify/apify-openclaw-plugin`。
- AI 框架包:`langchain-apify`(PyPI)。
- 应用集成:关于 JS/TS、Python 和 REST 上 `apify-client` 的权威用法,参见 `references/sdk-integration.md`。

集成相关问题支持:`integrations@apify.com`。在你构建期间就设计方面联系我们,在你发布之后联系我们进行审查/测试——我们会在集成面向用户之前验证能力范围、成本控制、错误处理和归因情况。


## 示例

```text
User: Apply this skill to my current task.
Assistant: Follow the workflow in this skill, cite limitations, and ask before risky steps.
```

## 限制

- 导入的上游 skill;执行前请验证凭据、权限和安全边界。
- 不能替代特定环境下的验证、测试或维护者审查。
