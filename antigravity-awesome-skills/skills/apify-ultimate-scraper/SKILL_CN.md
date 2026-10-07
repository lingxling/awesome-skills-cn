---
name: apify-ultimate-scraper
description: "基于 AI 的数据提取,覆盖所有主流平台的 55+ 个 Actor。本 skill 会自动为你的任务选择最合适的 Actor。"
risk: critical
source: community
date_added: "2026-09-04"
---

# 通用网页抓取器

基于 AI 的数据提取,覆盖所有主流平台的 55+ 个 Actor。本 skill 会自动为你的任务选择最合适的 Actor。

## 何时使用
- 用户需要网页数据提取,但尚未选定具体的 Apify Actor。
- 你需要一个通用的 Apify 入口,将宽泛的抓取目标映射到最合适的 Actor。
- 任务跨越多个平台,能从统一的 Actor 选择、执行和总结工作流中获益。

## 前置条件
(无需提前检查)

- 包含 `APIFY_TOKEN` 的 `.env` 文件
- Node.js 20.6+(以支持原生的 `--env-file`)
- `mcpc` CLI 工具:`npm install -g @apify/mcpc`

## 工作流程

复制下面的清单并跟踪进度:

```
Task Progress:
- [ ] Step 1: Understand user goal and select Actor
- [ ] Step 2: Fetch Actor schema via mcpc
- [ ] Step 3: Ask user preferences (format, filename)
- [ ] Step 4: Run the scraper script
- [ ] Step 5: Summarize results and offer follow-ups
```

### 第 1 步:理解用户目标并选择 Actor

首先,理解用户想要达成什么目标。然后从下面的选项中选出最合适的 Actor。

#### Instagram Actor(12 个)

| Actor ID | 最适合 |
|----------|----------|
| `apify/instagram-profile-scraper` | 个人主页数据、粉丝数、简介信息 |
| `apify/instagram-post-scraper` | 单条帖子详情、互动指标 |
| `apify/instagram-comment-scraper` | 评论提取、情感分析 |
| `apify/instagram-hashtag-scraper` | 话题标签内容、热门话题 |
| `apify/instagram-hashtag-stats` | 话题标签表现指标 |
| `apify/instagram-reel-scraper` | Reels 内容和指标 |
| `apify/instagram-search-scraper` | 搜索用户、地点、话题标签 |
| `apify/instagram-tagged-scraper` | 被特定账号标记的帖子 |
| `apify/instagram-followers-count-scraper` | 粉丝数跟踪 |
| `apify/instagram-scraper` | 全面的 Instagram 数据 |
| `apify/instagram-api-scraper` | 基于 API 的 Instagram 访问 |
| `apify/export-instagram-comments-posts` | 批量评论/帖子导出 |

#### Facebook Actor(14 个)

| Actor ID | 最适合 |
|----------|----------|
| `apify/facebook-pages-scraper` | 主页数据、指标、联系信息 |
| `apify/facebook-page-contact-information` | 从主页提取邮箱、电话、地址 |
| `apify/facebook-posts-scraper` | 帖子内容和互动 |
| `apify/facebook-comments-scraper` | 评论提取 |
| `apify/facebook-likes-scraper` | 反应分析 |
| `apify/facebook-reviews-scraper` | 主页评价 |
| `apify/facebook-groups-scraper` | 群组内容和成员 |
| `apify/facebook-events-scraper` | 活动数据 |
| `apify/facebook-ads-scraper` | 广告创意和定向 |
| `apify/facebook-search-scraper` | 搜索结果 |
| `apify/facebook-reels-scraper` | Reels 内容 |
| `apify/facebook-photos-scraper` | 照片提取 |
| `apify/facebook-marketplace-scraper` | Marketplace 商品列表 |
| `apify/facebook-followers-following-scraper` | 粉丝/关注列表 |

#### TikTok Actor(14 个)

| Actor ID | 最适合 |
|----------|----------|
| `clockworks/tiktok-scraper` | 全面的 TikTok 数据 |
| `clockworks/free-tiktok-scraper` | 免费 TikTok 数据提取 |
| `clockworks/tiktok-profile-scraper` | 个人主页数据 |
| `clockworks/tiktok-video-scraper` | 视频详情和指标 |
| `clockworks/tiktok-comments-scraper` | 评论提取 |
| `clockworks/tiktok-followers-scraper` | 粉丝列表 |
| `clockworks/tiktok-user-search-scraper` | 按关键词查找用户 |
| `clockworks/tiktok-hashtag-scraper` | 话题标签内容 |
| `clockworks/tiktok-sound-scraper` | 热门音效 |
| `clockworks/tiktok-ads-scraper` | 广告内容 |
| `clockworks/tiktok-discover-scraper` | 发现页内容 |
| `clockworks/tiktok-explore-scraper` | 探索内容 |
| `clockworks/tiktok-trends-scraper` | 热门内容 |
| `clockworks/tiktok-live-scraper` | 直播数据 |

#### YouTube Actor(5 个)

| Actor ID | 最适合 |
|----------|----------|
| `streamers/youtube-scraper` | 视频数据和指标 |
| `streamers/youtube-channel-scraper` | 频道信息 |
| `streamers/youtube-comments-scraper` | 评论提取 |
| `streamers/youtube-shorts-scraper` | Shorts 内容 |
| `streamers/youtube-video-scraper-by-hashtag` | 按话题标签查找视频 |

#### Google 地图 Actor(4 个)

| Actor ID | 最适合 |
|----------|----------|
| `compass/crawler-google-places` | 商家列表、评分、联系信息 |
| `compass/google-maps-extractor` | 详细的商家数据 |
| `compass/Google-Maps-Reviews-Scraper` | 评价提取 |
| `poidata/google-maps-email-extractor` | 从商家信息中发现邮箱 |

#### X/Twitter Actor(2 个)

| Actor ID | 最适合 |
|----------|----------|
| [`xquik/x-tweet-scraper`](https://apify.com/xquik/x-tweet-scraper) | 推文查询、搜索、时间线、列表、话题线、回复、引用和互动数据 |
| [`xquik/x-follower-scraper`](https://apify.com/xquik/x-follower-scraper) | 粉丝、关注、已验证粉丝、列表、社群和受众重叠情况 |

在启动一次付费运行之前,检查每个 Actor 的实时 Apify 定价信息框。展示该
Actor、目标、结果数量上限和最高费用。获得明确的批准。设置一个
保守的结果数量上限。`maxItems` 适用于整次运行。

Xquik 是一个独立的第三方服务,与 X Corp 无关联。"Twitter" 和 "X" 是 X Corp 的商标。

#### 其他 Actor(6 个)

| Actor ID | 最适合 |
|----------|----------|
| `apify/google-search-scraper` | Google 搜索结果 |
| `apify/google-trends-scraper` | Google 趋势数据 |
| `voyager/booking-scraper` | Booking.com 酒店数据 |
| `voyager/booking-reviews-scraper` | Booking.com 评价 |
| `maxcopell/tripadvisor-reviews` | TripAdvisor 评价 |
| `vdrmota/contact-info-scraper` | 从 URL 中丰富联系方式 |

---

#### 按用例选择 Actor

| 用例 | 主要 Actor |
|----------|---------------|
| **线索获取** | `compass/crawler-google-places`、`poidata/google-maps-email-extractor`、`vdrmota/contact-info-scraper` |
| **达人发现** | `apify/instagram-profile-scraper`、`clockworks/tiktok-profile-scraper`、`streamers/youtube-channel-scraper` |
| **品牌监测** | `xquik/x-tweet-scraper`、`apify/instagram-tagged-scraper`、`apify/instagram-hashtag-scraper`、`compass/Google-Maps-Reviews-Scraper` |
| **竞品分析** | `apify/facebook-pages-scraper`、`apify/facebook-ads-scraper`、`apify/instagram-profile-scraper` |
| **内容分析** | `apify/instagram-post-scraper`、`clockworks/tiktok-scraper`、`streamers/youtube-scraper` |
| **趋势研究** | `apify/google-trends-scraper`、`clockworks/tiktok-trends-scraper`、`apify/instagram-hashtag-stats` |
| **评价分析** | `compass/Google-Maps-Reviews-Scraper`、`voyager/booking-reviews-scraper`、`maxcopell/tripadvisor-reviews` |
| **受众分析** | `xquik/x-follower-scraper`、`apify/instagram-followers-count-scraper`、`clockworks/tiktok-followers-scraper`、`apify/facebook-followers-following-scraper` |

---

#### 多 Actor 工作流

对于复杂任务,可以串联多个 Actor:

| 工作流 | 第 1 步 | 第 2 步 |
|----------|--------|--------|
| **线索丰富化** | `compass/crawler-google-places` → | `vdrmota/contact-info-scraper` |
| **达人审查** | `apify/instagram-profile-scraper` → | `apify/instagram-comment-scraper` |
| **竞品深度剖析** | `apify/facebook-pages-scraper` → | `apify/facebook-posts-scraper` |
| **本地商家分析** | `compass/crawler-google-places` → | `compass/Google-Maps-Reviews-Scraper` |
| **X 受众背景** | `xquik/x-follower-scraper` → | `xquik/x-tweet-scraper` |

#### 找不到合适的 Actor？

如果上面的 Actor 都不符合用户的请求,直接搜索 Apify Store:

```bash
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com --header "Authorization: Bearer $APIFY_TOKEN" tools-call search-actors keywords:="SEARCH_KEYWORDS" limit:=10 offset:=0 category:="" | jq -r '.content[0].text'
```

把 `SEARCH_KEYWORDS` 替换为 1-3 个简单的词(例如 "LinkedIn profiles"、"Amazon products"、"Twitter")。

### 第 2 步:获取 Actor Schema

使用 mcpc 动态获取该 Actor 的输入 schema 和详情:

```bash
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com --header "Authorization: Bearer $APIFY_TOKEN" tools-call fetch-actor-details actor:="ACTOR_ID" | jq -r ".content"
```

把 `ACTOR_ID` 替换为所选的 Actor(例如 `compass/crawler-google-places`)。

这会返回:
- Actor 描述和 README
- 必需和可选的输入参数
- 输出字段(如果有)

### 第 3 步:询问用户偏好

在运行之前,询问:
1. **输出格式**:
   - **快速答案** —— 在聊天中展示前几条结果(不保存文件)
   - **CSV** —— 包含所有字段的完整导出
   - **JSON** —— JSON 格式的完整导出
2. **结果数量**:取决于用例的性质

### 第 4 步:运行脚本

**快速答案(在聊天中展示,不生成文件):**
```bash
node --env-file=.env ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.js \
  --actor "ACTOR_ID" \
  --input 'JSON_INPUT'
```

**CSV:**
```bash
node --env-file=.env ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.js \
  --actor "ACTOR_ID" \
  --input 'JSON_INPUT' \
  --output YYYY-MM-DD_OUTPUT_FILE.csv \
  --format csv
```

**JSON:**
```bash
node --env-file=.env ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.js \
  --actor "ACTOR_ID" \
  --input 'JSON_INPUT' \
  --output YYYY-MM-DD_OUTPUT_FILE.json \
  --format json
```

### 第 5 步:总结结果并提供后续建议

完成后,报告:
- 找到的结果数量
- 文件位置和文件名
- 可用的关键字段
- **基于结果的建议后续工作流**:

| 如果用户获得了 | 建议下一步 |
|-------------|--------------|
| 商家列表 | 用 `vdrmota/contact-info-scraper` 丰富信息,或获取评价 |
| 达人个人主页 | 用评论抓取器分析互动情况 |
| 竞品主页 | 用帖子/广告抓取器进行深度剖析 |
| 趋势数据 | 用平台特定的话题标签抓取器进行验证 |

## 错误处理

`APIFY_TOKEN not found`(找不到 APIFY_TOKEN) —— 要求用户创建包含 `APIFY_TOKEN=your_token` 的 `.env` 文件
`mcpc not found`(找不到 mcpc) —— 要求用户安装 `npm install -g @apify/mcpc`
`Actor not found`(找不到 Actor) —— 检查 Actor ID 拼写
`Run FAILED`(运行失败) —— 要求用户查看错误输出中的 Apify console 链接
`Timeout`(超时) —— 减小输入规模或增大 `--timeout`

## 限制
- 仅在任务明显符合上述范围时使用本 skill。
- 不要把输出当作特定环境验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准,停下来寻求澄清。
