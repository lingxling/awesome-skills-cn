---
name: vercel-react-native-skills
description:
  用于构建高性能移动应用的React Native和Expo最佳实践。在构建React Native组件、优化列表性能、实现动画或使用原生模块时使用。在涉及React Native、Expo、移动性能或原生平台API的任务时触发。
license: MIT
metadata:
  author: vercel
  version: '1.0.0'
---

# React Native 技能

React Native和Expo应用程序的综合最佳实践。包含跨多个类别的规则，涵盖性能、动画、UI模式和平台特定优化。

## 何时应用

在以下情况下参考这些指南：

- 构建React Native或Expo应用
- 优化列表和滚动性能
- 使用Reanimated实现动画
- 处理图像和媒体
- 配置原生模块或字体
- 使用原生依赖项构建monorepo项目

## 按优先级分类的规则

| 优先级 | 类别         | 影响   | 前缀               |
| -------- | ---------------- | -------- | -------------------- |
| 1        | 列表性能 | 关键 | `list-performance-`  |
| 2        | 动画        | 高     | `animation-`         |
| 3        | 导航       | 高     | `navigation-`        |
| 4        | UI模式      | 高     | `ui-`                |
| 5        | 状态管理 | 中等   | `react-state-`       |
| 6        | 渲染        | 中等   | `rendering-`         |
| 7        | Monorepo         | 中等   | `monorepo-`          |
| 8        | 配置    | 低      | `fonts-`, `imports-` |

## 快速参考

### 1. 列表性能（关键）

- `list-performance-virtualize` - 对大型列表使用FlashList
- `list-performance-item-memo` - 记忆列表项组件
- `list-performance-callbacks` - 稳定回调引用
- `list-performance-inline-objects` - 避免内联样式对象
- `list-performance-function-references` - 在渲染外提取函数
- `list-performance-images` - 优化列表中的图像
- `list-performance-item-expensive` - 将昂贵的工作移出项
- `list-performance-item-types` - 对异构列表使用项类型

### 2. 动画（高）

- `animation-gpu-properties` - 仅动画变换和不透明度
- `animation-derived-value` - 对计算动画使用useDerivedValue
- `animation-gesture-detector-press` - 使用Gesture.Tap而不是Pressable

### 3. 导航（高）

- `navigation-native-navigators` - 使用原生堆栈和原生标签页而非JS导航器

### 4. UI模式（高）

- `ui-expo-image` - 对所有图像使用expo-image
- `ui-image-gallery` - 使用Galeria进行图像灯箱
- `ui-pressable` - 使用Pressable而非TouchableOpacity
- `ui-safe-area-scroll` - 在ScrollViews中处理安全区域
- `ui-scrollview-content-inset` - 对页眉使用contentInset
- `ui-menus` - 使用原生上下文菜单
- `ui-native-modals` - 尽可能使用原生模态
- `ui-measure-views` - 使用onLayout，而非measure()
- `ui-styling` - 使用StyleSheet.create或Nativewind

### 5. 状态管理（中等）

- `react-state-minimize` - 最小化状态订阅
- `react-state-dispatcher` - 对回调使用调度器模式
- `react-state-fallback` - 在首次渲染时显示回退
- `react-compiler-destructure-functions` - 为React Compiler解构
- `react-compiler-reanimated-shared-values` - 使用编译器处理共享值

### 6. 渲染（中等）

- `rendering-text-in-text-component` - 将文本包装在Text组件中
- `rendering-no-falsy-and` - 避免对条件渲染使用falsy &&

### 7. Monorepo（中等）

- `monorepo-native-deps-in-app` - 将原生依赖项保留在应用包中
- `monorepo-single-dependency-versions` - 在包之间使用单一版本

### 8. 配置（低）

- `fonts-config-plugin` - 对自定义字体使用配置插件
- `imports-design-system-folder` - 组织设计系统导入
- `js-hoist-intl` - 提升Intl对象创建

## 如何使用

阅读单个规则文件以获取详细说明和代码示例：

```
rules/list-performance-virtualize.md
rules/animation-gpu-properties.md
```

每个规则文件包含：

- 为什么重要的简要说明
- 带有说明的错误代码示例
- 带有说明的正确代码示例
- 其他上下文和参考

## 完整编译文档

有关所有规则扩展的完整指南：`AGENTS.md`
