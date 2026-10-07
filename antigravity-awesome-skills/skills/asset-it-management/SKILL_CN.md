---
name: asset-it-management
description: '资产与 IT 登记册：序列号、型号、状态、责任人、位置、购买价值、保修到期日和归还日期，可按需生成 CSV、SQL、JSON Schema 或 Notion。用于资产审计。'
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
- onboard
tools: []
source_repo: WHOISABHISHEKADHIKARI/sme-ops-system-builder
---

# Asset & IT Management（资产与 IT 管理）

**这是什么：** 设备跟踪。

## 概述

针对眼前的业务，推算出最小可用的**资产与 IT 管理**设置,只有在被要求时才构建它。默认输出是一条简短的建议，而非一张表格。各类产出物——CSV、SQL DDL、JSON Schema、Notion 映射——均按需生成，且全部来自同一份字段清单，因此不会相互脱节。

层级：第 3 层：入职（Onboard）。适用于：成长阶段。表格代码：不适用。

## 何时使用此技能

- 资产跟踪器
- IT 资产管理
- 笔记本电脑清单
- 设备登记册

当用户说"设备跟踪"，或描述了同样的流程正发生在表格、文档或某人的收件箱中时，也使用此技能。

不要用于：薪资计算、报税或法律建议。本技能只生成空模板——它从不保存或处理真实的员工或客户数据。

## 工作方式

遵循共享的执行契约。以下模块特定规则仅定义领域字段、决策、计算和安全约束。

### 第 1 步 - 识别意图

阅读请求并在询问任何问题之前确定意图。

- "设置"或"搭建"或"创建" -> 用户想要产出物；进入第 2 步。
- "我们的流程是……"或"它在一个表格里" -> 用户想要迁移现有流程；先记录下来，再进入第 2 步。
- "这样对吗"或"审查"或"审计" -> 用户想要一次检查，而非搭建；根据他们提供的内容作答。
- "我该如何……" -> 建议性问题；直接回答，只有在有帮助时才提出搭建方案。

只在以下情形是最高价值的缺失信息时才询问；否则不要以开场白开头：

> **问：** 公司拥有多少台设备？

### 第 2 步 - 只问缺失的信息

跳过用户在任何之前的消息中已经回答过的内容。逐一询问其余问题，一旦剩余答案不会再改变输出结果，就停止询问。

- **资产** - 有多少资产？/ 笔记本电脑、手机还是两者都有？/ 显示器和其他设备？
- **分配** - 谁来分配？/ 是否需要签收？/ 共用还是个人使用？
- **跟踪** - 是否跟踪序列号？/ 保修日期？/ 保险？
- **当前流程** - 清单现在在哪里？/ 表格还是没有？/ 什么东西会丢失？
- **结果** - 你需要什么？/ 一份清单、归还记录还是支出视图？

永远不要编造答案。如果用户不知道，就记录为未知并继续。

### 第 3 步 - 保留内部上下文

以此结构保留答案。它保持为内部内容——除非用户要求，否则不展示给用户，并且永远不会包含用户没有给出的值。

```yaml
module: asset-it-management
intent: null            # setup | advice | review | fix | build | convert | export
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Assets": null
  "Assignment": null
  "Tracking": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion | xlsx - requested formats only
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### 第 4 步 - 推荐最小化工作流

如果已请求产出物，在解决了关键的缺失信息后再构建它。否则给出一条简短的建议，并提供相关的产出物选项。

**推荐方案：** 将资产作为行记录，配有序列号和指定的持有人。入职当天分配，离职时归还，清单就能保持准确。

**原因：** 资产登记册往往在交接环节失败，而非在采购环节。把每一项资产都绑定到一个人和一个日期，才是保证准确性的关键。

**工作流：** 采购 → 分配给个人 → 存放位置 → 离职归还 → 核销

### 第 5 步 - 仅在请求时构建

一旦用户提出要求，就从已确认的上下文中推导出字段，并生成所请求的产出物。对于机器可读的文本，将行文保留在数据之外；对于文件，提供一个可用的链接。单独报告重大的验证失败或局限性。

**选定的 Notion 输出由 `notion-manual-import` 渲染，因此将 Notion 这一步转交给它处理。**当用户选择 Notion 时，将该步骤交给 @notion-manual-import：它持有 CSV、属性映射、导入步骤和验证清单，并渲染下方的"字段参考"，而不是自行定义一张表格。不要在此重复映射内容，也不要自行修改导入步骤。手动 CSV 和映射类产出物无需任何连接。对于被请求的工作区变更，遵循共享契约：在写入前验证实际的工具访问权限和目标对象。用户说"已连接"并不构成工具证据。永远不要索要 Notion 密码或令牌。

对于与 Excel 兼容的 CSV，使用带字节顺序标记（BOM）的 UTF-8，以便 Excel 正确打开文本。CSV 不是 `.xlsx` 工作簿；只有在用户要求工作簿时才创建 `.xlsx`。
CSV 不携带类型，因此在生成 CSV 之后，需要指出哪些列需要应用数字、日期或货币格式。

```csv
Asset Name,Asset ID,Asset Type,Assigned Date,Assigned To,Linked Accounts,Brand/Model,Condition,Current Value,Department,Location,Notes,Purchase Date,Purchase Value,Currency,Return Date,Serial Number,Status,Warranty Expiry
Example Laptop 14,,Laptop,2026-01-15,Example Employee,"Workspace, VPN",Example Laptop 14 (2023),New,800.00,Delivery,Example City,"Warranty runs to December 2027, so the finance depreciation schedule needs to match.",2026-01-15,1000.00,INR,2026-01-15,SN-EXAMPLE-001,In Use,2027-11-14
```

```sql
CREATE TABLE asset_it_management (
  asset_name VARCHAR(255),
  asset_id SERIAL PRIMARY KEY,
  asset_type VARCHAR(100) NOT NULL,
  assigned_date DATE NOT NULL,
  assigned_to VARCHAR(255),
  linked_accounts VARCHAR(255),  -- relation -> target record
  brand_model VARCHAR(255),
  condition VARCHAR(100) NOT NULL,
  current_value NUMERIC(14,2) NOT NULL,
  department VARCHAR(255),
  location VARCHAR(255),
  notes TEXT,
  purchase_date DATE NOT NULL,
  purchase_value NUMERIC(14,2) NOT NULL,
  currency VARCHAR(255),
  return_date DATE,
  serial_number VARCHAR(255),
  status VARCHAR(100) NOT NULL,
  warranty_expiry DATE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_asset_it_management_status ON asset_it_management (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Asset & IT Management",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "Asset Name": {
      "type": "string"
    },
    "Asset ID": {
      "type": "integer"
    },
    "Asset Type": {
      "type": "string"
    },
    "Assigned Date": {
      "type": "string",
      "format": "date"
    },
    "Assigned To": {
      "type": "string"
    },
    "Linked Accounts": {
      "type": "string"
    },
    "Brand/Model": {
      "type": "string"
    },
    "Condition": {
      "type": "string"
    },
    "Current Value": {
      "type": "number"
    },
    "Department": {
      "type": "string"
    },
    "Location": {
      "type": "string"
    },
    "Notes": {
      "type": "string"
    },
    "Purchase Date": {
      "type": "string",
      "format": "date"
    },
    "Purchase Value": {
      "type": "number"
    },
    "Currency": {
      "type": "string"
    },
    "Return Date": {
      "type": "string",
      "format": "date"
    },
    "Serial Number": {
      "type": "string"
    },
    "Status": {
      "type": "string"
    },
    "Warranty Expiry": {
      "type": "string",
      "format": "date"
    }
  },
  "required": [
    "Asset Type",
    "Assigned Date",
    "Condition",
    "Current Value",
    "Purchase Date",
    "Purchase Value",
    "Status",
    "Warranty Expiry"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Asset Name | Title | Use as the database title |
| Asset ID | Text (preserve source ID) | Keep imported IDs as Text; optionally add a separate Unique ID property |
| Asset Type | Select (add options after import) | Convert to Select, add options: "Laptop", "Monitor", "Phone", "Tablet", "Accessory", "Furniture", "Software License" |
| Assigned Date | Date | Convert to Date |
| Assigned To | Text | Leave as Text |
| Linked Accounts | Relation (link to the target database) | Convert to Relation, link to the target database |
| Brand/Model | Text | Leave as Text |
| Condition | Select (add options after import) | Convert to Select, add options: "New", "Good", "Fair", "Needs Repair", "Retired" |
| Current Value | Number (format: currency) | Convert to Number, set format to Currency |
| Department | Text | Leave as Text |
| Location | Text | Leave as Text |
| Notes | Text | Leave as Text |
| Purchase Date | Date | Convert to Date |
| Purchase Value | Number (format: currency) | Convert to Number, set format to Currency |
| Currency | Text | Leave as Text |
| Return Date | Date | Convert to Date |
| Serial Number | Text | Leave as Text |
| Status | Select (add options after import) | Convert to Select, add options: "In Use", "In Stock", "In Repair", "Retired", "Lost" |
| Warranty Expiry | Date | Convert to Date |
```

上面的数据行仅为文档示例。除非用户明确要求示例，否则生成空模板。金额始终用 `currency`，日期始终用 `date`，任何指向其他表的字段始终用 `relation`。

## 字段参考

`Return Date`（归还日期）在相关生命周期阶段之前，或没有可验证来源时，可能不存在。不要为了满足模式而编造值。

| # | 字段 | 类型 | SQL | JSON Schema | Notion | CSV 示例 |
|---:|---|---|---|---|---|---|
| 1 | Asset Name | `text` | `VARCHAR(255)` | `string` | Text | `Example Laptop 14` |
| 2 | Asset ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (preserve source ID) | `(blank)` |
| 3 | Asset Type | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Laptop` |
| 4 | Assigned Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 5 | Assigned To | `text` | `VARCHAR(255)` | `string` | Text | `Example Employee` |
| 6 | Linked Accounts | `relation` | `VARCHAR(255)` | `string` | Relation (link to the target database) | `Workspace, VPN` |
| 7 | Brand/Model | `text` | `VARCHAR(255)` | `string` | Text | `Example Laptop 14 (2023)` |
| 8 | Condition | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `New` |
| 9 | Current Value | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `800.00` |
| 10 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 11 | Location | `text` | `VARCHAR(255)` | `string` | Text | `Example City` |
| 12 | Notes | `long_text` | `TEXT` | `string` | Text | `Warranty runs to December 2027, so the finance depreciation schedule needs to match.` |
| 13 | Purchase Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 14 | Purchase Value | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `1000.00` |
| 15 | Currency | `text` | `VARCHAR(255)` | `string` | Text | `INR` |
| 16 | Return Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 17 | Serial Number | `text` | `VARCHAR(255)` | `string` | Text | `SN-EXAMPLE-001` |
| 18 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `In Use` |
| 19 | Warranty Expiry | `date` | `DATE` | `string, format: date` | Date | `2027-11-14` |

## 选项值

**Asset Type**

```
Laptop | Monitor | Phone | Tablet | Accessory | Furniture | Software License
```
**Condition**

```
New | Good | Fair | Needs Repair | Retired
```
**Status**

```
In Use | In Stock | In Repair | Retired | Lost
```

## 关联关系

关联字段：`Linked Accounts`

## 示例

**提示语**

```
Laptops keep disappearing after people leave and we cannot find them.
```

**先了解背景** —— 每条消息问一个问题，不重复已回答的内容：

> **问：** 你们是否跟踪序列号？
> **答：** 没有。
>
> **问：** 谁来分配？
> **答：** IT 部门，在入职当天。
>
> **问：** 有多少资产？
> **答：** 大约 40 件。

**推荐的下一步** —— 提供建议，而非直接构建：

> 将资产作为行记录，配有序列号和指定的持有人。入职当天分配，离职时归还，清单就能保持准确。
>
> 工作流：采购 → 分配给个人 → 存放位置 → 离职归还 → 核销
>
> 需要为此生成 CSV、SQL、JSON Schema 和 Notion 映射吗？

## 最佳实践

- 在被要求时构建；对于仅咨询建议的请求，提出建议并提供构建选项。
- 每条消息问一个问题。一次性批量提问会显得像表单，并导致用户随意猜测回答。
- 在 CSV 和 JSON 中保持显示名称一致；对规范化的 SQL 标识符加以文档说明。
- 对于任何指向其他表的内容使用 `relation`，自由文本才用 `text`。
- 金额字段始终用 `currency`，绝不用 `text`。日期字段始终用 `date`，绝不用自由文本。
- 如果用户要求示例行，让它明显是虚构的,以免被当作真实数据导入。

## 局限性

- 仅为空模板。它不计算薪资、税款、休假余额或 KPI。
- Notion 的关联关系需要两个数据库都导入后才能解析链接列。
- 选项值只是一个起点。将它们重命名以匹配业务的实际说法。
- 没有自动化、提醒或同步功能。这些需要集成层支持。
- 不对设备进行镜像、擦除或强制执行 MDM 策略。
- 在用于真正的决策之前，仍需要法律、税务和人力资源审查。

## 安全与安全注意事项

- 永远不要填入真实的姓名、薪资、医疗或银行数据。只能使用占位符。
- 将示例行标记为合成数据，并对银行信息进行掩码处理。
- 本地读取、生成命令和验证属于请求产出物构建的一部分。外部写入、消息发送、资源配置和发布则需要针对该操作和目标获得授权；已有的明确授权不需要重复获取。
- 如果提供了敏感数据，避免重复不必要的标识符。只使用所请求审查所需的内容；保持生成的模板为空。不要声称已从对话或服务存储中删除。
- 隐私、法律和纪律案例在采取任何行动之前都需要合格的人工审查员介入。

## 常见陷阱

- **问题：** 将一份静态映射描述成一个已完成的工作区构建。
  **解决方案：** 在无连接的情况下提供手动映射；只有在授权的工具操作成功后，才声称已完成实时变更。
- **问题：** 在一条消息中问完了全部六个问题。
  **解决方案：** 一次问一个，等待回答，并去掉第一个答案已经覆盖的问题。
- **问题：** 只被要求做一张表,却构建了一整套系统。
  **解决方案：** 只构建被请求的内容；父技能单独提及即可。
- **问题：** 四种产出物相互脱节。
  **解决方案：** 始终从本文件中的字段清单推导全部四种产出物，而不是手工编写。
- **问题：** Notion 导入后每一列都显示为 Text。
  **解决方案：** 这是预期行为。导入完成后，一次性应用属性映射表即可。

## 相关技能

- [模块目录](https://github.com/sickn33/agentic-awesome-skills/blob/main/CATALOG.md) - 找到相关模块，然后阅读其技能文档。
- @people-directory - 本模块关联的大多数员工主记录来源。
- @notification-reminder-hub - 将本模块中的到期日期转化为提醒。

## 可复用提示语

```
I want to set up equipment tracking for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```
