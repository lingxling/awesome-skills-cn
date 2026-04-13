---
name: latex-posters
description: "使用LaTeX的beamerposter、tikzposter或baposter创建专业研究海报。支持会议演示、学术海报和科学交流。包括布局设计、配色方案、多列格式、图形集成和海报特定的视觉交流最佳实践。"
allowed-tools: Read Write Edit Bash
---

# LaTeX研究海报

## 概述

研究海报是会议、研讨会和学术活动中科学交流的关键媒介。该技能提供使用LaTeX包创建专业、视觉吸引力研究海报的综合指导。生成具有适当布局、排版、配色方案和视觉层次的出版质量海报。

## 何时使用此技能

在以下情况下应使用此技能：
- 为会议、研讨会或海报环节创建研究海报
- 为大学活动或论文答辩设计学术海报
- 准备用于公众参与的研究可视化摘要
- 将科学论文转换为海报格式
- 为研究小组或部门创建模板海报
- 设计符合特定会议尺寸要求（A0、A1、36×48英寸等）的海报
- 构建具有复杂多列布局的海报
- 在海报格式中集成图形、表格、方程和引文

## AI驱动的视觉元素生成

**标准工作流程：在创建LaTeX海报之前，使用AI生成所有主要视觉元素。**

这是创建视觉吸引力海报的推荐方法：
1. 规划所需的所有视觉元素（标题、引言、方法、结果、结论）
2. 使用scientific-schematics或Nano Banana Pro生成每个元素
3. 在LaTeX模板中组装生成的图像
4. 在视觉周围添加文本内容

**目标：海报面积的60-70%应为AI生成的视觉效果，30-40%为文本。**

---

### 关键：防止内容溢出

**⚠️ 海报不得在边缘处截断文本或内容。**

**常见溢出问题：**
1. **标题/页脚文本超出页面边界**
2. **太多部分挤在可用空间中**
3. **图形放置太靠近边缘**
4. **文本块超出列宽**

**预防规则：**

**1. 限制内容部分（A0最多5-6个部分）：**
```
✅ 好 - 5个部分，有呼吸空间：
   - 标题/页眉
   - 引言/问题
   - 方法
   - 结果（1-2个关键发现）
   - 结论

❌ 坏 - 8+个部分挤在一起：
   - 概述、引言、背景、方法、
   - 结果1、结果2、讨论、结论、未来工作
```

**2. 在LaTeX中设置安全边距：**
```latex
% tikzposter - 添加慷慨边距
\documentclass[25pt, a0paper, portrait, margin=25mm]{tikzposter}

% baposter - 确保内容不接触边缘
\begin{poster}{
  columns=3,
  colspacing=2em,           % 列之间的间距
  headerheight=0.1\textheight,  % 较小的页眉
  % 在底部留出空间
}
```

**3. 图形大小 - 永远不要100%宽度：**
```latex
% 在图形周围留出边距
\includegraphics[width=0.85\linewidth]{figure.png}  % 不是1.0\linewidth
```

**4. 在打印前检查溢出：**
```bash
# 以100%缩放编译并检查PDF
pdflatex poster.tex

# 查找：
# - 任何边缘处截断的文本
# - 接触页面边界的内容
# - .log文件中的overfull hbox警告
grep -i "overfull" poster.log
```

**5. 字数限制：**
- **A0海报**：最多300-800字
- **每部分**：最多50-100字
- **如果您有更多内容**：删除或制作传单

---

### 关键：海报尺寸字体要求

**⚠️ AI生成的可视化中的所有文本必须海报可读。**

为海报生成图形时，您必须在每个提示中包含字体大小规范。海报图形从4-6英尺远观看，因此文本必须很大。

**⚠️ 常见问题：内容溢出和密度**

AI生成海报图形的#1问题是**内容太多**。这导致：
- 文本超出边界
- 不可读的小字体
- 拥挤、压倒性的视觉效果
- 白色空间使用不佳

**解决方案：生成具有最少内容的简单图形。**

**每个海报图形的强制提示要求：**

```
海报格式要求（严格执行）：
- 每个图形绝对最多3-4个元素（3个最理想）
- 整个图形绝对最多10个单词
- 没有5个以上步骤的复杂工作流程（改为2-3个简单图形）
- 没有多级嵌套图表（展平到单级）
- 没有多个子部分的案例研究（每个案例一个关键点）
- 所有文本巨大粗体（标签80pt+，关键数字120pt+）
- 仅高对比度（深色在白色上或白色在深色上，带有文本的渐变）
- 强制最少50%白色空间（图形的一半应为空）
- 仅粗线（5px+最小），大图标（200px+最小）
- 每个图形一个单一消息（不是3个相关消息）
```

**⚠️ 生成前：审查您的提示并计算元素**
- 如果您的描述有5+项 → 停止。拆分为多个图形
- 如果您的工作流程有5+个阶段 → 停止。仅显示3-4个高级步骤
- 如果您的比较有4+个方法 → 停止。仅显示前3个或我们的方法与最佳基线

**每种图形类型的内容限制（严格）：**
| 图形类型 | 最大元素 | 最大字数 | 拒绝如果 | 好的示例 |
|--------------|--------------|-----------|-----------|--------------|
| 流程图 | **3-4个框MAX** | **8个字** | 5+个阶段、嵌套步骤 | "DISCOVER → VALIDATE → APPROVE"（3个字） |
| 关键发现 | **3项MAX** | **9个字** | 4+个指标、段落 | "95% ACCURATE" "2X FASTER" "FDA READY"（6个字） |
| 比较图表 | **3个条MAX** | **6个字** | 4+个方法、图例文本 | "OURS: 95%" "BEST: 85%"（4个字） |
| 案例研究 | **1个案例，3个元素** | **6个字** | 多个案例、子故事 | Logo + "18 MONTHS" + "to discovery"（2个字） |
| 时间线 | **3-4个点MAX** | **8个字** | 逐年细节 | "2020 START" "2022 TRIAL" "2024 APPROVED"（6个字） |

**示例 - 错误（7阶段工作流程 - 太复杂）：**
```bash
# ❌ 坏 - 这创建像药物发现海报那样不可读的小文本
python scripts/generate_schematic.py "药物发现工作流程显示：第1阶段靶点识别、第2阶段分子合成、第3阶段虚拟筛选、第4阶段AI先导优化、第5阶段临床试验设计、第6阶段FDA批准。包括每个阶段的成功指标、时间线和验证步骤。" -o figures/workflow.png
# 结果：7+个阶段，文本很小，从6英尺不可读 - 海报失败
```

**示例 - 正确（简化为3个关键阶段）：**
```bash
# ✅ 好 - 相同内容，拆分为一个简单的高级图形
python scripts/generate_schematic.py "POSTER FORMAT for A0. ULTRA-SIMPLE 3-box workflow: 'DISCOVER' (120pt bold) → 'VALIDATE' (120pt bold) → 'APPROVE' (120pt bold). Thick arrows (10px). 60% white space. ONLY these 3 words. NO substeps. Readable from 12 feet." -o figures/workflow_overview.png
# 结果：干净、有影响力、可读 - 如需要可单独添加详细图形
```

**示例 - 错误（具有多个部分的复杂案例研究）：**
```bash
# ❌ 坏 - 创建拥挤、不可读的部分
python scripts/generate_schematic.py "案例研究：Insilico Medicine（药物候选、发现时间、临床试验）、Recursion Pharma（平台、方法学、结果）、Exscientia（药物候选、FDA状态、时间线）。包括公司Logo、指标和结果。" -o figures/cases.png
# 结果：3个案例研究，每个有4+个元素 = 12+个总元素，小文本
```

**示例 - 正确（一个案例研究、一个关键指标）：**
```bash
# ✅ 好 - 显示一个案例和一个关键数字
python scripts/generate_schematic.py "POSTER FORMAT for A0. ONE case study card: Company logo (large), '18 MONTHS' in GIANT text (150pt), 'to discovery' below (60pt). 3 elements total: logo + number + caption. 50% white space. Readable from 10 feet." -o figures/case_single.png
# 结果：清晰、可读、有影响力。如果需要3个案例，制作3个独立的简单图形
```

**示例 - 错误（关键发现太复杂）：**
```bash
# 坏 - 项目太多，细节太多
python scripts/generate_schematic.py "关键发现显示8个指标：准确率95%、精确率92%、召回率94%、F1 0.93、AUC 0.97、训练时间2.3小时、推理50ms、模型大小145MB，与5个基线方法比较" -o figures/findings.png
# 结果：拥挤的图形，数字很小
```

**示例 - 正确（关键发现简单）：**
```bash
# GOOD - only 3 key items, giant numbers
python scripts/generate_schematic.py "POSTER FORMAT for A0. KEY FINDINGS with ONLY 3 large cards. Card 1: '95%' in GIANT text (120pt) with 'ACCURACY' below (48pt). Card 2: '2X' in GIANT text with 'FASTER' below. Card 3: checkmark icon with 'VALIDATED' in large text. 50% white space. High contrast colors. NO other text or details." -o figures/findings.png
# 结果：大胆、可读的影响声明
```

**Font size reference for poster prompts:**
| Element | Minimum Size | Prompt Keywords |
|---------|--------------|-----------------|
| Main numbers/metrics | 72pt+ | "huge", "very large", "giant", "poster-size" |
| Section titles | 60pt+ | "large bold", "prominent" |
| Labels/captions | 36pt+ | "readable from 6 feet", "clear labels" |
| Body text | 24pt+ | "poster-readable", "large text" |

**Always include in prompts:**
- "POSTER FORMAT" or "for A0 poster" or "readable from 6 feet"
- "VERY LARGE TEXT" or "huge bold fonts"
- Specific text that should appear (so it's baked into the image)
- "minimal text, maximum impact"
- "high contrast" for readability
- "generous margins" and "no text near edges"

---

### 关键：AI生成图形大小

**⚠️ 每个AI生成的图形应关注一个概念，内容最少。**

**问题**：生成具有许多元素的复杂图表会导致小文本。

**解决方案**：生成具有少量元素和大文本的简单图形。

**示例 - 错误（太复杂，文本会很小）：**
```bash
# 坏 - 一个图形中元素太多
python scripts/generate_schematic.py "完整的ML管道显示数据收集、
带有5个步骤的预处理、带有8个技术的特征工程、
带有超参数调整的模型训练、带有交叉验证的验证、
带有监控的部署。包括所有标签和描述。" -o figures/pipeline.png
```

**Example - CORRECT (simple, focused, large text):**
```bash
# GOOD - split into multiple simple graphics with large text

# Graphic 1: High-level overview (3-4 elements max)
python scripts/generate_schematic.py "POSTER FORMAT for A0: Simple 4-step pipeline. 
Four large boxes: DATA → PROCESS → MODEL → RESULTS. 
GIANT labels (80pt+), thick arrows, lots of white space. 
Only 4 words total. Readable from 8 feet." -o figures/overview.png

# Graphic 2: Key result (1 metric highlighted)
python scripts/generate_schematic.py "POSTER FORMAT for A0: Single key metric display.
Giant '95%' text (150pt+) with 'ACCURACY' below (60pt+).
Checkmark icon. Minimal design, high contrast.
Readable from 10 feet." -o figures/accuracy.png
```

**Rules for AI-generated poster graphics:**
| Rule | Limit | Reason |
|------|-------|--------|
| **Elements per graphic** | 3-5 maximum | More elements = smaller text |
| **Words per graphic** | 10-15 maximum | Minimal text = larger fonts |
| **Flowchart steps** | 4-5 maximum | Keeps labels readable |
| **Chart categories** | 3-4 maximum | Prevents crowding |
| **Nested levels** | 1-2 maximum | Avoids complexity |

**将复杂内容拆分为多个简单图形：**
```
不要创建1个具有12个元素的复杂图表：
→ 创建3个具有4个元素的简单图表
→ 每个图形可以有更大的文本
→ 在海报中排列，具有清晰的视觉流程
```

---

### 步骤0：强制生成前审查（首先执行此操作）

**⚠️ 在生成任何图形之前，审查您的内容计划：**

**对于每个计划的图形，问这些问题：**
1. **元素计数**：我可以用3-4项或更少来描述这个吗？
   - ❌ 否 → 简化或拆分为多个图形
   - ✅ 是 → 继续

2. **复杂性检查**：这是多阶段工作流程（5+个步骤）或嵌套图表吗？
   - ❌ 是 → 展平为仅3-4个高级步骤
   - ✅ 否 → 继续

3. **字数**：我可以用10个或更少单词描述所有文本吗？
   - ❌ 否 → 删除文本，使用单字标签
   - ✅ 是 → 继续

4. **消息清晰度**：这个图形传达一个清晰消息吗？
   - ❌ 否 → 拆分为多个聚焦图形
   - ✅ 是 → 继续生成

**Common patterns that ALWAYS fail (reject these):**
- "Show stages 1 through 7..." → Split into high-level overview (3 stages) + detail graphics
- "Multiple case studies..." → One case per graphic
- "Timeline from 2015 to 2024 with annual milestones..." → Show only 3-4 key years
- "Comparison of 6 methods..." → Show only top 3 or Our method vs Best baseline
- "Architecture with all layers and connections..." → High-level only (3-4 components)

### 步骤1：规划海报元素

通过生成前审查后，识别所需的视觉元素：

1. **标题块** - 带有机构品牌化的风格化标题（可选 - 可以是LaTeX文本）
2. **引言图形** - 概念概述（最多3个元素）
3. **方法图表** - 高级工作流程（最多3-4个步骤）
4. **结果图形** - 关键发现（每图最多3个指标，可能需要2-3个独立图形）
5. **结论图形** - 摘要视觉（最多3个要点）
6. **补充图标** - 简单图标、QR码、Logo（最少）

### 步骤2：生成每个元素（生成前审查后）

**⚠️ 关键：继续之前，审查步骤0检查清单。**

使用适当工具处理每种元素类型：

**For Schematics and Diagrams (scientific-schematics):**
```bash
# Create figures directory
mkdir -p figures

# Drug discovery workflow - HIGH-LEVEL ONLY, 3 stages
# BAD: "Stage 1: Target ID, Stage 2: Molecular Synthesis, Stage 3: Virtual Screening, Stage 4: AI Lead Opt..."
# GOOD: Collapse to 3 mega-stages
python scripts/generate_schematic.py "POSTER FORMAT for A0. ULTRA-SIMPLE 3-box workflow: 'DISCOVER' (120pt bold) → 'VALIDATE' (120pt bold) → 'APPROVE' (120pt bold). Thick arrows (10px). 60% white space. ONLY these 3 words. NO substeps. Readable from 12 feet." -o figures/workflow_simple.png

# System architecture - MAXIMUM 3 components
python scripts/generate_schematic.py "POSTER FORMAT for A0. ULTRA-SIMPLE 3-component stack: 'DATA' box (120pt) → 'AI MODEL' box (120pt) → 'PREDICTION' box (120pt). Thick vertical arrows. 60% white space. 3 words only. Readable from 12 feet." -o figures/architecture.png

# Timeline - ONLY 3 key milestones (not year-by-year)
# BAD: "2018, 2019, 2020, 2021, 2022, 2023, 2024 with events"
# GOOD: Only 3 breakthrough moments
python scripts/generate_schematic.py "POSTER FORMAT for A0. Timeline with ONLY 3 points: '2018' + icon, '2021' + icon, '2024' + icon. GIANT years (120pt). Large icons. 60% white space. NO connecting lines or details. Readable from 12 feet." -o figures/timeline.png

# Case study - ONE case, ONE key metric
# BAD: "3 case studies: Insilico (details), Recursion (details), Exscientia (details)"
# GOOD: ONE case with ONE number
python scripts/generate_schematic.py "POSTER FORMAT for A0. ONE case study: Large logo + '18 MONTHS' (150pt bold) + 'to discovery' (60pt). 3 elements total. 60% white space. Readable from 12 feet." -o figures/case1.png

# If you need 3 cases → make 3 separate simple graphics (not one complex graphic)
```

**For Styled Blocks and Graphics (Nano Banana Pro):**
```bash
# Title block - simple
python scripts/generate_schematic.py "POSTER FORMAT for A0. Title block: 'ML FOR DRUG DISCOVERY' in GIANT bold text (120pt+). Dark blue background. One subtle icon. NO other text. 40% white space. Readable from 15 feet." -o figures/title_block.png

# Introduction visual - simple, 3 elements only
python scripts/generate_schematic.py "POSTER FORMAT for A0. Simple problem visual, ONLY 3 icons: drug icon → arrow → target icon. One word label per icon (80pt+). 50% white space. NO detailed text. Readable from 8 feet." -o figures/intro_visual.png

# Conclusions/summary - 3 items only, giant numbers
python scripts/generate_schematic.py "POSTER FORMAT for A0. Key findings, EXACTLY 3 cards: Card 1: '95%' (150pt font) with 'ACCURACY' (60pt). Card 2: '2X' (150pt) with 'FASTER' (60pt). Card 3: checkmark icon with 'READY' (60pt). 50% white space. NO other text. Readable from 10 feet." -o figures/conclusions_graphic.png

# Background visual - simple, 3 icons only
python scripts/generate_schematic.py "POSTER FORMAT for A0. Simple visual, ONLY 3 large icons in a row: problem icon → challenge icon → impact icon. One word label each (80pt+). 50% white space. NO detailed text. Readable from 8 feet." -o figures/background_visual.png
```

**For Data Visualization - simple, max 3 bars:**
```bash
# Simple chart, 3 bars only, giant labels
python scripts/generate_schematic.py "POSTER FORMAT for A0. Simple bar chart, ONLY 3 bars: baseline (70%), existing (85%), ours (95%). GIANT percentage labels on bars (100pt+). NO axis labels, NO legend, NO grid lines. Our bar highlighted in different color. 40% white space. Readable from 8 feet." -o figures/comparison_chart.png
```

### Step 2b: Mandatory Post-Generation Review (Before Assembly)

**⚠️ CRITICAL: Review every generated graphic before adding it to the poster.**

**For each generated graphic, open at 25% zoom and check:**

1. **✅ PASS criteria (must all be true):**
   - All text is clearly readable at 25% zoom
   - Count elements: 3-4 or fewer
   - White space: 50%+ of image is empty
   - Simple enough to understand in 2 seconds
   - Not a complex workflow with 5+ stages
   - Not multiple nested sections

2. **❌ FAIL criteria (if any is true, regenerate):**
   - Text is small or hard to read at 25% zoom → regenerate with "150pt+" fonts
   - More than 4 elements → regenerate with "3 elements only"
   - Less than 50% white space → regenerate with "60% white space"
   - Complex multi-stage workflow → split into 2-3 simple graphics
   - Multiple case studies crammed together → split into separate graphics
   - Takes more than 3 seconds to understand → simplify and regenerate

**Common failures and fixes:**
- "7-stage workflow, text is tiny" → regenerate as "3 high-level stages only"
- "3 case studies in one graphic" → generate 3 separate simple graphics
- "Timeline with 8 years" → regenerate with "3 key milestones only"
- "Comparison of 5 methods" → regenerate with "our method vs best baseline only (2 bars)"

**Do NOT proceed to assembly if any graphic fails the above checks.**

### Step 3: Assemble in LaTeX Template

Once all graphics pass post-generation review, include them in the poster template:

**tikzposter example:**
```latex
\documentclass[25pt, a0paper, portrait]{tikzposter}

\begin{document}

\maketitle

\begin{columns}
\column{0.5}

\block{Introduction}{
  \centering
  \includegraphics[width=0.85\linewidth]{figures/intro_visual.png}

  \vspace{0.5em}
  Brief context text (2-3 sentences max).
}

\block{Methods}{
  \centering
  \includegraphics[width=0.9\linewidth]{figures/methods_flowchart.png}
}

\column{0.5}

\block{Results}{
  \begin{minipage}{0.48\linewidth}
    \centering
    \includegraphics[width=\linewidth]{figures/result_1.png}
  \end{minipage}
  \hfill
  \begin{minipage}{0.48\linewidth}
    \centering
    \includegraphics[width=\linewidth]{figures/result_2.png}
  \end{minipage}

  \vspace{0.5em}
  Key findings in 3-4 bullet points.
}

\block{Conclusions}{
  \centering
  \includegraphics[width=0.8\linewidth]{figures/conclusions_graphic.png}
}

\end{columns}

\end{document}
```

**baposter example:**
```latex
\headerbox{Methods}{name=methods,column=0,row=0}{
  \centering
  \includegraphics[width=0.95\linewidth]{figures/methods_flowchart.png}
}

\headerbox{Results}{name=results,column=1,row=0}{
  \includegraphics[width=\linewidth]{figures/comparison_chart.png}
  \vspace{0.3em}

  Key finding: Our method achieves 92% accuracy.
}
```

### Example: Complete Poster Generation Workflow

**Complete workflow with all quality checks:**

```bash
# Step 0: Pre-generation review (mandatory)
# Content plan: Drug discovery poster
# - Workflow: 7 stages → ❌ Too many → Reduce to 3 mega-stages ✅
# - 3 case studies → ❌ Too many → One case per graphic (make 3 graphics) ✅
# - 2018-2024 timeline → ❌ Too detailed → Only 3 key years ✅

# Step 1: Create figures directory
mkdir -p figures

# Step 2: Generate ultra-simple graphics with strict limits

# Workflow - high-level only (collapsed from 7 stages to 3)
python scripts/generate_schematic.py "POSTER FORMAT for A0. ULTRA-SIMPLE 3-box workflow: 'DISCOVER' (120pt bold) → 'VALIDATE' (120pt bold) → 'APPROVE' (120pt bold). Thick arrows (10px). 60% white space. ONLY these 3 words. Readable from 12 feet." -o figures/workflow.png

# Case study 1 - one case, one metric (will make 3 separate graphics)
python scripts/generate_schematic.py "POSTER FORMAT for A0. ONE case: Company logo + '18 MONTHS' (150pt bold) + 'to drug discovery' (60pt). 3 elements only: logo + number + caption. 60% white space. Readable from 12 feet." -o figures/case1.png

python scripts/generate_schematic.py "POSTER FORMAT for A0. ONE case: Company logo + '95% SUCCESS' (150pt bold) + 'in trials' (60pt). 3 elements only: logo + number + caption. 60% white space." -o figures/case2.png

python scripts/generate_schematic.py "POSTER FORMAT for A0. ONE case: Company logo + 'FDA APPROVED' (150pt bold) + '2024' (60pt). 3 elements only: logo + number + caption. 60% white space." -o figures/case3.png

# Timeline - 3 key years only (not 7 years)
python scripts/generate_schematic.py "POSTER FORMAT for A0. 3 years only: '2018' (150pt) + icon, '2021' (150pt) + icon, '2024' (150pt) + icon. Large icons. 60% white space. NO lines or details. Readable from 12 feet." -o figures/timeline.png

# Results - 2 bars only (our method vs best baseline, not 5 methods)
python scripts/generate_schematic.py "POSTER FORMAT for A0. 2 bars only: 'BASELINE 70%' and 'OURS 95%' (highlighted). GIANT percentages on bars (150pt). NO axes, NO legend. 60% white space. Readable from 12 feet." -o figures/results.png

# Step 2b: Post-generation review (mandatory)
# Open each graphic at 25% zoom:
# ✅ workflow.png: 3 elements, text readable, 60% white - PASS
# ✅ case1.png: 3 elements, giant numbers, clean - PASS
# ✅ case2.png: 3 elements, giant numbers, clean - PASS
# ✅ case3.png: 3 elements, giant numbers, clean - PASS
# ✅ timeline.png: 3 elements, readable, simple - PASS
# ✅ results.png: 2 bars, giant percentages, clear - PASS
# All pass → proceed to assembly

# Step 3: Compile LaTeX poster
pdflatex poster.tex

# Step 4: PDF overflow check (see Section 11)
grep "Overfull" poster.log
# Open at 100% zoom and check all 4 edges
```

**If any graphic fails Step 2b review:**
- Too many elements → regenerate with "3 elements only"
- Text is tiny → regenerate with "150pt+" or "giant bold (150pt+)"
- Crowded → regenerate with "60% white space" and "ultra-simple"
- Complex workflow → split into multiple simple 3-element graphics

### Visual Element Guide

**⚠️ CRITICAL: Each graphic must have one message and MAXIMUM 3-4 elements.**

**Absolute limits - these are not guidelines, these are hard limits:**
- **3-4 elements MAX** per graphic (3 is ideal)
- **10 words MAX** total per graphic
- **50% white space MIN** (60% is better)
- **120pt MIN** for key numbers/metrics
- **80pt MIN** for labels

**For each poster section - strict requirements:**

| Section | Max Elements | Max Words | Example Prompt (Required Pattern) |
|---------|--------------|-----------|-------------------------------------|
| **Introduction** | 3 icons | 6 words | "POSTER FORMAT for A0: ultra-simple 3 icons: [icon1] [icon2] [icon3]. One word label each (100pt bold). 60% white space. 3 words total." |
| **Methods** | 3 boxes | 6 words | "POSTER FORMAT for A0: ultra-simple 3-box workflow: 'STEP 1' → 'STEP 2' → 'STEP 3'. Giant labels (120pt+). 60% white space. 3 words only." |
| **Results** | 2-3 bars | 6 words | "POSTER FORMAT for A0: 3 bars only: 'BASELINE 70%' 'EXISTING 85%' 'OURS 95%'. Giant percentages on bars (150pt+). No axes. 60% white space." |
| **Conclusions** | 3 cards | 9 words | "POSTER FORMAT for A0: exactly 3 cards: '[number]' (150pt) '[label]' (60pt) each. 60% white space. No other text." |
| **Case Study** | 3 elements | 5 words | "POSTER FORMAT for A0: one case: Logo + '18 MONTHS' (150pt) + 'to discovery' (60pt). 60% white space." |
| **Timeline** | 3 points | 3 words | "POSTER FORMAT for A0: 3 years only: '2018' '2021' '2024' (150pt each). Large icons. 60% white space. No details." |

**Mandatory prompt elements (all required, no exceptions):**
1. **"POSTER FORMAT for A0"** - must be first
2. **"ultra-simple"** or **"X elements only"** - content limit
3. **"GIANT (120pt+)"** or specific font size - readability
4. **"60% white space"** - mandatory breathing room
5. **"Readable from 10-12 feet"** - viewing distance
6. **Exact word/element count** - "3 words total" or "3 icons only"

**Always failing patterns (reject immediately):**
- ❌ "7-stage drug discovery workflow" → split to "3 mega-stages"
- ❌ "Timeline from 2015-2024 with annual updates" → "3 key years only"
- ❌ "3 case studies with details" → make 3 separate simple graphics
- ❌ "5 method comparison with metrics" → "2 only: our method vs best baseline"
- ❌ "Complete architecture showing all layers" → "3 components only"
- ❌ "Show stages 1, 2, 3, 4, 5, 6" → "3 high-level stages"

**Valid patterns:**
- ✅ "3 mega-stages collapsed from 7" → appropriate simplification
- ✅ "One case with one metric" → will make multiple if needed
- ✅ "3 milestones only" → selective, focused
- ✅ "2 bars: our method vs baseline" → direct comparison
- ✅ "3 component high-level view" → appropriate simplification

---

## Scientific Schematics集成

有关创建示意图的详细指导，请参阅 **scientific-schematics** 技能文档。

**关键能力：**
- Nano Banana Pro自动生成、审查和完善图表
- 创建具有正确格式的出版质量图像
- 确保可访问性（色盲友好、高对比度）
- 支持复杂图表的迭代完善

---

## 核心能力

### 1. LaTeX海报包

支持三个主要LaTeX海报包，每个都有独特的优势。有关详细比较和包特定指导，请参阅 `references/latex_poster_packages.md`。

**beamerposter**：
- Beamer演示类的扩展
- Beamer用户熟悉的语法
- 优秀的主题支持和自定义
- 最适合：传统学术海报、机构品牌化

**tikzposter**：
- 具有TikZ集成的现代、灵活设计
- 内置配色方案和布局模板
- 通过TikZ命令进行广泛自定义
- 最适合：彩色、现代设计、自定义图形

**baposter**：
- 基于框的布局系统
- 自动间距和定位
- 专业外观的默认样式
- 最适合：多列布局、一致间距

### 2. 海报布局和结构

遵循视觉交流原则创建有效的海报布局。有关全面的布局指导，请参阅 `references/poster_layout_design.md`。

**常见海报部分：**
- **页眉/标题**：标题、作者、所属机构、Logo
- **引言/背景**：研究背景和动机
- **方法/方法**：方法学和实验设计
- **结果**：关键发现，带有图形和数据可视化
- **结论**：主要要点和意义
- **参考文献**：关键引文（通常缩写）
- **致谢**：资助、合作者、机构

**布局策略：**
- **基于列的布局**：2列、3列或4列网格
- **基于块的布局**：内容块的灵活排列
- **Z模式流程**：逻辑引导读者通过内容
- **视觉层次**：使用大小、颜色和间距强调关键点

### 3. 研究海报的设计原则

应用基于证据的设计原则以获得最大影响力。有关详细设计指导，请参阅 `references/poster_design_principles.md`。

**排版：**
- 标题：72-120pt，以便从远处可见
- 章节标题：48-72pt
- 正文：24-36pt最小，以便从4-6英尺可读
- 使用无衬线字体（Arial、Helvetica、Calibri）以提高清晰度
- 最多使用2-3个字体系列

**颜色和对比度：**
- 使用高对比度配色方案以提高可读性
- 机构配色方案用于品牌化
- 色盲友好调色板（避免红绿组合）
- 白色空间是活动空间 - 不要过度拥挤

**视觉元素：**
- 高分辨率图形（打印最少300 DPI）
- 所有图形上的大、清晰标签
- 整个海报一致的图形样式
- 图标和图形的战略使用
- 用视觉内容平衡文本（推荐40-50%视觉）

**内容指南：**
- **少即是多**：总共推荐300-800字
- 要点优于段落以提高可扫描性
- 清晰、简洁的消息
- 具有最少文本解释的自我解释图形
- 用于补充材料或在线资源的QR码

### 4. 标准海报尺寸

支持国际和会议特定的海报尺寸：

**国际标准：**
- A0（841 × 1189毫米 / 33.1 × 46.8英寸）- 最常见的欧洲标准
- A1（594 × 841毫米 / 23.4 × 33.1英寸）- 较小格式
- A2（420 × 594毫米 / 16.5 × 23.4英寸）- 紧凑海报

**北美标准：**
- 36 × 48英寸（914 × 1219毫米）- 常见美国会议尺寸
- 42 × 56英寸（1067 × 1422毫米）- 大格式
- 48 × 72英寸（1219 × 1829毫米）- 超大

**方向：**
- 纵向（垂直）- 最常见、传统
- 横向（水平）- 更适合宽内容、时间线

### 5. 包特定模板

为每个主要包提供即用型模板。模板可在 `assets/` 目录中获得。

**beamerposter模板：**
- `beamerposter_classic.tex` - 传统学术风格
- `beamerposter_modern.tex` - 干净、最小设计
- `beamerposter_colorful.tex` - 带有块的鲜艳主题

**tikzposter模板：**
- `tikzposter_default.tex` - 标准tikzposter布局
- `tikzposter_rays.tex` - 带有射线主题的现代设计
- `tikzposter_wave.tex` - 专业波浪风格主题

**baposter模板：**
- `baposter_portrait.tex` - 经典纵向布局
- `baposter_landscape.tex` - 横向多列
- `baposter_minimal.tex` - 最小主义设计

### 6. 图形和图像集成

优化海报演示的视觉内容：

**最佳实践：**
- 尽可能使用矢量图形（PDF、SVG）以实现可扩展性
- 光栅图像：最终打印尺寸最少300 DPI
- 一致的图像样式（边框、标题、大小）
- 将相关图形分组
- 使用子图进行比较

**LaTeX图形命令：**
```latex
% 包含图形包
\usepackage{graphicx}

% 简单图形
\includegraphics[width=0.8\linewidth]{figure.pdf}

% 带有标题的tikzposter中的图形
\block{结果}{
  \begin{tikzfigure}
    \includegraphics[width=0.9\linewidth]{results.png}
  \end{tikzfigure}
}

% 多个子图
\usepackage{subcaption}
\begin{figure}
  \begin{subfigure}{0.48\linewidth}
    \includegraphics[width=\linewidth]{fig1.pdf}
    \caption{条件A}
  \end{subfigure}
  \begin{subfigure}{0.48\linewidth}
    \includegraphics[width=\linewidth]{fig2.pdf}
    \caption{条件B}
  \end{subfigure}
\end{figure}
```

### 7. 配色方案和主题

为各种上下文提供专业调色板：

**学术机构颜色：**
- 匹配大学或部门品牌化
- 使用官方颜色代码（RGB、CMYK或LaTeX颜色定义）

**科学配色方案**（色盲友好）：
- Viridis：从紫色到黄色的专业渐变
- ColorBrewer：数据可视化的研究测试调色板
- IBM色盲安全：可访问的企业调色板

**包特定主题选择：**

**beamerposter**：
```latex
\usetheme{Berlin}
\usecolortheme{beaver}
```

**tikzposter**：
```latex
\usetheme{Rays}
\usecolorstyle{Denmark}
```

**baposter**：
```latex
\begin{poster}{
  background=plain,
  bgColorOne=white,
  headerColorOne=blue!70,
  textborder=rounded
}
```

### 8. 排版和文本格式

确保可读性和视觉吸引力：

**字体选择：**
```latex
% 海报推荐无衬线字体
\usepackage{helvet}      % Helvetica
\usepackage{avant}       % Avant Garde
\usepackage{sfmath}      % 无衬线数学字体

% 设置默认为无衬线
\renewcommand{\familydefault}{\sfdefault}
```

**文本大小：**
```latex
% 为可见性调整文本大小
\setbeamerfont{title}{size=\VeryHuge}
\setbeamerfont{author}{size=\Large}
\setbeamerfont{institute}{size=\normalsize}
```

**强调和突出：**
- 对关键术语使用粗体：`\textbf{important}`
- 谨慎使用颜色突出：`\textcolor{blue}{highlight}`
- 用于关键信息的框
- 避免斜体（从远处更难阅读）

### 9. QR码和交互元素

通过QR码增强海报的交互性以用于现代会议：

**QR码集成：**
```latex
\usepackage{qrcode}

% 链接到论文、代码存储库或补充材料
\qrcode[height=2cm]{https://github.com/username/project}

% 带有标题的QR码
\begin{center}
  \qrcode[height=3cm]{https://doi.org/10.1234/paper}\\
  \small 扫描完整论文
\end{center}
```

**数字增强：**
- 链接到GitHub存储库的代码
- 链接到视频演示或演示
- 链接到交互式Web可视化
- 链接到补充数据或附录

### 10. 编译和输出

生成高质量PDF输出以用于打印或数字显示：

**编译命令：**
```bash
# 基本编译
pdflatex poster.tex

# 带有书目
pdflatex poster.tex
bibtex poster
pdflatex poster.tex
pdflatex poster.tex

# 对于基于beamer的海报
lualatex poster.tex  # 更好的字体支持
xelatex poster.tex   # Unicode和现代字体
```

**确保全页覆盖：**

海报应使用整个页面，没有过多的边距。正确配置包：

**beamerposter - 全页设置：**
```latex
\documentclass[final,t]{beamer}
\usepackage[size=a0,scale=1.4,orientation=portrait]{beamerposter}

% 删除默认beamer边距
\setbeamersize{text margin left=0mm, text margin right=0mm}

% 使用geometry进行精确控制
\usepackage[margin=10mm]{geometry}  % 四周10mm边距

% 删除导航符号
\setbeamertemplate{navigation symbols}{}

% 如果不需要，删除页脚和页眉
\setbeamertemplate{footline}{}
\setbeamertemplate{headline}{}
```

**tikzposter - 全页设置：**
```latex
\documentclass[
  25pt,                      % 字体缩放
  a0paper,                   % 纸张尺寸
  portrait,                  % 方向
  margin=10mm,               % 外边距（最小）
  innermargin=15mm,          % 块内空间
  blockverticalspace=15mm,   % 块之间的空间
  colspace=15mm,             % 列之间的空间
  subcolspace=8mm            % 子列之间的空间
]{tikzposter}

% 这确保内容填充页面
```

**baposter - 全页设置：**
```latex
\documentclass[a0paper,portrait,fontscale=0.285]{baposter}

\begin{poster}{
  grid=false,
  columns=3,
  colspacing=1.5em,          % 列之间的空间
  eyecatcher=true,
  background=plain,
  bgColorOne=white,
  borderColor=blue!50,
  headerheight=0.12\textheight,  % 12%用于页眉
  textborder=roundedleft,
  headerborder=closed,
  boxheaderheight=2em        % 一致的框页眉高度
}
% 内容在这里
\end{poster}
```

**常见问题和修复：**

**问题：海报周围有大白色边距**
```latex
% 修复beamerposter
\setbeamersize{text margin left=5mm, text margin right=5mm}

% 修复tikzposter
\documentclass[..., margin=5mm, innermargin=10mm]{tikzposter}

% 修复baposter - 在文档类中调整
\documentclass[a0paper, margin=5mm]{baposter}
```

**问题：内容不填充垂直空间**
```latex
% 使用\vfill在部分之间分配空间
\block{引言}{...}
\vfill
\block{方法}{...}
\vfill
\block{结果}{...}

% 或手动调整块间距
\vspace{1cm}  % 在特定块之间添加空间
```

**问题：海报超出页面边界**
```latex
% 检查总宽度计算
% 对于带有间距的3列：
% 总计 = 3×列宽 + 2×列空间 + 2×边距
% 确保这等于\paperwidth

% 通过添加可见页面边界进行调试
\usepackage{eso-pic}
\AddToShipoutPictureBG{
  \AtPageLowerLeft{
    \put(0,0){\framebox(\LenToUnit{\paperwidth},\LenToUnit{\paperheight}){}}
  }
}
```

**打印准备：**
- 生成PDF/X-1a以用于专业打印
- 嵌入所有字体
- 如果需要，将颜色转换为CMYK
- 检查所有图像的分辨率（最少300 DPI）
- 如果打印机要求，添加出血区域（通常3-5毫米）
- 验证页面尺寸完全匹配要求

**数字显示：**
- 屏幕显示的RGB颜色空间
- 优化文件大小以用于电子邮件/Web
- 在不同屏幕上测试可读性

### 11. PDF审查和质量控制

**关键**：在打印或演示之前始终审查生成的PDF。使用此系统检查清单：

**步骤1：页面尺寸验证**
```bash
# 检查PDF尺寸（应完全匹配海报尺寸）
pdfinfo poster.pdf | grep "Page size"

# 预期输出：
# A0: 2384 x 3370点（841 x 1189毫米）
# 36x48"：2592 x 3456点
# A1: 1684 x 2384点（594 x 841毫米）
```

**步骤2：溢出检查（关键）- 编译后立即执行此操作**

**⚠️ 这是海报失败的#1原因。在继续之前检查。**

**步骤2a：检查LaTeX日志文件**
```bash
# 检查溢出警告（这些是错误，不是建议）
grep -i "overfull\|underfull\|badbox" poster.log

# 任何"Overfull"警告 = 内容被截断或超出边界
# 在继续之前修复所有这些
```

**常见溢出警告及其含义：**
- `Overfull \hbox (15.2pt too wide)` → 文本或图形比列宽15.2pt
- `Overfull \vbox (23.5pt too high)` → 内容比可用空间高23.5pt
- `Badbox` → LaTeX难以在边界内拟合内容

**步骤2b：视觉边缘检查（PDF查看器中100%缩放）**

**系统检查所有四条边缘：**

1. **顶边缘：**
   - [ ] 标题完全可见（未截断）
   - [ ] 作者姓名完全可见
   - [ ] 没有图形接触顶边距
   - [ ] 页眉内容在安全区域内

2. **底边缘：**
   - [ ] 参考文献完全可见（未截断）
   - [ ] 致谢完整
   - [ ] 联系信息可读
   - [ ] 底部没有图形被截断

3. **左边缘：**
   - [ ] 没有文本接触左边距
   - [ ] 所有要点完全可见
   - [ ] 图形有左边距（未流出）
   - [ ] 列内容在边界内

4. **右边缘：**
   - [ ] 没有文本超出右边距
   - [ ] 图形在右侧未截断
   - [ ] 列内容保持在边界内
   - [ ] QR码完全可见

5. **列之间：**
   - [ ] 内容保持在各个列内
   - [ ] 没有文本流入相邻列
   - [ ] 图形尊重列边界

**如果任何检查失败，您有溢出。在继续之前立即修复：**

**修复层次（按顺序尝试）：**
1. **首先检查AI生成的图形：**
   - 它们太复杂（5+个元素）吗？→ 重新生成更简单
   - 它们有小文本吗？→ 用"150pt+"字体重新生成
   - 它们太多吗？→ 减少图形数量

2. **减少部分：**
   - 超过5-6个部分？→ 合并或删除
   - 示例：将"讨论"合并到"结论"

3. **删除文本内容：**
   - 超过800字总数？→ 删除到300-500
   - 超过每部分100字？→ 删除到50-80

4. **调整图形大小：**
   - 使用`width=\linewidth`？→ 更改为`width=0.85\linewidth`
   - 使用`width=1.0\columnwidth`？→ 更改为`width=0.9\columnwidth`

5. **增加边距（最后手段）：**
   ```latex
   \documentclass[25pt, a0paper, portrait, margin=25mm]{tikzposter}
   ```

**如果存在任何溢出，请勿继续到步骤3。**

**步骤3：视觉检查清单**

以100%缩放打开PDF并检查：

**布局和间距：**
- [ ] 内容填充整个页面（没有大白色边距）
- [ ] 列之间一致的间距
- [ ] 块/部分之间一致的间距
- [ ] 所有元素正确对齐（使用标尺工具）
- [ ] 没有重叠的文本或图形
- [ ] 白色空间均匀分布

**排版：**
- [ ] 标题清晰可见且很大（72pt+）
- [ ] 章节标题可读（48-72pt）
- [ ] 正文在100%缩放时可读（24-36pt最小）
- [ ] 没有文本截断或从边缘流出
- [ ] 整个一致的字体使用
- [ ] 所有特殊字符正确渲染（符号、希腊字母）

**视觉元素：**
- [ ] 所有图形正确显示
- [ ] 没有像素化或模糊的图像
- [ ] 图形标题存在且可读
- [ ] 颜色按预期渲染（未褪色或太暗）
- [ ] Logo清晰显示
- [ ] QR码可见且可扫描

**内容完整性：**
- [ ] 标题和作者完整
- [ ] 所有部分存在（引言、方法、结果、结论）
- [ ] 包括参考文献
- [ ] 联系信息可见
- [ ] 致谢（如适用）
- [ ] 没有占位符文本（Lorem ipsum、TODO等）

**技术质量：**
- [ ] 重要区域中没有LaTeX编译警告
- [ ] 所有引文已解析（没有[?]标记）
- [ ] 所有交叉引用工作
- [ ] 页面边界正确（没有内容被截断）

**步骤4：缩小打印测试**

**必要的打印前测试：**
```bash
# 创建缩小尺寸测试打印（最终尺寸的25%）
# 这模拟从~8-10英尺观看完整海报

# 对于A0海报，在A4纸上打印（24.7%缩放）
# 对于36×48"海报，在letter纸上打印（~25%缩放）
```

**打印测试检查清单：**
- [ ] 从6英尺可读标题
- [ ] 从4英尺可读章节标题
- [ ] 从2英尺可读正文
- [ ] 图形清晰易懂
- [ ] 颜色准确打印
- [ ] 没有明显的设计缺陷

**步骤5：数字质量检查**

**字体嵌入验证：**
```bash
# 检查所有字体已嵌入（打印所需）
pdffonts poster.pdf

# 所有字体应在"emb"列中显示"是"
# 如果任何显示"否"，用以下重新编译：
pdflatex -dEmbedAllFonts=true poster.tex
```

**图像分辨率检查：**
```bash
# 提取图像信息
pdfimages -list poster.pdf

# 检查所有图像至少为300 DPI
# 公式：DPI = 像素 /（海报中的英寸）
# 对于A0宽度（33.1"）：300 DPI = 9930像素最小
```

**文件大小优化：**
```bash
# 用于电子邮件/Web，如果需要压缩（>50MB）
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 \
   -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH \
   -sOutputFile=poster_compressed.pdf poster.pdf

# 用于打印，保留原始（不压缩）
```

**步骤6：可访问性检查**

**颜色对比度验证：**
- [ ] 文本-背景对比度比≥4.5:1（WCAG AA）
- [ ] 重要元素对比度比≥7:1（WCAG AAA）
- 在线测试：https://webaim.org/resources/contrastchecker/

**色盲模拟：**
- [ ] 通过色盲模拟器查看PDF
- [ ] 红绿模拟中信息未丢失
- [ ] 使用Coblis（color-blindness.com）或类似工具

**步骤7：内容校对**

**系统审查：**
- [ ] 检查所有文本的拼写
- [ ] 验证所有作者姓名和所属机构
- [ ] 检查所有数字和统计数据的准确性
- [ ] 确认所有引文正确
- [ ] 审查图形标签和标题
- [ ] 检查标题和页眉中的拼写错误

**同行评审：**
- [ ] 请同事审查海报
- [ ] 30秒测试：他们能识别主要消息吗？
- [ ] 5分钟评审：他们理解结论吗？
- [ ] 注意任何令人困惑的元素

**步骤8：技术验证**

**LaTeX编译日志审查：**
```bash
# 检查.log文件中的警告
grep -i "warning\|error\|overfull\|underfull" poster.log

# 需要修复的常见问题：
# - Overfull hbox：文本超出边距
# - Underfull hbox：过度间距
# - 缺少参考文献：引文未解析
# - 缺少图形：未找到图像文件
```

**修复常见警告：**
```latex
% Overfull hbox（文本太宽）
\usepackage{microtype}  % 更好的间距
\sloppy  % 允许稍微更宽松的间距
\hyphenation{long-word}  % 手动连字符

% 缺少字体
\usepackage[T1]{fontenc}  % 更好的字体编码

% 未找到图像
% 确保路径正确且文件存在
\graphicspath{{./figures/}{./images/}}
```

**步骤9：打印前最终检查清单**

**发送到打印机之前：**
- [ ] PDF尺寸完全匹配要求（用pdfinfo检查）
- [ ] 所有字体已嵌入（用pdffonts检查）
- [ ] 颜色模式正确（屏幕用RGB，打印用CMYK如需要）
- [ ] 如果需要，添加出血区域（通常3-5毫米）
- [ ] 如果需要，可见裁剪标记
- [ ] 测试打印已完成并审查
- [ ] 文件命名清晰：[LastName]_[Conference]_Poster.pdf
- [ ] 已保存备份副本

**打印规格确认：**
- [ ] 纸张类型（哑光与光面）
- [ ] 打印方法（喷墨、大幅面、织物）
- [ ] 颜色配置（如果需要提供给打印机）
- [ ] 交付截止日期和收货地址
- [ ] 管或扁平包装偏好

**数字演示检查清单：**
- [ ] PDF大小已优化（<10MB用于电子邮件）
- [ ] 在多个PDF查看器上测试（Adobe、Preview等）
- [ ] 在不同屏幕上正确显示
- [ ] QR码已测试且功能正常
- [ ] 已准备替代格式（PNG用于社交媒体）

**审查脚本**（可在 `scripts/review_poster.sh` 中获得）：
```bash
#!/bin/bash
# 自动海报PDF审查脚本

echo "海报PDF质量检查"
echo "======================="

# 检查文件存在
if [ ! -f "$1" ]; then
    echo "错误：未找到文件"
    exit 1
fi

echo "文件：$1"
echo ""

# 检查页面尺寸
echo "1. 页面尺寸："
pdfinfo "$1" | grep "Page size"
echo ""

# 检查字体
echo "2. 字体嵌入："
pdffonts "$1" | head -20
echo ""

# 检查文件大小
echo "3. 文件大小："
ls -lh "$1" | awk '{print $5}'
echo ""

# 计算页数（海报应为1）
echo "4. 页数："
pdfinfo "$1" | grep "Pages"
echo ""

echo "需要手动检查："
echo "- 以100%缩放的视觉检查"
echo "- 缩小打印测试（25%）"
echo "- 颜色对比度验证"
echo "- 拼写错误校对"
```

**常见PDF问题和解决方案：**

| 问题 | 原因 | 解决方案 |
|-------|-------|----------|
| 大白色边距 | 不正确的边距设置 | 在documentclass中减少边距 |
| 内容被截断 | 超出页面边界 | 检查总宽度/高度计算 |
| 模糊图像 | 低分辨率（<300 DPI） | 替换为更高分辨率图像 |
| 缺少字体 | 字体未嵌入 | 用-dEmbedAllFonts=true编译 |
| 错误页面尺寸 | 不正确的纸张尺寸设置 | 验证documentclass纸张尺寸 |
| 颜色错误 | RGB与CMYK不匹配 | 如需要转换颜色空间以用于打印 |
| 文件太大（>50MB） | 未压缩图像 | 优化图像或压缩PDF |
| QR码不工作 | 太小或低分辨率 | 最小2×2cm，高对比度 |

### 11. 常见海报内容模式

不同研究类型的有效内容组织：

**实验研究海报：**
1. 标题和作者
2. 引言：问题和假设
3. 方法：实验设计（带图表）
4. 结果：关键发现（2-4个主要图形）
5. 结论：主要要点（3-5个要点）
6. 未来工作（可选）
7. 参考文献和致谢

**计算/建模海报：**
1. 标题和作者
2. 动机：问题陈述
3. 方法：算法或模型（带流程图）
4. 实现：技术细节
5. 结果：性能指标和比较
6. 应用：用例
7. 代码可用性（QR码到GitHub）
8. 参考文献

**综述/调查海报：**
1. 标题和作者
2. 范围：主题概述
3. 方法：文献搜索策略
4. 关键发现：主要主题（按类别组织）
5. 趋势：发表模式的可视化
6. 空白：识别的研究需求
7. 结论：总结和意义
8. 参考文献

### 12. 可访问性和包容性设计

设计对多样化受众可访问的海报：

**色盲考虑：**
- 避免红绿组合（最常见的色盲）
- 除颜色外，使用图案或形状
- 用色盲模拟器测试
- 提供高对比度（WCAG AA标准：最少4.5:1）

**视觉障碍适应：**
- 大、清晰的字体（正文最少24pt）
- 高对比度文本和背景
- 清晰的视觉层次
- 避免背景中的复杂纹理或图案

**语言和内容：**
- 清晰、简洁的语言
- 定义缩写和术语
- 国际受众考虑
- 考虑全球会议的多语言QR码选项

### 13. 海报演示最佳实践

超越LaTeX的有效海报环节指导：

**内容策略：**
- 讲故事，不要只是列出事实
- 聚焦1-3个主要消息
- 使用视觉摘要或图形摘要
- 为对话留出空间（不要过度解释）

**物理演示提示：**
- 带有QR码的打印传单或名片
- 准备30秒、2分钟和5分钟的口头摘要
- 站在一侧，不要阻挡海报
- 用开放式问题吸引观众

**数字备份：**
- 在移动设备上保存海报为PDF
- 准备用于电子邮件共享的数字版本
- 为社交媒体创建社交媒体友好的图像版本
- 备份打印副本或数字显示选项

## 海报创建工作流程

### 阶段1：规划和内容开发

1. **确定海报要求**：
   - 会议尺寸规格（A0、36×48"等）
   - 方向（纵向与横向）
   - 提交截止日期和格式要求

2. **开发内容大纲**：
   - 识别1-3个核心消息
   - 选择关键图形（通常3-6个主要视觉）
   - 为每个部分起草简洁文本（要点首选）
   - 总共瞄准300-800字

3. **选择LaTeX包**：
   - 如果熟悉Beamer，需要机构主题 → beamerposter
   - 对于现代、彩色设计，具有灵活性 → tikzposter
   - 对于结构化、专业多列布局 → baposter

### 阶段2：生成视觉元素（AI驱动）

**关键：生成具有最少内容的简单图形。每个图形 = 一个消息。**

**内容限制：**
- 每个图形最多4-5个元素
- 每个图形总共最多15个单词
- 最少50%白色空间
- 用于标签的巨大字体（80pt+），用于关键数字的巨大字体（120pt+）

1. **创建figures目录**：
   ```bash
   mkdir -p figures
   ```

2. **生成简单视觉元素：**
   ```bash
   # 引言 - 仅3个图标/元素
   python scripts/generate_schematic.py "海报格式A0。简单视觉，仅3个元素：[图标1] [图标2] [图标3]。每个词标签（80pt+）。50%白色空间。从8英尺可读。" -o figures/intro.png
   
   # 方法 - 仅最多4个步骤
   python scripts/generate_schematic.py "海报格式A0。简单流程图，仅4个框：步骤1 → 步骤2 → 步骤3 → 步骤4。巨大标签（100pt+）。50%白色空间。无子步骤。" -o figures/methods.png
   
   # 结果 - 仅最多3个条/比较
   python scripts/generate_schematic.py "海报格式A0。简单图表，仅3个条。条上巨大百分比（120pt+）。无轴、无图例。50%白色空间。" -o figures/results.png
   
   # 结论 - 恰好3个项目，巨大数字
   python scripts/generate_schematic.py "海报格式A0。确切3个关键发现：'[数字]'（150pt）'[标签]'（60pt）每个。50%白色空间。无其他文本。" -o figures/conclusions.png
   ```

3. **审查生成的图形 - 检查溢出：**
   - **以25%缩放查看**：所有文本仍然可读？
   - **计算元素**：超过5个？→ 重新生成更简单
   - **检查白色空间**：少于40%？→ 添加"60%白色空间"到提示
   - **字体太小？**：添加"更大"或增加pt大小
   - **仍然溢出？**：减少到3个元素而不是4-5个

### 阶段3：设计和布局

1. **选择或创建模板**：
   - 从 `assets/` 中提供的模板开始
   - 自定义配色方案以匹配品牌化
   - 配置页面尺寸和方向

2. **设计布局结构**：
   - 规划列结构（2、3或4列）
   - 映射内容流程（通常从左到右，从上到下）
   - 为标题分配空间（10-15%）、内容（70-80%）、页脚（5-10%）

3. **设置排版**：
   - 为不同层次级别配置字体大小
   - 确保最少24pt正文
   - 从4-6英尺距离测试可读性

### 阶段4：内容集成

1. **创建海报页眉**：
   - 标题（简洁、描述性、10-15个字）
   - 作者和所属机构
   - 机构Logo（高分辨率）
   - 如需要，会议Logo

2. **集成AI生成的图形**：
   - 将阶段2的所有图形添加到适当部分
   - 使用 `\includegraphics` 和适当大小
   - 确保图形主导每个部分（视觉优先，文本其次）
   - 将图形在块内居中以产生视觉影响

3. **添加最少支持文本**：
   - 保持文本最少且可扫描（总共300-800字）
   - 使用要点，而非段落
   - 用主动语写作
   - 文本应补充图形，不重复

4. **添加补充元素**：
   - 用于补充材料的QR码
   - 参考文献（仅引用关键论文，5-10个典型）
   - 联系信息和致谢

### 阶段5：完善和测试

1. **审查和迭代**：
   - 检查拼写错误和错误
   - 验证所有图形为高分辨率
   - 确保一致的格式
   - 确认配色方案协同工作良好

2. **测试可读性**：
   - 以25%缩放打印并从2-3英尺阅读（模拟海报从8-12英尺）
   - 在不同显示器上检查颜色
   - 验证QR码功能正常
   - 请同事审查

3. **优化以用于打印**：
   - 在PDF中嵌入所有字体
   - 验证图像分辨率
   - 检查PDF大小要求
   - 如需要，包含出血区域

### 阶段6：编译和交付

1. **编译最终PDF**：
   ```bash
   pdflatex poster.tex
   # 或为了更好的字体支持：
   lualatex poster.tex
   ```

2. **验证输出质量**：
   - 检查所有元素可见且正确定位
   - 缩放到100%并检查图形质量
   - 验证颜色按预期匹配
   - 确认PDF在不同查看器上正确打开

3. **准备以用于打印**：
   - 如需要，导出为PDF/X-1a
   - 保存备份副本
   - 首先在常规纸上获取测试打印
   - 在截止日期前2-3天订购专业打印

4. **创建补充材料**：
   - 保存PNG/JPG版本以用于社交媒体
   - 创建传单版本（8.5×11"摘要）
   - 准备用于电子邮件共享的数字版本

## 与其他技能的集成

该技能有效与以下技能配合：

- **Scientific Schematics**：关键 - 用于生成所有海报图表和流程图
- **Generate Image / Nano Banana Pro**：用于样式化图形、概念插图和摘要视觉
- **Scientific Writing**：用于从论文开发海报内容
- **Literature Review**：用于情境化研究
- **Data Analysis**：用于创建结果图形和图表

**推荐工作流程**：始终在创建LaTeX海报之前使用scientific-schematics和generate-image技能以生成所有视觉元素。

## 常见陷阱

**AI生成图形错误（最常见）：**
- ❌ 一个图形中元素太多（10+项）→ 保持最多3-5个
- ❌ AI图形中文本太小 → 指定"巨大（100pt+）"或"巨大（150pt+）"
- ❌ 提示中细节太多 → 使用"简单"和"仅X个元素"
- ❌ 无白色空间规范 → 在每个提示中添加"50%白色空间"
- ❌ 带有8+个步骤的复杂流程图 → 限制到最多4-5个步骤
- ❌ 带有6+个项目的比较图表 → 限制到最多3个项目
- ❌ 带有5+个指标的关键发现 → 仅显示前3个

**修复AI图形中的溢出：**
如果您的AI生成的图形溢出或有小文本：
1. 添加"更简单"或"仅3个元素"到提示
2. 增加字体大小："150pt+"而不是"80pt+"
3. 添加"60%白色空间"而不是"50%"
4. 删除子细节："无子步骤"、"无轴标签"、"无图例"
5. 用更少元素重新生成

**设计错误：**
- ❌ 文本太多（超1000字）
- ❌ 字体大小太小（正文低于24pt）
- ❌ 低对比度颜色组合
- ❌ 拥挤的布局，没有白色空间
- ❌ 跨部分的不一致样式
- ❌ 质量差或像素化的图像

**内容错误：**
- ❌ 没有清晰的叙述或消息
- ❌ 太多研究问题或目标
- ❌ 过度使用术语而不定义
- ❌ 没有上下文或解释的结果
- ❌ 缺少作者联系信息

**技术错误：**
- ❌ 会议要求的海报尺寸错误
- ❌ 发送到CMYK打印机的RGB颜色（颜色偏移）
- ❌ PDF中字体未嵌入
- ❌ 提交门户的文件大小太大
- ❌ QR码太小或未测试

**最佳实践：**
- ✅ 生成具有最多3-5个元素的简单AI图形
- ✅ 使用巨大字体（100pt+）用于图形中的关键数字
- ✅ 在每个AI提示中指定"50%白色空间"
- ✅ 完全遵循会议尺寸规格
- ✅ 在最终打印前以缩小比例测试
- ✅ 使用高对比度、可访问的配色方案
- ✅ 保持文本最少且高度可扫描
- ✅ 包括清晰的联系信息和QR码
- ✅ 仔细校对（错误在海报上被放大！）

## 包安装

确保安装了所需的LaTeX包：

```bash
# 对于TeX Live（Linux/Mac）
tlmgr install beamerposter tikzposter baposter

# 对于MiKTeX（Windows）
# 包通常在首次使用时自动安装

# 其他推荐包
tlmgr install qrcode graphics xcolor tcolorbox subcaption
```

## 脚本和自动化

`scripts/` 目录中可用的辅助脚本：

- `compile_poster.sh`：具有错误处理的自动编译
- `generate_template.py`：交互式模板生成器
- `resize_images.py`：用于海报的批量图像优化
- `poster_checklist.py`：提交前验证工具

## 参考资料

全面的参考文件用于详细指导：

- `references/latex_poster_packages.md`：beamerposter、tikzposter和baposter的详细比较及示例
- `references/poster_layout_design.md`：布局原则、网格系统和视觉流程
- `references/poster_design_principles.md`：排版、颜色理论、视觉层次和可访问性
- `references/poster_content_guide.md`：内容组织、写作风格和部分特定指导

## 模板

`assets/` 目录中可用的即用型海报模板：

- beamerposter模板（经典、现代、彩色）
- tikzposter模板（默认、射线、波浪、信封）
- baposter模板（纵向、横向、最小）
- 来自各种科学学科的示例海报
- 配色方案定义和机构模板

加载这些模板并针对您的特定研究和会议要求进行自定义。
