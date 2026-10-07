---
name: architecture-review
description: 使用 Ontoly 软件图和 MCP 能力审查代码库架构。当被要求解释架构、模块边界、包拓扑、服务所有权或架构风险时使用。
license: AGPL-3.0-only
compatibility: 可移植代理技能格式；需要 Ontoly CLI 和支持 MCP 或 CLI 的编码代理。
metadata:
  ontoly.skill.version: 1.3.3
  ontoly.min.version: 1.3.3
  ontoly.capabilities: ExplainArchitecture, GraphStatistics, FindCycles, FindDependencies,
    EvidencePack
  ontoly.category: architecture
  ontoly.enhancement: LLM Enhancement
  ontoly.deprecated: 'false'
source_repo: 0xsarwagya/ontoly
source_type: community
source: community
date_added: '2026-09-21'
risk: unknown
---
## 何时使用

- 当上游工作流与用户说明的目标匹配时使用。
- 当任务需要此技能中记录的程序时使用。

# 架构审查

当用户要求使用 Ontoly 证据进行架构审查时使用此技能。

## 必需工作流

遵循[共享的 Ontoly 工作流。同时阅读[图证据规则、[MCP 使用、[最佳实践和[当任务需要详细信息时的回退规则。

## Ontoly 能力

首先使用这些能力：`ExplainArchitecture`、`GraphStatistics`、`FindCycles`、`FindDependencies`、`EvidencePack`。

## 输出合约

返回：

- 答案或计划
- 调用的能力
- 图证据，包含节点 ID、边类型、源跨度和图哈希（如果可用）
- 置信度：高、中或低
- 如果检查了代码库文件，则提供回退原因

## 边界

不在技能中实现编译器、查询、MCP、SDK 或业务逻辑。在 Ontoly 无法回答或必须确认证据之前，不搜索代码库文件。

## 资源

- [示例
- [提示模板
- [能力说明

## 了解更多

- 文档：https://ontoly.xyz/docs
- 此技能在网上：https://ontoly.xyz/skills#architecture-review
- 所有 Ontoly 代理技能：https://ontoly.xyz/skills
- 通过 skills.sh 安装：https://www.skills.sh/?q=0xsarwagya/ontoly

## 示例

```text
用户：将此技能应用于我的当前任务。
助手：遵循此技能中的工作流，引用限制，并在风险步骤之前询问。
```

## 限制

- 导入的上游技能；在执行前验证凭证、权限和安全边界。
- 不会替代特定环境的验证、测试或维护者审查。
