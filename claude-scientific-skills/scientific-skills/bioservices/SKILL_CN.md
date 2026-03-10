---
name: bioservices
description: 统一的 Python 接口，用于访问 40 多个生物信息学服务。在单个工作流程中使用一致的 API 查询多个数据库（UniProt、KEGG、ChEMBL、Reactome）时使用。最适合跨数据库分析、跨服务 ID 映射。对于快速单数据库查找使用 gget；对于序列/文件操作使用 biopython。
license: GPLv3 license
metadata:
    skill-author: K-Dense Inc.
---

# BioServices

## 概述

BioServices 是一个 Python 包，提供对大约 40 个生物信息学 Web 服务和数据库的程序化访问。在 Python 工作流程中检索生物数据、执行跨数据库查询、映射标识符、分析序列并集成多个生物资源。该包透明地处理 REST 和 SOAP/WSDL 协议。

## 何时使用此技能

在以下情况应使用此技能：
- 从 UniProt、PDB、Pfam 检索蛋白质序列、注释或结构
- 通过 KEGG 或 Reactome 分析代谢途径和基因功能
- 搜索化合物数据库（ChEBI、ChEMBL、PubChem）以获取化学信息
- 在不同生物数据库之间转换标识符（KEGG↔UniProt、化合物 ID）
- 运行序列相似性搜索（BLAST、MUSCLE 比对）
- 查询基因本体术语（QuickGO、GO 注释）
- 访问蛋白质-蛋白质相互作用数据（PSICQUIC、IntactComplex）
- 挖掘基因组数据（BioMart、ArrayExpress、ENA）
- 在单个工作流程中集成来自多个生物信息学资源的数据

## 核心能力

### 1. 蛋白质分析

检索蛋白质信息、序列和功能注释：

```python
from bioservices import UniProt

u = UniProt(verbose=False)

# 按名称搜索蛋白质
results = u.search("ZAP70_HUMAN", frmt="tab", columns="id,genes,organism")

# 检索 FASTA 序列
sequence = u.retrieve("P43403", "fasta")

# 在数据库之间映射标识符
kegg_ids = u.mapping(fr="UniProtKB_AC-ID", to="KEGG", query="P43403")
```

**关键方法：**
- `search()`：使用灵活的搜索词查询 UniProt
- `retrieve()`：以各种格式（FASTA、XML、tab）获取蛋白质条目
- `mapping()`：在数据库之间转换标识符

参考：`references/services_reference.md` 获取完整的 UniProt API 详细信息。

### 2. 途径发现和分析

访问 KEGG 途径信息以获取基因和生物体：

```python
from bioservices import KEGG

k = KEGG()
k.organism = "hsa"  # 设置为人类

# 搜索生物体
k.lookfor_organism("droso")  # 查找果蝇物种

# 按名称查找途径
k.lookfor_pathway("B cell")  # 返回匹配的途径 ID

# 获取包含特定基因的途径
pathways = k.get_pathway_by_gene("7535", "hsa")  # ZAP70 基因

# 检索和解析途径数据
data = k.get("hsa04660")
parsed = k.parse(data)

# 提取途径相互作用
interactions = k.parse_kgml_pathway("hsa04660")
relations = interactions['relations']  # 蛋白质-蛋白质相互作用

# 转换为简单相互作用格式
sif_data = k.pathway2sif("hsa04660")
```

**关键方法：**
- `lookfor_organism()`、`lookfor_pathway()`：按名称搜索
- `get_pathway_by_gene()`：查找包含基因的途径
- `parse_kgml_pathway()`：提取结构化途径数据
- `pathway2sif()`：获取蛋白质相互作用网络

参考：`references/workflow_patterns.md` 获取完整的途径分析工作流程。

### 3. 化合物数据库搜索

在多个数据库中搜索和交叉引用化合物：

```python
from bioservices import KEGG, UniChem

k = KEGG()

# 按名称搜索化合物
results = k.find("compound", "Geldanamycin")  # 返回 cpd:C11222

# 获取包含数据库链接的化合物信息
compound_info = k.get("cpd:C11222")  # 包括 ChEBI 链接

# 使用 UniChem 进行 KEGG → ChEMBL 映射
u = UniChem()
chembl_id = u.get_compound_id_from_kegg("C11222")  # 返回 CHEMBL278315
```

**常见工作流程：**
1. 在 KEGG 中按名称搜索化合物
2. 提取 KEGG 化合物 ID
3. 使用 UniChem 进行 KEGG → ChEMBL 映射
4. ChEBI ID 通常在 KEGG 条目中提供

参考：`references/identifier_mapping.md` 获取完整的跨数据库映射指南。

### 4. 序列分析

运行 BLAST 搜索和序列比对：

```python
from bioservices import NCBIblast

s = NCBIblast(verbose=False)

# 针对 UniProtKB 运行 BLASTP
jobid = s.run(
    program="blastp",
    sequence=protein_sequence,
    stype="protein",
    database="uniprotkb",
    email="your.email@example.com"  # NCBI 要求
)

# 检查作业状态并检索结果
s.getStatus(jobid)
results = s.getResult(jobid, "out")
```

**注意：** BLAST 作业是异步的。在检索结果之前检查状态。

### 5. 标识符映射

在不同生物数据库之间转换标识符：

```python
from bioservices import UniProt, KEGG

# UniProt 映射（支持许多数据库对）
u = UniProt()
results = u.mapping(
    fr="UniProtKB_AC-ID",  # 源数据库
    to="KEGG",              # 目标数据库
    query="P43403"          # 要转换的标识符
)

# KEGG 基因 ID → UniProt
kegg_to_uniprot = u.mapping(fr="KEGG", to="UniProtKB_AC-ID", query="hsa:7535")

# 对于化合物，使用 UniChem
from bioservices import UniChem
u = UniChem()
chembl_from_kegg = u.get_compound_id_from_kegg("C11222")
```

**支持的映射（UniProt）：**
- UniProtKB ↔ KEGG
- UniProtKB ↔ Ensembl
- UniProtKB ↔ PDB
- UniProtKB ↔ RefSeq
- 以及更多（参见 `references/identifier_mapping.md`）

### 6. 基因本体查询

访问 GO 术语和注释：

```python
from bioservices import QuickGO

g = QuickGO(verbose=False)

# 检索 GO 术语信息
term_info = g.Term("GO:0003824", frmt="obo")

# 搜索注释
annotations = g.Annotation(protein="P43403", format="tsv")
```

### 7. 蛋白质-蛋白质相互作用

通过 PSICQUIC 查询相互作用数据库：

```python
from bioservices import PSICQUIC

s = PSICQUIC(verbose=False)

# 查询特定数据库（例如，MINT）
interactions = s.query("mint", "ZAP70 AND species:9606")

# 列出可用的相互作用数据库
databases = s.activeDBs
```

**可用数据库：** MINT、IntAct、BioGRID、DIP 和 30 多个其他数据库。

## 多服务集成工作流程

BioServices 擅长于结合多个服务进行综合分析。常见的集成模式：

### 完整蛋白质分析流程

执行完整的蛋白质表征工作流程：

```bash
python scripts/protein_analysis_workflow.py ZAP70_HUMAN your.email@example.com
```

此脚本演示：
1. UniProt 搜索蛋白质条目
2. FASTA 序列检索
3. BLAST 相似性搜索
4. KEGG 途径发现
5. PSICQUIC 相互作用映射

### 途径网络分析

分析生物体的所有途径：

```bash
python scripts/pathway_analysis.py hsa output_directory/
```

提取和分析：
- 生物体的所有途径 ID
- 每个途径的蛋白质-蛋白质相互作用
- 相互作用类型分布
- 导出到 CSV/SIF 格式

### 跨数据库化合物搜索

跨数据库映射化合物标识符：

```bash
python scripts/compound_cross_reference.py Geldanamycin
```

检索：
- KEGG 化合物 ID
- ChEBI 标识符
- ChEMBL 标识符
- 基本化合物属性

### 批量标识符转换

一次转换多个标识符：

```bash
python scripts/batch_id_converter.py input_ids.txt --from UniProtKB_AC-ID --to KEGG
```

## 最佳实践

### 输出格式处理

不同的服务以各种格式返回数据：
- **XML**：使用 BeautifulSoup 解析（大多数 SOAP 服务）
- **制表符分隔（TSV）**：用于表格数据的 Pandas DataFrame
- **字典/JSON**：直接 Python 操作
- **FASTA**：用于序列分析的 BioPython 集成

### 速率限制和详细程度

控制 API 请求行为：

```python
from bioservices import KEGG

k = KEGG(verbose=False)  # 抑制 HTTP 请求详细信息
k.TIMEOUT = 30  # 为慢速连接调整超时
```

### 错误处理

将服务调用包装在 try-except 块中：

```python
try:
    results = u.search("ambiguous_query")
    if results:
        # 处理结果
        pass
except Exception as e:
    print(f"Search failed: {e}")
```

### 生物体代码

使用标准生物体缩写：
- `hsa`：智人（人类）
- `mmu`：小家鼠（小鼠）
- `dme`：黑腹果蝇
- `sce`：酿酒酵母

列出所有生物体：`k.list("organism")` 或 `k.organismIds`

### 与其他工具集成

BioServices 与以下工具配合良好：
- **BioPython**：对检索的 FASTA 数据进行序列分析
- **Pandas**：表格数据操作
- **PyMOL**：3D 结构可视化（检索 PDB ID）
- **NetworkX**：途径相互作用的网络分析
- **Galaxy**：工作流程平台的自定义工具包装器

## 资源

### scripts/

演示完整工作流程的可执行 Python 脚本：

- `protein_analysis_workflow.py`：端到端蛋白质表征
- `pathway_analysis.py`：KEGG 途径发现和网络提取
- `compound_cross_reference.py`：多数据库化合物搜索
- `batch_id_converter.py`：批量标识符映射实用程序

脚本可以直接执行或针对特定用例进行调整。

### references/

根据需要加载的详细文档：

- `services_reference.md`：所有 40 多个服务及其方法的综合列表
- `workflow_patterns.md`：详细的多步骤分析工作流程
- `identifier_mapping.md`：跨数据库 ID 转换的完整指南

在使用特定服务或复杂集成任务时加载参考。

## 安装

```bash
uv pip install bioservices
```

依赖项自动管理。软件包在 Python 3.9-3.12 上测试。

## 其他信息

有关详细的 API 文档和高级功能，请参阅：
- 官方文档：https://bioservices.readthedocs.io/
- 源代码：https://github.com/cokelaer/bioservices
- `references/services_reference.md` 中的服务特定参考
