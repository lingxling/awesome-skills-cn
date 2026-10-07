---
name: accint-solve
description: 通过 acc_act(runtime="solve") 路由一个目标通过 acc 的评分内存循环；斟酌任何返回的 brain_frame 并通过 continue 提交。
risk: critical
source: https://github.com/maxbaluev/accreted-intelligence/tree/main/plugins/claude/skills/solve
source_repo: maxbaluev/accreted-intelligence
source_type: community
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/maxbaluev/accreted-intelligence/blob/main/LICENSE
---

# solve

## 何时使用

当你需要通过 acc_act(runtime="solve") 路由一个目标通过 acc 的评分内存循环；斟酌任何返回的 brain_frame 并通过 continue 提交时使用此技能。

在两个 MCP 动词上进行路由糖 — 此处没有逻辑。

1. 调用 `acc_act(runtime="solve", input="<目标>")`。
2. 如果结果是**最终的**：表面答案、`commitment` id 和引用的 `[ids]`。
3. 如果结果是一个 **brain_frame**：这是你的斟酌轮 — 框架是类型化的
   （哪个孔、检索了什么、预测了什么）。理由贯穿它，然后通过以下方式提交
   `acc_act(runtime="continue", input={"frame_id": ..., "submit_token": ..., "proposal_text": ...})`。
4. 用 `PREDICT: <0.00-1.00> <why>` 结束 `proposal_text`；acc 在所有者看到之前剥离该行，并使用它来根据后来的结果校准工作模型。
5. 绝不留下收到的框架未解决；绝不在循环外单独推导。
6. 后来通过 `acc_act(runtime="outcome", ...)` 诚实地关闭承诺。

## 示例

**用户请求：**

> 为此任务使用 @accint-solve：通过 acc_act(runtime="solve") 路由一个目标通过 acc 的评分内存循环；斟酌任何返回的 brain_frame 并通过 continue 提交。

## 限制条件

- 仅在任务明确符合其上游来源和本地项目背景时使用此技能。
- 在应用更改前验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例视为环境特定测试、安全审查或破坏性或昂贵操作用户批准的替代品。
