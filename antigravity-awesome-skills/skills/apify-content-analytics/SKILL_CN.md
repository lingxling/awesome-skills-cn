---
name: apify-content-analytics
description: 跟踪参与指标、测量营销活动投资回报率并分析 Instagram、Facebook、YouTube 和 TikTok 上的内容性能。
risk: critical
source: community
date_added: "2026-09-04"
---

# 内容分析

使用 Apify Actor 跟踪和分析内容性能，从多个平台提取参与指标。

## 何时使用
- 您需要帖子、Reels、视频、广告或标签的参与、增长或投资回报率指标。
- 任务是使用 Apify Actor 收集跨平台内容性能数据。
- 您需要导出的分析结果以及对哪些内容表现最好的简明解释。

## 先决条件
（无需提前检查）

- 带有 `APIFY_TOKEN` 的 `.env` 文件
- Node.js 20.6+（支持本机 `--env-file`）
- `mcpc` CLI 工具：`npm install -g @apify/mcpc`

## 工作流

复制此检查清单并跟踪进度：

```
任务进度：
- [ ] 步骤 1：识别内容分析类型（选择 Actor）
- [ ] 步骤 2：通过 mcpc 获取 Actor 模式
- [ ] 步骤 3：询问用户偏好（格式、文件名）
- [ ] 步骤 4：运行分析脚本
- [ ] 步骤 5：总结发现
```

### 步骤 1：识别内容分析类型

根据分析需求选择合适的 Actor：

| 用户需求 | Actor ID | 最适合 |
|-----------|----------|----------|
| 帖子参与指标 | `apify/instagram-post-scraper` | 帖子性能 |
| Reel 性能 | `apify/instagram-reel-scraper` | Reel 分析 |
| 追随者增长跟踪 | `apify/instagram-followers-count-scraper` | 增长指标 |
| 评论参与 | `apify/instagram-comment-scraper` | 评论分析 |
| 标签性能 | `apify/instagram-hashtag-scraper` | 品牌标签 |
| 提及跟踪 | `apify/instagram-tagged-scraper` | 标签跟踪 |
| 综合指标 | `apify/instagram-scraper` | 完整数据 |
| 基于 API 的分析 | `apify/instagram-api-scraper` | API 访问 |
| Facebook 帖子性能 | `apify/facebook-posts-scraper` | 帖子指标 |
| 反应分析 | `apify/facebook-likes-scraper` | 参与类型 |
| Facebook Reels 指标 | `apify/facebook-reels-scraper` | Reels 性能 |
| 广告性能跟踪 | `apify/facebook-ads-scraper` | 广告分析 |
| Facebook 评论分析 | `apify/facebook-comments-scraper` | 评论参与 |
| 页面性能审计 | `apify/facebook-pages-scraper` | 页面指标 |
| YouTube 视频指标 | `streamers/youtube-scraper` | 视频性能 |
| YouTube Shorts 分析 | `streamers/youtube-shorts-scraper` | Shorts 性能 |
| TikTok 内容指标 | `clockworks/tiktok-scraper` | TikTok 分析 |

### 步骤 2：获取 Actor 模式

使用 mcpc 动态获取 Actor 的输入模式和详细信息：

```bash
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com --header "Authorization: Bearer $APIFY_TOKEN" tools-call fetch-actor-details actor:="ACTOR_ID" | jq -r ".content"
```

将 `ACTOR_ID` 替换为所选的 Actor（例如 `apify/instagram-post-scraper`）。

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
- 分析的内容数量
- 文件位置和名称
- 关键性能见解
- 建议的后续步骤（深度分析、内容优化）

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
