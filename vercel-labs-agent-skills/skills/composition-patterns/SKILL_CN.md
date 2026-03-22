---
name: vercel-composition-patterns
description:
  可扩展的 React 组合模式。在重构具有布尔属性泛滥的组件、构建灵活的组件库或设计可重用 API 时使用。在涉及复合组件、render props、context providers 或组件架构的任务时触发。包含 React 19 API 更改。
license: MIT
metadata:
  author: vercel
  version: '1.0.0'
---

# React 组合模式

用于构建灵活、可维护的 React 组件的组合模式。通过使用复合组件、提升状态和组合内部来避免布尔属性泛滥。这些模式使代码库在扩展时更容易让人类和 AI 智能体使用。

## 何时应用

在以下情况下参考这些指南：

- 重构具有许多布尔属性的组件
- 构建可重用的组件库
- 设计灵活的组件 API
- 审查组件架构
- 使用复合组件或 context providers

## 按优先级分类的规则

| 优先级 | 类别 | 影响 | 前缀 |
| -------- | ----------------------- | ------ | --------------- |
| 1 | 组件架构 | 高 | `architecture-` |
| 2 | 状态管理 | 中 | `state-` |
| 3 | 实现模式 | 中 | `patterns-` |
| 4 | React 19 API | 中 | `react19-` |

## 快速参考

### 1. 组件架构 (高)

- `architecture-avoid-boolean-props` - 不要添加布尔属性来自定义行为；使用组合
- `architecture-compound-components` - 使用共享上下文构建复杂组件

### 2. 状态管理 (中)

- `state-decouple-implementation` - Provider 是唯一知道如何管理状态的地方
- `state-context-interface` - 定义包含状态、操作、元数据的通用接口用于依赖注入
- `state-lift-state` - 将状态移动到 provider 组件中以便兄弟组件访问

### 3. 实现模式 (中)

- `patterns-explicit-variants` - 创建显式的变体组件而不是布尔模式
- `patterns-children-over-render-props` - 使用 children 进行组合而不是 renderX 属性

### 4. React 19 API (中)

> **⚠️ 仅限 React 19+。** 如果使用 React 18 或更早版本，请跳过此部分。

- `react19-no-forwardref` - 不要使用 `forwardRef`；使用 `use()` 代替 `useContext()`

## 如何使用

阅读单个规则文件以获取详细说明和代码示例：

```
rules/architecture-avoid-boolean-props.md
rules/state-context-interface.md
```

每个规则文件包含：

- 为什么重要的简要说明
- 带有说明的错误代码示例
- 带有说明的正确代码示例
- 其他上下文和参考

## 完整编译文档

获取所有规则展开的完整指南：`AGENTS.md`
