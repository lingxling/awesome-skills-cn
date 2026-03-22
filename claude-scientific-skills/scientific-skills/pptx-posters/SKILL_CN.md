---
name: pptx-posters
description: 使用HTML/CSS创建研究海报，可以导出为PDF或PPTX。仅当用户明确请求PowerPoint/PPTX海报格式时使用此技能。对于标准研究海报，请使用latex-posters。此技能提供现代基于网络的海报设计，具有响应式布局和易于视觉集成。
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# PPTX研究海报（基于HTML）

## 概述

**⚠️ 仅当用户明确请求PPTX/POWERPOINT海报格式时使用此技能。**

对于标准研究海报，请使用**latex-posters**技能，它提供更好的排版控制，是学术会议的默认选择。

此技能使用HTML/CSS创建研究海报，然后可以导出为PDF或转换为PowerPoint格式。基于网络的方法提供：
- 现代、响应式布局
- 易于集成AI生成的视觉效果
- 在浏览器中快速迭代和预览
- 通过浏览器打印功能导出为PDF
- 如果特别需要，转换为PPTX

## 何时使用此技能

**仅在以下情况使用此技能：**
- 用户明确请求"PPTX海报"、"PowerPoint海报"或"PPT海报"
- 用户特别要求基于HTML的海报
- 用户需要在创建后在PowerPoint中编辑海报
- LaTeX不可用或用户请求非LaTeX解决方案

**不要在以下情况使用此技能：**
- 用户要求"海报"但未指定格式 → 使用latex-posters
- 用户要求"研究海报"或"会议海报" → 使用latex-posters
- 用户提到LaTeX、tikzposter、beamerposter或baposter → 使用latex-posters

## AI驱动的视觉元素生成

**标准工作流程：在创建HTML海报之前，使用AI生成所有主要视觉元素。**

这是创建视觉上引人注目的海报的推荐方法：
1. 计划所有需要的视觉元素（主图像、介绍、方法、结果、结论）
2. 使用scientific-schematics或Nano Banana Pro生成每个元素
3. 在HTML模板中组装生成的图像
4. 在视觉元素周围添加文本内容

**目标：海报面积的60-70%应该是AI生成的视觉效果，30-40%是文本。**

---

### 关键：海报尺寸字体要求

**⚠️ AI生成的可视化中的所有文本必须是海报可读的。**

为海报生成图形时，您必须在每个提示中包含字体大小规格。海报图形从4-6英尺外观看，因此文本必须大。

**每个海报图形的强制提示要求：**

```
POSTER FORMAT REQUIREMENTS (STRICTLY ENFORCE):
- ABSOLUTE MAXIMUM 3-4 elements per graphic (3 is ideal)
- ABSOLUTE MAXIMUM 10 words total in the entire graphic
- NO complex workflows with 5+ steps (split into 2-3 simple graphics instead)
- NO multi-level nested diagrams (flatten to single level)
- NO case studies with multiple sub-sections (one key point per case)
- ALL text GIANT BOLD (80pt+ for labels, 120pt+ for key numbers)
- High contrast ONLY (dark on white OR white on dark, NO gradients with text)
- MANDATORY 50% white space minimum (half the graphic should be empty)
- Thick lines only (5px+ minimum), large icons (200px+ minimum)
- ONE SINGLE MESSAGE per graphic (not 3 related messages)
```

**⚠️ 生成前：检查您的提示并计算元素**
- 如果您的描述有5+项 → 停止。拆分为多个图形
- 如果您的工作流程有5+阶段 → 停止。只显示3-4个高级步骤
- 如果您的比较有4+方法 → 停止。只显示前3个或我们的vs最佳基线

**示例 - 错误（7阶段工作流程）：**
```bash
# ❌ 创建微小不可读的文本
python scripts/generate_schematic.py "Drug discovery workflow: Stage 1 Target ID, Stage 2 Synthesis, Stage 3 Screening, Stage 4 Lead Opt, Stage 5 Validation, Stage 6 Clinical Trial, Stage 7 FDA Approval with metrics." -o figures/workflow.png
```

**示例 - 正确（3个大型阶段）：**
```bash
# ✅ 相同内容，简化为可读的海报格式
python scripts/generate_schematic.py "POSTER FORMAT for A0. ULTRA-SIMPLE 3-box workflow: 'DISCOVER' → 'VALIDATE' → 'APPROVE'. Each word in GIANT bold (120pt+). Thick arrows (10px). 60% white space. ONLY these 3 words. NO substeps. Readable from 12 feet." -o figures/workflow_simple.png
```

---

### 关键：防止内容溢出

**⚠️ 海报在边缘处不得有文本或内容被截断。**

**预防规则：**

**1. 限制内容部分（最多5-6个部分）：**
```
✅ 良好 - 5个部分，有呼吸空间：
   - 标题/头部
   - 介绍/问题
   - 方法
   - 结果（1-2个关键发现）
   - 结论

❌ 不良 - 8+个部分挤在一起
```

**2. 字数限制：**
- **每个部分**：最多50-100字
- **总海报**：最多300-800字
- **如果您有更多内容**：删除或制作手册

---

## 核心功能

### 1. HTML/CSS海报设计

HTML模板（`assets/poster_html_template.html`）提供：
- 固定海报尺寸（36×48英寸 = 2592×3456点）
- 带有渐变样式的专业头部
- 三列内容布局
- 带有现代样式的基于块的部分
- 带有参考文献和联系信息的页脚

### 2. 海报结构

**标准布局：**
```
┌─────────────────────────────────────────┐
│  HEADER: Title, Authors, Hero Image     │
├─────────────┬─────────────┬─────────────┤
│ Introduction│   Results   │  Discussion │
│             │             │             │
│   Methods   │   (charts)  │ Conclusions │
│             │             │             │
│  (diagram)  │   (data)    │   (summary) │
├─────────────┴─────────────┴─────────────┤
│  FOOTER: References & Contact Info      │
└─────────────────────────────────────────┘
```

### 3. 视觉集成

每个部分应突出显示AI生成的视觉效果：

**主图像（头部）：**
```html
<img src="figures/hero.png" class="hero-image">
```

**部分图形：**
```html
<div class="block">
  <h2 class="block-title">Methods</h2>
  <div class="block-content">
    <img src="figures/workflow.png" class="block-image">
    <ul>
      <li>Brief methodology point</li>
    </ul>
  </div>
</div>
```

### 4. 生成视觉元素

**在创建HTML之前，生成所有视觉元素：**

```bash
# 创建figures目录
mkdir -p figures

# 主图像 - 简单，有冲击力
python scripts/generate_schematic.py "POSTER FORMAT for A0. Hero banner: '[TOPIC]' in HUGE text (120pt+). Dark blue gradient background. ONE iconic visual. Minimal text. Readable from 15 feet." -o figures/hero.png

# 介绍视觉 - 仅3个元素
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE visual with ONLY 3 icons: [icon1] → [icon2] → [icon3]. ONE word labels (80pt+). 50% white space. Readable from 8 feet." -o figures/intro.png

# 方法流程图 - 仅4个步骤
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE flowchart with ONLY 4 boxes: STEP1 → STEP2 → STEP3 → STEP4. GIANT labels (100pt+). Thick arrows. 50% white space. NO sub-steps." -o figures/workflow.png

# 结果可视化 - 仅3个条形
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE bar chart with ONLY 3 bars: BASELINE (70%), EXISTING (85%), OURS (95%). GIANT percentages ON bars (120pt+). NO axis, NO legend. 50% white space." -o figures/results.png

# 结论 - 恰好3个关键发现
python scripts/generate_schematic.py "POSTER FORMAT for A0. EXACTLY 3 cards: '95%' (150pt) 'ACCURACY' (60pt), '2X' (150pt) 'FASTER' (60pt), checkmark 'READY' (60pt). 50% white space. NO other text." -o figures/conclusions.png
```

---

## PPTX海报创建工作流程

### 阶段1：规划

1. **确认明确请求PPTX**
2. **确定海报要求：**
   - 尺寸：36×48英寸（最常见）或A0
   - 方向：纵向（最常见）
3. **制定内容大纲：**
   - 确定1-3个核心信息
   - 计划3-5个视觉元素
   - 起草最少文本（总共300-800字）

### 阶段2：生成视觉元素（AI驱动）

**关键：生成简单的图形，内容最少。**

```bash
mkdir -p figures

# 使用POSTER FORMAT规格生成每个元素
# （见上面第4节中的示例）
```

### 阶段3：创建HTML海报

1. **复制模板：**
   ```bash
   cp skills/pptx-posters/assets/poster_html_template.html poster.html
   ```

2. **更新内容：**
   - 替换占位符标题和作者
   - 插入AI生成的图像
   - 添加最少的支持文本
   - 更新参考文献和联系信息

3. **在浏览器中预览：**
   ```bash
   open poster.html  # macOS
   # 或
   xdg-open poster.html  # Linux
   ```

### 阶段4：导出为PDF

**浏览器打印方法：**
1. 在Chrome或Firefox中打开poster.html
2. 打印（Cmd/Ctrl + P）
3. 选择"保存为PDF"
4. 将纸张大小设置为与海报尺寸匹配
5. 移除边距
6. 启用"背景图形"

**命令行（如果Chrome可用）：**
```bash
# Chrome无头PDF导出
google-chrome --headless --print-to-pdf=poster.pdf \
  --print-to-pdf-no-header \
  --no-margins \
  poster.html
```

### 阶段5：转换为PPTX（如果需要）

**选项1：PDF到PPTX转换**
```bash
# 使用LibreOffice
libreoffice --headless --convert-to pptx poster.pdf

# 或在简单情况下使用在线转换器
```

**选项2：使用python-pptx直接创建PPTX**
```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()
prs.slide_width = Inches(48)
prs.slide_height = Inches(36)

slide = prs.slides.add_slide(prs.slide_layouts[6])  # 空白

# 从figures/添加图像
slide.shapes.add_picture("figures/hero.png", Inches(0), Inches(0), width=Inches(48))
# ... 添加其他元素

prs.save("poster.pptx")
```

---

## HTML模板结构

提供的模板（`assets/poster_html_template.html`）包括：

### 用于自定义的CSS变量

```css
/* 海报尺寸 */
body {
  width: 2592pt;   /* 36 inches */
  height: 3456pt;  /* 48 inches */
}

/* 配色方案 - 自定义这些 */
.header {
  background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 50%, #3182ce 100%);
}

/* 排版 */
.poster-title { font-size: 108pt; }
.authors { font-size: 48pt; }
.block-title { font-size: 52pt; }
.block-content { font-size: 34pt; }
```

### 关键类

| 类 | 用途 | 字体大小 |
|-------|---------|-----------|
| `.poster-title` | 主标题 | 108pt |
| `.authors` | 作者姓名 | 48pt |
| `.affiliations` | 机构 | 38pt |
| `.block-title` | 部分标题 | 52pt |
| `.block-content` | 正文文本 | 34pt |
| `.key-finding` | 突出显示框 | 36pt |

---

## 质量检查表

### 步骤0：生成前审查（必需）

**对于每个计划的图形，验证：**
- [ ] 可以用3-4个项目或更少描述吗？（不是5+）
- [ ] 是简单的工作流程（3-4步骤，不是7+）？
- [ ] 可以用10个单词或更少描述所有文本吗？
- [ ] 它传达一个信息（不是多个）吗？

**拒绝这些模式：**
- ❌ "7阶段工作流程" → 简化为"3个大型阶段"
- ❌ "多个案例研究" → 每个图形一个案例
- ❌ "时间线2015-2024年度" → "仅3个关键年份"
- ❌ "比较6种方法" → "仅2个：我们的vs最佳"

### 步骤2b：生成后审查（必需）

**对于每个25%缩放的生成图形：**

**✅ 通过标准（全部必须为真）：**
- [ ] 可以清楚阅读所有文本
- [ ] 计数：3-4个元素或更少
- [ ] 空白：50%+ 空
- [ ] 2秒内理解
- [ ] 不是复杂的5+阶段工作流程
- [ ] 不是多个嵌套部分

**❌ 失败标准（如果任何为真，重新生成）：**
- [ ] 文本小/难以阅读 → 使用"150pt+"重新生成
- [ ] 超过4个元素 → 重新生成"仅3个元素"
- [ ] 少于50%空白 → 重新生成"60%空白"
- [ ] 复杂多阶段 → 拆分为2-3个图形
- [ ] 多个案例拥挤 → 拆分为单独的图形

### 导出后

- [ ] 在任何4个边缘没有内容被截断（仔细检查）
- [ ] 所有图像正确显示
- [ ] 颜色渲染符合预期
- [ ] 文本在25%比例下可读
- [ ] 图形看起来简单（不像复杂的7阶段工作流程）

---

## 要避免的常见陷阱

**AI生成的图形错误：**
- ❌ 太多元素（10+项）→ 最多保持3-5项
- ❌ 文本太小 → 在提示中指定"巨大（100pt+）"
- ❌ 没有空白 → 在每个提示中添加"50%空白"
- ❌ 复杂流程图（8+步骤）→ 限制为4-5步骤

**HTML/导出错误：**
- ❌ 内容超出海报尺寸 → 在浏览器中检查溢出
- ❌ PDF中缺少背景图形 → 在打印设置中启用
- ❌ PDF中纸张尺寸错误 → 完全匹配海报尺寸
- ❌ 低分辨率图像 → 使用最低300 DPI

**内容错误：**
- ❌ 文本过多（超过1000字）→ 减少到300-800字
- ❌ 部分过多（7+）→ 合并为5-6个
- ❌ 没有清晰的视觉层次结构 → 使关键发现突出

---

## 与其他技能的集成

此技能与以下技能配合使用：
- **Scientific Schematics**：生成所有海报图表和流程图
- **Generate Image / Nano Banana Pro**：创建风格化图形和主图像
- **LaTeX Posters**：海报创建的默认技能（除非明确请求PPTX，否则使用此技能）

---

## 模板资产

在`assets/`目录中可用：

- `poster_html_template.html`：主要HTML海报模板（36×48英寸）
- `poster_quality_checklist.md`：提交前验证检查表

## 参考

在`references/`目录中可用：

- `poster_content_guide.md`：内容组织和写作指南
- `poster_design_principles.md`：排版、色彩理论和视觉层次结构
- `poster_layout_design.md`：布局原则和网格系统