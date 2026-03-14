---
name: research-lookup
description: 使用Parallel Chat API（主要）或Perplexity sonar-pro-search（学术论文搜索）查找当前研究信息。自动将查询路由到最佳后端。用于查找论文、收集研究数据和验证科学信息。
allowed-tools: Read Write Edit Bash
license: MIT license
compatibility: PARALLEL_API_KEY和OPENROUTER_API_KEY必需
metadata:
    skill-author: K-Dense Inc.
---

# 研究信息查找

## 概述

此技能提供具有**智能后端路由**的实时研究信息查找：

- **Parallel Chat API**（`core`模型）：所有一般研究查询的默认后端。通过位于`https://api.parallel.ai`的OpenAI兼容Chat API提供带内联引用的综合、多源研究报告。
- **Perplexity sonar-pro-search**（通过OpenRouter）：仅用于学术特定论文搜索，其中学术数据库访问至关重要。

该技能自动检测查询类型并路由到最佳后端。

## 何时使用此技能

当您需要以下内容时使用此技能：

- **当前研究信息**：最新研究、论文和发现
- **文献验证**：根据当前研究检查事实、统计数据或声明
- **背景研究**：为科学写作收集上下文和支持证据
- **引用来源**：找到相关的论文和研究进行引用
- **技术文档**：查找规范、协议或方法
- **市场/行业数据**：当前统计数据、趋势、竞争情报
- **最新发展**：新兴趋势、突破、公告

## 使用科学示意图进行视觉增强

**使用此技能创建文档时，始终考虑添加科学图表和示意图以增强视觉沟通。**

如果您的文档尚未包含示意图或图表：
- 使用**scientific-schematics**技能生成AI驱动的出版物质量图表
- 只需用自然语言描述您想要的图表

```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

---

## 自动后端选择

该技能根据内容自动将查询路由到最佳后端：

### 路由逻辑

```
查询到达
    |
    +-- 包含学术关键词？（论文、DOI、期刊、同行评审等）
    |       是 --> Perplexity sonar-pro-search（学术搜索模式）
    |
    +-- 其他所有内容（一般研究、市场数据、技术信息、分析）
            --> Parallel Chat API（核心模型）
```

### 学术关键词（路由到Perplexity）

包含这些术语的查询被路由到Perplexity进行学术导向搜索：

- 论文查找：`find papers`、`find articles`、`research papers on`、`published studies`
- 引用：`cite`、`citation`、`doi`、`pubmed`、`pmid`
- 学术来源：`peer-reviewed`、`journal article`、`scholarly`、`arxiv`、`preprint`
- 综述类型：`systematic review`、`meta-analysis`、`literature search`
- 论文质量：`foundational papers`、`seminal papers`、`landmark papers`、`highly cited`

### 其他所有内容（路由到Parallel）

所有其他查询都进入Parallel Chat API（核心模型），包括：

- 一般研究问题
- 市场和行业分析
- 技术信息和文档
- 当前事件和最新发展
- 比较分析
- 统计数据检索
- 复杂分析查询

### 手动覆盖

您可以强制使用特定后端：

```bash
# 强制使用Parallel深度研究
python research_lookup.py "your query" --force-backend parallel

# 强制使用Perplexity学术搜索
python research_lookup.py "your query" --force-backend perplexity
```

---

## 核心功能

### 1. 一般研究查询（Parallel Chat API）

**默认后端。**通过Chat API（`core`模型）提供带引用的综合、多源研究。

```
查询示例：
- "CRISPR基因编辑2025年的最新进展"
- "比较mRNA疫苗与传统疫苗在癌症治疗中的应用"
- "医疗保健行业AI采用统计数据"
- "全球可再生能源市场趋势和预测"
- "解释肠道微生物组与抑郁症的潜在机制"
```

**响应包括：**
- Markdown格式的综合研究报告
- 来自权威网络来源的内联引用
- 带有关键发现的结构化部分
- 多个视角和数据点
- 用于验证的来源URL

### 2. 学术论文搜索（Perplexity sonar-pro-search）

**用于学术特定查询。**优先考虑学术数据库和同行评审来源。

```
查询示例：
- "Find papers on transformer attention mechanisms in NeurIPS 2024"
- "量子错误校正的基础论文"
- "非小细胞肺癌免疫疗法的系统综述"
- "引用原始BERT论文及其最具影响力的后续研究"
- "CRISPR在临床试验中的脱靶效应的已发表研究"
```

**响应包括：**
- 学术文献关键发现的摘要
- 5-8个高质量引用，包含作者、标题、期刊、年份、DOI
- 引用次数和发表场所级别指标
- 关键统计数据和方法亮点
- 研究差距和未来方向

### 3. 技术和方法信息

```
查询示例：
- "蛋白质检测的Western blot协议"
- "临床试验的统计功效分析"
- "机器学习模型评估指标比较"
```

### 4. 统计和市场数据

```
查询示例：
- "2025年美国人口糖尿病患病率"
- "全球AI市场规模和增长预测"
- "各国COVID-19疫苗接种率"
```

---

## 论文质量和流行度优先级

**关键**：搜索论文时，始终优先考虑高质量、有影响力的论文。

### 基于引用的排名

| 论文年龄 | 引用阈值 | 分类 |
|---------|----------|------|
| 0-3年 | 20+引用 | 值得注意 |
| 0-3年 | 100+引用 | 高度有影响力 |
| 3-7年 | 100+引用 | 重要 |
| 3-7年 | 500+引用 | 里程碑论文 |
| 7+年 | 500+引用 | 开创性工作 |
| 7+年 | 1000+引用 | 基础性 |

### 发表场所质量等级

**一级 - 顶级场所**（始终优先）：
- **一般科学**：Nature、Science、Cell、PNAS
- **医学**：NEJM、Lancet、JAMA、BMJ
- **领域特定**：Nature Medicine、Nature Biotechnology、Nature Methods
- **顶级CS/AI**：NeurIPS、ICML、ICLR、ACL、CVPR

**二级 - 高影响力专业**（强烈偏好）：
- 影响因子>10的期刊
- 子领域顶级会议（EMNLP、NAACL、ECCV、MICCAI）

**三级 - 受尊重的专业**（相关时包括）：
- 影响因子5-10的期刊

---

## 技术集成

### 环境变量

```bash
# 主要后端（Parallel Chat API）- 必需
export PARALLEL_API_KEY="your_parallel_api_key"

# 学术搜索后端（Perplexity）- 学术查询必需
export OPENROUTER_API_KEY="your_openrouter_api_key"
```

### API规格

**Parallel Chat API：**
- 端点：`https://api.parallel.ai`（兼容OpenAI SDK）
- 模型：`core`（60秒-5分钟延迟，复杂多源合成）
- 输出：带内联引用的Markdown文本
- 引用：带有URL、推理和置信度级别的研究基础
- 速率限制：300请求/分钟
- Python包：`openai`

**Perplexity sonar-pro-search：**
- 模型：`perplexity/sonar-pro-search`（通过OpenRouter）
- 搜索模式：学术（优先考虑同行评审来源）
- 搜索上下文：高（综合研究）
- 响应时间：5-15秒

### 命令行使用

```bash
# 自动路由研究（推荐）— 始终保存到sources/
python research_lookup.py "your query" -o sources/research_YYYYMMDD_HHMMSS_<topic>.md

# 强制使用特定后端 — 始终保存到sources/
python research_lookup.py "your query" --force-backend parallel -o sources/research_<topic>.md
python research_lookup.py "your query" --force-backend perplexity -o sources/papers_<topic>.md

# JSON输出 — 始终保存到sources/
python research_lookup.py "your query" --json -o sources/research_<topic>.json

# 批量查询 — 始终保存到sources/
python research_lookup.py --batch "query 1" "query 2" "query 3" -o sources/batch_research_<topic>.md
```

---

## 强制要求：将所有结果保存到Sources文件夹

**每个research-lookup结果必须保存到项目的`sources/`文件夹。**

这是不可协商的。研究结果获取成本高且对可重现性至关重要。

### 保存规则

| 后端 | `-o`标志目标 | 文件名模式 |
|------|------------|------------|
| Parallel深度研究 | `sources/research_<topic>.md` | `research_YYYYMMDD_HHMMSS_<brief_topic>.md` |
| Perplexity（学术） | `sources/papers_<topic>.md` | `papers_YYYYMMDD_HHMMSS_<brief_topic>.md` |
| 批量查询 | `sources/batch_<topic>.md` | `batch_research_YYYYMMDD_HHMMSS_<brief_topic>.md` |

### 如何保存

**关键：每个对`research_lookup.py`的调用必须包含指向`sources/`文件夹的`-o`标志。**

**关键：保存的文件必须保留所有引用、来源URL和DOI。**默认文本输出自动包含一个`Sources`部分（每个来源的标题、日期、URL）和一个`Additional References`部分（从响应文本中提取的DOI和学术URL）。要获取最大引用元数据，请使用`--json`。

```bash
# 一般研究 — 保存到sources/（包含Sources + Additional References部分）
python research_lookup.py "CRISPR基因编辑2025年的最新进展" \
  -o sources/research_20250217_143000_crispr_advances.md

# 学术论文搜索 — 保存到sources/（包含带DOI的论文引用）
python research_lookup.py "Find papers on transformer attention mechanisms in NeurIPS 2024" \
  -o sources/papers_20250217_143500_transformer_attention.md

# JSON格式获取最大引用元数据（带有URL、DOI、片段的完整引用对象）
python research_lookup.py "CRISPR临床试验" --json \
  -o sources/research_20250217_143000_crispr_trials.json

# 强制后端 — 保存到sources/
python research_lookup.py "AI监管格局" --force-backend parallel \
  -o sources/research_20250217_144000_ai_regulation.md

# 批量查询 — 保存到sources/
python research_lookup.py --batch "mRNA疫苗 efficacy" "mRNA疫苗 safety" \
  -o sources/batch_research_20250217_144500_mrna_vaccines.md
```

### 保存文件中的引用保留

每种输出格式保留引用的方式不同：

| 格式 | 包含的引用 | 何时使用 |
|------|-----------|----------|
| 文本（默认） | `Sources (N):`部分，包含`[title] (date) + URL` + `Additional References (N):`，包含DOI和学术URL | 标准使用 — 人类可读，包含所有引用 |
| JSON (`--json`) | 完整引用对象：`url`、`title`、`date`、`snippet`、`doi`、`type` | 当您需要最大引用元数据时 |

**对于Parallel后端**，保存的文件包括：研究报告 + 来源列表（标题、URL） + 附加参考文献（DOI、学术URL）。
**对于Perplexity后端**，保存的文件包括：学术摘要 + 来源列表（标题、日期、URL、片段） + 附加参考文献（DOI、学术URL）。

**当您需要以下内容时使用`--json`：**
- 以编程方式解析引用元数据
- 保留完整的DOI和URL数据以生成BibTeX
- 维护结构化引用对象用于交叉引用

### 为什么保存所有内容

1. **可重现性**：每个引用和声明都可以追溯到其原始研究来源
2. **上下文窗口恢复**：如果上下文被压缩，保存的结果可以重新读取而无需重新查询
3. **审计跟踪**：`sources/`文件夹记录了所有研究信息的收集方式
4. **跨部分重用**：多个部分可以引用相同的保存研究而无需重复查询
5. **成本效率**：在进行新API调用前检查`sources/`中是否有现有结果
6. **同行评审支持**：评审者可以验证每个引用背后的研究

### 进行新查询前，先检查Sources

调用`research_lookup.py`之前，检查是否已存在相关结果：

```bash
ls sources/  # 检查现有的保存结果
```

如果之前的查找涵盖了相同主题，重新阅读保存的文件而不是进行新的API调用。

### 日志记录

保存研究结果时，始终记录：

```
[HH:MM:SS] SAVED: Research lookup to sources/research_20250217_143000_crispr_advances.md (3,800 words, 8 citations)
[HH:MM:SS] SAVED: Paper search to sources/papers_20250217_143500_transformer_attention.md (6 papers found)
```

---

## 与科学写作的集成

此技能通过提供以下内容增强科学写作：

1. **文献综述支持**：为引言和讨论收集当前研究 — **保存到`sources/`**
2. **方法验证**：根据当前标准验证协议 — **保存到`sources/`**
3. **结果情境化**：将发现与最近的类似研究进行比较 — **保存到`sources/`**
4. **讨论增强**：用最新证据支持论点 — **保存到`sources/`**
5. **引用管理**：提供格式正确的引用 — **保存到`sources/`**

## 互补工具

| 任务 | 工具 |
|------|------|
| 一般网络搜索 | `parallel-web`技能（`parallel_web.py search`） |
| 引用验证 | `parallel-web`技能（`parallel_web.py extract`） |
| 深度研究（任何主题） | `research-lookup`或`parallel-web`技能 |
| 学术论文搜索 | `research-lookup`（自动路由到Perplexity） |
| Google Scholar搜索 | `citation-management`技能 |
| PubMed搜索 | `citation-management`技能 |
| DOI转BibTeX | `citation-management`技能 |
| 元数据验证 | `parallel-web`技能（`parallel_web.py search`或`extract`） |

---

## 错误处理和限制

**已知限制：**
- Parallel Chat API（核心模型）：复杂查询可能需要长达5分钟
- Perplexity：信息截止，可能无法访问付费墙后的全文
- 两者：无法访问专有或受限数据库

**回退行为：**
- 如果所选后端的API密钥缺失，尝试另一个后端
- 如果两个后端都失败，返回结构化错误响应
- 如果初始响应不足，重新措辞查询以获得更好的结果

---

## 使用示例

### 示例1：一般研究（路由到Parallel）

**查询**："transformer注意力机制2025年的最新进展"

**后端**：Parallel Chat API（核心模型）

**响应**：综合Markdown报告，包含来自权威来源的引用，涵盖最近论文、关键创新和性能基准。

### 示例2：学术论文搜索（路由到Perplexity）

**查询**："Find papers on CRISPR off-target effects in clinical trials"

**后端**：Perplexity sonar-pro-search（学术模式）

**响应**：5-8篇高影响力论文的精选列表，包含完整引用、DOI、引用次数和发表场所级别指标。

### 示例3：比较分析（路由到Parallel）

**查询**："比较mRNA疫苗与传统疫苗在癌症治疗中的应用"

**后端**：Parallel Chat API（核心模型）

**响应**：详细的比较报告，包含来自多个来源的数据、结构化分析和引用证据。

### 示例4：市场数据（路由到Parallel）

**查询**："2025年全球医疗保健AI采用统计数据"

**后端**：Parallel Chat API（核心模型）

**响应**：当前市场数据、采用率、增长预测和带有来源引用的区域分析。

---

## 摘要

此技能作为具有智能双后端路由的主要研究界面：

- **Parallel Chat API**（默认，`core`模型）：任何主题的综合、多源研究
- **Perplexity sonar-pro-search**：仅用于学术特定论文搜索
- **自动路由**：检测学术查询并适当路由
- **手动覆盖**：必要时强制使用任何后端
- **互补**：与`parallel-web`技能一起用于网络搜索和URL提取