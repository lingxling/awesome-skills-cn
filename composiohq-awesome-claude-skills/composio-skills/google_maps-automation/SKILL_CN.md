---
name: google_maps-automation
description: "通过 Rube MCP（Composio）自动化 Google Maps 任务：地理编码、路线规划、地点搜索和距离计算。请始终先搜索工具以获取当前的模式。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 实现 Google Maps 自动化

通过 Rube MCP，借助 Composio 的 Google Maps 工具包自动化 Google Maps 操作。

**工具包文档**: [composio.dev/toolkits/google_maps](https://composio.dev/toolkits/google_maps)

## 前置条件

- 必须已连接 Rube MCP（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立有效的 Google Maps 连接，工具包为 `google_maps`
- 始终先调用 `RUBE_SEARCH_TOOLS` 以获取当前的工具模式

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥——只需添加该端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，工具包为 `google_maps`
3. 如果连接状态不是 ACTIVE，请按照返回的授权链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 工具发现

在执行工作流之前，务必先发现可用工具：

```
RUBE_SEARCH_TOOLS: queries=[{"use_case": "geocoding, directions, place search, and distance calculations", "known_fields": ""}]
```

这将返回：
- Google Maps 可用的工具 slug
- 推荐的执行计划步骤
- 已知陷阱和边缘情况
- 每个工具的输入模式

## 核心工作流

### 1. 发现可用的 Google Maps 工具

```
RUBE_SEARCH_TOOLS:
  queries:
    - use_case: "list all available Google Maps tools and capabilities"
```

在继续之前，请查看返回的工具、其描述和输入模式。

### 2. 执行 Google Maps 操作

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

对于涉及多个 Google Maps 操作的复杂工作流：

1. 搜索所有相关工具：使用具体用例调用 `RUBE_SEARCH_TOOLS`
2. 先执行前置步骤（例如，先获取再更新）
3. 使用工具响应在步骤之间传递数据
4. 使用 `RUBE_REMOTE_WORKBENCH` 进行批量操作或数据处理

## 常见模式

### 先搜索再操作
在创建新资源之前，务必先搜索现有资源，以避免重复。

### 分页
许多列表操作支持分页。检查响应中的 `next_cursor` 或 `page_token`，并持续获取直至结束。

### 错误处理
- 在继续之前检查工具响应中是否有错误
- 如果工具失败，请验证连接是否仍为 ACTIVE
- 如果连接已过期，通过 `RUBE_MANAGE_CONNECTIONS` 重新认证

### 批量操作
对于批量操作，使用 `RUBE_REMOTE_WORKBENCH`，并在循环中配合 `ThreadPoolExecutor` 调用 `run_composio_tool()` 以实现并行执行。

## 已知陷阱

- **始终先搜索工具**：工具模式和可用操作可能会变化。在未通过 `RUBE_SEARCH_TOOLS` 发现工具 slug 之前，切勿硬编码。
- **检查连接状态**：在执行任何工具之前，确保 Google Maps 连接处于 ACTIVE 状态。过期的 OAuth 令牌需要重新认证。
- **遵守速率限制**：如果收到速率限制错误，请降低请求频率并实现退避机制。
- **验证模式**：始终传递严格符合模式的参数。当返回的是 `schemaRef` 而非 `input_schema` 时，使用 `RUBE_GET_TOOL_SCHEMAS` 加载完整的输入模式。

## 快速参考

| 操作 | 方法 |
|-----------|----------|
| 查找工具 | 使用 Google Maps 特定用例调用 `RUBE_SEARCH_TOOLS` |
| 连接 | 使用工具包 `google_maps` 调用 `RUBE_MANAGE_CONNECTIONS` |
| 执行 | 使用发现的工具 slug 调用 `RUBE_MULTI_EXECUTE_TOOL` |
| 批量操作 | 使用 `run_composio_tool()` 调用 `RUBE_REMOTE_WORKBENCH` |
| 完整模式 | 对带有 `schemaRef` 的工具使用 `RUBE_GET_TOOL_SCHEMAS` |

> **工具包文档**: [composio.dev/toolkits/google_maps](https://composio.dev/toolkits/google_maps)
