---
name: citation-management
description: 学术研究的全面引文管理。搜索 Google Scholar 和 PubMed 查找论文,提取准确的元数据,验证引文,生成正确格式的 BibTeX 条目。当您需要查找论文、验证引文信息、将 DOI 转换为 BibTeX 或确保科学写作中的参考准确性时使用此技能。
allowed-tools: Read Write Edit Bash
license: MIT 许可证
metadata:
    skill-author: K-Dense Inc.
---

# 引文管理

## 概述

在整个研究和写作过程中系统地管理引文。此技能提供用于搜索学术数据库(Google Scholar、PubMed)、从多个来源(CrossRef、PubMed、arXiv)提取准确元数据、验证引文信息以及生成正确格式的 BibTeX 条目的工具和策略。

对于维护引文准确性、避免参考错误和确保可重现研究至关重要。与 literature-review 技能无缝集成,以实现全面的研究工作流程。

**关键原则: 引文必须准确、完整、客观并符合适用法规(HIPAA、FDA、ICH-GCP)。患者隐私和数据完整性至关重要。所有临床文档必须支持基于证据的决策制定并符合专业标准。**

## 何时使用此技能

在以下情况下使用此技能:
- 在 Google Scholar 或 PubMed 上搜索特定论文
- 将 DOI、PMID 或 arXiv ID 转换为正确格式的 BibTeX
- 提取引文的完整元数据(作者、标题、期刊、年份等)
- 验证现有引文的准确性
- 清理和格式化 BibTeX 文件
- 查找特定领域的高被引论文
- 验证引文信息是否与实际发表相符
- 为手稿或论文构建参考书目
- 检查重复引文
- 确保一致的引文格式

## 使用科学原理图进行视觉增强

**当使用此技能创建文档时,始终考虑添加科学图表和原理图以增强视觉传达。**

如果您的文档尚未包含原理图或图表:
- 使用 **scientific-schematics** 技能生成 AI 驱动的出版质量图表
- 只需用自然语言描述您想要的图表
- Nano Banana Pro 将自动生成、审查和精炼原理图

**对于新文档:** 科学原理图应默认生成,以可视化表示文本中描述的关键概念、工作流程、架构或关系。

**如何生成原理图:**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

AI 将自动:
- 创建具有正确格式的出版质量图像
- 通过多次迭代审查和精炼
- 确保可访问性(色盲友好、高对比度)
- 将输出保存在 figures/ 目录中

**何时添加原理图:**
- 引文工作流程图表
- 文献搜索方法流程图
- 参考管理系统架构
- 引文风格决策树
- 数据库集成图表
- 任何受益于可视化的复杂概念

有关创建原理图的详细指导,请参阅 scientific-schematics 技能文档。

---

## 核心工作流程

引文管理遵循系统化过程:

### 第一阶段: 论文发现和搜索

**目标**: 使用学术搜索引擎查找相关论文。

#### Google Scholar 搜索

Google Scholar 提供跨学科的最全面覆盖。

**基本搜索:**
```bash
# 搜索主题论文
python scripts/search_google_scholar.py "CRISPR gene editing" \
  --limit 50 \
  --output results.json

# 使用年份筛选器搜索
python scripts/search_google_scholar.py "machine learning protein folding" \
  --year-start 2020 \
  --year-end 2024 \
  --limit 100 \
  --output ml_proteins.json
```

**高级搜索策略**(参见 `references/google_scholar_search.md`):
- 使用引号表示精确短语: `"deep learning"`
- 按作者搜索: `author:LeCun`
- 在标题中搜索: `intitle:"neural networks"`
- 排除术语: `machine learning -survey`
- 使用排序选项查找高被引论文
- 按日期范围筛选以获取最新工作

**最佳实践:**
- 使用具体、有针对性的搜索术语
- 包含关键术语和缩写
- 为快速发展的领域按最近年份筛选
- 检查"被引用次数"以查找开创性论文
- 导出前几个结果以进行进一步分析

#### PubMed 搜索

PubMed 专门用于生物医学和生命科学文献(3500万+引文)。

**基本搜索:**
```bash
# 搜索 PubMed
python scripts/search_pubmed.py "Alzheimer's disease treatment" \
  --limit 100 \
  --output alzheimers.json

# 使用 MeSH 术语和筛选器搜索
python scripts/search_pubmed.py \
  --query '"Alzheimer Disease"[MeSH] AND "Drug Therapy"[MeSH]' \
  --date-start 2020 \
  --date-end 2024 \
  --publication-types "Clinical Trial,Review" \
  --output alzheimers_trials.json
```

**高级 PubMed 查询**(参见 `references/pubmed_search.md`):
- 使用 MeSH 术语: `"Diabetes Mellitus, Type 2"[MeSH]`
- 字段标签: `"cancer"[Title]`、`"Smith J"[Author]`
- 布尔运算符: `AND`、`OR`、`NOT`
- 日期筛选器: `2020:2024[Publication Date]`
- 发表类型: `"Review"[Publication Type]`
- 与 E-utilities API 结合以实现自动化

**最佳实践:**
- 使用 MeSH Browser 查找正确的控制词汇
- 首先在 PubMed Advanced Search Builder 中构建复杂查询
- 使用 OR 包含多个同义词
- 检索 PMIDs 以便轻松提取元数据
- 导出为 JSON 或直接导出为 BibTeX

### 第二阶段: 元数据提取

**目标**: 将论文标识符(DOI、PMID、arXiv ID)转换为完整、准确的元数据。

#### 快速 DOI 到 BibTeX 转换

对于单个 DOI,使用快速转换工具:

```bash
# 转换单个 DOI
python scripts/doi_to_bibtex.py 10.1038/s41586-021-03819-2

# 从文件转换多个 DOI
python scripts/doi_to_bibtex.py --input dois.txt --output references.bib

# 不同的输出格式
python scripts/doi_to_bibtex.py 10.1038/nature12345 --format json
```

#### 全面元数据提取

对于 DOI、PMID、arXiv ID 或 URL:

```bash
# 从 DOI 提取
python scripts/extract_metadata.py --doi 10.1038/s41586-021-03819-2

# 从 PMID 提取
python scripts/extract_metadata.py --pmid 34265844

# 从 arXiv ID 提取
python scripts/extract_metadata.py --arxiv 2103.14030

# 从 URL 提取
python scripts/extract_metadata.py \
  --url "https://www.nature.com/articles/s41586-021-03819-2"

# 从文件批量提取(混合标识符)
python scripts/extract_metadata.py --input identifiers.txt --output citations.bib
```

**元数据来源**(参见 `references/metadata_extraction.md`):

1. **CrossRef API**: DOI 的主要来源
   - 期刊文章的全面元数据
   - 出版商提供的信息
   - 包括作者、标题、期刊、卷、页、日期
   - 免费,无需 API 密钥

2. **PubMed E-utilities**: 生物医学文献
   - 官方 NCBI 元数据
   - 包括 MeSH 术语、摘要
   - PMID 和 PMCID 标识符
   - 免费,建议高容量使用 API 密钥

3. **arXiv API**: 物理、数学、CS、q-bio 中的预印本
   - 预印本的完整元数据
   - 版本跟踪
   - 作者隶属关系
   - 免费,开放获取

4. **DataCite API**: 研究数据集、软件、其他资源
   - 非传统学术输出的元数据
   - 数据集和代码的 DOI
   - 免费访问

**提取内容:**
- **必填字段**: 作者、标题、年份
- **期刊文章**: 期刊、卷、号、页、DOI
- **书籍**: 出版商、ISBN、版本
- **会议论文**: 书名、会议地点、页
- **预印本**: 存储库(arXiv、bioRxiv)、预印本 ID
- **附加**: 摘要、关键词、URL

### 第三阶段: BibTeX 格式化

**目标**: 生成干净、正确格式的 BibTeX 条目。

#### 了解 BibTeX 条目类型

完整指南请参阅 `references/bibtex_formatting.md`。

**常见条目类型:**
- `@article`: 期刊文章(最常见)
- `@book`: 书籍
- `@inproceedings`: 会议论文
- `@incollection`: 书章
- `@phdthesis`: 学位论文
- `@misc`: 预印本、软件、数据集

**按类型的必填字段:**

```bibtex
@article{citationkey,
  author  = {Last1, First1 and Last2, First2},
  title   = {Article Title},
  journal = {Journal Name},
  year    = {2024},
  volume  = {10},
  number  = {3},
  pages   = {123--145},
  doi     = {10.1234/example}
}

@inproceedings{citationkey,
  author    = {Last, First},
  title     = {Paper Title},
  booktitle = {Conference Name},
  year      = {2024},
  pages     = {1--10}
}

@book{citationkey,
  author    = {Last, First},
  title     = {Book Title},
  publisher = {Publisher Name},
  year      = {2024}
}
```

#### 格式化和清理

使用格式化程序标准化 BibTeX 文件:

```bash
# 格式化和清理 BibTeX 文件
python scripts/format_bibtex.py references.bib \
  --output formatted_references.bib

# 按引文键排序
python scripts/format_bibtex.py references.bib \
  --sort key \
  --output sorted_references.bib

# 按年份排序(最新的在前)
python scripts/format_bibtex.py references.bib \
  --sort year \
  --descending \
  --output sorted_references.bib

# 删除重复项
python scripts/format_bibtex.py references.bib \
  --deduplicate \
  --output clean_references.bib

# 验证并报告问题
python scripts/format_bibtex.py references.bib \
  --validate \
  --report validation_report.txt
```

**格式化操作:**
- 标准化字段顺序
- 一致的缩进和间距
- 标题中的正确大写(用 {} 保护)
- 标准化的作者姓名格式
- 一致的引文键格式
- 删除不必要的字段
- 修复常见错误(缺少逗号、大括号)

### 第四阶段: 引文验证

**目标**: 验证所有引文准确且完整。

#### 全面验证

```bash
# 验证 BibTeX 文件
python scripts/validate_citations.py references.bib

# 验证并修复常见问题
python scripts/validate_citations.py references.bib \
  --auto-fix \
  --output validated_references.bib

# 生成详细验证报告
python scripts/validate_citations.py references.bib \
  --report validation_report.json \
  --verbose
```

**验证检查**(参见 `references/citation_validation.md`):

1. **DOI 验证**:
   - DOI 通过 doi.org 正确解析
   - BibTeX 和 CrossRef 之间的元数据匹配
   - 无损坏或无效的 DOI

2. **必填字段**:
   - 条目类型的所有必填字段都存在
   - 无空缺或缺失的关键信息
   - 作者姓名格式正确

3. **数据一致性**:
   - 年份有效(4 位数字,合理范围)
   - 卷/号是数字
   - 页格式正确(例如 123--145)
   - URL 可访问

4. **重复检测**:
   - 同一 DOI 多次使用
   - 相似标题(可能重复)
   - 相同的作者/年份/标题组合

5. **格式合规性**:
   - 有效的 BibTeX 语法
   - 正确的大括号和引号
   - 引文键唯一
   - 特殊字符正确处理

**验证输出:**
```json
{
  "total_entries": 150,
  "valid_entries": 145,
  "errors": [
    {
      "citation_key": "Smith2023",
      "error_type": "missing_field",
      "field": "journal",
      "severity": "high"
    },
    {
      "citation_key": "Jones2022",
      "error_type": "invalid_doi",
      "doi": "10.1234/broken",
      "severity": "high"
    }
  ],
  "warnings": [
    {
      "citation_key": "Brown2021",
      "warning_type": "possible_duplicate",
      "duplicate_of": "Brown2021a",
      "severity": "medium"
    }
  ]
}
```

### 第五阶段: 与写作工作流程集成

#### 为手稿构建参考文献

为创建参考书目的完整工作流程:

```bash
# 1. 搜索您主题的论文
python scripts/search_google_scholar.py "transformer neural networks" \
  --year-start 2017 \
  --limit 50 \
  --output transformers_gs.json

python scripts/search_pubmed.py "deep learning medical imaging" \
  --date-start 2020 \
  --limit 50 \
  --output medical_dl_pm.json

# 2. 从搜索结果提取 DOI 并转换为 BibTeX
python scripts/extract_metadata.py \
  --input transformers_gs.json \
  --output transformers.bib

python scripts/extract_metadata.py \
  --input medical_dl_pm.json \
  --output medical.bib

# 3. 添加您已知的特定论文
python scripts/doi_to_bibtex.py 10.1038/s41586-021-03819-2 >> specific.bib
python scripts/doi_to_bibtex.py 10.1126/science.abcd1234 >> specific.bib

# 4. 格式化和清理 BibTeX 文件
python scripts/format_bibtex.py combined.bib \
  --deduplicate \
  --sort year \
  --descending \
  --output formatted.bib

# 5. 验证所有引文
python scripts/validate_citations.py formatted.bib \
  --auto-fix \
  --report validation.json \
  --output final_references.bib

# 6. 审查验证报告并修复任何剩余问题
cat validation.json

# 7. 在 LaTeX 文档中使用
# \bibliography{final_references}
```

#### 与文献综述技能集成

此技能与 `literature-review` 技能互补:

**文献综述技能** → 系统搜索和综合
**引文管理技能** → 技术引文处理

**组合工作流程:**
1. 使用 `literature-review` 进行全面的多数据库搜索
2. 使用 `citation-management` 提取和验证所有引文
3. 使用 `literature-review` 按主题综合发现
4. 使用 `citation-management` 确保参考书目准确性

## 搜索策略

### Google Scholar 最佳实践

**查找开创性和高影响力论文**(至关重要):

始终基于引用计数、期刊质量和作者声誉对论文进行优先排序:

**引用计数阈值:**
| 论文年龄 | 引用数 | 分类 |
|-----------|---------|--------|
| 0-3 年 | 20+ | 值得注意 |
| 0-3 年 | 100+ | 高影响力 |
| 3-7 年 | 100+ | 重要 |
| 3-7 年 | 500+ | 标志性论文 |
| 7+ 年 | 500+ | 开创性工作 |
| 7+ 年 | 1000+ | 基础性 |

**期刊质量等级:**
- **第一级(首选)**: Nature、Science、Cell、NEJM、Lancet、JAMA、PNAS
- **第二级(高优先级)**: 影响因子 >10,顶级会议(NeurIPS、ICML、ICLR)
- **第三级(良好)**: 专业期刊(IF 5-10)
- **第四级(谨慎使用)**: 低影响力同行评审期刊

**作者声誉指标:**
- h-index >40 的高级研究人员
- 在第一级期刊发表多篇论文
- 在知名机构担任领导职务
- 获奖和编辑职位

**高影响力论文的搜索策略:**
- 按引用计数排序(最被引在前)
- 查找第一级期刊的综述文章以获取概述
- 检查"被引用次数"以进行影响力评估和最新后续工作
- 使用引用警报跟踪关键论文的新引用
- 使用 `source:Nature` 或 `source:Science` 按顶级期刊筛选
- 使用 `author:LastName` 搜索已知领域领导者的论文

**高级运算符**(完整列表见 `references/google_scholar_search.md`):
```
"exact phrase"           # 精确短语匹配
author:lastname          # 按作者搜索
intitle:keyword          # 仅在标题中搜索
source:journal           # 搜索特定期刊
-exclude                 # 排除术语
OR                       # 替代术语
2020..2024              # 年份范围
```

**示例搜索:**
```
# 查找主题的最近综述
"CRISPR" intitle:review 2023..2024

# 按主题搜索特定作者的论文
author:Church "synthetic biology"

# 查找高被引基础性工作
"deep learning" 2012..2015 sort:citations

# 排除调查并专注于方法
"protein folding" -survey -review intitle:method
```

### PubMed 最佳实践

**使用 MeSH 术语:**
MeSH(医学主题词)为精确搜索提供控制词汇。

1. 在 https://meshb.nlm.nih.gov/search 查找 MeSH 术语
2. 在查询中使用: `"Diabetes Mellitus, Type 2"[MeSH]`
3. 与关键词结合以实现全面覆盖

**字段标签:**
```
[Title]              # 仅在标题中搜索
[Title/Abstract]     # 在标题或摘要中搜索
[Author]             # 按作者姓名搜索
[Journal]            # 搜索特定期刊
[Publication Date]   # 日期范围
[Publication Type]   # 文章类型
[MeSH]              # MeSH 术语
```

**构建复杂查询:**
```bash
# 最近发表的糖尿病治疗临床试验
"Diabetes Mellitus, Type 2"[MeSH] AND "Drug Therapy"[MeSH] 
AND "Clinical Trial"[Publication Type] AND 2020:2024[Publication Date]

# 特定期刊中的 CRISPR 综述
"CRISPR-Cas Systems"[MeSH] AND "Nature"[Journal] AND "Review"[Publication Type]

# 特定作者的最近工作
"Smith AB"[Author] AND cancer[Title/Abstract] AND 2022:2024[Publication Date]
```

**E-utilities 自动化:**
脚本使用 NCBI E-utilities API 进行编程访问:
- **ESearch**: 搜索和检索 PMIDs
- **EFetch**: 检索完整元数据
- **ESummary**: 获取摘要信息
- **ELink**: 查找相关文章

完整 API 文档请参阅 `references/pubmed_search.md`。

## 工具和脚本

### search_google_scholar.py

搜索 Google Scholar 并导出结果。

**功能:**
- 自动搜索和速率限制
- 分页支持
- 年份范围筛选
- 导出为 JSON 或 BibTeX
- 引用计数信息

**用法:**
```bash
# 基本搜索
python scripts/search_google_scholar.py "quantum computing"

# 使用筛选器的高级搜索
python scripts/search_google_scholar.py "quantum computing" \
  --year-start 2020 \
  --year-end 2024 \
  --limit 100 \
  --sort-by citations \
  --output quantum_papers.json

# 直接导出为 BibTeX
python scripts/search_google_scholar.py "machine learning" \
  --limit 50 \
  --format bibtex \
  --output ml_papers.bib
```

### search_pubmed.py

使用 E-utilities API 搜索 PubMed。

**功能:**
- 复杂查询支持(MeSH、字段标签、布尔运算符)
- 日期范围筛选
- 发表类型筛选
- 批量检索和元数据
- 导出为 JSON 或 BibTeX

**用法:**
```bash
# 简单关键词搜索
python scripts/search_pubmed.py "CRISPR gene editing"

# 使用筛选器的复杂查询
python scripts/search_pubmed.py \
  --query '"CRISPR-Cas Systems"[MeSH] AND "therapeutic"[Title/Abstract]' \
  --date-start 2020-01-01 \
  --date-end 2024-12-31 \
  --publication-types "Clinical Trial,Review" \
  --limit 200 \
  --output crispr_therapeutic.json

# 导出为 BibTeX
python scripts/search_pubmed.py "Alzheimer's disease" \
  --limit 100 \
  --format bibtex \
  --output alzheimers.bib
```

### extract_metadata.py

从论文标识符提取完整元数据。

**功能:**
- 支持 DOI、PMID、arXiv ID、URL
- 查询 CrossRef、PubMed、arXiv API
- 处理多种标识符类型
- 批量处理
- 多种输出格式

**用法:**
```bash
# 单个 DOI
python scripts/extract_metadata.py --doi 10.1038/s41586-021-03819-2

# 单个 PMID
python scripts/extract_metadata.py --pmid 34265844

# 单个 arXiv ID
python scripts/extract_metadata.py --arxiv 2103.14030

# 从 URL
python scripts/extract_metadata.py \
  --url "https://www.nature.com/articles/s41586-021-03819-2"

# 批量处理(文件中每行一个标识符)
python scripts/extract_metadata.py \
  --input paper_ids.txt \
  --output references.bib

# 不同的输出格式
python scripts/extract_metadata.py \
  --doi 10.1038/nature12345 \
  --format json  # 或 bibtex, yaml
```

### validate_citations.py

验证 BibTeX 条目的准确性和完整性。

**功能:**
- 通过 doi.org 和 CrossRef 进行 DOI 验证
- 必填字段检查
- 重复检测
- 格式验证
- 自动修复常见问题
- 详细报告

**用法:**
```bash
# 基本验证
python scripts/validate_citations.py references.bib

# 使用自动修复
python scripts/validate_citations.py references.bib \
  --auto-fix \
  --output fixed_references.bib

# 详细验证报告
python scripts/validate_citations.py references.bib \
  --report validation_report.json \
  --verbose

# 仅检查 DOI
python scripts/validate_citations.py references.bib \
  --check-dois-only
```

### format_bibtex.py

格式化和清理 BibTeX 文件。

**功能:**
- 标准化格式化
- 按键、年份、作者排序条目
- 删除重复项
- 验证语法
- 修复常见错误
- 强制执行引文键约定

**用法:**
```bash
# 基本格式化
python scripts/format_bibtex.py references.bib

# 按年份排序(最新的在前)
python scripts/format_bibtex.py references.bib \
  --sort year \
  --descending \
  --output sorted_refs.bib

# 删除重复项
python scripts/format_bibtex.py references.bib \
  --deduplicate \
  --output clean_refs.bib

# 完整清理
python scripts/format_bibtex.py references.bib \
  --deduplicate \
  --sort year \
  --validate \
  --auto-fix \
  --output final_refs.bib
```

### doi_to_bibtex.py

快速 DOI 到 BibTeX 转换。

**功能:**
- 快速单个 DOI 转换
- 批量处理
- 多种输出格式
- 剪贴板支持

**用法:**
```bash
# 单个 DOI
python scripts/doi_to_bibtex.py 10.1038/s41586-021-03819-2

# 多个 DOI
python scripts/doi_to_bibtex.py \
  10.1038/nature12345 \
  10.1126/science.abc1234 \
  10.1016/j.cell.2023.01.001

# 从文件(每行一个 DOI)
python scripts/doi_to_bibtex.py --input dois.txt --output references.bib

# 复制到剪贴板
python scripts/doi_to_bibtex.py 10.1038/nature12345 --clipboard
```

## 最佳实践

### 搜索策略

1. **先宽后窄**:
   - 从一般术语开始以了解领域
   - 使用具体关键词和筛选器进行细化
   - 使用同义词和相关术语

2. **使用多个来源**:
   - Google Scholar 用于全面覆盖
   - PubMed 用于生物医学重点
   - arXiv 用于预印本
   - 结合结果以确保完整性

3. **利用引用**:
   - 检查"被引用次数"以查找开创性论文
   - 审查关键论文的参考文献
   - 使用引用网络发现相关工作

4. **记录您的搜索**:
   - 保存搜索查询和日期
   - 记录结果数量
   - 注意应用的任何筛选器或限制

### 元数据提取

1. **可用时始终使用 DOI**:
   - 最可靠的标识符
   - 发表的永久链接
   - 通过 CrossRef 获取最佳元数据

2. **验证提取的元数据**:
   - 检查作者姓名正确
   - 验证期刊/会议名称
   - 确认发表年份
   - 验证页码和卷

3. **处理边缘情况**:
   - 预印本: 包括存储库和 ID
   - 预印本后来发表: 使用发表版本
   - 会议论文: 包括会议名称和地点
   - 书章: 包括书名和编辑

4. **保持一致性**:
   - 使用一致的作者姓名格式
   - 标准化期刊缩写
   - 使用相同的 DOI 格式(URL 首选)

### BibTeX 质量

1. **遵循约定**:
   - 使用有意义的引文键(FirstAuthor2024keyword)
   - 用 {} 保护标题中的大写
   - 使用 -- 表示页码范围(不是单个破折号)
   - 为所有现代发表包括 DOI 字段

2. **保持干净**:
   - 删除不必要的字段
   - 无冗余信息
   - 一致的格式化
   - 定期验证语法

3. **系统组织**:
   - 按年份或主题排序
   - 分组相关论文
   - 为不同项目使用单独的文件
   - 合并时小心避免重复

### 验证

1. **尽早且频繁验证**:
   - 添加引文时检查
   - 提交前验证完整参考书目
   - 任何手动编辑后重新验证

2. **立即修复问题**:
   - 损坏的 DOI: 查找正确的标识符
   - 缺失字段: 从原始来源提取
   - 重复项: 选择最佳版本,删除其他
   - 格式错误: 安全时使用自动修复

3. **关键引文的手动审查**:
   - 验证关键论文引用正确
   - 检查作者姓名与发表匹配
   - 确认页码和卷
   - 确保 URL 当前

## 常见陷阱

1. **单一来源偏见**: 仅使用 Google Scholar 或 PubMed
   - **解决方案**: 搜索多个数据库以实现全面覆盖

2. **盲目接受元数据**: 不验证提取的信息
   - **解决方案**: 根据原始来源抽查提取的元数据

3. **忽略 DOI 错误**: 参考书目中有损坏或不正确的 DOI
   - **解决方案**: 最终提交前运行验证

4. **不一致的格式化**: 混合的引文键样式、格式化
   - **解决方案**: 使用 format_bibtex.py 进行标准化

5. **重复条目**: 同一论文多次引用,键不同
   - **解决方案**: 使用验证中的重复检测

6. **缺失必填字段**: 不完整的 BibTeX 条目
   - **解决方案**: 验证并确保所有必填字段都存在

7. **过时的预印本**: 存在发表版本时引用预印本
   - **解决方案**: 检查预印本是否已发表,更新为期刊版本

8. **特殊字符问题**: 由于字符导致 LaTeX 编译失败
   - **解决方案**: 在 BibTeX 中使用正确的转义或 Unicode

9. **提交前无验证**: 提交时有引文错误
   - **解决方案**: 始终将验证作为最终检查运行

10. **手动 BibTeX 条目**: 手动输入条目
    - **解决方案**: 始终使用脚本从元数据来源提取

## 示例工作流程

### 示例 1: 为论文构建参考书目

```bash
# 步骤 1: 查找您主题的关键论文
python scripts/search_google_scholar.py "transformer neural networks" \
  --year-start 2017 \
  --limit 50 \
  --output transformers_gs.json

python scripts/search_pubmed.py "deep learning medical imaging" \
  --date-start 2020 \
  --limit 50 \
  --output medical_dl_pm.json

# 步骤 2: 从搜索结果提取元数据
python scripts/extract_metadata.py \
  --input transformers_gs.json \
  --output transformers.bib

python scripts/extract_metadata.py \
  --input medical_dl_pm.json \
  --output medical.bib

# 步骤 3: 添加您已知的特定论文
python scripts/doi_to_bibtex.py 10.1038/s41586-021-03819-2 >> specific.bib
python scripts/doi_to_bibtex.py 10.1126/science.aam9317 >> specific.bib

# 步骤 4: 合并所有 BibTeX 文件
cat transformers.bib medical.bib specific.bib > combined.bib

# 步骤 5: 格式化和去重
python scripts/format_bibtex.py combined.bib \
  --deduplicate \
  --sort year \
  --descending \
  --output formatted.bib

# 步骤 6: 验证
python scripts/validate_citations.py formatted.bib \
  --auto-fix \
  --report validation.json \
  --output final_references.bib

# 步骤 7: 审查任何问题
cat validation.json | grep -A 3 '"errors"'

# 步骤 8: 在 LaTeX 中使用
# \bibliography{final_references}
```

### 示例 2: 转换 DOI 列表

```bash
# 您有一个包含 DOI 的文本文件(每行一个)
# dois.txt 包含:
# 10.1038/s41586-021-03819-2
# 10.1126/science.aam9317
# 10.1016/j.cell.2023.01.001

# 全部转换为 BibTeX
python scripts/doi_to_bibtex.py --input dois.txt --output references.bib

# 验证结果
python scripts/validate_citations.py references.bib --verbose
```

### 示例 3: 清理现有的 BibTeX 文件

```bash
# 您有一个来自各种来源的混乱 BibTeX 文件
# 系统地清理它

# 步骤 1: 格式化和标准化
python scripts/format_bibtex.py messy_references.bib \
  --output step1_formatted.bib

# 步骤 2: 删除重复项
python scripts/format_bibtex.py step1_formatted.bib \
  --deduplicate \
  --output step2_deduplicated.bib

# 步骤 3: 验证和自动修复
python scripts/validate_citations.py step2_deduplicated.bib \
  --auto-fix \
  --output step3_validated.bib

# 步骤 4: 按年份排序
python scripts/format_bibtex.py step3_validated.bib \
  --sort year \
  --descending \
  --output clean_references.bib

# 步骤 5: 最终验证报告
python scripts/validate_citations.py clean_references.bib \
  --report final_validation.json \
  --verbose

# 审查报告
cat final_validation.json
```

### 示例 4: 查找和引用开创性论文

```bash
# 查找主题的高被引论文
python scripts/search_google_scholar.py "AlphaFold protein structure" \
  --year-start 2020 \
  --year-end 2024 \
  --sort-by citations \
  --limit 20 \
  --output alphafold_seminal.json

# 提取前 10 个按引用计数
# (脚本将在 JSON 中包含引用计数)

# 转换为 BibTeX
python scripts/extract_metadata.py \
  --input alphafold_seminal.json \
  --output alphafold_refs.bib

# BibTeX 文件现在包含最有影响力的论文
```

## 与其他技能集成

### 文献综述技能

**引文管理**为**文献综述**提供技术基础设施:

- **文献综述**: 多数据库系统搜索和综合
- **引文管理**: 元数据提取和验证

**组合工作流程:**
1. 使用 literature-review 进行系统搜索方法
2. 使用 citation-management 提取和验证引文
3. 使用 literature-review 综合发现
4. 使用 citation-management 确保参考书目准确性

### 科学写作技能

**引文管理**确保**科学写作**的准确参考:

- 导出验证的 BibTeX 用于 LaTeX 手稿
- 验证引文符合发表标准
- 根据期刊要求格式化参考文献

### 场所模板技能

**引文管理**与**场所示例**一起用于提交就绪的手稿:

- 不同场所需不同的引文风格
- 生成正确格式的参考文献
- 验证引文符合场所示求

## 资源

### 捆绑资源

**参考**(在 `references/` 中):
- `google_scholar_search.md`: 完整的 Google Scholar 搜索指南
- `pubmed_search.md`: PubMed 和 E-utilities API 文档
- `metadata_extraction.md`: 元数据来源和字段要求
- `citation_validation.md`: 验证标准和质量检查
- `bibtex_formatting.md`: BibTeX 条目类型和格式化规则

**脚本**(在 `scripts/` 中):
- `search_google_scholar.py`: Google Scholar 搜索自动化
- `search_pubmed.py`: PubMed E-utilities API 客户端
- `extract_metadata.py`: 通用元数据提取器
- `validate_citations.py`: 引文验证和验证
- `format_bibtex.py`: BibTeX 格式化程序和清理器
- `doi_to_bibtex.py`: 快速 DOI 到 BibTeX 转换器

**资产**(在 `assets/` 中):
- `bibtex_template.bib`: 所有类型的示例 BibTeX 条目
- `citation_checklist.md`: 质量保证检查清单

### 外部资源

**搜索引擎:**
- Google Scholar: https://scholar.google.com/
- PubMed: https://pubmed.ncbi.nlm.nih.gov/
- PubMed 高级搜索: https://pubmed.ncbi.nlm.nih.gov/advanced/

**元数据 API:**
- CrossRef API: https://api.crossref.org/
- PubMed E-utilities: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- arXiv API: https://arxiv.org/help/api/
- DataCite API: https://api.datacite.org/

**工具和验证器:**
- MeSH Browser: https://meshb.nlm.nih.gov/search
- DOI 解析器: https://doi.org/
- BibTeX 格式: http://www.bibtex.org/Format/

**引文风格:**
- BibTeX 文档: http://www.bibtex.org/
- LaTeX 参考书目管理: https://www.overleaf.com/learn/latex/Bibliography_management

## 依赖项

### 必需的 Python 包

```bash
# 核心依赖
pip install requests  # API 的 HTTP 请求
pip install bibtexparser  # BibTeX 解析和格式化
pip install biopython  # PubMed E-utilities 访问

# 可选(用于 Google Scholar)
pip install scholarly  # Google Scholar API 包装器
# 或
pip install selenium  # 用于更强大的 Scholar 抓取
```

### 可选工具

```bash
# 用于高级验证
pip install crossref-commons  # 增强的 CrossRef API 访问
pip install pylatexenc  # LaTeX 特殊字符处理
```

## 摘要

引文管理技能提供:

1. **全面的搜索功能**,用于 Google Scholar 和 PubMed
2. **自动元数据提取**,来自 DOI、PMID、arXiv ID、URL
3. **引文验证**,包含 DOI 验证和完整性检查
4. **BibTeX 格式化**,包含标准化和清理工具
5. **质量保证**,通过验证和报告
6. **集成**,与科学写作工作流程
7. **可重现性**,通过记录的搜索和提取方法

使用此技能在整个研究和写作过程中维护准确、完整的引文,并确保提交就绪的参考书目。
