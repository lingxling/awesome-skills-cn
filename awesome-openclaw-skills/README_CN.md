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
    <strong>Discover 5490+ community-built OpenClaw skills, organized by category.
    </strong>
    <br />
    <br />
</div>

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![Skills Count](https://img.shields.io/badge/skills-5352-blue?style=flat-square)](#table-of-contents)
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

### ClawHub CLI

```bash
clawhub install <skill-slug>
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

截至 2026 年 2 月 28 日，OpenClaw 的公共注册表（ClawHub）托管了 **13,729 个社区构建的技能**。这个精选列表包含 **5,366 个技能**。以下是我们过滤掉的内容：

| 过滤器 | 排除 |
|--------|----------|
| 可能的垃圾内容 — 批量账户、机器人账户、测试/垃圾 | 4,065 |
| 重复/相似名称 | 1,040 |
| 低质量或非英语描述 | 851 |
| 加密货币/区块链/金融/交易 | 731 |
| 恶意 — 由研究人员发布的安全审计识别（不包括 VirusTotal） | 373 |
| **未从 OpenClaw 官方技能注册表获取的总数** | **7,060** |

### 想要添加技能？

此列表仅包括 **已发布** 在 `github.com/openclaw/skills` 存储库中的技能。我们不接受指向个人存储库、要点或任何其他外部来源的链接。如果您的技能尚未在 OpenClaw 技能存储库中，请先在那里发布。

在您的 PR 描述中包含 ClawHub 链接（例如 `https://clawhub.ai/steipete/slack`）和 GitHub 链接（例如 `https://github.com/openclaw/skills/tree/main/skills/steipete/slack`）。有关详细信息，请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

## OpenClaw 生态系统工具

### 🔌 连接到外部服务

OpenClaw 代理可以与 GitHub、Slack、Gmail 等外部服务交互。您可以通过技能或插件自己构建集成，或使用托管服务来处理所有连接的身份验证、令牌刷新和权限。

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

### ☁️ 托管和部署

您可以在任何 VPS 或云平台上部署 OpenClaw，在自己的基础设施或托管主机上安全运行您的技能。Docker、Podman、Nix 和 Ansible 都作为安装方法受支持。

> **提示：** 如果您正在寻找快速的云设置，请使用您首选的提供商启动 VPS，通过 Docker 安装 OpenClaw，然后就可以开始了。

## 安全注意事项

此列表中的技能是 **经过策划的，而非经过审计的**。它们可能在被添加到此处后由其原始维护者随时更新、修改或替换。

在安装或使用任何代理技能之前，请审查潜在的安全风险并自己验证来源。OpenClaw 与 **VirusTotal** 建立了合作伙伴关系，为技能提供安全扫描，请访问 ClawHub 上的技能页面并检查 VirusTotal 报告，查看它是否被标记为有风险。

**推荐工具：**

- [Snyk Skill Security Scanner](https://github.com/snyk/agent-scan)
- [Agent Trust Hub](https://ai.gendigital.com/agent-trust-hub)

> 代理技能可能包含提示注入、工具中毒、隐藏的恶意软件有效载荷或不安全的数据处理模式。在安装之前始终审查源代码，并自行决定使用技能。

如果您认为此列表中的技能应该被标记或存在安全问题，请 [打开一个问题](https://github.com/VoltAgent/awesome-clawdbot-skills/issues)，以便我们可以审查它。

## 目录

| | | |
|---|---|---|
| [Git & GitHub](#git--github) (170) | [Marketing & Sales](#marketing--sales) (105) | [Communication](#communication) (149) |
| [Coding Agents & IDEs](#coding-agents--ides) (1222) | [Productivity & Tasks](#productivity--tasks) (206) | [Speech & Transcription](#speech--transcription) (45) |
| [Browser & Automation](#browser--automation) (335) | [AI & LLMs](#ai--llms) (197) | [Smart Home & IoT](#smart-home--iot) (43) |
| [Web & Frontend Development](#web--frontend-development) (938) | [Data & Analytics](#data--analytics) (28) | [Shopping & E-commerce](#shopping--e-commerce) (55) |
| [DevOps & Cloud](#devops--cloud) (409) | [Finance](#finance) (21) | [Calendar & Scheduling](#calendar--scheduling) (65) |
| [Image & Video Generation](#image--video-generation) (169) | [Media & Streaming](#media--streaming) (85) | [PDF & Documents](#pdf--documents) (111) |
| [Apple Apps & Services](#apple-apps--services) (44) | [Notes & PKM](#notes--pkm) (71) | [Self-Hosted & Automation](#self-hosted--automation) (33) |
| [Search & Research](#search--research) (352) | [iOS & macOS Development](#ios--macos-development) (29) | [Security & Passwords](#security--passwords) (54) |
| [Clawdbot Tools](#clawdbot-tools) (37) | [Transportation](#transportation) (110) | [Moltbook](#moltbook) (29) |
| [CLI Utilities](#cli-utilities) (186) | [Personal Development](#personal-development) (51) | [Gaming](#gaming) (36) |
| [Health & Fitness](#health--fitness) (88) | [Agent-to-Agent Protocols](#agent-to-agent-protocols) (17) | |

## 技能分类

### Git & GitHub

> **[查看 Git & GitHub 中的所有 166 个技能 →](categories/git-and-github.md)**

### Coding Agents & IDEs

> **[查看 Coding Agents & IDEs 中的所有 1200 个技能 →](categories/coding-agents-and-ides.md)**

### Browser & Automation

> **[查看 Browser & Automation 中的所有 320 个技能 →](categories/browser-and-automation.md)**

### Web & Frontend Development

> **[查看 Web & Frontend Development 中的所有 925 个技能 →](categories/web-and-frontend-development.md)**

### DevOps & Cloud

> **[查看 DevOps & Cloud 中的所有 392 个技能 →](categories/devops-and-cloud.md)**

### Image & Video Generation

> **[查看 Image & Video Generation 中的所有 169 个技能 →](categories/image-and-video-generation.md)**

### Apple Apps & Services

> **[查看 Apple Apps & Services 中的所有 44 个技能 →](categories/apple-apps-and-services.md)**

### Search & Research

> **[查看 Search & Research 中的所有 352 个技能 →](categories/search-and-research.md)**

### 其他分类

- [Marketing & Sales](categories/marketing-and-sales.md) (105)
- [Communication](categories/communication.md) (149)
- [Productivity & Tasks](categories/productivity-and-tasks.md) (206)
- [Speech & Transcription](categories/speech-and-transcription.md) (45)
- [AI & LLMs](categories/ai-and-llms.md) (197)
- [Smart Home & IoT](categories/smart-home-and-iot.md) (43)
- [Data & Analytics](categories/data-and-analytics.md) (28)
- [Shopping & E-commerce](categories/shopping-and-e-commerce.md) (55)
- [Finance](categories/finance.md) (21)
- [Calendar & Scheduling](categories/calendar-and-scheduling.md) (65)
- [Media & Streaming](categories/media-and-streaming.md) (85)
- [PDF & Documents](categories/pdf-and-documents.md) (111)
- [Notes & PKM](categories/notes-and-pkm.md) (71)
- [Self-Hosted & Automation](categories/self-hosted-and-automation.md) (33)
- [iOS & macOS Development](categories/ios-and-macos-development.md) (29)
- [Security & Passwords](categories/security-and-passwords.md) (54)
- [Clawdbot Tools](categories/clawdbot-tools.md) (37)
- [Transportation](categories/transportation.md) (110)
- [Moltbook](categories/moltbook.md) (29)
- [CLI Utilities](categories/cli-utilities.md) (186)
- [Personal Development](categories/personal-development.md) (51)
- [Gaming](categories/gaming.md) (36)
- [Health & Fitness](categories/health-and-fitness.md) (88)
- [Agent-to-Agent Protocols](categories/agent-to-agent-protocols.md) (17)

---

## 原项目文档

如需查看原项目的完整英文文档，请访问：

- [README.md (英文原版)](README.md) - 原项目的完整说明文档

原项目由 [VoltAgent](https://github.com/VoltAgent) 维护。