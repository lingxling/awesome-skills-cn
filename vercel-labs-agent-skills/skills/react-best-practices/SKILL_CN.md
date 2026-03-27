---
name: vercel-react-best-practices
description: 来自 Vercel 工程团队的 React 和 Next.js 性能优化指南。在编写、审查或重构 React/Next.js 代码以确保最佳性能模式时使用。在涉及 React 组件、Next.js 页面、数据获取、包优化或性能改进的任务时触发。
license: MIT
metadata:
  author: vercel
  version: "1.0.0"
---

# Vercel React 最佳实践

由 Vercel 维护的 React 和 Next.js 应用的综合性能优化指南。包含 8 个类别中的 65 条规则，按影响优先级排序，指导自动重构和代码生成。

## 何时应用

在以下情况下参考这些指南：
- 编写新的 React 组件或 Next.js 页面
- 实现数据获取（客户端或服务器端）
- 审查代码的性能问题
- 重构现有的 React/Next.js 代码
- 优化包大小或加载时间

## 按优先级排序的规则类别

| 优先级 | 类别 | 影响 | 前缀 |
|----------|----------|--------|--------|
| 1 | 消除瀑布流 | 关键 | `async-` |
| 2 | 包大小优化 | 关键 | `bundle-` |
| 3 | 服务器端性能 | 高 | `server-` |
| 4 | 客户端数据获取 | 中高 | `client-` |
| 5 | 重渲染优化 | 中 | `rerender-` |
| 6 | 渲染性能 | 中 | `rendering-` |
| 7 | JavaScript 性能 | 低中 | `js-` |
| 8 | 高级模式 | 低 | `advanced-` |

## 快速参考

### 1. 消除瀑布流（关键）

- `async-defer-await` - 将 await 移到实际使用的分支中
- `async-parallel` - 对独立操作使用 Promise.all()
- `async-dependencies` - 对部分依赖使用 better-all
- `async-api-routes` - 在 API 路由中尽早启动 Promise，延迟 await
- `async-suspense-boundaries` - 使用 Suspense 流式传输内容

### 2. 包大小优化（关键）

- `bundle-barrel-imports` - 直接导入，避免桶文件
- `bundle-dynamic-imports` - 对重组件使用 next/dynamic
- `bundle-defer-third-party` - 在水合后加载分析/日志记录
- `bundle-conditional` - 仅当功能激活时加载模块
- `bundle-preload` - 为感知速度在悬停/焦点时预加载

### 3. 服务器端性能（高）

- `server-auth-actions` - 像 API 路由一样验证服务器操作
- `server-cache-react` - 使用 React.cache() 进行每个请求的去重
- `server-cache-lru` - 使用 LRU 缓存进行跨请求缓存
- `server-dedup-props` - 避免 RSC props 中的重复序列化
- `server-hoist-static-io` - 将静态 I/O（字体、徽标）提升到模块级别
- `server-serialization` - 最小化传递给客户端组件的数据
- `server-parallel-fetching` - 重构组件以并行化获取
- `server-parallel-nested-fetching` - 对 Promise.all 中的每个项目链接嵌套获取
- `server-after-nonblocking` - 对非阻塞操作使用 after()

### 4. 客户端数据获取（中高）

- `client-swr-dedup` - 使用 SWR 进行自动请求去重
- `client-event-listeners` - 去重全局事件监听器
- `client-passive-event-listeners` - 对滚动使用 passive 监听器
- `client-localstorage-schema` - 版本化并最小化 localStorage 数据

### 5. 重渲染优化（中）

- `rerender-defer-reads` - 不要订阅仅在回调中使用的状态
- `rerender-memo` - 将昂贵的工作提取到 memoized 组件中
- `rerender-memo-with-default-value` - 提升默认非原始 props
- `rerender-dependencies` - 在 effects 中使用原始依赖项
- `rerender-derived-state` - 订阅派生的布尔值，而不是原始值
- `rerender-derived-state-no-effect` - 在渲染期间派生状态，而不是在 effects 中
- `rerender-functional-setstate` - 对稳定回调使用 functional setState
- `rerender-lazy-state-init` - 为昂贵值传递函数给 useState
- `rerender-simple-expression-in-memo` - 避免对简单原始值使用 memo
- `rerender-split-combined-hooks` - 拆分具有独立依赖项的 hooks
- `rerender-move-effect-to-event` - 将交互逻辑放在事件处理程序中
- `rerender-transitions` - 对非紧急更新使用 startTransition
- `rerender-use-deferred-value` - 延迟昂贵的渲染以保持输入响应
- `rerender-use-ref-transient-values` - 对瞬态频繁值使用 refs
- `rerender-no-inline-components` - 不要在组件内部定义组件

### 6. 渲染性能（中）

- `rendering-animate-svg-wrapper` - 为 div 包装器设置动画，而不是 SVG 元素
- `rendering-content-visibility` - 对长列表使用 content-visibility
- `rendering-hoist-jsx` - 将静态 JSX 提取到组件外部
- `rendering-svg-precision` - 减少 SVG 坐标精度
- `rendering-hydration-no-flicker` - 对仅客户端数据使用内联脚本
- `rendering-hydration-suppress-warning` - 抑制预期的不匹配
- `rendering-activity` - 使用 Activity 组件进行显示/隐藏
- `rendering-conditional-render` - 使用三元运算符，而不是 && 进行条件渲染
- `rendering-usetransition-loading` - 对加载状态使用 useTransition
- `rendering-resource-hints` - 使用 React DOM 资源提示进行预加载
- `rendering-script-defer-async` - 在脚本标签上使用 defer 或 async

### 7. JavaScript 性能（低中）

- `js-batch-dom-css` - 通过类或 cssText 分组 CSS 更改
- `js-index-maps` - 为重复查找构建 Map
- `js-cache-property-access` - 在循环中缓存对象属性
- `js-cache-function-results` - 在模块级 Map 中缓存函数结果
- `js-cache-storage` - 缓存 localStorage/sessionStorage 读取
- `js-combine-iterations` - 将多个 filter/map 合并到一个循环中
- `js-length-check-first` - 在昂贵比较之前检查数组长度
- `js-early-exit` - 从函数中提前返回
- `js-hoist-regexp` - 将 RegExp 创建提升到循环外部
- `js-min-max-loop` - 对 min/max 使用循环而不是 sort
- `js-set-map-lookups` - 对 O(1) 查找使用 Set/Map
- `js-tosorted-immutable` - 对不可变性使用 toSorted()
- `js-flatmap-filter` - 使用 flatMap 在一次传递中映射和过滤
- `js-request-idle-callback` - 将非关键工作延迟到浏览器空闲时间

### 8. 高级模式（低）

- `advanced-event-handler-refs` - 在 refs 中存储事件处理程序
- `advanced-init-once` - 每个应用加载初始化一次应用
- `advanced-use-latest` - 对稳定回调 refs 使用 useLatest

## 如何使用

阅读单个规则文件以获取详细说明和代码示例：

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
```

每个规则文件包含：
- 简要解释为什么它很重要
- 带有解释的错误代码示例
- 带有解释的正确代码示例
- 其他上下文和参考

## 完整编译文档

有关所有规则的完整指南：`AGENTS.md`