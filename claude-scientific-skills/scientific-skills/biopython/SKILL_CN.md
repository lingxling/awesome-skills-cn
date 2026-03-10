---
name: biopython
description: 综合分子生物学工具包。用于序列操作、文件解析（FASTA/GenBank/PDB）、系统发育学和程序化 NCBI/PubMed 访问（Bio.Entrez）。最适合批量处理、自定义生物信息学流程、BLAST 自动化。对于快速查找使用 gget；对于多服务集成使用 bioservices。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# Biopython：Python 计算分子生物学

## 概述

Biopython 是一套全面可免费使用的 Python 工具，用于生物计算。它提供序列操作、文件 I/O、数据库访问、结构生物信息学、系统发育学以及许多其他生物信息学任务的功能。当前版本是 **Biopython 1.85**（2025 年 1 月发布），支持 Python 3 并需要 NumPy。

## 何时使用此技能

在以下情况使用此技能：

- 处理生物序列（DNA、RNA 或蛋白质）
- 读取、写入或转换生物文件格式（FASTA、GenBank、FASTQ、PDB、mmCIF 等）
- 通过 Entrez 访问 NCBI 数据库（GenBank、PubMed、Protein、Gene 等）
- 运行 BLAST 搜索或解析 BLAST 结果
- 执行序列比对（成对或多序列比对）
- 分析来自 PDB 文件的蛋白质结构
- 创建、操作或可视化系统发育树
- 查找序列基序或分析基序模式
- 计算序列统计信息（GC 含量、分子量、熔解温度等）
- 执行结构生物信息学任务
- 处理群体遗传学数据
- 任何其他计算分子生物学任务

## 核心能力

Biopython 组织成模块化子包，每个子包解决特定的生物信息学领域：

1. **序列处理** - Bio.Seq 和 Bio.SeqIO 用于序列操作和文件 I/O
2. **比对分析** - Bio.Align 和 Bio.AlignIO 用于成对和多序列比对
3. **数据库访问** - Bio.Entrez 用于程序化访问 NCBI 数据库
4. **BLAST 操作** - Bio.Blast 用于运行和解析 BLAST 搜索
5. **结构生物信息学** - Bio.PDB 用于处理 3D 蛋白质结构
6. **系统发育学** - Bio.Phylo 用于系统发育树操作和可视化
7. **高级功能** - 基序、群体遗传学、序列实用程序等

## 安装和设置

使用 pip 安装 Biopython（需要 Python 3 和 NumPy）：

```python
uv pip install biopython
```

对于 NCBI 数据库访问，始终设置您的电子邮件地址（NCBI 要求）：

```python
from Bio import Entrez
Entrez.email = "your.email@example.com"

# 可选：API 密钥以获得更高的速率限制（10 次/秒而不是 3 次/秒）
Entrez.api_key = "your_api_key_here"
```

## 使用此技能

此技能提供按功能领域组织的综合文档。在处理任务时，请查阅相关的参考文档：

### 1. 序列处理（Bio.Seq 和 Bio.SeqIO）

**参考：** `references/sequence_io.md`

用于：
- 创建和操作生物序列
- 读取和写入序列文件（FASTA、GenBank、FASTQ 等）
- 在文件格式之间转换
- 从大文件中提取序列
- 序列翻译、转录和反向互补
- 处理 SeqRecord 对象

**快速示例：**
```python
from Bio import SeqIO

# 从 FASTA 文件读取序列
for record in SeqIO.parse("sequences.fasta", "fasta"):
    print(f"{record.id}: {len(record.seq)} bp")

# 将 GenBank 转换为 FASTA
SeqIO.convert("input.gb", "genbank", "output.fasta", "fasta")
```

### 2. 比对分析（Bio.Align 和 Bio.AlignIO）

**参考：** `references/alignment.md`

用于：
- 成对序列比对（全局和局部）
- 读取和写入多序列比对
- 使用替换矩阵（BLOSUM、PAM）
- 计算比对统计信息
- 自定义比对参数

**快速示例：**
```python
from Bio import Align

# 成对比对
aligner = Align.PairwiseAligner()
aligner.mode = 'global'
alignments = aligner.align("ACCGGT", "ACGGT")
print(alignments[0])
```

### 3. 数据库访问（Bio.Entrez）

**参考：** `references/databases.md`

用于：
- 搜索 NCBI 数据库（PubMed、GenBank、Protein、Gene 等）
- 下载序列和记录
- 获取出版物信息
- 在数据库中查找相关记录
- 使用适当的速率限制进行批量下载

**快速示例：**
```python
from Bio import Entrez
Entrez.email = "your.email@example.com"

# 搜索 PubMed
handle = Entrez.esearch(db="pubmed", term="biopython", retmax=10)
results = Entrez.read(handle)
handle.close()
print(f"Found {results['Count']} results")
```

### 4. BLAST 操作（Bio.Blast）

**参考：** `references/blast.md`

用于：
- 通过 NCBI Web 服务运行 BLAST 搜索
- 运行本地 BLAST 搜索
- 解析 BLAST XML 输出
- 按 E 值或同一性过滤结果
- 提取命中序列

**快速示例：**
```python
from Bio.Blast import NCBIWWW, NCBIXML

# 运行 BLAST 搜索
result_handle = NCBIWWW.qblast("blastn", "nt", "ATCGATCGATCG")
blast_record = NCBIXML.read(result_handle)

# 显示前几个命中
for alignment in blast_record.alignments[:5]:
    print(f"{alignment.title}: E-value={alignment.hsps[0].expect}")
```

### 5. 结构生物信息学（Bio.PDB）

**参考：** `references/structure.md`

用于：
- 解析 PDB 和 mmCIF 结构文件
- 导航蛋白质结构层次（SMCRA：结构/模型/链/残基/原子）
- 计算距离、角度和二面角
- 二级结构分配（DSSP）
- 结构叠加和 RMSD 计算
- 从结构中提取序列

**快速示例：**
```python
from Bio.PDB import PDBParser

# 解析结构
parser = PDBParser(QUIET=True)
structure = parser.get_structure("1crn", "1crn.pdb")

# 计算α碳之间的距离
chain = structure[0]["A"]
distance = chain[10]["CA"] - chain[20]["CA"]
print(f"Distance: {distance:.2f} Å")
```

### 6. 系统发育学（Bio.Phylo）

**参考：** `references/phylogenetics.md`

用于：
- 读取和写入系统发育树（Newick、NEXUS、phyloXML）
- 从距离矩阵或比对构建树
- 树操作（修剪、重新生根、梯形化）
- 计算系统发育距离
- 创建共识树
- 可视化树

**快速示例：**
```python
from Bio import Phylo

# 读取和可视化树
tree = Phylo.read("tree.nwk", "newick")
Phylo.draw_ascii(tree)

# 计算距离
distance = tree.distance("Species_A", "Species_B")
print(f"Distance: {distance:.3f}")
```

### 7. 高级功能

**参考：** `references/advanced.md`

用于：
- **序列基序**（Bio.motifs）- 查找和分析基序模式
- **群体遗传学**（Bio.PopGen）- GenePop 文件、Fst 计算、Hardy-Weinberg 检验
- **序列实用程序**（Bio.SeqUtils）- GC 含量、熔解温度、分子量、蛋白质分析
- **限制分析**（Bio.Restriction）- 查找限制酶位点
- **聚类**（Bio.Cluster）- K 均值和层次聚类
- **基因组图**（GenomeDiagram）- 可视化基因组特征

**快速示例：**
```python
from Bio.SeqUtils import gc_fraction, molecular_weight
from Bio.Seq import Seq

seq = Seq("ATCGATCGATCG")
print(f"GC content: {gc_fraction(seq):.2%}")
print(f"Molecular weight: {molecular_weight(seq, seq_type='DNA'):.2f} g/mol")
```

## 一般工作流程指南

### 阅读文档

当用户询问特定的 Biopython 任务时：

1. **根据任务描述识别相关模块**
2. **使用 Read 工具读取适当的参考文件**
3. **提取相关的代码模式**并将其适应用户的特定需求
4. **组合多个模块**（当任务需要时）

参考文件的搜索模式示例：
```bash
# 查找特定函数的信息
grep -n "SeqIO.parse" references/sequence_io.md

# 查找特定任务的示例
grep -n "BLAST" references/blast.md

# 查找特定概念的信息
grep -n "alignment" references/alignment.md
```

### 编写 Biopython 代码

编写 Biopython 代码时遵循以下原则：

1. **显式导入模块**
   ```python
   from Bio import SeqIO, Entrez
   from Bio.Seq import Seq
   ```

2. **设置 Entrez 电子邮件**（当使用 NCBI 数据库时）
   ```python
   Entrez.email = "your.email@example.com"
   ```

3. **使用适当的文件格式** - 检查哪种格式最适合任务
   ```python
   # 常见格式："fasta"、"genbank"、"fastq"、"clustal"、"phylip"
   ```

4. **正确处理文件** - 使用后关闭句柄或使用上下文管理器
   ```python
   with open("file.fasta") as handle:
       records = SeqIO.parse(handle, "fasta")
   ```

5. **对大文件使用迭代器** - 避免将所有内容加载到内存中
   ```python
   for record in SeqIO.parse("large_file.fasta", "fasta"):
       # 一次处理一个记录
   ```

6. **优雅地处理错误** - 网络操作和文件解析可能会失败
   ```python
   try:
       handle = Entrez.efetch(db="nucleotide", id=accession)
   except HTTPError as e:
       print(f"Error: {e}")
   ```

## 常见模式

### 模式 1：从 GenBank 获取序列

```python
from Bio import Entrez, SeqIO

Entrez.email = "your.email@example.com"

# 获取序列
handle = Entrez.efetch(db="nucleotide", id="EU490707", rettype="gb", retmode="text")
record = SeqIO.read(handle, "genbank")
handle.close()

print(f"Description: {record.description}")
print(f"Sequence length: {len(record.seq)}")
```

### 模式 2：序列分析流程

```python
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction

for record in SeqIO.parse("sequences.fasta", "fasta"):
    # 计算统计信息
    gc = gc_fraction(record.seq)
    length = len(record.seq)

    # 查找 ORF、翻译等
    protein = record.seq.translate()

    print(f"{record.id}: {length} bp, GC={gc:.2%}")
```

### 模式 3：BLAST 并获取前几个命中

```python
from Bio.Blast import NCBIWWW, NCBIXML
from Bio import Entrez, SeqIO

Entrez.email = "your.email@example.com"

# 运行 BLAST
result_handle = NCBIWWW.qblast("blastn", "nt", sequence)
blast_record = NCBIXML.read(result_handle)

# 获取前几个命中的登录号
accessions = [aln.accession for aln in blast_record.alignments[:5]]

# 获取序列
for acc in accessions:
    handle = Entrez.efetch(db="nucleotide", id=acc, rettype="fasta", retmode="text")
    record = SeqIO.read(handle, "fasta")
    handle.close()
    print(f">{record.description}")
```

### 模式 4：从序列构建系统发育树

```python
from Bio import AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor

# 读取比对
alignment = AlignIO.read("alignment.fasta", "fasta")

# 计算距离
calculator = DistanceCalculator("identity")
dm = calculator.get_distance(alignment)

# 构建树
constructor = DistanceTreeConstructor()
tree = constructor.nj(dm)

# 可视化
Phylo.draw_ascii(tree)
```

## 最佳实践

1. **在编写代码之前始终阅读相关的参考文档**
2. **使用 grep 搜索参考文件**以查找特定函数或示例
3. **在解析之前验证文件格式**
4. **优雅地处理缺失数据** - 并非所有记录都有所有字段
5. **缓存下载的数据** - 不要重复下载相同的序列
6. **尊重 NCBI 速率限制** - 使用 API 密钥和适当的延迟
7. **在处理大文件之前用小数据集测试**
8. **保持 Biopython 更新**以获得最新功能和错误修复
9. **使用适当的遗传密码表**进行翻译
10. **记录分析参数**以实现可重现性

## 常见问题故障排除

### 问题："No handlers could be found for logger 'Bio.Entrez'"
**解决方案：** 这只是一个警告。设置 Entrez.email 以抑制它。

### 问题：来自 NCBI 的"HTTP Error 400"
**解决方案：** 检查 ID/登录号是否有效且格式正确。

### 问题：解析文件时出现"ValueError: EOF"
**解决方案：** 验证文件格式与指定的格式字符串匹配。

### 问题：比对失败并显示"sequences are not same length"
**解决方案：** 在使用 AlignIO 或 MultipleSeqAlignment 之前确保序列已比对。

### 问题：BLAST 搜索很慢
**解决方案：** 对大规模搜索使用本地 BLAST，或缓存结果。

### 问题：PDB 解析器警告
**解决方案：** 使用 `PDBParser(QUIET=True)` 抑制警告，或调查结构质量。

## 其他资源

- **官方文档**：https://biopython.org/docs/latest/
- **教程**：https://biopython.org/docs/latest/Tutorial/
- **Cookbook**：https://biopython.org/docs/latest/Tutorial/（高级示例）
- **GitHub**：https://github.com/biopython/biopython
- **邮件列表**：biopython@biopython.org

## 快速参考

要在参考文件中定位信息，请使用以下搜索模式：

```bash
# 搜索特定函数
grep -n "function_name" references/*.md

# 查找特定任务的示例
grep -n "example" references/sequence_io.md

# 查找模块的所有出现
grep -n "Bio.Seq" references/*.md
```

## 总结

Biopython 为计算分子生物学提供全面的工具。使用此技能时：

1. **识别任务领域**（序列、比对、数据库、BLAST、结构、系统发育学或高级）
2. **查阅 `references/` 目录中的适当参考文件**
3. **调整代码示例**以适应特定用例
4. **组合多个模块**（当复杂工作流程需要时）
5. **遵循最佳实践**进行文件处理、错误检查和数据管理

模块化参考文档确保每个主要 Biopython 功能都有详细的、可搜索的信息。
