---
name: clinpgx-database
description: 访问 ClinPGx 药物基因组学数据(PharmGKB 的继任者)。查询基因-药物相互作用、CPIC 指南、等位基因功能,用于精准医学和基因型指导的给药决策。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# ClinPGx 数据库

## 概述

ClinPGx(临床药物基因组学数据库)是临床药物基因组学信息的综合资源,是 PharmGKB 的继任者。它整合了来自 PharmGKB、CPIC 和 PharmCAT 的数据,提供关于遗传变异如何影响药物反应的策展信息。访问基因-药物对、临床指南、等位基因功能和药物标签,用于精准医学应用。

## 何时使用此技能

在以下情况下使用此技能:

- **基因-药物相互作用**: 查询遗传变异如何影响药物代谢、疗效或毒性
- **CPIC 指南**: 访问药物遗传学的基于证据的临床实践指南
- **等位基因信息**: 检索等位基因功能、频率和表型数据
- **药物标签**: 探索 FDA 和其他监管机构的药物基因组学药物标签
- **药物基因组学注释**: 访问基因-药物-疾病关系的策展文献
- **临床决策支持**: 使用 PharmDOG 工具进行表型转换和自定义基因型解释
- **精准医学**: 在临床实践中实施药物基因组学测试
- **药物代谢**: 了解 CYP450 和其他药物基因的功能
- **个性化给药**: 查找基因型指导的给药推荐
- **药物不良反应**: 识别药物毒性的遗传风险因素

## 安装和设置

### Python API 访问

ClinPGx REST API 提供对所有数据库资源的编程访问。基本设置:

```bash
uv pip install requests
```

### API 端点

```python
BASE_URL = "https://api.clinpgx.org/v1/"
```

**速率限制:**
- 每秒最多 2 个请求
- 过多请求将导致 HTTP 429(请求过多)响应

**身份验证**: 基本访问不需要

**数据许可**: 知识共享署名-相同方式 4.0 国际许可

对于大量 API 使用,请通知 ClinPGx 团队: api@clinpgx.org

## 核心功能

### 1. 基因查询

**检索基因信息**,包括功能、临床注释和药物基因组学意义:

```python
import requests

# 获取基因详细信息
response = requests.get("https://api.clinpgx.org/v1/gene/CYP2D6")
gene_data = response.json()

# 按名称搜索基因
response = requests.get("https://api.clinpgx.org/v1/gene",
                       params={"q": "CYP"})
genes = response.json()
```

**关键药物基因:**
- **CYP450 酶**: CYP2D6、CYP2C19、CYP2C9、CYP3A4、CYP3A5
- **转运蛋白**: SLCO1B1、ABCB1、ABCG2
- **其他代谢酶**: TPMT、DPYD、NUDT15、UGT1A1
- **受体**: OPRM1、HTR2A、ADRB1
- **HLA 基因**: HLA-B、HLA-A

### 2. 药物和化学物质查询

**检索药物信息**,包括药物基因组学注释和机制:

```python
# 获取药物详细信息
response = requests.get("https://api.clinpgx.org/v1/chemical/PA448515")  # Warfarin
drug_data = response.json()

# 按名称搜索药物
response = requests.get("https://api.clinpgx.org/v1/chemical",
                       params={"name": "warfarin"})
drugs = response.json()
```

**具有药物基因组学意义的药物类别:**
- 抗凝剂(华法林、氯吡格雷)
- 抗抑郁药(SSRIs、TCAs)
- 免疫抑制剂(他克莫司、硫唑嘌呤)
- 肿瘤药物(5-氟尿嘧啶、伊立替康、他莫昔芬)
- 心血管药物(他汀类、β 受体阻滞剂)
- 止痛药(可待因、曲马多)
- 抗病毒药(阿巴卡韦)

### 3. 基因-药物对查询

**访问策展的基因-药物关系**,包含临床注释:

```python
# 获取基因-药物对信息
response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                       params={"gene": "CYP2D6", "drug": "codeine"})
pair_data = response.json()

# 获取基因的所有对
response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                       params={"gene": "CYP2C19"})
all_pairs = response.json()
```

**临床注释来源:**
- CPIC(临床药物遗传学实施联盟)
- DPWG(荷兰药物遗传学工作组)
- FDA(美国食品药品监督管理局)标签
- 同行评审文献摘要注释

### 4. CPIC 指南

**访问基于证据的临床实践指南:**

```python
# 获取 CPIC 指南
response = requests.get("https://api.clinpgx.org/v1/guideline/PA166104939")
guideline = response.json()

# 列出所有 CPIC 指南
response = requests.get("https://api.clinpgx.org/v1/guideline",
                       params={"source": "CPIC"})
guidelines = response.json()
```

**CPIC 指南组件:**
- 涵盖的基因-药物对
- 按表型的临床推荐
- 证据水平和强度评级
- 支持文献
- 可下载的 PDF 和补充材料
- 实施考虑

**示例指南:**
- CYP2D6-可待因(超快代谢者避免使用)
- CYP2C19-氯吡格雷(慢代谢者替代治疗)
- TPMT-硫唑嘌呤(中/慢代谢者剂量减少)
- DPYD-氟嘧啶类药物(基于活性调整剂量)
- HLA-B*57:01-阿巴卡韦(阳性时避免)

### 5. 等位基因和变异信息

**查询等位基因功能和频率数据:**

```python
# 获取等位基因信息
response = requests.get("https://api.clinpgx.org/v1/allele/CYP2D6*4")
allele_data = response.json()

# 获取基因的所有等位基因
response = requests.get("https://api.clinpgx.org/v1/allele",
                       params={"gene": "CYP2D6"})
alleles = response.json()
```

**等位基因信息包括:**
- 功能状态(正常、降低、无功能、增加、不确定)
- 各种族群体的频率
- 定义变异(SNP、indel、CNV)
- 表型分配
- PharmVar 和其他命名法系统的参考文献

**表型类别:**
- **超快代谢者**(UM): 酶活性增加
- **正常代谢者**(NM): 正常酶活性
- **中间代谢者**(IM): 酶活性降低
- **慢代谢者**(PM): 极少或无酶活性

### 6. 变异注释

**访问特定遗传变异的临床注释:**

```python
# 获取变异信息
response = requests.get("https://api.clinpgx.org/v1/variant/rs4244285")
variant_data = response.json()

# 按位置搜索变异(如支持)
response = requests.get("https://api.clinpgx.org/v1/variant",
                       params={"chromosome": "10", "position": 94781859})
variants = response.json()
```

**变异数据包括:**
- rsID 和基因组坐标
- 基因和功能后果
- 等位基因关联
- 临床意义
- 群体频率
- 文献参考文献

### 7. 临床注释

**检索策展文献注释**(原 PharmGKB 临床注释):**

```python
# 获取临床注释
response = requests.get("https://api.clinpgx.org/v1/clinicalAnnotation",
                       params={"gene": "CYP2D6"})
annotations = response.json()

# 按证据水平筛选
response = requests.get("https://api.clinpgx.org/v1/clinicalAnnotation",
                       params={"evidenceLevel": "1A"})
high_evidence = response.json()
```

**证据水平**(从高到低):
- **水平 1A**: 高质量证据,CPIC/FDA/DPWG 指南
- **水平 1B**: 高质量证据,尚无指南
- **水平 2A**: 来自设计良好的研究的中等证据
- **水平 2B**: 存在一些局限性的中等证据
- **水平 3**: 有限或相互矛盾的证据
- **水平 4**: 病例报告或弱证据

### 8. 药物标签

**访问来自药物标签的药物基因组学信息:**

```python
# 获取具有药物基因组学信息的药物标签
response = requests.get("https://api.clinpgx.org/v1/drugLabel",
                       params={"drug": "warfarin"})
labels = response.json()

# 按监管来源筛选
response = requests.get("https://api.clinpgx.org/v1/drugLabel",
                       params={"source": "FDA"})
fda_labels = response.json()
```

**标签信息包括:**
- 检测推荐
- 按基因型的给药指导
- 警告和注意事项
- 生物标志物信息
- 监管来源(FDA、EMA、PMDA 等)

### 9. 通路

**探索药代动力学和药效学通路:**

```python
# 获取通路信息
response = requests.get("https://api.clinpgx.org/v1/pathway/PA146123006")  # 华法林通路
pathway_data = response.json()

# 按药物搜索通路
response = requests.get("https://api.clinpgx.org/v1/pathway",
                       params={"drug": "warfarin"})
pathways = response.json()
```

**通路图显示:**
- 药物代谢步骤
- 涉及的酶和转运蛋白
- 影响每个步骤的基因变异
- 对疗效/毒性的下游影响
- 与其他通路的相互作用

## 查询工作流程

### 工作流程 1: 药物处方的临床决策支持

1. **识别相关药物基因的患者基因型**:
   ```python
   # 示例: 患者为 CYP2C19 *1/*2(中间代谢者)
   response = requests.get("https://api.clinpgx.org/v1/allele/CYP2C19*2")
   allele_function = response.json()
   ```

2. **查询感兴趣药物的基因-药物对**:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                          params={"gene": "CYP2C19", "drug": "clopidogrel"})
   pair_info = response.json()
   ```

3. **检索 CPIC 指南以获取给药推荐**:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/guideline",
                          params={"gene": "CYP2C19", "drug": "clopidogrel"})
   guideline = response.json()
   # 推荐: IM/PM 的替代抗血小板治疗
   ```

4. **检查药物标签以获取监管指导**:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/drugLabel",
                          params={"drug": "clopidogrel"})
   label = response.json()
   ```

### 工作流程 2: 基因面板分析

1. **获取临床面板中的药物基因列表**:
   ```python
   pgx_panel = ["CYP2C19", "CYP2D6", "CYP2C9", "TPMT", "DPYD", "SLCO1B1"]
   ```

2. **对于每个基因,检索所有药物相互作用**:
   ```python
   all_interactions = {}
   for gene in pgx_panel:
       response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                              params={"gene": gene})
       all_interactions[gene] = response.json()
   ```

3. **筛选 CPIC 指南水平证据**:
   ```python
   for gene, pairs in all_interactions.items():
       for pair in pairs:
           if pair.get('cpicLevel'):  # 有 CPIC 指南
               print(f"{gene} - {pair['drug']}: {pair['cpicLevel']}")
   ```

4. **生成可操作的药物基因组学发现的患者报告**。

### 工作流程 3: 药物安全性评估

1. **查询药物的药物基因组学关联**:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/chemical",
                          params={"name": "abacavir"})
   drug_id = response.json()[0]['id']
   ```

2. **获取临床注释**:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/clinicalAnnotation",
                          params={"drug": drug_id})
   annotations = response.json()
   ```

3. **检查 HLA 关联和毒性风险**:
   ```python
   for annotation in annotations:
       if 'HLA' in annotation.get('genes', []):
           print(f"Toxicity risk: {annotation['phenotype']}")
           print(f"Evidence level: {annotation['evidenceLevel']}")
   ```

4. **从指南和标签检索筛查推荐**。

### 工作流程 4: 研究分析 - 人群药物基因组学

1. **获取人群比较的等位基因频率**:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/allele",
                          params={"gene": "CYP2D6"})
   alleles = response.json()
   ```

2. **提取人群特异性频率**:
   ```python
   populations = ['European', 'African', 'East Asian', 'Latino']
   frequency_data = {}
   for allele in alleles:
       allele_name = allele['name']
       frequency_data[allele_name] = {
           pop: allele.get(f'{pop}_frequency', 'N/A')
           for pop in populations
       }
   ```

3. **按人群计算表型分布**:
   ```python
   # 结合等位基因频率与功能以预测表型
   phenotype_dist = calculate_phenotype_frequencies(frequency_data)
   ```

4. **分析对多样化人群药物给药的影响**。

### 工作流程 5: 文献证据审查

1. **搜索基因-药物对**:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                          params={"gene": "TPMT", "drug": "azathioprine"})
   pair = response.json()
   ```

2. **检索所有临床注释**:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/clinicalAnnotation",
                          params={"gene": "TPMT", "drug": "azathioprine"})
   annotations = response.json()
   ```

3. **按证据水平和发表日期筛选**:
   ```python
   high_quality = [a for a in annotations
                   if a['evidenceLevel'] in ['1A', '1B', '2A']]
   ```

4. **提取 PMIDs 并检索完整参考文献**:
   ```python
   pmids = [a['pmid'] for a in high_quality if 'pmid' in a]
   # 使用 PubMed 技能检索完整引文
   ```

## 速率限制和最佳实践

### 速率限制合规

```python
import time

def rate_limited_request(url, params=None, delay=0.5):
    """进行速率限制的 API 请求(每秒最多 2 个请求)"""
    response = requests.get(url, params=params)
    time.sleep(delay)  # 请求之间等待 0.5 秒
    return response

# 在循环中使用
genes = ["CYP2D6", "CYP2C19", "CYP2C9"]
for gene in genes:
    response = rate_limited_request(
        "https://api.clinpgx.org/v1/gene/" + gene
    )
    data = response.json()
```

### 错误处理

```python
def safe_api_call(url, params=None, max_retries=3):
    """具有错误处理和重试的 API 调用"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                # 速率限制
                wait_time = 2 ** attempt  # 指数退避
                print(f"Rate limit hit. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
```

### 缓存结果

```python
import json
from pathlib import Path

def cached_query(cache_file, api_func, *args, **kwargs):
    """缓存 API 结果以避免重复查询"""
    cache_path = Path(cache_file)

    if cache_path.exists():
        with open(cache_path) as f:
            return json.load(f)

    result = api_func(*args, **kwargs)

    with open(cache_path, 'w') as f:
        json.dump(result, f, indent=2)
    return result

# 使用
gene_data = cached_query(
    'cyp2d6_cache.json',
    rate_limited_request,
    "https://api.clinpgx.org/v1/gene/CYP2D6"
)
```

## PharmDOG 工具

PharmDOG(原 DDRx)是 ClinPGx 的临床决策支持工具,用于解释药物基因组学测试结果:

**关键功能:**
- **表型转换计算器**: 调整表型预测以考虑影响 CYP2D6 的药物-药物相互作用
- **自定义基因型**: 输入患者基因型以获取表型预测
- **二维码共享**: 生成可共享的患者报告
- **灵活的指导来源**: 选择要应用的指南(CPIC、DPWG、FDA)
- **多药物分析**: 同时评估多种药物

**访问**: 可在 https://www.clinpgx.org/pharmacogenomic-decision-support 获取

**用例:**
- 临床解释药物基因组学面板结果
- 已知基因型患者的药物审查
- 患者教育材料
- 床边决策支持

## 资源

### scripts/query_clinpgx.py

Python 脚本,包含常见 ClinPGx 查询的即用型函数:

- `get_gene_info(gene_symbol)` - 检索基因详细信息
- `get_drug_info(drug_name)` - 获取药物信息
- `get_gene_drug_pairs(gene, drug)` - 查询基因-药物相互作用
- `get_cpic_guidelines(gene, drug)` - 检索 CPIC 指南
- `get_alleles(gene)` - 获取基因的所有等位基因
- `get_clinical_annotations(gene, drug, evidence_level)` - 查询文献注释
- `get_drug_labels(drug)` - 检索药物基因组学药物标签
- `search_variants(rsid)` - 按 rsID 搜索变异
- `export_to_dataframe(data)` - 将结果转换为 pandas DataFrame

查阅此脚本以获取实现示例和适当的速率限制及错误处理。

### references/api_reference.md

全面的 API 文档,包括:
- 完整的端点列表及参数
- 请求/响应格式规范
- 每个端点的示例查询
- 筛选运算符和搜索模式
- 数据架构定义
- 速率限制详情
- 身份验证要求(如任何)
- 排查常见错误

需要详细 API 信息或构建复杂查询时参考此文档。

## 重要说明

### 数据来源和集成

ClinPGx 整合了多个权威来源:
- **PharmGKB**: 策展的药物基因组学知识库(现为 ClinPGx 的一部分)
- **CPIC**: 基于证据的临床实施指南
- **PharmCAT**: 等位基因调用和表型解释工具
- **DPWG**: 荷兰药物遗传学指南
- **FDA/EMA 标签**: 监管药物基因组学信息

截至 2025 年 7 月,所有 PharmGKB URL 都重定向到相应的 ClinPGx 页面。

### 临床实施考虑

- **证据水平**: 临床应用前始终检查证据强度
- **人群差异**: 等位基因频率在不同人群中差异显著
- **表型转换**: 考虑影响酶活性的药物-药物相互作用
- **多基因效应**: 某些药物受多个药物基因影响
- **非遗传因素**: 年龄、器官功能、药物相互作用也影响反应
- **测试局限性**: 并非所有临床相关等位基因都被所有检测检测到

### 数据更新

- ClinPGx 随着新证据和指南的出现持续更新
- 检查临床注释的发表日期
- 监控 ClinPGx 博客(https://blog.clinpgx.org/)获取公告
- 随着新证据的出现更新 CPIC 指南
- PharmVar 提供等位基因定义的命名法更新

### API 稳定性

- API 端点相对稳定,但可能在开发期间发生变化
- 参数和响应格式可能被修改
- 监控 API 更改日志和 ClinPGx 博客以获取更新
- 考虑为生产应用固定版本
- 在生产部署前测试 API 更改

## 常见用例

### 预防性药物基因组学测试

查询所有临床可操作的基因-药物对以指导面板选择:

```python
# 获取所有 CPIC 指南对
response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                       params={"cpicLevel": "A"})  # A 级推荐
actionable_pairs = response.json()
```

### 药物治疗管理

根据已知基因型审查患者药物:

```python
patient_genes = {"CYP2C19": "*1/*2", "CYP2D6": "*1/*1", "SLCO1B1": "*1/*5"}
medications = ["clopidogrel", "simvastatin", "escitalopram"]

for med in medications:
    for gene in patient_genes:
        response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                               params={"gene": gene, "drug": med})
        # 检查相互作用和给药指导
```

### 临床试验资格

筛查药物基因组学禁忌症:

```python
# 阿巴卡韦试验前检查 HLA-B*57:01
response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                       params={"gene": "HLA-B", "drug": "abacavir"})
pair_info = response.json()
# CPIC: HLA-B*57:01 阳性时不要使用
```

## 其他资源

- **ClinPGx 网站**: https://www.clinpgx.org/
- **ClinPGx 博客**: https://blog.clinpgx.org/
- **API 文档**: https://api.clinpgx.org/
- **CPIC 网站**: https://cpicpgx.org/
- **PharmCAT**: https://pharmcat.clinpgx.org/
- **ClinGen**: https://clinicalgenome.org/
- **联系方式**: api@clinpgx.org(用于大量 API 使用)
