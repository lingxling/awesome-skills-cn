# Skills CLI 中文翻译

> 本文档是 [Vercel Skills CLI](https://github.com/vercel-labs/skills) 的中文翻译版本。

## 关于本翻译

### 原项目介绍

**Skills CLI** 是开放代理技能生态系统的命令行工具，用于管理 AI 编程助手的技能包。它支持 40+ 种 AI 编程助手，包括：

- Claude Code
- Cursor
- OpenCode
- Codex
- Trae
- Windsurf
- GitHub Copilot
- 以及更多...

Skills CLI 让你可以：
- **安装技能** - 从 GitHub 或其他来源安装技能包
- **查找技能** - 交互式搜索或关键词搜索技能
- **管理技能** - 列表、更新、移除已安装的技能
- **创建技能** - 创建新的技能模板

### 翻译说明

本翻译将原项目的核心文档翻译成中文，帮助中文用户更好地理解和使用 Skills CLI。

### 翻译内容

- `skills/find-skills/SKILL.md` - 技能发现与安装指南的中文翻译

### 翻译原则

- 保持技术术语的准确性
- 使用简洁明了的中文表达
- 保留原文档的结构和格式
- 命令示例保持原样（不翻译命令）

### 原项目链接

- [GitHub 仓库](https://github.com/vercel-labs/skills)
- [技能目录](https://skills.sh)
- [代理技能规范](https://agentskills.io)

### 翻译项目

本翻译属于 [awesome-skills-cn](https://github.com/lingxling/awesome-skills-cn) 项目的一部分，致力于将优秀的英文 SKILL 翻译成中文。

---
以下是原README.md的内容：

## 安装skills

```bash
npx skills add vercel-labs/agent-skills
```

### 源格式

```bash
# GitHub 简写 (owner/repo)
npx skills add vercel-labs/agent-skills

# 完整 GitHub URL
npx skills add https://github.com/vercel-labs/agent-skills

# 仓库中特定技能的直接路径
npx skills add https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines

# GitLab URL
npx skills add https://gitlab.com/org/repo

# 任何 git URL
npx skills add git@github.com:vercel-labs/agent-skills.git

# 本地路径
npx skills add ./my-local-skills
```

### 可选项

| 选项                    | 描述                                                                                                                                        |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-g, --global`            | 安装到用户目录而不是项目目录                                                                                                       |
| `-a, --agent <agents...>` | <!-- agent-names:start -->目标特定代理（例如，`claude-code`、`codex`）。参见[可用代理](#available-agents)<!-- agent-names:end -->                  |
| `-s, --skill <skills...>` | 按名称安装特定技能（使用 `'*'` 安装所有技能）                                                                                         |
| `-l, --list`              | 列出可用技能而不安装                                                                                                           |
| `--copy`                  | 复制文件而不是符号链接到代理目录                                                                                              |
| `-y, --yes`               | 跳过所有确认提示                                                                                                                      |
| `--all`                   | 在不提示的情况下将所有技能安装到所有代理                                                                                                   |

### 示例

```bash
# 列出仓库中的技能
npx skills add vercel-labs/agent-skills --list

# 安装特定技能
npx skills add vercel-labs/agent-skills --skill frontend-design --skill skill-creator

# 安装名称中包含空格的技能（必须加引号）
npx skills add owner/repo --skill "Convex Best Practices"

# 安装到特定代理
npx skills add vercel-labs/agent-skills -a claude-code -a opencode

# 非交互式安装（CI/CD 友好）
npx skills add vercel-labs/agent-skills --skill frontend-design -g -a claude-code -y

# 将仓库中的所有技能安装到所有代理
npx skills add vercel-labs/agent-skills --all

# 将所有技能安装到特定代理
npx skills add vercel-labs/agent-skills --skill '*' -a claude-code

# 将特定技能安装到所有代理
npx skills add vercel-labs/agent-skills --agent '*' --skill frontend-design
```

### 安装范围

| 范围       | 标志      | 位置            | 使用场景                                      |
| ----------- | --------- | ------------------- | --------------------------------------------- |
| **项目** | (默认) | `./<agent>/skills/` | 与项目一起提交，与团队共享 |
| **全局**  | `-g`      | `~/<agent>/skills/` | 在所有项目中可用                 |

### 安装方法

交互式安装时，您可以选择：

| 方法                    | 描述                                                                                 |
| ------------------------- | ------------------------------------------------------------------------------------------- |
| **符号链接**（推荐） | 从每个代理创建符号链接到规范副本。单一事实来源，易于更新。 |
| **复制**                  | 为每个代理创建独立副本。当不支持符号链接时使用。              |

## 其他命令

| 命令                      | 描述                                    |
| ---------------------------- | ---------------------------------------------- |
| `npx skills list`            | 列出已安装的技能（别名：`ls`）            |
| `npx skills find [query]`    | 交互式或按关键词搜索技能  |
| `npx skills remove [skills]` | 从代理中移除已安装的技能            |
| `npx skills check`           | 检查可用的技能更新              |
| `npx skills update`          | 将所有已安装的技能更新到最新版本 |
| `npx skills init [name]`     | 创建新的 SKILL.md 模板                 |

### `skills list`

列出所有已安装的技能。类似于 `npm ls`。

```bash
# 列出所有已安装的技能（项目和全局）
npx skills list

# 仅列出全局技能
npx skills ls -g

# 按特定代理过滤
npx skills ls -a claude-code -a cursor
```

### `skills find`

交互式或按关键词搜索技能。

```bash
# 交互式搜索（fzf 风格）
npx skills find

# 按关键词搜索
npx skills find typescript
```

### `skills check` / `skills update`

```bash
# 检查是否有任何已安装的技能有更新
npx skills check

# 将所有技能更新到最新版本
npx skills update
```

### `skills init`

```bash
# 在当前目录创建 SKILL.md
npx skills init

# 在子目录中创建新技能
npx skills init my-skill
```

### `skills remove`

从代理中移除已安装的技能。

```bash
# 交互式移除（从已安装的技能中选择）
npx skills remove

# 按名称移除特定技能
npx skills remove web-design-guidelines

# 移除多个技能
npx skills remove frontend-design web-design-guidelines

# 从全局范围移除
npx skills remove --global web-design-guidelines

# 仅从特定代理移除
npx skills remove --agent claude-code cursor my-skill

# 在不确认的情况下移除所有已安装的技能
npx skills remove --all

# 从特定代理移除所有技能
npx skills remove --skill '*' -a cursor

# 从所有代理移除特定技能
npx skills remove my-skill --agent '*'

# 使用 'rm' 别名
npx skills rm my-skill
```

| 选项         | 描述                                      |
| -------------- | ------------------------------------------------ |
| `-g, --global` | 从全局范围（~/）而不是项目移除 |
| `-a, --agent`  | 从特定代理移除（对所有使用 `'*'）  |
| `-s, --skill`  | 指定要移除的技能（对所有使用 `'*'）     |
| `-y, --yes`    | 跳过确认提示                        |
| `--all`        | `--skill '*' --agent '*' -y` 的简写       |

## 什么是代理技能？

代理技能是可重用的指令集，用于扩展您的编码代理的能力。它们定义在包含 `name` 和 `description` 的 YAML 前置数据的 `SKILL.md` 文件中。

技能让代理可以执行专业任务，例如：

- 从 git 历史生成发布说明
- 按照团队的约定创建 PR
- 与外部工具集成（Linear、Notion 等）

在 **[skills.sh](https://skills.sh)** 发现技能

## 支持的代理

技能可以安装到以下任何代理：
