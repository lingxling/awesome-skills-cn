---
name: apify-competitor-intelligence
description: 分析 Google 地图、Booking.com、Facebook、Instagram、YouTube 和 TikTok 上的竞争对手策略、内容、定价、广告和市场定位。
risk: critical
source: community
date_added: "2026-09-04"
---

# 竞争对手情报

使用 Apify Actor 从多个平台分析竞争对手以提取数据。

## 何时使用
- 您需要竞争对手基准以比较内容、评论、定价、广告、受众或频道性能。
- 任务涉及选择 Apify Actor 来跨地图、预订、社交或视频平台比较竞争对手。
- 您需要结构化的竞争对手数据加上综合的战略或定位要点。

## 先决条件
（无需提前检查）

- 带有 `APIFY_TOKEN` 的 `.env` 文件
- Node.js 20.6+（支持本机 `--env-file`）
- `mcpc` CLI 工具：`npm install -g @apify/mcpc`

## 工作流

复制此检查清单并跟踪进度：

```
任务进度：
- [ ] 步骤 1：识别竞争对手分析类型（选择 Actor）
- [ ] 步骤 2：通过 mcpc 获取 Actor 模式
- [ ] 步骤 3：询问用户偏好（格式、文件名）
- [ ] 步骤 4：运行分析脚本
- [ ] 步骤 5：总结发现
```

### 步骤 1：识别竞争对手分析类型

根据分析需求选择合适的 Actor：

| 用户需求 | Actor ID | 最适合 |
|-----------|----------|----------|
| 竞争对手业务数据 | `compass/crawler-google-places` | 位置分析 |
| 竞争对手联系发现 | `poidata/google-maps-email-extractor` | 电子邮件提取 |
| 特性基准测试 | `compass/google-maps-extractor` | 详细业务数据 |
| 竞争对手评论分析 | `compass/Google-Maps-Reviews-Scraper` | 评论比较 |
| 竞争对手酒店数据 | `voyager/booking-scraper` | 酒店基准测试 |
| 竞争对手酒店评论 | `voyager/booking-reviews-scraper` | 评论分析 |
| 竞争对手广告策略 | `apify/facebook-ads-scraper` | 广告创意分析 |
| 竞争对手页面指标 | `apify/facebook-pages-scraper` | 页面性能 |
| 竞争对手内容分析 | `apify/facebook-posts-scraper` | 帖子策略 |
| 竞争对手 reels 性能 | `apify/facebook-reels-scraper` | Reels 分析 |
| 竞争对手受众分析 | `apify/facebook-comments-scraper` | 评论情感 |
| 竞争对手事件监测 | `apify/facebook-events-scraper` | 事件跟踪 |
| 竞争对手受众重叠 | `apify/facebook-followers-following-scraper` | 追随者分析 |
| 竞争对手评论基准测试 | `apify/facebook-reviews-scraper` | 评论比较 |
| 竞争对手广告监测 | `apify/facebook-search-scraper` | 广告发现 |
| 竞争对手资料指标 | `apify/instagram-profile-scraper` | 资料分析 |
| 竞争对手内容监测 | `apify/instagram-post-scraper` | 帖子跟踪 |
| 竞争对手参与分析 | `apify/instagram-comment-scraper` | 评论分析 |
| 竞争对手 reel 性能 | `apify/instagram-reel-scraper` | Reel 指标 |
| 竞争对手增长跟踪 | `apify/instagram-followers-count-scraper` | 追随者跟踪 |
| 综合竞争对手数据 | `apify/instagram-scraper` | 完整分析 |
| 基于 API 的竞争对手分析 | `apify/instagram-api-scraper` | API 访问 |
| 竞争对手视频分析 | `streamers/youtube-scraper` | 视频指标 |
| 竞争对手情感分析 | `streamers/youtube-comments-scraper` | 评论情感 |
| 竞争对手频道指标 | `streamers/youtube-channel-scraper` | 频道分析 |
| TikTok 竞争对手分析 | `clockworks/tiktok-scraper` | TikTok 数据 |
| 竞争对手视频策略 | `clockworks/tiktok-video-scraper` | 视频分析 |
| 竞争对手 TikTok 资料 | `clockworks/tiktok-profile-scraper` | 资料数据 |

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

### 步骤 5：总结发现

完成后，报告：
- 分析的竞争对手数量
- 文件位置和名称
- 关键竞争见解
- 建议的后续步骤（深度分析、基准测试）

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
