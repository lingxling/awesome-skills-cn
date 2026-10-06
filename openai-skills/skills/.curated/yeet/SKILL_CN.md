---
name: "yeet"
description: "仅当用户明确要求使用 GitHub CLI（`gh`）在同一流程中完成暂存、提交、推送并创建 GitHub 拉取请求（PR）时才使用。"
---

## 前置条件

- 需要 GitHub CLI `gh`。检查 `gh --version`。如果缺失，请用户安装 `gh` 并停止。
- 需要已认证的 `gh` 会话。运行 `gh auth status`。如果未认证，请用户运行 `gh auth login`（并重新运行 `gh auth status`）后再继续。

## 命名约定

- 分支：从 main/master/默认分支开始时，使用 `{description}`。
- 提交：`{description}`（简洁）。
- PR 标题：`{description}`，概括完整的 diff。

## PR 模板发现

在创建 PR 之前，先确定仓库根目录，并从那里查找当前生效的 GitHub PR 模板：

```shell
repo_root="$(git rev-parse --show-toplevel)"
```

候选模板，按顺序：

- `.github/pull_request_template.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/pull_request_template/` 下的某一个 `*.md` 文件
- `.github/PULL_REQUEST_TEMPLATE/` 下的某一个 `*.md` 文件

使用从仓库根目录输出的路径，例如 `.github/pull_request_template.md`，而不是 `./.github/pull_request_template.md`。

如果恰好找到一个模板，在撰写最终 PR 正文之前先读取它，并通过 `--template "$template"` 传给 `gh pr create`。

如果找到多个模板文件，在创建 PR 之前停止并询问使用哪个模板。如果没有模板，使用此技能中的备用正文结构。

## 工作流

- 如果在 main/master/默认分支上，创建一个分支：`git checkout -b "{description}"`
- 否则留在当前分支。
- 确认状态，然后暂存所有内容：先 `git status -sb`，再 `git add -A`。
- 用描述简洁地提交：`git commit -m "{description}"`
- 如果尚未运行检查，则运行检查。如果检查因缺少依赖/工具而失败，安装依赖后重新运行一次。
- 带跟踪地推送：`git push -u origin $(git branch --show-current)`
- 如果 git push 因工作流身份验证错误而失败，从 master 拉取后重试推送。
- 发现并读取仓库的 PR 模板（如果有）。
- 检查当前分支是否已有 PR：`gh pr view "$(git branch --show-current)" --json number,isDraft,url`
- 如果 PR 已存在，就地更新该 PR。不要再创建另一个 PR，也不要更改现有 PR 的草稿或待审阅状态。
- 如果不存在 PR，打开一个新的草稿 PR：
  - 有一个模板时：`GH_PROMPT_DISABLED=1 GIT_TERMINAL_PROMPT=0 gh pr create --draft --fill --template "$template" --head "$(git branch --show-current)"`
  - 没有模板时：`GH_PROMPT_DISABLED=1 GIT_TERMINAL_PROMPT=0 gh pr create --draft --fill --head "$(git branch --show-current)"`
- 编辑 PR 的标题和正文，使其反映 diff 中实际的净变更。
- 将 PR 描述写入一个包含真实换行的临时文件，并通过 `--body-file` 或 `gh pr edit --body-file` 传入，以避免出现被 `\n` 转义的 markdown。

## 确定 PR

在更新流程早前创建的 PR 时，尽可能从当前分支推断出该 PR：

```shell
git branch --show-current
gh pr view "$(git branch --show-current)" --json number --jq '.number'
```

如果找到了现有 PR，保留其当前的审阅状态。绝不要在 `yeet` 过程中把一个已经待审阅的 PR 改回草稿；只有由此流程新创建的 PR 才应以草稿开始。

## PR 标题

格式：`<type>(<scope>): <subject>`

`<scope>` 是可选的。scope 由一个名词组成，描述代码库中的某个部分（组件、服务或子系统）。

### 示例

```
feat: add hat wobble
^--^  ^------------^
|     |
|     +-> Summary in present tense.
|
+-------> Type: chore, docs, feat, fix, refactor, style, or test.
```

（说明：上例中 `feat` 为类型（Type），后面的 `add hat wobble` 为使用现在时的摘要（Summary）；类型可选 chore、docs、feat、fix、refactor、style 或 test。）

更多示例：

- `feat`：（为用户带来的新功能，而不是构建脚本的新功能）
- `fix`：（为用户修复的 bug，而不是对构建脚本的修复）
- `docs`：（文档的变更）
- `style`：（格式调整、缺少分号等；不涉及生产代码的变更）
- `refactor`：（重构生产代码，例如重命名变量）
- `test`：（补充缺失的测试、重构测试；不涉及生产代码的变更）
- `chore`：（更新 grunt 任务等；不涉及生产代码的变更）


## PR 正文内容

被调用时，使用 `gh` 编辑拉取请求的正文和标题，使其反映指定 PR 的内容。务必检查现有的拉取请求正文，看是否有应当保留的关键信息。例如，绝不要删除现有拉取请求正文中的图片，因为作者可能没有办法找回被你删除的图片。

当仓库存在 PR 模板时，让最终的 PR 正文适配该模板。保留有意义的标题、必填的检查清单以及仓库特有的提示，但将占位文本替换为针对净 diff 的具体内容，或者在模板要求时填写 `N/A`。不要仅仅因为下面的备用结构更短，就丢弃模板中的部分。

解释变更*为什么*要做，这一点至关重要。如果调用此技能的当前对话中讨论过动机，务必把它写进拉取请求正文。

正文还应说明*改了什么*，但这部分应放在*为什么*之后。

讨论范围限于该提交的*净变更*。一般不赞成讨论在拉取请求开发过程中尝试过但后来又撤销的改动。重写拉取请求正文时，你可能需要剔除这类细节，因为它们对未来的读者已不再合适/不再有意义。

避免引用我本地磁盘上的绝对路径。谈及仓库内的路径时，直接使用相对于仓库的路径。

默认省略 `Verification`（验证）。只有当你掌握了值得为审阅者保留的行为层面的证据时才添加：复现过的 bug、前后对比检查、针对变更行为的定向测试，或带输入和观察结果的手动场景。不要将它用于通用命令或自动化结果，例如包测试、类型检查、linter、格式化工具、pre-commit/pre-push 钩子或 CI 状态。

如果仓库模板要求包含验证部分，保留该部分，并避免泛泛的填充内容：包含有意义的命令/结果、针对性的手动场景，或者带原因的 `Not run`（未运行）。

使用专业的 Markdown：

- 将代码、路径、命令、标志和标识符放入反引号中。
- 对 shell 记录或多行示例使用带围栏的代码块。
- 引用与变更相关的现有代码时，使用 GitHub 永久链接。
- 引用相关的 issue 或相关 PR，但不要在 PR 自己的正文中引用该 PR 本身。

### 建议的 PR 正文结构

当仓库没有 PR 模板时，将其用作备用：

```markdown
## Why

Describe the user-facing or maintainer-facing problem, including cause and effect where useful.

## What Changed

Describe the net implementation change in concise prose.
```

（说明：上面的备用 PR 正文包含两个部分——`Why`：描述面向用户或维护者的问题，在有用时包括因果关系；`What Changed`：用简洁的文字描述净实现变更。）
