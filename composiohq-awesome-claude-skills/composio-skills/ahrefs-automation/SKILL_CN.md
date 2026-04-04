---
name: Ahrefs Automation
description: "使用 Ahrefs 自动化 SEO 研究 -- 分析反向链接配置文件、研究关键词、跟踪域名指标历史、审计自然排名，并通过 Composio Ahrefs 集成执行批量 URL 分析。"
requires:
  mcp:
    - rube
---

# Ahrefs 自动化

直接从 Claude Code 运行 **Ahrefs** SEO 分析。分析反向链接配置文件、研究关键词、跟踪域名权威随时间的变化、审计自然关键词排名，并批量分析多个 URL，无需离开终端。

**工具包文档:** [composio.dev/toolkits/ahrefs](https://composio.dev/toolkits/ahrefs)

---

## 设置

1. 将 Composio MCP 服务器添加到您的配置：
   ```
   https://rube.app/mcp
   ```
2. 在提示时连接您的 Ahrefs 账户。代理将提供身份验证链接。
3. 大多数工具需要 `target`（域名或 URL）和 `country` 代码（ISO 3166-1 alpha-2）。有些还需要 `YYYY-MM-DD` 格式的 `date`。

---

## 核心工作流

### 1. 站点浏览器指标

检索域名的综合 SEO 指标，包括反向链接数量、引用域名、自然关键词排名和流量估算。

**工具：** `AHREFS_RETRIEVE_SITE_EXPLORER_METRICS`

**关键参数：**
- `target`（必需）-- 要分析的域名或 URL
- `date`（必需）-- `YYYY-MM-DD` 格式的指标日期
- `country` -- ISO 国家代码（例如 `us`、`gb`、`de`）
- `mode` -- 范围：`exact`、`prefix`、`domain` 或 `subdomains`（默认）
- `protocol` -- `both`、`http` 或 `https`
- `volume_mode` -- `monthly` 或 `average`

**示例提示：** *"获取今天美国的 example.com 的 Ahrefs 站点指标"*

---

### 2. 历史指标跟踪

跟踪域名的 SEO 指标随时间的变化，用于趋势分析和竞争基准测试。

**工具：** `AHREFS_RETRIEVE_SITE_EXPLORER_METRICS_HISTORY`、`AHREFS_DOMAIN_RATING_HISTORY`

**对于完整的指标历史：**
- `target`（必需）-- 要跟踪的域名
- `date_from`（必需）-- `YYYY-MM-DD` 格式的开始日期
- `date_to` -- 结束日期
- `history_grouping` -- `daily`、`weekly` 或 `monthly`（默认）
- `select` -- 列，如 `date,org_cost,org_traffic,paid_cost,paid_traffic`

**对于域名评级（DR）历史：**
- `target`（必需）、`date_from`（必需）、`date_to`、`history_grouping`

**示例提示：** *"显示过去一年 example.com 的月度域名评级历史"*

---

### 3. 反向链接分析

检索完整的反向链接列表，包括源 URL、锚文本、链接属性和引用域名指标。

**工具：** `AHREFS_FETCH_ALL_BACKLINKS`

**关键参数：**
- `target`（必需）-- 域名或 URL
- `select`（必需）-- 逗号分隔的列（例如 `url_from,url_to,anchor,domain_rating_source,first_seen_link`）
- `limit`（默认 1000）-- 结果数量
- `aggregation` -- `similar_links`（默认）、`1_per_domain` 或 `all`
- `mode` -- `exact`、`prefix`、`domain` 或 `subdomains`
- `history` -- `live`、`since:YYYY-MM-DD` 或 `all_time`
- `where` -- 列上的丰富过滤表达式，如 `is_dofollow`、`domain_rating_source`、`anchor`

**示例提示：** *"获取指向 example.com 的前 100 个 dofollow 反向链接，包含锚文本和引用 DR"*

---

### 4. 关键词研究

获取关键词概览指标并发现匹配的关键词变体，用于内容策略。

**工具：** `AHREFS_EXPLORE_KEYWORDS_OVERVIEW`、`AHREFS_EXPLORE_MATCHING_TERMS_FOR_KEYWORDS`

**对于关键词概览：**
- `select`（必需）-- 要返回的列（volume、difficulty、CPC 等）
- `country`（必需）-- ISO 国家代码
- `keywords` -- 逗号分隔的关键词列表
- `where` -- 按流量、难度、意图等过滤

**对于匹配词：**
- `select`（必需）和 `country`（必需）
- `keywords` -- 逗号分隔的种子关键词
- `match_mode` -- `terms`（任意顺序）或 `phrase`（精确顺序）
- `terms` -- `all` 或 `questions`（仅问题格式关键词）

**示例提示：** *"在美国查找具有流量和难度的'项目管理'关键词变体"*

---

### 5. 自然关键词审计

查看域名在自然搜索中的关键词排名，包含位置跟踪和历史比较。

**工具：** `AHREFS_RETRIEVE_ORGANIC_KEYWORDS`

**关键参数：**
- `target`（必需）-- 域名或 URL
- `country`（必需）-- ISO 国家代码
- `date`（必需）-- `YYYY-MM-DD` 格式的日期
- `select` -- 要返回的列（keyword、position、volume、traffic、URL 等）
- `date_compared` -- 与之前的日期比较
- `where` -- `keyword`、`volume`、`best_position`、意图标志等上的丰富过滤表达式
- `limit`（默认 1000）、`order_by`

**示例提示：** *"显示 example.com 在美国排名前 10 的所有自然关键词"*

---

### 6. 批量 URL 分析

同时分析多达 100 个 URL 或域名，以比较竞争对手或网站部分之间的 SEO 指标。

**工具：** `AHREFS_BATCH_URL_ANALYSIS`

**关键参数：**
- `targets`（必需）-- 包含 `url`、`mode`（`exact`/`prefix`/`domain`/`subdomains`）和 `protocol`（`both`/`http`/`https`）的对象数组
- `select`（必需）-- 列标识符数组
- `country` -- ISO 国家代码
- `output` -- `json` 或 `php`

**示例提示：** *"比较 competitor1.com、competitor2.com 和 competitor3.com 的 SEO 指标"*

---

## 已知陷阱

- **列选择是必需的：** 大多数 Ahrefs 工具需要 `select` 参数指定要返回的列。省略它或使用无效的列名将导致错误。请参阅每个工具的响应架构以获取有效的标识符。
- **日期格式一致性：** 日期必须采用 `YYYY-MM-DD` 格式。某些历史端点按照 `history_grouping` 设置的粒度返回数据，而不是按确切日期。
- **API 单位成本不同：** 不同的列消耗不同的单位数量。架构中标记为"(5 units)"或"(10 units)"的列更昂贵。在请求昂贵的列（如 `traffic`、`refdomains_source` 或 `difficulty`）时，请监控 API 使用情况。
- **批量限制为 100 个目标：** `AHREFS_BATCH_URL_ANALYSIS` 每个请求最多接受 100 个目标。对于更大的分析，请拆分为多个批次。
- **过滤表达式很复杂：** `where` 参数使用 Ahrefs 的过滤表达式语法，而不是标准 SQL。请参阅每个工具架构中的列描述以获取支持的过滤类型和值格式。
- **已弃用的 offset 参数：** `offset` 参数于 2024 年 5 月 31 日被弃用。请使用基于游标的分页或调整 `limit`。
- **模式显著影响范围：** 将 `mode` 设置为 `subdomains`（默认）包括所有子域，与 `domain` 或 `exact` 相比，这可能会急剧增加结果数量。

---

## 快速参考

| 工具标识符 | 描述 |
|---|---|
| `AHREFS_RETRIEVE_SITE_EXPLORER_METRICS` | 域名/URL 的当前 SEO 指标 |
| `AHREFS_RETRIEVE_SITE_EXPLORER_METRICS_HISTORY` | 随时间变化的 SEO 指标历史 |
| `AHREFS_DOMAIN_RATING_HISTORY` | 域名评级（DR）历史 |
| `AHREFS_FETCH_ALL_BACKLINKS` | 带过滤的完整反向链接列表 |
| `AHREFS_FETCH_SITE_EXPLORER_REFERRING_DOMAINS` | 引用域名列表 |
| `AHREFS_GET_SITE_EXPLORER_COUNTRY_METRICS` | 国家级别的流量细分 |
| `AHREFS_BATCH_URL_ANALYSIS` | 多达 100 个 URL 的批量分析 |
| `AHREFS_EXPLORE_KEYWORDS_OVERVIEW` | 关键词指标概览 |
| `AHREFS_EXPLORE_MATCHING_TERMS_FOR_KEYWORDS` | 匹配的关键词变体 |
| `AHREFS_EXPLORE_KEYWORD_VOLUME_BY_COUNTRY` | 各国的关键词流量 |
| `AHREFS_RETRIEVE_ORGANIC_KEYWORDS` | 域名的自然关键词排名 |
| `AHREFS_RETRIEVE_SITE_EXPLORER_KEYWORDS_HISTORY` | 历史关键词排名数据 |
| `AHREFS_RETRIEVE_TOP_PAGES_FROM_SITE_EXPLORER` | 按 SEO 指标排名靠前的页面 |
| `AHREFS_GET_SERP_OVERVIEW` | 特定关键词的 SERP 概览 |

---

*由 [Composio](https://composio.dev) 提供支持*
