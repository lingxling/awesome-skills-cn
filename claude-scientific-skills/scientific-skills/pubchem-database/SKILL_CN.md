---
name: pubchem-database
description: 通过PUG-REST API/PubChemPy查询PubChem（1.1亿+化合物）。通过名称/CID/SMILES搜索，检索属性，进行相似性/子结构搜索，获取生物活性数据，用于化学信息学。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# PubChem 数据库

## 概述

PubChem是世界上最大的免费可用化学数据库，包含1.1亿+化合物和2.7亿+生物活性数据。通过PUG-REST API和PubChemPy，可按名称、CID或SMILES查询化学结构，检索分子属性，执行相似性和子结构搜索，访问生物活性数据。

## 使用场景

本技能适用于以下情况：
- 通过名称、结构（SMILES/InChI）或分子式搜索化合物
- 检索分子属性（分子量、LogP、TPSA、氢键描述符）
- 执行相似性搜索以找到结构相关的化合物
- 进行子结构搜索以寻找特定的化学基序
- 访问来自筛选测定的生物活性数据
- 在化学标识符格式之间转换（CID、SMILES、InChI）
- 批量处理多个化合物以进行类药性筛选或属性分析

## 核心功能

### 1. 化学结构搜索

使用多种标识符类型搜索化合物：

**通过化学名称**：
```python
import pubchempy as pcp
compounds = pcp.get_compounds('aspirin', 'name')
compound = compounds[0]
```

**通过CID（化合物ID）**：
```python
compound = pcp.Compound.from_cid(2244)  # 阿司匹林
```

**通过SMILES**：
```python
compound = pcp.get_compounds('CC(=O)OC1=CC=CC=C1C(=O)O', 'smiles')[0]
```

**通过InChI**：
```python
compound = pcp.get_compounds('InChI=1S/C9H8O4/...', 'inchi')[0]
```

**通过分子式**：
```python
compounds = pcp.get_compounds('C9H8O4', 'formula')
# 返回所有匹配此分子式的化合物
```

### 2. 属性检索

使用高级或低级方法检索化合物的分子属性：

**使用PubChemPy（推荐）**：
```python
import pubchempy as pcp

# 获取带有所有属性的化合物对象
compound = pcp.get_compounds('caffeine', 'name')[0]

# 访问各个属性
molecular_formula = compound.molecular_formula
molecular_weight = compound.molecular_weight
iupac_name = compound.iupac_name
smiles = compound.canonical_smiles
inchi = compound.inchi
xlogp = compound.xlogp  # 分配系数
tpsa = compound.tpsa    # 拓扑极性表面积
```

**获取特定属性**：
```python
# 仅请求特定属性
properties = pcp.get_properties(
    ['MolecularFormula', 'MolecularWeight', 'CanonicalSMILES', 'XLogP'],
    'aspirin',
    'name'
)
# 返回字典列表
```

**批量属性检索**：
```python
import pandas as pd

compound_names = ['aspirin', 'ibuprofen', 'paracetamol']
all_properties = []

for name in compound_names:
    props = pcp.get_properties(
        ['MolecularFormula', 'MolecularWeight', 'XLogP'],
        name,
        'name'
    )
    all_properties.extend(props)

df = pd.DataFrame(all_properties)
```

**可用属性**：MolecularFormula、MolecularWeight、CanonicalSMILES、IsomericSMILES、InChI、InChIKey、IUPACName、XLogP、TPSA、HBondDonorCount、HBondAcceptorCount、RotatableBondCount、Complexity、Charge等（完整列表见`references/api_reference.md`）。

### 3. 相似性搜索

使用Tanimoto相似性查找结构相似的化合物：

```python
import pubchempy as pcp

# 从查询化合物开始
query_compound = pcp.get_compounds('gefitinib', 'name')[0]
query_smiles = query_compound.canonical_smiles

# 执行相似性搜索
similar_compounds = pcp.get_compounds(
    query_smiles,
    'smiles',
    searchtype='similarity',
    Threshold=85,  # 相似性阈值 (0-100)
    MaxRecords=50
)

# 处理结果
for compound in similar_compounds[:10]:
    print(f"CID {compound.cid}: {compound.iupac_name}")
    print(f"  MW: {compound.molecular_weight}")
```

**注意**：大型查询的相似性搜索是异步的，可能需要15-30秒才能完成。PubChemPy会自动处理异步模式。

### 4. 子结构搜索

查找包含特定结构基序的化合物：

```python
import pubchempy as pcp

# 搜索包含吡啶环的化合物
pyridine_smiles = 'c1ccncc1'

matches = pcp.get_compounds(
    pyridine_smiles,
    'smiles',
    searchtype='substructure',
    MaxRecords=100
)

print(f"Found {len(matches)} compounds containing pyridine")
```

**常见子结构**：
- 苯环：`c1ccccc1`
- 吡啶：`c1ccncc1`
- 苯酚：`c1ccc(O)cc1`
- 羧酸：`C(=O)O`

### 5. 格式转换

在不同的化学结构格式之间转换：

```python
import pubchempy as pcp

compound = pcp.get_compounds('aspirin', 'name')[0]

# 转换为不同格式
smiles = compound.canonical_smiles
inchi = compound.inchi
inchikey = compound.inchikey
cid = compound.cid

# 下载结构文件
pcp.download('SDF', 'aspirin', 'name', 'aspirin.sdf', overwrite=True)
pcp.download('JSON', '2244', 'cid', 'aspirin.json', overwrite=True)
```

### 6. 结构可视化

生成2D结构图像：

```python
import pubchempy as pcp

# 下载化合物结构为PNG
pcp.download('PNG', 'caffeine', 'name', 'caffeine.png', overwrite=True)

# 使用直接URL（通过requests）
import requests

cid = 2244  # 阿司匹林
url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG?image_size=large"
response = requests.get(url)

with open('structure.png', 'wb') as f:
    f.write(response.content)
```

### 7. 同义词检索

获取化合物的所有已知名称和同义词：

```python
import pubchempy as pcp

synonyms_data = pcp.get_synonyms('aspirin', 'name')

if synonyms_data:
    cid = synonyms_data[0]['CID']
    synonyms = synonyms_data[0]['Synonym']

    print(f"CID {cid} has {len(synonyms)} synonyms:")
    for syn in synonyms[:10]:  # 前10个
        print(f"  - {syn}")
```

### 8. 生物活性数据访问

从测定中检索生物活性数据：

```python
import requests
import json

# 获取化合物的生物测定摘要
cid = 2244  # 阿司匹林
url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/assaysummary/JSON"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    # 处理生物测定信息
    table = data.get('Table', {})
    rows = table.get('Row', [])
    print(f"Found {len(rows)} bioassay records")
```

**对于更复杂的生物活性查询**，使用`scripts/bioactivity_query.py`辅助脚本，提供：
- 带有活性结果过滤的生物测定摘要
- 测定靶点识别
- 按生物靶点搜索化合物
- 特定测定的活性化合物列表

### 9. 综合化合物注释

通过PUG-View访问详细的化合物信息：

```python
import requests

cid = 2244
url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON"

response = requests.get(url)
if response.status_code == 200:
    annotations = response.json()
    # 包含广泛的数据，包括：
    # - 化学和物理性质
    # - 药物和药物信息
    # - 药理学和生物化学
    # - 安全和危害
    # - 毒性
    # - 文献引用
    # - 专利
```

**获取特定部分**：
```python
# 仅获取药物信息
url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON?heading=Drug and Medication Information"
```

## 安装要求

安装PubChemPy用于基于Python的访问：

```bash
uv pip install pubchempy
```

对于直接API访问和生物活性查询：

```bash
uv pip install requests
```

数据分析的可选依赖：

```bash
uv pip install pandas
```

## 辅助脚本

本技能包含用于常见PubChem任务的Python脚本：

### scripts/compound_search.py

提供用于搜索和检索化合物信息的实用函数：

**关键函数**：
- `search_by_name(name, max_results=10)`：按名称搜索化合物
- `search_by_smiles(smiles)`：按SMILES字符串搜索
- `get_compound_by_cid(cid)`：通过CID检索化合物
- `get_compound_properties(identifier, namespace, properties)`：获取特定属性
- `similarity_search(smiles, threshold, max_records)`：执行相似性搜索
- `substructure_search(smiles, max_records)`：执行子结构搜索
- `get_synonyms(identifier, namespace)`：获取所有同义词
- `batch_search(identifiers, namespace, properties)`：批量搜索多个化合物
- `download_structure(identifier, namespace, format, filename)`：下载结构
- `print_compound_info(compound)`：打印格式化的化合物信息

**使用**：
```python
from scripts.compound_search import search_by_name, get_compound_properties

# 搜索化合物
compounds = search_by_name('ibuprofen')

# 获取特定属性
props = get_compound_properties('aspirin', 'name', ['MolecularWeight', 'XLogP'])
```

### scripts/bioactivity_query.py

提供用于检索生物活性数据的函数：

**关键函数**：
- `get_bioassay_summary(cid)`：获取化合物的生物测定摘要
- `get_compound_bioactivities(cid, activity_outcome)`：获取过滤的生物活性
- `get_assay_description(aid)`：获取详细的测定信息
- `get_assay_targets(aid)`：获取测定的生物靶点
- `search_assays_by_target(target_name, max_results)`：按靶点查找测定
- `get_active_compounds_in_assay(aid, max_results)`：获取活性化合物
- `get_compound_annotations(cid, section)`：获取PUG-View注释
- `summarize_bioactivities(cid)`：生成生物活性摘要统计
- `find_compounds_by_bioactivity(target, threshold, max_compounds)`：按靶点查找化合物

**使用**：
```python
from scripts.bioactivity_query import get_bioassay_summary, summarize_bioactivities

# 获取生物活性摘要
summary = summarize_bioactivities(2244)  # 阿司匹林
print(f"Total assays: {summary['total_assays']}")
print(f"Active: {summary['active']}, Inactive: {summary['inactive']}")
```

## API速率限制和最佳实践

**速率限制**：
- 每秒最多5个请求
- 每分钟最多400个请求
- 每分钟最多300秒运行时间

**最佳实践**：
1. **对重复查询使用CID**：CID比名称或结构更高效
2. **本地缓存结果**：存储频繁访问的数据
3. **批处理请求**：尽可能组合多个查询
4. **实现延迟**：在请求之间添加0.2-0.3秒的延迟
5. **优雅处理错误**：检查HTTP错误和缺失数据
6. **使用PubChemPy**：高级抽象处理许多边缘情况
7. **利用异步模式**：对于大型相似性/子结构搜索
8. **指定MaxRecords**：限制结果以避免超时

**错误处理**：
```python
from pubchempy import BadRequestError, NotFoundError, TimeoutError

try:
    compound = pcp.get_compounds('query', 'name')[0]
except NotFoundError:
    print("化合物未找到")
except BadRequestError:
    print("请求格式无效")
except TimeoutError:
    print("请求超时 - 尝试减小范围")
except IndexError:
    print("未返回结果")
```

## 常见工作流程

### 工作流程1：化学标识符转换管道

在不同的化学标识符之间转换：

```python
import pubchempy as pcp

# 从任何标识符类型开始
compound = pcp.get_compounds('caffeine', 'name')[0]

# 提取所有标识符格式
identifiers = {
    'CID': compound.cid,
    'Name': compound.iupac_name,
    'SMILES': compound.canonical_smiles,
    'InChI': compound.inchi,
    'InChIKey': compound.inchikey,
    'Formula': compound.molecular_formula
}
```

### 工作流程2：类药性属性筛选

使用Lipinski五规则筛选化合物：

```python
import pubchempy as pcp

def check_drug_likeness(compound_name):
    compound = pcp.get_compounds(compound_name, 'name')[0]

    # Lipinski五规则
    rules = {
        'MW <= 500': compound.molecular_weight <= 500,
        'LogP <= 5': compound.xlogp <= 5 if compound.xlogp else None,
        'HBD <= 5': compound.h_bond_donor_count <= 5,
        'HBA <= 10': compound.h_bond_acceptor_count <= 10
    }

    violations = sum(1 for v in rules.values() if v is False)
    return rules, violations

rules, violations = check_drug_likeness('aspirin')
print(f"Lipinski violations: {violations}")
```

### 工作流程3：寻找类似药物候选物

识别与已知药物结构相似的化合物：

```python
import pubchempy as pcp

# 从已知药物开始
reference_drug = pcp.get_compounds('imatinib', 'name')[0]
reference_smiles = reference_drug.canonical_smiles

# 查找相似化合物
similar = pcp.get_compounds(
    reference_smiles,
    'smiles',
    searchtype='similarity',
    Threshold=85,
    MaxRecords=20
)

# 按类药性属性过滤
candidates = []
for comp in similar:
    if comp.molecular_weight and 200 <= comp.molecular_weight <= 600:
        if comp.xlogp and -1 <= comp.xlogp <= 5:
            candidates.append(comp)

print(f"Found {len(candidates)} drug-like candidates")
```

### 工作流程4：批量化合物属性比较

比较多个化合物的属性：

```python
import pubchempy as pcp
import pandas as pd

compound_list = ['aspirin', 'ibuprofen', 'naproxen', 'celecoxib']

properties_list = []
for name in compound_list:
    try:
        compound = pcp.get_compounds(name, 'name')[0]
        properties_list.append({
            'Name': name,
            'CID': compound.cid,
            'Formula': compound.molecular_formula,
            'MW': compound.molecular_weight,
            'LogP': compound.xlogp,
            'TPSA': compound.tpsa,
            'HBD': compound.h_bond_donor_count,
            'HBA': compound.h_bond_acceptor_count
        })
    except Exception as e:
        print(f"Error processing {name}: {e}")

df = pd.DataFrame(properties_list)
print(df.to_string(index=False))
```

### 工作流程5：基于子结构的虚拟筛选

筛选包含特定药效团的化合物：

```python
import pubchempy as pcp

# 定义药效团（例如，磺酰胺基团）
pharmacophore_smiles = 'S(=O)(=O)N'

# 搜索包含此子结构的化合物
hits = pcp.get_compounds(
    pharmacophore_smiles,
    'smiles',
    searchtype='substructure',
    MaxRecords=100
)

# 进一步按属性过滤
filtered_hits = [
    comp for comp in hits
    if comp.molecular_weight and comp.molecular_weight < 500
]

print(f"Found {len(filtered_hits)} compounds with desired substructure")
```

## 参考文档

有关详细的API文档，包括完整的属性列表、URL模式、高级查询选项和更多示例，请查阅`references/api_reference.md`。此综合参考包括：

- 完整的PUG-REST API端点文档
- 可用分子属性的完整列表
- 异步请求处理模式
- PubChemPy API参考
- 用于注释的PUG-View API
- 常见工作流程和用例
- 官方PubChem文档链接

## 故障排除

**化合物未找到**：
- 尝试替代名称或同义词
- 如果已知，使用CID
- 检查拼写和化学名称格式

**超时错误**：
- 减小MaxRecords参数
- 在请求之间添加延迟
- 使用CID而不是名称进行更快的查询

**空属性值**：
- 并非所有化合物都有所有属性
- 在访问前检查属性是否存在：`if compound.xlogp:`
- 某些属性仅适用于特定类型的化合物

**速率限制超过**：
- 实现请求之间的延迟（0.2-0.3秒）
- 尽可能使用批处理操作
- 考虑本地缓存结果

**相似性/子结构搜索挂起**：
- 这些是异步操作，可能需要15-30秒
- PubChemPy自动处理轮询
- 如果超时，减小MaxRecords

## 其他资源

- PubChem主页：https://pubchem.ncbi.nlm.nih.gov/
- PUG-REST文档：https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
- PUG-REST教程：https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest-tutorial
- PubChemPy文档：https://pubchempy.readthedocs.io/
- PubChemPy GitHub：https://github.com/mcs07/PubChemPy