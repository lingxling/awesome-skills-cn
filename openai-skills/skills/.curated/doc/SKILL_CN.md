---
name: "doc"
description: "当任务涉及读取、创建或编辑 `.docx` 文档时使用，尤其是当格式或布局保真度很重要时；优先使用 `python-docx` 加上捆绑的 `scripts/render_docx.py` 进行视觉检查。"
---

# DOCX 技能

## 何时使用

- 读取或审查布局很重要的 DOCX 内容（表格、图表、分页）。
- 创建或编辑具有专业格式的 DOCX 文件。
- 在交付前验证视觉布局。

## 工作流程

1. 优先视觉审查（布局、表格、图表）。
   - 如果 `soffice` 和 `pdftoppm` 可用，将 DOCX → PDF → PNGs。
   - 或者使用 `scripts/render_docx.py`（需要 `pdf2image` 和 Poppler）。
   - 如果这些工具缺失，安装它们或要求用户在本地查看渲染的页面。
2. 使用 `python-docx` 进行编辑和结构化创建（标题、样式、表格、列表）。
3. 每次有意义的更改后，重新渲染并检查页面。
4. 如果无法进行视觉审查，使用 `python-docx` 提取文本作为后备方案并调用出布局风险。
5. 保持中间输出有序并在最终批准后清理。

## 临时文件和输出约定

- 使用 `tmp/docs/` 作为中间文件；完成后删除。
- 在此仓库中工作时将最终工件写入 `output/doc/`。
- 保持文件名稳定和描述性。

## 依赖项（如果缺失则安装）

优先使用 `uv` 进行依赖管理。

Python 包：
```
uv pip install python-docx pdf2image
```

如果 `uv` 不可用：
```
python3 -m pip install python-docx pdf2image
```

系统工具（用于渲染）：
```
# macOS (Homebrew)
brew install libreoffice poppler

# Ubuntu/Debian
sudo apt-get install -y libreoffice poppler-utils
```

如果在此环境中无法进行安装，告诉用户缺少哪个依赖项以及如何在本地安装它。

## 环境变量

无需环境变量。

## 渲染命令

DOCX → PDF：
```
soffice -env:UserInstallation=file:///tmp/lo_profile_$$ --headless --convert-to pdf --outdir $OUTDIR $INPUT_DOCX
```

PDF → PNGs：
```
pdftoppm -png $OUTDIR/$BASENAME.pdf $OUTDIR/$BASENAME
```

捆绑的辅助工具：
```
python3 scripts/render_docx.py /path/to/file.docx --output_dir /tmp/docx_pages
```

## 质量期望

- 提供客户端就绪的文档：一致的排版、间距、边距和清晰的层次结构。
- 避免格式缺陷：裁剪/重叠文本、断开的表格、不可读字符或默认模板样式。
- 图表、表格和视觉效果必须在渲染的页面中以正确的对齐方式可读。
- 仅使用 ASCII 连字符。避免 U+2011（非断开连字符）和其他 Unicode 破折号。
- 引用和参考必须可读；永远不要留下工具令牌或占位符字符串。

## 最终检查

- 在最终交付前以 100% 缩放重新渲染并检查每一页。
- 修复任何间距、对齐或分页问题并重复渲染循环。
- 确认没有残留物（临时文件、重复渲染），除非用户要求保留它们。
