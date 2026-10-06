---
name: hatch-pet
description: 根据角色美术、生成的图像、公司或潜在客户的品牌线索或视觉参考，创建、修复、验证、进行视觉 QA 并打包兼容 Codex 的动画宠物及宠物精灵图集（spritesheet）。当用户需要轻量级 worker 的 Codex 宠物工作流、非像素风格的自定义宠物、潜在客户或公司的吉祥物宠物，或者包含透明未使用单元格、QA 联系表（contact sheet）以及 pet.json 打包的完整 8x9 动画宠物图集时使用。本技能组合调用已安装的 $imagegen 系统技能进行视觉生成，并使用内置脚本进行确定性的精灵图集组装。
---

# Hatch Pet

## 概述

根据一个概念、品牌线索、公司/潜在客户名称、一张或多张参考图像，或这些输入的任意组合，创建兼容 Codex 的动画宠物。该工作流保留了确定性的 hatch-pet 流水线来处理图集几何、验证、视觉 QA 和打包，同时使用简洁的、针对各状态的提示词，并允许任何适合宠物的视觉风格。

面向用户的输入都是可选的。如果用户省略了宠物名称，则从概念、品牌、公司或参考文件名中推断一个；如果无法推断，则选择一个简短友好的名字。如果用户省略了描述，则从概念或参考中推断。如果用户省略了参考图像，则先根据文本生成基础宠物，然后将该基础图作为每个动画行的规范参考。

## 生成委托

所有常规视觉生成均使用 `$imagegen`。

在生成基础美术、行条带（row strip）或修复行之前，加载并遵循已安装的图像生成技能：

```text
${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/SKILL.md
```

不要直接调用 Image API、图像 CLI 或任何其他图像生成路径。让 `$imagegen` 自行选择其内置优先路径和回退规则。如果 `$imagegen` 表示某个回退需要确认，请在继续之前询问用户。

调用 `$imagegen` 时，将生成的宠物提示词作为权威视觉规范传入。宠物提示词应保持简洁、针对具体状态、面向精灵图制作，并以所列的输入图像为依据。将较长的策略和 QA 规则保留在本技能和确定性审查脚本中，而不是展开到每个图像提示词里。不要将提示词包装进通用的 `$imagegen` 共享提示词模式中。

本技能的脚本仅用于确定性的图像工作：准备布局指南和提示词、镜像已批准的 `running-left`、提取帧、验证行、合成最终图集，以及创建联系表和动作预览 QA 媒体。由父代理负责的 shell/`jq` 步骤处理清单更新、打包和清理。

## 存储控制

内置的 `$imagegen` 路径会把生成的 PNG 字节存储在调用它的 rollout 中，即使它同时也会在 `${CODEX_HOME:-$HOME/.codex}/generated_images` 下写入文件。之后删除文件可以减少文件系统占用，但无法缩小已经写入的 rollout。请保持图像生成隔离且有界：

- 每个视觉任务使用一个轻量级生成 worker。不要将多个基础/行任务批量放进同一个 worker。
- Worker 只能返回 `selected_source=...` 和 `qa_note=...`；它们的最终回复中不得包含 Markdown 图像预览、base64 或额外的视觉附件。
- 父代理不得逐一以视觉方式打开每个生成的 PNG。对每个任务使用 worker QA，并且只检查最终的联系表。
- 将选中的生成输出复制到 `decoded/` 后，如果选中的原始文件位于 `${CODEX_HOME:-$HOME/.codex}/generated_images` 中，则删除它，并在可能时删除其已变为空的生成目录。
- 对于对存储敏感的完整运行，询问用户是否在可用时使用 `$imagegen` CLI 回退。该路径需要本地 API 凭证和用户的明确确认，但可以避免内置图像负载被嵌入到 rollout 事件中。

## 品牌调研

如果用户提供的是品牌、公司、产品或潜在客户名称，而不是具体的形象描述或参考图像，则在准备宠物运行之前运行一个轻量级调研子代理。调研 worker 必须使用网络搜索，并优先使用官方来源，例如品牌网站、产品页面、文档、关于页面、新闻页面或品牌页面。仅当官方页面信息过少时才使用可信的二手来源。保持搜索范围狭窄：足以提取视觉和个性线索即可，而不是一份市场调研简报。

当用户已经提供了具体的吉祥物/形象描述或参考图像时，跳过调研，除非用户明确要求进行品牌研究。

调研 worker 的职责：

- 在网上搜索 2-4 个相关来源，优先选择官方页面
- 编写一份自适应的 markdown 简报，而不是僵硬的字段堆砌
- 涵盖身份/类别、受众/使用场景、视觉体系、个性/语气、产品/领域母题、吉祥物转化线索、需避免的内容，以及证据/置信度
- 将从来源推断出的吉祥物指导标注为推断
- 避免复制标志、可读标记、UI 截图、口号或文字
- 以一个紧凑的 `Generation handoff` 部分结尾，其中仅包含 `brand_name`、`brand_brief`、`avatar_seed`、`avoid` 和 `brand_sources`
- 不要生成图像、准备运行文件夹或编辑无关文件

使用以下调研 worker 提示词：

```text
Research a brand for hatch-pet mascot creation.

Brand/product/prospect: <brand name>
User context: <short user request>
Output file: <absolute path to brand-discovery.md>

Use web search. Prefer official brand, product, docs, about, press, or brand pages. Use reputable secondary sources only if official sources are too thin. Write an adaptive markdown brief to the output file. Headings may flex by brand, but the brief must cover:
- identity/category: canonical name, product type, what it does
- audience/use context: who it serves and where it appears
- visual system: palette, shapes, line quality, materials, typography feel, iconography, patterns
- personality/tone: emotional traits, energy, formality, playfulness
- product/domain motifs: objects, workflows, verbs, metaphors, environments
- mascot translation cues: candidate forms, signature traits, props, what must read at pet size
- avoidances: logos/text, trademark-sensitive elements, misleading cues, competitor confusion, poor mascot fits
- evidence/confidence: source URLs plus notes where evidence is weak or inferred

Do not copy logos, readable marks, UI screenshots, slogans, or text. Clearly label mascot guidance that is inferred rather than directly sourced.

End the brief with a `Generation handoff` section containing exactly:
- brand_name=<canonical brand/product name>
- brand_brief=<one sentence, max 45 words, covering palette/tone/domain motifs/personality>
- avatar_seed=<short mascot-safe visual idea, no logo copying>
- avoid=<short comma-separated list>
- brand_sources=<comma-separated source URLs>

Return exactly:
brand_discovery_file=<absolute output file path>
brand_name=<canonical brand/product name>
brand_brief=<same compact sentence from Generation handoff>
avatar_seed=<same short seed from Generation handoff>
avoid=<same short avoid list from Generation handoff>
brand_sources=<same comma-separated URLs from Generation handoff>
```

父代理应在准备运行之前保存该 markdown 简报，然后将其作为 `--brand-discovery-file` 传给 `prepare_pet_run.py`，同时传入 `--brand-name`、`--brand-brief`、重复的 `--brand-source`，以及在用户未提供更好的形象描述时基于 `avatar_seed` 的简洁 `--pet-notes` 值。保留完整简报以供审阅；只有紧凑的交接字段才应影响提示词。如果网络搜索不可用且用户只给出了一个光秃秃的品牌名称，请在生成之前询问品牌线索。

对于一次常规的宠物运行，预计最多有 10 个视觉生成任务：1 个基础宠物加 9 个行条带任务。Codex 应用契约目前使用全部 9 个状态：`idle`、`running-right`、`running-left`、`waving`、`jumping`、`failed`、`waiting`、`running` 和 `review`。唯一的确定性视觉派生是 `running-left`，它只有在 `running-right` 已经生成、经过视觉检查并被明确批准为可安全镜像之后，才可以通过镜像 `running-right` 得到。如果不适合镜像，则将 `running-left` 作为一个常规的、有依据的 `$imagegen` 行来生成。

选定一个视觉输出后，父代理将该图像原样复制到该任务的 `decoded/` 路径中，并在 `imagegen-jobs.json` 中将任务标记为完成。不要编写填充行输出的辅助脚本。确定性的 Python 脚本只能处理已经生成的视觉输出。

只有基础任务可以仅凭提示词生成。每个通过 `$imagegen` 生成的行条带任务都必须使用 `imagegen-jobs.json` 中列出的输入图像，包括在复制选定的基础输出之后创建的规范基础参考。任何未附带依据图像的行生成都应视为无效。

## 适合宠物的风格

默认风格为 `auto`：从用户的提示词和参考中推断宠物的风格，然后在每一行中保持该风格。如果用户指定了某种风格，则遵从它。支持的风格预设包括 `pixel`、`plush`、`clay`、`sticker`、`flat-vector`、`3d-toy`、`painterly`、`brand-inspired` 和 `auto`。

只要保持适合宠物，任何风格都可以接受：

- 紧凑的全身剪影，在 `192x208` 单元格内清晰可辨
- 所有行中的面部、比例、材质、调色板和道具保持一致
- 干净、可去除的色度键（chroma-key）背景
- 细节足够大，在宠物尺寸下也能看清
- 不含文字、标签、UI 或可读标志，除非用户明确提供了经批准的参考美术并要求包含它们

非像素风格同样是一等公民。毛绒、黏土、贴纸、矢量、3D 玩具、绘画风吉祥物、水墨以及受品牌启发的外观，只要满足图集和可读性约束，都应被接受。

## 透明度与特效

宠物行会被处理成透明的 `192x208` 单元格，因此每个生成的像素要么属于宠物精灵，要么是可以干净去除的色度键背景。优先通过姿势、表情和剪影的变化来表达，而不是装饰性特效。

确定性栅格流水线负责保证透明度不变量：变为完全透明的像素会被规范化，使其不保留隐藏的 RGB 残留；如果导出的文件违反该不变量，图集验证应当失败。不要通过接受视觉上不一致的输出来掩盖彩色光晕或透明像素残留。

允许的特效必须同时满足以下所有条件：

- 特效与状态相关，有助于说明动画。
- 特效在物理上依附于、接触或重叠宠物剪影，而不是漂浮在附近。
- 特效位于与宠物相同的帧槽内，不会形成单独的精灵组件。
- 特效不透明、边缘足够硬以便干净提取，并使用非色度键颜色。
- 特效足够小，在 `192x208` 下仍可辨认且不显杂乱。

默认避免以下内容，因为它们通常会破坏透明背景清理或组件提取：

- 挥手标记、运动弧线、速度线、动作条纹、残影、模糊或拖影
- 分离的星星、零散的闪光、漂浮的标点、漂浮的图标、下落的泪滴、分离的烟云或零散的灰尘
- 投射阴影、接触阴影、下落阴影、椭圆形地面阴影、地面色块、落地痕迹、冲击爆发、发光、光环、光晕或柔和的透明特效
- 文字、标签、帧编号、可见网格、指示标记、对话气泡、思维气泡、UI 面板、代码片段、棋盘格透明背景、白色背景、黑色背景或场景
- 宠物、道具、特效、高光或阴影中出现接近色度键的颜色
- 杂散像素、断开的轮廓碎片、斑点/噪点、被裁切的身体部位、重叠的姿势，或任何越过相邻帧槽的姿势

各状态的具体指导：

- `idle`：保持平静、低干扰。只使用细微的呼吸、轻微的眨眼、头部或身体的轻微起伏、非常小的材质摆动，或其他安静且保持角色设定的动作。循环中仍必须包含可见的微小变化；不要接受六个实际上完全相同的副本。不要表现挥手、走路、跑步、跳跃、说话、工作、审阅、情绪反应、大幅手势、与物品互动或新道具。
- `waving`：仅通过爪子、手、翅膀或肢体的姿势来表现挥手。不要在手势周围绘制挥手标记、运动弧线、线条、闪光、符号或漂浮特效。
- `jumping`：仅通过身体位置表现垂直运动。不要绘制阴影、灰尘、落地痕迹、冲击爆发、弹跳垫或地面提示。
- `failed`：如果遵守允许特效的规则，可以使用眼泪、依附的烟雾团或依附的星星；不要使用红色 X 标记、漂浮符号、分离的烟雾、分离的星星或单独的泪滴。
- `waiting`：通过期待的、询问式的姿势表现 Codex 需要批准、帮助或用户输入。使其与普通的 idle 和 review 区分开。
- `running`：表现正在进行的任务工作、处理、思考、扫描、打字或专注努力。不要表现字面意义上的用脚跑步、慢跑、冲刺、跑步机运动、抬膝、大步、摆臂、定向移动、速度线、尘云、地面阴影、运动轨迹或分离的运动特效。
- `review`：通过前倾、眨眼、眼神、歪头或爪子/手的位置来表现专注。不要添加放大镜、纸张、代码、UI、标点、符号或其他新道具，除非它们本来就属于基础宠物的身份设定。
- `running-right` 和 `running-left`：仅通过身体、肢体和道具的运动来表现定向的拖拽移动。`running-right` 必须面向右方并向右移动；`running-left` 必须面向左方并向左移动。它们的步伐节奏必须在循环中明显交替，而不是重复一个几乎静止的步幅。不要绘制速度线、尘云、地面阴影、运动轨迹或分离的运动特效。

## 可见的进度计划

对于每次宠物运行，保持一个可见的检查清单，让用户能看到工作进展到了哪里。在开始前创建清单，同一时间只保持一个步骤处于活动状态，并在每个步骤完成时更新它。

对于常规的宠物运行使用以下清单，将 `<Pet>` 替换为宠物名称或 `your pet`：

1. 正在准备 `<Pet>`。
2. 正在构想 `<Pet>` 的主要外观。
3. 正在描绘 `<Pet>` 的姿势。
4. 正在孵化 `<Pet>`。

每个步骤的含义：

- `正在准备 <Pet>。` 选择或确认宠物名称、描述、源图像、风格预设、风格说明和工作文件夹。对于只有品牌/产品/公司名称的请求，先运行品牌调研 worker，并获取紧凑的品牌简报、来源 URL 和形象种子。
- `正在构想 <Pet> 的主要外观。` 生成宠物的主参考图像。它将成为视觉上的唯一事实来源。
- `正在描绘 <Pet> 的姿势。` 通过轻量级 worker 生成姿势行，先从 `idle` 和 `running-right` 开始，以确认身份和步态。只有当 `running-right` 翻转后明显可用时，才镜像得到 `running-left`。
- `正在孵化 <Pet>。` 将已批准的姿势转换为最终的宠物文件，审阅联系表、预览和验证结果，修复任何损坏的部分，保存 `pet.json` 和 `spritesheet.webp`，然后报告输出路径。

只有当真实的文件、图像或决定已经存在时，才将步骤标记为完成。如果这是一次修复运行，则从第一个相关步骤开始，而不是重新开始整个清单。

## 默认工作流

1. 准备一个宠物运行文件夹和 imagegen 任务清单：

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/hatch-pet"
python "$SKILL_DIR/scripts/prepare_pet_run.py" \
  --pet-name "<Name>" \
  --description "<one sentence>" \
  --reference /absolute/path/to/reference.png \
  --output-dir /absolute/path/to/run \
  --pet-notes "<stable pet description>" \
  --brand-discovery-file /absolute/path/to/brand-discovery.md \
  --brand-name "<optional researched brand name>" \
  --brand-brief "<optional compact researched brand cue sentence>" \
  --brand-source "https://example.com/source" \
  --style-preset auto \
  --style-notes "<optional freeform style notes>" \
  --force
```

上述所有参数都是可选的，除了表达用户约束所需的标志。对于纯文本请求，通过 `--pet-notes` 传入概念并省略 `--reference`；`prepare_pet_run.py` 会根据需要推断名称、描述、色度键和输出目录。
对于仅有品牌的请求，先运行调研 worker，保存 markdown 简报，然后通过 `--brand-discovery-file` 传入简报路径，通过 `--pet-notes` 传入 `avatar_seed`，通过 `--brand-name` 传入 `brand_name`，通过 `--brand-brief` 传入 `brand_brief`，并通过重复的 `--brand-source` 传入每个来源 URL。

2. 检查 `imagegen-jobs.json` 中接下来可执行的 `$imagegen` 任务。当一个任务的 `status` 不是 `complete` 且 `depends_on` 中的每个 id 都已完成时，该任务即为就绪。优先直接用 `jq` 或编辑器读取清单，而不是添加用于显示状态的辅助脚本：

```bash
jq '.jobs[] | {id, kind, status, depends_on, prompt_file, retry_prompt_file, input_images, output_path, derivation_policy}' /absolute/path/to/run/imagegen-jobs.json
```

3. 默认使用轻量级 worker 生成视觉任务：

- 首先使用一个轻量级基础 worker 生成并复制 `base`。
- 接着生成并复制 `idle` 和 `running-right`，作为身份和步态检查，每行使用一个轻量级 worker。
- 检查 `running-right`；只有当视觉身份、道具位置、标记、光照和方向语义都保持正确时，才镜像得到 `running-left`。
- 当镜像会改变含义或身份时，使用轻量级 worker 正常生成 `running-left`。
- 使用轻量级 worker 生成其余各行，并使用每个任务列出的全部输入图像。

对于每个就绪的视觉任务，使用 `imagegen-jobs.json` 中列出的提示词文件、每个列出的输入图像及其角色标签来调用 `$imagegen`，并使用默认的内置 `image_gen` 路径，除非 `$imagegen` 自身另行路由。父代理必须尽量减少自身的图像处理：不要在父 rollout 中打开每个生成的基础图或行。Worker 只返回选定的源路径和一句话的 QA 说明；父代理将选定的源路径记录到清单中。

`prepare_pet_run.py` 会在 `references/layout-guides/` 下创建 9 张针对各行的布局指南图像，每个动画状态一张。行任务会将匹配的指南作为仅用于布局的输入附上，以便模型遵循正确的帧数、间距、居中和安全边距。将这些指南视为不可见的构造参考：生成的行条带中不得包含可见的方框、边框、中心标记、标签、指南颜色或指南背景。

生成行条带时，以行提示词中的身份锁定为准。保持与规范基础图相同的风格、面部、标记、调色板、材质、道具设计、身体比例和剪影。行任务默认附带布局指南和规范基础图；解码后的基础图保存在运行文件夹中用于确定性处理，而不是作为冗余的生成输入发送。

如果 `$imagegen` 对某一行返回传输层的 `Bad Request`，则使用为其生成的 `retry_prompt_file` 对同一行重试一次。重试提示词保留了行 id、帧数、色度键、规范基础身份和状态动作。保持规范基础图附带。如果重试仍然失败，则停止并报告失败的行及提示词路径，而不是切换到任何其他生成路径。

4. 为某个任务选定生成输出后，将其复制到解码输出路径并将任务标记为完成。对于 `base`，还要创建规范身份参考：

```bash
RUN_DIR=/absolute/path/to/run
JOB_ID=<job-id>
SOURCE=/absolute/path/to/generated-output.png
OUTPUT_REL=$(jq -r --arg id "$JOB_ID" '.jobs[] | select(.id == $id) | .output_path' "$RUN_DIR/imagegen-jobs.json")
mkdir -p "$(dirname "$RUN_DIR/$OUTPUT_REL")"
cp "$SOURCE" "$RUN_DIR/$OUTPUT_REL"
```

```bash
if [ "$JOB_ID" = "base" ]; then mkdir -p "$RUN_DIR/references"; cp "$RUN_DIR/$OUTPUT_REL" "$RUN_DIR/references/canonical-base.png"; fi
```

```bash
UPDATED_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)
TMP_MANIFEST=$(mktemp)
jq --arg id "$JOB_ID" --arg source "$SOURCE" --arg at "$UPDATED_AT" '(.jobs[] | select(.id == $id)) += {status: "complete", source_path: $source, completed_at: $at}' "$RUN_DIR/imagegen-jobs.json" > "$TMP_MANIFEST"
mv "$TMP_MANIFEST" "$RUN_DIR/imagegen-jobs.json"
```

如果复制的源文件位于 `${CODEX_HOME:-$HOME/.codex}/generated_images` 下，则在解码副本存在后删除原始生成文件：

```bash
GENERATED_ROOT="${CODEX_HOME:-$HOME/.codex}/generated_images"
case "$SOURCE" in
  "$GENERATED_ROOT"/*)
    rm -f "$SOURCE"
    rmdir "$(dirname "$SOURCE")" 2>/dev/null || true
    ;;
esac
```

5. 仅在视觉上安全时才派生 `running-left`：

```bash
python "$SKILL_DIR/scripts/derive_running_left_from_running_right.py" \
  --run-dir /absolute/path/to/run \
  --confirm-appropriate-mirror \
  --decision-note "<why mirroring preserves this pet's identity>"
```

该脚本会原地镜像每个生成的帧槽，使向左的行保留向右行的时间顺序。不要用会反转动画时序的整条带镜像来替代它。

6. 所有任务完成后，直接运行图像处理脚本：

```bash
RUN_DIR=/absolute/path/to/run
mkdir -p "$RUN_DIR/final" "$RUN_DIR/qa"
```

```bash
python "$SKILL_DIR/scripts/extract_strip_frames.py" \
  --decoded-dir "$RUN_DIR/decoded" \
  --output-dir "$RUN_DIR/frames" \
  --states all \
  --method auto
```

```bash
python "$SKILL_DIR/scripts/inspect_frames.py" \
  --frames-root "$RUN_DIR/frames" \
  --json-out "$RUN_DIR/qa/review.json" \
  --require-components
```

```bash
python "$SKILL_DIR/scripts/compose_atlas.py" \
  --frames-root "$RUN_DIR/frames" \
  --output "$RUN_DIR/final/spritesheet.png" \
  --webp-output "$RUN_DIR/final/spritesheet.webp"
```

```bash
python "$SKILL_DIR/scripts/validate_atlas.py" \
  "$RUN_DIR/final/spritesheet.webp" \
  --json-out "$RUN_DIR/final/validation.json"
```

```bash
python "$SKILL_DIR/scripts/make_contact_sheet.py" \
  "$RUN_DIR/final/spritesheet.webp" \
  --output "$RUN_DIR/qa/contact-sheet.png"
```

```bash
python "$SKILL_DIR/scripts/render_animation_previews.py" \
  --frames-root "$RUN_DIR/frames" \
  --output-dir "$RUN_DIR/qa/previews"
```

如果预览 GIF 显示出由逐帧适配单元格提取导致的尺寸跳变或基线跳动，而原始行条带本身的缩放和位置是稳定的，则使用显式的行稳定模式重新运行帧提取，然后重新运行检查、图集合成、验证、联系表生成和预览：

```bash
python "$SKILL_DIR/scripts/extract_strip_frames.py" \
  --decoded-dir "$RUN_DIR/decoded" \
  --output-dir "$RUN_DIR/frames" \
  --states all \
  --method stable-slots
```

```bash
python "$SKILL_DIR/scripts/inspect_frames.py" \
  --frames-root "$RUN_DIR/frames" \
  --json-out "$RUN_DIR/qa/review.json" \
  --require-components \
  --allow-stable-slots
```

将 `stable-slots` 作为一种由 QA 驱动的有意修正，而不是默认选项。它应当减少由提取引起的动作跳变，同时不掩盖被裁切的宽姿势或糟糕的源条带。

清理前的预期输出：

```text
run/
  pet_request.json
  imagegen-jobs.json
  prompts/
  decoded/
  frames/frames-manifest.json
  final/spritesheet.webp
  final/validation.json
  qa/contact-sheet.png
  qa/previews/*.gif
  qa/review.json
  qa/run-summary.json
```

打包输出默认写入运行目录之外。如果设置了 `CODEX_HOME`，则使用它；否则使用 `$HOME/.codex`。

```text
${CODEX_HOME:-$HOME/.codex}/pets/<pet-name>/
  pet.json
  spritesheet.webp
```

使用 shell 和 `jq` 打包：

```bash
RUN_DIR=/absolute/path/to/run
PET_ID=$(jq -r '.pet_id' "$RUN_DIR/pet_request.json")
DISPLAY_NAME=$(jq -r '.display_name' "$RUN_DIR/pet_request.json")
DESCRIPTION=$(jq -r '.description' "$RUN_DIR/pet_request.json")
PET_DIR="${CODEX_HOME:-$HOME/.codex}/pets/$PET_ID"
mkdir -p "$PET_DIR"
cp "$RUN_DIR/final/spritesheet.webp" "$PET_DIR/spritesheet.webp"
jq -n --arg id "$PET_ID" --arg displayName "$DISPLAY_NAME" --arg description "$DESCRIPTION" '{id: $id, displayName: $displayName, description: $description, spritesheetPath: "spritesheet.webp"}' > "$PET_DIR/pet.json"
```

打包后写入 `qa/run-summary.json`：

```bash
jq -n --arg run_dir "$RUN_DIR" --arg spritesheet "$RUN_DIR/final/spritesheet.webp" --arg validation "$RUN_DIR/final/validation.json" --arg contact_sheet "$RUN_DIR/qa/contact-sheet.png" --arg review "$RUN_DIR/qa/review.json" --arg package "$PET_DIR" '{ok: true, run_dir: $run_dir, spritesheet: $spritesheet, validation: $validation, contact_sheet: $contact_sheet, review: $review, package: $package}' > "$RUN_DIR/qa/run-summary.json"
```

完成确定性图像处理后，在接受宠物之前，使用一个轻量级视觉 QA worker 检查 `qa/contact-sheet.png` 和 `qa/previews/*.gif`。确定性验证是必要的，但并不充分。如果任何一行意外地改变了物种/体型、面部、标记、调色板、材质、道具设计、风格、道具所在的一侧或整体剪影，则阻止接受。动作预览还必须拒绝非预期的尺寸跳变、反向或停滞的定向步伐节奏、错误的朝向，以及技术上有差异但视觉上毫无动静的 idle 循环。

模型视觉 QA 接受联系表后，删除中间运行产物：

保留 `pet_request.json`、`final/spritesheet.webp`、`final/validation.json`、`qa/contact-sheet.png`、`qa/previews/`、`qa/review.json` 和 `qa/run-summary.json`。删除生成的提示词文件、布局指南、解码后的行条带、提取的帧、`final/spritesheet.png` 以及 imagegen 任务清单。当用户需要调试产物或运行仍需修复时，跳过清理。

## 轻量级视觉 Worker

默认对图像密集型工作使用轻量级子代理。这样可以将每次 `$imagegen` rollout 限制为一张选定的图像，使联系表的视觉负载不进入父线程，并在保留完整 9 状态应用契约的同时降低成本。

## 子代理委托

除非用户明确禁止，否则本次运行应使用子代理。如果用户尚未允许使用子代理，或对子代理使用的意图不明确，则请求用户允许生成子代理以并行处理工作。

父代理的职责：

- 当用户只提供品牌/产品/公司/潜在客户名称时，在准备之前运行品牌调研 worker
- 准备运行并检查 `imagegen-jobs.json`
- 将基础任务、行任务和最终联系表 QA 分配给轻量级 worker
- 将选定的 worker 输出复制到其解码路径中，并在 `imagegen-jobs.json` 中将任务标记为完成
- 根据选定的基础输出创建 `references/canonical-base.png`
- 在合适时运行已批准的 `running-left` 镜像派生
- 运行确定性图像处理、打包、修复重新生成和清理

基础 worker 的职责：

- 仅处理 `base` 任务
- 读取 `prompts/base-pet.md` 并使用列出的所有参考图像
- 仅使用 `$imagegen`
- 将提示词中任何紧凑的品牌灵感行视为宽泛的视觉/个性指导，不复制标志、可读标记、UI 截图、口号或文字
- 仅返回 `selected_source=/absolute/path/to/selected-output.png` 和 `qa_note=<one sentence>`

行 worker 的职责：

- 只处理恰好一个行任务
- 读取行提示词并使用所有列出的输入图像
- 仅使用 `$imagegen`；不要在本地绘制、编辑、平铺或合成精灵
- 对帧数、身份、色度背景、间距、裁切和分离特效进行快速视觉合理性检查
- 执行行提示词中的透明度和特效规则，包括：不得有分离特效，`waving` 不得有挥手标记，定向奔跑行不得有速度线或灰尘，非定向的 `running` 行不得出现字面意义上的用脚跑步，并且只有在状态提示词允许时才可使用依附的、不透明的、精灵风格的眼泪/烟雾/星星
- 仅返回 `selected_source=/absolute/path/to/selected-output.png` 和 `qa_note=<one sentence>`

最终视觉 QA worker 的职责：

- 检查 `qa/contact-sheet.png` 以及 `qa/previews/` 下的各行 GIF，必要时将 `qa/review.json` 和 `final/validation.json` 作为文本上下文
- 验证全部 9 行都符合 Codex 应用的状态契约，且是同一个宠物身份
- 返回紧凑的结果：`visual_qa=pass` 或 `visual_qa=fail`，失败时附上针对各行的修复说明
- 不要编辑文件、排队修复、打包或清理

Worker 的模型选择：

- 品牌调研优先使用较小但能力足够的模型，因为它返回的是紧凑的研究简报，而不是进行编排。
- 视觉 worker 优先使用较小但能力足够的模型，例如在可覆盖模型时使用中等推理强度的 `gpt-5.4-mini`。
- 仅在编排时或没有更小的 worker 模型可用时，才使用父代理/默认模型。
- 同时最多保持两个生成 worker 处于活动状态，除非用户明确要求更高的并行度。在确定性图像处理之后，以单个 worker 运行最终视觉 QA。在 worker 的结果被使用后关闭它们。

使用以下基础 worker 提示词：

```text
Generate the hatch-pet base image.

Run dir: <absolute run dir>
Job id: base
Prompt file: <absolute base prompt file>
Input images:
- <absolute path> — <role>

Use $imagegen only. Read the base prompt and attach every listed input image. If the prompt contains brand inspiration, use it only as broad mascot-safe guidance; do not copy logos, readable marks, UI screenshots, slogans, or text. Before returning, visually check that the result is one centered full-body pet on a flat chroma background, with no text, scenery, shadows, or detached effects.

Do not edit manifests, copy into decoded, mark jobs complete, generate rows, run image-processing scripts, repair, package, or open unrelated files.
Do not include Markdown image previews, base64, or extra attachments in the final response.

Return exactly:
selected_source=/absolute/path/to/selected-output.png
qa_note=<one sentence>
```

使用以下行 worker 提示词：

```text
Generate one hatch-pet row.

Run dir: <absolute run dir>
Row id: <row-id>
Prompt file: <absolute prompt file>
Retry prompt file: <absolute retry prompt file>
Input images:
- <absolute path> — <role>
- <absolute path> — <role>

Use $imagegen only. Read the row prompt and attach every listed input image. If imagegen returns Bad Request, retry once with the retry prompt and the same input images.

Before returning, visually check: exact frame count, same pet identity as canonical base, flat chroma background, complete separated unclipped poses, and no detached effects or guide marks. The prompt's transparency and effects rules are mandatory: no detached effects, no wave marks for `waving`, no speed lines or dust for directional running rows, no literal foot-running for the non-directional `running` row, and only attached opaque sprite-like tears/smoke/stars when allowed by the state prompt.

Do not edit manifests, copy into decoded, mark jobs complete, mirror rows, run image-processing scripts, repair, package, or open unrelated files.
Do not include Markdown image previews, base64, or extra attachments in the final response.

Return exactly:
selected_source=/absolute/path/to/selected-output.png
qa_note=<one sentence>
```

使用以下最终视觉 QA worker 提示词：

```text
Visually QA one finalized hatch-pet contact sheet.

Run dir: <absolute run dir>
Contact sheet: <absolute run dir>/qa/contact-sheet.png
Preview dir: <absolute run dir>/qa/previews
Review JSON: <absolute run dir>/qa/review.json
Validation JSON: <absolute run dir>/final/validation.json

Inspect the contact sheet and the preview GIFs visually. Confirm the same pet identity, style, palette, silhouette, face, proportions, and props across all rows:
0 idle, 1 running-right, 2 running-left, 3 waving, 4 jumping, 5 failed, 6 waiting, 7 running, 8 review.

Fail rows with identity drift, missing/blank frames, copied guide marks, white/nontransparent backgrounds, cropped bodies, slot overlap, detached effects, shadows/glows/smears/dust, chroma-key artifacts, motion that does not match the row state, unintended size popping, wrong facing direction, reversed or non-alternating gait, or idle loops that are effectively static.

Do not edit files, queue repairs, package, clean up, or inspect unrelated files.

Return exactly:
visual_qa=pass|fail
qa_note=<one sentence summary>
repair_rows=<comma-separated row ids, or none>
repair_notes=<short row-specific notes, or none>
```

## 修复工作流

如果帧检查或最终视觉 QA 失败，读取 `qa/review.json`，重新生成最小的失败范围，将替换行复制到相同的解码输出路径中，并保持该任务标记为完成，同时更新 `source_path` 和 `completed_at`。修复失败的行，而不是整张图集。

对于身份修复，使用规范基础图、原始参考、联系表以及确切的行失败说明作为依据上下文。向行 worker 提供现有的行提示词，加上来自 `qa/review.json` 的简短修复说明；保持规范的宠物身份和所选风格。

对于由提取引起的动作跳变，不要首先重新生成图像。如果源条带已经保持了行级的缩放和基线，则使用 `--method stable-slots` 重新运行确定性流水线，使用 `--allow-stable-slots` 进行检查，然后重新检查预览 GIF。只有当原始条带本身被裁切、不稳定或语义错误时，才重新生成该行。

## 规则

- 将 `$imagegen` 保持为主要的生成层。
- 对于没有具体形象描述或参考图像的品牌/产品/公司/潜在客户请求，在生成基础图之前运行品牌调研，并只将紧凑的简报传入运行。
- 将 `$imagegen` 作为唯一的视觉生成层。不要在本技能中调用图像 API、图像 CLI、本地栅格生成器或一次性生成脚本。
- 只要所选路径支持参考图，就为 `$imagegen` 保持参考图像附带/可见。
- 为每个行条带任务附上该行的 `references/layout-guides/<state>.png` 图像作为仅用于布局的指南，并且不接受复制了指南像素的输出。
- 默认使用轻量级视觉 worker 进行基础图生成、行条带视觉生成和最终联系表 QA；父代理负责清单更新、确定性图像脚本、打包和清理。
- 使用 `$imagegen` 生成每个常规视觉任务：基础图以及所有未被明确批准为 `running-left` 镜像派生的行条带。
- 只有基础任务有资格仅凭提示词生成；每个行任务都必须附上其列出的依据图像。
- 先生成 `running-right`，再决定 `running-left` 是否可以镜像。
- 当镜像 `running-left` 时，保持帧顺序和时序语义；通过确定性脚本派生，而不是对整条带进行整体镜像。
- 不要从其他状态派生或复用 `waiting`、`running`、`failed`、`review`、`jumping` 或 `waving`；它们各自具有不同的应用语义，必须作为独立的行生成。
- 永远不要用本地绘制、平铺、变换或代码生成的行条带来替代缺失的 `$imagegen` 输出。
- 只有在选定的输出已复制到解码输出路径之后，才将视觉任务标记为完成。
- 不要依赖生成的图像来获得精确的图集几何；使用本技能的确定性图像脚本。
- 使用存储在 `pet_request.json` 中的色度键；不要强制使用固定的绿幕。
- 在所有行中保持宠物的剪影、面部、材质、调色板、风格和道具一致。
- 即使 `qa/review.json` 和 `final/validation.json` 没有错误，也要将视觉身份或风格漂移视为阻断问题。
- 将显示出裁切的参考、重复的图块、白色单元格背景或非精灵碎片的联系表视为失败。
- 将显示出由提取引起的尺寸跳变、反向的定向时序、错误朝向或毫无动静的 idle 循环的预览 GIF 视为失败。
- 将包含被禁止的分离特效、接近色度键的伪影、阴影、发光、拖影、灰尘、落地痕迹、挥手标记、速度线或运动轨迹的行视为失败。
- 将 `qa/review.json` 中的错误视为阻断问题。警告需要进行视觉审查。

## 验收标准

- 最终图集为 PNG 或 WebP 格式，尺寸 `1536x1872`，支持透明，并基于 `192x208` 单元格。
- 已使用的单元格非空，未使用的单元格完全透明。
- 图集遵循 `references/animation-rows.md` 中的行/帧数量。
- 联系表和逐行动作预览已生成，并已由轻量级视觉 QA worker 检查。
- `qa/review.json` 没有错误。
- 逐行审查确认动画循环足够完整，可用于 Codex 应用。
- 动作预览没有出现非预期的尺寸跳变、反向的定向步伐节奏或错误的行语义。
- 非像素风格只要在宠物尺寸下可辨认且在各行之间保持一致，即可接受。
- 对于自定义宠物，`${CODEX_HOME:-$HOME/.codex}/pets/<pet-name>/pet.json` 和 `${CODEX_HOME:-$HOME/.codex}/pets/<pet-name>/spritesheet.webp` 被一起放置到位。
