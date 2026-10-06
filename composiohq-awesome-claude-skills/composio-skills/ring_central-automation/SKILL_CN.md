---
name: ring_central-automation
description: "通过 Rube MCP（Composio）自动化 RingCentral 任务：通话、消息、会议和统一通信。始终先搜索工具以获取最新的结构定义。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 实现 RingCentral 自动化

通过 Rube MCP 使用 Composio 的 RingCentral 工具包自动化 RingCentral 操作。

**工具包文档**：[composio.dev/toolkits/ring_central](https://composio.dev/toolkits/ring_central)

## 前置条件

- 必须已连接 Rube MCP（RUBE_SEARCH_TOOLS 可用）
- 已通过 `RUBE_MANAGE_CONNECTIONS` 对工具包 `ring_central` 建立活动连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 以获取最新的工具结构定义

## 设置

**获取 Rube MCP**：在你的客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——只需添加该端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 是否可用
2. 对工具包 `ring_central` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接未处于 ACTIVE 状态，请按返回的验证链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 工具发现

执行工作流之前，始终先发现可用的工具：

```
RUBE_SEARCH_TOOLS: queries=[{"use_case": "calls, messages, meetings, and unified communications", "known_fields": ""}]
```

这将返回：
- RingCentral 可用的工具标识
- 推荐的执行计划步骤
- 已知的陷阱和边界情况
- 每个工具的输入结构定义

## 核心工作流

### 1. 发现可用的 RingCentral 工具

```
RUBE_SEARCH_TOOLS:
  queries:
    - use_case: "list all available RingCentral tools and capabilities"
```

在继续操作之前，请查看返回的工具、它们的描述以及输入结构定义。

### 2. 执行 RingCentral 操作

发现工具后，通过以下方式执行它们：

```
RUBE_MULTI_EXECUTE_TOOL:
  tools:
    - tool_slug: "<discovered_tool_slug>"
      arguments: {<schema-compliant arguments>}
  memory: {}
  sync_response_to_workbench: false
```

### 3. 多步骤工作流

对于涉及多个 RingCentral 操作的复杂工作流：

1. 搜索所有相关工具：针对特定用例使用 `RUBE_SEARCH_TOOLS`
2. 先执行前置步骤（例如先获取再更新）
3. 使用工具响应在各步骤之间传递数据
4. 对批量操作或数据处理使用 `RUBE_REMOTE_WORKBENCH`

## 常见模式

### 先搜索再操作
创建新资源之前，始终先搜索现有资源，以避免重复。

### 分页
许多列表操作支持分页。检查响应中的 `next_cursor` 或 `page_token`，并持续获取直到数据穷尽。

### 错误处理
- 在继续之前检查工具响应中是否存在错误
- 如果工具调用失败，验证连接是否仍为 ACTIVE
- 如果连接已过期，请通过 `RUBE_MANAGE_CONNECTIONS` 重新进行身份验证

### 批量操作
对于批量操作，在循环中使用 `RUBE_REMOTE_WORKBENCH` 配合 `run_composio_tool()`，并使用 `ThreadPoolExecutor` 实现并行执行。

## 常见陷阱

- **始终先搜索工具**：工具结构定义和可用操作可能会发生变化。切勿在未先通过 `RUBE_SEARCH_TOOLS` 发现工具的情况下硬编码工具标识。
- **检查连接状态**：在执行任何工具之前，确保 RingCentral 连接处于 ACTIVE 状态。过期的 OAuth 令牌需要重新进行身份验证。
- **遵守速率限制**：如果收到速率限制错误，请降低请求频率并实现退避重试。
- **验证结构定义**：始终传递严格符合结构定义的参数。当返回 `schemaRef` 而非 `input_schema` 时，使用 `RUBE_GET_TOOL_SCHEMAS` 加载完整的输入结构定义。

## 快速参考

| 操作 | 方法 |
|-----------|----------|
| 查找工具 | 针对 RingCentral 特定用例使用 `RUBE_SEARCH_TOOLS` |
| 连接 | 对工具包 `ring_central` 使用 `RUBE_MANAGE_CONNECTIONS` |
| 执行 | 使用发现的工具标识调用 `RUBE_MULTI_EXECUTE_TOOL` |
| 批量操作 | 使用 `RUBE_REMOTE_WORKBENCH` 配合 `run_composio_tool()` |
| 完整结构定义 | 对带有 `schemaRef` 的工具使用 `RUBE_GET_TOOL_SCHEMAS` |

> **工具包文档**：[composio.dev/toolkits/ring_central](https://composio.dev/toolkits/ring_central)
