# datawebot MCP 服务中文翻译版

> 本项目是 [datawebot MCP server](https://github.com/datawebot/datawebot-mcp) 的中文翻译版本，隶属于 [awesome-skills-cn](https://github.com/lingxling/awesome-skills-cn) 项目。
>
> 原项目介绍：datawebot 是官方托管的 MCP 服务，同时提供一个 Agent Skill 和 Claude Code 插件，为 Agent 提供电商商品数据。
>
> 翻译说明：本翻译力求准确传达原项目内容，技能名称、工具名、命令、代码块、URL 和文件路径均保持英文原文，以确保技术准确性。品牌名 datawebot 按原文使用小写。
>
> - 原项目链接：[https://github.com/datawebot/datawebot-mcp](https://github.com/datawebot/datawebot-mcp)
> - 翻译项目（awesome-skills-cn）：[https://github.com/lingxling/awesome-skills-cn](https://github.com/lingxling/awesome-skills-cn)

---

让你的 Agent 告诉你：谁在卖这个商品、卖多少钱。datawebot 在全球的在线商店中查找商品，几秒钟内返回每个卖家的价格和直达链接。

- **服务地址：** `https://mcp.datawebot.com/mcp`（远程，Streamable HTTP）
- **登录：** 免费，通过邮件确认登录。无需密码，无需银行卡。
- **网站：** [datawebot.com](https://www.datawebot.com) · [Agent 文档](https://www.datawebot.com/docs/agents)

原仓库包含公开的连接信息、MCP Registry 条目（`server.json`，名称 `com.datawebot/datawebot`）、Cursor 插件清单、Claude Code 插件、Gemini CLI 扩展、一个 Agent Skill（`skills/datawebot/SKILL.md`）、Agent 安装说明（`llms-install.md`）以及可运行的示例。服务本身是托管的，无需安装任何东西。

## 当前功能

| 工具 | 返回内容 |
| --- | --- |
| `search_products` | 全球在线商店中在售的商品，支持当地语言：标题、价格、原价、商店、评分、评论数、图片、商品状况、链接和获取时间。可按国家筛选，也可选择限定商店域名。 |
| `get_product_offers` | 针对搜索结果中的一个商品：每个卖家的价格、含运费总价、配送说明、卖家评分，以及商品页面的直达链接。 |
| `discover` | 列出当前可用的所有工具，包括会话开始后新增的工具。请首先调用它。 |
| `list_job_blueprints`、`submit_job`、`get_job`、`get_results` | 数据提取任务（Jobs），覆盖 Amazon（10 个国家）的搜索结果页与商品页，以及 Allbirds、Ring、Arlo、ecobee、iFixit 等受支持的商店。所有账户均可使用：新账户有 200 个免费试用积分，更多积分可在 [控制台](https://www.datawebot.com/dashboard) 购买。当前列表请调用 `list_job_blueprints` 查看。 |

结果是尽力而为的快照，并附带获取时间。它们不是经过验证或保证最新的价格。datawebot 不存储价格历史、不运行定时检查、不发送提醒；需要保留的数据由你的 Agent 或脚本自行保存。

每个账户每天有免费额度，每次响应都会报告剩余额度。

## 连接

### Claude（claude.ai 和 Claude 桌面版）

设置 → Connectors → **Add custom connector** → URL 填 `https://mcp.datawebot.com/mcp` → Connect，然后确认 datawebot 发来的邮件。

### ChatGPT

添加一个自定义 MCP 服务，URL 为 `https://mcp.datawebot.com/mcp`，认证方式选择 OAuth（需要允许自定义 MCP 服务的套餐和工作区）。

### Claude Code

安装 datawebot 插件，它会添加 MCP 服务和 datawebot 技能。在 Claude Code 会话中：

```text
/plugin install datawebot --marketplace datawebot/datawebot-mcp
```

Claude Code 2.1.275 之前的版本，请先添加 marketplace 再安装：

```text
/plugin marketplace add datawebot/datawebot-mcp
/plugin install datawebot@datawebot
```

然后运行 `/mcp`，选择 `datawebot` 并确认登录邮件。如果只想添加 MCP 服务而不安装插件：

```bash
claude mcp add --transport http datawebot https://mcp.datawebot.com/mcp
```

或者告诉任何带 shell 的编程 Agent：`set up https://mcp.datawebot.com/setup.md`。它会读取该文件、询问你的邮箱并自行保存密钥，因此不会有密钥被粘贴到对话中。

### Gemini CLI

```bash
gemini extensions install https://github.com/datawebot/datawebot-mcp
```

该扩展会添加 MCP 服务、一个简短的 `GEMINI.md` 上下文文件和 datawebot 技能。启动 `gemini`，服务会在首次使用时要求登录；也可以运行 `/mcp auth datawebot` 并确认 datawebot 发来的邮件。

### Cursor

在原仓库 README 顶部点击 **Add to Cursor**，或将以下链接粘贴到浏览器：

```
cursor://anysphere.cursor-deeplink/mcp/install?name=datawebot&config=eyJ1cmwiOiJodHRwczovL21jcC5kYXRhd2Vib3QuY29tL21jcCJ9
```

原仓库本身也是一个 Cursor 插件（`.cursor-plugin/plugin.json` 和 `mcp.json`）。也可以手动添加到 `~/.cursor/mcp.json` 或 `.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "datawebot": { "url": "https://mcp.datawebot.com/mcp" }
  }
}
```

### VS Code

在原仓库 README 顶部点击 **Install in VS Code**，或添加到 `.vscode/mcp.json`：

```json
{
  "servers": {
    "datawebot": { "type": "http", "url": "https://mcp.datawebot.com/mcp" }
  }
}
```

### Cline

**MCP Servers → Remote Servers**：Server Name 填 `datawebot`，Server URL 填 `https://mcp.datawebot.com/mcp`，Transport Type 选 **Streamable HTTP** → **Add Server**，然后在该服务上点击 **Authenticate** 并确认 datawebot 发来的邮件。如果直接编辑配置文件，请使用 `"type": "streamableHttp"`（不写的话 Cline 会使用旧的 SSE）：

```json
{
  "mcpServers": {
    "datawebot": { "type": "streamableHttp", "url": "https://mcp.datawebot.com/mcp" }
  }
}
```

会替你安装服务的 Agent（例如 Cline）可以按照 [`llms-install.md`](https://github.com/datawebot/datawebot-mcp/blob/main/llms-install.md) 操作。

### LM Studio

在原仓库 README 顶部点击 **Add to LM Studio**（LM Studio 0.3.17 或更高版本），或打开以下链接：

```
lmstudio://add_mcp?name=datawebot&config=eyJ1cmwiOiJodHRwczovL21jcC5kYXRhd2Vib3QuY29tL21jcCJ9
```

它会将 `{"url": "https://mcp.datawebot.com/mcp"}` 添加到 LM Studio 的 `mcp.json`。

### Replit

[Add to Replit](https://replit.com/integrations?mcp=eyJkaXNwbGF5TmFtZSI6ImRhdGF3ZWJvdCIsImJhc2VVcmwiOiJodHRwczovL21jcC5kYXRhd2Vib3QuY29tL21jcCJ9)，然后点击 **Test & save** 并确认 datawebot 发来的登录邮件。

### Agent 技能

[`skills/datawebot/SKILL.md`](skills/datawebot/SKILL.md)（中文版：[`SKILL_CN.md`](skills/datawebot/SKILL_CN.md)）遵循 [Agent Skills](https://agentskills.io) 格式，教 Agent 掌握 datawebot 的工作流程：搜索、卖家报价、提取任务、积分和错误处理。Claude Code 插件和 Gemini CLI 扩展已包含该技能；其他支持技能的 Agent 可将 `skills/datawebot` 文件夹复制到其技能目录。

### 脚本、n8n 和 Agent 框架（API 密钥）

无法完成邮件登录的工具使用 API 密钥。在 [datawebot.com/dashboard](https://www.datawebot.com/dashboard) 登录 → **API keys**，创建一个密钥（有效期 30 天、90 天或 1 年），并通过请求头发送：

```
Authorization: Bearer <your API key>
```

任何可以带请求头调用远程 MCP 服务的客户端都可以使用，例如 n8n 的 MCP Client 工具、LangChain 的 `langchain-mcp-adapters`、OpenAI Agents SDK、Vercel AI SDK 和 CrewAI。请将密钥保存在环境变量或工具的凭据存储中，不要写进代码。

## 示例

- [`examples/python-price-tracker`](https://github.com/datawebot/datawebot-mcp/tree/main/examples/python-price-tracker)：一个用纯 Python（仅标准库）编写的商品篮价格追踪器，由脚本自己把带日期的记录存入 SQLite 并报告变化。

## 支持

发送邮件至 [hello@datawebot.com](mailto:hello@datawebot.com)，或在原仓库中提交 issue。

## 隐私

参见 [隐私政策](https://www.datawebot.com/privacy)。

## 许可证

原仓库中的示例和文档采用 MIT 许可证。托管服务的使用受 [服务条款](https://www.datawebot.com/terms) 约束。
