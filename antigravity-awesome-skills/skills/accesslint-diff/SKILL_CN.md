---
name: accesslint-diff
description: "对实时页面的无障碍违规进行差异比较 — 默认情况下比较未提交的更改（基于 stash），或传递 --branch [<name>] 来对分支进行差异。仅报告引入的新违规、已修复的违规和已存在的计数。使用 `scan` 进行完整审计，无差异。"
risk: safe
source: "https://github.com/AccessLint/skills"
date_added: "2026-06-02"
---

默认分支：!`git symbolic-ref refs/remotes/origin/HEAD --short 2>/dev/null | sed 's|.*/||' || echo main`

仅报告更改的内容。定位；不要修复。如果 `$ARGUMENTS` 中没有 URL，请要求一个。

解析 `$ARGUMENTS`：如果存在则剥离 `--branch <name>` → 分支模式。如果 `--branch` 没有值，使用上面的默认分支。剩余是 URL。

## 何时使用

- 当任务与此描述匹配时使用此技能：对实时页面的无障碍违规进行差异比较 — 默认情况下比较未提交的更改（基于 stash），或传递 --branch [<name>] 来对分支进行差异。仅报告引入的新违规、已修复的违规和已存在的计数。使用 `scan` 进行完整审计，无差异。

## 1. 审计

```bash
PORT=$(npx -y @accesslint/chrome@latest ensure | node -e 'process.stdin.on("data",d=>process.stdout.write(""+JSON.parse(d).port))')
```

**Stash 模式**（默认 — 未提交的更改）。首先告知用户：_"以差异模式运行 — stashing 你的更改以捕获基线，然后恢复。你的工作树将完全恢复。"_ 如果 `git stash push` 失败，警告并退出。

```bash
git stash push -u -m "accesslint-diff-baseline"
npx -y @accesslint/cli@latest "<url>" --port "$PORT" --snapshot accesslint-diff --snapshot-dir /tmp --update-snapshot
git stash pop && sleep 2
npx -y @accesslint/cli@latest "<url>" --port "$PORT" --snapshot accesslint-diff --snapshot-dir /tmp --format json
```

**分支模式**（`--branch <name>`）。首先告知用户：_"对 `<name>` 进行差异 — 检出该分支以捕获基线，然后恢复。你的工作树将完全恢复。"_

分支切换触发重建但不触发浏览器重新加载 — CLI 每次打开一个新选项卡，所以它总是读取当前构建。使用 `--wait-for "<selector>"` 来阻止审计直到重建就绪；没有它，警告用户慢构建可能会产生过时的基线。

在下面的引用 `branch` 变量中保持分支值；绝不要粘贴或评估分支名称作为 shell 语法。

```bash
git diff --quiet && git diff --cached --quiet || git stash push -u -m "accesslint-diff-branch"
branch="<branch>"
git check-ref-format --branch "$branch" >/dev/null
case "$branch" in -*) echo "Refusing option-like branch name: $branch" >&2; exit 1 ;; esac
git rev-parse --verify --quiet "$branch^{commit}" >/dev/null
git switch "$branch"
npx -y @accesslint/cli@latest "<url>" --port "$PORT" --snapshot accesslint-diff --snapshot-dir /tmp --update-snapshot [--wait-for "<selector>"]
git switch - && git stash pop 2>/dev/null
npx -y @accesslint/cli@latest "<url>" --port "$PORT" --snapshot accesslint-diff --snapshot-dir /tmp --format json [--wait-for "<selector>"]
```

将 `--selector`、`--include-aaa` 传递给 **两个** 运行。

## 2. 报告

```
无障碍差异 — http://localhost:3000/ vs main (94 规则，实时 DOM)
2 新增 · 1 已修复 · 4 已存在隐藏

新增 — 严重
- color-contrast — 2.1:1（需要 4.5:1），#bbb 在 #fff
    位置：main > p.subtitle   修复：深化到 #767676
已修复
- img-alt — <img src="old.jpg">（不再存在）
```

每个新违规：**位置**（逐字选择器 + `file:line (symbol)` 如果 `source` 存在 — 绝不伪造），**证据**，**修复**（机械改变或 `需要人工`）。

不要编辑。对于修复：应用机械修复然后重新运行 `accesslint:diff` 以验证；对于大量工作移交给 `accesslint:audit`。

## 3. 清除

```bash
npx -y @accesslint/chrome@latest stop --all  # 如果 ensure 报告 "managed":false 则跳过
```

## 陷阱

- `ensure` 总是确定端口 — 永不硬编码 9222。
- CLI 退出 2 = 坏 URL 或页面从不加载；检查开发服务器。
- Stash 模式：`sleep 2` 覆盖大多数 HMR 情况；如果基线看起来与当前相同，添加 `--wait-for "<selector>"`。
- 分支模式：无 HMR — CLI 每次运行打开新选项卡。`--wait-for` 是重建门。
- 运行之间的大量 DOM 更改导致选择器漂移 — 使用 `accesslint:scan` 重新运行以获得完整图景。

## 限制条件

- 仅在任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并寻求澄清。
