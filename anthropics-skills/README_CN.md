# Skills 中文翻译

> 本文档是 [Anthropic Skills](https://github.com/anthropics/skills) 项目的中文翻译版本。

## 关于本翻译

### 原项目介绍

**Anthropic Skills** 是 Anthropic 为 Claude 实现的技能集合。这些技能展示了 Claude 技能系统的各种可能性，涵盖从创意应用（艺术、音乐、设计）到技术任务（Web 应用测试、MCP 服务器生成）再到企业工作流程（沟通、品牌等）。

每个技能都是自包含的，在自己的文件夹中包含 `SKILL.md` 文件，其中包含 Claude 使用的指令和元数据。

### 翻译说明

本翻译包含以下 16 个技能的中文翻译：

- [algorithmic-art/SKILL_CN.md](skills/algorithmic-art/SKILL_CN.md) - 算法艺术生成
- [brand-guidelines/SKILL_CN.md](skills/brand-guidelines/SKILL_CN.md) - 品牌指南
- [canvas-design/SKILL_CN.md](skills/canvas-design/SKILL_CN.md) - Canvas 设计
- [doc-coauthoring/SKILL_CN.md](skills/doc-coauthoring/SKILL_CN.md) - 文档协作
- [docx/SKILL_CN.md](skills/docx/SKILL_CN.md) - Word 文档处理
- [frontend-design/SKILL_CN.md](skills/frontend-design/SKILL_CN.md) - 前端设计
- [internal-comms/SKILL_CN.md](skills/internal-comms/SKILL_CN.md) - 内部沟通
- [mcp-builder/SKILL_CN.md](skills/mcp-builder/SKILL_CN.md) - MCP 服务器开发指南
- [pdf/SKILL_CN.md](skills/pdf/SKILL_CN.md) - PDF 处理
- [pptx/SKILL_CN.md](skills/pptx/SKILL_CN.md) - PowerPoint 处理
- [skill-creator/SKILL_CN.md](skills/skill-creator/SKILL_CN.md) - SKILL 创建指南
- [slack-gif-creator/SKILL_CN.md](skills/slack-gif-creator/SKILL_CN.md) - Slack GIF 创建器
- [theme-factory/SKILL_CN.md](skills/theme-factory/SKILL_CN.md) - 主题工厂
- [web-artifacts-builder/SKILL_CN.md](skills/web-artifacts-builder/SKILL_CN.md) - Web 构建器
- [webapp-testing/SKILL_CN.md](skills/webapp-testing/SKILL_CN.md) - Web 应用测试
- [xlsx/SKILL_CN.md](skills/xlsx/SKILL_CN.md) - Excel 处理

### 原项目链接

- [GitHub 仓库](https://github.com/anthropics/skills)
- [Agent Skills 规范](http://agentskills.io)
- [Claude 技能文档](https://support.claude.com/en/articles/12512176-what-are-skills)

### 翻译项目

本翻译属于 [awesome-skills-cn](https://github.com/lingxling/awesome-skills-cn) 项目的一部分，致力于将优秀的英文 SKILL 翻译成中文。

---

> **注意：** 本仓库包含 Anthropic 为 Claude 实现的技能。有关 Agent Skills 标准的信息，请参阅 [agentskills.io](http://agentskills.io)。

以下为原项目文件README.md的翻译。

---

# Skills

技能是包含指令、脚本和资源的文件夹，Claude 会动态加载这些内容以在专业任务上提高性能。技能教会 Claude 如何以可重复的方式完成特定任务，无论是根据公司的品牌指南创建文档、使用组织的特定工作流程分析数据，还是自动化个人任务。

更多信息，请查看：
- [什么是技能？](https://support.claude.com/en/articles/12512176-what-are-skills)
- [在 Claude 中使用技能](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [如何创建自定义技能](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [使用 Agent Skills 为现实世界配备代理](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

# 关于本仓库

本仓库包含展示 Claude 技能系统可能性的技能。这些技能范围从创意应用（艺术、音乐、设计）到技术任务（测试 Web 应用、MCP 服务器生成）再到企业工作流程（沟通、品牌等）。

每个技能都是自包含的，在自己的文件夹中包含 `SKILL.md` 文件，其中包含 Claude 使用的指令和元数据。浏览这些技能以获取自己技能的灵感或了解不同的模式和方法。

本仓库中的许多技能都是开源的（Apache 2.0）。我们还在 [`skills/docx`](./skills/docx)、[`skills/pdf`](./skills/pdf)、[`skills/pptx`](./skills/pptx) 和 [`skills/xlsx`](./skills/xlsx) 子文件夹中包含了为 [Claude 的文档功能](https://www.anthropic.com/news/create-files)提供支持的文档创建和编辑技能。这些是源代码可用，而非开源，但我们希望与开发者分享这些技能，作为在生产 AI 应用中积极使用的更复杂技能的参考。

## 免责声明

**这些技能仅供演示和教育目的提供。** 虽然其中某些功能可能在 Claude 中可用，但从 Claude 获得的实现和行为可能与这些技能中显示的不同。这些技能旨在说明模式和可能性。在依赖这些技能执行关键任务之前，请始终在自己的环境中彻底测试。

# 技能集合
- [./skills](./skills)：创意与设计、开发与技术、企业与沟通以及文档技能的示例
- [./spec](./spec)：Agent Skills 规范
- [./template](./template)：技能模板

# 在 Claude Code、Claude.ai 和 API 中尝试

## Claude Code
您可以通过在 Claude Code 中运行以下命令将此仓库注册为 Claude Code 插件市场：
```
/plugin marketplace add anthropics/skills
```

然后，要安装特定的技能集：
1. 选择 `Browse and install plugins`
2. 选择 `anthropic-agent-skills`
3. 选择 `document-skills` 或 `example-skills`
4. 选择 `Install now`

或者，直接通过以下方式安装任一插件：
```
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

安装插件后，您只需提及即可使用该技能。例如，如果您从市场安装了 `document-skills` 插件，您可以要求 Claude Code 执行以下操作："使用 PDF 技能从 `path/to/some-file.pdf` 中提取表单字段"

## Claude.ai

这些示例技能在 Claude.ai 的付费计划中已经可用。

要使用此仓库中的任何技能或上传自定义技能，请按照 [在 Claude 中使用技能](https://support.claude.com/en/articles/12512180-using-skills-in-claude#h_a4222fa77b) 中的说明进行操作。

## Claude API

您可以通过 Claude API 使用 Anthropic 的预构建技能并上传自定义技能。有关更多信息，请参阅 [Skills API 快速入门](https://docs.claude.com/en/api/skills-guide#creating-a-skill)。

# 创建基本技能

技能创建很简单 - 只需一个包含 YAML 前置数据和指令的 `SKILL.md` 文件的文件夹。您可以使用此仓库中的 **template-skill** 作为起点：

```markdown
---
name: my-skill-name
description: 对此技能的作用以及何时使用它的清晰描述
---

# My Skill Name

[在此处添加 Claude 在此技能激活时将遵循的指令]

## Examples
- 示例用法 1
- 示例用法 2

## Guidelines
- 指南 1
- 指南 2
```

前置数据只需要两个字段：
- `name` - 技能的唯一标识符（小写，空格用连字符）
- `description` - 对技能的作用以及何时使用它的完整描述

下面的 markdown 内容包含 Claude 将遵循的指令、示例和指南。有关更多详细信息，请参阅 [如何创建自定义技能](https://support.claude.com/en/articles/12512198-creating-custom-skills)。

# 合作伙伴技能

技能是教 Claude 更好地使用特定软件的好方法。当我们看到来自合作伙伴的优秀示例技能时，我们可能会在这里重点介绍其中一些：

- **Notion** - [Notion Skills for Claude](https://www.notion.so/notiondevs/Notion-Skills-for-Claude-28da4445d27180c7af1df7d8615723d0)

---

## 原项目文档

如需查看原项目的完整英文文档，请访问：

- [README.md (英文原版)](README.md) - 原项目的完整说明文档

原项目由 [Anthropic](https://github.com/anthropics) 维护。
