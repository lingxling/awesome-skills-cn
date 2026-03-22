---
name: pysam
description: 基因组文件工具包。读取/写入SAM/BAM/CRAM对齐文件、VCF/BCF变异文件、FASTA/FASTQ序列，提取区域，计算覆盖率，用于NGS数据处理管道。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# Pysam

## 概述

Pysam是一个用于读取、操作和写入基因组数据集的Python模块。通过htslib的Python接口读取/写入SAM/BAM/CRAM对齐文件、VCF/BCF变异文件和FASTA/FASTQ序列。查询tabix索引文件，执行覆盖度的pileup分析，以及执行samtools/bcftools命令。

## 使用场景

当您需要以下操作时使用此技能：
- 处理测序对齐文件（BAM/CRAM）
- 分析遗传变异（VCF/BCF）
- 提取参考序列或基因区域
- 处理原始测序数据（FASTQ）
- 计算覆盖率或读取深度
- 实现生物信息学分析管道
- 测序数据的质量控制
- 变异调用和注释工作流

## 快速开始

### 安装
```bash
uv pip install pysam
```

### 基本示例

**读取对齐文件：**
```python
import pysam

# 打开BAM文件并获取区域内的读取
samfile = pysam.AlignmentFile("example.bam", "rb")
for read in samfile.fetch("chr1", 1000, 2000):
    print(f"{read.query_name}: {read.reference_start}")
samfile.close()
```

**读取变异文件：**
```python
# 打开VCF文件并迭代变异
vcf = pysam.VariantFile("variants.vcf")
for variant in vcf:
    print(f"{variant.chrom}:{variant.pos} {variant.ref}>{variant.alts}")
vcf.close()
```

**查询参考序列：**
```python
# 打开FASTA并提取序列
fasta = pysam.FastaFile("reference.fasta")
sequence = fasta.fetch("chr1", 1000, 2000)
print(sequence)
fasta.close()
```

## 核心功能

### 1. 对齐文件操作（SAM/BAM/CRAM）

使用`AlignmentFile`类处理对齐的测序读取。适用于分析映射结果、计算覆盖率、提取读取或质量控制。

**常见操作：**
- 打开和读取BAM/SAM/CRAM文件
- 从特定基因组区域获取读取
- 按映射质量、标志或其他标准过滤读取
- 写入过滤或修改后的对齐
- 计算覆盖率统计
- 执行pileup分析（碱基级覆盖率）
- 访问读取序列、质量分数和对齐信息

**参考：** 有关详细文档，请参见`references/alignment_files.md`：
- 打开和读取对齐文件
- AlignedSegment属性和方法
- 使用`fetch()`进行基于区域的获取
- 覆盖率的pileup分析
- 写入和创建BAM文件
- 坐标系和索引
- 性能优化提示

### 2. 变异文件操作（VCF/BCF）

使用`VariantFile`类处理来自变异调用管道的遗传变异。适用于变异分析、过滤、注释或群体遗传学。

**常见操作：**
- 读取和写入VCF/BCF文件
- 查询特定区域的变异
- 访问变异信息（位置、等位基因、质量）
- 提取样本的基因型数据
- 按质量、等位基因频率或其他标准过滤变异
- 用额外信息注释变异
- 子集样本或区域

**参考：** 有关详细文档，请参见`references/variant_files.md`：
- 打开和读取变异文件
- VariantRecord属性和方法
- 访问INFO和FORMAT字段
- 处理基因型和样本
- 创建和写入VCF文件
- 过滤和子集变异
- 多样本VCF操作

### 3. 序列文件操作（FASTA/FASTQ）

使用`FastaFile`进行参考序列的随机访问，使用`FastxFile`读取原始测序数据。适用于提取基因序列、根据参考验证变异或处理原始读取。

**常见操作：**
- 按基因组坐标查询参考序列
- 提取感兴趣的基因或区域的序列
- 读取带有质量分数的FASTQ文件
- 验证变异参考等位基因
- 计算序列统计
- 按质量或长度过滤读取
- 在FASTA和FASTQ格式之间转换

**参考：** 有关详细文档，请参见`references/sequence_files.md`：
- FASTA文件访问和索引
- 按区域提取序列
- 处理基因的反向互补
- 顺序读取FASTQ文件
- 质量分数转换和过滤
- 处理tabix索引文件（BED、GTF、GFF）
- 常见序列处理模式

### 4. 集成生物信息学工作流

Pysam擅长集成多种文件类型进行综合基因组分析。常见工作流结合了对齐文件、变异文件和参考序列。

**常见工作流：**
- 计算特定区域的覆盖率统计
- 根据对齐读取验证变异
- 用覆盖率信息注释变异
- 提取变异位置周围的序列
- 根据多个标准过滤对齐或变异
- 生成用于可视化的覆盖率轨道
- 跨多种数据类型的质量控制

**参考：** 有关详细示例，请参见`references/common_workflows.md`：
- 质量控制工作流（BAM统计、参考一致性）
- 覆盖率分析（每碱基覆盖率、低覆盖率检测）
- 变异分析（注释、按读取支持过滤）
- 序列提取（变异上下文、基因序列）
- 读取过滤和子集
- 集成模式（BAM+VCF、VCF+BED等）
- 复杂工作流的性能优化

## 关键概念

### 坐标系

**关键：** Pysam使用**0-based, half-open**坐标（Python约定）：
- 起始位置是0-based（第一个碱基是位置0）
- 结束位置是排他的（不包含在范围内）
- 区域1000-2000包含碱基1000-1999（共1000个碱基）

**例外：** `fetch()`中的区域字符串遵循samtools约定（1-based）：
```python
samfile.fetch("chr1", 999, 2000)      # 0-based: 位置999-1999
samfile.fetch("chr1:1000-2000")       # 1-based字符串: 位置1000-2000
```

**VCF文件：** 在文件格式中使用1-based坐标，但`VariantRecord.start`是0-based。

### 索引要求

对特定基因组区域的随机访问需要索引文件：
- **BAM文件**：需要`.bai`索引（使用`pysam.index()`创建）
- **CRAM文件**：需要`.crai`索引
- **FASTA文件**：需要`.fai`索引（使用`pysam.faidx()`创建）
- **VCF.gz文件**：需要`.tbi` tabix索引（使用`pysam.tabix_index()`创建）
- **BCF文件**：需要`.csi`索引

没有索引时，使用`fetch(until_eof=True)`进行顺序读取。

### 文件模式

打开文件时指定格式：
- `"rb"` - 读取BAM（二进制）
- `"r"` - 读取SAM（文本）
- `"rc"` - 读取CRAM
- `"wb"` - 写入BAM
- `"w"` - 写入SAM
- `"wc"` - 写入CRAM

### 性能考虑

1. **始终使用索引文件**进行随机访问操作
2. **使用`pileup()`进行列分析**，而不是重复的fetch操作
3. **使用`count()`进行计数**，而不是手动迭代和计数
4. **并行处理区域**分析独立基因组区域时
5. **显式关闭文件**以释放资源
6. **使用`until_eof=True`** 用于无索引的顺序处理
7. **避免多个迭代器**，除非必要（如果需要，使用`multiple_iterators=True`）

## 常见陷阱

1. **坐标混淆：** 记住不同上下文中的0-based与1-based系统
2. **缺少索引：** 许多操作需要索引文件—首先创建它们
3. **部分重叠：** `fetch()`返回重叠区域边界的读取，而不仅仅是完全包含的读取
4. **迭代器作用域：** 保持pileup迭代器引用活动，以避免"PileupProxy accessed after iterator finished"错误
5. **质量分数编辑：** 更改`query_sequence`后无法原地修改`query_qualities`—先创建副本
6. **流限制：** 仅支持stdin/stdout进行流处理，不支持任意Python文件对象
7. **线程安全：** 虽然在I/O期间释放GIL，但尚未完全验证全面的线程安全性

## 命令行工具

Pysam提供对samtools和bcftools命令的访问：

```python
# 排序BAM文件
pysam.samtools.sort("-o", "sorted.bam", "input.bam")

# 索引BAM
pysam.samtools.index("sorted.bam")

# 查看特定区域
pysam.samtools.view("-b", "-o", "region.bam", "input.bam", "chr1:1000-2000")

# BCF工具
pysam.bcftools.view("-O", "z", "-o", "output.vcf.gz", "input.vcf")
```

**错误处理：**
```python
try:
    pysam.samtools.sort("-o", "output.bam", "input.bam")
except pysam.SamtoolsError as e:
    print(f"Error: {e}")
```

## 资源

### references/

每个主要功能的详细文档：

- **alignment_files.md** - SAM/BAM/CRAM操作的完整指南，包括AlignmentFile类、AlignedSegment属性、fetch操作、pileup分析和写入对齐

- **variant_files.md** - VCF/BCF操作的完整指南，包括VariantFile类、VariantRecord属性、基因型处理、INFO/FORMAT字段和多样本操作

- **sequence_files.md** - FASTA/FASTQ操作的完整指南，包括FastaFile和FastxFile类、序列提取、质量分数处理和tabix索引文件访问

- **common_workflows.md** - 整合多种文件类型的实用生物信息学工作流示例，包括质量控制、覆盖率分析、变异验证和序列提取

## 获取帮助

有关特定操作的详细信息，请参考相应的参考文档：

- 处理BAM文件或计算覆盖率 → `alignment_files.md`
- 分析变异或基因型 → `variant_files.md`
- 提取序列或处理FASTQ → `sequence_files.md`
- 整合多种文件类型的复杂工作流 → `common_workflows.md`

官方文档：https://pysam.readthedocs.io/