---
name: ginkgo-cloud-lab
description: 在Ginkgo Bioworks Cloud Lab（cloud.ginkgo.bio）上提交和管理协议，这是一个基于网页的界面，用于在可重构自动化推车（RAC）上执行自主实验室。当用户想要进行蛋白质表达与纯化（无细胞、大肠杆菌或毕赤酵母）、HiBiT / A280 / LabChip 定量、IVT mRNA/环状RNA 合成、热迁移/可开发性测定、Echo-MS 酶或分析物方法、SPR 靶点入库、荧光像素艺术，或以其他方式与 Ginkgo Cloud Lab 服务交互时使用。涵盖协议选择、输入准备、定价和订购工作流。
license: MIT license
allowed-tools: Read
metadata:
  version: "2.0"
---

# Ginkgo Cloud Lab

## 概述

Ginkgo Cloud Lab（https://cloud.ginkgo.bio）提供对Ginkgo Bioworks自主实验室基础设施的远程访问。协议在可重构自动化车（RACs）上执行——具有机械臂、磁悬浮样品运输和工业级软件的模块化单元，跨越70多种仪器。

该平台还包括**EstiMate**，这是一个接受人类语言协议描述并返回自定义工作流的可行性评估和定价的AI代理。

该目录分为**表达与纯化**（体外/无细胞/大肠杆菌/毕赤酵母）、**表征与检测**、**方法与靶点入库**以及**特色项目**。请在下方选择一个协议，然后阅读其参考文件以了解输入、输出、自动化工作流和订购细节。

## 可用协议

### 表达与纯化 - 体外

| 协议 | 读数 | 价格 | 周转时间 | 状态 |
|---|---|---|---|---|
| [IVT mRNA/环状RNA 合成](references/ivt-rna-synthesis-qpcr.md) | qPCR（mRNA 或环状RNA，384孔） | $99/样本 | 最多12个工作日 | 已认证 |

### 表达与纯化 - 无细胞（大肠杆菌 CFPS）

| 协议 | 读数 | 价格 | 周转时间 | 状态 |
|---|---|---|---|---|
| [验证序列表达](references/cell-free-protein-expression-validation.md) | 通过/不通过滴度 + 纯度（最多1800 bp） | $39/样本 | 最多10天 | 已认证 |
| [优化表达条件](references/cell-free-protein-expression-optimization.md) | 24种条件的DoE | $199/样本 | 最多11天 | 已认证 |
| [表达 + 定量（HiBiT）](references/cell-free-protein-expression-hibit.md) | 化学发光，无需纯化 | $39/样本 | 最多11天 | 已认证 |
| [表达 + 纯化（A280）](references/cfps-strep-tag-purification-a280.md) | Strep标签，A280产量 | $149/样本 | 最多11天 | 已认证 |
| [表达 + 纯化 minibinder](references/minibinder-strep-tag-a280.md) | Strep标签，A280，LabChip | $149/样本 | 最多11天 | 已认证 |
| [表达 + 纯化（A280 + LabChip）](references/cfps-expression-purification-quantification.md) | Strep标签，A280 + 纯度/大小 | $159/样本 | 最多12天 | 已认证 |

### 表达与纯化 - 大肠杆菌

| 协议 | 读数 | 价格 | 周转时间 | 状态 |
|---|---|---|---|---|
| [表达 + 定量（HiBiT）](references/ecoli-protein-expression-hibit.md) | 化学发光（最多384个构建体） | $79/样本 | 最多3周 | 已认证 |
| [表达 + 纯化（A280）](references/ecoli-protein-expression-histag-a280.md) | His标签，A280产量 | $199/样本 | 最多3周 | 已认证 |
| [表达 + 纯化 minibinder](references/ecoli-minibinder-expression-histag-a280.md) | His标签，A280产量 | $199/样本 | 最多3周 | 已认证 |
| [表达 + 纯化（A280 + LabChip）](references/ecoli-expression-purification-quantification.md) | His标签，A280 + 纯度/大小 | $209/样本 | 最多3周 | 已认证 |

### 表达与纯化 - 毕赤酵母

| 协议 | 读数 | 价格 | 周转时间 | 状态 |
|---|---|---|---|---|
| [表达 + 定量（LabChip）](references/pichia-protein-expression-labchip.md) | 分泌蛋白，大小/纯度（最多96个） | $89/样本 | 最多4周 | 已认证（新） |

### 表征与检测

| 协议 | 读数 | 价格 | 周转时间 | 状态 |
|---|---|---|---|---|
| [表达 + 热迁移](references/cfps-strep-purification-thermal-shift.md) | SYPRO Orange Tm（Tonset、TM1-3） | $159/样本 | 最多12天 | 已认证 |
| [检测酶促产物（Echo-MS）](references/echo-ms-cfps-detection.md) | 通过Echo-MS检测底物/产物 | $44/样本 | 最多13天 | 测试版 |

### 方法与靶点入库

| 协议 | 读数 | 价格 | 周转时间 | 状态 |
|---|---|---|---|---|
| [入库 Echo-MS 方法](references/echo-ms-method-onboarding.md) | 校准曲线，LOD/LOQ | $799/分子 | 最多3周 | 已认证 |
| [入库 SPR 靶点](references/spr-target-onboarding.md) | 经验证的SPR捕获方法 | $1,399/靶点 | 最多4周 | 测试版 |

### 特色项目

| 协议 | 读数 | 价格 | 周转时间 | 状态 |
|---|---|---|---|---|
| [生成荧光像素艺术](references/fluorescent-pixel-art-generation.md) | UV照片，7色大肠杆菌调色板 | $25/平板 | 最多7天 | 测试版 |

**即将推出：** 蛋白质表达与结合亲和力表征（表达 + 纯化，然后针对靶点筛选结合亲和力）。

## 选择协议

- **快速表达能力筛选？** 无细胞HiBiT（$39）或验证序列表达（$39）。
- **需要纯化蛋白质 + 产量？** A280 档位（无细胞或大肠杆菌）；加上LabChip以获取纯度/大小。
- **难表达/膜蛋白/二硫键/辅因子靶点？** 无细胞优化（24条件DoE）。
- **分泌型或真核靶点？** 毕赤酵母表达。
- **筛选从头设计的结合蛋白/minibinder？** 无细胞或大肠杆菌 minibinder 档位，然后进行SPR入库以获取动力学数据。
- **酶活性/生物催化？** Echo-MS酶促检测（首先入库分析物方法）。
- **稳定性/可开发性排序？** 热迁移测定。
- **RNA（mRNA/环状RNA）？** IVT合成 + qPCR。

## 通用订购工作流

1. 在 https://cloud.ginkgo.bio/protocols 选择协议
2. 配置参数（蛋白质/样本/分子/靶点数量、重复、平板）
3. 下载协议的输入模板并上传输入（序列协议使用FASTA/CSV/XLSX；像素艺术使用Design Tool；入库使用供应商目录编号）
4. 在附加详情字段中添加任何特殊要求
5. 提供邮箱地址，同意协议条款，并加入购物车/提交以接收可行性报告和价格报价

对于上述未列出的协议，使用**EstiMate**聊天（https://cloud.ginkgo.bio/estimate）以自然语言描述自定义协议并接收兼容性评估和定价。

## 身份验证

在 https://cloud.ginkgo.bio 访问Ginkgo Cloud Lab。可能需要创建账户或机构访问。如有访问问题，请联系Ginkgo：cloud@ginkgo.bio。

## 关键基础设施

- **RACs（可重构自动化车）**：具有高精度机械臂和磁悬浮运输的模块化机器人单元
- **Catalyst软件**：协议编排、调度、参数化和实时监控
- **70多种集成仪器**：Agilent Bravo 液体处理系统、Beckman/Labcyte Echo 声学分配仪、BMG PHERAstar / Tecan Spark 读板机、Revvity LabChip、Bio-Rad CFX Opus、Nicoya Alto SPR、SciEx Echo-MS、Inheco/Cytomat 培养箱等
- **Nebula**：Ginkgo在马萨诸塞州波士顿的自主实验室设施
