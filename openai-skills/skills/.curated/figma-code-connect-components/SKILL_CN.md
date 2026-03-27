---
name: figma-code-connect-components
description: 使用 Code Connect 映射工具将 Figma 设计组件连接到代码组件。当用户说 "code connect"、"connect this component to code"、"map this component"、"link component to code"、"create code connect mapping" 或想要在 Figma 设计和代码实现之间建立映射时使用。对于通过 `use_figma` 进行画布写入，请使用 `figma-use`。
---

# Code Connect 组件

## 概述

此技能帮助您使用 Figma 的 Code Connect 功能将 Figma 设计组件连接到其相应的代码实现。它分析 Figma 设计结构，在您的代码库中搜索匹配的组件，并建立保持设计代码一致性的映射。

## 技能边界

- 将此技能用于 `get_code_connect_suggestions` + `send_code_connect_mappings` 工作流程。
- 如果任务需要使用插件 API 脚本写入 Figma 画布，请切换到 [figma-use](../figma-use/SKILL.md)。
- 如果任务是从代码或描述在 Figma 中构建或更新完整页面屏幕，请切换到 [figma-generate-design](../figma-generate-design/SKILL.md)。
- 如果任务是从 Figma 实现产品代码，请切换到 [figma-implement-design](../figma-implement-design/SKILL.md)。

## 先决条件

- Figma MCP 服务器必须已连接并可访问
- 用户必须提供带有节点 ID 的 Figma URL：`https://figma.com/design/:fileKey/:fileName?node-id=1-2`
  - **重要：** Figma URL 必须包含 `node-id` 参数。没有它，Code Connect 映射将失败。
- **或者** 使用 `figma-desktop` MCP 时：用户可以直接在 Figma 桌面应用程序中选择节点（不需要 URL）
- **重要：** Figma 组件必须发布到团队库。Code Connect 仅适用于已发布的组件或组件集。
- **重要：** Code Connect 仅在组织和Enterprise计划中可用。
- 访问项目代码库以进行组件扫描

## 必需的工作流程

**按顺序执行这些步骤。不要跳过步骤。**

### 步骤 1：获取 Code Connect 建议

调用 `get_code_connect_suggestions` 以在单个操作中识别所有未映射的组件。此工具自动：

- 从 Figma 场景图获取组件信息
- 识别所选内容中的已发布组件
- 检查现有的 Code Connect 映射并过滤掉已连接的组件
- 返回每个未映射组件的组件名称、属性和缩略图图像

#### 选项 A：使用 `figma-desktop` MCP（未提供 URL）

如果 `figma-desktop` MCP 服务器已连接且用户**未**提供 Figma URL，请立即调用 `get_code_connect_suggestions`。不需要 URL 解析 — 桌面 MCP 服务器自动使用打开的 Figma 文件中当前选定的节点。

**注意：** 用户必须打开 Figma 桌面应用程序并选择节点。`fileKey` 不作为参数传递 — 服务器使用当前打开的文件。

#### 选项 B：提供 Figma URL 时

解析 URL 以提取 `fileKey` 和 `nodeId`，然后调用 `get_code_connect_suggestions`。

**重要：** 从 Figma URL 提取节点 ID 时，转换格式：

- URL 格式使用连字符：`node-id=1-2`
- 工具期望冒号：`nodeId=1:2`

**解析 Figma URL：**

- URL 格式：`https://figma.com/design/:fileKey/:fileName?node-id=1-2`
- 提取文件密钥：`:fileKey`（`/design/` 后的段）
- 提取节点 ID：URL 中的 `1-2`，然后转换为 `1:2` 用于工具

```
get_code_connect_suggestions(fileKey=":fileKey", nodeId="1:2")
```

**处理响应：**

- 如果工具返回 **"此选择中未找到已发布组件"** → 通知用户并停止。组件可能需要先发布到团队库。
- 如果工具返回 **"此选择中的所有组件实例已通过 Code Connect 连接到代码"** → 通知用户所有内容都已映射。
- 否则，响应包含未映射组件列表，每个组件包含：
  - 组件名称
  - 节点 ID
  - 组件属性（具有属性名称和值的 JSON）
  - 组件的缩略图图像（用于视觉检查）

### 步骤 2：扫描代码库以查找匹配组件

对于 `get_code_connect_suggestions` 返回的每个未映射组件，在代码库中搜索匹配的代码组件。

**查找内容：**

- 与 Figma 组件名称匹配或相似的组件名称
- 与 Figma 层次结构对齐的组件结构
- 与 Figma 属性对应的 Props（变体、文本、样式）
- 典型组件目录中的文件（`src/components/`、`components/`、`ui/` 等）

**搜索策略：**

1. 搜索具有匹配名称的组件文件
2. 读取候选文件以检查结构和 props
3. 将代码组件的 props 与步骤 1 中返回的 Figma 组件属性进行比较
4. 检测编程语言（TypeScript、JavaScript）和框架（React、Vue 等）
5. 基于结构相似性确定最佳匹配，权衡：
   - 与 Figma 属性对应的 Prop 名称
   - 与 Figma 默认值匹配的默认值
   - CSS 类或样式对象
   - 阐明意图的描述性注释
6. 如果多个候选同样好，选择具有最接近 prop 接口匹配的那个，并在工具调用前用 1-2 句注释记录您的推理

**示例搜索模式：**

- 如果 Figma 组件是 "PrimaryButton"，搜索 `Button.tsx`、`PrimaryButton.tsx`、`Button.jsx`
- 检查常见组件路径：`src/components/`、`app/components/`、`lib/ui/`
- 查找匹配 Figma 变体的变体 props，如 `variant`、`size`、`color`

### 步骤 3：向用户展示匹配

展示您的发现，让用户选择要创建哪些映射。用户可以接受全部、部分或不接受任何建议的映射。

**以以下格式展示匹配：**

```
以下组件与设计匹配：
- [ComponentName](path/to/component): DesignComponentName at nodeId [nodeId](figmaUrl?node-id=X-Y)
- [AnotherComponent](path/to/another): AnotherDesign at nodeId [nodeId2](figmaUrl?node-id=X-Y)

您想连接这些组件吗？您可以接受全部、选择特定组件或跳过。
```

**如果找不到组件的完全匹配：**

- 展示 2 个最接近的候选
- 解释差异
- 询问用户确认使用哪个组件或提供正确的路径

**如果用户拒绝所有映射**，通知他们并停止。不需要进一步的工具调用。

### 步骤 4：创建 Code Connect 映射

用户确认其选择后，仅使用接受的映射调用 `send_code_connect_mappings`。此工具在单个调用中处理所有映射的批量创建。

**示例：**

```
send_code_connect_mappings(
  fileKey=":fileKey",
  nodeId="1:2",
  mappings=[
    { nodeId: "1:2", componentName: "Button", source: "src/components/Button.tsx", label: "React" },
    { nodeId: "1:5", componentName: "Card", source: "src/components/Card.tsx", label: "React" }
  ]
)
```

**每个映射的关键参数：**

- `nodeId`：Figma 节点 ID（使用冒号格式：`1:2`）
- `componentName`：要连接的组件名称（例如 "Button"、"Card"）
- `source`：代码组件文件的路径（相对于项目根目录）
- `label`：此 Code Connect 映射的框架或语言标签。有效值包括：
  - Web：'React'、'Web Components'、'Vue'、'Svelte'、'Storybook'、'Javascript'
  - iOS：'Swift UIKit'、'Objective-C UIKit'、'SwiftUI'
  - Android：'Compose'、'Java'、'Kotlin'、'Android XML Layout'
  - 跨平台：'Flutter'
  - 文档：'Markdown'

**调用后：**

- 成功时：工具确认映射已创建
- 错误时：工具报告哪些特定映射失败以及原因（例如 "组件已映射到代码"、"未找到已发布组件"、"权限不足"）

**处理后提供摘要：**

```
Code Connect 摘要：
- 成功连接：3
  - Button (1:2) → src/components/Button.tsx
  - Card (1:5) → src/components/Card.tsx
  - Input (1:8) → src/components/Input.tsx
- 无法连接：1
  - CustomWidget (1:10) - 在代码库中未找到匹配组件
```

## 示例

### 示例 1：连接按钮组件

用户说："将此 Figma 按钮连接到我的代码：https://figma.com/design/kL9xQn2VwM8pYrTb4ZcHjF/DesignSystem?node-id=42-15"

**操作：**

1. 解析 URL：fileKey=`kL9xQn2VwM8pYrTb4ZcHjF`，nodeId=`42-15` → 转换为 `42:15`
2. 运行 `get_code_connect_suggestions(fileKey="kL9xQn2VwM8pYrTb4ZcHjF", nodeId="42:15")`
3. 响应显示：Button 组件（未映射）具有 `variant`（primary/secondary）和 `size`（sm/md/lg）属性，以及缩略图图像
4. 在代码库中搜索 Button 组件：找到 `src/components/Button.tsx`
5. 读取 `Button.tsx` 并确认它具有 `variant` 和 `size` props
6. 向用户展示：
   ```
   我找到了一个匹配：
   - [Button](src/components/Button.tsx)：nodeId [42:15](https://figma.com/design/kL9xQn2VwM8pYrTb4ZcHjF/DesignSystem?node-id=42-15) 处的 Button

   您想连接此组件吗？
   ```

7. 用户确认："是"
8. 检测到它是 TypeScript React 组件
9. 运行 `send_code_connect_mappings(fileKey="kL9xQn2VwM8pYrTb4ZcHjF", nodeId="42:15", mappings=[{ nodeId: "42:15", componentName: "Button", source: "src/components/Button.tsx", label: "React" }])`

**结果：** Figma 按钮组件现在已连接到代码 Button 组件。

### 示例 2：具有部分选择的多个组件

用户说："连接此框架中的组件：https://figma.com/design/pR8mNv5KqXzGwY2JtCfL4D/Components?node-id=10-50"

**操作：**

1. 解析 URL：fileKey=`pR8mNv5KqXzGwY2JtCfL4D`，nodeId=`10-50` → 转换为 `10:50`
2. 运行 `get_code_connect_suggestions(fileKey="pR8mNv5KqXzGwY2JtCfL4D", nodeId="10:50")`
3. 响应显示 3 个未映射组件：ProductCard、Badge 和 CustomWidget
4. 搜索代码库：
   - ProductCard：找到 `src/components/ProductCard.tsx`（props 匹配）
   - Badge：找到 `src/components/Badge.tsx`（props 匹配）
   - CustomWidget：未找到匹配组件
5. 向用户展示：
   ```
   以下组件与设计匹配：
   - [ProductCard](src/components/ProductCard.tsx)：nodeId [10:51](https://figma.com/design/pR8mNv5KqXzGwY2JtCfL4D/Components?node-id=10-51) 处的 ProductCard
   - [Badge](src/components/Badge.tsx)：nodeId [10:52](https://figma.com/design/pR8mNv5KqXzGwY2JtCfL4D/Components?node-id=10-52) 处的 Badge

   我找不到 CustomWidget (10:53) 的匹配。

   您想连接这些组件吗？您可以接受全部、选择特定组件或跳过。
   ```

6. 用户："只连接 ProductCard，暂时跳过 Badge"
7. 运行 `send_code_connect_mappings(fileKey="pR8mNv5KqXzGwY2JtCfL4D", nodeId="10:50", mappings=[{ nodeId: "10:51", componentName: "ProductCard", source: "src/components/ProductCard.tsx", label: "React" }])`

**结果：** 仅根据用户的选择连接 ProductCard。

### 示例 3：需要创建组件

用户说："连接此图标：https://figma.com/design/8yJDMeWDyBz71EnMOSuUiw/Icons?node-id=5-20"

**操作：**

1. 解析 URL：fileKey=`8yJDMeWDyBz71EnMOSuUiw`，nodeId=`5-20` → 转换为 `5:20`
2. 运行 `get_code_connect_suggestions(fileKey="8yJDMeWDyBz71EnMOSuUiw", nodeId="5:20")`
3. 响应显示：CheckIcon 组件（未映射）具有颜色和大小属性
4. 在代码库中搜索 CheckIcon：未找到匹配
5. 搜索通用图标组件：找到包含其他图标的 `src/icons/` 目录
6. 向用户报告："我找不到 CheckIcon 组件，但我找到了位于 src/icons/ 的图标目录。您想：
   - 首先创建一个新的 CheckIcon.tsx 组件，然后连接它
   - 连接到不同的现有图标
   - 如果它存在于其他位置，请提供 CheckIcon 的路径"
7. 用户提供路径："src/icons/CheckIcon.tsx"
8. 从文件检测语言和框架
9. 运行 `send_code_connect_mappings(fileKey="8yJDMeWDyBz71EnMOSuUiw", nodeId="5:20", mappings=[{ nodeId: "5:20", componentName: "CheckIcon", source: "src/icons/CheckIcon.tsx", label: "React" }])`

**结果：** CheckIcon 组件成功连接到 Figma 设计。

## 最佳实践

### 主动组件发现

不要只询问用户文件路径 — 主动搜索他们的代码库以找到匹配的组件。这提供了更好的体验并捕获潜在的映射机会。

### 准确的结构匹配

比较 Figma 组件和代码组件时，不要只看名称。检查：

- Props 对齐（变体类型、大小选项等）
- 组件层次结构匹配（嵌套元素）
- 组件服务于相同目的

### 清晰沟通

提供创建映射时，清楚解释：

- 您找到了什么
- 为什么它是好的匹配
- 映射将做什么
- Props 将如何连接

### 处理歧义

如果多个组件可能匹配，请展示选项而不是猜测。让用户对连接哪个组件做出最终决定。

### 优雅降级

如果找不到完全匹配，请提供有用的后续步骤：

- 展示接近的候选
- 建议组件创建
- 请求用户指导

## 常见问题及解决方案

### 问题："此选择中未找到已发布组件"

**原因：** Figma 组件未发布到团队库。Code Connect 仅适用于已发布组件。
**解决方案：** 用户需要将组件发布到 Figma 中的团队库：

1. 在 Figma 中，选择组件或组件集
2. 右键单击并选择 "Publish to library" 或使用 Team Library 发布模态框
3. 发布组件
4. 发布后，使用相同的节点 ID 重试 Code Connect 映射

### 问题："Code Connect 仅在组织和Enterprise计划中可用"

**原因：** 用户的 Figma 计划不包括 Code Connect 访问权限。
**解决方案：** 用户需要升级到组织或Enterprise计划，或联系其管理员。

### 问题：在代码库中未找到匹配组件

**原因：** 代码库搜索未找到具有匹配名称或结构的组件。
**解决方案：** 询问用户组件是否以不同名称存在于其他位置。他们可能需要先创建组件，或者它可能位于意外目录中。

### 问题："未找到已发布组件" (CODE_CONNECT_ASSET_NOT_FOUND)

**原因：** 源文件路径不正确，该位置的组件不存在，或 componentName 与实际导出不匹配。
**解决方案：** 验证源路径是否正确且相对于项目根目录。检查组件是否以确切的 componentName 从文件中正确导出。

### 问题："组件已映射到代码" (CODE_CONNECT_MAPPING_ALREADY_EXISTS)

**原因：** 此组件已存在 Code Connect 映射。
**解决方案：** 组件已连接。如果用户想更新映射，他们可能需要在 Figma 中先删除现有映射。

### 问题："权限不足，无法创建映射" (CODE_CONNECT_INSUFFICIENT_PERMISSIONS)

**原因：** 用户对 Figma 文件或库没有编辑权限。
**解决方案：** 用户需要对包含组件的文件具有编辑访问权限。联系文件所有者或团队管理员。

### 问题：Code Connect 映射因 URL 错误而失败

**原因：** Figma URL 格式不正确或缺少 `node-id` 参数。
**解决方案：** 验证 URL 遵循所需格式：`https://figma.com/design/:fileKey/:fileName?node-id=1-2`。`node-id` 参数是必需的。还要确保在调用工具时将 `1-2` 转换为 `1:2`。

### 问题：找到多个相似组件

**原因：** 代码库包含可能匹配 Figma 组件的多个组件。
**解决方案：** 向用户展示所有候选及其文件路径，让他们选择连接哪个。不同的组件可能在不同上下文中使用（例如，`Button.tsx` 与 `LinkButton.tsx`）。

## 了解 Code Connect

Code Connect 建立设计和代码之间的双向链接：

**对于设计师：** 查看哪个代码组件实现了 Figma 组件
**对于开发人员：** 直接从 Figma 设计导航到实现它们的代码
**对于团队：** 维护组件映射的单一事实来源

您创建的映射通过使这些连接显式和可发现来帮助保持设计和代码同步。

## 其他资源

有关 Code Connect 的更多信息：

- [Code Connect 文档](https://help.figma.com/hc/en-us/articles/23920389749655-Code-Connect)
- [Figma MCP 服务器工具和提示](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/)
