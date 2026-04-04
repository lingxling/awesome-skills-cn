---
name: paper-lookup
description: 通过 REST API 搜索 10 个学术论文数据库，查找研究论文、预印本和学术文章。涵盖生物医学文献（PubMed、PMC 全文）、预印本服务器（bioRxiv、medRxiv、arXiv）、多学科索引（OpenAlex、Crossref、Semantic Scholar）、开放获取聚合器（CORE、Unpaywall）。当用户想要搜索研究论文、查找引用、通过 DOI 或 PMID 查找文章、检索摘要或全文、检查开放获取可用性、查找预印本、探索引用图、按作者或关键词搜索，或访问任何学术文献数据库时使用此技能。当用户提到 PubMed、PMC、bioRxiv、medRxiv、arXiv、OpenAlex、Crossref、Semantic Scholar、CORE、Unpaywall，或询问论文元数据、引用计数、期刊文章、手稿查找、文献综述或系统性搜索时也会触发。即使用户只是说"查找关于 X 的论文"或"关于 Y 发表了什么"或"查找这个 DOI"，此技能也应该激活。
metadata:
  skill-author: K-Dense Inc.
---

# 论文查找

您可以通过 REST API 访问 10 个学术论文数据库。您的任务是确定哪些数据库最适合用户的查询，调用它们，并返回结果。

## 核心工作流程

1. **理解查询** -- 用户在寻找什么？通过 DOI 查找特定论文？关于某个主题的论文？作者的出版物？开放获取 PDF？全文？这决定了要访问哪些数据库。

2. **选择数据库** -- 使用下面的数据库选择指南。许多查询受益于访问多个数据库 -- 例如，在 PubMed 中搜索论文，然后在 Unpaywall 中检查开放获取副本。

3. **阅读参考文件** -- 每个数据库在 `references/` 目录中都有一个参考文件，包含端点详细信息、查询格式和示例调用。在进行 API 调用之前阅读相关文件。

4. **进行 API 调用** -- 请参阅下面的**进行 API 调用**部分，了解在您的平台上使用哪个 HTTP 抓取工具。

5. **返回结果** -- 始终返回：
   - 每个数据库的**原始 JSON**（或 arXiv 的解析 XML）响应
   - **查询的数据库列表**以及使用的特定端点
   - 如果查询返回无结果，明确说明而不是省略

## 数据库选择指南

将用户的意图与正确的数据库匹配。

### 按用例

| 用户询问关于... | 主要数据库 | 也可考虑 |
|---|---|---|
| 生物医学主题的论文 | PubMed | Semantic Scholar、OpenAlex |
| 生物医学文章的全文 | PMC | CORE |
| 生物学预印本 | bioRxiv | Semantic Scholar、OpenAlex |
| 健康/医学预印本 | medRxiv | Semantic Scholar、OpenAlex |
| 物理、数学或计算机科学预印本 | arXiv | Semantic Scholar、OpenAlex |
| 跨所有领域的论文 | OpenAlex | Semantic Scholar、Crossref |
| 通过 DOI 查找特定论文 | Crossref | Unpaywall、Semantic Scholar |
| 论文的开放获取 PDF | Unpaywall | CORE、PMC |
| 引用图（谁引用谁） | Semantic Scholar | OpenAlex |
| 作者的出版物 | Semantic Scholar | OpenAlex |
| 论文推荐 | Semantic Scholar | -- |
| 全文（任何领域） | CORE | PMC（仅限生物医学） |
| 期刊/出版商元数据 | Crossref | OpenAlex |
| 资助者信息 | Crossref | OpenAlex |
| 在 PMID/PMCID/DOI 之间转换 | PMC (ID Converter) | Crossref |
| 按日期排序的最新预印本 | bioRxiv、medRxiv | arXiv |

### 跨数据库查询

| 用户询问关于... | 要查询的数据库 |
|---|---|
| 关于论文的一切（元数据 + 引用 + OA） | Crossref + Semantic Scholar + Unpaywall |
| 综合文献搜索 | PubMed + OpenAlex + Semantic Scholar |
| 查找并阅读论文 | PubMed（查找） + Unpaywall（OA 链接） + PMC 或 CORE（全文） |
| 预印本及其已发表版本 | bioRxiv/medRxiv + Crossref |
| 带引用指标的作者概述 | Semantic Scholar + OpenAlex |

当查询跨越多个需求时（例如，"查找关于 CRISPR 的论文并给我 PDF"），并行查询相关数据库。

## 常见标识符格式

不同的数据库使用不同的标识符系统。如果查询失败，标识符格式可能错误。

| 标识符 | 格式 | 示例 | 使用数据库 |
|---|---|---|---|
| DOI | `10.xxxx/xxxxx` | `10.1038/nature12373` | 所有数据库 |
| PMID | 整数 | `34567890` | PubMed、PMC、Semantic Scholar |
| PMCID | `PMC` + 数字 | `PMC7029759` | PMC、Europe PMC |
| arXiv ID | `YYMM.NNNNN` | `2103.15348` | arXiv、Semantic Scholar |
| OpenAlex ID | `W` + 数字 | `W2741809807` | OpenAlex |
| Semantic Scholar ID | 40 字符十六进制 | `649def34f8be...` | Semantic Scholar |
| ORCID | `0000-XXXX-XXXX-XXXX` | `0000-0001-6187-6610` | OpenAlex、Crossref |
| ISSN | `XXXX-XXXX` | `0028-0836` | Crossref、OpenAlex |

**交叉引用 ID：** Semantic Scholar 通过前缀接受 DOI、PMID、PMCID 和 arXiv ID（例如，`DOI:10.1038/nature12373`、`PMID:34567890`、`ARXIV:2103.15348`）。OpenAlex 通过前缀接受 DOI 和 PMID（`doi:10.1038/...`、`pmid:34567890`）。使用 PMC ID Converter 在 PMID、PMCID 和 DOI 之间转换。

## API 密钥和访问

这些数据库大多完全开放。少数受益于 API 密钥以获得更高的速率限制。

### 需要或受益于 API 密钥的数据库

| 数据库 | 环境变量 | 是否必需？ | 注册 |
|---|---|---|---|
| NCBI (PubMed, PMC) | `NCBI_API_KEY` | 否（无密钥 3 req/s，有密钥 10 req/s） | https://www.ncbi.nlm.nih.gov/account/settings/ |
| CORE | `CORE_API_KEY` | 全文需要 | https://core.ac.uk/services/api |
| Semantic Scholar | `S2_API_KEY` | 否（无密钥共享池） | https://www.semanticscholar.org/product/api#api-key-form |
| OpenAlex | `OPENALEX_API_KEY` | 推荐 | https://openalex.org/settings/api |

### 完全开放的数据库（无需密钥）

| 数据库 | 说明 |
|---|---|
| bioRxiv / medRxiv | 无认证，无记录的速率限制 |
| arXiv | 无认证，最多每 3 秒 1 个请求 |
| Crossref | 无认证；添加 `mailto` 参数以获得礼貌池（2 倍速率限制） |
| Unpaywall | 无认证；需要 `email` 参数 |

### 加载 API 密钥

1. **首先检查环境** -- 密钥可能已经导出（例如，`$NCBI_API_KEY`）。
2. **回退到 `.env`** -- 检查当前工作目录中的 `.env` 文件。
3. **继续无密钥** -- 大多数 API 仍以较低的速率限制工作。告诉用户缺少哪个密钥以及如何获取。

## 进行 API 调用

使用环境的 HTTP 抓取工具调用 REST 端点：

| 平台 | HTTP 抓取工具 | 回退 |
|---|---|---|
| Claude Code | `WebFetch` | `curl` via Bash |
| Gemini CLI | `web_fetch` | `curl` via shell |
| Windsurf | `read_url_content` | `curl` via terminal |
| Cursor | 无专用抓取工具 | `curl` via `run_terminal_cmd` |
| Codex CLI | 无专用抓取工具 | `curl` via `shell` |
| Cline | 无专用抓取工具 | `curl` via `execute_command` |

如果抓取工具失败，回退到通过任何可用的 shell 工具使用 `curl`。

### 特殊情况

- **arXiv 返回 Atom XML**，不是 JSON。解析它或使用 `curl` 并提取相关字段。如果可用，考虑通过简单解析器管道传递。
- **PMC eFetch 返回 JATS XML** 作为全文。这是预期的 -- 全文文章采用 XML 格式。
- **Crossref 和 Unpaywall** 受益于包含 `mailto` 参数或电子邮件以获得礼貌/快速池。

### 请求指南

- 对于 **NCBI API**（PubMed、PMC）：无密钥 3 req/sec，有密钥 10 req/sec。顺序进行请求。
- 对于 **arXiv**：最多每 3 秒 1 个请求。请耐心等待。
- 对于 **Crossref**：5 req/sec（公共），10 req/sec（带 `mailto` 的礼貌池）。
- 对于没有严格限制的其他 API，您可以并行查询多个数据库。
- 如果收到 HTTP 429（速率限制），短暂等待并重试一次。

### 错误恢复

1. **检查标识符格式** -- 使用常见标识符格式表。PMID 在 arXiv 中不起作用，arXiv ID 不能直接在 PubMed 中使用。
2. **尝试替代标识符** -- 如果 DOI 在一个数据库中失败，尝试标题或 PMID 代替。
3. **尝试不同的数据库** -- 如果 PubMed 对 CS 论文返回无结果，尝试 Semantic Scholar 或 OpenAlex。
4. **报告失败** -- 告诉用户哪个数据库失败，错误是什么，以及您尝试了什么替代方案。

## 输出格式

按以下结构组织您的响应：

```
## 已查询数据库
- **PubMed** -- esearch + esummary for "CRISPR gene therapy"
- **Unpaywall** -- DOI lookup for 10.1038/...

## 结果

### PubMed
[原始 JSON 响应或格式化结果]

### Unpaywall
[原始 JSON 响应]
```

如果结果非常大，展示最相关的部分并注意还有更多数据可用。但默认显示完整的原始 JSON -- 用户要求了它。

## 可用数据库

在进行任何 API 调用之前，请阅读相关参考文件。

### 生物医学文献
| 数据库 | 参考文件 | 涵盖内容 |
|---|---|---|
| PubMed | `references/pubmed.md` | 37M+ 生物医学引用、摘要、MeSH 术语 |
| PMC | `references/pmc.md` | 10M+ 全文生物医学文章（JATS XML）、ID 转换 |

### 预印本服务器
| 数据库 | 参考文件 | 涵盖内容 |
|---|---|---|
| bioRxiv | `references/biorxiv.md` | 生物学预印本（按日期/DOI 浏览，无关键词搜索） |
| medRxiv | `references/medrxiv.md` | 健康科学预印本（按日期/DOI 浏览，无关键词搜索） |
| arXiv | `references/arxiv.md` | 物理、数学、计算机科学、生物学、经济学预印本（关键词搜索，Atom XML） |

### 多学科索引
| 数据库 | 参考文件 | 涵盖内容 |
|---|---|---|
| OpenAlex | `references/openalex.md` | 250M+ 作品、作者、机构、主题、引用数据 |
| Crossref | `references/crossref.md` | 150M+ DOI 元数据、期刊、资助者、参考文献 |
| Semantic Scholar | `references/semantic-scholar.md` | 200M+ 论文、引用图、AI 生成的 TLDR、推荐 |

### 开放获取与全文
| 数据库 | 参考文件 | 涵盖内容 |
|---|---|---|
| CORE | `references/core.md` | 37M+ 来自全球 OA 存储库的全文 |
| Unpaywall | `references/unpaywall.md` | 任何 DOI 的 OA 状态和 PDF 链接 |