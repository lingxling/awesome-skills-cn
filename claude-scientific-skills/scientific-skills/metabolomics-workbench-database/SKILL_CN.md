---
name: metabolomics-workbench-database
description: Metabolomics Workbench是美国NIH支持的代谢组学数据库和资源平台。提供代谢物数据、实验数据、分析工具、代谢通路和文献资源。支持代谢物鉴定、定量分析、代谢通路分析、数据上传和共享。整合了HMDB、KEGG、PubChem等数据库，提供REST API和Web界面访问。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# Metabolomics Workbench数据库

## 概述

Metabolomics Workbench是美国NIH支持的代谢组学数据库和资源平台。它提供了代谢物数据、实验数据、分析工具、代谢通路和文献资源。该平台支持代谢物鉴定、定量分析、代谢通路分析、数据上传和共享，并整合了HMDB、KEGG、PubChem等数据库，提供REST API和Web界面访问。

## 核心能力

### 1. 代谢物数据库

- **代谢物信息**：代谢物名称、结构、性质
- **代谢物鉴定**：基于质谱和NMR的代谢物鉴定
- **代谢物定量**：定量代谢组学数据
- **代谢物分类**：按化学类别和生物途径分类

### 2. 实验数据

- **研究数据**：公开可用的代谢组学研究数据
- **实验设计**：实验设计和方法学信息
- **原始数据**：原始质谱和NMR数据
- **处理数据**：经过处理和注释的数据

### 3. 分析工具

- **代谢物鉴定**：基于质谱和NMR的代谢物鉴定工具
- **定量分析**：代谢物定量分析工具
- **统计分析**：差异分析、聚类分析、PCA等
- **通路分析**：代谢通路富集分析

### 4. 代谢通路

- **通路映射**：代谢物到代谢通路的映射
- **通路富集**：代谢通路富集分析
- **通路可视化**：代谢通路可视化工具
- **通路比较**：跨条件或物种的通路比较

### 5. 文献资源

- **文献检索**：代谢组学相关文献检索
- **文献注释**：文献的代谢物和通路注释
- **文献关联**：文献与代谢物和通路的关联

## 何时使用此技能

在以下情况下使用此技能：
- 查询代谢物信息和性质
- 进行代谢物鉴定
- 访问代谢组学实验数据
- 进行代谢通路分析
- 使用代谢组学分析工具
- 上传和共享代谢组学数据
- 检索代谢组学文献
- 整合多个代谢组学数据库

## API访问

Metabolomics Workbench提供REST API用于程序化访问。

### 基本端点

```
https://www.metabolomicsworkbench.org/rest/
```

### 常用端点

- `/study/study_id` - 获取研究信息
- `/study/study_id/analysis` - 获取分析信息
- `/compound/compound_id` - 获取代谢物信息
- `/compound/name` - 按名称搜索代谢物
- `/pathway/pathway_id` - 获取通路信息
- `/pathway/compound_id` - 获取代谢物的通路

## 使用示例

### 查询研究信息

```python
import requests

# 查询研究信息
study_id = "ST000001"
url = f"https://www.metabolomicsworkbench.org/rest/study/{study_id}"
response = requests.get(url)
study_data = response.json()

print(f"研究标题: {study_data['study_title']}")
print(f"研究描述: {study_data['study_description']}")
```

### 查询代谢物信息

```python
# 查询代谢物信息
compound_name = "glucose"
url = f"https://www.metabolomicsworkbench.org/rest/compound/{compound_name}"
response = requests.get(url)
compound_data = response.json()

print(f"代谢物名称: {compound_data['name']}")
print(f"代谢物ID: {compound_data['inchikey']}")
```

### 查询代谢通路

```python
# 查询代谢通路
pathway_id = "PWY-5415"
url = f"https://www.metabolomicsworkbench.org/rest/pathway/{pathway_id}"
response = requests.get(url)
pathway_data = response.json()

print(f"通路名称: {pathway_data['name']}")
print(f"通路描述: {pathway_data['description']}")
```

### 搜索代谢物

```python
# 搜索代谢物
search_term = "glucose"
url = f"https://www.metabolomicsworkbench.org/rest/compound/search/{search_term}"
response = requests.get(url)
results = response.json()

for compound in results:
    print(f"名称: {compound['name']}, ID: {compound['inchikey']}")
```

## 数据格式

### 代谢物数据

- **InChIKey**：国际化学标识符
- **SMILES**：简化分子线性输入规范
- **分子量**：分子量
- **化学式**：化学式
- **分类**：化学类别和生物途径

### 实验数据

- **研究ID**：研究标识符
- **分析ID**：分析标识符
- **样本ID**：样本标识符
- **代谢物ID**：代谢物标识符
- **定量值**：代谢物定量值

## 最佳实践

1. **使用标准标识符**：使用InChIKey、HMDB ID等标准标识符
2. **验证数据**：验证查询结果的准确性和完整性
3. **理解数据格式**：理解数据格式和结构
4. **使用API限制**：遵守API速率限制和使用政策
5. **缓存结果**：缓存常用查询结果以提高性能
6. **处理分页**：处理大型结果集的分页
7. **错误处理**：实现适当的错误处理和重试逻辑

## 常见问题

**Q: Metabolomics Workbench支持哪些代谢物？**
A: 支持各种代谢物，包括氨基酸、脂质、碳水化合物等。

**Q: 如何上传数据到Metabolomics Workbench？**
A: 通过Web界面或API上传数据。

**Q: Metabolomics Workbench的数据来源是什么？**
A: 数据来自公开的代谢组学研究和公共数据库。

**Q: 如何进行代谢通路分析？**
A: 使用通路分析工具或API进行代谢通路分析。

## 资源

- **Metabolomics Workbench官网**：https://www.metabolomicsworkbench.org
- **API文档**：https://www.metabolomicsworkbench.org/rest
- **GitHub**：https://github.com/MetabolomicsWorkBench
