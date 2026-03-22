---
name: mcp-builder
description: 指导创建高质量的 MCP (Model Context Protocol) 服务器，使 LLM 能够通过设计良好的工具与外部服务交互。当构建 MCP 服务器以集成外部 API 或服务时使用，无论是使用 Python (FastMCP) 还是 Node/TypeScript (MCP SDK)。
license: 完整条款见 LICENSE.txt
---

# MCP 服务器开发指南

## 概述

要创建高质量的 MCP (Model Context Protocol) 服务器，使 LLM 能够有效地与外部服务交互，请使用此技能。MCP 服务器提供工具，允许 LLM 访问外部服务和 API。MCP 服务器的质量取决于它如何有效地使 LLM 使用提供的工具完成实际任务。

---

# 流程

## 🚀 高级工作流

创建高质量的 MCP 服务器涉及四个主要阶段：

### 阶段 1：深入研究和规划

#### 1.1 理解以代理为中心的设计原则

在开始实现之前，通过审查以下原则了解如何为 AI 代理设计工具：

**为工作流程构建，而不仅仅是 API 端点：**
- 不要简单地包装现有的 API 端点 - 构建深思熟虑、高影响力的工作流工具
- 整合相关操作（例如，`schedule_event` 同时检查可用性并创建事件）
- 专注于启用完整任务的工具，而不仅仅是单个 API 调用
- 考虑代理实际需要完成的工作流程

**针对有限上下文进行优化：**
- 代理具有受限的上下文窗口 - 让每个 token 都有价值
- 返回高信号信息，而不是详尽的数据转储
- 提供 "简洁" 与 "详细" 响应格式选项
- 默认为人类可读的标识符，而不是技术代码（名称而不是 ID）
- 将代理的上下文预算视为稀缺资源

**设计可操作的错误消息：**
- 错误消息应指导代理朝向正确的使用模式
- 建议具体的后续步骤："尝试使用 filter='active_only' 来减少结果"
- 使错误具有教育意义，而不仅仅是诊断
- 通过清晰的反馈帮助代理学习正确的工具使用

**遵循自然任务细分：**
- 工具名称应反映人类如何思考任务
- 使用一致的前缀对相关工具进行分组，以提高可发现性
- 围绕自然工作流程设计工具，而不仅仅是 API 结构

**使用评估驱动的开发：**
- 尽早创建现实的评估场景
- 让代理反馈驱动工具改进
- 快速原型设计并根据实际代理性能进行迭代

#### 1.3 研究 MCP 协议文档

**获取最新的 MCP 协议文档：**

使用 WebFetch 加载：`https://modelcontextprotocol.io/llms-full.txt`

此综合文档包含完整的 MCP 规范和指南。

#### 1.4 研究框架文档

**加载并阅读以下参考文件：**

- **MCP 最佳实践**：[📋 查看最佳实践](./reference/mcp_best_practices.md) - 所有 MCP 服务器的核心指南

**对于 Python 实现，还需加载：**
- **Python SDK 文档**：使用 WebFetch 加载 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- [🐍 Python 实现指南](./reference/python_mcp_server.md) - Python 特定的最佳实践和示例

**对于 Node/TypeScript 实现，还需加载：**
- **TypeScript SDK 文档**：使用 WebFetch 加载 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- [⚡ TypeScript 实现指南](./reference/node_mcp_server.md) - Node/TypeScript 特定的最佳实践和示例

#### 1.5 详尽研究 API 文档

要集成服务，请通读**所有**可用的 API 文档：
- 官方 API 参考文档
- 身份验证和授权要求
- 速率限制和分页模式
- 错误响应和状态码
- 可用的端点及其参数
- 数据模型和架构

**要收集全面的信息，根据需要使用网络搜索和 WebFetch 工具。**

#### 1.6 创建全面的实施计划

基于您的研究，创建详细的计划，包括：

**工具选择：**
- 列出最有价值的端点/操作来实现
- 优先考虑能够启用最常见和最重要用例的工具
- 考虑哪些工具一起工作以启用复杂的工作流程

**共享实用程序和助手：**
- 识别常见的 API 请求模式
- 计划分页助手
- 设计过滤和格式化实用程序
- 计划错误处理策略

**输入/输出设计：**
- 定义输入验证模型（Python 使用 Pydantic，TypeScript 使用 Zod）
- 设计一致的响应格式（例如，JSON 或 Markdown），以及可配置的详细程度（例如，详细或简洁）
- 为大规模使用（数千用户/资源）做计划
- 实现字符限制和截断策略（例如，25,000 个 token）

**错误处理策略：**
- 计划优雅的失败模式
- 设计清晰、可操作、对 LLM 友好的自然语言错误消息，提示进一步操作
- 考虑速率限制和超时场景
- 处理身份验证和授权错误

---

### 阶段 2：实现

现在您有了全面的计划，开始按照特定语言的最佳实践进行实现。

#### 2.1 设置项目结构

**对于 Python：**
- 创建单个 `.py` 文件或如果复杂则组织成模块（请参阅 [🐍 Python 指南](./reference/python_mcp_server.md)）
- 使用 MCP Python SDK 进行工具注册
- 定义用于输入验证的 Pydantic 模型

**对于 Node/TypeScript：**
- 创建适当的项目结构（请参阅 [⚡ TypeScript 指南](./reference/node_mcp_server.md)）
- 设置 `package.json` 和 `tsconfig.json`
- 使用 MCP TypeScript SDK
- 定义用于输入验证的 Zod 模式

#### 2.2 首先实现核心基础设施

**开始实现时，在实现工具之前创建共享实用程序：**
- API 请求助手函数
- 错误处理实用程序
- 响应格式化函数（JSON 和 Markdown）
- 分页助手
- 身份验证/令牌管理

#### 2.3 系统地实现工具

对于计划中的每个工具：

**定义输入模式：**
- 使用 Pydantic（Python）或 Zod（TypeScript）进行验证
- 包括适当的约束（最小/最大长度、正则表达式模式、最小/最大值、范围）
- 提供清晰、描述性的字段描述
- 在字段描述中包含多样化的示例

**编写全面的文档字符串/描述：**
- 工具功能的单行摘要
- 目的和功能的详细说明
- 带有示例的明确参数类型
- 完整的返回类型架构
- 使用示例（何时使用，何时不使用）
- 错误处理文档，概述给定特定错误时如何处理

**实现工具逻辑：**
- 使用共享实用程序避免代码重复
- 对所有 I/O 遵循 async/await 模式
- 实现适当的错误处理
- 支持多种响应格式（JSON 和 Markdown）
- 尊重分页参数
- 检查字符限制并适当截断

**添加工具注释：**
- `readOnlyHint`: true（对于只读操作）
- `destructiveHint`: false（对于非破坏性操作）
- `idempotentHint`: true（如果重复调用具有相同效果）
- `openWorldHint`: true（如果与外部系统交互）

#### 2.4 遵循特定语言的最佳实践

**此时，加载适当的语言指南：**

**对于 Python：加载 [🐍 Python 实现指南](./reference/python_mcp_server.md) 并确保：**
- 使用 MCP Python SDK 进行适当的工具注册
- 带有 `model_config` 的 Pydantic v2 模型
- 贯穿始终的类型提示
- 所有 I/O 操作的 Async/await
- 适当的导入组织
- 模块级常量（CHARACTER_LIMIT、API_BASE_URL）

**对于 Node/TypeScript：加载 [⚡ TypeScript 实现指南](./reference/node_mcp_server.md) 并确保：**
- 正确使用 `server.registerTool`
- 带有 `.strict()` 的 Zod 模式
- 启用 TypeScript 严格模式
- 无 `any` 类型 - 使用适当的类型
- 明确的 Promise<T> 返回类型
- 构建过程配置（`npm run build`）

---

### 阶段 3：审查和完善

初始实现后：

#### 3.1 代码质量审查

为确保质量，审查代码以确保：
- **DRY 原则**：工具之间无重复代码
- **可组合性**：共享逻辑提取到函数中
- **一致性**：相似操作返回相似格式
- **错误处理**：所有外部调用都有错误处理
- **类型安全**：完全类型覆盖（Python 类型提示，TypeScript 类型）
- **文档**：每个工具都有全面的文档字符串/描述

#### 3.2 测试和构建

**重要：** MCP 服务器是长期运行的进程，通过 stdio/stdin 或 sse/http 等待请求。直接在主进程中运行它们（例如，`python server.py` 或 `node dist/index.js`）会导致进程无限期挂起。

**安全测试服务器的方法：**
- 使用评估工具（见阶段 4）- 推荐方法
- 在 tmux 中运行服务器以将其保持在主进程之外
- 测试时使用超时：`timeout 5s python server.py`

**对于 Python：**
- 验证 Python 语法：`python -m py_compile your_server.py`
- 通过查看文件检查导入是否正确工作
- 手动测试：在 tmux 中运行服务器，然后在主进程中使用评估工具测试
- 或直接使用评估工具（它为 stdio 传输管理服务器）

**对于 Node/TypeScript：**
- 运行 `npm run build` 并确保它完成无错误
- 验证 dist/index.js 已创建
- 手动测试：在 tmux 中运行服务器，然后在主进程中使用评估工具测试
- 或直接使用评估工具（它为 stdio 传输管理服务器）

#### 3.3 使用质量检查表

要验证实现质量，从特定语言的指南中加载适当的检查表：
- Python：参见 [🐍 Python 指南](./reference/python_mcp_server.md) 中的 "质量检查表"
- Node/TypeScript：参见 [⚡ TypeScript 指南](./reference/node_mcp_server.md) 中的 "质量检查表"

---

### 阶段 4：创建评估

实现 MCP 服务器后，创建全面的评估以测试其有效性。

**加载 [✅ 评估指南](./reference/evaluation.md) 获取完整的评估指南。**

#### 4.1 理解评估目的

评估测试 LLM 是否能够有效地使用您的 MCP 服务器回答现实、复杂的问题。

#### 4.2 创建 10 个评估问题

要创建有效的评估，请按照评估指南中概述的过程：

1. **工具检查**：列出可用工具并了解其功能
2. **内容探索**：使用只读操作探索可用数据
3. **问题生成**：创建 10 个复杂、现实的问题
4. **答案验证**：自己解决每个问题以验证答案

#### 4.3 评估要求

每个问题必须：
- **独立**：不依赖于其他问题
- **只读**：只需要非破坏性操作
- **复杂**：需要多个工具调用和深入探索
- **现实**：基于人类关心的实际用例
- **可验证**：单一、清晰的答案，可以通过字符串比较验证
- **稳定**：答案不会随时间变化

#### 4.4 输出格式

创建具有以下结构的 XML 文件：

```xml
<evaluation>
  <qa_pair>
    <question>Find discussions about AI model launches with animal codenames. One model needed a specific safety designation that uses the format ASL-X. What number X was being determined for the model named after a spotted wild cat?</question>
    <answer>3</answer>
  </qa_pair>
<!-- More qa_pairs... -->
</evaluation>
```

---

# 参考文件

## 📚 文档库

在开发过程中根据需要加载这些资源：

### 核心 MCP 文档（首先加载）
- **MCP 协议**：从 `https://modelcontextprotocol.io/llms-full.txt` 获取 - 完整的 MCP 规范
- [📋 MCP 最佳实践](./reference/mcp_best_practices.md) - 通用 MCP 指南，包括：
  - 服务器和工具命名约定
  - 响应格式指南（JSON 与 Markdown）
  - 分页最佳实践
  - 字符限制和截断策略
  - 工具开发指南
  - 安全和错误处理标准

### SDK 文档（在阶段 1/2 期间加载）
- **Python SDK**：从 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md` 获取
- **TypeScript SDK**：从 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md` 获取

### 特定语言实现指南（在阶段 2 期间加载）
- [🐍 Python 实现指南](./reference/python_mcp_server.md) - 完整的 Python/FastMCP 指南，包括：
  - 服务器初始化模式
  - Pydantic 模型示例
  - 使用 `@mcp.tool` 进行工具注册
  - 完整的工作示例
  - 质量检查表

- [⚡ TypeScript 实现指南](./reference/node_mcp_server.md) - 完整的 TypeScript 指南，包括：
  - 项目结构
  - Zod 模式模式
  - 使用 `server.registerTool` 进行工具注册
  - 完整的工作示例
  - 质量检查表

### 评估指南（在阶段 4 期间加载）
- [✅ 评估指南](./reference/evaluation.md) - 完整的评估创建指南，包括：
  - 问题创建指南
  - 答案验证策略
  - XML 格式规范
  - 示例问题和答案
  - 使用提供的脚本运行评估