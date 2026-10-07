---
name: agent-orchestration-improve-agent
description: "通过性能分析、提示词工程和持续迭代,对现有智能体进行系统化改进。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 智能体性能优化工作流

通过性能分析、提示词工程和持续迭代,对现有智能体进行系统化改进。

[扩展思考:智能体优化需要一种数据驱动的方法,将性能指标、用户反馈分析和先进的提示词工程技术结合起来。成功与否取决于系统化的评估、有针对性的改进,以及具备生产安全回滚能力的严格测试。]

## 使用本技能的场景

- 改进现有智能体的性能或可靠性
- 分析失败模式、提示词质量或工具使用情况
- 运行结构化的 A/B 测试或评估套件
- 为智能体设计迭代式优化工作流

## 不使用本技能的场景

- 你正在从零开始构建一个全新的智能体
- 没有可用的指标、反馈或测试用例
- 任务与智能体性能或提示词质量无关

## 操作说明

1. 建立基线指标并收集具有代表性的样本。
2. 识别失败模式,并优先处理影响最大的修复项。
3. 以可衡量的目标应用提示词和工作流改进。
4. 通过测试进行验证,并分阶段、受控地推出变更。

## 安全性

- 避免在没有回归测试的情况下部署提示词变更。
- 如果质量或安全指标出现回退,应迅速回滚。

## 第一阶段:性能分析与基线指标

使用 context-manager 对历史数据进行收集,全面分析智能体性能。

### 1.1 收集性能数据

```
Use: context-manager
Command: analyze-agent-performance $ARGUMENTS --days 30
```

收集的指标包括:

- 任务完成率(成功任务与失败任务)
- 响应准确性与事实正确性
- 工具使用效率(工具选择是否正确、调用频率)
- 平均响应时间与 Token 消耗
- 用户满意度指标(修正次数、重试次数)
- 幻觉事件与错误模式

### 1.2 用户反馈模式分析

识别用户交互中的重复出现的模式:

- **修正模式**:用户持续修改输出结果的地方
- **澄清请求**:常见的歧义区域
- **任务放弃**:用户放弃的节点
- **追问**:响应不完整的信号
- **正面反馈**:应当保留的成功模式

### 1.3 失败模式分类

按根本原因对失败进行分类:

- **指令误解**:角色或任务混淆
- **输出格式错误**:结构或格式问题
- **上下文丢失**:长对话中的质量退化
- **工具误用**:工具选择不正确或低效
- **约束违反**:安全或业务规则被突破
- **边缘情况处理**:异常输入场景

### 1.4 基线性能报告

生成量化的基线指标:

```
Performance Baseline:
- Task Success Rate: [X%]
- Average Corrections per Task: [Y]
- Tool Call Efficiency: [Z%]
- User Satisfaction Score: [1-10]
- Average Response Latency: [Xms]
- Token Efficiency Ratio: [X:Y]
```

## 第二阶段:提示词工程改进

使用 prompt-engineer 智能体应用先进的提示词优化技术。

### 2.1 思维链增强

实现结构化的推理模式:

```
Use: prompt-engineer
Technique: chain-of-thought-optimization
```

- 添加显式的推理步骤:"让我们一步一步来解决这个问题……"
- 加入自我验证检查点:"在继续之前,先验证……"
- 为复杂任务实现递归式拆解
- 添加推理轨迹的可见性,以便调试

### 2.2 少样本示例优化

从成功的交互中整理出高质量的示例:

- **选择多样化的示例**,覆盖常见的使用场景
- **包含先前失败过的边缘情况**
- **同时展示正例和反例**并附带解释
- **按从简单到复杂的顺序**排列示例
- **在示例中标注**关键的决策点

示例结构:

```
Good Example:
Input: [User request]
Reasoning: [Step-by-step thought process]
Output: [Successful response]
Why this works: [Key success factors]

Bad Example:
Input: [Similar request]
Output: [Failed response]
Why this fails: [Specific issues]
Correct approach: [Fixed version]
```

### 2.3 角色定义优化

强化智能体的身份和能力定位:

- **核心定位**:清晰、单句的使命陈述
- **专长领域**:具体的知识领域
- **行为特质**:个性与互动风格
- **工具熟练度**:可用的工具以及何时使用它们
- **约束条件**:智能体不应做的事情
- **成功标准**:如何衡量任务完成情况

### 2.4 宪法式 AI 集成

实现自我纠正机制:

```
Constitutional Principles:
1. Verify factual accuracy before responding
2. Self-check for potential biases or harmful content
3. Validate output format matches requirements
4. Ensure response completeness
5. Maintain consistency with previous responses
```

添加"批判-修订"循环:

- 生成初始响应
- 依据原则进行自我批判
- 发现问题时自动修订
- 输出前进行最终验证

### 2.5 输出格式调优

优化响应结构:

- 针对常见任务的**结构化模板**
- 根据复杂度进行的**动态格式化**
- 详细信息的**渐进式展开**
- 为可读性进行的**Markdown 优化**
- 带语法高亮的**代码块格式化**
- 用于数据呈现的**表格和列表生成**

## 第三阶段:测试与验证

包含 A/B 对比的全面测试框架。

### 3.1 测试套件开发

创建具有代表性的测试场景:

```
Test Categories:
1. Golden path scenarios (common successful cases)
2. Previously failed tasks (regression testing)
3. Edge cases and corner scenarios
4. Stress tests (complex, multi-step tasks)
5. Adversarial inputs (potential breaking points)
6. Cross-domain tasks (combining capabilities)
```

### 3.2 A/B 测试框架

比较原始版本与改进版本的智能体:

```
Use: parallel-test-runner
Config:
  - Agent A: Original version
  - Agent B: Improved version
  - Test set: 100 representative tasks
  - Metrics: Success rate, speed, token usage
  - Evaluation: Blind human review + automated scoring
```

统计显著性检验:

- 最小样本量:每个变体 100 个任务
- 置信水平:95%(p < 0.05)
- 效应量计算(Cohen's d)
- 面向未来测试的功效分析

### 3.3 评估指标

全面的评分框架:

**任务层级指标:**

- 完成率(成功/失败二元结果)
- 正确性得分(0-100% 准确率)
- 效率得分(实际步骤数与最优步骤数的比较)
- 工具使用的恰当性
- 响应相关性与完整性

**质量指标:**

- 幻觉率(每次响应中的事实性错误)
- 一致性得分(与先前响应的一致程度)
- 格式合规性(是否符合指定结构)
- 安全得分(约束遵守情况)
- 用户满意度预测

**性能指标:**

- 响应延迟(首个 token 的耗时)
- 总生成时间
- Token 消耗(输入 + 输出)
- 每任务成本(API 使用费用)
- 内存/上下文效率

### 3.4 人工评估流程

结构化的人工审查流程:

- 盲评(评估者不知道是哪个版本)
- 带有明确标准的标准化评分规则
- 每个样本由多名评估者评估(评估者间信度)
- 收集定性反馈
- 偏好排序(A 与 B 的比较)

## 第四阶段:版本控制与部署

带有监控和回滚能力的安全上线流程。

### 4.1 版本管理

系统化的版本管理策略:

```
Version Format: agent-name-v[MAJOR].[MINOR].[PATCH]
Example: customer-support-v2.3.1

MAJOR: Significant capability changes
MINOR: Prompt improvements, new examples
PATCH: Bug fixes, minor adjustments
```

维护版本历史:

- 基于 Git 的提示词存储
- 带改进细节的变更日志
- 每个版本的性能指标
- 已记录的回滚流程

### 4.2 分阶段上线

渐进式部署策略:

1. **Alpha 测试**:内部团队验证(5% 流量)
2. **Beta 测试**:选定用户(20% 流量)
3. **Canary 发布**:逐步增加(20% → 50% → 100%)
4. **全量部署**:在满足成功标准之后
5. **监控周期**:7 天观察窗口

### 4.3 回滚流程

快速恢复机制:

```
Rollback Triggers:
- Success rate drops >10% from baseline
- Critical errors increase >5%
- User complaints spike
- Cost per task increases >20%
- Safety violations detected

Rollback Process:
1. Detect issue via monitoring
2. Alert team immediately
3. Switch to previous stable version
4. Analyze root cause
5. Fix and re-test before retry
```

### 4.4 持续监控

实时性能追踪:

- 包含关键指标的仪表盘
- 异常检测告警
- 用户反馈收集
- 自动化回归测试
- 每周性能报告

## 成功标准

智能体改进在以下情况下被视为成功:

- 任务成功率提升 ≥15%
- 用户修正次数减少 ≥25%
- 安全违规事件未增加
- 响应时间保持在基线的 10% 以内
- 每任务成本增幅不超过 5%
- 正面用户反馈有所增加

## 部署后审查

生产环境使用 30 天后:

1. 分析累积的性能数据
2. 与基线和目标进行对比
3. 识别新的改进机会
4. 记录经验教训
5. 规划下一轮优化周期

## 持续改进周期

建立常规的改进节奏:

- **每周**:监控指标并收集反馈
- **每月**:分析模式并规划改进
- **每季度**:带新能力的重大版本更新
- **每年**:战略回顾与架构更新

请记住:智能体优化是一个迭代过程。每个周期都建立在之前的经验之上,在保持稳定性和安全性的同时逐步提升性能。

## 局限性
- 仅在任务明确符合上述范围时使用本技能。
- 不要把输出当作针对特定环境的验证、测试或专家评审的替代品。
- 如果所需的输入、权限、安全边界或成功标准缺失,应停下来寻求澄清。
