---
name: figma-use
description: "**强制先决条件** — 在每次调用 `use_figma` 工具之前，您必须调用此技能。切勿在未先加载此技能的情况下直接调用 `use_figma`。跳过它会导致常见且难以调试的失败。当用户想要在 Figma 文件上下文中执行写入操作或需要 JavaScript 执行的独特读取操作时触发 — 例如，创建/编辑/删除节点、设置变量或令牌、构建组件和变体、修改自动布局或填充、将变量绑定到属性，或以编程方式检查文件结构。"
---

# use_figma — Figma 插件 API 技能

使用 `use_figma` MCP 通过插件 API 在 Figma 文件中执行 JavaScript。所有详细的参考文档都位于 `references/` 中。

**在调用 `use_figma` 时，始终传递 `skillNames: "figma-use"`。** 这是一个用于跟踪技能使用情况的日志记录参数 — 它不会影响执行。

**如果任务涉及从代码在 Figma 中构建或更新完整页面、屏幕或多部分布局**，还要加载 [figma-generate-design](../figma-generate-design/SKILL.md)。它提供了通过 `search_design_system` 发现设计系统组件、导入它们并逐步组装屏幕的工作流程。这两种技能协同工作：这一种用于 API 规则，那一种用于屏幕构建工作流程。

首先，加载 [plugin-api-standalone.index.md](references/plugin-api-standalone.index.md) 以了解什么是可能的。当您被要求编写插件 API 代码时，使用此上下文在 [plugin-api-standalone.d.ts](references/plugin-api-standalone.d.ts) 中搜索相关类型、方法和属性。这是 API 表面的最终事实来源。它是一个大型类型文件，因此不要一次加载全部，根据需要搜索相关部分。

重要：每当您使用设计系统时，从 [working-with-design-systems/wwds.md](references/working-with-design-systems/wwds.md) 开始，以了解在 Figma 中使用设计系统的关键概念、流程和指南。然后根据需要加载更具体的参考文档，包括组件、变量、文本样式和效果样式。

## 1. 关键规则

1.  **使用 `return` 发送数据。** 返回值会自动 JSON 序列化（对象、数组、字符串、数字）。不要调用 `figma.closePlugin()` 或将代码包装在异步 IIFE 中 — 这会为您处理。
2.  **编写带有顶层 `await` 和 `return` 的普通 JavaScript。** 代码会自动包装在异步上下文中。不要包装在 `(async () => { ... })()` 中。
3.  `figma.notify()` **抛出 "未实现"** — 永远不要使用它
3a. `getPluginData()` / `setPluginData()` 在 `use_figma` 中**不受支持** — 不要使用它们。改用 `getSharedPluginData()` / `setSharedPluginData()`（这些是受支持的），或者通过返回它们来跟踪节点 ID，并将它们传递给后续调用。
4.  `console.log()` 不会返回 — 使用 `return` 输出
5.  **以小步骤增量工作。** 将大型操作分解为多个 `use_figma` 调用。在每一步之后验证。这是避免错误的最重要的实践。
6.  颜色是 **0–1 范围**（不是 0–255）：`{r: 1, g: 0, b: 0}` = 红色
7.  填充/描边是**只读数组** — 克隆、修改、重新赋值
8.  字体**必须**在任何文本操作之前加载：`await figma.loadFontAsync({family, style})`
9.  **页面增量加载** — 使用 `await figma.setCurrentPageAsync(page)` 切换页面并加载其内容（请参阅下面的页面规则）
10. `setBoundVariableForPaint` 返回一个**新的** paint — 必须捕获并重新赋值
11. `createVariable` 接受集合**对象或 ID 字符串**（首选对象）
12. **`layoutSizingHorizontal/Vertical = 'FILL'` 必须在 `parent.appendChild(child)` 之后设置** — 在 append 之前设置会抛出错误。这也适用于非自动布局节点上的 `'HUG'`。
13. **将新的顶级节点定位在远离 (0,0) 的位置。** 直接附加到页面的节点默认为 (0,0)。扫描 `figma.currentPage.children` 以找到清晰的位置（例如，在最右侧节点的右侧）。这仅适用于页面级节点 — 嵌套在其他框架或自动布局容器中的节点由其父级定位。请参阅 [陷阱](references/gotchas.md)。
14. **在 `use_figma` 错误时，停止。不要立即重试。** 失败的脚本是**原子的** — 如果脚本出错，它根本不会执行，也不会对文件进行任何更改。仔细阅读错误消息，修复脚本，然后重试。请参阅 [错误恢复](#6-error-recovery--self-correction)。
15. **必须 `return` 所有创建/变异的节点 ID。** 每当脚本在画布上创建新节点或变异现有节点时，收集每个受影响的节点 ID 并以结构化对象返回（例如 `return { createdNodeIds: [...], mutatedNodeIds: [...] }`）。这对于后续调用引用、验证或清理这些节点至关重要。
16. **创建变量时始终显式设置 `variable.scopes`。** 默认的 `ALL_SCOPES` 会污染每个属性选择器 — 几乎永远不是您想要的。对背景使用特定范围，如 `["FRAME_FILL", "SHAPE_FILL"]`，对文本颜色使用 `["TEXT_FILL"]`，对间距使用 `["GAP"]` 等。请参阅 [variable-patterns.md](references/variable-patterns.md) 获取完整列表。
17. **`await` 每个 Promise。** 永远不要留下未等待的 Promise — 未等待的异步调用（例如，没有 `await` 的 `figma.loadFontAsync(...)`，或没有 `await` 的 `figma.setCurrentPageAsync(page)`）会触发并忘记，导致静默失败或竞争条件。脚本可能在异步操作完成之前返回，导致数据丢失或更改部分应用。

> 有关每个规则的详细错误/正确示例，请参阅 [陷阱和常见错误](references/gotchas.md)。

## 2. 页面规则（关键）

**页面上下文在 `use_figma` 调用之间重置** — `figma.currentPage` 在每次开始时都位于第一页。

### 切换页面

使用 `await figma.setCurrentPageAsync(page)` 切换页面并加载其内容。同步设置器 `figma.currentPage = page` 在 `use_figma` 运行时中会**抛出错误**。

```js
// 切换到特定页面（加载其内容）
const targetPage = figma.root.children.find((p) => p.name === "我的页面");
await figma.setCurrentPageAsync(targetPage);
// targetPage.children 现在已填充

// 遍历所有页面
for (const page of figma.root.children) {
  await figma.setCurrentPageAsync(page);
  // page.children 现在已加载 — 在此处读取或修改它们
}
```

### 跨脚本运行

`figma.currentPage` 在每次 `use_figma` 调用开始时重置为**第一页**。如果您的工作流程跨越多个调用并针对非默认页面，请在每次调用开始时调用 `await figma.setCurrentPageAsync(page)`。

您可以多次调用 `use_figma` 以增量方式构建文件状态，或在编写另一个脚本之前检索信息。例如，编写一个脚本以获取有关现有节点的元数据，`return` 该数据，然后在后续脚本中使用它来修改这些节点。

## 3. `return` 是您的输出通道

代理只看到您 `return` 的值。其他一切都是不可见的。

- **返回 ID（关键）**：每个创建或变异画布节点的脚本**必须**返回所有受影响的节点 ID — 例如 `return { createdNodeIds: [...], mutatedNodeIds: [...] }`。这是一个硬性要求，不是可选的。
- **进度报告**：`return { createdNodeIds: [...], count: 5, errors: [] }`
- **错误信息**：抛出的错误会自动捕获并返回 — 只需让它们传播或显式 `throw`。
- `console.log()` 输出**永远不会**返回给代理
- 始终返回可操作的数据（ID、计数、状态），以便后续调用可以引用创建的对象

## 4. 编辑器模式

`use_figma` 在**设计模式**（editorType `"figma"`，默认）下工作。FigJam (`"figjam"`) 有一组不同的可用节点类型 — 大多数设计节点在那里被阻止。

设计模式下可用：Rectangle, Frame, Component, Text, Ellipse, Star, Line, Vector, Polygon, BooleanOperation, Slice, Page, Section, TextPath。

在设计模式下**被阻止**：Sticky, Connector, ShapeWithText, CodeBlock, Slide, SlideRow, Webpage。

## 5. 增量工作流程（如何避免错误）

错误最常见的原因是试图在单个 `use_figma` 调用中做太多事情。**以小步骤工作，并在每一步之后验证。**

### 模式

1. **首先检查。** 在创建任何内容之前，运行一个只读的 `use_figma` 以发现文件中已存在的内容 — 页面、组件、变量、命名约定。匹配那里的内容。
2. **每次调用做一件事。** 在一个调用中创建变量，在下一个调用中创建组件，在另一个调用中组合布局。不要试图在一个脚本中构建整个屏幕。
3. **从每次调用返回 ID。** 始终 `return` 创建的节点 ID、变量 ID、集合 ID 作为对象（例如 `return { createdNodeIds: [...] }`）。您需要这些作为后续调用的输入。
4. **在每一步之后验证。** 使用 `get_metadata` 验证结构（计数、名称、层次结构、位置）。在主要里程碑之后使用 `get_screenshot` 捕获视觉问题。
5. **在继续之前修复。** 如果验证揭示了一个问题，请在进入下一步之前修复它。不要在破损的基础上构建。

### 复杂任务的建议步骤顺序

```
步骤 1：检查文件 — 发现现有页面、组件、变量、约定
步骤 2：创建令牌/变量（如果需要）
       → 使用 get_metadata 验证
步骤 3：创建单个组件
       → 使用 get_metadata + get_screenshot 验证
步骤 4：从组件实例组合布局
       → 使用 get_screenshot 验证
步骤 5：最终验证
```

### 在每一步验证什么

| 在...之后 | 使用 `get_metadata` 检查 | 使用 `get_screenshot` 检查 |
|---|---|---|
| 创建变量 | 集合计数、变量计数、模式名称 | — |
| 创建组件 | 子计数、变体名称、属性定义 | 变体可见、未折叠、网格可读 |
| 绑定变量 | 节点属性反映绑定 | 颜色/令牌正确解析 |
| 组合布局 | 实例节点具有 mainComponent，层次结构正确 | 无裁剪/截断文本，无重叠元素，间距正确 |

## 6. 错误恢复和自我纠正

**`use_figma` 是原子的 — 失败的脚本不会执行。** 如果脚本出错，不会对文件进行任何更改。文件保持与调用之前相同的状态。这意味着失败的脚本不会产生部分节点，不会产生孤立元素，修复后重试是安全的。

### 当 `use_figma` 返回错误时

1. **停止。** 不要立即修复代码并重试。
2. **仔细阅读错误消息。** 准确理解出了什么问题 — 错误的 API 使用、缺少字体、无效的属性值等。
3. **如果错误不清楚**，调用 `get_metadata` 或 `get_screenshot` 以了解当前文件状态。
4. **根据错误消息修复脚本**。
5. **重试**更正后的脚本。

### 常见的自我纠正模式

| 错误消息 | 可能的原因 | 如何修复 |
|---|---|---|
| `"not implemented"` | 使用了 `figma.notify()` | 移除它 — 使用 `return` 输出 |
| `"node must be an auto-layout frame..."` | 在附加到自动布局父级之前设置了 `FILL`/`HUG` | 在 `layoutSizingX = 'FILL'` 之前移动 `appendChild` |
| `"Setting figma.currentPage is not supported"` | 使用了同步页面设置器 | 使用 `await figma.setCurrentPageAsync(page)` |
| 属性值超出范围 | 颜色通道 > 1（使用了 0–255 而不是 0–1） | 除以 255 |
| `"Cannot read properties of null"` | 节点不存在（错误的 ID，错误的页面） | 检查页面上下文，验证 ID |
| 脚本挂起 / 无响应 | 无限循环或未解决的 promise | 检查 `while(true)` 或缺少 `await`；确保代码终止 |
| `"The node with id X does not exist"` | 父实例被隐式分离，子 `detachInstance()` 更改了 ID | 通过从稳定（非实例）父框架遍历来重新发现节点 |

### 当脚本成功但结果看起来错误时

1. 调用 `get_metadata` 检查结构正确性（层次结构、计数、位置）。
2. 调用 `get_screenshot` 检查视觉正确性。仔细查找裁剪/截断的文本（行高截断内容）和重叠元素 — 这些很常见且容易被忽略。
3. 识别差异 — 是结构性的（错误的层次结构、缺少节点）还是视觉性的（错误的颜色、损坏的布局、裁剪的内容）？
4. 编写一个仅修改损坏部分的有针对性的修复脚本 — 不要重新创建所有内容。

> 有关完整的验证工作流程，请参阅 [验证和错误恢复](references/validation-and-recovery.md)。

## 7. 飞行前检查清单

在提交**任何** `use_figma` 调用之前，验证：

- [ ] 代码使用 `return` 发送数据（不是 `figma.closePlugin()`）
- [ ] 代码**没有**包装在异步 IIFE 中（自动为您包装）
- [ ] `return` 值包含有可操作信息的结构化数据（ID、计数）
- [ ] 任何地方都没有使用 `figma.notify()`
- [ ] 没有使用 `console.log()` 作为输出（改用 `return`）
- [ ] 所有颜色使用 0–1 范围（不是 0–255）
- [ ] 填充/描边作为新数组重新赋值（不是就地变异）
- [ ] 页面切换使用 `await figma.setCurrentPageAsync(page)`（同步设置器抛出）
- [ ] `layoutSizingVertical/Horizontal = 'FILL'` 在 `parent.appendChild(child)` 之后设置
- [ ] `loadFontAsync()` 在任何文本属性更改之前调用
- [ ] `lineHeight`/`letterSpacing` 使用 `{unit, value}` 格式（不是裸数字）
- [ ] `resize()` 在设置大小模式之前调用（resize 将它们重置为 FIXED）
- [ ] 对于多步骤工作流程：来自先前调用的 ID 作为字符串文字传递（不是变量）
- [ ] 新的顶级节点定位在远离 (0,0) 的位置，以避免与现有内容重叠
- [ ] **所有**创建/变异的节点 ID 都收集并包含在 `return` 值中
- [ ] 每个异步调用（`loadFontAsync`、`setCurrentPageAsync`、`importComponentByKeyAsync` 等）都是 `await` 的 — 没有触发并忘记的 Promises

## 8. 在创建之前发现约定

**始终在创建任何内容之前检查 Figma 文件。** 不同的文件使用不同的命名约定、变量结构和组件模式。您的代码应该匹配那里已有的内容，而不是强加新的约定。

如果对任何约定（命名、范围、结构）有疑问，请先检查 Figma 文件，然后检查用户的代码库。仅当两者都不存在时才回退到常见模式。

### 快速检查脚本

**列出所有页面和顶级节点：**
```js
const pages = figma.root.children.map(p => `${p.name} id=${p.id} children=${p.children.length}`);
return pages.join('\n');
```

**列出跨所有页面的现有组件：**
```js
const results = [];
for (const page of figma.root.children) {
  await figma.setCurrentPageAsync(page);
  page.findAll(n => {
    if (n.type === 'COMPONENT' || n.type === 'COMPONENT_SET')
      results.push(`[${page.name}] ${n.name} (${n.type}) id=${n.id}`);
    return false;
  });
}
return results.join('\n');
```

**列出现有变量集合及其约定：**
```js
const collections = await figma.variables.getLocalVariableCollectionsAsync();
const results = collections.map(c => ({
  name: c.name, id: c.id,
  varCount: c.variableIds.length,
  modes: c.modes.map(m => m.name)
}));
return results;
```

## 9. 参考文档

根据需要加载这些，基于您的任务涉及的内容：

| 文档 | 何时加载 | 涵盖内容 |
|-----|-------------|----------------|
| [gotchas.md](references/gotchas.md) | 在任何 `use_figma` 之前 | 每个已知陷阱的错误/正确代码示例 |
| [common-patterns.md](references/common-patterns.md) | 需要工作代码示例时 | 脚本脚手架：形状、文本、自动布局、变量、组件、多步骤工作流程 |
| [plugin-api-patterns.md](references/plugin-api-patterns.md) | 创建/编辑节点时 | 填充、描边、自动布局、效果、分组、克隆、样式 |
| [api-reference.md](references/api-reference.md) | 需要确切的 API 表面时 | 节点创建、变量 API、核心属性、什么有效和什么无效 |
| [validation-and-recovery.md](references/validation-and-recovery.md) | 多步骤写入或错误恢复时 | `get_metadata` 与 `get_screenshot` 工作流程、强制错误恢复步骤 |
| [component-patterns.md](references/component-patterns.md) | 创建组件/变体时 | combineAsVariants、组件属性、INSTANCE_SWAP、变体布局、发现现有组件、元数据遍历 |
| [variable-patterns.md](references/variable-patterns.md) | 创建/绑定变量时 | 集合、模式、范围、别名、绑定模式、发现现有变量 |
| [text-style-patterns.md](references/text-style-patterns.md) | 创建/应用文本样式时 | 字体比例、字体探测、列出样式、将样式应用于节点 |
| [effect-style-patterns.md](references/effect-style-patterns.md) | 创建/应用效果样式时 | 阴影、列出样式、将样式应用于节点 |
| [plugin-api-standalone.index.md](references/plugin-api-standalone.index.md) | 需要了解完整的 API 表面时 | 插件 API 中所有类型、方法和属性的索引 |
| [plugin-api-standalone.d.ts](references/plugin-api-standalone.d.ts) | 需要确切的类型签名时 | 完整的类型文件 — 搜索特定符号，不要一次加载全部 |

## 10. 代码片段示例

您将在整个文档中看到代码片段。这些片段包含有用的插件 API 代码，可以重新利用。按原样使用它们，或作为您前进的入门代码。如果有一些关键概念最好记录为通用片段，请将它们调出并写入磁盘，以便您将来可以重复使用。
