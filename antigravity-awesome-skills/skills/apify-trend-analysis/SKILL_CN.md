---
name: apify-trend-analysis
description: 跨 Google Trends、Instagram、Facebook、YouTube 和 TikTok 发现和追踪新兴趋势，以告知内容策略。
risk: critical
source: community
date_added: "2026-09-04"
---

# 趋势分析

使用 Apify Actors 从多个平台提取数据发现和追踪新兴趋势。

## 前置条件

（无需提前检查）

- `.env` 文件包含 `APIFY_TOKEN`
- Node.js 20.6+（支持原生 `--env-file`）
- `mcpc` CLI 工具：`npm install -g @apify/mcpc`

## 工作流

复制此清单并跟踪进度：

```
任务进度：
- [ ] 步骤 1：确定趋势类型（选择 Actor）
- [ ] 步骤 2：通过 mcpc 获取 Actor 架构
- [ ] 步骤 3：询问用户偏好（格式、文件名）
- [ ] 步骤 4：运行分析脚本
- [ ] 步骤 5：总结发现
```

### 步骤 1：确定趋势类型

根据研究需求选择适当的 Actor：

| 用户需求 | Actor ID | 最适合用于 |
|-----------|----------|----------|
| 搜索趋势 | `apify/google-trends-scraper` | Google Trends 数据 |
| 主题标签追踪 | `apify/instagram-hashtag-scraper` | 主题标签内容 |
| 主题标签指标 | `apify/instagram-hashtag-stats` | 性能统计 |
| 视觉趋势 | `apify/instagram-post-scraper` | 帖子分析 |
| 趋势发现 | `apify/instagram-search-scraper` | 搜索趋势 |
| 全面追踪 | `apify/instagram-scraper` | 完整数据 |
| 基于 API 的趋势 | `apify/instagram-api-scraper` | API 访问 |
| 参与度趋势 | `apify/export-instagram-comments-posts` | 评论追踪 |
| 产品趋势 | `apify/facebook-marketplace-scraper` | 市场数据 |
| 视觉分析 | `apify/facebook-photos-scraper` | 照片趋势 |
| 社区趋势 | `apify/facebook-groups-scraper` | 群组监控 |
| YouTube Shorts | `streamers/youtube-shorts-scraper` | 短视频趋势 |
| YouTube 主题标签 | `streamers/youtube-video-scraper-by-hashtag` | 主题标签视频 |
| TikTok 主题标签 | `clockworks/tiktok-hashtag-scraper` | 主题标签内容 |
| 趋势音效 | `clockworks/tiktok-sound-scraper` | 音频趋势 |
| TikTok 广告 | `clockworks/tiktok-ads-scraper` | 广告趋势 |
| 发现页面 | `clockworks/tiktok-discover-scraper` | 发现趋势 |
| 探索趋势 | `clockworks/tiktok-explore-scraper` | 探索内容 |
| 趋势内容 | `clockworks/tiktok-trends-scraper` | 病毒内容 |

### 步骤 2：获取 Actor 架构

使用 mcpc 动态获取 Actor 的输入架构和详细信息：

```bash
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com --header "Authorization: Bearer $APIFY_TOKEN" tools-call fetch-actor-details actor:="ACTOR_ID" | jq -r ".content"
```

用选定的 Actor 替换 `ACTOR_ID`（例如 `apify/google-trends-scraper`）。

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
- 关键趋势洞察
- 建议的后续步骤（更深入的分析、内容机遇）

## 错误处理

`APIFY_TOKEN not found` - 要求用户创建包含 `APIFY_TOKEN=your_token` 的 `.env`
`mcpc not found` - 要求用户安装 `npm install -g @apify/mcpc`
`Actor not found` - 检查 Actor ID 拼写
`Run FAILED` - 要求用户检查错误输出中的 Apify 控制台链接
`Timeout` - 减少输入大小或增加 `--timeout`

## 何时使用

处理与其主要领域或上述功能相关的任务时使用此技能。

## 限制

- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
