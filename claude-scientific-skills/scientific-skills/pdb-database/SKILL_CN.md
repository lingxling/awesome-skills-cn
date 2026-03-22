---
name: pdb-database
description: 访问 RCSB PDB 获取 3D 蛋白质/核酸结构。通过文本/序列/结构搜索，下载坐标（PDB/mmCIF），检索元数据，用于结构生物学和药物发现。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# PDB 数据库

## 概述

RCSB PDB 是生物大分子 3D 结构数据的全球存储库。搜索结构，检索坐标和元数据，对 200,000+ 实验确定的结构和计算模型执行序列和结构相似性搜索。

## 何时使用此技能

此技能应在以下情况使用：
- 通过文本、序列或结构相似性搜索蛋白质或核酸 3D 结构
- 下载 PDB、mmCIF 或 BinaryCIF 格式的坐标文件
- 检索结构元数据、实验方法或质量指标
- 对多个结构执行批处理操作
- 将 PDB 数据集成到药物发现、蛋白质工程或结构生物学研究的计算工作流程中

## 核心功能

### 1. 搜索结构

使用各种搜索条件查找 PDB 条目：

**文本搜索：** 按蛋白质名称、关键字或描述搜索
```python
from rcsbapi.search import TextQuery
query = TextQuery("hemoglobin")
results = list(query())
print(f"Found {len(results)} structures")
```

**属性搜索：** 查询特定属性（生物、分辨率、方法等）
```python
from rcsbapi.search import AttributeQuery
from rcsbapi.search.attrs import rcsb_entity_source_organism

# 查找人类蛋白质结构
query = AttributeQuery(
    attribute=rcsb_entity_source_organism.scientific_name,
    operator="exact_match",
    value="Homo sapiens"
)
results = list(query())
```

**序列相似性：** 查找与给定序列相似的结构
```python
from rcsbapi.search import SequenceQuery

query = SequenceQuery(
    value="MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQVVIDGETCLLDILDTAGQEEYSAMRDQYMRTGEGFLCVFAINNTKSFEDIHHYREQIKRVKDSEDVPMVLVGNKCDLPSRTVDTKQAQDLARSYGIPFIETSAKTRQGVDDAFYTLVREIRKHKEKMSKDGKKKKKKSKTKCVIM",
    evalue_cutoff=0.1,
    identity_cutoff=0.9
)
results = list(query())
```

**结构相似性：** 查找具有相似 3D 几何结构的结构
```python
from rcsbapi.search import StructSimilarityQuery

query = StructSimilarityQuery(
    structure_search_type="entry",
    entry_id="4HHB"  # 血红蛋白
)
results = list(query())
```

**组合查询：** 使用逻辑运算符构建复杂搜索
```python
from rcsbapi.search import TextQuery, AttributeQuery
from rcsbapi.search.attrs import rcsb_entry_info

# 高分辨率人类蛋白质
query1 = AttributeQuery(
    attribute=rcsb_entity_source_organism.scientific_name,
    operator="exact_match",
    value="Homo sapiens"
)
query2 = AttributeQuery(
    attribute=rcsb_entry_info.resolution_combined,
    operator="less",
    value=2.0
)
combined_query = query1 & query2  # AND 操作
results = list(combined_query())
```

### 2. 检索结构数据

访问特定 PDB 条目的详细信息：

**基本条目信息：**
```python
from rcsbapi.data import Schema, fetch

# 获取条目级数据
entry_data = fetch("4HHB", schema=Schema.ENTRY)
print(entry_data["struct"]["title"])
print(entry_data["exptl"][0]["method"])
```

**聚合物实体信息：**
```python
# 获取蛋白质/核酸信息
entity_data = fetch("4HHB_1", schema=Schema.POLYMER_ENTITY)
print(entity_data["entity_poly"]["pdbx_seq_one_letter_code"])
```

**使用 GraphQL 进行灵活查询：**
```python
from rcsbapi.data import fetch

# 自定义 GraphQL 查询
query = """
{
  entry(entry_id: "4HHB") {
    struct {
      title
    }
    exptl {
      method
    }
    rcsb_entry_info {
      resolution_combined
      deposited_atom_count
    }
  }
}
"""
data = fetch(query_type="graphql", query=query)
```

### 3. 下载结构文件

以各种格式检索坐标文件：

**下载方法：**
- **PDB 格式**（传统文本格式）：`https://files.rcsb.org/download/{PDB_ID}.pdb`
- **mmCIF 格式**（现代标准）：`https://files.rcsb.org/download/{PDB_ID}.cif`
- **BinaryCIF**（压缩二进制）：使用 ModelServer API 进行高效访问
- **生物学组装体**：`https://files.rcsb.org/download/{PDB_ID}.pdb1`（对于组装体 1）

**下载示例：**
```python
import requests

pdb_id = "4HHB"

# 下载 PDB 格式
pdb_url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
response = requests.get(pdb_url)
with open(f"{pdb_id}.pdb", "w") as f:
    f.write(response.text)

# 下载 mmCIF 格式
cif_url = f"https://files.rcsb.org/download/{pdb_id}.cif"
response = requests.get(cif_url)
with open(f"{pdb_id}.cif", "w") as f:
    f.write(response.text)
```

### 4. 使用结构数据

使用检索到的结构进行常见操作：

**解析和分析坐标：**
使用 BioPython 或其他结构生物学库处理下载的文件：
```python
from Bio.PDB import PDBParser

parser = PDBParser()
structure = parser.get_structure("protein", "4HHB.pdb")

# 遍历原子
for model in structure:
    for chain in model:
        for residue in chain:
            for atom in residue:
                print(atom.get_coord())
```

**提取元数据：**
```python
from rcsbapi.data import fetch, Schema

# 获取实验细节
data = fetch("4HHB", schema=Schema.ENTRY)

resolution = data.get("rcsb_entry_info", {}).get("resolution_combined")
method = data.get("exptl", [{}])[0].get("method")
deposition_date = data.get("rcsb_accession_info", {}).get("deposit_date")

print(f"Resolution: {resolution} Å")
print(f"Method: {method}")
print(f"Deposited: {deposition_date}")
```

### 5. 批处理操作

高效处理多个结构：

```python
from rcsbapi.data import fetch, Schema

pdb_ids = ["4HHB", "1MBN", "1GZX"]  # 血红蛋白、肌红蛋白等

results = {}
for pdb_id in pdb_ids:
    try:
        data = fetch(pdb_id, schema=Schema.ENTRY)
        results[pdb_id] = {
            "title": data["struct"]["title"],
            "resolution": data.get("rcsb_entry_info", {}).get("resolution_combined"),
            "organism": data.get("rcsb_entity_source_organism", [{}])[0].get("scientific_name")
        }
    except Exception as e:
        print(f"Error fetching {pdb_id}: {e}")

# 显示结果
for pdb_id, info in results.items():
    print(f"\n{pdb_id}: {info['title']}")
    print(f"  Resolution: {info['resolution']} Å")
    print(f"  Organism: {info['organism']}")
```

## Python 包安装

安装官方 RCSB PDB Python API 客户端：

```bash
# 当前推荐的包
uv pip install rcsb-api

# 对于遗留代码（已弃用，使用 rcsb-api 代替）
uv pip install rcsbsearchapi
```

`rcsb-api` 包通过 `rcsbapi.search` 和 `rcsbapi.data` 模块提供对搜索和数据 API 的统一访问。

## 常见用例

### 药物发现
- 搜索药物靶点的结构
- 分析配体结合位点
- 比较蛋白质-配体复合物
- 识别相似的结合口袋

### 蛋白质工程
- 找到用于建模的同源结构
- 分析序列-结构关系
- 比较突变体结构
- 研究蛋白质稳定性和动力学

### 结构生物学研究
- 下载结构进行计算分析
- 构建基于结构的比对
- 分析结构特征（二级结构、结构域）
- 比较实验方法和质量指标

### 教育和可视化
- 检索用于教学的结构
- 生成分子可视化
- 探索结构-功能关系
- 研究进化保守性

## 关键概念

**PDB ID：** 每个结构条目的唯一 4 字符标识符（例如，"4HHB"）。AlphaFold 和 ModelArchive 条目以 "AF_" 或 "MA_" 前缀开头。

**mmCIF/PDBx：** 现代文件格式，使用键值结构，取代大型结构的传统 PDB 格式。

**生物学组装体：** 大分子的功能形式，可能包含来自不对称单位的多个链副本。

**分辨率：** 晶体结构中细节的度量（值越低 = 细节越高）。典型范围：高质量结构为 1.5-3.5 Å。

**实体：** 结构中的唯一分子组件（蛋白质链、DNA、配体等）。

## 资源

此技能在 `references/` 目录中包含参考文档：

### references/api_reference.md
综合 API 文档，包括：
- 详细的 API 端点规范
- 高级查询模式和示例
- 数据模式参考
- 速率限制和最佳实践
- 常见问题的故障排除

当您需要有关 API 功能、复杂查询构建或详细数据模式信息的深入信息时，请使用此参考。

## 其他资源

- **RCSB PDB 网站：** https://www.rcsb.org
- **PDB-101 教育门户：** https://pdb101.rcsb.org
- **API 文档：** https://www.rcsb.org/docs/programmatic-access/web-apis-overview
- **Python 包文档：** https://rcsbapi.readthedocs.io/
- **数据 API 文档：** https://data.rcsb.org/
- **GitHub 仓库：** https://github.com/rcsb/py-rcsb-api