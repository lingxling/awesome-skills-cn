---
name: ginkgo-cloud-lab
description: 在Ginkgo Bioworks Cloud Lab（cloud.ginkgo.bio）上提交和管理协议，这是一个用于在可重构自动化车（RACs）上执行自主实验室的基于Web的界面。用于用户想要运行无细胞蛋白表达（验证或优化）、生成荧光像素艺术或与Ginkgo Cloud Lab服务交互时。涵盖协议选择、输入准备、定价和订购工作流。
---

# Ginkgo Cloud Lab

## 概述

Ginkgo Cloud Lab（https://cloud.ginkgo.bio）提供对Ginkgo Bioworks自主实验室基础设施的远程访问。协议在可重构自动化车（RACs）上执行——具有机械臂、磁悬浮样品运输和工业级软件的模块化单元，跨越70多种仪器。

该平台还包括**EstiMate**，这是一个接受人类语言协议描述并返回自定义工作流的可行性评估和定价的AI代理。

## 可用协议

### 1. 无细胞蛋白表达验证

使用重组大肠杆菌CFPS进行快速通过/不通过表达筛选。提交FASTA序列（最多1800 bp），接收表达确认、基线滴度（mg/L）和初始纯度以及虚拟凝胶图像。

- **价格**：$39/样本 | **周转时间**：5-10天 | **状态**：已认证
- **详情**：参见 [references/cell-free-protein-expression-validation.md](references/cell-free-protein-expression-validation.md)

### 2. 无细胞蛋白表达优化

使用DoE方法在多达24种条件/蛋白质（裂解物、温度、分子伴侣、二硫键增强剂、辅因子）中进行优化。设计用于难表达蛋白质和膜蛋白。

- **价格**：$199/样本 | **周转时间**：6-11天 | **状态**：已认证
- **详情**：参见 [references/cell-free-protein-expression-optimization.md](references/cell-free-protein-expression-optimization.md)

### 3. 荧光像素艺术生成

通过声学分配将像素艺术图像（48x48到96x96像素，PNG/SVG）转换为使用多达11种大肠杆菌菌株的荧光细菌艺术品。以高分辨率UV照片形式交付。

- **价格**：$25/平板 | **周转时间**：5-7天 | **状态**：测试版
- **详情**：参见 [references/fluorescent-pixel-art-generation.md](references/fluorescent-pixel-art-generation.md)

## 通用订购工作流

1. 在 https://cloud.ginkgo.bio/protocols 选择协议
2. 配置参数（样本/蛋白质数量、重复、平板）
3. 上传输入文件（蛋白质协议的FASTA，像素艺术的PNG/SVG）
4. 在附加详情字段中添加任何特殊要求
5. 提交并接收可行性报告和价格报价

对于上述未列出的协议，使用**EstiMate**聊天以自然语言描述自定义协议并接收兼容性评估和定价。

## 身份验证

在 https://cloud.ginkgo.bio 访问Ginkgo Cloud Lab。可能需要创建账户或机构访问。如有访问问题，请联系Ginkgo：cloud@ginkgo.bio。

## 关键基础设施

- **RACs（可重构自动化车）**：具有高精度机械臂和磁悬浮运输的模块化机器人单元
- **Catalyst软件**：协议编排、调度、参数化和实时监控
- **70多种集成仪器**：样品制备、液体处理、分析读出、存储、培养
- **Nebula**：Ginkgo在马萨诸塞州波士顿的自主实验室设施
