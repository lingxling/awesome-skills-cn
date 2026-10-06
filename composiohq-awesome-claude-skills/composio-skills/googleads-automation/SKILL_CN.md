---
name: googleads-automation
description: "通过 Rube MCP（Composio）自动化 Google Ads 分析任务：列出 Google Ads 关联链接、运行 GA4 报告、检查兼容性、列出属性和账户。务必先搜索工具以获取最新的模式定义。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 实现 Google Ads 自动化

通过 Google Analytics 集成访问 Google Ads 数据，运行效果报告，列出已关联的 Ads 账户，并使用 Rube MCP（Composio）分析广告系列指标。

**工具包文档**：[composio.dev/toolkits/googleads](https://composio.dev/toolkits/googleads)

## 前置条件
- 必须已连接 Rube MCP（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 对工具包 `google_analytics` 建立有效连接
- 务必先调用 `RUBE_SEARCH_TOOLS` 以获取最新的工具模式定义

## 设置
**获取 Rube MCP**：将 `https://rube.app/mcp` 作为 MCP 服务器添加到你的客户端配置中。无需 API 密钥——只需添加端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 有响应来验证 Rube MCP 是否可用
2. 对工具包 `google_analytics` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接未处于 ACTIVE 状态，请按返回的身份验证链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

> **注意**：Google Ads 数据是通过 Google Analytics 工具包集成来访问的。以下工具使用与 Google Ads 账户关联的 GA4 属性。

## 核心工作流

### 1. 列出某个属性的 Google Ads 关联链接
使用 `GOOGLE_ANALYTICS_ANALYTICS_ADMIN_PROPERTIES_GOOGLE_ADS` 获取为某个 GA4 属性配置的所有 Google Ads 账户关联链接。
```
Tool: GOOGLE_ANALYTICS_ANALYTICS_ADMIN_PROPERTIES_GOOGLE_ADS
Parameters:
  - parent (required): Property resource name (format: "properties/{propertyId}")
  - pageSize: Max results (1-200, default 50)
  - pageToken: Pagination token
```

### 2. 运行 GA4 效果报告
使用 `GOOGLE_ANALYTICS_RUN_REPORT` 运行带有维度、指标、日期范围和筛选条件的定制报告。
```
Tool: GOOGLE_ANALYTICS_RUN_REPORT
Parameters:
  - property (required): Property resource (format: "properties/{property_id}")
  - dimensions: Array of dimension objects (e.g., [{"name": "sessionCampaignName"}, {"name": "date"}])
  - metrics: Array of metric objects (e.g., [{"name": "sessions"}, {"name": "totalRevenue"}])
  - dateRanges: Array with startDate and endDate (e.g., [{"startDate": "2025-01-01", "endDate": "2025-01-31"}])
  - dimensionFilter: Filter by dimension values
  - metricFilter: Filter by metric values (applied after aggregation)
  - orderBys: Sort results
  - limit: Max rows to return (1-250000)
```

### 3. 检查维度/指标兼容性
使用 `GOOGLE_ANALYTICS_CHECK_COMPATIBILITY` 在运行报告之前验证维度和指标的组合是否兼容。
```
Tool: GOOGLE_ANALYTICS_CHECK_COMPATIBILITY
Description: Validates compatibility of chosen dimensions or metrics
  before running a report.
Note: Call RUBE_SEARCH_TOOLS to get the full schema for this tool.
```

### 4. 列出 GA4 账户
使用 `GOOGLE_ANALYTICS_LIST_ACCOUNTS` 枚举所有可访问的 Google Analytics 账户。
```
Tool: GOOGLE_ANALYTICS_LIST_ACCOUNTS
Parameters:
  - pageSize: Max accounts to return
  - pageToken: Pagination token
  - showDeleted: Include soft-deleted accounts
```

### 5. 列出某个账户下的 GA4 属性
使用 `GOOGLE_ANALYTICS_LIST_PROPERTIES` 列出特定 GA4 账户下的属性。
```
Tool: GOOGLE_ANALYTICS_LIST_PROPERTIES
Parameters:
  - account (required): Account resource name (format: "accounts/{account_id}")
  - pageSize: Max properties (1-200)
  - pageToken: Pagination token
  - showDeleted: Include trashed properties
```

### 6. 获取可用的维度和指标
使用 `GOOGLE_ANALYTICS_GET_METADATA` 发现构建报告时可用的所有字段。
```
Tool: GOOGLE_ANALYTICS_GET_METADATA
Description: Gets metadata for dimensions, metrics, and comparisons
  for a GA4 property.
Note: Call RUBE_SEARCH_TOOLS to get the full schema for this tool.
```

## 常见模式

- **先发现再报告**：使用 `GOOGLE_ANALYTICS_LIST_ACCOUNTS` 找到账户 ID，然后使用 `GOOGLE_ANALYTICS_LIST_PROPERTIES` 找到属性 ID，最后使用 `GOOGLE_ANALYTICS_RUN_REPORT` 拉取数据。
- **查询前先验证**：使用 `GOOGLE_ANALYTICS_CHECK_COMPATIBILITY` 在运行报告前验证维度/指标组合，以避免出现 400 错误。
- **广告系列效果**：使用诸如 `sessionCampaignName`、`sessionSource`、`sessionMedium` 的维度，以及 `sessions`、`activeUsers`、`totalRevenue` 的指标来运行报告。
- **Ads 关联发现**：使用 `GOOGLE_ANALYTICS_ANALYTICS_ADMIN_PROPERTIES_GOOGLE_ADS` 查找每个 GA4 属性关联了哪些 Google Ads 账户。
- **字段发现**：在构建复杂报告之前，使用 `GOOGLE_ANALYTICS_GET_METADATA` 列出所有可用的维度和指标。

## 常见陷阱

- **维度/指标兼容性**：GA4 API 有严格的兼容性规则。并非所有维度都可以与所有指标组合使用。人口统计维度（例如 `userAgeBracket`、`userGender`）通常与会话范围的维度/筛选条件（例如 `sessionCampaignName`、`sessionSource`）不兼容。
- **`dateRange` 不是维度**：不要在 dimensions 数组中包含 `dateRange`。请改用 `date`、`dateHour`、`year`、`month` 或 `week`。
- **`exits` 无效**：在 GA4 中，`exits` 既不是有效的维度，也不是有效的指标。
- **属性 ID 格式**：必须是 `properties/{numeric_id}`（例如 `properties/123456789`）。不要使用 Google 账户 ID（长的 OAuth ID）。
- **账户 ID 格式**：必须是 `accounts/{numeric_id}`，其中数字 ID 为 6-10 位。
- **筛选条件分离**：`dimensionFilter` 仅用于维度字段，`metricFilter` 仅用于指标字段。混用会导致错误。
- **每个报告请求最多 9 个维度和 10 个指标**。

## 快速参考
| 操作 | 工具 | 关键参数 |
|--------|------|----------------|
| 列出 Ads 关联链接 | `GOOGLE_ANALYTICS_ANALYTICS_ADMIN_PROPERTIES_GOOGLE_ADS` | `parent` |
| 运行报告 | `GOOGLE_ANALYTICS_RUN_REPORT` | `property`、`dimensions`、`metrics`、`dateRanges` |
| 检查兼容性 | `GOOGLE_ANALYTICS_CHECK_COMPATIBILITY` | （通过 RUBE_SEARCH_TOOLS 查看完整模式） |
| 列出账户 | `GOOGLE_ANALYTICS_LIST_ACCOUNTS` | `pageSize` |
| 列出属性 | `GOOGLE_ANALYTICS_LIST_PROPERTIES` | `account`、`pageSize` |
| 获取元数据 | `GOOGLE_ANALYTICS_GET_METADATA` | （通过 RUBE_SEARCH_TOOLS 查看完整模式） |

---
*由 [Composio](https://composio.dev) 提供支持*
