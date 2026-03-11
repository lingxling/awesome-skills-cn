---
name: gtex-database
description: 查询GTEx（基因型-组织表达）门户获取组织特异性基因表达、eQTL（表达数量性状位点）和sQTL。对于将GWAS变体链接到基因调控、理解组织特异性表达和解释非编码变体效应至关重要。
license: CC-BY-4.0
metadata:
    skill-author: Kuan-lin Huang
---

# GTEx 数据库

## 概述

基因型-组织表达（GTEx）项目为研究跨54个非疾病人类组织的组织特异性基因表达和遗传调控提供了全面的资源。GTEx v10（最新版本）使研究人员能够理解遗传变体如何以组织特异性方式调控基因表达（eQTL）和剪接（sQTL），这对于解释GWAS位点和识别调控机制至关重要。

**关键资源：**
- GTEx门户：https://gtexportal.org/
- GTEx API v2：https://gtexportal.org/api/v2/
- 数据下载：https://gtexportal.org/home/downloads/adult-gtex/
- 文档：https://gtexportal.org/home/documentationPage

## 何时使用此技能

使用GTEx当：

- **GWAS位点解释**：通过eQTL识别非编码GWAS变体调控哪个基因
- **组织特异性表达**：跨54个人类组织比较基因表达水平
- **eQTL共定位**：测试GWAS信号和eQTL信号是否共享相同的因果变体
- **多组织eQTL分析**：查找在多个组织中调控表达的变体
- **剪接QTL（sQTL）**：识别影响剪接比例的变体
- **组织特异性分析**：确定哪些组织表达感兴趣的基因
- **基因表达探索**：检索每个组织的标准化表达水平（TPM）

## 核心功能

### 1. GTEx REST API v2

基础URL：`https://gtexportal.org/api/v2/`

API返回JSON，不需要身份验证。所有端点都支持分页。

```python
import requests

BASE_URL = "https://gtexportal.org/api/v2"

def gtex_get(endpoint, params=None):
    """向GTEx API发出GET请求。"""
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, params=params, headers={"Accept": "application/json"})
    response.raise_for_status()
    return response.json()
```

### 2. 按组织的基因表达

```python
import requests
import pandas as pd

def get_gene_expression_by_tissue(gene_id_or_symbol, dataset_id="gtex_v10"):
    """获取所有组织的基因中位数表达。"""
    url = "https://gtexportal.org/api/v2/expression/medianGeneExpression"
    params = {
        "gencodeId": gene_id_or_symbol,
        "datasetId": dataset_id,
        "itemsPerPage": 100
    }
    response = requests.get(url, params=params)
    data = response.json()

    records = data.get("data", [])
    df = pd.DataFrame(records)
    if not df.empty:
        df = df[["tissueSiteDetailId", "tissueSiteDetail", "median", "unit"]].sort_values(
            "median", ascending=False
        )
    return df

# 示例：获取APOE跨组织的表达
df = get_gene_expression_by_tissue("ENSG00000130203.10")  # APOE GENCODE ID
# 或使用基因符号（某些端点接受两者）
print(df.head(10))
# 输出：组织名称、中位数TPM，按最高表达排序
```

### 3. eQTL查找

```python
import requests
import pandas as pd

def query_eqtl(gene_id, tissue_id=None, dataset_id="gtex_v10"):
    """查询基因的显著eQTL，可选择按组织过滤。"""
    url = "https://gtexportal.org/api/v2/association/singleTissueEqtl"
    params = {
        "gencodeId": gene_id,
        "datasetId": dataset_id,
        "itemsPerPage": 250
    }
    if tissue_id:
        params["tissueSiteDetailId"] = tissue_id

    all_results = []
    page = 0
    while True:
        params["page"] = page
        response = requests.get(url, params=params)
        data = response.json()
        results = data.get("data", [])
        if not results:
            break
        all_results.extend(results)
        if len(results) < params["itemsPerPage"]:
            break
        page += 1

    df = pd.DataFrame(all_results)
    if not df.empty:
        df = df.sort_values("pval", ascending=True)
    return df

# 示例：查找PCSK9的eQTL
df = query_eqtl("ENSG00000169174.14")
print(df[["snpId", "tissueSiteDetailId", "slope", "pval", "gencodeId"]].head(20))
```

### 4. 按变体的单组织eQTL

```python
import requests

def query_variant_eqtl(variant_id, tissue_id=None, dataset_id="gtex_v10"):
    """获取特定变体的所有eQTL关联。"""
    url = "https://gtexportal.org/api/v2/association/singleTissueEqtl"
    params = {
        "variantId": variant_id,  # 例如"chr1_55516888_G_GA_b38"
        "datasetId": dataset_id,
        "itemsPerPage": 250
    }
    if tissue_id:
        params["tissueSiteDetailId"] = tissue_id

    response = requests.get(url, params=params)
    return response.json()

# GTEx变体ID格式：chr{chrom}_{pos}_{ref}_{alt}_b38
# 示例："chr17_43094692_G_A_b38"
```

### 5. 多组织eQTL（eGenes）

```python
import requests

def get_egenes(tissue_id, dataset_id="gtex_v10"):
    """获取组织中的所有eGenes（至少有一个显著eQTL的基因）。"""
    url = "https://gtexportal.org/api/v2/association/egene"
    params = {
        "tissueSiteDetailId": tissue_id,
        "datasetId": dataset_id,
        "itemsPerPage": 500
    }

    all_egenes = []
    page = 0
    while True:
        params["page"] = page
        response = requests.get(url, params=params)
        data = response.json()
        batch = data.get("data", [])
        if not batch:
            break
        all_egenes.extend(batch)
        if len(batch) < params["itemsPerPage"]:
            break
        page += 1
    return all_egenes

# 示例：全血中的所有eGenes
egenes = get_egenes("Whole_Blood")
print(f"在Whole Blood中找到{len(egenes)}个eGenes")
```

### 6. 组织列表

```python
import requests

def get_tissues(dataset_id="gtex_v10"):
    """获取所有可用组织及其元数据。"""
    url = "https://gtexportal.org/api/v2/dataset/tissueSiteDetail"
    params = {"datasetId": dataset_id, "itemsPerPage": 100}
    response = requests.get(url, params=params)
    return response.json()["data"]

tissues = get_tissues()
# 关键字段：tissueSiteDetailId、tissueSiteDetail、colorHex、samplingSite
# 常见组织ID：
# Whole_Blood、Brain_Cortex、Liver、Kidney_Cortex、Heart_Left_Ventricle、
# Lung、Muscle_Skeletal、Adipose_Subcutaneous、Colon_Transverse、...
```

### 7. sQTL（剪接QTL）

```python
import requests

def query_sqtl(gene_id, tissue_id=None, dataset_id="gtex_v10"):
    """查询基因的显著sQTL。"""
    url = "https://gtexportal.org/api/v2/association/singleTissueSqtl"
    params = {
        "gencodeId": gene_id,
        "datasetId": dataset_id,
        "itemsPerPage": 250
    }
    if tissue_id:
        params["tissueSiteDetailId"] = tissue_id

    response = requests.get(url, params=params)
    return response.json()
```

## 查询工作流

### 工作流1：通过eQTL解释GWAS变体

1. **识别GWAS变体**（rs ID或染色体位置）
2. **转换为GTEx变体ID格式**（`chr{chrom}_{pos}_{ref}_{alt}_b38`）
3. **跨组织查询所有eQTL关联**
4. **检查效应方向**：GWAS风险等位基因是否与eQTL效应等位基因相同？
5. **优先考虑组织**：选择与疾病生物学相关的组织
6. **考虑共定位**：使用`coloc`（R包）和完整汇总统计

```python
import requests, pandas as pd

def interpret_gwas_variant(variant_id, dataset_id="gtex_v10"):
    """查找GWAS变体调控的所有基因。"""
    url = "https://gtexportal.org/api/v2/association/singleTissueEqtl"
    params = {"variantId": variant_id, "datasetId": dataset_id, "itemsPerPage": 500}
    response = requests.get(url, params=params)
    data = response.json()

    df = pd.DataFrame(data.get("data", []))
    if df.empty:
        return df
    return df[["geneSymbol", "tissueSiteDetailId", "slope", "pval", "maf"]].sort_values("pval")

# 示例
results = interpret_gwas_variant("chr1_154453788_A_T_b38")
print(results.groupby("geneSymbol")["tissueSiteDetailId"].count().sort_values(ascending=False))
```

### 工作流2：基因表达图谱

1. 获取基因跨所有组织的中位数表达
2. 识别主要表达位点
3. 与疾病相关组织比较
4. 下载原始数据进行统计比较

### 工作流3：组织特异性eQTL分析

1. 选择与疾病相关的组织
2. 查询该组织中的所有eGenes
3. 与GWAS显著位点交叉引用
4. 识别共定位信号

## 关键API端点

| 端点 | 描述 |
|----------|-------------|
| `/expression/medianGeneExpression` | 基因每个组织的中位数TPM |
| `/expression/geneExpression` | 每个组织的完整表达分布 |
| `/association/singleTissueEqtl` | 显著eQTL关联 |
| `/association/singleTissueSqtl` | 显著sQTL关联 |
| `/association/egene` | 组织中的eGenes |
| `/dataset/tissueSiteDetail` | 具有元数据的可用组织 |
| `/reference/gene` | 基因元数据（GENCODE ID、坐标） |
| `/variant/variantPage` | 按rsID或位置查找变体 |

## 可用数据集

| ID | 描述 |
|----|-------------|
| `gtex_v10` | GTEx v10（当前；~960个供体，54个组织） |
| `gtex_v8` | GTEx v8（838个供体，49个组织）——较旧但被广泛引用 |

## 最佳实践

- **使用GENCODE ID**（例如`ENSG00000130203.10`）进行基因查询；`.version`后缀对某些端点很重要
- **GTEx变体ID**使用格式`chr{chrom}_{pos}_{ref}_{alt}_b38`（GRCh38）——与rs ID不同
- **处理分页**：大型查询（例如所有eGenes）需要迭代遍历页面
- **组织命名法**：对API调用使用`tissueSiteDetailId`（例如`Whole_Blood`）而不是显示名称
- **FDR校正**：GTEx使用FDR < 0.05（q值）作为eQTL的显著性阈值
- **效应等位基因**：`slope`字段是替代等位基因的效应；正数=替代等位基因具有更高表达

## 数据下载（用于大规模分析）

对于全基因组分析，下载完整汇总统计而不是使用API：

```bash
# 所有显著eQTL（v10）
wget https://storage.googleapis.com/adult-gtex/bulk-qtl/v10/single-tissue-cis-qtl/GTEx_Analysis_v10_eQTL.tar

# 标准化表达矩阵
wget https://storage.googleapis.com/adult-gtex/bulk-gex/v10/rna-seq/GTEx_Analysis_v10_RNASeQCv2.4.2_gene_reads.gct.gz
```

## 其他资源

- **GTEx门户**: https://gtexportal.org/
- **API文档**: https://gtexportal.org/api/v2/
- **数据下载**: https://gtexportal.org/home/downloads/adult-gtex/
- **GitHub**: https://github.com/broadinstitute/gtex-pipeline
- **引用**: GTEx Consortium (2020) Science. PMID: 32913098
