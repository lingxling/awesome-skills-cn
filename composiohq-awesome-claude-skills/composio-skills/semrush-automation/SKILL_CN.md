---
name: SEMrush Automation
description: "通过 SEMrush 自动化 SEO 分析 -- 研究关键词、分析域名自然排名、审查反向链接、评估关键词难度，并通过 Composio SEMrush 集成发现相关词汇。"
requires:
  mcp:
    - rube
---

# SEMrush Automation

直接从 Claude Code 运行 **SEMrush** SEO 分析。无需离开终端即可分析域名关键词、审查反向链接概况、研究关键词难度、发现相关词汇，并跟踪自然页面表现。

**工具包文档：** [composio.dev/toolkits/semrush](https://composio.dev/toolkits/semrush)

---

## 设置

1. 将 Composio MCP 服务器添加到你的配置中：
   ```
   https://rube.app/mcp
   ```
2. 按提示连接你的 SEMrush 账户。智能体会提供一个身份验证链接。
3. 所有 SEMrush 工具都需要 `database` 参数来指定区域数据库（例如 `us`、`uk`、`de`）。请根据目标受众选择正确的区域。

---

## 核心工作流

### 1. 域名自然关键词分析

获取某个域名的所有自然搜索关键词，包括排名位置、流量估算、CPC 和关键词难度。

**工具：** `SEMRUSH_DOMAIN_ORGANIC_SEARCH_KEYWORDS`

关键参数：
- `domain`（必填）-- 例如 `example.com`
- `database`（必填）-- 区域数据库代码（例如 `us`、`uk`、`de`）
- `display_limit`（默认 10000）和 `display_offset`（默认 0）-- 分页
- `display_sort` -- 按位置、流量、搜索量等排序（例如 `tr_desc` 表示按流量降序）
- `display_date` -- 历史数据，格式为 `YYYYMM15`（月度）或 `YYYYMMDD`（每日）
- `export_columns` -- 指定列，例如 `Ph`（短语）、`Po`（位置）、`Nq`（搜索量）、`Tr`（流量）、`Kd`（难度）
- `display_filter` -- 按特定列筛选

示例提示：*"获取 example.com 在美国数据库中按流量排序的前 100 个自然关键词"*

---

### 2. 关键词概览与批量分析

获取单个关键词的详细指标，或一次分析最多 100 个关键词。

**工具：** `SEMRUSH_KEYWORD_OVERVIEW_ONE_DATABASE`、`SEMRUSH_BATCH_KEYWORD_OVERVIEW`

单个关键词：
- `phrase`（必填）-- 要调查的关键词
- `database`（必填）-- 区域数据库

批量（最多 100 个关键词）：
- `phrase`（必填）-- 用分号分隔的关键词（总字符数最多 255）
- `database`（必填）-- 区域数据库
- `export_columns` -- `Ph`（短语）、`Nq`（搜索量）、`Cp`（CPC）、`Co`（竞争度）、`Kd`（难度）、`In`（意图）

示例提示：*"获取美国数据库中 'seo services;content marketing;link building' 的关键词指标"*

---

### 3. 域名自然页面报告

发现域名中哪些 URL 带来了最多的自然流量和可见度。

**工具：** `SEMRUSH_DOMAIN_ORGANIC_PAGES`

关键参数：
- `domain`（必填）-- 目标域名
- `database`（必填）-- 区域数据库
- `display_sort` -- 例如 `pc_desc` 表示按流量占比降序
- `display_limit` 和 `display_offset` -- 分页
- `export_columns` -- `Ur`（URL）、`Pc`（流量占比）、`Tg`（流量）、`Tr`（流量成本）

示例提示：*"显示 example.com 按流量占比排名的前 50 个自然页面"*

---

### 4. 反向链接概况总览

获取某个域名的反向链接摘要，包括权威分数（Authority Score）、链接类型和引用域名数量。

**工具：** `SEMRUSH_BACKLINKS_OVERVIEW`

关键参数：
- `target`（必填）-- 域名、子域名或完整 URL
- `target_type`（必填）-- `root_domain`、`domain` 或 `url`
- `export_columns` -- `ascore`（权威分数）、`total`（反向链接总数）、`domains_num`（引用域名数）、`follows_num`、`nofollows_num` 等

示例提示：*"获取 example.com 的反向链接概览，包括权威分数和引用域名数量"*

---

### 5. 关键词难度评估

对特定关键词进入前 10 名的难度进行打分（0-100 分）。

**工具：** `SEMRUSH_KEYWORD_DIFFICULTY`

关键参数：
- `phrase`（必填）-- 要分析的关键词
- `database`（必填）-- 区域数据库
- `export_columns` -- `Ph`（短语）、`Kd`（难度分数）

示例提示：*"'best project management software' 在美国的关键词难度是多少？"*

---

### 6. 发现相关关键词

为种子关键词找到同义词、变体和相关词汇，以扩展你的内容策略。

**工具：** `SEMRUSH_RELATED_KEYWORDS`

关键参数：
- `phrase`（必填）-- 种子关键词
- `database`（必填）-- 区域数据库
- `display_limit`（默认 10000）-- 最大结果数
- `display_sort` -- 例如 `nq_desc` 表示按搜索量降序，`kd_asc` 表示难度从易到难
- `export_columns` -- `Ph`、`Nq`、`Kd`、`Cp`、`Co`、`Rr`（相关度分数）

示例提示：*"查找 'project management' 的相关关键词，按搜索量排序"*

---

## 常见陷阱

- **分页是必不可少的：** `SEMRUSH_DOMAIN_ORGANIC_SEARCH_KEYWORDS` 和 `SEMRUSH_DOMAIN_ORGANIC_PAGES` 可能返回非常大的数据集。始终使用 `display_limit` 和 `display_offset`，不要假设单页数据就是完整的。
- **CSV 风格的响应：** 许多 SEMrush 工具会以单个字段中的 CSV 风格文本返回数据（例如 `data/keyword_data`）。在进行分析或联接报告之前，你必须先解析行和列。
- **"ERROR 50 :: NOTHING FOUND"：** 这个字符串字面意思是该域名或关键词在该数据库中没有数据。应将其视为合法的零结果响应，而不是传输错误。
- **批量关键词限制：** 对于存在问题或过大的批量请求，`SEMRUSH_BATCH_KEYWORD_OVERVIEW` 可能返回 HTTP 400（`phrase` 字段总字符数最多 255）。请缩小批量规模，或改用 `SEMRUSH_KEYWORD_OVERVIEW_ONE_DATABASE` 进行单项查询。
- **日期格式：** 月度历史数据必须使用 `YYYYMM15` 格式（例如 `20231015`）。使用不正确的格式会返回意外结果。
- **区域数据库很重要：** 始终为目标受众使用正确的区域数据库。`us` 与 `uk` 的结果在搜索量、CPC 和排名上可能有显著差异。
- **列代码：** 导出列使用简短代码（`Ph`、`Nq`、`Kd` 等）。避免过度收窄 `export_columns`，以保留流量、CPC、排名和难度等关键指标。

---

## 快速参考

| 工具 Slug | 描述 |
|---|---|
| `SEMRUSH_DOMAIN_ORGANIC_SEARCH_KEYWORDS` | 域名的自然关键词，包含排名位置和流量 |
| `SEMRUSH_KEYWORD_OVERVIEW_ONE_DATABASE` | 单个关键词指标（搜索量、CPC、难度） |
| `SEMRUSH_BATCH_KEYWORD_OVERVIEW` | 最多 100 个关键词的批量指标 |
| `SEMRUSH_DOMAIN_ORGANIC_PAGES` | 域名按流量排名的热门自然页面 |
| `SEMRUSH_BACKLINKS_OVERVIEW` | 带权威分数的反向链接概况摘要 |
| `SEMRUSH_BACKLINKS` | 目标的详细反向链接列表 |
| `SEMRUSH_KEYWORD_DIFFICULTY` | 关键词难度分数（0-100） |
| `SEMRUSH_RELATED_KEYWORDS` | 种子短语的相关/相似关键词 |
| `SEMRUSH_CATEGORIES` | 带置信度评级的域名分类 |
| `SEMRUSH_DOMAIN_ORGANIC_SUBDOMAINS` | 子域名级别的自然排名细分 |

---

*由 [Composio](https://composio.dev) 提供支持*
