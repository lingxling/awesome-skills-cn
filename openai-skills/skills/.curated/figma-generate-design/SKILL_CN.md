---
name: figma-generate-design
description: "当任务涉及将应用程序页面、视图或多部分布局转换为 Figma 时，将此技能与 figma-use 一起使用。触发器：'write to Figma'、'create in Figma from code'、'push page to Figma'、'take this app/page and build it in Figma'、'create a screen'、'build a landing page in Figma'、'update the Figma screen to match code'。每当用户想要从代码或描述在 Figma 中构建或更新完整页面、屏幕或视图时，这是首选的工作流程技能。通过 search_design_system 发现设计系统组件、变量和样式，导入它们，并使用设计系统令牌而不是硬编码值逐步组装屏幕。"
---

# 从设计系统构建/更新屏幕

使用此技能通过**重用已发布的设计系统** — 组件、变量和样式 — 而不是使用硬编码值绘制基元，在 Figma 中创建或更新全页屏幕。关键见解：Figma 文件可能具有与代码库的 UI 组件和令牌相对应的已发布设计系统，包括组件、颜色/间距变量以及文本/效果样式。找到并使用这些，而不是用十六进制颜色绘制框。

**强制**：在调用 `use_figma` 之前，您还必须加载 [figma-use](../figma-use/SKILL.md)。该技能包含适用于您编写的每个脚本的关键规则（颜色范围、字体加载等）。

**在作为此技能的一部分调用 `use_figma` 时，始终传递 `skillNames: "figma-generate-design"`。** 这是一个日志记录参数 — 它不会影响执行。

## 技能边界

- 当可交付成果是**由设计系统组件实例组成的 Figma 屏幕**（新的或更新的）时，使用此技能。
- 如果用户想要**从 Figma 设计生成代码**，请切换到 [figma-implement-design](../figma-implement-design/SKILL.md)。
- 如果用户想要**创建新的可重用组件或变体**，请直接使用 [figma-use](../figma-use/SKILL.md)。
- 如果用户想要**编写 Code Connect 映射**，请切换到 [figma-code-connect-components](../figma-code-connect-components/SKILL.md)。

## 先决条件

- Figma MCP 服务器必须已连接
- 目标 Figma 文件必须具有已发布的设计系统，包括组件（或访问团队库）
- 用户应提供：
  - 要在其中工作的 Figma 文件 URL / 文件密钥
  - 或有关要定位哪个文件的上下文（代理可以发现页面）
- 要构建/更新的屏幕的源代码或描述

## 与 generate_figma_design 的并行工作流程（仅限 Web 应用）

当从可以在浏览器中呈现的** Web 应用**构建屏幕时，最佳结果来自并行运行两种方法：

1. **并行：**
   - 开始使用此技能的工作流程构建屏幕（use_figma + 设计系统组件）
   - 运行 `generate_figma_design` 以捕获正在运行的 Web 应用的像素级完美屏幕截图
2. **两者都完成后：** 更新 use_figma 输出以匹配 `generate_figma_design` 捕获的像素级完美布局。捕获提供了要瞄准的确切间距、大小和视觉处理，而您的 use_figma 输出具有链接到设计系统的正确组件实例。
3. **一旦确认看起来不错：** 删除 `generate_figma_design` 输出 — 它仅用作视觉参考。

这结合了两种方法的最佳优点：`generate_figma_design` 提供像素级完美的布局精度，而 use_figma 提供链接到设计系统并保持链接和可更新的正确设计系统组件实例。

**此工作流程仅适用于** `generate_figma_design` 可以捕获正在运行的页面的 Web 应用。对于非 Web 应用（iOS、Android 等）或更新现有屏幕时，请使用下面的标准工作流程。

## 必需的工作流程

**按顺序执行这些步骤。不要跳过步骤。**

### 步骤 1：了解屏幕

在接触 Figma 之前，了解您要构建的内容：

1. 如果从代码构建，请阅读相关的源文件以了解页面结构、部分以及使用了哪些组件。
2. 确定屏幕的主要部分（例如，Header、Hero、内容面板、定价网格、FAQ 手风琴、Footer）。
3. 对于每个部分，列出所涉及的 UI 组件（按钮、输入、卡片、导航 pills、手风琴等）。

### 步骤 2：发现设计系统 — 组件、变量和样式

您需要从设计系统中获取三件事：**组件**（按钮、卡片等）、**变量**（颜色、间距、半径）和**样式**（文本样式、阴影等效果）。当设计系统令牌存在时，不要硬编码十六进制颜色或像素值。

#### 2a：发现组件

**首选：首先检查现有屏幕。** 如果目标文件已包含使用相同设计系统的屏幕，请跳过 `search_design_system` 并直接检查现有实例。单个遍历现有框架实例的 `use_figma` 调用会为您提供确切的、权威的组件映射：

```js
const frame = figma.currentPage.findOne(n => n.name === "现有屏幕");
const uniqueSets = new Map();
frame.findAll(n => n.type === "INSTANCE").forEach(inst => {
  const mc = inst.mainComponent;
  const cs = mc?.parent?.type === "COMPONENT_SET" ? mc.parent : null;
  const key = cs ? cs.key : mc?.key;
  const name = cs ? cs.name : mc?.name;
  if (key && !uniqueSets.has(key)) {
    uniqueSets.set(key, { name, key, isSet: !!cs, sampleVariant: mc.name });
  }
});
return [...uniqueSets.values()];
```

仅当文件没有要引用的现有屏幕时，才回退到 `search_design_system`。使用它时，**广泛搜索** — 尝试多个术语和同义词（例如，"button"、"input"、"nav"、"card"、"accordion"、"header"、"footer"、"tag"、"avatar"、"toggle"、"icon" 等）。使用 `includeComponents: true` 专注于组件。

**在映射中包括组件属性** — 您需要知道每个组件公开哪些 TEXT 属性以进行文本覆盖。创建一个临时实例，读取其 `componentProperties`（以及嵌套实例的属性），然后删除临时实例。

带有属性信息的示例组件映射：

```
组件映射：
- Button → key: "abc123", type: COMPONENT_SET
  属性：{ "Label#2:0": TEXT, "Has Icon#4:64": BOOLEAN }
- PricingCard → key: "ghi789", type: COMPONENT_SET
  属性：{ "Device": VARIANT, "Variant": VARIANT }
  嵌套的 "Text Heading" 具有：{ "Text#2104:5": TEXT }
  嵌套的 "Button" 具有：{ "Label#2:0": TEXT }
```

#### 2b：发现变量（颜色、间距、半径）

**首先检查现有屏幕**（与组件相同）。或使用 `includeVariables: true` 的 `search_design_system`。

> **警告：两种不同的变量发现方法 — 不要混淆它们。**
>
> - `use_figma` 与 `figma.variables.getLocalVariableCollectionsAsync()` — 仅返回**在当前文件中定义的本地变量**。如果此返回为空，则**不**意味着不存在变量。远程/已发布库变量对此 API 不可见。
> - `search_design_system` 与 `includeVariables: true` — 搜索**所有链接的库**，包括远程和已发布的库。这是发现设计系统变量的正确工具。
>
> **永远不要仅基于 `getLocalVariableCollectionsAsync()` 返回空就得出"不存在变量"的结论。** 在决定创建自己的变量之前，始终还运行 `includeVariables: true` 的 `search_design_system` 以检查库变量。

**查询策略：** `search_design_system` 匹配**变量名称**（例如，"Gray/gray-9"、"core/gray/100"、"space/400"），而不是类别。并行运行多个简短、简单的查询，而不是一个复合查询：

- **基元颜色：** "gray"、"red"、"blue"、"green"、"white"、"brand"
- **语义颜色：** "background"、"foreground"、"border"、"surface"、"text"
- **间距/大小：** "space"、"radius"、"gap"、"padding"

如果初始搜索返回为空，请尝试更短的片段或不同的命名约定 — 库差异很大（"grey" 与 "gray"、"spacing" 与 "space"、"color/bg" 与 "background"）。

检查现有屏幕的绑定变量以获得最权威的结果：

```js
const frame = figma.currentPage.findOne(n => n.name === "现有屏幕");
const varMap = new Map();
frame.findAll(() => true).forEach(node => {
  const bv = node.boundVariables;
  if (!bv) return;
  for (const [prop, binding] of Object.entries(bv)) {
    const bindings = Array.isArray(binding) ? binding : [binding];
    for (const b of bindings) {
      if (b?.id && !varMap.has(b.id)) {
        const v = await figma.variables.getVariableByIdAsync(b.id);
        if (v) varMap.set(b.id, { name: v.name, id: v.id, key: v.key, type: v.resolvedType, remote: v.remote });
      }
    }
  }
});
return [...varMap.values()];
```

对于库变量（remote = true），使用 `figma.variables.importVariableByKeyAsync(key)` 按密钥导入它们。对于本地变量，直接使用 `figma.variables.getVariableByIdAsync(id)`。

有关绑定模式，请参阅 [variable-patterns.md](../figma-use/references/variable-patterns.md)。

#### 2c：发现样式（文本样式、效果样式）

使用 `includeStyles: true` 和 "heading"、"body"、"shadow"、"elevation" 等术语的 `search_design_system` 搜索样式。或检查现有屏幕使用的内容：

```js
const frame = figma.currentPage.findOne(n => n.name === "现有屏幕");
const styles = { text: new Map(), effect: new Map() };
frame.findAll(() => true).forEach(node => {
  if ('textStyleId' in node && node.textStyleId) {
    const s = figma.getStyleById(node.textStyleId);
    if (s) styles.text.set(s.id, { name: s.name, id: s.id, key: s.key });
  }
  if ('effectStyleId' in node && node.effectStyleId) {
    const s = figma.getStyleById(node.effectStyleId);
    if (s) styles.effect.set(s.id, { name: s.name, id: s.id, key: s.key });
  }
});
return {
  textStyles: [...styles.text.values()],
  effectStyles: [...styles.effect.values()]
};
```

使用 `figma.importStyleByKeyAsync(key)` 导入库样式，然后使用 `node.textStyleId = style.id` 或 `node.effectStyleId = style.id` 应用它们。

有关详细信息，请参阅 [text-style-patterns.md](../figma-use/references/text-style-patterns.md) 和 [effect-style-patterns.md](../figma-use/references/effect-style-patterns.md)。

### 步骤 3：首先创建页面包装器框架

**不要将部分构建为顶级页面子级，然后再重新定位它们** — 跨 `use_figma` 调用使用 `appendChild()` 移动节点会静默失败并产生孤立的框架。相反，首先创建包装器，然后直接在内部构建每个部分。

在其自己的 `use_figma` 调用中创建页面包装器。将其定位在远离现有内容的位置，并返回其 ID：

```js
// 找到清晰的空间
let maxX = 0;
for (const child of figma.currentPage.children) {
  maxX = Math.max(maxX, child.x + child.width);
}

const wrapper = figma.createFrame();
wrapper.name = "主页";
wrapper.layoutMode = "VERTICAL";
wrapper.primaryAxisAlignItems = "CENTER";
wrapper.counterAxisAlignItems = "CENTER";
wrapper.resize(1440, 100);
wrapper.layoutSizingHorizontal = "FIXED";
wrapper.layoutSizingVertical = "HUG";
wrapper.x = maxX + 200;
wrapper.y = 0;

return { success: true, wrapperId: wrapper.id };
```

### 步骤 4：在包装器内部构建每个部分

**这是最重要的步骤。** 一次构建一个部分，每个部分都在其自己的 `use_figma` 调用中。在每个脚本的开头，通过 ID 获取包装器并将新内容直接附加到它。

```js
const createdNodeIds = [];
const wrapper = await figma.getNodeByIdAsync("来自步骤 3 的 WRAPPER_ID");

// 按键导入设计系统组件
const buttonSet = await figma.importComponentSetByKeyAsync("BUTTON_SET_KEY");
const primaryButton = buttonSet.children.find(c =>
  c.type === "COMPONENT" && c.name.includes("variant=primary")
) || buttonSet.defaultVariant;

// 为颜色和间距导入设计系统变量
const bgColorVar = await figma.variables.importVariableByKeyAsync("BG_COLOR_VAR_KEY");
const spacingVar = await figma.variables.importVariableByKeyAsync("SPACING_VAR_KEY");

// 使用变量绑定（而不是硬编码值）构建部分框架
const section = figma.createFrame();
section.name = "Header";
section.layoutMode = "HORIZONTAL";
section.setBoundVariable("paddingLeft", spacingVar);
section.setBoundVariable("paddingRight", spacingVar);
const bgPaint = figma.variables.setBoundVariableForPaint(
  { type: 'SOLID', color: { r: 0, g: 0, b: 0 } }, 'color', bgColorVar
);
section.fills = [bgPaint];

// 导入并应用文本/效果样式
const shadowStyle = await figma.importStyleByKeyAsync("SHADOW_STYLE_KEY");
section.effectStyleId = shadowStyle.id;

// 在部分内部创建组件实例
const btnInstance = primaryButton.createInstance();
section.appendChild(btnInstance);
createdNodeIds.push(btnInstance.id);

// 将部分附加到包装器
wrapper.appendChild(section);
section.layoutSizingHorizontal = "FILL"; // 在附加之后

createdNodeIds.push(section.id);
return { success: true, createdNodeIds };
```

在每个部分之后，在继续之前使用 `get_screenshot` 进行验证。仔细查找裁剪/截断的文本（行高截断内容）和重叠元素 — 这些是最常见的问题，很容易被忽略。

#### 使用 setProperties() 覆盖实例文本

组件实例带有占位符文本（"Title"、"Heading"、"Button"）。使用您在步骤 2 中发现的组件属性键，使用 `setProperties()` 覆盖它们 — 这比直接操作 `node.characters` 更可靠。有关完整模式，请参阅 [component-patterns.md](../figma-use/references/component-patterns.md#overriding-text-in-a-component-instance)。

对于公开其自己的 TEXT 属性的嵌套实例，在嵌套实例上调用 `setProperties()`：

```js
const nestedHeading = cardInstance.findOne(n => n.type === "INSTANCE" && n.name === "Text Heading");
if (nestedHeading) {
  nestedHeading.setProperties({ "Text#2104:5": "来自源代码的实际标题" });
}
```

仅对不受任何组件属性管理的文本回退到直接 `node.characters`。

#### 仔细阅读源代码默认值

将代码组件转换为 Figma 实例时，请检查组件的默认 prop 值，而不仅仅是显式传递的内容。例如，没有 variant prop 的 `<Button size="small">Register</Button>` — 检查组件定义以找到 `variant = "primary"` 作为默认值。选择错误的变体（例如，Neutral 而不是 Primary）会产生视觉上不正确的结果，很容易被忽略。

#### 手动构建与从设计系统导入的内容

| 手动构建 | 从设计系统导入 |
|----------------|--------------------------|
| 页面包装器框架 | **组件**：按钮、卡片、输入、导航等 |
| 部分容器框架 | **变量**：颜色（填充、描边）、间距（padding、gap）、半径 |
| 布局网格（行、列） | **文本样式**：heading、body、caption 等 |
| | **效果样式**：阴影、模糊等 |

**当设计系统变量存在时，永远不要硬编码十六进制颜色或像素间距。** 对间距/半径使用 `setBoundVariable`，对颜色使用 `setBoundVariableForPaint`。使用 `node.textStyleId` 应用文本样式，使用 `node.effectStyleId` 应用效果样式。

### 步骤 5：验证完整屏幕

组合所有部分后，在完整页面框架上调用 `get_screenshot` 并与源进行比较。使用有针对性的 `use_figma` 调用修复任何问题 — 不要重建整个屏幕。

**截图各个部分，而不仅仅是完整页面。** 以缩小分辨率显示的完整页面屏幕截图会隐藏文本截断、错误颜色和尚未覆盖的占位符文本。按节点 ID 对每个部分进行截图以捕获：
- **裁剪/截断的文本** — 行高或框架大小截断下降器、上升器或整行
- **重叠内容** — 由于大小不正确或缺少自动布局而堆叠在彼此之上的元素
- 仍显示的占位符文本（"Title"、"Heading"、"Button"）
- 布局大小错误导致的截断内容
- 错误的组件变体（例如，Neutral 与 Primary 按钮）

### 步骤 6：更新现有屏幕

更新而不是从头开始创建时：

1. 使用 `get_metadata` 检查现有屏幕结构。
2. 确定哪些部分需要更新，哪些可以保留。
3. 对于每个需要更改的部分：
   - 通过 ID 或名称定位现有节点
   - 如果设计系统组件发生更改，则交换组件实例
   - 根据需要更新文本内容、变体属性或布局
   - 删除已弃用的部分
   - 添加新部分
4. 在每次修改后使用 `get_screenshot` 进行验证。

```js
// 示例：在现有屏幕中交换按钮变体
const existingButton = await figma.getNodeByIdAsync("EXISTING_BUTTON_INSTANCE_ID");
if (existingButton && existingButton.type === "INSTANCE") {
  // 导入更新的组件
  const buttonSet = await figma.importComponentSetByKeyAsync("BUTTON_SET_KEY");
  const newVariant = buttonSet.children.find(c =>
    c.name.includes("variant=primary") && c.name.includes("size=lg")
  ) || buttonSet.defaultVariant;
  existingButton.swapComponent(newVariant);
}
return { success: true, mutatedNodeIds: [existingButton.id] };
```

## 参考文档

根据需要，从 [figma-use](../figma-use/SKILL.md) 参考中加载这些：

- [component-patterns.md](../figma-use/references/component-patterns.md) — 按键导入、查找变体、setProperties、文本覆盖、使用实例
- [variable-patterns.md](../figma-use/references/variable-patterns.md) — 创建/绑定变量、导入库变量、范围、别名、发现现有变量
- [text-style-patterns.md](../figma-use/references/text-style-patterns.md) — 创建/应用文本样式、导入库文本样式、字体比例
- [effect-style-patterns.md](../figma-use/references/effect-style-patterns.md) — 创建/应用效果样式（阴影）、导入库效果样式
- [gotchas.md](../figma-use/references/gotchas.md) — 布局陷阱（HUG/FILL 交互、counterAxisAlignItems、大小顺序）、paint/颜色问题、页面上下文重置

## 错误恢复

遵循 [figma-use](../figma-use/SKILL.md#6-error-recovery--self-correction) 中的错误恢复过程：

1. **在错误时停止** — 不要立即重试。
2. **仔细阅读错误消息** 以了解出了什么问题。
3. 如果错误不清楚，请调用 `get_metadata` 或 `get_screenshot` 以检查当前文件状态。
4. **根据错误消息修复脚本**。
5. **重试**更正后的脚本 — 这是安全的，因为失败的脚本是原子的（如果脚本出错，则不会创建任何内容）。

因为此技能是增量工作的（每个调用一个部分），所以错误自然限定在单个部分。来自成功调用的先前部分保持完整。

## 最佳实践

- **始终在构建之前搜索。** 设计系统可能具有您需要的组件、变量或样式。手动构造和硬编码值应该是例外，而不是规则。
- **广泛搜索。** 尝试同义词和部分术语。"NavigationPill" 可能在 "pill"、"nav"、"tab" 或 "chip" 下找到。对于变量，搜索 "color"、"spacing"、"radius" 等。
- **优先选择设计系统令牌而不是硬编码值。** 对颜色、间距和半径使用变量绑定。对排版使用文本样式。对阴影使用效果样式。这使屏幕保持链接到设计系统。
- **优先选择组件实例而不是手动构建。** 实例保持链接到源组件，并在设计系统演进时自动更新。
- **逐部分工作。** 每个 `use_figma` 调用永远不要构建多个主要部分。
- **从每次调用返回节点 ID。** 您需要它们来组合部分并用于错误恢复。
- **在每个部分之后进行视觉验证。** 使用 `get_screenshot` 尽早发现问题。
- **匹配现有约定。** 如果文件已有屏幕，请匹配其命名、大小和布局模式。
