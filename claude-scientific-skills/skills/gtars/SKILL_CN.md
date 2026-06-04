---
name: gtars
description: 用于Rust中基因组区间分析的高性能工具包，带Python绑定。当处理基因组区域、BED文件、覆盖度轨道、重叠检测、ML模型的标记化或计算基因组学和机器学习应用中的片段分析时使用。
license: Unknown
metadata:
  version: "1.0"
  skill-author: K-Dense Inc.
---






# Gtars: Rust 基因组工具与算法

## 概述

Gtars 是一个基于 Rust 的高性能工具包，用于操作、分析和处理基因组区间数据。它提供了重叠检测、覆盖度分析、机器学习分词以及参考序列管理等专用工具。

在以下场景中使用此技能：
- 基因组区间文件（BED 格式）
- 基因组区域之间的重叠检测
- 覆盖度轨迹生成（WIG、BigWig）
- 基因组机器学习预处理与分词
- 单细胞基因组学中的片段分析
- 参考序列检索与验证

## 安装

### Python 安装

安装 gtars Python 绑定：

```bash
uv pip install gtars
```

### CLI 安装

安装命令行工具（需要 Rust/Cargo）：

```bash
# 安装全部功能
cargo install gtars-cli --features "uniwig overlaprs igd bbcache scoring fragsplit"

# 或仅安装特定功能
cargo install gtars-cli --features "uniwig overlaprs"
```

### Rust 库

为 Rust 项目添加到 Cargo.toml：

```toml
[dependencies]
gtars = { version = "0.1", features = ["tokenizers", "overlaprs"] }
```

## 核心功能

Gtars 按专用模块组织，每个模块专注于特定的基因组分析任务：

### 1. 重叠检测与 IGD 索引

使用整合基因组数据库（IGD）数据结构高效检测基因组区间之间的重叠。

**适用场景：**
- 查找重叠的调控元件
- 变异注释
- 比较 ChIP-seq 峰
- 识别共享的基因组特征

**快速示例：**
```python
import gtars

# 构建 IGD 索引并查询重叠
igd = gtars.igd.build_index("regions.bed")
overlaps = igd.query("chr1", 1000, 2000)
```

详见 `references/overlap.md` 获取重叠检测的完整文档。

### 2. 覆盖度轨迹生成

使用 uniwig 模块从测序数据生成覆盖度轨迹。

**适用场景：**
- ATAC-seq 可及性图谱
- ChIP-seq 覆盖度可视化
- RNA-seq 读段覆盖度
- 差异覆盖度分析

**快速示例：**
```bash
# 生成 BigWig 覆盖度轨迹
gtars uniwig generate --input fragments.bed --output coverage.bw --format bigwig
```

详见 `references/coverage.md` 获取覆盖度分析工作流的详细信息。

### 3. 基因组分词

将基因组区域转换为离散 token，用于机器学习应用，特别是针对基因组数据的深度学习模型。

**适用场景：**
- 基因组机器学习模型的预处理
- 与 geniml 库集成
- 创建位置编码
- 在基因组序列上训练 transformer 模型

**快速示例：**
```python
from gtars.tokenizers import TreeTokenizer

tokenizer = TreeTokenizer.from_bed_file("training_regions.bed")
token = tokenizer.tokenize("chr1", 1000, 2000)
```

详见 `references/tokenizers.md` 获取分词文档。

### 4. 参考序列管理

处理参考基因组序列，并按照 GA4GH refget 协议计算摘要值。

**适用场景：**
- 验证参考基因组完整性
- 提取特定基因组序列
- 计算序列摘要值
- 交叉引用比较

**快速示例：**
```python
# 加载参考序列并提取序列
store = gtars.RefgetStore.from_fasta("hg38.fa")
sequence = store.get_subsequence("chr1", 1000, 2000)
```

详见 `references/refget.md` 获取参考序列操作文档。

### 5. 片段处理

拆分和分析片段文件，特别适用于单细胞基因组学数据。

**适用场景：**
- 处理单细胞 ATAC-seq 数据
- 按细胞条形码拆分片段
- 基于聚类的片段分析
- 片段质量控制

**快速示例：**
```bash
# 按聚类拆分片段
gtars fragsplit cluster-split --input fragments.tsv --clusters clusters.txt --output-dir ./by_cluster/
```

详见 `references/cli.md` 获取片段处理命令文档。

### 6. 片段评分

针对参考数据集对片段重叠进行评分。

**适用场景：**
- 评估片段富集程度
- 将实验数据与参考数据比较
- 计算质量指标
- 跨样本批量评分

**快速示例：**
```bash
# 针对参考数据对片段评分
gtars scoring score --fragments fragments.bed --reference reference.bed --output scores.txt
```

## 常见工作流

### 工作流 1：峰重叠分析

识别重叠的基因组特征：

```python
import gtars

# 加载两组区域
peaks = gtars.RegionSet.from_bed("chip_peaks.bed")
promoters = gtars.RegionSet.from_bed("promoters.bed")

# 查找重叠
overlapping_peaks = peaks.filter_overlapping(promoters)

# 导出结果
overlapping_peaks.to_bed("peaks_in_promoters.bed")
```

### 工作流 2：覆盖度轨迹流程

生成用于可视化的覆盖度轨迹：

```bash
# 步骤 1：生成覆盖度
gtars uniwig generate --input atac_fragments.bed --output coverage.wig --resolution 10

# 步骤 2：转换为 BigWig 以用于基因组浏览器
gtars uniwig generate --input atac_fragments.bed --output coverage.bw --format bigwig
```

### 工作流 3：机器学习预处理

为机器学习准备基因组数据：

```python
from gtars.tokenizers import TreeTokenizer
import gtars

# 步骤 1：加载训练区域
regions = gtars.RegionSet.from_bed("training_peaks.bed")

# 步骤 2：创建分词器
tokenizer = TreeTokenizer.from_bed_file("training_peaks.bed")

# 步骤 3：对区域进行分词
tokens = [tokenizer.tokenize(r.chromosome, r.start, r.end) for r in regions]

# 步骤 4：在机器学习流程中使用 token
# (与 geniml 或自定义模型集成)
```

## Python 与 CLI 用法对比

**使用 Python API 的场景：**
- 与分析流程集成
- 需要程序化控制
- 与 NumPy/Pandas 配合使用
- 构建自定义工作流

**使用 CLI 的场景：**
- 快速的一次性分析
- Shell 脚本编写
- 批量处理文件
- 工作流原型设计

## 参考文档

完整的模块文档：

- **`references/python-api.md`** - 完整的 Python API 参考，包含 RegionSet 操作、NumPy 集成和数据导出
- **`references/overlap.md`** - IGD 索引、重叠检测和集合操作
- **`references/coverage.md`** - 使用 uniwig 生成覆盖度轨迹
- **`references/tokenizers.md`** - 面向机器学习应用的基因组分词
- **`references/refget.md`** - 参考序列管理和摘要值计算
- **`references/cli.md`** - 命令行接口完整参考

## 与 geniml 集成

Gtars 作为 geniml Python 包的基础，为机器学习工作流提供核心基因组区间操作。在进行 geniml 相关任务时，使用 gtars 进行数据预处理和分词。

## 性能特征

- **原生 Rust 性能**：执行速度快，内存开销低
- **并行处理**：针对大数据集的多线程操作
- **内存高效**：支持流式处理和内存映射文件
- **零拷贝操作**：与 NumPy 集成，数据拷贝最小化

## 数据格式

Gtars 支持标准基因组格式：

- **BED**：基因组区间（3 列或扩展格式）
- **WIG/BigWig**：覆盖度轨迹
- **FASTA**：参考序列
- **Fragment TSV**：带条形码的单细胞片段文件

## 错误处理与调试

启用详细日志记录以进行故障排除：

```python
import gtars

# 启用调试日志记录
gtars.set_log_level("DEBUG")
```

```bash
# CLI 详细模式
gtars --verbose <command>
```
