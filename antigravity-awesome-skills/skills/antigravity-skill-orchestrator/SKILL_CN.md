---
name: antigravity-skill-orchestrator
description: "一个元技能，理解任务需求、动态选择适当的技能、使用 agent-memory-mcp 追踪成功的技能组合，并防止对简单任务过度使用技能。"
category: meta
risk: safe
source: community
tags: "[orchestration, meta-skill, agent-memory, task-evaluation]"
date_added: "2026-03-13"
---

# antigravity-skill-orchestrator

## 概述

`skill-orchestrator` 是一个元技能，旨在增强 AI 代理解决复杂问题的能力。它充当一个智能协调器，首先评估用户请求的复杂性。根据该评估，它确定是否需要专门的技能。如果需要，它选择正确的技能组合，使用 `@agent-memory-mcp` 明确追踪这些组合以供将来参考，并指导代理完成执行过程。关键是，它包括严格的防护措施，以防止不必要地对可以通过基本功能解决的简单任务使用专门技能。

## 何时使用此技能

- 当处理可能需要多个专业领域的复杂、多步问题时使用。
- 当您不确定哪些特定技能最适合给定的用户请求，并需要从更广泛的生态系统中发现它们时使用。
- 当用户明确要求对重大任务"编排"、"组合技能"或"使用最佳工具完成工作"时使用。
- 当您想查找特定类型问题的之前成功技能组合时使用。

## 核心概念

### 任务评估防护措施

并非每个任务都需要专门的技能。对于简单的问题（例如，小 CSS 修复、简单脚本编写、重命名变量），**不要使用**专门的技能。过度设计简单任务会浪费令牌和时间。

此外，编排器严格禁止创建新技能。它的唯一目的是组合和使用社区提供的或当前环境中存在的现有技能。

在调用任何技能之前，评估任务：
1. **任务是简单/独立的吗？** 使用代理在当前环境中可用的常规文件编辑、搜索和终端功能直接解决。
2. **任务是复杂/多领域的吗？** 只有这样，您才应该继续编排技能。

### 技能选择与组合

当任务被判定为复杂时，识别必要的领域（例如，前端、数据库、部署）。搜索当前环境中可用的技能以找到最相关的。如果本地找不到所需的技能，请查阅主技能目录。

### 主技能目录

Antigravity 生态系统在 `https://raw.githubusercontent.com/sickn33/agentic-awesome-skills/main/CATALOG.md` 维护一个精选技能的主目录。当本地技能不足时，获取此目录以发现跨 9 个主要类别的适当技能：
- `architecture`
- `business`
- `data-ai`
- `development`
- `general`
- `infrastructure`
- `security`
- `testing`
- `workflow`

### 内存集成（`@agent-memory-mcp`）

为了建立机构知识，编排器依赖于 `agent-memory-mcp` 技能来记录和检索成功的技能组合。

## 分步指南

### 1. 任务评估和防护措施检查

[在面临可能需要技能的新用户请求时触发]
1. 阅读用户的请求。
2. 问自己："我能仅使用基本文件编辑和终端命令有效地解决这个问题吗？"
3. 如果是：继续，无需调用专门的技能。在此处停止编排。
4. 如果否：继续到步骤 2。

### 2. 检索过去的知识

[在任务复杂时触发]
1. 使用 `agent-memory-mcp` 提供的 `memory_search` 工具来搜索类似的过去任务。
   - 示例查询：`memory_search({ query: "skill combination for react native and firebase", type: "skill_combination" })`
2. 如果存在有效的组合，使用 `memory_read` 读取详细信息。
3. 如果不存在相关内存，继续到步骤 3。

### 3. 发现和选择技能

[在没有过去知识覆盖此任务时触发]
1. 分析核心需求（例如，"需要 React UI、Node.js 后端和 PostgreSQL 数据库"）。
2. 使用当前环境的技能列表或等效发现机制查询本地可用的技能，为每个需求找到最佳匹配。
3. **如果本地技能不足**，使用当前环境中可用的 web 或命令行检索工具获取主目录：`https://raw.githubusercontent.com/sickn33/agentic-awesome-skills/main/CATALOG.md`。
4. 扫描目录的 9 个主要类别以识别要引入当前上下文中的适当技能。
5. 选择所需的最少技能集。**不要过度选择。**

### 4. 应用技能并追踪组合

[在使用选定技能执行任务后触发]
1. 假设任务已使用新的技能组合成功完成（例如，`@react-patterns` + `@nodejs-backend-patterns` + `@postgresql`）。
2. 使用 `agent-memory-mcp` 中的 `memory_write` 记录此组合以供将来使用。
   - 确保类型为 `skill_combination`。
   - 提供详细的密钥和内容，说明为什么这些技能能很好地协同工作。

## 示例

### 示例 1：处理简单任务（防护措施的作用）

**用户请求：** "将 `index.css` 中的提交按钮颜色更改为蓝色。"
**操作：** 技能编排器评估任务。它确定这是一个"简单/独立"的任务。它**不会**调用专门的技能。它直接编辑 `index.css`。

### 示例 2：记录新技能组合

```javascript
// 在使用技能成功构建复杂功能后，使用 agent-memory-mcp 工具
memory_write({ 
  key: "combination-ecommerce-checkout", 
  type: "skill_combination", 
  content: "对于电子商务结账，使用 @stripe-integration 与 @react-state-management 和 @postgresql 组合有效处理从 UI 状态到支付处理再到订单记录的完整流程。",
  tags: ["ecommerce", "checkout", "stripe", "react"]
})
```

### 示例 3：检索组合

```javascript
// 在新电子商务任务开始时
memory_search({ 
  query: "ecommerce checkout", 
  type: "skill_combination" 
})
// 返回密钥 "combination-ecommerce-checkout"，然后您读取：
memory_read({ key: "combination-ecommerce-checkout" })
```

## 最佳实践

- ✅ **应该做：** 始终在查找技能*之前*评估任务复杂性。
- ✅ **应该做：** 将编排的技能数量保持尽可能小。
- ✅ **应该做：** 运行 `memory_write` 时使用高度描述性的密钥，以便稍后容易搜索。
- ❌ **不应该做：** 对简单的错误修复或 UI 微调使用此技能。
- ❌ **不应该做：** 组合具有重叠和冲突说明的技能而没有解决冲突的明确计划。
- ❌ **不应该做：** 尝试构造、生成或创建新技能。仅组合可用的内容。

## 相关技能

- `@agent-memory-mcp` - 此技能运行所必需的。为技能组合提供持久存储。

## 限制

- 仅在任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审核的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
