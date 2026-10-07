---
name: antigravity-workflows
description: "当被要求交付 SaaS MVP、审计应用程序安全、构建 AI 代理、运行浏览器 QA 或使用多个技能和经过验证的检查点设计域模型时使用。"
risk: none
source: self
date_added: "2026-02-27"
---

# Antigravity 工作流程

使用此技能将复杂的目标转变为有指导的技能调用序列。

## 何时使用此技能

在以下情况下使用此技能：
- 用户想要组合多个技能而无需手动选择每一个。
- 目标是多阶段的（例如：计划、构建、测试、交付）。
- 用户要求对常见场景的最佳实践执行，如：
  - 交付 SaaS MVP
  - 运行网络安全审计
  - 构建 AI 代理系统
  - 实现浏览器自动化和 E2E QA

## 工作流程事实来源

按以下顺序读取工作流程：
1. `docs/users/workflows.md` 用于人类可读的操作手册和记录的案例。
2. `data/workflows.json` 用于机器可读的工作流程元数据。

这些路径属于 AAS 存储库，不一定属于用户的项目。
当它们在独立安装中不存在时，使用捆绑的
[工作流程卡片](references/workflow-cards.md)。不要发明缺失的文件，
无声地获取移动替换，或在项目中创建 AAS 文档。

## 如何运行此技能

1. 识别用户的具体结果。
2. 提议 1-2 个最匹配的工作流程。
3. 遵循已指定的工作流程；仅在选择从根本上改变范围时提出问题。
4. 逐步执行：
   - 宣布当前步骤和预期工件。
   - 为该步骤调用推荐的技能。
   - 在继续下一步之前验证完成标准。
   - 如果检查失败，保留失败，修复相关输入或实现，
     重新运行该检查，并仅在通过后继续。如果先决条件是
     不可用，报告该确切的阻塞步骤并继续独立工作。
   - 在安装前查看确切的技能 ID 及其支持文件。使用
     支持的直接安装程序的 `--dry-run` 与选定的 ID 和目标；
     仅在用户授权范围内安装。核心组合和不可变
     计划保持审查工件，不安装技能。
     如果预览失败，更正 ID、版本、先决条件或目标，并
     再次预览。失败的预览从不授权安装。
5. 最后，提供：
   - 已完成的工件
   - 验证证据
   - 剩余风险和后续操作

## 默认工作流程路由

- 产品交付请求 -> `ship-saas-mvp`
- 安全审查请求 -> `security-audit-web-app`
- 代理/LLM 产品请求 -> `build-ai-agent-system`
- E2E/浏览器测试请求 -> `qa-browser-automation`
- 域驱动设计请求 -> `design-ddd-core-domain`

对于具体的选择和安装程序命令，请参见
[经过审查的选择交接](references/workflow-cards.md#reviewed-selection-handoff)。

## 复制粘贴提示

```text
使用 @antigravity-workflows 为我的项目创意运行"交付 SaaS MVP"工作流程。
```

```text
使用 @antigravity-workflows 并执行完整的"网络应用安全审计"工作流程。
```

```text
使用 @antigravity-workflows 指导我通过"构建 AI 代理系统"工作流程并进行检查点。
```

```text
使用 @antigravity-workflows 执行"QA 和浏览器自动化"工作流程并稳定不稳定的测试。
```

```text
使用 @antigravity-workflows 为我的新服务执行"设计 DDD 核心域"工作流程。
```

## 限制

- 此技能进行编排；它不能替代专门的技能。
- 它取决于引用技能的本地可用性。
- 没有环境访问、凭证或所需基础设施，它不能保证成功。
- 对于 Go 中的堆栈特定浏览器自动化，`go-playwright` 可能需要在本地技能存储库中存在相应的技能。

## 相关技能

- `concise-planning`
- `brainstorming`
- `workflow-automation`
- `verification-before-completion`
