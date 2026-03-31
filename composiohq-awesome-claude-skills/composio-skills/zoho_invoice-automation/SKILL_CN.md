---
name: zoho_invoice-automation
description: "通过 Rube MCP (Composio) 自动化 Zoho Invoice 任务：发票、估算、费用、客户和付款跟踪。始终先搜索工具以获取当前架构。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 进行 Zoho Invoice 自动化

通过 Rube MCP 使用 Composio 的 Zoho Invoice 工具包自动化 Zoho Invoice 操作。

**工具包文档**: [composio.dev/toolkits/zoho_invoice](https://composio.dev/toolkits/zoho_invoice)

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用工具包 `zoho_invoice` 建立活动的 Zoho Invoice 连接
- 始终首先调用 `RUBE_SEARCH_TOOLS` 以获取当前工具架构

## 设置

**获取 Rube MCP**: 在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 响应来验证 Rube MCP 可用
2. 使用工具包 `zoho_invoice` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接未处于 ACTIVE 状态，请按照返回的授权链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 工具发现

在执行工作流之前，始终发现可用工具：

```
RUBE_SEARCH_TOOLS: queries=[{"use_case": "invoices, estimates, expenses, clients, and payment tracking", "known_fields": ""}]
```

这将返回：
- Zoho Invoice 的可用工具标识符
- 推荐的执行计划步骤
- 已知陷阱和边缘情况
- 每个工具的输入架构

## 核心工作流

### 1. 发现可用的 Zoho Invoice 工具

```
RUBE_SEARCH_TOOLS:
  queries:
    - use_case: "list all available Zoho Invoice tools and capabilities"
```

在继续之前，请查看返回的工具、它们的描述和输入架构。

### 2. 执行 Zoho Invoice 操作

发现工具后，通过以下方式执行：

```
RUBE_MULTI_EXECUTE_TOOL:
  tools:
    - tool_slug: "<discovered_tool_slug>"
      arguments: {<符合架构的参数>}
  memory: {}
  sync_response_to_workbench: false
```

### 3. 多步骤工作流

对于涉及多个 Zoho Invoice 操作的复杂工作流：

1. 搜索所有相关工具：使用特定用例的 `RUBE_SEARCH_TOOLS`
2. 首先执行先决条件步骤（例如，更新前先获取）
3. 使用工具响应在步骤之间传递数据
4. 使用 `RUBE_REMOTE_WORKBENCH` 进行批量操作或数据处理

## 常见模式

### 操作前搜索

在创建新资源之前，始终搜索现有资源以避免重复。

### 分页

许多列表操作支持分页。检查响应中的 `next_cursor` 或 `page_token` 并继续获取，直到完成。

### 错误处理

- 在继续之前检查工具响应是否有错误
- 如果工具失败，验证连接是否仍处于 ACTIVE 状态
- 如果连接过期，通过 `RUBE_MANAGE_CONNECTIONS` 重新认证

### 批量操作

对于批量操作，使用 `RUBE_REMOTE_WORKBENCH` 和 `run_composio_tool()` 在循环中使用 `ThreadPoolExecutor` 进行并行执行。

## 已知陷阱

- **始终先搜索工具**: 工具架构和可用操作可能会变化。不要在不首先通过 `RUBE_SEARCH_TOOLS` 发现它们的情况下硬编码工具标识符。
- **检查连接状态**: 在执行任何工具之前，确保 Zoho Invoice 连接处于 ACTIVE 状态。过期的 OAuth 令牌需要重新认证。
- **遵守速率限制**: 如果收到速率限制错误，请降低请求频率并实施退避策略。
- **验证架构**: 始终传递严格符合架构的参数。当返回 `schemaRef` 而不是 `input_schema` 时，使用 `RUBE_GET_TOOL_SCHEMAS` 加载完整的输入架构。

## 快速参考

| 操作 | 方法 |
|-----------|----------|
| 查找工具 | 使用 Zoho Invoice 特定用例的 `RUBE_SEARCH_TOOLS` |
| 连接 | 使用工具包 `zoho_invoice` 的 `RUBE_MANAGE_CONNECTIONS` |
| 执行 | 使用发现的工具标识符的 `RUBE_MULTI_EXECUTE_TOOL` |
| 批量操作 | 使用 `run_composio_tool()` 的 `RUBE_REMOTE_WORKBENCH` |
| 完整架构 | 对于具有 `schemaRef` 的工具使用 `RUBE_GET_TOOL_SCHEMAS` |

> **工具包文档**: [composio.dev/toolkits/zoho_invoice](https://composio.dev/toolkits/zoho_invoice)
