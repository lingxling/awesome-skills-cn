---
name: glycoengineering
description: 分析和工程化蛋白质糖基化。扫描序列中的N-糖基化序列子（N-X-S/T）、预测O-糖基化热点，并访问精选的糖基化工程工具（NetOGlyc、GlycoShield、GlycoWorkbench）。用于糖蛋白工程、治疗性抗体优化和疫苗设计。
license: Unknown
metadata:
    skill-author: Kuan-lin Huang
---

# 糖基化工程

## 概述

糖基化是蛋白质最常见和最复杂的翻译后修饰（PTM），影响超过50%的所有人类蛋白质。糖链调节蛋白质折叠、稳定性、免疫识别、受体相互作用和治疗性蛋白质的药代动力学。糖基化工程涉及对糖基化模式进行合理修饰，以提高治疗功效、稳定性或免疫逃逸。

**两种主要糖基化类型：**
- **N-糖基化**：附着于序列子N-X-[S/T]中的天冬酰胺（N），其中X ≠ 脯氨酸；发生在内质网/高尔基体中
- **O-糖基化**：附着于丝氨酸（S）或苏氨酸（T）；无严格共识基序；主要是GalNAc起始

## 何时使用此技能

使用此技能当：

- **抗体工程**：优化Fc糖基化以增强ADCC、CDC或降低免疫原性
- **治疗性蛋白质设计**：识别影响半衰期、稳定性或免疫原性的糖基化位点
- **疫苗抗原设计**：工程化糖链屏蔽以将免疫反应集中在保守表位上
- **生物类似药表征**：比较参考药和生物类似药之间的糖链模式
- **药物靶点分析**：糖基化是否影响受体的靶点参与？
- **蛋白质稳定性**：N-糖链通常稳定蛋白质；识别稳定化突变的位点

## N-糖基化序列子分析

### 扫描N-糖基化位点

N-糖基化发生在序列子**N-X-[S/T]**，其中X ≠ 脯氨酸。

```python
import re
from typing import List, Tuple

def find_n_glycosylation_sequons(sequence: str) -> List[dict]:
    """
    扫描蛋白质序列以查找规范N连接糖基化序列子。
    基序：N-X-[S/T]，其中X ≠ 脯氨酸。

    参数:
        sequence: 单字母氨基酸序列

    返回:
        包含位置（1-based）、基序和上下文的字典列表
    """
    seq = sequence.upper()
    results = []
    i = 0
    while i <= len(seq) - 3:
        triplet = seq[i:i+3]
        if triplet[0] == 'N' and triplet[1] != 'P' and triplet[2] in {'S', 'T'}:
            context = seq[max(0, i-3):i+6]  # ±3残基上下文
            results.append({
                'position': i + 1,   # 1-based
                'motif': triplet,
                'context': context,
                'sequon_type': 'NXS' if triplet[2] == 'S' else 'NXT'
            })
            i += 3
        else:
            i += 1
    return results

def summarize_glycosylation_sites(sequence: str, protein_name: str = "") -> str:
    """生成N-糖基化位点的研究日志摘要。"""
    sequons = find_n_glycosylation_sequons(sequence)

    lines = [f"# N-糖基化序列子分析：{protein_name or '蛋白质'}"]
    lines.append(f"序列长度：{len(sequence)}")
    lines.append(f"总N-糖基化序列子：{len(sequons)}")

    if sequons:
        lines.append(f"\nN-X-S位点：{sum(1 for s in sequons if s['sequon_type'] == 'NXS')}")
        lines.append(f"N-X-T位点：{sum(1 for s in sequons if s['sequon_type'] == 'NXT')}")
        lines.append(f"\n位点详情：")
        for s in sequons:
            lines.append(f"  位置 {s['position']}：{s['motif']}（上下文：...{s['context']}...）")
    else:
        lines.append("未检测到规范N-糖基化序列子。")

    return "\n".join(lines)

# 示例：IgG1 Fc区域
fc_sequence = "APELLGGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSHEDPEVKFNWYVDGVEVHNAKTKPREEQYNSTYRVVSVLTVLHQDWLNGKEYKCKVSNKALPAPIEKTISKAKGQPREPQVYTLPPSREEMTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPVLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK"
print(summarize_glycosylation_sites(fc_sequence, "IgG1 Fc"))
```

### 突变N-糖基化位点

```python
def eliminate_glycosite(sequence: str, position: int, replacement: str = "Q") -> str:
    """
    通过将天冬酰胺突变为谷氨酰胺（保守）来消除N-糖基化位点。

    参数:
        sequence: 蛋白质序列
        position: 要突变的天冬酰胺的1-based位置
        replacement: 要替换的氨基酸（默认Q = 谷氨酰胺；大小相似，不被糖基化）

    返回:
        突变后的序列
    """
    seq = list(sequence.upper())
    idx = position - 1
    assert seq[idx] == 'N', f"位置{position}是'{seq[idx]}'，不是'N'"
    seq[idx] = replacement.upper()
    return ''.join(seq)

def add_glycosite(sequence: str, position: int, flanking_context: str = "S") -> str:
    """
    通过将残基突变为天冬酰胺来引入N-糖基化位点，
    并确保X ≠ 脯氨酸且+2 = S/T。

    参数:
        position: 要引入天冬酰胺的1-based位置
        flanking_context: 位置+2处的'S'或'T'（如果需要修改）
    """
    seq = list(sequence.upper())
    idx = position - 1

    # 突变为天冬酰胺
    seq[idx] = 'N'

    # 确保X+1 != 脯氨酸（如果需要则突变为丙氨酸）
    if idx + 1 < len(seq) and seq[idx + 1] == 'P':
        seq[idx + 1] = 'A'

    # 确保X+2 = S或T
    if idx + 2 < len(seq) and seq[idx + 2] not in ('S', 'T'):
        seq[idx + 2] = flanking_context

    return ''.join(seq)
```

## O-糖基化分析

### 启发式O-糖基化热点预测

```python
def predict_o_glycosylation_hotspots(
    sequence: str,
    window: int = 7,
    min_st_fraction: float = 0.4,
    disallow_proline_next: bool = True
) -> List[dict]:
    """
    基于局部S/T密度的启发式O-糖基化热点评分。
    不能替代NetOGlyc；用作快速基线。

    规则:
    - O-GalNAc糖基化聚集在富含S/T的片段上
    - 标记S/T残基在富含S/T的窗口中
    - 避免S/T紧随脯氨酸（TP/SP基序抑制GalNAc-T）

    参数:
        window: 局部S/T密度的奇数窗口大小
        min_st_fraction: 标记位点的窗口中S/T的最小分数
    """
    if window % 2 == 0:
        window = 7
    seq = sequence.upper()
    half = window // 2
    candidates = []

    for i, aa in enumerate(seq):
        if aa not in ('S', 'T'):
            continue
        if disallow_proline_next and i + 1 < len(seq) and seq[i+1] == 'P':
            continue

        start = max(0, i - half)
        end = min(len(seq), i + half + 1)
        segment = seq[start:end]
        st_count = sum(1 for c in segment if c in ('S', 'T'))
        frac = st_count / len(segment)

        if frac >= min_st_fraction:
            candidates.append({
                'position': i + 1,
                'residue': aa,
                'st_fraction': round(frac, 3),
                'window': f"{start+1}-{end}",
                'segment': segment
            })

    return candidates
```

## 外部糖基化工程工具

### 1. NetOGlyc 4.0（O-糖基化预测）

用于高精度O-GalNAc位点预测的Web服务：
- **URL**：https://services.healthtech.dtu.dk/services/NetOGlyc-4.0/
- **输入**：FASTA蛋白质序列
- **输出**：每个残基的O-糖基化概率评分
- **方法**：在实验验证的O-GalNAc位点上训练的神经网络

```python
import requests

def submit_netoglycv4(fasta_sequence: str) -> str:
    """
    将序列提交到NetOGlyc 4.0 Web服务。
    返回结果检索的作业URL。

    注意：这使用DTU Health Tech Web服务。结果需要~1-5分钟。
    """
    url = "https://services.healthtech.dtu.dk/cgi-bin/webface2.cgi"
    # NetOGlyc提交（参数可能随Web服务版本变化）
    # 建议大多数用例直接使用Web界面
    print("在以下位置提交序列：https://services.healthtech.dtu.dk/services/NetOGlyc-4.0/")
    return url

# 还有：NetNGlyc用于N-糖基化预测
# URL: https://services.healthtech.dtu.dk/services/NetNGlyc-1.0/
```

### 2. GlycoShield-MD（糖链屏蔽分析）

GlycoShield-MD在MD模拟期间分析糖链如何屏蔽蛋白质表面：
- **URL**：https://gitlab.mpcdf.mpg.de/dioscuri-biophysics/glycoshield-md/
- **用途**：在MD轨迹上映射糖链屏蔽
- **输出**：每个残基的屏蔽分数、可视化

```bash
# 安装
pip install glycoshield

# 基本用法：分析糖基化蛋白质MD轨迹的糖链屏蔽
glycoshield \
    --topology glycoprotein.pdb \
    --trajectory glycoprotein.xtc \
    --glycan_resnames BGLCNA FUC \
    --output shielding_analysis/
```

### 3. GlycoWorkbench（糖链结构绘制/分析）

- **URL**：https://www.eurocarbdb.org/project/glycoworkbench
- **用途**：绘制糖链结构、计算质量、注释MS谱
- **格式**：GlycoCT、IUPAC浓缩糖链表示法

### 4. GlyConnect（糖链-蛋白质数据库）

- **URL**：https://glyconnect.expasy.org/
- **用途**：查找实验验证的糖蛋白和糖基化位点
- **查询**：按蛋白质（UniProt ID）、糖链结构或组织

```python
import requests

def query_glyconnect(uniprot_id: str) -> dict:
    """查询蛋白质的糖基化数据。"""
    url = f"https://glyconnect.expasy.org/api/proteins/uniprot/{uniprot_id}"
    response = requests.get(url, headers={"Accept": "application/json"})
    if response.status_code == 200:
        return response.json()
    return {}

# 示例：查询EGFR糖基化
egfr_glyco = query_glyconnect("P00533")
```

### 5. UniCarbKB（糖链结构数据库）

- **URL**：https://unicarbkb.org/
- **用途**：浏览糖链结构、按质量或组成搜索
- **格式**：GlycoCT或IUPAC表示法

## 关键糖基化工程策略

### 用于治疗性抗体

| 目标 | 策略 | 注意 |
|------|----------|-------|
| 增强ADCC | 去岩藻糖化于Fc Asn297 | 去岩藻糖基化IgG1的FcγRIIIa结合力提高约50倍 |
| 降低免疫原性 | 去除非人类糖链 | 消除α-Gal、NGNA表位 |
| 改善PK半衰期 | 唾酸化 | 唾酸化糖链延长半衰期 |
| 减少炎症 | 超唾液酸化 | IVIG抗炎机制 |
| 创建糖链屏蔽 | 添加N-糖基化位点到表面 | 屏蔽脆弱表位（疫苗设计） |

### 常用突变

| 突变 | 效应 |
|----------|--------|
| N297A/Q（IgG1） | 移除Fc糖基化（无糖） |
| N297D（IgG1） | 移除Fc糖基化 |
| S298A/E333A/K334A | 增加FcγRIIIa结合 |
| F243L（IgG1） | 增加去岩藻糖化 |
| T299A | 移除Fc糖基化 |

## 糖链表示法

### IUPAC 浓缩表示法（单糖缩写）

| 符号 | 全名 | 类型 |
|--------|-----------|------|
| Glc | 葡萄糖 | 己糖 |
| GlcNAc | N-乙酰葡萄糖 | 己糖胺 |
| Man | 甘露糖 | 己糖 |
| Gal | 半乳糖 | 己糖 |
| Fuc | 岩藻糖 | 脱氧己糖 |
| Neu5Ac | N-乙酰神经氨酸（唾液酸） | 唾液酸 |
| GalNAc | N-乙酰半乳糖胺 | 己糖胺 |

### 复杂N-糖链结构

```
典型复杂双天线N-糖链：
Neu5Ac-Gal-GlcNAc-Man\
                       Man-GlcNAc-GlcNAc-[Asn]
Neu5Ac-Gal-GlcNAc-Man/
（±核心岩藻糖在最内层GlcNAc上）
```

## 最佳实践

- **从NetNGlyc/NetOGlyc开始**，在实验验证之前进行计算预测
- **用质谱验证**：糖蛋白质组学（Byonic、Mascot）用于位点特异性糖链谱分析
- **考虑位点上下文**：并非所有预测的序列子实际上都被糖基化（可及性、细胞类型、蛋白质构象）
- **对于抗体**：Fc N297糖链至关重要——始终首先表征此位点
- **使用GlyConnect**检查感兴趣的蛋白质是否具有实验验证的糖基化数据

## 其他资源

- **GlyTouCan**（糖链结构存储库）：https://glytoucan.org/
- **GlyConnect**：https://glyconnect.expasy.org/
- **CFG功能糖组学**：http://www.functionalglycomics.org/
- **DTU Health Tech服务器**（NetNGlyc、NetOGlyc）：https://services.healthtech.dtu.dk/
- **GlycoWorkbench**：https://glycoworkbench.software.informer.com/
- **综述**：Apweiler R et al. (1999) Biochim Biophys Acta. PMID: 10564035
- **治疗性糖基化工程综述**：Jefferis R (2009) Nature Reviews Drug Discovery. PMID: 19448661
