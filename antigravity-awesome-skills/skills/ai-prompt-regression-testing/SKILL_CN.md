---
name: ai-prompt-regression-testing
description: '提示工程回归测试矩阵注册表：基线输出、语义漂移阈值、判断评估和黄金数据集。'
category: engineering
risk: safe
source: self
source_type: self
date_added: "2026-10-01"
author: Ranjeet2063
tags: [ai, prompt-engineering, testing, evaluation, llm, benchmarking]
tools: []
source_repo: Ranjeet2063/agentic-awesome-skills
---

# AI 提示回归测试矩阵

**什么是它：** 追踪回归基线、评估标准和自动判断判决，以防止提示修订中的输出降级。

## 概述

为分布式工程和去中心化应用系统中的 **AI 提示回归测试矩阵** 操作提供标准化、可审计的框架和数据模型。

## 何时使用此技能

- 当为 AI 提示回归测试矩阵形式化架构合同、安全不变量或操作限制时。
- 当需要协议开发人员、智能合约审计员和 AI 工程代理之间的跨职能审查时。
- 当生成可重现的 CSV、SQL DDL、JSON Schema 和 Notion 属性注册表以追踪合规性时。

## 工作原理

1. 为目标操作注册表定义所需的参数、阈值和身份绑定。
2. 从验证的枚举选择集中选择适当的边界强制值。
3. 导出标准化工件（CSV 表、SQL DDL、JSON Schema）以集成到验证 CI 管道中。

## 字段参考

| # | 字段名称 | 类型 | SQL 类型 | JSON Schema 类型 | Notion 属性类型 | 示例值 |
|---|---------|------|---------|------------------|-----------------|--------|
| 1 | 提示测试用例 ID | `id` | `SERIAL PRIMARY KEY` | `integer` | 文本 | `PTEST-001` |
| 2 | 提示标识符 | `text` | `VARCHAR(64)` | `string` | 文本 | `soroban_code_refactor_v2` |
| 3 | 目标 LLM 模型系列 | `select` | `VARCHAR(64)` | `string` | 选择 | `Claude 3.5 Sonnet` |
| 4 | 评估指标 | `select` | `VARCHAR(64)` | `string` | 选择 | `AST 代码正确性` |
| 5 | 语义漂移阈值 | `number` | `NUMERIC(5,2)` | `number` | 数字 | `0.05` |
| 6 | 黄金基线匹配 % | `number` | `NUMERIC(5,2)` | `number` | 数字 | `98.50` |
| 7 | 判断模型评估器 | `text` | `VARCHAR(64)` | `string` | 文本 | `Gemini 1.5 Pro` |
| 8 | 零样本推理已验证 | `select` | `VARCHAR(16)` | `string` | 选择 | `是` |
| 9 | 延迟界限秒 | `number` | `NUMERIC(6,2)` | `number` | 数字 | `3.20` |
| 10 | 测试套件判决 | `select` | `VARCHAR(32)` | `string` | 选择 | `通过` |
| 11 | 基准测试日期 | `date` | `DATE` | `string, format: date` | 日期 | `2026-10-01` |

## 选择选项

**目标 LLM 模型系列**

```
Claude 3.5 Sonnet | GPT-4o | Gemini 1.5 Pro | DeepSeek Coder
```

**评估指标**

```
AST 代码正确性 | 语义嵌入余弦 | 精确匹配 | 评分表
```

**零样本推理已验证**

```
是 | 否
```

**测试套件判决**

```
通过 | 降级 | 回归失败
```

## 关系

- `审计参考` -> 链接到正式审查文档或测试存储库。
- `目标架构` -> 链接到已部署的合同或自主代理运行时组件。

## 示例

**提示**

```
我如何为生产环境配置和追踪 AI 提示回归测试矩阵？
```

**建议的下一步**

> 生成统一的字段模式、SQL DDL 迁移和 JSON 验证模式，以注册到您的系统目录中。
>
> 工作流：定义标准 -> 运行自动验证 -> 记录基线 -> 监控不变量。

## 最佳实践

- 对数值界限和金额强制严格类型；避免为关键状态使用非结构化自由文本字段。
- 在每次改变状态的提交或参数更改时重新运行验证测试套件。
- 保持示例数据是合成的，与生产密码密钥或私有端点隔离。

## 限制

- 提供架构规范、数据模型和验证模式；在没有授权外部工具的情况下不执行直接交易签名。
- 查询链上状态时需要网络连接和有效的 RPC 凭证。

## 安全和安全说明

- 所有参数声明 `risk: safe`。不执行未授权的状态修改或特权凭证访问。
- 在测试套件和本地验证脚本中使用合成虚拟密钥和模拟地址。

## 常见缺陷

- **问题：** 合同运行时和数据库注册表之间小数精度不匹配。
  **解决方案：** 始终使用此参考中的显式字段映射验证小数。
- **问题：** 在状态更新前缺少授权检查。
  **解决方案：** 在部署前交叉验证安全审计注册表。

## 相关技能

- @ai-agent-tool-routing - 涵盖工具模式注册和重试策略。
- @cross-chain-relayer-audit - 涵盖消息哈希、随机数和仲裁证明。
- @smart-contract-formal-verification - 以数学方式验证状态不变量。

## 可重用提示

```
我想为我们的生产协议建立一个经过验证的 AI 提示回归测试矩阵注册表。
指导我完成所需的字段参数，并输出相应的 SQL DDL 和 JSON Schema。
```
