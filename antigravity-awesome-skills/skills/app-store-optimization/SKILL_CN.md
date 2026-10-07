---
name: app-store-optimization
description: "完整的应用商店优化（ASO）工具包，用于研究、优化和跟踪移动应用在 Apple App Store 和 Google Play Store 上的表现"
risk: critical
source: community
date_added: "2026-02-27"
---

# 应用商店优化（ASO）技能

本技能提供完整的 ASO 能力,帮助在 Apple App Store 和 Google Play Store 上成功发布和优化移动应用。

## 能力

### 研究与分析
- **关键词研究**：分析关键词搜索量、竞争程度和与应用可发现性的相关性
- **竞品分析**：深入研究所在类别中表现最佳的应用
- **市场趋势分析**：识别应用类别中新兴的趋势和机会
- **评论情感分析**：从用户评论中提取洞见,识别优势与问题
- **类别分析**：评估最优的类别及子类别放置策略

### 元数据优化
- **标题优化**：创建兼具吸引力和最优关键词布局的标题（受平台特定字符数限制）
- **描述优化**：撰写既能转化又能排名靠前的简短描述和完整描述
- **副标题/推广文本**：优化 Apple 特有的副标题（30 字符）和推广文本（170 字符）
- **关键词字段**：通过策略性选择最大化 Apple 的 100 字符关键词字段
- **类别选择**：基于数据的主类别和次类别推荐
- **图标最佳实践**：设计高转化率应用图标的指南
- **截图优化**：制作能带动安装量的截图策略
- **预览视频**：应用预览视频的最佳实践
- **本地化**：面向全球覆盖的多语言优化策略

### 转化率优化
- **A/B 测试框架**：规划并跟踪元数据实验,实现持续改进
- **视觉素材测试**：测试图标、截图和视频以实现最大转化
- **商店页面优化**：针对展示到安装转化的全面页面优化
- **行动号召（CTA）**：优化描述和推广素材中的行动号召

### 评分与评论管理
- **评论监控**：跟踪和分析用户评论以获取可执行的洞见
- **回复策略**：评论回复的模板和最佳实践
- **评分提升**：有机提升应用评分的策略方法
- **问题识别**：从评论中挖掘常见问题和功能请求

### 发布与更新策略
- **发布前检查清单**：提交到商店前的完整验证
- **发布时机**：优化发布时机以获得最大曝光和下载量
- **更新节奏**：规划最优的更新频率和功能发布
- **功能公告**："新功能"部分的撰写,以重新吸引用户
- **季节性优化**：利用季节性趋势和事件

### 分析与跟踪
- **ASO 得分**：计算涵盖多个因素的整体 ASO 健康度得分
- **关键词排名**：跟踪关键词排名随时间的变化
- **转化指标**：监控展示到安装的转化率
- **下载速度**：跟踪下载趋势与动能
- **性能基准**：与类别平均水平及竞争对手进行比较

### 平台特定要求
- **Apple App Store**：
  - 标题：30 字符
  - 副标题：30 字符
  - 推广文本：170 字符（可在无需应用更新的情况下编辑）
  - 描述：4,000 字符
  - 关键词：100 字符（逗号分隔,不含空格）
  - 新功能：4,000 字符
- **Google Play Store**：
  - 标题：50 字符（此前为 30,2021 年提升）
  - 简短描述：80 字符
  - 完整描述：4,000 字符
  - 无单独的关键词字段（关键词从标题和描述中提取）

## 输入要求

### 关键词研究
```json
{
  "app_name": "MyApp",
  "category": "Productivity",
  "target_keywords": ["task manager", "productivity", "todo list"],
  "competitors": ["Todoist", "Any.do", "Microsoft To Do"],
  "language": "en-US"
}
```

### 元数据优化
```json
{
  "platform": "apple" | "google",
  "app_info": {
    "name": "MyApp",
    "category": "Productivity",
    "target_audience": "Professionals aged 25-45",
    "key_features": ["Task management", "Team collaboration", "AI assistance"],
    "unique_value": "AI-powered task prioritization"
  },
  "current_metadata": {
    "title": "Current Title",
    "subtitle": "Current Subtitle",
    "description": "Current description..."
  },
  "target_keywords": ["productivity", "task manager", "todo"]
}
```

### 评论分析
```json
{
  "app_id": "com.myapp.app",
  "platform": "apple" | "google",
  "date_range": "last_30_days" | "last_90_days" | "all_time",
  "rating_filter": [1, 2, 3, 4, 5],
  "language": "en"
}
```

### ASO 得分计算
```json
{
  "metadata": {
    "title_quality": 0.8,
    "description_quality": 0.7,
    "keyword_density": 0.6
  },
  "ratings": {
    "average_rating": 4.5,
    "total_ratings": 15000
  },
  "conversion": {
    "impression_to_install": 0.05
  },
  "keyword_rankings": {
    "top_10": 5,
    "top_50": 12,
    "top_100": 18
  }
}
```

## 输出格式

### 关键词研究报告
- 包含搜索量估算的推荐关键词列表
- 竞争程度分析（低/中/高）
- 每个关键词的相关性得分
- 主关键词与次关键词的策略建议
- 长尾关键词机会

### 优化后的元数据包
- 平台特定的标题（含字符数验证）
- 副标题/推广文本（Apple）
- 简短描述（Google）
- 完整描述（两个平台）
- 关键词字段（Apple - 100 字符）
- 所有字段的字符数验证
- 关键词密度分析
- 优化前后对比

### 竞品分析报告
- 类别内前 10 名竞争对手
- 他们的元数据策略
- 关键词重叠分析
- 视觉素材评估
- 评分与评论数量对比
- 识别出的差距与机会

### ASO 健康度得分
- 总体得分（0-100）
- 分类细目:
  - 元数据质量（0-25）
  - 评分与评论（0-25）
  - 关键词表现（0-25）
  - 转化指标（0-25）
- 具体改进建议
- 优先行动项

### A/B 测试计划
- 假设与测试变量
- 测试时长建议
- 成功指标定义
- 样本量计算
- 统计显著性阈值

### 发布检查清单
- 提交前验证（所有必需素材、元数据）
- 商店合规性验证
- 测试检查清单（设备、操作系统版本）
- 营销准备事项
- 发布后监控计划

## 使用方法

### 关键词研究
```
Hey Claude——我刚添加了 "app-store-optimization" 技能。能帮我为一款面向专业人士的效率类应用研究最佳关键词吗？重点关注搜索量高但竞争较低的关键词。
```

### 优化应用商店列表
```
Hey Claude——我刚添加了 "app-store-optimization" 技能。能帮我优化我应用在 Apple App Store 上的元数据吗？这是我目前的列表信息：[提供当前元数据]。我想在 "task management" 和 "productivity tools" 上获得排名。
```

### 分析竞争对手策略
```
Hey Claude——我刚添加了 "app-store-optimization" 技能。能帮我分析一下 Todoist、Any.do 和 Microsoft To Do 的 ASO 策略吗？我想了解他们做得好的地方以及存在哪些机会。
```

### 评论情感分析
```
Hey Claude——我刚添加了 "app-store-optimization" 技能。能帮我分析一下我应用（com.myapp.ios）最近的评论,找出最常见的用户抱怨和功能请求吗？
```

### 计算 ASO 得分
```
Hey Claude——我刚添加了 "app-store-optimization" 技能。能帮我计算一下我应用的整体 ASO 健康度得分,并提供具体的改进建议吗？
```

### 规划 A/B 测试
```
Hey Claude——我刚添加了 "app-store-optimization" 技能。我想对应用图标和首张截图做 A/B 测试。能帮我设计这个测试,并确定运行多长时间吗？
```

### 发布前检查清单
```
Hey Claude——我刚添加了 "app-store-optimization" 技能。能帮我生成一份全面的发布前检查清单,用于将我的应用提交到 Apple App Store 和 Google Play Store 吗？
```

## 脚本

### keyword_analyzer.py
分析关键词的搜索量、竞争程度和相关性。为主关键词和次关键词提供策略性建议。

**关键函数：**
- `analyze_keyword()`：分析单个关键词指标
- `compare_keywords()`：比较多个关键词
- `find_long_tail()`：发现长尾关键词机会
- `calculate_keyword_difficulty()`：评估竞争程度

### metadata_optimizer.py
优化标题、描述和关键词字段,并验证平台特定的字符数限制。

**关键函数：**
- `optimize_title()`：创建有吸引力、富含关键词的标题
- `optimize_description()`：生成以转化为导向的描述
- `optimize_keyword_field()`：最大化 Apple 的 100 字符关键词字段
- `validate_character_limits()`：确保符合平台限制
- `calculate_keyword_density()`：分析元数据中的关键词使用情况

### competitor_analyzer.py
分析顶级竞争对手的 ASO 策略并识别机会。

**关键函数：**
- `get_top_competitors()`：识别类别领导者
- `analyze_competitor_metadata()`：提取并分析竞争对手关键词
- `compare_visual_assets()`：评估图标和截图
- `identify_gaps()`：发现竞争机会

### aso_scorer.py
计算涵盖多个维度的综合 ASO 健康度得分。

**关键函数：**
- `calculate_overall_score()`：计算 0-100 的 ASO 得分
- `score_metadata_quality()`：评估标题、描述、关键词
- `score_ratings_reviews()`：评估评分质量与数量
- `score_keyword_performance()`：分析排名位置
- `score_conversion_metrics()`：评估展示到安装的转化率
- `generate_recommendations()`：提供优先级行动项

### ab_test_planner.py
规划并跟踪元数据和视觉素材的 A/B 测试。

**关键函数：**
- `design_test()`：创建测试假设与变量
- `calculate_sample_size()`：确定所需测试时长
- `calculate_significance()`：评估统计显著性
- `track_results()`：监控测试表现
- `generate_report()`：汇总测试结果

### localization_helper.py
管理多语言 ASO 优化策略。

**关键函数：**
- `identify_target_markets()`：推荐本地化优先级
- `translate_metadata()`：生成本地化元数据
- `adapt_keywords()`：研究特定语言区域的关键词
- `validate_translations()`：按语言检查字符数限制
- `calculate_localization_roi()`：评估本地化的影响

### review_analyzer.py
分析用户评论的情感、问题和功能请求。

**关键函数：**
- `analyze_sentiment()`：计算正面/负面/中性比例
- `extract_common_themes()`：识别频繁提及的主题
- `identify_issues()`：挖掘漏洞和用户投诉
- `find_feature_requests()`：提取期望的功能
- `track_sentiment_trends()`：随时间监控情感变化
- `generate_response_templates()`：创建评论回复草稿

### launch_checklist.py
生成全面的发布前及更新检查清单。

**关键函数：**
- `generate_prelaunch_checklist()`：完整的提交验证
- `validate_app_store_compliance()`：检查 Apple 指南
- `validate_play_store_compliance()`：检查 Google 政策
- `create_update_plan()`：规划更新节奏和功能
- `optimize_launch_timing()`：推荐发布日期
- `plan_seasonal_campaigns()`：识别季节性机会

## 最佳实践

### 关键词研究
1. **搜索量与竞争的平衡**：在高搜索量关键词与可实现的排名之间取得平衡
2. **相关性优先**：只针对与你的应用真正相关的关键词
3. **长尾策略**：纳入竞争较低的 3-4 词短语
4. **持续研究**：关键词趋势会变化——每季度做一次研究
5. **竞争对手关键词**：不要盲目复制;要确保与你自身功能的相关性

### 元数据优化
1. **关键词前置**：将最重要的关键词放在标题/描述的前面
2. **自然语言**：先为人写,再为 SEO 写
3. **功能带来的好处**：聚焦用户利益,而非单纯的功能列举
4. **系统化 A/B 测试**：系统地测试标题、描述、截图
5. **定期更新**：每次重大更新时刷新元数据
6. **字符数限制**：用好每一个字符——不要浪费宝贵的空间
7. **Apple 关键词字段**：不要有复数形式、重复项,逗号之间也不要有空格

### 视觉素材
1. **图标**：在小尺寸下（60x60px）必须仍可辨识
2. **截图**：前 2-3 张至关重要——大多数用户不会滑动查看更多
3. **说明文字**：用截图说明文字来讲述你的价值故事
4. **一致性**：视觉风格要与应用设计相匹配
5. **A/B 测试图标**：图标是单一最重要的视觉元素

### 评论与评分
1. **快速响应**：在 24-48 小时内回复评论
2. **专业语气**：始终保持礼貌,即使面对负面评论
3. **解决问题**：展示你正在积极修复被报告的问题
4. **感谢支持者**：对正面评论给予认可
5. **策略性请求**：在正向体验之后请求评分

### 发布策略
1. **软发布**：考虑先在较小市场发布
2. **公关时机**：将媒体报道与发布时间协调一致
3. **频繁更新**：初期的频繁更新能体现活跃开发
4. **密切监控**：发布后头两周每天跟踪指标
5. **快速迭代**：立即修复关键问题

### 本地化
1. **优先确定市场**：从英语、西班牙语、中文、法语、德语开始
2. **母语者**：使用专业翻译,而非机器翻译
3. **文化适配**：某些功能在不同文化中的接受度不同
4. **本地测试**：在发布前让母语者进行审阅
5. **衡量投资回报**：按语言区域跟踪下载量以评估影响

## 可选的外部研究工具

仅在工作流需要当前市场输入,或需要对方向性估算做二次核验时才使用外部工具。将第三方估算数据视为近似值,并注明获取日期。

- [AppNiche Revenue Checker](https://getappniche.com/tools/app-revenue-checker) - 免费的 iOS App Store 收入基准工具,用于竞品优先级排序和 ASO 得分上下文参考。
- [AppNiche ASO Keyword Opportunity Checker](https://getappniche.com/tools/app-store-keyword-tool) - 免费的 iOS 关键词机会检测工具,用于关键词研究和 Apple 关键词字段规划。

## 局限性

### 数据依赖
- 关键词搜索量估算是近似值（Apple/Google 并未提供官方数据）
- 对私有应用的竞争对手数据可能不完整
- 评论分析仅限于公开评论（无法获取私下反馈）
- 新应用可能没有历史数据

### 平台限制
- Apple App Store 关键词变更需要重新提交应用（推广文本除外）
- Google Play Store 元数据变更需要 1-2 小时才能完成索引
- A/B 测试需要足够的流量才能达到统计显著性
- 商店算法属于专有机制,会在不通知的情况下变更

### 行业差异
- ASO 基准因类别差异很大（游戏类 vs. 工具类）
- 季节性对不同类别的影响方式不同
- 不同地理市场的竞争格局不同
- 文化偏好会影响不同国家的实际效果

### 范围边界
- 不包括付费用户获取策略（Apple Search Ads、Google Ads）
- 不涉及应用开发或 UI/UX 优化
- 不包括应用分析系统的实现（使用 Firebase、Mixpanel 等）
- 不处理应用提交的技术问题（配置文件、证书）

### 何时不应使用本技能
- 针对 Web 应用（适用不同的 SEO 策略）
- 针对未上架公共商店的企业内部应用
- 针对仅处于 beta/TestFlight 阶段的应用
- 如果你需要付费广告策略（请改用营销类技能）

## 与其他技能的集成

本技能可与以下技能很好地配合使用：
- **内容策略技能**：用于撰写应用描述和营销文案
- **分析技能**：用于分析下载量和参与度数据
- **本地化技能**：用于管理多语言内容
- **设计技能**：用于创建优化的视觉素材
- **营销技能**：用于协调更大范围的发布活动

## 版本与更新

本技能基于截至 2025 年 11 月的 Apple App Store 和 Google Play Store 的当前要求。商店政策和最佳实践会不断演变——在重大发布前请核实当前要求。

**需要关注的重要更新：**
- Apple App Store Connect 更新（apple.com/app-store/review/guidelines）
- Google Play Console 更新（play.google.com/console/about/guides/releasewithconfidence）
- iOS/Android 版本采用率（影响设备测试）
- 商店算法变化（关注 ASO 博客和社区）

## 何时使用
本技能适用于执行概述中所描述的工作流或操作。
