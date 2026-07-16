---
name: liteparse
description: 具有空间文本和边界框的本地文档和PDF解析。用于从PDF、DOCX、Office文件和图像中提取文本；对扫描件进行OCR；保留布局的JSON用于RAG；批量摄入论文文件夹；或用于多模态代理的页面截图——即使用户没有提及liteparse。当需要bboxes、快速本地解析或PNG页面渲染时优先于MarkItDown；合并/拆分/表单优先于pdf技能。
license: Apache-2.0
allowed-tools: Read Write Edit Bash
compatibility: Python 3.10+。可选LibreOffice（Office格式）和ImageMagick（图像）。捆绑Tesseract进行OCR。所有处理都是本地的——无需云API。
metadata: {"version": "1.0", "skill-author": "K-Dense Inc."}
---






# LiteParse — 本地文档解析

## 概述

LiteParse 是一个快速、开源的文档解析器（Rust 核心，Python/Node 绑定），专注于具有边界框的**本地、布局感知文本提取**。它不产生 Markdown，也不调用云 LLM。输出是**纯文本**（保留布局）或具有每页 `text_items`（位置、字体元数据、可选置信度）的**结构化 JSON**。

**版本说明：** 示例针对 **liteparse 2.0.0**（PyPI，2025 年 5 月）。上游 V1 分支是遗留版本；此技能仅记录 **V2 / main**。

关于解析器选择与 MarkItDown、pdf 技能或 LlamaParse 的比较，见 `references/choosing_a_parser.md`。

## 何时使用此技能

当您需要以下功能时使用 LiteParse：

- **快速本地解析** PDF 或转换后的 Office/图像文件，无需云依赖
- **空间文本**，具有用于布局感知 RAG、引用锚定或图表/表格区域逻辑的边界框
- **OCR** 用于扫描的 PDF 或图像（捆绑 Tesseract，或用户运行的 HTTP OCR 服务器）
- **页面截图**（PNG），用于必须看到图表、图表或手写的多模态代理
- **批量导入** 文献文件夹、补充 PDF 或协议库
- **页面子集** 或 **密码保护的** PDF

## 何时不使用

| 任务 | 使用替代方案 |
|------|-------------|
| 用于 LLM 摄入的 Markdown（EPUB、音频、YouTube、HTML） | `markitdown` 技能 |
| 合并/拆分 PDF、表单、水印、旋转 | `pdf` 技能 |
| 密集表格、手写、生产云管道 | [LlamaParse](https://docs.cloud.llamaindex.ai/llamaparse/overview)（云；需单独注册） |

## 安装

```bash
uv pip install "liteparse==2.0.0"
```

这将安装 Python 绑定和 **`lit`** CLI。验证：

```bash
lit --help
python -c "import liteparse; print(liteparse.__version__)"
```

**可选系统工具**（用于非 PDF 输入）：

- **LibreOffice** — Word、Excel、PowerPoint、OpenDocument、CSV/TSV
- **ImageMagick** — PNG、JPEG、TIFF、WebP、SVG 等

安装命令在 `references/ocr_and_formats.md` 中。

**Node.js / TypeScript**（可选）：`npm i @llamaindex/liteparse` — 见 `references/api_reference.md`。

## 快速开始

### Python

```python
from liteparse import LiteParse

parser = LiteParse(quiet=True)
result = parser.parse("paper.pdf")
print(result.text)

for page in result.pages:
    print(f"Page {page.page_num}: {len(page.text_items)} items")
```

### CLI

```bash
# 保留布局的文本（默认）
lit parse paper.pdf

# 带边界框的结构化 JSON
lit parse paper.pdf --format json -o paper.json

# 在原生 PDF 上禁用 OCR（更快）
lit parse paper.pdf --no-ocr
```

## 核心工作流程

### 1. 解析为保留布局的文本

最适合快速获取完整文档文本或馈送给不需要坐标的分块器。

```python
parser = LiteParse(ocr_enabled=True, quiet=True)
result = parser.parse("document.pdf")
full_text = result.text
```

```bash
lit parse document.pdf -o output.txt
```

### 2. 解析为结构化 JSON（边界框）

在构建布局感知 RAG、突出显示源区域或连接文本与截图时使用。

```python
import json
from liteparse import LiteParse

parser = LiteParse(output_format="json", quiet=True)
result = parser.parse("document.pdf")

# 程序化访问
for page in result.pages:
    for item in page.text_items:
        bbox = (item.x, item.y, item.width, item.height)
        # item.text, item.confidence, item.font_name, item.font_size
```

```bash
lit parse document.pdf --format json -o document.json
```

JSON 字段布局：`references/output_formats.md`。

### 3. 解析特定页面

```python
parser = LiteParse(target_pages="1-5,10,15-20", quiet=True)
result = parser.parse("long_paper.pdf")
```

```bash
lit parse long_paper.pdf --target-pages "1-5,10"
```

### 4. 从字节或 stdin 解析

对上传、S3 下载或管道传输远程 PDF 很有用。

```python
with open("document.pdf", "rb") as f:
    result = parser.parse(f.read())
```

```bash
curl -sL https://example.com/report.pdf | lit parse -
```

### 5. 为多模态代理截取页面截图

截图捕获纯文本提取遗漏的视觉内容（图表、复杂表格、手写）。

```python
from pathlib import Path

parser = LiteParse(dpi=150, quiet=True)
shots = parser.screenshot("document.pdf", page_numbers=[1, 2, 3])
out = Path("screenshots")
out.mkdir(exist_ok=True)
for s in shots:
    (out / f"page_{s.page_num}.png").write_bytes(s.image_bytes)
```

```bash
lit screenshot document.pdf --target-pages "1,3,5" -o ./screenshots
lit screenshot document.pdf --dpi 300 -o ./screenshots
```

当代理需要同一页面的坐标和像素时，结合 **JSON 解析 + 截图**。

### 6. 批量解析目录

对于大型语料库，优先使用 CLI（并行 OCR 工作线程）或捆绑脚本。

```bash
lit batch-parse ./papers ./parsed --format json --recursive
lit batch-parse ./papers ./parsed --extension .pdf --no-ocr
```

```bash
python scripts/batch_parse_dir.py ./papers ./parsed --format json --recursive
```

见 `scripts/batch_parse_dir.py` 用于无网络调用的 Python 批量包装器。

### 7. OCR 配置

OCR **默认开启**。Tesseract 已捆绑；基本英语 OCR 无需额外安装。

```python
parser = LiteParse(
    ocr_enabled=True,
    ocr_language="eng",       # Tesseract 代码：fra、deu 等
    num_workers=4,            # 并行 OCR（默认：CPU 核心数 - 1）
    dpi=150,                  # 更高 DPI → 更好 OCR，更慢
)
```

```bash
lit parse scan.pdf --ocr-language fra
lit parse scan.pdf --no-ocr
lit parse scan.pdf --ocr-server-url http://localhost:8080/ocr
```

**离线/气隙：** 设置 `TESSDATA_PREFIX` 到 `.traineddata` 文件目录，或传递 `--tessdata-path`。详情：`references/ocr_and_formats.md`。

### 8. 加密 PDF

```python
parser = LiteParse(password="secret", quiet=True)
result = parser.parse("protected.pdf")
```

```bash
lit parse protected.pdf --password secret
```

### 9. 按短语搜索文本项

合并相邻项并返回短语的组合边界框（例如节标题）。

```python
from liteparse import search_items

page = result.get_page(1)
matches = search_items(page.text_items, "Materials and Methods", case_sensitive=False)
```

## 多格式输入

| 类别 | 扩展名（示例） | 要求 |
|------|--------------|------|
| PDF | `.pdf` | 原生 |
| Office | `.docx`、`.xlsx`、`.pptx`、`.doc`、`.odt`、… | LibreOffice |
| 图像 | `.png`、`.jpg`、`.tiff`、`.webp`、`.svg`、… | ImageMagick |

文件在内部转换为 PDF，然后解析。如果转换工具缺失，解析失败并显示可操作的错误 — 安装依赖并重试。

## 性能提示

- **`--no-ocr`** 在数字原生 PDF 上 — 最大加速
- **`target_pages`** — 仅解析方法/补充部分
- **`num_workers`** — 跨 CPU 核心扩展 OCR
- **`max_pages`** — 限制非常大的文件（默认 1000）
- **`lit batch-parse`** — 带 `--recursive` 和 `--extension` 的目录级作业
- 降低 **`dpi`**（例如 100）当 OCR 质量已经足够时

## 参考文件

| 文件 | 需要时阅读 |
|------|-----------|
| `references/choosing_a_parser.md` | 不确定是否使用 LiteParse、MarkItDown、pdf 或 LlamaParse |
| `references/api_reference.md` | Python/TypeScript API、类型、`search_items` |
| `references/cli_reference.md` | 完整 `lit` 命令标志 |
| `references/output_formats.md` | JSON 模式、边界框、置信度分数 |
| `references/ocr_and_formats.md` | Tesseract、HTTP OCR、LibreOffice、ImageMagick |

## 故障排除

| 问题 | 修复 |
|------|------|
| Office 文件失败 | 安装 LibreOffice；确保 `soffice` 在 PATH 上（Windows：添加 LibreOffice `program` 目录） |
| 图像失败 | 安装 ImageMagick；验证 `convert` 或 `magick` 可用 |
| OCR 质量差 | 增加 `--dpi`；尝试 `--ocr-language`；或 HTTP OCR 服务器 |
| OCR 慢 | 如果不需要则 `--no-ocr`；减少页面；增加 `num_workers` |
| 气隙 OCR | `export TESSDATA_PREFIX=/path/to/tessdata` 或 `--tessdata-path` |
| 字节上 `ParseError` | 确保输入是有效的 PDF 字节（Office 字节需要文件路径 + 转换） |

## 资源

- **GitHub**: https://github.com/run-llama/liteparse
- **文档**: https://developers.llamaindex.ai/liteparse/
- **PyPI**: https://pypi.org/project/liteparse/2.0.0/
- **npm**: https://www.npmjs.com/package/@llamaindex/liteparse
- **OCR API 规范**: https://github.com/run-llama/liteparse/blob/main/OCR_API_SPEC.md
