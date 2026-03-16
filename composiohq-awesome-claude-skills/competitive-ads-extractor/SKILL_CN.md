---
name: competitive-ads-extractor
description: 从广告库（Facebook、LinkedIn 等）中提取和分析竞争对手的广告，以了解哪些消息传递、问题和创意方法正在发挥作用。帮助启发和改进您自己的广告活动。
---

# 竞争对手广告提取器

此技能从广告库中提取您竞争对手的广告，并分析哪些内容有效——他们强调的问题、他们针对的用例以及引起共鸣的文案/创意。

## 何时使用此技能

- 研究竞争对手的广告策略
- 为自己的广告寻找灵感
- 了解市场定位
- 识别成功的广告模式
- 分析有效的消息传递
- 发现新的用例或痛点
- 使用经过验证的概念规划广告活动

## 此技能的功能

1. **提取广告**：从 Facebook Ad Library、LinkedIn 等抓取广告
2. **捕获屏幕截图**：保存所有广告的视觉副本
3. **分析消息传递**：识别问题、用例和价值主张
4. **分类广告**：按主题、受众或格式分组
5. **识别模式**：发现常见的成功方法
6. **提供见解**：解释为什么某些广告可能表现良好

## 如何使用

### 基本提取

```
Extract all current ads from [Competitor Name] on Facebook Ad Library
```

```
Scrape ads from [Company] and analyze their messaging
```

### 特定分析

```
Get all ads from [Competitor] focusing on their messaging 
about [specific problem]. What pain points are they highlighting?
```

### 竞争集合

```
Extract ads from these 5 competitors: [list]. 
Compare their approaches and tell me what's working.
```

### 特定平台

```
Get LinkedIn ads from [Competitor] and analyze their 
B2B positioning strategy
```

## 示例

**用户**："Extract ads from Notion on Facebook Ad Library and tell me what messaging is working for them."

**流程**：
```
Accessing Facebook Ad Library...
Searching for: Notion
Found: 23 active ads

Extracting screenshots...
[████████████████████] 100%

Saved to: competitor-ads/notion/
- ad-001-collaboration.png
- ad-002-productivity.png
- ad-003-templates.png
...

Analyzing messaging...
```

**输出**：
```
# Notion 广告分析

## 概述
- 总广告数：23 个活跃
- 主要主题：生产力（35%）、协作（30%）、
  模板（20%）、AI 功能（15%）
- 广告格式：静态图像（60%）、视频（40%）
- CTA 模式："免费试用"、"开始使用"

## 他们强调的关键问题

1. **信息分散**（8 个广告）
   文案："停止在 10 个不同工具之间切换"
   为什么有效：直接解决许多团队面临的痛点

2. **会议过载**（5 个广告）
   文案："用异步更新替换不必要的会议"
   为什么有效：后 COVID 远程工作痛点

3. **文档丢失**（4 个广告）
   文案："再也不用问'那个文档在哪里？'"
   为什么有效：普遍的工作场所挫折

## 成功的创意模式

### 模式 1：前后对比
- 展示混乱的工具环境 → 干净的 Notion 工作区
- 用于 6 个表现良好的广告
- 视觉隐喻立即清晰

### 模式 2：功能展示
- 实际产品使用的 GIF
- 在 5 秒内展示特定功能
- 用于新功能（AI、模板）

### 模式 3：社会证明
- "加入 2000 万用户"消息
- 客户标志
- 用于 4 个针对企业的广告

## 有效的文案

最佳标题：
1. "您团队的知识，终于集中在一个地方"
   → 关注收益，直接解决痛苦
   
2. "一体化工作区"
   → 清晰定位，广泛吸引力
   
3. "真正帮助您工作的 AI"
   → 解决 AI 怀疑论，实用角度

最佳正文文案模式：
- 短句（10 字以下）
- 关注结果而非功能
- 包含具体数字（"减少 50% 的会议"）

## 受众定位洞察

基于广告变体：
- 初创公司创始人：个人生产力角度
- 团队领导：协作和对齐
- 企业：安全性和合规性提及
- 学生：免费计划、模板、组织

## 对您广告的建议

1. **测试"工具蔓延"痛点**
   → 基于他们广告频率的强烈共鸣

2. **使用产品截图而非抽象视觉**
   → 所有表现最佳的广告都展示实际 UI

3. **以问题为导向，而非解决方案**
   → "厌倦了 X？"比"介绍 Y"表现更好

4. **保持文案在 100 字符以下**
   → 他们最短的广告似乎最频繁

5. **测试前后视觉格式**
   → 他们创意中的已验证模式

## 保存的文件
- 所有广告：~/competitor-ads/notion/
- 分析：~/competitor-ads/notion/analysis.md
- 最佳表现者：~/competitor-ads/notion/top-10/
```

**灵感来源**：Sumant Subrahmanya 在 Lenny's Newsletter 中的用例

## 您可以学习的内容

### 消息传递分析
- 他们强调的问题
- 他们如何与竞争对手定位
- 引起共鸣的价值主张
- 目标受众细分

### 创意模式
- 有效的视觉风格
- 视频与静态图像表现
- 配色方案和品牌
- 布局模式

### 文案公式
- 标题结构
- 行动号召模式
- 长度和语气
- 情感触发器

### 活动策略
- 季节性活动
- 产品发布方法
- 功能公告策略
- 重定向模式

## 最佳实践

### 法律与道德
✓ 仅用于研究和灵感
✓ 不要直接复制广告
✓ 尊重知识产权
✓ 使用洞察来指导原创创意
✗ 不要剽窃文案或窃取设计

### 分析提示
1. **寻找模式**：哪些主题重复？
2. **随时间跟踪**：每月保存广告以查看演变
3. **测试假设**：为您的品牌调整成功模式
4. **按受众细分**：不同目标的不同消息
5. **比较平台**：LinkedIn 与 Facebook 消息传递不同

## 高级功能

### 趋势跟踪
```
Compare [Competitor]'s ads from Q1 vs Q2. 
What messaging has changed?
```

### 多竞争对手分析
```
Extract ads from [Company A], [Company B], [Company C]. 
What are the common patterns? Where do they differ?
```

### 行业基准
```
Show me ad patterns across the top 10 project management 
tools. What problems do they all focus on?
```

### 格式分析
```
Analyze video ads vs static image ads from [Competitor]. 
Which gets more engagement? (if data available)
```

## 常见工作流程

### 广告活动规划
1. 提取竞争对手广告
2. 识别成功模式
3. 注意他们消息传递中的差距
4. 头脑风暴独特角度
5. 起草测试广告变体

### 定位研究
1. 获取 5 个竞争对手的广告
2. 映射他们的定位
3. 找到未被充分服务的角度
4. 开发差异化消息传递
5. 测试与他们的方法对比

### 创意灵感
1. 按主题提取广告
2. 分析视觉模式
3. 注意颜色和布局趋势
4. 调整成功模式
5. 创建原创变体

## 成功提示

1. **定期监控**：每月检查变化
2. **广泛研究**：也查看相邻竞争对手
3. **保存一切**：建立参考库
4. **测试洞察**：运行自己的实验
5. **跟踪表现**：A/B 测试受启发的概念
6. **保持原创**：用于灵感，而非复制
7. **多个平台**：比较 Facebook、LinkedIn、TikTok 等

## 输出格式

- **屏幕截图**：所有广告保存为图像
- **分析报告**：洞察的 Markdown 摘要
- **电子表格**：包含广告文案、CTA、主题的 CSV
- **演示文稿**：表现最佳者的视觉幻灯片
- **模式库**：按方法分类

## 相关用例

- 为您的活动编写更好的广告文案
- 了解市场定位
- 发现您消息传递中的内容差距
- 为您的产品发现新的用例
- 规划产品营销策略
- 启发社交媒体内容