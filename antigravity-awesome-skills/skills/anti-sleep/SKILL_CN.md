---
name: anti-sleep
description: "在长时间构建、下载或监督的自动化运行期间使用 caffeinate 保持 Mac 清醒。"
category: operations
risk: critical
source: community
source_repo: davidondrej/skills
source_type: community
date_added: "2026-07-07"
author: davidondrej
tags: [macos, caffeinate, operations]
tools: [claude, codex]
license: "MIT"
license_source: "https://github.com/davidondrej/skills/blob/main/LICENSE"
---

# 反睡眠（macOS caffeinate）

## 何时使用

- 当用户希望 Mac 在长时间监督任务期间保持清醒时使用。
- 当构建、下载或自动化运行不应被睡眠中断时使用。

使用内置 `caffeinate` 命令保持 Mac 清醒。无需安装。

## 快速开始——标准命令

```bash
caffeinate -d -i -t 7200    # 全功率：屏幕保持开启 + 无空闲睡眠，持续 2 小时
```

持续时间是 `-t <seconds>`：2h = 7200，7h = 25200，彻夜（9h）= 32400。

## 侵略性水平

| 标志 | 效果 |
|---|---|
| `-i` | 仅防止空闲**系统**睡眠（屏幕仍可能变暗/锁定） |
| `-d` | 防止**显示**睡眠（屏幕保持开启） |
| `-d -i` | **默认选择**——屏幕开启 + 系统清醒 |
| `-d -i -s` | 添加 `-s`：即使在 AC 电源语义上也防止睡眠；`-s` 仅在接入电源时有效 |
| `-u -t 1` | 模拟用户活动——立即唤醒显示器 |

除非用户另有说明，否则默认为 `-d -i -t <seconds>`。

## 绑定到进程而不是计时器

```bash
caffeinate -d -i -w <PID>          # 保持清醒直到该进程退出（非常适合构建）
caffeinate -i npm run build       # 包装命令；命令完成后退出
```

## 在可见终端中运行（cmux 窗格）

最好在用户自己的终端窗格中运行它，使其可见且易于 Ctrl+C。在 cmux 中（如果与窗格交互，请先阅读 `cmux` 技能）：

```bash
cmux send --surface surface:<N> "caffeinate -d -i -t 25200\n"
```

否则作为后台 Bash 任务运行它。永远不要用它阻止自己的前台 shell。

## 验证和监控

```bash
pgrep -fl caffeinate                       # 它在运行吗？显示确切标志
ps -o etime= -p <PID>                      # 它运行了多久
pmset -g assertions | grep -i deny        # 确认睡眠断言处于活动状态
```

**陷阱：** `caffeinate` 不打印任何内容并保持提示符——看起来"卡住"或就像未按 Enter。它没有卡住。使用 `pgrep` 验证，不要看终端。

**过期：** 使用 `-t` 时，时间用完后会静默退出——没有通知。如果用户在几小时后问"它还在开启吗？"，首先检查 `pgrep`；它可能已经过期。

## 键盘背光

`caffeinate` 无法保持键盘背光开启——它有自己的空闲计时器，在 Apple Silicon 上没有 CLI/API（研究于 2026-07）。修复很简单，一次性的：系统设置 > 键盘 > "空闲后关闭键盘背光" > 永不。

## 早期停止

```bash
pkill -f "caffeinate -d -i"    # 或在运行它的窗格中按 Ctrl+C
```

启动后：向用户确认 PID、标志和它将过期的挂钟时间。

## 限制

- 改编自 `davidondrej/skills`；在采取行动之前验证本地路径、工具、凭证和代理功能。
- 对于命令、远程访问、计划、浏览器自动化或文件更改工作流，获得明确的用户批准并首先确认目标环境。
