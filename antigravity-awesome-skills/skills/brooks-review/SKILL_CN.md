---
name: brooks-review
description: "PR 代码审查，呈现衰退风险、设计异味和可维护性问题，具有具体的症状 → 源 → 后果 → 补救发现，借鉴十二部经典工程著作。"
risk: safe
source: https://github.com/hyhmrright/brooks-lint/tree/main/skills/brooks-review
source_repo: hyhmrright/brooks-lint
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/hyhmrright/brooks-lint/blob/main/LICENSE
---

# Brooks-Lint — PR 审查
## 何时使用

当你需要 PR 代码审查来呈现衰退风险、设计异味和可维护性问题，具有具体的症状 → 源 → 后果 → 补救发现，借鉴十二部经典工程著作时，使用此技能。触发条件：用户要求审查代码、检查 PR、共享 diff 或粘贴代码要求...


## 设置

1. 读取 `../_shared/common.md` 以获取铁律、项目配置、报告模板和健康评分规则
2. 读取 `../_shared/source-coverage.md` 以获取书籍级别覆盖、例外和权衡
3. 读取 `../_shared/decay-risks.md` 以获取症状定义和源属性
4. 读取此目录中的 `pr-review-guide.md` 以获取分析流程

## 流程

**如果用户未指定文件或粘贴代码：**在继续前从 `../_shared/common.md` 应用自动作用域检测以确定审查作用域。

1. 理解审查作用域，然后按指定顺序扫描每个衰退风险（指南的第 1-6 步）
2. 运行快速测试检查（指南的第 7 步）— 跳过仅文档或非生产更改
3. 将铁律应用于每项发现
4. 使用 common.md 中的报告模板输出

**报告中的模式行：** `PR Review`

## 示例

**用户请求：**

> 使用 @brooks-review 完成此任务：PR 代码审查，呈现衰退风险、设计异味和可维护性问题，具有具体的症状 → 源 → 后果 → 补救发现，借鉴十二部经典工程著作。

## 限制

- 仅当任务清楚地符合其上游源和本地项目背景时才使用此技能。
- 在应用更改之前验证命令、生成的代码、依赖项、凭据和外部服务行为。
- 不要将示例视为特定于环境的测试、安全审查或用户批准破坏性或昂贵操作的替代。
