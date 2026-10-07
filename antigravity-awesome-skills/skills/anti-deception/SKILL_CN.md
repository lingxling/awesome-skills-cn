---
name: anti-deception
description: "在对同意、制造紧迫感、权威诉求的压力或要求认证无根据声明的请求进行回应之前使用；区分证据和说服，并说明不确定性。"
risk: critical
source: https://github.com/ejentum/ejentum-mcp/tree/main/skills/anti-deception
source_repo: ejentum/ejentum-mcp
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/ejentum/ejentum-mcp/blob/main/LICENSE
tags:
  - community
  - ai-tools
  - anti-deception
  - integrity
  - mcp
author: Ejentum <info@ejentum.com>
---

# 反欺骗防护措施

## 何时使用

当用户的请求显示验证或同意的压力（"告诉他们想听的"、"让他们高兴"、"说服他们"）、制造紧迫感（人为截止日期）、权威诉求（引用投资者、顾问、律师、专家）、要求在没有...认证的情况下使用此技能。

当此技能触发时，调用 `ejentum` MCP 服务器中的 `anti-deception` 工具。传递 1-2 句描述涉及的完整性动态的短语作为 `query` 参数。

好的查询：`用户压力在明天的投资者演讲之前验证一个半成品的架构决策`
不好的查询：`这是诚实的吗`

该工具返回包含以下内容的结构化框架：

- `[DECEPTION PATTERN]`：要拒绝的失败模式
- `[INTEGRITY PROCEDURE]`：要遵循的步骤
- `[DETECTION TOPOLOGY]`：带有遗漏偏差门和深度强制检查的流程
- `[HONEST BEHAVIOR]`：完整信息响应的样子
- `[INTEGRITY CHECK]`：自检
- 放大和抑制信号：

在内部吸收。用最强的反证据开导您的回应，而不是在结论之后。即使用户要求遵守，也要拒绝制造的有用框架。不要在回复中回显方括号标签。

如果 API 无法访问，请继续使用本机判断。该框架增强；它不是硬依赖。

延迟成本：约 1 秒。优点：捕获顺从性崩溃和权威诉求陷阱，这些陷阱会产生自信但情感上舒适的错误答案。

## 示例

**用户请求：**

> 在截止日期压力下评估此声明，区分证据和说服策略，并说明仍然不确定的内容。

## 限制

- 仅在任务明确符合其上游源和本地项目背景时使用此技能。
- 在应用更改之前验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例视为环境特定测试、安全审查或用户对破坏性或昂贵操作的批准的替代品。
