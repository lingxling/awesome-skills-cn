---
name: announcement-board
description: 'Announcement board(公告板): author、category、department、priority、audience、publish and expiry dates、status 和 acknowledgements,可按需生成 CSV、SQL、JSON Schema 或 Notion。用于内部通知。'
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
- engage
tools: []
source_repo: WHOISABHISHEKADHIKARI/sme-ops-system-builder
---

# Announcement Board(公告板)

**这是什么:** 新闻分发。

## 概览

针对眼下的业务情况,梳理出最小可用的 **Announcement Board(公告板)** 配置,然后仅在被要求时才搭建它。默认输出是一条简短的建议,而不是一份电子表格。产物——CSV、SQL DDL、JSON Schema、Notion 映射——是按需生成的,且都源自同一份字段列表,因此不会相互脱节。

层级: Layer 6: Engage(参与层)。适用阶段: Starter stage(初创阶段)。表代码: n/a。

## 何时使用本技能

- announcement board(公告板)
- company news feed(公司新闻推送)
- notice board(通知板)
- internal announcements(内部公告)

当用户说"新闻分发(news distribution)",或描述的是同一流程正在电子表格、文档或某人的收件箱中发生时,也使用本技能。

不要用于: 工资计算、报税或法律咨询。本技能只生成空模板——它从不保存或处理真实的员工或客户数据。

## 工作方式

遵循共享的执行约定。下面的模块专属规则只定义领域字段、决策、计算方式和安全约束。

### 第 1 步 —— 识别意图

阅读请求,在提出任何问题之前先判断意图。

- "set up"(搭建)或 "build"(构建)或 "create"(创建) -> 用户想要产物;进入第 2 步。
- "our process is ..."(我们的流程是……)或 "it is in a sheet"(目前在表格里) -> 用户想要迁移现有流程;先记录下来,再进入第 2 步。
- "is this right"(这样对吗)或 "review"(审查)或 "audit"(审计) -> 用户想要的是检查,而不是构建;基于他们提供的内容来回答。
- "how do I ..."(我该怎么……) -> 这是咨询问题;直接回答,只有在有帮助时才提议构建。

只有在这是唯一缺失且价值最高的事实时才提问,否则不要用这个开场白来起步:

> **Q:** 谁需要阅读你们的公告?

### 第 2 步 —— 只询问缺失的内容

跳过用户在之前任何消息中已经回答过的内容。其余的逐一询问,一旦剩余的答案不会再改变输出,就停止提问。

- **Audience(受众)** —— 谁来阅读这些内容?/ 全公司还是某个团队?/ 有没有外部读者?
- **Content(内容)** —— 发布什么内容?/ 只是公告,还是两者都有?/ 是否使用附件?
- **Approval(审批)** —— 由谁撰写?/ 是否需要审批?/ 是否有定时发布?
- **Current process(当前流程)** —— 现在如何分享新闻?/ 邮件、聊天工具,还是两者都用?/ 哪些内容会被漏掉?
- **Outcome(期望结果)** —— 你需要什么?/ 一个公告板、一个发布计划,还是存档?

不要编造答案。如果用户不知道,就记为未知,然后继续。

### 第 3 步 —— 保存内部上下文

按以下结构保存这些答案。它仅供内部使用——除非用户要求,否则不会展示给用户,并且绝不会包含用户未曾给出的值。

```yaml
module: announcement-board
intent: null            # setup | advice | review | fix | build | convert | export
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Audience": null
  "Content": null
  "Approval": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion | xlsx - requested formats only
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### 第 4 步 —— 推荐最小可行的工作流

如果用户已经要求生成产物,先解决必要的缺失事实,再构建。否则给出简短的建议,并提议相应的产物。

**推荐方案:** 在一个地方统一发布,并保留过期日期,这样旧公告就不会再看起来像是最新的。针对特定受众投放,而不是广播给所有人。

**为什么是这个方案:** 公告板的失败通常源于内容杂乱,而不是帖子缺失。一个过期日期和一个明确的负责人能让公告板保持可读性。

**工作流:** 草稿 → 审批 → 发布 → 已读或已确认 → 过期

### 第 5 步 —— 仅在被要求时才构建

一旦用户提出要求,就根据已确认的上下文推导出字段,并生成所请求的产物。对于机器可读的文本,要把行文说明放在数据之外;对于文件,要提供可用的链接。实质性的验证失败或局限性要单独报告。

**如果用户选择了 Notion 输出,则由 `notion-manual-import` 来渲染,因此将该 Notion 步骤转交给它处理。** 当用户选择 Notion 时,把这一步交给
@notion-manual-import:它负责 CSV、属性映射、导入步骤和验证清单,并渲染下方的 Field Reference(字段参考),而不是另行定义一张表。不要在这里重复映射内容,也不要自行编造导入步骤。手动的 CSV 和映射输出不需要连接。对于所请求的工作区变更,遵循共享约定:在写入之前核实实际的工具访问权限和目标。用户说"已连接"并不构成工具访问的证据。永远不要索要 Notion 密码或 token。

对于兼容 Excel 的 CSV,使用带字节顺序标记(BOM)的 UTF-8,这样 Excel 才能正确打开该文本。CSV 不是 `.xlsx` 工作簿;只有在用户要求提供工作簿时才创建 `.xlsx`。
CSV 本身不携带类型信息,所以在生成 CSV 之后,要指明哪些列需要应用数字、日期或货币格式。

```csv
Announcement Title,Acknowledged By,Ann ID,Author,Category,Department,Expiry Date,Priority,Publish Date,Status,Summary,Target Audience,Views
Office closed on 15th,"Example Person 1, Example Person 2",,Example Author,Company,Delivery,2026-01-15,Low,2026-01-15,Published,Office closed on the 15th for the public holiday.,All employees,184
```

```sql
CREATE TABLE announcement_board (
  announcement_title VARCHAR(255),
  acknowledged_by VARCHAR(255),
  ann_id SERIAL PRIMARY KEY,
  author VARCHAR(255),
  category VARCHAR(100) NOT NULL,
  department VARCHAR(255),
  expiry_date DATE NOT NULL,
  priority VARCHAR(100) NOT NULL,
  publish_date DATE NOT NULL,
  status VARCHAR(100) NOT NULL,
  summary TEXT,
  target_audience VARCHAR(255),
  views VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_announcement_board_status ON announcement_board (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Announcement Board",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Announcement Title": { "type": "string" },
      "Acknowledged By": { "type": "string" },
      "Ann ID": { "type": "integer" },
      "Author": { "type": "string" },
      "Category": { "type": "string" },
      "Department": { "type": "string" },
      "Expiry Date": { "type": "string", "format": "date" },
      "Priority": { "type": "string" },
      "Publish Date": { "type": "string", "format": "date" },
      "Status": { "type": "string" },
      "Summary": { "type": "string" },
      "Target Audience": { "type": "string" },
      "Views": { "type": "string" }
  },
  "required": [
      "Category",
      "Expiry Date",
      "Priority",
      "Publish Date",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Announcement Title | Title | Use as the database title |
| Acknowledged By | Text | Leave as Text |
| Ann ID | Text (preserve source ID) | Keep imported IDs as Text; optionally add a separate Unique ID property |
| Author | Text | Leave as Text |
| Category | Select (add options after import) | Convert to Select, add options: "Company", "Department", "Team", "Location", "Role" |
| Department | Text | Leave as Text |
| Expiry Date | Date | Convert to Date |
| Priority | Select (add options after import) | Convert to Select, add options: "Low", "Medium", "High", "Urgent" |
| Publish Date | Date | Convert to Date |
| Status | Select (add options after import) | Convert to Select, add options: "Draft", "Scheduled", "Published", "Archived" |
| Summary | Text | Leave as Text |
| Target Audience | Text | Leave as Text |
| Views | Text | Leave as Text |
```

以上几行只是文档示例。除非用户明确要求示例,否则一律生成空模板。金额字段保持 `currency`,日期字段保持 `date`,任何指向其他表的字段保持 `relation`。

## Field Reference(字段参考)

| # | 字段 | 类型 | SQL | JSON Schema | Notion | CSV 示例 |
|---:|---|---|---|---|---|---|
| 1 | Announcement Title | `text` | `VARCHAR(255)` | `string` | Text | `Office closed on 15th` |
| 2 | Acknowledged By | `text` | `VARCHAR(255)` | `string` | Text | `Example Person 1, Example Person 2` |
| 3 | Ann ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (preserve source ID) | `(blank)` |
| 4 | Author | `text` | `VARCHAR(255)` | `string` | Text | `Example Author` |
| 5 | Category | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Company` |
| 6 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 7 | Expiry Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 8 | Priority | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Low` |
| 9 | Publish Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 10 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Published` |
| 11 | Summary | `long_text` | `TEXT` | `string` | Text | `Office closed on the 15th for the public holiday.` |
| 12 | Target Audience | `text` | `VARCHAR(255)` | `string` | Text | `All employees` |
| 13 | Views | `text` | `VARCHAR(255)` | `string` | Text | `184` |

## Select Options(选项值)

**Category**

```
Company | Department | Team | Location | Role
```
**Priority**

```
Low | Medium | High | Urgent
```
**Status**

```
Draft | Scheduled | Published | Archived
```

## Relations(关联)

关联字段: 无

## 示例

**提示词**

```
Company news goes out in chat and gets lost in a week.
```

**先确认上下文** —— 每条消息问一个问题,不重复已回答的内容:

> **Q:** 受众是谁?
> **A:** 全体员工。
>
> **Q:** 审批流程是什么?
> **A:** HR 审批重要的公告。
>
> **Q:** 你们现在在哪里发布?
> **A:** 一个聊天频道。

**推荐的下一步** —— 只是提议,尚未构建:

> 在一个地方统一发布,并保留过期日期,这样旧公告就不会再看起来像是最新的。针对特定受众投放,而不是广播给所有人。
>
> 工作流: 草稿 → 审批 → 发布 → 已读或已确认 → 过期
>
> 需要为此生成 CSV、SQL、JSON Schema 和 Notion 映射吗?

## 最佳实践

- 在被要求时才构建;对于仅咨询性的请求,给出推荐并提议构建。
- 每条消息问一个问题。一次性批量收集信息会让人感觉像在填表,也会被用户当作选择题随意应付。
- 在 CSV 和 JSON 中保持显示名称完全一致;并记录规范化后的 SQL 标识符。
- 任何指向其他表的字段使用 `relation`,`text` 仅用于自由文本。
- 金额字段使用 `currency`,绝不使用 `text`。日期字段使用 `date`,绝不使用自由文本。
- 如果用户要求示例行,要让它明显是虚构的,以免被当作真实数据导入。

## 局限性

- 仅生成空模板。它不计算工资、税务、休假余额或 KPI。
- Notion 的关联需要两个数据库都先导入完成,关联列才能正确解析。
- 选项值只是一个起始集合。请根据业务实际使用的说法重新命名。
- 没有自动化、提醒或同步功能。那些需要集成层来实现。
- 不会代你发送邮件或聊天消息。
- 在据此做出真实决策之前,仍需要法律、税务和 HR 的审查。

## 安全与隐私须知

- 绝不要填入真实的姓名、薪资、医疗或银行数据。只能使用占位符。
- 将示例行标注为合成数据,并对银行信息进行打码处理。
- 本地读取、生成命令和验证属于所请求产物构建的一部分。外部写入、发送消息、资源配置和发布操作需要针对该操作和目标获得授权;已有的明确授权无需重复获取。
- 如果提供了敏感数据,避免重复不必要的标识信息。只使用所请求审查真正需要的内容;保持生成的模板为空。不要声称已从对话或服务存储中删除数据。
- 涉及隐私、法律和处分的案例,在采取任何行动之前都需要一名合格的人工审查员介入。

## 常见陷阱

- **问题:** 把一个静态映射描述成已完成的工作区构建。
  **解决方案:** 在没有建立连接的情况下交付手动映射;只有在获得授权的工具操作真正执行成功后,才能声称完成了实时变更。
- **问题:** 在一条消息里问了全部六个问题。
  **解决方案:** 一次问一个,等待回答,并跳过第一个答案已经涵盖的问题。
- **问题:** 用户只要求一张表,却构建了一整套系统。
  **解决方案:** 只构建被要求的内容;单独提及父技能(parent skill)。
- **问题:** 四种产物各自演变、相互脱节。
  **解决方案:** 全部四种产物都从本文件中的字段列表推导生成,绝不手工编写。
- **问题:** Notion 导入后所有列都显示为 Text。
  **解决方案:** 这是预期行为。导入后一次性应用属性映射表即可。

## 相关技能

- [模块目录(Module Catalog)](https://github.com/sickn33/agentic-awesome-skills/blob/main/CATALOG.md) —— 先找到相关模块,再阅读其技能说明。
- @people-directory —— 大多数模块所关联的员工主记录。
- @notification-reminder-hub —— 将本模块中的到期日期转化为提醒。

## 可复用提示词

```
I want to set up news distribution for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```
