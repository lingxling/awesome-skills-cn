---
name: googleads-automation
description: "Automate Google Ads analytics tasks via Rube MCP (Composio): list Google Ads links, run GA4 reports, check compatibility, list properties and accounts. Always search tools first for current schemas."
requires:
  mcp: [rube]
---

# Google Ads Automation via Rube MCP

Access Google Ads data through Google Analytics integration, run performance reports, list linked Ads accounts, and analyze campaign metrics using Rube MCP (Composio).

**Toolkit docs**: [composio.dev/toolkits/googleads](https://composio.dev/toolkits/googleads)

## 前置条件
- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- Active connection via `RUBE_MANAGE_CONNECTIONS` with toolkit `google_analytics`
- 始终首先调用 `RUBE_SEARCH_TOOLS` 以获取当前工具架构

## 设置
**获取 Rube MCP**: 在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥 — 只需添加端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 响应来验证 Rube MCP 可用
2. Call `RUBE_MANAGE_CONNECTIONS` with toolkit `google_analytics`
3. 如果连接未处于 ACTIVE 状态，请按照返回的授权链接完成设置
4. 在运行任何工作流之前，确认连接状态显示为 ACTIVE

> **Note**: Google Ads data is accessed through the Google Analytics toolkit integration. The tools below use GA4 properties linked to Google Ads accounts.

## Core Workflows

### 1. List Google Ads Links for a Property
Use `GOOGLE_ANALYTICS_ANALYTICS_ADMIN_PROPERTIES_GOOGLE_ADS` to retrieve all Google Ads account links configured for a GA4 property.
```
Tool: GOOGLE_ANALYTICS_ANALYTICS_ADMIN_PROPERTIES_GOOGLE_ADS
Parameters:
  - parent (required): Property resource name (format: "properties/{propertyId}")
  - pageSize: Max results (1-200, default 50)
  - pageToken: Pagination token
```

### 2. Run a GA4 Performance Report
Use `GOOGLE_ANALYTICS_RUN_REPORT` to run customized reports with dimensions, metrics, date ranges, and filters.
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

### 3. Check Dimension/Metric Compatibility
Use `GOOGLE_ANALYTICS_CHECK_COMPATIBILITY` to validate dimension and metric combinations before running a report.
```
Tool: GOOGLE_ANALYTICS_CHECK_COMPATIBILITY
Description: Validates compatibility of chosen dimensions or metrics
  before running a report.
Note: Call RUBE_SEARCH_TOOLS to get the full schema for this tool.
```

### 4. List GA4 Accounts
Use `GOOGLE_ANALYTICS_LIST_ACCOUNTS` to enumerate all accessible Google Analytics accounts.
```
Tool: GOOGLE_ANALYTICS_LIST_ACCOUNTS
Parameters:
  - pageSize: Max accounts to return
  - pageToken: Pagination token
  - showDeleted: Include soft-deleted accounts
```

### 5. List GA4 Properties Under an Account
Use `GOOGLE_ANALYTICS_LIST_PROPERTIES` to list properties for a specific GA4 account.
```
Tool: GOOGLE_ANALYTICS_LIST_PROPERTIES
Parameters:
  - account (required): Account resource name (format: "accounts/{account_id}")
  - pageSize: Max properties (1-200)
  - pageToken: Pagination token
  - showDeleted: Include trashed properties
```

### 6. Get Available Dimensions and Metrics
Use `GOOGLE_ANALYTICS_GET_METADATA` to discover all available fields for building reports.
```
Tool: GOOGLE_ANALYTICS_GET_METADATA
Description: Gets metadata for dimensions, metrics, and comparisons
  for a GA4 property.
Note: Call RUBE_SEARCH_TOOLS to get the full schema for this tool.
```

## Common Patterns

- **Discover then report**: Use `GOOGLE_ANALYTICS_LIST_ACCOUNTS` to find account IDs, then `GOOGLE_ANALYTICS_LIST_PROPERTIES` to find property IDs, then `GOOGLE_ANALYTICS_RUN_REPORT` to pull data.
- **Validate before querying**: Use `GOOGLE_ANALYTICS_CHECK_COMPATIBILITY` to validate dimension/metric combinations before running reports to avoid 400 errors.
- **Campaign performance**: Run reports with dimensions like `sessionCampaignName`, `sessionSource`, `sessionMedium` and metrics like `sessions`, `activeUsers`, `totalRevenue`.
- **Ads link discovery**: Use `GOOGLE_ANALYTICS_ANALYTICS_ADMIN_PROPERTIES_GOOGLE_ADS` to find which Google Ads accounts are linked to each GA4 property.
- **Field discovery**: Use `GOOGLE_ANALYTICS_GET_METADATA` to list all available dimensions and metrics before constructing complex reports.

## 已知陷阱

- **Dimension/metric compatibility**: The GA4 API has strict compatibility rules. Not all dimensions can be combined with all metrics. Demographic dimensions (e.g., `userAgeBracket`, `userGender`) are often incompatible with session-scoped dimensions/filters (e.g., `sessionCampaignName`, `sessionSource`).
- **`dateRange` is NOT a dimension**: Do not include `dateRange` in the dimensions array. Use `date`, `dateHour`, `year`, `month`, or `week` instead.
- **`exits` is NOT valid**: Neither `exits` as a dimension nor as a metric is valid in GA4.
- **Property ID format**: Must be `properties/{numeric_id}` (e.g., `properties/123456789`). Do not use Google Account IDs (long OAuth IDs).
- **Account ID format**: Must be `accounts/{numeric_id}` where the numeric ID is 6-10 digits.
- **Filter separation**: Use `dimensionFilter` only for dimension fields and `metricFilter` only for metric fields. Mixing them will cause errors.
- **Max 9 dimensions and 10 metrics** per report request.

## 快速参考
| Action | Tool | Key Parameters |
|--------|------|----------------|
| List Ads links | `GOOGLE_ANALYTICS_ANALYTICS_ADMIN_PROPERTIES_GOOGLE_ADS` | `parent` |
| Run report | `GOOGLE_ANALYTICS_RUN_REPORT` | `property`, `dimensions`, `metrics`, `dateRanges` |
| Check compatibility | `GOOGLE_ANALYTICS_CHECK_COMPATIBILITY` | (see full schema via RUBE_SEARCH_TOOLS) |
| List accounts | `GOOGLE_ANALYTICS_LIST_ACCOUNTS` | `pageSize` |
| List properties | `GOOGLE_ANALYTICS_LIST_PROPERTIES` | `account`, `pageSize` |
| Get metadata | `GOOGLE_ANALYTICS_GET_METADATA` | (see full schema via RUBE_SEARCH_TOOLS) |

---
*由 [Composio](https://composio.dev) 提供支持*
