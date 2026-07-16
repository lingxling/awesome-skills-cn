# Obsidian Skills 中文翻译版

> 本项目是 [Obsidian Skills](https://github.com/kepano/obsidian-skills) 的中文翻译版本，隶属于 [awesome-skills-cn](https://github.com/lxl666666/awesome-skills-cn) 项目。
>
> 原项目介绍：Obsidian Skills 是一组遵循 [Agent Skills 规范](https://agentskills.io/specification) 的技能集合，可与 Obsidian 配合使用，支持任何兼容 Agent Skills 的代理，包括 Claude Code、Codex 和 Open Code。
>
> 翻译说明：本翻译力求准确传达原项目内容，技能名称、命令、代码块、URL 和文件路径均保持英文原文，以确保技术准确性。
>
> - 原项目链接：[https://github.com/kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)
> - 翻译项目（awesome-skills-cn）：[https://github.com/lxl666666/awesome-skills-cn](https://github.com/lxl666666/awesome-skills-cn)

---

供 Obsidian 使用的 Agent Skills。

这些技能遵循 [Agent Skills 规范](https://agentskills.io/specification)，因此可以被任何兼容技能的代理使用，包括 Claude Code、Codex 和 Open Code。

## 安装

### 应用市场

```
/plugin marketplace add kepano/obsidian-skills
/plugin install obsidian@obsidian-skills
```

### npx skills

```
npx skills add git@github.com:kepano/obsidian-skills.git
```

如果你更倾向于使用 https 而非 ssh：

```
npx skills add https://github.com/kepano/obsidian-skills
```

### 手动安装

#### Claude Code

将此仓库的内容添加到你的 Obsidian 仓库根目录下的 `/.claude` 文件夹中（或你正在与 Claude Code 配合使用的任何文件夹）。更多信息请参阅 [Claude Skills 官方文档](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)。

#### Codex

将 `skills/` 目录复制到你的 Codex skills 路径中（通常是 `~/.codex/skills`）。标准技能格式请参阅 [Agent Skills 规范](https://agentskills.io/specification)。

#### OpenCode

将整个仓库克隆到 OpenCode skills 目录中（`~/.opencode/skills/`）：

```sh
git clone https://github.com/kepano/obsidian-skills.git ~/.opencode/skills/obsidian-skills
```

不要只复制内部的 `skills/` 文件夹 —— 请克隆完整的仓库，以确保目录结构为 `~/.opencode/skills/obsidian-skills/skills/<skill-name>/SKILL.md`。

OpenCode 会自动发现 `~/.opencode/skills/` 下的所有 `SKILL.md` 文件。无需修改 `opencode.json` 或任何配置文件。重启 OpenCode 后，技能即可使用。

## 技能

| 技能 | 描述 |
|-------|-------------|
| [obsidian-markdown](skills/obsidian-markdown) | 创建和编辑 [Obsidian 风格 Markdown](https://help.obsidian.md/obsidian-flavored-markdown)（`.md`），支持维基链接、嵌入、标注、属性及其他 Obsidian 特有语法 |
| [obsidian-bases](skills/obsidian-bases) | 创建和编辑 [Obsidian Bases](https://help.obsidian.md/bases/syntax)（`.base`），支持视图、筛选器、公式和摘要 |
| [json-canvas](skills/json-canvas) | 创建和编辑 [JSON Canvas](https://jsoncanvas.org/) 文件（`.canvas`），支持节点、边、组和连接 |
| [obsidian-cli](skills/obsidian-cli) | 通过 [Obsidian CLI](https://help.obsidian.md/cli) 与 Obsidian 仓库交互，包括插件和主题开发 |
| [defuddle](skills/defuddle) | 使用 [Defuddle](https://github.com/kepano/defuddle-cli) 从网页中提取干净的 Markdown，去除杂乱内容以节省 token |
