---
name: reactome-database
description: 查询Reactome REST API进行通路分析、富集分析、基因-通路映射、疾病通路、分子相互作用、表达分析，用于系统生物学研究。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# Reactome数据库

## 概述

Reactome是一个免费、开源、经过精心策划的通路数据库，包含2,825+人类通路。通过REST API和Python客户端查询生物通路、执行过表达和表达分析、将基因映射到通路、探索分子相互作用，用于系统生物学研究。

## 何时使用此技能

当以下情况时应使用此技能：
- 对基因或蛋白质列表进行通路富集分析
- 分析基因表达数据以识别相关生物通路
- 查询特定通路信息、反应或分子相互作用
- 将基因或蛋白质映射到生物通路和过程
- 探索疾病相关通路和机制
- 在Reactome通路浏览器中可视化分析结果
- 进行跨物种的比较通路分析

## 核心功能

Reactome提供两个主要API服务和一个Python客户端库：

### 1. 内容服务 - 数据检索

查询和检索生物通路数据、分子相互作用和实体信息。

**常见操作：**
- 检索通路信息和层次结构
- 查询特定实体（蛋白质、反应、复合物）
- 获取通路中的参与分子
- 访问数据库版本和元数据
- 探索通路区室和位置

**API基础URL：** `https://reactome.org/ContentService`

### 2. 分析服务 - 通路分析

对基因列表和表达数据执行计算分析。

**分析类型：**
- **过表达分析**：从基因/蛋白质列表中识别统计显著的通路
- **表达数据分析**：分析基因表达数据集以找到相关通路
- **物种比较**：比较不同生物体的通路数据

**API基础URL：** `https://reactome.org/AnalysisService`

### 3. reactome2py Python包

Python客户端库，包装Reactome API调用以实现更简单的编程访问。

**安装：**
```bash
uv pip install reactome2py
```

**注意：** reactome2py包（2021年1月发布的3.0.0版本）功能正常但不再积极维护。对于最新功能，考虑使用直接的REST API调用。

## 查询通路数据

### 使用内容服务REST API

内容服务使用REST协议并以JSON或纯文本格式返回数据。

**获取数据库版本：**
```python
import requests

response = requests.get("https://reactome.org/ContentService/data/database/version")
version = response.text
print(f"Reactome版本: {version}")
```

**查询特定实体：**
```python
import requests

entity_id = "R-HSA-69278"  # 示例通路ID
response = requests.get(f"https://reactome.org/ContentService/data/query/{entity_id}")
data = response.json()
```

**获取通路中的参与分子：**
```python
import requests

event_id = "R-HSA-69278"
response = requests.get(
    f"https://reactome.org/ContentService/data/event/{event_id}/participatingPhysicalEntities"
)
molecules = response.json()
```

### 使用reactome2py包

```python
import reactome2py
from reactome2py import content

# 查询通路信息
pathway_info = content.query_by_id("R-HSA-69278")

# 获取数据库版本
version = content.get_database_version()
```

**详细API端点和参数**，请参阅此技能中的 `references/api_reference.md`。

## 执行通路分析

### 过表达分析

提交基因/蛋白质标识符列表以找到富集的通路。

**使用REST API：**
```python
import requests

# 准备标识符列表
identifiers = ["TP53", "BRCA1", "EGFR", "MYC"]
data = "\n".join(identifiers)

# 提交分析
response = requests.post(
    "https://reactome.org/AnalysisService/identifiers/",
    headers={"Content-Type": "text/plain"},
    data=data
)

result = response.json()
token = result["summary"]["token"]  # 保存令牌以便稍后检索结果

# 访问通路
for pathway in result["pathways"]:
    print(f"{pathway['stId']}: {pathway['name']} (p值: {pathway['entities']['pValue']})")
```

**通过令牌检索分析：**
```python
# 令牌有效期为7天
response = requests.get(f"https://reactome.org/AnalysisService/token/{token}")
results = response.json()
```

### 表达数据分析

分析具有定量值的基因表达数据集。

**输入格式（带#开头的TSV表头）：**
```
#Gene	Sample1	Sample2	Sample3
TP53	2.5	3.1	2.8
BRCA1	1.2	1.5	1.3
EGFR	4.5	4.2	4.8
```

**提交表达数据：**
```python
import requests

# 读取TSV文件
with open("expression_data.tsv", "r") as f:
    data = f.read()

response = requests.post(
    "https://reactome.org/AnalysisService/identifiers/",
    headers={"Content-Type": "text/plain"},
    data=data
)

result = response.json()
```

### 物种投影

使用`/projection/`端点将标识符专门映射到人类通路：

```python
response = requests.post(
    "https://reactome.org/AnalysisService/identifiers/projection/",
    headers={"Content-Type": "text/plain"},
    data=data
)
```

## 可视化结果

分析结果可以通过使用分析令牌构建URL在Reactome通路浏览器中可视化：

```python
token = result["summary"]["token"]
pathway_id = "R-HSA-69278"
url = f"https://reactome.org/PathwayBrowser/#{pathway_id}&DTAB=AN&ANALYSIS={token}"
print(f"查看结果: {url}")
```

## 使用分析令牌

- 分析令牌有效期为**7天**
- 令牌允许检索先前计算的结果而无需重新提交
- 存储令牌以在会话间访问结果
- 使用`GET /token/{TOKEN}`端点检索结果

## 数据格式和标识符

### 支持的标识符类型

Reactome接受各种标识符格式：
- UniProt访问码（例如，P04637）
- 基因符号（例如，TP53）
- Ensembl ID（例如，ENSG00000141510）
- EntrezGene ID（例如，7157）
- 小分子的ChEBI ID

系统会自动检测标识符类型。

### 输入格式要求

**对于过表达分析：**
- 纯文本标识符列表（每行一个）
- 或TSV格式的单列

**对于表达分析：**
- TSV格式，强制表头行以"#"开头
- 第1列：标识符
- 第2+列：数值表达值
- 使用点（.）作为小数分隔符

### 输出格式

所有API响应返回包含以下内容的JSON：
- `pathways`：带有统计指标的富集通路数组
- `summary`：分析元数据和令牌
- `entities`：匹配和未映射的标识符
- 统计值：pValue、FDR（错误发现率）

## 辅助脚本

此技能包含`scripts/reactome_query.py`，一个用于常见Reactome操作的辅助脚本：

```bash
# 查询通路信息
python scripts/reactome_query.py query R-HSA-69278

# 执行过表达分析
python scripts/reactome_query.py analyze gene_list.txt

# 获取数据库版本
python scripts/reactome_query.py version
```

## 额外资源

- **API文档**：https://reactome.org/dev
- **用户指南**：https://reactome.org/userguide
- **文档门户**：https://reactome.org/documentation
- **数据下载**：https://reactome.org/download-data
- **reactome2py文档**：https://reactome.github.io/reactome2py/

有关全面的API端点文档，请参阅此技能中的 `references/api_reference.md`。

## 当前数据库统计（2025年9月版本94）

- 2,825个人类通路
- 16,002个反应
- 11,630个蛋白质
- 2,176个小分子
- 1,070种药物
- 41,373个文献引用