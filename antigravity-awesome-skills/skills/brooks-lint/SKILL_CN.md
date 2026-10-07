---
name: brooks-lint
description: "基于经典软件工程书籍的人工智能代码评审器，用于捕捉设计异味、耦合问题和架构风险。"
category: development
risk: safe
source: community
source_repo: hyhmrright/brooks-lint
source_type: community
license: "MIT"
license_source: "https://github.com/hyhmrright/brooks-lint/blob/main/LICENSE"
date_added: "2026-04-29"
author: hyhmrright
tags: [code-review, architecture, software-design, refactoring, claude-code]
tools: [claude, codex, cursor, gemini]
---

# Brooks Lint

## 概述

Brooks Lint 是一个 Claude Code 技能，通过 12 部经典软件工程书籍的角度查看你的代码。与其检查样式规则，不如问："《程序员修养》、《代码整洁之道》和《设计数据密集型应用》的作者会怎么说这段代码？"

它将里程碑工程书籍中的原则合成为可操作的、结构化的反馈 — 捕捉设计异味、紧耦合、缺失的抽象和架构风险，这些是 linters 和 AI 工具通常会漏掉的。

以 Fred Brooks 命名，《人月神话》的作者 — 因为最难的错误是概念性的，而不是语法性的。

## 12 部书籍

| 书籍 | 应用的关键原则 |
|------|--------------|
| *程序员修养* | DRY、正交性、追踪子弹 |
| *代码整洁之道* | 命名、函数大小、注释清晰度 |
| *人月神话* | 概念完整性、第二系统效应 |
| *设计数据密集型应用* | 数据一致性、容错性、可扩展性 |
| *软件设计哲学* | 深度模块、信息隐藏、复杂性 |
| *重构* | 代码异味、提取方法、封装 |
| *有效地处理遗留代码* | 接缝、特性化测试、依赖破坏 |
| *领域驱动设计* | 通用语言、界限上下文、聚合体 |
| *发布它！* | 稳定性模式、超时、隔舱、断路器 |
| *计算机程序的结构和解释* | 抽象、递归、元语言抽象 |
| *UNIX 编程艺术* | 模块性、可组合性、最小惊讶原则 |
| *极限编程解说* | YAGNI、简单设计、集体所有权 |

## 何时使用此技能

- 当你希望获得超过 linters 提供的架构反馈时使用
- 在主要重构前使用以识别结构债务
- 当审查"有效但感觉错误"的代码时使用
- 当入职到代码库以快速映射风险区域时使用
- 在启动新模块或服务前用于设计审查

## 它如何工作

Brooks Lint 将每本书的核心原则应用为审查镜头：

1. **异味检测**：标记 DRY、SRP、得墨忒尔法则等的违规
2. **耦合分析**：识别紧密依赖和缺失的抽象层
3. **命名评论**：将代码整洁之道命名规则应用于变量、方法、类
4. **架构审查**：检查 DDIA 式数据一致性和容错性差距
5. **稳定性模式**：标记缺失的超时、重试和断路器（发布它！）
6. **复杂性评分**：应用 APOSD 复杂性指标以识别过度工程化部分

## 安装

```bash
# 通过 Claude Code 插件市场安装
# 搜索：Claude Code > 扩展中的"brooks-lint"

# 或通过 NPX 安装（Antigravity）
npx agentic-awesome-skills --claude
# 然后调用：@brooks-lint
```

## 示例

### 示例 1：审查服务类

```
@brooks-lint review src/services/PaymentService.ts
```

**Brooks Lint 输出：**
```
[Pragmatic Programmer] DRY 违规：支付验证逻辑在 3 个地方重复
[Clean Code] 方法 processPayment() 做 4 件事 — 违反单一责任
[Release It!] 外部支付网关调用上没有超时 — 级联失败风险
[DDIA] 没有幂等密钥 — 网络错误重试会双重收费
[APOSD] PaymentService 对 UserRepository 的了解太多 — 高耦合
```

### 示例 2：完整代码库架构审查

```
@brooks-lint analyze the overall architecture of this codebase
```

### 示例 3：重构前审查

```
@brooks-lint what are the biggest design smells in this module before I refactor it?
```

## 审查类别

| 类别 | 应用的书籍 | 捕捉的内容 |
|-----|---------|----------|
| **DRY / 重复** | PP、重构 | 复制粘贴代码、未提取的共享逻辑 |
| **命名** | 代码整洁之道、DDD | 不清晰的名称、领域语言违规 |
| **耦合** | APOSD、PP | 紧密依赖、缺失接口 |
| **稳定性** | 发布它！ | 缺失超时、无重试逻辑、无断路器 |
| **数据完整性** | DDIA | 竞态条件、非幂等操作 |
| **复杂性** | APOSD、SICP | 过度工程化、不必要的抽象 |
| **遗留债务** | WELC | 难以测试的代码、缺失接缝 |
| **领域清晰度** | DDD、XP | 贫血模型、缺失界限上下文 |

## 最佳实践

- 在编写新的服务层或数据管道后运行 `@brooks-lint`
- 与 `@logic-lens` 结合以获得完整覆盖：逻辑错误 + 设计异味
- 在增长的代码库上每周使用 `@brooks-lint analyze architecture`
- 首先关注关键和高级发现 — 低级发现是样式建议

## 相关技能

- `@logic-lens` — 互补：捕捉逻辑错误；brooks-lint 捕捉设计问题
- `@security-auditor` — 专门的仅安全深度扫描
- `@lint-and-validate` — 样式/语法 linting 以配合设计审查运行

## 其他资源

- [GitHub 存储库](https://github.com/hyhmrright/brooks-lint)
- [Dev.to 文章：我将 12 部经典工程书合成为一个人工智能代码评审器](https://dev.to/hyhmrright/i-synthesized-12-classic-engineering-books-into-an-ai-code-reviewer-heres-what-it-caught-3ed1)
- [相关技能：logic-lens](https://github.com/hyhmrright/logic-lens)

## 限制

仅当任务清楚地符合上述范围（设计审查和架构分析）时才使用此技能。Brooks Lint 应用基于既定工程原则的人工智能驱动分析。它应补充而非取代人工设计审查以进行生产关键决策。结果反映 12 部源书籍的原则，可能不适用于所有架构风格或领域。
