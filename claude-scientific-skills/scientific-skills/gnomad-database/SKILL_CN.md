---
name: gnomad-database
description: 查询gnomAD（基因组聚合数据库）获取群体等位基因频率、变体约束评分（pLI、LOEUF）和功能缺失耐受性。用于变体致病性解释、罕见疾病遗传学和识别功能缺失不耐受基因。
license: CC0-1.0
metadata:
    skill-author: Kuan-lin Huang
---

# gnomAD 数据库

## 概述

基因组聚合数据库（gnomAD）是来自大规模测序项目的人类遗传变异的最大公开可用集合。gnomAD v4包含来自730,947个个体的外显子序列和来自76,215个个体的基因组序列，涵盖多样化的祖先。它提供群体等位基因频率、变体后果注释和基因级约束指标，对于解释遗传变异的临床意义至关重要。

**关键资源：**
- gnomAD浏览器：https://gnomad.broadinstitute.org/
- GraphQL API：https://gnomad.broadinstitute.org/api
- 数据下载：https://gnomad.broadinstitute.org/downloads
- 文档：https://gnomad.broadinstitute.org/help

## 何时使用此技能

使用gnomAD当：

- **变体频率查找**：检查变体是罕见、常见还是在一般群体中不存在
- **致病性评估**：罕见变体（MAF < 1%）是疾病致病的候选者；gnomAD帮助过滤良性常见变体
- **功能缺失不耐受性**：使用pLI和LOEUF评分评估基因是否耐受蛋白质截断变体
- **群体分层频率**：跨祖先比较等位基因频率（非洲/非裔美国人、混合美洲人、阿什肯纳兹犹太人、东亚人、芬兰人、中东人、非芬兰欧洲人、南亚人）
- **ClinVar/ACMG变体分类**：gnomAD频率数据输入BA1/BS1证据代码用于变体分类
- **约束分析**：识别缺失错义或功能缺失变异的基因（z评分、pLI、LOEUF）

## 核心功能

### 1. gnomAD GraphQL API

gnomAD使用位于`https://gnomad.broadinstitute.org/api`的GraphQL API。大多数查询通过基因或特定基因组位置获取变体。

**可用数据集：**
- `gnomad_r4` — gnomAD v4外显子（推荐默认，GRCh38）
- `gnomad_r4_genomes` — gnomAD v4基因组（GRCh38）
- `gnomad_r3` — gnomAD v3基因组（GRCh38）
- `gnomad_r2_1` — gnomAD v2外显子（GRCh37）

**参考基因组：**
- `GRCh38` — v3/v4的默认
- `GRCh37` — 用于v2

### 2. 按基因查询变体

```python
import requests

def query_gnomad_gene(gene_symbol, dataset="gnomad_r4", reference_genome="GRCh38"):
    """从gnomAD获取基因中的变体。"""
    url = "https://gnomad.broadinstitute.org/api"

    query = """
    query GeneVariants($gene_symbol: String!, $dataset: DatasetId!, $reference_genome: ReferenceGenomeId!) {
      gene(gene_symbol: $gene_symbol, reference_genome: $reference_genome) {
        gene_id
        gene_symbol
        variants(dataset: $dataset) {
          variant_id
          pos
          ref
          alt
          consequence
          genome {
            af
            ac
            an
            ac_hom
            populations {
              id
              ac
              an
              af
            }
          }
          exome {
            af
            ac
            an
            ac_hom
          }
          lof
          lof_flags
          lof_filter
        }
      }
    }
    """

    variables = {
        "gene_symbol": gene_symbol,
        "dataset": dataset,
        "reference_genome": reference_genome
    }

    response = requests.post(url, json={"query": query, "variables": variables})
    return response.json()

# 示例
result = query_gnomad_gene("BRCA1")
gene_data = result["data"]["gene"]
variants = gene_data["variants"]

# 过滤到罕见PTV
rare_ptvs = [
    v for v in variants
    if v.get("lof") == "LC" or v.get("consequence") in ["stop_gained", "frameshift_variant"]
    and v.get("genome", {}).get("af", 1) < 0.001
]
print(f"在{gene_data['gene_symbol']}中找到{len(rare_ptvs)}个罕见PTV")
```

### 3. 查询特定变体

```python
import requests

def query_gnomad_variant(variant_id, dataset="gnomad_r4"):
    """获取特定变体（例如'1-55516888-G-GA'）的详情。"""
    url = "https://gnomad.broadinstitute.org/api"

    query = """
    query VariantDetails($variantId: String!, $dataset: DatasetId!) {
      variant(variantId: $variantId, dataset: $dataset) {
        variant_id
        chrom
        pos
        ref
        alt
        genome {
          af
          ac
          an
          ac_hom
          populations {
            id
            ac
            an
            af
          }
        }
        exome {
          af
          ac
          an
          ac_hom
          populations {
            id
            ac
            an
            af
          }
        }
        consequence
        lof
        rsids
        in_silico_predictors {
          id
          value
          flags
        }
        clinvar_variation_id
      }
    }
    """

    response = requests.post(
        url,
        json={"query": query, "variables": {"variantId": variant_id, "dataset": dataset}}
    )
    return response.json()

# 示例：查询特定变体
result = query_gnomad_variant("17-43094692-G-A")  # BRCA1错义
variant = result["data"]["variant"]

if variant:
    genome_af = variant.get("genome", {}).get("af", "N/A")
    exome_af = variant.get("exome", {}).get("af", "N/A")
    print(f"变体：{variant['variant_id']}")
    print(f"  后果：{variant['consequence']}")
    print(f"  基因组AF：{genome_af}")
    print(f"  外显子AF：{exome_af}")
    print(f"  LoF：{variant.get('lof')}")
```

### 4. 基因约束评分

gnomAD约束评分评估基因相对于预期对变异的耐受程度：

```python
import requests

def query_gnomad_constraint(gene_symbol, reference_genome="GRCh38"):
    """获取基因的约束评分。"""
    url = "https://gnomad.broadinstitute.org/api"

    query = """
    query GeneConstraint($gene_symbol: String!, $reference_genome: ReferenceGenomeId!) {
      gene(gene_symbol: $gene_symbol, reference_genome: $reference_genome) {
        gene_id
        gene_symbol
        gnomad_constraint {
          exp_lof
          exp_mis
          exp_syn
          obs_lof
          obs_mis
          obs_syn
          oe_lof
          oe_mis
          oe_syn
          oe_lof_lower
          oe_lof_upper
          lof_z
          mis_z
          syn_z
          pLI
        }
      }
    }
    """

    response = requests.post(
        url,
        json={"query": query, "variables": {"gene_symbol": gene_symbol, "reference_genome": reference_genome}}
    )
    return response.json()

# 示例
result = query_gnomad_constraint("KCNQ2")
gene = result["data"]["gene"]
constraint = gene["gnomad_constraint"]

print(f"基因：{gene['gene_symbol']}")
print(f"  pLI：   {constraint['pLI']:.3f}  (>0.9 = LoF不耐受）")
print(f"  LOEUF： {constraint['oe_lof_upper']:.3f}  (<0.35 = 高度约束）")
print(f"  Obs/Exp LoF：{constraint['oe_lof']:.3f}")
print(f"  错义Z：  {constraint['mis_z']:.3f}")
```

**约束评分解释：**
| 评分 | 范围 | 含义 |
|-------|-------|---------|
| `pLI` | 0–1 | LoF不耐受概率；>0.9 = 高度不耐受 |
| `LOEUF` | 0–∞ | LoF观察/期望上限；<0.35 = 约束 |
| `oe_lof` | 0–∞ | LoF变体的观察/期望比率 |
| `mis_z` | −∞ 到 ∞ | 错义约束z评分；>3.09 = 约束 |
| `syn_z` | −∞ 到 ∞ | 同义z评分（对照；应接近0） |

### 5. 群体频率分析

```python
import requests
import pandas as pd

def get_population_frequencies(variant_id, dataset="gnomad_r4"):
    """提取变体的每个群体等位基因频率。"""
    url = "https://gnomad.broadinstitute.org/api"

    query = """
    query PopFreqs($variantId: String!, $dataset: DatasetId!) {
      variant(variantId: $variantId, dataset: $dataset) {
        variant_id
        genome {
          populations {
            id
            ac
            an
            af
            ac_hom
          }
        }
      }
    }
    """

    response = requests.post(
        url,
        json={"query": query, "variables": {"variantId": variant_id, "dataset": dataset}}
    )
    data = response.json()
    populations = data["data"]["variant"]["genome"]["populations"]

    df = pd.DataFrame(populations)
    df = df[df["an"] > 0].copy()
    df["af"] = df["ac"] / df["an"]
    df = df.sort_values("af", ascending=False)
    return df

# gnomAD v4中的群体ID：
# afr = 非洲/非裔美国人
# ami = 阿米什人
# amr = 混合美洲人
# asj = 阿什肯纳兹犹太人
# eas = 东亚人
# fin = 芬兰人
# mid = 中东人
# nfe = 非芬兰欧洲人
# sas = 南亚人
# remaining = 其他
```

### 6. 结构变体（gnomAD-SV）

gnomAD还包含结构变体数据集：

```python
import requests

def query_gnomad_sv(gene_symbol):
    """查询与基因重叠的结构变体。"""
    url = "https://gnomad.broadinstitute.org/api"

    query = """
    query SVsByGene($gene_symbol: String!) {
      gene(gene_symbol: $gene_symbol, reference_genome: GRCh38) {
        structural_variants {
          variant_id
          type
          chrom
          pos
          end
          af
          ac
          an
        }
      }
    }
    """

    response = requests.post(url, json={"query": query, "variables": {"gene_symbol": gene_symbol}})
    return response.json()
```

## 查询工作流

### 工作流1：变体致病性评估

1. **检查群体频率** — 变体是否足够罕见以致可能是致病性的？
   - 对隐性使用gnomAD AF < 1%，对显性条件使用< 0.1%
   - 检查祖先特异性频率（在一个群体中罕见的变体可能在另一个群体中常见）

2. **评估功能影响** — LoF变体具有最高的先验概率
   - 检查`lof`字段：`HC` = 高置信度LoF，`LC` = 低置信度
   - 检查`lof_flags`是否存在"NAGNAG_SITE"、"PHYLOCSF_WEAK"等问题

3. **应用ACMG标准：**
   - BA1：AF > 5% → 良性独立证据
   - BS1：AF > 疾病患病率阈值 → 良性支持证据
   - PM2：在gnomAD中不存在或非常罕见 → 致病性中度证据

### 工作流2：罕见疾病中的基因优先级排序

1. 查询候选基因的约束评分
2. 过滤pLI > 0.9（单倍体剂量不足）或LOEUF < 0.35的基因
3. 与基因中观察到的LoF变体交叉引用
4. 与ClinVar和疾病数据库集成

### 工作流3：群体遗传学研究

1. 从GWAS或临床数据识别感兴趣的变体
2. 查询每个群体的频率
3. 跨祖先比较频率差异
4. 测试特定始祖群体中的富集

## 最佳实践

- **使用gnomAD v4（gnomad_r4）**获取最新数据；仅当GRCh37兼容性需要时使用v2（gnomad_r2_1）
- **处理空响应**：在gnomAD中未观察到的变体不一定是致病性的——不存在是有信息的
- **区分外显子与基因组数据**：基因组数据具有更均匀的覆盖；外显子数据更大但可能有覆盖缺口
- **限制GraphQL查询**：在请求之间添加延迟；尽可能批量查询
- **纯合子计数**（`ac_hom`）与隐性疾病分析相关
- **LOEUF优于pLI**用于基因约束（对样本量不太敏感）

## 数据访问

- **浏览器**：https://gnomad.broadinstitute.org/ — 交互式变体和基因浏览
- **GraphQL API**：https://gnomad.broadinstitute.org/api — 程序化访问
- **下载**：https://gnomad.broadinstitute.org/downloads — VCF、Hail表、约束表
- **Google Cloud**：gs://gcp-public-data--gnomad/

## 其他资源

- **gnomAD网站**：https://gnomad.broadinstitute.org/
- **gnomAD博客**：https://gnomad.broadinstitute.org/news
- **下载**：https://gnomad.broadinstitute.org/downloads
- **API资源管理器**：https://gnomad.broadinstitute.org/api（交互式GraphiQL）
- **约束文档**：https://gnomad.broadinstitute.org/help/constraint
- **引用**：Karczewski KJ et al. (2020) Nature. PMID: 32461654; Chen S et al. (2024) Nature. PMID: 38conservation
- **GitHub**：https://github.com/broadinstitute/gnomad-browser
