---
name: mx-technologies-automation
description: "通过 Rube MCP（Composio）自动化 MX Technologies 任务。请始终先搜索工具以获取最新的模式。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 自动化 MX Technologies

通过 Composio 的 MX Technologies 工具包，借助 Rube MCP 自动化 MX Technologies 操作。

**工具包文档**：[composio.dev/toolkits/mx_technologies](https://composio.dev/toolkits/mx_technologies)

## 前置条件

- 必须已连接 Rube MCP（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 对工具包 `mx_technologies` 建立有效连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 以获取当前的工具模式

## 设置

**获取 Rube MCP**：将 `https://rube.app/mcp` 作为 MCP 服务器添加到你的客户端配置中。无需 API 密钥——只需添加端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 是否可用
2. 对工具包 `mx_technologies` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接未处于 ACTIVE 状态，请按返回的认证链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 工具发现

在执行工作流之前，始终先发现可用工具：

```
RUBE_SEARCH_TOOLS
queries: [{use_case: "MX Technologies operations", known_fields: ""}]
session: {generate_id: true}
```

这将返回可用的工具标识、输入模式、推荐的执行计划以及已知的陷阱。

## 核心工作流模式

### 第 1 步：发现可用工具

```
RUBE_SEARCH_TOOLS
queries: [{use_case: "your specific MX Technologies task"}]
session: {id: "existing_session_id"}
```

### 第 2 步：检查连接

```
RUBE_MANAGE_CONNECTIONS
toolkits: ["mx_technologies"]
session_id: "your_session_id"
```

### 第 3 步：执行工具

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

- **始终先搜索**：工具模式会发生变化。切勿在未调用 `RUBE_SEARCH_TOOLS` 的情况下硬编码工具标识或参数
- **检查连接**：在执行工具之前，验证 `RUBE_MANAGE_CONNECTIONS` 显示 ACTIVE 状态
- **模式合规**：使用搜索结果中的确切字段名称和类型
- **memory 参数**：在 `RUBE_MULTI_EXECUTE_TOOL` 调用中始终包含 `memory`，即使为空（`{}`）
- **会话复用**：在一个工作流内复用会话 ID。为新的工作流生成新的会话 ID
- **分页**：检查响应中的分页令牌，并持续获取直到完整

## 快速参考

| 操作 | 方法 |
|-----------|-------|
| 查找工具 | 针对 MX Technologies 特定用例使用 `RUBE_SEARCH_TOOLS` |
| 连接 | 对工具包 `mx_technologies` 使用 `RUBE_MANAGE_CONNECTIONS` |
| 执行 | 使用 `RUBE_MULTI_EXECUTE_TOOL` 配合已发现的工具标识 |
| 批量操作 | 使用 `RUBE_REMOTE_WORKBENCH` 配合 `run_composio_tool()` |
| 完整模式 | 对带有 `schemaRef` 的工具使用 `RUBE_GET_TOOL_SCHEMAS` |

---
*由 [Composio](https://composio.dev) 提供支持*
