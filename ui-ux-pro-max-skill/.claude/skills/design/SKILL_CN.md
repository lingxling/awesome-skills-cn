---
name: ckm:design
description: "全面的设计技能：品牌标识、设计令牌、UI样式、标志生成（55种风格，Gemini AI）、企业标识计划（50个交付物，CIP模型）、HTML演示文稿（Chart.js）、横幅设计（22种风格，社交/广告/网络/印刷）、图标设计（15种风格，SVG，Gemini 3.1 Pro）、社交照片（HTML→截图，多平台）。操作：设计标志、创建CIP、生成模型、构建幻灯片、设计横幅、生成图标、创建社交照片、社交媒体图像、品牌标识、设计系统。平台：Facebook、Twitter、LinkedIn、YouTube、Instagram、Pinterest、TikTok、Threads、Google Ads。"
argument-hint: "[设计类型] [上下文]"
license: MIT
metadata:
  author: claudekit
  version: "2.1.0"
---

# 设计

统一设计技能：品牌、令牌、UI、标志、CIP、幻灯片、横幅、社交照片、图标。

## 何时使用

- 品牌标识、声音、资产
- 设计系统令牌和规范
- 使用shadcn/ui + Tailwind的UI样式
- 标志设计和AI生成
- 企业标识计划（CIP）交付物
- 演示文稿和宣传幻灯片
- 社交媒体、广告、网络、印刷的横幅设计
- Instagram、Facebook、LinkedIn、Twitter、Pinterest、TikTok的社交照片

## 子技能路由

| 任务 | 子技能 | 详情 |
|------|--------|------|
| 品牌标识、声音、资产 | `brand` | 外部技能 |
| 令牌、规范、CSS变量 | `design-system` | 外部技能 |
| shadcn/ui、Tailwind、代码 | `ui-styling` | 外部技能 |
| 标志创建、AI生成 | 标志（内置） | `references/logo-design.md` |
| CIP模型、交付物 | CIP（内置） | `references/cip-design.md` |
| 演示文稿、宣传幻灯片 | 幻灯片（内置） | `references/slides.md` |
| 横幅、封面、标题 | 横幅（内置） | `references/banner-sizes-and-styles.md` |
| 社交媒体图像/照片 | 社交照片（内置） | `references/social-photos-design.md` |
| SVG图标、图标集 | 图标（内置） | `references/icon-design.md` |

## 标志设计（内置）

55+ 种风格，30个调色板，25个行业指南。Gemini Nano Banana模型。

### 标志：生成设计简报

```bash
python3 ~/.claude/skills/design/scripts/logo/search.py "tech startup modern" --design-brief -p "BrandName"
```

### 标志：搜索风格/颜色/行业

```bash
python3 ~/.claude/skills/design/scripts/logo/search.py "minimalist clean" --domain style
python3 ~/.claude/skills/design/scripts/logo/search.py "tech professional" --domain color
python3 ~/.claude/skills/design/scripts/logo/search.py "healthcare medical" --domain industry
```

### 标志：用AI生成

**始终**生成白色背景的输出标志图像。

```bash
python3 ~/.claude/skills/design/scripts/logo/generate.py --brand "TechFlow" --style minimalist --industry tech
python3 ~/.claude/skills/design/scripts/logo/generate.py --prompt "coffee shop vintage badge" --style vintage
```

**重要：** 当脚本失败时，尝试直接修复它们。

生成后，**始终**通过`AskUserQuestion`询问用户关于HTML预览的问题。如果是，调用`/ui-ux-pro-max`查看图库。

## CIP设计（内置）

50+ 交付物，20种风格，20个行业。Gemini Nano Banana（Flash/Pro）。

### CIP：生成简报

```bash
python3 ~/.claude/skills/design/scripts/cip/search.py "tech startup" --cip-brief -b "BrandName"
```

### CIP：搜索域

```bash
python3 ~/.claude/skills/design/scripts/cip/search.py "business card letterhead" --domain deliverable
python3 ~/.claude/skills/design/scripts/cip/search.py "luxury premium elegant" --domain style
python3 ~/.claude/skills/design/scripts/cip/search.py "hospitality hotel" --domain industry
python3 ~/.claude/skills/design/scripts/cip/search.py "office reception" --domain mockup
```

### CIP：生成模型

```bash
# 带标志（推荐）
python3 ~/.claude/skills/design/scripts/cip/generate.py --brand "TopGroup" --logo /path/to/logo.png --deliverable "business card" --industry "consulting"

# 完整CIP集
python3 ~/.claude/skills/design/scripts/cip/generate.py --brand "TopGroup" --logo /path/to/logo.png --industry "consulting" --set

# Pro模型（4K文本）
python3 ~/.claude/skills/design/scripts/cip/generate.py --brand "TopGroup" --logo logo.png --deliverable "business card" --model pro

# 无标志
python3 ~/.claude/skills/design/scripts/cip/generate.py --brand "TechFlow" --deliverable "business card" --no-logo-prompt
```

模型：`flash`（默认，`gemini-2.5-flash-image`），`pro`（`gemini-3-pro-image-preview`）

### CIP：渲染HTML演示文稿

```bash
python3 ~/.claude/skills/design/scripts/cip/render-html.py --brand "TopGroup" --industry "consulting" --images /path/to/cip-output
```

**提示：** 如果没有标志，请先使用上面的标志设计部分。

## 幻灯片（内置）

带有Chart.js、设计令牌、文案公式的战略性HTML演示文稿。

加载`references/slides-create.md`获取创建工作流程。

### 幻灯片：知识库

| 主题 | 文件 |
|------|------|
| 创建指南 | `references/slides-create.md` |
| 布局模式 | `references/slides-layout-patterns.md` |
| HTML模板 | `references/slides-html-template.md` |
| 文案 | `references/slides-copywriting-formulas.md` |
| 策略 | `references/slides-strategies.md` |

## 横幅设计（内置）

跨社交、广告、网络、印刷的22种艺术指导风格。使用`frontend-design`、`ai-artist`、`ai-multimodal`、`chrome-devtools`技能。

加载`references/banner-sizes-and-styles.md`获取完整的尺寸和风格参考。

### 横幅：工作流程

1. **收集需求** 通过`AskUserQuestion` — 目的、平台、内容、品牌、风格、数量
2. **研究** — 激活`ui-ux-pro-max`，浏览Pinterest获取参考
3. **设计** — 使用`frontend-design`创建HTML/CSS横幅，使用`ai-artist`/`ai-multimodal`生成视觉效果
4. **导出** — 通过`chrome-devtools`以准确尺寸截图为PNG
5. **展示** — 并排显示所有选项，根据反馈迭代

### 横幅：快速尺寸参考

| 平台 | 类型 | 尺寸（像素） |
|------|------|-------------|
| Facebook | 封面 | 820 x 312 |
| Twitter/X | 标题 | 1500 x 500 |
| LinkedIn | 个人 | 1584 x 396 |
| YouTube | 频道艺术 | 2560 x 1440 |
| Instagram | 故事 | 1080 x 1920 |
| Instagram | 帖子 | 1080 x 1080 |
| Google Ads | 中等矩形 | 300 x 250 |
| 网站 | 标题 | 1920 x 600-1080 |

### 横幅：顶级艺术风格

| 风格 | 最适合 |
|------|--------|
| 极简主义 | SaaS、科技 |
| 大胆排版 | 公告 |
| 渐变 | 现代品牌 |
| 基于照片 | 生活方式、电子商务 |
| 几何 | 科技、金融科技 |
| 玻璃态 | SaaS、应用 |
| 霓虹/赛博朋克 | 游戏、活动 |

### 横幅：设计规则

- 安全区域：关键内容位于中央70-80%
- 每个横幅一个号召性用语，右下角，最小44px高度
- 最多2种字体，最小16px正文，≥32px标题
- 广告文本低于20%（Meta会惩罚）
- 印刷：300 DPI，CMYK，3-5mm出血

## 图标设计（内置）

15种风格，12个类别。Gemini 3.1 Pro Preview生成SVG文本输出。

### 图标：生成单个图标

```bash
python3 ~/.claude/skills/design/scripts/icon/generate.py --prompt "settings gear" --style outlined
python3 ~/.claude/skills/design/scripts/icon/generate.py --prompt "shopping cart" --style filled --color "#6366F1"
python3 ~/.claude/skills/design/scripts/icon/generate.py --name "dashboard" --category navigation --style duotone
```

### 图标：生成批量变体

```bash
python3 ~/.claude/skills/design/scripts/icon/generate.py --prompt "cloud upload" --batch 4 --output-dir ./icons
```

### 图标：多尺寸导出

```bash
python3 ~/.claude/skills/design/scripts/icon/generate.py --prompt "user profile" --sizes "16,24,32,48" --output-dir ./icons
```

### 图标：顶级风格

| 风格 | 最适合 |
|------|--------|
| outlined | UI界面、网络应用 |
| filled | 移动应用、导航栏 |
| duotone | 营销、着陆页 |
| rounded | 友好应用、健康 |
| sharp | 科技、金融科技、企业 |
| flat | 材料设计、Google风格 |
| gradient | 现代品牌、SaaS |

**模型：** `gemini-3.1-pro-preview` — 纯文本输出（SVG是XML文本）。无需图像生成API。

## 社交照片（内置）

多平台社交图像设计：HTML/CSS → 截图导出。使用`ui-ux-pro-max`、`brand`、`design-system`、`chrome-devtools`技能。

加载`references/social-photos-design.md`获取尺寸、模板、最佳实践。

### 社交照片：工作流程

1. **编排** — `project-management`技能用于TODO任务；并行子代理用于独立工作
2. **分析** — 解析提示：主题、平台、风格、品牌上下文、内容元素
3. **构思** — 3-5个概念，通过`AskUserQuestion`展示
4. **设计** — `/ckm:brand` → `/ckm:design-system` → 随机调用`/ck:ui-ux-pro-max`或`/ck:frontend-design`；每个创意×尺寸的HTML
5. **导出** — `chrome-devtools`或Playwright以准确像素截图（2x设备缩放因子）
6. **验证** — 使用Chrome MCP或`chrome-devtools`技能视觉检查导出的设计；修复布局/样式问题并重新导出
7. **报告** — 向`plans/reports/`提交设计决策摘要
8. **组织** — 调用`assets-organizing`技能对输出文件和报告进行排序

### 社交照片：关键尺寸

| 平台 | 尺寸（像素） | 平台 | 尺寸（像素） |
|------|-------------|------|-------------|
| IG帖子 | 1080×1080 | FB帖子 | 1200×630 |
| IG故事 | 1080×1920 | X帖子 | 1200×675 |
| IG轮播 | 1080×1350 | LinkedIn | 1200×627 |
| YT缩略图 | 1280×720 | Pinterest | 1000×1500 |

## 工作流程

### 完整品牌包

1. **标志** → `scripts/logo/generate.py` → 生成标志变体
2. **CIP** → `scripts/cip/generate.py --logo ...` → 创建交付物模型
3. **演示文稿** → 加载`references/slides-create.md` → 构建宣传幻灯片

### 新设计系统

1. **品牌**（品牌技能）→ 定义颜色、排版、声音
2. **令牌**（设计系统技能）→ 创建语义令牌层
3. **实施**（ui-styling技能）→ 配置Tailwind、shadcn/ui

## 参考

| 主题 | 文件 |
|------|------|
| 设计路由 | `references/design-routing.md` |
| 标志设计指南 | `references/logo-design.md` |
| 标志风格 | `references/logo-style-guide.md` |
| 标志颜色 | `references/logo-color-psychology.md` |
| 标志提示 | `references/logo-prompt-engineering.md` |
| CIP设计指南 | `references/cip-design.md` |
| CIP交付物 | `references/cip-deliverable-guide.md` |
| CIP风格 | `references/cip-style-guide.md` |
| CIP提示 | `references/cip-prompt-engineering.md` |
| 幻灯片创建 | `references/slides-create.md` |
| 幻灯片布局 | `references/slides-layout-patterns.md` |
| 幻灯片模板 | `references/slides-html-template.md` |
| 幻灯片文案 | `references/slides-copywriting-formulas.md` |
| 幻灯片策略 | `references/slides-strategies.md` |
| 横幅尺寸和风格 | `references/banner-sizes-and-styles.md` |
| 社交照片指南 | `references/social-photos-design.md` |
| 图标设计指南 | `references/icon-design.md` |

## 脚本

| 脚本 | 用途 |
|------|------|
| `scripts/logo/search.py` | 搜索标志风格、颜色、行业 |
| `scripts/logo/generate.py` | 用Gemini AI生成标志 |
| `scripts/logo/core.py` | 标志数据的BM25搜索引擎 |
| `scripts/cip/search.py` | 搜索CIP交付物、风格、行业 |
| `scripts/cip/generate.py` | 用Gemini生成CIP模型 |
| `scripts/cip/render-html.py` | 从CIP模型渲染HTML演示文稿 |
| `scripts/cip/core.py` | CIP数据的BM25搜索引擎 |
| `scripts/icon/generate.py` | 用Gemini 3.1 Pro生成SVG图标 |

## 设置

```bash
export GEMINI_API_KEY="your-key"  # https://aistudio.google.com/apikey
pip install google-genai pillow
```

## 集成

**外部子技能：** brand、design-system、ui-styling
**相关技能：** frontend-design、ui-ux-pro-max、ai-multimodal、chrome-devtools