---
name: figma-generate-library
description: "从代码库在 Figma 中构建或更新专业级设计系统。当用户想要创建变量/令牌、构建组件库、设置主题（亮/暗模式）、记录基础或协调代码和 Figma 之间的差距时使用。此技能教授要构建什么以及按什么顺序构建 — 它补充了教授如何调用插件 API 的 `figma-use` 技能。两个技能应一起加载。"
---

# 设计系统构建器 — Figma MCP 技能

在 Figma 中构建与代码匹配的专业级设计系统。此技能跨 20–100+ 个 `use_figma` 调用编排多阶段工作流程，强制执行来自真实设计系统（Material 3、Polaris、Figma UI3、Simple DS）的质量模式。

**先决条件**：`figma-use` 技能也必须在每次 `use_figma` 调用时加载。它提供插件 API 语法规则（返回模式、页面重置、ID 返回、字体加载、颜色范围）。此技能提供设计系统领域知识和工作流程编排。

**在作为此技能的一部分调用 `use_figma` 时，始终传递 `skillNames: "figma-generate-library"`。** 这是一个日志记录参数 — 它不会影响执行。

---

## 1. 最重要的规则

**这永远不是一次性任务。** 构建设计系统需要跨多个阶段的 20–100+ 个 `use_figma` 调用，在它们之间有强制性的用户检查点。任何试图在一个调用中创建所有内容的尝试都会产生损坏、不完整或无法恢复的结果。将每个操作分解到最小的有用单元，验证，获取反馈，继续。

---

## 2. 强制性工作流程

每个设计系统构建都遵循此阶段顺序。跳过或重新排序阶段会导致昂贵的撤消结构故障。

```
阶段 0：发现（始终第一 — 尚无 use_figma 写入）
  0a. 分析代码库 → 提取令牌、组件、命名约定
  0b. 检查 Figma 文件 → 页面、变量、组件、样式、现有约定
  0c. 搜索订阅的库 → 使用 search_design_system 查找可重用资源
  0d. 锁定 v1 范围 → 在任何创建之前同意确切的令牌集 + 组件列表
  0e. 映射代码 → Figma → 解决冲突（代码和 Figma 不同意 = 询问用户）
  ✋ 用户检查点：呈现完整计划，等待明确批准

阶段 1：基础（令牌优先 — 始终在组件之前）
  1a. 创建变量集合和模式
  1b. 创建基元变量（原始值，1 种模式）
  1c. 创建语义变量（别名到基元，感知模式）
  1d. 在所有变量上设置范围
  1e. 在所有变量上设置代码语法
  1f. 创建效果样式（阴影）和文本样式（排版）
  → 退出标准：来自商定计划的每个令牌都存在，所有范围设置，所有代码语法设置
  ✋ 用户检查点：显示变量摘要，等待批准

阶段 2：文件结构（组件之前）
  2a. 创建页面骨架：封面 → 入门 → 基础 → --- → 组件 → --- → 实用程序
  2b. 创建基础文档页面（颜色样本、字体样本、间距条）
  → 退出标准：所有计划页面存在，基础文档可导航
  ✋ 用户检查点：显示页面列表 + 屏幕截图，等待批准

阶段 3：组件（一次一个 — 从不批量）
  对于每个组件（按依赖顺序：原子在分子之前）：
    3a. 创建专用页面
    3b. 使用自动布局 + 完整变量绑定构建基础组件
    3c. 创建所有变体组合（combineAsVariants + 网格布局）
    3d. 添加组件属性（TEXT、BOOLEAN、INSTANCE_SWAP）
    3e. 将属性链接到子节点
    3f. 添加页面文档（标题、描述、使用说明）
    3g. 验证：get_metadata（结构）+ get_screenshot（视觉）
    3h. 可选：在上下文新鲜时进行轻量级 Code Connect 映射
    → 退出标准：变体计数正确，所有绑定已验证，屏幕截图看起来正确
    ✋ 每个组件的用户检查点：显示屏幕截图，在进入下一个组件之前等待批准

阶段 4：集成 + QA（最终通过）
  4a. 最终确定所有 Code Connect 映射
  4b. 可访问性审计（对比度、最小触摸目标、焦点可见性）
  4c. 命名审计（无重复、无未命名节点、一致的大小写）
  4d. 未解析绑定审计（无剩余硬编码填充/描边）
  4e. 每个页面的最终审查屏幕截图
  ✋ 用户检查点：完整签收
```

---

## 3. 关键规则

**插件 API 基础**（来自 use_figma 技能 — 这里也强制执行）：
- 使用 `return` 发送数据（自动序列化）。不要包装在 IIFE 中或调用 closePlugin。
- 在每个返回值中返回所有创建/变异的节点 ID
- 页面上下文每次调用重置 — 始终在开始时 `await figma.setCurrentPageAsync(page)`
- `figma.notify()` 抛出 — 永远不要使用它
- 颜色是 0–1 范围，不是 0–255
- 字体必须在任何文本写入之前加载：`await figma.loadFontAsync({family, style})`

**设计系统规则**：
1. **变量在组件之前** — 组件绑定到变量。没有令牌 = 没有组件。
2. **创建之前检查** — 运行只读 `use_figma` 以发现现有约定。匹配它们。
3. **每个组件一个页面** *（默认）* — 例外：紧密相关的族（例如，Input + 辅助程序）可能共享具有清晰部分分隔的页面。
4. **将视觉属性绑定到变量** *（默认）* — 填充、描边、padding、radius、gap。例外：故意固定的几何形状（图标像素网格大小、静态分隔线）。
5. **每个变量上的范围** — 永远不要保留为 `ALL_SCOPES`。背景：`FRAME_FILL, SHAPE_FILL`。文本：`TEXT_FILL`。边框：`STROKE_COLOR`。间距：`GAP`。半径：`CORNER_RADIUS`。基元：`[]`（隐藏）。
6. **每个变量上的代码语法** — WEB 语法必须使用 `var()` 包装器：`var(--color-bg-primary)`，而不是 `--color-bg-primary`。使用代码库中的实际 CSS 变量名。ANDROID/iOS 不使用包装器。
7. **将语义别名到基元** — `{ type: 'VARIABLE_ALIAS', id: primitiveVar.id }`。切勿在语义层中重复原始值。
8. **combineAsVariants 后定位变体** — 它们堆叠在 (0,0)。手动网格布局 + 调整大小。
9. **图标的 INSTANCE_SWAP** — 切勿为每个图标创建变体。上限变体矩阵：如果大小 × 样式 × 状态 > 30 种组合，拆分为子组件。
10. **确定性命名** — 对幂等清理和可恢复性使用一致、唯一的节点名称。通过返回值和状态分类帐跟踪创建的节点 ID。
11. **无破坏性清理** — 清理脚本通过名称约定或返回的 ID 识别节点，而不是通过猜测。
12. **继续之前验证** — 切勿在未经验证的工作上构建。每次创建后 `get_metadata`，每个组件后 `get_screenshot`。
13. **切勿并行化 `use_figma` 调用** — Figma 状态突变必须严格顺序。即使您的工具支持并行调用，也切勿同时运行两个 use_figma 调用。
14. **切勿幻觉节点 ID** — 始终从先前调用返回的状态分类帐中读取 ID。切勿从内存中重建或猜测 ID。
15. **使用辅助脚本** — 将 `scripts/` 中的脚本嵌入到您的 use_figma 调用中。不要从头开始编写 200 行内联脚本。
16. **显式阶段批准** — 在每个检查点，显式命名下一个阶段。"看起来不错" 不是继续到阶段 3 的批准，如果您询问了阶段 1。

---

## 4. 状态管理（长工作流程必需）

> **`getPluginData()` / `setPluginData()` 在 `use_figma` 中不受支持。** 改用 `getSharedPluginData()` / `setSharedPluginData()`（这些是受支持的），或使用基于名称的查找和状态分类帐（返回的 ID）。

| 实体类型 | 幂等性密钥 | 如何检查存在性 |
|-------------|----------------|----------------------|
| 场景节点（页面、框架、组件） | `setSharedPluginData('dsb', 'key', value)` 或唯一名称 | `node.getSharedPluginData('dsb', 'key')` 或 `page.findOne(n => n.name === 'Button')` |
| 变量 | 集合内的名称 | `(await figma.variables.getLocalVariablesAsync()).find(v => v.name === name && v.variableCollectionId === collId)` |
| 样式 | 名称 | `getLocalTextStyles().find(s => s.name === name)` |

在创建后立即标记每个创建的**场景节点**：
```javascript
node.setSharedPluginData('dsb', 'run_id', RUN_ID);        // 标识此构建运行
node.setSharedPluginData('dsb', 'phase', 'phase3');        // 哪个阶段创建了它
node.setSharedPluginData('dsb', 'key', 'component/button');// 唯一逻辑密钥
```

**状态持久性**：不要仅依赖对话上下文作为状态分类帐。将其写入磁盘：
```
/tmp/dsb-state-{RUN_ID}.json
```
在每次轮次开始时重新读取此文件。在长工作流程中，对话上下文将被截断 — 文件是事实的来源。

维护跟踪的状态分类帐：
```json
{
  "runId": "ds-build-2024-001",
  "phase": "phase3",
  "step": "component-button",
  "entities": {
    "collections": { "primitives": "id:...", "color": "id:..." },
    "variables": { "color/bg/primary": "id:...", "spacing/sm": "id:..." },
    "pages": { "Cover": "id:...", "Button": "id:..." },
    "components": { "Button": "id:..." }
  },
  "pendingValidations": ["Button:screenshot"],
  "completedSteps": ["phase0", "phase1", "phase2", "component-avatar"]
}
```

**幂等性检查**：每次创建之前：按名称 + 状态分类帐 ID 查询。如果存在，跳过或更新 — 切勿重复。

**恢复协议**：在会话开始或上下文截断时，运行只读 `use_figma` 以按名称扫描所有页面、组件、变量和样式，以重建 `{key → id}` 映射。然后如果可用，从磁盘重新读取状态文件。

**继续提示**（在新聊天中恢复时提供给用户）：
> "我正在继续设计系统构建。运行 ID：{RUN_ID}。加载 figma-generate-library 技能并从最后完成的步骤恢复。"

---

## 5. search_design_system — 重用决策矩阵

在阶段 0 首先搜索，然后在每个组件创建之前再次搜索。

```
search_design_system({ query, fileKey, includeComponents: true, includeVariables: true, includeStyles: true })
```

**如果**所有这些为真，则重用：
- 组件属性 API 与您的需求匹配（相同的变体轴、兼容的类型）
- 令牌绑定模型兼容（使用相同或可别名变量）
- 命名约定与目标文件匹配
- 组件可编辑（不在您不拥有的远程库中锁定）

**如果**以下任何一项，则重建：
- API 不兼容（不同的属性名称、错误的变体模型）
- 令牌模型不兼容（硬编码值、不同的变量模式）
- 所有权问题（无法修改库）

**如果**视觉匹配但 API 不兼容，则包装：
- 将库组件作为嵌套实例导入到新包装器组件内部
- 在包装器上公开干净的 API

**三向优先级**：本地现有 → 订阅库导入 → 创建新库。

---

## 6. 用户检查点

强制性的。设计决策需要人工判断。

| 之后 | 必需工件 | 询问 |
|-------|-------------------|-----|
| 发现 + 范围锁定 | 令牌列表、组件列表、差距分析 | "这是我的计划。在我创建任何东西之前批准？" |
| 基础 | 变量摘要（N 个集合、M 个变量、K 种模式）、样式列表 | "所有令牌已创建。在文件结构之前审查？" |
| 文件结构 | 页面列表 + 屏幕截图 | "页面已设置。在组件之前审查？" |
| 每个组件 | 组件页面的 get_screenshot | "这是具有 N 个变体的 [组件]。正确？" |
| 每个冲突（代码 ≠ Figma） | 显示两个版本 | "代码说 X，Figma 有 Y。哪个获胜？" |
| 最终 QA | 每页屏幕截图 + 审计报告 | "完成。签收？" |

**如果用户拒绝**：在继续之前修复。切勿在拒绝的工作上构建。

---

## 7. 命名约定

匹配现有文件约定。如果从头开始：

**变量**（斜杠分隔）：
```
color/bg/primary     color/text/secondary    color/border/default
spacing/xs  spacing/sm  spacing/md  spacing/lg  spacing/xl  spacing/2xl
radius/none  radius/sm  radius/md  radius/lg  radius/full
typography/body/font-size    typography/heading/line-height
```

**基元**：`blue/50` → `blue/900`，`gray/50` → `gray/900`

**组件名称**：`Button`、`Input`、`Card`、`Avatar`、`Badge`、`Checkbox`、`Toggle`

**变体名称**：`Property=Value, Property=Value` — 例如，`Size=Medium, Style=Primary, State=Default`

**页面分隔符**：`---`（最常见）或 `——— COMPONENTS ———`

> 完整命名参考：[naming-conventions.md](references/naming-conventions.md)

---

## 8. 令牌架构

| 复杂性 | 模式 |
|-----------|---------|
| < 50 个令牌 | 单个集合，2 种模式（亮/暗） |
| 50–200 个令牌 | **标准**：基元（1 种模式）+ 颜色语义（亮/暗）+ 间距（1 种模式）+ 排版（1 种模式） |
| 200+ 个令牌 | **高级**：多个语义集合，4–8 种模式（亮/暗 × 对比度 × 品牌）。请参阅 [token-creation.md](references/token-creation.md) 中的 M3 模式 |

标准模式（推荐起点）：
```
集合："基元"    模式：["值"]
  blue/500 = #3B82F6, gray/900 = #111827, ...

集合："颜色"         模式：["亮", "暗"]
  color/bg/primary → 亮：别名基元/white，暗：别名基元/gray-900
  color/text/primary → 亮：别名基元/gray-900，暗：别名基元/white

集合："间距"       模式：["值"]
  spacing/xs = 4, spacing/sm = 8, spacing/md = 16, ...
```

---

## 9. 每阶段反模式

**阶段 0 反模式：**
- ❌ 在范围与用户锁定之前开始创建任何东西
- ❌ 忽略现有文件约定并强加新的约定
- ❌ 在计划组件创建之前跳过 `search_design_system`

**阶段 1 反模式：**
- ❌ 在任何变量上使用 `ALL_SCOPES`
- ❌ 在语义层中重复原始值而不是别名
- ❌ 不设置代码语法（破坏开发模式和往返）
- ❌ 在同意令牌分类法之前创建组件令牌

**阶段 2 反模式：**
- ❌ 跳过封面页面或基础文档
- ❌ 将多个不相关的组件放在一个页面上

**阶段 3 反模式：**
- ❌ 在基础存在之前创建组件
- ❌ 在组件中硬编码任何填充/描边/间距/半径值
- ❌ 为每个图标创建变体（改用 INSTANCE_SWAP）
- ❌ 不在 combineAsVariants 后定位变体（它们都堆叠在 0,0）
- ❌ 在不拆分的情况下构建 > 30 的变体矩阵（变体爆炸）
- ❌ 导入远程组件然后立即分离它们

**一般反模式：**
- ❌ 在首先理解错误之前重试失败的脚本
- ❌ 使用名称前缀匹配进行清理（删除用户拥有的节点）
- ❌ 在上一步的未经证实的工作上构建
- ❌ 跳过用户检查点以"节省时间"
- ❌ 并行化 use_figma 调用（始终顺序）
- ❌ 从内存中猜测/幻觉节点 ID（始终从状态分类帐读取）
- ❌ 编写大量内联脚本而不是使用提供的辅助脚本
- ❌ 启动阶段 3，因为用户说"构建按钮"而没有完成阶段 0-2

---

## 10. 参考文档

按需加载 — 每个参考对其阶段具有权威性：

使用您的文件读取工具在需要时阅读这些文档。不要从文件名假设其内容。

| 文档 | 阶段 | 必需 / 可选 | 何时加载 |
|-----|-------|---------------------|-----------|
| [discovery-phase.md](references/discovery-phase.md) | 0 | **必需** | 启动任何构建 — 代码库分析 + Figma 检查 |
| [token-creation.md](references/token-creation.md) | 1 | **必需** | 创建变量、集合、模式、样式 |
| [documentation-creation.md](references/documentation-creation.md) | 2 | 必需 | 创建封面页面、基础文档、样本 |
| [component-creation.md](references/component-creation.md) | 3 | **必需** | 创建任何组件或变体 |
| [code-connect-setup.md](references/code-connect-setup.md) | 3–4 | 必需 | 设置 Code Connect 或变量代码语法 |
| [naming-conventions.md](references/naming-conventions.md) | 任何 | 可选 | 命名任何东西 — 变量、页面、变体、样式 |
| [error-recovery.md](references/error-recovery.md) | 任何 | **错误时必需** | 脚本失败、多步骤工作流程恢复、放弃的工作流程状态清理 |

---

## 11. 脚本

可重用的插件 API 辅助函数。嵌入到 `use_figma` 调用中：

| 脚本 | 目的 |
|--------|---------|
| [inspectFileStructure.js](scripts/inspectFileStructure.js) | 发现所有页面、组件、变量、样式；返回完整清单 |
| [createVariableCollection.js](scripts/createVariableCollection.js) | 创建具有模式的命名集合；返回 `{collectionId, modeIds}` |
| [createSemanticTokens.js](scripts/createSemanticTokens.js) | 从令牌映射创建别名语义变量 |
| [createComponentWithVariants.js](scripts/createComponentWithVariants.js) | 从变体矩阵构建组件集；处理网格布局 |
| [bindVariablesToComponent.js](scripts/bindVariablesToComponent.js) | 将设计令牌绑定到所有组件视觉属性 |
| [createDocumentationPage.js](scripts/createDocumentationPage.js) | 创建具有标题 + 描述 + 部分结构的页面 |
| [validateCreation.js](scripts/validateCreation.js) | 验证创建的节点是否匹配预期的计数、名称、结构 |
| [cleanupOrphans.js](scripts/cleanupOrphans.js) | 按名称约定或状态分类帐 ID 删除孤立节点 |
| [rehydrateState.js](scripts/rehydrateState.js) | 按名称扫描文件以查找所有页面、组件、变量；返回完整的 `{key → nodeId}` 映射以进行状态重建 |
