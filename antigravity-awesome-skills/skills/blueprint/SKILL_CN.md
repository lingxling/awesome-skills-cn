---
name: blueprint
description: 将单行目标转变为任何编码代理都可以冷启动执行的分步构建计划。每个步骤都有一个自包含的上下文简介 — 在新会话中的新代理可以不读先前步骤而采取任何步骤。
category: planning
risk: critical
source: community
date_added: "2026-03-10"
---

# Blueprint — 构建计划生成器

将单行目标转变为任何编码代理都可以冷启动执行的分步计划。

## 概述

Blueprint 适用于多会话、多代理工程项目，其中每个步骤都必须由从未见过对话历史的新代理独立执行。安装一次，使用 `/blueprint <project> <objective>` 调用。

## 何时使用此技能

- 当任务需要多个 PR 或会话时使用
- 当多个代理或团队成员需要共享执行时使用
- 当您想要在执行前对计划进行对抗性审查时使用
- 当并行步骤检测和依赖关系图很重要时使用

## 工作原理

1. **研究** — 扫描代码库、读取项目内存、运行预检查
2. **设计** — 将目标分解为单个 PR 大小的步骤、识别并行性、分配模型层
3. **草稿** — 从结构化模板生成计划，其中包含分支工作流规则、CI 策略和回滚策略
4. **审查** — 委托对抗性审查给最强模型子代理（如果不可用则回退到默认模型）
5. **注册** — 保存计划并更新项目内存

## 示例

### 示例 1：数据库迁移

```
/blueprint myapp "migrate database to PostgreSQL"
```

### 示例 2：插件提取

```
/blueprint antbot "extract providers into plugins"
```

## 最佳实践

- ✅ 用于需要 3+ PR 或多个会话的任务
- ✅ 让 Blueprint 自动检测 git/gh 可用性 — 它优雅地降级
- ❌ 不要为单个 PR 可完成的任务调用
- ❌ 当用户说"只是做吧"时不要调用

## 关键区别

- **冷启动执行**：每个步骤都有一个自包含的上下文简介
- **对抗性审查门**：执行前的最强模型审查
- **Markdown 优先分发**：审查的版本主要是说明和模板，但安装或遵循它仍然可能导致代理运行命令。在检查前将存储库视为不受信任。
- **计划突变协议**：步骤可以用审计追踪分割、插入、跳过

## 安装

不要将动态分支直接克隆到活跃的技能目录中。首先要求用户批准对指定存储库的网络访问。然后检查审查的版本并在激活前单独要求：

```bash
review_dir="$(mktemp -d)"
git clone --filter=blob:none https://github.com/antbotlab/blueprint.git "$review_dir/blueprint"
git -C "$review_dir/blueprint" checkout --detach 07c5b305cf2d95d584a0d0398c390e839fec5954
git -C "$review_dir/blueprint" ls-files
git -C "$review_dir/blueprint" status --short
```

在该确切提交处阅读 `SKILL.md` 和每个捆绑文件。检查脚本、钩子、符号链接、网络调用、凭证访问和请求命令或提升权限的说明。仅在明确的用户批准后，将审查的文件复制到所选主机的技能目录中。重新审查更新的版本，而不是以静默方式更新此固定。

## 其他资源

- [GitHub 存储库](https://github.com/antbotlab/blueprint)
- [示例：小计划](https://github.com/antbotlab/blueprint/blob/main/examples/small-plan.md)
- [示例：大计划](https://github.com/antbotlab/blueprint/blob/main/examples/large-plan.md)

## 限制

- 仅在任务明确符合上述范围时使用此技能。
- 不要将输出作为特定于环境的验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并要求澄清。
- 固定的版本是可重现的，不是自动可信的；其内容仍需要审查。
