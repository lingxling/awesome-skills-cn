---
name: agent-qa-authoring
description: "通过 MCP 或 CLI 创建、编辑、验证和运行 Agent QA 测试、套件和钩子，同时保留规范的 ID 和模式契约。"
category: testing
risk: critical
source: https://github.com/vostride/agent-qa/tree/main/skills/agent-qa-authoring
source_repo: vostride/agent-qa
source_type: official
date_added: "2026-08-16"
author: Vostride
tags: [testing, qa, mcp, web-testing, mobile-testing]
tools: [claude, cursor, gemini, codex]
license: FSL-1.1-ALv2
license_source: https://github.com/vostride/agent-qa/blob/main/LICENSE.md
---

# Agent QA 编写

## 概述

编写 Agent QA 测试、套件和钩子，不需要发明模式字段或标识符。优先使用 Agent QA 的 MCP 工具，使用捆绑的契约参考获取确切的字段，并在保存或运行前验证每个定义。

## 何时使用

- 创建或编辑 Agent QA 测试、套件或钩子。
- 验证 Agent QA YAML 或规范 ID。
- 通过 MCP 或 CLI 运行新编写的 Agent QA 定义。
- 调查哪些 Agent QA 配置字段或工作空间模式适用。

## 前置条件和批准边界

- 仅在用户已授权的已配置 Agent QA 工作空间中工作。
- 在任何创建、更新、删除或测试运行操作前检查请求的范围。
- 在删除定义或运行可能改变外部应用状态的测试前获得明确确认。
- 将凭证保持在定义和输出之外；使用工作空间配置的秘密处理。

## 工作流

1. 使用 `agent_qa_discover` 发现本地表面。
2. 使用 `agent_qa_get_config` 检查活跃配置，特别是目标、设备、提供商和 `services.mcp`。
3. 需要确切的模式字段或 ID 契约时加载 `references/agent-qa-contracts.json`。
4. 使用 Agent QA 工具生成每个新 ID：
   - MCP：`agent_qa_generate_id`
   - CLI 回退：`agent-qa ids generate <test|suite|hook|run|observation>`
   - 如果两个表面都未安装，停止并要求用户批准
     精确的 Agent QA 安装。不要在运行时通过 `npx` 或其他
     活动包引用获取并执行包。
5. 永远不要手工编写 ID。使用 `agent_qa_validate_id` 或 `agent-qa ids validate <type> <id> --json` 验证现有 ID。
6. 在保存前验证定义：
   - 测试：`agent_qa_validate_test` 或 `agent_qa_validate_definition`（使用 `kind: "test"`）
   - 套件：`agent_qa_validate_suite` 或 `agent_qa_validate_definition`（使用 `kind: "suite"`）
   - 钩子：`agent_qa_validate_definition`（使用 `kind: "hooks"`）
7. 优先使用 MCP 编写变更：
   - 测试：`agent_qa_create_test`、`agent_qa_update_test`、`agent_qa_delete_test`
   - 套件：`agent_qa_create_suite`、`agent_qa_update_suite`、`agent_qa_delete_suite`
   - 钩子：`agent_qa_create_hook`、`agent_qa_update_hook`、`agent_qa_delete_hook`
8. 仅在 MCP 不可用时使用 CLI 或 YAML 回退。保持文件路径与 `workspace.testMatch` 或 `workspace.suiteMatch` 匹配。

## 需要的 ID 契约

- 测试 ID：`t_` 加 10 个 id-agent 单词。
- 套件 ID：`s_` 加 10 个 id-agent 单词。
- 钩子 ID：`h_` 加 10 个 id-agent 单词。
- 运行 ID：`r_` 加 10 个 id-agent 单词。
- 观察 ID：`obs_` 加 10 个 id-agent 单词。

## 运行前

- 先验证 YAML。
- 优先使用 `agent_qa_enqueue_test_run` 和 `agent_qa_enqueue_suite_run` 而不是执行 shell 命令。
- 如果使用 CLI 回退，仅在验证成功后运行。
- 当测试可能改变真实数据或触发外部操作时重新确认目标和环境。

## 示例

```text
用户：为暂存目标添加 Agent QA 检出测试并验证，但暂不运行。

预期处理：发现工作空间，检查暂存目标，生成测试 ID，
创建最小的有效定义，验证它，并在排队运行前停止。
```

## 限制

- 需要已安装和配置的 Agent QA 工作空间加上所选目标使用的任何浏览器、移动设备、模型提供商或应用依赖。
- 不推断未记录的配置键、选择器、UI 状态、凭证或测试数据。
- MCP 可用性和权限因工作空间而异；说明使用了哪个 CLI 或 YAML 回退。
- 验证证明了模式兼容性，而不是应用行为或外部环境是否安全来执行。

## 不要

- 不要发明配置键或使用旧版根配置桶。
- 不要手工编写 ID。
- 不要改变已配置工作空间模式之外的文件。
- 不要在没有用户明确范围和确认的情况下运行破坏性或面向生产的场景。
