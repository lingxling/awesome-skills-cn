---
name: aider-delegate
description: 仅在用户明确要求时,将编码任务委托给 Aider(`aider`),同时由编排者保留审查和落地的职责。
risk: critical
category: agent-orchestration
source: https://github.com/amElnagdy/delegate-skills
source_repo: amElnagdy/delegate-skills
source_type: community
date_added: '2026-08-26'
license: MIT
license_source: https://github.com/amElnagdy/delegate-skills/blob/master/LICENSE
compatibility: Requires the `aider` CLI (`python -m pip install aider-chat`), Node
  18+, and git. Aider must be able to authenticate to a model before dispatch - export
  the provider key it expects (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, …) or set it
  in Aider's own config; a local OpenAI-compatible endpoint still needs a non-empty
  `OPENAI_API_KEY`. The orchestrating agent must be able to run shell commands and
  read files. Shell examples assume bash/zsh (macOS/Linux, or Git Bash/WSL on Windows).
metadata:
  version: 0.5.0
---
# Aider Delegate

## 何时使用

- 你想把一个边界明确的编码任务委托给一个独立的 `aider` 实现者(`Aider`),然后自己审查它产生的差异(diff)。
- 用户明确要求委托给这个实现者。

你是**编排者(orchestrator)**。把一个边界明确的编码任务交给一个独立的**实现者(implementer)**——
Aider——然后审查它的产出并自行落地。你负责撰写任务说明并掌握判断权;Aider 在自己的运行中完成输入;
你负责验证并提交。

这个循环只需要一个 shell 命令和文件访问权限,因此任何类似的编排者都可以驱动它。

## 关于 Aider 需要知道的一件事

**Aider 默认会自动提交。** 它的两个默认设置会破坏本技能存在的目的——即产出一个可审查的 diff:

- `--auto-commits`(默认 `True`)——Aider 在每次交互后提交自己的编辑。
- `--dirty-commits`(默认 `True`)——Aider 在开始编辑之前,会提交**你**已有的未提交工作。

中继(relay)始终会传入 `--no-auto-commits` 和 `--no-dirty-commits`,且这两项都不可通过它进行配置。
如果你曾经手动而非通过中继驱动 `aider`,请自行传入这两个参数,否则产出的工作会变成你从未审查过的提交。
中继还会传入 `--no-gitignore`,因为否则 Aider 会在启动时把 `.aider*` 写入 `.gitignore`,
从而污染你即将读取的工作树。

## 何时不应使用此技能

- 任务规模小到可以直接处理;委托的开销不值得。
- 未安装 `aider` CLI,或没有为其配置模型。
- 你希望实现者自己管理提交。Aider 可以做到,但本技能特意关闭了这一点——diff 才是交付物。

## 前提条件(只需检查一次)

1. 安装 Aider——`python -m pip install aider-chat`,或使用 [Aider 安装文档](https://aider.chat/docs/install.html)
   中的独立安装程序。
2. 配置模型。Aider 从环境变量(`OPENAI_API_KEY`、`ANTHROPIC_API_KEY`……)或其自身的配置中读取提供商密钥;
   参见 [Aider 的模型文档](https://aider.chat/docs/llms.html)。
3. 确认 `aider --version` 能够成功运行。
4. 在目标 git 仓库中工作,或通过 `--cd` 指向它。

## 选择模型

如果省略 `--model`,Aider 会使用它自己配置的模型。传入 `--model <name>` 以选择其他模型。

## 本地和自托管模型

Aider 可以与任何 OpenAI 兼容的端点通信,因此本技能同样适用于委托给运行在用户自有硬件上的模型——
llama.cpp 的 server、Ollama、vLLM、LM Studio,或任何提供同样 API 的服务。将 `--model` 与 `--api-base`
搭配使用:

```bash
node "<skill-dir>/scripts/relay.mjs" --brief brief.txt --cd /path/to/repo \
  --model openai/<served-model-name> --api-base http://127.0.0.1:<port>/v1
```

与托管提供商相比,有三点不同:

- **必须带有 `openai/` 前缀。** 它告诉 Aider 以 OpenAI 协议与你的端点通信;前缀之后的部分是你的
  服务器报告的名称,而不是提供商目录中的名称。
- **仍然需要一个占位密钥。** 导出任意非空的 `OPENAI_API_KEY`。即使服务器忽略其值,客户端库也要求
  该请求头存在。
- **要求使用更简单的编辑格式。** 本地模型通常无法满足 Aider 默认的 `diff` 格式,该格式需要精确的
  查找/替换块。`--edit-format whole` 用更多令牌换取可靠性;请通过 `--file` 把任务说明的范围
  控制得足够小,以保持整文件重写的成本低廉。

未运行的本地端点看起来像是卡住了,而不是报错:Aider 会不断重试连接,直到中继的 `--timeout` 看门狗
触发并报告 `status: "timeout"`。在发送一份长任务说明之前,先确认服务器已启动。

### 保持离线

不涉及任何账户或提供商注册:Aider 只是一个 pip 安装包,端点是你自己的,`OPENAI_API_KEY` 只需非空
即可。中继固定了那些本来会自行触网的参数——`--no-check-update`、`--no-analytics`
(Aider 自身的默认值是 `random`,这会让一部分会话自动选择启用),以及 `--no-detect-urls`——没有
这个参数,Aider 会主动提议抓取任务说明中出现的任何 URL,而 `--yes-always` 会默默接受这个提议。

`--no-suggest-shell-commands` 关闭了剩下的那条可能未经请求就触网的路径。中继无法控制的是任务说明
本身的内容:指示 Aider 安装软件包或调用 API 的指令仍然会被执行,而 `--auto-lint` 会运行仓库自己的
工具链。这里的"离线"指的是派发路径中没有任何东西会主动外联——而不是说有沙箱在阻止它。

## 这个循环

每个任务运行以下五个步骤。第 1、4、5 步需要判断力;第 2、3 步是机械性的。

### 1. 撰写任务说明

Aider 只能看到你发送的文本,以及处于其编辑范围内的文件——没有聊天历史或共享上下文。要包含目标、
当前状态、需要改动的内容、需要保持不变的内容、项目**实际**的质量关口(gates),以及报告约定。
每份任务说明只写一个任务。参见
[references/writing-the-brief.md](references/writing-the-brief.md)。

### 2. 派发

使用随附的辅助脚本。它封装了 Aider 的无头 `--message-file` 模式,捕获运行过程,并写出
`result.json`。(`<skill-dir>` 是包含本 `SKILL.md` 的已安装目录。)

```bash
node "<skill-dir>/scripts/relay.mjs" --brief brief.txt --cd /path/to/repo
# choose a model:                        add --model <name>
# point at an OpenAI-compatible server:  add --api-base <url>
# scope the edit surface:                add --file <path> (repeatable), --read <path> for context only
# dry run, no files modified:            add --read-only
# continue the previous chat:            add --resume-last  (delta brief only)
# hard time limit (watchdog):            add --timeout 2h  (the 30m default suits short runs; implementation briefs routinely need 1-2h)
# see all options:                       node .../relay.mjs --help
```

子进程的 cwd 固定了工作区。任务说明通过 `--message-file` 传递,因此它永远不会出现在 argv 中:
它不会出现在主机进程列表里,也不受操作系统参数长度上限的限制。中继默认将产物写入系统临时目录,
且从不进行提交。参见
[references/dispatch-and-poll.md](references/dispatch-and-poll.md)。

### 3. 等待完成

辅助脚本会阻塞直到 Aider 完成。用编排者自身的后台命令机制运行它,或者在 shell 中将其放到后台
并轮询 `result.json`。运行前的用法错误以退出码 2 结束,且不写出任何结果;缺少 `aider` 时以退出码
127 结束,并写出 `status: "aider_unavailable"`。

要信任进程状态和工作树,而不是进度显示。完成意味着进程已退出且 `result.json` 已存在。Aider 的
报告是 `result.json` 中的 `finalMessage` 字段(也会在 stdout 中完整打印在报告标记之间)。

即使从未连上模型,Aider 也会以退出码 0 结束,因此中继会扫描运行记录,寻找 Aider 自身的端点和
认证错误,并在发现时报告 `status: "failed"`。如果 `failed` 状态的 `error` 提到端点,应把它当作
配置问题,而不是编码失败。

### 4. 审查——不要信任自我报告

把 Aider 最终的消息和关于质量关口的说法当作有待验证的说法:

- 自己重新运行项目的质量关口。
- 对照任务说明阅读 diff,从 `touchedFiles` 开始。
- 运行已安装的相关守护技能。
- 在删除或重命名之后,反复检查迁移脚本,并 grep 查找悬空引用。

Aider 的 `--auto-lint` 默认是开启的,所以它可能已经运行过 linter 并修复了自己的问题。那是 Aider
自己的 lint,不是你的质量关口——无论如何都要自己再运行一次。参见
[references/review-and-land.md](references/review-and-land.md)。

### 5. 落地

实现者编辑工作树;**编排者负责提交。** 只有在质量关口通过且 diff 经得起检验之后才提交。如果需要
重做,用 `--resume-last` 发送一份增量任务说明,然后再次审查。

## 自主性与权限

中继会传入 `--yes-always`——这是 Aider 自己对"自动确认所有提示"的称呼,因为无头运行无法回答
任何提示。**提前理解这意味着你在同意什么。** 自动确认适用于 Aider 原本会提出的每一个提示,而
Aider 的提示不限于文件编辑:在默认设置下,它还会提议运行自己建议的 shell 命令,而 `--yes-always`
会在没有人审阅的情况下接受这些提议。因此中继固定了 `--no-suggest-shell-commands`,以消除这条路径。

剩下的部分不是沙箱,本文档也从未假装它是。Aider 没有权限模式,也没有隔离机制:在其文件范围内,
它可以自由编辑,而 `--auto-lint`(默认开启)会运行仓库配置的任何 linter。如果任务说明指示 Aider
运行某个命令,该命令仍会被执行。委托本身就是授权;如果某次运行绝不能触碰主机,就在容器或临时工作树
(throwaway worktree)中运行它,因为本中继中没有任何参数能为你提供那种保证。

**文件选择不是安全边界。** `--file`、`--read` 和 `--subtree-only` 决定的是 Aider 把什么放入其
聊天上下文中,这是一个范围限定和令牌成本的决策。它们并不限制 Aider 实际能够触及的范围。参见
[references/writing-the-brief.md](references/writing-the-brief.md)。

`--read-only` 对应 Aider 的 `--dry-run`,它会执行运行过程但不修改文件。中继不会独立验证这一说法——
它只是报告 `git status --porcelain` 显示的内容,并在 `--read-only` 运行结束后工作树仍发生变化时
给出警告。`touchedFiles` 和 diff,而不是某个标志位,才是真正的保证。

## 恢复

Aider 没有会话 ID。它的恢复单元是它保存在仓库中的聊天历史文件(`.aider.chat.history.md`),
因此 `--resume-last` 对应 Aider 的 `--restore-chat-history`,而 `--history-file` 可以固定指向
某个特定文件。由于该历史记录存放在仓库中,恢复是按工作树(worktree)划分的,而不是按用户划分的:
同一项目的两个克隆不会共享它。

## 授权模型

委托是人类主动选择启用的事情。一旦他们这样做了("运行这个队列"、"继续"),提交经过验证、通过
质量关口的工作就是双方约定的合约。仍然保留两条限制:**呈报,而不是吞没**(报告 Aider 的设计决策、
有道理但未被要求的改动,以及非阻塞性的小问题)以及**范围变更时停下来**(如果要正确完成任务需要
超出任务说明的范围,应该询问,而不是自行扩大任务授权)。参见
[references/review-and-land.md](references/review-and-land.md)。

## 参考资料

- [references/writing-the-brief.md](references/writing-the-brief.md) - 结构、报告约定、
  真实的质量关口、文件范围,以及增量任务说明。
- [references/dispatch-and-poll.md](references/dispatch-and-poll.md) - 标志位、产物、
  `result.json`、轮询,以及故障恢复。
- [references/review-and-land.md](references/review-and-land.md) - 审查清单、提交边界,
  以及通过 Aider 聊天历史进行的重做。
- [references/multi-task-queues.md](references/multi-task-queues.md) - 顺序队列、约束条件的
  延续传递、进度跟踪,以及最终的一致性检查。


## 限制

- 仅导入文档——未包含可执行的 `scripts/relay.mjs`;完整运行时请参见上游。需要 `aider` CLI、
  Node 18+ 和 git。
- 中继从不进行提交——它只返回结构化的结果 JSON;你负责审查并落地提交。

> 改编自 [amElnagdy/delegate-skills](https://github.com/amElnagdy/delegate-skills) (MIT) —— 仅导入文档,未随附运行时代码。
