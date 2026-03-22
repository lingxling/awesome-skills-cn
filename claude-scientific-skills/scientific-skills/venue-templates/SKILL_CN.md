---
name: venue-templates
description: 访问主要科学出版物（Nature、Science、PLOS、IEEE、ACM）、学术会议（NeurIPS、ICML、CVPR、CHI）、研究海报和资助提案（NSF、NIH、DOE、DARPA）的综合LaTeX模板、格式要求和提交指南。当准备期刊投稿、会议论文、研究海报或资助提案并需要特定场所的格式要求和模板时，应使用此技能。
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# 场所模板

## 概述

访问主要科学出版物、学术会议、研究海报和资助提案的综合LaTeX模板、格式要求和提交指南。此技能提供即用模板和详细规范，以支持跨学科的成功学术提交。

当准备期刊投稿、会议论文、研究海报或资助提案并需要特定场所的格式要求和模板时，使用此技能。

## 何时使用此技能

此技能应在以下情况使用：
- 准备提交给特定期刊（Nature、Science、PLOS、IEEE等）的 manuscript
- 撰写具有特定格式要求的会议论文（NeurIPS、ICML、CHI等）
- 为会议创建学术研究海报
- 为联邦机构（NSF、NIH、DOE、DARPA）或私人基金会起草资助提案
- 检查目标场所的格式要求和页面限制
- 使用作者信息和项目详情自定义模板
- 验证文档是否符合场所规范

## 使用科学示意图增强视觉效果

**使用此技能创建文档时，始终考虑添加科学图表和示意图以增强视觉沟通。**

如果您的文档尚未包含示意图或图表：
- 使用**scientific-schematics**技能生成AI驱动的出版质量图表
- 只需用自然语言描述您想要的图表
- Nano Banana Pro将自动生成、审查和完善示意图

**对于新文档：** 应默认生成科学示意图，以可视化表示文本中描述的关键概念、工作流程、架构或关系。

**如何生成示意图：**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

AI将自动：
- 创建具有适当格式的出版质量图像
- 通过多次迭代进行审查和完善
- 确保可访问性（色盲友好、高对比度）
- 将输出保存在figures/目录中

**何时添加示意图：**
- 论文的方法流程图
- 概念框架图
- 系统架构插图
- 数据流图
- 实验设计可视化
- 研究工作流程图
- 任何从可视化中受益的复杂概念

有关创建示意图的详细指导，请参阅scientific-schematics技能文档。

---

## 核心功能

### 1. 期刊文章模板

访问50+个主要科学期刊的LaTeX模板和格式指南，涵盖各个学科：

**Nature系列：**
- Nature、Nature Methods、Nature Biotechnology、Nature Machine Intelligence
- Nature Communications、Nature Protocols
- Scientific Reports

**Science系列：**
- Science、Science Advances、Science Translational Medicine
- Science Immunology、Science Robotics

**PLOS（科学公共图书馆）：**
- PLOS ONE、PLOS Biology、PLOS Computational Biology
- PLOS Medicine、PLOS Genetics

**Cell Press：**
- Cell、Neuron、Immunity、Cell Reports
- Molecular Cell、Developmental Cell

**IEEE出版物：**
- IEEE Transactions（各学科）
- IEEE Access、IEEE Journal模板

**ACM出版物：**
- ACM Transactions、Communications of the ACM
- ACM会议论文集

**其他主要出版商：**
- Springer期刊（各学科）
- Elsevier期刊（自定义模板）
- Wiley期刊
- BMC期刊
- Frontiers期刊

### 2. 会议论文模板

为主要学术会议提供具有适当格式的会议特定模板：

**机器学习与AI：**
- NeurIPS（神经信息处理系统）
- ICML（国际机器学习会议）
- ICLR（学习表示国际会议）
- CVPR（计算机视觉与模式识别）
- AAAI（人工智能促进协会）

**计算机科学：**
- ACM CHI（人机交互）
- SIGKDD（知识发现与数据挖掘）
- EMNLP（自然语言处理经验方法）
- SIGIR（信息检索）
- USENIX会议

**生物学与生物信息学：**
- ISMB（分子生物学智能系统）
- RECOMB（计算分子生物学研究）
- PSB（太平洋生物计算研讨会）

**工程学：**
- IEEE会议模板（各学科）
- ASME、AIAA会议

### 3. 研究海报模板

用于会议演示的学术海报模板：

**标准格式：**
- A0（841 × 1189 mm / 33.1 × 46.8 in）
- A1（594 × 841 mm / 23.4 × 33.1 in）
- 36" × 48"（914 × 1219 mm）- 常见美国尺寸
- 42" × 56"（1067 × 1422 mm）
- 48" × 36"（横向）

**模板包：**
- **beamerposter**：经典学术海报模板
- **tikzposter**：现代、彩色海报设计
- **baposter**：结构化多列布局

**设计特点：**
- 远距离可读性的最佳字体大小
- 配色方案（色盲安全调色板）
- 网格布局和列结构
- 补充材料的QR码集成

### 4. 资助提案模板

主要资助机构的模板和格式要求：

**NSF（国家科学基金会）：**
- 完整提案模板（15页项目描述）
- 项目摘要（1页：概述、知识价值、更广泛影响）
- 预算和预算说明
- 个人简介（3页限制）
- 设施、设备和其他资源
- 数据管理计划

**NIH（国立卫生研究院）：**
- R01研究资助（多年）
- R21探索/发展资助
- K奖（职业发展）
- 特定目标页（1页，最关键部分）
- 研究策略（意义、创新、方法）
- 个人简介（5页限制）

**DOE（能源部）：**
- 科学办公室提案
- ARPA-E模板
- 技术就绪水平（TRL）描述
- 商业化和影响部分

**DARPA（国防高级研究计划局）：**
- BAA（广泛机构公告）响应
- Heilmeier问答框架
- 技术方法和里程碑
- 过渡规划

**私人基金会：**
- 盖茨基金会
- Wellcome Trust
- 霍华德·休斯医学研究所（HHMI）
- 陈·扎克伯格计划（CZI）

## 工作流程：查找和使用模板

### 步骤1：确定目标场所

确定具体的出版物、会议或资助机构：

```
示例查询：
- "我需要提交到Nature"
- "NeurIPS 2025的要求是什么？"
- "显示NSF提案格式"
- "我正在为ISMB创建海报"
```

### 步骤2：查询模板和要求

访问特定场所的模板和格式指南：

**对于期刊：**
```bash
# 加载期刊格式要求
参考：references/journals_formatting.md
搜索："Nature"或特定期刊名称

# 检索模板
模板：assets/journals/nature_article.tex
```

**对于会议：**
```bash
# 加载会议格式
参考：references/conferences_formatting.md
搜索："NeurIPS"或特定会议

# 检索模板
模板：assets/journals/neurips_article.tex
```

**对于海报：**
```bash
# 加载海报指南
参考：references/posters_guidelines.md

# 检索模板
模板：assets/posters/beamerposter_academic.tex
```

**对于资助：**
```bash
# 加载资助要求
参考：references/grants_requirements.md
搜索："NSF"或特定机构

# 检索模板
模板：assets/grants/nsf_proposal_template.tex
```

### 步骤3：审查格式要求

在自定义前检查关键规范：

**需要验证的关键要求：**
- 页面限制（因场所而异）
- 字体大小和字体族
- 页边距规格
- 行间距
- 引用风格（APA、Vancouver、Nature等）
- 图表/表格要求
- 文件格式（PDF、Word、LaTeX源）
- 匿名化（双盲评审）
- 补充材料限制

### 步骤4：自定义模板

使用辅助脚本或手动自定义：

**选项1：辅助脚本（推荐）：**
```bash
python scripts/customize_template.py \
  --template assets/journals/nature_article.tex \
  --title "Your Paper Title" \
  --authors "First Author, Second Author" \
  --affiliations "University Name" \
  --output my_nature_paper.tex
```

**选项2：手动编辑：**
- 打开模板文件
- 替换占位文本（用注释标记）
- 填写标题、作者、 affiliations、摘要
- 向每个部分添加内容

### 步骤5：验证格式

检查是否符合场所要求：

```bash
python scripts/validate_format.py \
  --file my_paper.pdf \
  --venue "Nature" \
  --check-all
```

**验证检查：**
- 页数在限制范围内
- 字体大小正确
- 页边距符合规格
- 参考文献格式正确
- 图表满足分辨率要求

### 步骤6：编译和审查

编译LaTeX并审查输出：

```bash
# 编译LaTeX
pdflatex my_paper.tex
bibtex my_paper
pdflatex my_paper.tex
pdflatex my_paper.tex

# 或使用latexmk进行自动编译
latexmk -pdf my_paper.tex
```

审查清单：
- [ ] 所有部分存在且格式正确
- [ ] 引用正确呈现
- [ ] 图表带有适当的标题
- [ ] 页数在限制范围内
- [ ] 遵循作者指南
- [ ] 准备了补充材料（如需要）

## 与其他技能集成

此技能与其他科学技能无缝协作：

### 科学写作
- 使用**scientific-writing**技能获取内容指导（IMRaD结构、清晰度、精确性）
- 应用此技能的特定场所模板进行格式化
- 结合使用以完成完整的 manuscript 准备

### 文献综述
- 使用**literature-review**技能进行系统文献搜索和综合
- 应用场所要求的适当引用风格
- 根据模板规范格式化参考文献

### 同行评审
- 使用**peer-review**技能评估 manuscript 质量
- 使用此技能验证格式合规性
- 确保遵守报告指南（CONSORT、STROBE等）

### 研究资助
- 与**research-grants**技能交叉参考以获取内容策略
- 使用此技能获取机构特定的模板和格式
- 结合使用以完成全面的资助提案准备

### LaTeX海报
- 此技能提供与场所无关的海报模板
- 用于会议特定的海报要求
- 与可视化技能集成以创建图表

## 模板类别

### 按文档类型

| 类别 | 模板数量 | 常见场所 |
|----------|---------------|---------------|
| **期刊文章** | 30+ | Nature、Science、PLOS、IEEE、ACM、Cell Press |
| **会议论文** | 20+ | NeurIPS、ICML、CVPR、CHI、ISMB |
| **研究海报** | 10+ | A0、A1、36×48、各种包 |
| **资助提案** | 15+ | NSF、NIH、DOE、DARPA、基金会 |

### 按学科

| 学科 | 支持的场所 |
|------------|------------------|
| **生命科学** | Nature、Cell Press、PLOS、ISMB、RECOMB |
| **物理科学** | Science、Physical Review、ACS、APS |
| **工程学** | IEEE、ASME、AIAA、ACM |
| **计算机科学** | ACM、IEEE、NeurIPS、ICML、ICLR |
| **医学** | NEJM、Lancet、JAMA、BMJ |
| **跨学科** | PNAS、Nature Communications、Science Advances |

## 辅助脚本

### query_template.py

按场所名称、类型或关键词搜索和检索模板：

```bash
# 查找特定期刊的模板
python scripts/query_template.py --venue "Nature" --type "article"

# 按关键词搜索
python scripts/query_template.py --keyword "machine learning"

# 列出所有可用模板
python scripts/query_template.py --list-all

# 获取场所的要求
python scripts/query_template.py --venue "NeurIPS" --requirements
```

### customize_template.py

使用作者和项目信息自定义模板：

```bash
# 基本自定义
python scripts/customize_template.py \
  --template assets/journals/nature_article.tex \
  --output my_paper.tex

# 带作者信息
python scripts/customize_template.py \
  --template assets/journals/nature_article.tex \
  --title "Novel Approach to Protein Folding" \
  --authors "Jane Doe, John Smith, Alice Johnson" \
  --affiliations "MIT, Stanford, Harvard" \
  --email "[email protected]" \
  --output my_paper.tex

# 交互模式
python scripts/customize_template.py --interactive
```

### validate_format.py

检查文档是否符合场所要求：

```bash
# 验证编译的PDF
python scripts/validate_format.py \
  --file my_paper.pdf \
  --venue "Nature" \
  --check-all

# 检查特定方面
python scripts/validate_format.py \
  --file my_paper.pdf \
  --venue "NeurIPS" \
  --check page-count,margins,fonts

# 生成验证报告
python scripts/validate_format.py \
  --file my_paper.pdf \
  --venue "Science" \
  --report validation_report.txt
```

## 最佳实践

### 模板选择
1. **验证时效性**：检查模板日期并与最新作者指南比较
2. **检查官方来源**：许多期刊提供官方LaTeX类
3. **测试编译**：在添加内容前编译模板
4. **阅读注释**：模板包含有用的内联注释

### 自定义
1. **保留结构**：不要删除必需的部分或包
2. **遵循占位符**：系统地替换标记的占位文本
3. **保持格式**：不要覆盖特定场所的格式
4. **保存备份**：在自定义前保存原始模板

### 合规性
1. **检查页面限制**：在最终提交前验证
2. **验证引用**：使用场所的正确引用风格
3. **测试图表**：确保图表满足分辨率要求
4. **审查匿名化**：如有需要，删除识别信息

### 提交
1. **遵循说明**：阅读完整的作者指南
2. **包含所有文件**：LaTeX源、图表、参考文献
3. **正确生成**：使用推荐的编译方法
4. **检查输出**：验证PDF符合预期

## 常见格式要求

### 页面限制（典型）

| 场所类型 | 典型限制 | 说明 |
|------------|---------------|-------|
| **Nature文章** | 5页 | ~3000字，不包括参考文献 |
| **Science报告** | 5页 | 图表计入限制 |
| **PLOS ONE** | 无限制 | 长度不限 |
| **NeurIPS** | 8页 | + 无限参考文献/附录 |
| **ICML** | 8页 | + 无限参考文献/附录 |
| **NSF提案** | 15页 | 仅项目描述 |
| **NIH R01** | 12页 | 研究策略 |

### 各场所的引用风格

| 场所 | 引用风格 | 格式 |
|-------|---------------|--------|
| **Nature** | 编号（上标） | Nature风格 |
| **Science** | 编号（上标） | Science风格 |
| **PLOS** | 编号（括号） | Vancouver |
| **Cell Press** | 作者-年份 | Cell风格 |
| **ACM** | 编号 | ACM风格 |
| **IEEE** | 编号（括号） | IEEE风格 |
| **APA期刊** | 作者-年份 | APA 7th |

### 图表要求

| 场所 | 分辨率 | 格式 | 颜色 |
|-------|-----------|--------|-------|
| **Nature** | 300+ dpi | TIFF、EPS、PDF | RGB或CMYK |
| **Science** | 300+ dpi | TIFF、PDF | RGB |
| **PLOS** | 300-600 dpi | TIFF、EPS | RGB |
| **IEEE** | 300+ dpi | EPS、PDF | RGB或灰度 |

## 写作风格指南

除格式外，此技能还提供全面的**写作风格指南**，捕获不同场所在写作上的要求——不仅仅是外观。

### 为什么风格很重要

为Nature撰写的研究与为NeurIPS撰写的研究读起来会非常不同：
- **Nature/Science**：对非专业人士可访问，以故事为导向，广泛意义
- **Cell Press**：机制深度，全面数据，需要图形摘要
- **医学期刊**：以患者为中心，证据分级，结构化摘要
- **ML会议**：贡献要点，消融研究，可重复性重点
- **CS会议**：领域特定惯例，不同的评估标准

### 可用的风格指南

| 指南 | 涵盖 | 关键主题 |
|-------|--------|------------|
| `venue_writing_styles.md` | 总览 | 风格谱系，快速参考 |
| `nature_science_style.md` | Nature、Science、PNAS | 可访问性，讲故事，广泛影响 |
| `cell_press_style.md` | Cell、Neuron、Immunity | 图形摘要，eTOC，要点 |
| `medical_journal_styles.md` | NEJM、Lancet、JAMA、BMJ | 结构化摘要，证据语言 |
| `ml_conference_style.md` | NeurIPS、ICML、ICLR、CVPR | 贡献要点，消融研究 |
| `cs_conference_style.md` | ACL、EMNLP、CHI、SIGKDD | 领域特定惯例 |
| `reviewer_expectations.md` | 所有场所 | 审稿人关注什么，反驳技巧 |

### 写作示例

具体示例可在`assets/examples/`中找到：
- `nature_abstract_examples.md`：高影响力期刊的流畅段落摘要
- `neurips_introduction_example.md`：带贡献要点的ML会议介绍
- `cell_summary_example.md`：Cell Press摘要、要点、eTOC格式
- `medical_structured_abstract.md`：NEJM、Lancet、JAMA结构化格式

### 工作流程：适应场所

1. **确定目标场所**并加载适当的风格指南
2. **审查写作惯例**：语气、声音、摘要格式、结构
3. **查看示例**以获取特定部分的指导
4. **审查期望**：此场所的审稿人优先考虑什么？
5. **应用格式**：使用`assets/`中的LaTeX模板

---

## 资源

### 捆绑资源

**写作风格指南**（在`references/`中）：
- `venue_writing_styles.md`：风格总览和比较
- `nature_science_style.md`：Nature/Science写作惯例
- `cell_press_style.md`：Cell Press期刊风格
- `medical_journal_styles.md`：医学期刊写作指南
- `ml_conference_style.md`：ML会议写作惯例
- `cs_conference_style.md`：CS会议写作指南
- `reviewer_expectations.md`：各场所审稿人关注的内容

**格式要求**（在`references/`中）：
- `journals_formatting.md`：综合期刊格式要求
- `conferences_formatting.md`：会议论文规格
- `posters_guidelines.md`：研究海报设计和尺寸
- `grants_requirements.md`：按机构划分的资助提案要求

**写作示例**（在`assets/examples/`中）：
- `nature_abstract_examples.md`：高影响力期刊摘要示例
- `neurips_introduction_example.md`：ML会议介绍格式
- `cell_summary_example.md`：Cell Press摘要/要点/eTOC
- `medical_structured_abstract.md`：NEJM/Lancet/JAMA摘要格式

**模板**（在`assets/`中）：
- `journals/`：期刊文章LaTeX模板
- `posters/`：研究海报模板
- `grants/`：资助提案模板

**脚本**（在`scripts/`中）：
- `query_template.py`：搜索和检索模板
- `customize_template.py`：使用作者信息自定义
- `validate_format.py`：检查是否符合要求

### 外部资源

**期刊作者指南**：
- Nature：https://www.nature.com/nature/for-authors
- Science：https://www.science.org/content/page/instructions-authors
- PLOS：https://plos.org/resources/for-authors/
- Cell Press：https://www.cell.com/author-guidelines

**会议格式**：
- NeurIPS：https://neurips.cc/Conferences/2024/CallForPapers
- ICML：https://icml.cc/Conferences/2024/StyleAuthorInstructions
- CVPR：https://cvpr.thecvf.com/Conferences/2024/AuthorGuidelines

**资助资源**：
- NSF PAPPG：https://www.nsf.gov/publications/pub_summ.jsp?ods_key=pappg
- NIH Forms：https://grants.nih.gov/grants/how-to-apply-application-guide.html
- DOE Funding：https://science.osti.gov/grants

## 示例用法

### 示例1：Nature文章提交

```markdown
用户："我需要为Nature准备manuscript"

响应：
1. 加载Nature格式要求（references/journals_formatting.md）
2. 检索Nature模板（assets/journals/nature_article.tex）
3. 关键要求：
   - 长度：~3000字，~5页
   - 格式：单列，12pt字体
   - 引用：编号上标（Nature风格）
   - 图表：300+ dpi，RGB颜色
4. 用您的标题、作者、affiliations自定义模板
5. 编译并根据要求验证
```

### 示例2：NeurIPS会议论文

```markdown
用户："NeurIPS的格式要求是什么？"

响应：
来自references/conferences_formatting.md：
- 页面限制：8页正文 + 无限参考文献/附录
- 格式：双列，10pt字体
- 模板：neurips_2024.sty（官方样式文件）
- 匿名化：初始提交必需
- 引用：编号（括号）
- 图表：高分辨率，推荐色盲安全
```

### 示例3：NSF提案

```markdown
用户："帮助我格式化NSF提案"

响应：
NSF要求（来自references/grants_requirements.md）：
- 项目描述：最多15页
- 项目摘要：1页（概述、知识价值、更广泛影响）
- 预算说明：3-5页
- 个人简介：每位高级人员3页
- 字体：最小10pt，Times Roman或类似
- 页边距：所有边1英寸
模板：assets/grants/nsf_proposal_template.tex
```

### 示例4：会议海报

```markdown
用户："我需要为ISMB创建海报"

响应：
ISMB海报规格：
- 尺寸：通常A0纵向（33.1 × 46.8英寸）
- 推荐模板：beamerposter或tikzposter
- 字体大小：标题60-85pt，标题36-48pt，正文24-32pt
- 包括：论文/补充材料的QR码
可用模板：
- assets/posters/beamerposter_academic.tex
- assets/posters/tikzposter_research.tex
```

## 更新和维护

**模板时效性：**
- 模板每年更新或在场所发布新指南时更新
- 最后更新：2024
- 查看官方场所网站获取最新要求

**报告问题：**
- 模板编译错误
- 过时的格式要求
- 缺少场所模板
- 不正确的规格

## 总结

venue-templates技能提供全面访问：

1. **50+ 出版物场所模板** 跨学科
2. **详细的格式要求** 适用于期刊、会议、海报、资助
3. **辅助脚本** 用于模板发现、自定义和验证
4. **与其他科学写作技能的集成**
5. **成功学术提交的最佳实践**

当您需要特定场所的格式指导或学术出版模板时，请使用此技能。