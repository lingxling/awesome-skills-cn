---
name: Firecrawl Automation
description: "通过 Composio Firecrawl 集成自动化网页抓取与数据提取 -- 抓取页面、爬取站点、提取结构化数据、批量抓取 URL，并绘制网站结构图。"
requires:
  mcp:
    - rube
---

# Firecrawl Automation

直接从 Claude Code 运行 **Firecrawl** 的网页爬取与提取功能。抓取单个页面、爬取整个站点、用 AI 提取结构化数据、批量处理 URL 列表，并绘制网站结构图，无需离开终端。

**工具包文档：** [composio.dev/toolkits/firecrawl](https://composio.dev/toolkits/firecrawl)

---

## 设置

1. 将 Composio MCP 服务器添加到你的配置中：
   ```
   https://rube.app/mcp
   ```
2. 按提示连接你的 Firecrawl 账户。代理会提供一个身份验证链接。
3. 注意信用额度消耗 -- 严格限定爬取范围，并先在小规模 URL 集合上测试，再扩大规模。

---

## 核心工作流

### 1. 抓取单个页面

以多种格式获取 URL 内容，并可对动态页面附加浏览器操作。

**工具：** `FIRECRAWL_SCRAPE`

关键参数：
- `url`（必填）-- 要抓取的完整 URL
- `formats` -- 输出格式：`markdown`（默认）、`html`、`rawHtml`、`links`、`screenshot`、`json`
- `onlyMainContent`（默认 true）-- 仅提取主要内容，排除导航/页脚/广告
- `waitFor` -- 等待 JS 渲染的毫秒数（默认 0）
- `timeout` -- 最大等待毫秒数（默认 30000）
- `actions` -- 抓取前的浏览器操作（点击、输入、等待、按键、滚动）
- `includeTags` / `excludeTags` -- 按 HTML 标签过滤
- `jsonOptions` -- 配合 `schema` 和/或 `prompt` 进行结构化提取

示例提示：*"以 markdown 格式抓取 https://example.com/pricing 的主要内容"*

---

### 2. 爬取整个站点

从网站发现并抓取多个页面，可配置深度、路径过滤器和并发数。

**工具：** `FIRECRAWL_CRAWL_V2`

关键参数：
- `url`（必填）-- 爬取的起始 URL
- `limit`（默认 10）-- 最多爬取的页面数
- `maxDiscoveryDepth` -- 相对根页面的深度限制
- `includePaths` / `excludePaths` -- URL 路径的正则表达式模式
- `allowSubdomains` -- 是否包含子域名（默认 false）
- `crawlEntireDomain` -- 跟随同级/父级链接，而不仅是子链接（默认 false）
- `sitemap` -- `include`（默认）、`skip` 或 `only`
- `prompt` -- 用自然语言自动配置爬取设置
- `scrapeOptions_formats` -- 每个页面的输出格式
- `scrapeOptions_onlyMainContent` -- 每个页面的主要内容提取

示例提示：*"爬取 firecrawl.dev 的文档部分，最多 50 页，仅限路径匹配 docs 的页面"*

---

### 3. 提取结构化数据

使用自然语言提示或 JSON Schema，借助 AI 从网页中提取结构化 JSON 数据。

**工具：** `FIRECRAWL_EXTRACT`

关键参数：
- `urls`（必填）-- 要提取的 URL 数组（beta 阶段最多 10 个）。支持通配符，如 `https://example.com/blog/*`
- `prompt` -- 要提取内容的自然语言描述
- `schema` -- 定义期望输出结构的 JSON Schema
- `enable_web_search` -- 是否允许爬取初始域名之外的链接（默认 false）

`prompt` 或 `schema` 必须至少提供一个。

使用返回的任务 `id`，通过 `FIRECRAWL_EXTRACT_GET` 检查提取状态。

示例提示：*"从 https://example.com/pricing 提取公司名称、定价档次和功能列表"*

---

### 4. 批量抓取多个 URL

使用共享配置并发抓取多个 URL，实现高效的批量数据采集。

**工具：** `FIRECRAWL_BATCH_SCRAPE`

关键参数：
- `urls`（必填）-- 要抓取的 URL 数组
- `formats` -- 所有页面的输出格式（默认 `markdown`）
- `onlyMainContent`（默认 true）-- 主要内容提取
- `maxConcurrency` -- 并行抓取限制
- `ignoreInvalidURLs`（默认 true）-- 跳过无效 URL，而不是使整个批次失败
- `location` -- 带 `country` 代码的地理位置设置
- `actions` -- 应用于每个页面的浏览器操作
- `blockAds`（默认 true）-- 屏蔽广告

示例提示：*"批量抓取这 20 个产品页面 URL，以 markdown 格式输出并开启广告屏蔽"*

---

### 5. 绘制网站结构图

从起始 URL 发现网站上的所有 URL，有助于规划爬取或审计站点结构。

**工具：** `FIRECRAWL_MAP_MULTIPLE_URLS_BASED_ON_OPTIONS`

关键参数：
- `url`（必填）-- 起始 URL（必须是 `https://` 或 `http://`）
- `search` -- 引导 URL 发现聚焦于特定页面类型
- `limit`（默认 5000，最大 100000）-- 最多返回的 URL 数量
- `includeSubdomains`（默认 true）-- 是否包含子域名
- `ignoreQueryParameters`（默认 true）-- 对仅查询参数不同的 URL 去重
- `sitemap` -- `include`、`skip` 或 `only`

示例提示：*"绘制 docs.example.com 上的所有 URL，重点关注 API 参考页面"*

---

### 6. 监控与管理爬取任务

跟踪爬取进度、获取结果，并取消失控的任务。

**工具：** `FIRECRAWL_CRAWL_GET`、`FIRECRAWL_GET_THE_STATUS_OF_A_CRAWL_JOB`、`FIRECRAWL_CANCEL_A_CRAWL_JOB`

- `FIRECRAWL_CRAWL_GET` -- 获取状态、进度、已用信用额度以及已爬取的页面数据
- `FIRECRAWL_CANCEL_A_CRAWL_JOB` -- 停止一个正在运行或排队中的爬取任务

两者都需要爬取创建时返回的任务 `id`（UUID）。

示例提示：*"查看爬取任务 019b0806-b7a1-7652-94c1-e865b5d2e89a 的状态"*

---

## 常见陷阱

- **速率限制：** Firecrawl 可能触发 "Rate limit exceeded" 错误（429）。优先使用 `FIRECRAWL_BATCH_SCRAPE` 而不是多次单独调用 `FIRECRAWL_SCRAPE`，并对 429/5xx 响应实现退避重试。
- **信用额度消耗：** `FIRECRAWL_EXTRACT` 可能因 "Insufficient credits" 而失败。严格限定范围，避免使用会产生稀疏字段的宽泛首页 URL。先在小规模 URL 集合上测试。
- **嵌套的错误响应：** 即使外层 API 调用成功，单页失败也可能嵌套在 `response.data.code` 中（例如 `SCRAPE_DNS_RESOLUTION_ERROR`）。始终校验内层的状态/错误字段。
- **JS 密集型页面：** 未渲染的抓取可能遗漏关键内容。对动态页面使用 `waitFor`（例如 1000-5000ms），或配置 `scrapeOptions_actions` 在抓取前与页面交互。
- **提取 schema 的精确性：** 模糊或不断变化的 schema/提示会产生嘈杂、不一致的输出。先固定你的 schema，在小样本上测试后再扩展到大量 URL。
- **爬取任务是异步的：** `FIRECRAWL_CRAWL_V2` 会立即返回一个任务 ID。使用 `FIRECRAWL_CRAWL_GET` 轮询结果。用 `FIRECRAWL_CANCEL_A_CRAWL_JOB` 取消卡住的爬取以避免浪费信用额度。
- **提取任务轮询：** 对于较大的任务，`FIRECRAWL_EXTRACT` 同样是异步的。使用 `FIRECRAWL_EXTRACT_GET` 获取最终输出。
- **提取的 URL 批量大小：** 将提取的 URL 批次保持小规模（约 10 个），以避免 429 速率限制错误。
- **深层嵌套的响应：** 结果通常嵌套在 `data.data` 或更深层级中。检查返回的结构，而不要假设是扁平的键。

---

## 快速参考

| 工具标识 | 说明 |
|---|---|
| `FIRECRAWL_SCRAPE` | 带格式/操作选项地抓取单个 URL |
| `FIRECRAWL_CRAWL_V2` | 带深度/路径控制地爬取网站 |
| `FIRECRAWL_EXTRACT` | 用 AI 提示/schema 提取结构化数据 |
| `FIRECRAWL_BATCH_SCRAPE` | 并发批量抓取多个 URL |
| `FIRECRAWL_MAP_MULTIPLE_URLS_BASED_ON_OPTIONS` | 发现/绘制站点上的所有 URL |
| `FIRECRAWL_CRAWL_GET` | 获取爬取任务状态及结果 |
| `FIRECRAWL_GET_THE_STATUS_OF_A_CRAWL_JOB` | 检查爬取任务进度 |
| `FIRECRAWL_CANCEL_A_CRAWL_JOB` | 取消正在运行的爬取任务 |
| `FIRECRAWL_EXTRACT_GET` | 获取提取任务状态及结果 |
| `FIRECRAWL_CRAWL_PARAMS_PREVIEW` | 在开始前预览爬取参数 |
| `FIRECRAWL_SEARCH` | 网络搜索 + 抓取排名靠前的结果 |

---

*由 [Composio](https://composio.dev) 提供支持*
