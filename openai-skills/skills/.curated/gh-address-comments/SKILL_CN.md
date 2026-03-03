---
name: gh-address-comments
description: "使用 gh CLI 帮助审查/解决当前分支上的开放 GitHub PR 的评论；首先验证 gh 身份验证，如果未登录则提示用户进行身份验证。"
---

# PR 评论处理程序

指导找到当前分支的开放 PR 并使用 gh CLI 解决其评论。使用提升的网络权限运行所有 `gh` 命令。

## 前置条件

确保 `gh` 已通过身份验证（例如，运行一次 `gh auth login`），然后运行 `gh auth status` 并使用提升的权限（包括 workflow/repo 范围），以便 `gh` 命令成功。如果沙箱阻止 `gh auth status`，使用 `sandbox_permissions=require_escalated` 重新运行它。

## 1) 检查需要注意的评论

- 运行 scripts/fetch_comments.py，它将打印出所有评论和 PR 上的审查线程。

## 2) 向用户寻求澄清

- 对所有审查线程和评论进行编号，并提供需要为它应用修复的简要总结。
- 询问用户应该解决哪些编号的评论。

## 3) 如果用户选择评论

- 为选定的评论应用修复。

## 注意事项

- 如果 gh 在运行中遇到身份验证/速率限制问题，请提示用户使用 `gh auth login` 重新验证，然后重试。
- 如果沙箱阻止 `gh auth status`，使用 `sandbox_permissions=require_escalated` 重新运行命令。
