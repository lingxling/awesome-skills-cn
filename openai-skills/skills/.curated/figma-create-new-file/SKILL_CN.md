---
name: figma-create-new-file
description: 创建一个新的空白 Figma 文件。当用户想要创建新的 Figma 设计或 FigJam 文件，或者在调用 use_figma 之前需要新文件时使用。通过 whoami 处理计划解析（如果需要）。用法 — /figma-create-new-file [editorType] [fileName]（例如 /figma-create-new-file figjam 我的白板）
---

# create_new_file — 创建新 Figma 文件

使用 `create_new_file` MCP 工具在用户的草稿文件夹中创建一个新的空白 Figma 文件。通常在需要处理新文件时，在调用 `use_figma` 之前使用。

## 技能参数

此技能接受可选参数：`/figma-create-new-file [editorType] [fileName]`

- **editorType**: `design`（默认）或 `figjam`
- **fileName**: 新文件的名称（默认为 "Untitled"）

示例：
- `/figma-create-new-file` — 创建一个名为 "Untitled" 的设计文件
- `/figma-create-new-file figjam 我的白板` — 创建一个名为 "我的白板" 的 FigJam 文件
- `/figma-create-new-file design 我的新设计` — 创建一个名为 "我的新设计" 的设计文件

从技能调用中解析参数。如果未提供 editorType，默认为 `"design"`。如果未提供 fileName，默认为 `"Untitled"`。

## 工作流程

### 步骤 1：解析 planKey

`create_new_file` 工具需要一个 `planKey` 参数。遵循此决策树：

1. **用户已提供 planKey**（例如，来自之前的 `whoami` 调用或在他们的提示中）→ 直接使用，跳到步骤 2。

2. **没有可用的 planKey** → 调用 `whoami` 工具。响应包含一个 `plans` 数组。每个计划都有一个 `key`、`name`、`seat` 和 `tier`。

   - **单个计划**：自动使用其 `key` 字段。
   - **多个计划**：询问用户他们想在哪个团队或组织中创建文件，然后使用相应计划的 `key`。

### 步骤 2：调用 create_new_file

使用以下参数调用 `create_new_file` 工具：

| 参数    | 必需 | 描述 |
|-------------|----------|-------------|
| `planKey`   | 是      | 来自步骤 1 的计划密钥 |
| `fileName`  | 是      | 新文件的名称 |
| `editorType`| 是      | `"design"` 或 `"figjam"` |

示例：
```json
{
  "planKey": "team:123456",
  "fileName": "我的新设计",
  "editorType": "design"
}
```

### 步骤 3：使用结果

工具返回：
- `file_key` — 新创建文件的密钥
- `file_url` — 在 Figma 中打开文件的直接 URL

将 `file_key` 用于后续的工具调用，如 `use_figma`。

## 重要说明

- 文件是在所选计划的用户的**草稿文件夹**中创建的。
- 仅支持 `"design"` 和 `"figjam"` 编辑器类型。
- 如果下一步是 `use_figma`，在调用之前先加载 `figma-use` 技能。
