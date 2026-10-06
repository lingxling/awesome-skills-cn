---
name: gh-address-comments
description: 使用 gh CLI 帮助处理当前分支上已打开的 GitHub PR 的审查/议题评论；首先验证 gh 身份验证，如果未登录则提示用户进行身份验证。
metadata:
  short-description: Address comments in a GitHub PR review
---

# PR 评论处理器

指导如何找到当前分支上已打开的 PR，并使用 gh CLI 处理其评论。使用提升的网络访问权限运行所有 `gh` 命令。

前置条件：确保 `gh` 已通过身份验证（例如，运行一次 `gh auth login`），然后使用提升的权限运行 `gh auth status`（包含 workflow/repo 范围），以便 `gh` 命令能够成功。如果沙箱阻止了 `gh auth status`，请使用 `sandbox_permissions=require_escalated` 重新运行它。

## 1) 检查需要处理的评论
- 运行 scripts/fetch_comments.py，它会打印出该 PR 上的所有评论和审查线程

## 2) 向用户寻求澄清
- 为所有审查线程和评论编号，并为每一条提供一份简短的摘要，说明要应用修复需要做什么
- 询问用户应该处理哪些编号的评论

## 3) 如果用户选择了评论
- 为选定的评论应用修复

注意：
- 如果 gh 在运行中途遇到身份验证/速率问题，提示用户使用 `gh auth login` 重新验证，然后重试。
