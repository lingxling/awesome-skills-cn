---
name: zoho_books-automation
description: "Automate Zoho Books tasks via Rube MCP (Composio): invoices, expenses, contacts, payments, and accounting. Always search tools first for current schemas."
requires:
  mcp: [rube]
---

# Zoho Books Automation via Rube MCP

Automate Zoho Books operations through Composio's Zoho Books toolkit via Rube MCP.

**Toolkit docs**: [composio.dev/toolkits/zoho_books](https://composio.dev/toolkits/zoho_books)

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- Active Zoho Books connection via `RUBE_MANAGE_CONNECTIONS` with toolkit `zoho_books`
- 始终首先调用 `RUBE_SEARCH_TOOLS` 以获取当前工具架构

## 设置

**获取 Rube MCP**: 在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 响应来验证 Rube MCP 可用
2. Call `RUBE_MANAGE_CONNECTIONS` with toolkit `zoho_books`
3. 如果连接未处于 ACTIVE 状态，请按照返回的授权链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 工具发现

在执行工作流之前，始终发现可用工具：

```
RUBE_SEARCH_TOOLS: queries=[{"use_case": "invoices, expenses, contacts, payments, and accounting", "known_fields": ""}]
```

This returns:
- Available tool slugs for Zoho Books
- Recommended execution plan steps
- Known pitfalls and edge cases
- Input schemas for each tool

## Core Workflows

### 1. Discover Available Zoho Books Tools

```
RUBE_SEARCH_TOOLS:
  queries:
    - use_case: "list all available Zoho Books tools and capabilities"
```

Review the returned tools, their descriptions, and input schemas before proceeding.

### 2. 执行 Zoho Books 操作s

After discovering tools, execute them via:

```
RUBE_MULTI_EXECUTE_TOOL:
  tools:
    - tool_slug: "<discovered_tool_slug>"
      arguments: {<schema-compliant arguments>}
  memory: {}
  sync_response_to_workbench: false
```

### 3. Multi-Step Workflows

For complex workflows involving multiple Zoho Books operations:

1. Search for all relevant tools: `RUBE_SEARCH_TOOLS` with specific use case
2. 执行 prerequisite steps first (e.g., fetch before update)
3. Pass data between steps using tool responses
4. Use `RUBE_REMOTE_WORKBENCH` for bulk operations or data processing

## Common Patterns

### Search Before Action
Always search for existing resources before creating new ones to avoid duplicates.

### Pagination
Many list operations support pagination. Check responses for `next_cursor` or `page_token` and continue fetching until exhausted.

### Error Handling
- Check tool responses for errors before proceeding
- If a tool fails, verify the connection is still ACTIVE
- Re-authenticate via `RUBE_MANAGE_CONNECTIONS` if connection expired

### Batch 操作s
For bulk operations, use `RUBE_REMOTE_WORKBENCH` with `run_composio_tool()` in a loop with `ThreadPoolExecutor` for parallel execution.

## 已知陷阱

- **Always search tools first**: Tool schemas and available operations may change. Never hardcode tool slugs without first discovering them via `RUBE_SEARCH_TOOLS`.
- **Check connection status**: Ensure the Zoho Books connection is ACTIVE before executing any tools. Expired OAuth tokens require re-authentication.
- **Respect rate limits**: If you receive rate limit errors, reduce request frequency and implement backoff.
- **Validate schemas**: Always pass strictly schema-compliant arguments. Use `RUBE_GET_TOOL_SCHEMAS` to load full input schemas when `schemaRef` is returned instead of `input_schema`.

## 快速参考

| 操作 | 方法 |
|-----------|----------|
| 查找工具 | `RUBE_SEARCH_TOOLS` with Zoho Books-specific use case |
| 连接 | `RUBE_MANAGE_CONNECTIONS` with toolkit `zoho_books` |
| 执行 | `RUBE_MULTI_EXECUTE_TOOL` with discovered tool slugs |
| 批量操作 | `RUBE_REMOTE_WORKBENCH` with `run_composio_tool()` |
| 完整架构 | `RUBE_GET_TOOL_SCHEMAS` for tools with `schemaRef` |

> **Toolkit docs**: [composio.dev/toolkits/zoho_books](https://composio.dev/toolkits/zoho_books)
