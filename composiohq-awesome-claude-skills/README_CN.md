<h1 align="center">Awesome Claude Skills</h1>

<p align="center">
<a href="https://dashboard.composio.dev/login?utm_source=Github&utm_medium=Youtube&utm_campaign=2025-11&utm_content=AwesomeSkills">
  <img width="1280" height="640" alt="Composio banner" src="https://github.com/user-attachments/assets/e91255af-e4ba-4d71-b1a8-bd081e8a234a">
</a>

</p>

<p align="center">
  <a href="https://awesome.re">
    <img src="https://awesome.re/badge.svg" alt="Awesome" />
  </a>
  <a href="https://makeapullrequest.com">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square" alt="PRs Welcome" />
  </a>
  <a href="https://www.apache.org/licenses/LICENSE-2.0">
    <img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=flat-square" alt="License: Apache-2.0" />
  </a>
</p>
<div>
<p align="center">
  <a href="https://twitter.com/composio">
    <img src="https://img.shields.io/badge/Follow on X-000000?style=for-the-badge&logo=x&logoColor=white" alt="Follow on X" />
  </a>
  <a href="https://www.linkedin.com/company/composiohq/">
    <img src="https://img.shields.io/badge/Follow on LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="Follow on LinkedIn" />
  </a>
  <a href="https://discord.com/invite/composio">
    <img src="https://img.shields.io/badge/Join our Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Join our Discord" />
  </a>
  </p>
</div>

精心整理的实用 Claude Skills 列表，用于提升 Claude.ai、Claude Code 和 Claude API 的生产力。

> **想要能够执行更多操作的技能吗？** Claude 可以发送邮件、创建 issue、发布 Slack 消息，并在 1000+ 个应用中执行操作。[查看方法 →](./connect/)

---

## 快速开始：连接 Claude 到 500+ 应用

**connect-apps** 插件让 Claude 能够执行实际操作——发送邮件、创建 issue、发布 Slack 消息。它处理认证并使用 Composio 在后台连接 500+ 个应用。

### 1. 安装插件

```bash
claude --plugin-dir ./connect-apps-plugin
```

### 2. 运行设置

```
/connect-apps:setup
```

出现提示时粘贴您的 API 密钥。（在 [dashboard.composio.dev](https://dashboard.composio.dev/login?utm_source=Github&utm_content=AwesomeSkills) 获取免费密钥）

### 3. 重启并试用

```bash
exit
claude
```

> **想要能够执行更多操作的技能吗？** Claude 可以发送邮件、创建 issue、发布 Slack 消息，并在 1000+ 个应用中执行操作。[查看方法 →](./connect/)

如果您收到邮件，说明 Claude 已连接到 500+ 个应用。

**[查看所有支持的应用 →](https://composio.dev/toolkits)**

---

## 目录

- [快速开始：连接 Claude 到 500+ 应用](#快速开始连接-claude-到-500-应用)
  - [1. 安装插件](#1-安装插件)
  - [2. 运行设置](#2-运行设置)
  - [3. 重启并试用](#3-重启并试用)
- [目录](#目录)
- [什么是 Claude Skills？](#什么是-claude-skills)
- [技能列表](#技能列表)
  - [文档处理](#文档处理)
  - [开发与代码工具](#开发与代码工具)
  - [数据分析](#数据分析)
  - [商业与营销](#商业与营销)
  - [沟通与写作](#沟通与写作)
  - [创意与媒体](#创意与媒体)
  - [生产力与组织](#生产力与组织)
  - [协作与项目管理](#协作与项目管理)
  - [安全与系统](#安全与系统)
  - [通过 Composio 实现应用自动化](#通过-composio-实现应用自动化)
- [开始使用](#开始使用)
  - [在 Claude.ai 中使用技能](#在-claudeai-中使用技能)
  - [在 Claude Code 中使用技能](#在-claude-code-中使用技能)
  - [通过 API 使用技能](#通过-api-使用技能)
- [创建技能](#创建技能)
  - [技能结构](#技能结构)
  - [基础技能模板](#基础技能模板)
  - [技能最佳实践](#技能最佳实践)
- [贡献指南](#贡献指南)
  - [快速贡献步骤](#快速贡献步骤)
- [资源](#资源)
  - [官方文档](#官方文档)
  - [社区资源](#社区资源)
  - [灵感与用例](#灵感与用例)
- [加入社区](#加入社区)
- [许可证](#许可证)

## 什么是 Claude Skills？

Claude Skills 是可自定义的工作流程，用于教授 Claude 如何根据您的独特需求执行特定任务。技能使 Claude 能够以可重复、标准化的方式在所有 Claude 平台上执行任务。

## 技能列表

### 文档处理

- [docx](https://github.com/anthropics/skills/tree/main/skills/docx) - 创建、编辑、分析 Word 文档，支持修订跟踪、评论和格式。
- [pdf](https://github.com/anthropics/skills/tree/main/skills/pdf) - 提取文本、表格、元数据，合并和标注 PDF。
- [pptx](https://github.com/anthropics/skills/tree/main/skills/pptx) - 读取、生成和调整幻灯片、布局、模板。
- [xlsx](https://github.com/anthropics/skills/tree/main/skills/xlsx) - 电子表格操作：公式、图表、数据转换。
- [Markdown to EPUB Converter](https://github.com/smerchek/claude-epub-skill) - 将 markdown 文档和聊天摘要转换为专业的 EPUB 电子书文件。*作者 [@smerchek](https://github.com/smerchek)*
- [Master Claude for Legal](https://github.com/sboghossian/master-claude-for-legal) - 法律团队技能包。NDA 分类、多方版本差异、引用验证、会议简报和周五通讯状态合成模式。包含 10 个参考文档（特权、验证、长文档、实践领域）和 3 个公司模板。来源于公开的 Anthropic Claude for Legal Teams 网络研讨会数据集。*作者 [@sboghossian](https://github.com/sboghossian)*

### 开发与代码工具

- [artifacts-builder](https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder) - 一套工具，用于使用现代前端 Web 技术（React、Tailwind CSS、shadcn/ui）创建复杂的、多组件的 claude.ai HTML 产物。
- [aws-skills](https://github.com/zxkane/aws-skills) - AWS 开发，包含 CDK 最佳实践、成本优化 MCP 服务器和无服务器/事件驱动架构模式。
- [Changelog Generator](./changelog-generator/) - 通过分析 git 提交历史并将技术提交转换为面向客户的发布说明，自动创建面向用户的变更日志。
- [Chrome Relay](https://chrome-relay.kushalsm.com/) - 通过本地 CLI 桥接驱动用户已打开的 Chrome 会话——Cookie、SSO、扩展、localhost。Playwright 浏览器自动化的真实 Chrome 对应版本；通过 `npx skills add chrome-relay` + [Chrome Web Store 扩展](https://chromewebstore.google.com/detail/chrome-relay/cpdiapbifblhlcpnmlmfpgfjlacebokb) 安装。无需远程中继、无需 Playwright 夹具、无需 MCP 服务器。
- [Claude Code Terminal Title](https://github.com/bluzername/claude-code-terminal-title) - 为每个 Claude Code 终端窗口提供动态标题，描述正在执行的工作，这样您就不会丢失对窗口正在执行任务的跟踪。
- [D3.js Visualization](https://github.com/chrisvoncsefalvay/claude-d3js-skill) - 教 Claude 生成 D3 图表和交互式数据可视化。*作者 [@chrisvoncsefalvay](https://github.com/chrisvoncsefalvay)*
- [FFUF Web Fuzzing](https://github.com/jthack/ffuf_claude_skill) - 集成 ffuf Web 模糊测试工具，使 Claude 能够运行模糊测试任务并分析漏洞结果。*作者 [@jthack](https://github.com/jthack)*
- [finishing-a-development-branch](https://github.com/obra/superpowers/tree/main/skills/finishing-a-development-branch) - 通过呈现清晰的选项并处理选定的工作流程来指导开发工作的完成。
- [iOS Simulator](https://github.com/conorluddy/ios-simulator-skill) - 使 Claude 能够与 iOS 模拟器交互，用于测试和调试 iOS 应用程序。*作者 [@conorluddy](https://github.com/conorluddy)*
- [jules](https://github.com/sanjay3290/ai-skills/tree/main/skills/jules) - 将编码任务委托给 Google Jules AI 代理，用于 GitHub 仓库上的异步错误修复、文档编写、测试和功能实现。*作者 [@sanjay3290](https://github.com/sanjay3290)*
- [LangSmith Fetch](./langsmith-fetch/) - 通过自动从 LangSmith Studio 获取和分析执行跟踪来调试 LangChain 和 LangGraph 代理。Claude Code 首个 AI 可观测性技能。*作者 [@OthmanAdi](https://github.com/OthmanAdi)*
- [MCP Builder](./mcp-builder/) - 指导创建高质量的 MCP（Model Context Protocol）服务器，用于使用 Python 或 TypeScript 将外部 API 和服务与 LLM 集成。
- [move-code-quality-skill](https://github.com/1NickPappas/move-code-quality-skill) - 根据官方 Move Book 代码质量检查清单分析 Move 语言包，以符合 Move 2024 Edition 合规性和最佳实践。
- [Playwright Browser Automation](https://github.com/lackeyjb/playwright-skill) - 模型调用的 Playwright 自动化，用于测试和验证 Web 应用程序。*作者 [@lackeyjb](https://github.com/lackeyjb)*
- [prompt-engineering](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/customaize-agent/skills/prompt-engineering) - 教授著名的提示工程技术和模式，包括 Anthropic 最佳实践和代理说服原则。
- [pypict-claude-skill](https://github.com/omkamal/pypict-claude-skill) - 使用 PICT（成对独立组合测试）为需求或代码设计全面的测试用例，生成具有成对覆盖率的优化测试套件。
- [reddit-fetch](https://github.com/ykdojo/claude-code-tips/tree/main/skills/reddit-fetch) - 当 WebFetch 被阻止或返回 403 错误时，通过 Gemini CLI 获取 Reddit 内容。
- [Skill Creator](./skill-creator/) - 提供创建有效 Claude Skills 的指导，通过专门知识、工作流程和工具集成扩展能力。
- [Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) - 在几分钟内自动将任何文档网站转换为 Claude AI 技能。*作者 [@yusufkaraaslan](https://github.com/yusufkaraaslan)*
- [software-architecture](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/ddd/skills/software-architecture) - 实现设计模式，包括 Clean Architecture、SOLID 原则和全面的软件设计最佳实践。
- [subagent-driven-development](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/sadd/skills/subagent-driven-development) - 为单独任务分派独立子代理，迭代之间进行代码审查检查点，实现快速、受控的开发。
- [test-driven-development](https://github.com/obra/superpowers/tree/main/skills/test-driven-development) - 在实现任何功能或错误修复时使用，在编写实现代码之前。
- [using-git-worktrees](https://github.com/obra/superpowers/blob/main/skills/using-git-worktrees/) - 使用智能目录选择和安全验证创建隔离的 git worktree。
- [Connect](./connect/) - 将 Claude 连接到任何应用。发送邮件、创建 issue、发布消息、更新数据库——在 Gmail、Slack、GitHub、Notion 和 1000+ 服务上执行实际操作。
- [Webapp Testing](./webapp-testing/) - 使用 Playwright 测试本地 Web 应用程序，用于验证前端功能、调试 UI 行为和捕获屏幕截图。

### 数据分析

- [CSV Data Summarizer](https://github.com/coffeefuelbump/csv-data-summarizer-claude-skill) - 自动分析 CSV 文件并生成包含可视化的全面洞察，无需用户提示。*作者 [@coffeefuelbump](https://github.com/coffeefuelbump)*
- [deep-research](https://github.com/sanjay3290/ai-skills/tree/main/skills/deep-research) - 使用 Gemini Deep Research Agent 执行自主多步研究，用于市场分析、竞争格局和文献综述。*作者 [@sanjay3290](https://github.com/sanjay3290)*
- [postgres](https://github.com/sanjay3290/ai-skills/tree/main/skills/postgres) - 对 PostgreSQL 数据库执行安全的只读 SQL 查询，支持多连接和纵深防御安全。*作者 [@sanjay3290](https://github.com/sanjay3290)*
- [root-cause-tracing](https://github.com/obra/superpowers/tree/main/skills/root-cause-tracing) - 当错误发生在执行深处且需要追溯找到原始触发器时使用。

### 商业与营销

- [Brand Guidelines](./brand-guidelines/) - 应用 Anthropic 官方品牌颜色和排版到产物上，以保持一致的品牌形象和专业设计标准。
- [Competitive Ads Extractor](./competitive-ads-extractor/) - 从广告库中提取和分析竞争对手的广告，了解能引起共鸣的信息和创意方法。
- [Domain Name Brainstormer](./domain-name-brainstormer/) - 生成创意的域名想法，并在多种 TLD（包括 .com、.io、.dev 和 .ai 扩展名）中检查可用性。
- [Internal Comms](./internal-comms/) - 帮助编写内部沟通内容，包括 3P 更新、公司通讯、常见问题、状态报告和项目更新，使用公司特定格式。
- [Lead Research Assistant](./lead-research-assistant/) - 通过分析您的产品、搜索目标公司并提供可操作的联系策略来识别和筛选高质量潜在客户。

### 沟通与写作

- [article-extractor](https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/article-extractor) - 从网页提取完整文章文本和元数据。
- [brainstorming](https://github.com/obra/superpowers/tree/main/skills/brainstorming) - 通过结构化提问和替代方案探索将粗略想法转化为完整设计。
- [Content Research Writer](./content-research-writer/) - 通过进行研究、添加引用、改进开头和提供逐节反馈来帮助撰写高质量内容。
- [family-history-research](https://github.com/emaynard/claude-family-history-research-skill) - 提供家庭历史和谱系研究项目规划协助。
- [Meeting Insights Analyzer](./meeting-insights-analyzer/) - 分析会议记录以发现行为模式，包括冲突回避、发言比率、填充词和领导风格。
- [NotebookLM Integration](https://github.com/PleasePrompto/notebooklm-skill) - 让 Claude Code 能够直接与 NotebookLM 聊天，基于上传的文档获取来源支持的答案。*作者 [@PleasePrompto](https://github.com/PleasePrompto)*
- [Twitter Algorithm Optimizer](./twitter-algorithm-optimizer/) - 使用 Twitter 开源算法洞察分析和优化推文以获得最大覆盖面。重写和编辑推文以提高参与度和可见性。

### 创意与媒体

- [Canvas Design](./canvas-design/) - 使用设计理念和美学原则在 PNG 和 PDF 文档中创建美丽的视觉艺术，用于海报、设计和静态作品。
- [imagen](https://github.com/sanjay3290/ai-skills/tree/main/skills/imagen) - 使用 Google Gemini 图像生成 API 生成图像，用于 UI 模型、图标、插图和视觉资产。*作者 [@sanjay3290](https://github.com/sanjay3290)*
- [Image Enhancer](./image-enhancer/) - 通过增强分辨率、锐度和清晰度来提高图像和屏幕截图质量，用于专业演示和文档。
- [Slack GIF Creator](./slack-gif-creator/) - 创建针对 Slack 优化的动画 GIF，包含大小约束验证器和可组合动画原语。
- [Theme Factory](./theme-factory/) - 为幻灯片、文档、报告和 HTML 登录页面等产物应用专业字体和颜色主题，包含 10 个预设主题。
- [Video Downloader](./video-downloader/) - 从 YouTube 和其他平台下载视频以供离线观看、编辑或归档，支持多种格式和质量选项。
- [youtube-transcript](https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/youtube-transcript) - 获取 YouTube 视频的字幕并准备摘要。

### 生产力与组织

- [File Organizer](./file-organizer/) - 通过理解上下文、查找重复项并建议更好的组织结构来智能组织文件和文件夹。
- [Invoice Organizer](./invoice-organizer/) - 通过读取文件、提取信息并一致重命名来自动组织发票和收据以进行税务准备。
- [kaizen](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/kaizen/skills/kaizen) - 应用基于日本 Kaizen 理念和精益方法的持续改进方法论，包含多种分析方法。
- [n8n-skills](https://github.com/haunchen/n8n-skills) - 使 AI 助手能够直接理解和操作 n8n 工作流程。
- [Raffle Winner Picker](./raffle-winner-picker/) - 从列表、电子表格或 Google 表格中随机选择获奖者，用于赠品和竞赛，具有加密安全的随机性。
- [Tailored Resume Generator](./tailored-resume-generator/) - 分析职位描述并生成针对性简历，突出相关经验、技能和成就，以最大化面试机会。
- [ship-learn-next](https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/ship-learn-next) - 基于反馈循环帮助迭代接下来要构建或学习的内容。
- [tapestry](https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/tapestry) - 将相关文档相互链接并总结为知识网络。

### 协作与项目管理

- [git-pushing](https://github.com/mhattingpete/claude-skills-marketplace/tree/main/engineering-workflow-plugin/skills/git-pushing) - 自动化 git 操作和仓库交互。
- [google-workspace-skills](https://github.com/sanjay3290/ai-skills/tree/main/skills) - Google Workspace 集成套件：Gmail、Calendar、Chat、Docs、Sheets、Slides 和 Drive，支持跨平台 OAuth。*作者 [@sanjay3290](https://github.com/sanjay3290)*
- [outline](https://github.com/sanjay3290/ai-skills/tree/main/skills/outline) - 在 Outline wiki 实例（云或自托管）中搜索、读取、创建和管理文档。*作者 [@sanjay3290](https://github.com/sanjay3290)*
- [review-implementing](https://github.com/mhattingpete/claude-skills-marketplace/tree/main/engineering-workflow-plugin/skills/review-implementing) - 评估代码实现计划并与规格对齐。
- [test-fixing](https://github.com/mhattingpete/claude-skills-marketplace/tree/main/engineering-workflow-plugin/skills/test-fixing) - 检测失败的测试并提出补丁或修复方案。

### 安全与系统

- [computer-forensics](https://github.com/mhattingpete/claude-skills-marketplace/tree/main/computer-forensics-skills/skills/computer-forensics) - 数字取证分析和调查技术。
- [file-deletion](https://github.com/mhattingpete/claude-skills-marketplace/tree/main/computer-forensics-skills/skills/file-deletion) - 安全文件删除和数据清理方法。
- [metadata-extraction](https://github.com/mhattingpete/claude-skills-marketplace/tree/main/computer-forensics-skills/skills/metadata-extraction) - 提取和分析取证目的的文件元数据。
- [threat-hunting-with-sigma-rules](https://github.com/jthack/threat-hunting-with-sigma-rules-skill) - 使用 Sigma 检测规则来搜寻威胁和分析安全事件。

### 通过 Composio 实现应用自动化

通过 [Rube MCP (Composio)](https://composio.dev) 为 78 个 SaaS 应用提供预构建的工作流程技能。每个技能都包含工具序列、参数指导、已知陷阱和快速参考表——全部使用从 Composio API 发现的实际工具 slug。

**CRM 与销售**
- [Close Automation](./close-automation/) - 自动化 Close CRM：潜在客户、联系人、机会、活动和管道。
- [HubSpot Automation](./hubspot-automation/) - 自动化 HubSpot CRM：联系人、交易、公司、门票和邮件参与。
- [Pipedrive Automation](./pipedrive-automation/) - 自动化 Pipedrive：交易、联系人、组织、活动和管道。
- [Salesforce Automation](./salesforce-automation/) - 自动化 Salesforce：对象、记录、SOQL 查询和批量操作。
- [Zoho CRM Automation](./zoho-crm-automation/) - 自动化 Zoho CRM：潜在客户、联系人、交易、账户和模块。

**项目管理**
- [Asana Automation](./asana-automation/) - 自动化 Asana：任务、项目、部分、分配和工作区。
- [Basecamp Automation](./basecamp-automation/) - 自动化 Basecamp：待办事项、消息、人员、组和项目。
- [ClickUp Automation](./clickup-automation/) - 自动化 ClickUp：任务、列表、空间、目标和时间跟踪。
- [Jira Automation](./jira-automation/) - 自动化 Jira：问题、项目、看板、冲刺和 JQL 查询。
- [Linear Automation](./linear-automation/) - 自动化 Linear：问题、项目、周期、团队和工作流。
- [Monday Automation](./monday-automation/) - 自动化 Monday.com：板块、项目、列、组和工作区。
- [Notion Automation](./notion-automation/) - 自动化 Notion：页面、数据库、块、评论和搜索。
- [Todoist Automation](./todoist-automation/) - 自动化 Todoist：任务、项目、部分、标签和过滤器。
- [Trello Automation](./trello-automation/) - 自动化 Trello：看板、卡片、列表、成员和检查清单。
- [Wrike Automation](./wrike-automation/) - 自动化 Wrike：任务、文件夹、项目、评论和工作流。

**通讯**
- [Discord Automation](./discord-automation/) - 自动化 Discord：消息、频道、服务器、角色和反应。
- [Intercom Automation](./intercom-automation/) - 自动化 Intercom：对话、联系人、公司、门票和文章。
- [Microsoft Teams Automation](./microsoft-teams-automation/) - 自动化 Teams：消息、频道、团队、聊天和会议。
- [Slack Automation](./slack-automation/) - 自动化 Slack：消息、频道、搜索、反应、线程和定时发送。
- [Telegram Automation](./telegram-automation/) - 自动化 Telegram：消息、聊天、媒体、群组和机器人。
- [WhatsApp Automation](./whatsapp-automation/) - 自动化 WhatsApp：消息、媒体、模板、群组和商业资料。

**邮件**
- [Gmail Automation](./gmail-automation/) - 自动化 Gmail：发送/回复、搜索、标签、草稿和附件。
- [Outlook Automation](./outlook-automation/) - 自动化 Outlook：邮件、文件夹、联系人和日历集成。
- [Postmark Automation](./postmark-automation/) - 自动化 Postmark：交易邮件、模板、服务器和投递统计。
- [SendGrid Automation](./sendgrid-automation/) - 自动化 SendGrid：邮件、模板、联系人、列表和营销活动统计。

**代码与 DevOps**
- [Bitbucket Automation](./bitbucket-automation/) - 自动化 Bitbucket：仓库、PR、分支、issue 和工作区。
- [CircleCI Automation](./circleci-automation/) - 自动化 CircleCI：管道、工作流、作业和项目配置。
- [Datadog Automation](./datadog-automation/) - 自动化 Datadog：监控、仪表板、指标、事件和警报。
- [GitHub Automation](./github-automation/) - 自动化 GitHub：issue、PR、仓库、分支、actions 和代码搜索。
- [GitLab Automation](./gitlab-automation/) - 自动化 GitLab：issue、MR、项目、管道和分支。
- [PagerDuty Automation](./pagerduty-automation/) - 自动化 PagerDuty：事件、服务、排班、升级策略和值班。
- [Render Automation](./render-automation/) - 自动化 Render：服务、部署和项目管理。
- [Sentry Automation](./sentry-automation/) - 自动化 Sentry：issue、事件、项目、版本和警报。
- [Supabase Automation](./supabase-automation/) - 自动化 Supabase：SQL 查询、表架构、edge functions 和存储。
- [Vercel Automation](./vercel-automation/) - 自动化 Vercel：部署、项目、域名、环境变量和日志。

**存储与文件**
- [Box Automation](./box-automation/) - 自动化 Box：文件、文件夹、搜索、共享、协作和签名请求。
- [Dropbox Automation](./dropbox-automation/) - 自动化 Dropbox：文件、文件夹、搜索、共享和批量操作。
- [Google Drive Automation](./google-drive-automation/) - 自动化 Google Drive：上传、下载、搜索、共享和组织文件。
- [OneDrive Automation](./one-drive-automation/) - 自动化 OneDrive：文件、文件夹、搜索、共享、权限和版本控制。

**电子表格与数据库**
- [Airtable Automation](./airtable-automation/) - 自动化 Airtable：记录、表格、基础、视图和字段管理。
- [Coda Automation](./coda-automation/) - 自动化 Coda：文档、表格、行、公式和自动化。
- [Google Sheets Automation](./googlesheets-automation/) - 自动化 Google Sheets：读取/写入单元格、格式、公式和批量操作。

**日历与调度**
- [Cal.com Automation](./cal-com-automation/) - 自动化 Cal.com：活动类型、预订、可用性和调度。
- [Calendly Automation](./calendly-automation/) - 自动化 Calendly：活动、受邀者、活动类型、调度链接和可用性。
- [Google Calendar Automation](./google-calendar-automation/) - 自动化 Google Calendar：活动、受邀者、忙/闲和重复日程。
- [Outlook Calendar Automation](./outlook-calendar-automation/) - 自动化 Outlook Calendar：活动、受邀者、提醒和重复日程。

**社交媒体**
- [Instagram Automation](./instagram-automation/) - 自动化 Instagram：帖子、故事、评论、媒体和商业洞察。
- [LinkedIn Automation](./linkedin-automation/) - 自动化 LinkedIn：帖子、个人资料、公司、图片和评论。
- [Reddit Automation](./reddit-automation/) - 自动化 Reddit：帖子、评论、子版块、投票和 moderation。
- [TikTok Automation](./tiktok-automation/) - 自动化 TikTok：视频上传、查询和创作者管理。
- [Twitter Automation](./twitter-automation/) - 自动化 Twitter/X：推文、搜索、用户、列表和参与度。
- [YouTube Automation](./youtube-automation/) - 自动化 YouTube：视频、频道、播放列表、评论和订阅。

**营销与邮件营销**
- [ActiveCampaign Automation](./activecampaign-automation/) - 自动化 ActiveCampaign：联系人、交易、营销活动、列表和自动化。
- [Brevo Automation](./brevo-automation/) - 自动化 Brevo：联系人、邮件营销活动、交易邮件和列表。
- [ConvertKit Automation](./convertkit-automation/) - 自动化 ConvertKit (Kit)：订阅者、标签、序列、广播和表单。
- [Klaviyo Automation](./klaviyo-automation/) - 自动化 Klaviyo：个人资料、列表、细分、营销活动和事件。
- [Mailchimp Automation](./mailchimp-automation/) - 自动化 Mailchimp：受众、营销活动、模板、细分和报告。

**支持与服务台**
- [Freshdesk Automation](./freshdesk-automation/) - 自动化 Freshdesk：票务、联系人、代理、组和预设回复。
- [Freshservice Automation](./freshservice-automation/) - 自动化 Freshservice：票务、资产、变更、问题和服务中心目录。
- [Help Scout Automation](./helpdesk-automation/) - 自动化 Help Scout：对话、客户、邮箱和标签。
- [Zendesk Automation](./zendesk-automation/) - 自动化 Zendesk：票务、用户、组织、搜索和宏。

**电子商务与支付**
- [Shopify Automation](./shopify-automation/) - 自动化 Shopify：产品、订单、客户、库存和 GraphQL 查询。
- [Square Automation](./square-automation/) - 自动化 Square：支付、客户、目录、订单和位置。
- [Stripe Automation](./stripe-automation/) - 自动化 Stripe：扣款、客户、产品、订阅和退款。

**设计与协作**
- [Canva Automation](./canva-automation/) - 自动化 Canva：设计、模板、资产、文件夹和品牌工具包。
- [Confluence Automation](./confluence-automation/) - 自动化 Confluence：页面、空间、搜索、CQL、标签和版本。
- [DocuSign Automation](./docusign-automation/) - 自动化 DocuSign：信封、模板、签名和文档管理。
- [Figma Automation](./figma-automation/) - 自动化 Figma：文件、组件、评论、项目和团队管理。
- [Miro Automation](./miro-automation/) - 自动化 Miro：看板、便签、形状、连接器和项目。
- [Webflow Automation](./webflow-automation/) - 自动化 Webflow：CMS 集合、项目、站点、发布和资产。

**分析与数据**
- [Amplitude Automation](./amplitude-automation/) - 自动化 Amplitude：事件、用户群、用户属性和分析查询。
- [Google Analytics Automation](./google-analytics-automation/) - 自动化 Google Analytics：报告、维度、指标和属性管理。
- [Mixpanel Automation](./mixpanel-automation/) - 自动化 Mixpanel：事件、漏斗、用户群、注释和 JQL 查询。
- [PostHog Automation](./posthog-automation/) - 自动化 PostHog：事件、人物、功能标志、洞察和注释。
- [Segment Automation](./segment-automation/) - 自动化 Segment：源、目标、跟踪和仓库连接。

**人力资源**
- [BambooHR Automation](./bamboohr-automation/) - 自动化 BambooHR：员工、假期、报告和目录管理。

**自动化平台**
- [Make Automation](./make-automation/) - 自动化 Make (Integromat)：场景、连接和执行管理。

**Zoom 与会议**
- [Zoom Automation](./zoom-automation/) - 自动化 Zoom：会议、录制、参与者、网络研讨会和报告。

## 开始使用

### 在 Claude.ai 中使用技能

1. 在聊天界面中点击技能图标（🧩）。
2. 从市场添加技能或上传自定义技能。
3. Claude 会根据您的任务自动激活相关技能。

### 在 Claude Code 中使用技能

1. 将技能放入 `~/.config/claude-code/skills/`：
   ```bash
   mkdir -p ~/.config/claude-code/skills/
   cp -r skill-name ~/.config/claude-code/skills/
   ```

2. 验证技能元数据：
   ```bash
   head ~/.config/claude-code/skills/skill-name/SKILL.md
   ```

3. 启动 Claude Code：
   ```bash
   claude
   ```

4. 技能会自动加载并在相关时激活。

### 通过 API 使用技能

使用 Claude Skills API 以编程方式加载和管理技能：

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    skills=["skill-id-here"],
    messages=[{"role": "user", "content": "Your prompt"}]
)
```

详情请参阅 [Skills API 文档](https://docs.claude.com/en/api/skills-guide)。

## 创建技能

### 技能结构

每个技能都是一个包含 `SKILL.md` 文件的文件夹，带有 YAML 头信息：

```
skill-name/
├── SKILL.md          # 必需：技能说明和元数据
├── scripts/          # 可选：辅助脚本
├── templates/        # 可选：文档模板
└── resources/        # 可选：参考文件
```

### 基础技能模板

```markdown
---
name: my-skill-name
description: 清晰描述此技能的用途和使用时机。
---

# 我的技能名称

技能目的和功能的详细说明。

## 何时使用此技能

- 用例 1
- 用例 2
- 用例 3

## 说明

[关于 Claude 如何执行此技能的详细说明]

## 示例

[展示技能实际运作的真实世界示例]
```

### 技能最佳实践

- 专注于具体、可重复的任务
- 包含清晰的示例和边缘情况
- 为 Claude 编写说明，而非最终用户
- 在 Claude.ai、Claude Code 和 API 中测试
- 记录先决条件和依赖项
- 包含错误处理指导

## 贡献指南

我们欢迎贡献！请阅读我们的 [贡献指南](CONTRIBUTING.md) 了解详情：

- 如何提交新技能
- 技能质量标准
- 拉取请求流程
- 行为准则

### 快速贡献步骤

1. 确保您的技能基于真实用例
2. 检查现有技能中是否有重复
3. 遵循技能结构模板
4. 在各个平台上测试您的技能
5. 提交带有清晰文档的拉取请求

## 资源

### 官方文档

- [Claude Skills 概述](https://www.anthropic.com/news/skills) - 官方公告和功能
- [技能用户指南](https://support.claude.com/en/articles/12512180-using-skills-in-claude) - 如何在 Claude 中使用技能
- [创建自定义技能](https://support.claude.com/en/articles/12512198-creating-custom-skills) - 技能开发指南
- [Skills API 文档](https://docs.claude.com/en/api/skills-guide) - API 集成指南
- [Agent Skills 博客文章](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) - 工程深度解析

### 社区资源

- [Anthropics Skills 仓库](https://github.com/anthropics/skills) - 官方示例技能
- [Claude 社区](https://community.anthropic.com) - 与其他用户讨论技能
- [技能市场](https://claude.ai/marketplace) - 发现和分享技能

### 灵感与用例

- [Lenny's Newsletter](https://www.lennysnewsletter.com/p/everyone-should-be-using-claude-code) - 人们使用 Claude Code 的 50 种方式
- [Notion Skills](https://www.notion.so/notiondevs/Notion-Skills-for-Claude-28da4445d27180c7af1df7d8615723d0) - Notion 集成技能

## 加入社区

- [加入我们的 Discord](https://discord.com/invite/composio) - 与其他开发 Claude Skills 的开发者聊天
- [在 Twitter/X 上关注我们](https://x.com/composio) - 了解新技能和功能的最新动态
- 有问题？[support@composio.dev](mailto:support@composio.dev)

---

<p align="center">
  <b>加入 20,000+ 开发者的行列，构建并交付代理</b>
</p>

<p align="center">
  <a href="https://platform.composio.dev/?utm_source=Github&utm_content=AwesomeSkills">
    <img src="https://img.shields.io/badge/Get_Started_Free-4F46E5?style=for-the-badge" alt="Get Started"/>
  </a>
</p>

## 许可证

本仓库基于 Apache License 2.0 许可证。

各个技能可能有不同的许可证——请查看每个技能文件夹以了解具体的许可信息。

---

**注意**：Claude Skills 适用于 Claude.ai、Claude Code 和 Claude API。一旦创建了技能，它就可以在所有平台上移植，使您的工作流程在您使用 Claude 的任何地方都保持一致。

- [AgentsKB](https://agentskb.com) - 使用研究得到的答案升级您的 AI。我们做了研究，所以您的 AI 第一次就能做对。
