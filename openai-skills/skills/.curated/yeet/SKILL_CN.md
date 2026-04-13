---
name: "yeet"
description: "仅当用户明确要求在一个流程中使用 GitHub CLI（`gh`）暂存、提交、推送和打开 GitHub 拉取请求时使用。"
---

## 前置条件

- 需要 GitHub CLI `gh`。检查 `gh --version`。如果缺少，请要求用户安装 `gh` 并停止。
- 需要经过身份验证的 `gh` 会话。运行 `gh auth status`。如果未通过身份验证，请在继续之前要求用户运行 `gh auth login`（并重新运行 `gh auth status`）。

## 命名约定

- 分支：从 main/master/default 开始时使用 `{description}`。
- 提交：`{description}`（简洁）。
- PR 标题：`{description}` 总结完整差异。

## 工作流程

- 如果在 main/master/default 上，创建一个分支：`git checkout -b "{description}"`
- 否则停留在当前分支上。
- 确认状态，然后暂存所有内容：`git status -sb` 然后 `git add -A`。
- 使用描述简洁地提交：`git commit -m "{description}"`
- 如果尚未运行检查。如果由于缺少依赖/工具而导致检查失败，请安装依赖项并重新运行一次。
- 使用跟踪推送：`git push -u origin $(git branch --show-current)`
- 如果由于工作流程身份验证错误而导致 git push 失败，请从 master 拉取并重试推送。
- 打开一个 PR 并编辑标题/正文以反映描述和增量：`GH_PROMPT_DISABLED=1 GIT_TERMINAL_PROMPT=0 gh pr create --draft --fill --head $(git branch --show-current)`
- 将 PR 描述写入带有真实换行符的临时文件（例如，pr-body.md ... EOF）并运行 pr-body.md 以避免 \\n 转义的 markdown。
- PR 描述（markdown）必须是详细的散文，涵盖问题、原因和对用户的影响、根本原因、修复以及用于验证的任何测试或检查。
