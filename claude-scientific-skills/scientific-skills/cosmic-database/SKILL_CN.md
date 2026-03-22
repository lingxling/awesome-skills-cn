---
name: cosmic-database
description: 查询 COSMIC 癌症体细胞突变目录。按基因/组织/突变搜索,获取突变频率、功能影响和临床相关性,用于癌症基因组学和转化研究。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# COSMIC 数据库

## 概述

COSMIC(Catalogue Of Somatic Mutations In Cancer)是癌症体细胞突变的最全面数据库,由威康桑格研究所维护。它包含来自数千项癌症基因组学研究的策展数据,提供有关突变频率、功能影响和临床相关性的信息。

## 何时使用此技能

在以下情况下使用此技能:

- **突变频率分析**: 确定癌症类型中特定基因的突变频率
- **功能影响**: 了解突变的功能后果(错义、无义、剪接位点等)
- **临床相关性**: 探索突变与临床结果或治疗反应之间的关联
- **癌症基因组学**: 分析癌症中的体细胞突变模式
- **药物靶点识别**: 识别癌症中的可药物突变
- **转化研究**: 将基因组发现转化为临床应用
- **生物标志物发现**: 发现诊断或预后生物标志物
- **比较基因组学**: 比较不同癌症类型的突变谱

## 安装和设置

### Python 客户端

COSMIC 提供用于数据访问的 Python 客户端:

```bash
uv pip install cosmic-py
```

### API 访问

COSMIC 提供 REST API 用于编程访问:

```python
import requests

BASE_URL = "https://cancer.sanger.ac.uk/cosmic/api/v0"
```

**身份验证**: 需要有效的 COSMIC 许可证和 API 密钥

**速率限制**: 每秒最多 10 个请求

## 核心功能

### 1. 基因查询

**检索基因信息**,包括突变频率和功能影响:

```python
import requests

# 获取基因信息
response = requests.get(
    "https://cancer.sanger.ac.uk/cosmic/api/v0/genes/TP53",
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)
gene_data = response.json()
```

**基因信息包括:**
- 突变频率(按癌症类型)
- 突变类型(错义、无义、剪接位点等)
- 功能影响
- 临床相关性
- 参考文献引用

### 2. 突变查询

**查询特定突变**:

```python
# 按基因组坐标查询
response = requests.get(
    "https://cancer.sanger.ac.uk/cosmic/api/v0/mutations",
    params={
        "chromosome": "17",
        "position": "7579472",
        "ref": "G",
        "alt": "A"
    },
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)
mutation_data = response.json()
```

**突变信息包括:**
- 基因和转录本
- 蛋白质变化
- 突变类型
- 癌症类型分布
- 功能影响
- 临床意义

### 3. 癌症类型查询

**按癌症类型搜索突变**:

```python
# 获取癌症类型的突变谱
response = requests.get(
    "https://cancer.sanger.ac.uk/cosmic/api/v0/cancers/lung",
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)
cancer_data = response.json()
```

**癌症类型信息包括:**
- 突变频率
- 突变基因列表
- 突变谱
- 临床特征

### 4. 样本查询

**查询特定样本的突变**:

```python
# 获取样本信息
response = requests.get(
    "https://cancer.sanger.ac.uk/cosmic/api/v0/samples/COSMIC_ID",
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)
sample_data = response.json()
```

**样本信息包括:**
- 样本元数据
- 突变列表
- 拷贝数变异
- 结构变异
- 表达数据

### 5. 批量查询

**批量查询多个基因或突变**:

```python
# 批量查询基因
genes = ["TP53", "KRAS", "BRAF"]
for gene in genes:
    response = requests.get(
        f"https://cancer.sanger.ac.uk/cosmic/api/v0/genes/{gene}",
        headers={"Authorization": "Bearer YOUR_API_KEY"}
    )
    data = response.json()
    # 处理数据
```

### 6. 突变频率分析

**分析突变频率**:

```python
# 获取基因的突变频率
response = requests.get(
    "https://cancer.sanger.ac.uk/cosmic/api/v0/genes/TP53/frequency",
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)
frequency_data = response.json()

# 按癌症类型分析
for cancer_type, freq in frequency_data.items():
    print(f"{cancer_type}: {freq}%")
```

### 7. 功能影响分析

**分析突变的功能影响**:

```python
# 获取功能影响数据
response = requests.get(
    "https://cancer.sanger.ac.uk/cosmic/api/v0/genes/TP53/functional",
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)
functional_data = response.json()

# 分析功能影响
for mutation, impact in functional_data.items():
    print(f"{mutation}: {impact}")
```

### 8. 临床相关性分析

**分析临床相关性**:

```python
# 获取临床相关性数据
response = requests.get(
    "https://cancer.sanger.ac.uk/cosmic/api/v0/genes/TP53/clinical",
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)
clinical_data = response.json()

# 分析临床相关性
for association in clinical_data:
    print(f"Association: {association}")
```

### 9. 突变谱分析

**分析突变谱**:

```python
# 获取突变谱
response = requests.get(
    "https://cancer.sanger.ac.uk/cosmic/api/v0/cancers/lung/spectrum",
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)
spectrum_data = response.json()

# 可视化突变谱
import matplotlib.pyplot as plt
plt.bar(spectrum_data.keys(), spectrum_data.values())
plt.xlabel("Mutation Type")
plt.ylabel("Frequency")
plt.show()
```

### 10. 数据导出

**导出数据为各种格式**:

```python
# 导出为 CSV
import pandas as pd

# 获取数据
response = requests.get(
    "https://cancer.sanger.ac.uk/cosmic/api/v0/genes/TP53",
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)
data = response.json()

# 转换为 DataFrame
df = pd.DataFrame(data['mutations'])

# 导出为 CSV
df.to_csv("tp53_mutations.csv", index=False)
```

## 查询工作流程

### 工作流程 1: 分析基因的突变谱

1. **获取基因信息**:
   ```python
   response = requests.get(
       "https://cancer.sanger.ac.uk/cosmic/api/v0/genes/TP53",
       headers={"Authorization": "Bearer YOUR_API_KEY"}
   )
   gene_data = response.json()
   ```

2. **分析突变频率**:
   ```python
   frequencies = gene_data['mutation_frequencies']
   for cancer_type, freq in frequencies.items():
       print(f"{cancer_type}: {freq}%")
   ```

3. **分析突变类型**:
   ```python
   mutation_types = gene_data['mutation_types']
   for mut_type, count in mutation_types.items():
       print(f"{mut_type}: {count}")
   ```

4. **可视化突变谱**:
   ```python
   import matplotlib.pyplot as plt
   plt.bar(mutation_types.keys(), mutation_types.values())
   plt.xlabel("Mutation Type")
   plt.ylabel("Count")
   plt.show()
   ```

### 工作流程 2: 识别癌症中的驱动突变

1. **获取癌症类型信息**:
   ```python
   response = requests.get(
       "https://cancer.sanger.ac.uk/cosmic/api/v0/cancers/lung",
       headers={"Authorization": "Bearer YOUR_API_KEY"}
   )
   cancer_data = response.json()
   ```

2. **识别高频突变基因**:
   ```python
   high_freq_genes = {
       gene: freq for gene, freq in cancer_data['gene_frequencies'].items()
       if freq > 5  # 频率 > 5%
   }
   ```

3. **分析功能影响**:
   ```python
   for gene in high_freq_genes.keys():
       response = requests.get(
           f"https://cancer.sanger.ac.uk/cosmic/api/v0/genes/{gene}/functional",
           headers={"Authorization": "Bearer YOUR_API_KEY"}
       )
       functional_data = response.json()
       # 分析功能影响
   ```

### 工作流程 3: 探索突变的临床相关性

1. **查询特定突变**:
   ```python
   response = requests.get(
       "https://cancer.sanger.ac.uk/cosmic/api/v0/mutations",
       params={
           "gene": "EGFR",
           "protein_change": "L858R"
       },
       headers={"Authorization": "Bearer YOUR_API_KEY"}
   )
   mutation_data = response.json()
   ```

2. **分析临床相关性**:
   ```python
   clinical_associations = mutation_data['clinical_associations']
   for association in clinical_associations:
       print(f"Association: {association}")
   ```

3. **分析治疗反应**:
   ```python
   treatment_response = mutation_data['treatment_response']
   for drug, response in treatment_response.items():
       print(f"{drug}: {response}")
   ```

## 数据类型

### 突变类型

COSMIC 包含多种突变类型:

- **点突变**: 单核苷酸变异
- **插入**: 插入一个或多个核苷酸
- **缺失**: 删除一个或多个核苷酸
- **拷贝数变异**: 基因拷贝数的变化
- **结构变异**: 染色体重排、易位等
- **融合基因**: 两个基因融合形成新的基因

### 功能影响

突变的功能影响分类:

- **错义**: 氨基酸变化
- **无义**: 提前终止密码子
- **剪接位点**: 影响剪接
- **移码**: 阅读框移位
- **同义**: 无氨基酸变化
- **非编码**: 非编码区域

### 临床相关性

突变的临床相关性:

- **预后**: 与预后相关
- **预测**: 预测治疗反应
- **诊断**: 用于诊断
- **易感性**: 癌症易感性

## 最佳实践

### 1. 速率限制管理

```python
import time

def rate_limited_request(url, headers, params=None):
    """进行速率限制的 API 请求"""
    response = requests.get(url, headers=headers, params=params)
    time.sleep(0.1)  # 请求之间等待 0.1 秒
    return response
```

### 2. 错误处理

```python
def safe_api_call(url, headers, params=None, max_retries=3):
    """具有错误处理和重试的 API 调用"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # 指数退避
```

### 3. 数据验证

```python
def validate_mutation_data(data):
    """验证突变数据"""
    required_fields = ['gene', 'mutation_type', 'protein_change']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    return True
```

### 4. 缓存结果

```python
import json
from pathlib import Path

def cached_query(cache_file, api_func, *args, **kwargs):
    """缓存 API 结果"""
    cache_path = Path(cache_file)

    if cache_path.exists():
        with open(cache_path) as f:
            return json.load(f)

    result = api_func(*args, **kwargs)

    with open(cache_path, 'w') as f:
        json.dump(result, f, indent=2)
    return result
```

## 资源

### scripts/query_cosmic.py

Python 脚本,包含常见 COSMIC 查询的即用型函数:

- `get_gene_info(gene_symbol)` - 检索基因详细信息
- `get_mutation_info(chromosome, position, ref, alt)` - 查询特定突变
- `get_cancer_info(cancer_type)` - 获取癌症类型信息
- `get_sample_info(cosmic_id)` - 获取样本信息
- `analyze_mutation_frequency(gene_symbol)` - 分析突变频率
- `analyze_functional_impact(gene_symbol)` - 分析功能影响
- `export_to_csv(data, filename)` - 导出数据为 CSV
- `visualize_mutation_spectrum(data)` - 可视化突变谱

查阅此脚本以获取实现示例和适当的速率限制及错误处理。

### references/api_reference.md

全面的 API 文档,包括:
- 完整的端点列表及参数
- 请求/响应格式规范
- 每个端点的示例查询
- 数据架构定义
- 速率限制详情
- 身份验证要求
- 排查常见错误

需要详细 API 信息或构建复杂查询时参考此文档。

## 重要说明

### 数据许可

COSMIC 数据需要有效的许可证:
- **学术许可证**: 供学术研究使用
- **商业许可证**: 供商业使用
- **API 密钥**: 需要用于 API 访问

联系: cosmic@sanger.ac.uk 获取许可证信息

### 数据质量

- **策展数据**: COSMIC 数据是手工策展的
- **验证**: 数据经过验证和交叉检查
- **更新**: 数据定期更新
- **版本控制**: 使用特定版本以确保可重现性

### 数据覆盖

- **癌症类型**: 涵盖多种癌症类型
- **样本数量**: 数百万个样本
- **基因覆盖**: 涵盖大多数癌症相关基因
- **突变类型**: 包含所有主要突变类型

### 技术局限

- **API 速率限制**: 每秒最多 10 个请求
- **数据大小**: 大型数据集可能需要很长时间下载
- **复杂性**: 某些查询可能很复杂
- **网络依赖**: 需要稳定的网络连接

## 常见用例

### 癌症基因组学研究

```python
# 分析癌症类型中的突变谱
response = requests.get(
    "https://cancer.sanger.ac.uk/cosmic/api/v0/cancers/lung",
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)
cancer_data = response.json()

# 识别驱动突变
driver_mutations = identify_driver_mutations(cancer_data)
```

### 药物靶点识别

```python
# 识别可药物突变
drug_targets = []
for gene in cancer_genes:
    response = requests.get(
        f"https://cancer.sanger.ac.uk/cosmic/api/v0/genes/{gene}/clinical",
        headers={"Authorization": "Bearer YOUR_API_KEY"}
    )
    clinical_data = response.json()
    if is_druggable(clinical_data):
        drug_targets.append(gene)
```

### 生物标志物发现

```python
# 发现预后生物标志物
prognostic_markers = []
for mutation in mutations:
    if mutation['clinical_association'] == 'prognostic':
        prognostic_markers.append(mutation)
```

## 其他资源

- **COSMIC 网站**: https://cancer.sanger.ac.uk/cosmic
- **COSMIC 文档**: https://cancer.sanger.ac.uk/cosmic/documentation
- **API 文档**: https://cancer.sanger.ac.uk/cosmic/api/documentation
- **威康桑格研究所**: https://www.sanger.ac.uk/
- **联系方式**: cosmic@sanger.ac.uk
