---
name: apify-ecommerce
description: "使用 Apify 的电商抓取工具(E-commerce Scraping Tool)，从任意电商平台提取产品数据、价格、评论和卖家信息。"
risk: critical
source: community
date_added: "2026-09-04"
---

# 电商数据提取

使用 Apify 的电商抓取工具(E-commerce Scraping Tool)，从任意电商平台提取产品数据、价格、评论和卖家信息。

## 何时使用
- 你需要从电商网站获取产品、定价、评论、库存或卖家数据。
- 任务涉及价格监控、竞品对比、MAP(最低广告价)合规检查，或评论分析。
- 你需要一个用于提取市场数据并总结发现的引导式工作流程。

## 前提条件

- 包含 `APIFY_TOKEN` 的 `.env` 文件(位于 `~/.claude/.env`)
- Node.js 20.6+(用于原生的 `--env-file` 支持)

## 工作流程选择

| 用户需求 | 工作流程 | 最适用场景 |
|-----------|----------|----------|
| 追踪价格、比较产品 | 工作流程 1：产品与定价 | 价格监控、MAP 合规、竞品分析。可添加 AI 摘要以获取洞察。 |
| 分析评论(情绪或质量) | 工作流程 2：评论 | 品牌认知、客户情绪、质量问题、缺陷模式 |
| 跨店铺查找卖家 | 工作流程 3：卖家 | 未授权经销商、通过 Google Shopping 进行供应商发现 |

## 进度追踪

```
任务进度：
- [ ] 第 1 步：选择工作流程并确定数据源
- [ ] 第 2 步：配置 Actor 输入
- [ ] 第 3 步：询问用户偏好(格式、文件名)
- [ ] 第 4 步：运行提取脚本
- [ ] 第 5 步：总结结果
```

---

## 工作流程 1：产品与定价

**使用场景：** 提取产品数据、价格和库存状态。追踪竞品价格、检测 MAP 违规、对产品进行基准比较，或进行市场调研。

**最适合：** 定价分析师、产品经理、市场研究人员。

### 输入选项

| 输入类型 | 字段 | 描述 |
|------------|-------|-------------|
| 产品 URL | `detailsUrls` | 产品页面的直接链接(使用对象格式) |
| 分类 URL | `listingUrls` | 分类/搜索结果页面的链接 |
| 关键词搜索 | `keyword` + `marketplaces` | 在选定的多个市场中搜索关键词 |

### 示例 - 产品 URL
```json
{
  "detailsUrls": [
    {"url": "https://www.amazon.com/dp/B09V3KXJPB"},
    {"url": "https://www.walmart.com/ip/123456789"}
  ],
  "additionalProperties": true
}
```

### 示例 - 关键词搜索
```json
{
  "keyword": "Samsung Galaxy S24",
  "marketplaces": ["www.amazon.com", "www.walmart.com"],
  "additionalProperties": true,
  "maxProductResults": 50
}
```

### 可选：AI 摘要

添加以下字段以获得 AI 生成的洞察：

| 字段 | 描述 |
|-------|-------------|
| `fieldsToAnalyze` | 要分析的数据点：`["name", "offers", "brand", "description"]` |
| `customPrompt` | 自定义分析指令 |

**带 AI 摘要的示例：**
```json
{
  "keyword": "robot vacuum",
  "marketplaces": ["www.amazon.com"],
  "maxProductResults": 50,
  "additionalProperties": true,
  "fieldsToAnalyze": ["name", "offers", "brand"],
  "customPrompt": "Summarize price range and identify top brands"
}
```

### 输出字段
- `name` - 产品名称
- `url` - 产品 URL
- `offers.price` - 当前价格
- `offers.priceCurrency` - 货币代码(可能因卖家所在地区而异)
- `brand.slogan` - 品牌名称(嵌套在对象中)
- `image` - 产品图片 URL
- 当 `additionalProperties: true` 时，还会有额外的卖家/库存信息

> **说明：** 即使是美国的搜索，结果中的货币也可能有所不同，因为价格反映的是不同卖家所在的地区。

---

## 工作流程 2：客户评论

**使用场景：** 提取评论用于情绪分析、品牌认知监控，或质量问题检测。

**最适合：** 品牌经理、客户体验团队、QA 团队、产品经理。

### 输入选项

| 输入类型 | 字段 | 描述 |
|------------|-------|-------------|
| 产品 URL | `reviewListingUrls` | 要提取评论的产品页面 |
| 关键词搜索 | `keywordReviews` + `marketplacesReviews` | 按关键词搜索产品评论 |

### 示例 - 从产品中提取评论
```json
{
  "reviewListingUrls": [
    {"url": "https://www.amazon.com/dp/B09V3KXJPB"}
  ],
  "sortReview": "Most recent",
  "additionalReviewProperties": true,
  "maxReviewResults": 500
}
```

### 示例 - 关键词搜索
```json
{
  "keywordReviews": "wireless earbuds",
  "marketplacesReviews": ["www.amazon.com"],
  "sortReview": "Most recent",
  "additionalReviewProperties": true,
  "maxReviewResults": 200
}
```

### 排序选项
- `Most recent` - 最新评论优先(推荐)
- `Most relevant` - 平台默认相关性排序
- `Most helpful` - 投票最高的评论
- `Highest rated` - 5 星评论优先
- `Lowest rated` - 1 星评论优先

> **说明：** `sortReview: "Lowest rated"` 选项在所有市场上可能都无法稳定生效。对于质量分析，建议收集较大样本，并在后处理阶段按评分进行筛选。

### 质量分析技巧
- 设置较高的 `maxReviewResults` 以获得统计显著性
- 关注反复出现的关键词："broke"(损坏)、"defect"(缺陷)、"quality"(质量)、"returned"(退货)
- 如果排序未按预期生效，可按评分对结果进行筛选
- 与竞品进行交叉比对以做基准分析

---

## 工作流程 3：卖家情报

**使用场景：** 跨店铺查找卖家、发现未授权的经销商、评估供应商选项。

**最适合：** 品牌保护团队、采购部门、供应链管理人员。

> **说明：** 此工作流程使用 Google Shopping 来跨店铺查找卖家。直接的卖家资料页 URL 并不被可靠地支持。

### 输入配置
```json
{
  "googleShoppingSearchKeyword": "Nike Air Max 90",
  "scrapeSellersFromGoogleShopping": true,
  "countryCode": "us",
  "maxGoogleShoppingSellersPerProduct": 20,
  "maxGoogleShoppingResults": 100
}
```

### 选项
| 字段 | 描述 |
|-------|-------------|
| `googleShoppingSearchKeyword` | 要搜索的产品名称 |
| `scrapeSellersFromGoogleShopping` | 设为 `true` 以提取卖家信息 |
| `scrapeProductsFromGoogleShopping` | 设为 `true` 以同时提取产品详情 |
| `countryCode` | 目标国家(例如 `us`、`uk`、`de`) |
| `maxGoogleShoppingSellersPerProduct` | 每个产品的最大卖家数 |
| `maxGoogleShoppingResults` | 结果总数上限 |

---

## 支持的市场平台

### Amazon(20+ 个地区)
`www.amazon.com`、`www.amazon.co.uk`、`www.amazon.de`、`www.amazon.fr`、`www.amazon.it`、`www.amazon.es`、`www.amazon.ca`、`www.amazon.com.au`、`www.amazon.co.jp`、`www.amazon.in`、`www.amazon.com.br`、`www.amazon.com.mx`、`www.amazon.nl`、`www.amazon.pl`、`www.amazon.se`、`www.amazon.ae`、`www.amazon.sa`、`www.amazon.sg`、`www.amazon.com.tr`、`www.amazon.eg`

### 美国主要零售商
`www.walmart.com`、`www.costco.com`、`www.costco.ca`、`www.homedepot.com`

### 欧洲零售商
`allegro.pl`、`allegro.cz`、`allegro.sk`、`www.alza.cz`、`www.alza.sk`、`www.alza.de`、`www.alza.at`、`www.alza.hu`、`www.kaufland.de`、`www.kaufland.pl`、`www.kaufland.cz`、`www.kaufland.sk`、`www.kaufland.at`、`www.kaufland.fr`、`www.kaufland.it`、`www.cdiscount.com`

### IKEA(40+ 个国家/语言组合)
支持所有主要的 IKEA 区域站点，并提供多种语言选项。

### Google Shopping
用于跨多个店铺进行卖家发现。

---

## 运行提取任务

### 第 1 步：设置技能路径
```bash
SKILL_PATH=~/.claude/skills/apify-ecommerce
```

### 第 2 步：运行脚本

**快速查看结果(在对话中显示)：**
```bash
node --env-file=~/.claude/.env $SKILL_PATH/reference/scripts/run_actor.js \
  --actor "apify/e-commerce-scraping-tool" \
  --input 'JSON_INPUT'
```

**导出为 CSV：**
```bash
node --env-file=~/.claude/.env $SKILL_PATH/reference/scripts/run_actor.js \
  --actor "apify/e-commerce-scraping-tool" \
  --input 'JSON_INPUT' \
  --output YYYY-MM-DD_filename.csv \
  --format csv
```

**导出为 JSON：**
```bash
node --env-file=~/.claude/.env $SKILL_PATH/reference/scripts/run_actor.js \
  --actor "apify/e-commerce-scraping-tool" \
  --input 'JSON_INPUT' \
  --output YYYY-MM-DD_filename.json \
  --format json
```

### 第 3 步：总结结果

报告以下内容：
- 提取的条目数量
- 文件位置(如已导出)
- 基于工作流程的关键洞察：
  - **产品：** 价格区间、异常值、MAP 违规情况
  - **评论：** 平均评分、情绪趋势、质量问题
  - **卖家：** 卖家数量、发现的未授权卖家

---

## 错误处理

| 错误 | 解决方案 |
|-------|----------|
| `APIFY_TOKEN not found` | 确保 `~/.claude/.env` 中包含 `APIFY_TOKEN=your_token` |
| `Actor not found` | 核实 Actor ID：`apify/e-commerce-scraping-tool` |
| `Run FAILED` | 检查错误输出中的 Apify console 链接 |
| `Timeout` | 减小 `maxProductResults`，或增加 `--timeout` |
| `No results` | 核实 URL 是否有效且可访问 |
| `Invalid marketplace` | 检查市场值是否与受支持列表完全匹配 |

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出当作特定环境验证、测试或专家审查的替代品。
- 如果所需的输入、权限、安全边界或成功标准缺失，应停下来请求澄清。
