# Awesome OpenClaw Skills 中文翻译

> 本文档是 [Awesome OpenClaw Skills](https://github.com/VoltAgent/awesome-clawdbot-skills) 项目的中文翻译版本。

## 关于本翻译

### 翻译项目介绍

本翻译属于 [awesome-skills-cn](https://github.com/lingxling/awesome-skills-cn) 项目的一部分，致力于将优秀的英文 SKILL 翻译成中文。本翻译涵盖了 OpenClaw 生态系统中的技能集合，帮助中文用户更好地了解和使用这些技能。

### 原项目介绍

**Awesome OpenClaw Skills** 是一个收集和整理 OpenClaw 社区构建的技能的项目。OpenClaw 是一个在本地运行的 AI 助手，直接在用户机器上操作。技能扩展了它的功能，使其能够与外部服务交互、自动化工作流程并执行专门任务。这个集合帮助用户发现和安装适合其需求的技能，也可以作为 OpenClaw 使用案例的灵感来源。

本列表中的技能来自 ClawHub（OpenClaw 的公共技能注册表）并按类别进行分类，以便于发现。

### 原项目链接

- [GitHub 仓库](https://github.com/VoltAgent/awesome-clawdbot-skills)
- [ClawHub](https://clawhub.ai/)
- [OpenClaw 官方网站](https://openclaw.ai/)

---

以下为原项目文件 README.md 的翻译。

---

<div align="center">

<a href="https://clawskills.sh/">
<img width="1500" height="500" alt="social" src="https://github.com/user-attachments/assets/a6f310af-8fed-4766-9649-b190575b399d" />
</a>

<br/>
<br/>

<div align="center">
    <strong>Discover 5300+ community-built OpenClaw skills, organized by category.
    </strong>
    <br />
    <br />
</div>

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![Skills Count](https://img.shields.io/badge/skills-5199-blue?style=flat-square)](#table-of-contents)
[![Last Update](https://img.shields.io/github/last-commit/VoltAgent/awesome-clawdbot-skills?label=Last%20update&style=flat-square)](https://github.com/VoltAgent/awesome-clawdbot-skills/pulls?q=is%3Apr+is%3Amerged+sort%3Aupdated-desc)
<a href="https://github.com/VoltAgent/voltagent">
  <img alt="VoltAgent" src="https://cdn.voltagent.dev/website/logo/logo-2-svg.svg" height="20" />
</a> 
[![Discord](https://img.shields.io/discord/1361559153780195478.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)](https://s.voltagent.dev/discord)

</div>

<div align="center">
    <strong>More awesome collections for developers</strong>
    <br />
    <br />
</div>

<div align="center">

[![Agent Skills](https://img.shields.io/github/stars/VoltAgent/awesome-agent-skills?style=classic&label=%E2%9A%A1%20Agent%20Skills&color=black)](https://github.com/VoltAgent/awesome-agent-skills)
[![Claude Code Subagents](https://img.shields.io/github/stars/VoltAgent/awesome-claude-code-subagents?style=classic&label=Claude%20Code%20Subagents&color=D97757&logo=claude&logoColor=D97757)](https://github.com/VoltAgent/awesome-claude-code-subagents)
[![Codex Subagents][codex-badge]][codex-link]
[![AI Agent Papers](https://img.shields.io/github/stars/VoltAgent/awesome-ai-agent-papers?style=classic&label=AI%20Agent%20Papers&color=b31b1b&logo=arxiv)](https://github.com/VoltAgent/awesome-ai-agent-papers)

</div>

</div>

</div>


# Awesome OpenClaw Skills

OpenClaw 是一个在本地运行的 AI 助手，直接在您的机器上操作。技能扩展了它的功能，使其能够与外部服务交互、自动化工作流程并执行专门任务。这个集合帮助您发现和安装适合您需求的技能，也可以作为 OpenClaw 使用案例的灵感来源。

本列表中的技能来自 ClawHub（OpenClaw 的公共技能注册表）并按类别进行分类，以便于发现。

## 安装

### OpenClaw CLI

```bash
openclaw skills install <skill-slug>
```

### ClawHub CLI

也可以使用 ClawHub CLI，适用于不在完整 OpenClaw 工作区内、由注册表管理的技能文件夹：

```bash
npx clawhub install <skill-slug>
```

### 手动安装

将技能文件夹复制到以下位置之一：

| 位置 | 路径 |
|----------|------|
| 全局 | `~/.openclaw/skills/` |
| 工作区 | `<project>/skills/` |

优先级：工作区 > 本地 > 捆绑

### 替代方法

您也可以直接将技能的 GitHub 存储库链接粘贴到助手的聊天中，并要求它使用它。助手将在后台自动处理设置。

## 为什么这个列表存在？

OpenClaw 的公共注册表（ClawHub）托管了数千个社区构建的技能。这份精选列表收录了其中最优质的部分。以下是我们过滤掉的内容：

| 过滤器 | 排除 |
|--------|----------|
| 可能的垃圾内容 — 批量账户、机器人账户、测试/垃圾 | 4,065 |
| 重复/相似名称 | 1,040 |
| 低质量或非英语描述 | 851 |
| 加密货币/区块链/金融/交易 | 886 |
| 恶意 — 由研究人员发布的安全审计识别（不包括 VirusTotal） | 373 |
| **未从 OpenClaw 官方技能注册表获取的总数** | **7,215** |

### 想要添加技能？

此列表仅包括已在 [ClawHub](https://clawhub.ai)（OpenClaw 的公共技能注册表）上**发布**的技能。我们不接受指向个人仓库、gist 或任何其他外部来源的链接。如果您的技能尚未发布到 ClawHub，请先在那里发布。

请在您的 PR 描述中附上技能对应的 ClawHub 链接（例如 `https://clawhub.ai/steipete/slack`）——`clawskills.sh` 上的列表由我们单独管理。详情请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

## OpenClaw 生态系统工具

### 🔌 连接到外部服务

OpenClaw 代理可以与 GitHub、Slack、Gmail 等外部服务交互。您可以通过技能或插件自己构建集成，或使用托管服务来处理所有连接的身份验证、令牌刷新和权限。

<a href="https://composio.dev/claw?utm_source=github&utm_campaign=volt-agent">
<img src="https://cdn.voltagent.dev/awesome-repo/composio-img.png" alt="Composio"  />
托管 OAuth、范围权限和跨 1000+ 应用的原生工具调用日志。
</a>

### ☁️ 托管和部署

您可以在任何 VPS 或云平台上部署 OpenClaw，在自己的基础设施上安全运行您的技能，也可以使用托管主机，由其负责服务器、更新和隔离。

<a href="https://myclaw.ai/?utm_source=github&utm_campaign=awesome-openclaw-skills">
<img src="https://cdn.voltagent.dev/awesome-repo/myclaw-banner.svg" alt="MyClaw"  /><br/>
您无需管理服务器即可运行这些技能 — 一键设置的全云托管 OpenClaw 实例，24/7 运行时间，完全数据所有权。
</a>


<br/>
<br/>

> **提示：** 如果您是自托管，请将 OpenClaw 的 Docker 镜像固定到指定标签，并在升级前对技能卷做快照 — 这样当某次技能更新出问题时，回滚会轻松很多。

### 🔍 搜索与网络数据

OpenClaw 代理经常需要获取新鲜的真实世界数据 — 搜索结果、商品列表、视频等等。您可以自己抓取和解析这些数据，也可以使用搜索 API，实时返回干净、结构化的数据，无需自己管理代理、验证码或 HTML 解析。

<a href="https://serpapi.com/search-engine-apis?utm_source=awesomeopenclawskills_github">
<img src="https://cdn.voltagent.dev/awesome-repo/serpapi.png" alt="SerpApi"  /><br/>
让 OpenClaw 代理通过单一 API 访问实时的 Google 搜索、YouTube、Amazon 商品和网页搜索数据。
</a>

### 🛡️ 安全与配置审计

随着您添加越来越多的技能、自定义代码和已连接服务，您的 OpenClaw 配置会积累大量密钥、文件访问权限和工具权限，很容易失去追踪。您可以手动审查这些内容，也可以运行持续审计，在配置错误和权限过宽演变成问题之前就发现它们。

<a href="https://trent.ai/openclaw/?utm_source=github&utm_medium=referral&utm_campaign=volt-agent">
<img src="https://cdn.voltagent.dev/awesome-repo/trentclaw-banner.png" alt="trentclaw"  /><br/>
trentclaw：审计您的 OpenClaw 配置、已安装的技能和自定义代码，并以 diff 形式返回修复建议。安装命令：openclaw skills install trentclaw
</a>

### 🤖 模型提供商

OpenClaw 开箱即用地支持 **25+ LLM 提供商**，包括 Anthropic、OpenAI 等。通过单个配置更改即可在它们之间切换。

<details>
<summary><strong>示例：使用 OpenAI 模型</strong></summary>

OpenClaw 通过直接 API 密钥或 ChatGPT/Codex OAuth 支持 `gpt-5.4` 和 `gpt-5.4-pro`。默认启用 WebSocket 传输以降低延迟。

```bash
openclaw onboard --auth-choice openai-api-key
# 或使用基于订阅的访问：
openclaw onboard --auth-choice openai-codex
```
</details>

<div align="center">

<table>
<tr>
<td align="center" width="100%">

<h3>🦞 您可以在上面的部分展示您的 OpenClaw 生态系统工具。</h3>

<p></p>

<sub>仅次于官方 OpenClaw 资源的访问量最高的社区资源</sub>


<a href="https://sponsors.voltagent.dev/#awesome-openclaw-skills"><img src="https://img.shields.io/badge/📩_成为赞助商-联系我们-blue?style=for-the-badge&logoColor=white" alt="成为赞助商" /></a>

</td>
</tr>
</table>

</div>

## 安全注意事项

此列表中的技能是 **经过策划的，而非经过审计的**。它们可能在被添加到此处后由其原始维护者随时更新、修改或替换。

在安装或使用任何代理技能之前，请审查潜在的安全风险并自己验证来源。OpenClaw 与 **VirusTotal** 建立了合作伙伴关系，为技能提供安全扫描，请访问 ClawHub 上的技能页面并检查 VirusTotal 报告，查看它是否被标记为有风险。

**推荐工具：**

- [Snyk Skill Security Scanner](https://github.com/snyk/agent-scan)
- [Agent Trust Hub](https://ai.gendigital.com/agent-trust-hub)

> 代理技能可能包含提示注入、工具中毒、隐藏的恶意软件有效载荷或不安全的数据处理模式。在安装之前始终审查源代码，并自行决定使用技能。

如需更全面地了解 ClawHub 生态系统，请参阅 Trent AI 的 **[ClawHub by the Numbers](https://trent.ai/blog/clawhub-by-the-numbers/)**。

如果您认为此列表中的技能应该被标记或存在安全问题，请 [打开一个问题](https://github.com/VoltAgent/awesome-clawdbot-skills/issues)，以便我们可以审查它。

## 目录

| | | |
|---|---|---|
| [Git & GitHub](#git--github) (167) | [Marketing & Sales](#marketing--sales) (106) | [Communication](#communication) (146) |
| [Coding Agents & IDEs](#coding-agents--ides) (1184) | [Productivity & Tasks](#productivity--tasks) (206) | [Speech & Transcription](#speech--transcription) (46) |
| [Browser & Automation](#browser--automation) (323) | [AI & LLMs](#ai--llms) (176) | [Smart Home & IoT](#smart-home--iot) (41) |
| [Web & Frontend Development](#web--frontend-development) (920) | [Data & Analytics](#data--analytics) (28) | [Shopping & E-commerce](#shopping--e-commerce) (51) |
| [DevOps & Cloud](#devops--cloud) (393) | [Calendar & Scheduling](#calendar--scheduling) (66) | |
| [Image & Video Generation](#image--video-generation) (170) | [Media & Streaming](#media--streaming) (86) | [PDF & Documents](#pdf--documents) (105) |
| [Apple Apps & Services](#apple-apps--services) (44) | [Notes & PKM](#notes--pkm) (69) | [Self-Hosted & Automation](#self-hosted--automation) (33) |
| [Search & Research](#search--research) (345) | [iOS & macOS Development](#ios--macos-development) (29) | [Security & Passwords](#security--passwords) (54) |
| [Clawdbot Tools](#clawdbot-tools) (37) | [Transportation](#transportation) (111) | [Moltbook](#moltbook) (29) |
| [CLI Utilities](#cli-utilities) (180) | [Personal Development](#personal-development) (52) | [Gaming](#gaming) (35) |
| [Health & Fitness](#health--fitness) (87) | | |

<br/>

<a href="https://launchkit.getdesign.md/">
<img src="https://cdn.voltagent.dev/awesome-repo/launchkit-banner-3.png" alt="launchkit"  /><br/>
</a>

<br/>

## 技能分类

### Git & GitHub

> **[查看 Git & GitHub 中的所有 159 个技能 →](categories/git-and-github.md)**

### Coding Agents & IDEs

> **[查看 Coding Agents & IDEs 中的所有 1200 个技能 →](categories/coding-agents-and-ides.md)**

### Browser & Automation

> **[查看 Browser & Automation 中的所有技能 →](categories/browser-and-automation.md)**

### Web & Frontend Development

> **[查看 Web & Frontend Development 中的所有技能 →](categories/web-and-frontend-development.md)**

### DevOps & Cloud

> **[查看 DevOps & Cloud 中的所有技能 →](categories/devops-and-cloud.md)**

### Image & Video Generation

> **[查看 Image & Video Generation 中的所有 170 个技能 →](categories/image-and-video-generation.md)**

### Apple Apps & Services

> **[查看 Apple Apps & Services 中的所有 44 个技能 →](categories/apple-apps-and-services.md)**

### Search & Research

> **[查看 Search & Research 中的所有 352 个技能 →](categories/search-and-research.md)**

### 其他分类

- [Marketing & Sales](categories/marketing-and-sales.md) (106)
- [Communication](categories/communication.md) (146)
- [Productivity & Tasks](categories/productivity-and-tasks.md) (206)
- [Speech & Transcription](categories/speech-and-transcription.md) (46)
- [AI & LLMs](categories/ai-and-llms.md) (176)
- [Smart Home & IoT](categories/smart-home-and-iot.md) (41)
- [Data & Analytics](categories/data-and-analytics.md) (28)
- [Shopping & E-commerce](categories/shopping-and-e-commerce.md) (51)
- [Calendar & Scheduling](categories/calendar-and-scheduling.md) (66)
- [Media & Streaming](categories/media-and-streaming.md) (86)
- [PDF & Documents](categories/pdf-and-documents.md) (105)
- [Notes & PKM](categories/notes-and-pkm.md) (69)
- [Self-Hosted & Automation](categories/self-hosted-and-automation.md) (33)
- [iOS & macOS Development](categories/ios-and-macos-development.md) (29)
- [Security & Passwords](categories/security-and-passwords.md) (54)
- [Clawdbot Tools](categories/clawdbot-tools.md) (37)
- [Transportation](categories/transportation.md) (111)
- [Moltbook](categories/moltbook.md) (29)
- [CLI Utilities](categories/cli-utilities.md) (180)
- [Personal Development](categories/personal-development.md) (52)
- [Gaming](categories/gaming.md) (35)
- [Health & Fitness](categories/health-and-fitness.md) (87)

---

## 原项目文档

如需查看原项目的完整英文文档，请访问：

- [README.md (英文原版)](README.md) - 原项目的完整说明文档

原项目由 [VoltAgent](https://github.com/VoltAgent) 维护。