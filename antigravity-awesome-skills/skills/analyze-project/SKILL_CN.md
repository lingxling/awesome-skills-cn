---
name: analyze-project
description: Antigravity 会话的取证式根因分析器。对范围变化(scope delta)、返工模式、根本原因、热点问题进行分类,并自动改进提示词/项目健康度。
risk: critical
source: community
date_added: "2026-09-04"
version: "1.0"
tags: [analysis, diagnostics, meta, root-cause, project-health, session-review]
---

# /analyze-project —— 根因分析师工作流

分析 `~/.gemini/antigravity/brain/` 中记录的 AI 辅助编码会话,并生成一份报告,不仅解释**发生了什么**,还要解释**为什么会发生**、**是谁/什么导致的**,以及**下次应该改变什么**。

## 目标

针对每个会话,确定:

1. 从最初的请求到最终执行的工作之间发生了哪些变化
2. 主要原因是:
   - 用户/需求规格问题
   - agent 问题
   - 代码仓库问题
   - 验证/测试问题
   - 合理的任务复杂度
3. 最初的提示词是否充分
4. 哪些文件/子系统反复与困难相关联
5. 哪些改动最能改善未来的会话

## 何时使用
- 你需要对 AI 辅助编码会话进行事后分析(postmortem),尤其是在出现范围漂移(scope drift)或重复返工时。
- 你想要一份能将用户/需求规格问题、agent 失误、代码仓库摩擦、验证缺口区分开的根因分析。
- 你需要有证据支持的建议,用于改进未来的提示词、代码仓库健康度或交付工作流。

## 全局规则

- 将 `.resolved.N` 计数视为**迭代信号**,而非失败的证据
- 区分**人类新增的范围**、**必要的、被发现的范围**和**agent 引入的范围**
- 区分**agent 错误**与**代码仓库摩擦**
- 每个诊断都必须包含**证据**和**置信度**
- 置信度级别:
  - **High(高)** = 有直接的产物/时间戳证据
  - **Medium(中)** = 有多个支持性信号
  - **Low(低)** = 合理的推断,但没有直接证实
- 证据优先级:
  - 产物内容 > 时间戳 > 元数据摘要 > 推断
- 如果证据薄弱,就明确说明这一点

---

## 第 0.5 步:会话意图分类

根据目标(objective)和产物,对会话的主要意图进行分类:

- `DELIVERY`(交付)
- `DEBUGGING`(调试)
- `REFACTOR`(重构)
- `RESEARCH`(研究)
- `EXPLORATION`(探索)
- `AUDIT_ANALYSIS`(审计分析)

记录:
- `session_intent`
- `session_intent_confidence`

使用意图来对严重性和返工形态进行情境化判断。
不要用同一套标准去评判探索性/研究性会话和范围狭窄的交付型会话。

---

## 第 1 步:发现对话

1. 从系统上下文中读取可用的对话摘要
2. 列出用户 Antigravity `brain/` 目录中的对话文件夹
3. 构建包含以下字段的对话索引:
   - `conversation_id`
   - `title`
   - `objective`
   - `created`
   - `last_modified`
4. 如果用户提供了关键词/路径,则筛选出匹配的对话;否则分析全部对话

输出:待分析对话的索引列表。

---

## 第 2 步:提取会话证据

对每个对话,读取(如果存在)以下内容:

### 核心产物
- `task.md`
- `implementation_plan.md`
- `walkthrough.md`

### 元数据
- `*.metadata.json`

### 版本快照
- `task.md.resolved.0 ... N`
- `implementation_plan.md.resolved.0 ... N`
- `walkthrough.md.resolved.0 ... N`

### 其他信号
- 其他 `.md` 产物
- 各产物更新的时间戳
- 计划/演示文稿中提到的文件/文件夹/子系统名称
- 验证/测试相关的措辞
- 明确的验收标准、约束条件、非目标(non-goals)和文件目标

针对每个对话记录:

#### 生命周期
- `has_task`
- `has_plan`
- `has_walkthrough`
- `is_completed`
- `is_abandoned_candidate` = 存在 task 但没有 walkthrough

#### 修订/变更量
- `task_versions`
- `plan_versions`
- `walkthrough_versions`
- `extra_artifacts`

#### 范围
- `task_items_initial`
- `task_items_final`
- `task_completed_pct`
- `scope_delta_raw`
- `scope_creep_pct_raw`

#### 时间
- `created_at`
- `completed_at`
- `duration_minutes`

#### 内容/质量
- `objective_text`
- `initial_plan_summary`
- `final_plan_summary`
- `initial_task_excerpt`
- `final_task_excerpt`
- `walkthrough_summary`
- `mentioned_files_or_subsystems`
- `validation_requirements_present`
- `acceptance_criteria_present`
- `non_goals_present`
- `scope_boundaries_present`
- `file_targets_present`
- `constraints_present`

---

## 第 3 步:提示词充分性

按 0–2 分的量表为最初的请求打分,维度包括:

- **清晰度(Clarity)**
- **边界性(Boundedness)**
- **可测试性(Testability)**
- **架构具体性(Architectural specificity)**
- **约束意识(Constraint awareness)**
- **依赖意识(Dependency awareness)**

生成:
- `prompt_sufficiency_score`
- `prompt_sufficiency_band` = High / Medium / Low

然后指出哪些缺失的提示词要素可能导致了后续的摩擦。

默认情况下不要因为提示词短而惩罚它;一个范围狭窄、明确的任务即使提示词很短,也可能充分性很高。

---

## 第 4 步:范围变化分类

将范围变化分类为:

- **人类新增的范围** —— 超出原始任务的新请求
- **必要的、被发现的范围** —— 为正确完成原始任务所必须的工作
- **agent 引入的范围** —— agent 引入的、可能并非必要的额外工作

记录:
- `scope_change_type_primary`
- `scope_change_type_secondary`(可选)
- `scope_change_confidence`
- 证据

记住一个简单的校准示例:
- 人类新增:"趁你在这里,也顺便重构一下附近的代码"
- 必要的、被发现的:隐藏的依赖必须被修复,原始任务才能正常工作
- agent 引入的:未经请求、也不必要的额外清理或重新设计

---

## 第 5 步:返工形态

将每个会话归类为以下主要模式之一:

- **干净执行(Clean execution)**
- **早期重新规划后稳定完成(Early replan then stable finish)**
- **渐进式范围扩张(Progressive scope expansion)**
- **反复重开/重关的拉锯(Reopen/reclose churn)**
- **后期验证拉锯(Late-stage verification churn)**
- **半途放弃(Abandoned mid-flight)**
- **探索性/研究性会话(Exploratory / research session)**

记录:
- `rework_shape`
- `rework_shape_confidence`
- 证据

---

## 第 6 步:根因分析

对每个非"干净执行"的会话,分配:

### 主要根因
以下之一:
- `SPEC_AMBIGUITY`(需求规格模糊)
- `HUMAN_SCOPE_CHANGE`(人为范围变更)
- `REPO_FRAGILITY`(代码仓库脆弱性)
- `AGENT_ARCHITECTURAL_ERROR`(agent 架构性错误)
- `VERIFICATION_CHURN`(验证拉锯)
- `LEGITIMATE_TASK_COMPLEXITY`(合理的任务复杂度)

### 次要根因
如果有实质相关性则可选填

### 根因判定指引
- **SPEC_AMBIGUITY**:最初的请求缺乏边界、目标、验收标准或约束条件
- **HUMAN_SCOPE_CHANGE**:因用户扩大了任务范围而导致范围扩张
- **REPO_FRAGILITY**:隐藏的耦合、脆弱的文件、不清晰的架构或环境问题导致了额外的工作
- **AGENT_ARCHITECTURAL_ERROR**:错误的文件、错误的假设、错误的方法、虚构出的结构
- **VERIFICATION_CHURN**:实现基本可行,但测试/验证环节导致了反复循环
- **LEGITIMATE_TASK_COMPLEXITY**:鉴于任务难度,修订是可预期的,且难以明显避免

每一次根因判定都必须包含:
- 证据
- 为什么排除了更有说服力的其他原因
- 置信度

---

## 第 6.5 步:会话严重性评分(0–100)

为每个会话分配一个严重性分数,用以确定关注优先级。

分量(相加,限制在 0–100 之间):
- **完成失败**: 0–25(`abandoned(放弃)= 25`)
- **重新规划强度**: 0–15
- **范围不稳定性**: 0–15
- **返工形态严重性**: 0–15
- **提示词充分性缺陷**: 0–10(`low(低)= 10`)
- **根因影响**: 0–10(`REPO_FRAGILITY` / `AGENT_ARCHITECTURAL_ERROR` 最高)
- **热点复发**: 0–10

区间:
- **0–19 低(Low)**
- **20–39 中等(Moderate)**
- **40–59 显著(Significant)**
- **60–79 高(High)**
- **80–100 严重(Critical)**

记录:
- `session_severity_score`
- `severity_band`
- `severity_drivers` = 排名前 2–4 的贡献因素
- `severity_confidence`

将严重性作为优先级排序信号,而非最终结论。始终要解释其驱动因素。
根据会话意图对严重性进行情境化处理,以免过度惩罚研究/探索性会话。

---

## 第 7 步:子系统/文件聚类

在所有对话中,按文件、文件夹或子系统对反复出现的困难进行聚类。

针对每个聚类,计算:
- 涉及该聚类的对话数量
- 平均修订次数
- 完成率
- 放弃率
- 常见根因
- 平均严重性

目标:判断摩擦主要是提示词驱动的、agent 驱动的,还是集中在特定的代码仓库区域。

---

## 第 8 步:对比群组

比较:
- 一次成功 vs 需要重新规划的会话
- 已完成 vs 已放弃
- 高提示词充分性 vs 低提示词充分性
- 范围狭窄 vs 范围高度增长
- 短会话 vs 长会话
- 低摩擦子系统 vs 高摩擦子系统

对每一组对比,找出:
- 实质性的差异是什么
- 哪些提示词特征与更顺畅的执行相关
- 哪些代码仓库特征与反复出现的困难相关

不要只是重复陈述平均值;要提取出谨慎的、有证据支持的模式。

---

## 第 9 步:非显而易见的发现

生成 3–7 条并非简单重复指标的发现。

每条发现都必须包含:
- 观察结果
- 为什么它重要
- 证据
- 置信度

强有力发现的示例:
- 重新规划多聚集在文件定位不准,而非验收标准不明确
- 范围增长往往在初步成功之后开始,暗示这是成功后的人为扩张
- 认证(auth)相关的困难更多是由代码仓库脆弱性而非 agent 幻觉导致的

---

## 第 10 步:生成报告

按以下结构创建 `session_analysis_report.md`:

# 📊 Session Analysis Report — [Project Name]

**Generated**: [timestamp]  
**Conversations Analyzed**: [N]  
**Date Range**: [earliest] → [latest]

## Executive Summary

| Metric | Value | Rating |
|:---|:---|:---|
| First-Shot Success Rate | X% | 🟢/🟡/🔴 |
| Completion Rate | X% | 🟢/🟡/🔴 |
| Avg Scope Growth | X% | 🟢/🟡/🔴 |
| Replan Rate | X% | 🟢/🟡/🔴 |
| Median Duration | Xm | — |
| Avg Session Severity | X | 🟢/🟡/🔴 |
| High-Severity Sessions | X / N | 🟢/🟡/🔴 |

阈值:
- 一次成功率(First-shot): 🟢 >70 / 🟡 40–70 / 🔴 <40
- 范围增长(Scope growth): 🟢 <15 / 🟡 15–40 / 🔴 >40
- 重新规划率(Replan rate): 🟢 <20 / 🟡 20–50 / 🔴 >50

平均严重性参考:
- 🟢 <25
- 🟡 25–50
- 🔴 >50

说明:平均严重性是一个汇总性的健康信号,与单个会话的严重性区间不是同一回事。

然后添加一段简短的叙述性总结,说明哪些方面进展良好、哪些方面正在恶化,以及主要问题是提示词质量、代码仓库脆弱性、工作流纪律,还是验证拉锯。

## Root Cause Breakdown(根因细分)

| Root Cause | Count | % | Notes |
|:---|:---|:---|:---|

## Prompt Sufficiency Analysis(提示词充分性分析)
- 高充分性提示词的常见特征
- 低充分性提示词中常见的缺失输入
- 哪些缺失的提示词要素与重新规划或放弃最相关

## Scope Change Analysis(范围变化分析)
区分:
- 人类新增的范围
- 必要的、被发现的范围
- agent 引入的范围

## Rework Shape Analysis(返工形态分析)
总结各会话中的主要失败模式。

## Friction Hotspots(摩擦热点)
展示与重新规划、放弃、验证拉锯和高严重性最相关的文件/文件夹/子系统。

## First-Shot Successes(一次成功)
列出最干净的会话,并提炼出是什么让它们成功的。

## Non-Obvious Findings(非显而易见的发现)
列出 3–7 条有证据支持的发现,并附上置信度。

## Severity Triage(严重性分级)
列出严重性最高的会话,并说明最佳干预措施是:
- 提示词改进
- 范围纪律
- 针对性的技能/工作流
- 代码仓库重构/架构清理
- 验证/测试框架改进

## Recommendations(建议)
每条建议使用:
- **Observed pattern(观察到的模式)**
- **Likely cause(可能的原因)**
- **Evidence(证据)**
- **Change to make(应做的改动)**
- **Expected benefit(预期收益)**
- **Confidence(置信度)**

## Per-Conversation Breakdown(逐对话细分)

| # | Title | Intent | Duration | Scope Δ | Plan Revs | Task Revs | Root Cause | Rework Shape | Severity | Complete? |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|

---

## 第 11 步:可选的事后分析改进

如适用,还可以:
- 更新本地的项目健康度或记忆产物(如果存在),记录反复出现的失败模式和脆弱的子系统
- 从高充分性/一次成功的会话中生成 `prompt_improvement_tips.md`
- 当同一子系统或任务序列反复导致困难时,建议缺失的技能或工作流

只有当某种模式反复出现时,才建议新增工作流/技能。

---

## 最终输出标准

该工作流必须产出:
1. 指标摘要
2. 根因诊断
3. 提示词充分性评估
4. 子系统/摩擦地图
5. 严重性分级与优先级排序
6. 有证据支持的建议
7. 非显而易见的发现

宁可明确表达不确定性,也不要制造虚假的精确感。

## 局限性
- 仅在任务明显符合上述描述的范围时使用本技能。
- 不要将输出当作替代环境特定验证、测试或专家评审的手段。
- 如果所需的输入、权限、安全边界或成功标准缺失,应停下并要求澄清。
