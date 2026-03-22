---
name: slides
description: 使用 PptxGenJS、捆绑的布局助手和渲染/验证实用程序创建和编辑演示文稿（`.pptx`）。当任务涉及构建新的 PowerPoint 演示文稿、从屏幕截图/PDF/参考演文稿重新创建幻灯片、在保留可编辑输出的同时修改幻灯片内容、添加图表/图表/视觉效果，或诊断布局问题（如溢出、重叠和字体替换）时使用。
---

# Slides

## 概述

使用 PptxGenJS 进行幻灯片创作。不要使用 `python-pptx` 进行演文稿生成，除非任务仅是检查；在 JavaScript 中保持可编辑输出并交付 `.pptx` 和源 `.js`。

将工作保留在任务本地目录中。仅在渲染和验证传递后将最终工件复制到请求的目标。

## 捆绑资源

- `assets/pptxgenjs_helpers/`：将此文件夹复制到演文稿工作区并从那里本地导入，而不是重新实现助手逻辑。
- `scripts/render_slides.py`：将 `.pptx` 或 `.pdf` 光栅化为每张幻灯片的 PNG。
- `scripts/slides_test.py`：检测溢出幻灯片画布的内容。
- `scripts/create_montage.py`：构建渲染幻灯片的联系表风格蒙太奇。
- `scripts/detect_font.py`：报告 LibreOffice 解析它们的缺失或替换字体。
- `scripts/ensure_raster_image.py`：将 SVG/EMF/HEIC/PDF 类资产转换为 PNG 以进行快速检查。
- `references/pptxgenjs-helpers.md`：仅在您需要 API 详细信息或依赖说明时加载。

## 工作流程

1. 检查请求并确定您是创建新演文稿、重新创建现有演文稿还是编辑演文稿。
2. 前期设置幻灯片大小。默认为 16:9（`LAYOUT_WIDE`），除非源材料清楚地使用另一个宽高比。
3. 将 `assets/pptxgenjs_helpers/` 复制到工作目录并从那里导入助手。
4. 使用显式主题字体、稳定间距和实用的 PowerPoint 原生元素在 JavaScript 中构建演文稿。
5. 运行此技能目录中的捆绑脚本或将需要的脚本复制到任务工作区。使用 `render_slides.py` 渲染结果，审查 PNG，并在交付前修复布局问题。
6. 当幻灯片边缘紧或演文稿密集时，运行 `slides_test.py` 进行溢出检查。
7. 交付 `.pptx`、创作 `.js` 以及重建演文稿所需的任何生成的资产。

## 创作规则

- 显式设置主题字体。如果字体排印很重要，不要依赖 PowerPoint 默认值。
- 使用 `autoFontSize`、`calcTextBox` 和相关助手来调整文本框大小；不要使用 PptxGenJS `fit` 或 `autoFit`。
- 使用项目符号选项，而不是字面量 `•` 字符。
- 使用 `imageSizingCrop` 或 `imageSizingContain` 而不是 PptxGenJS 内置图像大小调整。
- 对方程使用 `latexToSvgDataUri()`，对语法高亮的代码块使用 `codeToRuns()`。
- 对简单的条形/线形/饼图/直方图风格视觉效果优先考虑原生 PowerPoint 图表，以便审查者以后可以编辑它们。
- 对于 PptxGenJS 不能很好表达的图表或图表，在外部渲染 SVG 并将 SVG 放在幻灯片中。
- 每当您生成或实质编辑幻灯片时，在提交的 JavaScript 中包括 `warnIfSlideHasOverlaps(slide, pptx)` 和 `warnIfSlideElementsOutOfBounds(slide, pptx)`。
- 在交付之前修复所有非故意的重叠和越界警告。如果重叠是有意的，请在相关元素附近留下简短的代码注释。

## 重新创建或编辑现有幻灯片

- 首先渲染源演文稿或参考 PDF，以便您可以视觉上比较幻灯片几何形状。
- 在重新构建布局之前匹配原始宽高比。
- 尽可能保留可编辑性：文本应保持文本，简单图表应保持原生图表。
- 如果参考幻灯片使用光栅艺术品，请在放置它们之前使用 `ensure_raster_image.py` 从矢量或奇数图像格式生成调试 PNG。

## 验证命令

下面的示例假设您将所需的脚本复制到了工作目录。如果不是，请相对于此技能文件夹调用相同的脚本路径。

```bash
# 将幻灯片渲染为 PNG 以供审查
python3 scripts/render_slides.py deck.pptx --output_dir rendered

# 构建蒙太奇以进行快速扫描
python3 scripts/create_montage.py --input_dir rendered --output_file montage.png

# 检查超出原始幻灯片画布的溢出
python3 scripts/slides_test.py deck.pptx

# 检测缺失或替换的字体
python3 scripts/detect_font.py deck.pptx --json
```

如果您需要助手 API 摘要或依赖详细信息，请加载 `references/pptxgenjs-helpers.md`。
