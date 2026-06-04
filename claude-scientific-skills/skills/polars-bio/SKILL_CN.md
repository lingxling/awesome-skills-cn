---
name: polars-bio
description: 在Polars DataFrames上进行高性能基因组区间操作和生物信息学文件I/O。支持BED/VCF/BAM/GFF区间的重叠、最近邻、合并、覆盖、补集、减法操作。支持流式处理、云原生架构，是bioframe的更快替代方案。
license: Apache-2.0
allowed-tools: Read Write Edit Bash
compatibility: Requires Python 3.11–3.14 and polars-bio (uv pip install). Cloud I/O uses standard AWS/GCS/Azure SDK env vars when paths use s3://, gs://, or az:// URIs.
metadata:
  version: "1.0"
  skill-author: K-Dense Inc.
---






# polars-bio

## 概述

polars-bio 是一个基于 Polars、Apache Arrow 和 Apache DataFusion 构建的高性能 Python 库，用于基因组区间操作和生物信息学文件 I/O。它为区间运算（重叠、最近邻、合并、覆盖、互补、减法）和读取/写入常见生物信息学格式（BED、VCF、BAM、CRAM、GFF/GTF、FASTA、FASTQ）提供熟悉的 DataFrame -centric API。

核心价值主张：
- 在真实基因组基准上比 bioframe **快 6-38 倍**
- 通过 DataFusion 支持大型基因组的**流式/核外**处理
- **云原生**文件 I/O（S3、GCS、Azure），带谓词下推
- **两种 API 风格**：函数式（`pb.overlap(df1, df2)`）和链式方法（`df1.lazy().pb.overlap(df2)`）
- 通过 DataFusion SQL 引擎对基因组数据进行**SQL 接口**

## 何时使用此技能

当您有以下需求时使用此技能：
- 执行基因组区间操作（重叠、最近邻、合并、覆盖、互补、减法）
- 读取/写入生物信息学文件格式（BED、VCF、BAM、CRAM、GFF/GTF、FASTA、FASTQ）
- 处理不适合内存的大型基因组数据集（流式模式）
- 对基因组数据文件运行 SQL 查询
- 从 bioframe 迁移到更快的替代方案
- 从 BAM/CRAM 文件计算读数深度/堆积
- 处理包含基因组区间的 Polars DataFrame

## 快速开始

### 安装

需要 Python 3.11–3.14（见 [PyPI](https://pypi.org/project/polars-bio/)）。

```bash
uv pip install "polars-bio==0.31.0"
```

要获取 pandas 兼容性（pandas ≥3.0）：

```bash
uv pip install "polars-bio[pandas]==0.31.0"
```

### 基本重叠示例

```python
import polars as pl
import polars_bio as pb

# 创建两个区间 DataFrame
df1 = pl.DataFrame({
    "chrom": ["chr1", "chr1", "chr1"],
    "start": [1, 5, 22],
    "end":   [6, 9, 30],
})

df2 = pl.DataFrame({
    "chrom": ["chr1", "chr1"],
    "start": [3, 25],
    "end":   [8, 28],
})

# 函数式 API（默认返回 LazyFrame）
result = pb.overlap(df1, df2)
result_df = result.collect()

# 直接获取 DataFrame
result_df = pb.overlap(df1, df2, output_type="polars.DataFrame")

# 链式方法 API（通过 LazyFrame 的 .pb 访问器）
result = df1.lazy().pb.overlap(df2)
result_df = result.collect()
```

### 读取 BED 文件

```python
import polars_bio as pb

# 立即读取（加载整个文件）
df = pb.read_bed("regions.bed")

# 懒扫描（流式，用于大文件）
lf = pb.scan_bed("regions.bed")
result = lf.collect()
```

## 核心能力

### 1. 基因组区间操作

polars-bio 提供 8 个核心区间操作，用于基因组范围运算。所有操作接受带有 `chrom`、`start`、`end` 列（可配置）的 Polars DataFrame。所有操作默认返回 `LazyFrame`（使用 `output_type="polars.DataFrame"` 获取即时结果）。

**操作：**
- `overlap` / `count_overlaps` - 查找或计数两组之间的重叠区间（`overlap_output="left"` 自 0.30.0 起返回仅 df1 的命中）
- `nearest` - 查找最近的区间（带可配置的 `k`、`overlap`、`distance` 参数）
- `merge` - 合并集合内的重叠/相邻区间
- `cluster` - 为重叠区间分配聚类 ID
- `coverage` - 计算每个区间的覆盖计数（双输入操作）
- `complement` - 查找基因组中间隔之间的间隙
- `subtract` - 移除与另一组重叠的区间部分

**示例：**
```python
import polars_bio as pb

# 查找重叠区间（返回 LazyFrame）
result = pb.overlap(df1, df2, suffixes=("_1", "_2"))

# 计数每个区间的重叠
counts = pb.count_overlaps(df1, df2)

# 合并重叠区间
merged = pb.merge(df1)

# 查找最近的区间
nearest = pb.nearest(df1, df2)

# 将任何 LazyFrame 结果收集为 DataFrame
result_df = result.collect()
```

**参考：** 详见 `references/interval_operations.md`，了解所有操作、参数、输出模式和性能考虑的详细文档。

### 2. 生物信息学文件 I/O

使用 `read_*`、`scan_*`、`write_*` 和 `sink_*` 函数读取和写入常见生物信息学格式。支持云存储（S3、GCS、Azure）和压缩（GZIP、BGZF）。

**支持的格式：**
- **BED** - 基因组区间（`read_bed`、`scan_bed`、通过通用接口 `write_*`）
- **VCF** - 遗传变异（`read_vcf`、`scan_vcf`、`write_vcf`、`sink_vcf`）
- **VCF Zarr** - 分析就绪的 Zarr 存储（`read_vcf_zarr`、`scan_vcf_zarr`；本地目录路径）
- **BAM** - 比对读数（`read_bam`、`scan_bam`、`write_bam`、`sink_bam`）
- **CRAM** - 压缩比对（`read_cram`、`scan_cram`、`write_cram`、`sink_cram`）
- **GFF** - 基因注释（`read_gff`、`scan_gff`）
- **GTF** - 基因注释（`read_gtf`、`scan_gtf`）
- **FASTA** - 参考序列（`read_fasta`、`scan_fasta`、`write_fasta`、`sink_fasta`）
- **FASTQ** - 测序读数（`read_fastq`、`scan_fastq`、`write_fastq`、`sink_fastq`）
- **SAM** - 文本比对（`read_sam`、`scan_sam`、`write_sam`、`sink_sam`）
- **Hi-C pairs** - 染色质接触（`read_pairs`、`scan_pairs`）

**示例：**
```python
import polars_bio as pb

# 读取 VCF 文件
variants = pb.read_vcf("samples.vcf.gz")

# 懒扫描 BAM 文件（流式）
alignments = pb.scan_bam("aligned.bam")

# 读取 GFF 注释
genes = pb.read_gff("annotations.gff3")

# 云存储（单独参数，非字典）
df = pb.read_bed("s3://bucket/regions.bed",
                 allow_anonymous=True)
```

**参考：** 详见 `references/file_io.md`，了解每种格式的列模式、参数、云存储选项和压缩支持。

### 3. SQL 数据处理

将生物信息学文件注册为表，并使用 DataFusion SQL 查询。将 SQL 的强大功能与 polars-bio 的基因组感知读取器相结合。

```python
import polars as pl
import polars_bio as pb

# 将文件注册为 SQL 表（路径优先，name= 关键字）
pb.register_vcf("samples.vcf.gz", name="variants")
pb.register_bed("target_regions.bed", name="regions")

# 使用 SQL 查询（返回 LazyFrame）
result = pb.sql("SELECT chrom, start, end, ref, alt FROM variants WHERE qual > 30")
result_df = result.collect()

# 将 Polars DataFrame 注册为 SQL 表
pb.from_polars("my_intervals", df)
result = pb.sql("SELECT * FROM my_intervals WHERE chrom = 'chr1'").collect()
```

**参考：** 详见 `references/sql_processing.md`，了解注册函数、SQL 语法和示例。

### 4. 堆积操作

使用 CIGAR 感知的深度计算，从 BAM/CRAM 文件计算每个碱基的读数深度。

```python
import polars_bio as pb

# 计算 BAM 文件的深度
depth_lf = pb.depth("aligned.bam")
depth_df = depth_lf.collect()

# 带质量过滤
depth_lf = pb.depth("aligned.bam", min_mapping_quality=20)
```

**参考：** 详见 `references/pileup_operations.md`，了解参数和集成模式。

## 关键概念

### 坐标系统

polars-bio 默认为**1-based** 坐标（基因组约定）。这可以全局更改：

```python
import polars_bio as pb

# 切换到 0-based 半开坐标（默认是 1-based / False）
pb.set_option("datafusion.bio.coordinate_system_zero_based", True)

# 切换回 1-based（默认）
pb.set_option("datafusion.bio.coordinate_system_zero_based", False)
```

I/O 函数也接受 `use_zero_based` 在结果 DataFrame 上设置坐标元数据：

```python
# 使用显式 0-based 元数据读取 BED
df = pb.read_bed("regions.bed", use_zero_based=True)
```

**重要：** BED 文件在文件格式中始终是 0-based 半开的。polars-bio 在读取 BED 文件时自动处理转换。I/O 函数将坐标元数据附加到 DataFrame，并通过操作传播。

### 两种 API 风格

**函数式 API** - 独立函数，显式输入：
```python
result = pb.overlap(df1, df2, suffixes=("_1", "_2"))
merged = pb.merge(df)
```

**链式方法 API** - 通过 **LazyFrame** 上的 `.pb` 访问器（不是 DataFrame）：
```python
result = df1.lazy().pb.overlap(df2)
merged = df.lazy().pb.merge()
```

**重要：** 区间操作的 `.pb` 访问器仅在 `LazyFrame` 上可用。在 `DataFrame` 上，`.pb` 仅提供写入操作（`write_bam`、`write_vcf` 等）。

链式方法支持流畅的管道：
```python
# 链式区间操作（注意：重叠输出带后缀的列，
# 所以在合并前重命名，合并期望 chrom/start/end）
result = (
    df1.lazy()
    .pb.overlap(df2)
    .filter(pl.col("start_2") > 1000)
    .select(
        pl.col("chrom_1").alias("chrom"),
        pl.col("start_1").alias("start"),
        pl.col("end_1").alias("end"),
    )
    .pb.merge()
    .collect()
)
```

### 探针-构建架构

对于双输入操作（overlap、nearest、count_overlaps、coverage），polars-bio 使用探针-构建连接策略：
- 第一个 DataFrame 是**探针**（迭代）
- 第二个 DataFrame 是**构建**（索引以进行查找）

为获得最佳性能，将较大的 DataFrame 作为第一个参数（探针），较小的作为第二个（构建）。

### 列约定

默认情况下，polars-bio 期望名为 `chrom`、`start`、`end` 的列。可通过列表指定自定义列名：

```python
result = pb.overlap(
    df1, df2,
    cols1=["chromosome", "begin", "finish"],
    cols2=["chr", "pos_start", "pos_end"],
)
```

### 返回类型和收集结果

所有区间操作和 `pb.sql()` 默认返回 **LazyFrame**。使用 `.collect()` 来物化结果，或传入 `output_type="polars.DataFrame"` 进行即时求值：

```python
# 懒（默认）- 需要时收集
result_lf = pb.overlap(df1, df2)
result_df = result_lf.collect()

# 即时 - 直接获取 DataFrame
result_df = pb.overlap(df1, df2, output_type="polars.DataFrame")
```

### 流式和核外处理

对于大于可用 RAM 的数据集，使用 `scan_*` 函数和流式执行：

```python
# 懒扫描文件
lf = pb.scan_bed("large_intervals.bed")

# 使用 Polars 流式处理（需要 polars ≥1.37，随 polars-bio 捆绑）
result = lf.collect(engine="streaming")
```

区间操作默认启用 DataFusion 流式处理，分批处理数据而无需将整个数据集加载到内存中。

## 常见陷阱

1. **DataFrame vs LazyFrame 上的 `.pb` 访问器：** 区间操作（overlap、merge 等）仅在 `LazyFrame.pb` 上可用。`DataFrame.pb` 只有写入方法。在链式区间操作前使用 `.lazy()` 转换。

2. **LazyFrame 返回：** 所有区间操作和 `pb.sql()` 默认返回 `LazyFrame`。不要忘记 `.collect()` 或使用 `output_type="polars.DataFrame"`。

3. **列名不匹配：** polars-bio 默认期望 `chrom`、`start`、`end`。如果您的列名不同，使用 `cols1`/`cols2` 参数（作为列表）。

4. **坐标系统元数据：** 区间操作从 I/O 函数或 DataFrame `config_meta` 读取坐标元数据。对于手动构建的 DataFrame，设置 `df.config_meta.set(coordinate_system_zero_based=True)`（0-based）或 `False`（1-based）。如果元数据缺失，polars-bio 回退到全局 `datafusion.bio.coordinate_system_zero_based` 设置（带警告）。设置 `pb.set_option("datafusion.bio.coordinate_system_check", True)` 以抛出 `MissingCoordinateSystemError` 而非警告。输入之间的不匹配系统会抛出 `CoordinateSystemMismatchError`。

5. **探针-构建顺序很重要：** 对于 overlap、nearest 和 coverage，第一个 DataFrame 被探针针对第二个。交换参数会改变哪些区间出现在左vs右输出列中，并可能影响性能。

6. **INT32 位置限制：** 基因组位置存储为 32 位整数，限制坐标约 21 亿。这对所有已知基因组都足够，但可能与自定义坐标空间有问题。

7. **BAM 索引要求：** `read_bam` 和 `scan_bam` 需要 BAM 旁边的 `.bai` 索引文件。如果缺失，用 `samtools index` 创建。

8. **默认禁用并行执行：** DataFusion 并行性默认为 1 个分区。为大型数据集启用：
   ```python
   pb.set_option("datafusion.execution.target_partitions", 8)
   ```

9. **CRAM 有单独的函数：** 对 CRAM 文件使用 `read_cram`/`scan_cram`/`register_cram`（不是 `read_bam`）。CRAM 函数需要 `reference_path` 参数。

## 最佳实践

1. **使用 lazy API**：对于大数据集，尽可能使用 lazy API 以获得更好的优化
   ```python
   df = pl.scan_csv("large_file.csv").filter(pl.col("score") > 0.5)
   result = df.collect()
   ```

2. **选择合适的文件格式**：对于基因组数据，优先使用 BED、BCF/VCF 等流式友好的格式

3. **利用表达式求值**：使用 Polars 表达式进行高效的数据转换
   ```python
   df.select([
       pl.col("start") + pl.col("end"),
       (pl.col("end") - pl.col("start")).alias("length")
   ])
   ```

4. **正确处理区间操作**：确保基因组坐标系统一致（0-based vs 1-based）

5. **内存管理**：对于超大型数据集，使用 streaming 模式
   ```python
   pl.scan_csv("huge.csv").sink("output.parquet")
   ```

## 资源

- [Polars-bio 文档](https://kaiko-ai.github.io/polars-bio/)
- [Polars 文档](https://docs.pola.rs/)
- [GitHub 仓库](https://github.com/kaiko-ai/polars-bio)

### 参考文件

- `references/genomic_intervals.md` - 基因组区间操作详细指南
- `references/bioinformatics_io.md` - 生物信息学文件格式处理
- `references/sql_queries.md` - SQL 查询示例
