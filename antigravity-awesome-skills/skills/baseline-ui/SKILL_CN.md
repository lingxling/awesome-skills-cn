---
name: baseline-ui
description: 通过修复间距、层级、排版和小型布局问题来快速去除 UI 代码中的空话。当界面需要快速清理或抛光时使用。
risk: critical
source: https://github.com/ibelick/ui-skills/tree/main/skills/baseline-ui
source_repo: ibelick/ui-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/ibelick/ui-skills/blob/main/LICENSE
---

# 基准 UI

## 何时使用

当您需要通过修复间距、层级、排版和小型布局问题来快速去除 UI 代码中的空话时，请使用此技能。当界面需要快速清理或抛光时使用。

强制执行武断的 UI 基准以防止 AI 生成的界面空话。

## 如何使用

- `/baseline-ui`
  将这些约束应用于此对话中的任何 UI 工作。

- `/baseline-ui <file>`
  根据下面的所有约束审查文件并输出：
  - 违规项（引用确切的行/代码片段）
  - 为什么重要（1 个短句）
  - 具体修复（代码级建议）

## 技术栈

- 必须使用 Tailwind CSS 默认值，除非已存在自定义值或明确要求
- 需要 JavaScript 动画时必须使用 `motion/react`（以前是 `framer-motion`）
- 应该在 Tailwind CSS 中为进场和微动画使用 `tw-animate-css`
- 必须为类逻辑使用 `cn` 实用程序（`clsx` + `tailwind-merge`）

## 组件

- 对于具有键盘或焦点行为的任何内容，必须使用可访问的组件基元（`Base UI`、`React Aria`、`Radix`）
- 必须首先使用项目现有的组件基元
- 从不在同一交互表面中混合基元系统
- 如果与堆栈兼容，应该为新基元优先考虑 [`Base UI`](https://base-ui.com/react/components)
- 必须为仅图标按钮添加 `aria-label`
- 从不手动重建键盘或焦点行为，除非明确要求

## 交互

- 对于破坏性或不可逆的操作，必须使用 `AlertDialog`
- 应该为加载状态使用结构性骨架
- 从不使用 `h-screen`，使用 `h-dvh`
- 必须尊重固定元素的 `safe-area-inset`
- 必须在操作发生的地方显示错误
- 从不在 `input` 或 `textarea` 元素中阻止粘贴

## 动画

- 从不添加动画，除非明确要求
- 必须仅动画合成器属性（`transform`、`opacity`）
- 从不动画布局属性（`width`、`height`、`top`、`left`、`margin`、`padding`）
- 应该避免动画绘制属性（`background`、`color`），除非是小的、本地化的 UI（文本、图标）
- 应该在进场上使用 `ease-out`
- 从不超过 `200ms` 的交互反馈
- 必须在屏幕外暂停循环动画
- 应该尊重 `prefers-reduced-motion`
- 从不引入自定义缓动曲线，除非明确要求
- 应该避免动画大图像或全屏表面

## 排版

- 必须为标题使用 `text-balance`，为正文/段落使用 `text-pretty`
- 必须为数据使用 `tabular-nums`
- 应该为密集 UI 使用 `truncate` 或 `line-clamp`
- 从不修改 `letter-spacing`（`tracking-*`），除非明确要求

## 布局

- 必须使用固定的 `z-index` 刻度（无任意 `z-*`）
- 应该为方形元素使用 `size-*` 而不是 `w-*` + `h-*`

## 性能

- 从不在大 `blur()` 或 `backdrop-filter` 表面上动画
- 从不在活跃动画外应用 `will-change`
- 从不为可以表示为渲染逻辑的任何内容使用 `useEffect`

## 设计

- 从不使用渐变，除非明确要求
- 从不使用紫色或多色渐变
- 从不使用辉光效果作为主要可视化提示
- 应该使用 Tailwind CSS 默认阴影刻度，除非明确要求
- 必须为空状态提供一个明确的下一步操作
- 应该将重点颜色使用限制为每个视图一种
- 应该在引入新的主题之前使用现有主题或 Tailwind CSS 颜色令牌

## 示例

**用户请求：**

> 用 @baseline-ui 审查此界面，识别最高影响的设计问题，并提出实现就绪的改进。

## 限制

- 仅在任务明确符合其上游源和本地项目上下文时使用此技能。
- 在应用更改前验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例作为环境特定测试、安全审查或用户批准破坏性或成本高昂操作的替代品。
