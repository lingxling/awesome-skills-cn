---
name: uniprot-database
description: 直接通过REST API访问UniProt。蛋白质搜索、FASTA检索、ID映射、Swiss-Prot/TrEMBL。对于使用多个数据库的Python工作流，建议使用bioservices（40+服务的统一接口）。使用此技能进行直接HTTP/REST工作或UniProt特定控制。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# UniProt数据库

## 概述

UniProt是世界领先的综合性蛋白质序列和功能信息资源。通过名称、基因或登录号搜索蛋白质，以FASTA格式检索序列，在数据库之间执行ID映射，通过REST API访问Swiss-Prot/TrEMBL注释进行蛋白质分析。

## 何时使用此技能

应在以下情况使用此技能：
- 按名称、基因符号、登录号或生物体搜索蛋白质条目
- 以FASTA或其他格式检索蛋白质序列
- 在UniProt和外部数据库（Ensembl、RefSeq、PDB等）之间映射标识符
- 访问包括GO术语、结构域和功能描述在内的蛋白质注释
- 高效批量检索多个蛋白质条目
- 查询已审核（Swiss-Prot）与未审核（TrEMBL）蛋白质数据
- 流式处理大型蛋白质数据集
- 使用特定字段的搜索语法构建自定义查询

## 核心功能

### 1. 搜索蛋白质

使用自然语言查询或结构化搜索语法搜索UniProt。

**常见搜索模式：**
```python
# 按蛋白质名称搜索
query = "insulin AND organism_name:\"Homo sapiens\""

# 按基因名称搜索
query = "gene:BRCA1 AND reviewed:true"

# 按登录号搜索
query = "accession:P12345"

# 按序列长度搜索
query = "length:[100 TO 500]"

# 按分类学搜索
query = "taxonomy_id:9606"  # 人类蛋白质

# 按GO术语搜索
query = "go:0005515"  # 蛋白质结合
```

使用API搜索端点：`https://rest.uniprot.org/uniprotkb/search?query={query}&format={format}`

**支持的格式：** JSON, TSV, Excel, XML, FASTA, RDF, TXT

### 2. 检索单个蛋白质条目

通过登录号检索特定的蛋白质条目。

**登录号格式：**
- 经典：P12345, Q1AAA9, O15530（6个字符：字母+5个字母数字）
- 扩展：A0A022YWF9（较新条目的10个字符）

**检索端点：** `https://rest.uniprot.org/uniprotkb/{accession}.{format}`

示例：`https://rest.uniprot.org/uniprotkb/P12345.fasta`

### 3. 批量检索和ID映射

在不同数据库系统之间映射蛋白质标识符并高效检索多个条目。

**ID映射工作流程：**
1. 提交映射作业至：`https://rest.uniprot.org/idmapping/run`
2. 检查作业状态：`https://rest.uniprot.org/idmapping/status/{jobId}`
3. 检索结果：`https://rest.uniprot.org/idmapping/results/{jobId}`

**支持映射的数据库：**
- UniProtKB AC/ID
- 基因名称
- Ensembl, RefSeq, EMBL
- PDB, AlphaFoldDB
- KEGG, GO术语
- 以及更多（见`/references/id_mapping_databases.md`）

**限制：**
- 每个作业最多100,000个ID
- 结果存储7天

### 4. 流式处理大型结果集

对于超出分页限制的大型查询，使用流端点：

`https://rest.uniprot.org/uniprotkb/stream?query={query}&format={format}`

流端点返回所有结果而不分页，适合下载完整数据集。

### 5. 自定义检索字段

指定要检索的确切字段以实现高效数据传输。

**常见字段：**
- `accession` - UniProt登录号
- `id` - 条目名称
- `gene_names` - 基因名称
- `organism_name` - 生物体
- `protein_name` - 蛋白质名称
- `sequence` - 氨基酸序列
- `length` - 序列长度
- `go_*` - 基因本体论注释
- `cc_*` - 注释字段（功能、相互作用等）
- `ft_*` - 特征注释（结构域、位点等）

**示例：** `https://rest.uniprot.org/uniprotkb/search?query=insulin&fields=accession,gene_names,organism_name,length,sequence&format=tsv`

完整字段列表见`/references/api_fields.md`。

## Python实现

对于编程访问，使用提供的辅助脚本`scripts/uniprot_client.py`，实现：

- `search_proteins(query, format)` - 使用任何查询搜索UniProt
- `get_protein(accession, format)` - 检索单个蛋白质条目
- `map_ids(ids, from_db, to_db)` - 在标识符类型之间映射
- `batch_retrieve(accessions, format)` - 检索多个条目
- `stream_results(query, format)` - 流式处理大型结果集

**替代Python包：**
- **Unipressed**：现代、类型化的UniProt REST API Python客户端
- **bioservices**：全面的生物信息学网络服务客户端

## 查询语法示例

**布尔运算符：**
```
kinase AND organism_name:human
(diabetes OR insulin) AND reviewed:true
cancer NOT lung
```

**特定字段搜索：**
```
gene:BRCA1
accession:P12345
organism_id:9606
taxonomy_name:"Homo sapiens"
annotation:(type:signal)
```

**范围查询：**
```
length:[100 TO 500]
mass:[50000 TO 100000]
```

**通配符：**
```
gene:BRCA*
protein_name:kinase*
```

详细语法文档见`/references/query_syntax.md`。

## 最佳实践

1. **尽可能使用已审核条目**：使用`reviewed:true`过滤Swiss-Prot（人工 curated）条目
2. **明确指定格式**：选择最合适的格式（序列使用FASTA，表格数据使用TSV，程序解析使用JSON）
3. **使用字段选择**：仅请求您需要的字段以减少带宽和处理时间
4. **处理分页**：对于大型结果集，实现适当的分页或使用流端点
5. **缓存结果**：在本地存储频繁访问的数据以最小化API调用
6. **速率限制**：尊重API资源；为大型批处理操作实现延迟
7. **检查数据质量**：TrEMBL条目是计算预测；Swiss-Prot条目是人工审核

## 资源

### scripts/
`uniprot_client.py` - 带有辅助函数的Python客户端，用于常见的UniProt操作，包括搜索、检索、ID映射和流式处理。

### references/
- `api_fields.md` - 用于自定义查询的可用字段完整列表
- `id_mapping_databases.md` - ID映射操作支持的数据库
- `query_syntax.md` - 带有高级示例的综合查询语法
- `api_examples.md` - 多种语言（Python、curl、R）的代码示例

## 其他资源

- **API文档**：https://www.uniprot.org/help/api
- **交互式API浏览器**：https://www.uniprot.org/api-documentation
- **REST教程**：https://www.uniprot.org/help/uniprot_rest_tutorial
- **查询语法帮助**：https://www.uniprot.org/help/query-fields
- **SPARQL端点**：https://sparql.uniprot.org/（用于高级图形查询）