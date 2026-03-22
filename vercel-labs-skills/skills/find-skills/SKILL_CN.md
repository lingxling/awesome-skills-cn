---
name: find-skills
description: 帮助用户发现和安装 agent skills，当用户问"如何做X"、"找一个X的skill"、"有没有一个skill可以..."或表达对扩展能力的兴趣时使用。当用户寻找可能作为可安装skill存在的功能时，应使用此skill。
---

# 发现 Skills

此技能帮助你从开放的 agent skills 生态系统中发现和安装 skills。

## 何时使用此技能

当用户出现以下情况时使用此技能：

- 问"如何做X"，其中X可能是已有skill的常见任务
- 说"找一个X的skill"或"有没有一个X的skill"
- 问"你能做X吗"，其中X是专业能力
- 表达对扩展agent能力的兴趣
- 想要搜索工具、模板或工作流程
- 提到希望在某特定领域获得帮助（设计、测试、部署等）

## 什么是 Skills CLI？

Skills CLI（`npx skills`）是开放 agent skills 生态系统的包管理器。Skills 是模块化包，通过专业知识和工作流程、工具来扩展agent能力。

**核心命令：**

- `npx skills find [query]` - 交互式或按关键词搜索skills
- `npx skills add <package>` - 从GitHub或其他来源安装skill
- `npx skills check` - 检查skill更新
- `npx skills update` - 更新所有已安装的skills

**浏览skills地址：** https://skills.sh/

## 如何帮助用户发现 Skills

### 步骤1：理解他们的需求

当用户请求帮助时，识别：

1. 领域（例如：React、测试、设计、部署）
2. 具体任务（例如：编写测试、创建动画、审查PR）
3. 这是否是常见到很可能存在skill的任务

### 步骤2：搜索 Skills

使用相关查询运行find命令：

```bash
npx skills find [query]
```

例如：

- 用户问"如何让我的React应用更快？" → `npx skills find react performance`
- 用户问"你能帮我审查PR吗？" → `npx skills find pr review`
- 用户问"我需要创建一个变更日志" → `npx skills find changelog`

命令将返回如下结果：

```
使用 npx skills add <owner/repo@skill> 安装

vercel-labs/agent-skills@vercel-react-best-practices
└ https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

### 步骤3：向用户展示选项

当找到相关skills时，向用户展示：

1. skill名称及其功能
2. 他们可以运行的安装命令
3. 了解更多信息的链接到skills.sh

示例响应：

```
我找到了一个可能有帮助的skill！"vercel-react-best-practices" skill
提供来自Vercel工程的React和Next.js性能优化指南。

安装方法：
npx skills add vercel-labs/agent-skills@vercel-react-best-practices

了解更多：https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

### 步骤4：提供安装

如果用户想要继续，你可以为他们安装skill：

```bash
npx skills add <owner/repo@skill> -g -y
```

`-g` 标志全局安装（用户级别），`-y` 跳过确认提示。

## 常见 Skill 类别

搜索时，考虑这些常见类别：

| 类别 | 示例查询 |
| --------------- | ---------------------------------------- |
| Web 开发 | react, nextjs, typescript, css, tailwind |
| 测试 | testing, jest, playwright, e2e |
| DevOps | deploy, docker, kubernetes, ci-cd |
| 文档 | docs, readme, changelog, api-docs |
| 代码质量 | review, lint, refactor, best-practices |
| 设计 | ui, ux, design-system, accessibility |
| 生产力 | workflow, automation, git |

## 有效搜索技巧

1. **使用具体关键词**："react testing"比只用"testing"更好
2. **尝试替代术语**：如果"deploy"不起作用，尝试"deployment"或"ci-cd"
3. **检查流行来源**：许多skills来自`vercel-labs/agent-skills`或`ComposioHQ/awesome-claude-skills`

## 未找到 Skills 时

如果没有找到相关的skills：

1. 承认没有找到现有的skill
2. 提供使用通用能力直接帮助完成任务
3. 建议用户可以使用`npx skills init`创建自己的skill

示例：

```
我搜索了与"xyz"相关的skills，但没有找到匹配项。
我仍然可以直接帮助你完成此任务！你希望我继续吗？

如果你经常需要做这个，你可以创建自己的skill：
npx skills init my-xyz-skill
```
