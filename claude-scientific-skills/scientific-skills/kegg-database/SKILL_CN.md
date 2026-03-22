---
name: kegg-database
description: KEGG的直接REST API访问（仅学术使用）。通路分析、基因-通路映射、代谢通路、药物相互作用、ID转换。对于具有多个数据库的Python工作流，首选bioservices。对于直接HTTP/REST工作或KEGG特定控制使用此技能。
license: KEGG的非学术使用需要商业许可证
metadata:
    skill-author: K-Dense Inc.
---

# KEGG数据库

## 概述

KEGG（京都基因与基因组百科全书）是生物通路分析和分子相互作用网络的综合生物信息学资源。

**重要：** KEGG API仅提供给学术用户用于学术使用。

## 何时使用此技能

当使用KEGG的REST API跨多个生物体查询通路、基因、化合物、酶、疾病和药物时，应使用此技能。

## 快速开始

此技能提供：
1. 用于所有KEGG REST API操作的Python辅助函数（`scripts/kegg_api.py`）
2. 综合参考文档（`references/kegg_reference.md`），包含详细的API规范

当用户请求KEGG数据时，确定需要哪种操作并使用`scripts/kegg_api.py`中的适当函数。

## 核心操作

### 1. 数据库信息（`kegg_info`）

检索KEGG数据库的元数据和统计信息。

**何时使用：** 理解数据库结构、检查可用数据、获取发布信息。

**用法：**
```python
from scripts.kegg_api import kegg_info

# 获取通路数据库信息
info = kegg_info('pathway')

# 获取生物体特定信息
hsa_info = kegg_info('hsa')  # 人类基因组
```

**常用数据库：** `kegg`、`pathway`、`module`、`brite`、`genes`、`genome`、`compound`、`glycan`、`reaction`、`enzyme`、`disease`、`drug`

### 2. 列出条目（`kegg_list`）

从KEGG数据库列出条目标识符和名称。

**何时使用：** 获取生物体的所有通路、列出基因、检索化合物目录。

**用法：**
```python
from scripts.kegg_api import kegg_list

# 列出所有参考通路
pathways = kegg_list('pathway')

# 列出人类特定通路
hsa_pathways = kegg_list('pathway', 'hsa')

# 列出特定基因（最多10个）
genes = kegg_list('hsa:10458+hsa:10459')
```

**常用生物体代码：** `hsa`（人类）、`mmu`（小鼠）、`dme`（果蝇）、`sce`（酵母）、`eco`（大肠杆菌）

### 3. 搜索（`kegg_find`）

按关键词或分子属性搜索KEGG数据库。

**何时使用：** 按名称/描述查找基因、按分子式或质量搜索化合物、通过关键词发现条目。

**用法：**
```python
from scripts.kegg_api import kegg_find

# 关键词搜索
results = kegg_find('genes', 'p53')
shiga_toxin = kegg_find('genes', 'shiga toxin')

# 化学式搜索（精确匹配）
compounds = kegg_find('compound', 'C7H10N4O2', 'formula')

# 分子量范围搜索
drugs = kegg_find('drug', '300-310', 'exact_mass')
```

**搜索选项：** `formula`（精确匹配）、`exact_mass`（范围）、`mol_weight`（范围）

### 4. 检索条目（`kegg_get`）

获取完整的数据库条目或特定数据格式。

**何时使用：** 检索通路详情、获取基因/蛋白质序列、下载通路图、访问化合物结构。

**用法：**
```python
from scripts.kegg_api import kegg_get

# 获取通路条目
pathway = kegg_get('hsa00010')  # 糖酵解通路

# 获取多个条目（最多10个）
genes = kegg_get(['hsa:10458', 'hsa:10459'])

# 获取蛋白质序列（FASTA）
sequence = kegg_get('hsa:10458', 'aaseq')

# 获取核苷酸序列
nt_seq = kegg_get('hsa:10458', 'ntseq')

# 获取化合物结构
mol_file = kegg_get('cpd:C00002', 'mol')  # ATP的MOL格式

# 获取通路为JSON（仅单个条目）
pathway_json = kegg_get('hsa05130', 'json')

# 获取通路为图像（仅单个条目）
pathway_img = kegg_get('hsa05130', 'image')
```

**输出格式：** `aaseq`（蛋白质FASTA）、`ntseq`（核苷酸FASTA）、`mol`（MOL格式）、`kcf`（KCF格式）、`image`（PNG）、`kgml`（XML）、`json`（通路JSON）

**重要：** 图像、KGML和JSON格式仅允许一次一个条目。

### 5. ID转换（`kegg_conv`）

在KEGG和外部数据库之间转换标识符。

**何时使用：** 将KEGG数据与其他数据库集成、映射基因ID、转换化合物标识符。

**用法：**
```python
from scripts.kegg_api import kegg_conv

# 将所有人类基因转换为NCBI基因ID
conversions = kegg_conv('ncbi-geneid', 'hsa')

# 转换特定基因
gene_id = kegg_conv('ncbi-geneid', 'hsa:10458')

# 转换为UniProt
uniprot_id = kegg_conv('uniprot', 'hsa:10458')

# 将化合物转换为PubChem
pubchem_ids = kegg_conv('pubchem', 'compound')

# 反向转换（NCBI基因ID到KEGG）
kegg_id = kegg_conv('hsa', 'ncbi-geneid')
```

**支持的转换：** `ncbi-geneid`、`ncbi-proteinid`、`uniprot`、`pubchem`、`chebi`

### 6. 交叉引用（`kegg_link`）

在KEGG数据库内部和之间查找相关条目。

**何时使用：** 查找包含基因的通路、获取通路中的基因、将基因映射到KO组、查找通路中的化合物。

**用法：**
```python
from scripts.kegg_api import kegg_link

# 查找与人类基因链接的通路
pathways = kegg_link('pathway', 'hsa')

# 获取特定通路中的基因
genes = kegg_link('genes', 'hsa00010')  # 糖酵解基因

# 查找包含特定基因的通路
gene_pathways = kegg_link('pathway', 'hsa:10458')

# 查找通路中的化合物
compounds = kegg_link('compound', 'hsa00010')

# 将基因映射到KO（同源）组
ko_groups = kegg_link('ko', 'hsa:10458')
```

**常用链接：** genes ↔ pathway、pathway ↔ compound、pathway ↔ enzyme、genes ↔ ko（同源）

### 7. 药物-药物相互作用（`kegg_ddi`）

检查药物-药物相互作用。

**何时使用：** 分析药物组合、检查禁忌症、药理学研究。

**用法：**
```python
from scripts.kegg_api import kegg_ddi

# 检查单个药物
interactions = kegg_ddi('D00001')

# 检查多个药物（最多10个）
interactions = kegg_ddi(['D00001', 'D00002', 'D00003'])
```

## 常见分析工作流程

### 工作流程1：基因到通路映射

**用例：** 查找与感兴趣的基因关联的通路（例如，用于通路富集分析）。

```python
from scripts.kegg_api import kegg_find, kegg_link, kegg_get

# 步骤1：按名称查找基因ID
gene_results = kegg_find('genes', 'p53')

# 步骤2：将基因链接到通路
pathways = kegg_link('pathway', 'hsa:7157')  # TP53基因

# 步骤3：获取详细通路信息
for pathway_line in pathways.split('\n'):
    if pathway_line:
        pathway_id = pathway_line.split('\t')[1].replace('path:', '')
        pathway_info = kegg_get(pathway_id)
        # 处理通路信息
```

### 工作流程2：通路富集背景

**用例：** 获取生物体通路中的所有基因以进行富集分析。

```python
from scripts.kegg_api import kegg_list, kegg_link

# 步骤1：列出所有人类通路
pathways = kegg_list('pathway', 'hsa')

# 步骤2：对于每个通路，获取关联的基因
for pathway_line in pathways.split('\n'):
    if pathway_line:
        pathway_id = pathway_line.split('\t')[0]
        genes = kegg_link('genes', pathway_id)
        # 处理基因以进行富集分析
```

### 工作流程3：化合物到通路分析

**用例：** 查找包含感兴趣化合物的代谢通路。

```python
from scripts.kegg_api import kegg_find, kegg_link, kegg_get

# 步骤1：搜索化合物
compound_results = kegg_find('compound', 'glucose')

# 步骤2：将化合物链接到反应
reactions = kegg_link('reaction', 'cpd:C00031')  # 葡萄糖

# 步骤3：将反应链接到通路
pathways = kegg_link('pathway', 'rn:R00299')  # 特定反应

# 步骤4：获取通路详情
pathway_info = kegg_get('map00010')  # 糖酵解
```

### 工作流程4：跨数据库集成

**用例：** 将KEGG数据与UniProt、NCBI或PubChem数据库集成。

```python
from scripts.kegg_api import kegg_conv, kegg_get

# 步骤1：将KEGG基因ID转换为外部数据库ID
uniprot_map = kegg_conv('uniprot', 'hsa')
ncbi_map = kegg_conv('ncbi-geneid', 'hsa')

# 步骤2：解析转换结果
for line in uniprot_map.split('\n'):
    if line:
        kegg_id, uniprot_id = line.split('\t')
        # 使用外部ID进行集成

# 步骤3：使用KEGG获取序列
sequence = kegg_get('hsa:10458', 'aaseq')
```

### 工作流程5：生物体特定通路分析

**用例：** 比较不同生物体的通路。

```python
from scripts.kegg_api import kegg_list, kegg_get

# 步骤1：列出多个生物体的通路
human_pathways = kegg_list('pathway', 'hsa')
mouse_pathways = kegg_list('pathway', 'mmu')
yeast_pathways = kegg_list('pathway', 'sce')

# 步骤2：获取参考通路以进行比较
ref_pathway = kegg_get('map00010')  # 参考糖酵解

# 步骤3：获取生物体特定版本
hsa_glycolysis = kegg_get('hsa00010')
mmu_glycolysis = kegg_get('mmu00010')
```

## 通路类别

KEGG将通路组织为七个主要类别。在解释通路ID或向用户推荐通路时：

1. **代谢**（例如，`map00010` - 糖酵解、`map00190` - 氧化磷酸化）
2. **遗传信息处理**（例如，`map03010` - 核糖体、`map03040` - 剪接体）
3. **环境信息处理**（例如，`map04010` - MAPK信号传导、`map02010` - ABC转运蛋白）
4. **细胞过程**（例如，`map04140` - 自噬、`map04210` - 细胞凋亡）
5. **生物体系统**（例如，`map04610` - 补体级联、`map04910` - 胰岛素信号传导）
6. **人类疾病**（例如，`map05200` - 癌症通路、`map05010` - 阿尔茨海默病）
7. **药物开发**（按时间顺序和基于靶点的分类）

有关详细通路列表和分类，请参考`references/kegg_reference.md`。

## 重要标识符和格式

### 通路ID
- `map#####` - 参考通路（通用，非生物体特定）
- `hsa#####` - 人类通路
- `mmu#####` - 小鼠通路

### 基因ID
- 格式：`organism:gene_number`（例如，`hsa:10458`）

### 化合物ID
- 格式：`cpd:C#####`（例如，`cpd:C00002`表示ATP）

### 药物ID
- 格式：`dr:D#####`（例如，`dr:D00001`）

### 酶ID
- 格式：`ec:EC_number`（例如，`ec:1.1.1.1`）

### KO（KEGG同源）ID
- 格式：`ko:K#####`（例如，`ko:K00001`）

## API限制

使用KEGG API时请遵守这些约束：

1. **条目限制：** 每次操作最多10个条目（图像/kgml/json：仅1个条目）
2. **学术使用：** API仅用于学术使用；商业使用需要许可
3. **HTTP状态代码：** 检查200（成功）、400（错误请求）、404（未找到）
4. **速率限制：** 无明确限制，但避免快速连续请求

## 详细参考

有关全面的API文档、数据库规范、生物体代码和高级用法，请参阅`references/kegg_reference.md`。这包括：

- KEGG数据库的完整列表
- 详细的API操作语法
- 所有生物体代码
- HTTP状态代码和错误处理
- 与Biopython和R/Bioconductor的集成
- API使用的最佳实践

## 故障排除

**404未找到：** 条目或数据库不存在；验证ID和生物体代码
**400错误请求：** API调用中的语法错误；检查参数格式
**空结果：** 搜索词可能不匹配条目；尝试更广泛的关键词
**图像/KGML错误：** 这些格式仅适用于单个条目；删除批量处理

## 其他工具

用于交互式通路可视化和注释：
- **KEGG Mapper**：https://www.kegg.jp/kegg/mapper/
- **BlastKOALA**：自动化基因组注释
- **GhostKOALA**：宏基因组/宏转录组注释
