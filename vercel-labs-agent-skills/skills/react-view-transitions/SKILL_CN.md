---
name: vercel-react-view-transitions
description: 使用 React 的 View Transition API（`<ViewTransition>` 组件、`addTransitionType` 和 CSS 视图过渡伪元素）实现流畅、原生感动画的指南。当用户想要添加页面过渡、动画路由更改、创建共享元素动画、动画组件的进入/退出、动画列表重新排序、实现定向（前进/后退）导航动画，或在 Next.js 中集成视图过渡时使用此技能。当用户提及视图过渡、`startViewTransition`、`ViewTransition`、过渡类型，或询问在不使用第三方动画库的情况下在 React 中动画 UI 状态之间的切换时也使用此技能。
license: MIT
metadata:
  author: vercel
  version: "1.0.0"
---

# React 视图过渡

使用浏览器的原生 `document.startViewTransition` 在 UI 状态之间创建动画。使用 `<ViewTransition>` 声明*什么*需要动画，使用 `startTransition` / `useDeferredValue` / `Suspense` 触发*何时*动画，使用 CSS 类控制*如何*动画。不支持的浏览器会优雅地跳过动画。

## 何时添加动画

每个 `<ViewTransition>` 都应该传达空间关系或连续性。如果你无法明确它传达的内容，就不要添加它。

按照以下顺序实现**所有**适用的模式：

| 优先级 | 模式 | 传达的内容 |
|----------|---------|---------------------|
| 1 | **共享元素** (`name`) | "同一事物 — 深入了解" |
| 2 | **Suspense 揭示** | "数据已加载" |
| 3 | **列表标识** (每项目 `key`) | "相同项目，新排列" |
| 4 | **状态变化** (`enter`/`exit`) | "某物出现/消失" |
| 5 | **路由变化** (布局级别) | "前往新位置" |

这是一个实现顺序，不是"选择一个"的列表。实现适合应用的每一个模式。只有当应用没有该模式的用例时才跳过它。

### 选择动画风格

| 上下文 | 动画 | 原因 |
|---------|-----------|-----|
| 层次导航（列表 → 详情） | 类型键控 `nav-forward` / `nav-back` | 传达空间深度 |
| 横向导航（标签到标签） | 简单 `<ViewTransition>`（淡入淡出）或 `default="none"` | 无需传达深度 |
| Suspense 揭示 | `enter`/`exit` 字符串属性 | 内容到达 |
| 重新验证 / 后台刷新 | `default="none"` | 静默 — 无需动画 |

为层次导航（列表 → 详情）和有序序列（上一张/下一张照片、轮播、分页结果）保留定向滑动。对于有序序列，方向传达位置："下一个"从右侧滑动，"上一个"从左侧滑动。横向/无序导航（标签到标签）不应使用定向滑动 — 这会错误地暗示空间深度。

---

## 可用性

- **Next.js：** 不要安装 `react@canary` — App Router 已经在内部捆绑了 React canary。`ViewTransition` 开箱即用。`npm ls react` 可能显示一个看起来稳定的版本；这是预期的。
- **没有 Next.js：** 安装 `react@canary react-dom@canary`（`ViewTransition` 不在稳定版 React 中）。
- 浏览器支持：Chromium 111+、Firefox 144+、Safari 18.2+。在不支持的浏览器上优雅降级。

---

## 实现工作流

当向现有应用添加视图过渡时，**逐步遵循 `references/implementation.md`**。从审计开始 — 不要跳过它。将 `references/css-recipes.md` 中的 CSS 配方复制到全局样式表中 — 不要自己编写动画 CSS。

---

## 核心概念

### `<ViewTransition>` 组件

```jsx
import { ViewTransition } from 'react';

<ViewTransition>
  <Component />
</ViewTransition>
```

React 会自动分配唯一的 `view-transition-name` 并在后台调用 `document.startViewTransition`。永远不要自己调用 `startViewTransition`。

### 动画触发器

| 触发器 | 触发时机 |
|---------|--------------|
| **enter** | `<ViewTransition>` 在过渡期间首次插入 |
| **exit** | `<ViewTransition>` 在过渡期间首次移除 |
| **update** | `<ViewTransition>` 内部的 DOM 突变。对于嵌套 VT，突变应用于最内层的一个 |
| **share** | 命名 VT 卸载，另一个具有相同 `name` 的 VT 在同一过渡中挂载 |

只有 `startTransition`、`useDeferredValue` 或 `Suspense` 会激活 VT。常规 `setState` 不会动画。

### 关键放置规则

`<ViewTransition>` 只有在**出现在任何 DOM 节点之前**时才会激活 enter/exit：

```jsx
// 有效
<ViewTransition enter="auto" exit="auto">
  <div>Content</div>
</ViewTransition>

// 无效 — div 包裹了 VT，抑制了 enter/exit
<div>
  <ViewTransition enter="auto" exit="auto">
    <div>Content</div>
  </ViewTransition>
</div>
```

---

## 使用视图过渡类进行样式设计

### 属性

值：`"auto"`（浏览器交叉淡入淡出）、`"none"`（禁用）、`"class-name"`（自定义 CSS），或用于类型特定动画的 `{ [type]: value }`。

```jsx
<ViewTransition default="none" enter="slide-in" exit="slide-out" share="morph" />
```

如果 `default` 为 `"none"`，则所有触发器都关闭，除非明确列出。

### CSS 伪元素

- `::view-transition-old(.class)` — 出站快照
- `::view-transition-new(.class)` — 入站快照
- `::view-transition-group(.class)` — 容器
- `::view-transition-image-pair(.class)` — 旧 + 新配对

有关即用型动画配方，请参见 `references/css-recipes.md`。

---

## 过渡类型

使用 `addTransitionType` 标记过渡，以便 VT 可以根据上下文选择不同的动画。多次调用它来堆叠类型 — 树中的不同 VT 对不同类型做出反应：

```jsx
startTransition(() => {
  addTransitionType('nav-forward');
  addTransitionType('select-item');
  router.push('/detail/1');
});
```

传递一个对象来将类型映射到 CSS 类。适用于 `enter`、`exit` 和 `share`：

```jsx
<ViewTransition
  enter={{ 'nav-forward': 'slide-from-right', 'nav-back': 'slide-from-left', default: 'none' }}
  exit={{ 'nav-forward': 'slide-to-left', 'nav-back': 'slide-to-right', default: 'none' }}
  share={{ 'nav-forward': 'morph-forward', 'nav-back': 'morph-back', default: 'morph' }}
  default="none"
>
  <Page />
</ViewTransition>
```

`enter` 和 `exit` 不必对称。例如，淡入但定向滑出：

```jsx
<ViewTransition
  enter={{ 'nav-forward': 'fade-in', 'nav-back': 'fade-in', default: 'none' }}
  exit={{ 'nav-forward': 'nav-forward', 'nav-back': 'nav-back', default: 'none' }}
  default="none"
>
```

**TypeScript：** `ViewTransitionClassPerType` 要求对象中有一个 `default` 键。

对于有多页面的应用，将类型键控 VT 提取到可重用的包装器中：

```jsx
export function DirectionalTransition({ children }: { children: React.ReactNode }) {
  return (
    <ViewTransition
      enter={{ 'nav-forward': 'nav-forward', 'nav-back': 'nav-back', default: 'none' }}
      exit={{ 'nav-forward': 'nav-forward', 'nav-back': 'nav-back', default: 'none' }}
      default="none"
    >
      {children}
    </ViewTransition>
  );
}
```

### `router.back()` 和浏览器后退按钮

`router.back()` 和浏览器的后退/前进按钮**不会**触发视图过渡（`popstate` 是同步的，与 `startViewTransition` 不兼容）。改用带有显式 URL 的 `router.push()`。

### 类型和 Suspense

类型在导航期间可用，但在后续的 Suspense 揭示期间**不可用**（单独的过渡，无类型）。对页面级 enter/exit 使用类型映射；对 Suspense 揭示使用简单的字符串属性。

---

## 共享元素过渡

两个 VT 上的相同 `name` — 一个卸载，一个挂载 — 创建共享元素变形：

```jsx
<ViewTransition name="hero-image">
  <img src="/thumb.jpg" onClick={() => startTransition(() => onSelect())} />
</ViewTransition>

// 在另一个视图上 — 相同名称
<ViewTransition name="hero-image">
  <img src="/full.jpg" />
</ViewTransition>
```

- 一次只能挂载一个具有给定 `name` 的 VT — 使用唯一名称 (`photo-${id}`)。注意可重用组件：如果带有命名 VT 的组件同时在模态框/弹出框和页面中渲染，两者会同时挂载并破坏变形。要么使名称条件化（通过属性），要么将命名 VT 从共享组件移到特定消费者中。
- `share` 优先于 `enter`/`exit`。仔细考虑每个导航路径：当没有形成匹配对时（例如，目标页面没有相同的名称），`enter`/`exit` 会触发。考虑元素是否需要这些路径的回退动画。
- 永远不要在带有共享变形的页面上使用淡出退出 — 改用定向滑动。

---

## 常见模式

### 进入/退出

```jsx
{show && (
  <ViewTransition enter="fade-in" exit="fade-out"><Panel /></ViewTransition>
)}
```

### 列表重新排序

```jsx
{items.map(item => (
  <ViewTransition key={item.id}><ItemCard item={item} /></ViewTransition>
))}
```

在 `startTransition` 内部触发。避免在列表和 VT 之间使用包装 `<div>`。

### 组合共享元素和列表标识

共享元素和列表标识是独立的关注点 — 不要将它们混淆。当列表项包含共享元素时（例如，一个会变形为详情视图的图像），使用两个嵌套的 `<ViewTransition>` 边界：

```jsx
{items.map(item => (
  <ViewTransition key={item.id}>                                      {/* 列表标识 */}
    <Link href={`/items/${item.id}`}>
      <ViewTransition name={`item-image-${item.id}`} share="morph">   {/* 共享元素 */}
        <Image src={item.image} />
      </ViewTransition>
      <p>{item.name}</p>
    </Link>
  </ViewTransition>
))}
```

外部 VT 处理列表重新排序/进入动画。内部 VT 处理跨路由共享元素变形。缺少任何一层都意味着动画会静默不发生。

### 使用 `key` 强制重新进入

```jsx
<ViewTransition key={searchParams.toString()} enter="slide-up" default="none">
  <ResultsGrid />
</ViewTransition>
```

**注意：** 如果包装 `<Suspense>`，更改 `key` 会重新挂载边界并重新获取数据。

### 从 Suspense 回退到内容

简单的交叉淡入淡出：
```jsx
<ViewTransition>
  <Suspense fallback={<Skeleton />}><Content /></Suspense>
</ViewTransition>
```

定向揭示：
```jsx
<Suspense fallback={<ViewTransition exit="slide-down"><Skeleton /></ViewTransition>}>
  <ViewTransition enter="slide-up" default="none"><Content /></ViewTransition>
</Suspense>
```

有关更多模式，请参见 `references/patterns.md`。

---

## 多个 VT 如何交互

每个匹配触发器的 VT 在单个 `document.startViewTransition` 中同时触发。**不同**过渡中的 VT（导航与稍后的 Suspense 解析）不会竞争。

### 大量使用 `default="none"`

没有它，每个 VT 会在**每次**过渡时触发浏览器交叉淡入淡出 — Suspense 解析、`useDeferredValue` 更新、后台重新验证。始终使用 `default="none"` 并仅明确启用所需的触发器。

### 两种模式共存

**模式 A — 定向滑动：** 每个页面上的类型键控 VT，在导航期间触发。
**模式 B — Suspense 揭示：** 简单的字符串属性，在数据加载时触发（无类型）。

它们共存是因为它们在不同的时刻触发。两者都使用 `default="none"` 可防止交叉干扰。始终将 `enter` 与 `exit` 配对。将定向 VT 放在页面组件中，而不是布局中。

### 嵌套 VT 限制

当父 VT 退出时，其内部的嵌套 VT **不会**触发自己的 enter/exit — 只有最外层的 VT 会动画。页面导航期间的每项目交错动画目前不可能实现。有关实验性选择加入修复，请参见 [react#36135](https://github.com/facebook/react/pull/36135)。

---

## Next.js 集成

有关 Next.js 设置（`experimental.viewTransition` 标志、`next/link` 上的 `transitionTypes` 属性、App Router 模式、服务器组件），请参见 `references/nextjs.md`。

---

## 可访问性

始终将 `references/css-recipes.md` 中的减少运动 CSS 添加到全局样式表中。

---

## 参考文件

- **`references/implementation.md`** — 逐步实现工作流。
- **`references/patterns.md`** — 模式、动画时机、事件 API、故障排除。
- **`references/css-recipes.md`** — 即用型 CSS 动画配方。
- **`references/nextjs.md`** — Next.js App Router 模式和服务器组件详细信息。

## 完整编译文档

有关所有参考文件的完整指南：`AGENTS.md`