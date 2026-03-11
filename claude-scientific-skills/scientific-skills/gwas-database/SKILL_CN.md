---
name: gwas-database
description: 查询NHGRI-EBI GWAS目录获取SNP-性状关联。按rs ID、疾病/性状、基因搜索变体，检索p值和汇总统计，用于遗传流行病学和多基因风险评分。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# GWAS 目录数据库

## 概述

GWAS目录是由国家人类基因组研究所（NHGRI）和欧洲生物信息学研究所（EBI）维护的已发表全基因组关联研究的综合存储库。该目录包含来自数千个GWAS发表的精选SNP-性状关联，包括遗传变体、相关性状和疾病、p值、效应大小，以及许多研究的完整汇总统计。

## 何时使用此技能

此技能应在以下情况下使用：

- **遗传变体关联：** 查找与疾病或性状相关的SNP
- **SNP查找：** 检索特定遗传变体（rs ID）的信息
- **性状/疾病搜索：** 发现表型的遗传关联
- **基因关联：** 查找特定基因内或附近的变体
- **GWAS汇总统计：** 访问完整的全基因组关联数据
- **研究元数据：** 检索发表和队列信息
- **群体遗传学：** 探索祖先特异性关联
- **多基因风险评分：** 识别风险预测模型的变体
- **功能基因组学：** 理解变体效应和基因组背景
- **系统评价：** 遗传关联的全面文献综合

## 核心功能

### 1. 理解GWAS目录数据结构

GWAS目录围绕四个核心实体组织：

- **研究：** 具有元数据（PMID、作者、队列详情）的GWAS发表
- **关联：** 具有统计证据（p ≤ 5×10⁻⁸）的SNP-性状关联
- **变体：** 具有基因组坐标和等位基因的遗传标记（SNP）
- **性状：** 表型和疾病（映射到EFO本体术语）

**关键标识符：**
- 研究访问号：`GCST` ID（例如GCST001234）
- 变体ID：`rs`编号（例如rs7903146）或`variant_id`格式
- 性状ID：EFO术语（例如EFO_0001360用于2型糖尿病）
- 基因符号：HGNC批准的名称（例如TCF7L2）

### 2. Web界面搜索

位于https://www.ebi.ac.uk/gwas/的Web界面支持多种搜索模式：

**按变体（rs ID）：**
```
rs7903146
```
返回此SNP的所有性状关联。

**按疾病/性状：**
```
type 2 diabetes
Parkinson disease
body mass index
```
返回所有相关遗传变体。

**按基因：**
```
APOE
TCF7L2
```
返回基因区域内的变体。

**按染色体区域：**
```
10:114000000-115000000
```
返回指定基因组区间内的变体。

**按发表：**
```
PMID:20581827
作者: McCarthy MI
GCST001234
```
返回研究详情和所有报告的关联。

### 3. REST API 访问

GWAS目录提供两个REST API用于程序化访问：

**基础URL：**
- GWAS目录API：`https://www.ebi.ac.uk/gwas/rest/api`
- 汇总统计API：`https://www.ebi.ac.uk/gwas/summary-statistics/api`

**API文档：**
- 主要API文档：https://www.ebi.ac.uk/gwas/rest/docs/api
- 汇总统计文档：https://www.ebi.ac.uk/gwas/summary-statistics/docs/

**核心端点：**

1. **研究端点** - `/studies/{accessionID}`
   ```python
   import requests

   # 获取特定研究
   url = "https://www.ebi.ac.uk/gwas/rest/api/studies/GCST001795"
   response = requests.get(url, headers={"Content-Type": "application/json"})
   study = response.json()
   ```

2. **关联端点** - `/associations`
   ```python
   # 查找变体的关联
   variant = "rs7903146"
   url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{variant}/associations"
   params = {"projection": "associationBySnp"}
   response = requests.get(url, params=params, headers={"Content-Type": "application/json"})
   associations = response.json()
   ```

3. **变体端点** - `/singleNucleotidePolymorphisms/{rsID}`
   ```python
   # 获取变体详情
   url = "https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/rs7903146"
   response = requests.get(url, headers={"Content-Type": "application/json"})
   variant_info = response.json()
   ```

4. **性状端点** - `/efoTraits/{efoID}`
   ```python
   # 获取性状信息
   url = "https://www.ebi.ac.uk/gwas/rest/api/efoTraits/EFO_0001360"
   response = requests.get(url, headers={"Content-Type": "application/json"})
   trait_info = response.json()
   ```

### 4. 查询示例和模式

**示例1：查找疾病的所有关联**
```python
import requests

trait = "EFO_0001360"  # 2型糖尿病
base_url = "https://www.ebi.ac.uk/gwas/rest/api"

# 查询此性状的关联
url = f"{base_url}/efoTraits/{trait}/associations"
response = requests.get(url, headers={"Content-Type": "application/json"})
associations = response.json()

# 处理结果
for assoc in associations.get('_embedded', {}).get('associations', []):
    variant = assoc.get('rsId')
    pvalue = assoc.get('pvalue')
    risk_allele = assoc.get('strongestAllele')
    print(f"{variant}: p={pvalue}, 风险等位基因={risk_allele}")
```

**示例2：获取变体信息和所有性状关联**
```python
import requests

variant = "rs7903146"
base_url = "https://www.ebi.ac.uk/gwas/rest/api"

# 获取变体详情
url = f"{base_url}/singleNucleotidePolymorphisms/{variant}"
response = requests.get(url, headers={"Content-Type": "application/json"})
variant_data = response.json()

# 获取此变体的所有关联
url = f"{base_url}/singleNucleotidePolymorphisms/{variant}/associations"
params = {"projection": "associationBySnp"}
response = requests.get(url, params=params, headers={"Content-Type": "application/json"})
associations = response.json()

# 提取性状名称和p值
for assoc in associations.get('_embedded', {}).get('associations', []):
    trait = assoc.get('efoTrait')
    pvalue = assoc.get('pvalue')
    print(f"性状: {trait}, p值: {pvalue}")
```

**示例3：访问汇总统计**
```python
import requests

# 查询汇总统计API
base_url = "https://www.ebi.ac.uk/gwas/summary-statistics/api"

# 按性状和p值阈值查找关联
trait = "EFO_0001360"  # 2型糖尿病
p_upper = "0.000000001"  # p < 1e-9
url = f"{base_url}/traits/{trait}/associations"
params = {
    "p_upper": p_upper,
    "size": 100  # 结果数
}
response = requests.get(url, params=params)
results = response.json()

# 处理全基因组显著命中
for hit in results.get('_embedded', {}).get('associations', []):
    variant_id = hit.get('variant_id')
    chromosome = hit.get('chromosome')
    position = hit.get('base_pair_location')
    pvalue = hit.get('p_value')
    print(f"{chromosome}:{position} ({variant_id}): p={pvalue}")
```

**示例4：按染色体区域查询**
```python
import requests

# 查找特定基因组区域中的变体
chromosome = "10"
start_pos = 114000000
end_pos = 115000000

base_url = "https://www.ebi.ac.uk/gwas/rest/api"
url = f"{base_url}/singleNucleotidePolymorphisms/search/findByChromBpLocationRange"
params = {
    "chrom": chromosome,
    "bpStart": start_pos,
    "bpEnd": end_pos
}
response = requests.get(url, params=params, headers={"Content-Type": "application/json"})
variants_in_region = response.json()
```

### 5. 使用汇总统计

GWAS目录为许多研究提供完整汇总统计，提供对所有测试变体（不仅仅是全基因组显著命中）的访问。

**访问方法：**
1. **FTP下载**：http://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/
2. **REST API**：基于查询的汇总统计访问
3. **Web界面**：通过网站浏览和下载

**汇总统计API功能：**
- 按染色体、位置、p值过滤
- 跨研究查询特定变体
- 检索效应大小和等位基因频率
- 访问标准化和标准化数据

**示例：下载研究汇总统计**
```python
import requests
import gzip

# 获取可用汇总统计
base_url = "https://www.ebi.ac.uk/gwas/summary-statistics/api"
url = f"{base_url}/studies/GCST001234"
response = requests.get(url)
study_info = response.json()

# 下载链接在响应中提供
# 或者，使用FTP：
# ftp://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/GCSTXXXXXX/
```

### 6. 数据集成和交叉引用

GWAS目录提供到外部资源的链接：

**基因组数据库：**
- Ensembl：基因注释和变体后果
- dbSNP：变体标识符和群体频率
- gnomAD：群体等位基因频率

**功能资源：**
- Open Targets：靶点-疾病关联
- PGS目录：多基因风险评分
- UCSC基因组浏览器：基因组背景

**表型资源：**
- EFO（实验因子本体）：标准化性状术语
- OMIM：疾病基因关系
- 疾病本体：疾病层次结构

**在API响应中跟踪链接：**
```python
import requests

# API响应包含相关资源的_links
response = requests.get("https://www.ebi.ac.uk/gwas/rest/api/studies/GCST001234")
study = response.json()

# 跟随链接到关联
associations_url = study['_links']['associations']['href']
associations_response = requests.get(associations_url)
```

## 查询工作流

### 工作流1：通过eQTL解释GWAS变体

1. **识别GWAS变体**（rs ID或染色体位置）
2. **转换为GTEx变体ID格式**（`chr{chrom}_{pos}_{ref}_{alt}_b38`）
3. **跨组织查询所有eQTL关联**
4. **检查效应方向**：GWAS风险等位基因是否与eQTL效应等位基因相同？
5. **优先考虑组织**：选择与疾病生物学相关的组织
6. **考虑共定位**：使用`coloc`（R包）和完整汇总统计

```python
import requests, pandas as pd

def interpret_gwas_variant(variant_id, dataset_id="gtex_v10"):
    """查找GWAS变体调控的所有基因。"""
    url = "https://gtexportal.org/api/v2/association/singleTissueEqtl"
    params = {"variantId": variant_id, "datasetId": dataset_id, "itemsPerPage": 500}
    response = requests.get(url, params=params)
    data = response.json()

    df = pd.DataFrame(data.get("data", []))
    if df.empty:
        return df
    return df[["geneSymbol", "tissueSiteDetailId", "slope", "pval", "maf"]].sort_values("pval")

# 示例
results = interpret_gwas_variant("chr1_154453788_A_T_b38")
print(results.groupby("geneSymbol")["tissueSiteDetailId"].count().sort_values(ascending=False))
```

### 工作流2：调查特定遗传变体

1. **查询变体：**
   ```python
   url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{rs_id}"
   ```

2. **检索所有性状关联：**
   ```python
   url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{rs_id}/associations"
   ```

3. **分析多效性：**
   - 识别与此变体相关的所有性状
   - 跨性状检查效应方向
   - 寻找共享生物学通路

4. **检查基因组背景：**
   - 确定附近基因
   - 识别变体是否在编码/调控区域
   - 审查与其他变体的连锁不平衡

### 工作流3：基因中心关联分析

1. **按基因符号搜索**在Web界面或：
   ```python
   url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/search/findByGene"
   params = {"geneName": gene_symbol}
   ```

2. **检索基因区域变体：**
   - 获取基因的染色体坐标
   - 查询区域变体
   - 包括启动子和调控区域（扩展边界）

3. **分析关联模式：**
   - 识别此基因中关联的性状
   - 寻找跨研究的一致关联
   - 审查效应大小和方向

4. **功能解释：**
   - 确定变体后果（错义、调控等）
   - 检查表达QTL（eQTL）数据
   - 审查通路和网络背景

### 工作流4：遗传证据系统评价

1. **定义研究问题：**
   - 特定性状或疾病
   - 群体考虑
   - 研究设计要求

2. **全面变体提取：**
   - 查询性状的所有关联
   - 设置显著性阈值
   - 注意发现和重复研究

3. **质量评估：**
   - 审查研究样本量
   - 检查群体多样性
   - 评估跨研究异质性
   - 识别潜在偏差

4. **数据综合：**
   - 跨研究聚合关联
   - 如适用，执行荟萃分析
   - 创建汇总表
   - 生成曼哈顿或森林图

5. **导出和文档：**
   - 下载完整关联数据
   - 如需要，导出汇总统计
   - 记录搜索策略和日期
   - 创建可重现分析脚本

### 工作流5：访问和分析汇总统计

1. **识别具有汇总统计的研究：**
   - 浏览汇总统计门户
   - 检查FTP目录列表
   - 查询API获取可用研究

2. **下载汇总统计：**
   ```bash
   # 通过FTP
   wget ftp://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/GCSTXXXXXX/harmonised/GCSTXXXXXX-harmonised.tsv.gz
   ```

3. **通过API查询特定变体：**
   ```python
   url = f"https://www.ebi.ac.uk/gwas/summary-statistics/api/chromosomes/{chrom}/associations"
   params = {"start": start_pos, "end": end_pos}
   ```

4. **处理和分析：**
   - 按p值阈值过滤
   - 提取效应大小和置信区间
   - 执行下游分析（精细定位、共定位等）

## 响应格式和数据字段

**关联记录中的关键字段：**
- `rsId`：变体标识符（rs编号）
- `strongestAllele`：关联的风险等位基因
- `pvalue`：关联p值
- `pvalueText`：P值作为文本（可能包含不等式）
- `orPerCopyNum`：优势比或beta系数
- `betaNum`：效应大小（用于数量性状）
- `betaUnit`：beta的测量单位
- `range`：置信区间
- `efoTrait`：相关性状名称
- `mappedLabel`：EFO映射的性状术语

**研究元数据字段：**
- `accessionId`：GCST研究标识符
- `pubmedId`：PubMed ID
- `author`：第一作者
- `publicationDate`：发表日期
- `ancestryInitial`：发现群体祖先
- `ancestryReplication`：重复群体祖先
- `sampleSize`：总样本量

**分页：**
结果已分页（默认每页20项）。使用以下方式导航：
- `size`参数：每页结果数
- `page`参数：页码（从0开始索引）
- 响应中的`_links`：下一页/上一页的URL

## 最佳实践

### 查询策略
- 从Web界面开始以识别相关EFO术语和研究访问号
- 对批量数据提取和自动化分析使用API
- 对大型结果集实施分页处理
- 最小化冗余请求，缓存API响应

### 数据解释
- 始终检查p值阈值（全基因组：5×10⁻⁸）
- 审查群体信息的群体适用性
- 考虑评估证据强度时的样本量
- 检查跨独立研究的重复
- 注意效应大小估计中的赢家诅咒

### 速率限制和伦理
- 尊重API使用指南（无过度请求）
- 对全基因组分析使用汇总统计下载
- 在迭代分析中实施API调用之间的适当延迟
- 执行迭代分析时在本地缓存结果
- 在发表时引用GWAS目录

### 数据质量考虑
- GWAS目录精选已发表的关联（可能包含不一致）
- 按发表报告效应大小（可能需要标准化）
- 某些研究报告条件或联合关联
- 组合结果时检查研究重叠
- 注意抽样和选择偏差

## Python 集成示例

查询和分析GWAS数据的完整工作流：

```python
import requests
import pandas as pd
from time import sleep

def query_gwas_catalog(trait_id, p_threshold=5e-8):
    """
    查询GWAS目录获取性状关联

    参数:
        trait_id: EFO性状标识符（例如'EFO_0001360'）
        p_threshold: P值阈值用于过滤

    返回:
        包含关联结果的pandas DataFrame
    """
    base_url = "https://www.ebi.ac.uk/gwas/rest/api"
    url = f"{base_url}/efoTraits/{trait_id}/associations"

    headers = {"Content-Type": "application/json"}
    results = []
    page = 0

    while True:
        params = {"page": page, "size": 100}
        response = requests.get(url, params=params, headers=headers)

        if response.status_code != 200:
            break

        data = response.json()
        associations = data.get('_embedded', {}).get('associations', [])

        if not associations:
            break

        for assoc in associations:
            pvalue = assoc.get('pvalue')
            if pvalue and float(pvalue) <= p_threshold:
                results.append({
                    'variant': assoc.get('rsId'),
                    'pvalue': pvalue,
                    'risk_allele': assoc.get('strongestAllele'),
                    'or_beta': assoc.get('orPerCopyNum') or assoc.get('betaNum'),
                    'trait': assoc.get('efoTrait'),
                    'pubmed_id': assoc.get('pubmedId')
                })

        page += 1
        sleep(0.1)  # 速率限制

    return pd.DataFrame(results)

# 示例用法
df = query_gwas_catalog('EFO_0001360')  # 2型糖尿病
print(df.head())
print(f"\n总关联数: {len(df)}")
print(f"唯一变体数: {df['variant'].nunique()}")
```

## 资源

### references/api_reference.md

全面的API文档包括：
- 两个API的详细端点规范
- 完整的查询参数和过滤器列表
- 响应格式规范和字段描述
- 高级查询示例和模式
- 错误处理和故障排除
- 与外部数据库的集成

在以下情况下查阅此参考：
- 构建复杂的API查询
- 理解响应结构
- 实施分页或批量操作
- 故障排除API错误
- 探索高级过滤选项

### 培训材料

GWAS目录团队提供研讨会材料：
- GitHub仓库：https://github.com/EBISPOT/GWAS_Catalog-workshop
- 带有示例查询的Jupyter笔记本
- 用于云执行的Google Colab集成

## 重要说明

### 数据更新
- GWAS目录定期更新新发表
- 定期重新运行查询以实现全面覆盖
- 随着研究发布数据，添加汇总统计
- EFO映射可能随时间更新

### 引用要求
使用GWAS目录数据时，请引用：
- Sollis E, et al. (2023) The NHGRI-EBI GWAS Catalog: knowledgebase and deposition resource. Nucleic Acids Research. PMID: 37953337
- 包括访问日期和版本（如果可用）
- 讨论特定发现时引用原始研究

### 局限性
- 并非所有GWAS发表都包括在内（应用精选标准）
- 汇总统计可用于研究子集
- 跨研究的效应大小可能需要标准化
- 群体多样性在增长但历史上有限
- 某些关联代表条件或联合效应

### 数据访问
- Web界面：免费，无需注册
- REST API：免费，无需API密钥
- FTP下载：开放访问
- API适用速率限制（请尊重）

## 其他资源

- **GWAS目录网站**: https://www.ebi.ac.uk/gwas/
- **文档**: https://www.ebi.ac.uk/gwas/docs
- **API文档**: https://www.ebi.ac.uk/gwas/rest/docs/api
- **汇总统计API**: https://www.ebi.ac.uk/gwas/summary-statistics/docs/
- **FTP站点**: http://ftp.ebi.ac.uk/pub/databases/gwas/
- **培训材料**: https://github.com/EBISPOT/GWAS_Catalog-workshop
- **PGS目录**（多基因评分）: https://www.pgscatalog.org/
- **帮助和支持**: gwas-info@ebi.ac.uk
