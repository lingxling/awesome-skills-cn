---
name: agent-qa-result-triage
description: "使用 MCP 证据、工件、日志、固定的失败类别、置信度和可行的后续步骤对失败的 Agent QA 运行进行分类。"
category: testing
risk: safe
source: https://github.com/vostride/agent-qa/tree/main/skills/agent-qa-result-triage
source_repo: vostride/agent-qa
source_type: official
date_added: "2026-08-16"
author: Vostride
tags: [testing, qa, triage, mcp, debugging]
tools: [claude, cursor, gemini, codex]
license: FSL-1.1-ALv2
license_source: https://github.com/vostride/agent-qa/blob/main/LICENSE.md
---

# Agent QA 结果分类

## 概述

从记录的证据而非猜测对失败的 Agent QA 运行进行分类。检查运行、步骤、工件和日志；选择一个固定类别；并返回置信度、可能的所有权和下一个证据支持的操作。

## 何时使用

- 调查失败或中断的 Agent QA 运行。
- 检查运行工件、步骤结果或执行日志。
- 比较最近的相关运行以找出重复出现的失败模式。
- 决定失败是否属于测试、产品、钩子、浏览器/移动运行时或基础设施所有者。

## 工作流

1. 从 `agent_qa_get_run` 开始获取运行状态、套件子上下文、步骤和尝试。
2. 在决定前获取证据：
   - `agent_qa_get_run_artifact`
   - `agent_qa_get_run_steps`
   - `agent_qa_get_run_logs`
   - `agent_qa_get_run_execution_logs`
3. 调用 `agent_qa_classify_failure` 并使用其类别作为默认分类，除非更强的证据与之矛盾。
4. 当分类器输出中有可用的最近相关运行时进行比较。
5. 返回简洁的分类结果：类别、置信度、证据、可能的修复区域和下一步操作。
6. 对于代码变更，在分类完成后切换到 `agent-qa-debug-fix`。

## 类别

使用 `references/triage-categories.md` 中的一个类别：

- `timeout`
- `appium_startup`
- `browser_disconnect`
- `element_not_found`
- `assertion_failure`
- `hook_failure`
- `infrastructure`
- `unknown_failure`

## 证据规则

- 引用或总结具体的工件、日志或步骤证据。
- 当工件部分缺失时提及限制置信度。
- 不要发明 MCP 未返回的截图、视频、日志或内存上下文。
- 如果 MCP 不可用，使用仪表板 REST API 或 Agent QA CLI 输出作为回退，并说明哪些证据不可用。
- 从报告中删除凭证、会话令牌、个人数据和无关的应用内容。

## 示例

```json
{
  "category": "element_not_found",
  "confidence": "high",
  "evidence": ["第 4 步无法解析描述的结账按钮"],
  "likely_fix_area": "测试定义或已更改的产品 UI",
  "next_action": "检查捕获的 UI 上下文，然后比较当前结账屏幕"
}
```

## 限制

- 分类的可靠性仅取决于保留的运行工件和日志。
- 失败类别指出最可能的失败表面；它不能证明根本原因。
- 缺失的截图、DOM/可访问性上下文、设备日志或先前的运行必须降低置信度。
- 该技能不修改测试或应用代码；使用 `agent-qa-debug-fix` 进行授权的修复。
