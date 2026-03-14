---
name: pydeseq2
description: 差异基因表达分析（Python DESeq2）。从批量RNA-seq计数数据中识别差异表达基因，执行Wald检验，FDR校正，火山/MA图，用于RNA-seq分析。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# PyDESeq2

## 概述

PyDESeq2是DESeq2的Python实现，用于批量RNA-seq数据的差异表达分析。设计并执行从数据加载到结果解释的完整工作流程，包括单因素和多因素设计、带多重测试校正的Wald检验、可选的apeGLM收缩，以及与pandas和AnnData的集成。

## 使用场景

本技能适用于以下情况：
- 分析批量RNA-seq计数数据的差异表达
- 比较实验条件之间的基因表达（例如，处理组vs对照组）
- 执行考虑批次效应或协变量的多因素设计
- 将基于R的DESeq2工作流转换为Python
- 将差异表达分析集成到基于Python的管道中
- 用户提到"DESeq2"、"差异表达"、"RNA-seq分析"或"PyDESeq2"

## 快速开始工作流程

对于想要执行标准差异表达分析的用户：

```python
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

# 1. 加载数据
counts_df = pd.read_csv("counts.csv", index_col=0).T  # 转置为样本 × 基因
metadata = pd.read_csv("metadata.csv", index_col=0)

# 2. 过滤低计数基因
genes_to_keep = counts_df.columns[counts_df.sum(axis=0) >= 10]
counts_df = counts_df[genes_to_keep]

# 3. 初始化并拟合DESeq2
dds = DeseqDataSet(
    counts=counts_df,
    metadata=metadata,
    design="~condition",
    refit_cooks=True
)
dds.deseq2()

# 4. 执行统计测试
ds = DeseqStats(dds, contrast=["condition", "treated", "control"])
ds.summary()

# 5. 访问结果
results = ds.results_df
significant = results[results.padj < 0.05]
print(f"Found {len(significant)} significant genes")
```

## 核心工作流程步骤

### 步骤1：数据准备

**输入要求：**
- **计数矩阵：** 样本 × 基因的DataFrame，包含非负整数读取计数
- **元数据：** 样本 × 变量的DataFrame，包含实验因素

**常见数据加载模式：**

```python
# 从CSV（典型格式：基因 × 样本，需要转置）
counts_df = pd.read_csv("counts.csv", index_col=0).T
metadata = pd.read_csv("metadata.csv", index_col=0)

# 从TSV
counts_df = pd.read_csv("counts.tsv", sep="\t", index_col=0).T

# 从AnnData
import anndata as ad
adata = ad.read_h5ad("data.h5ad")
counts_df = pd.DataFrame(adata.X, index=adata.obs_names, columns=adata.var_names)
metadata = adata.obs
```

**数据过滤：**

```python
# 移除低计数基因
genes_to_keep = counts_df.columns[counts_df.sum(axis=0) >= 10]
counts_df = counts_df[genes_to_keep]

# 移除元数据缺失的样本
samples_to_keep = ~metadata.condition.isna()
counts_df = counts_df.loc[samples_to_keep]
metadata = metadata.loc[samples_to_keep]
```

### 步骤2：设计规范

设计公式指定基因表达的建模方式。

**单因素设计：**
```python
design = "~condition"  # 简单的两组比较
```

**多因素设计：**
```python
design = "~batch + condition"  # 控制批次效应
design = "~age + condition"     # 包含连续协变量
design = "~group + condition + group:condition"  # 交互效应
```

**设计公式指南：**
- 使用Wilkinson公式表示法（R风格）
- 将调整变量（如批次）放在主要感兴趣变量之前
- 确保变量作为元数据DataFrame中的列存在
- 使用适当的数据类型（离散变量使用分类类型）

### 步骤3：DESeq2拟合

初始化DeseqDataSet并运行完整管道：

```python
from pydeseq2.dds import DeseqDataSet

dds = DeseqDataSet(
    counts=counts_df,
    metadata=metadata,
    design="~condition",
    refit_cooks=True,  # 移除异常值后重新拟合
    n_cpus=1           # 并行处理（根据需要调整）
)

# 运行完整的DESeq2管道
dds.deseq2()
```

**`deseq2()`的功能：**
1. 计算大小因子（标准化）
2. 拟合基因级分散度
3. 拟合分散度趋势曲线
4. 计算分散度先验
5. 拟合MAP分散度（收缩）
6. 拟合对数倍数变化
7. 计算Cook距离（异常值检测）
8. 如果检测到异常值则重新拟合（可选）

### 步骤4：统计测试

执行Wald检验以识别差异表达基因：

```python
from pydeseq2.ds import DeseqStats

ds = DeseqStats(
    dds,
    contrast=["condition", "treated", "control"],  # 测试treated vs control
    alpha=0.05,                # 显著性阈值
    cooks_filter=True,         # 过滤异常值
    independent_filter=True    # 过滤低功效测试
)

ds.summary()
```

**对比规范：**
- 格式：`[variable, test_level, reference_level]`
- 示例：`["condition", "treated", "control"]` 测试treated vs control
- 如果为`None`，使用设计中的最后一个系数

**结果DataFrame列：**
- `baseMean`：跨样本的平均标准化计数
- `log2FoldChange`：条件之间的log2倍数变化
- `lfcSE`：LFC的标准误差
- `stat`：Wald检验统计量
- `pvalue`：原始p值
- `padj`：调整后的p值（通过Benjamini-Hochberg进行FDR校正）

### 步骤5：可选的LFC收缩

应用收缩以减少倍数变化估计中的噪声：

```python
ds.lfc_shrink()  # 应用apeGLM收缩
```

**何时使用LFC收缩：**
- 用于可视化（火山图，热图）
- 用于按效应大小对基因进行排序
- 当优先考虑用于后续实验的基因时

**重要：** 收缩仅影响log2FoldChange值，不影响统计测试结果（p值保持不变）。使用收缩值进行可视化，但报告未收缩的p值用于显著性。

### 步骤6：结果导出

保存结果和中间对象：

```python
import pickle

# 导出结果为CSV
ds.results_df.to_csv("deseq2_results.csv")

# 仅保存显著基因
significant = ds.results_df[ds.results_df.padj < 0.05]
significant.to_csv("significant_genes.csv")

# 保存DeseqDataSet供以后使用
with open("dds_result.pkl", "wb") as f:
    pickle.dump(dds.to_picklable_anndata(), f)
```

## 常见分析模式

### 两组比较

标准病例对照比较：

```python
dds = DeseqDataSet(counts=counts_df, metadata=metadata, design="~condition")
dds.deseq2()

ds = DeseqStats(dds, contrast=["condition", "treated", "control"])
ds.summary()

results = ds.results_df
significant = results[results.padj < 0.05]
```

### 多重比较

测试多个治疗组与对照组：

```python
dds = DeseqDataSet(counts=counts_df, metadata=metadata, design="~condition")
dds.deseq2()

treatments = ["treatment_A", "treatment_B", "treatment_C"]
all_results = {}

for treatment in treatments:
    ds = DeseqStats(dds, contrast=["condition", treatment, "control"])
    ds.summary()
    all_results[treatment] = ds.results_df

    sig_count = len(ds.results_df[ds.results_df.padj < 0.05])
    print(f"{treatment}: {sig_count} significant genes")
```

### 考虑批次效应

控制技术变异：

```python
# 在设计中包含批次
dds = DeseqDataSet(counts=counts_df, metadata=metadata, design="~batch + condition")
dds.deseq2()

# 在控制批次的同时测试条件
ds = DeseqStats(dds, contrast=["condition", "treated", "control"])
ds.summary()
```

### 连续协变量

包含年龄或剂量等连续变量：

```python
# 确保连续变量是数值型
metadata["age"] = pd.to_numeric(metadata["age"])

dds = DeseqDataSet(counts=counts_df, metadata=metadata, design="~age + condition")
dds.deseq2()

ds = DeseqStats(dds, contrast=["condition", "treated", "control"])
ds.summary()
```

## 使用分析脚本

本技能包含一个完整的命令行脚本，用于标准分析：

```bash
# 基本用法
python scripts/run_deseq2_analysis.py \
  --counts counts.csv \
  --metadata metadata.csv \
  --design "~condition" \
  --contrast condition treated control \
  --output results/

# 带有附加选项
python scripts/run_deseq2_analysis.py \
  --counts counts.csv \
  --metadata metadata.csv \
  --design "~batch + condition" \
  --contrast condition treated control \
  --output results/ \
  --min-counts 10 \
  --alpha 0.05 \
  --n-cpus 4 \
  --plots
```

**脚本功能：**
- 自动数据加载和验证
- 基因和样本过滤
- 完整的DESeq2管道执行
- 具有可自定义参数的统计测试
- 结果导出（CSV，pickle）
- 可选的可视化（火山图和MA图）

当用户需要独立分析工具或想要批量处理多个数据集时，请参考`scripts/run_deseq2_analysis.py`。

## 结果解释

### 识别显著基因

```python
# 按调整后p值过滤
significant = ds.results_df[ds.results_df.padj < 0.05]

# 同时按显著性和效应大小过滤
sig_and_large = ds.results_df[
    (ds.results_df.padj < 0.05) &
    (abs(ds.results_df.log2FoldChange) > 1)
]

# 分离上调和下调基因
upregulated = significant[significant.log2FoldChange > 0]
downregulated = significant[significant.log2FoldChange < 0]

print(f"Upregulated: {len(upregulated)}")
print(f"Downregulated: {len(downregulated)}")
```

### 排序和排名

```python
# 按调整后p值排序
top_by_padj = ds.results_df.sort_values("padj").head(20)

# 按绝对倍数变化排序（使用收缩值）
ds.lfc_shrink()
ds.results_df["abs_lfc"] = abs(ds.results_df.log2FoldChange)
top_by_lfc = ds.results_df.sort_values("abs_lfc", ascending=False).head(20)

# 按组合指标排序
ds.results_df["score"] = -np.log10(ds.results_df.padj) * abs(ds.results_df.log2FoldChange)
top_combined = ds.results_df.sort_values("score", ascending=False).head(20)
```

### 质量指标

```python
# 检查标准化（大小因子应接近1）
print("Size factors:", dds.obsm["size_factors"])

# 检查分散度估计
import matplotlib.pyplot as plt
plt.hist(dds.varm["dispersions"], bins=50)
plt.xlabel("Dispersion")
plt.ylabel("Frequency")
plt.title("Dispersion Distribution")
plt.show()

# 检查p值分布（应大部分平坦，在0附近有峰值）
plt.hist(ds.results_df.pvalue.dropna(), bins=50)
plt.xlabel("P-value")
plt.ylabel("Frequency")
plt.title("P-value Distribution")
plt.show()
```

## 可视化指南

### 火山图

可视化显著性与效应大小：

```python
import matplotlib.pyplot as plt
import numpy as np

results = ds.results_df.copy()
results["-log10(padj)"] = -np.log10(results.padj)

plt.figure(figsize=(10, 6))
significant = results.padj < 0.05

plt.scatter(
    results.loc[~significant, "log2FoldChange"],
    results.loc[~significant, "-log10(padj)"],
    alpha=0.3, s=10, c='gray', label='Not significant'
)
plt.scatter(
    results.loc[significant, "log2FoldChange"],
    results.loc[significant, "-log10(padj)"],
    alpha=0.6, s=10, c='red', label='padj < 0.05'
)

plt.axhline(-np.log10(0.05), color='blue', linestyle='--', alpha=0.5)
plt.xlabel("Log2 Fold Change")
plt.ylabel("-Log10(Adjusted P-value)")
plt.title("Volcano Plot")
plt.legend()
plt.savefig("volcano_plot.png", dpi=300)
```

### MA图

显示倍数变化与平均表达：

```python
plt.figure(figsize=(10, 6))

plt.scatter(
    np.log10(results.loc[~significant, "baseMean"] + 1),
    results.loc[~significant, "log2FoldChange"],
    alpha=0.3, s=10, c='gray'
)
plt.scatter(
    np.log10(results.loc[significant, "baseMean"] + 1),
    results.loc[significant, "log2FoldChange"],
    alpha=0.6, s=10, c='red'
)

plt.axhline(0, color='blue', linestyle='--', alpha=0.5)
plt.xlabel("Log10(Base Mean + 1)")
plt.ylabel("Log2 Fold Change")
plt.title("MA Plot")
plt.savefig("ma_plot.png", dpi=300)
```

## 排查常见问题

### 数据格式问题

**问题：** "Index mismatch between counts and metadata"

**解决方案：** 确保样本名称完全匹配
```python
print("Counts samples:", counts_df.index.tolist())
print("Metadata samples:", metadata.index.tolist())

# 如有需要，取交集
common = counts_df.index.intersection(metadata.index)
counts_df = counts_df.loc[common]
metadata = metadata.loc[common]
```

**问题：** "All genes have zero counts"

**解决方案：** 检查数据是否需要转置
```python
print(f"Counts shape: {counts_df.shape}")
# 如果基因 > 样本，需要转置
if counts_df.shape[1] < counts_df.shape[0]:
    counts_df = counts_df.T
```

### 设计矩阵问题

**问题：** "Design matrix is not full rank"

**原因：** 变量混淆（例如，所有处理样本都在一个批次中）

**解决方案：** 移除混淆变量或添加交互项
```python
# 检查混淆
print(pd.crosstab(metadata.condition, metadata.batch))

# 简化设计或添加交互
# 移除批次
design = "~condition"  
# 或
# 模型交互
design = "~condition + batch + condition:batch"  
```

### 无显著基因

**诊断：**
```python
# 检查分散度分布
plt.hist(dds.varm["dispersions"], bins=50)
plt.show()

# 检查大小因子
print(dds.obsm["size_factors"])

# 查看按原始p值排序的前基因
print(ds.results_df.nsmallest(20, "pvalue"))
```

**可能的原因：**
- 效应大小小
- 生物变异性高
- 样本量不足
- 技术问题（批次效应，异常值）

## 参考文档

对于超出此工作流导向指南的全面详细信息：

- **API参考**（`references/api_reference.md`）：PyDESeq2类、方法和数据结构的完整文档。当需要详细参数信息或理解对象属性时使用。

- **工作流指南**（`references/workflow_guide.md`）：深入指南，涵盖完整的分析工作流、数据加载模式、多因素设计、故障排除和最佳实践。当处理复杂的实验设计或遇到问题时使用。

当用户需要以下内容时，将这些参考加载到上下文中：
- 详细的API文档：`Read references/api_reference.md`
- 综合工作流示例：`Read references/workflow_guide.md`
- 故障排除指南：`Read references/workflow_guide.md`（见故障排除部分）

## 关键提醒

1. **数据方向很重要：** 计数矩阵通常以基因 × 样本的形式加载，但需要是样本 × 基因。如果需要，始终使用`.T`进行转置。

2. **样本过滤：** 在分析前移除元数据缺失的样本以避免错误。

3. **基因过滤：** 过滤低计数基因（例如，总读取数 < 10）以提高功效并减少计算时间。

4. **设计公式顺序：** 将调整变量放在感兴趣变量之前（例如，`"~batch + condition"`而不是`"~condition + batch"`）。

5. **LFC收缩时机：** 在统计测试后应用收缩，仅用于可视化/排名目的。P值基于未收缩的估计值。

6. **结果解释：** 使用`padj < 0.05`表示显著性，而不是原始p值。Benjamini-Hochberg程序控制错误发现率。

7. **对比规范：** 格式为`[variable, test_level, reference_level]`，其中test_level与reference_level进行比较。

8. **保存中间对象：** 使用pickle保存DeseqDataSet对象，以便以后使用或进行额外分析，而无需重新运行昂贵的拟合步骤。

## 安装和要求

```bash
uv pip install pydeseq2
```

**系统要求：**
- Python 3.10-3.11
- pandas 1.4.3+
- numpy 1.23.0+
- scipy 1.11.0+
- scikit-learn 1.1.1+
- anndata 0.8.0+

**可视化可选依赖：**
- matplotlib
- seaborn

## 其他资源

- **官方文档：** https://pydeseq2.readthedocs.io
- **GitHub存储库：** https://github.com/owkin/PyDESeq2
- **出版物：** Muzellec et al. (2023) Bioinformatics, DOI: 10.1093/bioinformatics/btad547
- **原始DESeq2 (R)：** Love et al. (2014) Genome Biology, DOI: 10.1186/s13059-014-0550-8