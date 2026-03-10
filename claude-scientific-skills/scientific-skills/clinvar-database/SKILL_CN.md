---
name: clinvar-database
description: 查询 NCBI ClinVar 以获取变异临床意义。按基因/位置搜索,解释致病性分类,通过 E-utilities API 或 FTP 访问,注释 VCF,用于基因组医学。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# ClinVar 数据库

## 概述

ClinVar 是 NCBI 免费获取的关于人类遗传变异与表型之间关系的报告档案,包含支持证据。该数据库聚合了基因组变异及其与人类健康关系的信息,提供临床遗传学和研究使用的标准化变异分类。

## 何时使用此技能

在以下情况下使用此技能:

- 按基因、疾病或临床意义搜索变异
- 解释临床意义分类(致病性、良性、VUS)
- 通过 E-utilities API 以编程方式访问 ClinVar
- 从 FTP 下载和处理批量数据
- 了解审查状态和星级评级
- 解决冲突的变异解释
- 用临床意义注释变异调用集

## 核心功能

### 1. 搜索和查询 ClinVar

#### Web 界面查询

在 https://www.ncbi.nlm.nih.gov/clinvar/ 使用 Web 界面搜索 ClinVar

**常见搜索模式:**
- 按基因: `BRCA1[gene]`
- 按临床意义: `pathogenic[CLNSIG]`
- 按疾病: `breast cancer[disorder]`
- 按变异: `NM_000059.3:c.1310_1313del[variant name]`
- 按染色体: `13[chr]`
- 组合: `BRCA1[gene] AND pathogenic[CLNSIG]`

#### 通过 E-utilities 编程访问

使用 NCBI 的 E-utilities API 以编程方式访问 ClinVar。有关全面的 API 文档,包括:
- **esearch** - 搜索匹配条件的变异
- **esummary** - 检索变异摘要
- **efetch** - 下载完整 XML 记录
- **elink** - 在其他 NCBI 数据库中查找相关记录

**使用 curl 的快速示例:**
```bash
# 搜索致病性 BRCA1 变异
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=BRCA1[gene]+AND+pathogenic[CLNSIG]&retmode=json"
```

**最佳实践:**
- 自动化之前先在 Web 界面上测试查询
- 使用 API 密钥将速率限制从 3 提高到每秒 10 个请求
- 为速率限制错误实施指数退避
- 使用 Biopython 时设置 `Entrez.email`

### 2. 解释临床意义

#### 了解分类

ClinVar 使用标准化术语进行变异分类。有关详细解释指南,请参阅 `references/clinical_significance.md`。

**关键胚系分类术语(ACMG/AMP):**
- **致病性(P)** - 变异导致疾病(~99% 概率)
- **可能致病性(LP)** - 变异可能导致疾病(~90% 概率)
- **意义未明(VUS)** - 证据不足以分类
- **可能良性(LB)** - 变异可能不导致疾病
- **良性(B)** - 变异不导致疾病

**审查状态(星级评级):**
- ★★★ 实践指南 - 最高置信度
- ★★★ 专家小组审查(例如 ClinGen) - 高置信度
- ★★ 多个提交者,无冲突 - 中等置信度
- ★ 单个提交者,有标准 - 标准权重
- ☆ 无断言标准 - 低置信度

**关键考虑:**
- 始终检查审查状态 - 优先考虑 ★★★ 或 ★★★★ 评级
- 冲突的解释需要手动评估
- 随着新证据的出现,分类可能会发生变化
- VUS(意义未明)变异缺乏临床使用的足够证据

### 3. 从 FTP 下载批量数据

#### 访问 ClinVar FTP 站点

从 `ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/` 下载完整数据集

有关文件格式和处理的全面文档,请参阅 `references/data_formats.md`。

**更新计划:**
- 月度发布: 每月第一个星期四(完整数据集,已归档)
- 每周更新: 每周一(增量更新)

#### 可用格式

**XML 文件**(最全面):
- VCV(变异)文件: `xml/clinvar_variation/` - 变异中心聚合
- RCV(记录)文件: `xml/RCV/` - 变异-疾病对
- 包括完整的提交详细信息、证据和元数据

**VCF 文件**(用于基因组流程):
- GRCh37: `vcf_GRCh37/clinvar.vcf.gz`
- GRCh38: `vcf_GRCh38/clinvar.vcf.gz`
- 局限性: 排除 >10kb 的变异和复杂结构变异

**制表符分隔文件**(用于快速分析):
- `tab_delimited/variant_summary.txt.gz` - 所有变异的摘要
- `tab_delimited/var_citations.txt.gz` - PubMed 引用
- `tab_delimited/cross_references.txt.gz` - 数据库交叉引用

**示例下载:**
```bash
# 下载最新的月度 XML 发布
wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/clinvar_variation/ClinVarVariationRelease_00-latest.xml.gz

# 下载 GRCh38 的 VCF
wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz
```

### 4. 处理和分析 ClinVar 数据

#### 使用 XML 文件

处理 XML 文件以提取变异详细信息、分类和证据。

**使用 xml.etree 的 Python 示例:**
```python
import gzip
import xml.etree.ElementTree as ET

with gzip.open('ClinVarVariationRelease.xml.gz', 'rt') as f:
    for event, elem in ET.iterparse(f, events=('end',)):
        if elem.tag == 'VariationArchive':
            variation_id = elem.attrib.get('VariationID')
            # 提取临床意义、审查状态等
            elem.clear()  # 释放内存
```

#### 使用 VCF 文件

使用 bcftools 或 Python 注释变异调用或按临床意义筛选。

**使用 bcftools:**
```bash
# 筛选致病性变异
bcftools view -i 'INFO/CLNSIG~"Pathogenic"' clinvar.vcf.gz

# 提取特定基因
bcftools view -i 'INFO/GENEINFO~"BRCA"' clinvar.vcf.gz

# 用 ClinVar 注释您的 VCF
bcftools annotate -a clinvar.vcf.gz -c INFO/CLNSIG,INFO/CLNDN,INFO/CLNREVSTAT \
     -o annotated_variants.vcf \
     your_variants.vcf
```

**使用 PyVCF 的 Python:**
```python
import vcf

vcf_reader = vcf.Reader(filename='clinvar.vcf.gz')
for record in vcf_reader:
    clnsig = record.INFO.get('CLNSIG', [])
    if 'Pathogenic' in clnsig:
        gene = record.INFO.get('GENEINFO', [''])[0]
        print(f"{record.CHROM}:{record.POS} {gene} - {clnsig}")
```

#### 使用制表符分隔文件

使用 pandas 或命令行工具进行快速筛选和分析。

**使用 pandas:**
```python
import pandas as pd

# 加载变异摘要
df = pd.read_csv('variant_summary.txt.gz', sep='\t', compression='gzip')

# 筛选特定基因的致病性变异
pathogenic_brca = df[
    (df['GeneSymbol'] == 'BRCA1') &
    (df['ClinicalSignificance'].str.contains('Pathogenic', na=False))
]

# 按临床意义统计变异
sig_counts = df['ClinicalSignificance'].value_counts()
```

**使用命令行工具:**
```bash
# 提取特定基因的致病性变异
zcat variant_summary.txt.gz | \
  awk -F'\t' '$7=="TP53" && $13~"Pathogenic"' | \
  cut -f1,5,7,13,14
```

### 5. 处理冲突的解释

当多个提交者为同一变异提供不同分类时,ClinVar 报告"致病性相互冲突的解释。"

**解决策略:**
1. 检查审查状态(星级评级) - 更高评级权重更大
2. 检查每个提交者的证据和断言标准
3. 考虑提交日期 - 较新的提交可能反映更新的证据
4. 审查人群频率数据(例如 gnomAD)以获取背景
5. 查看专家小组分类(★★★)时可用
6. 对于临床使用,始终遵循遗传学专业人士的意见

**排除冲突的搜索查询:**
```
TP53[gene] AND pathogenic[CLNSIG] NOT conflicting[RVSTAT]
```

### 6. 跟踪分类更新

随着新证据的出现,变异分类可能会随时间变化。

**分类变化的原因:**
- 新的功能研究或临床数据
- 更新的人群频率信息
- 修订的 ACMG/AMP 指南
- 来自额外家族的分离数据

**最佳实践:**
- 记录 ClinVar 版本和访问日期以确保可重现性
- 定期重新检查关键变异的分类
- 订阅 ClinVar 邮件列表以获取主要更新
- 使用月度归档发布以获取稳定数据集

### 7. 向 ClinVar 提交数据

组织可以向 ClinVar 提交变异解释。

**提交方法:**
- Web 提交门户: https://submit.ncbi.nlm.nih.gov/subs/clinvar/
- API 提交(需要服务账户): 请参阅 `references/api_reference.md`
- 通过 Excel 模板批量提交

**要求:**
- NCBI 的组织账户
- 断言标准(最好为 ACMG/AMP 指南)
- 分类的支持证据

联系: clinvar@ncbi.nlm.nih.gov 以设置提交账户。

## 工作流程示例

### 示例 1: 识别基因中的高置信度致病性变异

**目标:** 查找 CFTR 基因中具有专家小组审查的致病性变异。

**步骤:**
1. 使用 Web 界面或 E-utilities 搜索:
   ```
   CFTR[gene] AND pathogenic[CLNSIG] AND (reviewed by expert panel[RVSTAT] OR practice guideline[RVSTAT])
   ```
2. 审查结果,注意审查状态(应为 ★★★ 或 ★★★★)
3. 导出变异列表或通过 efetch 检索完整记录
4. 如适用,与临床表现交叉参考

### 示例 2: 用 ClinVar 分类注释 VCF

**目标:** 为变异调用添加临床意义注释。

**步骤:**
1. 下载适当的 ClinVar VCF(匹配基因组构建: GRCh37 或 GRCh38):
   ```bash
   wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz
   wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz.tbi
   ```
2. 使用 bcftools 注释:
   ```bash
   bcftools annotate -a clinvar.vcf.gz \
     -c INFO/CLNSIG,INFO/CLNDN,INFO/CLNREVSTAT \
     -o annotated_variants.vcf \
     your_variants.vcf
   ```
3. 筛选致病性变异的注释 VCF:
   ```bash
   bcftools view -i 'INFO/CLNSIG~"Pathogenic"' annotated_variants.vcf
   ```

### 示例 3: 分析特定疾病的变异

**目标:** 研究与遗传性乳腺癌相关的所有变异。

**步骤:**
1. 按疾病搜索:
   ```
   hereditary breast cancer[disorder] OR "Breast-ovarian cancer, familial"[disorder]
   ```
2. 下载结果为 CSV 或通过 E-utilities 检索
3. 按审查状态筛选以优先考虑高置信度变异
4. 分析跨基因的分布(BRCA1、BRCA2、PALB2 等)
5. 单独检查具有冲突解释的变异

### 示例 4: 批量下载和数据库构建

**目标:** 为分析流程构建本地 ClinVar 数据库。

**步骤:**
1. 为可重现性下载月度发布:
   ```bash
   wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/clinvar_variation/ClinVarVariationRelease_YYYY-MM.xml.gz
   ```
2. 解析 XML 并加载到数据库(PostgreSQL、MySQL、MongoDB)
3. 按基因、位置、临床意义、审查状态建立索引
4. 实现版本跟踪以进行更新
5. 计划从 FTP 站点进行月度更新

## 重要局限性和考虑

### 数据质量
- **并非所有提交具有相同权重** - 检查审查状态(星级评级)
- **存在冲突的解释** - 需要手动评估
- **历史提交可能已过时** - 较新的数据可能更准确
- **VUS 分类不是临床诊断** - 意味着证据不足

### 范围局限
- **不用于直接临床诊断** - 始终涉及遗传学专业人士
- **人群特异性** - 变异频率因血统而异
- **覆盖不完整** - 并非所有基因或变异都得到充分研究
- **版本依赖性** - 跨分析协调基因组构建(GRCh37/GRCh38)

### 技术局限
- **VCF 文件排除大变异** - >10kb 的变异不在 VCF 格式中
- **API 上的速率限制** - 无密钥时每秒 3 个请求,有密钥时每秒 10 个请求
- **文件大小** - 完整的 XML 发布是数 GB 的压缩文件
- **无实时更新** - 网站每周更新,FTP 每月/每周更新

## 资源

### 参考文档

此技能包括全面的参考文档:

- **`references/api_reference.md`** - 完整的 E-utilities API 文档,包含 esearch、esummary、efetch 和 elink 的示例;包括速率限制、身份验证和 Python/Biopython 代码示例

- **`references/clinical_significance.md`** - 解释临床意义分类、审查状态星级评级、冲突解决和最佳实践的详细指南

- **`references/data_formats.md`** - XML、VCF 和制表符分隔文件格式的文档;FTP 目录结构、处理示例和格式选择指南

### 外部资源

- ClinVar 主页: https://www.ncbi.nlm.nih.gov/clinvar/
- ClinVar 文档: https://www.ncbi.nlm.nih.gov/clinvar/docs/
- E-utilities 文档: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- ACMG 变异解释指南: Richards et al., 2015 (PMID: 25741868)
- ClinGen 专家小组: https://clinicalgenome.org/

### 联系方式

有关 ClinVar 或数据提交的问题: clinvar@ncbi.nlm.nih.gov
