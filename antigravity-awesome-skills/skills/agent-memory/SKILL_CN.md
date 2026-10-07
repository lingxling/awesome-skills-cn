---
name: agent-memory
description: 一个混合内存系统，为 AI 代理提供持久的、可搜索的知识管理。
risk: critical
source: https://github.com/webzler/agentMemory/tree/main/
source_repo: webzler/agentMemory
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/webzler/agentMemory/blob/main/LICENSE
---

# agentMemory 技能
## 何时使用

当您需要一个为 AI 代理提供持久的、可搜索的知识管理的混合内存系统时，使用此技能。


此技能通过提供一个持久的、可搜索的内存库来扩展您的功能，该内存库自动与项目文档同步。

## 前置条件

- 已安装 Node.js
- 检查 `agentMemory` 是否已安装在项目中：
  ```bash
  ls -la .agentMemory
  ```

## 设置

1. **安装依赖项**：
   ```bash
   npm install
   ```

2. **构建项目**：
   ```bash
   npm run compile
   ```

3. **启动内存服务器**：
   您需要运行 MCP 服务器来与内存库交互。
   ```bash
   npm run start-server <project_id> <absolute_path_to_workspace>
   ```
   *注意：此技能通常作为后台进程运行或通过 mcp-server 配置运行。确保它正在运行是关键。*

## 功能（MCP 工具）

服务器运行后，您可以使用这些工具：

### `memory_search`
按查询、类型或标签搜索内存。
- **参数**：`query` (string)、`type?` (string)、`tags?` (string[])
- **用法**："查找所有身份验证模式" -> `memory_search({ query: "authentication", type: "pattern" })`

### `memory_write`
记录新知识或决策。
- **参数**：`key` (string)、`type` (string)、`content` (string)、`tags?` (string[])
- **用法**："保存此架构决策" -> `memory_write({ key: "auth-v1", type: "decision", content: "..." })`

### `memory_read`
通过密钥检索特定的内存内容。
- **参数**：`key` (string)
- **用法**："获取身份验证设计" -> `memory_read({ key: "auth-v1" })`

### `memory_stats`
查看内存使用分析。
- **用法**："显示内存统计信息" -> `memory_stats({})`

## 工作流程

1. **初始化**：第一次在项目中运行此操作时，它可能会尝试从 `.kilocode/`、`.clinerules/` 或 `.roo/` 导入现有 markdown 内存库。
2. **开发循环**：
   - **任务前**：搜索内存以获得相关上下文。
   - **任务期间**：使用读取/搜索来回答问题。
   - **任务后**：将新发现写入内存。
3. **同步**：您的写入会自动同步到项目中的标准 markdown 文件。

## 示例

**用户请求：**

> 为此任务使用 @agent-memory：一个为 AI 代理提供持久的、可搜索的知识管理的混合内存系统。

## 限制条件

- 仅在任务明确与其上游源和本地项目上下文相匹配时才使用此技能。
- 在应用更改之前验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例作为环境特定测试、安全审查或用户批准破坏性或成本高昂的操作的替代品。
