---
name: agent-self-scheduling
description: "使用 cron、循环或外部时钟调度 AI 代理运行，同时避免不安全的紧密自主计时器。"
category: agent-orchestration
risk: critical
source: community
source_repo: davidondrej/skills
source_type: community
date_added: "2026-07-07"
author: davidondrej
tags: [agents, scheduling, automation, cron]
tools: [claude, codex]
license: "MIT"
license_source: "https://github.com/davidondrej/skills/blob/main/LICENSE"
---

# 代理自我调度

## 何时使用

- 当用户要求定期、有计划、心跳或循环的代理工作时使用。
- 当需要在 cron、外部调度器、钩子或内置代理调度之间选择时使用。

首先问：代理是否有内置调度器（Hermes → Camp B），还是你拥有时钟（其他一切 → Camp A）？

通用底线：cron 最小为 1 分钟（5 字段表达式，无秒）—— 每个 camp。对于子分钟级别，必须使用 `while ...; sleep N; done` 循环、TS 扩展或事件钩子。永远不要让 LLM 在紧密计时器上运行。

## Camp A — 一次性代理，你拥有时钟

这些代理运行一次后退出（无状态，除非恢复）。在外部调度它们。

```bash
claude -p "PROMPT" --output-format json --allowedTools "Read,Edit,Bash"  # Claude Code
codex exec --json "PROMPT"                                                # Codex
pi run "PROMPT"                                                           # Pi
```

将其包装在时钟中：

```bash
# 1. cron (>= 1 分钟底线)
*/10 * * * * cd /path/to/project && pi run "check X and report" >> ~/agent.log 2>&1
# 2. systemd timer (Linux, survives reboot, better logging) — OnUnitActiveSec=10min
# 3. dumb loop (sub-minute, or no cron available)
while true; do pi run "check X"; sleep 30; done
```

注意事项（如果忽视每一个都会破坏无人参与的运行）：
- **权限永远挂起。** 传递 `--allowedTools`（Claude）或 sandbox/auto-approve 标志（Codex），或运行会被提示卡住。
- **使用 JSON 输出**（`--output-format json` / `--json`）以便包装器可以确定性地解析结果。
- **运行是无状态的。** 恢复（`codex exec resume --last`）或将状态持久化到下一个运行读取的文件。

Pi 根据设计没有内置调度器/循环/心跳 —— 仅外部时钟（或用于代理端计时器的 TS 扩展）。

### cmux — 仅编排，无调度器

cmux 没有计时器/监视/cron。三种方式循环它：编排器驱动（`send` → `sleep` → `read-screen` 在你自己的时钟上）、dumb while-sleep 包装器或 —— 优选 —— 通过 `cmux notify` + OSC 终端钩子的事件驱动，这比轮询更便宜且更响应。`read-screen` 是非中断的，安全轮询。

如果循环检查另一个代理，发送用户一行状态每次检查：代理在做什么，是否在轨道上。（Claude Code 可能在完成后预填一个预测的下一个用户消息 —— 那是 Claude，不是用户。）

## Camp B — Hermes 内置调度器

Hermes 的网关每 60 秒滴答一次，在新的隔离会话中运行到期的作业。首先状态检查：

```bash
hermes gateway install            # user-level ( --system to survive reboot)
hermes cron create "every 1h" "summarize new emails and report" --skill himalaya
hermes cron create "0 9 * * *" "post daily standup"      # cron 表达式
hermes cron create "30m" "one-shot reminder in 30 min"   # 一次性延迟
```

Hermes 独特：**零令牌模式**（运行脚本，逐字传递 stdout —— 用于监视程序）、**链接**（`context_from` 将一个作业的输出管道传输到下一个）、**自终止循环**和**循环安全**（计划会话无法创建更多 cron 作业 —— 不要从计划作业内部计划）。每次运行都是一个新会话：提示必须携带所有上下文。

## 心跳模式

一个快速定期滴答控制许多较慢的每任务检查：滴答读取任务列表 + 每任务 `last_run` 时间戳，仅在任务到期时采取行动。在 Hermes 中使用定期作业（当没有应该做的事时使用零令牌模式）；在 Camp A 中使用 while-sleep 循环。定义活跃时间，当没有应该做的事时保持沉默 —— 没有空洞噪音。

## 在报告成功前验证它是否触发

1. Camp A：日志文件在一个间隔后增长，或手动运行一次包装的命令 → 清洁 JSON，退出 0。
2. Camp B：`hermes cron list` 显示作业 + 合理的 `next_run`；触发立即运行以确认传递。
3. 确认权限/sandbox 标志存在 —— #1 无声故障是卡住的权限提示。
4. 心跳：确认无应做事项的滴答保持沉默。

## 限制

- 改编自 `davidondrej/skills`；在采取行动前验证本地路径、工具、凭证和代理功能。
- 对于命令、远程访问、调度、浏览器自动化或文件更改工作流，获得明确的用户批准并首先确认目标环境。
