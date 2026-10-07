---
name: brooks-sweep
description: "全面扫描模式：跨所有质量维度运行统一分析 — 代码衰退、架构、技术债务和测试质量 — 然后直接将修复应用于代码库。安全更改自动应用；风险更改在执行前确认。"
risk: critical
source: https://github.com/hyhmrright/brooks-lint/tree/main/skills/brooks-sweep
source_repo: hyhmrright/brooks-lint
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/hyhmrright/brooks-lint/blob/main/LICENSE
---

# Brooks-Lint — 全面扫描和自动修复
## 何时使用

当你需要全面扫描模式时使用此技能：跨所有质量维度运行统一分析 — 代码衰退、架构、技术债务和测试质量 — 然后直接将修复应用于代码库。安全更改自动应用；风险更改在执行前确认。借鉴十二部经典...


## 设置

1. 读取 `../_shared/common.md` 以获取铁律、项目配置、报告模板和健康评分规则
2. 读取 `../_shared/source-coverage.md` 以获取书籍级别覆盖、例外和权衡
3. 读取 `../_shared/decay-risks.md` 以获取生产风险症状定义
4. 读取 `../_shared/test-decay-risks.md` 以获取测试风险症状定义
5. 读取此目录中的 `sweep-guide.md` 以获取统一扫描和修复流程

## 流程

**如果用户未指定项目或目录：**在继续前从 `../_shared/common.md` 应用自动作用域检测以确定审查作用域。

1. 显示飞行前同意通知并等待用户的一次性批准（指南的第 0 步）
2. 列举作用域并初始化 `unresolvable` / `non_critical_rounds` / `fix_log` 状态（指南的第 1 步）
3. 按顺序运行四个维度 — 审查、测试、债务、审计 — 每个扫描、分类、应用安全 + 扩展安全修复，并通过项目测试命令验证（指南的第 2-5 步）
4. 迭代：重新扫描修改的文件 + 相同模块 + 静态消费者；收敛到干净轮次，将 3 次重试失败退出到 `unresolvable` 集，将非关键轮次上限设为 3（指南的第 6 步）
5. 汇总残留和不可解决的项目并输出全面扫描报告（指南的第 7-8 步）

**报告中的模式行：** `Full Sweep`

## 限制

- 仅当任务清楚地符合其上游源和本地项目背景时才使用此技能。
- 在应用更改之前验证命令、生成的代码、依赖项、凭据和外部服务行为。
- 不要将示例视为特定于环境的测试、安全审查或用户批准破坏性或昂贵操作的替代。
