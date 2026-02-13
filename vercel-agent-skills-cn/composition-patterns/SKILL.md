---
name: vercel-composition-patterns
description:
  可扩展的React组合模式。在重构具有布尔prop激增的组件、构建灵活的组件库或设计可重用API时使用。在涉及复合组件、render props、上下文提供者或组件架构的任务时触发。包括React 19 API更改。
license: MIT
metadata:
  author: vercel
  version: '1.0.0'
---

# React 组合模式

用于构建灵活、可维护的React组件的组合模式。通过使用复合组件、提升状态和组合内部来避免布尔prop激增。这些模式使代码库在扩展时更容易为人类和AI代理使用。

## 何时应用

在以下情况下参考这些指南：

- 重构具有许多布尔props的组件
- 构建可重用的组件库
- 设计灵活的组件API
- 审查组件架构
- 使用复合组件或上下文提供者

## 按优先级分类的规则

| 优先级 | 类别                | 影响 | 前缀          |
| -------- | ----------------------- | ------ | --------------- |
| 1        | 组件架构  | 高   | `architecture-` |
| 2        | 状态管理        | 中等 | `state-`        |
| 3        | 实现模式 | 中等 | `patterns-`     |
| 4        | React 19 APIs           | 中等 | `react19-`      |

## 快速参考

### 1. 组件架构（高）

- `architecture-avoid-boolean-props` - 不要添加布尔props来自定义行为；使用组合
- `architecture-compound-components` - 使用共享上下文结构复杂组件

### 2. 状态管理（中等）

- `state-decouple-implementation` - 提供者是唯一知道如何管理状态的地方
- `state-context-interface` - 定义通用接口，包括状态、操作、元数据以进行依赖注入
- `state-lift-state` - 将状态移动到提供者组件以进行兄弟访问

### 3. 实现模式（中等）

- `patterns-explicit-variants` - 创建显式变体组件而不是布尔模式
- `patterns-children-over-render-props` - 使用children进行组合而不是renderX props

### 4. React 19 API（中等）

> **⚠️ 仅限React 19+。** 如果使用React 18或更早版本，请跳过此部分。

- `react19-no-forwardref` - 不要使用`forwardRef`；使用`use()`而不是`useContext()`

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

有关所有规则扩展的完整指南：`AGENTS.md`
