---
name: ai-native-cli
description: "包含 98 条规则的设计规范，用于构建 AI agent 能安全使用的 CLI 工具。涵盖结构化 JSON 输出、错误处理、输入契约、安全护栏、退出码以及 agent 自描述。"
risk: safe
source: https://github.com/ChaosRealmsAI/agent-cli-spec
date_added: "2026-03-15"
---

# Agent-Friendly CLI Spec v0.1

在构建或修改 CLI 工具时,遵循这些规则可以让 AI agent 安全、可靠地使用它们。

## 概述

一份全面的设计规范,用于构建 AI 原生的 CLI 工具。它定义了跨三个认证级别(Agent-Friendly、Agent-Ready、Agent-Native)的 98 条规则,并附有优先级标注(P0/P1/P2)。该规范涵盖结构化 JSON 输出、错误处理、输入契约、安全护栏、退出码、自描述,以及通过内置问题反馈系统实现的反馈闭环。

## 何时使用此技能

- 当构建一个将被 AI agent 调用的新 CLI 工具时使用
- 当对现有 CLI 进行改造以使其对 agent 友好时使用
- 当为自动化流水线设计命令行界面时使用
- 当审核某个 CLI 工具是否符合 agent 安全标准时使用

## 核心理念

1. **Agent 优先** —— 默认输出为 JSON;人类友好格式通过 `--human` 可选启用
2. **Agent 不可信** —— 对所有输入的校验标准应与公开 API 相同
3. **故障关闭(Fail-Closed)** —— 当校验逻辑本身出错时,默认拒绝
4. **可验证** —— 每条规则的写法都应便于自动化检查

## 分层模型

该规范使用两个正交的维度:

- **层(Layer)** 回答推出范围:`core`、`recommended`、`ecosystem`
- **优先级(Priority)** 回答严重程度:`P0`、`P1`、`P2`

迁移和认证时使用层级:

- **core** —— 执行契约:JSON、错误、退出码、stdout/stderr、安全
- **recommended** —— 更好的机器可用性:自描述、显式模式、更丰富的 schema
- **ecosystem** —— agent 原生集成:`agent/`、skills、issue、内联上下文

认证级别与层级对应:

- **Agent-Friendly** —— 所有 `core` 规则通过
- **Agent-Ready** —— 所有 `core` + `recommended` 规则通过
- **Agent-Native** —— 所有层级规则通过

## 工作原理

### 步骤 1:输出模式

默认是 agent 模式(JSON)。可通过显式标志切换:

```bash
$ mycli list              # 默认 = JSON 输出(agent 模式)
$ mycli list --human      # 人类友好格式:带颜色、表格、格式化
$ mycli list --agent      # 显式 agent 模式(需要时可覆盖配置)
```

- **默认(无标志)** —— JSON 输出到 stdout。agent 永远不需要添加标志。
- **--human** —— 人类友好格式(颜色、表格、进度条)
- **--agent** —— 显式 JSON 模式(当环境变量/配置覆盖了默认值时有用)

### 步骤 2:agent/ 目录约定

每个 CLI 工具必须在其项目根目录下有一个 `agent/` 目录。这是该工具对 AI agent 的身份与行为契约。

```
agent/
  brief.md          # 一段话:我是谁,我能做什么
  rules/            # 行为约束(自动注册)
    trigger.md      # agent 何时应该使用此工具
    workflow.md     # 分步使用流程
    writeback.md    # 如何写回反馈
  skills/           # 扩展能力(自动注册)
    getting-started.md
```

### 步骤 3:四个层级的自描述

1. **--brief**(名片,注入到 agent 配置中)
2. **每次命令响应**(始终开启的上下文:数据 + 规则 + skills + issue)
3. **--help**(完整自描述:brief + 命令 + 规则 + skills + issue)
4. **skills \<name\>**(按需深入了解某个具体的 skill)

## 认证要求

每个级别包含前一级别的所有规则。
优先级标签 `[P0]` = 没有它 agent 就会出错,`[P1]` = agent 能工作但表现不佳,`[P2]` = 有则更好。

### 级别 1:Agent-Friendly(core —— 20 条规则)

目标:CLI 是一个稳定、可调用的 API。agent 能够调用、解析,并处理错误。

**输出** —— 默认 JSON,schema 稳定
- `[P0]` O1:默认输出为 JSON。无需 `--json` 标志
- `[P0]` O2:JSON 必须通过 `jq .` 校验
- `[P0]` O3:同一版本内 JSON schema 不得变化

**错误** —— 结构化、输出到 stderr、绝不进入交互模式
- `[P0]` E1:错误 -> `{"error":true, "code":"...", "message":"...", "suggestion":"..."}` 输出到 stderr
- `[P0]` E4:错误具有机器可读的 `code`(例如 `MISSING_REQUIRED`)
- `[P0]` E5:错误具有人类可读的 `message`
- `[P0]` E7:发生错误时,绝不进入交互模式 —— 立即退出
- `[P0]` E8:错误码是 API 契约 —— 跨版本不得重命名

**退出码** —— 可预测的失败信号
- `[P0]` X3:参数/用法错误必须以 2 退出
- `[P0]` X9:失败必须以非零状态退出 —— 绝不能退出 0 后又在 stdout 中报告错误

**可组合性** —— 干净的管道语义
- `[P0]` C1:stdout 只用于数据
- `[P0]` C2:日志、进度、警告只发送到 stderr

**输入** —— 对错误输入快速失败
- `[P1]` I4:缺少必需参数 -> 结构化错误,绝不交互式提示
- `[P1]` I5:类型不匹配 -> 退出 2 + 结构化错误

**安全** —— 防止 agent 失误
- `[P1]` S1:破坏性操作需要 `--yes` 确认
- `[P1]` S4:拒绝 `../../` 路径穿越、控制字符

**护栏** —— 运行时输入保护
- `[P1]` G1:未知标志以退出码 2 拒绝
- `[P1]` G2:检测参数中的 API key / token 模式,拒绝执行
- `[P1]` G3:拒绝敏感文件路径(*.env、*.key、*.pem)
- `[P1]` G8:拒绝参数中的 shell 元字符(; | && $())

### 级别 2:Agent-Ready(+ recommended —— 59 条规则)

目标:CLI 具有自描述性、命名良好、管道友好。agent 能够发现能力并串联命令,无需反复试错。

**自描述** —— agent 发现 CLI 能做什么
- `[P1]` D1:`--help` 输出带 `commands[]` 的结构化 JSON
- `[P1]` D3:schema 具有必需字段(help、commands)
- `[P1]` D4:所有参数都有类型声明
- `[P1]` D7:参数标注为必需/可选
- `[P1]` D9:每个命令都有描述
- `[P1]` D11:`--help` 输出包含 help、rules、skills、commands 的 JSON
- `[P1]` D15:`--brief` 输出 `agent/brief.md` 的内容
- `[P1]` D16:默认 JSON(agent 模式),`--human` 为人类友好格式
- `[P2]` D2/D5/D6/D8/D10:逐命令帮助、枚举、默认值、输出 schema、版本

**输入** —— 无歧义的调用约定
- `[P1]` I1:所有标志使用 `--long-name` 格式
- `[P1]` I2:无位置参数歧义
- `[P2]` I3/I6/I7:--json-input、布尔 --no-X、数组参数

**错误**
- `[P1]` E6:错误包含 `suggestion` 字段
- `[P2]` E2/E3:错误输出到 stderr,错误 JSON 有效

**安全**
- `[P1]` S8:外部输入使用 `--sanitize` 标志
- `[P2]` S2/S3/S5/S6/S7:默认拒绝、--dry-run、禁止自动更新、破坏性操作标注

**退出码**
- `[P1]` X1:0 = 成功
- `[P2]` X2/X4-X8:1=通用、10=认证、11=权限、20=未找到、30=冲突

**可组合性**
- `[P1]` C6:管道模式下无交互式提示
- `[P2]` C3/C4/C5/C7:管道友好、--quiet、管道链、幂等性

**命名** —— 可预测的标志约定
- `[P1]` N4:保留标志(--agent、--human、--brief、--help、--version、--yes、--dry-run、--quiet、--fields)
- `[P2]` N1/N2/N3/N5/N6:命名一致性、kebab-case、最多 3 层、--version 语义化版本

**护栏**
- `[P1]` I8/I9:无隐式状态、非交互式认证
- `[P1]` G6/G9:前置条件检查、故障关闭
- `[P2]` G4/G5/G7:权限级别、PII 遮蔽、批处理上限

#### 保留标志

| 标志 | 语义 | 备注 |
|------|-----------|-------|
| `--agent` | JSON 输出(默认) | 显式覆盖 |
| `--human` | 人类友好输出 | 颜色、表格、格式化 |
| `--brief` | 一段话的身份说明 | 用于同步到 agent 配置 |
| `--help` | 完整自描述 JSON | brief + commands + rules + skills + issue |
| `--version` | 语义化版本字符串 | |
| `--yes` | 确认破坏性操作 | 删除/销毁操作必需 |
| `--dry-run` | 预览而不执行 | |
| `--quiet` | 抑制 stderr 输出 | |
| `--fields` | 过滤输出字段 | 节省 token |

### 级别 3:Agent-Native(+ ecosystem —— 19 条规则)

目标:CLI 具有身份、行为契约、skill 系统和反馈闭环。agent 能够学习该工具、扩展其用法,并报告问题 —— 实现完整的闭环协作。

**Agent 目录** —— 工具身份与行为契约
- `[P1]` D12:存在 `agent/brief.md`
- `[P1]` D13:`agent/rules/` 包含 trigger.md、workflow.md、writeback.md
- `[P1]` D17:agent/rules/*.md 具有 YAML frontmatter(name、description)
- `[P1]` D18:agent/skills/*.md 具有 YAML frontmatter(name、description)
- `[P2]` D14:`agent/skills/` 目录 + `skills` 子命令

**响应结构** —— 每次调用都附带内联上下文
- `[P1]` R1:每个响应都包含 `rules[]`(来自 agent/rules/ 的完整内容)
- `[P1]` R2:每个响应都包含 `skills[]`(名称 + 描述 + 命令)
- `[P1]` R3:每个响应都包含 `issue`(反馈指引)

**元信息** —— 项目级集成
- `[P2]` M1:项目根目录下有 AGENTS.md
- `[P2]` M2:可选的 MCP 工具 schema 导出
- `[P2]` M3:CHANGELOG.md 标注破坏性变更

**反馈** —— 内置的问题反馈系统
- `[P2]` F1:`issue` 子命令(create/list/show)
- `[P2]` F2:带 version/context/exit_code 的结构化提交
- `[P2]` F3:分类:bug / requirement / suggestion / bad-output
- `[P2]` F4:问题本地存储,不依赖外部服务
- `[P2]` F5:`issue list` / `issue show <id>` 可查询
- `[P2]` F6:问题具有状态跟踪(open/in-progress/resolved/closed)
- `[P2]` F7:问题的 JSON 包含所有必需字段(id、type、status、message、created_at、updated_at)
- `[P2]` F8:所有问题都有 status 字段

## 示例

### 示例 1:JSON 输出(Agent 模式)

```bash
$ mycli list
{"result": [{"id": 1, "title": "Buy milk", "status": "todo"}], "rules": [...], "skills": [...], "issue": "..."}
```

### 示例 2:结构化错误

```json
{
  "error": true,
  "code": "AUTH_EXPIRED",
  "message": "Access token expired 2 hours ago",
  "suggestion": "Run 'mycli auth refresh' to get a new token"
}
```

### 示例 3:退出码表

```
0   success         10  auth failed       20  resource not found
1   general error   11  permission denied 30  conflict/precondition
2   param/usage error
```

## 快速实现清单

按层级实现 —— 每个阶段带你到达下一个认证级别。

**阶段 1:Agent-Friendly(core)**
1. 默认输出为 JSON —— 无需 `--json` 标志
2. 错误处理器:`{ error, code, message, suggestion }` 输出到 stderr
3. 退出码:0 成功、2 参数错误、1 通用错误
4. stdout = 仅数据,stderr = 仅日志
5. 缺少参数 -> 结构化错误(绝不交互式)
6. 破坏性操作加上 `--yes` 保护
7. 护栏:拒绝密钥泄露、路径穿越、shell 元字符

**阶段 2:Agent-Ready(+ recommended)**
8. `--help` 返回结构化 JSON(help、commands[]、rules[]、skills[])
9. `--brief` 读取并输出 `agent/brief.md` 的内容
10. `--human` 标志切换到人类友好格式
11. 保留标志:--agent、--version、--dry-run、--quiet、--fields
12. 退出码:20 未找到、30 冲突、10 认证、11 权限

**阶段 3:Agent-Native(+ ecosystem)**
13. 创建 `agent/` 目录:`brief.md`、`rules/trigger.md`、`rules/workflow.md`、`rules/writeback.md`
14. 每个命令响应都附加:rules[] + skills[] + issue
15. `skills` 子命令:列出全部 / 显示某一项的完整内容
16. 用于反馈的 `issue` 子命令(create/list/show/close/transition)
17. 项目根目录下的 AGENTS.md

## 最佳实践

- 应该:默认输出 JSON,让 agent 永远不需要添加标志
- 应该:在每个错误响应中包含 `suggestion` 字段
- 应该:使用三级认证模型实现渐进式采用
- 应该:为节省 token,将 `agent/brief.md` 控制在一段话以内
- 不应该:在出错时进入交互模式 —— 始终立即退出
- 不应该:在同一版本内更改 JSON schema 或错误码
- 不应该:将日志或进度信息放在 stdout —— 只使用 stderr
- 不应该:静默接受未知标志 —— 以退出码 2 拒绝

## 常见陷阱

- **问题:** CLI 默认输出人类可读文本,破坏了 agent 的解析
  **解决方案:** 让 JSON 成为默认输出格式;添加 `--human` 标志用于人类友好模式

- **问题:** 错误以退出码 0 报告在 stdout 中
  **解决方案:** 失败时始终以非零状态退出,并将结构化错误 JSON 写入 stderr

- **问题:** CLI 对缺失输入进行交互式提示
  **解决方案:** 返回带 suggestion 字段的结构化错误,并立即退出

## 相关技能

- `@cli-best-practices` - 通用 CLI 设计模式(本技能专注于 AI agent 兼容性)

## 更多资源

- [Agent CLI Spec 仓库](https://github.com/ChaosRealmsAI/agent-cli-spec)

## 限制
- 仅在任务明确符合上述范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果所需的输入、权限、安全边界或成功标准缺失,请停下来寻求澄清。
