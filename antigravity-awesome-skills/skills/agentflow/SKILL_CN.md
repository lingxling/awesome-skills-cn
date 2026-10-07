---
name: agentflow
description: "通过你的 Kanban 看板(Asana、GitHub Projects、Linear)编排自主式 AI 开发流水线。管理多 Worker 的 Claude Code 分发、确定性质量关卡、对抗式审查、按任务的成本追踪,以及抗崩溃的流水线执行。"
risk: safe
source: community
date_added: "2026-04-02"
---

# AgentFlow

## 概述

AgentFlow 把你现有的 Kanban 看板变成一个完全自主的 AI 开发流水线。它不构建自定义的编排基础设施,而是将你的项目管理工具(Asana、GitHub Projects、Linear)视作一个分布式状态机——任务在各阶段之间流转,AI 智能体通过评论读写状态,人类则通过他们本来就在用的同一个界面进行干预。

最终结果是:在手机上就能获得完整的流水线可观测性,免费的崩溃恢复能力(状态存放在你的项目管理工具中,而不是内存中),以及随时可以通过拖动卡片实现的人工干预。

## 何时使用此技能

- 需要在完整的开发生命周期(构建、审查、测试、集成)中编排多个 Claude Code Worker 时
- 希望在 AI 审查 AI 生成代码之前先设置确定性质量关卡(tsc/eslint/tests)时
- 希望从 Kanban 看板或手机获得完整的流水线可见性时
- 运行需要带成本追踪的自主任务分发的单人或团队项目时
- 需要能在会话重启后存活的抗崩溃编排时

## 核心概念

### 7 阶段 Kanban 流水线

任务流经:Backlog(待办)、Research(调研)、Build(构建)、Review(审查)、Test(测试)、Integrate(集成)、Done(完成)。每个阶段都有特定的关卡。Kanban 看板本身就是编排层——没有单独的数据库,没有消息队列,没有自定义基础设施。

### 无状态编排器

一个由 crontab 驱动的一次性扫描每 15 分钟运行一次。没有守护进程,不依赖会话。如果它崩溃了,下一次扫描会从中断处继续,因为所有状态都存放在你的项目管理工具中。

### 确定性优先于概率性

硬性关卡(tsc + eslint + tests)在任何 AI 审查之前运行,以近乎零成本捕获大约 60% 的问题。AI 审查在之后作为第二层出现。

### 对抗式审查

一个不同的 AI 智能体负责审查代码,必须先列出 3 处问题才能决定是否通过。这能防止"橡皮图章式"的敷衍批准。

### 传递优先级分发

能解锁最多下游工作的任务会自动被优先构建,自动计算关键路径。

## 技能 / 命令

### `/spec-to-board`
将一份 SPEC.md 拆解为 Kanban 看板上的原子任务,并映射好依赖关系。

### `/sdlc-orchestrate`
根据传递优先级和冲突检测向 Worker 分发任务。作为 crontab 扫描运行。

### `/sdlc-worker --slot <N>`
在一个终端槽位中运行一个 Worker,负责领取任务、构建代码并创建 PR。可并行运行 3-4 个 Worker。

### `/sdlc-health`
实时流水线状态仪表盘,展示每个任务的当前阶段、分配的智能体、重试次数和累计成本。

### `/sdlc-stop`
优雅关闭:活跃的 Worker 完成当前任务后停止,未开始的任务返回 Backlog。

## 分步指南

### 1. 编写你的 Spec

为你的项目创建一份 `SPEC.md`,描述你想构建的内容。

### 2. 拆解为任务

```
claude -p "/spec-to-board"
```

这会读取你的 SPEC.md,将其拆解为原子任务,映射依赖关系,并在你的 Kanban 看板上创建它们。

### 3. 启动 Worker

打开 3-4 个终端窗口,每个作为一个 Worker 槽位:

```bash
# 终端 2 —— Builder
claude -p "/sdlc-worker --slot T2"

# 终端 3 —— Builder
claude -p "/sdlc-worker --slot T3"

# 终端 4 —— Reviewer
claude -p "/sdlc-worker --slot T4"

# 终端 5 —— Tester
claude -p "/sdlc-worker --slot T5"
```

### 4. 启动编排器

```bash
# 添加到 crontab(每 15 分钟运行一次)
crontab -e
# 添加: */15 * * * * ~/.claude/sdlc/agentflow-cron.sh >> /tmp/agentflow-orchestrate.log 2>&1
```

### 5. 监控与干预

在手机上打开你的 Kanban 看板。观察任务在流水线中流转。将任意卡片拖动到"Needs Human"(需要人工)即可干预。运行 `/sdlc-health` 查看终端仪表盘。

### 6. 停止流水线

```
claude -p "/sdlc-stop"
```

## 质量关卡

每个阶段在晋级前都会强制执行特定关卡:

- **Build 到 Review**:`tsc` + `eslint` + `npm test` 必须全部通过(确定性)
- **Review 到 Test**:对抗式审查者在通过之前必须列出 3 个问题
- **Test 到 Integrate**:新文件覆盖率阈值须达 80%
- **Integrate 到 Done**:合并后在 main 上运行完整测试套件;失败时自动回退

## 成本追踪

按任务进行成本追踪,并设有阶段上限(以 Sonnet 为默认):

- Research:约 $0.10
- Build:约 $0.40
- Review:约 $0.10
- Test:约 $0.05
- Integrate:约 $0.03

自动护栏:达到 $3/$8 时发出警告,达到 $10/$20(Sonnet/Opus)时强制停止并上报人工处理。

## 安全与恢复

- **自动回退**:集成失败会触发 `git revert`(产生新提交,绝不强制推送)
- **被阻塞的任务**:两次尝试失败后,任务会上报给人工审查
- **僵死智能体检测**:每 5 分钟发送一次心跳,超时 10 分钟后重新分配
- **优雅关闭**:`/sdlc-stop` 会清空 Worker 队列,将未开始的任务返回 Backlog
- **范围蔓延检测**:将 PR 的变更文件与预测的文件列表进行对比
- **规格漂移检测**:通过 SHA-256 哈希比较,捕获冲刺过程中发生的需求变更

## 安装

```bash
# 克隆仓库
git clone https://github.com/UrRhb/agentflow.git

# 将技能和提示词复制到你的 Claude Code 配置中
cp -r agentflow/skills/* ~/.claude/skills/
cp -r agentflow/prompts/* ~/.claude/sdlc/prompts/
cp agentflow/conventions.md ~/.claude/sdlc/conventions.md
```

或作为 Claude Code 插件安装:

```bash
/plugin marketplace add UrRhb/agentflow
/plugin install agentflow
```

## 最佳实践

- 推荐:在运行 `/spec-to-board` 之前先写一份清晰的 SPEC.md
- 推荐:典型项目从 3-4 个 Worker 开始
- 推荐:从 Kanban 看板进行监控,需要时将卡片拖动到"Needs Human"
- 推荐:定期查看 LEARNINGS.md——它记录了常见的失败模式
- 不推荐:跳过确定性质量关卡——它们能以低成本捕获大多数问题
- 不推荐:强制推送到 main——AgentFlow 为安全起见使用 `git revert`
- 不推荐:运行超出项目并行能力支持的 Worker 数量

## 故障排查

### 问题:Worker 看起来卡住或已失效
**症状:** 任务卡片 15 分钟以上没有移动,也没有新评论
**解决方案:** 编排器会通过心跳检测失效的智能体,并在 10 分钟后重新分配。如果问题持续存在,运行 `/sdlc-health` 检查状态,并手动将卡片拖回 Backlog。

### 问题:触发了成本护栏
**症状:** 任务被移动到带有 COST:CRITICAL 标签的 "Needs Human"
**解决方案:** 查看该任务的评论线程以了解累积的上下文。决定是增加预算、简化任务,还是将其拆分为更小的部分。

### 问题:合并后集成测试失败
**症状:** 任务从 main 自动回退
**解决方案:** 自动回退保障了 main 的稳定性。查看任务评论中的重试上下文,其中记录了已经尝试过什么以及失败原因。下一个被分配的 Worker 会使用这个上下文。

## 相关技能

- `@brainstorming` - 在使用 AgentFlow 之前用于设计你的 SPEC.md
- `@writing-plans` - 与编写规格说明相辅相成,用于任务拆解
- `@test-driven-development` - 能与 AgentFlow 的质量关卡很好地配合
- `@subagent-driven-development` - 多智能体协调的替代方案

## 附加资源

- [AgentFlow 仓库](https://github.com/UrRhb/agentflow)
- [架构文档](https://github.com/UrRhb/agentflow/blob/main/docs/architecture.md)
- [差距登记册(45 种失败模式)](https://github.com/UrRhb/agentflow/blob/main/docs/gap-registry.md)
- [入门指南](https://github.com/UrRhb/agentflow/blob/main/docs/getting-started.md)

## 局限性
- 仅在任务明确符合上述范围时使用此技能。
- 不要将输出当作特定环境验证、测试或专家审查的替代品。
- 如果所需的输入、权限、安全边界或成功标准缺失,应停下来并请求澄清。
