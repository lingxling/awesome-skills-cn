---
name: agent-manager-skill
description: "通过 tmux 会话管理多个本地 CLI 代理（启动/停止/监控/分配），支持 cron 友好的调度。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 代理管理技能

## 何时使用
在以下情况下使用此技能：

- 在并行运行多个本地 CLI 代理（单独的 tmux 会话）
- 启动/停止代理并跟踪其日志
- 分配任务给代理并监控输出
- 安排重复的代理工作（cron）

## 前置条件

在您的工作区中安装 `agent-manager-skill`：

```bash
git clone https://github.com/fractalmind-ai/agent-manager-skill.git
```

## 常用命令

```bash
python3 agent-manager/scripts/main.py doctor
python3 agent-manager/scripts/main.py list
python3 agent-manager/scripts/main.py start EMP_0001
python3 agent-manager/scripts/main.py monitor EMP_0001 --follow
python3 agent-manager/scripts/main.py assign EMP_0002 <<'EOF'
Follow teams/fractalmind-ai-maintenance.md Workflow
EOF
```

## 说明

- 需要 `tmux` 和 `python3`。
- 代理在 `agents/` 目录下配置（详见仓库示例）。

## 限制条件
- 仅在任务明确与上述范围相匹配时才使用此技能。
- 不要将输出作为特定环境验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来并要求澄清。
