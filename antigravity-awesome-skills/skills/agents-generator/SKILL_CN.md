---
name: agents-generator
description: "通过分析代码库来生成项目专属的 AGENTS.md 及配套规则。支持完整、最简、更新和试运行(dry-run)模式,具备包管理器检测、monorepo 支持、备份、受管理区块、置信度评分以及命令验证能力。"
category: developer-tools
risk: critical
source: https://github.com/OJPalenzuela/agents-generator/tree/7a3201208a01bd25e69ad11e665efc1392f5356a
source_repo: OJPalenzuela/agents-generator
source_type: community
date_added: "2026-08-02"
author: OJPalenzuela
tags: [agents-md, project-conventions, developer-tools, codebase-analysis, ai-agents]
tools: [claude, cursor, copilot, opencode, codex, gemini]
license: MIT
license_source: https://github.com/OJPalenzuela/agents-generator/blob/7a3201208a01bd25e69ad11e665efc1392f5356a/LICENSE
allowed-tools: Read Write Edit Bash(ls:*) Bash(git:*) Bash(tree:*) Bash(find:*) Grep Glob WebFetch
metadata:
  author: OJPalenzuela
  version: "1.2.3"
---

# Skill: agents-generator

> [!WARNING]
> **【仅限授权使用】** 此技能会在目标项目中写入或更新 `AGENTS.md`、`.agents/rules/`、可选的平台专用指令文件,以及带时间戳的备份。请先阅读检测到的输入和拟议的输出,在更改目标文件前获取批准,并仅在用户预期的项目范围内使用此技能。

## 何时使用

当用户想要以下操作时使用此技能:

- 创建一份完整的、项目专属的 `AGENTS.md`,而不是泛泛的智能体规则;
- 为检测到的框架、测试、数据库、样式方案或 monorepo 的各个子包生成配套规则;
- 创建一份最简的 `AGENTS.md`、预览改动而不实际写入,或在技术栈变更后更新现有指令。

不要用它在未检查目标项目的情况下凭空编造约定、覆盖用户授权范围之外的指令,或把生成的指导当作人工审查的替代品。

为目标项目生成量身定制的 AGENTS.md + `.agents/rules/*.md`——不是带占位符的模板,而是一份与项目真实工具链相匹配的活文档。

## 你将得到什么

对于一个使用 **Bun + Next.js 16 + Tailwind + Vitest + Server Actions** 的项目,此技能会生成:

```
AGENTS.md
├── 安装命令: bun install, bun dev, bun run test:run, bun doctor
├── 验证流程: bunx tsc --noEmit → bun run lint → bun run test:run → bun doctor
├── 约定: "始终使用 Bun。使用纯 TypeScript 类型 + 守卫。"
└── 架构 → .agents/rules/architecture.md

.agents/rules/
├── architecture.md       ← 带真实目录和确切版本号的 ASCII 图
├── frontend-patterns.md  ← 组件规则、状态存放位置、信任边界
├── server-actions.md     ← downloadVideo() 流程、DownloadResult 类型、限流器
├── testing.md            ← "5 个文件中共 74 个测试"、vitest 命令、mock 模式
├── git-workflow.md       ← Conventional Commits 规范、pre-commit 检查
└── sdd-workflow.md       ← 预检默认值、应用后验证
```

未生成的规则:`backend.md`(没有 NestJS)、`database.md`(没有 ORM)、`i18n.md`(硬编码西班牙语)、`forms.md`(手动输入)、`styling.md`(Tailwind 已包含在前端规则中)。

## 激活合约

为目标项目生成 AGENTS.md + `.agents/rules/*.md`。绝不要猜测——先阅读项目的实际文件。

### 模式选择

| 用户说 | 模式 | 输出 |
|-----------|------|------|
| "simple AGENTS.md"、"just the basics"、"minimal" | **最简(Minimal)** | 单一 `AGENTS.md`(约 30 行,没有规则文件) |
| "full AGENTS.md"、"with rules"、"complete",或默认 | **完整(Full)** | `AGENTS.md` + `.agents/rules/*.md` |
| "update AGENTS.md"、"refresh"、"my stack changed" | **更新(Update)** | 比对现有内容,只重新生成有变化的部分 |

### 试运行模式

如果用户要求"预览"、"展示会有什么变化"、"dry-run":运行全部检测流程,但**不要**写入文件。展示检测摘要、将会创建的文件、被跳过的规则,以及示例输出。

## 硬性规则

- **先读后写,但绝不读取密钥。** 在生成任何内容之前,先阅读 `package.json`、非密钥配置文件和目录结构。绝不打开 `.env`、`.env.local`、凭据存储区,或其他类似的携带密钥的文件。环境变量名仅从 `.env.example` 中的占位符以及诸如 `process.env.NAME` 的源码引用中推导,不读取也不报告其值。
- **首先检测包管理器。** 检查锁文件:`bun.lock`→bun,`pnpm-lock.yaml`→pnpm,`package-lock.json`→npm,`yarn.lock`→yarn。绝不默认使用 npm。每条命令都使用检测到的包管理器。
- **只生成适用的内容。** 纯前端项目不生成后端规则。没有 ORM 不生成数据库规则。
- **默认不执行项目脚本。** 包管理器脚本是仓库控制的 shell 入口点。检测并记录候选的格式化/lint 命令,但除非用户在审查过确切的脚本内容和被调用的工具之后另行请求执行,否则不要运行它们。
- **验证命令。** 输出中的每条命令都必须作为 `package.json` 中的脚本键存在。
- **不留占位符。** 扫描输出中是否残留 `{{`、`TODO`、`add here`、`...`。若有残留则拒绝输出。
- **先备份。** 如果文件已存在,将其复制到带时间戳的 `.agents/backups/`。

## 执行步骤

### 通用步骤

1. `git rev-parse --show-toplevel` → 项目根目录。
2. **首先检测包管理器**:检查锁文件。`bun.lock`→bun,`pnpm-lock.yaml`→pnpm,`package-lock.json`→npm,`yarn.lock`→yarn。绝不默认使用 npm。
3. 阅读 `package.json`(脚本、依赖、工作区)。保存脚本信息用于后续验证。
4. 阅读非密钥配置文件,并探索目录结构。排除除仅含占位符的 `.env.example` 之外的所有 `.env*` 文件;绝不读取密钥值。
5. 选择模式(如有歧义则询问)。

### 完整模式

1. 阅读 `assets/agents-full.md`——这是包含所有章节和填充规则的 AGENTS.md 结构。
2. 阅读项目文件,用真实数据填充每一个占位符。绝不使用泛泛的文字。
3. 在项目根目录生成 `AGENTS.md`。将内容包裹在 `<!-- AGENTS-GENERATED-START -->` / `<!-- AGENTS-GENERATED-END -->` 之间。
4. 对每个适用的规则类别,从 `assets/` 读取对应模板,并在 `.agents/rules/` 中生成对应的规则文件。
5. 如果检测到 Claude(存在 `.claude/` 或 `CLAUDE.md`):从 `assets/claude.md` 生成精简版的 `CLAUDE.md`。
6. 如果检测到平台文件:从 `assets/platform.md` 生成。

### 最简模式

1. 阅读 `assets/agents-minimal.md`——30 行的 agents.md 标准格式。
2. 生成单一的 `AGENTS.md`。

### 更新模式

1. 备份现有文件。
2. 重新检测项目状态。
3. 比对新旧版本。只重新生成发生变化的类别。

### 生成后处理

- 将检测到的 `[format cmd]` 和 `[lint cmd]` 报告为未执行的候选命令。不要自动运行其中任何一个;仅在用户另行授权且已审查过其确切的、受项目控制的脚本内容之后才执行。
- 扫描是否存在 `{{`、`TODO`、`...`。如有则修复。
- 验证所有命令都存在于 package.json 的脚本中。
- 如果 AGENTS.md 超过 300 行,发出警告。如果超过 500 行,将内容移至规则文件。
- 在宣告完成之前,使用 Conventional Commits 格式总结所有更改。
- 报告:检测到了什么、生成了什么、跳过了什么,以及置信度评分。

## 输出合约

返回:
- 使用的模式及原因
- 已创建/修改的文件
- 检测摘要(所有类别)
- 已生成和已跳过的规则(附原因)
- 置信度评分

## 局限性

- 生成的指令是提案,在被采纳或提交之前需要人工审查。
- 命令验证仅限于目标项目中可见的脚本和文件;无法证明工具、服务或平台专属命令在每个环境中都能正常工作。
- 项目提供的包脚本是不受信任的可执行代码。生成和记录某个脚本并不授权运行它。
- 此技能不授权在预期项目范围之外进行写入,也不能替代项目专属的安全、构建或部署审查。

## 参考资料

| 优先级 | 文件 | 用途 |
|----------|------|------|
| **必需** | `assets/agents-full.md` | 包含全部 25+ 个章节及填充规则的完整 AGENTS.md 模板 |
| **必需** | `assets/agents-minimal.md` | 30 行的 agents.md 标准模板 |
| 完整模式 | `assets/architecture.md` | 架构规则模板 |
| 完整模式 | `assets/frontend-patterns.md` | 前端模式模板 |
| 完整模式 | `assets/server-actions.md` | Server Actions / 后端模板 |
| 完整模式 | `assets/testing.md` | 测试策略模板 |
| 完整模式 | `assets/git-workflow.md` | Git 工作流模板 |
| 完整模式 | `assets/sdd-workflow.md` | SDD 工作流模板 |
| 完整模式 | `assets/styling.md` | 样式规则模板 |
| 完整模式 | `assets/forms.md` | 表单模式模板 |
| 完整模式 | `assets/database.md` | 数据库规则模板 |
| 完整模式 | `assets/i18n.md` | i18n 规则模板 |
| 完整模式 | `assets/backend.md` | 后端/NestJS 模板 |
| 条件生成 | `assets/claude.md` | CLAUDE.md —— 仅在检测到 Claude 时生成 |
| 条件生成 | `assets/platform.md` | 多平台文件 |
| 条件生成 | `assets/agents-nested.md` | Monorepo 嵌套 AGENTS.md |
| 参考 | `references/decision-matrix.md` | 完整的检测逻辑与边界情况 |
| 参考 | `references/example-output/README.md` | 质量基准 |
| 参考 | `references/template-filling-guide.md` | 占位符填充规则 |
