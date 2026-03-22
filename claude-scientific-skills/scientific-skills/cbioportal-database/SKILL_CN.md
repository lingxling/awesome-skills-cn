---
name: cbioportal-database
description: 查询 cBioPortal 的癌症基因组学数据,包括体细胞突变、拷贝数变异、基因表达和生存数据,涵盖数百项癌症研究。适用于癌症靶点验证、癌基因/肿瘤抑制因子分析和患者级基因组谱分析。
license: LGPL-3.0
metadata:
    skill-author: Kuan-lin Huang
---

# cBioPortal 数据库

## 概述

cBioPortal 癌症基因组学(https://www.cbioportal.org/)是一个开放获取的资源,用于探索、可视化和分析多维癌症基因组学数据。它托管了来自癌症基因组图谱(TCGA)、AACR GENIE 项目、MSK-IMPACT 和数百个其他癌症研究的数据——涵盖数千个癌症样本的突变、拷贝数变异(CNA)、结构变异、mRNA/蛋白质表达、甲基化和临床数据。

**关键资源:**
- cBioPortal 网站: https://www.cbioportal.org/
- REST API: https://www.cbioportal.org/api/
- API 文档(Swagger): https://www.cbioportal.org/api/swagger-ui/index.html
- Python 客户端: `bravado` 或 `requests`
- GitHub: https://github.com/cBioPortal/cbioportal

## 何时使用此技能

在以下情况下使用 cBioPortal:

- **突变谱系**: 特定癌症类型中有多少比例的样本在特定基因中发生突变?
- **癌基因/TSG 验证**: 某基因在癌症中是否频繁突变、扩增或缺失?
- **共突变模式**: 基因 A 和基因 B 的突变是否互斥或共存?
- **生存分析**: 某基因的突变是否与更好的或更差的患者预后相关?
- **变异谱系**: 哪些类型的变异(错义、截短、扩增、缺失)影响某个基因?
- **泛癌分析**: 比较不同癌症类型的变异频率
- **临床关联**: 将基因组变异与临床变量(分期、分级、治疗反应)联系起来
- **TCGA/GENIE 探索**: 系统访问 TCGA 和临床测序数据集

## 核心功能

### 1. cBioPortal REST API

基础 URL: `https://www.cbioportal.org/api`

API 是 RESTful 的,返回 JSON,公共数据无需 API 密钥。

```python
import requests

BASE_URL = "https://www.cbioportal.org/api"
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}

def cbioportal_get(endpoint, params=None):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def cbioportal_post(endpoint, body):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.post(url, json=body, headers=HEADERS)
    response.raise_for_status()
    return response.json()
```

### 2. 浏览研究

```python
def get_all_studies():
    """列出所有可用的癌症研究。"""
    return cbioportal_get("studies", {"pageSize": 500})

# 每个研究包含:
# studyId: 唯一标识符(例如 "brca_tcga")
# name: 人类可读的名称
# description: 数据集描述
# cancerTypeId: 癌症类型缩写
# referenceGenome: GRCh37 或 GRCh38
# pmid: 相关发表文献

studies = get_all_studies()
print(f"研究总数: {len(studies)}")

# 常见的 TCGA 研究 ID:
# brca_tcga, luad_tcga, coadread_tcga, gbm_tcga, prad_tcga,
# skcm_tcga, blca_tcga, hnsc_tcga, lihc_tcga, stad_tcga

# 筛选 TCGA 研究
tcga_studies = [s for s in studies if "tcga" in s["studyId"]]
print([s["studyId"] for s in tcga_studies[:10]])
```

### 3. 分子谱系

每个研究有多个分子谱系(突变、CNA、表达等):

```python
def get_molecular_profiles(study_id):
    """获取研究的所有分子谱系。"""
    return cbioportal_get(f"studies/{study_id}/molecular-profiles")

profiles = get_molecular_profiles("brca_tcga")
for p in profiles:
    print(f"  {p['molecularProfileId']}: {p['name']} ({p['molecularAlterationType']})")

# 变异类型:
# MUTATION_EXTENDED — 体细胞突变
# COPY_NUMBER_ALTERATION — CNA (GISTIC)
# MRNA_EXPRESSION — mRNA 表达
# PROTEIN_LEVEL — RPPA 蛋白质表达
# STRUCTURAL_VARIANT — 融合/重排
```

### 4. 突变数据

```python
def get_mutations(molecular_profile_id, entrez_gene_ids, sample_list_id=None):
    """获取分子谱系中指定基因的突变。"""
    body = {
        "entrezGeneIds": entrez_gene_ids,
        "sampleListId": sample_list_id or molecular_profile_id.replace("_mutations", "_all")
    }
    return cbioportal_post(
        f"molecular-profiles/{molecular_profile_id}/mutations/fetch",
        body
    )

# BRCA1 的 Entrez ID 是 672,TP53 是 7157,PTEN 是 5728
mutations = get_mutations("brca_tcga_mutations", entrez_gene_ids=[7157])  # TP53

# 每个突变记录包含:
# patientId, sampleId, entrezGeneId, gene.hugoGeneSymbol
# mutationType (Missense_Mutation, Nonsense_Mutation, Frame_Shift_Del 等)
# proteinChange (例如 "R175H")
# variantClassification, variantType
# ncbiBuild, chr, startPosition, endPosition, referenceAllele, variantAllele
# mutationStatus (Somatic/Germline)
# alleleFreqT (肿瘤 VAF)

import pandas as pd
df = pd.DataFrame(mutations)
print(df[["patientId", "mutationType", "proteinChange", "alleleFreqT"]].head())
print(f"\n突变类型:\n{df['mutationType'].value_counts()}")
```

### 5. 拷贝数变异数据

```python
def get_cna(molecular_profile_id, entrez_gene_ids):
    """获取离散 CNA 数据(GISTIC: -2, -1, 0, 1, 2)。"""
    body = {
        "entrezGeneIds": entrez_gene_ids,
        "sampleListId": molecular_profile_id.replace("_gistic", "_all").replace("_cna", "_all")
    }
    return cbioportal_post(
        f"molecular-profiles/{molecular_profile_id}/discrete-copy-number/fetch",
        body
    )

# GISTIC 值:
# -2 = 深度缺失(纯合子丢失)
# -1 = 浅度缺失(杂合子丢失)
#  0 = 二倍体(中性)
#  1 = 低水平获得
#  2 = 高水平扩增

cna_data = get_cna("brca_tcga_gistic", entrez_gene_ids=[1956])  # EGFR
df_cna = pd.DataFrame(cna_data)
print(df_cna["value"].value_counts())
```

### 6. 变异频率(OncoPrint 风格)

```python
def get_alteration_frequency(study_id, gene_symbols, alteration_types=None):
    """计算癌症研究中基因的变异频率。"""
    import requests, pandas as pd

    # 获取样本列表
    samples = requests.get(
        f"{BASE_URL}/studies/{study_id}/sample-lists",
        headers=HEADERS
    ).json()
    all_samples_id = next(
        (s["sampleListId"] for s in samples if s["category"] == "all_cases_in_study"), None
    )
    total_samples = len(requests.get(
        f"{BASE_URL}/sample-lists/{all_samples_id}/sample-ids",
        headers=HEADERS
    ).json())

    # 获取基因 Entrez ID
    gene_data = requests.post(
        f"{BASE_URL}/genes/fetch",
        json=[{"hugoGeneSymbol": g} for g in gene_symbols],
        headers=HEADERS
    ).json()
    entrez_ids = [g["entrezGeneId"] for g in gene_data]

    # 获取突变
    mutation_profile = f"{study_id}_mutations"
    mutations = get_mutations(mutation_profile, entrez_ids, all_samples_id)

    freq = {}
    for g_symbol, e_id in zip(gene_symbols, entrez_ids):
        mutated = len(set(m["patientId"] for m in mutations if m["entrezGeneId"] == e_id))
        freq[g_symbol] = mutated / total_samples * 100

    return freq

# 示例
freq = get_alteration_frequency("brca_tcga", ["TP53", "PIK3CA", "BRCA1", "BRCA2"])
for gene, pct in sorted(freq.items(), key=lambda x: -x[1]):
    print(f"  {gene}: {pct:.1f}%")
```

### 7. 临床数据

```python
def get_clinical_data(study_id, attribute_ids=None):
    """获取患者级临床数据。"""
    params = {"studyId": study_id}
    all_clinical = cbioportal_get(
        "clinical-data/fetch",
        params
    )
    # 返回 {patientId, studyId, clinicalAttributeId, value} 列表

# 临床属性包括:
# OS_STATUS, OS_MONTHS, DFS_STATUS, DFS_MONTHS (生存)
# TUMOR_STAGE, GRADE, AGE, SEX, RACE
# 研究特定属性各不相同

def get_clinical_attributes(study_id):
    """列出研究的所有可用临床属性。"""
    return cbioportal_get(f"studies/{study_id}/clinical-attributes")
```

## 查询工作流程

### 工作流程 1: 癌症类型中的基因变异谱系

```python
import requests, pandas as pd

def alteration_profile(study_id, gene_symbol):
    """癌症研究中基因的完整变异谱系。"""

    # 1. 获取基因 Entrez ID
    gene_info = requests.post(
        f"{BASE_URL}/genes/fetch",
        json=[{"hugoGeneSymbol": gene_symbol}],
        headers=HEADERS
    ).json()[0]
    entrez_id = gene_info["entrezGeneId"]

    # 2. 获取突变
    mutations = get_mutations(f"{study_id}_mutations", [entrez_id])
    mut_df = pd.DataFrame(mutations) if mutations else pd.DataFrame()

    # 3. 获取 CNA
    cna = get_cna(f"{study_id}_gistic", [entrez_id])
    cna_df = pd.DataFrame(cna) if cna else pd.DataFrame()

    # 4. 汇总
    n_mut = len(set(mut_df["patientId"])) if not mut_df.empty else 0
    n_amp = len(cna_df[cna_df["value"] == 2]) if not cna_df.empty else 0
    n_del = len(cna_df[cna_df["value"] == -2]) if not cna_df.empty else 0

    return {"mutations": n_mut, "amplifications": n_amp, "deep_deletions": n_del}

result = alteration_profile("brca_tcga", "PIK3CA")
print(result)
```

### 工作流程 2: 泛癌基因突变频率

```python
import requests, pandas as pd

def pan_cancer_mutation_freq(gene_symbol, cancer_study_ids=None):
    """多个癌症类型中基因的突变频率。"""
    studies = get_all_studies()
    if cancer_study_ids:
        studies = [s for s in studies if s["studyId"] in cancer_study_ids]

    results = []
    for study in studies[:20]:  # 演示时限制
        try:
            freq = get_alteration_frequency(study["studyId"], [gene_symbol])
            results.append({
                "study": study["studyId"],
                "cancer": study.get("cancerTypeId", ""),
                "mutation_pct": freq.get(gene_symbol, 0)
            })
        except Exception:
            pass

    df = pd.DataFrame(results).sort_values("mutation_pct", ascending=False)
    return df
```

### 工作流程 3: 基于突变状态的生存分析

```python
import requests, pandas as pd

def survival_by_mutation(study_id, gene_symbol):
    """获取按突变状态分组的生存数据。"""
    # 此工作流程获取临床和突变数据用于下游分析

    gene_info = requests.post(
        f"{BASE_URL}/genes/fetch",
        json=[{"hugoGeneSymbol": gene_symbol}],
        headers=HEADERS
    ).json()[0]
    entrez_id = gene_info["entrezGeneId"]

    mutations = get_mutations(f"{study_id}_mutations", [entrez_id])
    mutated_patients = set(m["patientId"] for m in mutations)

    clinical = cbioportal_get("clinical-data/fetch", {"studyId": study_id})
    clinical_df = pd.DataFrame(clinical)

    os_data = clinical_df[clinical_df["clinicalAttributeId"].isin(["OS_MONTHS", "OS_STATUS"])]
    os_wide = os_data.pivot(index="patientId", columns="clinicalAttributeId", values="value")
    os_wide["mutated"] = os_wide.index.isin(mutated_patients)

    return os_wide
```

## 关键 API 端点摘要

| 端点 | 描述 |
|----------|-------------|
| `GET /studies` | 列出所有研究 |
| `GET /studies/{studyId}/molecular-profiles` | 研究的分子谱系 |
| `POST /molecular-profiles/{profileId}/mutations/fetch` | 获取突变数据 |
| `POST /molecular-profiles/{profileId}/discrete-copy-number/fetch` | 获取 CNA 数据 |
| `POST /molecular-profiles/{profileId}/molecular-data/fetch` | 获取表达数据 |
| `GET /studies/{studyId}/clinical-attributes` | 可用的临床变量 |
| `GET /clinical-data/fetch` | 临床数据 |
| `POST /genes/fetch` | 按符号或 Entrez ID 获取基因元数据 |
| `GET /studies/{studyId}/sample-lists` | 样本列表 |

## 最佳实践

- **了解研究 ID**: 使用 Swagger UI 或 `GET /studies` 查找正确的研究 ID
- **使用样本列表**: 每个研究有一个 `all` 样本列表和子集;始终指定合适的列表
- **TCGA vs. GENIE**: TCGA 数据全面但较旧;GENIE 有更新的临床测序数据
- **Entrez 基因 ID**: API 使用 Entrez ID — 使用 `/genes/fetch` 从符号转换
- **处理 404 错误**: 某些分子谱系可能不存在于所有研究
- **速率限制**: 批量查询时添加延迟;大规模分析考虑下载数据文件

## 数据下载

对于大规模分析,直接下载研究数据:
```bash
# 下载 TCGA BRCA 数据
wget https://cbioportal-datahub.s3.amazonaws.com/brca_tcga.tar.gz
```

## 其他资源

- **cBioPortal 网站**: https://www.cbioportal.org/
- **API Swagger UI**: https://www.cbioportal.org/api/swagger-ui/index.html
- **文档**: https://docs.cbioportal.org/
- **GitHub**: https://github.com/cBioPortal/cbioportal
- **数据中心**: https://datahub.cbioportal.org/
- **引用**: Cerami E et al. (2012) Cancer Discovery. PMID: 22588877
- **API 客户端**: https://docs.cbioportal.org/web-api-and-clients/
