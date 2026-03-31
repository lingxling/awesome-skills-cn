---
name: typless-automation
description: "通过 Rube MCP (Composio) 自动化 Typless 任务。始终先搜索工具以获取当前架构。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 进行 Typless 自动化

通过 Rube MCP 使用 Composio 的 Typless 工具包自动化 Typless 操作。

**Toolkit docs**: [composio.dev/toolkits/typless](https://composio.dev/toolkits/typless)

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- Active Typless connection via `RUBE_MANAGE_CONNECTIONS` with toolkit `typless`
- 始终首先调用 `RUBE_SEARCH_TOOLS` 以获取当前工具架构

## 设置

**获取 Rube MCP**: 在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 响应来验证 Rube MCP 可用
2. Call `RUBE_MANAGE_CONNECTIONS` with toolkit `typless`
3. 如果连接未处于 ACTIVE 状态，请按照返回的授权链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 工具发现

在执行工作流之前，始终发现可用工具：

```
RUBE_SEARCH_TOOLS
queries: [{use_case: "Typless operations", known_fields: ""}]
session: {generate_id: true}
```

这将返回可用的工具标识符、输入架构、推荐的执行计划和已知陷阱。

## 核心工作流模式

### 步骤 1：发现可用工具

```
RUBE_SEARCH_TOOLS
queries: [{use_case: "your specific Typless task"}]
session: {id: "existing_session_id"}
```

### 步骤 2：检查连接

```
RUBE_MANAGE_CONNECTIONS
toolkits: ["typless"]
session_id: "your_session_id"
```

### 步骤 3：执行工具

```
RUBE_MULTI_EXECUTE_TOOL
tools: [{
  tool_slug: "TOOL_SLUG_FROM_SEARCH",
  arguments: {/* 符合架构的参数，来自搜索结果 */}
}]
memory: {}
session_id: "your_session_id"
```

## 已知陷阱

- **始终先搜索**: 工具架构会变化。不要在不调用 `RUBE_SEARCH_TOOLS` 的情况下硬编码工具标识符或参数
- **检查连接**: 在执行工具之前，验证 `RUBE_MANAGE_CONNECTIONS` 显示 ACTIVE 状态
- **架构合规**: 使用搜索结果中的确切字段名称和类型
- **Memory 参数**: 始终在 `RUBE_MULTI_EXECUTE_TOOL` 调用中包含 `memory`，即使为空 (`{}`)
- **会话重用**: 在工作流内重用会话 ID。为新工作流生成新的会话 ID
- **分页**: 检查响应中的分页令牌并继续获取，直到完成

## 快速参考

| 操作 | 方法 |
|-----------|----------|
| 查找工具 | `RUBE_SEARCH_TOOLS` with Typless-specific use case |
| 连接 | `RUBE_MANAGE_CONNECTIONS` with toolkit `typless` |
| 执行 | `RUBE_MULTI_EXECUTE_TOOL` with discovered tool slugs |
| 批量操作 | `RUBE_REMOTE_WORKBENCH` with `run_composio_tool()` |
| 完整架构 | `RUBE_GET_TOOL_SCHEMAS` for tools with `schemaRef` |

---
*由 [Composio](https://composio.dev) 提供支持*
