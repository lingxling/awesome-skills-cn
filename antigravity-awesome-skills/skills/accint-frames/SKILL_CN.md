---
name: accint-frames
description: 清空 acc 的斟酌队列 — 由无头运行检查点的开放/等待 brain_frames — 通过 acc_act(runtime="continue")。
risk: critical
source: https://github.com/maxbaluev/accreted-intelligence/tree/main/plugins/claude/skills/frames
source_repo: maxbaluev/accreted-intelligence
source_type: community
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/maxbaluev/accreted-intelligence/blob/main/LICENSE
---

# frames

## 何时使用

当你需要清空 acc 的斟酌队列 — 由无头运行检查点的开放/等待 brain_frames — 通过 acc_act(runtime="continue") 时使用此技能。

在两个 MCP 动词上进行路由糖 — 此处没有逻辑。

1. 列出队列：`acc frames`（CLI、只读观察）。
2. 对于每个开放/等待框架：阅读其类型化孔 + 检索上下文、斟酌，
   然后通过以下方式提交
   `acc_act(runtime="continue", input={"frame_id": ..., "submit_token": ..., "proposal_text": ...})`。
3. 用 `PREDICT: <0.00-1.00> <why>` 结束 `proposal_text`；acc 在所有者看到之前剥离该行，并使用它来根据后来的结果校准工作模型。
4. 相同的重复提交重放缓存的结果 — 重新提交是安全的。
5. 表面每个分辨率的 `commitment` id 和引用的 `[ids]`；在承担新工作前完全清空队列 — 检查点框架是无头运行为你保存的工作。

## 示例

**用户请求：**

> 为此任务使用 @accint-frames：清空 acc 的斟酌队列 — 由无头运行检查点的开放/等待 brain_frames — 通过 acc_act(runtime="continue")。

## 限制条件

- 仅在任务明确符合其上游来源和本地项目背景时使用此技能。
- 在应用更改前验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例视为环境特定测试、安全审查或破坏性或昂贵操作用户批准的替代品。
