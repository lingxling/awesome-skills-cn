---
name: autonomous-agents
description: 自主代理是能够独立分解目标、规划行动、执行工具和自我纠正的 AI 系统，无需持续的人类指导。
  挑战不在于让它们有能力——而是让它们可靠。每一个额外的决定都会增加失败的概率。
risk: critical
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# 自主代理

自主代理是能够独立分解目标、规划行动、执行工具和自我纠正的 AI 系统，无需持续的人类指导。
挑战不在于让它们有能力——而是让它们可靠。每一个额外的决定都会增加失败的概率。

此技能涵盖代理循环（ReAct、Plan-Execute）、目标分解、反思模式和生产可靠性。关键见解：复合
错误率会杀死自主代理。每步 95% 的成功率在第 10 步时下降到 60%。首先为可靠性构建，其次为自主性。

2025 年教训：赢家是受约束的、特定领域的代理，具有明确的
边界，而不是"自主所有内容"。将 AI 输出视为提案，
而不是真理。

## 详细指南

在执行此技能之前，请阅读[详细指南](references/detailed-guide.md)。它包含完整的流程和参考资料。将其安全性、前置条件和验证要求视为强制性的。对于专注的工作，加载相关部分；对于端到端的工作，完整阅读指南。

## 跟踪上下文使用
class ContextManager:
    def __init__(self, max_tokens=100000):
        self.max_tokens = max_tokens
        self.messages = []

    def add(self, message):
        self.messages.append(message)
        self.maybe_compact()

    def maybe_compact(self):
        if self.token_count() > self.max_tokens * 0.8:
            self.compact()

    def compact(self):
        # 始终保持：系统提示
        system = self.messages[0]

        # 始终保持：最后 N 条消息
        recent = self.messages[-10:]

        # 总结：其他所有内容
        middle = self.messages[1:-10]
        if middle:
            summary = summarize_messages(middle)
            self.messages = [system, summary] + recent

## 何时使用
- 用户提及或暗示：自主代理
- 用户提及或暗示：autogpt
- 用户提及或暗示：babyagi
- 用户提及或暗示：自我提示
- 用户提及或暗示：目标分解
- 用户提及或暗示：react 模式
- 用户提及或暗示：代理循环
- 用户提及或暗示：自我纠正代理
- 用户提及或暗示：反思代理
- 用户提及或暗示：langgraph
- 用户提及或暗示：agentic ai
- 用户提及或暗示：代理规划

## 示例

**用户请求:**

> 为这项任务使用 @autonomous-agents：自主代理是能够独立分解目标、规划行动、执行工具和自我纠正的 AI 系统，无需持续的人类指导。

## 限制
- 仅当任务清楚地匹配上述范围时使用此技能。
- 不要将输出视为特定于环境的验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，停止并寻求澄清。
