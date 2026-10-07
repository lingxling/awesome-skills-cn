---
name: bats-testing-patterns
description: 掌握 Bash 自动化测试系统 (Bats) 以实现全面的 shell 脚本测试。在为 shell 脚本编写测试、CI/CD 管道或需要 shell 工具的测试驱动开发时使用。
risk: critical
source: community
date_added: "2026-02-27"
---

# Bats 测试模式

使用 Bats（Bash 自动化测试系统）为 shell 脚本编写全面单元测试的综合指导，包括测试模式、设施和用于生产级 shell 测试的最佳实践。

## 何时使用此技能

- 为 shell 脚本编写单元测试
- 为脚本实现 TDD
- 在 CI/CD 管道中设置自动化测试
- 测试边界情况和错误条件
- 跨 shell 环境验证行为

## 何时不使用此技能

- 项目不使用 shell 脚本
- 您需要超出 shell 行为的集成测试
- 目标仅是 linting 或格式化

## 说明

- 确认 shell 方言和支持的环境。
- 设置包含帮助和设施的测试结构。
- 编写测试以验证退出代码、输出和副作用。
- 添加设置/拆卸并在 CI 中运行测试。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 资源

- `resources/implementation-playbook.md` - 详细的模式和示例。

## 限制

- 仅在任务明确符合上述范围时使用此技能。
- 不要将输出作为特定于环境的验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并要求澄清。
