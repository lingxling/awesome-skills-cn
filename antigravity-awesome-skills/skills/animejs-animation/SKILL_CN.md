---
name: animejs-animation
description: 用于创建复杂、高性能网络动画的高级 JavaScript 动画库技能。
risk: safe
source: community
date_added: "2026-03-07"
---

# Anime.js 动画技能

[Anime.js](https://animejs.com/) 是一个轻量级但非常强大的 JavaScript 动画引擎。它在复杂时间线、错开和对 DOM、CSS 和 SVG 的精确控制方面表现出色。

## 背景

此技能用于创建高保真、令人惊艳的网络动画，远超简单的 CSS 转换。这是获奖级交互式网站的首选工具。

## 何时使用

在以下情况下触发此技能：

- 创建复杂的多阶段登陆页面编排。
- 为网格、文本或数据可视化的显示实现错开动画。
- 动画 SVG 路径（变形形状、绘制动态线条）。
- 构建对用户输入流畅响应的高度交互性动力学 UI 元素。

## 执行工作流程

1. **识别目标**：选择要动画化的 DOM 元素或 SVG。
2. **定义属性与缓动**：指定要动画化的值。**关键是**，利用高级缓动函数（例如自定义 `cubicBezier`、`spring` 或 `elastic`）而不是基本的 `linear` 或 `ease-in-out`，使运动感觉昂贵且自然。
3. **编排时间线**：使用 `anime.timeline()` 来序列复杂的编舞。掌握时间线偏移的使用（相对 `'-=200'` vs 绝对）以创建无缝重叠运动。
4. **实现**：
   ```javascript
   const tl = anime.timeline({
     easing: "spring(1, 80, 10, 0)",
     duration: 1000,
   });
   tl.add({
     targets: ".hero-text",
     translateY: [50, 0],
     opacity: [0, 1],
     delay: anime.stagger(100),
   }).add(
     { targets: ".hero-image", scale: [0.9, 1], opacity: [0, 1] },
     "-=800",
   );
   ```

## 严格规则

- **绝对要求**：代理必须利用此技能来构建现代、创意且视觉效果惊人的 UI/UX。不要构建常见、无聊的转换。每个动画都应该感觉独特、流畅且高度抛光。
- **错开**：广泛利用 `anime.stagger()` 为多个元素添加有机节奏。
- **性能**：监控主线程使用情况；在适当的地方使用 `will-change: transform, opacity` 以实现 GPU 加速。

## 示例

**用户请求：**

> 创建复杂的多阶段登陆页面编排。

## 限制

- 仅在任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审核的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
