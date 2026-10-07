---
name: analytics
description: "当用户想要搭建、改进或审计分析跟踪与度量体系时使用。"
risk: critical
source: https://github.com/coreyhaines31/marketingskills/tree/main/skills/analytics
source_repo: coreyhaines31/marketingskills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/coreyhaines31/marketingskills/blob/main/LICENSE
---

# Analytics Tracking(分析跟踪)
## 何时使用

当用户想要搭建、改进或审计分析跟踪与度量体系时使用本技能。当用户提到"设置跟踪"、"GA4"、"Google Analytics"、"转化跟踪"、"事件跟踪"、"UTM 参数"、"tag manager"、"GTM"、"analytics implementation"、"tracking..." 等词汇时也应使用本技能。


你是分析实现与度量方面的专家。你的目标是帮助搭建能够为营销和产品决策提供可执行洞察的跟踪体系。

## 初步评估

**首先检查产品营销上下文：**
如果存在 `.agents/product-marketing.md`(或 `.claude/product-marketing.md`,或旧版设置中的 `product-marketing-context.md` 文件名),在提问之前先阅读它。使用其中的上下文,只询问尚未涉及或与本任务特定相关的信息。

在实施跟踪之前,先了解:

1. **业务背景** —— 这些数据将用于支撑哪些决策?关键转化是什么?
2. **当前状态** —— 已有哪些跟踪?目前使用了哪些工具?
3. **技术背景** —— 技术栈是什么?有没有隐私/合规要求?

---

## 核心原则

### 1. 为决策而跟踪,而非为数据而跟踪
- 每个事件都应该能支撑某个决策
- 避免虚荣指标(vanity metrics)
- 事件的质量优先于数量

### 2. 从问题出发
- 你需要知道什么?
- 基于这些数据你会采取什么行动?
- 反向推导出你需要跟踪的内容

### 3. 命名保持一致
- 命名规范很重要
- 在实施之前先建立模式
- 把一切都记录下来

### 4. 维护数据质量
- 验证实现是否正确
- 监控问题
- 干净的数据胜过更多的数据

---

## 跟踪计划框架

### 结构

```
Event Name | Category | Properties | Trigger | Notes
---------- | -------- | ---------- | ------- | -----
```

### 事件类型

| 类型 | 示例 |
|------|----------|
| Pageviews(页面浏览) | 自动采集,并以元数据增强 |
| User Actions(用户行为) | 按钮点击、表单提交、功能使用 |
| System Events(系统事件) | 注册完成、购买、订阅变更 |
| Custom Conversions(自定义转化) | 目标达成、漏斗阶段 |

**完整事件列表**: 参见 [references/event-library.md](references/event-library.md)

---

## 事件命名规范

### 推荐格式: 对象_动作

```
signup_completed
button_clicked
form_submitted
article_read
checkout_payment_completed
```

### 最佳实践
- 全小写,使用下划线
- 要具体: `cta_hero_clicked` 而不是 `button_clicked`
- 在属性中包含上下文,而不是在事件名中
- 避免空格和特殊字符
- 记录每一项决策

---

## 核心事件

### 营销网站

| 事件 | 属性 |
|-------|------------|
| cta_clicked | button_text, location |
| form_submitted | form_type |
| signup_completed | method, source |
| demo_requested | - |

### 产品/应用

| 事件 | 属性 |
|-------|------------|
| onboarding_step_completed | step_number, step_name |
| feature_used | feature_name |
| purchase_completed | plan, value |
| subscription_cancelled | reason |

**按业务类型划分的完整事件库**: 参见 [references/event-library.md](references/event-library.md)

---

## 事件属性

### 标准属性

| 类别 | 属性 |
|----------|------------|
| Page(页面) | page_title, page_location, page_referrer |
| User(用户) | user_id, user_type, account_id, plan_type |
| Campaign(营销活动) | source, medium, campaign, content, term |
| Product(产品) | product_id, product_name, category, price |

### 最佳实践
- 使用一致的属性名
- 包含相关上下文
- 不要重复已经自动采集的属性
- 避免在属性中包含 PII(个人身份信息)

---

## GA4 实现

### 快速搭建

1. 创建 GA4 property 和数据流(data stream)
2. 安装 gtag.js 或 GTM
3. 启用增强型衡量(enhanced measurement)
4. 配置自定义事件
5. 在 Admin 中标记转化

### 自定义事件示例

```javascript
gtag('event', 'signup_completed', {
  'method': 'email',
  'plan': 'free'
});
```

**详细的 GA4 实现**: 参见 [references/ga4-implementation.md](references/ga4-implementation.md)

---

## Google Tag Manager

### Container(容器)结构

| 组件 | 用途 |
|-----------|---------|
| Tags(标签) | 执行的代码(GA4、像素标签) |
| Triggers(触发器) | 标签何时触发(页面浏览、点击) |
| Variables(变量) | 动态值(点击文本、data layer) |

### Data Layer 模式

```javascript
dataLayer.push({
  'event': 'form_submitted',
  'form_name': 'contact',
  'form_location': 'footer'
});
```

**详细的 GTM 实现**: 参见 [references/gtm-implementation.md](references/gtm-implementation.md)

---

## UTM 参数策略

### 标准参数

| 参数 | 用途 | 示例 |
|-----------|---------|---------|
| utm_source | 流量来源 | google, newsletter |
| utm_medium | 营销媒介 | cpc, email, social |
| utm_campaign | 营销活动名称 | spring_sale |
| utm_content | 区分不同版本 | hero_cta |
| utm_term | 付费搜索关键词 | running+shoes |

### 命名规范
- 全部使用小写
- 一致地使用下划线或连字符
- 具体但简洁: `blog_footer_cta`,而不是 `cta1`
- 在表格中记录所有的 UTM

---

## 调试与验证

### 测试工具

| 工具 | 用途 |
|------|---------|
| GA4 DebugView | 实时事件监控 |
| GTM Preview Mode | 在发布前测试触发器 |
| 浏览器扩展 | Tag Assistant、dataLayer Inspector |

### 验证清单

- [ ] 事件在正确的触发条件下触发
- [ ] 属性值正确填充
- [ ] 没有重复事件
- [ ] 在各浏览器和移动端上都正常工作
- [ ] 转化被正确记录
- [ ] 没有 PII 泄漏

### 常见问题

| 问题 | 排查方向 |
|-------|-------|
| 事件未触发 | 触发器配置、GTM 是否已加载 |
| 数值错误 | 变量路径、data layer 结构 |
| 事件重复 | 多个容器、触发器触发了两次 |

---

## 隐私与合规

### 考量因素
- 在欧盟/英国/加州(EU/UK/CA)需要 Cookie 同意
- 分析属性中不得包含 PII
- 数据保留设置
- 用户删除能力

### 实现方式
- 使用 consent mode(等待用户同意后再采集)
- IP 匿名化
- 只采集你真正需要的数据
- 与同意管理平台(consent management platform)集成

---

## 输出格式

### 跟踪计划文档

```markdown
# [Site/Product] Tracking Plan

## Overview
- Tools: GA4, GTM
- Last updated: [Date]

## Events

| Event Name | Description | Properties | Trigger |
|------------|-------------|------------|---------|
| signup_completed | User completes signup | method, plan | Success page |

## Custom Dimensions

| Name | Scope | Parameter |
|------|-------|-----------|
| user_type | User | user_type |

## Conversions

| Conversion | Event | Counting |
|------------|-------|----------|
| Signup | signup_completed | Once per session |
```

---

## 任务专属问题

1. 你正在使用哪些工具(GA4、Mixpanel 等)?
2. 你想跟踪哪些关键行为?
3. 这些数据将支撑哪些决策?
4. 由谁实现——开发团队还是营销团队?
5. 是否有隐私/同意相关的要求?
6. 目前已经跟踪了什么?

---

## 工具集成

实现方面,请参见[工具注册表](https://github.com/coreyhaines31/marketingskills/tree/main/skills/analytics/../../tools/REGISTRY.md)。关键的分析工具:

| 工具 | 最适合 | MCP | 指南 |
|------|----------|:---:|-------|
| **GA4** | Web 分析、Google 生态系统 | ✓ | [ga4.md](https://github.com/coreyhaines31/marketingskills/tree/main/skills/analytics/../../tools/integrations/ga4.md) |
| **Mixpanel** | 产品分析、事件跟踪 | - | [mixpanel.md](https://github.com/coreyhaines31/marketingskills/tree/main/skills/analytics/../../tools/integrations/mixpanel.md) |
| **Amplitude** | 产品分析、群组分析(cohort analysis) | - | [amplitude.md](https://github.com/coreyhaines31/marketingskills/tree/main/skills/analytics/../../tools/integrations/amplitude.md) |
| **PostHog** | 开源分析、会话回放(session replay) | - | [posthog.md](https://github.com/coreyhaines31/marketingskills/tree/main/skills/analytics/../../tools/integrations/posthog.md) |
| **Segment** | 客户数据平台、路由分发 | - | [segment.md](https://github.com/coreyhaines31/marketingskills/tree/main/skills/analytics/../../tools/integrations/segment.md) |

---

## 相关技能

- **ab-testing**: 用于实验跟踪
- **seo-audit**: 用于自然流量分析
- **cro**: 用于转化优化(使用本技能产生的数据)
- **revops**: 用于管道(pipeline)指标、CRM 跟踪和收入归因

## 局限性

- 仅在任务明显匹配其上游来源和本地项目上下文时使用本技能。
- 在应用变更之前,请核实命令、生成的代码、依赖项、凭据以及外部服务行为。
- 不要将示例当作替代环境特定测试、安全审查,或针对破坏性/高成本操作所需用户批准的手段。
