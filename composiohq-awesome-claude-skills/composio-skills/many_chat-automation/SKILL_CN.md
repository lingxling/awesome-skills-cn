---
name: many_chat-automation
description: "通过 Rube MCP（Composio）自动化 ManyChat 任务：聊天机器人流程、订阅者、广播以及 Messenger 自动化。务必先搜索工具以获取当前架构。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 实现 ManyChat 自动化

通过 Rube MCP 使用 Composio 的 ManyChat 工具包自动化 ManyChat 操作。

**工具包文档**：[composio.dev/toolkits/many_chat](https://composio.dev/toolkits/many_chat)

## 前置条件

- 必须已连接 Rube MCP（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 对工具包 `many_chat` 建立活动连接
- 务必先调用 `RUBE_SEARCH_TOOLS` 以获取当前的工具架构

## 设置

**获取 Rube MCP**：在你的客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——只需添加该端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 可用
2. 针对工具包 `many_chat` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按返回的身份验证链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 工具发现

在执行工作流之前，务必先发现可用的工具：

```
RUBE_SEARCH_TOOLS: queries=[{"use_case": "chatbot flows, subscribers, broadcasts, and messenger automation", "known_fields": ""}]
```

这会返回：
- ManyChat 可用的工具标识
- 推荐的执行计划步骤
- 已知坑点和边界情况
- 每个工具的输入架构

## 核心工作流

### 1. 发现可用的 ManyChat 工具

```
RUBE_SEARCH_TOOLS:
  queries:
    - use_case: "list all available ManyChat tools and capabilities"
```

在继续之前，审阅返回的工具、它们的描述和输入架构。

### 2. 执行 ManyChat 操作

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

对于涉及多个 ManyChat 操作的复杂工作流：

1. 针对具体用例搜索所有相关工具：`RUBE_SEARCH_TOOLS`
2. 先执行前置步骤（例如先获取再更新）
3. 使用工具响应在各步骤之间传递数据
4. 对批量操作或数据处理使用 `RUBE_REMOTE_WORKBENCH`

## 常见模式

### 先搜索后行动
在创建新资源之前，务必先搜索现有资源以避免重复。

### 分页
许多列表操作支持分页。检查响应中的 `next_cursor` 或 `page_token`，并持续获取直到枚尽。

### 错误处理
- 在继续之前检查工具响应中是否存在错误
- 如果工具失败，验证连接是否仍为 ACTIVE
- 如果连接过期，通过 `RUBE_MANAGE_CONNECTIONS` 重新认证

### 批量操作
对于批量操作，在循环中使用 `RUBE_REMOTE_WORKBENCH` 的 `run_composio_tool()`，并配合 `ThreadPoolExecutor` 实现并行执行。

## 已知坑点

- **务必先搜索工具**：工具架构和可用操作可能会发生变化。切勿在未通过 `RUBE_SEARCH_TOOLS` 先行发现的情况下硬编码工具标识。
- **检查连接状态**：在执行任何工具之前，确保 ManyChat 连接为 ACTIVE。过期的 OAuth 令牌需要重新认证。
- **遵守速率限制**：如果收到速率限制错误，请降低请求频率并实施退避策略。
- **验证架构**：务必传递严格符合架构的参数。当返回 `schemaRef` 而非 `input_schema` 时，使用 `RUBE_GET_TOOL_SCHEMAS` 加载完整的输入架构。

## 快速参考

| 操作 | 方法 |
|-----------|----------|
| 查找工具 | 使用 ManyChat 相关用例调用 `RUBE_SEARCH_TOOLS` |
| 连接 | 使用工具包 `many_chat` 调用 `RUBE_MANAGE_CONNECTIONS` |
| 执行 | 使用已发现的工具标识调用 `RUBE_MULTI_EXECUTE_TOOL` |
| 批量操作 | 使用 `run_composio_tool()` 调用 `RUBE_REMOTE_WORKBENCH` |
| 完整架构 | 对带有 `schemaRef` 的工具调用 `RUBE_GET_TOOL_SCHEMAS` |

> **工具包文档**：[composio.dev/toolkits/many_chat](https://composio.dev/toolkits/many_chat)
