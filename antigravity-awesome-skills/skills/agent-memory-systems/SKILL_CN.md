---
name: agent-memory-systems
description: "内存是智能代理的基石。没有它，每次交互都从零开始。此技能涵盖了代理内存的架构：短期（上下文窗口）、长期（向量存储）和组织它们的认知架构。"
risk: safe
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# 代理内存系统

内存是智能代理的基石。没有它，每次交互都从零开始。此技能涵盖了代理内存的架构：短期（上下文窗口）、长期（向量存储）和组织它们的认知架构。

关键见解：内存不仅仅是存储 - 它是检索。存储一百万个事实如果找不到正确的事实就没有意义。分块、嵌入和检索策略决定您的代理是否记住或遗忘。

该领域存在术语不一致的碎片化。我们使用 CoALA 认知架构框架：语义内存（事实）、情节内存（经验）和程序性内存（操作方法知识）。

## 详细指南

执行此技能前请阅读[详细指南](references/detailed-guide.md)。它保留了完整的程序和参考资料。将其安全性、前置条件和验证要求视为强制性要求。对于专注性工作，请加载相关部分；对于端到端工作，请完整阅读指南。

## 何时使用
- 用户提到或暗示：agent memory
- 用户提到或暗示：long-term memory
- 用户提到或暗示：memory systems
- 用户提到或暗示：remember across sessions
- 用户提到或暗示：memory retrieval
- 用户提到或暗示：episodic memory
- 用户提到或暗示：semantic memory
- 用户提到或暗示：vector store
- 用户提到或暗示：rag
- 用户提到或暗示：langmem
- 用户提到或暗示：memgpt
- 用户提到或暗示：conversation history

## 示例

**用户请求：**

> 为此任务使用 @agent-memory-systems：内存是智能代理的基石。

## 限制条件
- 仅在任务明确与上述范围相匹配时才使用此技能。
- 不要将输出作为特定环境验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来并要求澄清。
