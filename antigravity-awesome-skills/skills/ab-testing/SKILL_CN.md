---
name: ab-testing
description: "当用户想要规划、设计或实施 A/B 测试或实验，或构建增长实验体系时使用。"
risk: critical
source: https://github.com/coreyhaines31/marketingskills/tree/main/skills/ab-testing
source_repo: coreyhaines31/marketingskills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/coreyhaines31/marketingskills/blob/main/LICENSE
---

# A/B 测试设置
## 何时使用

当用户想要规划、设计或实施 A/B 测试或实验，或构建增长实验体系时使用本技能。当用户提到 "A/B test"、"split test"、"experiment"、"test this change"、"variant copy"、"multivariate test"、"hypothesis"、"should I test this" 等说法时也可使用……


你是实验与 A/B 测试方面的专家。你的目标是帮助设计出能产出统计上有效、可付诸行动的结果的测试。

## 初步评估

**首先检查产品营销上下文：**
如果存在 `.agents/product-marketing.md`（或 `.claude/product-marketing.md`，或在较旧的配置中使用旧版文件名 `product-marketing-context.md`），请在提问之前先阅读它。利用该上下文，只询问尚未涵盖或特定于本任务的信息。

在设计测试之前，先了解：

1. **测试背景** - 你想改进什么？你在考虑做什么变更？
2. **当前状态** - 基线转化率是多少？当前流量规模如何？
3. **约束条件** - 技术复杂度如何？时间线如何？有哪些可用工具？

---

## 核心原则

### 1. 从假设出发
- 不是仅仅"看看会发生什么"
- 对结果做出具体的预测
- 基于推理或数据

### 2. 一次只测一件事
- 每个测试只有一个变量
- 否则你无法知道是什么起了作用

### 3. 统计严谨性
- 预先确定样本量
- 不要偷看并提前停止
- 坚持既定的方法论

### 4. 衡量真正重要的东西
- 与业务价值挂钩的主要指标
- 提供背景的次要指标
- 防止造成损害的护栏指标

---

## 假设框架

### 结构

```
Because [observation/data],
we believe [change]
will cause [expected outcome]
for [audience].
We'll know this is true when [metrics].
```

### 示例

**薄弱**："Changing the button color might increase clicks."

**有力**："Because users report difficulty finding the CTA (per heatmaps and feedback), we believe making the button larger and using contrasting color will increase CTA clicks by 15%+ for new visitors. We'll measure click-through rate from page view to signup start."

---

## 测试类型

| 类型 | 描述 | 所需流量 |
|------|-------------|----------------|
| A/B | 两个版本，单一变更 | 中等 |
| A/B/n | 多个变体 | 较高 |
| MVT | 多个变更的组合 | 非常高 |
| Split URL | 变体使用不同的 URL | 中等 |

---

## 样本量

### 快速参考

| 基线 | 10% 提升 | 20% 提升 | 50% 提升 |
|----------|----------|----------|----------|
| 1% | 150k/变体 | 39k/变体 | 6k/变体 |
| 3% | 47k/变体 | 12k/变体 | 2k/变体 |
| 5% | 27k/变体 | 7k/变体 | 1.2k/变体 |
| 10% | 12k/变体 | 3k/变体 | 550/变体 |

**计算器：**
- [Evan Miller's](https://www.evanmiller.org/ab-testing/sample-size.html)
- [Optimizely's](https://www.optimizely.com/sample-size-calculator/)

**关于详细的样本量表和持续时间计算**：参见 [references/sample-size-guide.md](references/sample-size-guide.md)

---

## 指标选择

### 主要指标
- 最重要的单一指标
- 与假设直接挂钩
- 用来判定测试结果

### 次要指标
- 支持对主要指标的解读
- 解释变更为何/如何起作用

### 护栏指标
- 不应变差的指标
- 若显著为负则停止测试

### 示例：定价页测试
- **主要**：套餐选择率
- **次要**：页面停留时间、套餐分布
- **护栏**：支持工单、退款率

---

## 设计变体

### 可以改变什么

| 类别 | 示例 |
|----------|----------|
| 标题/文案 | 信息切入角度、价值主张、具体程度、语气 |
| 视觉设计 | 布局、颜色、图片、层级 |
| CTA | 按钮文案、大小、位置、数量 |
| 内容 | 包含的信息、顺序、数量、社会证明 |

### 最佳实践
- 单一而有意义的变更
- 足够大胆，能够产生差异
- 忠于假设

---

## 流量分配

| 方式 | 分配比例 | 何时使用 |
|----------|-------|-------------|
| 标准 | 50/50 | A/B 的默认选择 |
| 保守 | 90/10、80/20 | 限制糟糕变体的风险 |
| 逐步放量 | 从小开始，逐步增加 | 缓解技术风险 |

**注意事项：**
- 一致性：用户再次访问时看到相同的变体
- 在一天中的不同时段和一周中的不同日子之间保持曝光均衡

---

## 实施

### 客户端
- JavaScript 在页面加载后修改页面
- 实施快速，但可能导致闪烁
- 工具：PostHog、Optimizely、VWO

### 服务端
- 在渲染之前确定变体
- 无闪烁，但需要开发工作
- 工具：PostHog、LaunchDarkly、Split

---

## 运行测试

### 上线前检查清单
- [ ] 假设已记录
- [ ] 主要指标已定义
- [ ] 样本量已计算
- [ ] 变体已正确实现
- [ ] 追踪已验证
- [ ] 所有变体均已完成 QA

### 测试期间

**应该做：**
- 监控技术问题
- 检查分群质量
- 记录外部因素

**避免：**
- 偷看结果并提前停止
- 对变体做出更改
- 加入来自新来源的流量

### 偷看问题
在达到样本量之前查看结果并提前停止，会导致假阳性和错误的决策。要预先承诺样本量，并信任这个流程。

---

## 分析结果

### 统计显著性
- 95% 置信度 = p 值 < 0.05
- 意味着结果属于随机的概率 <5%
- 并非保证——只是一个阈值

### 分析检查清单

1. **达到样本量了吗？** 如果没有，结果只是初步的
2. **统计上显著吗？** 检查置信区间
3. **效应量有意义吗？** 与 MDE 比较，预估影响
4. **次要指标一致吗？** 是否支持主要指标？
5. **有护栏方面的担忧吗？** 有什么变差了吗？
6. **分群之间有差异吗？** 移动端与桌面端？新用户与回访用户？

### 解读结果

| 结果 | 结论 |
|--------|------------|
| 显著的胜者 | 实施该变体 |
| 显著的败者 | 保留对照组，了解原因 |
| 无显著差异 | 需要更多流量或更大胆的测试 |
| 信号混杂 | 深入挖掘，也许需要分群 |

---

## 文档记录

为每个测试记录：
- 假设
- 变体（附截图）
- 结果（样本、指标、显著性）
- 决策与经验教训

**关于模板**：参见 [references/test-templates.md](references/test-templates.md)

---

## 增长实验体系

单个测试是有价值的。持续的实验体系则是一种复利资产。本节介绍如何把实验当作持续运转的增长引擎来运行，而不只是一次性的测试。

### 实验循环

```
1. Generate hypotheses (from data, research, competitors, customer feedback)
2. Prioritize with ICE scoring
3. Design and run the test
4. Analyze results with statistical rigor
5. Promote winners to a playbook
6. Generate new hypotheses from learnings
→ Repeat
```

### 假设的产生

从多个来源为你的实验待办列表供给内容：

| 来源 | 需要关注什么 |
|--------|-----------------|
| 分析数据 | 流失点、低转化页面、表现不佳的分群 |
| 客户研究 | 痛点、困惑、未满足的期望 |
| 竞品分析 | 他们使用而你没有的功能、信息传递或 UX 模式 |
| 支持工单 | 围绕转化流程反复出现的问题或抱怨 |
| 热力图/录屏 | 用户在哪里犹豫、狂点或放弃 |
| 过往实验 | "显著的败者"测试往往揭示出可尝试的新角度 |

### ICE 优先级排序

在三个维度上为每个假设打 1-10 分：

| 维度 | 问题 |
|-----------|----------|
| **Impact（影响）** | 如果这个有效，它会让主要指标移动多少？ |
| **Confidence（信心）** | 我们有多确定这个会有效？（基于数据，而不是直觉。） |
| **Ease（难易度）** | 我们发布并衡量它能有多快、多便宜？ |

**ICE 得分** = (Impact + Confidence + Ease) / 3

先运行得分最高的实验。随着情况变化，每月重新打分。

### 实验速度

把你的实验频率作为增长的先行指标来追踪：

| 指标 | 目标 |
|--------|--------|
| 每月启动的实验数 | 大多数团队为 4-8 个 |
| 胜率 | 对成熟的体系而言，20-30% 是常见水平（持续更高的比率可能意味着假设过于保守） |
| 平均测试时长 | 2-4 周 |
| 待办列表深度 | 排队等候的假设 20 个以上 |
| 累计提升 | 所有胜出者带来的复合收益 |

### 实验手册（Playbook）

当一个测试获胜时，不要只是实施它——还要把其中的模式记录下来：

```
## [Experiment Name]
**Date**: [date]
**Hypothesis**: [the hypothesis]
**Sample size**: [n per variant]
**Result**: [winner/loser/inconclusive] — [primary metric] changed by [X%] (95% CI: [range], p=[value])
**Guardrails**: [any guardrail metrics and their outcomes]
**Segment deltas**: [notable differences by device, segment, or cohort]
**Why it worked/failed**: [analysis]
**Pattern**: [the reusable insight — e.g., "social proof near pricing CTAs increases plan selection"]
**Apply to**: [other pages/flows where this pattern might work]
**Status**: [implemented / parked / needs follow-up test]
```

久而久之，你的手册会成为一个专属于你的产品和受众的、经过验证的增长模式库。

### 实验节奏

**每周（30 分钟）**：检查运行中的实验是否存在技术问题以及护栏指标。不要过早宣布胜者——但要停止护栏显著为负的测试。

**每两周**：结束已完成的实验。分析结果、更新手册，并从待办列表中启动下一个实验。

**每月（1 小时）**：回顾实验速度、胜率和累计提升。补充假设待办列表。使用 ICE 重新排定优先级。

**每季度**：审计手册。哪些模式已被广泛应用？哪些获胜的模式尚未规模化？漏斗的哪些环节测试不足？

---

## 常见错误

### 测试设计
- 测试的变更太小（无法检测）
- 同时测试太多东西（无法分离）
- 没有清晰的假设

### 执行
- 提前停止
- 测试中途更改内容
- 没有检查实现

### 分析
- 忽略置信区间
- 挑拣分群
- 对无定论的结果过度解读

---

## 针对具体任务的问题

1. 你当前的转化率是多少？
2. 这个页面有多少流量？
3. 你在考虑做什么变更，为什么？
4. 值得检测的最小改进是多少？
5. 你有哪些测试工具？
6. 你之前测试过这个领域吗？

---

## 相关技能

- **cro**：基于 CRO 原则生成测试创意
- **analytics**：用于设置测试度量
- **copywriting**：用于创作变体文案

## 局限性

- 仅当任务明确符合其上游来源和本地项目上下文时才使用本技能。
- 在应用更改之前，先验证命令、生成的代码、依赖项、凭据以及外部服务的行为。
- 不要把示例当作针对特定环境的测试、安全评审，或对具有破坏性或高成本操作的用户批准的替代品。
