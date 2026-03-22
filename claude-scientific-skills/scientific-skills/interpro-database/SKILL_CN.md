---
name: interpro-database
description: 查询InterPro以获取蛋白质家族、域和功能位点注释。整合Pfam、PANTHER、PRINTS、SMART、SUPERFAMILY和其他11个成员数据库。用于蛋白质功能预测、域架构分析、进化分类和GO术语映射。
license: CC0-1.0
metadata:
    skill-author: Kuan-lin Huang
---

# InterPro数据库

## 概述

InterPro（https://www.ebi.ac.uk/interpro/）是由EMBL-EBI维护的蛋白质家族和域分类的综合资源。它整合了来自13个成员数据库的签名，包括Pfam、PANTHER、PRINTS、ProSite、SMART、TIGRFAM、SUPERFAMILY、CDD等，为超过1亿个蛋白质序列提供统一的蛋白质功能注释视图。

InterPro将蛋白质分类为：
- **家族**：共享共同祖先和功能的蛋白质组
- **域**：独立折叠的结构/功能单元
- **同源超家族**：结构相似的蛋白质区域
- **重复**：短串联序列
- **位点**：功能位点（活性、结合、PTM）

**关键资源：**
- InterPro网站：https://www.ebi.ac.uk/interpro/
- REST API：https://www.ebi.ac.uk/interpro/api/
- API文档：https://github.com/ProteinsWebTeam/interpro7-api/blob/master/docs/
- Python客户端：通过`requests`

## 何时使用此技能

在以下情况下使用InterPro：

- **蛋白质功能预测**：未表征蛋白质可能具有什么功能？
- **域架构**：什么域组成蛋白质，以及以什么顺序？
- **蛋白质家族分类**：蛋白质属于哪个家族/超家族？
- **GO术语注释**：通过InterPro将蛋白质序列映射到基因本体术语
- **进化分析**：两个蛋白质是否在同一个同源超家族中？
- **结构预测背景**：新蛋白质结构应该与哪些域比较？
- **流程注释**：批量注释蛋白质组或新序列

## 核心功能

### 1. InterPro REST API

基础URL：`https://www.ebi.ac.uk/interpro/api/`

```python
import requests

BASE_URL = "https://www.ebi.ac.uk/interpro/api"

def interpro_get(endpoint, params=None):
    url = f"{BASE_URL}/{endpoint}"
    headers = {"Accept": "application/json"}
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()
```

### 2. 查找蛋白质

```python
def get_protein_entries(uniprot_id):
    """获取与UniProt蛋白质匹配的所有InterPro条目。"""
    data = interpro_get(f"protein/UniProt/{uniprot_id}/entry/InterPro/")
    return data

# 示例：人类p53（TP53）
result = get_protein_entries("P04637")
entries = result.get("results", [])

for entry in entries:
    meta = entry["metadata"]
    print(f"  {meta['accession']} ({meta['type']}): {meta['name']}")
    # 例如，IPR011615 (域): p53，四聚化域
    #       IPR010991 (域): p53，DNA结合域
    #       IPR013872 (家族): p53家族
```

### 3. 获取特定InterPro条目

```python
def get_entry(interpro_id):
    """获取InterPro条目的详细信息。"""
    return interpro_get(f"entry/InterPro/{interpro_id}/")

# 示例：获取Pfam域PF00397（WW域）
ww_entry = get_entry("IPR001202")
print(f"名称：{ww_entry['metadata']['name']}")
print(f"类型：{ww_entry['metadata']['type']}")

# 也支持成员数据库ID：
def get_pfam_entry(pfam_id):
    return interpro_get(f"entry/Pfam/{pfam_id}/")

pfam = get_pfam_entry("PF00397")
```

### 4. 按InterPro条目搜索蛋白质

```python
def get_proteins_for_entry(interpro_id, database="UniProt", page_size=25):
    """获取用InterPro条目注释的所有蛋白质。"""
    params = {"page_size": page_size}
    data = interpro_get(f"entry/InterPro/{interpro_id}/protein/{database}/", params)
    return data

# 示例：查找所有人类激酶域蛋白质
kinase_proteins = get_proteins_for_entry("IPR000719")  # 蛋白激酶域
print(f"总蛋白质数：{kinase_proteins['count']}")
```

### 5. 域架构

```python
def get_domain_architecture(uniprot_id):
    """获取蛋白质的完整域架构。"""
    data = interpro_get(f"protein/UniProt/{uniprot_id}/")
    return data

# 示例：获取EGFR的完整域架构
egfr = get_domain_architecture("P00533")

# 响应包括序列上所有匹配条目的位置
for entry in egfr.get("entries", []):
    for fragment in entry.get("entry_protein_locations", []):
        for loc in fragment.get("fragments", []):
            print(f"  {entry['accession']}: {loc['start']}-{loc['end']}")
```

### 6. GO术语映射

```python
def get_go_terms_for_protein(uniprot_id):
    """通过InterPro获取与蛋白质关联的GO术语。"""
    data = interpro_get(f"protein/UniProt/{uniprot_id}/")

    # GO术语嵌入在条目元数据中
    go_terms = []
    for entry in data.get("entries", []):
        go = entry.get("metadata", {}).get("go_terms", [])
        go_terms.extend(go)

    # 去重
    seen = set()
    unique_go = []
    for term in go_terms:
        if term["identifier"] not in seen:
            seen.add(term["identifier"])
            unique_go.append(term)

    return unique_go

# GO术语包括：
# {"identifier": "GO:0004672", "name": "protein kinase activity", "category": {"code": "F", "name": "Molecular Function"}}
```

### 7. 批量蛋白质查找

```python
def batch_lookup_proteins(uniprot_ids, database="UniProt"):
    """查找多个蛋白质并收集其InterPro条目。"""
    import time
    results = {}
    for uid in uniprot_ids:
        try:
            data = interpro_get(f"protein/{database}/{uid}/entry/InterPro/")
            entries = data.get("results", [])
            results[uid] = [
                {
                    "accession": e["metadata"]["accession"],
                    "name": e["metadata"]["name"],
                    "type": e["metadata"]["type"]
                }
                for e in entries
            ]
        except Exception as e:
            results[uid] = {"error": str(e)}
        time.sleep(0.3)  # 速率限制
    return results

# 示例
proteins = ["P04637", "P00533", "P38398", "Q9Y6I9"]
domain_info = batch_lookup_proteins(proteins)
for uid, entries in domain_info.items():
    print(f"\n{uid}:")
    for e in entries[:3]:
        print(f"  - {e['accession']} ({e['type']}): {e['name']}")
```

### 8. 按文本或分类学搜索

```python
def search_entries(query, entry_type=None, taxonomy_id=None):
    """按文本搜索InterPro条目。"""
    params = {"search": query, "page_size": 20}
    if entry_type:
        params["type"] = entry_type  # family、domain、homologous_superfamily等

    endpoint = "entry/InterPro/"
    if taxonomy_id:
        endpoint = f"entry/InterPro/taxonomy/UniProt/{taxonomy_id}/"

    return interpro_get(endpoint, params)

# 搜索激酶相关条目
kinase_entries = search_entries("kinase", entry_type="domain")
```

## 查询工作流程

### 工作流程1：表征未知蛋白质

1. **本地运行InterProScan**或通过web（https://www.ebi.ac.uk/interpro/search/sequence/）扫描蛋白质序列
2. **解析结果**以识别域架构
3. **查找每个InterPro条目**以获取生物学背景
4. **从关联的InterPro条目获取GO术语**以进行功能推断

```python
# 运行InterProScan并获取UniProt ID后：
def characterize_protein(uniprot_id):
    """完整表征工作流程。"""

    # 1. 获取所有注释
    entries = get_protein_entries(uniprot_id)

    # 2. 按类型分组
    by_type = {}
    for e in entries.get("results", []):
        t = e["metadata"]["type"]
        by_type.setdefault(t, []).append({
            "accession": e["metadata"]["accession"],
            "name": e["metadata"]["name"]
        })

    # 3. 获取GO术语
    go_terms = get_go_terms_for_protein(uniprot_id)

    return {
        "families": by_type.get("family", []),
        "domains": by_type.get("domain", []),
        "superfamilies": by_type.get("homologous_superfamily", []),
        "go_terms": go_terms
    }
```

### 工作流程2：查找蛋白质家族的所有成员

1. 识别InterPro家族条目ID（例如，IPR000719用于蛋白激酶）
2. 查询用该条目注释的所有UniProt蛋白质
3. 如有需要，按生物/分类学过滤
4. 下载FASTA序列以进行系统发育分析

### 工作流程3：比较域分析

1. 收集感兴趣的蛋白质（例如，所有旁系同源物）
2. 获取每个蛋白质的域架构
3. 比较域组成和顺序
4. 识别域获得/丢失事件

## API端点摘要

| 端点 | 描述 |
|----------|-------------|
| `/protein/UniProt/{id}/` | 蛋白质的完整注释 |
| `/protein/UniProt/{id}/entry/InterPro/` | 蛋白质的InterPro条目 |
| `/entry/InterPro/{id}/` | InterPro条目的详细信息 |
| `/entry/Pfam/{id}/` | Pfam条目详细信息 |
| `/entry/InterPro/{id}/protein/UniProt/` | 带有条目的蛋白质 |
| `/entry/InterPro/` | 搜索/列出InterPro条目 |
| `/taxonomy/UniProt/{tax_id}/` | 来自分类群的蛋白质 |
| `/structure/PDB/{pdb_id}/` | 映射到InterPro的结构 |

## 成员数据库

| 数据库 | 重点 |
|----------|-------|
| Pfam | 蛋白质域（HMM配置文件） |
| PANTHER | 蛋白质家族和亚家族 |
| PRINTS | 蛋白质指纹 |
| ProSitePatterns | 氨基酸模式 |
| ProSiteProfiles | 蛋白质配置文件模式 |
| SMART | 蛋白质域分析 |
| TIGRFAM | JCVI策划的蛋白质家族 |
| SUPERFAMILY | 结构分类 |
| CDD | 保守域数据库（NCBI） |
| HAMAP | 微生物蛋白质家族 |
| NCBIfam | NCBI策划的TIGRFAM |
| Gene3D | CATH结构分类 |
| PIRSR | PIR位点规则 |

## 最佳实践

- **使用UniProt登录号**（而非基因名称）以获得最可靠的查找
- **区分类型**：`family`提供广泛分类；`domain`提供特定结构/功能单元
- **InterProScan对于新序列更快**：对于UniProt中不存在的序列，提交到web服务
- **处理分页**：大型结果集需要遍历页面
- **与UniProt数据结合**：InterPro条目通常包含到UniProt、PDB和GO的链接

## 其他资源

- **InterPro网站**：https://www.ebi.ac.uk/interpro/
- **InterProScan**（本地运行）：https://github.com/ebi-pf-team/interproscan
- **API文档**：https://github.com/ProteinsWebTeam/interpro7-api/blob/master/docs/
- **Pfam**：https://www.ebi.ac.uk/interpro/entry/pfam/
- **引用**：Paysan-Lafosse T et al. (2023) Nucleic Acids Research. PMID: 36350672
