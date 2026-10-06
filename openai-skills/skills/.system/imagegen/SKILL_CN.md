---
name: "imagegen"
description: "当任务能从AI生成的位图视觉效果中获益时（例如照片、插图、纹理、精灵图、样图或透明背景裁切图），生成或编辑栅格图像。当Codex应该创建一个全新的图像、转换现有图像，或从参考图中衍生出视觉变体，并且输出应为位图资源而非仓库原生代码或矢量图时使用。当任务更适合通过编辑现有的SVG/矢量/代码原生资源、扩展已有的图标或徽标体系，或直接在HTML/CSS/canvas中构建视觉效果时，不要使用此技能。"
---

# 图像生成技能

为当前项目生成或编辑图像（例如网站资源、游戏资源、UI样图、产品样图、线框图、徽标设计、照片级真实感图像或信息图）。

## 顶层模式与规则

该技能恰好有两种顶层模式：

- **默认内置工具模式（首选）：** 内置的 `image_gen` 工具，用于常规的图像生成和编辑。不需要 `OPENAI_API_KEY`。
- **回退CLI模式（仅在明确要求时使用）：** `scripts/image_gen.py` CLI。仅当用户明确要求使用CLI路径时使用。需要 `OPENAI_API_KEY`。

仅在明确的CLI回退模式下，该CLI提供三个子命令：

- `generate`
- `edit`
- `generate-batch`

规则：
- 默认情况下，对所有常规图像生成和编辑请求使用内置的 `image_gen` 工具。
- 永远不要自动切换到CLI回退模式。
- 如果内置工具失败或不可用，告知用户存在CLI回退方案，并说明它需要 `OPENAI_API_KEY`。只有在用户明确要求使用该回退方案时才继续。
- 如果用户明确要求使用CLI模式，则使用附带的 `scripts/image_gen.py` 工作流。不要创建一次性的SDK运行器。
- 永远不要修改 `scripts/image_gen.py`。如果缺少某些内容，在采取任何其他行动之前先询问用户。

内置保存路径策略：
- 在内置工具模式下，Codex默认将生成的图像保存在 `$CODEX_HOME/*` 下。
- 不要将操作系统临时目录描述为或依赖其作为默认的内置目标路径。
- 不要描述或依赖内置 `image_gen` 工具上的目标路径参数（如果有的话）。如果需要特定位置，先生成，然后将所选输出从 `$CODEX_HOME/generated_images/...` 移动或复制过去。
- 内置模式下的保存路径优先级：
  1. 如果用户指定了目标位置，将所选输出移动或复制到那里。
  2. 如果图像是供当前项目使用的，在完成之前将最终选定的图像移动或复制到工作区中。
  3. 如果图像仅用于预览或头脑风暴，则内联渲染它；底层文件可以保留在默认的 `$CODEX_HOME/*` 路径下。
- 永远不要让一个被项目引用的资源只存在于默认的 `$CODEX_HOME/*` 路径下。
- 除非用户明确要求替换，否则不要覆盖现有资源；而是创建一个带版本号的同级文件名，例如 `hero-v2.png` 或 `item-icon-edited.png`。

两种模式共享的提示词指导位于 `references/prompting.md` 和 `references/sample-prompts.md`。

CLI模式专属的文档/资源（仅回退模式使用）：
- `references/cli.md`
- `references/image-api.md`
- `references/codex-network.md`
- `scripts/image_gen.py`

## 何时使用
- 生成一张新图像（概念艺术、产品照、封面、网站主图）
- 使用一张或多张参考图像来确定风格、构图或氛围，生成新图像
- 编辑现有图像（内绘、光照或天气变换、背景替换、物体移除、合成、透明背景）
- 为一项任务生成多个资源或变体

## 何时不使用
- 扩展或匹配仓库内已有的SVG/矢量图标集、徽标体系或插图库
- 创建更适合直接用SVG、HTML/CSS或canvas生成的简单形状、图表、线框图或图标
- 当源文件已经以可编辑的原生格式存在时，进行小型的项目本地资源编辑
- 任何用户明显希望得到确定性的代码原生输出而非生成式位图的任务

## 决策树

考虑两个独立的问题：

1. **意图：** 这是一张新图像还是对现有图像的编辑？
2. **执行策略：** 这是一个资源还是多个资源/变体？

意图：
- 如果用户想要在保留部分内容的同时修改现有图像，将请求视为**编辑**。
- 如果用户仅将图像作为风格、构图、氛围或主体指导的参考提供，将请求视为**生成**。
- 如果用户没有提供任何图像，将请求视为**生成**。

内置编辑语义：
- 内置编辑模式适用于已经在对话上下文中可见的图像，例如附件图像或线程中先前生成的图像。
- 如果用户想用内置工具编辑一个本地图像文件，先用内置的 `view_image` 工具加载它，使图像在对话上下文中可见，然后再进行内置编辑流程。
- 不要承诺通过内置工具可以进行任意文件系统路径的编辑。
- 如果本地文件仍需要直接的文件路径控制、蒙版或其他显式的仅CLI参数，仅在用户要求时使用显式的CLI回退方案。
- 对于编辑，默认要积极地保留不变量，并以非破坏性方式保存。

执行策略：
- 在内置默认路径中，通过为每个请求的资源或变体发出一次 `image_gen` 调用来生成多个资源或变体。
- 在显式的CLI回退路径中，仅当用户明确选择了CLI模式且需要大量提示词/资源时，才使用CLI的 `generate-batch` 子命令。

除非用户明确要求更改现有图像，否则假定用户想要一张新图像。

## 工作流程
1. 决定顶层模式：默认内置模式，仅在明确要求时才使用回退CLI模式。
2. 决定意图：`generate`（生成）还是 `edit`（编辑）。
3. 决定输出是仅供预览，还是供当前项目使用。
4. 决定执行策略：单个资源 vs 重复的内置调用 vs CLI的 `generate-batch`。
5. 预先收集输入：提示词、确切的文本（逐字）、约束/避免事项列表，以及任何输入图像。
6. 对每张输入图像，明确标注其角色：
   - 参考图像
   - 编辑目标
   - 辅助插入/风格/合成输入
7. 如果编辑目标仅存在于本地文件系统，并且你仍在使用内置路径，先用 `view_image` 检查它，使图像在对话上下文中可用。
8. 如果用户要求的是照片、插图、精灵图、产品图、横幅或其他明确的栅格风格资源，使用 `image_gen` 而不要用SVG/HTML/CSS占位符替代。如果请求的是应该匹配仓库现有原生SVG/矢量/代码资源的图标、徽标或UI图形，优先直接编辑那些资源。
9. 根据具体程度调整提示词：
   - 如果用户的提示词已经具体详尽，将其规范化为一个清晰的规格说明，不要添加创作性要求。
   - 如果用户的提示词比较笼统，仅在能实质性提升输出质量时，才做有节制的增补。
10. 默认使用内置的 `image_gen` 工具。
11. 只有当用户明确选择CLI回退方案时，才使用仅限回退模式的文档来处理质量、`input_fidelity`、蒙版、输出格式、输出路径和网络设置。
12. 检查并验证输出：主体、风格、构图、文本准确性以及不变量/避免事项。
13. 以单次有针对性的修改进行迭代，然后重新检查。
14. 对于仅供预览的工作，内联渲染图像；底层文件可以保留在默认的 `$CODEX_HOME/generated_images/...` 路径下。
15. 对于面向项目的工作，将选定的产物移动或复制到工作区中，并更新任何使用它的代码或引用。永远不要让一个被项目引用的资源只存在于默认的 `$CODEX_HOME/generated_images/...` 路径下。
16. 对于批量生成，除非用户明确要求保留被舍弃的变体，否则只在工作区中保留被选中的最终版本。
17. 始终报告任何面向工作区资源的最终保存路径，以及最终使用的提示词，并说明使用的是内置工具还是回退CLI模式。

## 提示词增强

将用户的提示词重新整理成一个结构化、面向生产的规格说明。使用户的目标更清晰、更可执行，但不要盲目添加细节。

将此视为提示词塑形指导，而非一个封闭的架构。只使用有帮助的行，并在能实质性提升清晰度时添加一行简短的额外标注。

### 具体程度策略

用用户提示词的具体程度来决定适当的增补量：

- 如果提示词已经具体详尽，保留这种具体性，只做规范化/结构化处理。
- 如果提示词比较笼统，在能实质性改善结果时，可以做有节制的增补。

允许的增补：
- 构图或取景提示
- 润色程度或预期用途提示
- 实用的版式指导
- 支撑既定请求的合理场景具体化

不允许的增补：
- 请求中未暗示的额外人物或物体
- 未被暗示的品牌名称、口号、调色板或叙事情节
- 除非周围布局支持，否则任意特定方位的放置

## 用例分类（精确标识符）

将每个请求归类到以下某个类别中，并在提示词和参考文件中保持该标识符的一致性。

生成：
- photorealistic-natural — 具有真实质感和自然光照的纪实/编辑类生活场景。
- product-mockup — 产品/包装照片、目录图像、周边概念图。
- ui-mockup — 应用/网页界面样图和线框图；指定所需的精细度。
- infographic-diagram — 带有结构化布局和文本的图表/信息图。
- logo-brand — 徽标/标志探索，适配矢量化。
- illustration-story — 漫画、童书插画、叙事场景。
- stylized-concept — 风格驱动的概念艺术、3D/风格化渲染。
- historical-scene — 符合时代特征/世界知识的场景。

编辑：
- text-localization — 翻译/替换图像内文本，保留布局。
- identity-preserve — 试穿、人物置入场景；锁定脸部/身体/姿势。
- precise-object-edit — 移除/替换某个具体元素（包括内部替换）。
- lighting-weather — 仅改变时间/季节/氛围。
- background-extraction — 透明背景/干净的裁切图。
- style-transfer — 在改变主体/场景的同时应用参考风格。
- compositing — 多图像插入/合并，并匹配光照/视角。
- sketch-to-render — 将草图/线稿转为照片级真实感渲染。

## 共享提示词架构

将以下带标签的规格说明作为两种顶层模式共享的提示词脚手架：

```text
Use case: <taxonomy slug>
Asset type: <where the asset will be used>
Primary request: <user's main prompt>
Input images: <Image 1: role; Image 2: role> (optional)
Scene/backdrop: <environment>
Subject: <main subject>
Style/medium: <photo/illustration/3D/etc>
Composition/framing: <wide/close/top-down; placement>
Lighting/mood: <lighting + mood>
Color palette: <palette notes>
Materials/textures: <surface details>
Text (verbatim): "<exact text>"
Constraints: <must keep/must avoid>
Avoid: <negative constraints>
```

说明：
- `Asset type` 和 `Input images` 是提示词脚手架，不是专用的CLI标志。
- `Scene/backdrop` 指的是视觉场景设定。它与回退CLI的 `background` 参数不同，后者控制的是输出的透明度行为。
- 诸如 `Quality:`、`Input fidelity:`、蒙版、输出格式和输出路径等仅限回退模式的执行说明，只属于显式CLI路径。不要将它们当作内置 `image_gen` 工具的参数。

增补规则：
- 保持简短。
- 只添加能实质性改善提示词所需的细节。
- 对于编辑，明确列出不变量（`change only X; keep Y unchanged`）。
- 如果缺少任何阻碍成功的关键细节，就提出一个问题；否则继续进行。

## 示例

### 生成示例（主图）
```text
Use case: product-mockup
Asset type: landing page hero
Primary request: a minimal hero image of a ceramic coffee mug
Style/medium: clean product photography
Composition/framing: wide composition with usable negative space for page copy if needed
Lighting/mood: soft studio lighting
Constraints: no logos, no text, no watermark
```

### 编辑示例（不变量）
```text
Use case: precise-object-edit
Asset type: product photo background replacement
Primary request: replace only the background with a warm sunset gradient
Constraints: change only the background; keep the product and its edges unchanged; no text; no watermark
```

## 提示词最佳实践
- 将提示词结构化为场景/背景 -> 主体 -> 细节 -> 约束。
- 包含预期用途（广告、UI样图、信息图），以确定模式和润色程度。
- 对于照片级真实感，使用摄影机/构图相关的语言。
- 只有在用户明确要求矢量输出或非图像占位符时，才使用SVG/矢量替代方案。
- 引用确切的文本并指定版式和位置。
- 对于棘手的词语，逐字拼写，并要求逐字渲染。
- 对于多图像输入，按索引引用图像并描述它们应如何被使用。
- 对于编辑，每次迭代都重复不变量，以减少漂移。
- 以单次改动的后续请求进行迭代。
- 如果提示词比较笼统，只添加能实质性帮助的额外细节。
- 如果提示词已经很详细，对其进行规范化而不是扩展它。
- 仅针对显式CLI回退模式，关于 `quality`、`input_fidelity`、蒙版、输出格式和输出路径的指导，请参阅 `references/cli.md` 和 `references/image-api.md`。

两种模式共享的更多原则：`references/prompting.md`。
两种模式共享的可复制粘贴规格说明：`references/sample-prompts.md`。

## 按资源类型的指导
资源类型模板（网站资源、游戏资源、线框图、徽标）汇总在 `references/sample-prompts.md` 中。

## 仅限回退CLI模式

### 临时文件和输出约定
这些约定仅适用于显式的CLI回退模式。它们不描述内置 `image_gen` 的输出行为。
- 将 `tmp/imagegen/` 用于中间文件（例如JSONL批次）；完成后删除它们。
- 将最终产物写入 `output/imagegen/` 下。
- 使用 `--out` 或 `--out-dir` 来控制输出路径；保持文件名稳定且具描述性。

### 依赖项
在本仓库中优先使用 `uv` 进行依赖管理。

必需的Python包：
```bash
uv pip install openai
```

仅用于缩小图像尺寸的可选依赖：
```bash
uv pip install pillow
```

可移植性说明：
- 如果你在本仓库之外使用已安装的技能，请用其包管理器将依赖项安装到该环境中。
- 在由uv管理的环境中，`uv pip install ...` 仍是首选路径。

### 环境
- 实时API调用必须设置 `OPENAI_API_KEY`。
- 使用内置的 `image_gen` 工具时，不要向用户询问 `OPENAI_API_KEY`。
- 永远不要要求用户在聊天中粘贴完整的密钥。请他们在本地设置好并在准备好后确认。

如果缺少密钥，给用户以下步骤：
1. 在OpenAI平台UI中创建一个API密钥：https://platform.openai.com/api-keys
2. 在他们的系统中将 `OPENAI_API_KEY` 设置为环境变量。
3. 如有需要，主动引导他们为其操作系统/shell设置该环境变量。

如果在当前环境中无法安装，告知用户缺少哪个依赖以及如何将其安装到他们的活动环境中。

### 脚本模式说明
- CLI命令和示例：`references/cli.md`
- API参数快速参考：`references/image-api.md`
- CLI模式的网络批准/沙箱设置：`references/codex-network.md`

## 参考文件索引
- `references/prompting.md`：两种模式共享的提示词原则。
- `references/sample-prompts.md`：两种模式共享的可复制粘贴提示词方案。
- `references/cli.md`：仅限回退模式，通过 `scripts/image_gen.py` 使用CLI。
- `references/image-api.md`：仅限回退模式的API/CLI参数参考。
- `references/codex-network.md`：仅限回退模式，CLI模式下的网络/沙箱故障排查。
- `scripts/image_gen.py`：仅限回退模式的CLI实现。除非用户明确选择CLI模式，否则不要加载或使用它。
