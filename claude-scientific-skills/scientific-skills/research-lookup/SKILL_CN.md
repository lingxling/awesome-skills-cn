---
name: research-lookup
description: 使用parallel-cli搜索（主要，快速网络搜索）、Parallel Chat API（深度研究）或Perplexity sonar-pro-search（学术论文搜索）查找当前研究信息。自动将查询路由到最佳后端。用于查找论文、收集研究数据和验证科学信息。
allowed-tools: Read Write Edit Bash
license: MIT license
compatibility: parallel-cli必需（主要）；PARALLEL_API_KEY和OPENROUTER_API_KEY可选，用于深度/学术后端
metadata:
    skill-author: K-Dense Inc.
---

# 研究信息查找

## 概述

此技能提供具有**智能后端路由**的实时研究信息查找：

- **parallel-cli搜索**（parallel-web技能）：**所有研究查询的主要和默认后端**。快速、经济的网络搜索，优先考虑学术来源。使用`parallel-cli search`并配合`--include-domains`来获取学术来源。
- **Parallel Chat API**（`core`模型）：用于需要扩展合成的复杂、多源深度研究的次要后端（60秒-5分钟延迟）。仅在明确需要时使用。
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
    +-- 需要深度多源合成？（用户说"深度研究"、"全面研究"）
    |       是 --> Parallel Chat API（核心模型，60秒-5分钟）
    |
    +-- 其他所有内容（一般研究、市场数据、技术信息、分析）
            --> parallel-cli搜索（快速，默认）
```

### 默认：parallel-cli搜索（parallel-web技能）

**所有标准研究查询的主要后端。**快速、经济，支持学术来源优先。

对于科学/技术查询，运行两次搜索以确保学术覆盖：

```bash
# 1. 学术导向搜索
parallel-cli search "your research query" -q "keyword1" -q "keyword2" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  --include-domains "scholar.google.com,arxiv.org,pubmed.ncbi.nlm.nih.gov,semanticscholar.org,biorxiv.org,medrxiv.org,ncbi.nlm.nih.gov,nature.com,science.org,ieee.org,acm.org,springer.com,wiley.com,cell.com,pnas.org,nih.gov" \
  -o sources/research_<topic>-academic.json

# 2. 一般搜索（捕获非学术来源）
parallel-cli search "your research query" -q "keyword1" -q "keyword2" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  -o sources/research_<topic>-general.json
```

选项：
- `--after-date YYYY-MM-DD` 用于时间敏感的查询
- `--include-domains domain1.com,domain2.com` 限制特定来源

合并结果，以学术来源领先。对于非科学查询，单个一般搜索就足够了。

所有其他查询默然路由到这里，包括：

- 一般研究问题
- 市场和行业分析
- 技术信息和文档
- 当前事件和最新发展
- 比较分析
- 统计数据检索
- 事实核查和验证

### 学术关键词（路由到Perplexity）

包含这些术语的查询被路由到Perplexity进行学术导向搜索：

- 论文查找：`find papers`、`find articles`、`research papers on`、`published studies`
- 引用：`cite`、`citation`、`doi`、`pubmed`、`pmid`
- 学术来源：`peer-reviewed`、`journal article`、`scholarly`、`arxiv`、`preprint`
- 综述类型：`systematic review`、`meta-analysis`、`literature search`
- 论文质量：`foundational papers`、`seminal papers`、`landmark papers`、`highly cited`

### 深度研究（路由到Parallel Chat API）

仅在用户明确请求深度、全面或综合研究时使用。比parallel-cli搜索慢得多且成本更高。

### 手动覆盖

您可以强制使用特定后端：

```bash
# 强制使用parallel-cli搜索（快速网络搜索）
parallel-cli search "your query" -q "keyword" --json --max-results 10 -o sources/research_<topic>.json

# 强制使用Parallel深度研究（慢，全面）
python research_lookup.py "your query" --force-backend parallel

# 强制使用Perplexity学术搜索
python research_lookup.py "your query" --force-backend perplexity
```

---

## 核心功能

### 1. 一般研究查询（parallel-cli搜索 — 默认）

**主要后端。**通过parallel-web技能进行快速、经济的网络搜索，优先考虑学术来源。

```
查询示例：
- "Recent advances in CRISPR gene editing 2025"
- "Compare mRNA vaccines vs traditional vaccines for cancer treatment"
- "AI adoption in healthcare industry statistics"
- "Global renewable energy market trends and projections"
- "Explain the mechanism underlying gut microbiome and depression"
```

```bash
# 示例：CRISPR进展研究
parallel-cli search "Recent advances in CRISPR gene editing 2025" \
  -q "CRISPR" -q "gene editing" -q "2025" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  --include-domains "scholar.google.com,arxiv.org,pubmed.ncbi.nlm.nih.gov,nature.com,science.org,cell.com,pnas.org,nih.gov" \
  -o sources/research_crispr_advances-academic.json

parallel-cli search "Recent advances in CRISPR gene editing 2025" \
  -q "CRISPR" -q "gene editing" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  -o sources/research_crispr_advances-general.json
```

**响应包括：**
- 来自搜索结果的内联引用的综合发现
- 优先考虑学术来源（同行评审、预印本）
- 具体事实、数字和日期
- 按类型分组的来源部分，列出所有引用的URL

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

### 3. 深度研究（Parallel Chat API — 仅按需）

**仅在用户明确请求深度/全面研究时使用。** 通过Chat API（`core`模型）提供综合、多源合成。60秒-5分钟延迟。

```
查询示例：
- "Deep research on the current state of quantum computing error correction"
- "Exhaustive analysis of mRNA vaccine platforms for cancer immunotherapy"
```

### 4. 技术和方法信息

使用parallel-cli搜索（默认）进行快速查询：

```bash
parallel-cli search "Western blot protocol for protein detection" \
  -q "western blot" -q "protocol" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  -o sources/research_western_blot.json
```

### 5. 统计和市场数据

使用parallel-cli搜索（默认）获取当前数据：

```bash
parallel-cli search "Global AI market size and growth projections 2025" \
  -q "AI market" -q "statistics" -q "growth" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  --after-date 2024-01-01 \
  -o sources/research_ai_market.json
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

### 前置条件

```bash
# 主要后端（parallel-cli）- 必需
# 如果尚未安装parallel-cli，请安装：
curl -fsSL https://parallel.ai/install.sh | bash
# 或：uv tool install "parallel-web-tools[cli]"

# 身份验证：
parallel-cli auth
# 或：export PARALLEL_API_KEY="your_parallel_api_key"
```

### 环境变量

```bash
# 主要后端（parallel-cli搜索）- 必需
export PARALLEL_API_KEY="your_parallel_api_key"

# 深度研究后端（Parallel Chat API）- 可选，仅用于深度研究
# 使用相同的PARALLEL_API_KEY

# 学术搜索后端（Perplexity）- 可选，仅用于学术论文查询
export OPENROUTER_API_KEY="your_openrouter_api_key"
```

### API规格

**parallel-cli搜索（主要）：**
- 命令：`parallel-cli search`，输出JSON格式
- 延迟：2-10秒（快速）
- 输出：包含title、URL、publish_date、excerpts的JSON
- 学术域名：使用`--include-domains`获取学术来源
- 保存结果：`-o filename.json`用于后续处理和可重现性

**Parallel Chat API（仅深度研究）：**
- 端点：`https://api.parallel.ai`（兼容OpenAI SDK）
- 模型：`core`（60秒-5分钟延迟，复杂多源合成）
- 输出：带内联引用的Markdown文本
- 引用：带有URL、推理和置信度级别的研究基础
- 速率限制：300请求/分钟
- Python包：`openai`

**Perplexity sonar-pro-search（仅学术）：**
- 模型：`perplexity/sonar-pro-search`（通过OpenRouter）
- 搜索模式：学术（优先考虑同行评审来源）
- 搜索上下文：高（综合研究）
- 响应时间：5-15秒

### 命令行使用

```bash
# 通过parallel-cli进行快速网络搜索（默认 — 推荐）— 始终保存到sources/
parallel-cli search "your query" -q "keyword1" -q "keyword2" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  -o sources/research_<topic>.json

# 通过parallel-cli进行学术导向搜索 — 始终保存到sources/
parallel-cli search "your query" -q "keyword1" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  --include-domains "scholar.google.com,arxiv.org,pubmed.ncbi.nlm.nih.gov,semanticscholar.org,biorxiv.org,medrxiv.org,nature.com,science.org,cell.com,pnas.org,nih.gov" \
  -o sources/research_<topic>-academic.json

# 通过parallel-cli进行时间敏感搜索
parallel-cli search "your query" -q "keyword" \
  --json --max-results 10 --after-date 2024-01-01 \
  -o sources/research_<topic>.json

# 从特定URL提取完整内容（使用parallel-web extract）
parallel-cli extract "https://example.com/paper" --json

# 强制使用Parallel深度研究（慢，全面）— 通过research_lookup.py
python research_lookup.py "your query" --force-backend parallel -o sources/research_<topic>.md

# 强制使用Perplexity学术搜索 — 通过research_lookup.py
python research_lookup.py "your query" --force-backend perplexity -o sources/papers_<topic>.md

# 通过research_lookup.py自动路由（传统方式）— 始终保存到sources/
python research_lookup.py "your query" -o sources/research_YYYYMMDD_HHMMSS_<topic>.md

# 批量查询 — 通过research_lookup.py — 始终保存到sources/
python research_lookup.py --batch "query 1" "query 2" "query 3" -o sources/batch_research_<topic>.md
```

---

## 强制要求：将所有结果保存到Sources文件夹

**每个research-lookup结果必须保存到项目的`sources/`文件夹。**

这是不可协商的。研究结果获取成本高且对可重现性至关重要。

### 保存规则

| 后端 | `-o`标志目标 | 文件名模式 |
|------|------------|------------|
| parallel-cli搜索（默认） | `sources/research_<topic>.json` | `research_<brief_topic>.json` 或 `research_<brief_topic>-academic.json` |
| Parallel深度研究 | `sources/research_<topic>.md` | `research_YYYYMMDD_HHMMSS_<brief_topic>.md` |
| Perplexity（学术） | `sources/papers_<topic>.md` | `papers_YYYYMMDD_HHMMSS_<brief_topic>.md` |
| 批量查询 | `sources/batch_<topic>.md` | `batch_research_YYYYMMDD_HHMMSS_<brief_topic>.md` |

### 如何保存

**关键：每个搜索必须使用`-o`标志将结果保存到`sources/`文件夹。**

**关键：保存的文件必须保留所有引用、来源URL和DOI。**

```bash
# parallel-cli搜索（默认）— 将JSON保存到sources/
parallel-cli search "Recent advances in CRISPR gene editing 2025" \
  -q "CRISPR" -q "gene editing" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  --include-domains "scholar.google.com,arxiv.org,pubmed.ncbi.nlm.nih.gov,nature.com,science.org,cell.com,pnas.org,nih.gov" \
  -o sources/research_crispr_advances-academic.json

parallel-cli search "Recent advances in CRISPR gene editing 2025" \
  -q "CRISPR" -q "gene editing" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  -o sources/research_crispr_advances-general.json

# 通过Perplexity进行学术论文搜索 — 保存到sources/
python research_lookup.py "Find papers on transformer attention mechanisms in NeurIPS 2024" \
  -o sources/papers_20250217_143500_transformer_attention.md

# 通过Parallel Chat API进行深度研究 — 保存到sources/
python research_lookup.py "AI regulation landscape" --force-backend parallel \
  -o sources/research_20250217_144000_ai_regulation.md

# 批量查询 — 保存到sources/
python research_lookup.py --batch "mRNA vaccines efficacy" "mRNA vaccines safety" \
  -o sources/batch_research_20250217_144500_mrna_vaccines.md
```

### 保存文件中的引用保留

每种输出格式保留引用的方式不同：

| 格式 | 包含的引用 | 何时使用 |
|------|-----------|----------|
| parallel-cli JSON（默认） | 完整结果对象：title、url、publish_date、excerpts | 标准使用 — 结构化、可解析、快速 |
| 文本（research_lookup.py） | `Sources (N):`部分，包含`[title] (date) + URL` + `Additional References (N):`，包含DOI和学术URL | 深度研究/Perplexity — 人类可读 |
| JSON (`--json` via research_lookup.py) | 完整引用对象：url、title、date、snippet、doi、type | 当您需要深度研究的最大引用元数据时 |

**对于parallel-cli搜索**，保存的JSON文件包括：完整搜索结果，包含每个结果的标题、URL、发布日期和内容摘录。
**对于Parallel Chat API后端**，保存的文件包括：研究报告 + 来源列表（标题、URL） + 附加参考文献（DOI、学术URL）。
**对于Perplexity后端**，保存的文件包括：学术摘要 + 来源列表（标题、日期、URL、摘录） + 附加参考文献（DOI、学术URL）。

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
| 一般网络搜索（快速） | `parallel-cli search`（内置于此技能） |
| 学术导向网络搜索 | `parallel-cli search --include-domains`（内置于此技能） |
| URL内容提取 | `parallel-cli extract`（parallel-web技能） |
| 深度研究（全面） | 通过Parallel Chat API的`research-lookup`或`parallel-web`深度研究 |
| 学术论文搜索 | `research-lookup`（自动路由到Perplexity） |
| Google Scholar搜索 | `citation-management`技能 |
| PubMed搜索 | `citation-management`技能 |
| DOI转BibTeX | `citation-management`技能 |
| 元数据验证 | `parallel-cli extract`（parallel-web技能） |

---

## 错误处理和限制

**已知限制：**
- parallel-cli搜索：需要安装并认证parallel-cli
- Parallel Chat API（核心模型）：复杂查询可能需要长达5分钟
- Perplexity：信息截止，可能无法访问付费墙后的全文
- 所有后端：无法访问专有或受限数据库

**回退行为：**
- 如果未找到`parallel-cli`，使用`curl -fsSL https://parallel.ai/install.sh | bash`或`uv tool install "parallel-web-tools[cli]"`安装
- 如果parallel-cli搜索返回结果不足，回退到Perplexity或Parallel Chat API
- 如果所选后端的API密钥缺失，尝试另一个后端
- 如果所有后端都失败，返回结构化错误响应
- 如果初始响应不足，重新措辞查询以获得更好的结果

---

## 使用示例

### 示例1：一般研究（路由到parallel-cli搜索）

**查询**："transformer注意力机制2025年的最新进展"

**后端**：parallel-cli搜索（通过parallel-web技能）

**响应**：综合搜索结果，包含来自学术来源的引用，涵盖最近论文、关键创新和性能基准。

### 示例2：学术论文搜索（路由到Perplexity）

**查询**："Find papers on CRISPR off-target effects in clinical trials"

**后端**：Perplexity sonar-pro-search（学术模式）

**响应**：5-8篇高影响力论文的精选列表，包含完整引用、DOI、引用次数和发表场所级别指标。

### 示例3：深度研究（路由到Parallel Chat API）

**查询**："Deep research on the current state of quantum computing error correction"

**后端**：Parallel Chat API（核心模型）

**响应**：综合Markdown报告，包含来自多个权威来源的引用，涵盖深入分析、关键发现和未来方向。

### 示例4：市场数据（路由到parallel-cli搜索）

**查询**："2025年全球医疗保健AI采用统计数据"

**后端**：parallel-cli搜索

**响应**：当前市场数据、采用率、增长预测和带有来源引用的区域分析。

---

## 摘要

此技能作为具有智能多后端路由的主要研究界面：

- **parallel-cli搜索**（默认）：任何主题的快速、经济的研究
- **Parallel Chat API**（仅按需）：深度、全面、多源研究
- **Perplexity sonar-pro-search**：仅用于学术特定论文搜索
- **自动路由**：检测学术查询和深度研究请求并适当路由
- **手动覆盖**：必要时强制使用任何后端
- **互补**：与`parallel-web`技能一起用于URL提取