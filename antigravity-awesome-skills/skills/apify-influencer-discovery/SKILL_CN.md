---
name: apify-influencer-discovery
description: 找到并评估用于品牌合作的影响者、验证真实性并跟踪 Instagram、Facebook、YouTube 和 TikTok 上的协作性能。
risk: critical
source: community
date_added: "2026-09-04"
---

# 影响者发现

使用 Apify Actor 跨多个平台发现和分析影响者。

## 何时使用
- 您需要为宣传、合作或营销活动规划发现创作者或影响者。
- 任务是在社交平台上评估真实性、参与度、利基契合度或受众信号。
- 您需要基于 Apify 的提取加上合适的影响者候选人的候选名单或摘要。

## 先决条件
（无需提前检查）

- 带有 `APIFY_TOKEN` 的 `.env` 文件
- Node.js 20.6+（支持本机 `--env-file`）
- `mcpc` CLI 工具：`npm install -g @apify/mcpc`

## 工作流

复制此检查清单并跟踪进度：

```
任务进度：
- [ ] 步骤 1：确定发现来源（选择 Actor）
- [ ] 步骤 2：通过 mcpc 获取 Actor 模式
- [ ] 步骤 3：询问用户偏好（格式、文件名）
- [ ] 步骤 4：运行发现脚本
- [ ] 步骤 5：总结结果
```

### 步骤 1：确定发现来源

根据用户需求选择合适的 Actor：

| 用户需求 | Actor ID | 最适合 |
|-----------|----------|----------|
| 影响者资料 | `apify/instagram-profile-scraper` | 资料指标、个人简介、追随者数 |
| 按标签查找 | `apify/instagram-hashtag-scraper` | 发现使用特定标签的影响者 |
| Reel 参与 | `apify/instagram-reel-scraper` | 分析 reel 性能和参与度 |
| 按利基发现 | `apify/instagram-search-scraper` | 按关键字/利基搜索影响者 |
| 品牌提及 | `apify/instagram-tagged-scraper` | 跟踪标记品牌/产品的人 |
| 综合数据 | `apify/instagram-scraper` | 完整资料、帖子、评论分析 |
| 基于 API 的发现 | `apify/instagram-api-scraper` | 快速基于 API 的数据提取 |
| 参与分析 | `apify/export-instagram-comments-posts` | 导出评论进行情感分析 |
| Facebook 内容 | `apify/facebook-posts-scraper` | 分析 Facebook 帖子性能 |
| 微观影响者 | `apify/facebook-groups-scraper` | 在利基群组中查找影响者 |
| 有影响力的页面 | `apify/facebook-search-scraper` | 搜索有影响力的页面 |
| YouTube 创作者 | `streamers/youtube-channel-scraper` | 频道指标和订阅者数据 |
| TikTok 影响者 | `clockworks/tiktok-scraper` | 综合 TikTok 数据提取 |
| TikTok（免费） | `clockworks/free-tiktok-scraper` | 免费 TikTok 数据提取器 |
| 直播主播 | `clockworks/tiktok-live-scraper` | 发现直播流媒体影响者 |

### 步骤 2：获取 Actor 模式

使用 mcpc 动态获取 Actor 的输入模式和详细信息：

```bash
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com --header "Authorization: Bearer $APIFY_TOKEN" tools-call fetch-actor-details actor:="ACTOR_ID" | jq -r ".content"
```

将 `ACTOR_ID` 替换为所选的 Actor（例如 `apify/instagram-profile-scraper`）。

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
- 找到的影响者数量
- 文件位置和名称
- 可用的关键指标（追随者、参与率等）
- 建议的后续步骤（筛选、外联、深度分析）

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
