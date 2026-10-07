---
name: brooks-debt
description: "技术债务评估，识别、分类和优先排列可维护性问题 — 帮助团队构建重构路线图 — 借鉴十二部经典工程著作。"
risk: safe
source: https://github.com/hyhmrright/brooks-lint/tree/main/skills/brooks-debt
source_repo: hyhmrright/brooks-lint
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/hyhmrright/brooks-lint/blob/main/LICENSE
---

# Brooks-Lint — 技术债务评估
## 何时使用

当你需要技术债务评估来识别、分类和优先排列可维护性问题 — 帮助团队构建重构路线图 — 借鉴十二部经典工程著作时，使用此技能。触发条件：用户提出关于技术债务、重构优先级、首先要清理什么，或询问"为什么...


## 设置

1. 读取 `../_shared/common.md` 以获取铁律、项目配置、报告模板和健康评分规则
2. 读取 `../_shared/source-coverage.md` 以获取书籍级别覆盖、例外和权衡
3. 读取 `../_shared/decay-risks.md` 以获取症状定义和源属性
4. 读取此目录中的 `debt-guide.md` 以获取债务分类框架

## 流程

**如果用户未描述代码库或指向特定区域：**在继续前从 `../_shared/common.md` 应用自动作用域检测以确定评估作用域。

1. 扫描所有六个衰退风险（指南的第 1 步）；在评分前列出每项发现
2. 应用 Pain × Spread 优先级公式并分类债务意图（指南的第 2-3 步）
3. 按衰退风险分组发现（指南的第 4 步）
4. 使用 common.md 中的报告模板输出，加上债务摘要表

**报告中的模式行：** `Tech Debt Assessment`

## 限制

- 仅当任务清楚地符合其上游源和本地项目背景时才使用此技能。
- 在应用更改之前验证命令、生成的代码、依赖项、凭据和外部服务行为。
- 不要将示例视为特定于环境的测试、安全审查或用户批准破坏性或昂贵操作的替代。
