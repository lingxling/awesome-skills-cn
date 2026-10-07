---
name: alumni-re-hire-tracker
description: '离职员工与返聘登记册:原职位、最后工作日、返聘资格、当前雇主与重新联系日期,可按需生成 CSV、SQL、JSON Schema 或 Notion 格式。用于校友/离职员工外联。'
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
- exit
tools: []
source_repo: WHOISABHISHEKADHIKARI/sme-ops-system-builder
---

# Alumni & Re-hire Tracker(离职员工与返聘跟踪器)

**它是什么:** 离职员工。

## Overview

针对眼前这家企业,摸索出最小可用的 **Alumni & Re-hire Tracker(离职员工与返聘跟踪器)** 设置方案,
只在被要求时才构建。默认输出是一条简短的建议,而不是一份
表格。各类产物——CSV、SQL DDL、JSON Schema、Notion 映射——是根据请求生成的,
均来自同一份字段清单,因此它们不会相互脱节。

层级:第 10 层:离职。适用阶段:Scale(规模化)阶段。表代码:n/a。

## When to Use This Skill

- alumni tracker(校友跟踪器)
- rehire tracker(返聘跟踪器)
- former employee register(前员工登记册)
- past employee list(过往员工名单)

当用户说"离职员工"时,或描述了同样的流程正在某个
表格、文档或某人的收件箱中发生时,也使用该技能。

不要将其用于:薪资计算、报税或法律咨询。该技能仅生成
空白模板——它从不保存或处理真实的员工或客户数据。

## How It Works

遵循共享的执行约定。下面特定于模块的规则仅定义领域字段、决策、计算和安全约束。

### Step 1 — 识别意图

阅读请求并在询问任何问题之前先确定意图。

- "set up" 或 "build" 或 "create" -> 用户想要产物;进入第 2 步。
- "our process is ..." 或 "it is in a sheet" -> 用户想要迁移现有流程;先记录下来,再进入第 2 步。
- "is this right" 或 "review" 或 "audit" -> 用户想要的是检查,而不是构建;根据其提供的内容回答。
- "how do I ..." -> 咨询类问题;直接回答,仅在有帮助时再提供构建选项。

仅当以下为最具价值的缺失信息时才提问;否则无需开场白直接进行:

> **问:** 有多少人已经离开公司?

### Step 2 — 只问缺失的信息

跳过用户在之前任何消息中已经回答的内容。逐一询问剩余的内容,
一旦剩余答案不会再改变输出结果,就停止提问。

- **Alumni(离职员工)** —— 有多少离职员工?/多久以前?/有没有可联系的熟人?
- **Fit(适配度)** —— 为什么要返聘?/他们担任过什么职位?/有哪些值得记录的技能?
- **Reach(联系方式)** —— 如何保持联系?/有书面同意记录吗?/多久联系一次?
- **Current process(现有流程)** —— 目前有记录吗?/LinkedIn 还是表格?/哪些会被遗漏?
- **Outcome(所需结果)** —— 需要什么?/一份离职员工登记册、一个返聘视图,还是两者都要?

绝不要编造答案。如果用户不知道,记为未知并继续。

### Step 3 — 保存内部上下文

按以下结构保存这些答案。它仅在内部使用——除非用户要求,否则不会展示给用户,
并且绝不会包含用户未曾给出的值。

```yaml
module: alumni-re-hire-tracker
intent: null            # setup | advice | review | fix | build | convert | export
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Alumni": null
  "Fit": null
  "Reach": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion | xlsx - requested formats only
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 — 推荐最小化工作流

如果用户已请求某个产物,在解决关键缺失信息后构建它。否则给出简短建议,并提供相应产物的选项。

**推荐方法:** 保留一份小型的离职员工记录,包含离职日期、所任职位,以及一行关于离职原因的说明,并仅在有职位空缺时才重新查看它。

**为什么选这个方案:** 离职员工记录只有在有某种事件触发重新查看时才值得维护。把它绑定到职位空缺上,而不是绑定到一份常规简讯上。

**工作流:** 记录离职 → 保留详情 → 职位空缺时考虑返聘 → 重新入职或建立联系

### Step 5 — 仅在请求时构建

一旦用户提出要求,从已确认的上下文中推导字段并生成
所请求的产物。对于机器可读文本,将行文内容放在数据之外;对于文件,
提供一个可用的链接。单独报告重大的验证失败或限制。

**选定的 Notion 输出由 `notion-manual-import` 渲染,因此将 Notion
步骤路由到那里。** 当用户选择 Notion 时,把该步骤交给
@notion-manual-import:它持有 CSV、属性
映射、导入步骤和验证清单,并渲染下方的字段参考,
而不是自行定义一个表。不要在此重复映射内容,也不要自行改编导入步骤。手动 CSV 和映射输出无需连接。
对于所请求的工作区更改,遵循共享约定:在写入之前核实实际的
工具权限和目标。用户说"已连接"并不能作为工具权限的证据。
绝不要索要 Notion 密码或令牌。

对于与 Excel 兼容的 CSV,使用带字节顺序标记(BOM)的 UTF-8,以便 Excel 能正确打开
该文本。CSV 不是 `.xlsx` 工作簿;只有当用户要求工作簿时才创建 `.xlsx`。
CSV 不携带类型信息,所以生成后需指明
哪些列需要应用数字、日期或货币格式。

```csv
Alumni Name,Former Department,Former Job Title,Last Working Day,Rehire Eligible,Personal Email,LinkedIn,Current Company,Last Contact,Re-engage Date,Notes,Alumni ID
Example Person,Delivery,Delivery Manager,2026-03-31,TRUE,person@example.com,https://example.com/in/example-person,Example Company,2026-01-20,2026-07-01,"Reached out in February; interested in returning once the current notice period ends.",
```

```sql
CREATE TABLE alumni_re_hire_tracker (
  alumni_name VARCHAR(255),
  former_department VARCHAR(255),
  former_job_title VARCHAR(255),
  last_working_day DATE NOT NULL,
  rehire_eligible BOOLEAN NOT NULL,
  personal_email VARCHAR(255),
  linkedin TEXT,
  current_company VARCHAR(255),
  last_contact DATE NOT NULL,
  re_engage_date DATE NOT NULL,
  notes TEXT,
  alumni_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Alumni & Re-hire Tracker",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Alumni Name": { "type": "string" },
      "Former Department": { "type": "string" },
      "Former Job Title": { "type": "string" },
      "Last Working Day": { "type": "string", "format": "date" },
      "Rehire Eligible": { "type": "boolean" },
      "Personal Email": { "type": "string", "format": "email" },
      "LinkedIn": { "type": "string", "format": "uri" },
      "Current Company": { "type": "string" },
      "Last Contact": { "type": "string", "format": "date" },
      "Re-engage Date": { "type": "string", "format": "date" },
      "Notes": { "type": "string" },
      "Alumni ID": { "type": "integer" }
  },
  "required": [
      "Last Working Day",
      "Last Contact",
      "Re-engage Date"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Alumni Name | Title | Use as the database title |
| Former Department | Text | Leave as Text |
| Former Job Title | Text | Leave as Text |
| Last Working Day | Date | Convert to Date |
| Rehire Eligible | Checkbox | Convert to Checkbox |
| Personal Email | Email | Convert to Email |
| LinkedIn | URL | Convert to URL |
| Current Company | Text | Leave as Text |
| Last Contact | Date | Convert to Date |
| Re-engage Date | Date | Convert to Date |
| Notes | Text | Leave as Text |
| Alumni ID | Text (preserve source ID) | Keep imported IDs as Text; optionally add a separate Unique ID property |
```

以上各行仅为文档示例。除非用户明确要求示例,否则生成空白模板。金额保持为 `currency`,日期保持为 `date`,
任何指向其他表的内容保持为 `relation`。

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Alumni Name | `text` | `VARCHAR(255)` | `string` | Text | `Example Person` |
| 2 | Former Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 3 | Former Job Title | `text` | `VARCHAR(255)` | `string` | Text | `Delivery Manager` |
| 4 | Last Working Day | `date` | `DATE` | `string, format: date` | Date | `2026-03-31` |
| 5 | Rehire Eligible | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `TRUE` |
| 6 | Personal Email | `email` | `VARCHAR(255)` | `string, format: email` | Email | `person@example.com` |
| 7 | LinkedIn | `url` | `TEXT` | `string, format: uri` | URL | `https://example.com/in/example-person` |
| 8 | Current Company | `text` | `VARCHAR(255)` | `string` | Text | `Example Company` |
| 9 | Last Contact | `date` | `DATE` | `string, format: date` | Date | `2026-01-20` |
| 10 | Re-engage Date | `date` | `DATE` | `string, format: date` | Date | `2026-07-01` |
| 11 | Notes | `long_text` | `TEXT` | `string` | Text | `Reached out in February; interested in returning once the current notice period ends.` |
| 12 | Alumni ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (preserve source ID) | `(blank)` |

## Select Options

_没有 Select 字段。_

## Relations

链接字段:无

## Examples

**Prompt**

```
Four good people left last year and we only noticed when a role came up.
```

**先了解背景** —— 每条消息一个问题,不重复已回答的内容:

> **问:** 有多少前员工?
> **答:** 三年里大约二十人。
>
> **问:** 有记录吗?
> **答:** 一份表格,大部分是空的。
>
> **问:** 为什么要返聘?
> **答:** 我们知道谁表现好。

**推荐的下一步** —— 提供建议,而非直接构建:

> 保留一份小型的离职员工记录,包含离职日期、所任职位,以及一行关于离职原因的说明,并仅在有职位空缺时才重新查看它。
>
> 工作流:记录离职 → 保留详情 → 职位空缺时考虑返聘 → 重新入职或建立联系
>
> 需要为此生成 CSV、SQL、JSON Schema 和 Notion 映射吗?

## Best Practices

- 仅在被请求时构建;对于仅咨询性的请求,给出建议并提供构建选项。
- 每条消息只问一个问题。批量提问会显得像表单,并引来猜测式的回答。
- 保持 CSV 和 JSON 中显示名称一致;为规范化的 SQL 标识符编写文档。
- 对任何指向其他表的内容使用 `relation`,仅对自由文本使用 `text`。
- 金额字段为 `currency`,绝不是 `text`。日期为 `date`,绝不是自由文本。
- 如果用户要求示例行,保持它明显是虚构的,以免被误当作真实数据导入。

## Limitations

- 仅为空白模板。它不计算薪资、税务、休假余额或 KPI。
- Notion 关系需要两个数据库都导入后,链接列才能解析。
- Select 选项只是一组起始值。请重命名以匹配企业的实际说法。
- 没有自动化、提醒或同步功能。这些需要集成层。
- 不会联系任何人、核实同意情况,或做出招聘决定。
- 在据此做出真实决策之前,仍需进行法律、税务和人力资源审查。

## Security & Safety Notes

- 绝不要填入真实姓名、薪资、医疗或银行数据。仅使用占位符。
- 将示例行标注为合成数据,并对银行信息进行遮蔽处理。
- 本地读取、生成命令和验证是请求的产物构建的一部分。
  外部写入、消息、资源配置和发布,需要针对该操作和目标获得授权;
  已有的明确授权不需要重复。
- 如果提供了敏感数据,避免重复不必要的标识信息。仅使用所请求审查
  所需的内容;保持生成的模板为空。不要声称已从对话或服务存储中删除数据。
- 隐私、法律和处分相关的案例,需要在采取任何行动之前由合格的人员进行审查。

## Common Pitfalls

- **问题:** 将一份静态映射描述为已完成的工作区构建。
  **解决方案:** 在没有连接的情况下交付手动映射;只有在获得授权的工具操作成功后,才声称实现了实时更改。
- **问题:** 在一条消息里问了全部六个问题。
  **解决方案:** 一次问一个,等待回答,并跳过第一个答案已经涵盖的问题。
- **问题:** 当只被要求一张表时,却构建了一整套系统。
  **解决方案:** 按请求构建;单独提及上级(parent)技能。
- **问题:** 四种产物彼此脱节。
  **解决方案:** 始终从本文件中的字段清单推导出全部四种产物,而不是手工编写。
- **问题:** Notion 导入后每一列都显示为 Text。
  **解决方案:** 这是预期行为。导入后应用一次属性映射表即可。

## Related Skills

- [Module Catalog](https://github.com/sickn33/agentic-awesome-skills/blob/main/CATALOG.md) —— 先找到相关模块,再阅读其技能说明。
- @people-directory —— 大多数模块所链接的员工主记录。
- @notification-reminder-hub —— 将本模块中的到期日期转化为提醒。

## Reusable Prompt

```
I want to set up former employees for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```
