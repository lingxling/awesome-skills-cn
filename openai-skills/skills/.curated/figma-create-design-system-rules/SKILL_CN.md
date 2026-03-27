---
name: figma-create-design-system-rules
description: 为用户的代码库生成自定义设计系统规则。当用户说 "create design system rules"、"generate rules for my project"、"set up design rules"、"customize design system guidelines" 或想要为 Figma 到代码的工作流程建立项目特定约定时使用。需要 Figma MCP 服务器连接。
---

# 创建设计系统规则

## 概述

此技能帮助您生成针对项目特定需求量身定制的自定义设计系统规则。这些规则指导 AI 编码代理在实现 Figma 设计时生成一致、高质量的代码，确保您团队的约定、组件模式和架构决策被自动遵循。

### 支持的规则文件

| 代理 | 规则文件 |
|-------|-----------|
| Claude Code | `CLAUDE.md` |
| Codex CLI | `AGENTS.md` |
| Cursor | `.cursor/rules/figma-design-system.mdc` |

## 什么是设计系统规则？

设计系统规则是项目级指令，编码了代码库的"不成文知识" — 经验丰富的开发人员知道并会传递给新团队成员的那种专业知识：

- 使用哪些布局原语和组件
- 组件文件应该位于何处
- 组件应该如何命名和结构化
- 什么不应该被硬编码
- 如何处理设计令牌和样式
- 项目特定的架构模式

一旦定义，这些规则大大减少了重复提示，并确保所有 Figma 实现任务的一致输出。

## 先决条件

- Figma MCP 服务器必须已连接并可访问
- 访问项目代码库以进行分析
- 了解您团队的组件约定（或愿意建立它们）

## 何时使用此技能

在以下情况下使用此技能：

- 启动将使用 Figma 设计的新项目
- 将 AI 编码代理引导到具有既定模式的现有项目
- 在整个团队中标准化 Figma 到代码的工作流程
- 更新或完善现有的设计系统约定
- 用户明确请求："create design system rules"、"set up Figma guidelines"、"customize rules for my project"

## 必需的工作流程

**按顺序执行这些步骤。不要跳过步骤。**

### 步骤 1：运行创建设计系统规则工具

调用 Figma MCP 服务器的 `create_design_system_rules` 工具以获取基础提示和模板。

**参数：**

- `clientLanguages`：项目中使用的语言的逗号分隔列表（例如，"typescript,javascript"、"python"、"javascript"）
- `clientFrameworks`：正在使用的框架（例如，"react"、"vue"、"svelte"、"angular"、"unknown"）

此工具返回创建设计系统规则的指导和模板。

按照工具响应中提供的模板格式构建您的设计系统规则。

### 步骤 2：分析代码库

在最终确定规则之前，分析项目以了解现有模式：

**组件组织：**

- UI 组件位于何处？（例如，`src/components/`、`app/ui/`、`lib/components/`）
- 是否有专用的设计系统目录？
- 组件如何组织？（按功能、按类型、扁平结构）

**样式方法：**

- 使用什么 CSS 框架或方法？（Tailwind、CSS Modules、styled-components 等）
- 设计令牌定义在何处？（CSS 变量、主题文件、配置文件）
- 是否有现有的颜色、排版或间距令牌？

**组件模式：**

- 使用什么命名约定？（PascalCase、kebab-case、前缀）
- 组件 props 通常如何结构化？
- 是否有常见的组合模式？

**架构决策：**

- 状态管理如何处理？
- 使用什么路由系统？
- 是否有特定的导入模式或路径别名？

### 步骤 3：生成项目特定规则

基于您的代码库分析，创建一套全面的规则。包括：

#### 通用组件规则

```markdown
- IMPORTANT: 尽可能使用来自 `[YOUR_PATH]` 的组件
- 将新的 UI 组件放在 `[COMPONENT_DIRECTORY]`
- 遵循 `[NAMING_CONVENTION]` 命名组件
- 组件必须导出为 `[EXPORT_PATTERN]`
```

#### 样式规则

```markdown
- 使用 `[CSS_FRAMEWORK/APPROACH]` 进行样式设置
- 设计令牌定义在 `[TOKEN_LOCATION]`
- IMPORTANT: 永远不要硬编码颜色 — 始终使用来自 `[TOKEN_FILE]` 的令牌
- 间距值必须使用 `[SPACING_SYSTEM]` 比例
- 排版遵循 `[TYPOGRAPHY_LOCATION]` 中定义的比例
```

#### Figma MCP 集成规则

```markdown
## Figma MCP 集成规则

这些规则定义了如何为此项目将 Figma 输入转换为代码，并且必须在每个 Figma 驱动的更改中遵循。

### 必需流程（不要跳过）

1. 首先运行 get_design_context 以获取确切节点的结构化表示
2. 如果响应太大或被截断，运行 get_metadata 以获取高级节点映射，然后仅使用 get_design_context 重新获取所需的节点
3. 运行 get_screenshot 以获取正在实现的节点变体的视觉参考
4. 只有在您同时拥有 get_design_context 和 get_screenshot 后，下载任何需要的资源并开始实现
5. 将输出（通常是 React + Tailwind）转换为此项目的约定、样式和框架
6. 在标记完成之前，针对 Figma 验证 1:1 的外观和行为

### 实现规则

- 将 Figma MCP 输出（React + Tailwind）视为设计和行为的表示，而不是最终代码样式
- 在适用时，用 `[YOUR_STYLING_APPROACH]` 替换 Tailwind 实用程序类
- 重用来自 `[COMPONENT_PATH]` 的现有组件，而不是重复功能
- 一致地使用项目的颜色系统、排版比例和间距令牌
- 尊重现有的路由、状态管理和数据获取模式
- 努力实现与 Figma 设计的 1:1 视觉一致性
- 针对 Figma 屏幕截图验证最终 UI，包括外观和行为
```

#### 资源处理规则

```markdown
## 资源处理

- Figma MCP 服务器提供一个资源端点，可以提供图像和 SVG 资源
- IMPORTANT: 如果 Figma MCP 服务器为图像或 SVG 返回 localhost 源，请直接使用该源
- IMPORTANT: 不要导入/添加新的图标包 — 所有资源都应在 Figma 有效负载中
- IMPORTANT: 如果提供了 localhost 源，不要使用或创建占位符
- 将下载的资源存储在 `[ASSET_DIRECTORY]`
```

#### 项目特定约定

```markdown
## 项目特定约定

- [添加任何独特的架构模式]
- [添加任何特殊的导入要求]
- [添加任何测试要求]
- [添加任何可访问性标准]
- [添加任何性能考虑]
```

### 步骤 4：将规则保存到适当的规则文件

检测用户正在使用哪个 AI 编码代理，并将生成的规则保存到相应的文件：

| 代理 | 规则文件 | 说明 |
|-------|-----------|-------|
| Claude Code | 项目根目录中的 `CLAUDE.md` | Markdown 格式。也可以使用 `.claude/rules/figma-design-system.md` 进行模块化组织。 |
| Codex CLI | 项目根目录中的 `AGENTS.md` | Markdown 格式。如果文件已存在，则作为新部分追加。32 KiB 组合大小限制。 |
| Cursor | `.cursor/rules/figma-design-system.mdc` | 带有 YAML 前置事项（`description`、`globs`、`alwaysApply`）的 Markdown。 |

如果不确定用户正在使用哪个代理，请检查项目中现有的规则文件或询问用户。

对于 Cursor，用 YAML 前置事项包装规则：

```markdown
---
description: 使用 Figma MCP 服务器实现 Figma 设计的规则。涵盖组件组织、样式约定、设计令牌、资源处理和必需的 Figma 到代码工作流程。
globs: "src/components/**"
alwaysApply: false
---

[此处为生成的规则]
```

自定义 `globs` 模式以匹配项目中 Figma 派生代码所在的目录（例如，`"src/**/*.tsx"` 或 `["src/components/**", "src/pages/**"]`）。

保存后，规则将由代理自动加载并应用于所有 Figma 实现任务。

### 步骤 5：验证和迭代

创建规则后：

1. 使用简单的 Figma 组件实现进行测试
2. 验证代理是否正确遵循规则
3. 完善任何未按预期工作的规则
4. 与团队成员分享以获取反馈
5. 随着项目的发展更新规则

## 规则类别和示例

### 基本规则（始终包括）

**组件发现：**

```markdown
- UI 组件位于 `src/components/ui/`
- 功能组件位于 `src/components/features/`
- 布局原语位于 `src/components/layout/`
```

**设计令牌使用：**

```markdown
- 颜色在 `src/styles/tokens.css` 中定义为 CSS 变量
- 永远不要硬编码十六进制颜色 — 使用 `var(--color-*)` 令牌
- 间距使用 4px 基本比例：`--space-1` (4px)、`--space-2` (8px) 等
```

**样式方法：**

```markdown
- 使用 Tailwind 实用程序类进行样式设置
- 自定义样式放在组件级 CSS 模块中
- 主题自定义在 `tailwind.config.js` 中
```

### 推荐规则（非常有价值）

**组件模式：**

```markdown
- 所有组件必须接受用于组合的 `className` prop
- 变体 props 应该使用联合类型：`variant: 'primary' | 'secondary'`
- 图标组件应该接受 `size` 和 `color` props
```

**导入约定：**

```markdown
- 使用路径别名：`@/components`、`@/styles`、`@/utils`
- 分组导入：React、第三方、内部、类型
- 没有超出父目录的相对导入
```

**代码质量：**

```markdown
- 为导出的组件添加 JSDoc 注释
- 为所有 props 包括 PropTypes 或 TypeScript 类型
- 将幻数提取到命名常量
```

### 可选规则（项目特定）

**可访问性：**

```markdown
- 所有交互元素必须具有 aria-labels
- 颜色对比度必须符合 WCAG AA 标准
- 所有交互都需要键盘导航
```

**性能：**

```markdown
- 使用 `@/components/Image` 中的 `Image` 组件延迟加载图像
- 对接收复杂 props 的组件使用 React.memo
- 图标应该是 SVG 组件，而不是图标字体
```

**测试：**

```markdown
- 在 `__tests__/` 目录中包括新组件的单元测试
- 使用 Testing Library 查询（getByRole、getByLabelText）
- 测试所有交互状态和变体
```

## 示例

### 示例 1：React + Tailwind 项目

用户说："为我的 React 项目创建设计系统规则"

**操作：**

1. 运行 `create_design_system_rules(clientLanguages="typescript,javascript", clientFrameworks="react")`
2. 分析代码库结构
3. 生成规则：

```markdown
# Figma MCP 集成规则

## 组件组织

- UI 组件位于 `src/components/ui/`
- 页面组件位于 `src/app/`
- 使用 Tailwind 进行样式设置

## Figma 实现流程

1. 为节点运行 get_design_context
2. 运行 get_screenshot 以获取视觉参考
3. 将 Figma 颜色映射到 `tailwind.config.js` 中定义的 Tailwind 颜色
4. 尽可能重用来自 `src/components/ui/` 的组件
5. 在完成之前针对屏幕截图进行验证

## 样式规则

- IMPORTANT: 使用 Tailwind 实用程序类，而不是内联样式
- 颜色在 `tailwind.config.js` theme.colors 中定义
- 间距使用 Tailwind 的默认比例
- 自定义组件放在 `src/components/ui/`

## 资源规则

- IMPORTANT: 直接使用来自 Figma MCP 服务器的 localhost 源
- 将静态资源存储在 `public/assets/`
- 不要安装新的图标库
```

4. 保存到用户代理的适当规则文件
5. 使用简单的按钮实现进行测试

**结果：** 代理现在在实现 Figma 设计时始终遵循项目的约定。

### 示例 2：Vue + 自定义 CSS 项目

用户说："为我的 Vue 应用设置 Figma 规则"

**操作：**

1. 运行 `create_design_system_rules(clientLanguages="typescript,javascript", clientFrameworks="vue")`
2. 发现项目使用 CSS 模块和自定义设计令牌系统
3. 生成规则：

```markdown
# Figma MCP 集成规则

## 组件组织

- 组件位于 `src/components/`
- 可组合项位于 `src/composables/`
- Vue SFC 结构：<script setup>、<template>、<style scoped>

## 设计令牌

- IMPORTANT: 所有颜色在 `src/styles/tokens.css` 中定义为 CSS 变量
- 使用 `var(--color-primary)`、`var(--color-secondary)` 等
- 间距：`var(--space-xs)` 到 `var(--space-xl)`
- 排版：`var(--text-sm)` 到 `var(--text-2xl)`

## Figma 实现流程

1. 运行 get_design_context 和 get_screenshot
2. 将 React 输出转换为 Vue 3 Composition API
3. 将 Figma 颜色映射到 `src/styles/tokens.css` 中的 CSS 变量
4. 对组件样式使用 CSS 模块
5. 在创建新组件之前检查 `src/components/` 中的现有组件

## 样式规则

- 使用 CSS 模块（`.module.css` 文件）
- IMPORTANT: 引用设计令牌，永远不要硬编码值
- 使用 CSS 模块的 Scoped 样式
```

4. 保存到用户代理的适当规则文件
5. 使用卡片组件进行验证

**结果：** 代理现在正确地将 Figma 设计转换为使用项目设计令牌系统的 Vue 组件。

### 示例 3：设计系统团队

用户说："为我们的设计系统库生成规则"

**操作：**

1. 运行 `create_design_system_rules(clientLanguages="typescript", clientFrameworks="react")`
2. 分析具有设计系统包的 monorepo 结构
3. 生成全面的规则：

```markdown
# 设计系统规则

## 仓库结构

- 设计系统组件：`packages/design-system/src/components/`
- 文档：`packages/docs/`
- 设计令牌：`packages/tokens/src/`

## 组件开发

- IMPORTANT: 所有组件必须位于 `packages/design-system/src/components/`
- 组件文件结构：`ComponentName/index.tsx`、`ComponentName.stories.tsx`、`ComponentName.test.tsx`
- 从 `packages/design-system/src/index.ts` 导出所有组件

## 设计令牌

- 颜色：`packages/tokens/src/colors.ts`
- 排版：`packages/tokens/src/typography.ts`
- 间距：`packages/tokens/src/spacing.ts`
- IMPORTANT: 永远不要硬编码值 — 从令牌包导入

## 文档要求

- 为每个组件添加 Storybook 故事
- 包括带有 @example 的 JSDoc
- 用描述记录所有 props
- 添加可访问性注释

## Figma 集成

1. 从 Figma 获取设计上下文和屏幕截图
2. 将 Figma 令牌映射到设计系统令牌
3. 在设计系统包中创建或扩展组件
4. 添加显示所有变体的 Storybook 故事
5. 针对 Figma 屏幕截图进行验证
6. 更新文档
```

4. 保存到适当的规则文件并与团队分享
5. 添加到团队文档

**结果：** 整个团队在将组件从 Figma 添加到设计系统时遵循一致的模式。

## 最佳实践

### 从简单开始，迭代

不要试图预先捕获每条规则。从最重要的约定开始，随着遇到不一致而添加规则。

### 具体明确

而不是："使用设计系统"
写："始终使用来自 `src/components/ui/Button.tsx` 的 Button 组件，并带有 variant prop ('primary' | 'secondary' | 'ghost')"

### 使规则可操作

每条规则都应该告诉代理确切该做什么，而不是只避免什么。

好："颜色在 `src/theme/colors.ts` 中定义 — 导入并使用这些常量"
坏："不要硬编码颜色"

### 对关键规则使用 IMPORTANT

用 "IMPORTANT:" 前缀必须永远不会违反的规则，以确保代理优先考虑它们。

```markdown
- IMPORTANT: 永远不要在客户端代码中暴露 API 密钥
- IMPORTANT: 始终在渲染之前清理用户输入
```

### 记录原因

当规则看起来随意时，解释推理：

```markdown
- 将所有数据获取放在服务器组件中（减少客户端包大小并提高性能）
- 使用带有 `@/` 别名的绝对导入（使重构更容易并防止破坏相对路径）
```

## 常见问题及解决方案

### 问题：代理没有遵循规则

**原因：** 规则可能太模糊或没有被代理正确加载。
**解决方案：**

- 使规则更具体和可操作
- 验证规则是否保存在正确的配置文件中
- 重新启动代理或 IDE 以重新加载规则
- 为关键规则添加 "IMPORTANT:" 前缀

### 问题：规则相互冲突

**原因：** 矛盾或重叠的规则。
**解决方案：**

- 审查所有规则以查找冲突
- 建立清晰的优先级层次结构
- 删除冗余规则
- 将相关规则合并为单一、清晰的陈述

### 问题：太多规则增加延迟

**原因：** 过多的规则会增加上下文大小和处理时间。
**解决方案：**

- 专注于解决 80% 一致性问题的 20% 规则
- 删除很少适用的过于具体的规则
- 合并相关规则
- 使用渐进式披露（首先基本规则，链接文件中的高级规则）

### 问题：随着项目的发展，规则变得过时

**原因：** 代码库更改但规则没有。
**解决方案：**

- 安排定期规则审查（每月或每季度）
- 架构决策更改时更新规则
- 对规则文件进行版本控制
- 在提交消息中记录规则更改

## 了解设计系统规则

设计系统规则改变了 AI 编码代理处理您的 Figma 设计的方式：

**规则之前：**

- 代理对组件结构做出假设
- 跨实现的不一致样式方法
- 与设计令牌不匹配的硬编码值
- 在随机位置创建的组件
- 项目约定的重复解释

**规则之后：**

- 代理自动遵循您的约定
- 一致的组件结构和样式
- 从一开始就正确使用设计令牌
- 组件正确组织
- 零重复提示

投资于创建良好规则的时间在每个 Figma 实现任务中都会得到指数级的回报。

## 其他资源

- [Figma MCP 服务器文档](https://developers.figma.com/docs/figma-mcp-server/)
- [Figma 变量和设计令牌](https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma)
