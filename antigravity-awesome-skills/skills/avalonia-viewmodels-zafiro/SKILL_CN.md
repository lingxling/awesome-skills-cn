---
name: avalonia-viewmodels-zafiro
description: "使用 Zafiro 和 ReactiveUI 为 Avalonia 创建 ViewModel 和向导的最优模式。"
risk: none
source: community
date_added: "2026-02-27"
---

# 使用 Zafiro 的 Avalonia ViewModel

此技能为创建 ViewModel、向导和管理 Avalonia 应用程序中的导航提供了一套最佳实践和模式，利用了 **ReactiveUI** 和 **Zafiro** 工具包的强大功能。

## 核心原则

1.  **函数式响应式方法**: 使用 ReactiveUI（`ReactiveObject`、`WhenAnyValue` 等）处理状态和逻辑。
2.  **增强命令**: 利用 `IEnhancedCommand` 获得更好的命令管理，包括进度报告和名称/文本属性。
3.  **向导模式**: 使用 `SlimWizard` 和 `WizardBuilder` 实现复杂流程，以实现声明式和可维护的方法。
4.  **自动部分发现**: 使用 `[Section]` 属性自动注册和发现 UI 部分。
5.  **干净组合**: 使用 `DataTypeViewLocator` 将 ViewModel 映射到视图，并在 `CompositionRoot` 中管理依赖项。

## 指南

- [ViewModel 和命令](viewmodels.md)：创建强大的 ViewModel 和处理命令。
- [向导和流程](wizards.md)：使用 `SlimWizard` 构建多步向导。
- [导航和部分](navigation_sections.md)：管理导航和基于部分的 UI。
- [组合和映射](composition.md)：View-ViewModel 连接和 DI 的最佳实践。

## 示例参考

有关真实世界的实现，请参考 **Angor** 项目：
- `CreateProjectFlowV2.cs`：复杂向导构建的出色示例。
- `HomeViewModel.cs`：使用函数式响应式命令的简单部分 ViewModel。

## 何时使用
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务清楚地匹配上述范围时使用此技能。
- 不要将输出视为特定于环境的验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，停止并寻求澄清。
