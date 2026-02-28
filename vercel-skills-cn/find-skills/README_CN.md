# Skills CLI 中文翻译

这是 [Vercel Skills CLI](https://github.com/vercel-labs/skills) 的中文翻译版本。

## 原项目简介

Skills CLI 是开放代理技能生态系统的命令行工具，用于管理 AI 编程助手的技能包。它支持多种 AI 编程助手，包括 Claude Code、Cursor、OpenCode、Codex 等 40+ 种工具。

## 本翻译项目说明

本项目将 Skills CLI 的核心技能文档翻译成中文，帮助中文用户更好地理解和使用这些技能。

### 翻译内容

- `skills/find-skills/SKILL.md` - 技能发现与安装指南的中文翻译

### 翻译原则

- 保持技术术语的准确性
- 使用简洁明了的中文表达
- 保留原文档的结构和格式
- 命令示例保持原样（不翻译命令）

## 如何使用

### 1. 安装 Skills CLI

```bash
npx skills add vercel-labs/agent-skills
```

### 2. 查找技能

```bash
# 交互式搜索
npx skills find

# 关键词搜索
npx skills find typescript
```

### 3. 安装技能

```bash
# 安装特定技能
npx skills add vercel-labs/agent-skills --skill frontend-design

# 全局安装
npx skills add vercel-labs/agent-skills -g

# 安装到特定代理
npx skills add vercel-labs/agent-skills -a claude-code
```

### 4. 查看已安装技能

```bash
npx skills list
```

### 5. 更新技能

```bash
# 检查更新
npx skills check

# 更新所有技能
npx skills update
```

### 6. 移除技能

```bash
npx skills remove web-design-guidelines
```

## 主要功能

### 技能管理

- **安装**: 从 GitHub 或其他来源安装技能包
- **查找**: 交互式搜索或关键词搜索技能
- **列表**: 查看已安装的技能
- **更新**: 更新技能到最新版本
- **移除**: 从代理中移除技能
- **创建**: 创建新的技能模板

### 支持的代理

Skills CLI 支持 40+ 种 AI 编程助手，包括：
- Claude Code
- Cursor
- OpenCode
- Codex
- Cline
- Trae
- Windsurf
- GitHub Copilot
- 等等...

## 技能是什么？

技能是可重用的指令集，用于扩展你的 AI 编程助手的能力。技能定义在 `SKILL.md` 文件中，包含 YAML 前置数据（frontmatter）和说明文档。

技能可以让代理执行专业任务，例如：
- 从 git 历史生成发布说明
- 按照团队约定创建 PR
- 与外部工具集成（Linear、Notion 等）

## 相关资源

- [原项目 GitHub](https://github.com/vercel-labs/skills)
- [技能目录](https://skills.sh)
- [代理技能规范](https://agentskills.io)
- [Vercel 技能仓库](https://github.com/vercel-labs/agent-skills)

## 许可证

MIT License（与原项目相同）

## 贡献

欢迎提交翻译改进建议和错误修正！
