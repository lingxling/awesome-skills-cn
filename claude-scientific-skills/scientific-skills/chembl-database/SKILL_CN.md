---
name: chembl-database
description: 查询 ChEMBL 生物活性分子和药物发现数据。按结构/属性搜索化合物,检索生物活性数据(IC50、Ki),查找抑制剂,进行 SAR 研究,用于药物化学。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# ChEMBL 数据库

## 概述

ChEMBL 是由欧洲生物信息学研究所(EBI)维护的手工策展生物活性分子数据库,包含超过200万个化合物、1900万个生物活性测量、13,000+药物靶点以及已批准药物和临床候选药物的数据。使用 ChEMBL Python 客户端以编程方式访问和查询此数据,用于药物发现和药物化学研究。

## 何时使用此技能

在以下情况下使用此技能:

- **化合物搜索**: 按名称、结构或属性查找分子
- **靶点信息**: 检索蛋白质、酶或生物靶点的数据
- **生物活性数据**: 查询 IC50、Ki、EC50 或其他活性测量值
- **药物信息**: 查找已批准药物、机制或适应症
- **结构搜索**: 执行相似性或子结构搜索
- **化学信息学**: 分析分子属性和药物相似性
- **靶点-配体关系**: 探索化合物-靶点相互作用
- **药物发现**: 识别抑制剂、激动剂或生物活性分子

## 安装和设置

### Python 客户端

ChEMBL Python 客户端是编程访问所必需的:

```bash
uv pip install chembl_webresource_client
```

### 基本使用模式

```python
from chembl_webresource_client.new_client import new_client

# 访问不同端点
molecule = new_client.molecule
target = new_client.target
activity = new_client.activity
drug = new_client.drug
```

## 核心功能

### 1. 分子查询

**按 ChEMBL ID 检索:**
```python
molecule = new_client.molecule
aspirin = molecule.get('CHEMBL25')
```

**按名称搜索:**
```python
results = molecule.filter(pref_name__icontains='aspirin')
```

**按属性筛选:**
```python
# 查找小分子(MW <= 500)且 LogP 有利
results = molecule.filter(
    molecule_properties__mw_freebase__lte=500,
    molecule_properties__alogp__lte=5
)
```

### 2. 靶点查询

**检索靶点信息:**
```python
target = new_client.target
egfr = target.get('CHEMBL203')
```

**搜索特定靶点类型:**
```python
# 查找所有激酶靶点
kinases = target.filter(
    target_type='SINGLE PROTEIN',
    pref_name__icontains='kinase'
)
```

### 3. 生物活性数据

**查询靶点的活性:**
```python
activity = new_client.activity
# 查找强效 EGFR 抑制剂
results = activity.filter(
    target_chembl_id='CHEMBL203',
    standard_type='IC50',
    standard_value__lte=100,
    standard_units='nM'
)
```

**获取化合物的所有活性:**
```python
compound_activities = activity.filter(
    molecule_chembl_id='CHEMBL25',
    pchembl_value__isnull=False
)
```

### 4. 基于结构的搜索

**相似性搜索:**
```python
similarity = new_client.similarity
# 查找与阿司匹林相似的化合物
similar = similarity.filter(
    smiles='CC(=O)Oc1ccccc1C(=O)O',
    similarity=85  # 85% 相似性阈值
)
```

**子结构搜索:**
```python
substructure = new_client.substructure
# 查找含有苯环的化合物
results = substructure.filter(smiles='c1ccccc1')
```

### 5. 药物信息

**检索药物数据:**
```python
drug = new_client.drug
drug_info = drug.get('CHEMBL25')
```

**获取作用机制:**
```python
mechanism = new_client.mechanism
mechanisms = mechanism.filter(molecule_chembl_id='CHEMBL25')
```

**查询药物适应症:**
```python
drug_indication = new_client.drug_indication
indications = drug_indication.filter(molecule_chembl_id='CHEMBL25')
```

## 查询工作流程

### 工作流程 1: 查找靶点的抑制剂

1. **通过搜索识别靶点**:
   ```python
   targets = new_client.target.filter(pref_name__icontains='EGFR')
   target_id = targets[0]['target_chembl_id']
   ```

2. **查询该靶点的生物活性数据**:
   ```python
   activities = new_client.activity.filter(
       target_chembl_id=target_id,
       standard_type='IC50',
       standard_value__lte=100
   )
   ```

3. **提取化合物 ID 并检索详细信息**:
   ```python
   compound_ids = [act['molecule_chembl_id'] for act in activities]
   compounds = [new_client.molecule.get(cid) for cid in compound_ids]
   ```

### 工作流程 2: 分析已知药物

1. **获取药物信息**:
   ```python
   drug_info = new_client.drug.get('CHEMBL1234')
   ```

2. **检索机制**:
   ```python
   mechanisms = new_client.mechanism.filter(molecule_chembl_id='CHEMBL1234')
   ```

3. **查找所有生物活性**:
   ```python
   activities = new_client.activity.filter(molecule_chembl_id='CHEMBL1234')
   ```

### 工作流程 3: 结构-活性关系(SAR)研究

1. **查找相似化合物**:
   ```python
   similar = new_client.similarity.filter(smiles='query_smiles', similarity=80)
   ```

2. **获取每个化合物的活性**:
   ```python
   for compound in similar:
       activities = new_client.activity.filter(
           molecule_chembl_id=compound['molecule_chembl_id']
       )
   ```

3. **使用结果中的分子属性分析属性-活性关系**。

## 筛选运算符

ChEMBL 支持 Django 风格的查询筛选器:

- `__exact` - 精确匹配
- `__iexact` - 不区分大小写的精确匹配
- `__contains` / `__icontains` - 子字符串匹配
- `__startswith` / `__endswith` - 前缀/后缀匹配
- `__gt`、`__gte`、`__lt`、`__lte` - 数值比较
- `__range` - 值在范围内
- `__in` - 值在列表中
- `__isnull` - 空值/非空值检查

## 数据导出和分析

将结果转换为 pandas DataFrame 进行分析:

```python
import pandas as pd

activities = new_client.activity.filter(target_chembl_id='CHEMBL203')
df = pd.DataFrame(list(activities))

# 分析结果
print(df['standard_value'].describe())
print(df.groupby('standard_type').size())
```

## 性能优化

### 缓存

客户端自动缓存结果24小时。配置缓存:

```python
from chembl_webresource_client.settings import Settings

# 禁用缓存
Settings.Instance().CACHING = False

# 调整缓存过期时间(秒)
Settings.Instance().CACHE_EXPIRE = 86400
```

### 延迟求值

查询仅在访问数据时执行。转换为列表以强制执行:

```python
# 查询尚未执行
results = molecule.filter(pref_name__icontains='aspirin')

# 强制执行
results_list = list(results)
```

### 分页

结果自动分页。迭代所有结果:

```python
for activity in new_client.activity.filter(target_chembl_id='CHEMBL203'):
    # 处理每个活性
    print(activity['molecule_chembl_id'])
```

## 常见用例

### 查找激酶抑制剂

```python
# 识别激酶靶点
kinases = new_client.target.filter(
    target_type='SINGLE PROTEIN',
    pref_name__icontains='kinase'
)

# 获取强效抑制剂
for kinase in kinases[:5]:  # 前5个激酶
    activities = new_client.activity.filter(
        target_chembl_id=kinase['target_chembl_id'],
        standard_type='IC50',
        standard_value__lte=50
    )
```

### 探索药物重定位

```python
# 获取已批准药物
drugs = new_client.drug.filter()

# 对每个药物,查找所有靶点
for drug in drugs[:10]:
    mechanisms = new_client.mechanism.filter(
        molecule_chembl_id=drug['molecule_chembl_id']
    )
```

### 虚拟筛选

```python
# 查找具有所需属性的化合物
candidates = new_client.molecule.filter(
    molecule_properties__mw_freebase__range=[300, 500],
    molecule_properties__alogp__lte=5,
    molecule_properties__hba__lte=10,
    molecule_properties__hbd__lte=5
)
```

## 资源

### scripts/example_queries.py

即用型 Python 函数,演示常见的 ChEMBL 查询模式:

- `get_molecule_info()` - 按 ID 检索分子详细信息
- `search_molecules_by_name()` - 基于名称的分子搜索
- `find_molecules_by_properties()` - 基于属性的筛选
- `get_bioactivity_data()` - 查询靶点的生物活性
- `find_similar_compounds()` - 相似性搜索
- `substructure_search()` - 子结构匹配
- `get_drug_info()` - 检索药物信息
- `find_kinase_inhibitors()` - 专用激酶抑制剂搜索
- `export_to_dataframe()` - 将结果转换为 pandas DataFrame

查阅此脚本以获取实现细节和使用示例。

### references/api_reference.md

全面的 API 文档包括:

- 完整端点列表(molecule、target、activity、assay、drug 等)
- 所有筛选运算符和查询模式
- 分子属性和生物活性字段
- 高级查询示例
- 配置和性能调优
- 错误处理和速率限制

需要详细 API 信息或排查查询问题时参考此文档。

## 重要说明

### 数据可靠性

- ChEMBL 数据是手工策展的,但可能包含不一致
- 始终检查活性记录中的 `data_validity_comment` 字段
- 注意 `potential_duplicate` 标志

### 单位和标准

- 生物活性值使用标准单位(nM、uM 等)
- `pchembl_value` 提供标准化活性(-log 标度)
- 检查 `standard_type` 以了解测量类型(IC50、Ki、EC50 等)

### 速率限制

- 遵守 ChEMBL 的公平使用政策
- 使用缓存以最小化重复请求
- 对于大型数据集,考虑批量下载
- 避免快速连续请求对 API 造成过大压力

### 化学结构格式

- SMILES 字符串是主要结构格式
- 化合物提供 InChI 键
- 可以通过图像端点生成 SVG 图像

## 其他资源

- ChEMBL 网站: https://www.ebi.ac.uk/chembl/
- API 文档: https://www.ebi.ac.uk/chembl/api/data/docs
- Python 客户端 GitHub: https://github.com/chembl/chembl_webresource_client
- 接口文档: https://chembl.gitbook.io/chembl-interface-documentation/
- 示例笔记本: https://github.com/chembl/notebooks
