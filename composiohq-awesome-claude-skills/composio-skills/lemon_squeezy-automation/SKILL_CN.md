---
name: lemon_squeezy-automation
description: "通过 Rube MCP（Composio）自动化 Lemon Squeezy 任务：产品、订单、订阅、结账和数字商品销售。请始终先搜索工具以获取最新的模式。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 自动化 Lemon Squeezy

通过 Composio 的 Lemon Squeezy 工具包，借助 Rube MCP 自动化 Lemon Squeezy 操作。

**工具包文档**：[composio.dev/toolkits/lemon_squeezy](https://composio.dev/toolkits/lemon_squeezy)

## 前置条件

- 必须已连接 Rube MCP（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 对工具包 `lemon_squeezy` 建立有效连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 以获取当前的工具模式

## 设置

**获取 Rube MCP**：将 `https://rube.app/mcp` 作为 MCP 服务器添加到你的客户端配置中。无需 API 密钥——只需添加端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 是否可用
2. 对工具包 `lemon_squeezy` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接未处于 ACTIVE 状态，请按返回的认证链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 工具发现

在执行工作流之前，始终先发现可用工具：

```
RUBE_SEARCH_TOOLS: queries=[{"use_case": "products, orders, subscriptions, checkouts, and digital sales", "known_fields": ""}]
```

这将返回：
- Lemon Squeezy 的可用工具标识
- 推荐的执行计划步骤
- 已知的陷阱和边界情况
- 每个工具的输入模式

## 核心工作流

### 1. 发现可用的 Lemon Squeezy 工具

```
RUBE_SEARCH_TOOLS:
  queries:
    - use_case: "list all available Lemon Squeezy tools and capabilities"
```

在继续之前，先查看返回的工具、它们的描述和输入模式。

### 2. 执行 Lemon Squeezy 操作

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

对于涉及多个 Lemon Squeezy 操作的复杂工作流：

1. 搜索所有相关工具：针对具体用例调用 `RUBE_SEARCH_TOOLS`
2. 先执行前提步骤（例如先获取再更新）
3. 使用工具响应在各步骤之间传递数据
4. 对批量操作或数据处理使用 `RUBE_REMOTE_WORKBENCH`

## 常见模式

### 先搜索再操作
在创建新资源之前，始终先搜索现有资源，以避免重复。

### 分页
许多列表操作支持分页。检查响应中的 `next_cursor` 或 `page_token`，并持续获取直到结果耗尽。

### 错误处理
- 在继续之前检查工具响应中是否有错误
- 如果工具调用失败，验证连接是否仍为 ACTIVE
- 如果连接过期，通过 `RUBE_MANAGE_CONNECTIONS` 重新认证

### 批量操作
对于批量操作，在循环中使用带 `ThreadPoolExecutor` 的 `RUBE_REMOTE_WORKBENCH` 和 `run_composio_tool()` 以实现并行执行。

## 已知陷阱

- **始终先搜索工具**：工具模式和可用操作可能会变化。切勿在未先通过 `RUBE_SEARCH_TOOLS` 发现的情况下硬编码工具标识。
- **检查连接状态**：在执行任何工具之前，确保 Lemon Squeezy 连接处于 ACTIVE 状态。过期的 OAuth 令牌需要重新认证。
- **遵守速率限制**：如果收到速率限制错误，请降低请求频率并实施退避策略。
- **验证模式**：始终传递严格符合模式的参数。当返回 `schemaRef` 而不是 `input_schema` 时，使用 `RUBE_GET_TOOL_SCHEMAS` 加载完整的输入模式。

## 快速参考

| 操作 | 方法 |
|-----------|-------|
| 查找工具 | 针对 Lemon Squeezy 特定用例使用 `RUBE_SEARCH_TOOLS` |
| 连接 | 对工具包 `lemon_squeezy` 使用 `RUBE_MANAGE_CONNECTIONS` |
| 执行 | 使用 `RUBE_MULTI_EXECUTE_TOOL` 配合已发现的工具标识 |
| 批量操作 | 使用 `RUBE_REMOTE_WORKBENCH` 配合 `run_composio_tool()` |
| 完整模式 | 对带有 `schemaRef` 的工具使用 `RUBE_GET_TOOL_SCHEMAS` |

> **工具包文档**：[composio.dev/toolkits/lemon_squeezy](https://composio.dev/toolkits/lemon_squeezy)
