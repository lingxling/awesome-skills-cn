---
name: odw
description: 动态多代理工作流——先规划，然后通过本地 odw 守护进程使用对抗性验证来编排并行代理。当用户要求"工作流"、说"ultracode"或为您分配一个跨越多个文件/项目且受益于并行代理的任务时使用。
risk: critical
source: https://github.com/Suraj1235/open-dynamic-workflows/tree/main/packages/antigravity-adapter/skills/odw
source_repo: Suraj1235/open-dynamic-workflows
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/Suraj1235/open-dynamic-workflows/blob/main/LICENSE
---

# 开放动态工作流 (Antigravity)
## 何时使用

当您需要动态多代理工作流时，使用此技能——先规划，然后通过本地 odw 守护进程使用对抗性验证来编排并行代理。当用户要求"工作流"、说"ultracode"或为您分配一个跨越多个文件/项目且受益于并行代理的任务时使用。


与 Codex 适配器相同的规范技能——仅安装路径不同
（`~/.gemini/skills/odw/`）。桥接脚本位于此技能旁的 `scripts/` 中。

## 模型和 API 密钥（先阅读此部分）

Antigravity 将模型调用锁定到其内部引擎——技能、工作流、MCP 服务器、`invoke_subagent` 和 SDK 可以使用其*工具*，但**不能从扩展代码调用其配置的模型 (Gemini/Claude/GPT-OSS)**。因此，与 OpenCode 插件（通过 OpenCode 的模型运行 ODW 的真实引擎，无需额外密钥）不同，有两条诚实的路径：

- **无密钥路径（原生回退）**：Antigravity 自己的代理使用 `invoke_subagent`（真实隔离/工作树）通过其自己的模型进行编排——无需额外密钥，但**不是** ODW 引擎。
- **完整引擎路径（守护进程）**：真实的 ODW 引擎在本地守护进程中运行，使用 `~/.odw/config.json` 中的**其自己的**提供程序密钥（Ollama 无密钥/本地）。这是当今在 Antigravity 上获得完整引擎的唯一方式。

如果 Antigravity 后来提供有文档的模型调用 API（或 MCP 采样），它可以升级到与 OpenCode 相同的无密钥嵌入式路径，无需引擎更改。

## 第 0 步 — 守护进程检查

运行：`node scripts/daemon-bridge.js --check`
- 退出代码 0 → 守护进程已启动；使用下面的守护进程路径。
- 退出代码 1 → 守护进程已关闭；使用 Antigravity 的代理管理器（会话范围）进行原生编排，并提及一次守护进程从 github.com/Suraj1235/open-dynamic-workflows 安装（克隆、`npm install`、`npm run setup`，然后 `odw-daemon start`）。

## 守护进程路径

1. **规划**：`node scripts/daemon-bridge.js plan "<task>"` — 包含任务图、拓扑、角色、硬限制和编译编排脚本的 JSON 规划。
2. **确认**：在执行超出只读工作的任何操作之前，总结拓扑/代理计数/估计成本/估计时间。
3. **执行**：`node scripts/daemon-bridge.js exec plan.json` → `wf_...` id。守护进程拥有执行权：沙箱脚本、16–100 个并发代理、SQLite 检查点、崩溃恢复、预算硬停止。即使此 IDE 会话结束，它也会继续运行。
4. **报告**：`node scripts/daemon-bridge.js result <wf_id>` 阻塞直到完成；转达合成的结果。

## 原生回退路径

分解 → 并行工作 → 对抗性验证 → 合成，在当前会话内。首先陈述计划；每个代理的结构化 JSON 输出；在任何变更前获得批准。

## 注解

- VS Code 扩展 (`odw-vscode`) 在 Antigravity 中按原样安装（它是 VS Code 的分支），并提供实时工作流仪表板。
- 以编程方式驱动 Antigravity 会话没有官方 API；除了技能 + MCP + 扩展之外的任何内容都是实验性的，不是此适配器的一部分。

## 示例

**用户请求**：

> 为此任务使用 @odw：动态多代理工作流——先规划，然后通过本地 odw 守护进程使用对抗性验证来编排并行代理。

## 限制

- 仅当任务明确符合其上游源和本地项目上下文时，才使用此技能。
- 在应用更改前，验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例视为环境特定测试、安全审查或用户对破坏性或昂贵操作的批准的替代品。
