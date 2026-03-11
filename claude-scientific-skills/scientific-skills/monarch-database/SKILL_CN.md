---
name: monarch-database
description: Monarch Initiative是一个整合多种生物数据库的跨物种生物医学知识平台。提供基因、疾病、表型、基因型-表型关联、通路、解剖学、同源性和比较基因组学数据。支持跨物种查询、疾病-基因关联、表型相似性分析、基因本体论注解和进化保守性研究。整合了OMIM、Orphanet、MGI、ZFIN、WormBase、FlyBase等数据库。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# Monarch数据库

## 概述

Monarch Initiative是一个整合多种生物数据库的跨物种生物医学知识平台。它提供了一个统一的接口，用于查询和探索基因、疾病、表型、基因型-表型关联、通路、解剖学、同源性和比较基因组学数据。

## 核心能力

### 1. 跨物种数据整合

Monarch整合了多个生物数据库，包括：
- **人类**：OMIM、Orphanet、ClinVar
- **小鼠**：MGI（Mouse Genome Informatics）
- **斑马鱼**：ZFIN（Zebrafish Information Network）
- **线虫**：WormBase
- **果蝇**：FlyBase
- **酵母**：SGD（Saccharomyces Genome Database）
- **其他**：多个物种和数据库

### 2. 基因和疾病关联

查询基因与疾病之间的关联，包括：
- 孟德尔疾病
- 复杂疾病
- 药物靶点
- 基因-疾病证据级别

### 3. 表型分析

分析表型数据，包括：
- 表型相似性
- 基因型-表型关联
- 跨物种表型比较
- 表型本体论（HPO、MP、ZP、WBPhenotype等）

### 4. 比较基因组学

进行跨物种比较，包括：
- 同源基因
- 基因家族
- 进化保守性
- 物种特异性基因

### 5. 通路和功能注解

访问通路和功能注解，包括：
- 基因本体论（GO）
- 通路数据库（KEGG、Reactome）
- 蛋白质-蛋白质相互作用
- 基因调控网络

## 何时使用此技能

在以下情况下使用此技能：
- 查询跨物种生物医学数据
- 研究基因与疾病的关联
- 分析表型相似性和基因型-表型关联
- 进行比较基因组学研究
- 查询基因本体论注解
- 研究进化保守性
- 查询通路和功能注解
- 整合多种生物数据库的数据

## API访问

Monarch提供REST API和GraphQL API用于程序化访问。

### REST API

基本端点：
```
https://api.monarchinitiative.org/api
```

常用端点：
- `/bioentity/gene/{id}` - 获取基因信息
- `/bioentity/disease/{id}` - 获取疾病信息
- `/bioentity/phenotype/{id}` - 获取表型信息
- `/association/between/{gene_id}/{disease_id}` - 获取基因-疾病关联
- `/homologs/{gene_id}` - 获取同源基因
- `/similarity/phenotype/{phenotype_id}` - 获取表型相似性

### GraphQL API

GraphQL端点：
```
https://api.monarchinitiative.org/api/graphql
```

使用GraphQL进行复杂查询，获取特定数据。

## 使用示例

### 查询基因信息

```python
import requests

# 查询基因信息
gene_id = "HGNC:1100"  # BRCA1
url = f"https://api.monarchinitiative.org/api/bioentity/gene/{gene_id}"
response = requests.get(url)
gene_data = response.json()

print(f"基因名称: {gene_data['name']}")
print(f"基因符号: {gene_data['symbol']}")
print(f"描述: {gene_data['description']}")
```

### 查询基因-疾病关联

```python
# 查询基因与疾病的关联
gene_id = "HGNC:1100"  # BRCA1
url = f"https://api.monarchinitiative.org/api/association/between/{gene_id}"
response = requests.get(url)
associations = response.json()

for assoc in associations['associations']:
    disease = assoc['object']
    print(f"疾病: {disease['name']} (ID: {disease['id']})")
    print(f"证据: {assoc['evidence']['label']}")
```

### 查询同源基因

```python
# 查询同源基因
gene_id = "HGNC:1100"  # BRCA1
url = f"https://api.monarchinitiative.org/api/homologs/{gene_id}"
response = requests.get(url)
homologs = response.json()

for homolog in homologs['homologs']:
    print(f"物种: {homolog['taxon']['label']}")
    print(f"基因符号: {homolog['symbol']}")
    print(f"同源类型: {homolog['homology_type']}")
```

### 查询表型相似性

```python
# 查询表型相似性
phenotype_id = "HP:0001250"  # Seizure
url = f"https://api.monarchinitiative.org/api/similarity/phenotype/{phenotype_id}"
response = requests.get(url)
similarities = response.json()

for sim in similarities['matches']:
    print(f"表型: {sim['match']['label']}")
    print(f"相似度: {sim['score']}")
```

## 数据模型

Monarch使用标准化的数据模型和本体论：

### 本体论
- **基因**：NCBI Gene、HGNC
- **疾病**：MONDO、OMIM、Orphanet、DOID
- **表型**：HPO（人类表型本体论）、MP（哺乳动物表型本体论）
- **解剖学**：UBERON（跨物种解剖学本体论）
- **通路**：GO（基因本体论）、KEGG、Reactome

### 关联类型
- **基因-疾病**：孟德尔、关联、治疗靶点
- **基因-表型**：基因型-表型关联
- **同源性**：直系同源、旁系同源
- **通路**：通路成员、调控

## 最佳实践

1. **使用标准标识符**：使用HGNC、OMIM、HPO等标准标识符
2. **理解本体论**：熟悉相关本体论的结构和层次
3. **验证数据**：验证查询结果的准确性和完整性
4. **使用API限制**：遵守API速率限制和使用政策
5. **缓存结果**：缓存常用查询结果以提高性能
6. **处理分页**：处理大型结果集的分页
7. **错误处理**：实现适当的错误处理和重试逻辑

## 常见问题

**Q: Monarch支持哪些物种？**
A: Monarch支持人类、小鼠、斑马鱼、线虫、果蝇、酵母等多个物种。

**Q: 如何获取基因-疾病关联？**
A: 使用 `/association/between/{gene_id}` 端点获取基因与疾病的关联。

**Q: Monarch的数据来源是什么？**
A: Monarch整合了OMIM、Orphanet、MGI、ZFIN、WormBase、FlyBase等多个数据库。

**Q: 如何查询表型相似性？**
A: 使用 `/similarity/phenotype/{phenotype_id}` 端点查询表型相似性。

## 资源

- **Monarch官方网站**：https://monarchinitiative.org
- **API文档**：https://monarchinitiative.org/page/about
- **GraphQL文档**：https://api.monarchinitiative.org/api/graphql
- **GitHub**：https://github.com/monarch-initiative
