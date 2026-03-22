---
name: ensembl-database
description: 查询 Ensembl 基因组数据库 REST API，支持 250+ 个物种。基因查找、序列检索、变异分析、比较基因组学、直系同源、VEP 预测，用于基因组学研究。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# Ensembl 数据库

## 概述

访问和查询 Ensembl 基因组数据库，这是由 EMBL-EBI 维护的脊椎动物基因组数据综合资源。该数据库为 250 多个物种提供基因注释、序列、变异、调控信息和比较基因组学数据。当前版本是 115（2025 年 9 月）。

## 何时使用此技能

此技能应在以下情况下使用：

- 按符号或 Ensembl ID 查询基因信息
- 检索 DNA、转录本或蛋白质序列
- 使用变异效应预测器（VEP）分析遗传变异
- 跨物种查找直系同源和旁系同源
- 访问调控特征和基因组注释
- 在不同基因组组装之间转换坐标（例如，GRCh37 到 GRCh38）
- 执行比较基因组学分析
- 将 Ensembl 数据集成到基因组学研究管道中

## 核心能力

### 1. 基因信息检索

按符号、Ensembl ID 或外部数据库标识符查询基因数据。

**常见操作：**
- 按符号查找基因信息（例如，"BRCA2"、"TP53"）
- 检索转录本和蛋白质信息
- 获取基因坐标和染色体位置
- 访问外部数据库的交叉引用（UniProt、RefSeq 等）

**使用 ensembl_rest 包：**
```python
from ensembl_rest import EnsemblClient

client = EnsemblClient()

# 按符号查找基因
gene_data = client.symbol_lookup(
    species='human',
    symbol='BRCA2'
)

# 获取详细基因信息
gene_info = client.lookup_id(
    id='ENSG00000139618',  # BRCA2 Ensembl ID
    expand=True
)
```

**直接 REST API（无包）：**
```python
import requests

server = "https://rest.ensembl.org"

# 符号查找
response = requests.get(
    f"{server}/lookup/symbol/homo_sapiens/BRCA2",
    headers={"Content-Type": "application/json"}
)
gene_data = response.json()
```

### 2. 序列检索

以各种格式（JSON、FASTA、纯文本）获取基因组、转录本或蛋白质序列。

**操作：**
- 获取基因或基因组区域的 DNA 序列
- 检索转录本序列（cDNA）
- 访问蛋白质序列
- 提取带有侧翼区域或修饰的序列

**示例：**
```python
# 使用 ensembl_rest 包
sequence = client.sequence_id(
    id='ENSG00000139618',  # 基因 ID
    content_type='application/json'
)

# 获取基因组区域的序列
region_seq = client.sequence_region(
    species='human',
    region='7:140424943-140624564'  # 染色体:起点-终点
)
```

### 3. 变异分析

查询遗传变异数据并使用变异效应预测器（VEP）预测变异后果。

**能力：**
- 按 rsID 或基因组坐标查找变异
- 预测变异的功能后果
- 访问群体频率数据
- 检索表型关联

**VEP 示例：**
```python
# 预测变异后果
vep_result = client.vep_hgvs(
    species='human',
    hgvs_notation='ENST00000380152.7:c.803C>T'
)

# 按 rsID 查询变异
variant = client.variation_id(
    species='human',
    id='rs699'
)
```

### 4. 比较基因组学

执行跨物种比较以识别直系同源、旁系同源和进化关系。

**操作：**
- 查找直系同源（不同物种中的同一基因）
- 识别旁系同源（同一物种中的相关基因）
- 访问显示进化关系的基因树
- 检索基因家族信息

**示例：**
```python
# 查找人类基因的直系同源
orthologs = client.homology_ensemblgene(
    id='ENSG00000139618',  # 人类 BRCA2
    target_species='mouse'
)

# 获取基因树
gene_tree = client.genetree_member_symbol(
    species='human',
    symbol='BRCA2'
)
```

### 5. 基因组区域分析

查找特定区域内的所有基因组特征（基因、转录本、调控元件）。

**用例：**
- 识别染色体区域中的所有基因
- 查找调控特征（启动子、增强子）
- 在区域内定位变异
- 检索结构特征

**示例：**
```python
# 查找区域内的所有特征
features = client.overlap_region(
    species='human',
    region='7:140424943-140624564',
    feature='gene'
)
```

### 6. 组装映射

在不同基因组组装之间转换坐标（例如，GRCh37 到 GRCh38）。

**重要：** 对 GRCh37/hg19 查询使用 `https://grch37.rest.ensembl.org`，对当前组装使用 `https://rest.ensembl.org`。

**示例：**
```python
from ensembl_rest import AssemblyMapper

# 将坐标从 GRCh37 映射到 GRCh38
mapper = AssemblyMapper(
    species='human',
    asm_from='GRCh37',
    asm_to='GRCh38'
)

mapped = mapper.map(chrom='7', start=140453136, end=140453136)
```

## API 最佳实践

### 速率限制

Ensembl REST API 有速率限制。遵循这些实践：

1. **遵守速率限制：** 匿名用户每秒最多 15 个请求
2. **处理 429 响应：** 当速率受限时，检查 `Retry-After` 标头并等待
3. **使用批量端点：** 查询多个项目时，使用可用的批量端点
4. **缓存结果：** 存储频繁访问的数据以减少 API 调用

### 错误处理

始终实施适当的错误处理：

```python
import requests
import time

def query_ensembl(endpoint, params=None, max_retries=3):
    server = "https://rest.ensembl.org"
    headers = {"Content-Type": "application/json"}

    for attempt in range(max_retries):
        response = requests.get(
            f"{server}{endpoint}",
            headers=headers,
            params=params
        )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            # 速率受限 - 等待并重试
            retry_after = int(response.headers.get('Retry-After', 1))
            time.sleep(retry_after)
        else:
            response.raise_for_status()

    raise Exception(f"在 {max_retries} 次尝试后失败")
```

## 安装

### Python 包（推荐）

```bash
uv pip install ensembl_rest
```

`ensembl_rest` 包为所有 Ensembl REST API 端点提供了 Pythonic 接口。

### 直接 REST API

无需安装 - 使用标准 HTTP 库，如 `requests`：

```bash
uv pip install requests
```

## 资源

### references/

- `api_endpoints.md`：所有 17 个 API 端点类别的综合文档，包含示例和参数

### scripts/

- `ensembl_query.py`：用于常见 Ensembl 查询的可重用 Python 脚本，具有内置的速率限制和错误处理

## 常见工作流

### 工作流 1：基因注释管道

1. 按符号查找基因以获取 Ensembl ID
2. 检索转录本信息
3. 获取所有转录本的蛋白质序列
4. 在其他物种中查找直系同源
5. 导出结果

### 工作流 2：变异分析

1. 按 rsID 或坐标查询变异
2. 使用 VEP 预测功能后果
3. 检查群体频率
4. 检索表型关联
5. 生成报告

### 工作流 3：比较分析

1. 从参考物种中的感兴趣基因开始
2. 在目标物种中查找直系同源
3. 检索所有直系同源的序列
4. 比较基因结构和特征
5. 分析进化保守性

## 物种和组装信息

要查询可用的物种和组装：

```python
# 列出所有可用物种
species_list = client.info_species()

# 获取物种的组装信息
assembly_info = client.info_assembly(species='human')
```

常见物种标识符：
- 人类：`homo_sapiens` 或 `human`
- 小鼠：`mus_musculus` 或 `mouse`
- 斑马鱼：`danio_rerio` 或 `zebrafish`
- 果蝇：`drosophila_melanogaster`

## 其他资源

- **官方文档：** https://rest.ensembl.org/documentation
- **Python 包文档：** https://ensemblrest.readthedocs.io
- **EBI 培训：** https://www.ebi.ac.uk/training/online/courses/ensembl-rest-api/
- **Ensembl 浏览器：** https://useast.ensembl.org
- **GitHub 示例：** https://github.com/Ensembl/ensembl-rest/wiki
