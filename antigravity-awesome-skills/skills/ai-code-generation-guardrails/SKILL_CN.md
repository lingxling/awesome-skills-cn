---
name: ai-code-generation-guardrails
description: '自主 AI 代码生成安全护栏寄存器：静态 AST 分析、禁止导入过滤器和零日漏洞检查。'
category: engineering
risk: safe
source: self
source_type: self
date_added: "2026-10-01"
author: Ranjeet2063
tags: [ai, security, guardrails, ast, code-quality, devsecops]
tools: []
source_repo: Ranjeet2063/agentic-awesome-skills
---

# AI 代码生成安全护栏

**这是什么：** 为生成 AI 模型合成的代码定义自动 AST 验证过滤器、禁止模式检查和边界不变式。

## 概述

为分布式工程和分散应用系统提供 **AI 代码生成安全护栏** 操作的标准化、可审计的框架和数据模型。

## 何时使用此技能

- 当形式化 AI 代码生成安全护栏的架构约定、安全不变式或操作限制时使用。
- 当协议开发人员、智能合约审计人员和 AI 工程代理之间需要跨职能审查时使用。
- 当生成可重现的 CSV、SQL DDL、JSON Schema 和 Notion 属性寄存器来跟踪合规性时使用。

## 工作原理

1. 定义目标操作寄存器所需的参数、阈值和身份绑定。
2. 从验证的枚举选择集中选择适当的边界强制值。
3. 导出标准化工件（CSV 表、SQL DDL、JSON Schema）以集成到验证 CI 管道中。

## 字段参考

| # | 字段名 | 类型 | SQL 类型 | JSON Schema 类型 | Notion 属性类型 | 示例值 |
|---|--------|------|----------|------------------|-----------------|--------|
| 1 | 护栏策略 ID | `id` | `SERIAL PRIMARY KEY` | `integer` | 文本 | `SEC-001` |
| 2 | 目标语言管道 | `select` | `VARCHAR(32)` | `string` | 选择 | `Rust (Soroban)` |
| 3 | AST 安全扫描器 | `text` | `VARCHAR(64)` | `string` | 文本 | `cargo-audit & clippy` |
| 4 | 危险原始类型过滤器 | `select` | `VARCHAR(16)` | `string` | 选择 | `是` |
| 5 | 禁止的不安全块 | `select` | `VARCHAR(16)` | `string` | 选择 | `强制严格` |
| 6 | 重入检测规则 | `select` | `VARCHAR(32)` | `string` | 选择 | `CEI 模式强制` |
| 7 | 提示注入保护 | `select` | `VARCHAR(32)` | `string` | 选择 | `双层边界` |
| 8 | 最大允许圈复杂度 | `number` | `INTEGER` | `number` | 数字 | `15` |
| 9 | 管道强制状态 | `select` | `VARCHAR(32)` | `string` | 选择 | `阻挡 CI 门` |
| 10 | 负责安全工程师 | `text` | `VARCHAR(64)` | `string` | 文本 | `Ranjeet2063` |
| 11 | 策略验证日期 | `date` | `DATE` | `string, format: date` | 日期 | `2026-10-01` |

## 选择选项

**目标语言管道**

```
Rust (Soroban) | TypeScript (React) | Solidity (EVM) | Python (FastAPI)
```

**危险原始类型过滤器**

```
是 | 否
```

**禁止的不安全块**

```
强制严格 | 警告宽容
```

**重入检测规则**

```
CEI 模式强制 | 互斥锁 | 未检查
```

**提示注入保护**

```
双层边界 | 启发式过滤器 | 无
```

**管道强制状态**

```
阻挡 CI 门 | 仅建议 | 禁用
```

## 关系

- `审计参考` -> 链接到正式审查文档或测试存储库。
- `目标架构` -> 链接到部署的合约或自主代理运行时组件。

## 示例

**提示**

```
我如何为生产环境配置和跟踪 AI 代码生成安全护栏？
```

**建议的下一步**

> 生成统一字段架构、SQL DDL 迁移和 JSON 验证架构以注册到您的系统目录中。
>
> 工作流：定义标准 -> 运行自动化验证 -> 记录基线 -> 监控不变式。

## 最佳实践

- 对数值边界和货币金额强制严格类型；避免对关键状态使用非结构化自由文本字段。
- 在每个状态改变提交或参数更改时重新运行验证测试套件。
- 保持示例数据合成且与生产密码密钥或私有端点隔离。

## 限制

- 提供架构规范、数据模型和验证架构；不执行没有授权外部工具的直接交易签署。
- 查询链上状态时需要网络连接和有效的 RPC 凭证。

## 安全与安全性说明

- 所有参数声明 `risk: safe`。不执行任何未授权的状态修改或特权凭证访问。
- 在测试套件和本地验证脚本中使用合成虚拟密钥和模拟地址。

## 常见陷阱

- **问题：** 合约运行时和数据库寄存器之间小数精度不匹配。
  **解决方案：** 始终使用此参考中的显式字段映射验证小数。
- **问题：** 在状态更新前缺少授权检查。
  **解决方案：** 在部署前针对安全审计寄存器进行交叉验证。

## 相关技能

- @ai-agent-tool-routing - 涵盖工具架构注册和重试策略。
- @ai-agent-evaluation-benchmarking - 涵盖任务完成和成本基准测试。
- @ai-prompt-regression-testing - 涵盖提示回归基线和偏差。

## 可重用提示

```
我想为生产协议建立经过验证的 AI 代码生成安全护栏寄存器。
指导我完成所需的字段参数，并输出相应的 SQL DDL 和 JSON Schema。
```
