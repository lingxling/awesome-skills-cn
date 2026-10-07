---
# agentskills.io compliant frontmatter
name: clarity-gate
risk: critical
source: community
date_added: "2026-09-04"
version: 2.1.3
description: >
  RAG 系统中知识论质量的预摄入验证。
  确保文件在进入知识库前得到正确限定。
  生成 CGD（清晰度限制的文件）并验证 SOT（真实来源）文件。
author: Francesco Marinoni Moretto
license: CC-BY-4.0
repository: https://github.com/frmoretto/clarity-gate
triggers:
  - clarity gate
  - check for hallucination risks
  - can an LLM read this safely
  - review for equivocation
  - verify document clarity
  - pre-ingestion check
  - cgd verify
  - sot verify
capabilities:
  - document-verification
  - epistemic-quality
  - rag-preparation
  - cgd-generation
  - sot-validation
outputs:
  - type: cgd
    extension: .cgd.md
    spec: docs/CLARITY_GATE_FORMAT_SPEC.md
spec_version: "2.1"
---

# Clarity Gate v2.1

**目的**：预摄入验证系统，在文件进入 RAG 知识库前强制实施知识论质量。生成符合 Clarity Gate 格式规范 v2.1 的清晰度限制的文件 (CGD)。

**核心问题**："如果另一个 LLM 读这份文件，它会将假设误认为事实吗？"

**核心原则**：*"检测找到现状；强制实施确保应该如何。实际上：在它们成为自信的幻觉之前，找到缺失的不确定性标记。"*

---

## 详细指南

在执行此技能前，阅读[详细指南](references/detailed-guide.md)。它保留了完整的程序和参考资料。将其安全性、先决条件和验证要求视为强制性的。对于专注工作，加载相关部分；对于端到端工作，完全阅读指南。

## 关键限制

> **Clarity Gate 验证格式，而不是真实性。**
>
> 此技能检查索赔是否已正确标记为不确定 — 它无法验证索赔是否真实。
>
> **风险**：LLM 可以将事实幻觉化到文件中，然后通过向虚假索赔添加源标记来"通过" Clarity Gate。
>
> **解决方案**：HITL（人在环中）验证**必须**在声明通过之前进行。

---

## 何时使用
- 在将文件摄入 RAG 系统之前
- 在与其他 AI 系统共享文件之前
- 编写规范、状态文件或方法描述之后
- 当文件包含预测、估计或假设时
- 在发布尚未验证的索赔之前
- 在 LLM 会话之间移交文件时

---

## 此技能不做什么

- 不对文件类型进行分类（对此使用 Stream Coding）
- 不重构文件
- 不添加深层链接或参考
- 不评估写作质量
- **不自主检查事实准确性**（需要 HITL）

---
