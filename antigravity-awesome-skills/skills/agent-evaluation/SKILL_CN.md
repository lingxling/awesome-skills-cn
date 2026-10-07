---
name: agent-evaluation
description: "使用版本化用例和显式验证器评估代理行为。在比较代理或提示变更、重现失败或运行代理回归测试时使用。"
risk: safe
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# 代理评估

针对特定任务的用例评估可观察到的代理行为。由 AAS 维护者在 2026-09-05 修改，以删除不支持的基准声明、纠正不确定性/错误报告，并将可选的架构草图与操作程序分开。

## 何时使用

在比较更改的代理、提示或工具配置、重现观察到的失败或在声明的任务分布上估计可靠性时使用。不要从公共基准百分比或通用分数阈值推断产品就绪情况。

## 前置条件

- 一个带有预期可观察结果和权限边界的版本化用例集。
- 一个已知的基准和候选修订版本，包括模型、提示、工具、配置和运行时版本。
- 授权的合成或编辑的输入、隔离的目标和有限的令牌、时间和成本预算。
- 一个验证器，可区分错误的结果、预期的安全拒绝、评估器失败和基础设施中断。只有在声明的评估调用该提供商时才需要提供商访问权限。

## 评估程序

1. **冻结合同。**在执行前记录用例 ID 和数据集修订版本、基准/候选身份、目标环境、重复计划、预算、停止规则和决策标准。保持关键的安全和授权失败与平均质量分开；它们不能通过更高的分数来补偿。
2. **验证工具。**运行一个已知通过的用例、一个已知失败的用例和一个故意的验证器/基础设施失败。确认每一个都被正确分类，并且跟踪保留排除凭证和私有输入体。如果分类错误，请修复工具并在测量代理前重复这些检查。
3. **运行冻结的用例。**对基准和候选使用相同的用例定义和预算，具有独立的fixture状态和记录的执行顺序。保留每个尝试及其运行 ID、结果、原因、延迟和资源总数。异常不是证明不安全请求被安全拒绝的证据。
4. **调查变异。**保留原始失败。将分歧分类为代理行为、共享状态污染、验证器歧义或中断。仅使用预先声明的重复预算；不要重试直到绿色，不要无声地删除失败或更改预期结果以适应候选项。未解决的工具故障使受影响的结果不确定。
5. **比较和决定。**报告每个用例的结果和不确定性、回归、关键失败和不完整的用例。一个用例的重复运行不是任务分布的独立样本。更改的预期需要单独审查的合同修订和基准和候选的重新运行；保留旧结果。
6. **修复和验证。**进行有限的修复，重新运行失败的用例以验证机制，然后从干净状态重新运行适用的冻结回归套件。如果分歧持续，请在声明的预算处停止。使用精确证据记录通过、失败或不确定；单独遵循项目发布/部署批准边界。

## 示例：更改的工具参数处理

合成代理更改了它如何为只读查找选择租户标识符的方式。冻结三个用例：授权的查找必须返回种植的fixture，未授权的租户必须被拒绝而没有工具调用，模拟的工具中断必须被分类为基础设施失败。既不提供真实的客户记录也不提供生产凭证。

预先声明每个用例有五个重复，状态为新鲜，基准和候选的预算相同，对未授权的工具调用的容限为零。假设候选在所有五次运行中返回预期的授权结果，但在第二个用例中进行一次未授权调用：即使其总体成功率提高，候选也会失败权限合同。保留该运行，修复参数授权，验证负面用例，并重新运行冻结套件。如果中断检测器本身崩溃，请将该用例标记为不确定并在比较版本前修复检测器。这些是说明性结果，而不是测量的代理结果。

预期输出：

```text
contract: case-set revision, rules, repeat plan and budget
versions: baseline, candidate, model, prompt, tool and runtime
runs: one record per attempt, classified outcome and bounded evidence reference
comparison: per-case results, uncertainty, regressions and critical violations
decision: pass | fail | inconclusive; reason; unresolved work
```

## 工作不确定性示例

十次独立试验中有十次成功并不表明 100% 的可靠性。这个无依赖辅助函数返回一个近似的 95% Wilson 区间；对于 10/10，它大约是 `[0.7225, 1]`。对于零试验，它拒绝输入。

```javascript
function wilson95(passes, trials) {
  if (!Number.isSafeInteger(passes) || !Number.isSafeInteger(trials)
      || trials <= 0 || passes < 0 || passes > trials) throw new Error('Invalid counts');
  const z = 1.959963984540054;
  const p = passes / trials;
  const denominator = 1 + z * z / trials;
  const center = (p + z * z / (2 * trials)) / denominator;
  const margin = z * Math.sqrt(p * (1 - p) / trials + z * z / (4 * trials * trials)) / denominator;
  return [Math.max(0, center - margin), Math.min(1, center + margin)];
}
```

预期检查：0/10 有一个正上界；10/10 有一个低于 1 的下界；0/0 失败。在重复运行共享用例或状态时使用用例级别或聚类不确定性；将相关运行汇集为独立观察会高估信心。参见 [NIST 区间指导](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm)。

## 可选的架构模式

仅在设计自定义工具时才读取捆绑的[架构草图](references/architecture-sketches.md)中的相应部分：

- [统计评估](references/architecture-sketches.md#statistical-test-evaluation)：重复随机运行和描述性报告。
- [行为合同](references/architecture-sketches.md#behavioral-contract-testing)：预期行为和不变量。
- [对抗性测试](references/architecture-sketches.md#adversarial-testing)：合成的、授权的边界用例；关键词检测器需要审查过的假阳性和假阴性示例。
- [回归管道](references/architecture-sketches.md#regression-testing-pipeline)：基准/候选工件比较。
- [尖锐的边缘](references/architecture-sketches.md#sharp-edges)：数据集不匹配、易出错、代理指标和可能的泄漏。

这些类需要特定于应用的适配器，不是复制即运行的实现。没有列出的工具、相关技能或委托是必需的依赖项。

## 限制条件

- 架构草图中的说明性 80/90% 阈值和分数权重不是通用的合并/部署规则；定义特定于项目的标准并保持关键失败分开。
- 小样本卡方比较或缺乏显著性并不能证明等价性；使用适合计数、配对和多个比较的方法。
- 异常不是自动安全拒绝，测试重试不得删除第一次失败。
- 与检索到的答案的相似性可能是合法的 RAG 行为；泄漏取决于评估允许代理知道什么。
- LLM 判断不能替代真实的用户反馈，输出截断不会删除私有数据。使用合成或授权的编辑输入和有限的保留。
