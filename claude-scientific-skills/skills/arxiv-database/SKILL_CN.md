---
name: arxiv-database
description: 通过Atom API从arXiv搜索和检索预印本。当通过关键词、作者、arXiv ID、日期范围或类别搜索物理、数学、计算机科学、定量生物学、定量金融、统计学、电气工程或经济学论文时使用此技能。
license: MIT
metadata:
    skill-author: Orchestra Research
---






# arXiv 数据库

## 概述

此技能提供 Python 工具，用于通过公开的 Atom API 从 arXiv.org 搜索和检索预印本。它支持关键词搜索、作者搜索、类别筛选、arXiv ID 查询和 PDF 下载。结果以结构化 JSON 格式返回，包含标题、摘要、作者、类别和链接。

## 何时使用此技能

在以下情况下使用此技能：
- 搜索 CS、ML、AI、物理、数学、统计学、q-bio、q-fin 或经济学领域的预印本
- 按 arXiv ID 查找特定论文（例如 `2309.10668`）
- 追踪某位作者最近的预印本
- 按 arXiv 类别筛选论文（例如 `cs.LG`、`cs.CL`、`stat.ML`）
- 下载 PDF 进行全文分析
- 为 AI/ML 研究构建文献综述数据集
- 监控某子领域的新提交

在以下情况下考虑使用替代方案：
- 专门搜索生物医学文献 -> 使用 **pubmed-database** 或 **biorxiv-database**
- 需要引用次数或影响因子 -> 使用 **openalex-database**
- 只需要同行评审的期刊文章 -> 使用 **pubmed-database**

## 核心搜索功能

### 1. 关键词搜索

按标题、摘要或所有字段中的关键词搜索论文。

```bash
python scripts/arxiv_search.py \
  --keywords "sparse autoencoders" "mechanistic interpretability" \
  --max-results 20 \
  --output results.json
```

带类别筛选：
```bash
python scripts/arxiv_search.py \
  --keywords "transformer" "attention mechanism" \
  --category cs.LG \
  --max-results 50 \
  --output transformer_papers.json
```

搜索特定字段：
```bash
# 仅标题
python scripts/arxiv_search.py \
  --keywords "GRPO" \
  --search-field ti \
  --max-results 10

# 仅摘要
python scripts/arxiv_search.py \
  --keywords "reward model" "RLHF" \
  --search-field abs \
  --max-results 30
```

### 2. 作者搜索

```bash
python scripts/arxiv_search.py \
  --author "Anthropic" \
  --max-results 50 \
  --output anthropic_papers.json
```

```bash
python scripts/arxiv_search.py \
  --author "Ilya Sutskever" \
  --category cs.LG \
  --max-results 20
```

### 3. arXiv ID 查询

检索特定论文的元数据：

```bash
python scripts/arxiv_search.py \
  --ids 2309.10668 2406.04093 2310.01405 \
  --output sae_papers.json
```

也接受完整的 arXiv URL：
```bash
python scripts/arxiv_search.py \
  --ids "https://arxiv.org/abs/2309.10668"
```

### 4. 类别浏览

列出某类别中的最新论文：
```bash
python scripts/arxiv_search.py \
  --category cs.AI \
  --max-results 100 \
  --sort-by submittedDate \
  --output recent_cs_ai.json
```

### 5. PDF 下载

```bash
python scripts/arxiv_search.py \
  --ids 2309.10668 \
  --download-pdf papers/
```

从搜索结果批量下载：
```python
import json
from scripts.arxiv_search import ArxivSearcher

searcher = ArxivSearcher()

# 先搜索
results = searcher.search(query="ti:sparse autoencoder", max_results=5)

# 下载全部
for paper in results:
    arxiv_id = paper["arxiv_id"]
    searcher.download_pdf(arxiv_id, f"papers/{arxiv_id.replace('/', '_')}.pdf")
```

## arXiv 类别

### 计算机科学 (cs.*)
| 类别 | 描述 |
|------|------|
| `cs.AI` | 人工智能 |
| `cs.CL` | 计算与语言（自然语言处理） |
| `cs.CV` | 计算机视觉 |
| `cs.LG` | 机器学习 |
| `cs.NE` | 神经与进化计算 |
| `cs.RO` | 机器人学 |
| `cs.CR` | 密码学与安全 |
| `cs.DS` | 数据结构与算法 |
| `cs.IR` | 信息检索 |
| `cs.SE` | 软件工程 |

### 数学与统计
| 类别 | 描述 |
|------|------|
| `stat.ML` | 机器学习（统计学） |
| `stat.ME` | 方法论 |
| `math.OC` | 优化与控制 |
| `math.ST` | 统计理论 |

### 其他相关类别
| 类别 | 描述 |
|------|------|
| `q-bio.BM` | 生物分子 |
| `q-bio.GN` | 基因组学 |
| `q-bio.QM` | 定量方法 |
| `q-fin.ST` | 统计金融 |
| `eess.SP` | 信号处理 |
| `physics.comp-ph` | 计算物理 |

完整列表：见 [references/api_reference.md](references/api_reference.md)。

## 查询语法

arXiv API 使用基于前缀的字段搜索，结合布尔运算符。

**字段前缀：**
- `ti:` - 标题
- `au:` - 作者
- `abs:` - 摘要
- `cat:` - 类别
- `all:` - 所有字段（默认）
- `co:` - 评论
- `jr:` - 期刊引用
- `id:` - arXiv ID

**布尔运算符**（必须大写）：
```
ti:transformer AND abs:attention
au:bengio OR au:lecun
cat:cs.LG ANDNOT cat:cs.CV
```

**使用括号分组：**
```
(ti:sparse AND ti:autoencoder) AND cat:cs.LG
au:anthropic AND (abs:interpretability OR abs:alignment)
```

**示例：**
```python
from scripts.arxiv_search import ArxivSearcher

searcher = ArxivSearcher()

# 关于 ML 中 SAE 的论文
results = searcher.search(
    query="ti:sparse autoencoder AND cat:cs.LG",
    max_results=50,
    sort_by="submittedDate"
)

# 特定作者在特定领域
results = searcher.search(
    query="au:neel nanda AND cat:cs.LG",
    max_results=20
)

# 复杂布尔查询
results = searcher.search(
    query="(abs:RLHF OR abs:reinforcement learning from human feedback) AND cat:cs.CL",
    max_results=100
)
```

## 输出格式

所有搜索返回结构化 JSON：

```json
{
  "query": "ti:sparse autoencoder AND cat:cs.LG",
  "result_count": 15,
  "results": [
    {
      "arxiv_id": "2309.10668",
      "title": "Towards Monosemanticity: Decomposing Language Models With Dictionary Learning",
      "authors": ["Trenton Bricken", "Adly Templeton", "..."],
      "abstract": "Full abstract text...",
      "categories": ["cs.LG", "cs.AI"],
      "primary_category": "cs.LG",
      "published": "2023-09-19T17:58:00Z",
      "updated": "2023-10-04T14:22:00Z",
      "doi": "10.48550/arXiv.2309.10668",
      "pdf_url": "http://arxiv.org/pdf/2309.10668v1",
      "abs_url": "http://arxiv.org/abs/2309.10668v1",
      "comment": "42 pages, 30 figures",
      "journal_ref": ""
    }
  ]
}
```

## 常见使用模式

### 文献综述工作流

1. **定义研究问题**：明确您的研究问题和关键词
2. **广泛搜索**：使用关键词搜索获取相关论文
3. **筛选结果**：按日期或相关性筛选
4. **深入阅读**：下载PDF进行详细阅读
5. **追踪引用**：查看引用的论文

### 跟踪研究小组

```python
# 跟踪特定作者的最近论文
results = searcher.search(
    query="au:neel nanda",
    max_results=50
)

# 过滤最近一年的论文
from datetime import datetime, timedelta
one_year_ago = datetime.now() - timedelta(days=365)
recent_papers = [r for r in results 
                 if datetime.strptime(r['published'], '%Y-%m-%dT%H:%M:%SZ') > one_year_ago]
```

### 监控新提交

```python
# 定期检查新论文
import time

while True:
    results = searcher.search(
        query="cat:cs.LG AND submittedDate:[NOW-7DAYS TO NOW]",
        max_results=10
    )
    
    for paper in results:
        print(f"新论文: {paper['title']}")
    
    time.sleep(86400)  # 每天检查一次
```

## Python API

```python
from arxiv import Search, Client

# 创建客户端
client = Client()

# 搜索论文
search = Search(
    query="quantum computing",
    max_results=10,
    sort_by="submittedDate",
    sort_order="descending"
)

# 获取结果
for result in client.results(search):
    print(f"标题: {result.title}")
    print(f"作者: {result.authors}")
    print(f"PDF: {result.pdf_url}")
```

## 最佳实践

1. **使用精确的查询**：越具体的查询返回越相关的结果
2. **设置适当的限制**：不要一次获取太多结果
3. **缓存结果**：避免重复查询
4. **尊重速率限制**：arXiv 有请求频率限制
5. **使用类别过滤**：使用类别缩小搜索范围

## 限制

1. **搜索范围**：仅搜索 arXiv，不包括其他学术数据库
2. **全文搜索**：不提供全文搜索，只搜索标题和摘要
3. **速率限制**：需要遵守 arXiv 的使用政策
4. **数据延迟**：新提交可能需要一些时间才能被索引

## 参考文档

- [arXiv API 文档](http://arxiv.org/help/api)
- [arXiv 类别列表](http://arxiv.org/category_taxonomy)
- [Python arxiv 库](https://pypi.org/project/arxiv/)
