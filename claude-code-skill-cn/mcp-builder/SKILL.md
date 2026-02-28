---
name: mcp-builder
description: 创建高质量MCP（模型上下文协议）服务器的指南，使大语言模型能够通过精心设计的工具与外部服务交互。在构建MCP服务器以集成外部API或服务时使用，无论是使用Python（FastMCP）还是Node/TypeScript（MCP SDK）。
license: 完整条款见LICENSE.txt
---

# MCP服务器开发指南

## 概述

创建MCP（模型上下文协议）服务器，使大语言模型能够通过精心设计的工具与外部服务交互。MCP服务器的质量取决于它如何有效地使大语言模型完成现实世界的任务。

## 流程

### 🚀 高级工作流

创建高质量的MCP服务器涉及四个主要阶段：

### 第一阶段：深入研究和规划

#### 1.1 了解现代MCP设计

**API覆盖范围 vs 工作流工具：**

在全面的API端点覆盖与专门的工作流工具之间取得平衡。工作流工具对于特定任务可能更方便，而全面覆盖则为代理提供了组合操作的灵活性。性能因客户端而异——某些客户端受益于结合基本工具的代码执行，而其他客户端则更适合更高级的工作流。当不确定时，优先考虑全面的API覆盖。

**工具命名和可发现性：**

清晰、描述性的工具名称有助于代理快速找到合适的工具。使用一致的前缀（例如 github_create_issue、github_list_repos）和面向操作的命名。

**上下文管理：**

代理受益于简洁的工具描述以及过滤/分页结果的能力。设计返回专注、相关数据的工具。某些客户端支持代码执行，这可以帮助代理高效地过滤和处理数据。

**可操作的错误消息：**

错误消息应通过具体建议和后续步骤引导代理找到解决方案。

#### 1.2 研究MCP协议文档

导航到MCP规范：

从站点地图开始查找相关页面：https://modelcontextprotocol.io/sitemap.xml

然后使用.md后缀获取特定页面以获取markdown格式（例如 https://modelcontextprotocol.io/specification/draft.md）。

需要查看的关键页面：

- 规范概述和架构
- 传输机制（可流式HTTP、stdio）
- 工具、资源和提示定义

#### 1.3 研究框架文档

**推荐技术栈：**

- **语言：** TypeScript（高质量的SDK支持和在许多执行环境中的良好兼容性，例如MCPB。此外，AI模型擅长生成TypeScript代码，得益于其广泛使用、静态类型和良好的lint工具）
- **传输：** 远程服务器使用可流式HTTP，使用无状态JSON（更容易扩展和维护，相对于有状态的会话和流式响应）。本地服务器使用stdio。

加载框架文档：

**MCP最佳实践：** 📋 查看最佳实践 - 核心指南

**对于TypeScript（推荐）：**

- **TypeScript SDK：** 使用WebFetch加载 https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md
- **⚡ TypeScript指南** - TypeScript模式和示例

**对于Python：**

- **Python SDK：** 使用WebFetch加载 https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md
- **🐍 Python指南** - Python模式和示例

#### 1.4 规划实现

**了解API：**

查看服务的API文档以识别关键端点、身份验证要求和数据模型。根据需要使用网络搜索和WebFetch。

**工具选择：**

优先考虑全面的API覆盖。列出要实现的端点，从最常见的操作开始。

### 第二阶段：实现

#### 2.1 设置项目结构

查看特定语言的指南以进行项目设置：

- **⚡ TypeScript指南** - 项目结构、package.json、tsconfig.json
- **🐍 Python指南** - 模块组织、依赖项

#### 2.2 实现核心基础设施

创建共享实用程序：

- 带身份验证的API客户端
- 错误处理助手
- 响应格式化（JSON/Markdown）
- 分页支持

#### 2.3 实现工具

对于每个工具：

**输入模式：**

- 使用Zod（TypeScript）或Pydantic（Python）
- 包含约束和清晰的描述
- 在字段描述中添加示例

**输出模式：**

- 尽可能定义outputSchema以获得结构化数据
- 在工具响应中使用structuredContent（TypeScript SDK功能）
- 帮助客户端理解和处理工具输出

**工具描述：**

- 功能的简洁摘要
- 参数描述
- 返回类型模式

**实现：**

- I/O操作使用async/await
- 带有可操作消息的适当错误处理
- 在适用时支持分页
- 使用现代SDK时返回文本内容和结构化数据

**注释：**

- readOnlyHint: true/false
- destructiveHint: true/false
- idempotentHint: true/false
- openWorldHint: true/false

### 第三阶段：审查和测试

#### 3.1 代码质量

审查以下方面：

- 没有重复代码（DRY原则）
- 一致的错误处理
- 完整的类型覆盖
- 清晰的工具描述

#### 3.2 构建和测试

**TypeScript：**

- 运行npm run build以验证编译
- 使用MCP Inspector测试：npx @modelcontextprotocol/inspector

**Python：**

- 验证语法：python -m py_compile your_server.py
- 使用MCP Inspector测试

查看特定语言的指南以获取详细的测试方法和质量检查清单。

### 第四阶段：创建评估

实现MCP服务器后，创建全面的评估以测试其有效性。

加载 ✅ 评估指南以获取完整的评估指南。

#### 4.1 了解评估目的

使用评估测试大语言模型是否能够有效地使用您的MCP服务器来回答现实的、复杂的问题。

#### 4.2 创建10个评估问题

要创建有效的评估，请遵循评估指南中概述的过程：

1. **工具检查：** 列出可用工具并了解其功能
2. **内容探索：** 使用只读操作探索可用数据
3. **问题生成：** 创建10个复杂的、现实的问题
4. **答案验证：** 自己解决每个问题以验证答案

#### 4.3 评估要求

确保每个问题：

- **独立：** 不依赖于其他问题
- **只读：** 只需要非破坏性操作
- **复杂：** 需要多个工具调用和深入探索
- **现实：** 基于人类关心的真实用例
- **可验证：** 可以通过字符串比较验证的单一、清晰的答案
- **稳定：** 答案不会随时间改变

#### 4.4 输出格式

创建具有以下结构的XML文件：

```xml
<evaluation>
  <qa_pair>
    <question>查找关于以动物代号命名的AI模型发布的讨论。一个模型需要使用ASL-X格式的特定安全指定。为以斑点野猫命名的模型确定的数字X是什么？</question>
    <answer>3</answer>
  </qa_pair>
  <!-- 更多qa_pairs... -->
</evaluation>
```

## 参考文件

### 📚 文档库

在开发期间根据需要加载这些资源：

#### 核心MCP文档（首先加载）

**MCP协议：** 从https://modelcontextprotocol.io/sitemap.xml开始，然后使用.md后缀获取特定页面

**📋 MCP最佳实践** - 通用MCP指南，包括：

- 服务器和工具命名约定
- 响应格式指南（JSON vs Markdown）
- 分页最佳实践
- 传输选择（可流式HTTP vs stdio）
- 安全和错误处理标准

#### SDK文档（在阶段1/2期间加载）

**Python SDK：** 从 https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md 获取

**TypeScript SDK：** 从 https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md 获取

#### 特定语言实现指南（在阶段2期间加载）

**🐍 Python实现指南** - 完整的Python/FastMCP指南，包括：

- 服务器初始化模式
- Pydantic模型示例
- 使用@mcp.tool进行工具注册
- 完整的工作示例
- 质量检查清单

**⚡ TypeScript实现指南** - 完整的TypeScript指南，包括：

- 项目结构
- Zod模式模式
- 使用server.registerTool进行工具注册
- 完整的工作示例
- 质量检查清单

#### 评估指南（在阶段4期间加载）

**✅ 评估指南** - 完整的评估创建指南，包括：

- 问题创建指南
- 答案验证策略
- XML格式规范
- 示例问题和答案
- 使用提供的脚本运行评估
