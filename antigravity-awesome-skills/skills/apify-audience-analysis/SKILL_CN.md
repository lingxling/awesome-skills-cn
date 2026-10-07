---
name: apify-audience-analysis
description: 了解 Facebook、Instagram、YouTube 和 TikTok 上的受众人口统计数据、偏好、行为模式和参与质量。
risk: critical
source: community
date_added: "2026-09-04"
---

# 受众分析

使用 Apify Actor 分析和理解您的受众，从多个平台提取追随者人口统计数据、参与模式和行为数据。

## 何时使用
- 您需要来自社交平台的受众人口统计数据、参与模式或追随者行为。
- 任务是选择并运行 Apify Actor 以跨 Facebook、Instagram、YouTube 或 TikTok 进行受众分析。
- 您需要结构化提取加上受众发现的总结解释。

## 先决条件
（无需提前检查）

- 带有 `APIFY_TOKEN` 的 `.env` 文件
- Node.js 20.6+（支持本机 `--env-file`）
- `mcpc` CLI 工具：`npm install -g @apify/mcpc`

## 工作流

复制此检查清单并跟踪进度：

```
任务进度：
- [ ] 步骤 1：识别受众分析类型（选择 Actor）
- [ ] 步骤 2：通过 mcpc 获取 Actor 模式
- [ ] 步骤 3：询问用户偏好（格式、文件名）
- [ ] 步骤 4：运行分析脚本
- [ ] 步骤 5：总结发现
```

### 步骤 1：识别受众分析类型

根据分析需求选择合适的 Actor：

| 用户需求 | Actor ID | 最适合 |
|-----------|----------|----------|
| Facebook 追随者人口统计 | `apify/facebook-followers-following-scraper` | FB 追随者/正在关注的列表 |
| Facebook 参与行为 | `apify/facebook-likes-scraper` | FB 帖子点赞分析 |
| Facebook 视频受众 | `apify/facebook-reels-scraper` | FB Reels 观看者 |
| Facebook 评论分析 | `apify/facebook-comments-scraper` | FB 帖子/视频评论 |
| Facebook 内容参与 | `apify/facebook-posts-scraper` | FB 帖子参与指标 |
| Instagram 受众规模 | `apify/instagram-profile-scraper` | IG 个人资料人口统计 |
| Instagram 基于位置 | `apify/instagram-search-scraper` | IG 地理标记受众 |
| Instagram 标记网络 | `apify/instagram-tagged-scraper` | IG 标记网络分析 |
| Instagram 综合 | `apify/instagram-scraper` | 完整 IG 受众数据 |
| Instagram API 基础 | `apify/instagram-api-scraper` | IG API 访问 |
| Instagram 追随者计数 | `apify/instagram-followers-count-scraper` | IG 追随者跟踪 |
| Instagram 评论导出 | `apify/export-instagram-comments-posts` | IG 评论批量导出 |
| Instagram 评论分析 | `apify/instagram-comment-scraper` | IG 评论情感 |
| YouTube 观看者反馈 | `streamers/youtube-comments-scraper` | YT 评论分析 |
| YouTube 频道受众 | `streamers/youtube-channel-scraper` | YT 频道订阅者 |
| TikTok 追随者人口统计 | `clockworks/tiktok-followers-scraper` | TT 追随者列表 |
| TikTok 个人资料分析 | `clockworks/tiktok-profile-scraper` | TT 个人资料人口统计 |
| TikTok 评论分析 | `clockworks/tiktok-comments-scraper` | TT 评论参与 |

### 步骤 2：获取 Actor 模式

使用 mcpc 动态获取 Actor 的输入模式和详细信息：

```bash
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com --header "Authorization: Bearer $APIFY_TOKEN" tools-call fetch-actor-details actor:="ACTOR_ID" | jq -r ".content"
```

将 `ACTOR_ID` 替换为所选的 Actor（例如 `apify/facebook-followers-following-scraper`）。

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
- 分析的受众成员/个人资料数量
- 文件位置和名称
- 关键人口统计见解
- 建议的后续步骤（深度分析、细分）

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
