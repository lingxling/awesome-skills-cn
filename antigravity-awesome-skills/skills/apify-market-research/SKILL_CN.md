---
name: apify-market-research
description: 分析市场条件、地理机遇、定价、消费者行为，以及跨 Google Maps、Facebook、Instagram、Booking.com 和 TripAdvisor 的产品验证。
risk: critical
source: community
date_added: "2026-09-04"
---

# 市场研究

使用 Apify Actors 从多个平台提取数据进行市场研究。

## 何时使用

- 需要市场规模、地区需求、定价、趋势或消费者行为数据。
- 任务是使用 Apify 从地图、旅游、Facebook、Instagram 或趋势来源收集研究输入。
- 需要结构化的市场数据加上机遇或风险的综合视图。

## 前置条件

（无需提前检查）

- `.env` 文件包含 `APIFY_TOKEN`
- Node.js 20.6+（支持原生 `--env-file`）
- `mcpc` CLI 工具：`npm install -g @apify/mcpc`

## 工作流

复制此清单并跟踪进度：

```
任务进度：
- [ ] 步骤 1：确定市场研究类型（选择 Actor）
- [ ] 步骤 2：通过 mcpc 获取 Actor 架构
- [ ] 步骤 3：询问用户偏好（格式、文件名）
- [ ] 步骤 4：运行分析脚本
- [ ] 步骤 5：总结发现
```

### 步骤 1：确定市场研究类型

根据研究需求选择适当的 Actor：

| 用户需求 | Actor ID | 最适合用于 |
|-----------|----------|----------|
| 市场密度 | `compass/crawler-google-places` | 位置分析 |
| 地理空间分析 | `compass/google-maps-extractor` | 商业地图 |
| 地区兴趣 | `apify/google-trends-scraper` | 趋势数据 |
| 定价和需求 | `apify/facebook-marketplace-scraper` | 市场定价 |
| 活动市场 | `apify/facebook-events-scraper` | 活动分析 |
| 消费者需求 | `apify/facebook-groups-scraper` | 群组研究 |
| 市场格局 | `apify/facebook-pages-scraper` | 商业页面 |
| 商业密度 | `apify/facebook-page-contact-information` | 联系数据 |
| 文化洞察 | `apify/facebook-photos-scraper` | 视觉研究 |
| 利基定位 | `apify/instagram-hashtag-scraper` | 主题标签研究 |
| 主题标签统计 | `apify/instagram-hashtag-stats` | 市场规模 |
| 市场活动 | `apify/instagram-reel-scraper` | 活动分析 |
| 市场智能 | `apify/instagram-scraper` | 完整数据 |
| 产品发布研究 | `apify/instagram-api-scraper` | API 访问 |
| 酒店市场 | `voyager/booking-scraper` | 酒店数据 |
| 旅游洞察 | `maxcopell/tripadvisor-reviews` | 评价分析 |

### 步骤 2：获取 Actor 架构

使用 mcpc 动态获取 Actor 的输入架构和详细信息：

```bash
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com --header "Authorization: Bearer $APIFY_TOKEN" tools-call fetch-actor-details actor:="ACTOR_ID" | jq -r ".content"
```

用选定的 Actor 替换 `ACTOR_ID`（例如 `compass/crawler-google-places`）。

这将返回：
- Actor 说明和 README
- 必需和可选的输入参数
- 输出字段（如果可用）

### 步骤 3：询问用户偏好

运行前，询问：
1. **输出格式**：
   - **快速答案** - 在聊天中显示前几个结果（不保存文件）
   - **CSV** - 包含所有字段的完整导出
   - **JSON** - JSON 格式的完整导出
2. **结果数量**：根据用例特性

### 步骤 4：运行脚本

**快速答案（在聊天中显示，不保存文件）：**
```bash
node --env-file=.env ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.js \
  --actor "ACTOR_ID" \
  --input 'JSON_INPUT'
```

**CSV：**
```bash
node --env-file=.env ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.js \
  --actor "ACTOR_ID" \
  --input 'JSON_INPUT' \
  --output YYYY-MM-DD_OUTPUT_FILE.csv \
  --format csv
```

**JSON：**
```bash
node --env-file=.env ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.js \
  --actor "ACTOR_ID" \
  --input 'JSON_INPUT' \
  --output YYYY-MM-DD_OUTPUT_FILE.json \
  --format json
```

### 步骤 5：总结发现

完成后，报告：
- 找到的结果数量
- 文件位置和名称
- 关键市场洞察
- 建议的后续步骤（更深入的分析、验证）

## 错误处理

`APIFY_TOKEN not found` - 要求用户创建包含 `APIFY_TOKEN=your_token` 的 `.env`
`mcpc not found` - 要求用户安装 `npm install -g @apify/mcpc`
`Actor not found` - 检查 Actor ID 拼写
`Run FAILED` - 要求用户检查错误输出中的 Apify 控制台链接
`Timeout` - 减少输入大小或增加 `--timeout`

## 限制

- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
