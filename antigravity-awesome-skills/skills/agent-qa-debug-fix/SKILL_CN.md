---
name: agent-qa-debug-fix
description: "从 MCP 证据、工件、日志和本地代码调试、修补和验证失败的 Agent QA 运行，不隐藏产品或基础设施缺陷。"
category: testing
risk: critical
source: https://github.com/vostride/agent-qa/tree/main/skills/agent-qa-debug-fix
source_repo: vostride/agent-qa
source_type: official
date_added: "2026-08-16"
author: Vostride
tags: [testing, qa, debugging, mcp, self-healing]
tools: [claude, cursor, gemini, codex]
license: FSL-1.1-ALv2
license_source: https://github.com/vostride/agent-qa/blob/main/LICENSE.md
---

# Agent QA 调试修复

## 概述

从记录的证据和相关的本地源代码修复失败的 Agent QA 运行。将分类器视为一个假设，进行最小的合理变更，并验证最狭窄的受影响行为，不仅仅为了隐藏真实缺陷而重写测试。

## 何时使用

- 失败的 Agent QA 运行已经过分类，现在需要代码或 YAML 修复。
- 工件和日志指向测试、钩子、产品、运行时或代理行为缺陷。
- 提议的修复必须用最狭窄的 Agent QA 或单元测试重新运行进行验证。
- 用户要求从证据自动修复或更新陈旧的 Agent QA 定义。

## 前置条件和批准边界

- 确认用户授权修改的存储库、工作空间、目标环境和文件。
- 在重新运行测试前检查该测试的外部副作用；对面向生产、破坏性或不可逆操作获得明确确认。
- 保留不相关的用户更改，并使修补程序限制在所证实的失败范围内。
- 不要暴露工件和日志中的凭证或敏感应用数据。

## 工作流

1. 从证据收集开始：
   - `agent_qa_get_run`
   - `agent_qa_get_run_steps`
   - `agent_qa_get_run_artifact`
   - `agent_qa_get_run_logs`
   - `agent_qa_get_run_execution_logs`
2. 调用 `agent_qa_classify_failure` 并将其类别视为假设，而不是判断。
3. 确定失败的表面：测试定义、钩子、被测试应用、运行时基础设施或代理行为。
4. 直接检查相关的本地文件。不要仅从工件推断修补程序。
5. 解释证据到变更的链接，然后应用最小的代码或 YAML 变更来解释证据。
6. 在执行前验证任何已更改的 Agent QA 定义。
7. 在批准的环境内重新运行最狭窄的受影响 Agent QA 测试、套件、钩子或单元测试。
8. 报告根本原因、已更改文件、验证命令或 MCP 操作、结果和剩余风险。

## 修复规则

- 不要从工件中发明选择器、屏幕状态、截图、日志或源文件。
- 当工件显示产品或运行时缺陷时，不要仅为了让测试通过而重写测试。
- 在编辑测试、套件、钩子或内存文件时保留规范的 Agent QA ID。
- 在重新运行编辑的 YAML 前优先使用 `agent_qa_validate_test`、`agent_qa_validate_suite` 和 `agent_qa_validate_definition`。
- 当 MCP 不可用时，使用仪表板 REST API 或本地 `.agent-qa` 工件，并说明 MCP 证据不可用。
- 当证据无法区分实质上不同的修复时停止并报告阻止因素。

## 示例

```text
用户：修复失败的暂存检出运行，但不要接触生产。

预期处理：收集失败的运行证据，分类，检查涉及的本地
定义和应用代码，仅修补所证实的原因，验证，重新运行单一
暂存测试，并报告已更改的文件加上剩余的不确定性。
```

## 限制

- 需要访问相关的运行证据和本地源代码；仅工件可能无法确定根本原因。
- 在一次成功重新运行后，无法保证间歇性浏览器、设备、网络或提供商故障已修复。
- 不授权生产变更、数据改变、依赖安装或超出用户批准范围的更广泛重构。
- 一次通过的狭窄重新运行不能替代存储库的正常测试套件或人工审查。
