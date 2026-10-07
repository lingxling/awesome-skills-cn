---
name: brooks-audit
description: "架构审计，映射模块依赖关系、检查分层完整性并标记整个代码库的结构衰退，借鉴十二部经典工程著作。"
risk: safe
source: https://github.com/hyhmrright/brooks-lint/tree/main/skills/brooks-audit
source_repo: hyhmrright/brooks-lint
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/hyhmrright/brooks-lint/blob/main/LICENSE
---

# Brooks-Lint — 架构审计
## 何时使用

当你需要架构审计来映射模块依赖关系、检查分层完整性并标记整个代码库的结构衰退，借鉴十二部经典工程著作时，使用此技能。触发条件：用户要求审计架构、查看文件夹/模块结构、检查循环导入、理解...


## 设置

1. 读取 `../_shared/common.md` 以获取铁律、项目配置、报告模板和健康评分规则
2. 读取 `../_shared/source-coverage.md` 以获取书籍级别覆盖、例外和权衡
3. 读取 `../_shared/decay-risks.md` 以获取症状定义和源属性
4. 读取此目录中的 `architecture-guide.md` 以获取审计框架

## 流程

**入职模式：**如果用户要求入职报告、代码库导览或
"向新开发人员解释此代码库"，从此
目录读取 `onboarding-guide.md` 并按照它而不是 `architecture-guide.md`。此模式解释而不是诊断 — 无健康评分、无铁律发现。

**如果用户未指定要审计的文件或目录：**在继续之前从 `../_shared/common.md` 应用自动作用域检测以确定审计作用域。

1. 收集代码库上下文并将模块依赖关系图绘制为 Mermaid（指南的第 0-1 步）
2. 按指定顺序扫描每个衰退风险（指南的第 2-4 步）
3. 根据发现为 Mermaid 图中的节点分配颜色（红色/黄色/绿色）— 第 4 步之后
4. 运行可测试性接缝评估（指南的第 5 步）
5. 运行 Conway 定律检查（指南的第 6 步）
6. 使用 common.md 中的报告模板输出 — 首先是 Mermaid 图，然后是发现

**报告中的模式行：** `Architecture Audit`

## 限制

- 仅当任务清楚地符合其上游源和本地项目背景时才使用此技能。
- 在应用更改之前验证命令、生成的代码、依赖项、凭据和外部服务行为。
- 不要将示例视为特定于环境的测试、安全审查或用户批准破坏性或昂贵操作的替代。
