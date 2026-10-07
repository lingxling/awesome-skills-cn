---
name: ai-dev-jobs-mcp
description: "通过 AI Dev Jobs MCP 搜索 489 家公司中的 8,400+ AI 和 ML 工作，检查职位清单和雇主、匹配角色并查看薪酬和市场统计数据"
category: mcp
risk: safe
source: "https://aidevboard.com"
source_type: community
date_added: "2026-04-16"
author: unitedideas
tags: [mcp, jobs, ai-jobs, ml-jobs, recruiting, job-search, career]
tools: [claude, cursor, gemini]
---

# AI Dev Jobs MCP

## 概述

AI Dev Jobs 是一个远程 MCP 服务器，为 AI 代理提供对实时 AI 和 ML 职位清单索引的访问。截至 2026 年 4 月 17 日，实时 MCP 统计报告显示 489 家公司中有 8,405 个活跃职位，中位薪酬为 $213,500，本周新增 600 个职位。代理可以按角色、位置或公司搜索职位，检索完整的职位详情、列出招聘公司、匹配职位到个人资料，以及获取薪酬或聚合市场统计数据。它专为协助职位搜索、招聘或劳动力市场分析的 AI 代理设计。

## 何时使用此技能

- 当帮助用户搜索 AI 或 ML 工程职位时使用
- 当代理需要查找哪些公司正在招聘特定 AI 角色时使用
- 当构建招聘或人才匹配工作流时使用
- 当分析 AI 职位市场（空缺职位、顶级公司、角色分布）时使用

## MCP 配置

将 AI Dev Jobs MCP 服务器添加到您的客户端配置。端点使用可流式 HTTP，不需要身份验证。

### Claude Desktop / Cursor / Windsurf

```json
{
  "mcpServers": {
    "ai-dev-jobs": {
      "url": "https://aidevboard.com/mcp"
    }
  }
}
```

不需要 API 密钥或身份验证。

## 可用工具

### `search_jobs`

按关键字、位置、公司或工作安排搜索职位索引。返回匹配的职位清单，包括职位名称、公司、位置和薪酬信息。

```
search_jobs({ query: "machine learning engineer", location: "remote" })
```

### `get_job`

按 ID 检索特定职位清单的完整详情，包括描述、要求、薪酬范围和应聘链接。

```
get_job({ id: "abc123" })
```

### `list_companies`

列出索引中的所有公司及其空缺职位数。对于发现哪些公司正在积极招聘很有用。

```
list_companies({})
```

### `get_company`

检索特定公司的详情，包括端点公开的可用 AI 角色。

```
get_company({ id: "openai" })
```

### `get_stats`

获取关于职位市场的聚合统计数据：总清单数、空缺职位最多的顶级公司、角色分布和位置细分。

```
get_stats({})
```

### `match_jobs`

针对候选人资料、技能列表或偏好将职位进行匹配。

```
match_jobs({ skills: ["python", "llm", "pytorch"], workplace: "remote" })
```

### `get_salary_data`

在可用的情况下检索职位、标签、等级或位置的薪酬统计数据。

```
get_salary_data({ tag: "llm", level: "senior" })
```

### `list_tags`

列出可用于过滤搜索或薪酬分析的索引标签。

```
list_tags({})
```

## 示例

### 示例 1：查找远程 ML 职位

```text
使用 @ai-dev-jobs-mcp 查找远程机器学习工程师职位。
```

代理将调用 `search_jobs({ query: "machine learning engineer", location: "remote" })` 并返回匹配的职位清单。

### 示例 2：检查哪些公司正在招聘

```text
使用 @ai-dev-jobs-mcp 列出所有当前正在招聘 AI 角色的公司。
```

代理将调用 `list_companies({})` 并按空缺职位数量排序返回公司。

### 示例 3：获取职位市场概览

```text
使用 @ai-dev-jobs-mcp 显示当前 AI 职位市场统计数据。
```

代理将调用 `get_stats({})` 并返回关于职位清单、顶级雇主和角色分布的聚合数据。

### 示例 4：获取完整职位详情

```text
使用 @ai-dev-jobs-mcp 获取职位 ID abc123 的完整详情。
```

代理将调用 `get_job({ id: "abc123" })` 并返回完整的职位清单，包括要求和应聘链接。

### 示例 5：将职位与候选人资料进行匹配

```text
使用 @ai-dev-jobs-mcp 将远程 LLM 角色与资深 Python 和 PyTorch 资料进行匹配。
```

代理将调用 `match_jobs({ skills: ["python", "llm", "pytorch"], workplace: "remote" })` 并返回合适的职位清单。

### 示例 6：比较薪酬数据

```text
使用 @ai-dev-jobs-mcp 比较资深 LLM 薪酬数据。
```

代理将调用 `get_salary_data({ tag: "llm", level: "senior" })` 并总结可用的薪酬范围。

## 最佳实践

- 使用 `search_jobs` 并带上具体关键字以获得针对性结果，而不是宽泛查询
- 使用 `list_companies` 发现公司，然后 `search_jobs` 按公司名称过滤以进行专注搜索
- 使用 `get_stats` 在深入到特定职位清单前为用户提供市场背景
- 当用户提供技能、资历、位置或工作安排偏好时使用 `match_jobs`
- 仅将 `get_salary_data` 用作市场背景；提醒用户职位清单和薪酬变化迅速
- 与简历或求职信技能结合，创建端到端职位应聘工作流

## 限制

- 该索引特别覆盖 AI 和 ML 角色；AI 领域外的一般软件工程职位可能不包括在内。
- 职位清单定期更新，但新职位发布前可能有短延迟。
- 当公司提供薪酬数据时可获得；并非所有职位清单都包括薪酬信息。
- 数量和薪酬中位数是实时市场数据，在用户面向输出中引用前应使用 `get_stats` 进行刷新。

## 相关技能

- `@not-human-search-mcp` - 通过 MCP 发现 AI 就绪的工具和 API
- `@mcp-builder` - 用于构建您自己的 MCP 服务器
