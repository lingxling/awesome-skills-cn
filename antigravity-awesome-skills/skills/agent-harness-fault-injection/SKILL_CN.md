---
name: agent-harness-fault-injection
description: "适用于智能体工作流需要针对沙箱、MCP/工具、工作进程、检查点、记忆或编排故障获取确定性恢复证据的场景。"
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-19"
author: Whxuan0701
tags: [agent-harness, fault-injection, recovery, state-machine, mcp, multi-agent]
tools: [claude, cursor, gemini, codex-cli]
---

# 智能体测试框架故障注入

## 概述

使用确定性的、非生产的故障计划，测试智能体工作流在依赖项失败时，是否能够保持状态、预算、安全边界和证据。输出包括一个精简的故障矩阵、一条事件时间线，以及一个能区分已恢复、已遏制、不可恢复和无定论运行的结论。

## 何时使用此技能

- 当多步骤智能体、状态机、循环或多智能体工作流新增了恢复路径时使用。
- 当沙箱执行、MCP/工具调用、工作进程、检查点存储或记忆可能超时或消失时使用。
- 在声称重试、恢复、截止时间、隔离或部分失败的行为已达到生产就绪之前使用。
- 当回归问题需要可复现的失败证据，而不是一次随机的混沌运行时使用。

请勿针对生产目标、真实用户数据、实际凭据或不受限的外部服务使用此技能。应先将这些场景转换为本地模拟器或经授权的预发布测试框架。

## 安全与边界前置条件

1. 冻结工作流修订版本、模型/提示词配置、工具模式（schema）、随机种子、输入夹具、超时、重试预算、截止时间和预期的终态。
2. 在一次性沙箱中运行，使用合成输入和打桩（stub）的工具。除非测试明确需要本地测试服务器，否则保持网络禁用。
3. 让每一个注入的故障都是内存中或由夹具控制的事件。绝不要为了制造故障而删除真实数据、撤销真实凭据、杀死无关进程或修改线上服务。
4. 在开始之前记录测试范围和运行标识符。缺少范围、夹具或恢复契约时，结论为 `inconclusive`。

## 恢复契约

在注入故障之前先写下不变量。一份有用的契约会指明必须保留的状态，以及不得重复的副作用：

```text
After recovery, resume from the latest durable checkpoint, preserve the task
identity and safety policy, spend no more than the remaining retry/deadline
budget, and commit each externally visible effect at most once.
```

使用显式状态对工作流建模。例如：

```text
created -> running -> checkpointed -> waiting_for_tool
                       |                |
                       v                v
                    failed <--------- recovering -> resumed -> completed
```

对每一次状态转换，定义其所有者、持久化字段、允许的重试次数和终态行为。除非测试框架证明内存中的值能够在模拟重启后保留，否则它们不算检查点。

## 故障矩阵

选择能够覆盖新恢复逻辑的最小故障集合。在确定性计划通过之前，不要将计划随机化。

| 故障 | 注入边界 | 所需观察 | 预期遏制措施 |
|---|---|---|---|
| 沙箱拒绝 | 工具启动之前 | 无不安全的副作用；原因被保留 | 仅在策略允许时重试 |
| MCP/工具超时 | 请求 ID 分配之后 | 超时被归因到该请求 | 使用相同幂等键进行有界重试 |
| 工作进程重启 | 检查点写入之后 | 工作进程重新加载相同的任务版本 | 从最新检查点恢复 |
| 检查点缺失/过期 | 恢复之前 | 过期数据被拒绝或被标记 | 安全停止；绝不凭空编造进度 |
| 并行分支失败 | 扇出后的某一个分支 | 同级分支的状态被保留 | 由汇合（join）策略决定重试、降级或停止 |
| 记忆丢失 | 清除临时上下文 | 持久化的事实得以重建 | 缺少必需事实时询问或停止 |
| 重试/截止时间耗尽 | 最后一次尝试时 | 不再调度额外调用 | 终态为 `failed` 或 `timed_out` |

## 确定性注入计划

使用事件序号而不是依赖挂钟时间的随机性。计划应当能够在不同测试框架之间移植：

```json
{
  "seed": "harness-fixture-07",
  "faults": [
    {"event": "tool.call", "ordinal": 2, "kind": "timeout", "tool": "search"},
    {"event": "worker.start", "ordinal": 2, "kind": "restart"},
    {"event": "branch.join", "ordinal": 1, "kind": "partial_failure", "branch": "summarize"}
  ]
}
```

测试框架应当输出完整的计划，而不仅仅是种子。将故障标识与观察到的错误分开，这样包装层就不会不小心把超时变成泛化的失败。在尝试其他计划之前，先将同一计划运行两次并比较归一化后的时间线。

## 按边界划分的恢复规则

### 沙箱与 MCP/工具故障

- 在调用之前分配请求 ID 和幂等键。
- 区分超时、显式工具错误、无效输出和策略拒绝。
- 仅重试已声明的可重试类别；在证据中保留原始错误和尝试次数。
- 除非工具契约表明该键可以安全重放，否则不要重试有副作用的操作。读取超时并不能证明写入没有发生。
- 当截止时间或重试预算耗尽时，发出一个终态事件并停止调度工作。

### 工作进程重启与检查点

- 在重启测试之前，持久化任务 ID、工作流版本、状态名、已完成的效果、剩余预算和检查点序号。
- 重新加载最新的有效检查点，并拒绝未来版本或已损坏的检查点，而不是去猜测。
- 验证恢复不会重放已提交的效果。如果无法证明恰好一次，则降级结论并要求进行对账。

### 并行分支

将每个分支表示为其自己的子尝试。汇合记录必须保留成功、失败、超时和未启动这几种状态。选择一种预先声明的汇合策略：

- `all_required`：任何必需分支失败都会终止汇合；
- `best_effort`：继续执行，并附带明确的降级标记；
- `compensate`：执行有界的补偿动作，然后停止或恢复。

绝不要让成功的同级分支从最终台账中抹去失败的分支。

### 记忆丢失

仅清除计划中指定的临时上下文。从检查点和持久化证据中重建，然后检查智能体没有编造缺失的用户意图、工具输出或批准。如果缺少必需的事实，安全的结果是 `inconclusive` 或进入人工澄清状态。

## 预算与终态结论

在每个事件之后跟踪剩余尝试次数和剩余时间。不要在工作进程重启或分支重试时重置预算。使用以下结论：

| 结论 | 含义 |
|---|---|
| `recovered` | 声明的不变量得以保持，且工作流在预算内完成。 |
| `contained_failure` | 故障被隔离，工作流按设计安全停止。 |
| `unrecoverable` | 恢复违反了不变量、重复了副作用、越过了边界或超出了预算。 |
| `inconclusive` | 夹具、检查点、契约或证据不足以做出判断。 |

`contained_failure` 不等于自主成功。应将其与已完成的工作分开报告，并附上终止原因。

## 证据输出

生成一份机器可读的记录和一份简明的人类可读摘要。每个事件都应包含 `run_id`、单调递增的 `seq`、逻辑 `time`、`state_before`、`state_after`、`actor`、`event`、`fault_id`（注入时）、`attempt`、`checkpoint_seq`、`retry_remaining`、`deadline_remaining_ms`，以及经过脱敏的 `evidence_ref`。

```json
{
  "run_id": "fi-2026-08-19-07",
  "verdict": "recovered",
  "invariants": {"resume_from_checkpoint": "pass", "effect_at_most_once": "pass", "budget": "pass"},
  "faults": [{"id": "f1", "kind": "tool_timeout", "at": "tool.call#2", "handled": true}],
  "timeline": [
    {"seq": 4, "event": "checkpoint.write", "checkpoint_seq": 3},
    {"seq": 5, "event": "tool.timeout", "fault_id": "f1", "retry_remaining": 1},
    {"seq": 8, "event": "workflow.completed", "checkpoint_seq": 4}
  ],
  "limitations": ["Tool output was synthetic; no deployed MCP was exercised."]
}
```

人类可读的摘要应说明冻结的契约、注入的计划、结论、未通过的不变量、预算消耗，以及范围最窄的下一步验证。对提示词、令牌、私有记录和工具载荷进行脱敏；稳定的引用已足够用于重放。

## 示例：本地测试框架运行

```text
Fixture: checkout planner / seed harness-fixture-07
Schedule: search timeout on call 2; worker restart after checkpoint 3
Policy: one retry, 2s deadline, all_required branch join

Result: recovered
Proof: checkpoint 3 reloaded, search request key replayed once, no duplicate
commit, deadline remaining 640ms, final ledger contains both branch outcomes.
```

## 最佳实践

- 冻结输入和计划，使故障可以依据证据重放。
- 一次只测试一个边界，然后再添加组合计划来覆盖交互风险。
- 在每次恢复转换之后断言不变量，而不仅仅在最终输出时断言。
- 将尝试级故障与任务级结果保存在不同的台账中。
- 将缺失的证据视为 `inconclusive`，绝不视为恢复通过。

## 局限性

- 本地桩无法证明已部署的模型、MCP 服务器、调度器、文件系统或网络的行为。
- 确定性计划只覆盖已命名的路径；它们不能估计随机故障的频率，也无法发现未知的失败模式。
- 至多一次的效果需要有幂等且可观察的契约；仅凭时间线无法证明外部写入没有被重复。
- 此技能不会选择生产 SLO、修复损坏的工作流，也不会授权测试声明沙箱之外的系统。

## 安全与保障说明

- 默认保持测试仅限本地且只读；使用合成夹具和无法访问真实账户的假凭据。
- 在进行任何可能接触非本地服务的测试之前，要求明确授权和一次性的预发布边界。
- 不要在测试框架或报告中包含破坏性命令、利用载荷、凭据材料或对用户数据的自动清理。
- 在存储时间线或将其附加到拉取请求之前，对密钥和个人数据进行脱敏。

## 常见陷阱

- **问题：** 重试清除了原始超时并掩盖了故障。
  **解决方案：** 在台账中保留故障 ID、原始类别、尝试次数和重试谱系。
- **问题：** 重启测试之所以通过，是因为测试复用了内存中的状态。
  **解决方案：** 仅对声明的检查点字段进行序列化、清除和重新加载。
- **问题：** 部分扇出被报告为成功。
  **解决方案：** 保留每个分支的状态，并应用预先声明的汇合策略。
- **问题：** 缺失的检查点被猜测的进度所替代。
  **解决方案：** 安全停止，并连同证据返回 `inconclusive` 或 `unrecoverable`。
- **问题：** 一个看似正常的最终答案掩盖了截止时间或重复效果的违规。
  **解决方案：** 让结论取决于不变量和剩余预算，而不仅仅是输出文本。

## 相关技能

- `@agent-evaluation-reporting` - 报告自主、辅助、失败、超时和无效的结果。
- `@cross-platform-contract-propagation-audit` - 跨消费方追踪恢复字段和状态契约。
- `@multi-agent-patterns` - 在测试多智能体拓扑的失败行为之前，先选定拓扑。
