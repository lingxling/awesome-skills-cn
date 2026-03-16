---
name: connect
description: 将 Claude 连接到任何应用程序。发送电子邮件、创建问题、发布消息、更新数据库 - 在 Gmail、Slack、GitHub、Notion 和 1000+ 服务上采取实际行动。
---

# Connect

将 Claude 连接到任何应用程序。停止生成关于你可以做什么的文本 - 实际去做。

## 何时使用此技能

当你需要 Claude 执行以下操作时使用此技能：

- **发送邮件**而不是起草邮件
- **创建问题**而不是描述问题
- **发布消息**而不是建议消息
- **更新数据库**而不是解释如何更新

## 变化

| 没有 Connect | 有 Connect |
|-----------------|--------------|
| "这里是一封草稿邮件..." | 发送邮件 |
| "你应该创建一个问题..." | 创建问题 |
| "将此发布到 Slack..." | 发布它 |
| "将此添加到 Notion..." | 添加它 |

## 支持的应用

**1000+ 集成**包括：

- **邮件**：Gmail、Outlook、SendGrid
- **聊天**：Slack、Discord、Teams、Telegram
- **开发**：GitHub、GitLab、Jira、Linear
- **文档**：Notion、Google Docs、Confluence
- **数据**：Sheets、Airtable、PostgreSQL
- **CRM**：HubSpot、Salesforce、Pipedrive
- **存储**：Drive、Dropbox、S3
- **社交**：Twitter、LinkedIn、Reddit

## 设置

### 1. 获取 API 密钥

在 [platform.composio.dev](https://platform.composio.dev/?utm_source=Github&utm_content=AwesomeSkills) 获取你的免费密钥

### 2. 设置环境变量

```bash
export COMPOSIO_API_KEY="your-key"
```

### 3. 安装

```bash
pip install composio          # Python
npm install @composio/core    # TypeScript
```

完成。Claude 现在可以连接到任何应用程序。

## 示例

### 发送邮件
```
Email sarah@acme.com - Subject: "Shipped!" Body: "v2.0 is live, let me know if issues"
```

### 创建 GitHub 问题
```
Create issue in my-org/repo: "Mobile timeout bug" with label:bug
```

### 发布到 Slack
```
Post to #engineering: "Deploy complete - v2.4.0 live"
```

### 链式操作
```
Find GitHub issues labeled "bug" from this week, summarize, post to #bugs on Slack
```

## 工作原理

使用 Composio Tool Router：

1. **你请求** Claude 做某事
2. **Tool Router 找到**正确的工具（1000+ 选项）
3. **OAuth 自动处理**
4. **操作执行**并返回结果

### 代码

```python
from composio import Composio
from claude_agent_sdk.client import ClaudeSDKClient
from claude_agent_sdk.types import ClaudeAgentOptions
import os

composio = Composio(api_key=os.environ["COMPOSIO_API_KEY"])
session = composio.create(user_id="user_123")

options = ClaudeAgentOptions(
    system_prompt="You can take actions in external apps.",
    mcp_servers={
        "composio": {
            "type": "http",
            "url": session.mcp.url,
            "headers": {"x-api-key": os.environ["COMPOSIO_API_KEY"]},
        }
    },
)

async with ClaudeSDKClient(options) as client:
    await client.query("Send Slack message to #general: Hello!")
```

## 认证流程

首次使用应用程序：
```
要发送电子邮件，我需要 Gmail 访问权限。
在此授权：https://...
完成后说"已连接"。
```

之后连接会持续存在。

## 框架支持

| 框架 | 安装 |
|-----------|---------|
| Claude Agent SDK | `pip install composio claude-agent-sdk` |
| OpenAI Agents | `pip install composio openai-agents` |
| Vercel AI | `npm install @composio/core @composio/vercel` |
| LangChain | `pip install composio-langchain` |
| 任何 MCP 客户端 | 使用 `session.mcp.url` |

## 故障排除

- **需要认证** → 点击链接，授权，说"已连接"
- **操作失败** → 检查目标应用中的权限
- **找不到工具** → 具体说明："Slack #general" 而不是 "发送消息"

---

<p align="center">
  <b>加入 20,000+ 开发人员构建能够交付的代理</b>
</p>

<p align="center">
  <a href="https://platform.composio.dev/?utm_source=Github&utm_content=AwesomeSkills">
    <img src="https://img.shields.io/badge/Get_Started_Free-4F46E5?style=for-the-badge" alt="Get Started"/>
  </a>
</p>