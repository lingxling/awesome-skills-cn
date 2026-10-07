---
name: brooks-test
description: "使用既定测试文献审查测试套件质量；识别脆弱性、模拟滥用、不清晰的设备、弱断言、缓慢反馈和维护风险。"
risk: safe
source: https://github.com/hyhmrright/brooks-lint/tree/main/skills/brooks-test
source_repo: hyhmrright/brooks-lint
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/hyhmrright/brooks-lint/blob/main/LICENSE
---

# Brooks-Lint — 测试质量审查
## 何时使用

当你需要基于十二部经典工程书籍的测试质量审查时使用此技能 — 主要关注 xUnit 测试模式、单元测试艺术、Google 如何测试软件和有效处理遗留代码 — 它诊断现有测试套件中的结构问题：脆弱性、模拟...


## 设置

1. 读取 `../_shared/common.md` 以获取铁律、项目配置、报告模板和健康评分规则
2. 读取 `../_shared/source-coverage.md` 以获取书籍级别覆盖、例外和权衡
3. 读取 `../_shared/test-decay-risks.md` 以获取测试空间症状定义和源属性
4. 读取此目录中的 `test-guide.md` 以获取测试质量审查框架

## 流程

**如果用户未共享测试文件或指向测试目录：**在继续前从 `../_shared/common.md` 应用自动作用域检测以确定审查作用域。

1. 构建测试套件地图（指南的"开始前"部分）
2. 按指定顺序扫描每个测试衰退风险（指南的第 1-4 步）
3. 应用铁律并使用报告模板输出（指南的第 5 步）

**报告中的模式行：** `Test Quality Review`

## 限制

- 仅当任务清楚地符合其上游源和本地项目背景时才使用此技能。
- 在应用更改之前验证命令、生成的代码、依赖项、凭据和外部服务行为。
- 不要将示例视为特定于环境的测试、安全审查或用户批准破坏性或昂贵操作的替代。
