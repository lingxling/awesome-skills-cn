---
name: amara-automation
description: "通过 Rube MCP (Composio) 自动化 Amara 任务。始终先搜索工具以获取当前架构。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 实现 Amara 自动化

通过 Composio 的 Amara 工具包，经由 Rube MCP 实现 Amara 操作的自动化。

**工具包文档**：[composio.dev/toolkits/amara](https://composio.dev/toolkits/amara)

## 前提条件

- 必须连接 Rube MCP（RUBE_SEARCH_TOOLS 可用）
- 通过带有工具包 `amara` 的 `RUBE_MANAGE_CONNECTIONS` 激活 Amara 连接
- 始终首先调用 `RUBE_SEARCH_TOOLS` 以获取当前工具架构

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。不需要 API 密钥 — 只需添加端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 响应来验证 Rube MCP 可用
2. 使用工具包 `amara` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接不是 ACTIVE 状态，按照返回的认证链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 工具发现

在执行工作流之前，始终发现可用的工具：

```
RUBE_SEARCH_TOOLS
queries: [{use_case: "Amara operations", known_fields: ""}]
session: {generate_id: true}
```

这将返回可用的工具 slug、输入架构、推荐的执行计划和已知的陷阱。

## 核心工作流模式

### 步骤 1：发现可用工具

```
RUBE_SEARCH_TOOLS
queries: [{use_case: "your specific Amara task"}]
session: {id: "existing_session_id"}
```

### 步骤 2：检查连接

```
RUBE_MANAGE_CONNECTIONS
toolkits: ["amara"]
session_id: "your_session_id"
```

### 步骤 3：执行工具

```
RUBE_MULTI_EXECUTE_TOOL
tools: [{
  tool_slug: "TOOL_SLUG_FROM_SEARCH",
  arguments: {/* schema-compliant args from search results */}
}]
memory: {}
session_id: "your_session_id"
```

## 已知陷阱

- **始终先搜索**：工具架构会变化。在未调用 `RUBE_SEARCH_TOOLS` 的情况下，切勿硬编码工具 slug 或参数
- **检查连接**：在执行工具之前，验证 `RUBE_MANAGE_CONNECTIONS` 显示 ACTIVE 状态
- **架构合规性**：使用搜索结果中的确切字段名称和类型
- **内存参数**：在 `RUBE_MULTI_EXECUTE_TOOL` 调用中始终包含 `memory`，即使为空 (`{}`)
- **会话重用**：在工作流中重用会话 ID。为新工作流生成新的会话 ID
- **分页**：检查响应中的分页令牌，并继续获取直到完成

## 快速参考

| 操作 | 方法 |
|-----------|----------|
| 查找工具 | 使用 Amara 特定用例的 `RUBE_SEARCH_TOOLS` |
| 连接 | 使用工具包 `amara` 的 `RUBE_MANAGE_CONNECTIONS` |
| 执行 | 使用发现的工具 slug 的 `RUBE_MULTI_EXECUTE_TOOL` |
| 批量操作 | 使用 `run_composio_tool()` 的 `RUBE_REMOTE_WORKBENCH` |
| 完整架构 | 为带有 `schemaRef` 的工具使用 `RUBE_GET_TOOL_SCHEMAS` |

---
*由 [Composio](https://composio.dev) 提供支持*