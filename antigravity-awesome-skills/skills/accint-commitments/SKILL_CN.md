---
name: accint-commitments
description: 分流 acc 的开放承诺并通过 acc_act(runtime="outcome") 用诚实的真实世界判决关闭它们。
risk: critical
source: https://github.com/maxbaluev/accreted-intelligence/tree/main/plugins/claude/skills/commitments
source_repo: maxbaluev/accreted-intelligence
source_type: community
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/maxbaluev/accreted-intelligence/blob/main/LICENSE
---

# commitments

## 何时使用

当你需要分流 acc 的开放承诺并通过 acc_act(runtime="outcome") 用真实世界的判决关闭它们时使用此技能。

在两个 MCP 动词上进行路由糖 — 此处没有逻辑。

1. 列出开放承诺：`acc commitments`（CLI、只读观察）。
2. 对于每个可关闭的：`acc_act(runtime="outcome", input={"ref": "<id>", "good": true|false, "note": "..."})`。
3. 来源管理：默认 `self_graded` 是一个弱先验（学分为 0.25×）。
   仅当所有者验证时传递 `owner`，仅当现实时传递 `external`/`runtime`
   （真实回复、通过的测试、世界结果）。绝不将你自己的等级标记为现实。
4. 保留真正等待的承诺 — `waiting` 是一个一流的清晰状态。

## 示例

**用户请求：**

> 分流 acc 的开放承诺并通过 acc_act(runtime="outcome") 用真实世界的判决关闭它们。

## 限制条件

- 仅在任务明确符合其上游来源和本地项目背景时使用此技能。
- 在应用更改前验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例视为环境特定测试、安全审查或破坏性或昂贵操作用户批准的替代品。
