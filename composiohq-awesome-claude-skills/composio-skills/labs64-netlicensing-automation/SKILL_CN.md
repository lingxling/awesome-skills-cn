---
name: labs64-netlicensing-automation
description: "通过 Rube MCP（Composio）自动化 Labs64 Netlicensing 任务。请始终先搜索工具以获取最新架构。"
requires:
  mcp: [rube]
---

# Labs64 Netlicensing Automation via Rube MCP

通过 Rube MCP 使用 Composio 的 Labs64 Netlicensing 工具包自动化 Labs64 Netlicensing 操作。

**工具包文档**：[composio.dev/toolkits/labs64_netlicensing](https://composio.dev/toolkits/labs64_netlicensing)

## 前置条件

- 必须已连接 Rube MCP（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 对工具包 `labs64_netlicensing` 建立活动连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取最新的工具架构

## 设置

**获取 Rube MCP**：将 `https://rube.app/mcp` 作为 MCP 服务器添加到你的客户端配置中。无需 API 密钥——只需添加端点即可生效。

1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 是否可用
2. 对工具包 `labs64_netlicensing` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接未处于 ACTIVE 状态，请按返回的身份验证链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 工具发现

执行工作流之前，请始终先发现可用工具：

```
RUBE_SEARCH_TOOLS
queries: [{use_case: "Labs64 Netlicensing operations", known_fields: ""}]
session: {generate_id: true}
```

这会返回可用的工具 slug、输入架构、推荐的执行计划以及已知的陷阱。

## 核心工作流模式

### 第 1 步：发现可用工具

```
RUBE_SEARCH_TOOLS
queries: [{use_case: "your specific Labs64 Netlicensing task"}]
session: {id: "existing_session_id"}
```

### 第 2 步：检查连接

```
RUBE_MANAGE_CONNECTIONS
toolkits: ["labs64_netlicensing"]
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

## 常见陷阱

- **始终先搜索**：工具架构会发生变化。在没有调用 `RUBE_SEARCH_TOOLS` 之前，切勿硬编码工具 slug 或参数
- **检查连接**：在执行工具之前，验证 `RUBE_MANAGE_CONNECTIONS` 显示的状态为 ACTIVE
- **架构合规性**：使用搜索结果中准确的字段名称和类型
- **memory 参数**：即使为空（`{}`），也要始终在 `RUBE_MULTI_EXECUTE_TOOL` 调用中包含 `memory`
- **会话复用**：在同一工作流内复用会话 ID。新工作流请生成新的会话 ID
- **分页**：检查响应中的分页令牌，并持续获取直到完成

## 快速参考

| 操作 | 方法 |
|-----------|------|
| 查找工具 | 使用 Labs64 Netlicensing 特定用例调用 `RUBE_SEARCH_TOOLS` |
| 连接 | 对工具包 `labs64_netlicensing` 调用 `RUBE_MANAGE_CONNECTIONS` |
| 执行 | 使用发现的工具 slug 调用 `RUBE_MULTI_EXECUTE_TOOL` |
| 批量操作 | 使用 `run_composio_tool()` 调用 `RUBE_REMOTE_WORKBENCH` |
| 完整架构 | 对带有 `schemaRef` 的工具调用 `RUBE_GET_TOOL_SCHEMAS` |

---
*由 [Composio](https://composio.dev) 提供支持*
