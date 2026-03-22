---
name: geo-database
description: 查询GEO（基因表达汇编）数据库获取基因表达数据集、样本元数据、平台信息和实验设计。用于查找特定的基因表达研究、检索微阵列/RNA-seq数据、分析差异表达、识别生物标志物或探索基因表达模式。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# GEO 数据库

## 概述

基因表达汇编（GEO）是NCBI维护的公共功能基因组学数据存储库，包含微阵列和下一代测序数据。GEO提供对数百万个样本、数千个系列和数百个数据集的访问，使其成为基因表达研究、生物标志物发现和系统生物学分析的宝贵资源。

## 何时使用此技能

使用GEO数据库当：

- **查找基因表达数据集**：搜索与特定疾病、组织或实验条件相关的研究
- **检索原始数据**：下载微阵列或RNA-seq原始数据文件
- **获取元数据**：访问样本信息、实验设计、平台详情
- **差异表达分析**：识别实验条件之间的差异表达基因
- **生物标志物发现**：寻找与疾病状态相关的基因表达模式
- **系统生物学研究**：整合多个数据集以进行通路和网络分析
- **数据验证**：使用独立数据集验证实验结果

## 核心功能

### 1. GEO数据结构

GEO数据按三个层次组织：

- **GSE（GEO Series）**：包含相关样本的完整实验，包括实验设计、处理方法和摘要数据
- **GSM（GEO Sample）**：单个样本的原始和/或处理数据，包括样本元数据
- **GPL（GEO Platform）**：描述探针集、阵列元素或测序平台的物理格式

### 2. GEOquery（R包）

GEOquery是访问GEO数据的主要工具。

**安装：**
```r
# 使用Bioconductor安装
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
BiocManager::install("GEOquery")
```

**基本用法：**
```r
library(GEOquery)

# 获取GSE数据集
gse <- getGEO("GSE12345", GSEMatrix = TRUE)

# 获取GSM样本
gsm <- getGEO("GSM123456")

# 获取GPL平台
gpl <- getGEO("GPL12345")
```

### 3. 查询GEO数据

#### 按关键词搜索

```r
library(GEOquery)

# 搜索数据集
results <- getGEOmatrix(keyword = "breast cancer", GSEMatrix = TRUE)

# 搜索特定组织
results <- getGEOmatrix(keyword = "lung tissue", GSEMatrix = TRUE)

# 搜索疾病和平台
results <- getGEOmatrix(keyword = "diabetes AND RNA-seq", GSEMatrix = TRUE)
```

#### 按GSE ID获取数据

```r
library(GEOquery)

# 获取GSE数据集
gse <- getGEO("GSE12345", GSEMatrix = TRUE)

# 查看数据集信息
gse
print(gse[[1]])

# 获取表达矩阵
exprs_matrix <- exprs(gse[[1]])

# 获取表型数据
pheno_data <- pData(gse[[1]])

# 获取特征数据
feature_data <- fData(gse[[1]])
```

### 4. 处理GSE数据集

#### 提取表达矩阵

```r
library(GEOquery)

# 获取GSE数据集
gse <- getGEO("GSE12345", GSEMatrix = TRUE)

# 提取表达矩阵
exprs_matrix <- exprs(gse[[1]])

# 查看矩阵维度
dim(exprs_matrix)

# 查看前几行和列
head(exprs_matrix[, 1:5])
```

#### 处理表型数据

```r
# 获取表型数据
pheno_data <- pData(gse[[1]])

# 查看可用的表型变量
colnames(pheno_data)

# 按条件分组
condition <- pheno_data$source_name_ch1

# 创建实验设计矩阵
design <- model.matrix(~0 + condition)
colnames(design) <- levels(condition)
```

#### 处理特征数据

```r
# 获取特征数据
feature_data <- fData(gse[[1]])

# 查看探针信息
head(feature_data)

# 将探针ID映射到基因符号
gene_symbols <- feature_data$Gene.Symbol
```

### 5. 差异表达分析

#### 使用limma进行微阵列分析

```r
library(GEOquery)
library(limma)

# 获取GSE数据集
gse <- getGEO("GSE12345", GSEMatrix = TRUE)
exprs_matrix <- exprs(gse[[1]])
pheno_data <- pData(gse[[1]])

# 创建设计矩阵
condition <- factor(pheno_data$source_name_ch1)
design <- model.matrix(~0 + condition)
colnames(design) <- levels(condition)

# 拟合线性模型
fit <- lmFit(exprs_matrix, design)

# 创建比较矩阵
contrast.matrix <- makeContrasts(Treatment - Control, levels=design)

# 拟合对比
fit2 <- contrasts.fit(fit, contrast.matrix)
fit2 <- eBayes(fit2)

# 获取差异表达基因
top_genes <- topTable(fit2, adjust="fdr", number=Inf)

# 筛选显著基因
significant_genes <- top_genes[top_genes$adj.P.Val < 0.05, ]
```

#### 使用edgeR进行RNA-seq分析

```r
library(GEOquery)
library(edgeR)

# 获取GSE数据集
gse <- getGEO("GSE12345", GSEMatrix = TRUE)
counts <- exprs(gse[[1]])
pheno_data <- pData(gse[[1]])

# 创建DGEList对象
group <- factor(pheno_data$source_name_ch1)
dge <- DGEList(counts=counts, group=group)

# 标准化
dge <- calcNormFactors(dge)

# 创建设计矩阵
design <- model.matrix(~group)

# 估计离散度
dge <- estimateDisp(dge, design)

# 拟合模型
fit <- glmFit(dge, design)

# 执行检验
lrt <- glmLRT(fit, coef=2)

# 获取差异表达基因
top_genes <- topTags(lrt, n=Inf)

# 筛选显著基因
significant_genes <- top_genes[top_genes$FDR < 0.05, ]
```

### 6. 数据可视化

#### 热图

```r
library(pheatmap)

# 选择top差异表达基因
top_de_genes <- rownames(significant_genes)[1:50]
heatmap_data <- exprs_matrix[top_de_genes, ]

# 创建热图
pheatmap(heatmap_data,
         annotation_col = pheno_data[, c("source_name_ch1")],
         show_rownames = FALSE,
         scale = "row")
```

#### PCA图

```r
library(ggplot2)

# 执行PCA
pca_result <- prcomp(t(exprs_matrix), scale. = TRUE)

# 创建数据框
pca_df <- data.frame(PC1 = pca_result$x[,1],
                     PC2 = pca_result$x[,2],
                     condition = pheno_data$source_name_ch1)

# 绘制PCA
ggplot(pca_df, aes(x=PC1, y=PC2, color=condition)) +
  geom_point(size=3) +
  theme_minimal() +
  labs(title="PCA of Gene Expression Data")
```

#### 火山图

```r
library(ggplot2)

# 创建火山图
ggplot(top_genes, aes(x=logFC, y=-log10(adj.P.Val))) +
  geom_point(alpha=0.5) +
  geom_hline(yintercept=-log10(0.05), linetype="dashed", color="red") +
  geom_vline(xintercept=c(-1, 1), linetype="dashed", color="blue") +
  theme_minimal() +
  labs(title="Volcano Plot",
       x="Log2 Fold Change",
       y="-Log10 Adjusted P-Value")
```

### 7. 下载原始数据

#### 下载微阵列原始数据

```r
library(GEOquery)

# 获取GSM样本
gsm <- getGEO("GSM123456")

# 下载原始数据文件
raw_data <- getGEOSuppFiles("GSM123456")

# 解压文件
untar("GSM123456.tar.gz")
```

#### 下载RNA-seq原始数据

```r
library(GEOquery)

# 获取GSE数据集
gse <- getGEO("GSE12345", GSEMatrix = FALSE)

# 获取SRA访问号
sra_accessions <- gse@relation$`SRA`

# 使用SRA工具包下载数据
# 需要安装SRA Toolkit
# prefetch SRR12345678
```

### 8. 批量处理多个GSE数据集

```r
library(GEOquery)
library(limma)

# GSE ID列表
gse_ids <- c("GSE12345", "GSE12346", "GSE12347")

# 批量处理
results <- list()
for (gse_id in gse_ids) {
  # 获取数据集
  gse <- getGEO(gse_id, GSEMatrix = TRUE)

  # 提取表达矩阵
  exprs_matrix <- exprs(gse[[1]])
  pheno_data <- pData(gse[[1]])

  # 执行差异表达分析
  # ... (分析代码)

  # 保存结果
  results[[gse_id]] <- top_genes
}
```

## 最佳实践

1. **数据质量检查**：在分析之前始终检查数据质量
2. **适当的归一化**：根据数据类型使用适当的归一化方法
3. **批次效应校正**：如果存在批次效应，使用ComBat或其他方法
4. **多重检验校正**：使用FDR或Bonferroni校正调整p值
5. **验证结果**：使用独立数据集验证发现
6. **文档记录**：记录所有分析步骤以实现可重现性

## 常见问题

**问题：GSE数据集很大，下载很慢**
- 解决方案：使用GSEMatrix = FALSE仅下载元数据，或使用GEOquery的getGEOSuppFiles函数分批下载

**问题：探针ID到基因符号的映射不明确**
- 解决方案：检查GPL平台信息，使用适当的注释包

**问题：样本元数据不一致**
- 解决方案：仔细检查表型数据，必要时手动整理

**问题：数据质量差**
- 解决方案：执行质量控制分析，移除低质量样本或探针

## 其他资源

- **GEO网站**: https://www.ncbi.nlm.nih.gov/geo/
- **GEOquery文档**: https://bioconductor.org/packages/release/bioc/html/GEOquery.html
- **NCBI GEO教程**: https://www.ncbi.nlm.nih.gov/geo/info/tutorial.html
- **GEO数据格式规范**: https://www.ncbi.nlm.nih.gov/geo/info/soft2.html
- **GEO数据集提交指南**: https://www.ncbi.nlm.nih.gov/geo/info/submit.html
