---
name: cline-delegate
description: 仅在用户明确要求时将编码任务委托给 Cline CLI (`cline`)，而协调器保留审查和合并的责任。
risk: critical
category: agent-orchestration
source: https://github.com/amElnagdy/delegate-skills
source_repo: amElnagdy/delegate-skills
source_type: community
date_added: '2026-08-26'
license: MIT
license_source: https://github.com/amElnagdy/delegate-skills/blob/master/LICENSE
compatibility: 需要安装 `cline` CLI 并使用 `cline auth` 进行身份验证、Node 18+ 和 git。协调器必须能够运行
  shell 命令和读取文件。
metadata:
  version: 0.5.0
---
# Cline 委托

## 何时使用

- 您想将一个有限的编码任务委托给单独的 `cline` 实现者（`Cline`），然后自己审查其差异。
- 用户明确要求委托给此实现者。

您是**协调器**。将一个有限的编码任务委托给单独的**实现者** - Cline
编码代理 CLI - 然后审查它生成的内容并自己合并它。您编写简报并拥有
判断权；实现者在其自己的会话中在干净的工作树中进行更改；您验证
和提交。

该循环只需要 shell 命令和文件访问，因此任何可比较的协调器都可以驱动它。

## 何时不使用

- 任务足够小，可以内联完成；委托开销不值得。
- `cline` CLI 未安装或未进行身份验证。
- 您需要中继配置沙箱。Cline 公开沙箱控制，但此中继
  将它们留给 CLI 环境；当运行必须是只读时使用 `--plan`。

## 前提条件 (检查一次)

1. 安装 `cline`（npm 或捆绑二进制文件；中继探测 `cline --version`）。
2. 进行身份验证：运行 `cline auth`（交互式登录），或配置
   `ANTHROPIC_API_KEY` / OpenAI 兼容的基础 URL。
3. 确认 `cline --version` 成功。
4. 在目标 git 存储库中工作，或使用 `--cd` 指向它。

## 选择模型 (可选)

Cline 选择默认模型。要选择另一个，传递单独的 `--model <id>` 或 `--provider <name>`
(例如 `anthropic`, `openai-native`, `openrouter`)。中继只接受字母、数字
和 `. _ : / -`（该值在 Windows 上到达 shell）。

## 循环

每个任务运行这五个步骤。步骤 1、4 和 5 需要判断；2 和 3 是机械的。

### 1. 编写简报

Cline 只看到您发送的文本。它无法阅读您的对话：简报必须独立存在
目标、当前状态、要更改的内容、要保留的内容、项目的**真实**
门槛和报告合同。将每个简报保留为单一任务。将其写入文件并作为
中继的 `--brief` 传递。见 [references/writing-the-brief.md](references/writing-the-brief.md)。

### 2. 分派

使用捆绑的中继。它运行 `cline --json -v`，在固定后面的 stdin 上流式传输简报
位置指令，捕获 JSON 事件流，并写入 `result.json`。

```bash
node "<skill-dir>/scripts/relay.mjs" --brief brief.txt --cd /path/to/repo
# 选择模型 / 提供者：        添加 --model <id>  --provider <name>
# 只读计划通过：          添加 --plan   (强制 --auto-approve false)
# 拒绝需要审批的工具：     添加 --auto-approve false
# 硬时间限制 (看门狗)：        添加 --timeout 2h   (30m 默认适合简短运行；大多数实现简报应为 1-2h)
# 查看所有选项：                   node .../relay.mjs --help
```

子进程的 cwd 固定工作区。中继默认在系统临时目录下写入工件
永远不会提交。见 [references/dispatch-and-poll.md](references/dispatch-and-poll.md)。

### 3. 等待完成

中继阻塞直到 cline 完成。使用协调器的后台命令
工具运行，或在 shell 中后台运行并轮询 `result.json`。预运行使用错误退出 2
并不写入结果；缺少 `cline` 退出 127 并写入 `status: "cline_unavailable"`。

完成意味着进程已退出并 `result.json` 存在 - 信任进程状态和
工作树，而不是进度显示。Cline 的最终消息是
`result.json` 的 `finalMessage` 字段。

### 4. 审查 - 不要信任自我报告

- 自己重新运行项目的门槛。
- 针对简报阅读差异，从 `touchedFiles` 开始。
- 如果已安装，运行相关的保护技能。

见 [references/review-and-land.md](references/review-and-land.md)。

### 5. 合并

如果工作良好，提交它。中继永远不会提交 - 差异和 `result.json` 是
记录；首先运行 `git status` 和 `git diff` 以确认确切更改。如果团队有
PR 流程，进行提交并推送一个分支；进行人工审查。如果差异是错误的或
不完整，在新运行中重新分派更正的简报并再次审查。

## 自主权和权限

中继显式传递 Cline 的 `--auto-approve`，在行为模式下默认为 `true`。Cline
计划模式可以请求切换到行为模式，因此 `--plan` 强制 `--auto-approve false`；中继
拒绝 `--plan --auto-approve true`。该对是只读门槛。Cline 也通过公开沙箱
`--data-dir` / `CLINE_SANDBOX`，但中继不配置或覆盖它。对于任何风险的事情，计划优先，
然后在单独的行为模式分派前审查计划。格式错误或恶意的
简报在行为模式下仍然危险，因为命令以当前用户身份运行。

## 授权模型

委托是人们选择进行的事情。一旦进行简报，cline 作为您批准使用的工具工作。
边界是：**不要接受自我报告的结论**；验证磁盘上的一切。对于任何涉及
凭据、生产数据或不可逆操作的事情，停止并首先询问
人工，而不是将其编码在简报中。

## 参考资料

- [references/writing-the-brief.md](references/writing-the-brief.md) - 结构、范围、门槛、
  简报交付。
- [references/dispatch-and-poll.md](references/dispatch-and-poll.md) - 标志、工件、
  `result.json` 和故障恢复。
- [references/review-and-land.md](references/review-and-land.md) - 在调用
  差异完成前要验证的内容，在运行结束时。
- [references/multi-task-queues.md](references/multi-task-queues.md) - 顺序队列、
  约束前进、进度跟踪和最终一致性通过。


## 限制

- 仅文档导入 — 可执行 `scripts/relay.mjs` 未包含；有关完整运行时，请参阅上游。需要 `cline` CLI、Node 18+、git。
- 中继永远不会提交 — 它只返回结构化结果 JSON；您审查和合并提交。

> 适配自 [amElnagdy/delegate-skills](https://github.com/amElnagdy/delegate-skills) (MIT) — 仅文档，运行时未捆绑。
