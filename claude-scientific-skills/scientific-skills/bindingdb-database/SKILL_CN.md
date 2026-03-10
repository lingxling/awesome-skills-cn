---
name: bindingdb-database
description: 查询 BindingDB 以获取测量的药物-靶点结合亲和力（Ki、Kd、IC50、EC50）。按靶点（UniProt ID）、化合物（SMILES/名称）或病原体搜索。对于药物发现、先导化合物优化、多药理学分析和构效关系（SAR）研究至关重要。
license: CC-BY-3.0
metadata:
    skill-author: Kuan-lin Huang
---

# BindingDB 数据库

## 概述

BindingDB (https://www.bindingdb.org/) 是测量药物-蛋白质结合亲和力的主要公共数据库。它包含超过 300 万条结合数据记录，涵盖约 140 万种化合物，针对约 9,200 种蛋白质靶点进行测试，从科学文献和专利文献中精选。BindingDB 存储定量结合测量值（Ki、Kd、IC50、EC50），对于药物发现、药理学和计算化学研究至关重要。

**关键资源：**
- BindingDB 网站：https://www.bindingdb.org/
- REST API：https://www.bindingdb.org/axis2/services/BDBService
- 下载：https://www.bindingdb.org/bind/chemsearch/marvin/Download.jsp
- GitHub：https://github.com/drugilsberg/bindingdb

## 何时使用此技能

在以下情况使用 BindingDB：

- **基于靶点的药物发现**：哪些已知化合物与靶蛋白结合？它们的亲和力如何？
- **SAR 分析**：结构修饰如何影响一系列类似物的结合亲和力？
- **先导化合物谱分析**：化合物与哪些靶点结合（选择性/多药理学）？
- **基准数据集**：获取精选的蛋白质-配体亲和力数据用于 ML 模型训练
- **再利用分析**：已批准药物是否与意外靶点结合？
- **竞争分析**：靶点类别的最佳报告亲和力是什么？
- **片段筛选**：查找针对靶点的片段的验证结合数据

## 核心能力

### 1. BindingDB REST API

基本 URL：`https://www.bindingdb.org/axis2/services/BDBService`

```python
import requests

BASE_URL = "https://www.bindingdb.org/axis2/services/BDBService"

def bindingdb_query(method, params):
    """查询 BindingDB REST API。"""
    url = f"{BASE_URL}/{method}"
    response = requests.get(url, params=params, headers={"Accept": "application/json"})
    response.raise_for_status()
    return response.json()
```

### 2. 按靶点查询（UniProt ID）

```python
def get_ligands_for_target(uniprot_id, affinity_type="Ki", cutoff=10000, unit="nM"):
    """
    获取具有针对 UniProt 靶点的测量亲和力的所有配体。

    参数：
        uniprot_id：UniProt 登录号（例如，ABL1 为 "P00519"）
        affinity_type："Ki"、"Kd"、"IC50"、"EC50"
        cutoff：要返回的最大亲和力值（以 nM 为单位）
        unit："nM" 或 "uM"
    """
    params = {
        "uniprot_id": uniprot_id,
        "affinity_type": affinity_type,
        "affinity_cutoff": cutoff,
        "response": "json"
    }
    return bindingdb_query("getLigandsByUniprotID", params)

# 示例：获取与 ABL1 结合的所有化合物（伊马替尼靶点）
ligands = get_ligands_for_target("P00519", affinity_type="Ki", cutoff=100)
```

### 3. 按化合物名称或 SMILES 查询

```python
def search_by_name(compound_name, limit=100):
    """按名称在 BindingDB 中搜索化合物。"""
    params = {
        "compound_name": compound_name,
        "response": "json",
        "max_results": limit
    }
    return bindingdb_query("getAffinitiesByCompoundName", params)

def search_by_smiles(smiles, similarity=100, limit=50):
    """
    通过 SMILES 字符串搜索 BindingDB。

    参数：
        smiles：化合物的 SMILES 字符串
        similarity：Tanimoto 相似性阈值（1-100，100 = 完全匹配）
    """
    params = {
        "SMILES": smiles,
        "similarity": similarity,
        "response": "json",
        "max_results": limit
    }
    return bindingdb_query("getAffinitiesByBEI", params)

# 示例：搜索伊马替尼结合数据
result = search_by_name("imatinib")
```

### 4. 基于下载的分析（推荐用于大型查询）

对于综合分析，直接下载 BindingDB 数据：

```python
import pandas as pd

def load_bindingdb(filepath="BindingDB_All.tsv"):
    """
    加载 BindingDB TSV 文件。
    从以下地址下载：https://www.bindingdb.org/bind/chemsearch/marvin/Download.jsp
    """
    # 关键列
    usecols = [
        "BindingDB Reactant_set_id",
        "Ligand SMILES",
        "Ligand InChI",
        "Ligand InChI Key",
        "BindingDB Target Chain  Sequence",
        "PDB ID(s) for Ligand-Target Complex",
        "UniProt (SwissProt) Entry Name of Target Chain",
        "UniProt (SwissProt) Primary ID of Target Chain",
        "UniProt (TrEMBL) Primary ID of Target Chain",
        "Ki (nM)",
        "IC50 (nM)",
        "Kd (nM)",
        "EC50 (nM)",
        "kon (M-1-s-1)",
        "koff (s-1)",
        "Target Name",
        "Target Source Organism According to Curator or DataSource",
        "Number of Protein Chains in Target (>1 implies a multichain complex)",
        "PubChem CID",
        "PubChem SID",
        "ChEMBL ID of Ligand",
        "DrugBank ID of Ligand",
    ]

    df = pd.read_csv(filepath, sep="\t", usecols=[c for c in usecols if c],
                     low_memory=False, on_bad_lines='skip')

    # 将亲和力列转换为数值
    for col in ["Ki (nM)", "IC50 (nM)", "Kd (nM)", "EC50 (nM)"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

def query_target_affinity(df, uniprot_id, affinity_types=None, max_nm=10000):
    """查询加载的 BindingDB 以获取特定靶点。"""
    if affinity_types is None:
        affinity_types = ["Ki (nM)", "IC50 (nM)", "Kd (nM)"]

    # 按 UniProt ID 过滤
    mask = df["UniProt (SwissProt) Primary ID of Target Chain"] == uniprot_id
    target_df = df[mask].copy()

    # 按亲和力截止值过滤
    has_affinity = pd.Series(False, index=target_df.index)
    for col in affinity_types:
        if col in target_df.columns:
            has_affinity |= target_df[col] <= max_nm

    result = target_df[has_affinity][["Ligand SMILES"] + affinity_types +
                                      ["PubChem CID", "ChEMBL ID of Ligand"]].dropna(how='all')
    return result.sort_values(affinity_types[0])
```

### 5. SAR 分析

```python
import pandas as pd

def sar_analysis(df, target_uniprot, affinity_col="IC50 (nM)"):
    """
    针对靶点的构效关系分析。
    检索所有具有亲和力数据的化合物并按效力排序。
    """
    target_data = query_target_affinity(df, target_uniprot, [affinity_col])

    if target_data.empty:
        return target_data

    # 添加 pIC50（以摩尔为单位的 IC50 的负对数）
    if affinity_col in target_data.columns:
        target_data = target_data[target_data[affinity_col].notna()].copy()
        target_data["pAffinity"] = -((target_data[affinity_col] * 1e-9).apply(
            lambda x: __import__('math').log10(x)
        ))
        target_data = target_data.sort_values("pAffinity", ascending=False)

    return target_data

# 针对 EGFR (P00533) 的最有效化合物
# sar = sar_analysis(df, "P00533", "IC50 (nM)")
# print(sar.head(20))
```

### 6. 多药理学谱分析

```python
def polypharmacology_profile(df, ligand_smiles_or_name, affinity_cutoff_nM=1000):
    """
    查找化合物结合的所有靶点。
    使用 PubChem CID 或 SMILES 进行匹配。
    """
    # 按配体 SMILES 搜索（完全匹配）
    mask = df["Ligand SMILES"] == ligand_smiles_or_name

    ligand_data = df[mask].copy()

    # 按亲和力过滤
    aff_cols = ["Ki (nM)", "IC50 (nM)", "Kd (nM)"]
    has_aff = pd.Series(False, index=ligand_data.index)
    for col in aff_cols:
        if col in ligand_data.columns:
            has_aff |= ligand_data[col] <= affinity_cutoff_nM

    result = ligand_data[has_aff][
        ["Target Name", "UniProt (SwissProt) Primary ID of Target Chain"] + aff_cols
    ].dropna(how='all')

    return result.sort_values("Ki (nM)")
```

## 查询工作流程

### 工作流程 1：查找靶点的最佳抑制剂

```python
import pandas as pd

def find_best_inhibitors(uniprot_id, affinity_type="IC50 (nM)", top_n=20):
    """在 BindingDB 中查找针对靶点的最有效抑制剂。"""
    df = load_bindingdb("BindingDB_All.tsv")  # 加载一次并重复使用
    result = query_target_affinity(df, uniprot_id, [affinity_type])

    if result.empty:
        print(f"No data found for {uniprot_id}")
        return result

    result = result.sort_values(affinity_type).head(top_n)
    print(f"Top {top_n} inhibitors for {uniprot_id} by {affinity_type}:")
    for _, row in result.iterrows():
        print(f"  {row['PubChem CID']}: {row[affinity_type]:.1f} nM | SMILES: {row['Ligand SMILES'][:40]}...")
    return result
```

### 工作流程 2：选择性谱分析

1. 获取化合物在所有靶点上的所有亲和力数据
2. 比较靶点和脱靶之间的亲和力比率
3. 识别选择性悬崖（改善选择性的结构变化）
4. 与 ChEMBL 交叉引用以获取其他选择性数据

### 工作流程 3：机器学习数据集准备

```python
def prepare_ml_dataset(df, uniprot_ids, affinity_col="IC50 (nM)",
                        max_affinity_nM=100000, min_count=50):
    """准备 BindingDB 数据用于 ML 模型训练。"""
    records = []
    for uid in uniprot_ids:
        target_df = query_target_affinity(df, uid, [affinity_col], max_affinity_nM)
        if len(target_df) >= min_count:
            target_df = target_df.copy()
            target_df["target"] = uid
            records.append(target_df)

    if not records:
        return pd.DataFrame()

    combined = pd.concat(records)
    # 添加 pAffinity（归一化）
    combined["pAffinity"] = -((combined[affinity_col] * 1e-9).apply(
        lambda x: __import__('math').log10(max(x, 1e-12))
    ))
    return combined[["Ligand SMILES", "target", "pAffinity", affinity_col]].dropna()
```

## 关键数据字段

| 字段 | 描述 |
|-------|-------------|
| `Ligand SMILES` | 化合物的 2D 结构 |
| `Ligand InChI Key` | 唯一化学标识符 |
| `Ki (nM)` | 抑制常数（平衡、功能） |
| `Kd (nM)` | 解离常数（热力学、结合） |
| `IC50 (nM)` | 半最大抑制浓度 |
| `EC50 (nM)` | 半最大有效浓度 |
| `kon (M-1-s-1)` | 结合速率常数 |
| `koff (s-1)` | 解离速率常数 |
| `UniProt (SwissProt) Primary ID` | 靶点 UniProt 登录号 |
| `Target Name` | 蛋白质名称 |
| `PDB ID(s) for Ligand-Target Complex` | 晶体结构 |
| `PubChem CID` | PubChem 化合物 ID |
| `ChEMBL ID of Ligand` | ChEMBL 化合物 ID |

## 亲和力解释

| 亲和力 | 分类 | 药物相似性 |
|----------|---------------|---------------|
| < 1 nM | 亚纳摩尔 | 非常有效（皮摩尔范围） |
| 1–10 nM | 纳摩尔 | 有效，已批准药物的典型值 |
| 10–100 nM | 中等 | 常见先导化合物 |
| 100–1000 nM | 弱 | 片段/起点 |
| > 1000 nM | 非常弱 | 通常低于药物相关性阈值 |

## 最佳实践

- **使用 Ki 进行直接结合**：Ki 反映独立于酶机制的真实结合亲和力
- **IC50 上下文依赖性**：IC50 值取决于底物浓度（Cheng-Prusoff 方程）
- **归一化单位**：BindingDB 以 nM 报告；在跨研究比较时验证单位
- **按靶点生物体过滤**：使用 `Target Source Organism` 确保人类蛋白质数据
- **处理缺失值**：并非所有化合物都有所有测量类型
- **与 ChEMBL 交叉引用**：ChEMBL 拥有更多用于药物化学的精选活性数据

## 其他资源

- **BindingDB 网站**：https://www.bindingdb.org/
- **数据下载**：https://www.bindingdb.org/bind/chemsearch/marvin/Download.jsp
- **API 文档**：https://www.bindingdb.org/bind/BindingDBRESTfulAPI.jsp
- **引用**：Gilson MK et al. (2016) Nucleic Acids Research. PMID: 26481362
- **相关资源**：ChEMBL (https://www.ebi.ac.uk/chembl/)、PubChem BioAssay
