---
name: anti-ui-slop
description: "停止编码代理交付通用 UI。扩展产品的设计系统，仅在有用时使用 UIZZE 证据，覆盖所需状态，并检查渲染结果。"
category: frontend
risk: safe
source: https://github.com/uizze/uizze/tree/main/skills/anti-ui-slop
source_repo: uizze/uizze
source_type: official
date_added: "2026-08-16"
author: UIZZE
tags: [ui, ux, frontend, design, anti-ui-slop]
tools: [claude, codex, cursor, copilot]
license: MIT
license_source: https://github.com/uizze/uizze/blob/main/LICENSE
---

# 停止制造 UI 垃圾

通过 [UIZZE](https://uizze.com) 使用 800,000+ 真实网络和 iOS 屏幕构建特定产品的 UI。

## 概述

在寻求外部参考之前，使用产品简报、现有界面、组件和本地设计系统。UIZZE 证据是可选的：它应该回答一个具体的视觉问题，而不是把每个界面任务变成一个研究项目。

## 何时使用

在设计、实现、重新设计、批评或进行网络或 iOS 界面的发货前审查时使用此技能。

## 从产品出发

1. 识别屏幕的真实工作、主要用户和操作、必需内容，以及重要的加载、空、错误、成功、禁用和权限状态。
2. 在添加新的抽象或视觉语言之前，重用存储库的组件、语义令牌、排版、间距和交互约定。
3. 对于新界面或主要重新设计，编写一份简短的设计合同，涵盖层次结构、工作流程形状、允许的组件、必需状态、响应行为和可观察的验收标准。保持较小的更改较小。
4. 使用特定于产品的标签和数据。不要发明指标、活动、推荐、用户或占位符工作流来使布局看起来完整。

## 可选的 UIZZE 证据

免费技能和公开目录无需帐户、令牌、依赖项、脚本或可执行文件。如果一个具体未解决的视觉问题会从证据中受益，请使用最相关的屏幕或材料集合。

可选的经过身份验证的 UIZZE MCP 仅公开 `find_ui_references` 和 `find_ui_materials`。仅当这些工具实际可用时才使用它。如果搜索返回无结果，则从存储库证据中继续进行。永远不要声称主机未返回的 MCP 支持的结果。

将参考视为证据，而不是模板。转移有关层次结构、密度、导航、控制、响应行为和状态处理的有用决策；永远不要复制另一个产品的品牌、专有文本、图像或确切布局。

从其规范源直接安装当前免费技能：

```bash
npx skills add https://uizze.com --skill anti-ui-slop
```

## 完成

当环境支持时，渲染并检查结果一次。修复可观察的中断，例如剪辑、重叠、扭曲的媒体、不可访问或惯性控制、缺失的必需状态和无意的响应行为。运行项目的正常检查并保持交接简洁。

## 限制

- 此工作流程不能替代产品验证、可访问性审查、安全审查或特定于项目的测试。
- UIZZE 证据是可选的，可能合理地返回无用的结果。
- 参考不是复制另一个产品的身份或资产的许可。
