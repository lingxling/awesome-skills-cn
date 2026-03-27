---
name: "figma-implement-design"
description: "将 Figma 设计转换为生产就绪的应用代码，实现 1:1 的视觉保真度。当实现来自 Figma 文件的 UI 代码时使用，当用户提到 \"实现设计\"、\"生成代码\"、\"实现组件\"，提供 Figma URL，或要求构建与 Figma 规范匹配的组件时使用。对于通过 `use_figma` 进行的 Figma 画布写入，使用 `figma-use`。"
---

# 实现设计

## 概述

此技能为将 Figma 设计转换为生产就绪的代码提供了结构化的工作流程，确保与 Figma MCP 服务器的一致集成、正确使用设计令牌以及与设计 1:1 的视觉保真度。

## 技能边界

- 当交付物是用户仓库中的代码时，使用此技能。
- 如果用户要求在 Figma 中创建/编辑/删除节点，切换到 [figma-use](../figma-use/SKILL.md)。
- 如果用户要求从代码或描述在 Figma 中构建或更新整页屏幕，切换到 [figma-generate-design](../figma-generate-design/SKILL.md)。
- 如果用户仅要求 Code Connect 映射，切换到 [figma-code-connect-components](../figma-code-connect-components/SKILL.md)。
- 如果用户要求编写可重用的代理规则 (`CLAUDE.md`/`AGENTS.md`)，切换到 [figma-create-design-system-rules](../figma-create-design-system-rules/SKILL.md)。

## 前置条件

- Figma MCP 服务器必须已连接并可访问
- 用户必须以以下格式提供 Figma URL：`https://figma.com/design/:fileKey/:fileName?node-id=1-2`
  - `:fileKey` 是文件键（`/design/` 之后的段）
  - `1-2` 是节点 ID（要实现的特定组件或帧的值）
- **或者** 当使用 `figma-desktop` MCP 时：用户可以直接在 Figma 桌面应用中选择一个节点（不需要 URL）
- 项目应该已建立的设计系统或组件库（首选）

## 必需工作流程

**按顺序遵循这些步骤。不要跳过步骤。**

### 步骤 1：获取节点 ID

#### 选项 A：从 Figma URL 解析

当用户提供 Figma URL 时，提取文件键和节点 ID 以作为参数传递给 MCP 工具。

**URL 格式：** `https://figma.com/design/:fileKey/:fileName?node-id=1-2`

**提取：**
- **文件键：** `:fileKey`（`/design/` 之后的段）
- **节点 ID：** `1-2`（`node-id` 查询参数的值）

**注意：** 当使用本地桌面 MCP（`figma-desktop`）时，`fileKey` 不会作为参数传递给工具调用。服务器自动使用当前打开的文件，因此只需要 `nodeId`。

**示例：**
- URL: `https://figma.com/design/kL9xQn2VwM8pYrTb4ZcHjF/DesignSystem?node-id=42-15`
- 文件键: `kL9xQn2VwM8pYrTb4ZcHjF`
- 节点 ID: `42-15`

#### 选项 B：使用来自 Figma 桌面应用的当前选择（仅限 figma-desktop MCP）

当使用 `figma-desktop` MCP 且用户未提供 Figma URL 时，工具会自动使用在 Figma 桌面应用中当前选择的节点。

**注意：** 基于选择的提示仅适用于 `figma-desktop` MCP 服务器。远程服务器需要指向帧或图层的链接才能提取上下文。用户必须在 Figma 桌面应用中打开一个节点并选中它。

### 步骤 2：获取设计上下文

使用提取的文件键和节点 ID 运行 `get_design_context`。

```
get_design_context(fileKey=":fileKey", nodeId="1-2")
```

这提供了包括以下内容的结构化数据：

**布局属性：**
- 自动布局
- 约束
- 尺寸

**排版规范：**
- 字体规格
- 字重
- 行高
- 字母间距

**颜色值和设计令牌：**
- 主要颜色
- 次要颜色
- 背景色
- 文本色
- 边框颜色
- 阴影颜色
- 渐变

**组件结构和变体：**
- 组件名称
- 变体名称
- 层级结构
- 子节点 ID

**间距和填充值：**
- 内边距
- 外边距
- 填充
- 间隙

**如果响应太大或被截断：**

1. 运行 `get_metadata(fileKey=":fileKey", nodeId="1-2")` 获取高级节点映射。
2. 从元数据中识别特定的子节点。
3. 使用 `get_design_context(fileKey=":fileKey", nodeId="childNodeId")` 单独获取每个主要子节点。

### 步骤 3：捕获视觉参考

使用相同的文件键和节点 ID 运行 `get_screenshot`。

```
get_screenshot(fileKey=":fileKey", nodeId="1-2")
```

此截图作为视觉验证的真相来源。在整个实现过程中保持其可访问性。

### 步骤 4：下载所需资产

从 Figma MCP 服务器返回的任何资产（图像、图标、SVG）。

**重要：** 遵循这些资产规则：

- 如果 Figma MCP 服务器为图像或 SVG 返回 `localhost` 源，请直接使用该源。
- **不要导入或添加新的图标包** - 所有资产应来自 Figma 负载。
- **如果提供了 `localhost` 源，不要使用或创建占位符。**
- 资产通过 Figma MCP 服务器的内置资产端点提供。

### 步骤 5：转换到项目约定

将 Figma 输出（通常是 React + Tailwind）转换为此项目的框架、样式和约定。

**关键原则：**

- 将 Figma MCP 输出（通常是 React + Tailwind）视为设计和行为的表示，而不是最终代码样式。
- 在适用时，用项目首选的工具/设计系统令牌替换 Tailwind 实用类。
- 重用现有组件（例如，按钮、输入、排版、图标包装器），而不是重复功能。
- 一致地使用项目的颜色系统、排版比例和间距令牌。
- 尊重项目已采用的路由、状态管理和数据获取模式。

### 步骤 6：实现 1:1 视觉保真度

努力实现像素完美的视觉保真度。

**指南：**
- 优先考虑 Figma 保真度以完全匹配设计。
- 避免硬编码值 - 尽可能从 Figma 提取设计令牌。
- 当出现冲突时，优先考虑设计系统令牌但最小化调整间距或大小以匹配视觉效果。
- 遵循 WCAG 可访问性要求。
- 根据需要添加组件文档。

### 步骤 7：针对 Figma 进行验证

在标记完成之前，将最终 UI 针对 Figma 截图进行验证。

**验证检查清单：**

- [ ] 布局匹配（间距、对齐、尺寸）
- [ ] 排版匹配（字体、大小、行高）
- [ ] 颜色完全匹配
- [ ] 交互状态按设计工作（悬停、活动、禁用）
- [ ] 响应式行为遵循 Figma 约束
- [ ] 资产正确渲染
- [ ] 满足可访问性标准

## 实现规则

### 组件组织

- 将 UI 组件放在项目指定的设计系统目录中
- 遵循项目的组件命名约定
- 除非真正需要动态值，否则避免内联样式

### 设计系统集成

- 始终在可能时使用项目设计系统中的组件
- 将 Figma 设计令牌映射到项目设计令牌
- 当存在匹配组件时，扩展它而不是创建新组件
- 记录添加到设计系统的任何新组件

### 代码质量

- 避免硬编码值 - 提取到常量或设计令牌
- 保持组件可组合和可重用
- 为组件 props 添加 TypeScript 类型
- 为导出的组件包含 JSDoc 注释

## 示例

### 示例 1：实现按钮组件

用户说："实现此 Figma 按钮组件：https://figma.com/design/kL9xQn2VwM8pYrTb4ZcHjF/DesignSystem?node-id=42-15"

**操作：**

1. 解析 URL 以提取文件键=`kL9xQn2VwM8pYrTb4ZcHjF` 和节点 ID=`42-15`
2. 运行 `get_design_context(fileKey="kL9xQn2VwM8pYrTb4ZcHjF", nodeId="42-15")`
3. 运行 `get_screenshot(fileKey="kL9xQn2VwM8pYrTb4ZcHjF", nodeId="42-15")` 以获取视觉参考
4. 从资产端点下载任何按钮图标
5. 检查项目是否有现有的按钮组件
6. 如果有，使用新变体扩展它；如果没有，使用项目约定创建新组件
7. 将 Figma 颜色映射到项目设计令牌（例如，`primary-500`、`primary-hover`）
8. 针对截图验证填充、边框半径、排版

**结果：** 与 Figma 设计匹配的按钮组件，集成到项目设计系统。

### 示例 2：构建仪表板布局

用户说："构建此仪表板：https://figma.com/design/pR8mNv5KqXzGwY2JtCfL4D/Dashboard?node-id=10-5"

**操作：**

1. 解析 URL 以提取文件键=`pR8mNv5KqXzGwY2JtCfL4D` 和节点 ID=`10-5`
2. 运行 `get_metadata(fileKey="pR8mNv5KqXzGwY2JtCfL4D", nodeId="10-5")` 以了解页面结构
3. 从元数据中识别主要部分（页眉、侧边栏、内容区域、卡片）及其子节点 ID
4. 为每个主要部分运行 `get_design_context(fileKey="pR8mNv5KqXzGwY2JtCfL4D", nodeId=":childNodeId")`
5. 运行 `get_screenshot(fileKey="pR8mNv5KqXzGwY2JtCfL4D", nodeId="10-5")` 获取完整页面
6. 下载所有资产（徽标、图标、图表）
7. 使用项目的布局原语构建布局
8. 在可能的情况下使用现有组件实现每个部分
9. 针对 Figma 约束验证响应式行为

**结果：** 完全匹配 Figma 设计的响应式仪表板。

## 最佳实践

### 始终从上下文开始

永远不要基于假设进行实现。始终首先获取 `get_design_context` 和 `get_screenshot`。

### 增量验证

在实现过程中频繁验证，而不仅仅在最后。这可以尽早发现问题。

### 文档偏差

如果您必须偏离 Figma 设计（例如，为了可访问性或技术约束），在代码注释中说明原因。

### 重用而非重新创建

始终检查现有组件，然后再创建新的。代码库的一致性比精确的 Figma 复制更重要。

### 设计系统优先

当有疑问时，优先考虑项目的设计系统模式而不是字面翻译 Figma 设计。

## 常见问题和解决方案

### 问题：Figma 输出被截断

**原因：** 设计太复杂或嵌套层数太多，无法在单个响应中返回。

**解决方案：** 使用 `get_metadata` 获取节点结构，然后使用 `get_design_context` 单独获取特定子节点。

### 问题：实现后设计与 Figma 不匹配

**原因：** 实现代码与原始 Figma 设计之间的视觉差异。

**解决方案：** 与步骤 3 的截图并排比较。检查间距、颜色和排版值是否在设计上下文数据中。

### 问题：资产未加载

**原因：** Figma MCP 服务器的资产端点不可访问或 URL 被修改。

**解决方案：** 验证 Figma MCP 服务器的资产端点是否可访问。服务器在 `localhost` URL 上提供资产。直接使用这些，不要修改。

### 问题：设计令牌值与 Figma 不同

**原因：** 项目的设计令牌与 Figma 设计中指定的值不同。

**解决方案：** 当项目令牌与 Figma 值不同时，优先考虑项目令牌以保持一致性，但调整间距或大小以最小化匹配视觉效果。

## 理解设计实现

Figma 实现工作流程建立了将设计转换为代码的可靠过程：

**对于设计师：** 确保实现将与他们的设计匹配，具有像素完美的准确性。
**对于开发者：** 结构化的方法消除了猜测工作并减少了来回修改。
**对于团队：** 一致的、高质量的实现，保持设计系统完整性。

通过遵循此工作流程，您确保每个 Figma 设计都以相同的关怀和对细节的关注来实现。

## 其他资源

- [Figma MCP 服务器文档](https://developers.figma.com/docs/figma-mcp-server/)
- [Figma MCP 服务器工具和提示](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/)
- [Figma 变量和设计令牌](https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma)
