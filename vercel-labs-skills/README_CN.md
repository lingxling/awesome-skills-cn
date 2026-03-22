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

<!-- supported-agents:start -->
| 代理 | `--agent` | 项目路径 | 全局路径 |
|-------|-----------|--------------|-------------|
| Amp, Kimi Code CLI, Replit, Universal | `amp`, `kimi-cli`, `replit`, `universal` | `.agents/skills/` | `~/.config/agents/skills/` |
| Antigravity | `antigravity` | `.agents/skills/` | `~/.gemini/antigravity/skills/` |
| Augment | `augment` | `.augment/skills/` | `~/.augment/skills/` |
| Claude Code | `claude-code` | `.claude/skills/` | `~/.claude/skills/` |
| OpenClaw | `openclaw` | `skills/` | `~/.openclaw/skills/` |
| Cline, Warp | `cline`, `warp` | `.agents/skills/` | `~/.agents/skills/` |
| CodeBuddy | `codebuddy` | `.codebuddy/skills/` | `~/.codebuddy/skills/` |
| Codex | `codex` | `.agents/skills/` | `~/.codex/skills/` |
| Command Code | `command-code` | `.commandcode/skills/` | `~/.commandcode/skills/` |
| Continue | `continue` | `.continue/skills/` | `~/.continue/skills/` |
| Cortex Code | `cortex` | `.cortex/skills/` | `~/.snowflake/cortex/skills/` |
| Crush | `crush` | `.crush/skills/` | `~/.config/crush/skills/` |
| Cursor | `cursor` | `.agents/skills/` | `~/.cursor/skills/` |
| Deep Agents | `deepagents` | `.agents/skills/` | `~/.deepagents/agent/skills/` |
| Droid | `droid` | `.factory/skills/` | `~/.factory/skills/` |
| Gemini CLI | `gemini-cli` | `.agents/skills/` | `~/.gemini/skills/` |
| GitHub Copilot | `github-copilot` | `.agents/skills/` | `~/.copilot/skills/` |
| Goose | `goose` | `.goose/skills/` | `~/.config/goose/skills/` |
| Junie | `junie` | `.junie/skills/` | `~/.junie/skills/` |
| iFlow CLI | `iflow-cli` | `.iflow/skills/` | `~/.iflow/skills/` |
| Kilo Code | `kilo` | `.kilocode/skills/` | `~/.kilocode/skills/` |
| Kiro CLI | `kiro-cli` | `.kiro/skills/` | `~/.kiro/skills/` |
| Kode | `kode` | `.kode/skills/` | `~/.kode/skills/` |
| MCPJam | `mcpjam` | `.mcpjam/skills/` | `~/.mcpjam/skills/` |
| Mistral Vibe | `mistral-vibe` | `.vibe/skills/` | `~/.vibe/skills/` |
| Mux | `mux` | `.mux/skills/` | `~/.mux/skills/` |
| OpenCode | `opencode` | `.agents/skills/` | `~/.config/opencode/skills/` |
| OpenHands | `openhands` | `.openhands/skills/` | `~/.openhands/skills/` |
| Pi | `pi` | `.pi/skills/` | `~/.pi/agent/skills/` |
| Qoder | `qoder` | `.qoder/skills/` | `~/.qoder/skills/` |
| Qwen Code | `qwen-code` | `.qwen/skills/` | `~/.qwen/skills/` |
| Roo Code | `roo` | `.roo/skills/` | `~/.roo/skills/` |
| Trae | `trae` | `.trae/skills/` | `~/.trae/skills/` |
| Trae CN | `trae-cn` | `.trae/skills/` | `~/.trae-cn/skills/` |
| Windsurf | `windsurf` | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |
| Zencoder | `zencoder` | `.zencoder/skills/` | `~/.zencoder/skills/` |
| Neovate | `neovate` | `.neovate/skills/` | `~/.neovate/skills/` |
| Pochi | `pochi` | `.pochi/skills/` | `~/.pochi/skills/` |
| AdaL | `adal` | `.adal/skills/` | `~/.adal/skills/` |
<!-- supported-agents:end -->

> [!NOTE]
> **Kiro CLI 用户：** 安装技能后，需要在 `.kiro/agents/<agent>.json` 中手动将它们添加到自定义代理的 `resources` 中：
>
> ```json
> {
>   "resources": ["skill://.kiro/skills/**/SKILL.md"]
> }
> ```

CLI 会自动检测您已安装的编码代理。如果没有检测到任何代理，系统会提示您选择要安装到的代理。

## 创建技能

技能是包含带有 YAML 前置数据的 `SKILL.md` 文件的目录：

```markdown
---
name: my-skill
description: What this skill does and when to use it
---

# My Skill

Instructions for the agent to follow when this skill is activated.

## When to Use

Describe the scenarios where this skill should be used.

## Steps

1. First, do this
2. Then, do that
```

### 必填字段

- `name`：唯一标识符（小写，允许使用连字符）
- `description`：技能功能的简要说明

### 可选字段

- `metadata.internal`：设置为 `true` 以在正常发现中隐藏该技能。内部技能仅在设置了 `INSTALL_INTERNAL_SKILLS=1` 时可见和可安装。适用于进行中的技能或仅用于内部工具的技能。

```markdown
---
name: my-internal-skill
description: An internal skill not shown by default
metadata:
  internal: true
---
```

### 技能发现

CLI 在仓库中的以下位置搜索技能：

<!-- skill-discovery:start -->
- 根目录（如果包含 `SKILL.md`）
- `skills/`
- `skills/.curated/`
- `skills/.experimental/`
- `skills/.system/`
- `.agents/skills/`
- `.augment/skills/`
- `.claude/skills/`
- `./skills/`
- `.codebuddy/skills/`
- `.commandcode/skills/`
- `.continue/skills/`
- `.cortex/skills/`
- `.crush/skills/`
- `.factory/skills/`
- `.goose/skills/`
- `.junie/skills/`
- `.iflow/skills/`
- `.kilocode/skills/`
- `.kiro/skills/`
- `.kode/skills/`
- `.mcpjam/skills/`
- `.vibe/skills/`
- `.mux/skills/`
- `.openhands/skills/`
- `.pi/skills/`
- `.qoder/skills/`
- `.qwen/skills/`
- `.roo/skills/`
- `.trae/skills/`
- `.windsurf/skills/`
- `.zencoder/skills/`
- `.neovate/skills/`
- `.pochi/skills/`
- `.adal/skills/`
<!-- skill-discovery:end -->

### 插件清单发现

如果存在 `.claude-plugin/marketplace.json` 或 `.claude-plugin/plugin.json`，则也会发现这些文件中声明的技能：

```json
// .claude-plugin/marketplace.json
{
  "metadata": { "pluginRoot": "./plugins" },
  "plugins": [
    {
      "name": "my-plugin",
      "source": "my-plugin",
      "skills": ["./skills/review", "./skills/test"]
    }
  ]
}
```

这实现了与 [Claude Code 插件市场](https://code.claude.com/docs/en/plugin-marketplaces)生态系统的兼容性。

如果在标准位置未找到技能，则执行递归搜索。

## 兼容性

由于技能遵循共享的[代理技能规范](https://agentskills.io)，因此它们在代理之间通常是兼容的。但是，某些功能可能是特定于代理的：

| 特性         | OpenCode | OpenHands | Claude Code | Cline | CodeBuddy | Codex | Command Code | Kiro CLI | Cursor | Antigravity | Roo Code | Github Copilot | Amp | OpenClaw | Neovate | Pi  | Qoder | Zencoder |
| --------------- | -------- | --------- | ----------- | ----- | --------- | ----- | ------------ | -------- | ------ | ----------- | -------- | -------------- | --- | -------- | ------- | --- | ----- | -------- |
| 基本技能    | Yes      | Yes       | Yes         | Yes   | Yes       | Yes   | Yes          | Yes      | Yes    | Yes         | Yes      | Yes            | Yes | Yes      | Yes     | Yes | Yes   | Yes      |
| `allowed-tools` | Yes      | Yes       | Yes         | Yes   | Yes       | Yes   | Yes          | No       | Yes    | Yes         | Yes      | Yes            | Yes | Yes      | Yes     | Yes | Yes   | No       |
| `context: fork` | No       | No        | Yes         | No    | No        | No    | No           | No       | No     | No          | No       | No             | No  | No       | No      | No  | No    | No       |
| Hooks           | No       | No        | Yes         | Yes   | No        | No    | No           | No       | No     | No          | No       | No             | No  | No       | No      | No  | No    | No       |

## 故障排除

### "No skills found"

确保仓库包含有效的 `SKILL.md` 文件，其中前置数据中同时包含 `name` 和 `description`。

### 技能未在代理中加载

- 验证技能是否已安装到正确的路径
- 检查代理文档中的技能加载要求
- 确保 `SKILL.md` 前置数据是有效的 YAML

### 权限错误

确保您对目标目录具有写入权限。

## 环境变量

| 变量                  | 描述                                                                |
| ------------------------- | -------------------------------------------------------------------------- |
| `INSTALL_INTERNAL_SKILLS` | 设置为 `1` 或 `true` 以显示和安装标记为 `internal: true` 的技能 |
| `DISABLE_TELEMETRY`       | 设置以禁用匿名使用遥测                                   |
| `DO_NOT_TRACK`            | 禁用遥测的替代方法                                       |

```bash
# 安装内部技能
INSTALL_INTERNAL_SKILLS=1 npx skills add vercel-labs/agent-skills --list
```

## 遥测

此 CLI 收集匿名使用数据以帮助改进工具。不收集任何个人信息。

遥测在 CI 环境中会自动禁用。

## 相关链接

- [代理技能规范](https://agentskills.io)
- [技能目录](https://skills.sh)
- [Amp 技能文档](https://ampcode.com/manual#agent-skills)
- [Antigravity 技能文档](https://antigravity.google/docs/skills)
- [Factory AI / Droid 技能文档](https://docs.factory.ai/cli/configuration/skills)
- [Claude Code 技能文档](https://code.claude.com/docs/en/skills)
- [OpenClaw 技能文档](https://docs.openclaw.ai/tools/skills)
- [Cline 技能文档](https://docs.cline.bot/features/skills)
- [CodeBuddy 技能文档](https://www.codebuddy.ai/docs/ide/Features/Skills)
- [Codex 技能文档](https://developers.openai.com/codex/skills)
- [Command Code 技能文档](https://commandcode.ai/docs/skills)
- [Crush 技能文档](https://github.com/charmbracelet/crush?tab=readme-ov-file#agent-skills)
- [Cursor 技能文档](https://cursor.com/docs/context/skills)
- [Gemini CLI 技能文档](https://geminicli.com/docs/cli/skills/)
- [GitHub Copilot 代理技能](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)
- [iFlow CLI 技能文档](https://platform.iflow.cn/en/cli/examples/skill)
- [Kimi Code CLI 技能文档](https://moonshotai.github.io/kimi-cli/en/customization/skills.html)
- [Kiro CLI 技能文档](https://kiro.dev/docs/cli/custom-agents/configuration-reference/#skill-resources)
- [Kode 技能文档](https://github.com/shareAI-lab/kode/blob/main/docs/skills.md)
- [OpenCode 技能文档](https://opencode.ai/docs/skills)
- [Qwen Code 技能文档](https://qwenlm.github.io/qwen-code-docs/en/users/features/skills/)
- [OpenHands 技能文档](https://docs.openhands.ai/modules/usage/how-to/using-skills)
- [Pi 技能文档](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md)
- [Qoder 技能文档](https://docs.qoder.com/cli/Skills)
- [Replit 技能文档](https://docs.replit.com/replitai/skills)
- [Roo Code 技能文档](https://docs.roocode.com/features/skills)
- [Trae 技能文档](https://docs.trae.ai/ide/skills)
- [Vercel 代理技能仓库](https://github.com/vercel-labs/agent-skills)

## 许可证

MIT
