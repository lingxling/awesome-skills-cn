---
name: pubmed-database
description: 直接访问PubMed的REST API。高级布尔/MeSH查询，E-utilities API，批处理，引用管理。对于Python工作流，首选biopython (Bio.Entrez)。使用此技能进行直接HTTP/REST工作或自定义API实现。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# PubMed 数据库

## 概述

PubMed是美国国家医学图书馆的综合数据库，提供免费访问MEDLINE和生命科学文献。使用布尔运算符、MeSH术语和字段标签构建高级查询，通过E-utilities API以编程方式访问数据，用于系统评价和文献分析。

## 使用场景

本技能适用于以下情况：
- 搜索生物医学或生命科学研究文章
- 使用布尔运算符、字段标签或MeSH术语构建复杂搜索查询
- 进行系统文献综述或荟萃分析
- 通过E-utilities API以编程方式访问PubMed数据
- 按特定标准（作者、期刊、出版日期、文章类型）查找文章
- 检索引用信息、摘要或全文文章
- 使用PMID（PubMed ID）或DOI
- 创建用于文献监测或数据提取的自动化工作流程

## 核心功能

### 1. 高级搜索查询构建

使用布尔运算符、字段标签和专用语法构建复杂的PubMed查询。

**基本搜索策略**：
- 使用布尔运算符（AND、OR、NOT）组合概念
- 使用字段标签限制搜索到特定记录部分
- 使用双引号进行精确匹配的短语搜索
- 使用通配符表示术语变体
- 使用邻近搜索查找指定距离内的术语

**示例查询**：
```
# 关于糖尿病治疗的最新系统评价
diabetes mellitus[mh] AND treatment[tiab] AND systematic review[pt] AND 2023:2024[dp]

# 比较两种药物的临床试验
(metformin[nm] OR insulin[nm]) AND diabetes mellitus, type 2[mh] AND randomized controlled trial[pt]

# 作者特定研究
smith ja[au] AND cancer[tiab] AND 2023[dp] AND english[la]
```

**何时查阅search_syntax.md**：
- 需要可用字段标签的综合列表
- 需要搜索运算符的详细说明
- 构建复杂的邻近搜索
- 理解自动术语映射行为
- 需要日期范围、通配符或特殊字符的特定语法

字段标签的Grep模式：`\[au\]|\[ti\]|\[ab\]|\[mh\]|\[pt\]|\[dp\]`

### 2. MeSH术语和受控词汇

使用医学主题词（MeSH）进行生物医学文献的精确、一致搜索。

**MeSH搜索**：
- [mh]标签搜索MeSH术语，自动包含更窄的术语
- [majr]标签限制为主题为主要焦点的文章
- 将MeSH术语与副标题结合以提高特异性（例如，diabetes mellitus/therapy[mh]）

**常见MeSH副标题**：
- /diagnosis - 诊断方法
- /drug therapy - 药物治疗
- /epidemiology - 疾病模式和患病率
- /etiology - 疾病原因
- /prevention & control - 预防措施
- /therapy - 治疗方法

**示例**：
```
# 具有特定重点的糖尿病治疗
diabetes mellitus, type 2[mh]/drug therapy AND cardiovascular diseases[mh]/prevention & control
```

### 3. 文章类型和出版过滤

按出版类型、日期、文本可用性和其他属性过滤结果。

**出版类型**（使用[pt]字段标签）：
- Clinical Trial（临床试验）
- Meta-Analysis（荟萃分析）
- Randomized Controlled Trial（随机对照试验）
- Review（综述）
- Systematic Review（系统评价）
- Case Reports（病例报告）
- Guideline（指南）

**日期过滤**：
- 单年：`2024[dp]`
- 日期范围：`2020:2024[dp]`
- 特定日期：`2024/03/15[dp]`

**文本可用性**：
- 免费全文：在查询中添加`AND free full text[sb]`
- 有摘要：在查询中添加`AND hasabstract[text]`

**示例**：
```
# 关于高血压的最新免费全文RCT
hypertension[mh] AND randomized controlled trial[pt] AND 2023:2024[dp] AND free full text[sb]
```

### 4. 通过E-utilities API的程序化访问

使用NCBI E-utilities REST API以编程方式访问PubMed数据，用于自动化和批量操作。

**核心API端点**：
1. **ESearch** - 搜索数据库并检索PMID
2. **EFetch** - 下载各种格式的完整记录
3. **ESummary** - 获取文档摘要
4. **EPost** - 上传UID用于批处理
5. **ELink** - 查找相关文章和链接数据

**基本工作流程**：
```python
import requests

# 步骤1：搜索文章
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
search_url = f"{base_url}esearch.fcgi"
params = {
    "db": "pubmed",
    "term": "diabetes[tiab] AND 2024[dp]",
    "retmax": 100,
    "retmode": "json",
    "api_key": "YOUR_API_KEY"  # 可选但推荐
}
response = requests.get(search_url, params=params)
pmids = response.json()["esearchresult"]["idlist"]

# 步骤2：获取文章详情
fetch_url = f"{base_url}efetch.fcgi"
params = {
    "db": "pubmed",
    "id": ",".join(pmids),
    "rettype": "abstract",
    "retmode": "text",
    "api_key": "YOUR_API_KEY"
}
response = requests.get(fetch_url, params=params)
abstracts = response.text
```

**速率限制**：
- 无API密钥：3个请求/秒
- 有API密钥：10个请求/秒
- 始终包含User-Agent头

**最佳实践**：
- 对大型结果集使用历史服务器（usehistory=y）
- 通过EPost为多个UID实现批处理操作
- 本地缓存结果以最小化冗余调用
- 尊重速率限制以避免服务中断

**何时查阅api_reference.md**：
- 需要详细的端点文档
- 需要每个E-utility的参数规范
- 构建批处理操作或历史服务器工作流程
- 理解响应格式（XML、JSON、文本）
- 排查API错误或速率限制问题

API端点的Grep模式：`esearch|efetch|esummary|epost|elink|einfo`

### 5. 引用匹配和文章检索

使用部分引用信息或特定标识符查找文章。

**按标识符**：
```
# 按PMID
12345678[pmid]

# 按DOI
10.1056/NEJMoa123456[doi]

# 按PMC ID
PMC123456[pmc]
```

**引用匹配**（通过ECitMatch API）：
使用期刊名称、年份、卷、页码和作者查找PMID：
```
格式：journal|year|volume|page|author|key|
示例：Science|2008|320|5880|1185|key1|
```

**按作者和元数据**：
```
# 第一作者，年份和主题
smith ja[1au] AND 2023[dp] AND cancer[tiab]

# 期刊、卷和页码
nature[ta] AND 2024[dp] AND 456[vi] AND 123-130[pg]
```

### 6. 系统文献综述

为系统评价和荟萃分析进行全面的文献搜索。

**PICO框架**（人群、干预、比较、结果）：
系统地构建临床研究问题：
```
# 示例：糖尿病治疗效果
# P: diabetes mellitus, type 2[mh]
# I: metformin[nm]
# C: lifestyle modification[tiab]
# O: glycemic control[tiab]

diabetes mellitus, type 2[mh] AND
(metformin[nm] OR lifestyle modification[tiab]) AND
glycemic control[tiab] AND
randomized controlled trial[pt]
```

**综合搜索策略**：
```
# 包括多个同义词和MeSH术语
(disease name[tiab] OR disease name[mh] OR synonym[tiab]) AND
(treatment[tiab] OR therapy[tiab] OR intervention[tiab]) AND
(systematic review[pt] OR meta-analysis[pt] OR randomized controlled trial[pt]) AND
2020:2024[dp] AND
english[la]
```

**搜索优化**：
1. 开始广泛，回顾结果
2. 使用字段标签添加特异性
3. 应用日期和出版类型过滤器
4. 使用高级搜索查看查询翻译
5. 结合搜索历史进行复杂查询

**何时查阅common_queries.md**：
- 需要特定疾病类型或研究领域的示例查询
- 需要不同研究设计的模板
- 寻找特定人群的查询模式（儿科、老年科等）
- 构建特定方法的搜索
- 需要质量过滤器或最佳实践模式

查询示例的Grep模式：`diabetes|cancer|cardiovascular|clinical trial|systematic review`

### 7. 搜索历史和保存的搜索

使用PubMed的搜索历史和My NCBI功能实现高效的研究工作流程。

**搜索历史**（通过高级搜索）：
- 最多保存100次搜索
- 8小时不活动后过期
- 使用#引用组合以前的搜索
- 执行前预览结果计数

**示例**：
```
#1: diabetes mellitus[mh]
#2: cardiovascular diseases[mh]
#3: #1 AND #2 AND risk factors[tiab]
```

**My NCBI功能**：
- 无限期保存搜索
- 设置新匹配文章的电子邮件提醒
- 创建保存文章的集合
- 按项目或主题组织研究

**RSS订阅**：
为任何搜索创建RSS订阅，以监控您感兴趣领域的新出版物。

### 8. 相关文章和引用发现

查找相关研究并探索引用网络。

**相似文章功能**：
每个PubMed文章都包含基于以下内容的预先计算的相关文章：
- 标题和摘要相似性
- MeSH术语重叠
- 加权算法匹配

**ELink相关数据**：
```
# 以编程方式查找相关文章
elink.fcgi?dbfrom=pubmed&db=pubmed&id=PMID&cmd=neighbor
```

**引用链接**：
- 链接到出版商的全文
- 链接到PubMed Central免费文章
- 连接到相关NCBI数据库（GenBank、ClinicalTrials.gov等）

### 9. 导出和引用管理

以各种格式导出搜索结果，用于引用管理和进一步分析。

**导出格式**：
- .nbib文件用于参考文献管理器（Zotero、Mendeley、EndNote）
- AMA、MLA、APA、NLM引用样式
- 用于数据分析的CSV
- 用于程序化处理的XML

**剪贴板和集合**：
- 剪贴板：最多500个项目的临时存储（8小时过期）
- 集合：通过My NCBI账户的永久存储

**通过API批量导出**：
```python
# 以MEDLINE格式导出引用
efetch.fcgi?db=pubmed&id=PMID1,PMID2&rettype=medline&retmode=text
```

## 使用参考文件

本技能在`references/`目录中包含三个综合参考文件：

### references/api_reference.md
完整的E-utilities API文档，包括所有九个端点、参数、响应格式和最佳实践。在以下情况下查阅：
- 实现程序化PubMed访问
- 构建API请求
- 理解速率限制和认证
- 通过历史服务器处理大型数据集
- 排查API错误

### references/search_syntax.md
PubMed搜索语法的详细指南，包括字段标签、布尔运算符、通配符和特殊字符。在以下情况下查阅：
- 构建复杂的搜索查询
- 理解自动术语映射
- 使用高级搜索功能（邻近、通配符）
- 应用过滤器和限制
- 排查意外的搜索结果

### references/common_queries.md
各种研究场景、疾病类型和方法的大量示例查询。在以下情况下查阅：
- 开始新的文献搜索
- 需要特定研究领域的模板
- 寻找最佳实践查询模式
- 进行系统评价
- 搜索特定研究设计或人群

**参考加载策略**：
根据特定任务的需要将参考文件加载到上下文中。对于简短查询或基本搜索，本SKILL.md中的信息可能足够。对于复杂操作，请查阅适当的参考文件。

## 常见工作流程

### 工作流程1：基本文献搜索

1. 识别关键概念和同义词
2. 使用布尔运算符和字段标签构建查询
3. 回顾初始结果并优化查询
4. 应用过滤器（日期、文章类型、语言）
5. 导出结果进行分析

### 工作流程2：系统评价搜索

1. 使用PICO框架定义研究问题
2. 识别所有相关的MeSH术语和同义词
3. 构建综合搜索策略
4. 搜索多个数据库（包括PubMed）
5. 记录搜索策略和日期
6. 导出结果进行筛选和评价

### 工作流程3：程序化数据提取

1. 设计搜索查询并在Web界面中测试
2. 使用ESearch API实现搜索
3. 对大型结果集使用历史服务器
4. 使用EFetch检索详细记录
5. 解析XML/JSON响应
6. 本地存储数据并缓存
7. 实现速率限制和错误处理

### 工作流程4：引用发现

1. 从已知相关文章开始
2. 使用相似文章找到相关工作
3. 检查引用文章（如果可用）
4. 探索相关文章的MeSH术语
5. 基于发现构建新搜索
6. 使用ELink查找相关数据库条目

### 工作流程5：持续文献监测

1. 构建综合搜索查询
2. 测试并优化查询精度
3. 将搜索保存到My NCBI账户
4. 设置新匹配的电子邮件提醒
5. 为阅读器监控创建RSS订阅
6. 定期审查新文章

## 提示和最佳实践

### 搜索策略
- 从广泛开始，然后使用字段标签和过滤器缩小范围
- 包括同义词和MeSH术语以获得全面覆盖
- 使用引号表示精确短语
- 在高级搜索中检查搜索详情以验证查询翻译
- 使用搜索历史组合多个搜索

### API使用
- 获取API密钥以获得更高的速率限制（10次请求/秒 vs 3次请求/秒）
- 对> 500篇文章的结果集使用历史服务器
- 为速率限制处理实现指数退避
- 本地缓存结果以最小化冗余请求
- 始终包含描述性User-Agent头

### 质量过滤
- 优先选择系统评价和荟萃分析作为综合证据
- 使用出版类型过滤器查找特定研究设计
- 按日期过滤获取最新研究
- 适当地应用语言过滤器
- 使用免费全文过滤器获取即时访问

### 引用管理
- 尽早并经常导出以避免丢失搜索结果
- 使用.nbib格式以与大多数参考文献管理器兼容
- 创建My NCBI账户用于永久收藏
- 记录搜索策略以确保可重复性
- 使用集合按项目组织研究

## 限制和注意事项

### 数据库覆盖范围
- 主要是生物医学和生命科学文献
- 1975年前的文章通常缺少摘要
- 2002年起提供完整作者姓名
- 提供非英语摘要，但可能默认为英语显示

### 搜索限制
- 显示最多限制为10,000个结果
- 搜索历史在8小时不活动后过期
- 剪贴板最多保存500个项目，8小时过期
- 自动术语映射可能产生意外结果

### API考虑因素
- 适用速率限制（3-10次请求/秒）
- 大型查询可能超时（使用历史服务器）
- 详细数据提取需要XML解析
- 生产使用推荐API密钥

### 访问限制
- PubMed提供引用和摘要（并非总是全文）
- 全文访问取决于出版商、机构访问或开放获取状态
- LinkOut可用性因期刊和机构而异
- 某些内容需要订阅或付费

## 支持资源

- **PubMed帮助**：https://pubmed.ncbi.nlm.nih.gov/help/
- **E-utilities文档**：https://www.ncbi.nlm.nih.gov/books/NBK25501/
- **NLM帮助台**：1-888-FIND-NLM (1-888-346-3656)
- **技术支持**：vog.hin.mln.ibcn@seitilitue
- **邮件列表**：utilities-announce@ncbi.nlm.nih.gov