---
name: agy-delegate
description: 仅在用户明确提出要求时,将编码任务委派给 Google Antigravity CLI(`agy`),同时编排者保留审查和落地(landing)的责任。
risk: critical
category: agent-orchestration
source: https://github.com/amElnagdy/delegate-skills
source_repo: amElnagdy/delegate-skills
source_type: community
date_added: '2026-08-26'
license: MIT
license_source: https://github.com/amElnagdy/delegate-skills/blob/master/LICENSE
compatibility: 需要已安装并通过身份验证的 `agy` CLI、Node.js 和 git。编排者必须能够运行 shell
  命令并读取文件。Shell 示例假定使用 bash/zsh(macOS/Linux,或 Windows 上的 Git Bash/WSL)。
metadata:
  version: 0.5.0
---
# Antigravity Delegate

## 何时使用

- 你想把一个边界明确的编码任务委派给一个独立的 `agy` 实现者(`Google Antigravity`),然后自己审查它产生的差异。
- 用户明确要求委派给这个实现者。

你是**编排者(orchestrator)**。此技能让你能把一个边界明确的编码任务交给一个独立的
**实现者(implementer)**——即 Google Antigravity CLI(`agy`)——然后审查它产生的结果并自己落地。你负责撰写任务简报并掌握判断权;Antigravity 在它自己的对话中完成具体的代码输入;你负责验证并提交。

这里没有任何内容是专属于某一个特定编排智能体的。这个循环只需要运行 shell 命令和读取文件的能力,因此任何具备类似能力的智能体都可以驱动它。它是为 Claude Code 设计并在其上运行的;请将其他编排者视为"为之设计但尚未验证"。

## 何时不应使用

- 任务规模小到足以直接内联完成——委派的开销不值得。
- 未安装或未通过身份验证的 `agy` CLI。请从 Antigravity 的 CLI 文档中安装它,并完成首次启动设置。
- 你想自己写代码,或者你只需要 Antigravity 对你写的代码给出意见(`--read-only` 的分发方式已覆盖了无需编辑的审查场景,但一次普通审查可能根本不需要委派)。

## 前提条件(只需检查一次)

1. `agy help` 执行成功。如果不成功,安装 Antigravity CLI 并完成首次启动设置。
2. `agy models` 执行成功。这证明该 CLI 能够通过身份验证并列出可用的模型标签。
3. 你当前位于目标 git 仓库中(或将用 `--cd` 指向它)。

这些检查并不能证明一次无头(headless)写操作会被批准。在 `--print` 模式下,Antigravity
无法弹出写权限提示,可能会自动拒绝该请求。中转程序(relay)会检测到这种拒绝,而不是直接报告任务完成。

## 选择实现者模型

`agy` 有一个配置好的默认模型,因此 `--model` 是可选的。当用户对该任务有偏好的 Antigravity
模型标签时使用它。否则就让 Antigravity 使用它自己当前的默认模型,而不要去猜测。

## 这个循环

每个任务执行以下五个步骤。第 1、4、5 步靠你的判断;第 2、3 步是机械性的。

### 1. 撰写任务简报

Antigravity 只能看到你发送的文本,以及它能在工作区中检查到的内容——没有聊天历史,没有
共享上下文。任务所需的一切都必须写进简报中:目标、当前状态、要改什么、要保持不动的部分、
该项目**真实可用**的关卡命令,以及一份报告合约。告诉 Antigravity 它**不会**进行提交(由你来提交)。
每份简报只包含一个任务。完整指导和模板见:
[references/writing-the-brief.md](references/writing-the-brief.md)。

### 2. 分发

使用随附的辅助工具将简报发送给 Antigravity。它包装了 `agy --print`,捕获运行过程,并
写出一份结构化的 `result.json`——因此你唯一的工作就是"运行一条命令,读取一个文件"。(下文中的
`<skill-dir>` 是此技能的安装目录——即包含此 `SKILL.md` 的那个文件夹。)

```bash
node "<skill-dir>/scripts/relay.mjs" --brief brief.txt --cd /path/to/repo
# 选择一个模型标签:                     添加 --model "<来自 agy models 的标签>"
# 推理强度(low、medium、high):      添加 --effort high
# 只读模式(plan 模式 —— 不做编辑):   添加 --read-only
# 启用 Antigravity 终端沙箱:          添加 --sandbox
# 恢复最近的那次对话:                 添加 --resume-last (仅用于增量简报)
# 查看全部选项:                       node .../relay.mjs --help
```

该辅助工具默认会启动一个全新的 Antigravity 项目,并传入 `--add-dir <repo>`(即 `--cd`
的路径,绝对路径),从而让 `agy` 拥有一个明确的工作区。它**不会**默认传入 `--dangerously-skip-permissions`。
相关机制、参数以及 `result.json` 的结构详见:[references/dispatch-and-poll.md](references/dispatch-and-poll.md)。

### 3. 等待完成

该辅助工具会阻塞直到 Antigravity 完成,因此请用你的编排者所提供的任何机制来支撑这一等待,
并在它返回后继续:

- **Claude Code:** 以 `run_in_background: true` 运行该 Bash 调用;完成时你会收到通知。
- **纯 shell / 其他智能体:** 对于短任务直接在前台运行,或将其放到后台并轮询结果文件。

不要盲信进度跟踪器而不去核实现实:一次运行完成的标志是 `result.json` 已被写出且进程已退出。
要去读取工作区的实际内容,而不是一行状态文字。实现者的完整报告位于 `result.json` 中的
`finalMessage` 字段(也会在标准输出的报告标记之间完整打印出来)。

### 4. 审查 —— 不要盲信自我报告

Antigravity 的 `result.json` 包含它自己的最终消息以及任何关卡声称。**要重新验证,而不是直接接受:**

- **自己重新运行该项目的关卡**(第 1 步中的测试/lint/构建命令)。
- **将差异与简报对照阅读:** Antigravity 是否做到了被要求的事情,不多也不少?
  结果中的 `touchedFiles` 是你的起点。
- 如果你安装了相关的 guard 技能,在这份差异上**运行相关的 guard 技能**。
- 对于 schema/迁移变更,进行一次往返验证;对于删除操作,检索是否存在悬空引用。

完整检查清单见:[references/review-and-land.md](references/review-and-land.md)。

### 5. 落地

实现者编辑工作区;**编排者提交。** 只有在关卡通过且差异经得起检验之后:

- 由你自己提交经过验证的工作成果,并附上清晰的提交信息。
- 如果需要修改,附带 `--resume-last` 发送一份增量简报,再次审查。

## 权限模型

Antigravity 拥有自己的权限策略。中转程序默认不会绕过它。只有在人类明确接受
"Antigravity 可以自动批准工具权限请求"的情况下,才使用 `--dangerously-skip-permissions`。
`--read-only` 以 plan 模式(`--mode plan`)运行 `agy`,去除了写入和编辑路径,与
`--dangerously-skip-permissions` 互斥。当你想为此次运行启用 Antigravity 的终端沙箱时,使用
`--sandbox`。Antigravity 自身的帮助文档说明,`--dangerously-skip-permissions` 会自动批准
所有工具权限请求而不进行提示,包括在沙箱之外行动的请求。当两个标志组合使用时,不要将
`--sandbox` 视为一个强制执行的边界;应将该次运行视为完全访问。如果无头的 `--print`
模式自动拒绝了一次写操作,中转程序会报告 `status: "failed"` 并以非零状态码退出。
中转程序会在一次 `--read-only` 运行前后对工作区进行指纹对比,以在 `result.json` 中报告
`readOnlyViolation`。本文档没有把 Settings 允许规则作为修复方案记录下来,因为尚未证实
它们适用于这条无头路径。不要在没有明确人工批准的情况下添加绕过标志。

## 授权模型

委派是人类主动选择启用的。一旦他们启用了它("运行这个队列"、"继续"),提交经过验证、
通过关卡的工作成果就是双方达成的约定。这项授权有两个限制:**暴露,而不是吸收**
(应上报 Antigravity 的设计决策、虽未被要求但说得过去的转向,以及非阻塞性的小毛病,而不是
悄悄地自行承担下来)和**范围变化时应停下来**(如果要正确完成任务需要超出简报的范围,
应该询问——不要自行扩大授权范围)。完整的处理方式见
[references/review-and-land.md](references/review-and-land.md)。

## 参考资料

- [references/writing-the-brief.md](references/writing-the-brief.md) - 如何写一份
  Antigravity 可以盲执行的简报:结构、XML 代码块、报告合约,以及真实的关卡命令。
- [references/dispatch-and-poll.md](references/dispatch-and-poll.md) - `relay.mjs` 的参数、
  `result.json` 合约、针对不同编排者的后台化方式,以及运行异常时的恢复手段。
- [references/review-and-land.md](references/review-and-land.md) - 审查清单、提交边界,
  以及通过 `--resume-last` 进行的返工循环。
- [references/multi-task-queues.md](references/multi-task-queues.md) - 运行一个顺序队列:
  延续约束条件、进度追踪,以及运行结束时的一致性检查。


## 局限性

- 仅限文档引入 —— 未包含可执行的 `scripts/relay.mjs`;完整运行时请参见上游仓库。需要 `agy` CLI、Node 18+、git。
- 中转程序绝不提交 —— 它只返回结构化的结果 JSON;你负责审查并落地提交。

> 改编自 [amElnagdy/delegate-skills](https://github.com/amElnagdy/delegate-skills)(MIT 许可)—— 仅文档引入,未包含运行时。
