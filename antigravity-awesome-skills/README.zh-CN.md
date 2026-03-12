<!-- registry-sync: version=7.1.0; skills=1272; stars=21225; updated_at=2026-03-07T11:47:20+00:00 -->
# 🌌 Antigravity Awesome Skills: 1,272+ 通用代理技能 适用于 Claude Code、Gemini CLI、Cursor、Copilot 及更多

> **面向AI编码助手的1,272+通用代理技能终极集合 — Claude Code、Gemini CLI、Codex CLI、Antigravity IDE、GitHub Copilot、Cursor、OpenCode、AdaL**

[![GitHub stars](https://img.shields.io/badge/⭐%2021%2C000%20Stars-old?style=for-the-badge)](https://github.com/sickn33/antigravity-awesome-skills/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Anthropic-purple)](https://claude.ai)
[![Gemini CLI](https://img.shields.io/badge/Gemini%20CLI-Google-blue)](https://github.com/google-gemini/gemini-cli)
[![Codex CLI](https://img.shields.io/badge/Codex%20CLI-OpenAI-green)](https://github.com/openai/codex)
[![Kiro](https://img.shields.io/badge/Kiro-AWS-orange)](https://kiro.dev)
[![Cursor](https://img.shields.io/badge/Cursor-AI%20IDE-orange)](https://cursor.sh)
[![Copilot](https://img.shields.io/badge/GitHub%20Copilot-VSCode-lightblue)](https://github.com/features/copilot)
[![OpenCode](https://img.shields.io/badge/OpenCode-CLI-gray)](https://github.com/opencode-ai/opencode)
[![Antigravity](https://img.shields.io/badge/Antigravity-DeepMind-red)](https://github.com/sickn33/antigravity-awesome-skills)
[![AdaL CLI](https://img.shields.io/badge/AdaL%20CLI-SylphAI-pink)](https://sylph.ai/)
[![ASK Supported](https://img.shields.io/badge/ASK-Supported-blue)](https://github.com/yeasy/ask)
[![Web App](https://img.shields.io/badge/Web%20App-Browse%20Skills-blue)](apps/web-app)
[![Buy Me a Book](https://img.shields.io/badge/Buy%20me%20a-book-d13610?logo=buymeacoffee&logoColor=white)](https://buymeacoffee.com/sickn33)

🌟 **21,000+ GitHub Stars Milestone！** 感谢社区将此项目转变为同类最大技能库之一！

**Antigravity Awesome Skills** 是一个精选、经过实战检验的**1,272+高性能代理技能**库，旨在与所有主要AI编码助手无缝协作：

- 🟣 **Claude Code** (Anthropic CLI)
- 🔵 **Gemini CLI** (Google DeepMind)
- 🟢 **Codex CLI** (OpenAI)
- 🟠 **Kiro CLI** (AWS)
- 🟠 **Kiro IDE** (AWS)
- 🔴 **Antigravity IDE** (Google DeepMind)
- 🩵 **GitHub Copilot** (VSCode扩展)
- 🟠 **Cursor** (AI原生IDE)
- ⚪ **OpenCode** (开源CLI)
- 🌸 **AdaL CLI** (自我进化编码代理)

此仓库提供了将您的AI助手转变为**全栈数字代理**的基本技能，包括来自**Anthropic**、**OpenAI**、**Google**、**Microsoft**、**Supabase**、**Apify**和**Vercel Labs**的官方功能。

## 目录

- [🚀 新手？从这里开始！](#新手从这里开始)
- [📖 完整使用指南](docs_zh-CN/USAGE.md) - **如果安装后感到困惑，从这里开始！**
- [🔌 兼容性与调用方式](#兼容性与调用方式)
- [🛠️ 安装](#安装)
- [🧯 故障排除](#故障排除)
- [🎁 精选集合（包）](#精选集合)
- [🧭 Antigravity工作流](#antigravity工作流)
- [📦 功能与分类](#功能与分类)
- [📚 浏览1,272+技能](#浏览1272技能)
- [🤝 如何贡献](#如何贡献)
- [💬 社区](#社区)
- [☕ 支持项目](#支持项目)
- [🏆 致谢与来源](#致谢与来源)
- [👥 仓库贡献者](#仓库贡献者)
- [⚖️ 许可证](#许可证)
- [🌟 Star历史](#star历史)

---

## 新手？从这里开始！

**欢迎来到V7.1.0交互式网络版。**这不仅仅是一个脚本列表；它是您的AI代理的完整操作系统。

### 1. 🐣 背景：这是什么？

**Antigravity Awesome Skills** (Release 7.1.0) 是对AI能力的巨大升级。

AI代理（如Claude Code、Cursor或Gemini）很智能，但它们缺乏**特定工具**。它们不知道您公司的"部署协议"或"AWS CloudFormation"的特定语法。
**技能**是小型markdown文件，可以教它们如何完美地完成这些特定任务，每次都如此。

### 2. ⚡️ 快速开始（1分钟）

安装一次；然后使用[docs_zh-CN/BUNDLES.md](docs_zh-CN/BUNDLES.md)中的入门包来专注于您的角色。

1. **安装**：

   ```bash
   # 默认：~/.gemini/antigravity/skills (Antigravity全局)。使用--path指定其他位置。
   npx antigravity-awesome-skills
   ```

2. **验证**：

   ```bash
   test -d ~/.gemini/antigravity/skills && echo "技能已安装在 ~/.gemini/antigravity/skills"
   ```

3. **运行您的第一个技能**：

   > "使用**@brainstorming**来规划SaaS MVP。"

4. **选择一个包**：
    - **Web开发？**从`Web 向导`开始。
    - **安全？**从`Security Engineer`开始。
   - **通用使用？**从`基础`开始。

### 3. 🧠 如何使用

安装完成后，只需自然地询问您的代理：

> "使用**@brainstorming**技能帮我规划SaaS。"
> "在这个文件上运行**@lint-and-validate**。"

👉 **新功能：**[**完整使用指南 - 先读这个！**](docs_zh-CN/USAGE.md)（答案："安装后我该做什么？"、"我如何执行技能？"、"提示词应该是什么样的？"）

👉 **[完整入门指南](docs_zh-CN/GETTING_STARTED.md)**

---

## 兼容性与调用方式

这些技能遵循通用的**SKILL.md**格式，适用于任何支持代理技能的AI编码助手。

| 工具            | 类型 | 调用示例                      | 路径                                                                   |
| :-------------- | :--- | :---------------------------- | :--------------------------------------------------------------------- |
| **Claude Code** | CLI  | `>> /skill-name 帮我...`     | `.claude/skills/`                                                        |
| **Gemini CLI**  | CLI  | `(用户提示) 使用skill-name...` | `.gemini/skills/`                                                        |
| **Codex CLI**   | CLI  | `(用户提示) 使用skill-name...` | `.codex/skills/`                                                         |
| **Kiro CLI**    | CLI  | `(自动) 按需加载技能`        | 全局：`~/.kiro/skills/` · 工作区：`.kiro/skills/`                         |
| **Kiro IDE**    | IDE  | `/skill-name 或 (自动)`        | 全局：`~/.kiro/skills/` · 工作区：`.kiro/skills/`                         |
| **Antigravity** | IDE  | `(代理模式) 使用skill...`     | 全局：`~/.gemini/antigravity/skills/` · 工作区：`.agent/skills/`        |
| **Cursor**      | IDE  | `@skill-name (在聊天中)`      | `.cursor/skills/`                                                         |
| **Copilot**     | 扩展 | `(手动粘贴内容)`             | 不适用用                                                                   |
| **OpenCode**    | CLI  | `opencode run @skill-name`    | `.agents/skills/`                                                         |
| **AdaL CLI**    | CLI  | `(自动) 按需加载技能`        | `.adal/skills/`                                                           |

> [!TIP]
> **默认安装路径**：`~/.gemini/antigravity/skills` (Antigravity全局)。使用`--path ~/.agent/skills`进行工作区特定安装。对于手动克隆，`.agent/skills/`可作为Antigravity的工作区路径。
> **OpenCode路径更新**：opencode路径已更改为`.agents/skills`作为全局技能。请参见OpenCode文档上的[放置文件](https://opencode.ai/docs/skills/#place-files)指令。

> [!WARNING]
> **Windows用户**：此仓库为官方技能使用**符号链接**。
> 有关确切的修复方法，请参见[故障排除](#故障排除)。

---

## 安装

要在**Claude Code**、**Gemini CLI**、**Codex CLI**、**Kiro CLI**、**Kiro IDE**、**Cursor**、**Antigravity**、**OpenCode**或**AdaL**中使用这些技能：

### 选项A：npx（推荐）

```bash
npx antigravity-awesome-skills

# Antigravity（明确；与默认相同）
npx antigravity-awesome-skills --antigravity

# Kiro CLI/IDE（全局）
npx antigravity-awesome-skills --path ~/.kiro/skills

# Kiro CLI/IDE（工作区）
npx antigravity-awesome-skills --path .kiro/skills

# Cursor
npx antigravity-awesome-skills --cursor

# Claude Code
npx antigravity-awesome-skills --claude

# Gemini CLI
npx antigravity-awesome-skills --gemini

# Codex CLI
npx antigravity-awesome-skills --codex

# Kiro CLI
npx antigravity-awesome-skills --kiro

# OpenCode
npx antigravity-awesome-skills --path .agents/skills

# AdaL CLI
npx antigravity-awesome-skills --path .adal/skills

# 工作区特定（例如Antigravity工作区的.agent/skills）
npx antigravity-awesome-skills --path ~/.agent/skills

# 自定义路径
npx antigravity-awesome-skills --path ./my-skills
```

运行`npx antigravity-awesome-skills --help`查看所有选项。如果目录已存在，安装程序会运行`git pull`来更新。

### 选项B：git克隆

如果不使用`--path`，npx安装程序使用`~/.gemini/antigravity/skills`。对于手动克隆或不同路径（例如工作区`.agent/skills`），使用以下方法之一：

```bash
# Antigravity全局（匹配npx默认）
git clone https://github.com/sickn33/antigravity-awesome-skills.git ~/.gemini/antigravity/skills

# 工作区特定（例如项目中的.agent/skills）
git clone https://github.com/sickn33/antigravity-awesome-skills.git .agent/skills

# Kiro CLI/IDE全局
git clone https://github.com/sickn33/antigravity-awesome-skills.git ~/.kiro/skills

# Claude Code特定
git clone https://github.com/sickn33/antigravity-awesome-skills.git .claude/skills

# Gemini CLI特定
git clone https://github.com/sickn33/antigravity-awesome-skills.git .gemini/skills

# Codex CLI特定
git clone https://github.com/sickn33/antigravity-awesome-skills.git .codex/skills

# Cursor特定
git clone https://github.com/sickn33/antigravity-awesome-skills.git .cursor/skills

# OpenCode
git clone https://github.com/sickn33/antigravity-awesome-skills.git .agents/skills

# AdaL CLI特定
git clone https://github.com/sickn33/antigravity-awesome-skills.git .adal/skills
```

### 选项C：Kiro IDE导入（GUI）

对于Kiro IDE用户，您可以直接导入单个技能：

1. 在Kiro IDE中打开**Agent Steering & Skills**面板
2. 点击**+** → **导入技能** → **GitHub**
3. 粘贴技能URL：`https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/[skill-name]`
4. 示例：`https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/aws-cost-optimizer`

> **注意**：这一次只导入一个技能。对于批量安装，请使用上面的选项A或B。

---

## 故障排除

### `npx antigravity-awesome-skills`返回404

使用GitHub包回退：

```bash
npx github:sickn33/antigravity-awesome-skills
```

### Windows克隆问题（符号链接）

此仓库为官方技能使用符号链接。启用开发者模式或以管理员身份运行Git，然后使用以下方式克隆：

```bash
git clone -c core.symlinks=true https://github.com/sickn33/antigravity-awesome-skills.git .agent/skills
```

### 技能已安装但工具未检测到

安装到工具特定路径。使用安装程序标志：`--antigravity`（默认）、`--claude`、`--gemini`、`--codex`、`--cursor`或`--path <dir>`用于自定义位置（例如Antigravity工作区的`~/.agent/skills`）。

### 更新现有安装

**好消息！**您不再需要手动运行`git pull`或`npx antigravity-awesome-skills`来更新您的技能。

- **Windows：**双击**`START_APP.bat`**（或在终端中运行）。
- **macOS/Linux：**从仓库根目录运行`cd web-app && npm run app:dev`。

两种方法每次打开Web应用时都会自动从原始仓库获取并合并最新技能，确保您始终拥有最新的目录。

### 从头重新安装

```bash
rm -rf ~/.gemini/antigravity/skills
npx antigravity-awesome-skills
```

---

## 精选集合

**包**是针对特定角色或目标（例如：`Web Wizard`、`Security Engineer`、`OSS Maintainer`）的精选技能组。

它们帮助您避免从950+技能中逐个选择。

### ⚠️ 重要：包不是单独的安装！

**常见困惑**："我需要单独安装每个包吗？"

**答案：不需要！**以下是包的实际内容：

**包是什么：**

- ✅ 按角色组织的推荐技能列表
- ✅ 帮助您决定使用什么的精选起点
- ✅ 发现相关技能的省时快捷方式

**包不是什么：**

- ❌ 单独的安装或下载
- ❌ 不同的git命令
- ❌ 需要您"激活"的东西

### 如何使用包：

1. **安装仓库一次**（您已经拥有所有技能）
2. **浏览[docs_zh-CN/BUNDLES.md](docs_zh-CN/BUNDLES.md)中的包**来找到您的角色
3. **从该包中选择3-5个技能**开始在提示中使用
4. **在与AI的对话中引用它们**（例如，"使用@brainstorming..."）

有关如何实际使用技能的详细示例，请参见[**使用指南**](docs_zh-CN/USAGE.md)。

### 示例：

- 构建SaaS MVP：`Essentials` + `Full-Stack Developer` + `QA & Testing`。
- 加固生产环境：`Security Developer` + `DevOps & Cloud` + `Observability & Monitoring`。
- 发布OSS变更：`Essentials` + `OSS Maintainer`。

## Antigravity工作流

包帮助您选择技能。工作流帮助您按顺序执行它们。

- 当您需要按角色获取推荐时使用包。
- 当您需要为实现具体目标而逐步执行时使用工作流。

从这里开始：

- [docs_zh-CN/WORKFLOWS.md](docs_zh-CN/WORKFLOWS.md)：人类可读的剧本。
- [data/workflows.json](data/workflows.json)：机器可读的工作流元数据。

初始工作流包括：

- 发布SaaS MVP
- Web应用安全审计
- 构建AI代理系统
- QA和浏览器自动化（可选的`@go-playwright`支持Go堆栈）

## 功能与分类

仓库被组织成专业领域，将您的AI转变为整个软件开发生命周期的专家：

| 分类       | 重点                                              | 示例技能                                                                  |
| :------------- | :------------------------------------------------- | :------------------------------------------------------------------------------ |
| 架构   | 系统设计、ADR、C4和可扩展模式     | `architecture`, `c4-context`, `senior-architect`                                |
| 商业       | 增长、定价、CRO、SEO和进入市场        | `copywriting`, `pricing-strategy`, `seo-audit`                                  |
| 数据与AI      | LLM应用、RAG、代理、可观测性、分析    | `rag-engineer`, `prompt-engineer`, `langgraph`                                  |
| 开发    | 语言精通、框架模式、代码质量 | `typescript-expert`, `python-patterns`, `react-patterns`                        |
| 通用        | 规划、文档、产品运营、写作、指南   | `brainstorming`, `doc-coauthoring`, `writing-plans`                             |
| 基础设施 | DevOps、云、无服务器、部署、CI/CD       | `docker-expert`, `aws-serverless`, `vercel-deployment`                          |
| 安全       | 应用安全、渗透测试、漏洞分析、合规      | `api-security-best-practices`, `sql-injection-testing`, `vulnerability-scanner` |
| 测试        | TDD、测试设计、修复、QA工作流              | `test-driven-development`, `testing-patterns`, `test-fixing`                    |
| 工作流       | 自动化、编排、作业、代理            | `workflow-automation`, `inngest`, `trigger-dev`                                 |

计数随着新技能的添加而变化。有关当前完整注册表，请参见[CATALOG.md](CATALOG.md)。


## 浏览1,272+技能

- 在[`apps/web-app`](apps/web-app)中打开交互式浏览器。
- 阅读完整目录：[`CATALOG.md`](CATALOG.md)。
- 从[`docs_zh-CN/users/bundles.md`](docs_zh-CN/users/bundles.md)中的基于角色的包开始。
- 遵循[`docs_zh-CN/users/workflows.md`](docs_zh-CN/users/workflows.md)中以结果为导向的工作流。
- 使用[`docs_zh-CN/users/getting-started.md`](docs_zh-CN/users/getting-started.md)和[`docs_zh-CN/users/usage.md`](docs_zh-CN/users/usage.md)中的入门指南。

## 文档

| 面向用户                                                        | 面向贡献者                                                           | 面向维护者                                                                      |
| ---------------------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [`docs_zh-CN/users/getting-started.md`](docs_zh-CN/users/getting-started.md) | [`CONTRIBUTING.md`](CONTRIBUTING.md)                                       | [`docs_zh-CN/maintainers/release-process.md`](docs_zh-CN/maintainers/release-process.md)         |
| [`docs_zh-CN/users/usage.md`](docs_zh-CN/users/usage.md)                     | [`docs_zh-CN/contributors/skill-anatomy.md`](docs_zh-CN/contributors/skill-anatomy.md) | [`docs_zh-CN/maintainers/audit.md`](docs_zh-CN/maintainers/audit.md)                             |
| [`docs_zh-CN/users/faq.md`](docs_zh-CN/users/faq.md)                         | [`docs_zh-CN/contributors/quality-bar.md`](docs_zh-CN/contributors/quality-bar.md)     | [`docs_zh-CN/maintainers/ci-drift-fix.md`](docs_zh-CN/maintainers/ci-drift-fix.md)               |
| [`docs_zh-CN/users/visual-guide.md`](docs_zh-CN/users/visual-guide.md)       | [`docs_zh-CN/contributors/examples.md`](docs_zh-CN/contributors/examples.md)           | [`docs_zh-CN/maintainers/skills-update-guide.md`](docs_zh-CN/maintainers/skills-update-guide.md) |

## Web应用

Web应用是导航如此大型仓库的最快方式。

**本地运行：**

```bash
npm run app:install
npm run app:dev
```

这会将生成的技能索引复制到`apps/web-app/public/skills.json`，将当前的`skills/`目录树镜像到`apps/web-app/public/skills/`，并启动Vite开发服务器。

**在线托管：**相同的应用可在[https://sickn33.github.io/antigravity-awesome-skills/](https://sickn33.github.io/antigravity-awesome-skills/)获得，并在每次推送到`main`时自动部署。要启用一次：**Settings → Pages → Build and deployment → Source: GitHub Actions**。



## 贡献

- 在`skills/<skill-name>/SKILL.md`下添加新技能。
- 遵循[`CONTRIBUTING.md`](CONTRIBUTING.md)中的贡献者指南。
- 使用[`docs_zh-CN/contributors/skill-template.md`](docs_zh-CN/contributors/skill-template.md)中的模板。
- 在打开PR之前使用`npm run validate`进行验证。

## 社区

- [Discussions](https://github.com/sickn33/antigravity-awesome-skills/discussions)用于提问和反馈。
- [Issues](https://github.com/sickn33/antigravity-awesome-skills/issues)用于错误报告和改进请求。
- [`SECURITY.md`](SECURITY.md)用于安全报告。

---

## 支持项目

支持是可选的。这个项目对每个人保持免费和开源。

- [☕ 在Buy Me a Coffee上给原作者买本书](https://buymeacoffee.com/sickn33)
- Star仓库。
- 提出清晰、可重现的问题。
- 提交PR（技能、文档、修复）。

---

## 致谢与来源

我们站在巨人的肩膀上。

👉 **[查看完整归属账本](docs_zh-CN/SOURCES.md)**

主要贡献者和来源包括：

- **HackTricks**
- **OWASP**
- **Anthropic / OpenAI / Google**
- **开源社区**

如果没有Claude Code社区和官方来源的不可思议工作，这个集合是不可能的：

### 官方来源

- **[anthropics/skills](https://github.com/anthropics/skills)**：官方Anthropic技能仓库 - 文档操作（DOCX、PDF、PPTX、XLSX）、品牌指南、内部通信。
- **[anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks)**：与Claude一起构建的官方笔记本和食谱。
- **[remotion-dev/skills](https://github.com/remotion-dev/skills)**：官方Remotion技能 - React中视频创作，具有28个模块化规则。
- **[vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)**：Vercel Labs官方技能 - React最佳实践、Web设计指南。
- **[openai/skills](https://github.com/openai/skills)**：OpenAI Codex技能目录 - 代理技能、技能创建者、简洁规划。
- **[supabase/agent-skills](https://github.com/supabase/agent-skills)**：Supabase官方技能 - Postgres最佳实践。
- **[microsoft/skills](https://github.com/microsoft/skills)**：官方Microsoft技能 - Azure云服务、Bot Framework、认知服务，以及跨.NET、Python、TypeScript、Go、Rust和Java的企业开发模式。
- **[google-gemini/gemini-skills](https://github.com/google-gemini/gemini-skills)**：官方Gemini技能 - Gemini API、SDK和模型交互。
- **[apify/agent-skills](https://github.com/apify/agent-skills)**：官方Apify技能 - Web抓取、数据提取和自动化。

### 社区贡献者

- **[rmyndharis/antigravity-skills](https://github.com/rmyndharis/antigravity-skills)**：贡献了300+企业技能和目录生成逻辑。
- **[amartelr/antigravity-workspace-manager](https://github.com/amartelr/antigravity-workspace-manager)**：官方工作区管理器CLI配套工具，用于跨无限本地开发环境动态自动配置技能子集。
- **[obra/superpowers](https://github.com/obra/superpowers)**：Jesse Vincent的原始"Superpowers"。
- **[guanyang/antigravity-skills](https://github.com/guanyang/antigravity-skills)**：核心Antigravity扩展。
- **[diet103/claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase)**：基础设施和后端/前端指南。
- **[ChrisWiles/claude-code-showcase](https://github.com/ChrisWiles/claude-code-showcase)**：React UI模式和设计系统。
- **[travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)**：Loki模式和Playwright集成。
- **[zebbern/claude-code-guide](https://github.com/zebbern/claude-code-guide)**：综合安全套件和指南（约60个新技能的来源）。
- **[alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)**：高级工程和PM工具包。
- **[karanb192/awesome-claude-skills](https://github.com/karanb192/awesome-claude-skills)**：Claude Code的大量已验证技能列表。
- **[VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)**：精选的61个高质量技能集合，包括来自Sentry、Trail of Bits、Expo、Hugging Face的官方团队技能和综合上下文工程套件（v4.3.0集成）。
- **[zircote/.claude](https://github.com/zircote/.claude)**：Shopify开发技能参考。
- **[vibeforge1111/vibeship-spawner-skills](https://github.com/vibeforge1111/vibeship-spawner-skills)**：AI代理、集成、制作工具（57个技能，Apache 2.0）。
- **[coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills)**：用于CRO、文案、SEO、付费广告和增长的营销技能（23个技能，MIT）。
- **[Silverov/yandex-direct-skill](https://github.com/Silverov/yandex-direct-skill)**：Yandex Direct（API v5）广告审计技能 — 55个自动检查，A-F评分，俄罗斯PPC市场的活动/广告/关键词分析（MIT）。
- **[vudovn/antigravity-kit](https://github.com/vudovn/antigravity-kit)**：AI代理模板，包含技能、代理和工作流（33个技能，MIT）。
- **[affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code)**：来自Anthropic黑客马拉松获胜者的完整Claude Code配置集合 - 仅技能（8个技能，MIT）。
- **[whatiskadudoing/fp-ts-skills](https://github.com/whatiskadudoing/fp-ts-skills)**：TypeScript的实用fp-ts技能 – fp-ts-pragmatic、fp-ts-react、fp-ts-errors（v4.4.0）。
- **[webzler/agentMemory](https://github.com/webzler/agentMemory)**：agent-memory-mcp技能的来源。
- **[sstklen/claude-api-cost-optimization](https://github.com/sstklen/claude-api-cost-optimization)**：通过智能优化策略节省50-90%的Claude API成本（MIT）。
- **[Wittlesus/cursorrules-pro](https://github.com/Wittlesus/cursorrules-pro)**：8个框架的专业.cursorrules配置 - Next.js、React、Python、Go、Rust等。适用于Cursor、Claude Code和Windsurf。
- **[nedcodes-ok/rule-porter](https://github.com/nedcodes-ok/rule-porter)**：Cursor（.mdc）、Claude Code（CLAUDE.md）、GitHub Copilot、Windsurf和传统.cursorrules格式之间的双向规则转换器。零依赖。
- **[SSOJet/skills](https://github.com/ssojet/skills)**：生产就绪的SSOJet技能和流行框架及平台的集成指南 — Node.js、Next.js、React、Java、.NET Core、Go、iOS、Android等。与SSOJet SAML、OIDC和企业SSO流无缝协作。适用于Cursor、Antigravity、Claude Code和Windsurf。
- **[MojoAuth/skills](https://github.com/MojoAuth/skills)**：流行框架的生产就绪MojoAuth指南和示例，如Node.js、Next.js、React、Java、.NET Core、Go、iOS和Android。
- **[Xquik-dev/x-twitter-scraper](https://github.com/Xquik-dev/x-twitter-scraper)**：X（Twitter）数据平台 — 推文搜索、用户查询、关注者提取、参与指标、赠品抽奖、监控、webhooks、19个提取工具、MCP服务器。
- **[shmlkv/dna-claude-analysis](https://github.com/shmlkv/dna-claude-analysis)**：个人基因组分析工具包 — 分析原始DNA数据的Python脚本，跨越17个类别（健康风险、祖先、药物基因组学、营养、心理学等），具有终端风格的单页HTML可视化。
- **[AlmogBaku/debug-skill](https://github.com/AlmogBaku/debug-skill)**: Interactive debugger skill for AI agents — breakpoints, stepping, variable inspection, and stack traces via the `dap` CLI. Supports Python, Go, Node.js/TypeScript, Rust, and C/C++.

### 灵感来源
- **[f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts)**：提示库的灵感。
- **[leonardomso/33-js-concepts](https://github.com/leonardomso/33-js-concepts)**：JavaScript精通的灵感。
### 其他来源
- **[agent-cards/skill](https://github.com/agent-cards/skill)**：为AI代理管理预付虚拟Visa卡。创建卡片、检查余额、查看凭证、关闭卡片，并通过MCP工具获取支持。
---

## 仓库贡献者

<a href="https://github.com/sickn33/antigravity-awesome-skills/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=sickn33/antigravity-awesome-skills" alt="Repository contributors" />
</a>

使用[contrib.rocks](https://contrib.rocks)制作。

我们正式感谢以下贡献者帮助使这个仓库变得精彩！

- [@sickn33](https://github.com/sickn33)
- [@munir-abbasi](https://github.com/munir-abbasi)
- [@ssumanbiswas](https://github.com/ssumanbiswas)
- [@zinzied](https://github.com/zinzied)
- [@Mohammad-Faiz-Cloud-Engineer](https://github.com/Mohammad-Faiz-Cloud-Engineer)
- [@Dokhacgiakhoa](https://github.com/Dokhacgiakhoa)
- [@IanJ332](https://github.com/IanJ332)
- [@chauey](https://github.com/chauey)
- [@ar27111994](https://github.com/ar27111994)
- [@8hrsk](https://github.com/8hrsk)
- [@itsmeares](https://github.com/itsmeares)
- [@GuppyTheCat](https://github.com/GuppyTheCat)
- [@fernandorych](https://github.com/fernandorych)
- [@nikolasdehor](https://github.com/nikolasdehor)
- [@talesperito](https://github.com/talesperito)
- [@jackjin1997](https://github.com/jackjin1997)
- [@HuynhNhatKhanh](https://github.com/HuynhNhatKhanh)
- [@liyin2015](https://github.com/liyin2015)
- [@arathiesh](https://github.com/arathiesh)
- [@Tiger-Foxx](https://github.com/Tiger-Foxx)
- [@Musayrlsms](https://github.com/Musayrlsms)
- [@sohamganatra](https://github.com/sohamganatra)
- [@SuperJMN](https://github.com/SuperJMN)
- [@SebConejo](https://github.com/SebConejo)
- [@Onsraa](https://github.com/Onsraa)
- [@truongnmt](https://github.com/truongnmt)
- [@code-vj](https://github.com/code-vj)
- [@viktor-ferenczi](https://github.com/viktor-ferenczi)
- [@vprudnikoff](https://github.com/vprudnikoff)
- [@Vonfry](https://github.com/Vonfry)
- [@Wittlesus](https://github.com/Wittlesus)
- [@avimak](https://github.com/avimak)
- [@buzzbysolcex](https://github.com/buzzbysolcex)
- [@c1c3ru](https://github.com/c1c3ru)
- [@ckdwns9121](https://github.com/ckdwns9121)
- [@developer-victor](https://github.com/developer-victor)
- [@fbientrigo](https://github.com/fbientrigo)
- [@junited31](https://github.com/junited31)
- [@KrisnaSantosa15](https://github.com/KrisnaSantosa15)
- [@nocodemf](https://github.com/nocodemf)
- [@sstklen](https://github.com/sstklen)
- [@taksrules](https://github.com/taksrules)
- [@thuanlm215](https://github.com/thuanlm215)
- [@zebbern](https://github.com/zebbern)
- [@vuth-dogo](https://github.com/vuth-dogo)
- [@ALEKGG1](https://github.com/ALEKGG1)
- [@Abdulrahmansoliman](https://github.com/Abdulrahmansoliman)
- [@alexmvie](https://github.com/alexmvie)
- [@Andruia](https://github.com/Andruia)
- [@acbhatt12](https://github.com/acbhatt12)
- [@BenedictKing](https://github.com/BenedictKing)
- [@rcigor](https://github.com/rcigor)
- [@whatiskadudoing](https://github.com/whatiskadudoing)
- [@k-kolomeitsev](https://github.com/k-kolomeitsev)
- [@Krishna-Modi12](https://github.com/Krishna-Modi12)
- [@kromahlusenii-ops](https://github.com/kromahlusenii-ops)
- [@djmahe4](https://github.com/djmahe4)
- [@maxdml](https://github.com/maxdml)
- [@mertbaskurt](https://github.com/mertbaskurt)
- [@nedcodes-ok](https://github.com/nedcodes-ok)
- [@LocNguyenSGU](https://github.com/LocNguyenSGU)
- [@KhaiTrang1995](https://github.com/KhaiTrang1995)
- [@sharmanilay](https://github.com/sharmanilay)
- [@yubing744](https://github.com/yubing744)
- [@PabloASMD](https://github.com/PabloASMD)
- [@0xrohitgarg](https://github.com/0xrohitgarg)
- [@Silverov](https://github.com/Silverov)
- [@shmlkv](https://github.com/shmlkv)
- [@kriptoburak](https://github.com/kriptoburak)

---

## 许可证

MIT许可证。详细信息请参见[LICENSE](LICENSE)。

---

## Star历史

[![Star History Chart](https://api.star-history.com/svg?repos=sickn33/antigravity-awesome-skills&type=date&legend=top-left)](https://www.star-history.com/#sickn33/antigravity-awesome-skills&type=date&legend=top-left)

如果Antigravity Awesome Skills对您有用，请考虑⭐给仓库加星！

<!-- GitHub Topics (for maintainers): claude-code, gemini-cli, codex-cli, antigravity, cursor, github-copilot, opencode, agentic-skills, ai-coding, llm-tools, ai-agents, autonomous-coding, mcp, ai-developer-tools, ai-pair-programming, vibe-coding, skill, skills, SKILL.md, rules.md, CLAUDE.md, GEMINI.md, CURSOR.md -->
