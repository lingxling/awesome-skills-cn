---
name: gtars
description: 用于Rust中基因组区间分析的高性能工具包，具有Python绑定。用于处理基因组区域、BED文件、覆盖轨道、重叠检测、ML模型的标记化或计算基因组学和机器学习应用中的片段分析。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# Gtars: Rust中的基因组工具和算法

## 概述

Gtars是一个用于操作、分析和处理基因组区间数据的高性能Rust工具包。它提供专门用于重叠检测、覆盖分析、机器学习标记化和参考序列管理的专用工具。

在以下情况下使用此技能：
- 基因组区间文件（BED格式）
- 基因组区域之间的重叠检测
- 覆盖轨道生成（WIG、BigWig）
- 基因组ML预处理和标记化
- 单细胞基因组学中的片段分析
- 参考序列检索和验证

## 安装

### Python 安装

安装gtars Python绑定：

```bash
uv uv pip install gtars
```

### CLI 安装

安装命令行工具（需要Rust/Cargo）：

```bash
# 安装所有功能
cargo install gtars-cli --features "uniwig overlaprs igd bbcache scoring fragsplit"

# 或仅安装特定功能
cargo install gtars-cli --features "uniwig overlaprs"
```

### Rust 库

将以下内容添加到Rust项目的Cargo.toml中：

```toml
[dependencies]
gtars = { version = "0.1", features = ["tokenizers", "overlaprs"] }
```

## 核心功能

Gtars组织为专用模块，每个模块专注于特定的基因组分析任务：

### 1. 重叠检测和IGD索引

使用集成基因组数据库（IGD）数据结构高效检测基因组区间之间的重叠。

**何时使用：**
- 查找重叠的调控元件
- 变体注释
- 比较ChIP-seq峰
- 识别共享的基因组特征

**快速示例：**
```python
import gtars

# 构建IGD索引并查询重叠
igd = gtars.igd.build_index("regions.bed")
overlaps = igd.query("chr1", 1000, 2000)
```

参见 `references/overlap.md` 获取全面的重叠检测文档。

### 2. 覆盖轨道生成

使用uniwig模块从测序数据生成覆盖轨道。

**何时使用：**
- ATAC-seq可访问性概况
- ChIP-seq覆盖可视化
- RNA-seq读取覆盖
- 差异覆盖分析

**快速示例：**
```bash
# 生成BigWig覆盖轨道
gtars uniwig generate --input fragments.bed --output coverage.bw --format bigwig
```

参见 `references/coverage.md` 获取详细的覆盖分析工作流。

### 3. 基因组标记化

将基因组区域转换为机器学习应用的离散标记，特别用于基因组数据的深度学习模型。

**何时使用：**
- 基因组ML模型的预处理
- 与geniml库集成
- 创建位置编码
- 在基因组序列上训练transformer模型

**快速示例：**
```python
from gtars.tokenizers import TreeTokenizer

tokenizer = TreeTokenizer.from_bed_file("training_regions.bed")
token = tokenizer.tokenize("chr1", 1000, 2000)
```

参见 `references/tokenizers.md` 获取标记化文档。

### 4. 参考序列管理

按照GA4GH refget协议处理参考基因组序列并计算摘要。

**何时使用：**
- 验证参考基因组完整性
- 提取特定基因组序列
- 计算序列摘要
- 交叉引用比较

**快速示例：**
```python
# 加载参考并提取序列
store = gtars.RefgetStore.from_fasta("hg38.fa")
sequence = store.get_subsequence("chr1", 1000, 2000)
```

参见 `references/refget.md` 获取参考序列操作。

### 5. 片段处理

分割和分析片段文件，特别适用于单细胞基因组学数据。

**何时使用：**
- 处理单细胞ATAC-seq数据
- 按细胞条形码分割片段
- 基于簇的片段分析
- 片段质量控制

**快速示例：**
```bash
# 按簇分割片段
gtars fragsplit cluster-split --input fragments.tsv --clusters clusters.txt --output-dir ./by_cluster/
```

参见 `references/cli.md` 获取片段处理命令。

### 6. 片段评分

对参考数据集的片段重叠进行评分。

**何时使用：**
- 评估片段富集
- 将实验数据与参考比较
- 质量指标计算
- 跨样本批量评分

**快速示例：**
```bash
# 对参考评分片段
gtars scoring score --fragments fragments.bed --reference reference.bed --output scores.txt
```

## 常见工作流

### 工作流1：峰重叠分析

识别重叠的基因组特征：

```python
import gtars

# 加载两个区域集
peaks = gtars.RegionSet.from_bed("chip_peaks.bed")
promoters = gtars.RegionSet.from_bed("promoters.bed")

# 查找重叠
overlapping_peaks = peaks.filter_overlapping(promoters)

# 导出结果
overlapping_peaks.to_bed("peaks_in_promoters.bed")
```

### 工作流2：覆盖轨道管道

生成覆盖轨道以进行可视化：

```bash
# 步骤1：生成覆盖
gtars uniwig generate --input atac_fragments.bed --output coverage.wig --resolution 10

# 步骤2：转换为BigWig以用于基因组浏览器
gtars uniwig generate --input atac_fragments.bed --output coverage.bw --format bigwig
```

### 工作流3：ML预处理

为机器学习准备基因组数据：

```python
from gtars.tokenizers import TreeTokenizer
import gtars

# 步骤1：加载训练区域
regions = gtars.RegionSet.from_bed("training_peaks.bed")

# 步骤2：创建标记器
tokenizer = TreeTokenizer.from_bed_file("training_peaks.bed")

# 步骤3：标记化区域
tokens = [tokenizer.tokenize(r.chromosome, r.start, r.end) for r in regions]

# 步骤4：在ML管道中使用标记
# （与geniml或自定义模型集成）
```

## Python vs CLI 使用

**使用Python API当：**
- 与分析管道集成
- 需要程序化控制
- 使用NumPy/Pandas
- 构建自定义工作流

**使用CLI当：**
- 快速一次性分析
- Shell脚本
- 批量处理文件
- 原型制作工作流

## 参考文档

全面的模块文档：

- **`references/python-api.md`** - 完整的Python API参考，包括RegionSet操作、NumPy集成和数据导出
- **`references/overlap.md`** - IGD索引、重叠检测和集合操作
- **`references/coverage.md`** - 使用uniwig进行覆盖轨道生成
- **`references/tokenizers.md`** - 用于ML应用的基因组标记化
- **`references/refget.md`** - 参考序列管理和摘要
- **`references/cli.md`** - 命令行界面完整参考

## 与geniml集成

Gtars作为geniml Python包的基础，为机器学习工作流提供核心基因组区间操作。在处理geniml相关任务时，使用gtars进行数据预处理和标记化。

## 性能特征

- **原生Rust性能**：快速执行，低内存开销
- **并行处理**：大型数据集的多线程操作
- **内存效率**：流式和内存映射文件支持
- **零拷贝操作**：NumPy集成，最少数据复制

## 数据格式

Gtars使用标准基因组格式：

- **BED**：基因组区间（3列或扩展）
- **WIG/BigWig**：覆盖轨道
- **FASTA**：参考序列
- **片段TSV**：带有条形码的单细胞片段文件

## 错误处理和调试

启用详细日志记录以进行故障排除：

```python
import gtars

# 启用调试日志
gtars.set_log_level("DEBUG")
```

```bash
# CLI详细模式
gtars --verbose <command>
```
