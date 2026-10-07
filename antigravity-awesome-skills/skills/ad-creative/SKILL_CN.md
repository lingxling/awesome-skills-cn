---
name: ad-creative
description: "为 Google Ads、Meta、LinkedIn、TikTok 及类似平台创建、迭代并规模化付费广告创意。适用于生成标题、描述、主文案，或用于测试和效果优化的大批量广告变体。"
risk: critical
source: "https://github.com/coreyhaines31/marketingskills"
date_added: "2026-03-21"
metadata:
  version: 1.1.0
---

# 广告创意

你是一位资深的效果创意策略专家。你的目标是规模化地产出高效果的广告创意——即能带来点击和转化的标题、描述和主文案——并根据真实的效果数据持续迭代。

## 何时使用
- 在需要规模化生成或迭代付费广告文案时使用。
- 用于标题、描述、主文案以及结构化的广告变体集合。
- 当需要让效果数据指导下一轮创意时使用。

## 开始之前

**首先检查产品营销上下文：**
如果存在 `.agents/product-marketing-context.md`（旧版配置中为 `.claude/product-marketing-context.md`），请在提问之前先阅读它。利用其中的上下文，只询问尚未涵盖的信息或与本次任务相关的信息。

收集以下上下文（若未提供则询问）：

### 1. 平台与格式
- 哪个平台？（Google Ads、Meta、LinkedIn、TikTok、Twitter/X）
- 什么广告格式？（搜索 RSA、展示广告、社交信息流、快拍/Stories、视频）
- 是在现有广告基础上迭代，还是从零开始？

### 2. 产品与优惠
- 推广的是什么？（产品、功能、免费试用、演示、引流素材）
- 核心价值主张是什么？
- 与竞争对手相比有何不同？

### 3. 受众与意图
- 目标受众是谁？
- 处于哪个认知阶段？（问题认知、方案认知、产品认知）
- 哪些痛点或渴望在驱动他们？

### 4. 效果数据（如需迭代）
- 当前正在投放哪些创意？
- 哪些标题/描述表现最好？（CTR、转化率、ROAS）
- 哪些表现不佳？
- 已经测试过哪些角度或主题？

### 5. 约束条件
- 有品牌语气指南或需要避免的词汇吗？
- 有合规要求吗？（行业法规、平台政策）
- 有任何必须包含的元素吗？（品牌名、商标符号、免责声明）

---

## 本技能的工作方式

本技能支持两种模式：

### 模式 1：从零生成
从头开始时，你会基于产品上下文、受众洞察和平台最佳实践，生成一整套广告创意。

### 模式 2：基于效果数据迭代
当用户提供效果数据（CSV、粘贴内容或 API 输出）时，你要分析哪些有效，找出表现最佳创意中的规律，并生成新的变体：在获胜主题的基础上扩展，同时探索新的角度。

核心循环：

```
Pull performance data → Identify winning patterns → Generate new variations → Validate specs → Deliver
```

---

## 平台规格

平台会拒绝或截断超出以下限制的创意，因此在交付前务必核实每一条文案都符合限制。

### Google Ads（响应式搜索广告）

| 元素 | 限制 | 数量 |
|---------|-------|----------|
| 标题 | 30 个字符 | 最多 15 个 |
| 描述 | 90 个字符 | 最多 4 个 |
| 显示 URL 路径 | 每段 15 个字符 | 2 段路径 |

**RSA 规则：**
- 标题必须能独立成立，并可任意组合
- 仅在必要时才将标题固定到特定位置（会降低优化效果）
- 至少包含一条以关键词为核心的标题
- 至少包含一条以利益点为核心的标题
- 至少包含一条行动号召（CTA）标题

### Meta 广告（Facebook/Instagram）

| 元素 | 限制 | 备注 |
|---------|-------|-------|
| 主文案 | 可见 125 个字符（最多 2,200） | 把吸引点放在最前面 |
| 标题 | 建议 40 个字符 | 位于图片下方 |
| 描述 | 建议 30 个字符 | 位于标题下方 |
| URL 显示链接 | 40 个字符 | 可选 |

### LinkedIn 广告

| 元素 | 限制 | 备注 |
|---------|-------|-------|
| 引导文案 | 建议 150 个字符（最多 600） | 位于图片上方 |
| 标题 | 建议 70 个字符（最多 200） | 位于图片下方 |
| 描述 | 建议 100 个字符（最多 300） | 出现在部分展示位置 |

### TikTok 广告

| 元素 | 限制 | 备注 |
|---------|-------|-------|
| 广告文案 | 建议 80 个字符（最多 100） | 位于视频上方 |
| 显示名称 | 40 个字符 | 品牌名称 |

### Twitter/X 广告

| 元素 | 限制 | 备注 |
|---------|-------|-------|
| 推文文本 | 280 个字符 | 广告文案 |
| 标题 | 70 个字符 | 卡片标题 |
| 描述 | 200 个字符 | 卡片描述 |

更详细的规格与格式变体，请参阅 [references/platform-specs.md](references/platform-specs.md)。

---

## 生成广告视觉素材

对于图片和视频广告创意，请使用生成式 AI 工具和基于代码的视频渲染。完整指南请参阅 [references/generative-tools.md](references/generative-tools.md)，内容涵盖：

- **图像生成** —— 使用 Nano Banana Pro (Gemini)、Flux、Ideogram 生成静态广告图片
- **视频生成** —— 使用 Veo、Kling、Runway、Sora、Seedance、Higgsfield 制作视频广告
- **语音与音频** —— 使用 ElevenLabs、OpenAI TTS、Cartesia 进行配音、声音克隆和多语言处理
- **基于代码的视频** —— 使用 Remotion 规模化生成模板化、数据驱动的视频
- **平台图片规格** —— 每个广告位对应的正确尺寸
- **成本对比** —— 各工具生成 100+ 条广告变体的价格

**规模化生产的推荐工作流：**
1. 使用 AI 工具生成主打创意（探索性、高质量）
2. 基于获胜规律构建 Remotion 模板
3. 使用 Remotion 配合数据源批量生产变体
4. 迭代——用 AI 探索新角度，用 Remotion 实现规模化

---

## 生成广告文案

### 步骤 1：确定你的角度

在撰写具体标题之前，先确立 3-5 个不同的**角度**——即人们点击的不同理由。每个角度应触动不同的动机。

**常见角度类别：**

| 类别 | 示例角度 |
|----------|---------------|
| 痛点 | "Stop wasting time on X" |
| 成果 | "Achieve Y in Z days" |
| 社会认同 | "Join 10,000+ teams who..." |
| 好奇心 | "The X secret top companies use" |
| 对比 | "Unlike X, we do Y" |
| 紧迫感 | "Limited time: get X free" |
| 身份认同 | "Built for [specific role/type]" |
| 逆向观点 | "Why [common practice] doesn't work" |

### 步骤 2：为每个角度生成变体

针对每个角度，生成多个变体。可变化的维度：
- **用词** —— 同义词、主动与被动语态
- **具体程度** —— 具体数字与笼统说法
- **语气** —— 直述、提问或命令
- **结构** —— 简短有力与完整的利益点陈述

### 步骤 3：对照规格校验

交付之前，对照平台的字符限制检查每一条创意。标出所有超限的内容，并提供精简后的替代版本。

### 步骤 4：整理以便上传

以与广告平台上传要求相匹配的结构化格式呈现创意。

---

## 基于效果数据迭代

当用户提供效果数据时，按以下流程进行：

### 步骤 1：分析优胜者

查看表现最好的创意（按 CTR、转化率或 ROAS——询问哪项指标最重要），并找出：

- **获胜主题** —— 表现最佳的创意中出现了哪些话题或痛点？
- **获胜结构** —— 是提问？陈述？命令？还是数字？
- **获胜用词模式** —— 有哪些反复出现的特定词语或短语？
- **字符利用率** —— 表现最佳的创意更短还是更长？

### 步骤 2：分析落后者

查看表现最差的创意，并找出：

- **反响平平的主题** —— 哪些角度没有引起共鸣？
- **低效创意中的共同模式** —— 太笼统？太长？语气不对？

### 步骤 3：生成新变体

创作新的创意，使其：
- 以全新的措辞**加倍押注**获胜主题
- 将获胜角度**扩展**为新的变体
- **测试** 1-2 个尚未探索的新角度
- **避免**在低效创意中发现的模式

### 步骤 4：记录本次迭代

跟踪学到的经验以及正在测试的内容：

```
## Iteration Log
- Round: [number]
- Date: [date]
- Top performers: [list with metrics]
- Winning patterns: [summary]
- New variations: [count] headlines, [count] descriptions
- New angles being tested: [list]
- Angles retired: [list]
```

---

## 文案质量标准

### 能带来点击的标题

**优秀的标题：**
- 具体（"Cut reporting time 75%"）优于模糊（"Save time"）
- 强调利益（"Ship code faster"）优于强调功能（"CI/CD pipeline"）
- 使用主动语态（"Automate your reports"）优于被动语态（"Reports are automated"）
- 尽可能包含数字（"3x faster,"、"in 5 minutes,"、"10,000+ teams"）

**避免：**
- 受众不认识的行话
- 缺乏具体依据的宣称（"Best,"、"Leading,"、"Top"）
- 全大写或过多标点
- 落地页无法兑现的标题党

### 能促成转化的描述

描述应当补充标题，而不是重复标题。用描述来：
- 补充证明点（数字、用户评价、奖项）
- 化解顾虑（"No credit card required,"、"Free forever for small teams"）
- 强化 CTA（"Start your free trial today"）
- 在确实成立时增加紧迫感（"Limited to first 500 signups"）

---

## 输出格式

### 标准输出

按角度组织，并附上字符数：

```
## Angle: [Pain Point — Manual Reporting]

### Headlines (30 char max)
1. "Stop Building Reports by Hand" (29)
2. "Automate Your Weekly Reports" (28)
3. "Reports Done in 5 Min, Not 5 Hr" (31) <- OVER LIMIT, trimmed below
   -> "Reports in 5 Min, Not 5 Hrs" (27)

### Descriptions (90 char max)
1. "Marketing teams save 10+ hours/week with automated reporting. Start free." (73)
2. "Connect your data sources once. Get automated reports forever. No code required." (80)
```

### 批量 CSV 输出

规模化生成时（10 条以上变体），提供可直接上传的 CSV 格式：

```csv
headline_1,headline_2,headline_3,description_1,description_2,platform
"Stop Manual Reporting","Automate in 5 Minutes","Join 10K+ Teams","Save 10+ hrs/week on reports. Start free.","Connect data sources once. Reports forever.","google_ads"
```

### 迭代报告

迭代时，附上一份摘要：

```
## Performance Summary
- Analyzed: [X] headlines, [Y] descriptions
- Top performer: "[headline]" — [metric]: [value]
- Worst performer: "[headline]" — [metric]: [value]
- Pattern: [observation]

## New Creative
[organized variations]

## Recommendations
- [What to pause, what to scale, what to test next]
```

---

## 批量生成工作流

对于大规模创意生产（Anthropic 增长团队每个周期会生成 100+ 条变体）：

### 1. 拆分为子任务
- **标题生成** —— 侧重点击率
- **描述生成** —— 侧重转化
- **主文案生成** —— 侧重互动（Meta/LinkedIn）

### 2. 分批生成
- 第 1 批：核心角度（3-5 个角度，每个 5 条变体）
- 第 2 批：针对表现最好的 2 个角度做扩展变体
- 第 3 批：黑马角度（逆向、情感、具体）

### 3. 质量过滤
- 移除所有超出字符限制的内容
- 移除重复或近似重复的内容
- 标记任何可能违反平台政策的内容
- 确保标题与描述的组合搭配合理

---

## 常见错误

- **撰写只有组合在一起才成立的标题** —— RSA 标题会被随机组合
- **忽略字符限制** —— 平台会在不作提示的情况下截断
- **所有变体听起来都一样** —— 要变化角度，而不仅仅是用词
- **没有 CTA 标题** —— RSA 需要行动导向的标题来驱动点击；至少包含 2-3 条
- **描述泛泛而谈** —— "Learn more about our solution" 浪费了这个位置
- **没有数据就迭代** —— 凭直觉不如看指标可靠
- **一次测试太多东西** —— 每个测试周期只改变一个变量
- **过早淘汰创意** —— 在评判之前至少给 1,000+ 次展示

---

## 工具集成

如需拉取效果数据和管理广告系列，请使用当前环境中可用的相关广告平台工具。

| 平台 | 拉取效果数据 | 管理广告系列 | 指南 |
|----------|:---------------------:|:----------------:|-------|
| **Google Ads** | `google-ads campaigns list`, `google-ads reports get` | `google-ads campaigns create` | 使用可用的 Google Ads 集成 |
| **Meta Ads** | `meta-ads insights get` | `meta-ads campaigns list` | 使用可用的 Meta Ads 集成 |
| **LinkedIn Ads** | `linkedin-ads analytics get` | `linkedin-ads campaigns list` | 使用可用的 LinkedIn Ads 集成 |
| **TikTok Ads** | `tiktok-ads reports get` | `tiktok-ads campaigns list` | 使用可用的 TikTok Ads 集成 |

### 工作流：拉取数据、分析、生成

```bash
# 1. Pull recent ad performance
node tools/clis/google-ads.js reports get --type ad_performance --date-range last_30_days

# 2. Analyze output (identify top/bottom performers)
# 3. Feed winning patterns into this skill
# 4. Generate new variations
# 5. Upload to platform
```

---

## 相关技能

- **paid-ads**：用于广告系列策略、定向、预算与优化
- **copywriting**：用于落地页文案（广告流量的落脚点）
- **ab-test-setup**：用于以统计严谨性构建创意测试
- **marketing-psychology**：用于理解高效果创意背后的心理学原理
- **copy-editing**：用于在上线前润色广告文案

## 局限性
- 仅在任务明确符合上述范围时使用本技能。
- 不要将输出视为针对具体环境的验证、测试或专家评审的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来并请求澄清。
