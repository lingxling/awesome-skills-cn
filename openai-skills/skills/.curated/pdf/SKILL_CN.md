---
name: "pdf"
description: "当任务涉及读取、创建或审查渲染和布局很重要的 PDF 文件时使用；通过渲染页面（Poppler）进行视觉检查，并使用 Python 工具（如 `reportlab`、`pdfplumber` 和 `pypdf`）进行生成和提取。"
---


# PDF 技能

## 何时使用
- 读取或审查布局和视觉效果很重要的 PDF 内容。
- 以可靠的格式化方式以编程方式创建 PDF。
- 在交付之前验证最终渲染。

## 工作流程
1. 更喜欢视觉审查：将 PDF 页面渲染为 PNG 并检查它们。
   - 如果可用，使用 `pdftoppm`。
   - 如果不可用，请安装 Poppler 或要求用户在本地审查输出。
2. 创建新文档时使用 `reportlab` 生成 PDF。
3. 使用 `pdfplumber`（或 `pypdf`）进行文本提取和快速检查；不要依赖它进行布局保真度。
4. 在每次有意义的更新后，重新渲染页面并验证对齐、间距和可读性。

## 临时和输出约定
- 使用 `tmp/pdfs/` 作为中间文件；完成后删除。
- 在此仓库中工作时，将最终工件写入 `output/pdf/`。
- 保持文件名稳定和描述性。

## 依赖项（如果缺少则安装）
更喜欢 `uv` 进行依赖管理。

Python 包：
```
uv pip install reportlab pdfplumber pypdf
```
如果 `uv` 不可用：
```
python3 -m pip install reportlab pdfplumber pypdf
```
系统工具（用于渲染）：
```
# macOS (Homebrew)
brew install poppler

# Ubuntu/Debian
sudo apt-get install -y poppler-utils
```

如果在此环境中无法安装，请告诉用户缺少哪个依赖项以及如何在本地安装它。

## 环境
没有必需的环境变量。

## 渲染命令
```
pdftoppm -png $INPUT_PDF $OUTPUT_PREFIX
```

## 质量期望
- 保持精美的视觉设计：一致的排版、间距、边距和部分层次结构。
- 避免渲染问题：剪裁的文本、重叠的元素、损坏的表格、黑色方块或不可读的字形。
- 图表、表格和图像必须清晰、对齐并清晰标记。
- 仅使用 ASCII 连字符。避免 U+2011（不换行连字符）和其他 Unicode 破折号。
- 引用和参考必须是可读的；永远不要留下工具令牌或占位符字符串。

## 最终检查
- 在最新的 PNG 检查显示零视觉或格式缺陷之前不要交付。
- 确认页眉/页脚、页码和部分过渡看起来精美。
- 保持中间文件有序或在最终批准后删除它们。
