---
name: apify-lead-generation
description: "使用 Apify Actor 从多个平台抓取潜在客户。"
risk: critical
source: community
date_added: "2026-09-04"
---

# 潜在客户生成

使用 Apify Actor 从多个平台抓取潜在客户。

## 何时使用
- 您需要来自地图、搜索、社交或视频平台的业务、创作者或联系潜在客户。
- 任务涉及选择 Apify Actor 来发现前景并提取宣传数据。
- 您需要导出的潜在客户数据加上潜在客户质量或细分的简明摘要。

## 先决条件
（无需提前检查）

- 带有 `APIFY_TOKEN` 的 `.env` 文件
- Node.js 20.6+（支持本机 `--env-file`）
- `mcpc` CLI 工具：`npm install -g @apify/mcpc`

## 工作流

复制此检查清单并跟踪进度：

```
任务进度：
- [ ] 步骤 1：确定潜在客户来源（选择 Actor）
- [ ] 步骤 2：通过 mcpc 获取 Actor 模式
- [ ] 步骤 3：询问用户偏好（格式、文件名）
- [ ] 步骤 4：运行潜在客户查找脚本
- [ ] 步骤 5：总结结果
```

### 步骤 1：确定潜在客户来源

根据用户需求选择合适的 Actor：

| 用户需求 | Actor ID | 最适合 |
|-----------|----------|----------|
| 本地企业 | `compass/crawler-google-places` | 餐厅、健身房、商店 |
| 联系充实 | `vdrmota/contact-info-scraper` | 来自 URL 的电子邮件、电话 |
| Instagram 资料 | `apify/instagram-profile-scraper` | 影响者发现 |
| Instagram 帖子/评论 | `apify/instagram-scraper` | 帖子、评论、标签、地点 |
| Instagram 搜索 | `apify/instagram-search-scraper` | 地点、用户、标签发现 |
| TikTok 视频/标签 | `clockworks/tiktok-scraper` | 综合 TikTok 数据提取 |
| TikTok 标签/资料 | `clockworks/free-tiktok-scraper` | 免费 TikTok 数据提取器 |
| TikTok 用户搜索 | `clockworks/tiktok-user-search-scraper` | 按关键字查找用户 |
| TikTok 资料 | `clockworks/tiktok-profile-scraper` | 创作者宣传 |
| TikTok 追随者/正在关注 | `clockworks/tiktok-followers-scraper` | 受众分析、细分 |
| Facebook 页面 | `apify/facebook-pages-scraper` | 业务联系 |
| Facebook 页面联系 | `apify/facebook-page-contact-information` | 提取电子邮件、电话、地址 |
| Facebook 群组 | `apify/facebook-groups-scraper` | 购买意图信号 |
| Facebook 事件 | `apify/facebook-events-scraper` | 事件网络、合作 |
| Google 搜索 | `apify/google-search-scraper` | 广泛的潜在客户发现 |
| YouTube 频道 | `streamers/youtube-scraper` | 创作者合作 |
| Google 地图电子邮件 | `poidata/google-maps-email-extractor` | 直接电子邮件提取 |

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
- 找到的潜在客户数量
- 文件位置和名称
- 可用的关键字段
- 建议的后续步骤（筛选、充实）

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
