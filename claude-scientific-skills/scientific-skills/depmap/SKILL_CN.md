---
name: depmap
description: 查询癌症依赖图谱（DepMap）以获取癌细胞系基因依赖性评分（CRISPR Chronos）、药物敏感性数据和基因效应谱。用于识别癌症特异性脆弱性、合成致死相互作用和验证肿瘤学药物靶点。
license: CC-BY-4.0
metadata:
    skill-author: Kuan-lin Huang
---

# DepMap — 癌症依赖图谱

## 概述

癌症依赖图谱（DepMap）项目由 Broad Institute 运行，使用全基因组 CRISPR 敲除筛选（DepMap CRISPR）、RNA 干扰（RNAi）和化合物敏感性测定（PRISM）系统表征数百个癌细胞系的遗传依赖性。DepMap 数据对于以下方面至关重要：
- 识别哪些基因对特定癌症类型至关重要
- 发现癌症选择性依赖性（治疗靶点）
- 验证肿瘤学药物靶点
- 发现合成致死相互作用

**关键资源：**
- DepMap 门户：https://depmap.org/portal/
- DepMap 数据下载：https://depmap.org/portal/download/all/
- Python 包：`depmap`（或通过 API/下载访问）
- API：https://depmap.org/portal/api/

## 何时使用此技能

使用 DepMap 时：

- **靶点验证**：基因在具有特定突变的癌细胞系（例如，KRAS 突变）中是否对生存至关重要？
- **生物标志物发现**：哪些基因组特征预测对基因敲除的敏感性？
- **合成致死**：当另一个基因突变/缺失时，哪些基因选择性至关重要？
- **药物敏感性**：哪些细胞系特征预测对化合物的反应？
- **泛癌症必需性**：基因在所有癌症类型中广泛必需（不良靶点）还是选择性必需？
- **相关性分析**：哪些基因对具有相关的依赖性谱（共必需性）？

## 核心概念

### 依赖性评分

| 评分 | 范围 | 含义 |
|-------|-------|---------|
| **Chronos** (CRISPR) | ~ -3 到 0+ | 越负值越必需。常见必需阈值：−1。泛必需基因 ~−1 到 −2 |
| **RNAi DEMETER2** | ~ -3 到 0+ | 与 Chronos 相似的标度 |
| **基因效应** | 归一化 | 归一化的 Chronos；−1 = 常见必需基因的中位数效应 |

**关键阈值：**
- Chronos ≤ −0.5：可能依赖
- Chronos ≤ −1：强依赖（常见必需范围）

### 细胞系注释

每个细胞系具有：
- `DepMap_ID`：唯一标识符（例如，`ACH-000001`）
- `cell_line_name`：人类可读名称
- `primary_disease`：癌症类型
- `lineage`：广泛组织谱系
- `lineage_subtype`：特定亚型

## 核心能力

### 1. DepMap API

```python
import requests
import pandas as pd

BASE_URL = "https://depmap.org/portal/api"

def depmap_get(endpoint, params=None):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
```

### 2. 基因依赖性评分

```python
def get_gene_dependency(gene_symbol, dataset="Chronos_Combined"):
    """获取基因在所有细胞系中的 CRISPR 依赖性评分。"""
    url = f"{BASE_URL}/gene"
    params = {
        "gene_id": gene_symbol,
        "dataset": dataset
    }
    response = requests.get(url, params=params)
    return response.json()

# 或者，使用 /data 端点：
def get_dependencies_slice(gene_symbol, dataset_name="CRISPRGeneEffect"):
    """从数据集获取基因的依赖性切片。"""
    url = f"{BASE_URL}/data/gene_dependency"
    params = {"gene_name": gene_symbol, "dataset_name": dataset_name}
    response = requests.get(url, params=params)
    data = response.json()
    return data
```

### 3. 基于下载的分析（推荐用于大型查询）

对于大规模分析，下载 DepMap 数据文件并在本地分析：

```python
import pandas as pd
import requests, os

def download_depmap_data(url, output_path):
    """下载 DepMap 数据文件。"""
    response = requests.get(url, stream=True)
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

# DepMap 24Q4 数据文件（根据需要更新版本）
FILES = {
    "crispr_gene_effect": "https://figshare.com/ndownloader/files/...",
    # 或从以下下载：https://depmap.org/portal/download/all/
    # 可用文件：
    # CRISPRGeneEffect.csv - Chronos 基因效应评分
    # OmicsExpressionProteinCodingGenesTPMLogp1.csv - mRNA 表达
    # OmicsSomaticMutationsMatrixDamaging.csv - 突变二元矩阵
    # OmicsCNGene.csv - 拷贝数
    # sample_info.csv - 细胞系元数据
}

def load_depmap_gene_effect(filepath="CRISPRGeneEffect.csv"):
    """
    加载 DepMap CRISPR 基因效应矩阵。
    行 = 细胞系 (DepMap_ID)，列 = 基因 (Symbol (EntrezID))
    """
    df = pd.read_csv(filepath, index_col=0)
    # 将列重命名为仅基因符号
    df.columns = [col.split(" ")[0] for col in df.columns]
    return df

def load_cell_line_info(filepath="sample_info.csv"):
    """加载细胞系元数据。"""
    return pd.read_csv(filepath)
```

### 4. 识别选择性依赖性

```python
import numpy as np
import pandas as pd

def find_selective_dependencies(gene_effect_df, cell_line_info, target_gene,
                                 cancer_type=None, threshold=-0.5):
    """查找对基因选择性依赖的细胞系。"""

    # 获取目标基因的评分
    if target_gene not in gene_effect_df.columns:
        return None

    scores = gene_effect_df[target_gene].dropna()
    dependent = scores[scores <= threshold]

    # 添加细胞系信息
    result = pd.DataFrame({
        "DepMap_ID": dependent.index,
        "gene_effect": dependent.values
    }).merge(cell_line_info[["DepMap_ID", "cell_line_name", "primary_disease", "lineage"]])

    if cancer_type:
        result = result[result["primary_disease"].str.contains(cancer_type, case=False, na=False)]

    return result.sort_values("gene_effect")

# 示例用法（加载数据后）
# df_effect = load_depmap_gene_effect("CRISPRGeneEffect.csv")
# cell_info = load_cell_line_info("sample_info.csv")
# deps = find_selective_dependencies(df_effect, cell_info, "KRAS", cancer_type="Lung")
```

### 5. 生物标志物分析（基因效应与突变）

```python
import pandas as pd
from scipy import stats

def biomarker_analysis(gene_effect_df, mutation_df, target_gene, biomarker_gene):
    """
    测试生物标志物基因中的突变是否预测对目标基因的依赖性。

    参数：
        gene_effect_df: CRISPR 基因效应 DataFrame
        mutation_df: 二元突变 DataFrame (1 = 突变)
        target_gene: 要评估依赖性的基因
        biomarker_gene: 其突变可能预测依赖性的基因
    """
    if target_gene not in gene_effect_df.columns or biomarker_gene not in mutation_df.columns:
        return None

    # 对齐细胞系
    common_lines = gene_effect_df.index.intersection(mutation_df.index)
    scores = gene_effect_df.loc[common_lines, target_gene].dropna()
    mutations = mutation_df.loc[scores.index, biomarker_gene]

    mutated = scores[mutations == 1]
    wt = scores[mutations == 0]

    stat, pval = stats.mannwhitneyu(mutated, wt, alternative='less')

    return {
        "target_gene": target_gene,
        "biomarker_gene": biomarker_gene,
        "n_mutated": len(mutated),
        "n_wt": len(wt),
        "mean_effect_mutated": mutated.mean(),
        "mean_effect_wt": wt.mean(),
        "pval": pval,
        "significant": pval < 0.05
    }
```

### 6. 共必需性分析

```python
import pandas as pd

def co_essentiality(gene_effect_df, target_gene, top_n=20):
    """查找具有最相关依赖性谱的基因（共必需伙伴）。"""
    if target_gene not in gene_effect_df.columns:
        return None

    target_scores = gene_effect_df[target_gene].dropna()

    correlations = {}
    for gene in gene_effect_df.columns:
        if gene == target_gene:
            continue
        other_scores = gene_effect_df[gene].dropna()
        common = target_scores.index.intersection(other_scores.index)
        if len(common) < 50:
            continue
        r = target_scores[common].corr(other_scores[common])
        if not pd.isna(r):
            correlations[gene] = r

    corr_series = pd.Series(correlations).sort_values(ascending=False)
    return corr_series.head(top_n)

# 共必需基因通常共享生物复合物或通路
```

## 查询工作流

### 工作流 1：癌症类型的靶点验证

1. 下载 `CRISPRGeneEffect.csv` 和 `sample_info.csv`
2. 按癌症类型筛选细胞系
3. 计算目标基因在癌症与所有其他细胞系中的平均基因效应
4. 计算选择性：依赖性对您的癌症类型有多特异性？
5. 与突变、表达或 CNA 数据交叉引用作为生物标志物

### 工作流 2：合成致死筛选

1. 识别具有感兴趣基因突变/缺失的细胞系（例如，BRCA1 突变）
2. 计算突变与野生型细胞系中所有基因的基因效应评分
3. 识别在突变细胞系中显著更必需的基因（合成致死伙伴）
4. 按选择性和效应大小筛选

### 工作流 3：化合物敏感性分析

1. 下载 PRISM 化合物敏感性数据（`primary-screen-replicate-treatment-info.csv`）
2. 将化合物 AUC/log2(倍数变化) 与基因组特征相关联
3. 识别化合物敏感性的预测生物标志物

## DepMap 数据文件参考

| 文件 | 描述 |
|------|-------------|
| `CRISPRGeneEffect.csv` | CRISPR Chronos 基因效应（主要依赖性数据） |
| `CRISPRGeneEffectUnscaled.csv` | 未缩放的 CRISPR 评分 |
| `RNAi_merged.csv` | DEMETER2 RNAi 依赖性 |
| `sample_info.csv` | 细胞系元数据（谱系、疾病等） |
| `OmicsExpressionProteinCodingGenesTPMLogp1.csv` | mRNA 表达 |
| `OmicsSomaticMutationsMatrixDamaging.csv` | 损伤性体细胞突变（二元） |
| `OmicsCNGene.csv` | 每个基因的拷贝数 |
| `PRISM_Repurposing_Primary_Screens_Data.csv` | 药物敏感性（重新定位库） |

从以下地址下载所有文件：https://depmap.org/portal/download/all/

## 最佳实践

- **使用 Chronos 评分**（而不是 DEMETER2）进行当前 CRISPR 分析 — 对切割效率控制得更好
- **区分泛必需与癌症选择性**：具有低方差的靶基因（在所有系中都必需）是不良的药物靶点
- **通过表达数据验证**：在细胞系中不表达的基因无论实际功能如何都会被评分为非必需
- **使用 DepMap ID** 进行细胞系识别 — cell_line_name 可能模棱两可
- **考虑拷贝数**：扩增的基因可能由于拷贝数效应而显得必需（垃圾 DNA 假说）
- **多重检验校正**：在全基因组范围内计算生物标志物关联时，应用 FDR 校正

## 其他资源

- **DepMap 门户**：https://depmap.org/portal/
- **数据下载**：https://depmap.org/portal/download/all/
- **DepMap 论文**：Behan FM et al. (2019) Nature. PMID: 30971826
- **Chronos 论文**：Dempster JM et al. (2021) Nature Methods. PMID: 34349281
- **GitHub**：https://github.com/broadinstitute/depmap-portal
- **Figshare**：https://figshare.com/articles/dataset/DepMap_24Q4_Public/27993966
