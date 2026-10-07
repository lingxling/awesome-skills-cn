---
name: advanced-analytics-dashboard
description: '仪表盘指标登记册：指标、来源模块、公式、周期、数值、目标、趋势、负责人和最后更新时间，可按需输出为 CSV、SQL、JSON Schema 或 Notion。用于 KPI 仪表盘。'
category: business
risk: safe
source: self
source_type: self
date_added: '2026-09-26'
author: WHOISABHISHEKADHIKARI
tags:
- sme
- business
- operations
- database
- csv
- notion
- sql
- analyze
tools: []
source_repo: WHOISABHISHEKADHIKARI/sme-ops-system-builder
---

# 高级分析仪表盘

**它是什么：** 一份记录分析指标及其来源的登记册；它不会训练或运行预测模型。

## 概述

为眼前的业务梳理出最小可用的**高级分析仪表盘**方案，且仅在被要求时才进行构建。默认输出是一份简短的建议，而不是一张电子表格。产物——CSV、SQL DDL、JSON Schema、Notion 映射——按需生成，并且都源自同一份字段清单，因此不会互相偏离。

所属层级：第 9 层：分析（Analyze）。适用阶段：规模化阶段。表代码：不适用。

## 何时使用本技能

- 分析仪表盘
- 预测性指标
- KPI 仪表盘模板
- 业务指标仪表盘

当用户说"predictive insights"（预测性洞察），或描述同样的流程正发生在电子表格、文档或某人的收件箱里时，也应使用本技能。

以下情况请勿使用：薪资计算、税务申报或法律建议。本技能只生成空模板——绝不持有或处理真实的员工或客户数据。

## 工作方式

遵循共享的执行契约。下面的模块专属规则仅定义领域字段、决策、计算和安全约束。

### 步骤 1 - 识别意图

在提出任何问题之前，先阅读请求并判断意图。

- "set up"、"build" 或 "create" -> 用户想要产物；进入步骤 2。
- "our process is ..." 或 "it is in a sheet" -> 用户想迁移现有流程；先记录下来，然后进入步骤 2。
- "is this right"、"review" 或 "audit" -> 用户想要检查，而不是构建；根据他们分享的内容作答。
- "how do I ..." -> 咨询类问题；直接回答，仅在有帮助时才提议构建。

只有当这是最有价值的缺失信息时才提问；否则不要开场白，直接继续：

> **Q:** 这个仪表盘打算支持哪项决策？

### 步骤 2 - 只询问缺失的信息

跳过用户在之前任何消息中已经回答过的内容。其余问题一次只问一个，一旦剩下的答案不会改变输出，就立即停止。

- **决策** - 哪项决策？/ 谁来做？/ 多久做一次？
- **数据** - 哪些数据源？/ 有多少行？/ 需要多新鲜？
- **度量** - 哪些指标？/ 有多少个？/ 与什么对比？
- **现行流程** - 目前有仪表盘吗？/ 是手工的还是基于工具的？/ 是否可信？
- **期望结果** - 你需要什么？/ 一套指标、一个布局，还是两者都要？

绝不要编造答案。如果用户不知道，就记为未知并继续。

### 步骤 3 - 保留内部上下文

以如下结构保存答案。它仅供内部使用——除非用户询问，否则不向用户展示，且绝不包含用户未提供的值。

```yaml
module: advanced-analytics-dashboard
intent: null            # setup | advice | review | fix | build | convert | export
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Decision": null
  "Data": null
  "Measures": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion | xlsx - requested formats only
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### 步骤 4 - 推荐最小可行工作流

如果用户请求了某个产物，则在解决关键缺失信息后进行构建。否则，给出一份简短的建议，并提供相关产物。

**推荐方案：** 从决策出发，然后为决策的每个部分添加一个指标。布局是靠后的决定，很少是问题所在。

**为何选择这一方案：** 仪表盘失败是因为指标泛滥，而不是设计问题。先确定决策和指标数量，布局自然随之而来。

**工作流：** 定义指标 → 来源数据 → 计算 → 刷新 → 决策复盘

### 步骤 5 - 仅在被要求时构建

一旦用户提出要求，就根据已确认的上下文推导字段，并输出所请求的产物。对于机器可读文本，行文要放在数据之外；对于文件，提供可用的链接。重大的校验失败或局限性应单独报告。

**所选的 Notion 输出由 `notion-manual-import` 渲染，因此请将 Notion 这一步交给它。** 当用户选择 Notion 时，将该步骤交给 @notion-manual-import：它持有 CSV、属性映射、导入步骤和验证清单，并且渲染下方的字段参考，而不是自己定义一张表。不要在此处重述映射，也不要即兴发挥导入步骤。手动 CSV 和映射输出无需连接。对于要求的工作区更改，请遵循共享契约：在写入之前，先核实实际的工具访问权限和目标。用户说"已连接"并不构成工具层面的证据。绝不要索要 Notion 的密码或令牌。

对于兼容 Excel 的 CSV，请使用带字节顺序标记（BOM）的 UTF-8，以便 Excel 能正确打开文本。CSV 不是 `.xlsx` 工作簿；仅在用户要求工作簿时才创建 `.xlsx`。CSV 不带类型信息，因此在输出之后，要指出哪些列需要应用数字、日期或货币格式。

```csv
Metric,Category,Source Module,Formula or Method,Period,Value,Target,Trend,Owner,Last Updated,Metric ID
Net revenue,General,Invoices & Billing,"Revenue invoiced minus credits, divided by active clients.",2026-03,1000,100,Up 3 months running,Example Owner,2026-01-15,
```

```sql
CREATE TABLE advanced_analytics_dashboard (
  metric VARCHAR(255),
  category VARCHAR(100) NOT NULL,
  source_module VARCHAR(255),
  formula_or_method VARCHAR(255),
  period VARCHAR(255),
  value NUMERIC NOT NULL,
  target NUMERIC NOT NULL,
  trend VARCHAR(255),
  owner VARCHAR(255),
  last_updated DATE NOT NULL,
  metric_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Advanced Analytics Dashboard",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Metric": { "type": "string" },
      "Category": { "type": "string" },
      "Source Module": { "type": "string" },
      "Formula or Method": { "type": "string" },
      "Period": { "type": "string" },
      "Value": { "type": "number" },
      "Target": { "type": "number" },
      "Trend": { "type": "string" },
      "Owner": { "type": "string" },
      "Last Updated": { "type": "string", "format": "date" },
      "Metric ID": { "type": "integer" }
  },
  "required": [
      "Category",
      "Value",
      "Target",
      "Last Updated"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Metric | Title | Use as the database title |
| Category | Select (add options after import) | Convert to Select, add options: "General", "Operations", "Finance", "People", "Compliance" |
| Source Module | Text | Leave as Text |
| Formula or Method | Text | Leave as Text |
| Period | Text | Leave as Text |
| Value | Number | Convert to Number |
| Target | Number | Convert to Number |
| Trend | Text | Leave as Text |
| Owner | Text | Leave as Text |
| Last Updated | Date | Convert to Date |
| Metric ID | Text (preserve source ID) | Keep imported IDs as Text; optionally add a separate Unique ID property |
```

以上各行仅为文档示例。除非用户明确要求示例，否则请输出空模板。金额保持为 `currency`，日期保持为 `date`，指向其他表的内容保持为 `relation`。

## 字段参考

| # | 字段 | 类型 | SQL | JSON Schema | Notion | CSV 示例 |
|---:|---|---|---|---|---|---|
| 1 | Metric | `text` | `VARCHAR(255)` | `string` | Text | `Net revenue` |
| 2 | Category | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `General` |
| 3 | Source Module | `text` | `VARCHAR(255)` | `string` | Text | `Invoices & Billing` |
| 4 | Formula or Method | `text` | `VARCHAR(255)` | `string` | Text | `Revenue invoiced minus credits, divided by active clients.` |
| 5 | Period | `text` | `VARCHAR(255)` | `string` | Text | `2026-03` |
| 6 | Value | `number` | `NUMERIC` | `number` | Number | `1000` |
| 7 | Target | `number` | `NUMERIC` | `number` | Number | `100` |
| 8 | Trend | `text` | `VARCHAR(255)` | `string` | Text | `Up 3 months running` |
| 9 | Owner | `text` | `VARCHAR(255)` | `string` | Text | `Example Owner` |
| 10 | Last Updated | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 11 | Metric ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (preserve source ID) | `(blank)` |

## 选项值

**Category**

```
General | Operations | Finance | People | Compliance
```

## 关联关系

关联字段：无

## 示例

**提示词**

```
We have a dashboard with 30 tiles that nobody uses.
```

**先了解上下文** —— 每条消息一个问题，不重复已回答的内容：

> **Q:** 支持哪项决策？
> **A:** 哪些项目需要关注。
>
> **Q:** 数据来源？
> **A:** 项目跟踪工具和会计系统。
>
> **Q:** 多久一次？
> **A:** 每周。

**推荐的下一步** —— 只是提议，不直接构建：

> 从决策出发，然后为决策的每个部分添加一个指标。布局是靠后的决定，很少是问题所在。
>
> 工作流：定义指标 → 来源数据 → 计算 → 刷新 → 决策复盘
>
> 需要我为此生成 CSV、SQL、JSON Schema 和 Notion 映射吗？

## 最佳实践

- 被要求时就构建；对于仅咨询的请求，给出建议并提议构建。
- 每条消息只问一个问题。批量收集信息读起来像一张表单，人们只会去猜答案。
- 在 CSV 和 JSON 之间保持显示名称一致；记录规范化的 SQL 标识符。
- 凡是指向另一张表的内容使用 `relation`，只有自由文本才使用 `text`。
- 金额字段是 `currency`，绝不是 `text`。日期是 `date`，绝不是自由文本。
- 如果用户要求示例行，请让它明显是假的，以免有人把它当作真实数据导入。

## 局限性

- 预测需要提供的数据、指定的模型、评估证据和不确定性。
  仅凭此模板不会产生任何预测或经过验证的洞察。

- 仅为空模板。它不计算薪资、税款、假期余额或 KPI。
- Notion 关联需要先导入两个数据库，关联列才能解析。
- 选项值只是一组起始集合。请重命名以匹配业务的实际说法。
- 没有自动化、提醒或同步功能。这些需要集成层。
- 不会连接到源系统、清洗数据，也不保证指标的准确性。
- 在其驱动真实决策之前，仍需进行法律、税务和人力资源审查。

## 安全与保障说明

- 绝不填写真实的姓名、薪资、医疗或银行数据。仅使用占位符。
- 将示例行标注为合成数据，并保持银行信息被屏蔽。
- 本地读取、生成命令和验证属于所请求产物构建的一部分。外部写入、消息发送、资源开通和发布需要针对该操作和目标的授权；已有的明确授权无需重复。
- 如果提供了敏感数据，避免重复不必要的标识符。仅使用所请求审查所需的内容；保持生成的模板为空。不要声称已从对话或服务存储中删除。
- 隐私、法律和纪律类案件在采取任何行动之前，需要有资质的人工审核。

## 常见陷阱

- **问题：** 把静态映射描述成已完成的工作区构建。
  **解决：** 无需连接即可交付手动映射；只有在经授权的工具操作成功后，才声称已进行了实时更改。
- **问题：** 在一条消息中问了全部六个问题。
  **解决：** 只问一个，等待回答，并去掉第一个答案已经涵盖的问题。
- **问题：** 用户只要一张表，却构建了完整的系统。
  **解决：** 构建所请求的内容；母技能另行提及。
- **问题：** 四种产物互相偏离。
  **解决：** 四者都从本文件中的字段清单推导，绝不手工编写。
- **问题：** Notion 导入后每一列都显示为 Text。
  **解决：** 这是预期行为。导入之后，一次性应用属性映射表即可。

## 相关技能

- [Module Catalog](https://github.com/sickn33/agentic-awesome-skills/blob/main/CATALOG.md) - 找到相关模块，然后阅读其技能。
- @people-directory - 大多数模块所关联的员工主记录。
- @notification-reminder-hub - 将本模块中的到期日期转化为提醒。

## 可复用提示词

```
I want to set up predictive insights for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```
