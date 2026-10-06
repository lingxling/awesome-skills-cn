---
name: extracta-ai-automation
description: "通过 Rube MCP（Composio）自动化 Extracta AI 任务。请始终先搜索工具以获取当前的模式。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 实现 Extracta AI 自动化

通过 Rube MCP，借助 Composio 的 Extracta AI 工具包自动化 Extracta AI 操作。

**工具包文档**: [composio.dev/toolkits/extracta_ai](https://composio.dev/toolkits/extracta_ai)

## 前置条件

- 必须已连接 Rube MCP（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立有效的 Extracta AI 连接，工具包为 `extracta_ai`
- 始终先调用 `RUBE_SEARCH_TOOLS` 以获取当前的工具模式

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥——只需添加该端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，工具包为 `extracta_ai`
3. 如果连接状态不是 ACTIVE，请按照返回的授权链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 工具发现

在执行工作流之前，务必先发现可用工具：

```
RUBE_SEARCH_TOOLS
queries: [{use_case: "Extracta AI operations", known_fields: ""}]
session: {generate_id: true}
```

这将返回可用的工具 slug、输入模式、推荐的执行计划以及已知陷阱。

## 核心工作流模式

### 步骤 1：发现可用工具

```
RUBE_SEARCH_TOOLS
queries: [{use_case: "your specific Extracta AI task"}]
session: {id: "existing_session_id"}
```

### 步骤 2：检查连接

```
RUBE_MANAGE_CONNECTIONS
toolkits: ["extracta_ai"]
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

- **始终先搜索**：工具模式会变化。在未调用 `RUBE_SEARCH_TOOLS` 的情况下，切勿硬编码工具 slug 或参数
- **检查连接**：在执行工具之前，确认 `RUBE_MANAGE_CONNECTIONS` 显示 ACTIVE 状态
- **遵循模式**：使用搜索结果中的确切字段名称和类型
- **Memory 参数**：在 `RUBE_MULTI_EXECUTE_TOOL` 调用中始终包含 `memory`，即使为空（`{}`）
- **会话复用**：在同一工作流中复用会话 ID，为新工作流生成新的会话 ID
- **分页**：检查响应中的分页令牌，并持续获取直至完成

## 快速参考

| 操作 | 方法 |
|-----------|----------|
| 查找工具 | 使用 Extracta AI 特定用例调用 `RUBE_SEARCH_TOOLS` |
| 连接 | 使用工具包 `extracta_ai` 调用 `RUBE_MANAGE_CONNECTIONS` |
| 执行 | 使用发现的工具 slug 调用 `RUBE_MULTI_EXECUTE_TOOL` |
| 批量操作 | 使用 `run_composio_tool()` 调用 `RUBE_REMOTE_WORKBENCH` |
| 完整模式 | 对带有 `schemaRef` 的工具使用 `RUBE_GET_TOOL_SCHEMAS` |

---
*由 [Composio](https://composio.dev) 提供支持*
