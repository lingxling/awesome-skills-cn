---
name: ai-agent-evaluation-benchmarking
description: '自主 AI 代理基准评估寄存器：任务完成率、规划精度、工具调用精度和成本基准。'
category: engineering
risk: safe
source: self
source_type: self
date_added: "2026-10-01"
author: Ranjeet2063
tags: [ai, agents, evaluation, benchmarks, llm, automation, quality]
tools: []
source_repo: Ranjeet2063/agentic-awesome-skills
---

# AI 代理能力评估和基准测试

**这是什么：** 在自主编码代理中标准化多指标能力基准测试、令牌成本效率和回归监控。

## 概述

为分布式工程和分散应用系统提供 **AI 代理能力评估和基准测试** 操作的标准化、可审计的框架和数据模型。

## 何时使用此技能

- 当形式化 AI 代理能力评估和基准测试的架构约定、安全不变式或操作限制时使用。
- 当协议开发人员、智能合约审计人员和 AI 工程代理之间需要跨职能审查时使用。
- 当生成可重现的 CSV、SQL DDL、JSON Schema 和 Notion 属性寄存器来跟踪合规性时使用。

## 工作原理

1. 定义目标操作寄存器所需的参数、阈值和身份绑定。
2. 从验证的枚举选择集中选择适当的边界强制值。
3. 导出标准化工件（CSV 表、SQL DDL、JSON Schema）以集成到验证 CI 管道中。

## 字段参考

| # | 字段名 | 类型 | SQL 类型 | JSON Schema 类型 | Notion 属性类型 | 示例值 |
|---|--------|------|----------|------------------|-----------------|--------|
| 1 | 基准测试运行 ID | `id` | `SERIAL PRIMARY KEY` | `integer` | 文本 | `BENCH-001` |
| 2 | 评估代理模型 | `select` | `VARCHAR(64)` | `string` | 选择 | `Claude 3.7 Sonnet` |
| 3 | 基准测试套件域 | `select` | `VARCHAR(64)` | `string` | 选择 | `SWE-bench Verified` |
| 4 | 评估的任务数量 | `number` | `INTEGER` | `number` | 数字 | `100` |
| 5 | 通过率百分比 | `number` | `NUMERIC(5,2)` | `number` | 数字 | `78.40` |
| 6 | 工具幻觉率 % | `number` | `NUMERIC(5,2)` | `number` | 数字 | `0.60` |
| 7 | 每个任务的平均令牌数 | `number` | `INTEGER` | `number` | 数字 | `42500` |
| 8 | 每个解决的任务成本美元 | `currency` | `NUMERIC(8,4)` | `number` | 数字 | `0.3420` |
| 9 | 回归评估 | `select` | `VARCHAR(32)` | `string` | 选择 | `Superior` |
| 10 | 评估负责人 | `text` | `VARCHAR(64)` | `string` | 文本 | `Ranjeet2063` |
| 11 | 基准测试执行日期 | `date` | `DATE` | `string, format: date` | 日期 | `2026-10-01` |

## 选择选项

**评估代理模型**

```
Claude 3.7 Sonnet | Claude 3.5 Sonnet | GPT-4o | Gemini 2.0 Flash | DeepSeek V3
```

**基准测试套件域**

```
SWE-bench Verified | WebArena | AgentBench | HumanEval-Rust | Web3AuditBench
```

**回归评估**

```
Superior | Parity Baseline | Regression Failure
```

## 关系

- `审计参考` -> 链接到正式审查文档或测试存储库。
- `目标架构` -> 链接到部署的合约或自主代理运行时组件。

## 示例

**提示**

```
我如何为生产环境配置和跟踪 AI 代理能力评估和基准测试？
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
- @ai-prompt-regression-testing - 涵盖提示回归基线和偏差。
- @ai-code-generation-guardrails - 涵盖生成代码的静态护栏。

## 可重用提示

```
我想为生产协议建立经过验证的 AI 代理能力评估和基准测试寄存器。
指导我完成所需的字段参数，并输出相应的 SQL DDL 和 JSON Schema。
```
