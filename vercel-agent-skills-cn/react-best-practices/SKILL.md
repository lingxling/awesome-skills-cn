---
name: vercel-react-best-practices
description: 来自Vercel工程的React和Next.js性能优化指南。在编写、审查或重构React/Next.js代码时应使用此技能，以确保最佳性能模式。在涉及React组件、Next.js页面、数据获取、包优化或性能改进的任务时触发。
license: MIT
metadata:
  author: vercel
  version: "1.0.0"
---

# Vercel React 最佳实践

由Vercel维护的React和Next.js应用程序综合性能优化指南。包含8个类别中的57条规则，按影响优先级排序，以指导自动化重构和代码生成。

## 何时应用

在以下情况下参考这些指南：
- 编写新的React组件或Next.js页面
- 实现数据获取（客户端或服务器端）
- 审查代码的性能问题
- 重构现有的React/Next.js代码
- 优化包大小或加载时间

## 按优先级划分的规则类别

| 优先级 | 类别 | 影响 | 前缀 |
|----------|----------|--------|--------|
| 1 | 消除瀑布流 | 关键 | `async-` |
| 2 | 包大小优化 | 关键 | `bundle-` |
| 3 | 服务器端性能 | 高 | `server-` |
| 4 | 客户端数据获取 | 中-高 | `client-` |
| 5 | 重渲染优化 | 中 | `rerender-` |
| 6 | 渲染性能 | 中 | `rendering-` |
| 7 | JavaScript性能 | 低-中 | `js-` |
| 8 | 高级模式 | 低 | `advanced-` |

## 快速参考

### 1. 消除瀑布流（关键）

- `async-defer-await` - 将await移到实际使用的分支中
- `async-parallel` - 对独立操作使用Promise.all()
- `async-dependencies` - 对部分依赖使用better-all
- `async-api-routes` - 在API路由中尽早启动promise，延迟await
- `async-suspense-boundaries` - 使用Suspense流式传输内容

### 2. 包大小优化（关键）

- `bundle-barrel-imports` - 直接导入，避免桶文件
- `bundle-dynamic-imports` - 对重型组件使用next/dynamic
- `bundle-defer-third-party` - 在水合后加载分析/日志
- `bundle-conditional` - 仅在激活功能时加载模块
- `bundle-preload` - 在悬停/聚焦时预加载以获得感知速度

### 3. 服务器端性能（高）

- `server-auth-actions` - 像API路由一样认证服务器操作
- `server-cache-react` - 使用React.cache()进行每请求去重
- `server-cache-lru` - 使用LRU缓存进行跨请求缓存
- `server-dedup-props` - 避免在RSC props中重复序列化
- `server-serialization` - 最小化传递给客户端组件的数据
- `server-parallel-fetching` - 重构组件以并行化获取
- `server-after-nonblocking` - 使用after()进行非阻塞操作

### 4. 客户端数据获取（中-高）

- `client-swr-dedup` - 使用SWR进行自动请求去重
- `client-event-listeners` - 去重全局事件监听器
- `client-passive-event-listeners` - 对滚动使用被动监听器
- `client-localstorage-schema` - 版本化和最小化localStorage数据

### 5. 重渲染优化（中）

- `rerender-defer-reads` - 不要订阅仅在回调中使用的状态
- `rerender-memo` - 将昂贵的工作提取到记忆组件中
- `rerender-memo-with-default-value` - 提升默认非原始props
- `rerender-dependencies` - 在效果中使用原始依赖项
- `rerender-derived-state` - 订阅派生布尔值，而不是原始值
- `rerender-derived-state-no-effect` - 在渲染期间派生状态，而不是效果
- `rerender-functional-setstate` - 使用函数setState进行稳定回调
- `rerender-lazy-state-init` - 将函数传递给useState以获取昂贵值
- `rerender-simple-expression-in-memo` - 避免对简单原始值使用memo
- `rerender-move-effect-to-event` - 将交互逻辑放在事件处理程序中
- `rerender-transitions` - 对非紧急更新使用startTransition
- `rerender-use-ref-transient-values` - 对瞬态频繁值使用refs

### 6. 渲染性能（中）

- `rendering-animate-svg-wrapper` - 动画div包装器，而不是SVG元素
- `rendering-content-visibility` - 对长列表使用content-visibility
- `rendering-hoist-jsx` - 将静态JSX提取到组件外部
- `rendering-svg-precision` - 减少SVG坐标精度
- `rendering-hydration-no-flicker` - 对仅客户端数据使用内联脚本
- `rendering-hydration-suppress-warning` - 抑制预期的不匹配
- `rendering-activity` - 对显示/隐藏使用Activity组件
- `rendering-conditional-render` - 使用三元运算符，而不是&&进行条件渲染
- `rendering-usetransition-loading` - 优先使用useTransition进行加载状态

### 7. JavaScript性能（低-中）

- `js-batch-dom-css` - 通过类或cssText分组CSS更改
- `js-index-maps` - 为重复查找构建Map
- `js-cache-property-access` - 在循环中缓存对象属性
- `js-cache-function-results` - 在模块级Map中缓存函数结果
- `js-cache-storage` - 缓存localStorage/sessionStorage读取
- `js-combine-iterations` - 将多个filter/map组合到一个循环中
- `js-length-check-first` - 在昂贵比较之前检查数组长度
- `js-early-exit` - 从函数中提前返回
- `js-hoist-regexp` - 将RegExp创建提升到循环外部
- `js-min-max-loop` - 使用循环进行min/max而不是排序
- `js-set-map-lookups` - 使用Set/Map进行O(1)查找
- `js-tosorted-immutable` - 使用toSorted()进行不可变性

### 8. 高级模式（低）

- `advanced-event-handler-refs` - 在refs中存储事件处理程序
- `advanced-init-once` - 每次应用加载初始化一次
- `advanced-use-latest` - useLatest用于稳定回调refs

## 如何使用

阅读单个规则文件以获取详细解释和代码示例：

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
```

每个规则文件包含：
- 为什么重要的简要解释
- 带有解释的错误代码示例
- 带有解释的正确代码示例
- 额外上下文和参考

## 完整编译文档

获取所有规则扩展的完整指南：`AGENTS.md`
