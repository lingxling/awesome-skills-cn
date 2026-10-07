---
name: claude-code-guide
description: "为配置和使用 Claude Code（Agent 编码工具）充分发挥其潜力提供综合参考。此技能综合了最佳实践、配置模板和高级使用模式。"
risk: critical
source: community
date_added: "2026-02-27"
---

# Claude Code 指南

## 目的

为配置和使用 Claude Code（Agent 编码工具）充分发挥其潜力提供综合参考。此技能综合了最佳实践、配置模板和高级使用模式。

## 配置（`CLAUDE.md`）

启动新项目时，在根目录中创建一个 `CLAUDE.md` 文件来指导 Agent。

### 模板（通用）

```markdown
# Project Guidelines

## Commands

- Run app: `npm run dev`
- Test: `npm test`
- Build: `npm run build`

## Code Style

- Use TypeScript for all new code.
- Functional components with Hooks for React.
- Tailwind CSS for styling.
- Early returns for error handling.

## Workflow

- Read `README.md` first to understand project context.
- Before editing, read the file content.
- After editing, run tests to verify.
```

## 高级功能

### 思维关键词

在你的提示中使用这些关键词来触发 Agent 的更深层推理：

- "Think step-by-step"
- "Analyze the root cause"
- "Plan before executing"
- "Verify your assumptions"

### 调试

如果 Agent 卡住或行为异常：

1. **清除上下文**：启动新会话或要求 Agent "forget previous instructions"（如果困惑）。
2. **明确的说明**：对路径、文件名和所需结果非常具体。
3. **日志**：要求 Agent "check the logs"（检查日志）或"run the command with verbose output"（使用详细输出运行命令）。

## 最佳实践

1. **小型上下文**：不要将整个代码库转储到上下文中。首先使用 `grep` 或 `find` 定位相关文件。
2. **迭代开发**：要求小的变更、验证，然后继续。
3. **反馈循环**：如果 Agent 出错，立即纠正并要求它"add a lesson"（添加经验教训）到其记忆（如果支持）或 `CLAUDE.md`。

## 参考

基于 [Claude Code Guide by zebbern](https://github.com/zebbern/claude-code-guide)。

## 何时使用
此技能适用于执行概览中描述的工作流或操作。

## 限制
- 仅当任务明确与上述范围相符时，才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并要求澄清。
