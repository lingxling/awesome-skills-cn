---
name: mistral_ai-automation
description: "通过 Rube MCP（Composio）自动化 Mistral AI 任务：补全（completions）、嵌入（embeddings）、微调和模型管理。请始终先搜索工具以获取最新架构。"
requires:
  mcp: [rube]
---

# Mistral AI Automation via Rube MCP

通过 Rube MCP 使用 Composio 的 Mistral AI 工具包自动化 Mistral AI 操作。

**工具包文档**：[composio.dev/toolkits/mistral_ai](https://composio.dev/toolkits/mistral_ai)

## 前置条件

- 必须已连接 Rube MCP（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 对工具包 `mistral_ai` 建立活动连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取最新的工具架构

## 设置

**获取 Rube MCP**：将 `https://rube.app/mcp` 作为 MCP 服务器添加到你的客户端配置中。无需 API 密钥——只需添加端点即可生效。

1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 是否可用
2. 对工具包 `mistral_ai` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接未处于 ACTIVE 状态，请按返回的身份验证链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 工具发现

执行工作流之前，请始终先发现可用工具：

```
RUBE_SEARCH_TOOLS: queries=[{"use_case": "completions, embeddings, fine-tuning, and model management", "known_fields": ""}]
```

这会返回：
- Mistral AI 可用的工具 slug
- 推荐的执行计划步骤
- 已知的陷阱和边界情况
- 每个工具的输入架构

## 核心工作流

### 1. 发现可用的 Mistral AI 工具

```
RUBE_SEARCH_TOOLS:
  queries:
    - use_case: "list all available Mistral AI tools and capabilities"
```

在继续之前，请查看返回的工具、它们的描述和输入架构。

### 2. 执行 Mistral AI 操作

发现工具后，通过以下方式执行：

```
RUBE_MULTI_EXECUTE_TOOL:
  tools:
    - tool_slug: "<discovered_tool_slug>"
      arguments: {<schema-compliant arguments>}
  memory: {}
  sync_response_to_workbench: false
```

### 3. 多步骤工作流

对于涉及多个 Mistral AI 操作的复杂工作流：

1. 搜索所有相关工具：使用特定用例调用 `RUBE_SEARCH_TOOLS`
2. 先执行前置步骤（例如先获取再更新）
3. 使用工具响应在各步骤之间传递数据
4. 对批量操作或数据处理使用 `RUBE_REMOTE_WORKBENCH`

## 常见模式

### 先搜索再操作
在创建新资源之前始终先搜索现有资源，以避免重复。

### 分页
许多列表操作支持分页。检查响应中的 `next_cursor` 或 `page_token`，并持续获取直到结束。

### 错误处理
- 在继续之前检查工具响应中是否存在错误
- 如果工具调用失败，请验证连接是否仍处于 ACTIVE 状态
- 如果连接过期，请通过 `RUBE_MANAGE_CONNECTIONS` 重新进行身份验证

### 批量操作
对于批量操作，请在循环中使用 `RUBE_REMOTE_WORKBENCH` 的 `run_composio_tool()`，并配合 `ThreadPoolExecutor` 实现并行执行。

## 常见陷阱

- **始终先搜索工具**：工具架构和可用操作可能会发生变化。在没有先通过 `RUBE_SEARCH_TOOLS` 发现之前，切勿硬编码工具 slug。
- **检查连接状态**：在执行任何工具之前，确保 Mistral AI 连接处于 ACTIVE 状态。过期的 OAuth 令牌需要重新进行身份验证。
- **遵守速率限制**：如果收到速率限制错误，请降低请求频率并实现退避重试。
- **验证架构**：始终传递严格符合架构的参数。当返回的是 `schemaRef` 而非 `input_schema` 时，使用 `RUBE_GET_TOOL_SCHEMAS` 加载完整的输入架构。

## 快速参考

| 操作 | 方法 |
|-----------|------|
| 查找工具 | 使用 Mistral AI 特定用例调用 `RUBE_SEARCH_TOOLS` |
| 连接 | 对工具包 `mistral_ai` 调用 `RUBE_MANAGE_CONNECTIONS` |
| 执行 | 使用发现的工具 slug 调用 `RUBE_MULTI_EXECUTE_TOOL` |
| 批量操作 | 使用 `run_composio_tool()` 调用 `RUBE_REMOTE_WORKBENCH` |
| 完整架构 | 对带有 `schemaRef` 的工具调用 `RUBE_GET_TOOL_SCHEMAS` |

> **工具包文档**：[composio.dev/toolkits/mistral_ai](https://composio.dev/toolkits/mistral_ai)
