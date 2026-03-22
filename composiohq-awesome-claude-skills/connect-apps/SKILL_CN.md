---
name: connect-apps
description: 将 Claude 连接到 Gmail、Slack、GitHub 等外部应用程序。当用户想要发送电子邮件、创建问题、发布消息或在外部服务中采取行动时，使用此技能。
---

# 连接应用

将 Claude 连接到 1000+ 个应用程序。实际发送电子邮件、创建问题、发布消息 - 而不仅仅是生成关于它的文本。

## 快速开始

### 步骤 1：安装插件

```
/plugin install composio-toolrouter
```

### 步骤 2：运行设置

```
/composio-toolrouter:setup
```

这将：
- 询问你的免费 API 密钥（在 [platform.composio.dev](https://platform.composio.dev/?utm_source=Github&utm_content=AwesomeSkills) 获取）
- 配置 Claude 与 1000+ 个应用程序的连接
- 大约需要 60 秒

### 步骤 3：尝试一下！

设置后，重启 Claude Code 并尝试：

```
Send me a test email at YOUR_EMAIL@example.com
```

如果成功，你已连接！

## 你可以做什么

| 请 Claude... | 会发生什么 |
|------------------|--------------|
| "Send email to sarah@acme.com about the launch" | 实际发送邮件 |
| "Create GitHub issue: fix login bug" | 创建问题 |
| "Post to Slack #general: deploy complete" | 发布消息 |
| "Add meeting notes to Notion" | 添加到 Notion |

## 支持的应用

**邮件**：Gmail、Outlook、SendGrid
**聊天**：Slack、Discord、Teams、Telegram
**开发**：GitHub、GitLab、Jira、Linear
**文档**：Notion、Google Docs、Confluence
**数据**：Sheets、Airtable、PostgreSQL
**以及 1000+ 更多...**

## 工作原理

1. 你要求 Claude 做某事
2. Composio Tool Router 找到正确的工具
3. 第一次使用？你将通过 OAuth 授权（一次性）
4. 操作执行并返回结果

## 故障排除

- **"Plugin not found"** → 确保你运行了 `/plugin install composio-toolrouter`
- **"Need to authorize"** → 点击 Claude 提供的 OAuth 链接，然后说 "done"
- **Action failed** → 检查你在目标应用中有权限

---

<p align="center">
  <b>加入 20,000+ 开发人员构建能够交付的代理</b>
</p>

<p align="center">
  <a href="https://platform.composio.dev/?utm_source=Github&utm_content=AwesomeSkills">
    <img src="https://img.shields.io/badge/Get_Started_Free-4F46E5?style=for-the-badge" alt="Get Started"/>
  </a>
</p>