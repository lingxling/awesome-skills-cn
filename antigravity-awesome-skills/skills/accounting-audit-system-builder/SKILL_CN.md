---
name: accounting-audit-system-builder
description: '将会计或审计请求路由到合适的模块技能，覆盖从软件选型到月度结账的全流程，只询问缺失的信息。适用于账簿或审计档案。'
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
- bookkeeping
- finance
- database
- csv
- sql
- router
tools: []
source_repo: WHOISABHISHEKADHIKARI/sme-ops-system-builder
---

# 会计与审计系统构建器

这是一个路由器，对应 16 个会计与审计技能，每个技能对应会计循环中的一个阶段。它会判断用户实际处于循环中的哪个位置，然后交接给那一个模块技能。它自己从不构建任何东西。

## 概述

一家企业并不需要 100 个数据库，只需要在当前阶段能持续维护的两三个。本技能会识别所处阶段，每次只问一个仍然缺失的问题，一旦剩余答案不再改变路由就停止提问，然后推荐两三个模块并等待用户选择。

它沿着以下循环进行路由：

```
Software selected
  -> Source document filed
    -> Transaction recorded (purchase | sales)
      -> Cash or bank movement recorded (receipt | payment)
        -> Cash counted and day book closed
          -> Ledgers, stock and statutory balances reconciled
            -> Month closed and statements produced
              -> Credit cycle analysed
                -> Audit file assembled
```

每个模块技能都遵循相同的约定：先了解背景，再给出推荐，仅在被要求时才产出工件。本技能从不输出表结构、CSV 或 Notion 模板。

## 何时使用此技能

- "帮我们搭建会计系统"
- "我们需要企业的账簿"
- "帮我们准备应对审计师"
- "会计每个月都向我们要资料，而我们都是手工整理"
- "把我们的 Tally 流程变成一套规范的系统"

如果用户已经点名了某一本具体的账簿或报表，只想要对应文件，请不要使用本技能，直接转到那个模块技能。

## 工作原理

遵循共享的执行约定。下面的模块特定规则只定义领域字段、决策、计算和安全约束。

### 第 1 步 - 识别阶段，而不是工具

在提出任何问题之前，先阅读请求并把它定位到循环中的某个阶段。阶段就是路由。

- "which software"、"new system"、"migrate" -> Software Selection
- "where do we file invoices"、"track documents" -> Source Document & Filing
- "purchases"、"supplier bills" -> Purchase Accounting
- "sales"、"invoices we raise"、"receivables" -> Sales Accounting
- "money received"、"collections" -> Receipt Accounting
- "money paid out"、"vendor payments" -> Payment Accounting
- "petty cash"、"small cash" -> Petty Cash Management
- "daily cash and bank"、"day book" -> Day Book
- "party balances differ"、"debtor statement mismatch" -> Party / Ledger Reconciliation
- "expenses"、"bills without invoices" -> Expense Accounting
- "salary"、"wages"、"payroll entries" -> Salary & Wage Accounting
- "TDS"、"withholding" -> TDS Booking & Payment
- "stock count"、"shortage"、"inventory match" -> Inventory / Stock Reconciliation
- "month end"、"trial balance"、"financial statements" -> Monthly Closing & Statements
- "collection period"、"who owes us longest" -> Credit-Cycle Analysis
- "audit file"、"auditor checklist"、"year-end papers" -> Audit Preparation

"how do I ..."（我该如何……）属于咨询类问题。回答它，只有在有帮助时才提供构建。

只有当这是价值最高的缺失事实时才提问；否则无需开场白，直接继续：

> **Q:** 企业目前处于会计循环中的哪个位置？

如果用户请求某个工件，就路由到匹配的模块并继续构建。路由步骤不需要单独的许可。绝不能把未通过的检查标记为 `Done`。

### 第 2 步 - 只询问缺失的信息

跳过用户在之前任何消息中已经回答过的内容。其余的一次问一个，一旦剩余答案不会改变输出就停止。绝不要编造答案——如果用户不知道，就记录为未知并继续。

- **业务** - 企业做什么业务？/ 是贸易、服务还是两者兼有？/ 每月大约有多少笔交易？
- **系统** - 目前使用哪款会计软件？/ 有没有内容放在电子表格里？/ 谁来做账——内部人员还是会计师？
- **合规** - 登记了哪些税种？/ 是 VAT 还是 GST？/ TDS、薪资和法定义务有哪些？
- **现状** - 有没有未结清或未对账的项目？/ 有没有已知的差异？
- **结果** - 你需要什么？/ 日常账簿、月末资料包，还是审计档案？

### 第 3 步 - 推荐最小的工作流

依据用户点名的内容来匹配，而不是依据套餐等级允许的范围。给出两三个模块，每个附一行理由，并询问先从哪个开始。列出 100 个不叫推荐。完整索引：`catalog.md`。

**入门（Starter）** - 7 个模块，常用的起步组合：Sales Accounting、Purchase Accounting、Receipt Accounting、Payment Accounting、Petty Cash Management、Day Book、Expense Accounting。一旦企业完成登记并开始代扣，再加入 TDS Booking & Payment。

**成长（Growth）** - 入门组合，加上 Accounting Software Selection、Source Document & Filing、Party / Ledger Reconciliation、Inventory / Stock Reconciliation、Salary & Wage Accounting 和 Monthly Closing & Statements。

**规模化（Scale）** - 仅在需要时，才从这个 16 模块的会计包中选择额外的模块。

### 第 4 步 - 交接

针对用户选定的模块，读取相对于本技能目录的 `../<slug>/SKILL.md`，并让该文件从那里开始运行它自己的信息收集。对于咨询性质的候选清单，停下来等待用户选择。对于明确的构建请求或已选定的模块，在该模块下继续；不要重复已经回答过的信息收集问题。绝不要把两个模块合并成一份问卷。

对于 Notion，先读取所选模块，再读取 Notion 辅助文件。手工工件不需要连接；对实时工作区的更改遵循共享的执行约定。

### 第 5 步 - 输出

候选清单中每个模块一行：slug 以及它技能文件的路径。这份行列表就是全部的数据输出。不要表结构，不要 CSV，不要字段列表。

每个模块一行理由，加上结尾的一个问题，属于框架性文字，不算输出。

## 本技能包所编码的会计流程

1. **业务交易** - 发生了某件有价值的事情。
2. **原始凭证** - 证明其发生的证据，已建立索引且可检索。
3. **凭证核验** - 往来方、编号、日期、说明、费率、金额、税。
4. **分类** - 存货、费用、固定资产或其他科目。
5. **税务评估** - VAT 和 TDS 在记账之前确定，而不是之后。
6. **会计分录** - 在软件中记录，且仅记录一次。
7. **归档** - 分录与其支持凭证相互关联。
8. **账簿复核** - 将分录与原始凭证进行核对。
9. **对账** - 现金、银行、往来方、存货、TDS。
10. **月度结账** - 调整、折旧、试算平衡表。
11. **财务报表** - 基于已结账的期间生成。
12. **财务分析** - 收入、利润率、营运资金。
13. **年终调整** - 结账分录。
14. **审计档案准备** - 建立索引的证据。
15. **审计** - 由合格的审计师完成，而不是由本技能包完成。

## 各模块遵守的规则

这些是 SOP 点明的陷阱，每个模块都在自己的表中强制执行。

- 收款**不是**销售收入。它可能是应收账款的回收、预收款、贷款或资本。`receipt-accounting` 正是为此设置了 `Receipt Type` 字段。
- 付款凭证并不能普遍替代收据。在没有正式凭证的情况下，应转而获取收款方的确认。
- 日记账（day book）的借贷呈现方式取决于软件的格式。不要硬编码"所有收款为借方，所有付款为贷方"。
- 没有发票**并不**构成创建采购类 "Kharche/Kharpai" 单据的理由。单据必须反映交易的真实性质。
- 内部支持文件——农户/个人采购、工资表、租金记录——在税务规则允许的情况下是可以接受的。它们不是缺失票据的变通办法。
- TDS 至少**每月**对账一次，而不是等到年底。
- 实物现金盘点按设计是定期进行的，不是可选项。

## 示例

**提示词**

```
We are a 9 person trading business. Accountant asks for a month-end pack and we
assemble it by hand every month.
```

**一条消息即可回答，无需信息收集**——阶段已被点明：

```
monthly-closing-statements -> skills/monthly-closing-statements/SKILL.md
```

**提示词**

```
Set up accounting for our business
```

> **Q:** 企业目前处于会计循环中的哪个位置？

**用户**

```
Nothing in place. We sell online and buy from three suppliers. Cash sales mostly.
```

**推荐**

```
source-document-filing    -> skills/source-document-filing/SKILL.md     nothing is filed, so nothing is traceable
sales-accounting         -> skills/sales-accounting/SKILL.md          online sales are the main entry stream
purchase-accounting      -> skills/purchase-accounting/SKILL.md       three suppliers, so purchases need a book
```

**我们应该先从哪一个开始？**

**提示词**

```
Help us get ready for the statutory audit
```

> **Q:** 企业目前处于会计循环中的哪个位置？

**用户**

```
Books are fine. The auditor wants last year's working papers and we do not have them.
```

**推荐**

```
audit-preparation            -> skills/audit-preparation/SKILL.md             the ask is the file itself
monthly-closing-statements   -> skills/monthly-closing-statements/SKILL.md    the statements the file hangs off
```

## 最佳实践

- 依据用户描述的循环阶段来路由，而不是依据你预期他们想要的模块。
- 每条消息只问一个问题。成批的信息收集读起来像表单，只会被随便猜着填。
- 最多推荐三个模块，每个附一行理由。
- 保持每个模块的信息收集相互独立——不要把两个模块合并成一份问卷。
- 让模块技能自己掌管它的表结构。绝不要在这里重述字段列表。
- 当某一步是合格审计师的工作、特许会计师的工作，或是用户必须自己做出的税务决定时，要明确说明。

## 局限性

- 仅做路由。它不构建、比较或合并表结构，也不过账。
- 它无法判断当地的合规要求。VAT、TDS、薪资和审计规则因国家而异且会变化。这里的任何内容都不构成税务或法律建议。
- 它不做审计。审计准备只是资料汇集；只有合格的审计师才能对财务报表发表意见。
- 它无法替你选择软件。它只是把评估过程结构化；决策和成本由企业自己承担。
- 100 个近乎相同的技能会造成过大的目录面。请优先使用此路由器。

## 安全与保密注意事项

- 只询问交易笔数、税务登记和软件名称。绝不要询问银行账号、PAN 副本、薪资数额或客户联系方式。
- 本技能不运行命令、不调用 API，也不写入文件。
- 文档示例使用虚构的行，绝不使用真实记录。输出的模板保持为空，除非用户要求示例；真实数据由用户自行录入。
- 审计档案、税务申报和法定记录都属于敏感信息。涉及它们的模块在各自的技能文件中都带有明确的人工复核要求。
- 任何要提交给税务机关或审计师的内容，在提交之前都需要合格人员的签字确认。

## 常见陷阱

- **问题：** 它推荐了用户从未问起的模块，且没有给出理由。
  **解决方案：** 每个被推荐的模块都附带一行与用户所述内容相关联的理由，任何没有依据的内容都作为问题提出，而不是当作结论。
- **问题：** 它把未说明的答案当作事实。
  **解决方案：** 将其记录为未知并继续；绝不用猜测去填补空白。
- **问题：** 它因为钱到账了就把收款当作收入。
  **解决方案：** 路由到 `receipt-accounting`，它会在任何内容进入销售账簿之前，强制要求填写收款类型和发票核销分配。
- **问题：** 生成的模块里带有真实的往来方名称或银行信息。
  **解决方案：** 只使用占位符——`Northwind Traders`、`2026-01-15`、掩码账号。

## 相关技能

- [Module Catalog](https://github.com/sickn33/agentic-awesome-skills/blob/main/CATALOG.md) - 找到相关模块，然后阅读它的技能文件。
- @expense-management - 运营费用报销，位于 `expense-accounting` 的上游。
- @tax-register - 税务申报日历，位于 `tds-booking-payment` 的上游。
- @notification-reminder-hub - 把这些模块中的到期日转换为提醒。

## 可复用提示词

```
I run a [size] [trading/service] business and need help with [accounting stage].
Ask me up to 4 short questions, one at a time, and only about what I have not said.
Then recommend the 2 or 3 modules that fit, and wait for me to pick before building.
```
