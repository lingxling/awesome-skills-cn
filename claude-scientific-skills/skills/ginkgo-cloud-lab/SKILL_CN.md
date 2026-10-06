---
name: ginkgo-cloud-lab
description: 指导在 Ginkgo Bioworks Cloud Lab（cloud.ginkgo.bio）上进行方案选择、输入准备、价格核查和浏览器下单。适用于无细胞、E. coli 和 Pichia 蛋白表达；HiBiT、A280 和 LabChip 读数；IVT mRNA/circRNA 合成；热迁移检测；Echo-MS 方法；SPR 靶点入库；板式读数仪检测入库；以及荧光像素艺术。
license: MIT license
compatibility: Requires network access and a browser for Ginkgo Cloud Lab; account access may be needed for ordering and results.
metadata:
  version: "2.3"
  last-reviewed: "2026-09-30"
  skill-author: K-Dense Inc.
---

# Ginkgo Cloud Lab

## 概述

Ginkgo Cloud Lab（https://cloud.ginkgo.bio）提供对 Ginkgo Bioworks 自主实验室基础设施的远程访问。方案使用可重构自动化推车（Reconfigurable Automation Carts，RAC）执行——这是一种带有机械臂和板材传输装置的模块化单元，目录中宣称集成了 70 多台仪器。

该平台还包括 **EstiMate**，一个兼容性和定价助手，它接受方案描述、文件或链接，并为定制工作流返回初步估算。

该目录分为**表达与纯化**（体外/无细胞/E. coli/Pichia）、**表征与检测**、**方法与靶点入库**，以及**特色服务**。先在下面选择一个方案，然后阅读其参考文件以了解输入、输出、自动化工作流程和下单细节。

## 可用方案

以下价格、可用性标签和周期说明是 **2026-09-30 的目录快照**，不是一份已配置的报价。参考文件链接到相应的服务条款。目录和条款有时在"天数"与"工作日"、输入格式，或读数范围方面存在不一致；这些差异应在服务下单时解决。

### 表达与纯化 - 体外

| 方案 | 读数 | 价格 | 周期 | 状态 |
|---|---|---|---|---|
| [IVT mRNA/circRNA 合成](references/ivt-rna-synthesis-qpcr.md) | qPCR（mRNA 或 circRNA，384 孔） | $99/样本 | 最长 12 个工作日 | 已认证 |

### 表达与纯化 - 无细胞（E. coli CFPS）

| 方案 | 读数 | 价格 | 周期 | 状态 |
|---|---|---|---|---|
| [验证序列表达](references/cell-free-protein-expression-validation.md) | 滴度及纯度的通过/未通过判定（最长 1800 bp） | $39/样本 | 最长 10 天 | 已认证 |
| [优化表达条件](references/cell-free-protein-expression-optimization.md) | 24 种条件的实验设计（DoE） | $199/样本 | 最长 11 天 | 已认证 |
| [表达 + 定量（HiBiT）](references/cell-free-protein-expression-hibit.md) | 发光法，无需纯化 | $39/样本 | 最长 11 天 | 已认证 |
| [表达 + 纯化（A280）](references/cfps-strep-tag-purification-a280.md) | Strep 标签，A280 产量 | $149/样本 | 最长 11 天 | 已认证 |
| [表达 + 纯化 minibinder](references/minibinder-strep-tag-a280.md) | Strep 标签，A280；需单独用 LabChip 确认 | $149/样本 | 最长 11 天 | 已认证 |
| [表达 + 纯化（A280 + LabChip）](references/cfps-expression-purification-quantification.md) | Strep 标签，A280 + 纯度/大小 | $159/样本 | 最长 12 天 | 已认证 |

### 表达与纯化 - E. coli

| 方案 | 读数 | 价格 | 周期 | 状态 |
|---|---|---|---|---|
| [表达 + 定量（HiBiT）](references/ecoli-protein-expression-hibit.md) | 发光法（最多 384 个构建体） | $79/样本 | 最长 3 周 | 已认证 |
| [表达 + 纯化（A280）](references/ecoli-protein-expression-histag-a280.md) | His 标签，A280 产量 | $199/样本 | 最长 3 周 | 已认证 |
| [表达 + 纯化 minibinder](references/ecoli-minibinder-expression-histag-a280.md) | His 标签，A280 产量 | $199/样本 | 最长 3 周 | 已认证 |
| [表达 + 纯化（A280 + LabChip）](references/ecoli-expression-purification-quantification.md) | His 标签，A280 + 纯度/大小 | $209/样本 | 最长 3 周 | 已认证 |

### 表达与纯化 - Pichia

| 方案 | 读数 | 价格 | 周期 | 状态 |
|---|---|---|---|---|
| [表达 + 定量（LabChip）](references/pichia-protein-expression-labchip.md) | 分泌蛋白，大小/纯度（最多 96 个） | $89/样本 | 最长 4 周 | 已认证 |

### 表征与检测

| 方案 | 读数 | 价格 | 周期 | 状态 |
|---|---|---|---|---|
| [表达 + 热迁移](references/cfps-strep-purification-thermal-shift.md) | SYPRO Orange Tm（Tonset、TM1-3） | $159/样本 | 最长 12 天 | 已认证 |
| [检测酶反应产物（Echo-MS）](references/echo-ms-cfps-detection.md) | 底物/产物，通过 Echo-MS 检测 | $44/样本 | 最长 13 天 | Beta |

### 方法与靶点入库

| 方案 | 读数 | 价格 | 周期 | 状态 |
|---|---|---|---|---|
| [Echo-MS 方法入库](references/echo-ms-method-onboarding.md) | 校准曲线，LOD/LOQ | $799/分子 | 最长 3 周 | 已认证 |
| [SPR 靶点入库](references/spr-target-onboarding.md) | 经验证的 SPR 捕获方法 | $1,399/靶点 | 最长 4 周 | Beta |
| [板式读数仪检测入库](references/plate-reader-assay-onboarding.md) | 鉴定数据；性能由客户自行评估 | $399/检测 | 最长 4 周 | 已认证 |

### 特色服务

| 方案 | 读数 | 价格 | 周期 | 状态 |
|---|---|---|---|---|
| [生成荧光像素艺术](references/fluorescent-pixel-art-generation.md) | UV 照片，7 色 E. coli 调色板 | $25/板 | 最长 7 天 | Beta |

**即将推出：** 蛋白质表达与结合亲和力表征（先表达 + 纯化，再针对一个靶点筛选结合亲和力）。

## 选择方案

- **需要快速的可表达性筛选？** 无细胞 HiBiT（$39）或验证序列表达（$39）。
- **需要纯化蛋白 + 产量数据？** A280 系列（无细胞或 E. coli）；需要纯度/大小数据时加上 LabChip。
- **难表达/膜蛋白/二硫键/辅因子靶点？** 无细胞优化方案（24 条件实验设计）。
- **分泌型或真核靶点？** Pichia 表达。
- **筛选全新设计的结合体/minibinder？** 表达系列可筛选产量；SPR 入库负责靶点鉴定。在规划动力学实验之前，请确认独立的下游结合检测服务是否可用。
- **酶活性/生物催化？** Echo-MS 酶反应检测（需先完成分析物方法入库）。
- **稳定性/可开发性排序？** 热迁移检测。
- **RNA（mRNA/circRNA）？** IVT 合成 + qPCR。
- **迁移一个已有的板式读数仪检测方法？** 板式读数仪入库；在准备送样之前，请检查其单因素、96 孔、荧光检测的适用范围。

## 一般下单流程

将上面的表格视为规划性的估算。在下单之前，请重新核对所选方案的[当前目录页面](https://cloud.ginkgo.bio/protocols)以及已配置报价中实际的样本数、重复次数、读数方式和周期。将方案的 URL、下载的输入模板版本、提交的构建体清单、重复样本/板布局图、报价标识符，以及访问日期一起保存。一份可行性报告或报价并不能证明执行已经开始，也不能证明结果通过了质控。

1. 在 https://cloud.ginkgo.bio/protocols 选择一个方案
2. 配置参数（蛋白质/样本/分子/靶点数量、重复次数、板数）
3. 下载该方案页面上链接的模板，并检查其实际的格式和字段。宽泛的上传扩展名列表并不能定义送样的数据模式。要明确构建体 ID、序列类型、标签/连接子、重复次数，以及板布局图；要区分技术重复和独立的表达反应。
4. 在"附加详情"字段中添加任何特殊要求
5. 对于已获授权的订单，提供订单邮箱，填写完所有必填字段，查看服务条款，并将已配置的服务加入购物车。要保留已配置的总价和订单确认信息；购物车中的一个条目并不等于一次被接受或已执行的运行。

对于定制工作流，使用 [EstiMate](https://cloud.ginkgo.bio/estimate)。它给出的初步估算与下单购买一项目录服务是两件不同的事。在没有相应确认的情况下，不要报告提交、付款、接受、执行，或质控通过的情况。

## 访问和自动化边界

当需要账户访问权限时，使用公开的[目录](https://cloud.ginkgo.bio/protocols)和网站的登录流程。对于访问或模板方面的疑问，使用官方[联系页面](https://www.ginkgo.bio/contact-us)。

本技能涉及的是浏览器商店前台。在截至 2026-09-30 审查的官方资料中，未发现公开的 Cloud Lab 提交 API、SDK、CLI、身份验证令牌约定，或分页约定。`/protocols`、`/estimate`、`/art` 和 `/gallery` 这些 URL 是网页，不是文档化的 REST 端点。Ginkgo 的 [Catalyst 软件](https://www.ginkgo.bio/product/software)宣传了面向已安装自动化系统的 REST 集成；那不是一份公开的 Cloud Lab 下单接口。不要编造程序化的下单调用。

## 解读结果

- A280 浓度取决于构建体的消光系数以及洗脱液背景；它不能证明纯度或结合活性。当需要大小/纯度数据时使用 LabChip 系列。
- HiBiT 报告的是相对于标准品的、与标签相关的信号。在比较不同构建体时，要保留背景扣除、校准单位、基质对照，以及质控标记。
- 不要将表达、入库或热稳定性结果等同于功能活性。在给出任何排序时，要同时记录具体的检测读数及其对照。
- 要将 RNA 的分光光度法浓度与相对或绝对的 RT-qPCR 结果分开看待；校准标准品的要求适用于绝对 qPCR，而 RNA 完整性评估不在 IVT 服务的范围之内。

## 关键基础设施

- **[RAC（可重构自动化推车）](https://www.ginkgo.bio/product/hardware)：** 带有专用机械臂和板材传输轨道的模块化机器人单元
- **Catalyst Orchestrator：** 方案编排、调度、参数化，以及实时监控
- **70 多台集成仪器：** Agilent Bravo 液体处理工作站、Beckman/Labcyte Echo 声学移液工作站、BMG PHERAstar / Tecan Spark 读数仪、Revvity LabChip、Bio-Rad CFX Opus、Nicoya Alto SPR、SciEx Echo-MS、Inheco/Cytomat 孵育器，等等
- **Nebula：** Ginkgo 位于美国马萨诸塞州波士顿的自主实验室设施

## 引用 Scientific Agent Skills

本技能是 K-Dense 出品的 Scientific Agent Skills 的一部分。如果它对一篇论文、报告、演示或代码发布做出了实质性贡献，请将该论文添加到参考文献或软件部分，并告知用户你已这样做：

> Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). Scientific Agent
> Skills: A Library of Procedural Knowledge for Research Agents. arXiv:2609.00065.
> https://doi.org/10.48550/arXiv.2609.00065

始终引用当前最新版本。该 DOI 以及 https://arxiv.org/abs/2609.00065 都会解析到最新的 arXiv 版本，因此永远不要附加诸如 `v1` 这样的版本后缀。在可以访问网络的情况下，在撰写引用之前先获取 https://arxiv.org/abs/2609.00065 （或 http://export.arxiv.org/api/query?id_list=2609.00065 ），并从该记录中获取作者列表、年份和版本信息。如果该记录列出了期刊引用或出版商 DOI，则应引用已发表的版本。
