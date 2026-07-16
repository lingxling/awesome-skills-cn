---
name: biopython
description: 综合分子生物学工具包。用于序列操作、文件解析（FASTA/GenBank/PDB）、系统发育学和程序化NCBI/PubMed访问（Bio.Entrez）。最适合批量处理、自定义生物信息学管道、BLAST自动化。快速查找请使用gget；多服务集成请使用bioservices。
allowed-tools: Read Write Edit Bash
compatibility: Requires Python 3.10+, NumPy, and Biopython. Entrez and web BLAST examples require network access; local BLAST/MUSCLE examples require those command-line tools installed separately.
license: Biopython License Agreement
required_environment_variables: [{"name": "NCBI_EMAIL", "prompt": "Email for NCBI Entrez identification (required by NCBI policy for Entrez calls).", "required_for": "optional features"}, {"name": "NCBI_API_KEY", "prompt": "NCBI API key to raise Entrez rate limits.", "required_for": "optional features"}]
metadata: {"version": "1.2", "skill-author": "K-Dense Inc.", "openclaw": {"envVars": [{"name": "NCBI_EMAIL", "required": false, "description": "Email for NCBI Entrez identification (required by NCBI policy for Entrez calls)."}, {"name": "NCBI_API_KEY", "required": false, "description": "NCBI API key to raise Entrez rate limits."}]}}
---






# Biopython：Python 中的计算分子生物学

## 概述

Biopython 是一套免费的 Python 生物计算工具。它为序列操作、文件 I/O、数据库访问、结构生物信息学、系统发育学以及许多其他生物信息学任务提供功能。当前版本是 **Biopython 1.87**（2026 年 3 月 30 日发布）。它支持 **Python 3.10-3.14** 和 PyPy3.10，需要 NumPy。Biopython 1.87 还修复了 `Bio.Entrez.Parser` 在解析不可信文件时的 **CVE-2025-68463** 漏洞，因此解析外部提供的 Entrez XML 时推荐使用 1.87 及以上版本。

## 何时使用此技能

在以下情况下使用此技能：

- 处理生物序列（DNA、RNA 或蛋白质）
- 读取、写入或转换生物文件格式（FASTA、GenBank、FASTQ、PDB、mmCIF 等）
- 通过 Entrez 访问 NCBI 数据库（GenBank、PubMed、Protein、Gene 等）
- 运行 BLAST 搜索或解析 BLAST 结果
- 执行序列比对（成对比对或多序列比对）
- 分析 PDB 文件中的蛋白质结构
- 创建、操作或可视化系统发育树
- 查找序列模体或分析模体模式
- 计算序列统计数据（GC 含量、分子量、熔解温度等）
- 执行结构生物信息学任务
- 处理群体遗传学数据
- 任何其他计算分子生物学任务

## 核心能力

Biopython 组织成模块化的子包，每个子包针对特定的生物信息学领域：

1. **序列处理** - Bio.Seq 和 Bio.SeqIO 用于序列操作和文件 I/O
2. **比对分析** - Bio.Align 和 Bio.AlignIO 用于成对和多序列比对
3. **数据库访问** - Bio.Entrez 用于编程访问 NCBI 数据库
4. **BLAST 操作** - Bio.Blast 用于运行和解析 BLAST 搜索
5. **结构生物信息学** - Bio.PDB 用于处理 3D 蛋白质结构
6. **系统发育学** - Bio.Phylo 用于系统发育树的操作和可视化
7. **高级功能** - 模体、群体遗传学、序列工具等

## 安装和设置

安装当前稳定版 Biopython，并显式锁定版本号以保证可复现性：

```bash
uv pip install "biopython==1.87"
```

对于 NCBI 数据库访问，始终设置您的电子邮件地址（NCBI 要求）。对于可复用的软件，还应设置一个稳定的 `Entrez.tool` 值，并向 NCBI 注册该工具/邮箱。要获得更高的速率限制（10 req/s 而不是 3 req/s），只从环境变量读取 `NCBI_API_KEY`——不要硬编码密钥，也不要加载无关的环境变量：

```python
import os
from Bio import Entrez

Entrez.email = "your.email@example.com"  # 必需的 — 使用您的真实邮箱
Entrez.tool = "your_tool_name"  # 可选但推荐用于可复用软件

# 可选：在 https://www.ncbi.nlm.nih.gov/account/settings/ 注册
if api_key := os.environ.get("NCBI_API_KEY"):
    Entrez.api_key = api_key
```

## 使用此技能

此技能提供了按功能区域组织的全面文档。处理任务时，请参阅相关的参考文档：

### 1. 序列处理（Bio.Seq 和 Bio.SeqIO）

**参考：** `references/sequence_io.md`

用于：
- 创建和操作生物序列
- 读取和写入序列文件（FASTA、GenBank、FASTQ 等）
- 文件格式之间的转换
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
- 计算比对统计
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
- 跨数据库查找相关记录
- 批量下载并进行适当的速率限制

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
- 通过 NCBI 网络服务运行 BLAST 搜索
- 运行本地 BLAST 搜索
- 解析 BLAST XML 输出
- 按 E 值或一致性过滤结果
- 提取命中序列

**快速示例：**
```python
from Bio.Blast import NCBIWWW, NCBIXML

# 运行 BLAST 搜索
result_handle = NCBIWWW.qblast("blastn", "nt", "ATCGATCGATCG")
blast_record = NCBIXML.read(result_handle)

# 显示最佳命中
for alignment in blast_record.alignments[:5]:
    print(f"{alignment.title}: E-value={alignment.hsps[0].expect}")
```

### 5. 结构生物信息学（Bio.PDB）

**参考：** `references/structure.md`

用于：
- 解析 PDB 和 mmCIF 结构文件
- 导航蛋白质结构层次（SMCRA：结构/模型/链/残基/原子）
- 计算距离、角度和二面角
- 二级结构指认（DSSP）
- 结构叠加和 RMSD 计算
- 从结构中提取序列

**快速示例：**
```python
from Bio.PDB import PDBParser

# 解析结构
parser = PDBParser(QUIET=True)
structure = parser.get_structure("1crn", "1crn.pdb")

# 计算 alpha 碳之间的距离
chain = structure[0]["A"]
distance = chain[10]["CA"] - chain[20]["CA"]
print(f"Distance: {distance:.2f} Å")
```

### 6. 系统发育学（Bio.Phylo）

**参考：** `references/phylogenetics.md`

用于：
- 读取和写入系统发育树（Newick、NEXUS、phyloXML）
- 从距离矩阵或比对构建树
- 树操作（剪裁、重根化、梯形化）
- 计算系统发育距离
- 创建共识树
- 可视化树

**快速示例：**
```python
from Bio import Phylo

# 读取并可视化树
tree = Phylo.read("tree.nwk", "newick")
Phylo.draw_ascii(tree)

# 计算距离
distance = tree.distance("Species_A", "Species_B")
print(f"Distance: {distance:.3f}")
```

### 7. 高级功能

**参考：** `references/advanced.md`

用于：
- **序列模体**（Bio.motifs）- 查找和分析模体模式
- **群体遗传学**（Bio.PopGen）- GenePop 文件、Fst 计算、哈迪-温伯格检验
- **序列工具**（Bio.SeqUtils）- GC 含量、熔解温度、分子量、蛋白质分析
- **限制性分析**（Bio.Restriction）- 查找限制酶位点
- **聚类**（Bio.Cluster）- K-means 和层次聚类
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

1. **根据任务描述确定相关模块**
2. **使用 Read 工具读取适当的参考文件**
3. **提取相关的代码模式**并根据用户的具体需求进行调整
4. **在任务需要时组合多个模块**

参考文件的搜索模式示例：
```bash
# 查找特定函数的信息
rg -n "SeqIO.parse" references/sequence_io.md

# 查找特定任务的示例
rg -n "BLAST" references/blast.md

# 查找特定概念的信息
rg -n "alignment" references/alignment.md
```

### 编写 Biopython 代码

编写 Biopython 代码时遵循以下原则：

1. **显式导入模块**
   ```python
   from Bio import SeqIO, Entrez
   from Bio.Seq import Seq
   ```

2. **使用 NCBI 数据库时设置 Entrez 邮箱；如果存在，只从环境变量加载 `NCBI_API_KEY`**
   ```python
   import os
   from Bio import Entrez

   Entrez.email = "your.email@example.com"
   Entrez.tool = "your_tool_name"
   if api_key := os.environ.get("NCBI_API_KEY"):
       Entrez.api_key = api_key
   ```

3. **使用适当的文件格式** - 检查哪种格式最适合任务
   ```python
   # 常用格式："fasta"、"genbank"、"fastq"、"clustal"、"phylip"
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
   from urllib.error import HTTPError

   try:
       handle = Entrez.efetch(db="nucleotide", id=accession)
   except HTTPError as e:
       print(f"Error: {e}")
   ```

## 常见模式

### 模式 1：从 GenBank 获取序列
```python
from Bio import SeqIO

# 通过 accession 获取序列
record = SeqIO.read("AB123456.gb", "genbank")
print(f"序列: {record.seq}")
print(f"描述: {record.description}")
```

### 模式 2：序列分析管道
```python
from Bio import SeqIO, Seq, Align
from Bio.SeqUtils import MeltingTemp as mt

# 读取序列
records = list(SeqIO.parse("sequences.fasta", "fasta"))

# 分析每个序列
for record in records:
    seq = record.seq
    gc_content = Seq.GC(seq)
    tm = mt.Tm_NN(seq)
    print(f"{record.id}: GC={gc_content:.1f}%, Tm={tm:.1f}°C")
```

### 模式 3：BLAST 并获取最佳匹配
```python
from Bio.Blast import NCBIWWW
from Bio import SeqIO

# 读取查询序列
record = SeqIO.read("query.fasta", format="fasta")

# 执行 BLAST 搜索
result_handle = NCBIWWW.qblast("blastn", "nt", record.seq)

# 保存结果
with open("blast_result.xml", "w") as out_handle:
    out_handle.write(result_handle.read())
```

### 模式 4：从序列构建系统发育树
```python
from Bio import Phylo, SeqIO
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor

# 读取序列
records = list(SeqIO.parse("sequences.fasta", "fasta"))

# 计算距离
calculator = DistanceCalculator('identity')
dm = calculator.get_distance(records)

# 构建树
constructor = DistanceTreeConstructor()
tree = constructor.upgma(dm)

# 绘制树
Phylo.draw(tree)
```

## 最佳实践

1. **在编写代码前先阅读相关参考文档**
2. **使用 grep 在参考文件中搜索特定函数或示例**
3. **解析前验证文件格式**
4. **优雅地处理缺失数据** - 并非所有记录都包含所有字段
5. **缓存已下载的数据** - 避免重复下载相同序列
6. **遵守 NCBI 速率限制** - 对于可复用软件，使用 API 密钥、注册过的工具/邮箱值，并对大批量任务使用 Entrez history/批处理
7. **在处理大文件前先用小数据集测试**
8. **保持 Biopython 更新** 以获得最新功能和修复
9. **翻译时使用合适的遗传密码表**
10. **记录分析参数** 以确保可复现性

## 常见问题排查

### 问题：出现 "No handlers could be found for logger 'Bio.Entrez'"
- **原因**：这是 Biopython 的警告消息，不是错误
- **解决**：添加 `logging.basicConfig()` 来配置日志：
  ```python
  import logging
  logging.basicConfig()
  ```

### 问题：NCBI 返回 "HTTP Error 400"
- **原因**：请求格式不正确或 ID 无效
- **解决**：
  - 检查数据库名称是否正确（"nucleotide"、"protein"等）
  - 验证 accession ID 是否存在
  - 尝试使用不同的检索方式

### 问题：解析文件时出现 "ValueError: EOF"
- **原因**：文件格式不正确或文件损坏
- **解决**：
  - 检查文件完整性
  - 验证文件格式是否正确
  - 尝试使用不同的解析器

### 问题：比对失败，显示 "sequences are not the same length"
- **原因**：尝试比对不同长度的序列
- **解决**：
  - 使用全局比对处理不同长度的序列
  - 或先进行序列对齐

### 问题：BLAST 搜索速度慢
- **解决**：
  - 使用 API 密钥来提高速率限制
  - 减少搜索结果数量
  - 使用本地 BLAST 而非网络 BLAST

### 问题：PDB 解析器警告
- **原因**：PDB 文件格式问题
- **解决**：使用 `QUIET=True` 抑制警告：
  ```python
  parser = PDBParser(QUIET=True)
  ```

### 问题：导入 Bio.HMM、Bio.MarkovModel 或 Bio.Application 时出现 ImportError
- **原因**：这些模块已被弃用或移除
- **解决**：使用替代模块或更新代码

### 问题：升级到 1.86+ 后 PairwiseAligner 返回的比对数量减少
- **原因**：Biopython 1.86 修复了比对算法中的 bug
- **解决**：验证结果是否符合预期，必要时调整参数

## 附加资源

- **官方文档**：https://biopython.org/docs/latest/
- **教程**：https://biopython.org/docs/latest/Tutorial/
- **Cookbook**：https://biopython.org/docs/latest/Tutorial/（高级示例）
- **GitHub**：https://github.com/biopython/biopython
- **发布说明**：https://github.com/biopython/biopython/blob/master/NEWS.rst
- **已弃用 API**：https://github.com/biopython/biopython/blob/master/DEPRECATED.rst
- **邮件列表**：biopython@biopython.org

## 快速参考

要在参考文件中定位信息，请使用以下搜索模式：

```bash
# 搜索特定函数
rg -n "function_name" references/*.md

# 查找特定任务的示例
rg -n "example" references/sequence_io.md

# 查找模块的所有出现位置
rg -n "Bio.Seq" references/*.md
```
