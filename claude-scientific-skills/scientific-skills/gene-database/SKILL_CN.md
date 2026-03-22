---
name: gene-database
description: 查询多个基因数据库（NCBI Gene、Ensembl、UniProt、HGNC）以获取全面的基因信息，包括基因符号、描述、基因组位置、功能注释、蛋白质序列、疾病关联和表达模式。用于基因查找、功能注释、疾病研究或任何需要综合基因信息的任务。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# 基因数据库

## 概述

基因数据库技能提供对多个基因数据库的统一访问，包括NCBI Gene、Ensembl、UniProt和HGNC。它允许查询基因信息，包括基因符号、描述、基因组位置、功能注释、蛋白质序列、疾病关联和表达模式。

## 何时使用此技能

使用基因数据库当：

- **查找基因信息**：获取基因符号、描述、基因组位置
- **功能注释**：获取基因功能、通路、GO术语
- **蛋白质信息**：获取蛋白质序列、结构、功能域
- **疾病关联**：查找与疾病相关的基因
- **表达模式**：获取基因表达数据
- **跨数据库查询**：跨多个数据库查询基因信息
- **基因映射**：在不同数据库之间映射基因标识符

## 核心功能

### 1. NCBI Gene

#### 按基因符号查询

```python
from scripts.gene_query import GeneQuery

# 初始化
gene_query = GeneQuery()

# 按基因符号查询
gene_info = gene_query.query_ncbi_gene("BRCA1")

# 获取基因信息
print(f"基因符号: {gene_info['symbol']}")
print(f"描述: {gene_info['description']}")
print(f"基因组位置: {gene_info['chromosome']}:{gene_info['start']}-{gene_info['end']}")
print(f"基因ID: {gene_info['gene_id']}")
```

#### 按基因ID查询

```python
# 按NCBI Gene ID查询
gene_info = gene_query.query_ncbi_gene_by_id(672)

print(f"基因符号: {gene_info['symbol']}")
print(f"描述: {gene_info['description']}")
```

### 2. Ensembl

#### 按基因符号查询

```python
# 按基因符号查询Ensembl
gene_info = gene_query.query_ensembl("BRCA1")

# 获取Ensembl信息
print(f"Ensembl ID: {gene_info['ensembl_id']}")
print(f"基因符号: {gene_info['symbol']}")
print(f"基因组位置: {gene_info['chromosome']}:{gene_info['start']}-{gene_info['end']}")
print(f"生物型: {gene_info['biotype']}")
```

#### 按Ensembl ID查询

```python
# 按Ensembl ID查询
gene_info = gene_query.query_ensembl_by_id("ENSG00000012048")

print(f"基因符号: {gene_info['symbol']}")
print(f"描述: {gene_info['description']}")
```

### 3. UniProt

#### 按基因符号查询

```python
# 按基因符号查询UniProt
protein_info = gene_query.query_uniprot("BRCA1")

# 获取蛋白质信息
print(f"UniProt ID: {protein_info['uniprot_id']}")
print(f"蛋白质名称: {protein_info['protein_name']}")
print(f"基因名称: {protein_info['gene_name']}")
print(f"蛋白质长度: {protein_info['length']}")
```

#### 按UniProt ID查询

```python
# 按UniProt ID查询
protein_info = gene_query.query_uniprot_by_id("P38398")

print(f"蛋白质名称: {protein_info['protein_name']}")
print(f"基因名称: {protein_info['gene_name']}")
```

### 4. HGNC

#### 按基因符号查询

```python
# 按基因符号查询HGNC
gene_info = gene_query.query_hgnc("BRCA1")

# 获取HGNC信息
print(f"HGNC ID: {gene_info['hgnc_id']}")
print(f"基因符号: {gene_info['symbol']}")
print(f"基因名称: {gene_info['name']}")
print(f"符号状态: {gene_info['status']}")
```

### 5. 跨数据库查询

#### 综合基因信息

```python
# 获取综合基因信息
gene_info = gene_query.get_comprehensive_gene_info("BRCA1")

# 获取所有数据库的信息
print(f"NCBI Gene ID: {gene_info['ncbi']['gene_id']}")
print(f"Ensembl ID: {gene_info['ensembl']['ensembl_id']}")
print(f"UniProt ID: {gene_info['uniprot']['uniprot_id']}")
print(f"HGNC ID: {gene_info['hgnc']['hgnc_id']}")
```

### 6. 批量查询

#### 批量查询基因

```python
# 批量查询多个基因
gene_symbols = ["BRCA1", "BRCA2", "TP53", "EGFR"]

results = gene_query.batch_query_genes(gene_symbols)

# 处理结果
for gene_symbol, gene_info in results.items():
    print(f"{gene_symbol}: {gene_info['description']}")
```

### 7. 基因标识符映射

#### 映射基因标识符

```python
# 映射基因符号到Ensembl ID
ensembl_ids = gene_query.map_symbol_to_ensembl(["BRCA1", "BRCA2"])

# 映射Ensembl ID到基因符号
symbols = gene_query.map_ensembl_to_symbol(["ENSG00000012048", "ENSG00000139618"])

# 映射基因符号到UniProt ID
uniprot_ids = gene_query.map_symbol_to_uniprot(["BRCA1", "BRCA2"])
```

## 高级功能

### 1. 获取基因序列

```python
# 获取基因序列
gene_sequence = gene_query.get_gene_sequence("BRCA1")

print(f"基因长度: {len(gene_sequence)} bp")
print(f"序列: {gene_sequence[:100]}...")
```

### 2. 获取蛋白质序列

```python
# 获取蛋白质序列
protein_sequence = gene_query.get_protein_sequence("BRCA1")

print(f"蛋白质长度: {len(protein_sequence)} aa")
print(f"序列: {protein_sequence[:100]}...")
```

### 3. 获取基因注释

```python
# 获取基因注释
annotations = gene_query.get_gene_annotations("BRCA1")

# 获取GO术语
go_terms = annotations['go_terms']
print(f"生物过程: {go_terms['biological_process']}")
print(f"分子功能: {go_terms['molecular_function']}")
print(f"细胞组分: {go_terms['cellular_component']}")

# 获取通路
pathways = annotations['pathways']
print(f"通路: {pathways}")
```

### 4. 获取疾病关联

```python
# 获取疾病关联
diseases = gene_query.get_disease_associations("BRCA1")

for disease in diseases:
    print(f"疾病: {disease['name']}")
    print(f"关联类型: {disease['association_type']}")
    print(f"来源: {disease['source']}")
```

### 5. 获取表达数据

```python
# 获取表达数据
expression = gene_query.get_expression_data("BRCA1")

# 获取组织表达
tissue_expression = expression['tissue_expression']
print(f"组织表达: {tissue_expression}")

# 获取发育阶段表达
developmental_expression = expression['developmental_expression']
print(f"发育阶段表达: {developmental_expression}")
```

## 常见工作流

### 工作流1：查找基因信息

```python
from scripts.gene_query import GeneQuery

# 初始化
gene_query = GeneQuery()

# 查询基因
gene_symbol = "BRCA1"

# 获取综合信息
gene_info = gene_query.get_comprehensive_gene_info(gene_symbol)

# 打印信息
print(f"基因符号: {gene_symbol}")
print(f"描述: {gene_info['ncbi']['description']}")
print(f"基因组位置: {gene_info['ensembl']['chromosome']}:{gene_info['ensembl']['start']}-{gene_info['ensembl']['end']}")
print(f"蛋白质长度: {gene_info['uniprot']['length']} aa")
```

### 工作流2：批量查询基因

```python
from scripts.gene_query import GeneQuery

# 初始化
gene_query = GeneQuery()

# 批量查询
gene_symbols = ["BRCA1", "BRCA2", "TP53", "EGFR", "KRAS"]

results = gene_query.batch_query_genes(gene_symbols)

# 创建摘要表
import pandas as pd

summary = []
for gene_symbol, gene_info in results.items():
    summary.append({
        '基因符号': gene_symbol,
        '描述': gene_info['ncbi']['description'],
        '染色体': gene_info['ensembl']['chromosome'],
        '蛋白质长度': gene_info['uniprot']['length']
    })

df = pd.DataFrame(summary)
print(df)
```

### 工作流3：基因功能分析

```python
from scripts.gene_query import GeneQuery

# 初始化
gene_query = GeneQuery()

# 查询基因
gene_symbol = "TP53"

# 获取注释
annotations = gene_query.get_gene_annotations(gene_symbol)

# 打印GO术语
print(f"生物过程: {annotations['go_terms']['biological_process'][:5]}")
print(f"分子功能: {annotations['go_terms']['molecular_function'][:5]}")
print(f"细胞组分: {annotations['go_terms']['cellular_component'][:5]}")

# 打印通路
print(f"通路: {annotations['pathways'][:5]}")
```

### 工作流4：疾病基因分析

```python
from scripts.gene_query import GeneQuery

# 初始化
gene_query = GeneQuery()

# 查询疾病相关基因
disease = "breast cancer"

# 查找相关基因
genes = gene_query.search_disease_genes(disease)

# 获取基因信息
for gene_symbol in genes[:10]:
    gene_info = gene_query.get_comprehensive_gene_info(gene_symbol)
    print(f"{gene_symbol}: {gene_info['ncbi']['description']}")
```

### 工作流5：基因标识符映射

```python
from scripts.gene_query import GeneQuery

# 初始化
gene_query = GeneQuery()

# 映射标识符
gene_symbols = ["BRCA1", "BRCA2", "TP53"]

# 映射到Ensembl ID
ensembl_ids = gene_query.map_symbol_to_ensembl(gene_symbols)
print(f"Ensembl IDs: {ensembl_ids}")

# 映射到UniProt ID
uniprot_ids = gene_query.map_symbol_to_uniprot(gene_symbols)
print(f"UniProt IDs: {uniprot_ids}")

# 映射到NCBI Gene ID
ncbi_ids = gene_query.map_symbol_to_ncbi(gene_symbols)
print(f"NCBI Gene IDs: {ncbi_ids}")
```

## 最佳实践

1. **使用综合查询**：使用`get_comprehensive_gene_info`获取所有数据库的信息
2. **批量查询**：使用批量查询功能提高效率
3. **标识符映射**：使用标识符映射功能在不同数据库之间转换
4. **错误处理**：始终处理查询错误和缺失数据
5. **缓存结果**：缓存查询结果以避免重复请求
6. **验证结果**：验证查询结果的准确性

## 与其他工具集成

### 与gget集成

```python
import gget
from scripts.gene_query import GeneQuery

# 使用gget查询
gene_info = gget.info(["BRCA1"])

# 使用gene_query获取更详细的信息
gene_query = GeneQuery()
detailed_info = gene_query.get_comprehensive_gene_info("BRCA1")
```

### 与biopython集成

```python
from Bio import Entrez
from scripts.gene_query import GeneQuery

# 使用Biopython查询
Entrez.email = "your.email@example.com"
handle = Entrez.esearch(db="gene", term="BRCA1[Gene]")
record = Entrez.read(handle)

# 使用gene_query获取更多信息
gene_query = GeneQuery()
gene_info = gene_query.get_comprehensive_gene_info("BRCA1")
```

### 与pandas集成

```python
import pandas as pd
from scripts.gene_query import GeneQuery

# 批量查询
gene_query = GeneQuery()
gene_symbols = ["BRCA1", "BRCA2", "TP53", "EGFR"]

results = gene_query.batch_query_genes(gene_symbols)

# 创建DataFrame
df = pd.DataFrame.from_dict(results, orient='index')
print(df)
```

## 故障排除

**问题：查询失败**
- 解决方案：检查网络连接，验证基因符号，检查API限制

**问题：数据不完整**
- 解决方案：尝试其他数据库，检查基因符号是否正确

**问题：标识符映射失败**
- 解决方案：验证标识符格式，检查数据库版本

**问题：批量查询很慢**
- 解决方案：减少查询数量，使用缓存，或分批查询

**问题：API限制**
- 解决方案：实现速率限制，使用缓存，或等待一段时间后重试

## 其他资源

- **NCBI Gene**: https://www.ncbi.nlm.nih.gov/gene/
- **Ensembl**: https://www.ensembl.org/
- **UniProt**: https://www.uniprot.org/
- **HGNC**: https://www.genenames.org/
- **gget文档**: https://pachterlab.github.io/gget/
- **Biopython文档**: https://biopython.org/
