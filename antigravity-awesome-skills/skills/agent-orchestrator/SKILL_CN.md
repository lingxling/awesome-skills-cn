---
name: agent-orchestrator
description: 用于编排整个生态系统中所有智能体的元技能。自动扫描技能、按能力进行匹配、协调多技能工作流并管理注册表。
risk: safe
source: community
date_added: '2026-03-06'
author: renat
tags:
- orchestration
- multi-agent
- workflow
- automation
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# Agent Orchestrator(智能体编排器)

## 概述

用于编排整个生态系统中所有智能体的元技能。自动扫描技能、按能力进行匹配、协调多技能工作流并管理注册表。

## 何时使用本技能

- 当你需要针对该领域的专业协助时

## 不应使用本技能的情形

- 任务与智能体编排器无关
- 有更简单、更具体的工具可以处理该请求
- 用户需要的是不涉及领域专长的通用协助

## 工作原理

本元技能作为整个技能生态系统的中央决策与协调层。它会自动扫描、
识别相关的智能体,并为复杂任务编排多个技能协同工作。

## 原则:零人工干预

- 在处理任何请求之前**始终先进行扫描**
- 只要在任意子文件夹中创建了 SKILL.md,新技能就会被**自动检测并纳入**
- 被移除的技能会从注册表中**自动排除**
- 注册新技能不需要任何手动命令

---

## 必经工作流(每个请求都要执行)

在处理用户的任何请求**之前**,执行以下步骤。
脚本会自动使用相对路径——无论在哪个目录下都能正常工作。

## 第一步:自动发现(扫描)

```bash
python agent-orchestrator/scripts/scan_registry.py
```

借助 MD5 哈希缓存实现超快速(<100ms)扫描。只重新处理发生变化的文件。
返回一个包含所有已发现技能摘要的 JSON。

## 第二步:技能匹配

```bash
python agent-orchestrator/scripts/match_skills.py "<用户请求内容>"
```

返回按相关性排序的技能 JSON。结果解读方式如下:

| 结果                    | 操作                                                     |
|:------------------------|:---------------------------------------------------------|
| `matched: 0`           | 没有相关技能。正常运行,不使用任何技能。                   |
| `matched: 1`           | 有一个相关技能。加载其 SKILL.md 并照做。                  |
| `matched: 2+`          | 多个技能。执行第三步(编排)。                             |

## 第三步:编排(如果 Matched >= 2)

```bash
python agent-orchestrator/scripts/orchestrate.py --skills skill1,skill2 --query "<请求内容>"
```

返回一个执行计划,包含模式、步骤顺序以及技能之间的数据流。

## 快速步骤(捷径)

对于简单的查询,可以把第一步和第二步按顺序合并执行:
```bash
python agent-orchestrator/scripts/scan_registry.py && python agent-orchestrator/scripts/match_skills.py "<请求内容>"
```

---

## 技能注册表

注册表位于:
```
agent-orchestrator/data/registry.json
```

## 搜索位置

扫描器会在以下位置查找 SKILL.md:
1. `.claude/skills/*/`(已在 Claude Code 中注册的技能)
2. `*/`(顶层的独立技能)
3. `*/*\`(子文件夹中的技能,最多三层深度)

## 每个技能的元数据

注册表中的每一条记录包含:

| 字段           | 描述                                                 |
|:---------------|:-----------------------------------------------------|
| name           | 技能名称(来自 YAML frontmatter)                      |
| description    | 完整描述(包含触发条件)                               |
| location       | 目录的绝对路径                                        |
| skill_md       | SKILL.md 的绝对路径                                   |
| registered     | 是否位于 .claude/skills/ 中(true/false)              |
| capabilities   | 能力标签(自动提取 + 显式声明)                        |
| triggers       | 从 description 中提取的激活关键词                     |
| language       | 主要语言(python/nodejs/bash/none)                    |
| status         | active / incomplete / missing                        |

## 注册表命令

```bash

## 快速扫描(使用哈希缓存)

python agent-orchestrator/scripts/scan_registry.py

## 详细状态表

python agent-orchestrator/scripts/scan_registry.py --status

## 完整重新扫描(忽略缓存)

python agent-orchestrator/scripts/scan_registry.py --force
```

---

## 匹配算法

对于每个请求,匹配器使用以下方式为技能打分:

| 条件                          | 分数    | 示例                                   |
|:------------------------------|:--------|:----------------------------------------|
| 查询中出现技能名称            | +15     | "use web-scraper" -> web-scraper        |
| 精确匹配触发关键词            | +10     | "scrape" -> web-scraper                 |
| 能力类别匹配                  | +5      | data-extraction -> web-scraper          |
| 词语重叠                      | +1      | 查询中的词出现在 description 中          |
| 项目加成                      | +20     | 技能被分配给当前活跃项目                  |

最低阈值:5 分。低于此分数的技能会被忽略。

## 按项目匹配

```bash
python agent-orchestrator/scripts/match_skills.py --project 我的项目 "这里是查询内容"
```

被分配给该项目的技能会自动获得 +20 的加成。

---

## 编排模式

当多个技能都相关时,编排器会对模式进行分类:

## 1. 顺序管道

技能构成一条链,其中一个技能的输出会喂给下一个技能。

**适用场景:** "生产型"技能(data-extraction、government-data)与"消费型"技能(messaging、social-media)混合出现时。

**示例:** web-scraper 收集价格 -> whatsapp-cloud-api 发送提醒

```
user_query -> web-scraper -> whatsapp-cloud-api -> result
```

## 2. 并行执行

多个技能独立地处理请求的不同方面。

**适用场景:** 所有技能承担相同的角色(都是生产型或都是消费型)。

**示例:** instagram 发布帖子 + whatsapp 发送通知(两者接收相同的内容)

```
user_query -> [instagram, whatsapp-cloud-api] -> aggregated_result
```

## 3. 主要 + 辅助

一个主要技能主导流程;其他技能提供辅助数据。

**适用场景:** 某个技能的得分远高于其他技能(>= 2 倍)。

**示例:** whatsapp-cloud-api 发送消息(主要) + web-scraper 提供数据(辅助)

```
user_query -> whatsapp-cloud-api (primary) + web-scraper (support) -> result
```

## 详情见 `references/orchestration-patterns.md`

---

## 项目管理

将技能分配给项目可以获得相关性加成以及持久化的上下文。

## 项目文件

```
agent-orchestrator/data/projects.json
```

## 操作

**创建项目:**
向 projects.json 添加一条记录:
```json
{
  "name": "nome-do-projeto",
  "created_at": "2026-02-25T12:00:00",
  "skills": ["web-scraper", "whatsapp-cloud-api"],
  "description": "Descricao do projeto"
}
```

**向项目添加技能:** 更新该项目的 `skills` 数组。

**从项目移除技能:** 从数组中移除。

**查询项目的技能:** 读取 projects.json 并列出已分配的技能。

---

## 添加新技能

要向生态系统添加一个新技能:

1. 在 `skills root:` 下的任意位置创建一个文件夹
2. 创建一个带有 YAML frontmatter 的 `SKILL.md`:
```yaml
---
name: minha-nova-skill
description: "带有激活关键词的描述……"
---

## 技能文档

```
3. **完成!** 自动发现机制会在下一次请求时自动检测到它。

可选地,为了让 Claude Code 的原生发现机制生效:
4. 把 SKILL.md 复制到 `.claude/skills/<名称>/SKILL.md`

## 显式能力标签(可选)

在 frontmatter 中添加以下内容,以获得更精确的匹配:
```yaml
capabilities: [data-extraction, web-automation]
```

---

## 查看所有技能的状态

```bash
python agent-orchestrator/scripts/scan_registry.py --status
```

## 解读状态

| 状态       | 含义                                               |
|:-----------|:----------------------------------------------------|
| active     | SKILL.md 中同时存在 name 和 description             |
| incomplete | SKILL.md 存在但缺少 name 或 description              |
| missing    | 目录存在但没有 SKILL.md                              |

---

## 当前生态系统中的技能

| 技能               | 能力                                   | 状态     |
|:-------------------|:----------------------------------------|:---------|
| web-scraper        | data-extraction, web-automation         | active   |
| junta-leiloeiros   | government-data, data-extraction        | active   |
| whatsapp-cloud-api | messaging, api-integration              | active   |
| instagram          | social-media, api-integration           | partial  |

*该表通过 `scan_registry.py --status` 自动更新。*

## 最佳实践

- 就你的项目和需求提供清晰、具体的上下文
- 在将建议应用到生产代码之前,先审查所有建议
- 与其他互补技能结合使用,以获得全面的分析

## 常见陷阱

- 将本技能用于其领域专长之外的任务
- 在不理解你的具体上下文的情况下应用建议
- 没有提供足够的项目上下文以获得准确的分析

## 相关技能

- `multi-advisor` - 用于增强分析的互补技能
- `task-intelligence` - 用于增强分析的互补技能

## 局限性
- 仅在任务明确符合上述范围时使用本技能。
- 不要把输出当作针对特定环境的验证、测试或专家评审的替代品。
- 如果所需的输入、权限、安全边界或成功标准缺失,应停下来寻求澄清。
