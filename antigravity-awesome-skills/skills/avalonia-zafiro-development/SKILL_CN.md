---
name: avalonia-zafiro-development
description: "使用 Zafiro 工具包进行 Avalonia UI 开发的强制技能、约定和行为规则。"
risk: safe
source: community
date_added: "2026-02-27"
---

# Avalonia Zafiro 开发

此技能定义了使用 Avalonia UI 和 Zafiro 工具包开发跨平台应用程序的强制约定和行为规则。这些规则优先考虑可维护性、正确性和函数式响应式方法。

## 核心支柱

1.  **函数式响应式 MVVM**: 使用 DynamicData 和 ReactiveUI 的纯 MVVM 逻辑。
2.  **安全性和可预测性**: 使用 `Result` 类型显式处理错误，避免将异常用于流控制。
3.  **跨平台卓越**: 严格的 Avalonia 独立 ViewModel 和组合优于继承。
4.  **Zafiro 优先**: 利用现有的 Zafiro 抽象和辅助工具以避免冗余。

## 指南

- [核心技术技能和架构](core-technical-skills.md)：基本技能和架构原则。
- [命名和编码标准](naming-standards.md)：命名、字段和错误处理的规则。
- [Avalonia、Zafiro 和响应式规则](avalonia-reactive-rules.md)：UI、Zafiro 集成和 DynamicData 管道的具体指南。
- [Zafiro 快捷方式](zafiro-shortcuts.md)：常见 Rx/Zafiro 操作的简洁映射。
- [常见模式](patterns.md)：高级模式，如 `RefreshableCollection` 和验证。

## 编写代码前的流程

1.  **首先搜索**: 在代码库中搜索类似的实现或现有的 Zafiro 辅助工具。
2.  **可重用扩展**: 如果缺少辅助工具，建议创建新的可重用扩展方法，而不是内联复杂逻辑。
3.  **响应式管道**: 确保在适用的地方使用 DynamicData 运算符，而不是普通 Rx。

## 何时使用
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务清楚地匹配上述范围时使用此技能。
- 不要将输出视为特定于环境的验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，停止并寻求澄清。
