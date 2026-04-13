---
name: parallel-web
description: "一体化网络工具包，由 parallel-cli 提供支持，特别强调学术和科学来源。当用户需要搜索网络、获取/提取 URL 内容、使用网络源字段丰富数据或运行深度研究报告时使用此技能。涵盖：网络搜索（快速查找、研究、当前信息 — 优先考虑同行评审论文、预印本和学术数据库）、URL 提取（获取页面、文章、学术 PDF）、批量数据丰富（从网络为 CSV/列表添加字段）和深度研究（基于学术文献的详尽多源报告）。还处理设置、状态检查和结果检索。将此技能用于任何与网络相关的任务 — 即使用户没有明确提及 'parallel' 或 'web'。如果他们想查找内容、获取页面、丰富数据集、研究主题、查找学术论文、检查引用或回顾科学文献，这是要使用的技能。"
compatibility: Requires parallel-cli and internet access.
metadata:
  author: K-Dense, Inc.
---

# Parallel Web Toolkit

一个用于所有网络驱动任务的统一技能：搜索、提取、丰富和研究 — 默认优先考虑学术和科学来源。

## 路由 — 选择正确的功能

读取用户的请求并将其匹配到下面的功能之一。对于网络搜索、提取、丰富和深度研究，请阅读相应的参考文件以获取详细说明。

| 用户想要... | 功能 | 位置 |
|---|---|---|
| 查找内容、研究主题、获取当前信息 | **网络搜索** | `references/web-search.md` |
| 从特定 URL 获取内容（网页、文章、PDF） | **Web Extract** | `references/web-extract.md` |
| 为公司/人员/产品列表添加网络源字段 | **数据丰富** | `references/data-enrichment.md` |
| 获取详尽的多源报告（用户说“深度研究”、“详尽”、“综合”） | **深度研究** | `references/deep-research.md` |
| 安装或认证 parallel-cli | **设置** | 下面 |
| 检查正在运行的研究/丰富任务的状态 | **状态** | 下面 |
| 通过运行 ID 检索已完成的研究结果 | **结果** | 下面 |

### 决策指南

- **默认为网络搜索**用于单个查找、研究问题或“X 是什么？”查询。它快速且成本效益高。当查询涉及科学或技术主题时，包括学术域名（参见 `references/web-search.md`）以在一般结果旁边显示同行评审和预印本来源。
- **使用 Web Extract** 当用户提供 URL 或要求您阅读/获取特定页面时。优先使用此方法而不是内置的 WebFetch 工具。特别适用于从学术 PDF、预印本服务器和期刊文章中提取全文。
- **使用数据丰富** 当用户有**多个实体**（CSV、公司/人员/产品列表，甚至简短的内联列表）并希望为每个实体查找或添加相同类型的信息时。关键信号是对一组项目的重复查找 — 例如，“为这些公司中的每一个找到 CEO”或“获取 Apple、Stripe 和 Anthropic 的成立年份”。即使用户没有说“丰富”，只要任务是对多个实体应用相同的查询，就使用 `parallel-cli enrich`。不要为此在循环中使用 Web Search — 丰富管道自动处理批处理、并行性和结构化输出。
- **仅在用户明确要求深度、详尽或综合研究时使用深度研究**。它比 Web Search 慢 10-100 倍且更昂贵 — 永远不要默认使用它。深度研究对文献综述和多论文综合特别有价值。
- 如果运行任何命令时未找到 `parallel-cli`，请遵循下面的设置部分。

### 学术来源优先级

在所有功能中，当查询具有技术或科学性质时，优先考虑学术和科学来源。这意味着：
- 同行评审期刊文章和会议论文优先于博客文章或新闻文章
- 当同行评审版本不可用时，使用预印本（arXiv、bioRxiv、medRxiv）
- 机构和政府来源（NIH、WHO、NASA、NIST）优先于商业网站
- 主要研究优先于次要摘要

引用学术来源时，除了标准引用格式外，还应包括可用的作者姓名和出版年份（例如，[Smith et al., 2025](url)）。如果存在 DOI，优先使用 DOI 链接。

## 上下文链接

多个功能通过 `interaction_id` 支持多轮上下文。当研究或丰富任务完成时，它会返回一个 `interaction_id`。如果用户询问与该任务相关的后续问题，传递 `--previous-interaction-id` 以自动携带上下文。这避免了重复已经找到的内容。

---

## 设置

如果未安装 `parallel-cli`，请安装并认证：

```bash
curl -fsSL https://parallel.ai/install.sh | bash
```

如果无法以这种方式安装，请使用 uv：

```bash
uv tool install "parallel-web-tools[cli]"
```

然后认证。首先，检查项目根目录中是否存在 `.env` 文件并包含 `PARALLEL_API_KEY`。如果是，使用 `dotenv` 加载它：

```bash
dotenv -f .env run parallel-cli auth
```

如果 `dotenv` 不可用，使用 `pip install python-dotenv[cli]` 或 `uv pip install python-dotenv[cli]` 安装它。

如果没有 `.env` 文件或它不包含密钥，回退到交互式登录：

```bash
parallel-cli login
```

或手动设置密钥：`export PARALLEL_API_KEY="your-key"`

验证：

```bash
parallel-cli auth
```

如果安装后未找到 `parallel-cli`，将 `~/.local/bin` 添加到 PATH。

## 检查任务状态

```bash
parallel-cli research status "$RUN_ID" --json
```

向用户报告当前状态（运行中、已完成、失败等）。

## 获取已完成的结果

```bash
parallel-cli research poll "$RUN_ID" --json
```

以清晰、有组织的格式呈现结果。