---
name: acceptance-orchestrator
description: 当编码任务应该从问题接纳到实施、审查、部署和验收验证端到端驱动，且最少需要人工干预时使用。
risk: safe
source: community
date_added: "2026-03-12"
---

# 验收协调器

## 概述

将编码工作作为状态机进行协调，仅当验收标准得到证据验证或任务明确升级时结束。

核心规则：**不优化"代码已更改"；优化"DoD 已证明"。**

## 何时使用

- 任务已有问题或明确的验收标准，应该端到端运行，且最少需要人工干预。
- 你需要在实施、审查、部署和最终验证之间结构化交接。
- 你想要明确的停止条件和升级，而不是无声的部分完成。

## 必需子技能

- `create-issue-gate`
- `closed-loop-delivery`
- `verification-before-completion`

可选支持技能：

- `deploy-dev`
- `pr-watch`
- `pr-review-autopilot`
- `git-ship`

## 输入

需要这些输入：

- 问题 ID 或问题体
- 问题状态
- 验收标准（DoD）
- 目标环境（默认为 `dev`）

固定默认值：

- 最大迭代轮数 = `2`
- PR 审查轮询 = `3m -> 6m -> 10m`

## 状态机

- `intake`
- `issue-gated`
- `executing`
- `review-loop`
- `deploy-verify`
- `accepted`
- `escalated`

## 工作流程

1. **接纳**
   - 阅读问题并提取任务目标 + DoD。

2. **问题门控**
   - 使用 `create-issue-gate` 逻辑。
   - 如果问题不是 `ready` 或执行门不是 `allowed`，立即停止。
   - 在问题保持 `draft` 时不要实施任何东西。

3. **执行**
   - 移交给 `closed-loop-delivery` 以进行实施和本地验证。

4. **审查循环**
   - 如果 PR 反馈相关，将轮询窗口批处理为：
     - 等待 `3m`
     - 然后 `6m`
     - 然后 `10m`
   - 在 `10m` 轮后，停止等待并一起处理所有可见的注释。

5. **部署和运行时验证**
   - 如果 DoD 取决于运行时行为，默认仅部署到 `dev`。
   - 使用真实日志/API/Lambda 行为进行验证，而不是假设。

6. **完成门控**
   - 在声称完成前，需要 `verification-before-completion`。
   - 没有新证据就没有成功声明。

## 停止条件

仅当每个验收标准都有匹配的证据时才移至 `accepted`。

当发生以下任何情况时移至 `escalated`：

- DoD 在 `2` 个完整轮后仍然失败
- 缺失的秘密/权限/外部依赖阻止进展
- 任务需要生产操作或破坏性操作批准
- 审查指令冲突且不能同时满足

## 人工门控

始终停止进行人工确认：

- 超出同意范围的 prod/stage 部署
- 破坏性 git/数据操作
- 账单或安全态势更改
- 用户提供的缺失验收标准

## 输出契约

报告状态时，始终包括：

- `Status`：intake / executing / accepted / escalated
- `Acceptance Criteria`：通过/失败检查清单
- `Evidence`：命令、日志、API 结果或运行时证明
- `Open Risks`：仍然不确定的任何内容
- `Need Human Input`：最小的下一个决定（如果被阻止）

不要报告"完成"，除非状态是 `accepted`。

## 示例

**用户请求：**

> 让这个问题及其验收标准通过实施、验证、审查和最终的证据支持的判决。

## 限制条件

- 仅在任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并寻求澄清。
