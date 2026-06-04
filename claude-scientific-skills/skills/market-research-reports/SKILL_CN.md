---
name: market-research-reports
description: 以顶级咨询公司（麦肯锡、BCG、Gartner）的风格生成全面的市场研究报告（50+页）。具有专业的LaTeX格式、使用scientific-schematics和generate-image进行广泛的可视化生成、与research-lookup深度集成以收集数据，以及多框架战略分析，包括波特五力模型、PESTLE、SWOT、TAM/SAM/SOM和BCG矩阵。
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
  version: "1.0"
  skill-author: K-Dense Inc.
---





# 市场研究报告

## 概述

市场研究报告是用于分析行业、市场和竞争格局的综合战略文档，用于为商业决策、投资策略和战略规划提供信息。本技能可生成**专业的50页以上报告**，包含丰富的可视化内容，仿效麦肯锡、BCG、贝恩、Gartner和Forrester等顶级咨询公司的交付成果。

**主要特点：**
- **全面长度**：报告设计为50页以上，无token限制
- **视觉丰富内容**：开始时生成5-6个关键图表（写作过程中根据需要添加更多）
- **数据驱动分析**：深度集成research-lookup获取市场数据
- **多框架方法**：波特五力、PESTLE、SWOT、BCG矩阵、TAM/SAM/SOM
- **专业格式**：咨询公司质量的排版、色彩和布局
- **可操作的建议**：具有实施路线图的战略重点

**输出格式：** 带有专业样式的LaTeX，编译为PDF。使用`market_research.sty`样式包保持一致、专业的格式。

## 何时使用此技能

在以下情况下使用此技能：
- 为投资决策创建全面的市场分析
- 为战略规划开发行业报告
- 分析竞争格局和市场动态
- 进行市场规模估算练习（TAM/SAM/SOM）
- 评估市场进入机会
- 准备并购活动的尽职调查材料
- 为行业定位创建思想领导内容
- 开发进入市场战略文档
- 分析监管和政策对市场的影响
- 为新产品发布建立商业案例

## 视觉增强要求

**重要：市场研究报告应包含关键的可视化内容。**

每个报告应在开始时生成**6个基本可视化**，并在写作过程中根据需要添加额外的可视化。从最关键的可视化开始，建立报告框架。

### 可视化生成工具

**使用`scientific-schematics`生成：**
- 市场增长轨迹图表
- TAM/SAM/SOM分解图（同心圆）
- 波特五力图
- 竞争定位矩阵
- 市场细分图表
- 价值链图
- 技术路线图
- 风险热力图
- 战略优先级矩阵
- 实施时间表/甘特图
- SWOT分析图
- BCG增长-份额矩阵

```bash
# 示例：生成TAM/SAM/SOM图
python skills/scientific-schematics/scripts/generate_schematic.py \
  "TAM SAM SOM concentric circle diagram showing Total Addressable Market $50B outer circle, Serviceable Addressable Market $15B middle circle, Serviceable Obtainable Market $3B inner circle, with labels and arrows pointing to each segment" \
  -o figures/tam_sam_som.png --doc-type report

# 示例：生成波特五力
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Porter's Five Forces diagram with center box 'Competitive Rivalry' connected to four surrounding boxes: 'Threat of New Entrants' (top), 'Bargaining Power of Suppliers' (left), 'Bargaining Power of Buyers' (right), 'Threat of Substitutes' (bottom). Each box should show High/Medium/Low rating" \
  -o figures/porters_five_forces.png --doc-type report
```

**使用`generate-image`生成：**
- 执行摘要英雄信息图
- 行业/部门概念插图
- 抽象技术可视化
- 封面图片

```bash
# 示例：生成执行摘要信息图
python skills/generate-image/scripts/generate_image.py \
  "Professional executive summary infographic for market research report, showing key metrics in modern data visualization style, blue and green color scheme, clean minimalist design with icons representing market size, growth rate, and competitive landscape" \
  --output figures/executive_summary.png
```

### 按部分推荐的可视化（根据需要生成）

| 章节 | 优先可视化 | 可选可视化 |
|------|-----------|-----------|
| 执行摘要 | 执行摘要信息图（开始） | - |
| 市场规模与增长 | 增长轨迹（开始）、TAM/SAM/SOM（开始） | 区域细分、细分增长 |
| 竞争格局 | 波特五力（开始）、定位矩阵（开始） | 市场份额图、战略群体 |
| 风险分析 | 风险热力图（开始） | 缓解矩阵 |
| 战略建议 | 机会矩阵 | 优先级框架 |
| 实施路线图 | 时间表/甘特 | 里程碑追踪 |
| 投资论点 | 财务预测 | 情景分析 |

**从6个优先可视化开始**（上表标记为开始），然后在撰写特定章节需要可视化支持时生成额外的可视化。

---

## 报告结构（50+页）

### 封面（约5页）

#### 封面（1页）
- 报告标题和副标题
- 英雄可视化（生成）
- 日期和分类
- 编制对象/编制者

#### 目录（1-2页）
- 来自LaTeX的自动化
- 图表目录
- 表格目录

#### 执行摘要（2-3页）
- **市场概览框**：关键指标一览
- **投资论点**：3-5点摘要
- **关键发现**：主要发现和见解
- **战略建议**：前3-5个可操作建议
- **执行摘要信息图**：报告亮点的可视化综合

---

### 核心分析（约35页）

#### 第1章：市场概述与定义（4-5页）

**内容要求：**
- 市场定义和范围
- 行业生态系统映射
- 主要利益相关者及其角色
- 市场边界和相邻领域
- 历史背景和演变

**必需可视化（2）：**
1. 市场生态系统/价值链图
2. 行业结构图

**关键数据点：**
- 市场定义标准
- 包含/排除的细分
- 地理范围
- 分析时间范围

---

#### 第2章：市场规模与增长分析（6-8页）

**内容要求：**
- 总潜在市场（TAM）计算
- 可服务市场（SAM）定义
- 可服务可获得市场（SOM）估算
- 历史增长分析（5-10年）
- 增长预测（未来5-10年）
- 增长驱动因素和制约因素
- 区域市场细分
- 细分层面分析

**必需可视化（4）：**
1. 市场增长轨迹图（历史+预测）
2. TAM/SAM/SOM同心圆图
3. 区域市场细分（饼图或树图）
4. 细分增长比较（柱状图）

**关键数据点：**
- 当前市场规模（注明来源）
- 复合年增长率（历史和预测）
- 按区域划分的市场规模
- 按细分划分的市场规模
- 预测的关键假设

**数据来源：**
使用`research-lookup`查找：
- 市场研究报告（Gartner、Forrester、IDC等）
- 行业协会数据
- 政府统计数据
- 公司财务报告
- 学术研究

---

#### 第3章：行业驱动因素与趋势（5-6页）

**内容要求：**
- 宏观经济因素
- 技术趋势
- 监管驱动因素
- 社会和人口变化
- 环境因素
- 行业特定趋势

**分析框架：**
- **PESTLE分析**：政治、经济、社会、技术、法律、环境
- **趋势影响评估**：可能性与影响矩阵

**必需可视化（3）：**
1. 行业趋势时间表或雷达图
2. 驱动因素影响矩阵
3. PESTLE分析图

**关键数据点：**
- 前5-10个增长驱动因素及量化影响
- 新兴趋势及时间表
- 颠覆性因素

---

#### 第4章：竞争格局（6-8页）

**内容要求：**
- 市场结构分析
- 主要参与者简介
- 市场份额分析
- 竞争定位
- 进入壁垒
- 竞争动态

**分析框架：**
- **波特五力**：全面的行业分析
- **竞争定位矩阵**：关键维度的2x2矩阵
- **战略群体映射**：按策略聚类竞争对手

**必需可视化（4）：**
1. 波特五力图
2. 市场份额饼图或柱状图
3. 竞争定位矩阵（2x2）
4. 战略群体图

**关键数据点：**
- 各公司市场份额（前10名）
- 竞争强度评级
- 进入壁垒评估
- 供应商/买家议价能力评估

---

#### 第5章：客户分析与细分（4-5页）

**内容要求：**
- 客户细分定义
- 细分规模与增长
- 购买行为分析
- 客户需求和痛点
- 决策过程
- 各细分的价值驱动因素

**分析框架：**
- **客户细分矩阵**：规模与增长
- **价值主张画布**：工作、痛点、收益
- **客户旅程映射**：认知到倡导

**必需可视化（3）：**
1. 客户细分分解（饼图/树图）
2. 细分吸引力矩阵
3. 客户旅程或价值主张图

**关键数据点：**
- 细分规模和百分比
- 各细分增长率
- 平均交易规模/每客户收入
- 各细分客户获取成本

---

#### 第6章：技术与创新格局（4-5页）

**内容要求：**
- 当前技术栈
- 新兴技术
- 创新趋势
- 技术采用曲线
- 研发投资分析
- 专利格局

**分析框架：**
- **技术就绪评估**：TRL级别
- **炒作周期定位**：技术所在位置
- **技术路线图**：随时间的演变

**必需可视化（2）：**
1. 技术路线图图
2. 创新/采用曲线或炒作周期

**关键数据点：**
- 行业研发支出
- 关键技术里程碑
- 专利申请趋势
- 技术采用率

---

#### 第7章：监管与政策环境（3-4页）

**内容要求：**
- 当前监管框架
- 关键监管机构
- 合规要求
- 即将到来的监管变化
- 政策趋势
- 影响评估

**必需可视化（1）：**
1. 监管时间表或框架图

**关键数据点：**
- 关键法规及生效日期
- 合规成本
- 监管风险
- 政策变化可能性

---

#### 第8章：风险分析（3-4页）

**内容要求：**
- 市场风险
- 竞争风险
- 监管风险
- 技术风险
- 运营风险
- 财务风险
- 风险缓解策略

**分析框架：**
- **风险热力图**：可能性与影响
- **风险登记册**：综合风险清单
- **缓解矩阵**：风险与缓解策略

**必需可视化（2）：**
1. 风险热力图（可能性vs影响）
2. 风险缓解矩阵

**关键数据点：**
- 前10个风险及评级
- 风险可能性分数
- 影响严重性分数
- 缓解成本估算

---

### 战略建议（约10页）

#### 第9章：战略机会与建议（4-5页）

**内容要求：**
- 机会识别
- 机会规模
- 战略选项分析
- 优先级框架
- 详细建议
- 成功因素

**分析框架：**
- **机会吸引力矩阵**：吸引力与获胜能力
- **战略选项框架**：构建、购买、合作伙伴、忽略
- **优先级矩阵**：影响与努力

**必需可视化（3）：**
1. 机会矩阵
2. 战略选项框架
3. 优先级/建议矩阵

**关键数据点：**
- 机会规模
- 投资要求
- 预期回报
- 价值实现时间表

---

#### 第10章：实施路线图（3-4页）

**内容要求：**
- 分阶段实施计划
- 关键里程碑和交付物
- 资源要求
- 时间和排序
- 依赖关系和关键路径
- 治理结构

**必需可视化（2）：**
1. 实施时间表/甘特图
2. 里程碑追踪器或阶段图

**关键数据点：**
- 阶段持续时间
- 资源要求
- 关键里程碑及日期
- 各阶段预算分配

---

#### 第11章：投资论点与财务预测（3-4页）

**内容要求：**
- 投资摘要
- 财务预测
- 情景分析
- 回报预期
- 关键假设
- 敏感性分析

**必需可视化（2）：**
1. 财务预测图（收入、增长）
2. 情景分析比较

**关键数据点：**
- 收入预测（3-5年）
- 复合年增长率预测
- 投资回报率/内部收益率预期
- 关键财务假设

---

### 附录（约5页）

#### 附录A：方法论与数据来源（1-2页）
- 研究方法论
- 数据收集方法
- 数据来源和引用
- 局限性和假设

#### 附录B：详细市场数据表（2-3页）
- 综合市场数据表
- 区域细分
- 细分详情
- 历史数据系列

#### 附录C：公司简介（1-2页）
- 主要竞争对手简要简介
- 财务亮点
- 战略重点领域

#### 参考文献
- 所有引用的来源
- LaTeX的BibTeX格式

---

## 工作流程

### 第一阶段：研究与数据收集

**步骤1：定义范围**
- 明确市场定义
- 设定地理边界
- 确定时间范围
- 确定需要回答的关键问题

**步骤2：进行深入研究**

广泛使用`research-lookup`收集市场数据：

```bash
# 市场规模和增长数据
python skills/research-lookup/scripts/research_lookup.py \
  "What is the current market size and projected growth rate for [MARKET] industry? Include TAM, SAM, SOM estimates and CAGR projections"

# 竞争格局
python skills/research-lookup/scripts/research_lookup.py \
  "Who are the top 10 competitors in the [MARKET] market? What is their market share and competitive positioning?"

# 行业趋势
python skills/research-lookup/scripts/research_lookup.py \
  "What are the major trends and growth drivers in the [MARKET] industry for 2024-2030?"

# 监管环境
python skills/research-lookup/scripts/research_lookup.py \
  "What are the key regulations and policy changes affecting the [MARKET] industry?"
```

**步骤3：数据组织**
- 创建`sources/`文件夹存放研究笔记
- 按章节组织数据
- 识别数据缺口
- 根据需要进行后续研究

### 第二阶段：分析与框架应用

**步骤4：应用分析框架**

对每个框架进行结构化分析：

- **市场规模估算**：TAM → SAM → SOM，假设清晰
- **波特五力**：对每个力进行高/中/低评级并说明理由
- **PESTLE**：分析每个维度的趋势和影响
- **SWOT**：内部优势/劣势，外部机会/威胁
- **竞争定位**：定义轴，绘制竞争对手

**步骤5：形成见解**
- 将发现综合为关键见解
- 识别战略影响
- 制定建议
- 确定机会优先级

### 第三阶段：可视化生成

**步骤6：生成所有可视化**

在撰写报告之前生成可视化。使用批量生成脚本：

```bash
# 生成所有标准市场报告可视化
python skills/market-research-reports/scripts/generate_market_visuals.py \
  --topic "[MARKET NAME]" \
  --output-dir figures/
```

或单独生成：

```bash
# 1. 市场增长轨迹
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Bar chart showing market growth from 2020 to 2034, with historical bars in dark blue (2020-2024) and projected bars in light blue (2025-2034). Y-axis shows market size in billions USD. Include CAGR annotation" \
  -o figures/01_market_growth.png --doc-type report

# 2. TAM/SAM/SOM分解
python skills/scientific-schematics/scripts/generate_schematic.py \
  "TAM SAM SOM concentric circles diagram. Outer circle TAM Total Addressable Market, middle circle SAM Serviceable Addressable Market, inner circle SOM Serviceable Obtainable Market. Each labeled with acronym and description. Blue gradient" \
  -o figures/02_tam_sam_som.png --doc-type report

# 3. 波特五力
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Porter's Five Forces diagram with center box 'Competitive Rivalry' connected to four surrounding boxes: Threat of New Entrants (top), Bargaining Power of Suppliers (left), Bargaining Power of Buyers (right), Threat of Substitutes (bottom). Color code by rating: High=red, Medium=yellow, Low=green" \
  -o figures/03_porters_five_forces.png --doc-type report

# 4. 竞争定位矩阵
python skills/scientific-schematics/scripts/generate_schematic.py \
  "2x2 competitive positioning matrix with X-axis 'Market Focus (Niche to Broad)' and Y-axis 'Solution Approach (Product to Platform)'. Plot 8-10 competitors as labeled circles of varying sizes. Include quadrant labels" \
  -o figures/04_competitive_positioning.png --doc-type report

# 5. 风险热力图
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Risk heatmap matrix. X-axis Impact (Low to Critical), Y-axis Probability (Unlikely to Very Likely). Color gradient: Green (low risk) to Red (critical risk). Plot 10-12 risks as labeled points" \
  -o figures/05_risk_heatmap.png --doc-type report

# 6.（可选）执行摘要信息图
python skills/generate-image/scripts/generate_image.py \
  "Professional executive summary infographic for market research report, modern data visualization style, blue and green color scheme, clean minimalist design" \
  --output figures/06_exec_summary.png
```

### 第四阶段：报告撰写

**步骤7：初始化项目结构**

创建标准项目结构：

```
writing_outputs/YYYYMMDD_HHMMSS_market_report_[topic]/
├── progress.md
├── drafts/
│   └── v1_market_report.tex
├── references/
│   └── references.bib
├── figures/
│   └── [all generated visuals]
├── sources/
│   └── [research notes]
└── final/
```

**步骤8：使用模板撰写报告**

使用`market_report_template.tex`作为起点。按照结构指南撰写每个章节，确保：

- **全面覆盖**：每个小节都有涉及
- **数据驱动内容**：声明有研究支持
- **可视化集成**：引用所有生成的图表
- **专业语气**：咨询风格的写作
- **无token限制**：完整撰写，不要缩写

**写作指南：**
- 尽可能使用主动语态
- 以见解开头，用数据支持
- 建议使用编号列表
- 所有统计数据注明数据来源
- 章节之间过渡流畅

### 第五阶段：编译与审核

**步骤9：编译LaTeX**

```bash
cd writing_outputs/[project_folder]/drafts/
xelatex v1_market_report.tex
bibtex v1_market_report
xelatex v1_market_report.tex
xelatex v1_market_report.tex
```

**步骤10：质量审核**

验证报告是否符合质量标准：

- [ ] 总页数为50页以上
- [ ] 所有必要的可视化（5-6个核心+任何额外的）都已包含并正确渲染
- [ ] 执行摘要捕获了关键发现
- [ ] 所有数据点都有引用来源
- [ ] 分析框架正确应用
- [ ] 建议是可操作的且有优先级
- [ ] 没有孤立的图表或表格
- [ ] 目录、图表目录、表格目录准确
- [ ] 参考文献完整
- [ ] PDF渲染无错误

**步骤11：同行评审**

使用peer-review技能评估报告：
- 评估全面性
- 验证数据准确性
- 检查逻辑流程
- 评估建议质量

---

## 质量标准

### 页数目标

| 章节 | 最少页数 | 目标页数 |
|------|---------|---------|
| 封面 | 4 | 5 |
| 市场概述 | 4 | 5 |
| 市场规模与增长 | 5 | 7 |
| 行业驱动因素 | 4 | 6 |
| 竞争格局 | 5 | 7 |
| 客户分析 | 3 | 5 |
| 技术格局 | 3 | 5 |
| 监管环境 | 2 | 4 |
| 风险分析 | 2 | 4 |
| 战略建议 | 3 | 5 |
| 实施路线图 | 2 | 4 |
| 投资论点 | 2 | 4 |
| 附录 | 4 | 5 |
| **总计** | **43** | **66** |

### 视觉质量要求

- **分辨率**：所有图像至少 300 DPI
- **格式**：光栅图像使用 PNG，矢量图使用 PDF
- **无障碍**：使用色盲友好的调色板
- **一致性**：整个文档使用相同的配色方案
- **标注**：所有坐标轴、图例和数据点都有标注
- **来源引用**：图片来源在图例中注明

### 数据质量要求

- **来源可靠性**：使用权威来源（政府统计、行业协会、知名研究公司）
- **数据时效性**：使用最新可用数据（过去 12 个月内）
- **样本量透明**：报告样本量和抽样方法
- **方法论透明**：详细说明数据收集和分析方法
- **交叉验证**：通过多个来源验证关键数据点

## LaTeX 格式化

### 使用样式包

`market_research.sty` 包提供专业格式。在文档中包含它：

```latex
\documentclass[11pt,letterpaper]{report}
\usepackage{market_research}
```

### 盒子环境

使用彩色盒子突出显示关键内容：

```latex
% 关键洞察盒子（蓝色）
\begin{keyinsightbox}[关键发现]
市场预计以 15.3% 的复合年增长率增长至 2030 年。
\end{keyinsightbox}

% 市场数据盒子（绿色）
\begin{marketdatabox}[市场快照]
\begin{itemize}
    \item 市场规模（2024 年）：452 亿美元
    \item 预计规模（2030 年）：987 亿美元
    \item 复合年增长率：15.3%
\end{itemize}
\end{marketdatabox}
```

### 图表格式化

```latex
% 市场增长图表
\begin{figure}[htbp]
\centering
\begin{tikzpicture}
\begin{axis}[
    width=\textwidth,
    height=6cm,
    xlabel={年份},
    ylabel={市场规模（十亿美元）},
    legend pos=north west,
    grid=major
]
\addplot[blue,mark=*] coordinates {
    (2024, 45.2)
    (2025, 52.1)
    (2026, 60.0)
    (2027, 69.1)
    (2028, 79.6)
    (2029, 91.7)
    (2030, 98.7)
};
\legend{市场规模}
\end{axis}
\end{tikzpicture}
\caption{全球市场规模预测（2024-2030）}
\label{fig:market-size}
\end{figure}
```

### 表格格式化

```latex
% 竞争格局表格
\begin{table}[htbp]
\centering
\caption{主要竞争者市场份额}
\label{tab:market-share}
\begin{tabular}{lcc}
\toprule
公司 & 市场份额 & 年增长率 \\
\midrule
公司 A & 28.5\% & 12.3\% \\
公司 B & 22.1\% & 15.7\% \\
公司 C & 18.3\% & 9.8\% \\
其他 & 31.1\% & 8.2\% \\
\bottomrule
\end{tabular}
\end{table}
```

