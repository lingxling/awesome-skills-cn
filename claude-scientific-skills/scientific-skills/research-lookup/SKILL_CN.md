---
name: research-lookup
description: 使用 parallel-cli 搜索（主要、快速网页搜索）、Parallel Chat API（深度研究）或 Perplexity sonar-pro-search（学术论文搜索）查找当前研究信息。自动将查询路由到最佳后端。用于查找论文、收集研究数据和验证科学信息。注意：查询文本会传输到 api.parallel.ai（PARALLEL_API_KEY），对于学术搜索，还会传输到 openrouter.ai（OPENROUTER_API_KEY）。
allowed-tools: Read Write Edit Bash
license: MIT license
compatibility: parallel-cli required (primary); PARALLEL_API_KEY and OPENROUTER_API_KEY optional for deep/academic backends
metadata:
    skill-author: K-Dense Inc.
---

# 研究信息查找

## 概述

本技能提供实时研究信息查找，具备**智能后端路由**功能：

- **parallel-cli search**（parallel-web 技能）：所有研究查询的**主要和默认后端**。快速、经济的网页搜索，优先使用学术来源。使用带 `--include-domains` 参数的 `parallel-cli search` 来获取学术来源。
- **Parallel Chat API**（`core` 模型）：用于需要多来源深度综合的复杂研究（延迟 60 秒-5 分钟）的辅助后端。仅在明确需要时使用。
- **Perplexity sonar-pro-search**（通过 OpenRouter）：仅用于学术特定的论文搜索，其中学术数据库访问至关重要。

本技能自动检测查询类型并路由到最优后端。

## 何时使用本技能

当您需要以下功能时使用本技能：

- **当前研究信息**：最新研究、论文和发现
- **文献验证**：根据当前研究核查事实、统计数据或主张
- **背景研究**：为科学写作收集背景和支持证据
- **引用来源**：查找相关论文和研究以引用
- **技术文档**：查找规范、协议或方法
- **市场/行业数据**：当前统计数据、趋势、竞争情报
- **最新进展**：新兴趋势、突破、公告

## 使用科学示意图进行视觉增强

**使用本技能创建文档时，请始终考虑添加科学图表和示意图以增强视觉传达。**

如果您的文档尚未包含示意图或图表：
- 使用 **scientific-schematics** 技能生成 AI 驱动的出版级质量图表
- 只需用自然语言描述您想要的图表

```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

---

## 自动后端选择

本技能根据内容自动将查询路由到最佳后端：

### 路由逻辑

```
查询到达
    |
    +-- 包含学术关键词？（论文、DOI、期刊、同行评审等）
    |       是 --> Perplexity sonar-pro-search（学术搜索模式）
    |
    +-- 需要深度多来源综合？（用户说"深度研究"、"详尽"）
    |       是 --> Parallel Chat API（core 模型，60秒-5分钟）
    |
    +-- 其他所有情况（一般研究、市场数据、技术信息、分析）
            --> parallel-cli search（快速、默认）
```

### 默认：parallel-cli search（parallel-web 技能）

**所有标准研究查询的主要后端。** 快速、经济，并支持学术来源优先。

对于科学/技术查询，运行两次搜索以确保学术覆盖：

```bash
# 1. 学术聚焦搜索
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
- `--after-date YYYY-MM-DD` 用于时效性查询
- `--include-domains domain1.com,domain2.com` 以限制特定来源

合并结果，以学术来源为首。对于非科学查询，一次一般搜索就足够了。

所有其他查询默认路由到这里，包括：

- 一般研究问题
- 市场和行业分析
- 技术信息和文档
- 当前事件和最新进展
- 比较分析
- 统计数据检索
- 事实核查和验证

### 学术关键词（路由到 Perplexity）

包含这些术语的查询将被路由到 Perplexity 进行学术聚焦搜索：

- 论文查找：`find papers`、`find articles`、`research papers on`、`published studies`
- 引用：`cite`、`citation`、`doi`、`pubmed`、`pmid`
- 学术来源：`peer-reviewed`、`journal article`、`scholarly`、`arxiv`、`preprint`
- 综述类型：`systematic review`、`meta-analysis`、`literature search`
- 论文质量：`foundational papers`、`seminal papers`、`landmark papers`、`highly cited`

### 深度研究（路由到 Parallel Chat API）

仅在用户明确要求深度、详尽或全面研究时使用。比 parallel-cli search 慢得多且更昂贵。

### 手动覆盖

您可以强制使用特定后端：

```bash
# 强制 parallel-cli search（快速网页搜索）
parallel-cli search "your query" -q "keyword" --json --max-results 10 -o sources/research_<topic>.json

# 强制 Parallel 深度研究（慢、详尽）
python research_lookup.py "your query" --force-backend parallel

# 强制 Perplexity 学术搜索
python research_lookup.py "your query" --force-backend perplexity
```

---

## 核心功能

### 1. 一般研究查询（parallel-cli search — 默认）

**主要后端。** 通过 parallel-web 技能进行快速、经济的网页搜索，优先使用学术来源。

```
查询示例：
- "Recent advances in CRISPR gene editing 2025"
- "Compare mRNA vaccines vs traditional vaccines for cancer treatment"
- "AI adoption in healthcare industry statistics"
- "Global renewable energy market trends and projections"
- "Explain the mechanism underlying gut microbiome and depression"
```

```bash
# 示例：CRISPR 进展研究
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
- 带有搜索结果内联引用的综合发现
- 学术来源优先（同行评审、预印本）
- 具体事实、数字和日期
- 按类型分组列出所有引用 URL 的来源部分

### 2. 学术论文搜索（Perplexity sonar-pro-search）

**用于学术特定查询。** 优先使用学术数据库和同行评审来源。当查询明确要求论文、引用或 DOI 时使用。

```
查询示例：
- "Find papers on transformer attention mechanisms in NeurIPS 2024"
- "Foundational papers on quantum error correction"
- "Systematic review of immunotherapy in non-small cell lung cancer"
- "Cite the original BERT paper and its most influential follow-ups"
- "Published studies on CRISPR off-target effects in clinical trials"
```

**响应包括：**
- 学术文献关键发现摘要
- 5-8 个高质量引用，包含作者、标题、期刊、年份、DOI
- 引用次数和会议级别指标
- 关键统计和方法亮点
- 研究空白和未来方向

### 3. 深度研究（Parallel Chat API — 仅应请求）

**仅在用户明确要求深度/详尽研究时使用。** 通过 Chat API（`core` 模型）提供全面的多来源综合。延迟 60 秒-5 分钟。

```
查询示例：
- "Deep research on the current state of quantum computing error correction"
- "Exhaustive analysis of mRNA vaccine platforms for cancer immunotherapy"
```

### 4. 技术和方法信息

使用 parallel-cli search（默认）进行快速查找：

```bash
parallel-cli search "Western blot protocol for protein detection" \
  -q "western blot" -q "protocol" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  -o sources/research_western_blot.json
```

### 5. 统计和市场数据

使用 parallel-cli search（默认）获取当前数据：

```bash
parallel-cli search "Global AI market size and growth projections 2025" \
  -q "AI market" -q "statistics" -q "growth" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  --after-date 2024-01-01 \
  -o sources/research_ai_market.json
```

---

## 论文质量和影响力优先排序

**重要**：搜索论文时，始终优先选择高质量、有影响力的论文。

### 基于引用的排名

| 论文年限 | 引用阈值 | 分类 |
|---------|---------|------|
| 0-3 年 | 20+ 引用 | 值得关注 |
| 0-3 年 | 100+ 引用 | 高影响力 |
| 3-7 年 | 100+ 引用 | 重要 |
| 3-7 年 | 500+ 引用 | 里程碑论文 |
| 7+ 年 | 500+ 引用 | 开创性工作 |
| 7+ 年 | 1000+ 引用 | 奠基性 |

### 会议/期刊质量等级

**一级 - 顶级会议/期刊**（始终优先）：
- **综合科学**：Nature, Science, Cell, PNAS
- **医学**：NEJM, Lancet, JAMA, BMJ
- **特定领域**：Nature Medicine, Nature Biotechnology, Nature Methods
- **顶级 CS/AI**：NeurIPS, ICML, ICLR, ACL, CVPR

**二级 - 高影响力专业**（强烈偏好）：
- 影响因子 > 10 的期刊
- 子领域顶级会议（EMNLP, NAACL, ECCV, MICCAI）

**三级 - 受尊重的专业**（相关时包含）：
- 影响因子 5-10 的期刊

---

## 技术集成

### 先决条件

```bash
# 主要后端（parallel-cli）- 必需
# 如果尚未安装 parallel-cli，请安装：
curl -fsSL https://parallel.ai/install.sh | bash
# 或：uv tool install "parallel-web-tools[cli]"

# 认证：
parallel-cli auth
# 或：export PARALLEL_API_KEY="your_parallel_api_key"
```

### 环境变量

```bash
# 主要后端（parallel-cli search）- 必需
export PARALLEL_API_KEY="your_parallel_api_key"

# 深度研究后端（Parallel Chat API）- 可选，仅用于深度研究
# 使用相同的 PARALLEL_API_KEY

# 学术搜索后端（Perplexity）- 可选，用于学术论文查询
export OPENROUTER_API_KEY="your_openrouter_api_key"
```

### API 规范

**parallel-cli search（主要）：**
- 命令：带 `--json` 输出的 `parallel-cli search`
- 延迟：2-10 秒（快速）
- 输出：包含 title、URL、publish_date、excerpts 的 JSON
- 学术领域：使用 `--include-domains` 获取学术来源
- 保存结果：`-o filename.json` 用于后续处理和可重复性

**Parallel Chat API（仅深度研究）：**
- 端点：`https://api.parallel.ai`（兼容 OpenAI SDK）
- 模型：`core`（60秒-5分钟延迟，复杂多来源综合）
- 输出：带内联引用的 Markdown 文本
- 引用：包含 URL、推理和置信度的研究基础
- 速率限制：300 请求/分钟
- Python 包：`openai`

**Perplexity sonar-pro-search（仅学术）：**
- 模型：`perplexity/sonar-pro-search`（通过 OpenRouter）
- 搜索模式：学术（优先同行评审来源）
- 搜索上下文：高（综合研究）
- 响应时间：5-15 秒

### 命令行用法

```bash
# 通过 parallel-cli 进行快速网页搜索（默认 — 推荐）— 始终保存到 sources/
parallel-cli search "your query" -q "keyword1" -q "keyword2" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  -o sources/research_<topic>.json

# 通过 parallel-cli 进行学术聚焦搜索 — 始终保存到 sources/
parallel-cli search "your query" -q "keyword1" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  --include-domains "scholar.google.com,arxiv.org,pubmed.ncbi.nlm.nih.gov,semanticscholar.org,biorxiv.org,medrxiv.org,nature.com,science.org,cell.com,pnas.org,nih.gov" \
  -o sources/research_<topic>-academic.json

# 通过 parallel-cli 进行时效性搜索
parallel-cli search "your query" -q "keyword" \
  --json --max-results 10 --after-date 2024-01-01 \
  -o sources/research_<topic>.json

# 从特定 URL 提取完整内容（使用 parallel-web extract）
parallel-cli extract "https://example.com/paper" --json

# 强制 Parallel 深度研究（慢、详尽）— 通过 research_lookup.py
python research_lookup.py "your query" --force-backend parallel -o sources/research_<topic>.md

# 强制 Perplexity 学术搜索 — 通过 research_lookup.py
python research_lookup.py "your query" --force-backend perplexity -o sources/papers_<topic>.md

# 通过 research_lookup.py 自动路由（传统）— 始终保存到 sources/
python research_lookup.py "your query" -o sources/research_YYYYMMDD_HHMMSS_<topic>.md

# 通过 research_lookup.py 批量查询 — 始终保存到 sources/
python research_lookup.py --batch "query 1" "query 2" "query 3" -o sources/batch_research_<topic>.md
```

---

## 强制要求：将所有结果保存到 Sources 文件夹

**每个 research-lookup 结果都必须保存到项目的 `sources/` 文件夹中。**

这是不可协商的。研究结果获取成本高昂，对可重复性至关重要。

### 保存规则

| 后端 | `-o` 标志目标 | 文件名模式 |
|---------|-----------------|------------------|
| parallel-cli search（默认） | `sources/research_<topic>.json` | `research_<brief_topic>.json` 或 `research_<brief_topic>-academic.json` |
| Parallel 深度研究 | `sources/research_<topic>.md` | `research_YYYYMMDD_HHMMSS_<brief_topic>.md` |
| Perplexity（学术） | `sources/papers_<topic>.md` | `papers_YYYYMMDD_HHMMSS_<brief_topic>.md` |
| 批量查询 | `sources/batch_<topic>.md` | `batch_research_YYYYMMDD_HHMMSS_<brief_topic>.md` |

### 如何保存

**重要：每次搜索都必须使用 `-o` 标志将结果保存到 `sources/` 文件夹。**

**重要：保存的文件必须保留所有引用、来源 URL 和 DOI。**

```bash
# parallel-cli search（默认）— 保存 JSON 到 sources/
parallel-cli search "Recent advances in CRISPR gene editing 2025" \
  -q "CRISPR" -q "gene editing" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  --include-domains "scholar.google.com,arxiv.org,pubmed.ncbi.nlm.nih.gov,nature.com,science.org,cell.com,pnas.org,nih.gov" \
  -o sources/research_crispr_advances-academic.json

parallel-cli search "Recent advances in CRISPR gene editing 2025" \
  -q "CRISPR" -q "gene editing" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  -o sources/research_crispr_advances-general.json

# 通过 Perplexity 进行学术论文搜索 — 保存到 sources/
python research_lookup.py "Find papers on transformer attention mechanisms in NeurIPS 2024" \
  -o sources/papers_20250217_143500_transformer_attention.md

# 通过 Parallel Chat API 进行深度研究 — 保存到 sources/
python research_lookup.py "AI regulation landscape" --force-backend parallel \
  -o sources/research_20250217_144000_ai_regulation.md

# 批量查询 — 保存到 sources/
python research_lookup.py --batch "mRNA vaccines efficacy" "mRNA vaccines safety" \
  -o sources/batch_research_20250217_144500_mrna_vaccines.md
```

### 保存文件中的引用保留

每种输出格式以不同方式保留引用：

| 格式 | 包含的引用 | 何时使用 |
|--------|-------------------|-------------|
| parallel-cli JSON（默认） | 完整结果对象：`title`、`url`、`publish_date`、`excerpts` | 标准使用 — 结构化、可解析、快速 |
| 文本（research_lookup.py） | `Sources (N):` 部分，包含 `[title] (date) + URL` + `Additional References (N):` 包含 DOI 和学术 URL | 深度研究 / Perplexity — 人类可读 |
| JSON（通过 research_lookup.py 的 `--json`） | 完整引用对象：`url`、`title`、`date`、`snippet`、`doi`、`type` | 当您需要从深度研究获取最大引用元数据时 |

**对于 parallel-cli search**，保存的 JSON 文件包括：每个结果的完整搜索结果，包含标题、URL、发布日期和内容摘录。
**对于 Parallel Chat API 后端**，保存的文件包括：研究报告 + 来源列表（标题、URL）+ 附加参考（DOI、学术 URL）。
**对于 Perplexity 后端**，保存的文件包括：学术摘要 + 来源列表（标题、日期、URL、摘录）+ 附加参考（DOI、学术 URL）。

**在以下情况使用 `--json`：**
- 以编程方式解析引用元数据
- 保留完整的 DOI 和 URL 数据以生成 BibTeX
- 维护用于交叉引用的结构化引用对象

### 为什么保存所有内容

1. **可重复性**：每个引用和主张都可以追溯到其原始研究来源
2. **上下文窗口恢复**：如果上下文被压缩，可以重新读取保存的结果而无需重新查询
3. **审计跟踪**：`sources/` 文件夹准确记录了所有研究信息的收集方式
4. **跨章节复用**：多个章节可以引用相同的已保存研究，无需重复查询
5. **成本效益**：在进行新的 API 调用之前，检查 `sources/` 中是否已有现有结果
6. **同行评审支持**：评审员可以验证每个引用背后的研究

### 在进行新查询之前，先检查 Sources

在调用 `research_lookup.py` 之前，检查是否已存在相关结果：

```bash
ls sources/  # 检查现有保存的结果
```

如果之前的查找涵盖了相同主题，请重新读取保存的文件，而不是进行新的 API 调用。

### 日志记录

保存研究结果时，始终记录：

```
[HH:MM:SS] SAVED: Research lookup to sources/research_20250217_143000_crispr_advances.md (3,800 words, 8 citations)
[HH:MM:SS] SAVED: Paper search to sources/papers_20250217_143500_transformer_attention.md (6 papers found)
```

---

## 与科学写作集成

本技能通过以下方式增强科学写作：

1. **文献综述支持**：为引言和讨论收集当前研究 — **保存到 `sources/`**
2. **方法验证**：根据当前标准验证协议 — **保存到 `sources/`**
3. **结果情境化**：将发现与最近的类似研究进行比较 — **保存到 `sources/`**
4. **讨论增强**：用最新证据支持论点 — **保存到 `sources/`**
5. **引用管理**：提供正确格式的引用 — **保存到 `sources/`**

## 补充工具

| 任务 | 工具 |
|------|------|
| 一般网页搜索（快速） | `parallel-cli search`（内置于本技能） |
| 学术聚焦网页搜索 | `parallel-cli search --include-domains`（内置于本技能） |
| URL 内容提取 | `parallel-cli extract`（parallel-web 技能） |
| 深度研究（详尽） | `research-lookup` 通过 Parallel Chat API 或 `parallel-web` 深度研究 |
| 学术论文搜索 | `research-lookup`（自动路由到 Perplexity） |
| Google Scholar 搜索 | `citation-management` 技能 |
| PubMed 搜索 | `citation-management` 技能 |
| DOI 转 BibTeX | `citation-management` 技能 |
| 元数据验证 | `parallel-cli extract`（parallel-web 技能） |

---

## 错误处理和限制

**已知限制：**
- parallel-cli search：需要安装并认证 `parallel-cli`
- Parallel Chat API（core 模型）：复杂查询可能需要长达 5 分钟
- Perplexity：信息有截止日期，可能无法访问付费墙后的全文
- 所有后端：无法访问专有或受限数据库

**回退行为：**
- 如果未找到 `parallel-cli`，请使用 `curl -fsSL https://parallel.ai/install.sh | bash` 或 `uv tool install "parallel-web-tools[cli]"` 安装
- 如果 parallel-cli search 返回的结果不足，则回退到 Perplexity 或 Parallel Chat API
- 如果所选后端的 API 密钥缺失，则尝试其他后端
- 如果所有后端都失败，则返回结构化错误响应
- 如果初始响应不足，请改写查询以获得更好的结果

---

## 使用示例

### 示例 1：一般研究（路由到 parallel-cli search）

**查询**："Recent advances in transformer attention mechanisms 2025"

**后端**：parallel-cli search（默认、快速）

**命令**：
```bash
parallel-cli search "Recent advances in transformer attention mechanisms 2025" \
  -q "transformer" -q "attention" -q "2025" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  --include-domains "arxiv.org,semanticscholar.org,nature.com,science.org,ieee.org,acm.org" \
  -o sources/research_transformer_attention-academic.json

parallel-cli search "Recent advances in transformer attention mechanisms 2025" \
  -q "transformer" -q "attention" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  -o sources/research_transformer_attention-general.json
```

**响应**：来自学术和一般来源的综合发现，包含内联引用，涵盖近期论文、关键创新和性能基准。

### 示例 2：学术论文搜索（路由到 Perplexity）

**查询**："Find papers on CRISPR off-target effects in clinical trials"

**后端**：Perplexity sonar-pro-search（学术模式）

**响应**：5-8 篇高影响力论文的精选列表，包含完整引用、DOI、引用次数和会议级别指标。

### 示例 3：比较分析（路由到 parallel-cli search）

**查询**："Compare and contrast mRNA vaccines vs traditional vaccines for cancer treatment"

**后端**：parallel-cli search（默认、快速）

**响应**：来自多个网页来源的综合比较，包含内联引用、结构化分析和证据质量说明。

### 示例 4：市场数据（路由到 parallel-cli search）

**查询**："Global AI adoption in healthcare statistics 2025"

**后端**：parallel-cli search（默认、快速）

```bash
parallel-cli search "Global AI adoption in healthcare statistics 2025" \
  -q "AI healthcare" -q "adoption statistics" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  --after-date 2024-01-01 \
  -o sources/research_ai_healthcare_adoption.json
```

**响应**：当前市场数据、采用率、增长预测和区域分析，包含来源引用。

---

## 总结

本技能作为具有智能三后端路由的主要研究接口：

- **parallel-cli search**（默认）：通过 parallel-web 技能进行快速、经济的网页搜索，优先使用学术来源
- **Parallel Chat API**（`core` 模型）：深度、详尽的多来源综合（仅应明确请求）
- **Perplexity sonar-pro-search**：仅用于学术特定论文搜索
- **自动路由**：检测查询类型并路由到最优后端
- **手动覆盖**：在需要时强制使用任何后端
- **学术优先**：两次搜索模式确保科学查询的学术来源浮现
