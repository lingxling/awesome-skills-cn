---
name: admin-access-register
description: '管理员账号登记册：系统、主管理员与备份管理员、席位、套餐、双因素认证（2FA）、共享登录以及访问审查日期，可按需输出为 CSV、SQL、JSON Schema 或 Notion。用于访问权限审查。'
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
- protect
tools: []
source_repo: WHOISABHISHEKADHIKARI/sme-ops-system-builder
---

# 管理员访问登记册

**它是什么：** 记录每个系统上谁拥有管理员权限，并附有备份管理员和审查日期。

## 概述

为眼前的业务梳理出最小可用的**管理员访问登记册**方案，且仅在被要求时才进行构建。默认输出是一份简短的建议，而不是一张电子表格。产物——CSV、SQL DDL、JSON Schema、Notion 映射——按需生成，并且都源自同一份字段清单，因此不会互相偏离。

所属层级：第 7 层：保护（Protect）。适用阶段：成长期。表代码：不适用。

## 何时使用本技能

- 管理员访问登记册
- 系统访问审查
- 特权账号清单
- 季度访问审查

当用户说"每个系统上谁拥有管理员权限，并附有备份管理员和审查日期"，或描述同样的流程正发生在电子表格、文档或某人的收件箱里时，也应使用本技能。

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

> **Q:** 一共有多少个管理员账号？

### 步骤 2 - 只询问缺失的信息

跳过用户在之前任何消息中已经回答过的内容。其余问题一次只问一个，一旦剩下的答案不会改变输出，就立即停止。

- **范围** - 涉及哪些系统？/ 有多少管理员？/ 是供应商管理员还是员工管理员？
- **归属** - 谁来批准访问？/ 每个账号是否有具名负责人？/ 是否存在共享登录？
- **审查** - 多久审查一次？/ 人员离职时如何处理？/ 是否保留证据？
- **现行流程** - 目前有记录吗？/ 是 IT 工单还是没有任何记录？/ 是否是最新的？
- **期望结果** - 你需要什么？/ 一份登记册、一个审查周期，还是两者都要？

绝不要编造答案。如果用户不知道，就记为未知并继续。

### 步骤 3 - 保留内部上下文

以如下结构保存答案。它仅供内部使用——除非用户询问，否则不向用户展示，且绝不包含用户未提供的值。

```yaml
module: admin-access-register
intent: null            # setup | advice | review | fix | build | convert | export
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Scope": null
  "Ownership": null
  "Review": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion | xlsx - requested formats only
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### 步骤 4 - 推荐最小可行工作流

如果用户请求了某个产物，则在解决关键缺失信息后进行构建。否则，给出一份简短的建议，并提供相关产物。

**推荐方案：** 每个具名管理员账号一行，包含系统、负责人和最近审查日期。共享登录是最先需要修复的问题。

**为何选择这一方案：** 特权账号是在有人离职之后最要紧的账号。为每个账号指定负责人，才能使移除成为可能。

**工作流：** 列出系统 → 管理员账号 → 负责人与审批人 → 定期审查 → 移除

### 步骤 5 - 仅在被要求时构建

一旦用户提出要求，就根据已确认的上下文推导字段，并输出所请求的产物。对于机器可读文本，行文要放在数据之外；对于文件，提供可用的链接。重大的校验失败或局限性应单独报告。

**所选的 Notion 输出由 `notion-manual-import` 渲染，因此请将 Notion 这一步交给它。** 当用户选择 Notion 时，将该步骤交给 @notion-manual-import：它持有 CSV、属性映射、导入步骤和验证清单，并且渲染下方的字段参考，而不是自己定义一张表。不要在此处重述映射，也不要即兴发挥导入步骤。手动 CSV 和映射输出无需连接。对于要求的工作区更改，请遵循共享契约：在写入之前，先核实实际的工具访问权限和目标。用户说"已连接"并不构成工具层面的证据。绝不要索要 Notion 的密码或令牌。

对于兼容 Excel 的 CSV，请使用带字节顺序标记（BOM）的 UTF-8，以便 Excel 能正确打开文本。CSV 不是 `.xlsx` 工作簿；仅在用户要求工作簿时才创建 `.xlsx`。CSV 不带类型信息，因此在输出之后，要指出哪些列需要应用数字、日期或货币格式。

```csv
System or Tool,Category,Main Admin,Backup Admin,Department,Access Level,Number of Admin Users,Billing Owner,Plan,Seats,Renewal Date,Company Owned Account,Shared Login,Password Manager Entry,Two Factor On,Last Access Review,Next Access Review,Offboarding Checklist Item,Risk Level,Status,Notes,Admin ID
Example Product,General,Example Admin,Example Backup Admin,Delivery,Full,3,Example Owner,Business,5,2026-01-15,TRUE,FALSE,Shared vault - Finance,TRUE,2026-01-15,2026-01-15,"Remove from payroll, revoke accounts, collect laptop",Low,Provisioned,Shared logins retired after the February access review; two orphaned accounts still need an owner.,
```

```sql
CREATE TABLE admin_access_register (
  system_or_tool VARCHAR(255),
  category VARCHAR(100) NOT NULL,
  main_admin VARCHAR(255),
  backup_admin VARCHAR(255),
  department VARCHAR(255),
  access_level VARCHAR(100) NOT NULL,
  number_of_admin_users NUMERIC NOT NULL,
  billing_owner VARCHAR(255),
  plan VARCHAR(255),
  seats NUMERIC NOT NULL,
  renewal_date DATE NOT NULL,
  company_owned_account BOOLEAN NOT NULL,
  shared_login BOOLEAN NOT NULL,
  password_manager_entry VARCHAR(255),
  two_factor_on BOOLEAN NOT NULL,
  last_access_review DATE NOT NULL,
  next_access_review DATE NOT NULL,
  offboarding_checklist_item VARCHAR(255),
  risk_level VARCHAR(100) NOT NULL,
  status VARCHAR(100) NOT NULL,
  notes TEXT,
  admin_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_admin_access_register_status ON admin_access_register (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Admin Access Register",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "System or Tool": { "type": "string" },
      "Category": { "type": "string" },
      "Main Admin": { "type": "string" },
      "Backup Admin": { "type": "string" },
      "Department": { "type": "string" },
      "Access Level": { "type": "string" },
      "Number of Admin Users": { "type": "number" },
      "Billing Owner": { "type": "string" },
      "Plan": { "type": "string" },
      "Seats": { "type": "number" },
      "Renewal Date": { "type": "string", "format": "date" },
      "Company Owned Account": { "type": "boolean" },
      "Shared Login": { "type": "boolean" },
      "Password Manager Entry": { "type": "string" },
      "Two Factor On": { "type": "boolean" },
      "Last Access Review": { "type": "string", "format": "date" },
      "Next Access Review": { "type": "string", "format": "date" },
      "Offboarding Checklist Item": { "type": "string" },
      "Risk Level": { "type": "string" },
      "Status": { "type": "string" },
      "Notes": { "type": "string" },
      "Admin ID": { "type": "integer" }
  },
  "required": [
      "Category",
      "Access Level",
      "Number of Admin Users",
      "Seats",
      "Renewal Date",
      "Last Access Review",
      "Next Access Review",
      "Risk Level",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| System or Tool | Title | Use as the database title |
| Category | Select (add options after import) | Convert to Select, add options: "General", "Operations", "Finance", "People", "Compliance" |
| Main Admin | Text | Leave as Text |
| Backup Admin | Text | Leave as Text |
| Department | Text | Leave as Text |
| Access Level | Select (add options after import) | Convert to Select, add options: "Full", "Write", "Read", "No Access" |
| Number of Admin Users | Number | Convert to Number |
| Billing Owner | Text | Leave as Text |
| Plan | Text | Leave as Text |
| Seats | Number | Convert to Number |
| Renewal Date | Date | Convert to Date |
| Company Owned Account | Checkbox | Convert to Checkbox |
| Shared Login | Checkbox | Convert to Checkbox |
| Password Manager Entry | Text | Leave as Text |
| Two Factor On | Checkbox | Convert to Checkbox |
| Last Access Review | Date | Convert to Date |
| Next Access Review | Date | Convert to Date |
| Offboarding Checklist Item | Text | Leave as Text |
| Risk Level | Select (add options after import) | Convert to Select, add options: "Low", "Medium", "High", "Critical" |
| Status | Select (add options after import) | Convert to Select, add options: "Requested", "Approved", "Provisioned", "Review Due", "Revoked" |
| Notes | Text | Leave as Text |
| Admin ID | Text (preserve source ID) | Keep imported IDs as Text; optionally add a separate Unique ID property |
```

以上各行仅为文档示例。除非用户明确要求示例，否则请输出空模板。金额保持为 `currency`，日期保持为 `date`，指向其他表的内容保持为 `relation`。

## 字段参考

| # | 字段 | 类型 | SQL | JSON Schema | Notion | CSV 示例 |
|---:|---|---|---|---|---|---|
| 1 | System or Tool | `text` | `VARCHAR(255)` | `string` | Text | `Example Product` |
| 2 | Category | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `General` |
| 3 | Main Admin | `text` | `VARCHAR(255)` | `string` | Text | `Example Admin` |
| 4 | Backup Admin | `text` | `VARCHAR(255)` | `string` | Text | `Example Backup Admin` |
| 5 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 6 | Access Level | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Full` |
| 7 | Number of Admin Users | `number` | `NUMERIC` | `number` | Number | `3` |
| 8 | Billing Owner | `text` | `VARCHAR(255)` | `string` | Text | `Example Owner` |
| 9 | Plan | `text` | `VARCHAR(255)` | `string` | Text | `Business` |
| 10 | Seats | `number` | `NUMERIC` | `number` | Number | `5` |
| 11 | Renewal Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 12 | Company Owned Account | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `TRUE` |
| 13 | Shared Login | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `FALSE` |
| 14 | Password Manager Entry | `text` | `VARCHAR(255)` | `string` | Text | `Shared vault - Finance` |
| 15 | Two Factor On | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `TRUE` |
| 16 | Last Access Review | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 17 | Next Access Review | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 18 | Offboarding Checklist Item | `text` | `VARCHAR(255)` | `string` | Text | `Remove from payroll, revoke accounts, collect laptop` |
| 19 | Risk Level | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Low` |
| 20 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Provisioned` |
| 21 | Notes | `long_text` | `TEXT` | `string` | Text | `Shared logins retired after the February access review; two orphaned accounts still need an owner.` |
| 22 | Admin ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (preserve source ID) | `(blank)` |

## 选项值

**Category**

```
General | Operations | Finance | People | Compliance
```
**Access Level**

```
Full | Write | Read | No Access
```
**Risk Level**

```
Low | Medium | High | Critical
```
**Status**

```
Requested | Approved | Provisioned | Review Due | Revoked
```

## 关联关系

关联字段：无

## 示例

**提示词**

```
We have admin accounts for people who left two years ago.
```

**先了解上下文** —— 每条消息一个问题，不重复已回答的内容：

> **Q:** 涉及哪些系统？
> **A:** 会计、CRM 和电子邮件。
>
> **Q:** 每个都有具名负责人吗？
> **A:** 不总是有。
>
> **Q:** 有共享登录吗？
> **A:** 有，一两个。

**推荐的下一步** —— 只是提议，不直接构建：

> 每个具名管理员账号一行，包含系统、负责人和最近审查日期。共享登录是最先需要修复的问题。
>
> 工作流：列出系统 → 管理员账号 → 负责人与审批人 → 定期审查 → 移除
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

- 仅为空模板。它不计算薪资、税款、假期余额或 KPI。
- Notion 关联需要先导入两个数据库，关联列才能解析。
- 选项值只是一组起始集合。请重命名以匹配业务的实际说法。
- 没有自动化、提醒或同步功能。这些需要集成层。
- 不会在任何系统上授予、更改或撤销访问权限。
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
I want to set up who holds admin rights on each system, with a backup admin and review dates for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```
