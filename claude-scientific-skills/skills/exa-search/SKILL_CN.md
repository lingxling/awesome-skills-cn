---
name: exa-search
description: "使用Exa搜索科学和技术类网络内容，并批量从URL中提取页面或PDF文本。支持使用出版物类别和学术领域过滤器进行学术发现。适用于搜索网络、查询当前研究、获取一个页面，或使用Exa提取文章的请求。"
compatibility: Requires Python 3.11+, exa-py>=2.23.0,<3, an EXA_API_KEY, and internet access.
license: MIT
metadata:
  version: "1.4"
  last-reviewed: "2026-09-30"
  skill-author: Exa
  website: https://exa.ai
  docs: https://exa.ai/docs
  openclaw:
    primaryEnv: EXA_API_KEY
    envVars:
    - name: EXA_API_KEY
      required: true
      description: Exa search API key.
---

# Exa Web Toolkit

一个用于网络驱动研究任务的工具，由[Exa](https://exa.ai)提供支持：网页搜索和URL提取。Exa的索引结合了高质量的关键词检索和语义检索，使其非常适合科学、技术和概念性查询。

## 路由——选择正确的功能

阅读用户的请求，并将其与下面的某个功能匹配。在运行命令之前，阅读相应的参考文件以获取详细说明。

| 用户想要... | 功能 | 位置 |
|---|---|---|
| 查找信息、研究某个主题、获取当前信息 | **网页搜索** | `references/web-search.md` |
| 从特定URL获取内容（网页、文章、PDF） | **网页提取** | `references/web-extract.md` |
| 安装或认证 | **设置** | 下方 |

### 决策指南

- **默认使用网页搜索**，用于主题查找、研究问题或"什么是X？"类查询。当主题是科学或技术类时，传入 `--category publication` 以偏向学术来源，和/或使用学术性的 `--include-domains` 白名单。有关两遍学术策略，请参见 `references/web-search.md`。
- **使用网页提取**，当用户提供了URL或要求你读取/获取特定页面时。对于批量提取（一次调用多个URL）和学术PDF，优先使用此功能而非内置的WebFetch。

### 学术来源优先

对于技术或科学查询，优先选择学术和科学来源：
- 同行评审的期刊文章和会议论文优于博客文章或新闻
- 当无法获取同行评审版本时，使用预印本（arXiv、bioRxiv、medRxiv）
- 机构和政府来源（NIH、WHO、NASA、NIST）优于商业网站
- 一手研究优于二手综述

两个控制杆可以引导Exa偏向学术内容：
1. `--category publication` 使检索偏向学术来源。
2. 使用一个学术白名单（arxiv.org、nature.com、pubmed.ncbi.nlm.nih.gov等）的 `--include-domains` 来限制域名池。

结合两者可以缩小来源范围；在每个来源上核实出版物类型和同行评审状态。完整模式请参见 `references/web-search.md`。

在引用学术来源时，除了标准引用格式外，尽可能包含作者姓名和出版年份（例如，[Smith et al., 2025](url)）。如果存在DOI，优先使用DOI链接。

---

## 设置

此技能使用[`exa-py`](https://github.com/exa-labs/exa-py) Python SDK。`scripts/`中的脚本通过PEP 723内联元数据声明其依赖项，因此你可以直接用 `uv run` 运行它们，无需单独的安装步骤：

```bash
uv run "$SKILL_PATH/scripts/exa_search.py" --help
```

如果你希望进行持久化安装：

```bash
uv pip install "exa-py>=2.23.0,<3"
```

### 认证

所有命令都从 `EXA_API_KEY` 环境变量读取API密钥。在[dashboard.exa.ai/api-keys](https://dashboard.exa.ai/api-keys)获取你的Exa API密钥。

首先，检查项目根目录中是否存在包含 `EXA_API_KEY` 的 `.env` 文件。如果存在，加载它：

```bash
dotenv -f .env run -- uv run "$SKILL_PATH/scripts/exa_search.py" "your query"
```

如果 `dotenv` 不可用，安装它：`uv pip install 'python-dotenv[cli]'`。

如果没有 `.env`，为当前会话导出密钥：

```bash
export EXA_API_KEY="your-key"
```

使用 `--help` 来验证安装和CLI解析情况；这不需要API密钥，也不会验证身份认证。只有在发出一次真实查询时才会检查身份认证。

### 提取限制和新鲜度

提取器每次调用 `POST https://api.exa.ai/contents` 接受1–100个URL，
并导出每个URL的SDK状态（`id`、`status`、`source`）。它会拒绝更大
批次的请求。使用 `--max-age-hours 0` 来请求最新内容，使用 `-1`
来仅使用缓存，或使用一个最高为720小时的正数值。省略该参数会使用
Exa的缓存/回退策略。`published_date` 是估计的发表元数据，不是
检索时间。经过测试的SDK会丢弃逐URL的错误细节，因此报告失败时不要
杜撰原因。参见[URL提取](references/web-extract.md)。

### 已验证的API和SDK范围

于2026-09-30审查了[Search API](https://exa.ai/docs/reference/search)、
[Contents API](https://exa.ai/docs/reference/get-contents)，以及
[Exa变更日志](https://exa.ai/docs/changelog)。两个路由都使用JSON
POST请求和 `x-api-key` 身份认证（SDK会设置此标头）。搜索接口是
`POST https://api.exa.ai/search`；其SDK参数使用snake_case命名，
并会被序列化为camelCase。当前的学术类别是 `publication`；
`research paper` 在这个封装层中是一个兼容性别名。这些端点没有
文档记录的offset或cursor分页方式。

辅助工具已使用 `exa-py==2.23.0` 进行测试，包括通过真实SDK进行的
模拟HTTP传输测试。搜索内容标志是显式的：不传任何标志意味着只返回
元数据；`--highlights` 不会隐式地获取文本。下面以及参考文件中已
认证的搜索/提取示例均为示意性内容；本次审查中未进行任何付费的
实时调用。

### 追踪标头

此技能中的每个脚本都会将 `x-exa-integration` 请求标头设置为 `k-dense-ai--scientific-agent-skills`，以便Exa可以将来自K-Dense AI scientific-agent-skills仓库的使用情况归因于此集成。在修改脚本时，请勿删除或重命名此标头。

---

## 此技能中的文件

- `SKILL.md`——本文件（路由和设置）
- `references/web-search.md`——包含学术策略的详细网页搜索参考
- `references/web-extract.md`——URL内容提取参考
- `scripts/exa_search.py`——围绕 `client.search` 的CLI包装器
- `scripts/exa_extract.py`——围绕 `client.get_contents` 的CLI包装器
