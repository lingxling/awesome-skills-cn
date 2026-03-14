---
name: parallel-web
description: 使用 Parallel Chat API 和 Extract API 搜索网络、提取 URL 内容并运行深度研究。用于所有网络搜索、研究查询和一般信息收集。提供带有引用的综合摘要。
allowed-tools: Read Write Edit Bash
license: MIT license
compatibility: PARALLEL_API_KEY required
metadata:
    skill-author: K-Dense Inc.
---

# Parallel Web Systems API

## 概述

此技能提供对 **Parallel Web Systems** API 的访问，用于网络搜索、深度研究和内容提取。它是科学作家工作流程中**所有网络相关操作的主要工具**。

**主要接口**：Parallel Chat API（与 OpenAI 兼容）用于搜索和研究。
**次要接口**：Extract API 仅用于 URL 验证和特殊情况。

**API 文档**：https://docs.parallel.ai
**API 密钥**：https://platform.parallel.ai
**环境变量**：`PARALLEL_API_KEY`

## 何时使用此技能

将此技能用于**所有**以下情况：

- **网络搜索**：任何需要在互联网上搜索信息的查询
- **深度研究**：关于任何主题的综合研究报告
- **市场研究**：行业分析、竞争情报、市场数据
- **时事**：新闻、最新发展、公告
- **技术信息**：文档、规格、产品详情
- **统计数据**：市场规模、增长率、行业数据
- **一般信息**：公司简介、事实、比较

**仅将 Extract API 用于**：
- 引用验证（确认特定 URL 的内容）
- 需要从已知 URL 获取原始内容的特殊情况

**不要将此技能用于**：
- 学术特定论文搜索（使用 `research-lookup`，它将纯学术查询路由到 Perplexity）
- Google Scholar / PubMed 数据库搜索（使用 `citation-management` 技能）

---

## 两种功能

### 1. 网络搜索（`search` 命令）

通过 Parallel Chat API（`base` 模型）搜索网络，获取带有引用来源的**综合摘要**。

**最适合**：一般网络搜索、时事、事实查找、技术查询、新闻、市场数据。

```bash
# 基本搜索
python scripts/parallel_web.py search "latest advances in quantum computing 2025"

# 使用核心模型进行更复杂的查询
python scripts/parallel_web.py search "compare EV battery chemistries NMC vs LFP" --model core

# 将结果保存到文件
python scripts/parallel_web.py search "renewable energy policy updates" -o results.txt

# 用于编程使用的 JSON 输出
python scripts/parallel_web.py search "AI regulation landscape" --json -o results.json
```

**关键参数**：
- `objective`：您想要找到的内容的自然语言描述
- `--model`：要使用的聊天模型（默认 `base`，或 `core` 用于更深层次的研究）
- `-o`：输出文件路径
- `--json`：以 JSON 格式输出

**响应包括**：按主题组织的综合摘要，带有内联引用和来源列表。

### 2. 深度研究（`research` 命令）

通过 Parallel Chat API（`core` 模型）运行综合多源研究，生成带有引用的详细情报报告。

**最适合**：市场研究、综合分析、竞争情报、技术调查、行业报告、任何需要综合多个来源的研究问题。

```bash
# 默认深度研究（核心模型）
python scripts/parallel_web.py research "comprehensive analysis of the global EV battery market"

# 将研究报告保存到文件
python scripts/parallel_web.py research "AI adoption in healthcare 2025" -o report.md

# 使用基础模型进行更快、更轻量的研究
python scripts/parallel_web.py research "latest funding rounds in AI startups" --model base

# JSON 输出
python scripts/parallel_web.py research "renewable energy storage market in Europe" --json -o data.json
```

**关键参数**：
- `query`：研究问题或主题
- `--model`：要使用的聊天模型（默认 `core` 用于深度研究，或 `base` 用于更快的结果）
- `-o`：输出文件路径
- `--json`：以 JSON 格式输出

### 3. URL 提取（`extract` 命令）— 仅用于验证

从特定 URL 提取内容。**仅用于引用验证和特殊情况**。

对于一般研究，请使用 `search` 或 `research` 代替。

```bash
# 验证引用的内容
python scripts/parallel_web.py extract "https://example.com/article" --objective "key findings"

# 获取完整页面内容进行验证
python scripts/parallel_web.py extract "https://docs.example.com/api" --full-content

# 将提取内容保存到文件
python scripts/parallel_web.py extract "https://paper-url.com" --objective "methodology" -o extracted.md
```

---

## 模型选择指南

Chat API 支持两种研究模型。使用 `base` 进行大多数搜索，使用 `core` 进行深度研究。

| 模型   | 延迟      | 优势                              | 使用时机                    |
|--------|-----------|----------------------------------|-----------------------------|
| `base` | 15s-100s  | 标准研究，事实查询               | 网络搜索，快速查询          |
| `core` | 60s-5min  | 复杂研究，多源综合               | 深度研究，综合报告          |

**建议**：
- `search` 命令默认为 `base` — 快速，适合大多数查询
- `research` 命令默认为 `core` — 彻底，适合综合报告
- 当需要不同的深度/速度权衡时，使用 `--model` 覆盖

---

## Python API 使用

### 搜索

```python
from parallel_web import ParallelSearch

searcher = ParallelSearch()
result = searcher.search(
    objective="Find latest information about transformer architectures in NLP",
    model="base",
)

if result["success"]:
    print(result["response"])  # 综合摘要
    for src in result["sources"]:
        print(f"  {src['title']}: {src['url']}")
```

### 深度研究

```python
from parallel_web import ParallelDeepResearch

researcher = ParallelDeepResearch()
result = researcher.research(
    query="Comprehensive analysis of AI regulation in the EU and US",
    model="core",
)

if result["success"]:
    print(result["response"])  # 完整研究报告
    print(f"Citations: {result['citation_count']}")
```

### 提取（仅用于验证）

```python
from parallel_web import ParallelExtract

extractor = ParallelExtract()
result = extractor.extract(
    urls=["https://docs.example.com/api-reference"],
    objective="API authentication methods and rate limits",
)

if result["success"]:
    for r in result["results"]:
        print(r["excerpts"])
```

---

## 强制要求：将所有结果保存到 Sources 文件夹

**每个网络搜索和深度研究结果必须保存到项目的 `sources/` 文件夹中。**

这确保所有研究都被保存，以确保可重现性、可审计性和上下文窗口恢复。

### 保存规则

| 操作 | `-o` 标志目标 | 文件名模式 |
|-----------|-----------------|------------------|
| 网络搜索 | `sources/search_<topic>.md` | `search_YYYYMMDD_HHMMSS_<brief_topic>.md` |
| 深度研究 | `sources/research_<topic>.md` | `research_YYYYMMDD_HHMMSS_<brief_topic>.md` |
| URL 提取 | `sources/extract_<source>.md` | `extract_YYYYMMDD_HHMMSS_<brief_source>.md` |

### 如何保存（始终使用 `-o` 标志）

**关键：每个对 `parallel_web.py` 的调用必须包含指向 `sources/` 文件夹的 `-o` 标志。**

```bash
# 网络搜索 — 始终保存到 sources/
python scripts/parallel_web.py search "latest advances in quantum computing 2025" \
  -o sources/search_20250217_143000_quantum_computing.md

# 深度研究 — 始终保存到 sources/
python scripts/parallel_web.py research "comprehensive analysis of the global EV battery market" \
  -o sources/research_20250217_144000_ev_battery_market.md

# URL 提取（仅用于验证）— 保存到 sources/
python scripts/parallel_web.py extract "https://example.com/article" --objective "key findings" \
  -o sources/extract_20250217_143500_example_article.md
```

### 为什么保存所有内容

1. **可重现性**：最终文档中的每个声明都可以追溯到其原始源材料
2. **上下文窗口恢复**：如果任务中期上下文被压缩，可以从 `sources/` 重新读取保存的结果
3. **审计跟踪**：`sources/` 文件夹提供了信息收集方式的完全透明度
4. **跨部分重用**：保存的研究可以被多个部分引用，而无需重复 API 调用
5. **成本效率**：通过检查 `sources/` 中的现有结果避免冗余 API 调用
6. **同行评审支持**：评审人员可以验证支持每个声明的研究

### 日志记录

保存研究结果时，始终记录：

```
[HH:MM:SS] SAVED: Search results to sources/search_20250217_143000_quantum_computing.md
[HH:MM:SS] SAVED: Deep research report to sources/research_20250217_144000_ev_battery_market.md
```

### 在进行新查询之前，先检查 Sources

在调用 `parallel_web.py` 之前，检查 `sources/` 中是否已存在相关结果：

```bash
ls sources/  # 检查现有的保存结果
```

---

## 与科学作家的集成

### 路由表

| 任务 | 工具 | 命令 |
|------|------|---------|
| 网络搜索（任何） | `parallel_web.py search` | `python scripts/parallel_web.py search "query" -o sources/search_<topic>.md` |
| 深度研究 | `parallel_web.py research` | `python scripts/parallel_web.py research "query" -o sources/research_<topic>.md` |
| 引用验证 | `parallel_web.py extract` | `python scripts/parallel_web.py extract "url" -o sources/extract_<source>.md` |
| 学术论文搜索 | `research_lookup.py` | 路由到 Perplexity sonar-pro-search |
| DOI/元数据查询 | `parallel_web.py extract` | 从 DOI URL 提取（验证） |

### 编写科学文档时

1. **在编写任何部分之前**，使用 `search` 或 `research` 收集背景信息 — **将结果保存到 `sources/`**
2. **对于学术引用**，使用 `research-lookup`（将学术查询路由到 Perplexity）— **将结果保存到 `sources/`**
3. **对于引用验证**（确认特定 URL），使用 `parallel_web.py extract` — **将结果保存到 `sources/`**
4. **对于当前市场/行业数据**，使用 `parallel_web.py research --model core` — **将结果保存到 `sources/`**
5. **在任何新查询之前**，检查 `sources/` 中的现有结果以避免重复 API 调用

---

## 环境设置

```bash
# 必需：设置您的 Parallel API 密钥
export PARALLEL_API_KEY="your_api_key_here"

# 必需的 Python 包
pip install openai        # 用于 Chat API（搜索/研究）
pip install parallel-web  # 用于 Extract API（仅验证）
```

在 https://platform.parallel.ai 获取您的 API 密钥

---

## 错误处理

脚本优雅地处理错误并返回结构化的错误响应：

```json
{
  "success": false,
  "error": "Error description",
  "timestamp": "2025-02-14 12:00:00"
}
```

**常见问题**：
- `PARALLEL_API_KEY not set`：设置环境变量
- `openai not installed`：运行 `pip install openai`
- `parallel-web not installed`：运行 `pip install parallel-web`（仅提取需要）
- `Rate limit exceeded`：等待并重试（默认：Chat API 为 300 次请求/分钟）

---

## 互补技能

| 技能 | 用途 |
|-------|---------|
| `research-lookup` | 学术论文搜索（将学术查询路由到 Perplexity） |
| `citation-management` | Google Scholar、PubMed、CrossRef 数据库搜索 |
| `literature-review` | 跨学术数据库的系统文献综述 |
| `scientific-schematics` | 从研究结果生成图表 |