---
name: jaspar-database
description: 查询JASPAR以获取转录因子结合位点（TFBS）配置文件（PWMs/PFMs）。按TF名称、物种或类别搜索；扫描DNA序列以查找TF结合位点；比较矩阵；对于调节基因组学、基序分析和GWAS调节变异解释至关重要。
license: CC0-1.0
metadata:
    skill-author: Kuan-lin Huang
---

# JASPAR数据库

## 概述

JASPAR（https://jaspar.elixir.no/）是策划的、非冗余转录因子（TF）结合配置文件的黄金标准开放访问数据库，存储为位置频率矩阵（PFM）。JASPAR 2024包含164个真核生物的1,210个非冗余TF结合配置文件。每个配置文件都是实验衍生（ChIP-seq、SELEX、HT-SELEX、蛋白质结合微阵列等）并经过严格验证。

**关键资源：**
- JASPAR门户：https://jaspar.elixir.no/
- REST API：https://jaspar.elixir.no/api/v1/
- API文档：https://jaspar.elixir.no/api/v1/docs/
- Python软件包：`jaspar`（通过Biopython）或直接API

## 何时使用此技能

在以下情况下使用JASPAR：

- **TF结合位点预测**：扫描DNA序列以查找TF的潜在结合位点
- **调节变异解释**：GWAS/eQTL变异是否破坏TF结合基序？
- **启动子/增强子分析**：哪些TF预计与调节元件结合？
- **基因调控网络构建**：通过基序扫描将TF与其靶基因连接
- **TF家族分析**：跨TF家族比较结合配置文件（例如，所有同源盒因子）
- **ChIP-seq分析**：在ChIP-seq峰中查找已知TF基序的富集
- **ENCODE/ATAC-seq解释**：将开放染色质区域与TF结合配置文件匹配

## 核心功能

### 1. JASPAR REST API

基础URL：`https://jaspar.elixir.no/api/v1/`

```python
import requests

BASE_URL = "https://jaspar.elixir.no/api/v1"

def jaspar_get(endpoint, params=None):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, params=params, headers={"Accept": "application/json"})
    response.raise_for_status()
    return response.json()
```

### 2. 搜索TF配置文件

```python
def search_jaspar(
    tf_name=None,
    species=None,
    collection="CORE",
    tf_class=None,
    tf_family=None,
    page=1,
    page_size=25
):
    """搜索JASPAR以查找TF结合配置文件。"""
    params = {
        "collection": collection,
        "page": page,
        "page_size": page_size,
        "format": "json"
    }
    if tf_name:
        params["name"] = tf_name
    if species:
        params["species"] = species  # 使用分类学ID或名称，例如，"9606"表示人类
    if tf_class:
        params["tf_class"] = tf_class
    if tf_family:
        params["tf_family"] = tf_family

    return jaspar_get("matrix", params)
# 示例：
# 搜索人类CTCF配置文件
ctcf = search_jaspar("CTCF", species="9606")
print(f"找到{ctcf['count']}个CTCF配置文件")

# 搜索人类中的所有同源盒TF
hox_tfs = search_jaspar(tf_class="Homeodomain", species="9606")

# 搜索TF家族
nfkb = search_jaspar(tf_family="NF-kappaB")
```

### 3. 获取特定矩阵（PFM/PWM）

```python
def get_matrix(matrix_id):
    """按ID（例如，'MA0139.1'表示CTCF）获取特定JASPAR矩阵。"""
    return jaspar_get(f"matrix/{matrix_id}/")

# 示例：获取CTCF矩阵
ctcf_matrix = get_matrix("MA0139.1")

# 矩阵结构：
# {
#   "matrix_id": "MA0139.1",
#   "name": "CTCF",
#   "collection": "CORE",
#   "tax_group": "vertebrates",
#   "pfm": { "A": [...], "C": [...], "G": [...], "T": [...] },
#   "consensus": "CCGCGNGGNGGCAG",
#   "length": 19,
#   "species": [{"tax_id": 9606, "name": "Homo sapiens"}],
#   "class": ["C2H2 zinc finger factors"],
#   "family": ["BEN domain factors"],
#   "type": "ChIP-seq",
#   "uniprot_ids": ["P49711"]
# }
```

### 4. 将PFM/PWM下载为矩阵

```python
import numpy as np

def get_pwm(matrix_id, pseudocount=0.8):
    """
    从JASPAR获取PFM并转换为PWM（log-odds）。
    返回形状为(4, L)的numpy数组，顺序为A、C、G、T。
    """
    matrix = get_matrix(matrix_id)
    pfm = matrix["pfm"]

    # 将PFM转换为numpy
    pfm_array = np.array([pfm["A"], pfm["C"], pfm["G"], pfm["T"]], dtype=float)

    # 添加伪计数
    pfm_array += pseudocount

    # 归一化以获取PPM
    ppm = pfm_array / pfm_array.sum(axis=0, keepdims=True)

    # 转换为PWM（相对于背景0.25的log-odds）
    background = 0.25
    pwm = np.log2(ppm / background)

    return pwm, matrix["name"]

# 示例
pwm, name = get_pwm("MA0139.1")  # CTCF
print(f"{name}的PWM：形状{pwm.shape}")
max_score = pwm.max(axis=0).sum()
print(f"最大可能分数：{max_score:.2f}位")
```

### 5. 扫描DNA序列以查找TF结合位点

```python
import numpy as np
from typing import List, Tuple

NUCLEOTIDE_MAP = {'A': 0, 'C': 1, 'G': 2, 'T': 3,
                  'a': 0, 'c': 1, 'g': 2, 't': 3}

def scan_sequence(sequence: str, pwm: np.ndarray, threshold_pct: float = 0.8) -> List[dict]:
    """
    使用PWM扫描DNA序列以查找TF结合位点。

    参数：
        sequence: DNA序列字符串
        pwm: PWM数组（4 x L），ACGT顺序
        threshold_pct: 最大分数的分数用作阈值（0-1）

    返回：
        带有位置、分数和匹配序列的命中列表
    """
    motif_len = pwm.shape[1]
    max_score = pwm.max(axis=0).sum()
    min_score = pwm.min(axis=0).sum()
    threshold = min_score + threshold_pct * (max_score - min_score)

    hits = []
    seq = sequence.upper()

    for i in range(len(seq) - motif_len + 1):
        subseq = seq[i:i + motif_len]
        # 如果包含非ACGT则跳过
        if any(c not in NUCLEOTIDE_MAP for c in subseq):
            continue

        score = sum(pwm[NUCLEOTIDE_MAP[c], j] for j, c in enumerate(subseq))

        if score >= threshold:
            relative_score = (score - min_score) / (max_score - min_score)
            hits.append({
                "position": i + 1,  # 1-based
                "score": score,
                "relative_score": relative_score,
                "sequence": subseq,
                "strand": "+"
            })

    return hits

# 示例：扫描启动子序列以查找CTCF结合位点
promoter = "AGCCCGCGAGGNGGCAGTTGCCTGGAGCAGGATCAGCAGATC"
pwm, name = get_pwm("MA0139.1")
hits = scan_sequence(promoter, pwm, threshold_pct=0.75)
for hit in hits:
    print(f"  位置{hit['position']}：{hit['sequence']}（分数：{hit['score']:.2f}，{hit['relative_score']:.0%}）")
```

### 6. 扫描两条链

```python
def reverse_complement(seq: str) -> str:
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'N': 'N'}
    return ''.join(complement.get(b, 'N') for b in reversed(seq.upper()))

def scan_both_strands(sequence: str, pwm: np.ndarray, threshold_pct: float = 0.8):
    """扫描正向和反向互补链。"""
    fwd_hits = scan_sequence(sequence, pwm, threshold_pct)
    for h in fwd_hits:
        h["strand"] = "+"

    rev_seq = reverse_complement(sequence)
    rev_hits = scan_sequence(rev_seq, pwm, threshold_pct)
    seq_len = len(sequence)
    for h in rev_hits:
        h["strand"] = "-"
        h["position"] = seq_len - h["position"] - len(h["sequence"]) + 2  # 转换为正向坐标

    all_hits = fwd_hits + rev_hits
    return sorted(all_hits, key=lambda x: x["position"])
```

### 7. 变异对TF结合的影响

```python
def variant_tfbs_impact(ref_seq: str, alt_seq: str, pwm: np.ndarray,
                          tf_name: str, threshold_pct: float = 0.7):
    """
    通过比较ref与alt序列来评估SNP对TF结合的影响。
    两个序列应以变异为中心并带有侧翼上下文。
    """
    ref_hits = scan_both_strands(ref_seq, pwm, threshold_pct)
    alt_hits = scan_both_strands(alt_seq, pwm, threshold_pct)

    max_ref = max((h["score"] for h in ref_hits), default=None)
    max_alt = max((h["score"] for h in alt_hits), default=None)

    result = {
        "tf": tf_name,
        "ref_max_score": max_ref,
        "alt_max_score": max_alt,
        "ref_has_site": len(ref_hits) > 0,
        "alt_has_site": len(alt_hits) > 0,
    }
    if max_ref and max_alt:
        result["score_change"] = max_alt - max_ref
        result["effect"] = "gained" if max_alt > max_ref else "disrupted"
    elif max_ref and not max_alt:
        result["effect"] = "disrupted"
    elif not max_ref and max_alt:
        result["effect"] = "gained"
    else:
        result["effect"] = "no_site"

    return result
```

## 查询工作流程

### 工作流程1：查找启动子中的所有TF结合位点

```python
import requests, numpy as np

# 1. 获取相关TF矩阵（例如，CORE集合中的所有人类TF）
response = requests.get(
    "https://jaspar.elixir.no/api/v1/matrix/",
    params={"species": "9606", "collection": "CORE", "page_size": 500, "page": 1}
)
matrices = response.json()["results"]

# 2. 对于每个矩阵，计算PWM并扫描启动子
promoter = "CCCGCCCGCCCGCCGCCCGCAGTTAATGAGCCCAGCGTGCC"  # 示例

all_hits = []
for m in matrices[:10]:  # 限制用于演示
    pwm_data = requests.get(f"https://jaspar.elixir.no/api/v1/matrix/{m['matrix_id']}/").json()
    pfm = pwm_data["pfm"]
    pfm_arr = np.array([pfm["A"], pfm["C"], pfm["G"], pfm["T"]], dtype=float) + 0.8
    ppm = pfm_arr / pfm_arr.sum(axis=0)
    pwm = np.log2(ppm / 0.25)

    hits = scan_sequence(promoter, pwm, threshold_pct=0.8)
    for h in hits:
        h["tf_name"] = m["name"]
        h["matrix_id"] = m["matrix_id"]
    all_hits.extend(hits)

print(f"找到{len(all_hits)}个TF结合位点")
for h in sorted(all_hits, key=lambda x: -x["score"])[:5]:
    print(f"  {h['tf_name']}（{h['matrix_id']}）：位置{h['position']}，分数{h['score']:.2f}")
```

### 工作流程2：SNP对TF结合的影响（调节变异分析）

1. 检索侧翼SNP的基因组序列（每侧±20 bp）
2. 构建ref和alt序列
3. 使用所有相关TF PWM扫描
4. 报告其结合被SNP创建或破坏的TF

### 工作流程3：基序富集分析

1. 识别一组峰序列（例如，来自ChIP-seq或ATAC-seq）
2. 使用JASPAR PWM扫描所有峰
3. 比较峰与背景序列中的命中率
4. 报告显著富集的基序（Fisher精确检验或FIMO风格评分）

## 可用集合

| 集合 | 描述 | 配置文件 |
|------------|-------------|----------|
| `CORE` | 非冗余、高质量配置文件 | ~1,210 |
| `UNVALIDATED` | 实验衍生但未验证 | ~500 |
| `PHYLOFACTS` | 系统发育保守位点 | ~50 |
| `CNE` | 保守非编码元件 | ~30 |
| `POLII` | RNA Pol II结合配置文件 | ~20 |
| `FAM` | TF家族代表性配置文件 | ~170 |
| `SPLICE` | 剪接因子配置文件 | ~20 |

## 最佳实践

- **使用CORE集合**进行大多数分析 — 最佳验证和非冗余
- **阈值选择**：80%的最大分数是de novo预测的常见值；90%用于高置信度
- **始终扫描两条链** — TF可以任一方向结合
- **为变异分析提供侧翼上下文**：每侧至少（motif_length - 1）bp
- **考虑背景**：PWM分数相对于均匀（0.25）背景；针对实际GC含量调整
- **与ChIP-seq数据交叉验证**（如可用）— 基序扫描有许多假阳性
- **使用Biopython的motifs模块**进行全功能扫描：`from Bio import motifs`

## 其他资源

- **JASPAR门户**：https://jaspar.elixir.no/
- **API文档**：https://jaspar.elixir.no/api/v1/docs/
- **JASPAR 2024论文**：Castro-Mondragon et al. (2022) Nucleic Acids Research. PMID: 34875674
- **Biopython motifs**：https://biopython.org/docs/latest/Tutorial/chapter_motifs.html
- **FIMO工具**（用于大规模扫描）：https://meme-suite.org/meme/tools/fimo
- **HOMER**（基序富集）：http://homer.ucsd.edu/homer/
- **GitHub**：https://github.com/wassermanlab/JASPAR-UCSC-tracks
