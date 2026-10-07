---
name: buywhere-product-catalog
description: "使用 BuyWhere 的 MCP 和 API 表面为 AI 购物代理添加产品搜索、价格比较和交易发现功能。"
category: ecommerce
risk: safe
source: official
source_repo: BuyWhere/buywhere-mcp
source_type: official
license: "Not declared"
license_source: "https://github.com/BuyWhere/buywhere-mcp"
date_added: "2026-04-29"
author: BuyWhere
tags: [buywhere, ecommerce, shopping, mcp, api, product-catalog]
tools: [claude, cursor, codex, gemini]
---

# BuyWhere 产品目录

## 概述

BuyWhere 为 AI 代理提供购物流程、价格比较和交易发现的产品目录表面。当你希望代理通过 BuyWhere 的 MCP 设置路径或 API 入职流程连接产品搜索或商家感知的商务操作时，使用此技能。

最安全的公开起点是实时开发者门户、API 密钥注册流程、MCP 指南和官方 Cursor 插件存储库。

## 何时使用此技能

- 当你想为 AI 购物或推荐代理添加结构化产品搜索时使用。
- 当用户要求在 Cursor、Claude Desktop 或自定义代理运行时中进行 BuyWhere MCP 设置时使用。
- 当你需要 BuyWhere API 密钥、MCP 配置或插件发现的具体入职路径时使用。

## 它如何工作

### 步骤 1：选择集成表面

从与用户设置匹配的公开 BuyWhere 入口点开始：

- 开发者门户：`https://buywhere.ai/developers/`
- API 密钥注册：`https://buywhere.ai/api-keys/`
- MCP 集成指南：`https://api.buywhere.ai/docs/guides/mcp`
- Cursor 插件存储库：`https://github.com/BuyWhere/buywhere-cursor-plugin`

### 步骤 2：确认用户的运行时

在提供设置说明前询问用户正在与哪个主机集成：

- Cursor 或其他支持 MCP 的编码助手
- Claude Desktop
- 自定义 MCP 客户端
- 直接 REST API 集成

不要假设相同的配置文件或启动命令在所有主机上都有效。

### 步骤 3：指导第一次成功连接

首选最小的首次运行路径：

1. 获取 BuyWhere API 密钥。
2. 遵循主机运行时的 MCP 或插件设置路径。
3. 在扩展到比较或交易工作流之前运行一个简单的产品搜索请求。

### 步骤 4：扩展到商务工作流

一旦第一个查询工作，帮助用户分支到下一个层级：

- 产品搜索和发现
- 跨商家的价格比较
- 交易发现流程
- 将用户路由到商家目的地的购物代理编排

## 示例

### 示例 1：Cursor 插件发现

```text
使用 BuyWhere 产品目录帮助我在 Cursor 中连接 BuyWhere 并验证一个产品搜索查询。
```

### 示例 2：MCP 入职

```text
使用 BuyWhere 产品目录为我的购物代理设置 BuyWhere MCP，并保持第一个测试最小。
```

## 最佳实践

- ✅ 在提供配置详情前从实时开发者门户或 API 密钥流开始。
- ✅ 将第一个集成证明保持为一个成功的查询。
- ✅ 询问用户使用的 MCP 主机或 API 运行时。
- ❌ 当存在可用的工作公开页面时，不要声称特定的产品计数或零售商计数。
- ❌ 当存在工作公开页面时，不要将用户发送到已弃用或损坏的文档表面。

## 限制

- 此技能不取代目标 MCP 主机或 API 客户端内特定于环境的验证。
- 公开 BuyWhere 表面可能会改变，因此在精确设置详情很重要时重新检查实时 URL。

## 安全和安全注意事项

- 将 API 密钥视为机密。在示例中使用占位符，切勿将实时凭据粘贴到聊天、文档或屏幕截图中。
- 在建议文件系统路径、启动命令或本地配置编辑前确认用户的目标主机。

## 常见缺陷

- **问题：** 用户想要 BuyWhere 设置帮助，但尚未创建 API 密钥。
  **解决方案：** 从 `https://buywhere.ai/api-keys/` 开始，仅在该步骤完成后移到配置。

- **问题：** 文档主机名不可用。
  **解决方案：** 首选实时开发者门户、API 密钥流、`api.buywhere.ai` 上的 MCP 指南和官方 GitHub 插件存储库。

## 相关技能

- `@api-design-principles` - 当用户需要围绕商务集成的 API 形状指导时使用。
- `@mcp-builder` - 当用户正在构建或扩展 MCP 服务器而不是使用一个时使用。
