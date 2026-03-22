---
name: linear
description: 在 Linear 中管理问题、项目和团队工作流程。当用户想要读取、创建或更新 Linear 中的工单时使用。
metadata:
  short-description: 在 Codex 中管理 Linear 问题
---

# Linear

## 概述

此技能为在 Linear 中管理问题、项目和团队工作流程提供了结构化的工作流程。它确保与 Linear MCP 服务器的一致集成，该服务器为问题、项目、文档和团队协作提供自然语言项目管理。

## 前置条件
- Linear MCP 服务器必须通过 OAuth 连接和访问
- 确认对相关 Linear 工作区、团队和项目的访问权限

## 必需工作流程

**按顺序遵循这些步骤。不要跳过步骤。**

### 步骤 0：设置 Linear MCP（如果尚未配置）

如果任何 MCP 调用由于 Linear MCP 未连接而失败，请暂停并设置它：

1. 添加 Linear MCP：
   - `codex mcp add linear --url https://mcp.linear.app/mcp`
2. 启用远程 MCP 客户端：
   - 在 `config.toml` 中设置 `[features] rmcp_client = true` **或**运行 `codex --enable rmcp_client`
3. 使用 OAuth 登录：
   - `codex mcp login linear`

成功登录后，用户必须重新启动 codex。您应该完成您的回答并告诉他们，当他们再次尝试时可以从步骤 1 继续。

**Windows/WSL 注意：**如果您在 Windows 上看到连接错误，请尝试配置 Linear MCP 通过 WSL 运行：
```json
{"mcpServers": {"linear": {"command": "wsl", "args": ["npx", "-y", "mcp-remote", "https://mcp.linear.app/sse", "--transport", "sse-only"]}}
```

### 步骤 1
澄清用户的目标和范围（例如，问题分流、冲刺规划、文档审查、工作负载平衡）。根据需要确认团队/项目、优先级、标签、周期和截止日期。

### 步骤 2
选择适当的工作流程（见下面的实用工作流程）并确定您将需要的 Linear MCP 工具。在调用工具之前确认所需的标识符（问题 ID、项目 ID、团队密钥）。

### 步骤 3
按逻辑批次执行 Linear MCP 工具调用：
- 首先读取（列表/获取/搜索）以构建上下文。
- 接下来创建或更新（问题、项目、标签、评论）以及所有必需的字段。
- 对于批量操作，在应用更改之前解释分组逻辑。

### 步骤 4
总结结果，指出剩余的差距或阻塞，并提出后续行动（额外的问题、标签更改、分配或后续评论）。

## 可用工具

问题管理：`list_issues`、`get_issue`、`create_issue`、`update_issue`、`list_my_issues`、`list_issue_statuses`、`list_issue_labels`、`create_issue_label`

项目与团队：`list_projects`、`get_project`、`create_project`、`update_project`、`list_teams`、`get_team`、`list_users`

文档与协作：`list_documents`、`get_document`、`search_documentation`、`list_comments`、`create_comment`、`list_cycles`

## 实用工作流程

- 冲刺规划：审查目标团队的开放问题，按优先级选择顶级项目，并创建一个带有分配的新周期（例如，"Q1 Performance Sprint"）。
- Bug 分流：列出关键/高优先级的 bug，按用户影响排名，并将顶级项目移至"In Progress"。
- 文档审查：搜索文档（例如，API 身份验证），然后打开标记为"documentation"的问题以获取详细修复的缺口或过时部分。
- 团队工作负载平衡：按受让人分组活动问题，标记任何高负载的人员，并建议或应用重新分配。
- 发布规划：创建一个项目（例如，"v2.0 Release"）以及里程碑（功能冻结、测试版、文档、发布）并生成带有估算的问题。
- 跨项目依赖：查找所有"blocked"问题，识别阻塞者，并在缺少时创建链接的问题。
- 自动状态更新：查找您的状态更新过时的问题，并根据当前状态/阻塞者添加状态评论。
- 智能标签：分析未标记的问题，建议/应用标签，并创建缺少的标签类别。
- 冲刺回顾：为上一个完成的周期生成报告，注意已完成与推送的工作，并为模式打开讨论问题。

## 最大化生产力的提示

- 批量操作相关更改；考虑针对重复问题结构的智能模板。
- 尽可能使用自然查询（"Show me what John is working on this week"）。
- 利用上下文：在新请求中引用先前的问题。
- 将大型更新分解为较小的批次以避免速率限制；在频繁列出时缓存或重用过滤器。

## 故障排除

- 身份验证：清除浏览器 cookie，重新运行 OAuth，验证工作区权限，确保启用 API 访问。
- 工具调用错误：确认模型支持多个工具调用，提供所有必需的字段，并拆分复杂的请求。
- 缺少数据：刷新令牌，验证工作区访问，检查已归档的项目，并确认正确的团队选择。
- 性能：记住 Linear API 速率限制；批量批量操作，使用特定过滤器，或缓存频繁查询。
