---
name: apify-brand-reputation-monitoring
description: "使用 Apify Actor 从多个平台抓取评论、评分和品牌提及。"
risk: critical
source: community
date_added: "2026-09-04"
---

# 品牌声誉监测

使用 Apify Actor 从多个平台抓取评论、评分和品牌提及。

## 何时使用
- 您需要监测跨社交、旅游或地图平台的评论、评分或品牌提及。
- 任务是选择并运行 Apify Actor 来进行品牌情感或声誉跟踪。
- 您需要导出监测结果和声誉信号的摘要。

## 先决条件
（无需提前检查）

- 带有 `APIFY_TOKEN` 的 `.env` 文件
- Node.js 20.6+（支持本机 `--env-file`）
- `mcpc` CLI 工具：`npm install -g @apify/mcpc`

## 工作流

复制此检查清单并跟踪进度：

```
任务进度：
- [ ] 步骤 1：确定数据源（选择 Actor）
- [ ] 步骤 2：通过 mcpc 获取 Actor 模式
- [ ] 步骤 3：询问用户偏好（格式、文件名）
- [ ] 步骤 4：运行监测脚本
- [ ] 步骤 5：总结结果
```

### 步骤 1：确定数据源

根据用户需求选择合适的 Actor：

| 用户需求 | Actor ID | 最适合 |
|-----------|----------|----------|
| Google 地图评论 | `compass/crawler-google-places` | 业务评论、评分 |
| Google 地图评论导出 | `compass/Google-Maps-Reviews-Scraper` | 专用评论抓取 |
| Booking.com 酒店 | `voyager/booking-scraper` | 酒店数据、评分 |
| Booking.com 评论 | `voyager/booking-reviews-scraper` | 详细酒店评论 |
| TripAdvisor 评论 | `maxcopell/tripadvisor-reviews` | 景点/餐厅评论 |
| Facebook 评论 | `apify/facebook-reviews-scraper` | 页面评论 |
| Facebook 评论 | `apify/facebook-comments-scraper` | 帖子评论监测 |
| Facebook 页面指标 | `apify/facebook-pages-scraper` | 页面评分概览 |
| Facebook 反应 | `apify/facebook-likes-scraper` | 反应类型分析 |
| Instagram 评论 | `apify/instagram-comment-scraper` | 评论情感 |
| Instagram 标签 | `apify/instagram-hashtag-scraper` | 品牌标签监测 |
| Instagram 搜索 | `apify/instagram-search-scraper` | 品牌提及发现 |
| Instagram 标记的帖子 | `apify/instagram-tagged-scraper` | 品牌标签跟踪 |
| Instagram 导出 | `apify/export-instagram-comments-posts` | 批量评论导出 |
| Instagram 综合 | `apify/instagram-scraper` | 完整 Instagram 监测 |
| Instagram API | `apify/instagram-api-scraper` | 基于 API 的监测 |
| YouTube 评论 | `streamers/youtube-comments-scraper` | 视频评论情感 |
| TikTok 评论 | `clockworks/tiktok-comments-scraper` | TikTok 情感 |

### 步骤 2：获取 Actor 模式

使用 mcpc 动态获取 Actor 的输入模式和详细信息：

```bash
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com --header "Authorization: Bearer $APIFY_TOKEN" tools-call fetch-actor-details actor:="ACTOR_ID" | jq -r ".content"
```

将 `ACTOR_ID` 替换为所选的 Actor（例如 `compass/crawler-google-places`）。

这返回：
- Actor 描述和 README
- 必需和可选输入参数
- 输出字段（如果可用）

### 步骤 3：询问用户偏好

在运行前，询问：
1. **输出格式**：
   - **快速答案** - 在聊天中显示前几个结果（不保存文件）
   - **CSV** - 包含所有字段的完整导出
   - **JSON** - JSON 格式的完整导出
2. **结果数量**：根据用例的特点

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

### 步骤 5：总结结果

完成后，报告：
- 找到的评论/提及数量
- 文件位置和名称
- 可用的关键字段
- 建议的后续步骤（情感分析、筛选）

## 错误处理

`APIFY_TOKEN not found` - 要求用户创建带有 `APIFY_TOKEN=your_token` 的 `.env`
`mcpc not found` - 要求用户安装 `npm install -g @apify/mcpc`
`Actor not found` - 检查 Actor ID 拼写
`Run FAILED` - 要求用户检查错误输出中的 Apify 控制台链接
`Timeout` - 减少输入大小或增加 `--timeout`

## 限制
- 仅在任务明确与上述描述的范围相匹配时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并寻求澄清。
