---
name: geniml
description: 当处理基因组区间数据（BED 文件）用于机器学习任务时使用此技能。适用于训练区域嵌入（Region2Vec、BEDspace）、单细胞 ATAC-seq 分析（scEmbed）、构建一致性峰（universes），或任何基于机器学习的基因组区域分析。适用于 BED 文件集合、scATAC-seq 数据、染色质可及性数据集以及基于区域的基因组特征学习。
license: BSD-2-Clause 许可证
metadata:
    skill-author: K-Dense Inc.
---

# Geniml: 基因组区间机器学习

## 概述

Geniml 是一个用于在 BED 文件的基因组区间数据上构建机器学习模型的 Python 包。它提供了无监督方法来学习基因组区域、单细胞和元数据标签的嵌入，支持相似性搜索、聚类和下游机器学习任务。

## 安装

使用 uv 安装 geniml：

```bash
uv pip install geniml
```

安装机器学习依赖（PyTorch 等）：

```bash
uv pip install 'geniml[ml]'
```

从 GitHub 安装开发版本：

```bash
uv pip install git+https://github.com/databio/geniml.git
```

## 核心功能

Geniml 提供五大核心功能，每个功能在专门的参考文件中有详细说明：

### 1. Region2Vec：基因组区域嵌入

使用 word2vec 风格的学习方法训练基因组区域的无监督嵌入。

**适用场景：** BED 文件的降维、区域相似性分析、下游机器学习的特征向量。

**工作流程：**
1. 使用 universe 参考对 BED 文件进行分词
2. 在分词结果上训练 Region2Vec 模型
3. 生成区域的嵌入

**参考：** 详细工作流程、参数和示例请参见 `references/region2vec.md`。

### 2. BEDspace：联合区域与元数据嵌入

使用 StarSpace 训练区域集合和元数据标签的共享嵌入。

**适用场景：** 元数据感知搜索、跨模态查询（区域→标签或标签→区域）、基因组内容与实验条件的联合分析。

**工作流程：**
1. 预处理区域和元数据
2. 训练 BEDspace 模型
3. 计算距离
4. 跨区域和标签进行查询

**参考：** 详细工作流程、搜索类型和示例请参见 `references/bedspace.md`。

### 3. scEmbed：单细胞染色质可及性嵌入

在单细胞 ATAC-seq 数据上训练 Region2Vec 模型以生成细胞级别的嵌入。

**适用场景：** scATAC-seq 聚类、细胞类型注释、单细胞降维、与 scanpy 工作流集成。

**工作流程：**
1. 准备包含峰坐标信息的 AnnData
2. 对细胞进行预分词
3. 训练 scEmbed 模型
4. 生成细胞嵌入
5. 使用 scanpy 进行聚类和可视化

**参考：** 详细工作流程、参数和示例请参见 `references/scembed.md`。

### 4. 一致性峰：Universe 构建

使用多种统计方法从 BED 文件集合中构建参考峰集合（universes）。

**适用场景：** 创建分词参考、跨数据集标准化区域、以统计严谨性定义一致性特征。

**工作流程：**
1. 合并 BED 文件
2. 生成覆盖度轨迹
3. 使用 CC、CCF、ML 或 HMM 方法构建 universe

**方法：**
- **CC（Coverage Cutoff）**：基于简单阈值
- **CCF（Coverage Cutoff Flexible）**：边界置信区间
- **ML（Maximum Likelihood）**：位置的概率建模
- **HMM（Hidden Markov Model）**：复杂状态建模

**参考：** 方法比较、参数和示例请参见 `references/consensus_peaks.md`。

### 5. 工具：辅助工具

用于缓存、随机化、评估和搜索的附加工具。

**可用工具：**
- **BBClient**：BED 文件缓存，支持重复访问
- **BEDshift**：保留基因组上下文的随机化
- **Evaluation**：嵌入质量评估指标（轮廓系数、Davies-Bouldin 等）
- **Tokenization**：区域分词工具（硬分词、软分词、基于 universe）
- **Text2BedNN**：基因组查询的神经搜索后端

**参考：** 各工具的详细用法请参见 `references/utilities.md`。

## 常见工作流

### 基础区域嵌入流程

```python
from geniml.tokenization import hard_tokenization
from geniml.region2vec import region2vec
from geniml.evaluation import evaluate_embeddings

# 步骤 1：对 BED 文件进行分词
hard_tokenization(
    src_folder='bed_files/',
    dst_folder='tokens/',
    universe_file='universe.bed',
    p_value_threshold=1e-9
)

# 步骤 2：训练 Region2Vec
region2vec(
    token_folder='tokens/',
    save_dir='model/',
    num_shufflings=1000,
    embedding_dim=100
)

# 步骤 3：评估
metrics = evaluate_embeddings(
    embeddings_file='model/embeddings.npy',
    labels_file='metadata.csv'
)
```

### scATAC-seq 分析流程

```python
import scanpy as sc
from geniml.scembed import ScEmbed
from geniml.io import tokenize_cells

# 步骤 1：加载数据
adata = sc.read_h5ad('scatac_data.h5ad')

# 步骤 2：对细胞进行分词
tokenize_cells(
    adata='scatac_data.h5ad',
    universe_file='universe.bed',
    output='tokens.parquet'
)

# 步骤 3：训练 scEmbed
model = ScEmbed(embedding_dim=100)
model.train(dataset='tokens.parquet', epochs=100)

# 步骤 4：生成嵌入
embeddings = model.encode(adata)
adata.obsm['scembed_X'] = embeddings

# 步骤 5：使用 scanpy 进行聚类
sc.pp.neighbors(adata, use_rep='scembed_X')
sc.tl.leiden(adata)
sc.tl.umap(adata)
```

### Universe 构建与评估

```bash
# 生成覆盖度
cat bed_files/*.bed > combined.bed
uniwig -m 25 combined.bed chrom.sizes coverage/

# 使用覆盖度阈值构建 universe
geniml universe build cc \
  --coverage-folder coverage/ \
  --output-file universe.bed \
  --cutoff 5 \
  --merge 100 \
  --filter-size 50

# 评估 universe 质量
geniml universe evaluate \
  --universe universe.bed \
  --coverage-folder coverage/ \
  --bed-folder bed_files/
```

## CLI 参考

Geniml 为主要操作提供命令行接口：

```bash
# Region2Vec 训练
geniml region2vec --token-folder tokens/ --save-dir model/ --num-shuffle 1000

# BEDspace 预处理
geniml bedspace preprocess --input regions/ --metadata labels.csv --universe universe.bed

# BEDspace 训练
geniml bedspace train --input preprocessed.txt --output model/ --dim 100

# BEDspace 搜索
geniml bedspace search -t r2l -d distances.pkl -q query.bed -n 10

# Universe 构建
geniml universe build cc --coverage-folder coverage/ --output universe.bed --cutoff 5

# BEDshift 随机化
geniml bedshift --input peaks.bed --genome hg38 --preserve-chrom --iterations 100
```

## 工具选择指南

**使用 Region2Vec 的场景：**
- 处理批量基因组数据（ChIP-seq、ATAC-seq 等）
- 需要无监督嵌入且无需元数据
- 跨实验比较区域集合
- 为下游监督学习构建特征

**使用 BEDspace 的场景：**
- 有可用的元数据标签（细胞类型、组织、条件）
- 需要按元数据查询区域或反向查询
- 希望为区域和标签构建联合嵌入空间
- 构建可搜索的基因组数据库

**使用 scEmbed 的场景：**
- 分析单细胞 ATAC-seq 数据
- 按染色质可及性对细胞进行聚类
- 从 scATAC-seq 中注释细胞类型
- 希望与 scanpy 集成

**使用 Universe 构建的场景：**
- 需要用于分词的参考峰集合
- 将多个实验合并为一致性集合
- 希望以统计严谨性定义区域
- 为项目构建标准参考

**使用工具的场景：**
- 需要缓存远程 BED 文件（BBClient）
- 生成统计用的零模型（BEDshift）
- 评估嵌入质量（Evaluation）
- 构建搜索接口（Text2BedNN）

## 最佳实践

### 通用指南

- **Universe 质量至关重要**：投入时间构建全面、构造良好的 universe
- **分词验证**：训练前检查覆盖度（理想情况下 >80%）
- **参数调优**：尝试不同的嵌入维度、学习率和训练轮数
- **评估**：始终使用多种指标和可视化方法验证嵌入
- **文档记录**：记录参数和随机种子以确保可复现性

### 性能考虑

- **预分词**：对于 scEmbed，始终预先对细胞进行分词以加快训练速度
- **内存管理**：大型数据集可能需要分批处理或降采样
- **计算资源**：ML/HMM universe 方法计算密集
- **模型缓存**：使用 BBClient 避免重复下载

### 集成模式

- **与 scanpy 集成**：scEmbed 嵌入可作为 `adata.obsm` 条目无缝集成
- **与 BEDbase 集成**：使用 BBClient 访问远程 BED 仓库
- **与 Hugging Face 集成**：导出训练好的模型以便共享和复现
- **与 R 集成**：使用 reticulate 进行 R 集成（参见工具参考）

## 相关项目

Geniml 是 BEDbase 生态系统的一部分：

- **BEDbase**：基因组区域统一平台
- **BEDboss**：BED 文件处理流程
- **Gtars**：基因组工具与实用程序
- **BBClient**：BEDbase 仓库客户端

## 其他资源

- **文档**：https://docs.bedbase.org/geniml/
- **GitHub**：https://github.com/databio/geniml
- **预训练模型**：可在 Hugging Face 上获取（databio 组织）
- **出版物**：方法细节见文档引用

## 故障排除

**"Tokenization coverage too low"（分词覆盖度过低）：**
- 检查 universe 质量和完整性
- 调整 p 值阈值（尝试 1e-6 代替 1e-9）
- 确保 universe 与基因组组装版本匹配

**"Training not converging"（训练不收敛）：**
- 调整学习率（尝试 0.01-0.05 范围）
- 增加训练轮数
- 检查数据质量和预处理

**"Out of memory errors"（内存不足错误）：**
- 减小 scEmbed 的批次大小
- 分块处理数据
- 对单细胞数据使用预分词

**"StarSpace not found"（BEDspace）：**
- 单独安装 StarSpace：https://github.com/facebookresearch/StarSpace
- 正确设置 `--path-to-starspace` 参数

详细的故障排除和方法特定问题，请参阅相应的参考文件。
