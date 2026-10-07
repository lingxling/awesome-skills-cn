---
name: advanced-evaluation
description: 当用户要求"实现 LLM-as-judge"、"比较模型输出"、"创建评估量规"、"缓解评估偏差"，或提到直接评分、成对比较、位置偏差、评估流水线或自动化质量评估时，应使用本技能。
risk: safe
source: community
date_added: 2026-03-18
---

# 高级评估

本技能涵盖使用 LLM 作为评判者（LLM-as-judge）来评估 LLM 输出的生产级技术。它综合了学术论文、行业实践和实际落地经验，提炼为用于构建可靠评估系统的可操作模式。

**核心洞察**：LLM-as-a-Judge 不是单一技术，而是一系列方法的统称，每种方法适用于不同的评估场景。选择合适的方法并缓解已知偏差，是本技能所培养的核心能力。

## 何时使用
在以下情况下启用本技能：

- 构建 LLM 输出的自动化评估流水线
- 比较多个模型的回答以选出最佳者
- 在评估团队之间建立一致的质量标准
- 调试结果不一致的评估系统
- 为提示词或模型变更设计 A/B 测试
- 为人工或自动化评估创建量规
- 分析自动化评判与人工评判之间的相关性

## 核心概念

### 评估分类体系

评估方法分为两大类，二者的可靠性特征各不相同：

**直接评分（Direct Scoring）**：由单个 LLM 按既定量表为一个回答打分。
- 最适用于：客观标准（事实准确性、指令遵循、有害内容）
- 可靠性：对定义明确的标准而言为中到高
- 失效模式：评分校准漂移、对量表的理解不一致

**成对比较（Pairwise Comparison）**：由 LLM 比较两个回答并选出更好的一个。
- 最适用于：主观偏好（语气、风格、说服力）
- 可靠性：对于偏好类评估，高于直接评分
- 失效模式：位置偏差、长度偏差

MT-Bench 论文（Zheng et al., 2023）的研究表明，对于基于偏好的评估，成对比较与人类评判者的一致性高于直接评分，而对于具有明确标准答案的客观标准，直接评分仍然适用。

### 偏差全景

LLM 评判者表现出系统性偏差，必须主动加以缓解：

**位置偏差（Position Bias）**：在成对比较中，排在第一位的回答会得到偏袒。缓解方法：交换位置评估两次，使用多数投票或一致性检查。

**长度偏差（Length Bias）**：无论质量如何，较长的回答得分更高。缓解方法：在提示中明确要求忽略长度，采用长度归一化评分。

**自我增强偏差（Self-Enhancement Bias）**：模型会给自己的输出打更高的分。缓解方法：生成和评估使用不同的模型，或承认这一局限。

**冗长偏差（Verbosity Bias）**：详尽的解释即使并无必要也会得到更高的分数。缓解方法：使用针对具体标准的量规，对无关细节扣分。

**权威偏差（Authority Bias）**：无论是否准确，自信、权威的语气都会获得更高评价。缓解方法：要求引用证据，并增加事实核查层。

### 指标选择框架

根据评估任务的结构选择指标：

| 任务类型 | 主要指标 | 次要指标 |
|-----------|-----------------|-------------------|
| 二分类（通过/不通过） | Recall、Precision、F1 | Cohen's κ |
| 有序量表（1-5 评分） | Spearman's ρ、Kendall's τ | Cohen's κ（加权） |
| 成对偏好 | 一致率、位置一致性 | 置信度校准 |
| 多标签 | Macro-F1、Micro-F1 | 各标签的 precision/recall |

关键洞察：较高的绝对一致率不如系统性的分歧模式重要。一个在特定标准上持续与人类意见相左的评判者，比一个只带有随机噪声的评判者问题更大。

## 评估方法

### 直接评分的实现

直接评分需要三个组成部分：清晰的标准、经过校准的量表以及结构化的输出格式。

**标准定义模式**：
```
Criterion: [Name]
Description: [What this criterion measures]
Weight: [Relative importance, 0-1]
```

**量表校准**：
- 1-3 量表：带中立选项的二元量表，认知负担最低
- 1-5 量表：标准李克特量表，在粒度与可靠性之间取得良好平衡
- 1-10 量表：粒度高但更难校准，仅在有详细量规时使用

**直接评分的提示词结构**：
```
You are an expert evaluator assessing response quality.

## Task
Evaluate the following response against each criterion.

## Original Prompt
{prompt}

## Response to Evaluate
{response}

## Criteria
{for each criterion: name, description, weight}

## Instructions
For each criterion:
1. Find specific evidence in the response
2. Score according to the rubric (1-{max} scale)
3. Justify your score with evidence
4. Suggest one specific improvement

## Output Format
Respond with structured JSON containing scores, justifications, and summary.
```

**思维链要求**：所有评分提示词都必须要求先给出理由再给出分数。研究表明，与先打分的方式相比，这能将可靠性提高 15-25%。

### 成对比较的实现

对于基于偏好的评估，成对比较本身更为可靠，但需要缓解偏差。

**位置偏差缓解协议**：
1. 第一轮：回答 A 在第一位，回答 B 在第二位
2. 第二轮：回答 B 在第一位，回答 A 在第二位
3. 一致性检查：如果两轮结果不一致，则返回 TIE 并降低置信度
4. 最终裁决：结果一致的胜者，置信度取平均值

**成对比较的提示词结构**：
```
You are an expert evaluator comparing two AI responses.

## Critical Instructions
- Do NOT prefer responses because they are longer
- Do NOT prefer responses based on position (first vs second)
- Focus ONLY on quality according to the specified criteria
- Ties are acceptable when responses are genuinely equivalent

## Original Prompt
{prompt}

## Response A
{response_a}

## Response B
{response_b}

## Comparison Criteria
{criteria list}

## Instructions
1. Analyze each response independently first
2. Compare them on each criterion
3. Determine overall winner with confidence level

## Output Format
JSON with per-criterion comparison, overall winner, confidence (0-1), and reasoning.
```

**置信度校准**：置信度分数应反映位置一致性：
- 两轮结果一致：置信度 = 各次置信度的平均值
- 两轮结果不一致：置信度 = 0.5，裁决 = TIE

### 量规生成

与开放式评分相比，定义清晰的量规可将评估方差降低 40-60%。

**量规组成部分**：
1. **等级描述**：每个分数等级的清晰界限
2. **特征**：定义每个等级的可观察特征
3. **示例**：每个等级的代表性文本（可选但很有价值）
4. **边界情形**：针对模糊情形的指导
5. **评分指南**：保证一致应用的通用原则

**严格度校准**：
- **宽松**：通过分数的门槛较低，适合鼓励迭代
- **均衡**：公平、典型的预期，适用于生产环境
- **严格**：标准高，适用于安全关键或高风险的评估

**领域适配**：量规应使用领域专属术语。"代码可读性"量规会提到变量、函数和注释；"医学准确性"量规则会引用临床术语和证据标准。

## 实践指导

### 评估流水线设计

生产级评估系统需要多个层次：

```
┌─────────────────────────────────────────────────┐
│                 Evaluation Pipeline              │
├─────────────────────────────────────────────────┤
│                                                   │
│  Input: Response + Prompt + Context               │
│           │                                       │
│           ▼                                       │
│  ┌─────────────────────┐                         │
│  │   Criteria Loader   │ ◄── Rubrics, weights    │
│  └──────────┬──────────┘                         │
│             │                                     │
│             ▼                                     │
│  ┌─────────────────────┐                         │
│  │   Primary Scorer    │ ◄── Direct or Pairwise  │
│  └──────────┬──────────┘                         │
│             │                                     │
│             ▼                                     │
│  ┌─────────────────────┐                         │
│  │   Bias Mitigation   │ ◄── Position swap, etc. │
│  └──────────┬──────────┘                         │
│             │                                     │
│             ▼                                     │
│  ┌─────────────────────┐                         │
│  │ Confidence Scoring  │ ◄── Calibration         │
│  └──────────┬──────────┘                         │
│             │                                     │
│             ▼                                     │
│  Output: Scores + Justifications + Confidence     │
│                                                   │
└─────────────────────────────────────────────────┘
```

### 常见反模式

**反模式：不给理由就打分**
- 问题：分数缺乏依据，难以调试或改进
- 解决：始终要求在打分之前给出基于证据的理由

**反模式：单轮成对比较**
- 问题：位置偏差会破坏结果
- 解决：始终交换位置并检查一致性

**反模式：标准过载**
- 问题：衡量多个方面的标准不可靠
- 解决：一个标准 = 一个可衡量的方面

**反模式：缺少边界情形指导**
- 问题：评估者对模糊情形的处理不一致
- 解决：在量规中包含边界情形并给出明确指导

**反模式：忽视置信度校准**
- 问题：高置信度的错误判断比低置信度的更糟
- 解决：根据位置一致性和证据强度来校准置信度

### 决策框架：直接评分 vs. 成对比较

使用以下决策树：

```
Is there an objective ground truth?
├── Yes → Direct Scoring
│   └── Examples: factual accuracy, instruction following, format compliance
│
└── No → Is it a preference or quality judgment?
    ├── Yes → Pairwise Comparison
    │   └── Examples: tone, style, persuasiveness, creativity
    │
    └── No → Consider reference-based evaluation
        └── Examples: summarization (compare to source), translation (compare to reference)
```

### 规模化评估

对于大批量评估：

1. **LLM 评审团（Panel of LLMs，PoLL）**：使用多个模型作为评判者，汇总投票
   - 减少单个模型的偏差
   - 成本更高，但对高风险决策更可靠

2. **分层评估**：用快速廉价的模型做筛选，用昂贵的模型处理边界情形
   - 对大批量而言具有成本效益
   - 需要校准筛选阈值

3. **人在回路（Human-in-the-loop）**：对明确的情形使用自动化评估，对低置信度的情形交由人工审核
   - 对关键应用而言可靠性最佳
   - 设计反馈回路以改进自动化评估

## 示例

### 示例 1：针对准确性的直接评分

**输入**：
```
Prompt: "What causes seasons on Earth?"
Response: "Seasons are caused by Earth's tilted axis. As Earth orbits the Sun, 
different hemispheres receive more direct sunlight at different times of year."
Criterion: Factual Accuracy (weight: 1.0)
Scale: 1-5
```

**输出**：
```json
{
  "criterion": "Factual Accuracy",
  "score": 5,
  "evidence": [
    "Correctly identifies axial tilt as primary cause",
    "Correctly explains differential sunlight by hemisphere",
    "No factual errors present"
  ],
  "justification": "Response accurately explains the cause of seasons with correct 
scientific reasoning. Both the axial tilt and its effect on sunlight distribution 
are correctly described.",
  "improvement": "Could add the specific tilt angle (23.5°) for completeness."
}
```

### 示例 2：带位置交换的成对比较

**输入**：
```
Prompt: "Explain machine learning to a beginner"
Response A: [Technical explanation with jargon]
Response B: [Simple analogy-based explanation]
Criteria: ["clarity", "accessibility"]
```

**第一轮（A 在前）**：
```json
{ "winner": "B", "confidence": 0.8 }
```

**第二轮（B 在前）**：
```json
{ "winner": "A", "confidence": 0.6 }
```
（注意：胜者为 A，是因为 B 排在第一位）

**映射后的第二轮**：
```json
{ "winner": "B", "confidence": 0.6 }
```

**最终结果**：
```json
{
  "winner": "B",
  "confidence": 0.7,
  "positionConsistency": {
    "consistent": true,
    "firstPassWinner": "B",
    "secondPassWinner": "B"
  }
}
```

### 示例 3：量规生成

**输入**：
```
criterionName: "Code Readability"
criterionDescription: "How easy the code is to understand and maintain"
domain: "software engineering"
scale: "1-5"
strictness: "balanced"
```

**输出**（节选）：
```json
{
  "levels": [
    {
      "score": 1,
      "label": "Poor",
      "description": "Code is difficult to understand without significant effort",
      "characteristics": [
        "No meaningful variable or function names",
        "No comments or documentation",
        "Deeply nested or convoluted logic"
      ]
    },
    {
      "score": 3,
      "label": "Adequate",
      "description": "Code is understandable with some effort",
      "characteristics": [
        "Most variables have meaningful names",
        "Basic comments present for complex sections",
        "Logic is followable but could be cleaner"
      ]
    },
    {
      "score": 5,
      "label": "Excellent",
      "description": "Code is immediately clear and maintainable",
      "characteristics": [
        "All names are descriptive and consistent",
        "Comprehensive documentation",
        "Clean, modular structure"
      ]
    }
  ],
  "edgeCases": [
    {
      "situation": "Code is well-structured but uses domain-specific abbreviations",
      "guidance": "Score based on readability for domain experts, not general audience"
    }
  ]
}
```

## 准则

1. **始终要求在打分之前给出理由** - 思维链提示可将可靠性提高 15-25%

2. **成对比较中始终交换位置** - 单轮比较会被位置偏差破坏

3. **让量表粒度与量规的具体程度相匹配** - 没有详细的等级描述就不要使用 1-10 量表

4. **将客观标准与主观标准分开** - 客观标准用直接评分，主观标准用成对比较

5. **包含置信度分数** - 依据位置一致性和证据强度进行校准

6. **明确定义边界情形** - 模糊情形导致的评估方差最大

7. **使用领域专属量规** - 通用量规只会产生通用（价值较低）的评估

8. **对照人类判断进行验证** - 只有与人类评估相关，自动化评估才有价值

9. **监测系统性偏差** - 按标准、回答类型、模型跟踪分歧模式

10. **为迭代而设计** - 评估系统会随着反馈回路而改进

## 集成

本技能可与以下技能集成：

- **context-fundamentals** - 评估提示词需要有效的上下文结构
- **tool-design** - 评估工具需要合适的 schema 和错误处理
- **context-optimization** - 评估提示词可以针对 token 效率进行优化
- **evaluation**（基础）- 本技能扩展了基础评估概念

## 参考资料

内部参考：
- LLM-as-Judge Implementation Patterns
- Bias Mitigation Techniques
- Metric Selection Guide

外部研究：
- [Eugene Yan: Evaluating the Effectiveness of LLM-Evaluators](https://eugeneyan.com/writing/llm-evaluators/)
- [Judging LLM-as-a-Judge (Zheng et al., 2023)](https://arxiv.org/abs/2306.05685)
- [G-Eval: NLG Evaluation using GPT-4 (Liu et al., 2023)](https://arxiv.org/abs/2303.16634)
- [Large Language Models are not Fair Evaluators (Wang et al., 2023)](https://arxiv.org/abs/2305.17926)

本合集中的相关技能：
- evaluation - 基础评估概念
- context-fundamentals - 评估提示词的上下文结构
- tool-design - 构建评估工具

---

## 技能元数据

**创建时间**：2024-12-24
**最后更新**：2024-12-24
**作者**：Muratcan Koylan
**版本**：1.0.0

## 局限性
- 仅在任务明确符合上述范围时使用本技能。
- 不要将输出视为针对具体环境的验证、测试或专家评审的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来并请求澄清。
