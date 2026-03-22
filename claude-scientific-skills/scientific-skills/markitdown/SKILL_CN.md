---
name: markitdown
description: 将各种文件格式转换为Markdown的工具。支持PDF、DOCX、PPTX、XLSX、图像（带OCR）、音频（带转录）、HTML、CSV、JSON、XML、ZIP、YouTube URL、EPub等格式的转换。适用于文档处理、内容提取、数据分析和自动化工作流程。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# MarkItDown

## 概述

MarkItDown是一个将各种文件格式转换为Markdown的工具。它支持PDF、DOCX、PPTX、XLSX、图像（带OCR）、音频（带转录）、HTML、CSV、JSON、XML、ZIP、YouTube URL、EPub等格式的转换，适用于文档处理、内容提取、数据分析和自动化工作流程。

## 核心能力

### 1. 文档转换

- **PDF转换**：将PDF文档转换为Markdown
- **DOCX转换**：将Word文档转换为Markdown
- **PPTX转换**：将PowerPoint演示文稿转换为Markdown
- **其他文档格式**：支持其他文档格式

### 2. 图像处理

- **图像转换**：将图像转换为Markdown文本
- **OCR功能**：使用OCR从图像中提取文本
- **图像描述**：生成图像的描述

### 3. 音频处理

- **音频转换**：将音频文件转换为Markdown文本
- **音频转录**：使用语音识别转录音频
- **音频描述**：生成音频的描述

### 4. 网页处理

- **HTML转换**：将HTML网页转换为Markdown
- **网页抓取**：抓取网页内容并转换为Markdown
- **URL处理**：处理URL并转换为Markdown

### 5. 数据文件处理

- **CSV转换**：将CSV文件转换为Markdown表格
- **JSON转换**：将JSON文件转换为Markdown
- **XML转换**：将XML文件转换为Markdown
- **其他数据格式**：支持其他数据格式

### 6. 其他格式

- **ZIP文件**：处理ZIP文件中的内容
- **YouTube URL**：从YouTube URL提取内容
- **EPub**：将EPub电子书转换为Markdown

## 何时使用此技能

在以下情况下使用此技能：
- 将文档转换为Markdown格式
- 从图像中提取文本（OCR）
- 转录音频文件
- 抓取网页内容
- 处理数据文件
- 提取PDF内容
- 转换Office文档
- 自动化文档处理工作流程

## 安装

```bash
pip install markitdown
```

## 使用示例

### 基本使用

```python
from markitdown import MarkItDown

# 创建MarkItDown实例
md = MarkItDown()

# 转换文件
result = md.convert("document.pdf")

# 输出Markdown
print(result.text_content)
```

### PDF转换

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("document.pdf")

# 保存Markdown
with open("output.md", "w", encoding="utf-8") as f:
    f.write(result.text_content)
```

### 图像转换（带OCR）

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("image.png")

# 输出提取的文本
print(result.text_content)
```

### 音频转换（带转录）

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("audio.mp3")

# 输出转录的文本
print(result.text_content)
```

### HTML转换

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("https://example.com")

# 输出Markdown
print(result.text_content)
```

### CSV转换

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("data.csv")

# 输出Markdown表格
print(result.text_content)
```

### YouTube URL转换

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("https://www.youtube.com/watch?v=VIDEO_ID")

# 输出转录的文本
print(result.text_content)
```

### 批量转换

```python
from markitdown import MarkItDown
import os

md = MarkItDown()

# 遍历目录中的所有文件
for filename in os.listdir("input_dir"):
    if filename.endswith(".pdf"):
        input_path = os.path.join("input_dir", filename)
        output_path = os.path.join("output_dir", filename.replace(".pdf", ".md"))
        
        # 转换文件
        result = md.convert(input_path)
        
        # 保存Markdown
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.text_content)
        
        print(f"已转换: {filename}")
```

## 支持的格式

### 文档格式
- **PDF**：PDF文档
- **DOCX**：Word文档
- **PPTX**：PowerPoint演示文稿
- **其他**：其他文档格式

### 图像格式
- **PNG**：PNG图像
- **JPG/JPEG**：JPEG图像
- **TIFF**：TIFF图像
- **其他**：其他图像格式

### 音频格式
- **MP3**：MP3音频
- **WAV**：WAV音频
- **其他**：其他音频格式

### 网页格式
- **HTML**：HTML网页
- **URL**：网页URL

### 数据格式
- **CSV**：CSV文件
- **JSON**：JSON文件
- **XML**：XML文件
- **其他**：其他数据格式

### 其他格式
- **ZIP**：ZIP文件
- **YouTube URL**：YouTube视频URL
- **EPub**：EPub电子书

## 高级功能

### 自定义转换选项

```python
from markitdown import MarkItDown

md = MarkItDown()

# 自定义转换选项
result = md.convert("document.pdf", options={
    "extract_images": True,
    "preserve_formatting": True,
    "ocr_language": "chi_sim+eng"
})
```

### 处理转换错误

```python
from markitdown import MarkItDown

md = MarkItDown()

try:
    result = md.convert("document.pdf")
    print(result.text_content)
except Exception as e:
    print(f"转换失败: {e}")
```

### 获取转换元数据

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("document.pdf")

# 获取元数据
print(f"标题: {result.title}")
print(f"作者: {result.author}")
print(f"创建日期: {result.created_date}")
```

## 最佳实践

1. **错误处理**：实现适当的错误处理
2. **批量处理**：使用批量处理提高效率
3. **内存管理**：处理大文件时注意内存使用
4. **编码处理**：正确处理文件编码
5. **格式验证**：验证输入文件格式
6. **输出优化**：优化输出Markdown格式

## 常见问题

**Q: MarkItDown支持哪些格式？**
A: 支持PDF、DOCX、PPTX、XLSX、图像、音频、HTML、CSV、JSON、XML、ZIP、YouTube URL、EPub等格式。

**Q: 如何处理大型PDF文件？**
A: 可以分页处理或使用流式处理。

**Q: OCR支持哪些语言？**
A: 支持多种语言，包括中文、英文等。

**Q: 如何提高OCR准确性？**
A: 使用高质量图像、选择正确的语言、调整OCR参数。

## 资源

- **MarkItDown文档**：https://github.com/microsoft/markitdown
- **MarkItDown GitHub**：https://github.com/microsoft/markitdown
