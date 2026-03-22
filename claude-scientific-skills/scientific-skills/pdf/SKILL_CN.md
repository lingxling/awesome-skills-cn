---
name: pdf
description: 当用户需要处理PDF文件时使用此技能。包括读取或提取PDF中的文本/表格、将多个PDF合并为一个、拆分PDF、旋转页面、添加水印、创建新PDF、填写PDF表单、加密/解密PDF、提取图像以及对扫描PDF进行OCR使其可搜索。如果用户提到.pdf文件或要求生成PDF，使用此技能。
license: 专有。LICENSE.txt包含完整条款
---

# PDF处理指南

## 概述

本指南涵盖使用Python库和命令行工具进行的基本PDF处理操作。有关高级功能、JavaScript库和详细示例，请参阅REFERENCE.md。如果需要填写PDF表单，请阅读FORMS.md并按照其说明操作。

## 快速开始

```python
from pypdf import PdfReader, PdfWriter

# 读取PDF
reader = PdfReader("document.pdf")
print(f"页数: {len(reader.pages)}")

# 提取文本
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## Python库

### pypdf - 基本操作

#### 合并PDF
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

#### 拆分PDF
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

#### 提取元数据
```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"标题: {meta.title}")
print(f"作者: {meta.author}")
print(f"主题: {meta.subject}")
print(f"创建者: {meta.creator}")
```

#### 旋转页面
```python
reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # 顺时针旋转90度
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### pdfplumber - 文本和表格提取

#### 提取带布局的文本
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

#### 提取表格
```python
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"第{i+1}页的第{j+1}个表格:")
            for row in table:
                print(row)
```

#### 高级表格提取
```python
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:  # 检查表格是否非空
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# 合并所有表格
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

### reportlab - 创建PDF

#### 基本PDF创建
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter

# 添加文本
c.drawString(100, height - 100, "你好，世界！")
c.drawString(100, height - 120, "这是使用reportlab创建的PDF")

# 添加线条
c.line(100, height - 140, 400, height - 140)

# 保存
c.save()
```

#### 创建多页PDF
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# 添加内容
title = Paragraph("报告标题", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

body = Paragraph("这是报告的正文。" * 20, styles['Normal'])
story.append(body)
story.append(PageBreak())

# 第2页
story.append(Paragraph("第2页", styles['Heading1']))
story.append(Paragraph("第2页的内容", styles['Normal']))

# 构建PDF
doc.build(story)
```

#### 下标和上标

**重要**：在ReportLab PDF中永远不要使用Unicode下标/上标字符（₀₁₂₃₄₅₆₇₈₉, ⁰¹²³⁴⁵⁶⁷⁸⁹）。内置字体不包含这些字形，会导致它们渲染为实心黑框。

相反，在Paragraph对象中使用ReportLab的XML标记标签：
```python
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

# 下标：使用 <sub> 标签
chemical = Paragraph("H<sub>2</sub>O", styles['Normal'])

# 上标：使用 <super> 标签
squared = Paragraph("x<super>2</super> + y<super>2</super>", styles['Normal'])
```

对于画布绘制的文本（非Paragraph对象），手动调整字体大小和位置，而不是使用Unicode下标/上标。

## 命令行工具

### pdftotext (poppler-utils)
```bash
# 提取文本
pdftotext input.pdf output.txt

# 保留布局提取文本
pdftotext -layout input.pdf output.txt

# 提取特定页面
pdftotext -f 1 -l 5 input.pdf output.txt  # 第1-5页
```

### qpdf
```bash
# 合并PDF
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# 拆分页面
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf --pages . 6-10 -- pages6-10.pdf

# 旋转页面
qpdf input.pdf output.pdf --rotate=+90:1  # 将第1页旋转90度

# 移除密码
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

### pdftk（如果可用）
```bash
# 合并
pdftk file1.pdf file2.pdf cat output merged.pdf

# 拆分
pdftk input.pdf burst

# 旋转
pdftk input.pdf rotate 1east output rotated.pdf
```

## 常见任务

### 从扫描PDF中提取文本
```python
# 需要：pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path

# 将PDF转换为图像
images = convert_from_path('scanned.pdf')

# 对每一页进行OCR
text = ""
for i, image in enumerate(images):
    text += f"第{i+1}页:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

### 添加水印
```python
from pypdf import PdfReader, PdfWriter

# 创建水印（或加载现有水印）
watermark = PdfReader("watermark.pdf").pages[0]

# 应用到所有页面
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

### 提取图像
```bash
# 使用pdfimages (poppler-utils)
pdfimages -j input.pdf output_prefix

# 这会将所有图像提取为 output_prefix-000.jpg, output_prefix-001.jpg 等
```

### 密码保护
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# 添加密码
writer.encrypt("userpassword", "ownerpassword")

with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

## 快速参考

| 任务 | 最佳工具 | 命令/代码 |
|------|-----------|--------------|
| 合并PDF | pypdf | `writer.add_page(page)` |
| 拆分PDF | pypdf | 每页一个文件 |
| 提取文本 | pdfplumber | `page.extract_text()` |
| 提取表格 | pdfplumber | `page.extract_tables()` |
| 创建PDF | reportlab | Canvas或Platypus |
| 命令行合并 | qpdf | `qpdf --empty --pages ...` |
| OCR扫描PDF | pytesseract | 先转换为图像 |
| 填写PDF表单 | pdf-lib或pypdf（见FORMS.md） | 见FORMS.md |

## 后续步骤

- 有关高级pypdfium2用法，请参阅REFERENCE.md
- 有关JavaScript库（pdf-lib），请参阅REFERENCE.md
- 如果需要填写PDF表单，请按照FORMS.md中的说明操作
- 有关故障排除指南，请参阅REFERENCE.md