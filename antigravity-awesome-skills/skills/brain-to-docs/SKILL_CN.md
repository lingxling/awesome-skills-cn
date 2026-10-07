---
name: brain-to-docs
description: 采访用户，将项目愿景和决定转变为 README 和 ADR 文档。
category: productivity
risk: critical
source: community
source_repo: davidondrej/skills
source_type: community
date_added: "2026-07-07"
author: davidondrej
tags: [documentation, adr, planning]
tools: [claude, codex]
license: "MIT"
license_source: "https://github.com/davidondrej/skills/blob/main/LICENSE"
---

# brain-to-docs

## 何时使用

- 当用户想要将项目愿景、决定或偏好提取到持久文档中时使用。
- 当应通过来回采访构建 README 和 ADR 时使用。

整个目的：尽可能多地将用户的品味、判断、知识、愿景、偏好和决定提取到文本中 — 作为项目的清晰、简洁的 markdown 文档保存。README 持有愿景；`docs/adr/` 持有决定。

## 循环

1. **首先检查文档，每次都要。** 在做任何事情之前阅读 `docs/adr/`（和 `README.md`）— 其他代理和人员不断添加/编辑 ADR。
2. **用纯文本提出 5 个不同的问题**（从不是问题 UI）— 默认 5 个，除非用户要求不同的数字。使其具有高度多样性：具有各种角度的广泛、创意谱系，不都是同一类型（例如，不都是"技术堆栈"或都是"产品"或都是"货币化"）。例外：如果用户要求特定的焦点区域，请按照。用户回答他们认为最有用的内容。
3. **在每个答案后更新文档** — 没有例外。您决定是否更新 `README.md` 或成为新的 ADR — 随便什么有意义。
4. 重复直到用户说"我们完成了"（或类似）。

## 规则

- 此"大脑到文档"过程中的所有答案和回复必须非常简洁，所有句子都应简短，一切都应以纯英文写成。
- ADR：短、编号的 `NNNN-slug.md`、状态 + 上下文 + 决定 + 后果。
- README：仅限愿景。决定进入 ADR。
- 不要质疑用户的想法，除非他们要求或他们犯了严重错误。

## 示例

**用户请求：**

> 将项目愿景、决定或偏好提取到持久文档中。

## 限制

- 适应自 `davidondrej/skills`；在操作前验证本地路径、工具、凭证和代理功能。
- 对于命令、远程访问、调度、浏览器自动化或文件更改工作流，获得明确的用户批准并首先确认目标环境。
