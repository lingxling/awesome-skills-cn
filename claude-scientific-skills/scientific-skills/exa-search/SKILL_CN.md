---
name: exa-search
description: "由 Exa 驱动的网络工具包，针对科学和技术内容进行了优化。当用户需要搜索网页或获取/提取 URL 内容时使用此技能。涵盖：网页搜索（语义查找、研究、当前信息——可选研究论文类别和学术领域过滤）和 URL 提取（批量获取页面、文章、学术 PDF）。当用户需要高质量搜索或通过 category=research paper 进行学术过滤时，使用此技能进行与网页相关的任务。触发条件：搜索、查找、获取页面或提取文章的请求。"
compatibility: Requires exa-py Python SDK, an EXA_API_KEY, and internet access.
license: MIT
metadata:
  skill-author: Exa
  website: https://exa.ai
  docs: https://exa.ai/docs
---

# Exa Web Toolkit

一个用于网络驱动研究任务的工具，由 [Exa](https://exa.ai) 提供支持：网页搜索和 URL 提取。Exa 的索引结合了高质量的关键词和语义检索，使其非常适合科学、技术和概念性查询。

## 路由 —— 选择正确的功能

阅读用户的请求，并将其与下面的某个功能进行匹配。在运行命令之前，阅读相应的参考文件以获取详细说明。

| 用户想要... | 功能 | 位置 |
|---|---|---|
| 查找信息、研究某个主题、获取当前信息 | **网页搜索** | `references/web-search.md` |
| 从特定 URL 获取内容（网页、文章、PDF） | **网页提取** | `references/web-extract.md` |
| 安装或认证 | **设置** | 下方 |

### 决策指南

- **默认使用网页搜索** 进行主题查找、研究问题或 "什么是 X？" 类查询。当主题是科学或技术类时，传递 `--category "research paper"` 以偏向学术来源，和/或使用学术 `--include-domains` 白名单。有关两遍学术策略，请参见 `references/web-search.md`。
- **使用网页提取** 当用户提供 URL 或要求你读取/获取特定页面时。对于批量提取（一次调用多个 URL）和学术 PDF，优先使用此功能而非内置的 WebFetch。

### 学术来源优先

对于技术或科学查询，优先选择学术和科学来源：
- 同行评审的期刊文章和会议论文优于博客文章或新闻
- 预印本（arXiv、bioRxiv、medRxiv）在无法获取同行评审版本时使用
- 机构和政府来源（NIH、WHO、NASA、NIST）优于商业网站
- 一手研究优于二手综述

两个控制杆可引导 Exa 偏向学术内容：
1. `--category "research paper"` 使检索偏向学术来源。
2. 使用学术白名单（arxiv.org、nature.com、pubmed.ncbi.nlm.nih.gov 等）的 `--include-domains` 限制域名池。

结合两者可获得严格的学术结果。完整模式请参见 `references/web-search.md`。

引用学术来源时，在标准引用格式之外，尽可能包含作者姓名和出版年份（例如，[Smith et al., 2025](url)）。如果存在 DOI，优先使用 DOI 链接。

---

## 设置

此技能使用 [`exa-py`](https://github.com/exa-labs/exa-py) Python SDK。`scripts/` 中的脚本通过 PEP 723 内联元数据声明其依赖项，因此你可以直接使用 `uv run` 运行它们，无需单独的安装步骤：

```bash
uv run --with exa-py python "$SKILL_PATH/scripts/exa_search.py" --help
```

如果你希望进行持久化安装：

```bash
uv pip install "exa-py>=1.14.0"
```

### 认证

所有命令都从 `EXA_API_KEY` 环境变量读取 API 密钥。在 [dashboard.exa.ai/api-keys](https://dashboard.exa.ai/api-keys) 获取你的 Exa API 密钥。

首先，检查项目根目录中是否存在 `.env` 文件并包含 `EXA_API_KEY`。如果是，加载它：

```bash
dotenv -f .env run -- uv run --with exa-py python "$SKILL_PATH/scripts/exa_search.py" "your query"
```

如果 `dotenv` 不可用，请安装：`pip install python-dotenv[cli]` 或 `uv pip install python-dotenv[cli]`。

如果没有 `.env`，则为当前会话导出密钥：

```bash
export EXA_API_KEY="your-key"
```

通过使用 `--help` 运行任何脚本进行验证 —— 如果密钥已设置，它将干净地退出，并且仅在执行真实查询时才运行认证检查。

### 追踪标头

此技能中的每个脚本都会将 `x-exa-integration` 请求标头设置为 `k-dense-ai--scientific-agent-skills`，以便 Exa 可以将来自 K-Dense AI scientific-agent-skills 仓库的使用归因于此集成。在修改脚本时，请勿删除或重命名此标头。

---

## 此技能中的文件

- `SKILL.md` —— 本文件（路由和设置）
- `references/web-search.md` —— 包含学术策略的详细网页搜索参考
- `references/web-extract.md` —— URL 内容提取参考
- `scripts/exa_search.py` —— `client.search_and_contents` 的 CLI 包装器
- `scripts/exa_extract.py` —— `client.get_contents` 的 CLI 包装器
