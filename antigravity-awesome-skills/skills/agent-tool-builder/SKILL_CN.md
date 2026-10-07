---
name: agent-tool-builder
description: 工具是 AI 代理与世界交互的方式。一个设计良好的工具是代理有效工作与产生幻觉、
  静默失败或消耗 10 倍令牌的代理之间的区别。此技能涵盖从架构到错误处理的工具设计。
risk: critical
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Agent Tool Builder

工具是 AI 代理与世界交互的方式。一个设计良好的工具是代理有效工作与产生幻觉、静默失败或消耗 10 倍令牌的代理之间的区别。

此技能涵盖从架构到错误处理的工具设计。JSON Schema 最佳实践、真正帮助 LLM 的描述编写、验证以及正在成为 AI 工具通用语言的 MCP 新兴标准。

关键洞察：工具描述比工具实现更重要。LLM 从不看到你的代码——它仅看到架构和描述。

## 详细指南

在执行此技能前请阅读[详细指南](references/detailed-guide.md)。它保留了完整的程序和参考材料。将其安全性、前置条件和验证要求视为强制性的。对于重点工作，加载相关部分；对于端到端工作，请完整阅读指南。

## Python 示例
"""
import anthropic
from anthropic import beta_tool

client = anthropic.Anthropic()

@beta_tool
def get_weather(location: str, unit: str = "fahrenheit") -> str:
    '''Get the current weather in a given location.

    Args:
        location: The city and state, e.g. San Francisco, CA
        unit: Temperature unit, either 'celsius' or 'fahrenheit'
    '''
    # Implementation
    return json.dumps({"temperature": "72°F", "conditions": "Sunny"})

@beta_tool
def search_web(query: str) -> str:
    '''Search the web for information.

    Args:
        query: The search query
    '''
    # Implementation
    return json.dumps({"results": [...]})

# Tool runner handles the loop
runner = client.beta.messages.tool_runner(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[get_weather, search_web],
    messages=[
        {"role": "user", "content": "What's the weather in Paris?"}
    ]
)

# Process each message
for message in runner:
    print(message.content[0].text)

# Or just get final result
final = runner.until_done()
"""

## 何时使用
- 用户提及或暗示：agent tool
- 用户提及或暗示：function calling
- 用户提及或暗示：tool schema
- 用户提及或暗示：tool design
- 用户提及或暗示：mcp server
- 用户提及或暗示：mcp tool
- 用户提及或暗示：tool use
- 用户提及或暗示：build tool for agent
- 用户提及或暗示：define function
- 用户提及或暗示：input_schema
- 用户提及或暗示：tool_use
- 用户提及或暗示：tool_result

## 局限性
- 仅当任务清晰匹配上述描述的范围时才使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，停止并要求澄清。
