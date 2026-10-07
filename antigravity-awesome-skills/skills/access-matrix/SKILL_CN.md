---
name: access-matrix
description: '访问矩阵：按角色与模块划分的权限，附带每个角色的范围、保密级别和 SME 层级，可按需输出为 CSV、SQL、JSON Schema 或 Notion。适用于访问权限评审。'
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
- foundation
tools: []
source_repo: WHOISABHISHEKADHIKARI/sme-ops-system-builder
---

# 访问矩阵

**它是什么：** 每个角色能看到什么、能修改什么。

## 概述

为眼前的企业设计出最小可用的**访问矩阵**方案，并且仅在被要求时才构建。默认输出是一份简短的建议，而不是电子表格。产物——CSV、SQL DDL、JSON Schema、Notion 映射——按需生成，并且都来自同一份字段列表，因此不会出现彼此不一致的情况。

层级：Layer 1：Foundation（基础）。适用阶段：成长期。表代码：n/a。

## 何时使用此技能

- who can access what matrix
- role permission matrix
- access control spreadsheet
- who sees which data

当用户说 "what each role can see and change"，或描述同样的流程正发生在电子表格、文档或某人的收件箱里时，也可使用它。

不适用于：薪资计算、税务申报或法律建议。本技能只生成空模板——它从不持有或处理真实的员工或客户数据。

## 工作原理

遵循共享的执行契约。下面的模块专属规则只定义领域字段、决策、计算和安全约束。

### 步骤 1 - 识别意图

先阅读请求并确定意图，然后再提问。

- "set up" 或 "build" 或 "create" -> 用户想要产物；进入步骤 2。
- "our process is ..." 或 "it is in a sheet" -> 用户想要迁移现有流程；先记录下来，再进入步骤 2。
- "is this right" 或 "review" 或 "audit" -> 用户想要的是检查，而不是构建；根据他们分享的内容作答。
- "how do I ..." -> 咨询类问题；直接作答，仅在有帮助时才提议构建。

只有在这是价值最高的缺失事实时才提问；否则无需开场白，直接继续：

> **Q:** How many roles exist in the company?

### 步骤 2 - 只问缺失的信息

跳过用户已在任何先前消息中回答过的内容。其余的逐个提问，一旦剩余的答案不会改变输出就停止。

- **范围** - 哪个系统或数据？/ 有多少个角色？/ 有外部人员吗？
- **角色** - 谁是所有者或 CEO？/ 谁是管理员？/ 谁是直线经理？
- **规则** - 仅查看还是可编辑？/ 有保密区域吗？/ 多久评审一次？
- **当前流程** - 你现在如何追踪访问权限？/ 用电子表格还是没有？/ 有已知的缺口吗？
- **成果** - 这应该产出什么？/ 一份访问清单还是一个评审周期？

绝不要捏造答案。如果用户不知道，就把它记录为未知并继续。

### 步骤 3 - 保持内部上下文

按如下形式保存答案。它保持在内部——除非用户询问，否则不向用户展示，并且绝不携带用户没有给出的值。

```yaml
module: access-matrix
intent: null            # setup | advice | review | fix | build | convert | export
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Scope": null
  "Roles": null
  "Rules": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion | xlsx - requested formats only
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### 步骤 4 - 推荐最小工作流

如果已请求某个产物，则在解决了必要的缺失事实之后构建它。否则给出简短的建议，并提议相关的产物。

**推荐做法：** 把矩阵保存在团队已经在用来评审的工具中，并将其视为周期性的评审，而不是一次性的文档。

**原因：** 访问权限问题很少出在存储上。问题在于没有人重新检查谁仍然需要什么，因此评审周期比矩阵本身更重要。

**工作流：** 角色清单 → 系统清单 → 访问权限行 → 季度评审 → 移除

### 步骤 5 - 仅在被请求时构建

一旦用户提出要求，就根据已确认的上下文推导字段，并输出所请求的产物。对于机器可读的文本，行文要放在数据之外；对于文件，提供可用的链接。重大的验证失败或局限性要另行报告。

**被选中的 Notion 输出由 `notion-manual-import` 渲染，因此将 Notion 这一步路由到那里。** 当用户选择 Notion 时，把这一步交给
@notion-manual-import：它持有 CSV、属性映射、导入步骤和验证清单，并且它渲染下方的字段参考表，而不是自行定义一张表。不要在此处重述映射，也不要临时编造导入步骤。手动 CSV 和映射输出不需要连接。对于被请求的工作区变更，遵循共享契约：写入之前先核实实际的工具访问权限和目标。用户说 "connected" 并不是工具层面的证据。
绝不要索要 Notion 密码或令牌。

对于兼容 Excel 的 CSV，使用带字节顺序标记（BOM）的 UTF-8，以便 Excel 正确打开文本。CSV 不是 `.xlsx` 工作簿；只有在用户请求工作簿时才创建 `.xlsx`。
CSV 不携带类型，因此在给出 CSV 之后，要指明哪些列需要应用数字、日期或货币格式。

```csv
Module,Module ID,Layer,SME Tier,Owner / CEO,Board,Finance,Tax,HR,IT & Admin,Department Head,Line Manager,Employee,Intern,Client,Confidential
Invoices & Billing,,Layer 8: Operate,Small,Full - all modules,Read - board pack only,"Read, add, edit - payroll and invoices","Read, add, edit - tax register",Full - people and compliance modules,"Read, add, edit - assets and access",Example Reviewer,"Read, add, edit - own team",Read - own records,Read - onboarding only,Example Customer,Internal
```

```sql
CREATE TABLE access_matrix (
  module VARCHAR(255),
  module_id SERIAL PRIMARY KEY,
  layer VARCHAR(255),
  sme_tier VARCHAR(100) NOT NULL,
  owner_ceo VARCHAR(255),
  board VARCHAR(255),
  finance VARCHAR(255),
  tax VARCHAR(255),
  hr VARCHAR(255),
  it_admin VARCHAR(255),
  department_head VARCHAR(255),
  line_manager VARCHAR(255),
  employee VARCHAR(255),
  intern VARCHAR(255),
  client VARCHAR(255),
  confidential VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Access Matrix",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Module": { "type": "string" },
      "Module ID": { "type": "integer" },
      "Layer": { "type": "string" },
      "SME Tier": { "type": "string" },
      "Owner / CEO": { "type": "string" },
      "Board": { "type": "string" },
      "Finance": { "type": "string" },
      "Tax": { "type": "string" },
      "HR": { "type": "string" },
      "IT & Admin": { "type": "string" },
      "Department Head": { "type": "string" },
      "Line Manager": { "type": "string" },
      "Employee": { "type": "string" },
      "Intern": { "type": "string" },
      "Client": { "type": "string" },
      "Confidential": { "type": "string" }
  },
  "required": [
      "SME Tier",
      "Confidential"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Module | Title | Use as the database title |
| Module ID | Text (preserve source ID) | Keep imported IDs as Text; optionally add a separate Unique ID property |
| Layer | Text | Leave as Text |
| SME Tier | Select (add options after import) | Convert to Select, add options: "Micro", "Small", "Medium", "Large", "Enterprise" |
| Owner / CEO | Text | Leave as Text |
| Board | Text | Leave as Text |
| Finance | Text | Leave as Text |
| Tax | Text | Leave as Text |
| HR | Text | Leave as Text |
| IT & Admin | Text | Leave as Text |
| Department Head | Text | Leave as Text |
| Line Manager | Text | Leave as Text |
| Employee | Text | Leave as Text |
| Intern | Text | Leave as Text |
| Client | Text | Leave as Text |
| Confidential | Select (add options after import) | Convert to Select, add options: "Public", "Internal", "Restricted", "Highly Restricted" |
```

上面的行仅为文档示例。除非用户明确要求示例，否则输出空模板。金额保持为 `currency`，日期保持为 `date`，
任何指向另一张表的内容保持为 `relation`。

## 字段参考

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Module | `text` | `VARCHAR(255)` | `string` | Text | `Invoices & Billing` |
| 2 | Module ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (preserve source ID) | `(blank)` |
| 3 | Layer | `text` | `VARCHAR(255)` | `string` | Text | `Layer 8: Operate` |
| 4 | SME Tier | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Small` |
| 5 | Owner / CEO | `text` | `VARCHAR(255)` | `string` | Text | `Full - all modules` |
| 6 | Board | `text` | `VARCHAR(255)` | `string` | Text | `Read - board pack only` |
| 7 | Finance | `text` | `VARCHAR(255)` | `string` | Text | `Read, add, edit - payroll and invoices` |
| 8 | Tax | `text` | `VARCHAR(255)` | `string` | Text | `Read, add, edit - tax register` |
| 9 | HR | `text` | `VARCHAR(255)` | `string` | Text | `Full - people and compliance modules` |
| 10 | IT & Admin | `text` | `VARCHAR(255)` | `string` | Text | `Read, add, edit - assets and access` |
| 11 | Department Head | `text` | `VARCHAR(255)` | `string` | Text | `Example Reviewer` |
| 12 | Line Manager | `text` | `VARCHAR(255)` | `string` | Text | `Read, add, edit - own team` |
| 13 | Employee | `text` | `VARCHAR(255)` | `string` | Text | `Read - own records` |
| 14 | Intern | `text` | `VARCHAR(255)` | `string` | Text | `Read - onboarding only` |
| 15 | Client | `text` | `VARCHAR(255)` | `string` | Text | `Example Customer` |
| 16 | Confidential | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Internal` |

## 选择项

**SME Tier**

```
Micro | Small | Medium | Large | Enterprise
```
**Confidential**

```
Public | Internal | Restricted | Highly Restricted
```

## 关联

关联字段：无

## 示例

**Prompt**

```
We have 6 roles and want to know who can see payroll and bank details.
```

**先了解上下文** - 每条消息一个问题，不重复已回答的内容：

> **Q:** Which system?
> **A:** Payroll, bank details and HR records.
>
> **Q:** How often should it be reviewed?
> **A:** Every quarter.
>
> **Q:** What do you use today?
> **A:** Nothing tracked.

**推荐的下一步** - 只是提议，不构建：

> Keep the matrix in the tool the team already reviews in, and treat it as a recurring review rather than a one-time document.
>
> Workflow: Role list → System inventory → Access rows → Quarterly review → Removal
>
> Want the CSV, SQL, JSON Schema and Notion mapping for this?

## 最佳实践

- 被要求时就构建；对于仅咨询的请求，给出建议并提议构建。
- 每条消息一个问题。批量式的收集看起来像一张表单，只会让人去猜。
- 保持 CSV 与 JSON 中的显示名称一致；对规范化的 SQL 标识符加以说明。
- 对指向另一张表的内容使用 `relation`，`text` 仅用于自由文本。
- 金额字段为 `currency`，绝不使用 `text`。日期为 `date`，绝不使用自由文本。
- 如果用户请求示例行，要让它明显是假的，以免有人把它当作真实数据导入。

## 局限性

- 仅限空模板。它不计算薪资、税务、休假余额或 KPI。
- Notion 关联需要两个数据库都导入之后，关联列才能解析。
- 选择项只是一组起始集合。请重命名它们以匹配企业的说法。
- 没有自动化、提醒或同步。这些需要集成层。
- 不会开通或撤销访问权限。它只记录谁应该拥有什么。
- 在以此推动真实决策之前，仍需进行法务、税务和人力资源的审查。

## 安全与安全注意事项

- 绝不要填入真实的姓名、薪资、医疗或银行数据。只使用占位符。
- 将示例行标注为合成数据，并对银行详情做掩码处理。
- 本地读取、生成命令和验证属于所请求产物构建的一部分。
  外部写入、消息、开通和发布，需要针对该操作和目标获得授权；已有的明确授权无需重复。
- 如果提供了敏感数据，避免重复不必要的标识符。只使用所请求的评审所需要的内容；让生成的模板保持为空。不要声称已从对话或服务存储中删除。
- 涉及隐私、法律和纪律的案例，在采取任何行动之前需要有资质的人工审核。

## 常见陷阱

- **问题：** 把静态映射描述成已完成的工作区构建。
  **解决方案：** 手动映射无需连接即可交付；只有在获授权的工具操作成功之后，才声称做了实时变更。
- **问题：** 在一条消息中问了全部六个问题。
  **解决方案：** 问一个，等待，并去掉第一个答案已经涵盖的任何问题。
- **问题：** 被要求一张表时却构建了完整的系统。
  **解决方案：** 构建被要求的内容；另行提及上级技能。
- **问题：** 四种产物彼此漂移不一致。
  **解决方案：** 四种都由本文件中的字段列表派生，绝不手工编写。
- **问题：** Notion 导入后每一列都显示为 Text。
  **解决方案：** 这是预期行为。导入后一次性应用属性映射表即可。

## 相关技能

- [Module Catalog](https://github.com/sickn33/agentic-awesome-skills/blob/main/CATALOG.md) - 找到相关模块，然后阅读它的技能。
- @people-directory - 大多数模块所关联的员工主记录。
- @notification-reminder-hub - 把本模块中的到期日期转为提醒。

## 可复用提示词

```
I want to set up what each role can see and change for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```
