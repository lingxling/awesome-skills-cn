---
name: 360-feedback-system
description: '360 度反馈登记表：评审人、被评对象、评审周期、可见性、截止日期与评分，可按需输出为 CSV、SQL、JSON Schema 或 Notion。适用于 360 度评审或同事互评周期。'
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
- manage
tools: []
source_repo: WHOISABHISHEKADHIKARI/sme-ops-system-builder
---

# 360° 反馈系统

**它是什么：** 每行记录一条反馈回复，字段列表仅根据用户确认的内容构建。

## 概述

为眼前的企业设计出最小可用的 360° 反馈方案，并且仅在被要求时才构建。默认输出是一份简短的建议，而不是电子表格。CSV、SQL
DDL、JSON Schema 和 Notion 映射均由下方唯一的字段参考表（Field Reference）派生而来，因此不会出现彼此不一致的情况。

三个概念模型保持相互独立，因为把它们合并在一起会迫使人凭空捏造字段：

- **Response（回复）** - 每条反馈回复占一行。这是本技能中唯一对应数据表的模型。
- **Scoring Configuration（评分配置）** - 量表、权重、缺失与不适用的处理方式、舍入规则。
  它是配置，绝不是回复行上的一列。
- **Questions（问题）** - 问题集及其版本，仅在各周期之间问题会变化时才保存。只有在确认了该需求之后，问题 ID 才会成为 Response 上的一列。

产物默认是空模板。唯一的示例行只是一个形状占位符，带有 `Example` / `-EXAMPLE-` 值，绝不包含业务数据。

层级：Layer 4：Manage（管理）。适用阶段：成长期。表代码：n/a。

## 何时使用此技能

- 360 feedback
- feedback system
- peer review tool
- 360 degree feedback tracker

当用户说 "holistic feedback"，或描述同样的流程正发生在电子表格、文档或某人的收件箱里时，也可使用它。

不适用于薪资、税务、法律或雇佣决策类工作。本技能不会将这些自动化。

## 工作原理

遵循共享的执行契约。下面的模块专属规则只定义领域字段、决策、计算和安全约束。

下面的规则自成一体。如果位于 `../../references/execution-contract.md` 的共享执行契约不可用，则直接遵循本文件；缺少该引用绝不会阻碍基本执行。

### 步骤 1 - 识别意图

先阅读请求并选定一个意图，然后再提问。这是规范的意图集合，在此处和上下文块中使用相同的拼写：

| 意图 | 触发 | 前往 |
|---|---|---|
| `advice` | "how do I ..."、"what should we" | 作答，仅在有帮助时才提议构建 |
| `review` | "is this right"、"review"、"audit" | 检查他们分享的内容 |
| `build` | "set up"、"build"、"create" | 步骤 2 |
| `convert` | "move it from our sheet/forms" | 先了解他们的流程，再进入步骤 2 |
| `export` | 针对已确认规则的 "give me the CSV / SQL / JSON / Notion" | 步骤 5 |

一条消息，一个问题，不要批量提问。绝不要问那些答案不会改变建议或所请求产物的问题。

### 范围边界

只拒绝超出范围的那个具体高风险操作，并继续处理请求的其余部分。例如：对于把反馈收集与薪资混在一起的请求，拒绝薪资计算，并继续进行反馈方案的设置。

### 步骤 2 - 只问缺失的信息

跳过任何已在先前消息中回答过的内容。其余的逐个提问，一旦剩余的答案不会改变输出就停止。

字段由答案决定，而不是出于习惯。唯一无需确认的字段是下面最小核心中的那些。每个可选字段都需要有已确认的需求作为依据：

| 候选字段 | 仅在用户确认以下情况时才添加 |
|---|---|
| `Score` | 在定义好的量表上采用评分模式 |
| 附加评分字段 | 已命名的能力领域，每个已确认的领域对应一个 |
| `Due Date` | 截止日期是他们流程的一部分 |
| `Reviewer` | 回复是具名的或保密的，而非匿名的 |
| `Review Cycle` | 反馈会运行多个周期 |
| `Submitted Date` | 他们的流程中会为提交打时间戳 |
| `Question ID` | 问题集在各周期之间会变化 |
| `Feedback Subject` | 确实会记录被评对象 |

`Feedback Subject` 保持为通用标签。被评对象可能是一个人、一个项目、一位客户或一个团队，所以类型要向用户询问，而不是默认为员工。

绝不要捏造答案。把它记录为未知，然后继续。`Unknown` 是一个真实的值，表示尚未提供。绝不要把 Unknown 变成零，也绝不要把空白变成零。绝不要重复询问已记录为未知的内容。

像 `yes`、`no`、`maybe`、`same`、`okay` 或 `fine` 这样的回答，不算是对选择题的回答。请改为以明确的选项重新提问：

> **Q:** Which do you mean: **identified** or **anonymous** feedback?
>
> **A:** maybe

对于部分回答，只保留已回答的部分，其余保持为 `Unknown`。

### 步骤 3 - 保持内部上下文

按如下形式保存答案。它保持在内部，除非被询问否则不展示，并且绝不携带用户没有给出的值。

```yaml
module: 360-feedback-system
intent: null            # advice | review | build | convert | export
scale: null             # only when the answer changes the recommendation
areas:
  "Subject": null
  "Relationships": null
  "Visibility": null
  "Scoring": null
  "Follow-up": null
requested_outputs: []   # csv | sql | json | notion | xlsx - only what was explicitly asked
confirmed_facts: []     # only what the user actually said
unknowns: []            # asked and not answered
open_questions: []      # the unanswered ones, in the order worth asking
```

### 步骤 4 - 推荐最小工作流

给出最精简的建议：一句方案说明、一行工作流，以及仅限重要的未解决事实。方案和工作流都要根据已确认的上下文生成。不要在不同请求之间沿用固定的方案、固定的理由或固定的步骤列表。

工作流这一行，要依据用户描述的收集、评审和跟进流程来构建。如果他们没有描述，就说明工作流为 `Unknown` 并提问。不要假定评审角色、自动化分析步骤或某个特定工具。

除非用户要求提供 schema 或产物，否则不要列举字段、状态或 schema 映射。跟进与完成是流程步骤，不是本模块中的字段。

当提到了评分但其策略不完整时，要逐项明确标注每个缺失的输入：
`Scale: Unknown`、`Included scores: Unknown`、`Weights: Unknown`、
`Missing-score behavior: Unknown`、`Not-applicable handling: Unknown`、`Rounding: Unknown`。在这六项全部确定之前，不要计算总体得分。

不要主动构建。以一项提议收尾，列出尚未被请求的产物。

### 步骤 5 - 仅在被请求时构建

一旦被要求，就根据已确认的上下文推导字段，并且只输出所请求的产物。当请求了不止一种时，要在一次处理中基于同一份字段参考表生成所有产物，使它们不会相互矛盾。

**被选中的 Notion 输出由 `notion-manual-import` 渲染，因此将 Notion 这一步路由到那里。** 当用户选择 Notion 时，把这一步交给
@notion-manual-import：它持有 CSV、属性映射、导入步骤和验证清单，并且它渲染下方的字段参考表，而不是自行定义一张表。不要在此处重述映射，也不要临时编造导入步骤。手动 CSV 和映射输出不需要连接。对于被请求的工作区变更，遵循共享契约：写入之前先核实实际的工具访问权限和目标。用户说 "connected" 并不是工具层面的证据。
绝不要索要 Notion 密码或令牌。

回复之前先验证，然后检查跨格式的一致性：所有产物中的字段名相同、拼写相同、顺序相同、必填集合相同。

回复时给出产物或链接，只有在存在错误、限制或需要提示的未解决未知项时才附上简短说明。不要在一个本来干净的产物请求后面追加列数、验证声明或结束语。

如果产物生成或验证失败，用一行返回错误，指明失败的字段或格式，输出已成功的产物，并说明缺少哪一个。绝不要用看似合理的值替代来让构建通过。

下面的示例展示的是一种文档化的形状。它们不是这家企业的 schema。

**CSV。** 采用带字节顺序标记（BOM）的 UTF-8，以便 Excel 正确打开文本。CSV 不是
`.xlsx` 工作簿；只有在用户要求时才创建后者。CSV 不携带类型，因此当被要求提供导入指引时，要指明哪些列需要应用数字、日期或货币格式。

```csv
Feedback ID,Feedback Type,Feedback Subject,Reviewer,Visibility Mode,Review Cycle,Submitted Date,Status,Due Date,Score,Comments
,Peer,Example Subject 01,Example Reviewer,Identified,Example Cycle 2026-Q1,2026-01-15,Collecting,2026-01-22,4,Example comment recorded to show free text.
```

**SQL。** 使用可移植的类型。引擎未知，所以 `SERIAL PRIMARY KEY` 以 PostgreSQL 的形式展示；在引擎未确认时，使用可移植的 `feedback_id <int type> PRIMARY KEY`，并用一行说明引擎。此处不对 Select 列生成 `CHECK`，因为选项列表尚不是已确认的分类体系。一旦用户确认了某个 Select 字段的选项，就根据该已确认的集合生成约束：

```text
ALTER TABLE feedback_cycle_responses ADD CONSTRAINT chk_feedback_type CHECK (feedback_type IN (<confirmed options>));
```

```sql
CREATE TABLE feedback_cycle_responses (
  feedback_id SERIAL PRIMARY KEY,
  feedback_type VARCHAR(100) NOT NULL,
  feedback_subject VARCHAR(255),
  reviewer VARCHAR(255),
  visibility_mode VARCHAR(100) NOT NULL,
  review_cycle VARCHAR(255),
  submitted_date DATE,
  status VARCHAR(100) NOT NULL,
  due_date DATE,
  score NUMERIC,
  comments TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_feedback_cycle_responses_status ON feedback_cycle_responses (status);
```

**JSON Schema。** `required` 源自业务必要性，而不是现有数据恰好包含什么。三个必填字段是缺少它们就无法解读一条回复的字段。
`Reviewer` 和 `Due Date` 不在 `required` 中，因为合法的回复可以省略它们。

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "360 Feedback Response",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Feedback ID": { "type": "integer" },
      "Feedback Type": { "type": "string" },
      "Feedback Subject": { "type": "string" },
      "Reviewer": { "type": "string" },
      "Visibility Mode": { "type": "string" },
      "Review Cycle": { "type": "string" },
      "Submitted Date": { "type": "string", "format": "date" },
      "Status": { "type": "string" },
      "Due Date": { "type": "string", "format": "date" },
      "Score": { "type": "number" },
      "Comments": { "type": "string" }
  },
  "required": [
      "Feedback Type",
      "Visibility Mode",
      "Status"
  ]
}
```

**Notion。** 这是一张映射表，而不是构建。导入后再转换属性。

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Feedback ID | Title | Use as the database title |
| Feedback Type | Select (add options after import) | Convert to Select, add options: "Self", "Peer", "Manager", "Direct Report", "Cross Functional" |
| Feedback Subject | Text | Leave as Text |
| Reviewer | Text | Leave as Text |
| Visibility Mode | Select (add options after import) | Convert to Select, add options: "Identified", "Confidential", "Anonymous" |
| Review Cycle | Text | Leave as Text |
| Submitted Date | Date | Convert to Date |
| Status | Select (add options after import) | Convert to Select, add options: "Not Launched", "Collecting", "Consolidated", "Shared", "Closed" |
| Due Date | Date | Convert to Date |
| Score | Number | Convert to Number |
| Comments | Text | Leave as Text |
```

Notion 自带的自动 ID 是平台特有的，并不能取代规范的 `Feedback ID`。把其中一个用作 Notion 的主列，另一个用作业务引用，并说明哪个是哪个。

**内联与文件。** 内联输出把产物直接放在消息中返回。文件输出则返回链接。不要混用：当请求的是内联数据时绝不返回链接，当请求的是文件时也绝不返回内联数据。

## 字段参考

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Feedback ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text | `(blank)` |
| 2 | Feedback Type | `select` | `VARCHAR(100) NOT NULL` | `string` | Select (add options after import) | `Peer` |
| 3 | Feedback Subject | `text` | `VARCHAR(255)` | `string` | Text | `Example Subject 01` |
| 4 | Reviewer | `text` | `VARCHAR(255)` | `string` | Text | `Example Reviewer` |
| 5 | Visibility Mode | `select` | `VARCHAR(100) NOT NULL` | `string` | Select (add options after import) | `Identified` |
| 6 | Review Cycle | `text` | `VARCHAR(255)` | `string` | Text | `Example Cycle 2026-Q1` |
| 7 | Submitted Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 8 | Status | `select` | `VARCHAR(100) NOT NULL` | `string` | Select (add options after import) | `Collecting` |
| 9 | Due Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-22` |
| 10 | Score | `number` | `NUMERIC` | `number` | Number | `4` |
| 11 | Comments | `long_text` | `TEXT` | `string` | Text | `Example comment recorded to show free text.` |

这张表是唯一的数据来源。CSV 表头、SQL 列、JSON Schema 属性和 Notion
映射都由它生成，绝不手工编写。

有三条规则约束它：

- **命名。** 一个人类可读的标签加一个机器安全的键，只定义一次并在各处复用。
  键是将标签转为小写、并把非字母数字字符替换为 `_` 后得到的结果。
- **纳入。** 只有在有已确认的需求作为依据时，字段才会存在。这就是列表很短的原因。
- **去重。** 在输出任何产物之前，合并语义等价的字段。一个身份，一个字段。同一条记录的第二个标识符属于重复，除非用户要求在系统键之外再提供一个便于人读的引用。

`created_at` 和 `updated_at` 是仅存在于产物中的唯二补充项。它们是技术元数据，不是业务字段，并且会被如此标注。

## 选择项

这些列表是一种文档化的形状，而不是已确认的分类体系。Notion 一列始终写着
"add options after import"。如果用户提供了自己的值，则以他们的为准，这些列表被替换。绝不要把它们当作企业已确认的选项呈现。

**Feedback Type**

```
Self | Peer | Manager | Direct Report | Cross Functional
```

**Visibility Mode**

```
Identified | Confidential | Anonymous
```

**Status**

```
Not Launched | Collecting | Consolidated | Shared | Closed
```

Status 列表是一个最小的默认生命周期。仅在用户确认其周期具有这些阶段时才使用；否则根据他们描述的流程推导状态，或者在无需跟踪任何内容时省略该字段。

## 关联

没有关联字段。`Feedback Subject` 是文本，不是关联，因为被评对象的类型取决于用户的说法，而且不能保证存在任何目标数据库。如果用户在同一组产物中确认了被评对象目录，届时再将其建模为关联，并在 SQL 中保持目标为
`VARCHAR(255)` 并附上注释。

## 评分配置

它不是一张表。它是配置，存储在回复行之外。仅在用户确认要评分时才保存它，并且把每个未设置的输入报告为 `Unknown`，而不是假定默认值：

| 设置 | 在任何总体得分存在之前所需要的 |
|---|---|
| Scale | 允许的取值及其含义 |
| Included scores | 哪些字段参与计算 |
| Weights | 每个字段的权重，或明确的 `equal` |
| Missing-score behavior | 排除，或按零计 |
| Not-applicable handling | 与缺失不同：`N/A` 是一种有意的回答 |
| Rounding | 小数位数，以及是否仅在最后才舍入 |

`Not Applicable` 是评审人选择的一个值。要把它与缺失或未回答的评分区分开；缺失的评分和有意作出的 `N/A` 绝不能合并为同一个结果。

总体得分根据这些设置计算，绝不存储在回复行上。除非公式、输入和舍入规则都与之并列展示并且完全吻合，否则不要展示带计算过程的总体得分示例。

## 示例

**Prompt**

```
We have 12 people and want managers and peers to give anonymous feedback.
```

**先了解上下文** - 每条消息一个问题，不重复已回答的内容：

> **Q:** 这些反馈是用来做什么的？
> **A:** 绩效评估和团队改进。
>
> **Q:** 你们现在是如何收集的？
> **A:** Google Forms 和 Sheets。
>
> **Q:** 要评分、评论，还是两者都要？
> **A:** 两者都要。
>
> **Q:** 量表和权重尚未确定。评审人从哪些值中选择，各个领域的权重是否相同？
> **A:** 五分制，全部相同。
>
> **Q:** 收集结束后会怎样？
> **A:** 由经理阅读汇总，然后我们一起讨论。

**推荐的下一步** - 只是提议，不构建。下面的工作流是根据所提供的两条流程事实生成的，而不是从模板沿用的：

> 保留现有的收集工具并增加一个分析层，因为收集环节已经运转良好。只有在量表确定之后，评分才会变得有用，而现在已经确定：五分制，各领域权重相同。
>
> 工作流：Google Form 到 Sheet，经理阅读汇总，团队讨论
>
> 舍入规则仍为 `Unknown`。告诉我小数位数，我就可以构建 CSV、SQL DDL、JSON Schema 和 Notion 映射。

## 最佳实践

- 被要求时就构建；对于仅咨询的请求，给出建议并提议构建。
- 每条消息一个问题。批量式的收集看起来像一张表单，只会让人去猜。
- 基于字段参考表生成每一个产物，然后确认它们一致。
- 询问每个可选字段取代的是哪个字段，并去掉其余的。
- 不要把总体得分放进回复行。
- 如果用户要求示例行，要让每个值都明显是假的，以免有人导入它。

## 局限性

- 只输出空模板。它不运行收集、提醒、同步或调度。
- 不计算薪资、税务、休假余额、税务处理或雇佣决策。
- 评分是配置，不是自动化：本技能不会计算、汇总或对评审人排名。
- Notion 映射假定属性在导入后再转换。
- 选择项只是一种形状。在被确认之前，它们不会成为企业的分类体系。
- 不能替代人力资源或法务审查，也不做任何雇佣决策。

## 安全与安全注意事项

- 绝不要提供真实的姓名、联系方式、标识符、金额或日期作为示例。只使用示例值，标识符采用 `-EXAMPLE-` 模式。
- 产物默认是模板，不携带真实的个人数据。如果用户粘贴了真实的反馈数据，就构建模板，并且不要保留或复现其中不必要的敏感内容。
- 如果用户持有所粘贴数据的存储副本，建议他们在适当的情况下从自己的记录和设置中删除敏感信息。不要声称自己已经删除了任何内容。
- 在 `Anonymous` 模式下，让 `Reviewer` 保持空白。绝不要推断或重建身份。
- 提醒：无论处于哪种可见性模式，自由文本评论都可能通过内容暴露评审人身份。
- 当贡献回复的数量低于可配置的最小值时，抑制聚合结果。向用户询问该最小值；不要悄悄自行选定。
- 在反馈影响任何真实个人的雇佣、薪酬、晋升或绩效记录之前，必须经过人工审核。

## 常见陷阱

- **问题：** 把静态映射描述成已完成的工作区构建。
  **解决方案：** 手动映射无需连接即可交付；只有在获授权的工具操作成功之后，才声称做了实时变更。
- **问题：** 回复行最终携带了配置。
  **解决方案：** 权重、舍入和量表都放在评分配置中。
- **问题：** 因为类似模块里有某字段，所以它出现了。
  **解决方案：** 没有已确认的需求，就没有字段。
- **问题：** 出现了一个没人能复现的类似合计的值。
  **解决方案：** 展示公式和输入，否则什么都不展示。
- **问题：** Notion 导入后每一列都显示为 Text。
  **解决方案：** 这是预期行为。导入后一次性应用属性映射即可。

## 相关技能

仅供参考。运行本技能不需要其中任何一个，缺少其中之一也绝不会阻碍执行。

- [Module Catalog](https://github.com/sickn33/agentic-awesome-skills/blob/main/CATALOG.md) - 找到相关模块，然后阅读它的技能。
- @people-directory - 一个可能的被评对象来源，前提是用户选择为其建模。
- @notification-reminder-hub - 可选，如果用户希望把截止日期转为提醒。

## 可复用提示词

```
I want to set up holistic feedback for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, derive every requested format from one field list, and give me the data or the link.
```
