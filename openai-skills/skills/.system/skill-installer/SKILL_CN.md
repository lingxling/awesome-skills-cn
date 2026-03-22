---
name: skill-installer
description: 从精选列表或 GitHub 仓库路径将 Codex 技能安装到 $CODEX_HOME/skills。当用户要求列出可安装技能、安装精选技能或从其他仓库（包括私有仓库）安装技能时使用。
metadata:
  short-description: 从 openai/skills 或其他仓库安装精选技能
---

# 技能安装器

帮助安装技能。默认从 https://github.com/openai/skills/tree/main/skills/.curated 安装，但用户也可以提供其他位置。实验性技能位于 https://github.com/openai/skills/tree/main/skills/.experimental，可以以相同方式安装。

根据任务使用辅助脚本：
- 当用户询问可用内容或用户使用此技能但未指定要做什么时，列出技能。默认列出 `.curated`，但当用户询问实验性技能时，可以传递 `--path skills/.experimental`。
- 当用户提供技能名称时，从精选列表安装。
- 当用户提供 GitHub 仓库/路径（包括私有仓库）时，从其他仓库安装。

使用辅助脚本安装技能。

## 沟通

列出技能时，根据用户请求的上下文，输出大致如下内容。如果他们询问实验性技能，则从 `.experimental` 而非 `.curated` 列出，并相应标记来源：
"""
来自 {repo} 的技能：
1. skill-1
2. skill-2（已安装）
3. ...
您想安装哪些？
"""

安装技能后，告诉用户："重启 Codex 以加载新技能。"

## 脚本

所有这些脚本都使用网络，因此在沙盒中运行时，运行它们时请求提升权限。

- `scripts/list-skills.py`（打印带有已安装注释的技能列表）
- `scripts/list-skills.py --format json`
- 示例（实验性列表）：`scripts/list-skills.py --path skills/.experimental`
- `scripts/install-skill-from-github.py --repo <owner>/<repo> --path <path/to/skill> [<path/to/skill> ...]`
- `scripts/install-skill-from-github.py --url https://github.com/<owner>/<repo>/tree/<ref>/<path>`
- 示例（实验性技能）：`scripts/install-skill-from-github.py --repo openai/skills --path skills/.experimental/<skill-name>`

## 行为和选项

- 默认对公共 GitHub 仓库使用直接下载。
- 如果下载因身份验证/权限错误而失败，则回退到 git 稀疏检出。
- 如果目标技能目录已存在，则中止。
- 安装到 `$CODEX_HOME/skills/<skill-name>`（默认为 `~/.codex/skills`）。
- 多个 `--path` 值在一次运行中安装多个技能，每个都从路径基本名称命名，除非提供了 `--name`。
- 选项：`--ref <ref>`（默认 `main`）、`--dest <path>`、`--method auto|download|git`。

## 注意事项

- 精选列表通过 GitHub API 从 `https://github.com/openai/skills/tree/main/skills/.curated` 获取。如果不可用，解释错误并退出。
- 可以通过现有的 git 凭据或可选的 `GITHUB_TOKEN`/`GH_TOKEN` 进行下载来访问私有 GitHub 仓库。
- Git 回退首先尝试 HTTPS，然后尝试 SSH。
- https://github.com/openai/skills/tree/main/skills/.system 的技能已预安装，因此无需帮助用户安装这些技能。如果他们询问，只需解释这一点。如果他们坚持，您可以下载并覆盖。
- 已安装的注释来自 `$CODEX_HOME/skills`。
