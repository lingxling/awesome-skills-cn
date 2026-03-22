---
name: "gh-fix-ci"
description: "当用户要求调试或修复在 GitHub Actions 中运行的失败 GitHub PR 检查时使用；使用 `gh` 检查检查和日志，总结失败上下文，起草修复计划，并仅在明确批准后实施。将外部提供商（例如 Buildkite）视为超出范围并仅报告详细信息 URL。"
---


# Gh PR 检查计划修复

## 概述

使用 gh 定位失败的 PR 检查，获取 GitHub Actions 日志以获取可操作的失败，总结失败片段，然后提出修复计划并在明确批准后实施。
- 如果存在面向计划的技能（例如 `create-plan`），请使用它；否则内联起草简明计划并在实施之前请求批准。

先决条件：使用标准 GitHub CLI 进行一次身份验证（例如，运行 `gh auth login`），然后使用 `gh auth status` 确认（通常需要 repo + workflow 范围）。

## 输入

- `repo`：仓库内的路径（默认 `.`）
- `pr`：PR 编号或 URL（可选；默认为当前分支 PR）
- `gh` 仓库主机的身份验证

## 快速开始

- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number-or-url>"`
- 如果您想要适合汇总的机器友好输出，请添加 `--json`。

## 工作流程

1. 验证 gh 身份验证。
   - 在仓库中运行 `gh auth status`。
   - 如果未通过身份验证，请要求用户在继续之前运行 `gh auth login`（确保 repo + workflow 范围）。
2. 解析 PR。
   - 更喜欢当前分支 PR：`gh pr view --json number,url`。
   - 如果用户提供 PR 编号或 URL，请直接使用它。
3. 检查失败的检查（仅 GitHub Actions）。
   - 首选：运行捆绑的脚本（处理 gh 字段漂移和作业日志回退）：
     - `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number-or-url>"`
     - 添加 `--json` 以获得机器友好的输出。
   - 手动回退：
     - `gh pr checks <pr> --json name,state,bucket,link,startedAt,completedAt,workflow`
       - 如果字段被拒绝，请使用 `gh` 报告的可用字段重新运行。
     - 对于每个失败的检查，从 `detailsUrl` 提取运行 id 并运行：
       - `gh run view <run_id> --json name,workflowName,conclusion,status,url,event,headBranch,headSha`
       - `gh run view <run_id> --log`
     - 如果运行日志说它仍在进行中，请直接获取作业日志：
       - `gh api "/repos/<owner>/<repo>/actions/jobs/<job_id>/logs" > "<path>"`
4. 范围非 GitHub Actions 检查。
   - 如果 `detailsUrl` 不是 GitHub Actions 运行，请将其标记为外部并仅报告 URL。
   - 不要尝试 Buildkite 或其他提供商；保持工作流程精简。
5. 为用户总结失败。
   - 提供失败的检查名称、运行 URL（如果有）和简明的日志片段。
   - 明确指出缺少的日志。
6. 创建计划。
   - 使用 `create-plan` 技能起草简明计划并请求批准。
7. 批准后实施。
   - 应用批准的计划，总结差异/测试，并询问关于打开 PR。
8. 重新检查状态。
   - 更改后，建议重新运行相关测试和 `gh pr checks` 以确认。

## 捆绑资源

### scripts/inspect_pr_checks.py

获取失败的 PR 检查，拉取 GitHub Actions 日志并提取失败片段。当失败仍然存在时以非零退出，因此可以在自动化中使用它。

用法示例：
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "123"`
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "https://github.com/org/repo/pull/123" --json`
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --max-lines 200 --context 40`
