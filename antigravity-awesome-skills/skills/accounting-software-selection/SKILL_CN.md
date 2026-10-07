---
name: accounting-software-selection
description: '依据 57 个有证据支撑的字段，为入围的会计软件包打分，可按需输出为 CSV、SQL、JSON Schema 或 Notion。适用于会计软件选型。'
category: business
risk: safe
source: self
source_type: self
date_added: '2026-09-26'
author: WHOISABHISHEKADHIKARI
tags:
- sme
- accounting
- audit
- finance
- database
- csv
- notion
- sql
- evaluation
tools: []
source_repo: WHOISABHISHEKADHIKARI/sme-ops-system-builder
---

# 会计软件选型

**它是什么：** 软件采购背后的证据记录，使这项决策可以被论证——而决策本身仍然属于企业。

## 概述

为眼前的企业梳理出最小而有用的**会计软件选型**配置，并且仅在被要求时才去构建。默认输出是一份简短的推荐，而不是一张电子表格。工件——CSV、SQL DDL、JSON Schema、Notion 映射——按需产出，且都来自同一份字段列表，因此不会彼此漂移。

对于尼泊尔的贸易、制造或服务型企业，这份记录使采购变得可以论证：需求已排序、有候选短名单、对每个候选者运行相同的演示测试、每个分数背后都有证据、成本被拆分以便比较第一年和三年的总额，并且评估状态、选型决策、否决原因和一票否决（deal-breaker）标记被保存为四个独立字段，而不是一个笼统的意见。它是评估与决策支持工具，不是记账、报税、法务或采购系统。

四条护栏塑造每一行记录。

**不编造任何内容，没有来源就不断言任何事。** 绝不提供用户或某个具名来源没有给出的供应商能力、价格、合规状态、演示结果或干系人评分。无人验证过的内容，对于能力是 `Untested`，对于价格则是空的成本单元格并在 `Notes` 中写 `Unknown`。无人查看过的能力是 `Untested`；它不是 `1 Missing`，也绝不会为了让这一行看起来完整而用一个看似合理的数字填补空白。

**本技能从不做选择。** 它可以总结证据、指出某个候选者未满足的需求，并说明某项 Must-have 未通过。它不得宣布某个软件包是最佳选项、宣布赢家、给出合规结论或记录批准。`Selection Decision` 由企业自己填写。

**事实与意见分开。** 三十个能力字段记录供应商所记录或演示过的内容。三个 `Rating` 字段记录具名评估者自己的判断。宣传册上的说法绝不会被复制进 Rating，评估者的印象也绝不会被写进能力字段。跨评估者的平均值不是客观真相，分数也绝不会变成推荐。

**尼泊尔的税务和法定声明需要有引用的、最新的证据。** VAT、PAN、TDS、IRD 报告、电子开票、CBMS、尼泊尔财年与 BS/AD 日期、薪资和 SSF，在企业持有来自供应商或主管机关的最新证据之前，都是 `Untested`。不得凭宣传册或销售页面声称合规状态，而且无证据既不能证明有，也不能证明无。

层级：Layer 1：Foundation。适用阶段：Growth 阶段。表代码：n/a。

## 何时使用此技能

- 会计软件选型
- 会计与 ERP 软件对比
- 供应商演示评估表
- 会计软件包报价跟踪表
- 三年软件成本对比

当用户描述的是在选定之前对入围会计软件包进行打分评估，或者同样的流程正发生在电子表格、文档或某人的收件箱里时，也可使用它。

不要在以下情形使用：软件上线后的日常记账、报税、供应商合同或法律建议。本技能只产出空模板——它从不持有或处理真实的员工、客户、供应商或供应商方数据。

## 工作原理

遵循共享的执行约定。下面的模块特定规则只定义领域字段、决策、计算和安全约束。

### 第 1 步 - 识别意图

在提问之前，先阅读请求并选定意图。

- "set up" 或 "build" 或 "create" -> 用户想要工件；转到第 2 步。
- "compare" 或 "which one should we pick" -> 用户想要一次评估；先获取短名单，然后进入第 2 步。
- "our process is ..." 或 "it is in a sheet" -> 用户想迁移一项现有的评估；先获取它，然后进入第 2 步。
- "is this right" 或 "review" 或 "audit" -> 用户想要检查，而不是构建；根据他们分享的内容作答。
- "report" 或 "how do I ..." -> 咨询类问题；直接回答，只有在有帮助时才提供构建。

然后读完用户已经说过的所有内容，找出那个最能改变评估的、唯一缺失的答案。如果请求中已包含足够的信息来给出推荐，就先不要提问——直接进入第 4 步。如果用户描述的是一个问题而不是请求评估，则先回答它；并不欠对方一个提问。

一条消息，一个简短的问题，不要成批提问。以此开场：

> **Q:** 你们目前的短名单上有哪些会计或 ERP 软件包？

当请求中已经点明了软件包时，绝不要以这个问题开场，也绝不要用一个不会改变输出的问题开场——"本月你们最大的费用类别是什么"完全无法说明哪个软件包更合适。如果没有短名单，不要强行构造：先收集业务需求，并在第 4 步根据需求建立候选短名单。

不要在一个会改变评估的事实之前，去澄清可选的标识符、标签或引用。`Evaluation ID`、供应商名称以及其他可选的记录标签可以保持 `Unknown`；先问短名单，没有短名单时先问业务需求。

### 第 2 步 - 只询问缺失的信息

把含糊的回复视为未回答，并询问用户指的是哪个明确的选项。把未知值记录为 `Unknown`；`Unknown` 不是零。当必需的检查未通过时，记录不得为 `Done`。

跳过用户在之前任何消息中已经回答过的内容。其余的按下面的顺序一次问一个，因为这个顺序是从最能改变比较结果的答案排到最不影响它的答案。一旦剩余答案不会改变短名单、某个分数或构建，就停止。

1. **短名单** - 哪些软件包，或者没有短名单、需要根据需求建立。
2. **企业做什么** - 贸易、制造、服务，或混合。这决定了 35 个类别中哪些值得打分。
3. **规模** - 人数、每月交易笔数、公司数、分支机构数、仓库数。只有当答案会改变短名单时才问。
4. **需求及其优先级** - 先要求列出清单，然后要求把每一项排序为 Must-have、Should-have、Nice-to-have 或 Not required。在给任何东西打分之前，一票否决规则需要这个排序。
5. **尼泊尔需求** - VAT、PAN、TDS、IRD 报告、电子开票或 CBMS、尼泊尔财年与 BS/AD 日期、薪资、SSF。不要假定某个软件包支持其中任何一项。
6. **平台** - 云端或本地部署、权限、审批、制单-复核（maker-checker）、备份、安全、API、集成、数据导出、迁移、定制、本地支持、培训。
7. **资金** - 使用哪种币种，以及手头是否有书面报价。价格只能取自报价单。
8. **成果** - CSV、SQL DDL、JSON Schema、Notion 映射、上线检查清单，或仅仅是评估。没有被要求的不要构建。

没有做出选择的回答不算回答。对多选题回答 `yes`、`maybe`、`same`、`okay` 和 `fine` 一概被拒绝，并重新明确地询问选择：

> **Q:** 对于会计范围，你指的是哪一个：**仅总账和银行对账**，还是**总账、应收款、应付款和固定资产**？

部分回答保留已给出的那部分，其余保持 `Unknown`。绝不要填补空白。

绝不要编造答案。把它记录为 `Unknown` 并继续，同时绝不要重复询问同一个未知项。`Unknown` 不是零，`Unknown` 也不是低分：没有人报价的价格让成本单元格保持为空，没有人检查过的能力是 `Untested`，绝不是 `1 Missing`，也绝不是 `0`。

### 第 3 步 - 保存内部上下文

把答案按这种形态保存。它是内部的——除非用户询问，否则不向用户展示，并且它绝不会带有用户没有给出的值。

```yaml
module: accounting-software-selection
intent: null            # set in Step 1, one of: set up, compare, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Shortlist": null
  "Business activities": null
  "Requirements priority": null
  "Nepal requirements": null
  "Platform and money": null
requirement_priority: null   # each need as Must-have | Should-have | Nice-to-have | Not required
candidates: []          # shortlist, each with its own row and its own evidence
unverified: []          # every capability still Untested and every cost still Unknown
requested_outputs: []   # csv | sql | json | notion | xlsx - requested formats only
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

`unverified` 是在做出任何推荐之前必须可见的列表。无论分数如何，只要其中有条目，该候选者就还没有准备好被标为 `Selection Decision: Selected`。

### 第 4 步 - 推荐最小的工作流

给出一份简短的推荐，然后询问是否要构建。不要擅自构建，也不要在其中点名偏好的软件包。

**推荐的方法：** 每个入围软件包一条评估记录，在相同的能力、成本和支持字段上打分，证据和评估者与分数放在一起，使比较可重复，并且上线设置也来自同一条记录。

**为什么选这个：** 软件决策往往靠记忆来争论。用相同的字段、相同的测试给每个候选者打分，把争论变成一张表——并且让企业的决策保持可见，而不是埋在某个汇总列里。

**工作流：** Requirements → Candidate Shortlist → Vendor Demo → Standardized Tests → Stakeholder Evaluation → Cost/TCO Review → Business Decision → Configuration → Migration → Training → Go-live

**短名单：** 如果用户没有短名单，就依据已确认的需求建立一个。候选名称只是起点，因为是否入围取决于需求以及从最新来源核实过的能力。没有证据时，绝不要说某个具名产品支持或缺乏某项能力。

**需求优先级：** 在给任何东西打分之前，先把每一项需求排序为 Must-have、Should-have、Nice-to-have 或 Not required。规范列表中没有用于排序的单独列，因此把它写进 `Modules Needed`，使用 `Must-have:`、`Should-have:`、`Nice-to-have:` 和 `Not required:` 前缀，每行一条。

**一票否决：** 未通过某项 Must-have 的候选者被标记为 `Deal-breaker: Yes`。其他任何地方的分数都不得掩盖它，平均值也不是绕过它的办法。只有在候选者针对每一项 Must-have 都测试过之后，才写 `No`；在此之前 `Deal-breaker` 读作 `Unknown`，因为没有测试过的候选者并未被证明可以通过。

**评估框架：** 每个候选者都在相同的 35 个类别上打分——会计、销售、采购、库存、制造、BOM、生产/工单、生产成本核算、损耗/废料、批次/批号追踪、服务、VAT、TDS、薪资/SSF、尼泊尔法定报告、电子开票/CBMS、财务报告、多公司、分支机构、仓库、用户权限、审批工作流、安全、备份/恢复、数据迁移、API/集成、数据导出、实施、培训、定制、本地支持、可靠性、易用性、支持质量、总拥有成本。这 33 个打分字段覆盖了这 35 个类别：`Data Backup & Security` 同时承载安全和备份/恢复，只打一次分，所以当演示显示两者处于不同水平时，请把差异写在 `Notes` 中，而不是取平均。

**打分与证据：** 1 缺失或不可用，2 重大局限，3 够用，4 强，5 全面——另有 `Not Required` 表示企业不需要的能力，`Untested` 表示无人检查过的能力。只有依据供应商文档、供应商演示、试用、实际测试交易、书面报价，或具名评估者的评估，才能写下分数，并且证据写入 `Evidence/Source`，人员写入 `Evaluated By`，并附上收集日期。`Untested` 不是 `1 Missing`：无人查看是评估中的缺口，不是一个发现。

**事实与意见：** 三十个能力字段记录供应商所记录或演示过的内容。`Reliability Rating`、`Ease of Use Rating` 和 `Support Quality Rating` 记录评估者自己的意见，使用相同的 1-5 量表和相同的含义，使 `Untested` 和 `Not Required` 依旧可以记录——一个单纯的数字无法表示 `Untested`，而没有标签的数字是没人能核查的分数。绝不要把其中一个复制到另一个中。

**干系人：** 财务/会计、运营、制造、管理层、IT/管理员、销售和采购都可以分别评估。让每位评估者的看法附在他们自己的记录上或使用他们自己的话，并展示分歧；跨评估者的平均值不是客观真相。如果企业希望把每位评估者的看法保存为单独一行，就用不同的 `Evaluated By` 重复同一个 `Software` 值——绝不要把它们合并成一个数字。

**标准演示测试：** 每个候选者都尝试同一份脚本——日记账、总账过账、银行对账、试算平衡表、损益表、资产负债表；客户、报价单、发票、VAT 发票、退货、收款；供应商、采购订单、采购发票、VAT 采购、退货、付款；库存收货、发料、仓库调拨、调整、估值；BOM、生产订单、原材料消耗、成品、损耗/废料、生产成本；服务项目、客户/项目、服务发票、费用分摊、盈利性；VAT、TDS、法定报告、电子开票/CBMS；薪资运行、SSF 计算、薪资会计分录；用户、权限、审批工作流、备份/恢复；主数据、期初余额、期初库存、对账。无人运行的测试，在该类别上记为 `Untested`，在 `Demo Test Result` 中记为 `Not Tested`；实际尝试的数量写入 `Test Transactions Run`。

**成本、币种与合计：** 把成本拆分为供应商报价的各项——许可证或订阅、实施、定制、培训、年度续费，以及任何配置、数据迁移、硬件、持续支持、按用户、按分支机构或按模块收取的费用。该行为本表持有的第一年各项（`Licence Cost`、`Implementation Cost`、`Customization Cost`、`Training Cost`）以及 `Annual Renewal` 设有列；其余每一项报价在此都没有对应列，所以请把金额及其来源记录在 `Evidence/Source` 中并加入 `First-Year Cost`，或者有意识地把这些列添加到全部四种工件中。绝不要为了让合计成立而把一项未报价的成本并入 `Licence Cost`。

- `First-Year Cost` = `Licence Cost` + `Implementation Cost` + `Customization Cost` + `Training Cost`，再加上供应商报价的任何其他第一年项目。
- `Three-Year TCO` = `First-Year Cost` + (2 x `Annual Renewal`)，以三年为期。如果企业设定了不同的期限，就改变期限和公式，并说明使用了哪个期限。

只有当其中的每一项都是企业实际持有的数字时，才计算合计。如果缺少某一项，合计就是 `Unknown` 并保持为空——建立在猜测项之上的合计就是编造的价格。如果计算出的合计不等于各部分之和，就把差异记录在 `Notes` 中，并说明哪一项未经核实。绝不要为了让合计吻合而更改某个组成项。

**金额基准：** 每个成本字段都保存一个不带货币符号的纯数字，与报价单上所述完全一致。**NPR 是默认值，不是规则**——它适用于尼泊尔的成本，除非用户指明了另一种币种，此时以用户的为准；把每笔金额所用的币种记录在 `Evidence/Source` 中报价单的旁边。报价是含税还是不含税，是供应商的声明，绝不假定：不要加 VAT，不要剥离它，也不要从费用中扣除某项扣减。只在最后取整一次——每个组成项都严格按报价书写，只有 `First-Year Cost` 和 `Three-Year TCO` 在相加之后取整，保留到小数点后两位。

**上线检查清单：** 按需提供一份单独的检查清单，涵盖财务、销售、采购、库存、制造、服务、薪资、尼泊尔合规、安全、迁移和培训，然后是用户验收测试、问题解决、最终对账、管理层签字确认、最终备份、上线日期和上线后支持。它是企业与供应商共同执行的列表；其中没有任何一项是在这里完成的。

**记录决策之前的控制：**

- `Evaluation Status` 可以在部分能力为 `Untested` 时为 `Evaluated`，只有当 `Notes` 中点名这些能力时才是正当的。当某项 Must-have 为 `Untested` 时，它不得为 `Evaluated`：未测试的必备项要么去测试，要么附理由降级，绝不绕开它打分。
- 当 `Deal-breaker` 为 `Yes` 时，`Selection Decision` 不得读作 `Selected`；当某项 Must-have 为 `Untested` 时，也不得读作 `Selected`。
- `Selection Decision` 和 `Rejection Reason` 由企业来写。总结证据并说明一票否决项；把决策留给对方。
- 分数不是裁决。总分很高但 Must-have 未通过，依然是 Must-have 未通过。

然后询问："要不要我根据这些已确认的规则，构建 CSV、SQL DDL、JSON Schema、Notion 映射或 Excel 工作簿？"

### 第 5 步 - 仅在被要求时构建

当用户明确要求 CSV、SQL DDL、JSON Schema、Notion 映射或其他受支持的工件时，遵循[随附的 build-artifacts 参考文档](references/build-artifacts.md)中完整的构建流程。它包含各格式的模板和计算；请使用规范的字段参考，并保持示例数据为虚构。

## 字段参考

规范的 57 字段表结构、跨格式类型映射和示例值，维护在[随附的字段参考文档](references/field-reference.md)中。保持 CSV、SQL、JSON Schema 和 Notion 输出与该表一致；不要编造字段或值。

## 选项值

可直接导入的选项值列表维护在[随附的 select-options 参考文档](references/select-options.md)中。把它们当作起始值，并重命名以匹配企业的用语；用户提供的值优先。

## 关联关系

关联字段：无

本表是独立的。`Software`、`Vendor` 和 `Evaluated By` 是名称，不是关联——短名单里理所当然会包含企业没有登记册的软件包，并且同一位评估者可能为多个候选者打分。`Evidence/Source` 保存对供应商文档、演示或报价单的引用。只有当企业还运行着报价或演示登记册，并且该引用指向那里的真实一行时，它才会变成关联；届时请有意识地把它加到全部四种工件中，或者保持为文本并说明这一点。

## 示例

**提示词**

```
We are replacing our accounting package and cannot tell which one actually covers payroll and what it costs over three years.
```

**先了解背景**——每条消息一个简短的问题，已回答过的不再问：

> **Q:** 短名单上有哪些会计或 ERP 软件包？
> **A:** 一个云端产品和一个本地部署产品。
>
> **Q:** 薪资对企业来说是必备项吗？
> **A:** 要么是必备项，要么就不要。我还不知道——老板还没说。
>
> **Q:** 有人持有书面报价吗？
> **A:** 目前有一份。其中不包含续费。

**推荐的下一步**——只是提供，不去构建，也不点名任何赢家：

> 每个入围软件包一条评估记录，在相同的能力、成本和支持字段上打分，证据和评估者与分数放在一起。
>
> 薪资仍未排序，而一票否决规则需要在给任何东西打分之前有这个排序——所以它是下一个问题，并且它会改变两个候选者中哪一个能够留存。第二个产品没有报价，所以它的成本单元格保持为空，它的 `Deal-breaker` 读作 `Unknown`，直到续费被报价；不要用我们并不持有的价格去填补任何一个。
>
> 工作流：Requirements → Candidate Shortlist → Vendor Demo → Standardized Tests → Stakeholder Evaluation → Cost/TCO Review → Business Decision → Configuration → Migration → Training → Go-live
>
> 需要为此生成 CSV、SQL DDL、JSON Schema 和 Notion 映射吗？

## 最佳实践

- 在给任何东西打分之前，先把每项需求排序为 Must-have、Should-have、Nice-to-have 或 Not required，使一票否决规则有可依据之处。
- 在相同的 35 个类别和相同的演示测试上给每个候选者打分，否则这张表只是一份意见清单，而不是一次比较。
- 绝不写没有证据的分数，也绝不让高总分掩盖未通过的 Must-have。把它标记为 `Deal-breaker: Yes`，让企业来决定。
- 对任何无人检查过的内容使用 `Untested`，绝不用 `1 Missing`。从未被查看的能力根本没有分数。
- 把重要分数背后的证据记录在 `Evidence/Source` 中——来源类型及日期——并在 `Evaluated By` 中记录提供者，使一个数字可以被追溯。
- 把供应商记录的能力与评估者的意见放在不同的字段中。不要把评估者平均成一个裁决，也不要把分数变成推荐。
- 比较三年，而不是一年，并且只依据企业实际持有的数字。不完整的成本项意味着合计是 `Unknown`。
- 写一个空单元格，而不是没人给过你的报价，并且如果读者需要知道它已被检查过，就在 `Notes` 中写 `Unknown`。
- 被要求时才构建；对于仅咨询的请求，给出推荐并提供构建。
- 成批的信息收集读起来像表单，只会被随便猜着填。
- 在 CSV、SQL、JSON Schema 和 Notion 中保持每个字段名完全一致。
- 金额字段是 `currency`，绝不是 `text`。日期是 `date`，绝不是自由文本。
- 如果用户要求一行示例，请让它显然是假的，以免有人把它当作真实数据导入。

## 局限性

- 只是空模板。它不会替你打分、运行演示、核实供应商的说法，也不会把报价单变成 TCO。
- 它从不选择软件包。它只记录企业在 `Selection Decision` 中做出的决策，并在旁边附上 `Rejection Reason` 和 `Deal-breaker`；它不做决定，也不点名偏好的软件包。
- 不是记账、报税、法务或采购系统。报价单、合同和采购订单仍留在供应商自己的流程中。
- 它无法替你核实尼泊尔 IRD、VAT、TDS、电子开票、CBMS 或 SSF 的处理。在企业持有来自供应商或主管机关的最新证据之前，这些保持为 `Untested`。
- 它不能确认某个产品是否真如供应商页面所说。这需要一位具名的人工核验者和一个有日期的来源。
- 上线检查清单是企业与供应商共同执行的列表。科目表、税务配置、用户、库存、期初余额和测试分录并非由本技能完成。
- `Software`、`Vendor` 和 `Evaluated By` 是自由文本，所以重复的软件包或评估者是本表无法捕捉的数据录入问题。
- 没有关联字段。没有指向报价、演示或产品登记册的链接。
- 选项值只是起始集合。请重命名以匹配企业的说法。
- 没有自动化、提醒或同步。这些需要集成层。
- 在这份记录驱动一次真实采购之前，仍然需要采购、税务和法务审查。

## 安全与保密注意事项

- 绝不编造供应商能力、价格、合规状态、演示结果或干系人评分。如果无人提供，它就保持为 `Untested`，或者成本单元格保持为空，并把缺口记录在 `Notes` 中。
- 每项供应商能力、每个价格和每项合规声明，在被记录为事实之前，都需要一位具名的人工核验者和一个有日期的来源。本技能无法确认某个产品是否真如页面所说，也绝不能把未经核实的声明当作发现来呈现。
- 没有来自可靠来源的最新证据，绝不声称尼泊尔 IRD、VAT、TDS、电子开票、CBMS 或 SSF 合规。无证据既不能证明有，也不能证明无。
- 把供应商记录的事实与干系人的意见分开。一个字段记录供应商展示了什么，一个字段记录评估者对此的看法，绝不把两者混合。
- 绝不宣布赢家或偏好的软件包，也绝不自己记录 `Selection Decision: Selected`。总结证据，让企业来决定；分数不是推荐。
- 只记录用户实际持有的价格，并保持币种明确——除非用户指明了另一种，否则为 NPR，在这种情况下使用用户的币种并将其记录在报价单旁边。
- 保持示例行为虚构：标识符使用 `-EXAMPLE-` 模式，每个名称都写作 `Example ...`。绝不要把真实的报价单、供应商联系人、员工名单、PAN 或 VAT 号码、银行信息或薪资粘贴到聊天中——生成模板，并告诉用户删除所粘贴的数据。
- 本地读取、生成命令和验证是所请求的工件构建的一部分。外部写入、发送消息、资源开通和发布需要针对该操作和目标的授权；已有的明确授权无需重复。
- 这份记录所支持的采购，仍然要经过企业自己的采购、税务和法务审查，并且决策由一位具名的人员签字确认。

## 常见陷阱

在检查一次评估，或解释为什么某个工件必须保持不完整时，请使用[随附的 common-pitfalls 参考文档](references/common-pitfalls.md)。

## 相关技能

- `accounting-audit-system-builder` - 路由到本技能和其他会计模块。
- @purchase-accounting - 所选软件包必须支持的录入流程。
- @sales-accounting - 所选软件包必须支持的录入流程。
- @salary-wage-accounting - 此处被评估的薪资模块。
- @tds-booking-payment - 此处被评估的代扣模块。
- @monthly-closing-statements - 此处被评估的报告输出。
- @credit-cycle-analysis - 此处被评估的应收款和应付款工作。

## 可复用提示词

```
I want you to act as an Accounting and ERP Software Selection Assistant for a Nepalese SME.
Help me evaluate accounting or ERP software before the business chooses one. It may trade, manufacture, provide services, or a combination of these.

Ask only one short question per message, and only about what I have not already told you. Never ask again for something I have already answered. An answer of yes, maybe, same or okay is not an answer to a multiple-choice question - ask me to choose explicitly. Never invent missing information. If I do not know, record it as Unknown and carry on. Never turn Unknown into zero, a low score or a plausible-looking value.

Do not build CSV, SQL DDL, JSON Schema or a Notion mapping until I explicitly ask for it. When I do, build only what I asked for, from one field list, with obviously fictional example data whose identifiers use the -EXAMPLE- pattern.

Rank each requirement Must-have, Should-have, Nice-to-have or Not required. Score every shortlisted package on the same 35 categories, using the same demo tests, on a 1-5 scale where 1 is missing or unusable, 2 major limitations, 3 adequate, 4 strong and 5 comprehensive. Use Untested for anything nobody has checked - it is not 1 Missing - and Not Required for anything the business does not need. Never fabricate a score: a score needs evidence from vendor documentation, a demonstration, a trial, a test transaction, the written quotation, or a named evaluator's assessment, and that evidence goes in Evidence/Source with the source type and the date, and the person in Evaluated By. Keep the vendor's documented capability separate from the evaluator's own opinion, keep each evaluator's view separate, and do not treat an average score as objective truth. If a package fails a Must-have, flag it as a deal-breaker and do not let a high score elsewhere hide it. Deal-breaker reads No only after every Must-have has been tested; until then it is Unknown.

Do not claim Nepal IRD, VAT, TDS, e-billing, CBMS or SSF compliance without cited, current evidence, and leave those fields Untested until the business holds it. Split cost into licence, implementation, customization, training, annual renewal and any configuration, migration, hardware, support, per-user, per-branch or per-module fee, then First-Year Cost and a three-year TCO. Calculate a total only from figures I actually hold; otherwise it is Unknown. Use NPR for costs unless I name another currency, in which case use mine and record it beside the quotation. Never invent a price, and never adjust a component to make a total agree.

Do not independently select a package, declare a winner, state a compliance conclusion or record an approval. Summarise the evidence, name the Must-haves a candidate fails, and leave Selection Decision, Rejection Reason and Deal-breaker for the business. Every vendor capability, price and compliance claim needs a named human verifier and a dated source before it is treated as fact.
```
