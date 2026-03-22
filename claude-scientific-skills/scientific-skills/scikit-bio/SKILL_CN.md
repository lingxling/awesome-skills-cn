---
name: scikit-bio
description: 生物数据工具包。序列分析、比对、系统发育树、多样性指标（alpha/beta、UniFrac）、排序（PCoA）、PERMANOVA、FASTA/Newick I/O，用于微生物组分析。
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# scikit-bio

## 概述

scikit-bio是一个用于处理生物数据的综合Python库。将此技能应用于生物信息学分析，包括序列操作、比对、系统发育学、微生物生态学和多元统计。

## 何时使用此技能

当用户以下情况时应使用此技能：
- 处理生物序列（DNA、RNA、蛋白质）
- 需要读写生物文件格式（FASTA、FASTQ、GenBank、Newick、BIOM等）
- 执行序列比对或搜索基序
- 构建或分析系统发育树
- 计算多样性指标（alpha/beta多样性、UniFrac距离）
- 执行排序分析（PCoA、CCA、RDA）
- 对生物/生态数据运行统计测试（PERMANOVA、ANOSIM、Mantel）
- 分析微生物组或群落生态数据
- 处理来自语言模型的蛋白质嵌入
- 需要操作生物数据表

## 核心能力

### 1. 序列操作

使用专门的DNA、RNA和蛋白质数据类处理生物序列。

**关键操作：**
- 从FASTA、FASTQ、GenBank、EMBL格式读写序列
- 序列切片、连接和搜索
- 反向互补、转录（DNA→RNA）和翻译（RNA→蛋白质）
- 使用正则表达式查找基序和模式
- 计算距离（汉明、基于k-mer）
- 处理序列质量分数和元数据

**常见模式：**
```python
import skbio

# 从文件读取序列
seq = skbio.DNA.read('input.fasta')

# 序列操作
rc = seq.reverse_complement()
rna = seq.transcribe()
protein = rna.translate()

# 查找基序
motif_positions = seq.find_with_regex('ATG[ACGT]{3}')

# 检查属性
has_degens = seq.has_degenerates()
seq_no_gaps = seq.degap()
```

**重要说明：**
- 使用`DNA`、`RNA`、`Protein`类进行带验证的语法序列
- 使用`Sequence`类处理无字母表限制的通用序列
- 从FASTQ文件自动加载质量分数到位置元数据
- 元数据类型：序列级（ID、描述）、位置级（每碱基）、区间（区域/特征）

### 2. 序列比对

使用动态规划算法执行成对和多序列比对。

**关键能力：**
- 全局比对（Needleman-Wunsch及其半全局变体）
- 局部比对（Smith-Waterman）
- 可配置的评分方案（匹配/错配、间隙罚分、替换矩阵）
- CIGAR字符串转换
- 使用`TabularMSA`存储和操作多序列比对

**常见模式：**
```python
from skbio.alignment import local_pairwise_align_ssw, TabularMSA

# 成对比对
alignment = local_pairwise_align_ssw(seq1, seq2)

# 访问比对后的序列
msa = alignment.aligned_sequences

# 从文件读取多序列比对
msa = TabularMSA.read('alignment.fasta', constructor=skbio.DNA)

# 计算一致性序列
consensus = msa.consensus()
```

**重要说明：**
- 使用`local_pairwise_align_ssw`进行局部比对（更快，基于SSW）
- 使用`StripedSmithWaterman`进行蛋白质比对
- 生物序列推荐使用仿射间隙罚分
- 可在scikit-bio、BioPython和Biotite比对格式之间转换

### 3. 系统发育树

构建、操作和分析表示进化关系的系统发育树。

**关键能力：**
- 从距离矩阵构建树（UPGMA、WPGMA、邻接法、GME、BME）
- 树操作（剪枝、重新定根、遍历）
- 距离计算（路径、共表型、Robinson-Foulds）
- ASCII可视化
- Newick格式I/O

**常见模式：**
```python
from skbio import TreeNode
from skbio.tree import nj

# 从文件读取树
tree = TreeNode.read('tree.nwk')

# 从距离矩阵构建树
tree = nj(distance_matrix)

# 树操作
subtree = tree.shear(['taxon1', 'taxon2', 'taxon3'])
tips = [node for node in tree.tips()]
lca = tree.lowest_common_ancestor(['taxon1', 'taxon2'])

# 计算距离
patristic_dist = tree.find('taxon1').distance(tree.find('taxon2'))
cophenetic_matrix = tree.cophenetic_matrix()

# 比较树
rf_distance = tree.robinson_foulds(other_tree)
```

**重要说明：**
- 使用`nj()`进行邻接法（经典系统发育方法）
- 使用`upgma()`进行UPGMA（假设分子钟）
- GME和BME对大型树具有高度可扩展性
- 树可以是有根或无根的；某些指标需要特定的根

### 4. 多样性分析

计算微生物生态学和群落分析的alpha和beta多样性指标。

**关键能力：**
- Alpha多样性：丰富度、香农熵、辛普森指数、Faith's PD、Pielou's均匀度
- Beta多样性：Bray-Curtis、Jaccard、加权/未加权UniFrac、欧几里得距离
- 系统发育多样性指标（需要树输入）
- 稀疏化和亚采样
- 与排序和统计测试集成

**常见模式：**
```python
from skbio.diversity import alpha_diversity, beta_diversity
import skbio

# Alpha多样性
alpha = alpha_diversity('shannon', counts_matrix, ids=sample_ids)
faith_pd = alpha_diversity('faith_pd', counts_matrix, ids=sample_ids,
                          tree=tree, otu_ids=feature_ids)

# Beta多样性
bc_dm = beta_diversity('braycurtis', counts_matrix, ids=sample_ids)
unifrac_dm = beta_diversity('unweighted_unifrac', counts_matrix,
                           ids=sample_ids, tree=tree, otu_ids=feature_ids)

# 获取可用指标
from skbio.diversity import get_alpha_diversity_metrics
print(get_alpha_diversity_metrics())
```

**重要说明：**
- 计数必须是表示丰度的整数，而不是相对频率
- 系统发育指标（Faith's PD、UniFrac）需要树和OTU ID映射
- 使用`partial_beta_diversity()`仅计算特定样本对
- Alpha多样性返回Series，beta多样性返回DistanceMatrix

### 5. 排序方法

将高维生物数据减少到可可视化的低维空间。

**关键能力：**
- PCoA（主坐标分析）从距离矩阵
- CA（对应分析）用于列联表
- CCA（典范对应分析）带有环境约束
- RDA（冗余分析）用于线性关系
- 用于特征解释的双标图投影

**常见模式：**
```python
from skbio.stats.ordination import pcoa, cca

# 从距离矩阵进行PCoA
pcoa_results = pcoa(distance_matrix)
pc1 = pcoa_results.samples['PC1']
pc2 = pcoa_results.samples['PC2']

# 带环境变量的CCA
cca_results = cca(species_matrix, environmental_matrix)

# 保存/加载排序结果
pcoa_results.write('ordination.txt')
results = skbio.OrdinationResults.read('ordination.txt')
```

**重要说明：**
- PCoA适用于任何距离/相异矩阵
- CCA揭示群落组成的环境驱动因素
- 排序结果包括特征值、解释比例和样本/特征坐标
- 结果与绘图库（matplotlib、seaborn、plotly）集成

### 6. 统计测试

对生态和生物数据执行特定的假设测试。

**关键能力：**
- PERMANOVA：使用距离矩阵测试组差异
- ANOSIM：组差异的替代测试
- PERMDISP：测试组分散的同质性
- Mantel测试：距离矩阵之间的相关性
- Bioenv：找到与距离相关的环境变量

**常见模式：**
```python
from skbio.stats.distance import permanova, anosim, mantel

# 测试组是否显著不同
permanova_results = permanova(distance_matrix, grouping, permutations=999)
print(f"p值: {permanova_results['p-value']}")

# ANOSIM测试
anosim_results = anosim(distance_matrix, grouping, permutations=999)

# 两个距离矩阵之间的Mantel测试
mantel_results = mantel(dm1, dm2, method='pearson', permutations=999)
print(f"相关性: {mantel_results[0]}, p值: {mantel_results[1]}")
```

**重要说明：**
- 排列测试提供非参数显著性测试
- 使用999+排列获得稳健的p值
- PERMANOVA对分散差异敏感；与PERMDISP配对使用
- Mantel测试评估矩阵相关性（例如，地理与遗传距离）

### 7. 文件I/O和格式转换

读取和写入19+种生物文件格式，自动检测格式。

**支持的格式：**
- 序列：FASTA、FASTQ、GenBank、EMBL、QSeq
- 比对：Clustal、PHYLIP、Stockholm
- 树：Newick
- 表：BIOM（HDF5和JSON）
- 距离：分隔的方阵
- 分析：BLAST+6/7、GFF3、排序结果
- 元数据：带验证的TSV/CSV

**常见模式：**
```python
import skbio

# 自动格式检测读取
seq = skbio.DNA.read('file.fasta', format='fasta')
tree = skbio.TreeNode.read('tree.nwk')

# 写入文件
seq.write('output.fasta', format='fasta')

# 大文件生成器（内存高效）
for seq in skbio.io.read('large.fasta', format='fasta', constructor=skbio.DNA):
    process(seq)

# 转换格式
seqs = list(skbio.io.read('input.fastq', format='fastq', constructor=skbio.DNA))
skbio.io.write(seqs, format='fasta', into='output.fasta')
```

**重要说明：**
- 使用生成器处理大文件以避免内存问题
- 当指定`into`参数时，格式可以自动检测
- 某些对象可以写入多种格式
- 支持使用`verify=False`的stdin/stdout管道

### 8. 距离矩阵

创建和操作带有统计方法的距离/相异矩阵。

**关键能力：**
- 存储对称（DistanceMatrix）或非对称（DissimilarityMatrix）数据
- 基于ID的索引和切片
- 与多样性、排序和统计测试集成
- 读写分隔文本格式

**常见模式：**
```python
from skbio import DistanceMatrix
import numpy as np

# 从数组创建
data = np.array([[0, 1, 2], [1, 0, 3], [2, 3, 0]])
dm = DistanceMatrix(data, ids=['A', 'B', 'C'])

# 访问距离
dist_ab = dm['A', 'B']
row_a = dm['A']

# 从文件读取
dm = DistanceMatrix.read('distances.txt')

# 用于下游分析
pcoa_results = pcoa(dm)
permanova_results = permanova(dm, grouping)
```

**重要说明：**
- DistanceMatrix强制对称性和零对角线
- DissimilarityMatrix允许非对称值
- ID启用与元数据和生物学知识的集成
- 与pandas、numpy和scikit-learn兼容

### 9. 生物表

处理微生物组研究中常见的特征表（OTU/ASV表）。

**关键能力：**
- BIOM格式I/O（HDF5和JSON）
- 与pandas、polars、AnnData、numpy集成
- 数据增强技术（phylomix、mixup、组成方法）
- 样本/特征过滤和标准化
- 元数据集成

**常见模式：**
```python
from skbio import Table

# 读取BIOM表
table = Table.read('table.biom')

# 访问数据
sample_ids = table.ids(axis='sample')
feature_ids = table.ids(axis='observation')
counts = table.matrix_data

# 过滤
filtered = table.filter(sample_ids_to_keep, axis='sample')

# 转换为/从pandas
df = table.to_dataframe()
table = Table.from_dataframe(df)
```

**重要说明：**
- BIOM表是QIIME 2工作流程中的标准
- 行通常表示样本，列表示特征（OTU/ASV）
- 支持稀疏和密集表示
- 输出格式可配置（pandas/polars/numpy）

### 10. 蛋白质嵌入

处理用于下游分析的蛋白质语言模型嵌入。

**关键能力：**
- 存储来自蛋白质语言模型的嵌入（ESM、ProtTrans等）
- 将嵌入转换为距离矩阵
- 生成用于可视化的排序对象
- 导出到numpy/pandas用于ML工作流

**常见模式：**
```python
from skbio.embedding import ProteinEmbedding, ProteinVector

# 从数组创建嵌入
embedding = ProteinEmbedding(embedding_array, sequence_ids)

# 转换为距离矩阵进行分析
dm = embedding.to_distances(metric='euclidean')

# 嵌入空间的PCoA可视化
pcoa_results = embedding.to_ordination(metric='euclidean', method='pcoa')

# 导出用于机器学习
array = embedding.to_array()
df = embedding.to_dataframe()
```

**重要说明：**
- 嵌入连接蛋白质语言模型与传统生物信息学
- 与scikit-bio的距离/排序/统计生态系统兼容
- SequenceEmbedding和ProteinEmbedding提供专门功能
- 适用于序列聚类、分类和可视化

## 最佳实践

### 安装
```bash
uv pip install scikit-bio
```

### 性能考虑
- 对大序列文件使用生成器以最小化内存使用
- 对于大规模系统发育树，优先使用GME或BME而不是NJ
- Beta多样性计算可以通过`partial_beta_diversity()`并行化
- BIOM格式（HDF5）比JSON更高效处理大表

### 与生态系统集成
- 序列通过标准格式与Biopython互操作
- 表与pandas、polars和AnnData集成
- 距离矩阵与scikit-learn兼容
- 排序结果可通过matplotlib/seaborn/plotly可视化
- 与QIIME 2工件（BIOM、树、距离矩阵）无缝协作

### 常见工作流程
1. **微生物组多样性分析**：读取BIOM表 → 计算alpha/beta多样性 → 排序（PCoA） → 统计测试（PERMANOVA）
2. **系统发育分析**：读取序列 → 比对 → 构建距离矩阵 → 构建树 → 计算系统发育距离
3. **序列处理**：读取FASTQ → 质量过滤 → 修剪/清洁 → 查找基序 → 翻译 → 写入FASTA
4. **比较基因组学**：读取序列 → 成对比对 → 计算距离 → 构建树 → 分析分支

## 参考文档

有关详细的API信息、参数说明和高级使用示例，请参考`references/api_reference.md`，其中包含全面的文档：
- 所有功能的完整方法签名和参数
- 复杂工作流的扩展代码示例
- 常见问题的故障排除
- 性能优化提示
- 与其他库的集成模式

## 其他资源

- 官方文档：https://scikit.bio/docs/latest/
- GitHub仓库：https://github.com/scikit-bio/scikit-bio
- 论坛支持：https://forum.qiime2.org（scikit-bio是QIIME 2生态系统的一部分）