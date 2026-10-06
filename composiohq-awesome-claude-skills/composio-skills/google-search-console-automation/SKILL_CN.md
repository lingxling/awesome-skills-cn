---
name: google-search-console-automation
description: "通过 Rube MCP（Composio）自动化 Google Search Console 任务：查询搜索分析数据、列出网站、检查 URL、提交站点地图、监控搜索表现。请始终先搜索工具以获取最新的模式定义。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 实现 Google Search Console 自动化

通过 Rube MCP（Composio）使用 Google Search Console 查询搜索分析数据、检查 URL、管理站点地图并监控搜索表现。

**工具包文档**：[composio.dev/toolkits/google_search_console](https://composio.dev/toolkits/google_search_console)

## 前置条件
- 必须已连接 Rube MCP（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 对工具包 `google_search_console` 建立活跃连接
- 在 Google Search Console 中拥有已验证的站点所有权或相应权限
- 始终先调用 `RUBE_SEARCH_TOOLS` 以获取最新的工具模式

## 设置
**获取 Rube MCP**：在你的客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——只需添加该端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 是否可用
2. 对工具包 `google_search_console` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接未处于 ACTIVE 状态，按返回的身份验证链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

## 核心工作流

### 1. 列出所有已验证的网站
使用 `GOOGLE_SEARCH_CONSOLE_LIST_SITES` 检索已认证用户拥有或有权访问的所有网站。
```
Tool: GOOGLE_SEARCH_CONSOLE_LIST_SITES
Parameters: (none required)
Returns: List of site entries with siteUrl and permissionLevel
```

### 2. 查询搜索分析数据
使用 `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY` 获取搜索表现数据，包括点击量、展示量、点击率和排名位置。
```
Tool: GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY
Parameters:
  - site_url (required): Site URL (e.g., "https://www.example.com/" or "sc-domain:example.com")
  - start_date (required): Start date in YYYY-MM-DD format
  - end_date (required): End date in YYYY-MM-DD format
  - dimensions: Group by ["query", "page", "country", "device", "date", "searchAppearance"]
  - search_type: "web" (default), "image", "video", "news", "discover", "googleNews"
  - dimension_filter_groups: Filters for dimensions (operator: equals, notEquals, contains, notContains, includingRegex, excludingRegex)
  - row_limit: Max rows (1-25000, default 1000)
  - start_row: Pagination offset (default 0)
  - aggregation_type: "auto", "byPage", "byProperty", "byNewsShowcasePanel"
  - data_state: "final" (default), "all", "hourly_all"
```

### 3. 检查某个 URL
使用 `GOOGLE_SEARCH_CONSOLE_INSPECT_URL` 检查特定 URL 的索引状态和问题。
```
Tool: GOOGLE_SEARCH_CONSOLE_INSPECT_URL
Parameters:
  - inspection_url (required): Full URL to inspect (e.g., "https://www.example.com/page")
  - site_url (required): Property URL (e.g., "https://www.example.com/")
  - language_code: BCP-47 language (default: "en-US")
```

### 4. 列出站点地图
使用 `GOOGLE_SEARCH_CONSOLE_LIST_SITEMAPS` 检索某个网站已提交的所有站点地图。
```
Tool: GOOGLE_SEARCH_CONSOLE_LIST_SITEMAPS
Parameters:
  - site_url (required): Site URL (e.g., "https://www.example.com/")
  - sitemap_index: Specific sitemap index URL to list sitemaps from
```

### 5. 提交站点地图
使用 `GOOGLE_SEARCH_CONSOLE_SUBMIT_SITEMAP` 注册或重新提交一个站点地图以供索引。
```
Tool: GOOGLE_SEARCH_CONSOLE_SUBMIT_SITEMAP
Parameters:
  - site_url (required): Site URL or domain property (e.g., "sc-domain:example.com")
  - feedpath (required): Full sitemap URL (e.g., "https://www.example.com/sitemap.xml")
```

### 6. 获取站点地图详情
使用 `GOOGLE_SEARCH_CONSOLE_GET_SITEMAP` 检索某个已提交站点地图的信息。
```
Tool: GOOGLE_SEARCH_CONSOLE_GET_SITEMAP
Parameters:
  - site_url (required): Site URL
  - feedpath (required): Sitemap URL to retrieve details for
```

## 常见模式

- **表现监控**：使用 `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY` 并设置 `dimensions: ["date"]`，在一段日期范围内跟踪每日搜索表现趋势。
- **热门查询报告**：使用 `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY` 并设置 `dimensions: ["query"]`，找出点击量最高的搜索词。
- **页面级分析**：使用 `dimensions: ["page"]` 识别表现最佳的页面，再用 `dimensions: ["query", "page"]` 查看哪些查询为每个页面带来流量。
- **索引审计**：使用 `GOOGLE_SEARCH_CONSOLE_INSPECT_URL` 检查重要页面的索引状态。
- **站点地图管理**：使用 `GOOGLE_SEARCH_CONSOLE_LIST_SITEMAPS` 核实已提交的站点地图，然后用 `GOOGLE_SEARCH_CONSOLE_SUBMIT_SITEMAP` 提交新的或更新后的站点地图。
- **国家/设备细分**：使用 `dimensions: ["country", "device"]` 了解搜索流量的地理和设备类型分布。
- **筛选特定查询**：使用带 `contains` 或 `includingRegex` 操作符的 `dimension_filter_groups`，聚焦于特定关键词组。

## 常见陷阱

- **站点 URL 格式很重要**：URL 前缀类型的属性使用带协议和末尾斜杠的完整 URL（例如 `https://www.example.com/`）。域名属性使用 `sc-domain:` 前缀（例如 `sc-domain:example.com`）。格式错误会返回空结果或报错。
- **日期范围限制**：数据通常会有 2-3 天的延迟。`data_state: "all"` 包含可能仍会变化的更新数据。`hourly_all` 仅适用于最近 3 天内的日期。
- **行数限制与分页**：API 返回按点击量排序的最高结果（按日期分组时则按日期排序）。要获取完整数据，请使用 `start_row` 配合 `row_limit` 进行分页。
- **每次请求最多 25,000 行**：即使分页，每次请求最多也只返回 25,000 行。对于非常大的数据集，请缩小日期范围或添加维度过滤器。
- **检查 URL 必须与站点匹配**：`inspection_url` 必须是 `site_url` 属性下的一个页面。跨属性检查将会失败。
- **站点地图必须可访问**：`GOOGLE_SEARCH_CONSOLE_SUBMIT_SITEMAP` 要求站点地图文件在指定 URL 上可公开访问，并且是正确格式的 XML。
- **结果按点击量排序**：默认情况下，分析结果按点击数降序排列，但按 `date` 分组时例外（此时按日期升序排列）。

## 快速参考
| 操作 | 工具 | 关键参数 |
|--------|------|----------------|
| 列出网站 | `GOOGLE_SEARCH_CONSOLE_LIST_SITES` | (none) |
| 搜索分析 | `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY` | `site_url`, `start_date`, `end_date`, `dimensions` |
| 检查 URL | `GOOGLE_SEARCH_CONSOLE_INSPECT_URL` | `inspection_url`, `site_url` |
| 列出站点地图 | `GOOGLE_SEARCH_CONSOLE_LIST_SITEMAPS` | `site_url` |
| 提交站点地图 | `GOOGLE_SEARCH_CONSOLE_SUBMIT_SITEMAP` | `site_url`, `feedpath` |
| 获取站点地图信息 | `GOOGLE_SEARCH_CONSOLE_GET_SITEMAP` | `site_url`, `feedpath` |

---
*由 [Composio](https://composio.dev) 提供支持*
