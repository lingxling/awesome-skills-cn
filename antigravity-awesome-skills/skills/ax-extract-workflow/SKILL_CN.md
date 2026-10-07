---
name: ax-extract-workflow
description: "使用本地 ax 会话/提交/技能/工具跟踪重建过去的编码代理工件背后的工作流。当被问及 X 如何构建时使用。"
category: development
risk: safe
source: community
source_repo: Necmttn/ax
source_type: community
date_added: "2026-06-21"
author: Necmttn
tags: [ai-coding, workflow-reconstruction, session-analysis, observability]
tools: [claude, cursor, gemini, codex-cli]
license: "AGPL-3.0-only"
license_source: "https://github.com/Necmttn/ax/blob/main/LICENSE"
---

# ax 提取工作流

## 概述

使用此技能重建过去的编码代理工件背后的工作流：
一个已发布的功能、PR、演示、重构、报告或其他具体结果。它使用
本地 `ax` 图将提交、会话、轮次、技能和工具跟踪连接
到简短的"这是如何制造的"叙述中。

`ax` 必须已安装、在 `PATH` 上可用，且能够访问其本地数据库。
如果 ax 无法连接到其数据库，报告连接失败并停止，而不是
从内存中猜测。

## 何时使用此技能

- 当用户问"我们是如何构建 X 的？"、"是什么让 X 工作的？"或"提取此工件背后的工作流"时使用。
- 当锚点是提交 SHA、日期、功能名称、PR、会话或仓库本地工件时使用。
- 当用户想要导致结果的代理技能、提示、命令、决定和检查的序列时使用。
- 不要用于通用活动摘要；改用正常的会话列表。

## 工作原理

### 步骤 1：解决锚点

从用户的请求中识别最佳锚点：

- 提交 SHA：直接使用。
- 日期或日期范围：检查日期周围的会话。
- 主题、功能或工件名称：搜索召回相关的轮次、提交和技能。
- "此仓库最近"：列出当前仓库的最近会话。

```bash
ax recall "live ingest dashboard" --sources=turn,commit,skill --scope=here
ax sessions near abc1234 --json
ax sessions around 2026-06-15 --days=3 --json
ax sessions here --days=14
```

这些命令是只读检查命令。

### 步骤 2：挑选相关会话

选择几个最可能解释工件的会话。优先选择
提及工件、涉及相关文件、包括相关提交或具有
匹配工作的技能和工具调用的会话。

如果多个候选人都合理，显示用户候选人并询问哪个
应该检查。

### 步骤 3：检查会话轨迹

打开每个选定的会话并查找：

- 使用的技能及其顺序
- 用户转向点和明确的约束
- 改变工作方向的文件、测试和命令
- 产生关键证据的子代理或工具跟踪
- 在认为结果完成之前的验证步骤

```bash
ax sessions show <session-id> --json
ax sessions show <session-id> --by-role
ax recall "specific keyword from the artifact" --sources=turn,commit --scope=here
```

### 步骤 4：编写重建

内联返回结果，除非用户要求文件。保持简短且
基于证据：

1. 锚点：解决的日期、提交、功能或工件。
2. 有序工作流：4-8 个步骤，显示技能或操作及其产生的内容。
3. 关键决定：改变路径的用户或代理选择。
4. 验证：测试、审查、检查或手动证据。
5. 重现者简介：进行类似工作的紧凑秘诀。

在可用时使用会话 ID、提交 SHA 和文件路径作为引文。

## 示例

### 从提交重建功能

```bash
ax sessions near 8f31c2a --json
ax sessions show <session-id> --by-role
ax sessions show <session-id> --json
```

输出形状：

```text
锚点：8f31c2a，实时摄入仪表板

工作流：
1. 问题框架 -> 将故障缩小到过时的仪表板轮询。
2. 会话召回 -> 找到了早期的摄入流设计和约束。
3. 实施 -> 连接了服务器事件总线和浏览器订阅。
4. 验证 -> 运行了类型检查并在本地刷新了仪表板。

重现者简介：
从失败的工件开始，查找附近的会话，检查按角色分组的
技能，然后总结从框架到验证的最小有序路径。
```

### 围绕日期重建工作

```bash
ax sessions around 2026-06-15 --days=2 --json
ax recall "otel receiver" --sources=turn,commit,skill --scope=here
```

当用户记得工作发生的时间但不记得提交时使用。

## 最佳实践

- 从最具体的可用锚点开始：SHA 优于日期，日期优于模糊主题。
- 将 ax 视为真实来源；不要编造缺失的技能、成本、命令或决定。
- 尽可能少引用，仅当用户决定或命令对重建很重要时。
- 保持私人成绩单细节私密；总结而不是转储日志。
- 分开"发生了什么"和"下次重复什么"。

## 限制

- 需要有效的本地 ax 安装和可达的本地 ax 数据库。
- 仅看到 ax 已摄入的会话、提交、技能和工具跟踪。
- 当代理提供者省略工具输出、成本或推理数据时，会话数据可能不完整。
- 它重建工作流，而不是正确性；在进行工程决定时仍然检查代码并运行项目检查。

## 安全和安全性说明

- 不要上传私人成绩单、会话日志、提示、工具输出或本地数据库导出。
- 从摘要中编辑秘密、令牌、客户数据、文件内容和私人对话文本。
- 使用只读 ax 检查命令，除非用户明确要求单独的维护操作。
- 作为重建的一部分，不要运行改变 `.ax/`、重新生成索引、发布报告或更改仓库的命令。

## 相关技能

- `@agenttrace-session-audit` - 用于本地代理会话健康、成本、延迟和工具故障审计。
- `@domain-modeling` - 当重建揭示应捕获的术语或架构决定时使用。
- `@planning-with-files` - 当用户想要将重建的秘诀转变为带有跟踪笔记的新计划时使用。
