---
name: literature-review
description: 使用多个学术数据库（PubMed、arXiv、bioRxiv、Semantic Scholar等）进行全面、系统的文献综述。该技能应在进行系统文献综述、荟萃分析、研究综合或跨生物医学、科学和技术领域的全面文献搜索时使用。创建具有多种引文格式（APA、Nature、Vancouver等）验证引文的专业格式化markdown文档和PDF。
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# 文献综述

## 概述

遵循严格的学术方法论进行系统、全面的文献综述。搜索多个文献数据库，按主题综合发现，验证所有引文的准确性，并生成markdown和PDF格式的专业输出文档。

该技能集成了多个科学技能用于数据库访问（gget、bioservices、datacommons-client），并提供了专门的引文验证、结果聚合和文档生成工具。

## 何时使用此技能

在以下情况下使用此技能：
- 为研究或发表进行系统文献综述
- 跨多个来源综合特定主题的当前知识
- 进行荟萃分析或范围综述
- 撰写研究论文或学位论文的文献综述部分
- 调查研究领域的最新进展
- 识别研究空白和未来方向
- 需要验证引文和专业格式

## 使用科学图表进行视觉增强

**⚠️ 强制要求：每个文献综述必须至少包含1-2个使用scientific-schematics技能生成的AI生成图表。**

这不是可选的。没有视觉元素的文献综述是不完整的。在最终确定任何文档之前：
1. 至少生成一个示意图或图表（例如，系统综述的PRISMA流程图）
2. 对于全面综述，最好有2-3个图表（搜索策略流程图、主题综合图、概念框架）

**如何生成图表：**
- 使用 **scientific-schematics** 技能生成AI驱动的出版质量图表
- 只需用自然语言描述您想要的图表
- Nano Banana Pro将自动生成、审查和完善示意图

**如何生成示意图：**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

AI将自动：
- 创建具有正确格式的出版质量图像
- 通过多次迭代进行审查和完善
- 确保可访问性（色盲友好、高对比度）
- 将输出保存在figures/目录中

**何时添加示意图：**
- 系统综述的PRISMA流程图
- 文献搜索策略流程图
- 主题综合图
- 研究空白可视化图
- 引文网络图
- 概念框架图
- 任何受益于可视化的复杂概念

有关创建示意图的详细指导，请参阅scientific-schematics技能文档。

---

## 核心工作流程

文献综述遵循结构化的多阶段工作流程：

### 阶段1：规划和范围界定

1. **定义研究问题**：使用PICO框架（人群、干预、比较、结果）进行临床/生物医学综述
   - 示例："CRISPR-Cas9（I）治疗镰状细胞病（P）与标准治疗（C）相比的疗效如何？"

2. **确定范围和目标**：
   - 定义清晰、具体的研究问题
   - 确定综述类型（叙述性、系统性、范围性、荟萃分析）
   - 设置边界（时间范围、地理范围、研究类型）

3. **制定搜索策略**：
   - 从研究问题中识别2-4个主要概念
   - 列出每个概念的同义词、缩写和相关术语
   - 规划布尔运算符（AND、OR、NOT）以组合术语
   - 选择至少3个互补数据库

4. **设置纳入/排除标准**：
   - 日期范围（例如，最近10年：2015-2024）
   - 语言（通常为英语，或指定多语言）
   - 发表类型（同行评审、预印本、综述）
   - 研究设计（RCT、观察性、体外等）
   - 清楚记录所有标准

### 阶段2：系统文献搜索

1. **多数据库搜索**：

   选择适合该领域的数据库：

   **生物医学与生命科学：**
   - 使用 `gget` 技能：`gget search pubmed "search terms"` 搜索PubMed/PMC
   - 使用 `gget` 技能：`gget search biorxiv "search terms"` 搜索预印本
   - 使用 `bioservices` 技能搜索ChEMBL、KEGG、UniProt等

   **通用科学文献：**
   - 通过直接API搜索arXiv（物理、数学、计算机科学、q-bio的预印本）
   - 通过API搜索Semantic Scholar（2亿+论文，跨学科）
   - 使用Google Scholar进行全面覆盖（手动或谨慎爬取）

   **专业数据库：**
   - 使用 `gget alphafold` 搜索蛋白质结构
   - 使用 `gget cosmic` 搜索癌症基因组学
   - 使用 `datacommons-client` 搜索人口统计/统计数据
   - 根据领域使用适当的专业数据库

2. **记录搜索参数：**
   ```markdown
   ## 搜索策略

   ### 数据库：PubMed
   - **搜索日期**：2024-10-25
   - **日期范围**：2015-01-01 至 2024-10-25
   - **搜索字符串**：
     ```
     ("CRISPR"[Title] OR "Cas9"[Title])
     AND ("sickle cell"[MeSH] OR "SCD"[Title/Abstract])
     AND 2015:2024[Publication Date]
     ```
   - **结果**：247篇文章
   ```

   对每个搜索的数据库重复此操作。

3. **导出和聚合结果**：
   - 从每个数据库以JSON格式导出结果
   - 将所有结果合并到一个文件中
   - 使用 `scripts/search_databases.py` 进行后处理：
     ```bash
     python search_databases.py combined_results.json \
       --deduplicate \
       --format markdown \
       --output aggregated_results.md
     ```

### 阶段3：筛选和选择

1. **去重**：
   ```bash
   python search_databases.py results.json --deduplicate --output unique_results.json
   ```
   - 按DOI（主要）或标题（后备）删除重复项
   - 记录删除的重复项数量

2. **标题筛选**：
   - 根据纳入/排除标准审查所有标题
   - 排除明显不相关的研究
   - 记录在此阶段排除的数量

3. **摘要筛选**：
   - 阅读剩余研究的摘要
   - 严格应用纳入/排除标准
   - 记录排除原因

4. **全文筛选**：
   - 获取剩余研究的全文
   - 根据所有标准进行详细审查
   - 记录排除的具体原因
   - 记录最终纳入的研究数量

5. **创建PRISMA流程图**：
   ```
   初始搜索：n = X
   ├─ 去重后：n = Y
   ├─ 标题筛选后：n = Z
   ├─ 摘要筛选后：n = A
   └─ 纳入综述：n = B
   ```

### 阶段4：数据提取和质量评估

1. **从每个纳入的研究中提取关键数据**：
   - 研究元数据（作者、年份、期刊、DOI）
   - 研究设计和方法
   - 样本量和人群特征
   - 关键发现和结果
   - 作者指出的局限性
   - 资金来源和利益冲突

2. **评估研究质量**：
   - **对于RCT**：使用Cochrane偏倚风险工具
   - **对于观察性研究**：使用Newcastle-Ottawa量表
   - **对于系统综述**：使用AMSTAR 2
   - 对每项研究进行评级：高、中、低或极低质量
   - 考虑排除极低质量的研究

3. **按主题组织**：
   - 识别跨研究的3-5个主要主题
   - 按主题对研究进行分组（研究可能出现在多个主题中）
   - 注意模式、共识和争议

### 阶段5：综合和分析

1. **从模板创建综述文档**：
   ```bash
   cp assets/review_template.md my_literature_review.md
   ```

2. **撰写主题综合**（而非逐项研究总结）：
   - 按主题或研究问题组织结果部分
   - 在每个主题内综合跨多项研究的发现
   - 比较和对比不同的方法和结果
   - 识别共识领域和争议点
   - 突出最有力的证据

   示例结构：
   ```markdown
   #### 3.3.1 主题：CRISPR递送方法

   已研究多种递送方法用于治疗性基因编辑。病毒载体（AAV）在15项研究^1-15^中使用，
   显示出高转导效率（65-85%）但引起免疫原性担忧^3,7,12^。相比之下，脂质纳米颗粒显示出较低的
   效率（40-60%）但改善了安全性^16-23^。
   ```

3. **批判性分析**：
   - 评估跨研究的方法学优势和局限性
   - 评估证据的质量和一致性
   - 识别知识空白和方法学空白
   - 注意需要未来研究的领域

4. **撰写讨论**：
   - 在更广泛的背景下解释发现
   - 讨论临床、实践或研究意义
   - 承认综述本身的局限性
   - 如适用，与以前的综述进行比较
   - 提出具体的未来研究方向

### 阶段6：引文验证

**关键**：所有引文必须在最终提交前进行准确性验证。

1. **验证所有DOI**：
   ```bash
   python scripts/verify_citations.py my_literature_review.md
   ```

   该脚本：
   - 从文档中提取所有DOI
   - 验证每个DOI正确解析
   - 从CrossRef检索元数据
   - 生成验证报告
   - 输出正确格式的引文

2. **审查验证报告**：
   - 检查任何失败的DOI
   - 验证作者姓名、标题和发表详细信息匹配
   - 更正原始文档中的任何错误
   - 重新运行验证直到所有引文通过

3. **一致格式化引文**：
   - 选择一种引文格式并在全文中使用（参见 `references/citation_styles.md`）
   - 常见格式：APA、Nature、Vancouver、Chicago、IEEE
   - 使用验证脚本输出正确格式化引文
   - 确保文中引文与参考文献列表格式匹配

### 阶段7：文档生成

1. **生成PDF**：
   ```bash
   python scripts/generate_pdf.py my_literature_review.md \
     --citation-style apa \
     --output my_review.pdf
   ```

   选项：
   - `--citation-style`：apa、nature、chicago、vancouver、ieee
   - `--no-toc`：禁用目录
   - `--no-numbers`：禁用章节编号
   - `--check-deps`：检查是否安装了pandoc/xelatex

2. **审查最终输出**：
   - 检查PDF格式和布局
   - 验证所有部分都存在
   - 确保引文正确渲染
   - 检查图表/表格是否正确显示
   - 验证目录准确

3. **质量检查清单**：
   - [ ] 所有DOI已通过verify_citations.py验证
   - [ ] 引文格式一致
   - [ ] 包含PRISMA流程图（对于系统综述）
   - [ ] 搜索方法已完整记录
   - [ ] 纳入/排除标准已清楚说明
   - [ ] 结果按主题组织（而非逐项研究）
   - [ ] 质量评估已完成
   - [ ] 已承认局限性
   - [ ] 参考文献完整且准确
   - [ ] PDF生成无错误

## 数据库特定搜索指南

### PubMed / PubMed Central

通过 `gget` 技能访问：
```bash
# 搜索PubMed
gget search pubmed "CRISPR gene editing" -l 100

# 使用过滤器
# 使用PubMed高级搜索构建器构建复杂查询
# 然后通过gget或直接Entrez API执行
```

**搜索提示**：
- 使用MeSH术语：`"sickle cell disease"[MeSH]`
- 字段标签：`[Title]`、`[Title/Abstract]`、`[Author]`
- 日期过滤器：`2020:2024[Publication Date]`
- 布尔运算符：AND、OR、NOT
- 参见MeSH浏览器：https://meshb.nlm.nih.gov/search

### bioRxiv / medRxiv

通过 `gget` 技能访问：
```bash
gget search biorxiv "CRISPR sickle cell" -l 50
```

**重要注意事项**：
- 预印本未经同行评审
- 谨慎验证发现
- 检查预印本是否已发表（CrossRef）
- 记录预印本版本和日期

### arXiv

通过直接API或WebFetch访问：
```python
# 示例搜索类别：
# q-bio.QM（定量方法）
# q-bio.GN（基因组学）
# q-bio.MN（分子网络）
# cs.LG（机器学习）
# stat.ML（机器学习统计）

# 搜索格式：category AND terms
search_query = "cat:q-bio.QM AND ti:\"single cell sequencing\""
```

### Semantic Scholar

通过直接API访问（需要API密钥，或使用免费层）：
- 跨所有领域2亿+论文
- 非常适合跨学科搜索
- 提供引文图和论文推荐
- 用于查找高影响力论文

### 专业生物医学数据库

使用适当技能：
- **ChEMBL**：`bioservices` 技能用于化学生物活性
- **UniProt**：`gget` 或 `bioservices` 技能用于蛋白质信息
- **KEGG**：`bioservices` 技能用于通路和基因
- **COSMIC**：`gget` 技能用于癌症突变
- **AlphaFold**：`gget alphafold` 用于蛋白质结构
- **PDB**：`gget` 或直接API用于实验结构

### 引文链式搜索

通过引文网络扩展搜索：

1. **前向引文**（引用关键论文的论文）：
   - 使用Google Scholar"被引用"
   - 使用Semantic Scholar或OpenAlex API
   - 识别在开创性工作基础上构建的较新研究

2. **后向引文**（关键论文中的参考文献）：
   - 从纳入的论文中提取参考文献
   - 识别高引用的基础工作
   - 查找被多个纳入研究引用的论文

## 引文格式指南

`references/citation_styles.md`中有详细的格式化指南。快速参考：

### APA（第7版）
- 文中：(Smith et al., 2023)
- 参考文献：Smith, J. D., Johnson, M. L., & Williams, K. R. (2023). Title. *Journal*, *22*(4), 301-318. https://doi.org/10.xxx/yyy

### Nature
- 文中：上标数字^1,2^
- 参考文献：Smith, J. D., Johnson, M. L. & Williams, K. R. Title. *Nat. Rev. Drug Discov.* **22**, 301-318 (2023).

### Vancouver
- 文中：上标数字^1,2^
- 参考文献：Smith JD, Johnson ML, Williams KR. Title. Nat Rev Drug Discov. 2023;22(4):301-18.

**在最终确定之前始终验证引文**，使用verify_citations.py。

### 优先考虑高影响力论文（关键）

**始终优先考虑来自知名作者和顶级期刊的有影响力、高引用论文。** 在文献综述中，质量比数量更重要。

#### 引文计数阈值

使用引文计数识别最有影响力的论文：

| 论文年龄 | 引文阈值 | 分类 |
|-----------|-----------|--------|
| 0-3年 | 20+引用 | 值得注意 |
| 0-3年 | 100+引用 | 高影响力 |
| 3-7年 | 100+引用 | 重要 |
| 3-7年 | 500+引用 | 里程碑论文 |
| 7年以上 | 500+引用 | 开创性工作 |
| 7年以上 | 1000+引用 | 基础性 |

#### 期刊和场所层级

优先考虑来自更高层级场所的论文：

- **层级1（始终首选）**：Nature、Science、Cell、NEJM、Lancet、JAMA、PNAS、Nature Medicine、Nature Biotechnology
- **层级2（强偏好）**：高影响力专业期刊（IF>10）、顶级会议（ML/AI的NeurIPS、ICML）
- **层级3（相关时包括）**：受人尊敬的专业期刊（IF 5-10）
- **层级4（谨慎使用）**：低影响力同行评审场所

#### 作者声誉评估

优先考虑来自以下机构的论文：
- **资深研究人员**，具有高h指数（在既定领域>40）
- **知名机构**的领先研究组（哈佛、斯坦福、麻省理工、牛津等）
- **在相关领域具有多篇层级1发表**的作者
- **具有公认专业知识**的研究人员（奖项、编辑职位、学会会员）

#### 识别开创性论文

对于任何主题，通过以下方式识别基础工作：
1. **高引文计数**（通常5年以上论文500+）
2. **经常被其他纳入研究引用**（出现在许多参考文献列表中）
3. **发表在层级1场所**（Nature、Science、Cell家族）
4. **由领域先驱撰写**（通常被引用为建立概念）

## 最佳实践

### 搜索策略
1. **使用多个数据库**（最少3个）：确保全面覆盖
2. **包括预印本服务器**：捕获最新的未发表发现
3. **记录所有内容**：搜索字符串、日期、结果计数以确保可重复性
4. **测试和完善**：运行试点搜索，审查结果，调整搜索术语
5. **按引文排序**：可用时，按引文计数对搜索结果进行排序，首先突出有影响力的工作

### 筛选和选择
1. **使用多个数据库**（最少3个）：确保全面覆盖
2. **包括预印本服务器**：捕获最新的未发表发现
3. **记录所有内容**：搜索字符串、日期、结果计数以确保可重复性
4. **测试和完善**：运行试点搜索，审查结果，调整搜索术语

### 筛选和选择
1. **使用明确标准**：在筛选之前记录纳入/排除标准
2. **系统筛选**：标题 → 摘要 → 全文
3. **记录排除**：记录排除研究的原因
4. **考虑双重筛选**：对于系统综述，让两名评审员独立筛选

### 综合
1. **按主题组织**：按主题而非按单项研究分组
2. **跨研究综合**：比较、对比、识别模式
3. **批判性**：评估证据的质量和一致性
4. **识别空白**：注意缺失或研究不足的内容

### 质量和可重复性
1. **评估研究质量**：使用适当的质量评估工具
2. **验证所有引文**：运行verify_citations.py脚本
3. **记录方法学**：提供足够的细节供他人重复
4. **遵循指南**：使用PRISMA进行系统综述

### 写作
1. **客观**：公平呈现证据，承认局限性
2. **系统**：遵循结构化模板
3. **具体**：在可用时包括数字、统计数据、效应大小
4. **清晰**：使用清晰的标题、逻辑流程、主题组织

## 常见陷阱

1. **单数据库搜索**：遗漏相关论文；始终搜索多个数据库
2. **无搜索记录**：使综述不可重复；记录所有搜索
3. **逐项研究总结**：缺乏综合；改为按主题组织
4. **未验证引文**：导致错误；始终运行verify_citations.py
5. **搜索过宽**：产生数千个不相关结果；用具体术语完善
6. **搜索过窄**：遗漏相关论文；包括同义词和相关术语
7. **忽略预印本**：遗漏最新发现；包括bioRxiv、medRxiv、arXiv
8. **无质量评估**：同等对待所有证据；评估和报告质量
9. **发表偏倚**：仅发表阳性结果；注意潜在偏倚
10. **搜索过时**：领域快速演变；清楚说明搜索日期

## 示例工作流程

生物医学文献综述的完整工作流程：

```bash
# 1. 从模板创建综述文档
cp assets/review_template.md crispr_sickle_cell_review.md

# 2. 使用适当技能搜索多个数据库
# - 使用gget技能搜索PubMed、bioRxiv
# - 使用直接API访问arXiv、Semantic Scholar
# - 以JSON格式导出结果

# 3. 聚合和处理结果
python scripts/search_databases.py combined_results.json \
  --deduplicate \
  --rank citations \
  --year-start 2015 \
  --year-end 2024 \
  --format markdown \
  --output search_results.md \
  --summary

# 4. 筛选结果并提取数据
# - 手动筛选标题、摘要、全文
# - 将关键数据提取到综述文档中
# - 按主题组织

# 5. 按照模板结构撰写综述
# - 带有明确目标的引言
# - 详细方法学部分
# - 按主题组织的结果
# - 批判性讨论
# - 清晰的结论

# 6. 验证所有引文
python scripts/verify_citations.py crispr_sickle_cell_review.md

# 审查引文报告
cat crispr_sickle_cell_review_citation_report.json

# 修复任何失败的引文并重新验证
python scripts/verify_citations.py crispr_sickle_cell_review.md

# 7. 生成专业PDF
python scripts/generate_pdf.py crispr_sickle_cell_review.md \
  --citation-style nature \
  --output crispr_sickle_cell_review.pdf

# 8. 审查最终PDF和markdown输出
```

## 与其他技能的集成

该技能与其他科学技能无缝协作：

### 数据库访问技能
- **gget**：PubMed、bioRxiv、COSMIC、AlphaFold、Ensembl、UniProt
- **bioservices**：ChEMBL、KEGG、Reactome、UniProt、PubChem
- **datacommons-client**：人口统计、经济学、健康统计

### 分析技能
- **pydeseq2**：RNA-seq差异表达（用于方法部分）
- **scanpy**：单细胞分析（用于方法部分）
- **anndata**：单细胞数据（用于方法部分）
- **biopython**：序列分析（用于背景部分）

### 可视化技能
- **matplotlib**：为综述生成图表和图
- **seaborn**：统计可视化

### 写作技能
- **brand-guidelines**：将机构品牌应用于PDF
- **internal-comms**：为不同受众调整综述

## 资源

### 捆绑资源

**脚本：**
- `scripts/verify_citations.py`：验证DOI并生成格式化引文
- `scripts/generate_pdf.py`：将markdown转换为专业PDF
- `scripts/search_databases.py`：处理、去重和格式化搜索结果

**参考资料：**
- `references/citation_styles.md`：详细的引文格式化指南（APA、Nature、Vancouver、Chicago、IEEE）
- `references/database_strategies.md`：全面的数据库搜索策略

**资产：**
- `assets/review_template.md`：包含所有部分的完整文献综述模板

### 外部资源

**指南：**
- PRISMA（系统综述）：http://www.prisma-statement.org/
- Cochrane手册：https://training.cochrane.org/handbook
- AMSTAR 2（综述质量）：https://amstar.ca/

**工具：**
- MeSH浏览器：https://meshb.nlm.nih.gov/search
- PubMed高级搜索：https://pubmed.ncbi.nlm.nih.gov/advanced/
- 布尔搜索指南：https://www.ncbi.nlm.nih.gov/books/NBK3827/

**引文格式：**
- APA样式：https://apastyle.apa.org/
- Nature组合：https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards
- NLM/Vancouver：https://www.nlm.nih.gov/bsd/uniform_requirements.html

## 依赖项

### 所需Python包
```bash
pip install requests  # 用于引文验证
```

### 所需系统工具
```bash
# 用于PDF生成
brew install pandoc  # macOS
apt-get install pandoc  # Linux

# 用于LaTeX（PDF生成）
brew install --cask mactex  # macOS
apt-get install texlive-xetex  # Linux
```

检查依赖项：
```bash
python scripts/generate_pdf.py --check-deps
```

## 总结

该literature-review技能提供：

1. **系统方法学**，遵循学术最佳实践
2. **多数据库集成**，通过现有科学技能
3. **引文验证**，确保准确性和可信度
4. **专业输出**，markdown和PDF格式
5. **全面指导**，涵盖整个综述过程
6. **质量保证**，具有验证和验证工具
7. **可重复性**，通过详细的文档要求

进行全面、严格的文献综述，满足学术标准，并提供任何领域当前知识的综合。
