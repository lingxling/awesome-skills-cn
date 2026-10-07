---
name: agentmail
description: 面向 AI 智能体的邮件基础设施。通过 AgentMail API 创建账户、发送/接收邮件、管理 Webhook,并查询信誉值(karma)余额。
risk: safe
source: community
date_added: "2026-09-04"
---

# AgentMail — 面向 AI 智能体的邮件服务

AgentMail 通过一套 REST API,为 AI 智能体提供真实的电子邮箱地址(`@theagentmail.net`)。智能体可以发送和接收邮件、注册各类服务(GitHub、AWS、Slack 等),并获取验证码。一套信誉值(karma)系统可以防止垃圾邮件,维持共享域名的良好信誉。

基础 URL:`https://api.theagentmail.net`

## 何时使用
- AI 智能体需要一个真实的收发件箱,用于注册、验证流程或事务性通信。
- 你需要开通 AgentMail 账户、发送消息、读取收件箱内容,或注册入站 Webhook。
- 你需要监控 karma 使用情况,或将邮件事件接入智能体自动化流程。

## 快速开始

所有请求都需要携带 `Authorization: Bearer am_...` 请求头(来自控制台的 API 密钥)。

### 创建一个邮件账户(-10 karma)

```bash
curl -X POST https://api.theagentmail.net/v1/accounts \
  -H "Authorization: Bearer am_..." \
  -H "Content-Type: application/json" \
  -d '{"address": "my-agent@theagentmail.net"}'
```

响应:`{"data": {"id": "...", "address": "my-agent@theagentmail.net", "displayName": null, "createdAt": 123}}`

### 发送邮件(-1 karma)

```bash
curl -X POST https://api.theagentmail.net/v1/accounts/{accountId}/messages \
  -H "Authorization: Bearer am_..." \
  -H "Content-Type: application/json" \
  -d '{
    "to": ["recipient@example.com"],
    "subject": "Hello from my agent",
    "text": "Plain text body",
    "html": "<p>Optional HTML body</p>"
  }'
```

可选字段:`cc`、`bcc`(字符串数组)、`inReplyTo`、`references`(用于邮件线程串联的字符串)、`attachments`(`{filename, contentType, content}` 对象的数组,其中 content 为 base64 编码)。

### 读取收件箱

```bash
# 列出消息
curl https://api.theagentmail.net/v1/accounts/{accountId}/messages \
  -H "Authorization: Bearer am_..."

# 获取完整消息(含正文和附件)
curl https://api.theagentmail.net/v1/accounts/{accountId}/messages/{messageId} \
  -H "Authorization: Bearer am_..."
```

### 查询 karma

```bash
curl https://api.theagentmail.net/v1/karma \
  -H "Authorization: Bearer am_..."
```

响应:`{"data": {"balance": 90, "events": [...]}}`

### 注册 Webhook(实时入站通知)

```bash
curl -X POST https://api.theagentmail.net/v1/accounts/{accountId}/webhooks \
  -H "Authorization: Bearer am_..." \
  -H "Content-Type: application/json" \
  -d '{"url": "https://my-agent.example.com/inbox"}'
```

Webhook 投递包含两个安全头:
- `X-AgentMail-Signature` —— 对请求正文的 HMAC-SHA256 十六进制摘要,使用 Webhook 密钥签名
- `X-AgentMail-Timestamp` —— 投递发送时的毫秒级时间戳

验证签名,并拒绝时间戳超过 5 分钟的请求,以防止重放攻击:

```typescript
import { createHmac } from "crypto";

const verifyWebhook = (body: string, signature: string, timestamp: string, secret: string) => {
  if (Date.now() - Number(timestamp) > 5 * 60 * 1000) return false;
  return createHmac("sha256", secret).update(body).digest("hex") === signature;
};
```

### 下载附件

```bash
curl https://api.theagentmail.net/v1/accounts/{accountId}/messages/{messageId}/attachments/{attachmentId} \
  -H "Authorization: Bearer am_..."
```

返回 `{"data": {"url": "https://signed-download-url..."}}`。

## 完整 API 参考

| 方法 | 路径 | 说明 | Karma |
|--------|------|-------------|-------|
| POST | `/v1/accounts` | 创建邮件账户 | -10 |
| GET | `/v1/accounts` | 列出所有账户 | |
| GET | `/v1/accounts/:id` | 获取账户详情 | |
| DELETE | `/v1/accounts/:id` | 删除账户 | +10 |
| POST | `/v1/accounts/:id/messages` | 发送邮件 | -1 |
| GET | `/v1/accounts/:id/messages` | 列出消息 | |
| GET | `/v1/accounts/:id/messages/:msgId` | 获取完整消息 | |
| GET | `/v1/accounts/:id/messages/:msgId/attachments/:attId` | 获取附件 URL | |
| POST | `/v1/accounts/:id/webhooks` | 注册 Webhook | |
| GET | `/v1/accounts/:id/webhooks` | 列出 Webhook | |
| DELETE | `/v1/accounts/:id/webhooks/:whId` | 删除 Webhook | |
| GET | `/v1/karma` | 获取余额 + 事件记录 | |

## Karma 系统

每个操作都有一个 karma 成本或奖励:

| 事件 | Karma | 原因 |
|---|---|---|
| `money_paid` | +100 | 购买额度 |
| `email_received` | +2 | 来自可信域名的回复 |
| `account_deleted` | +10 | 删除地址时返还 karma |
| `email_sent` | -1 | 发送邮件消耗 karma |
| `account_created` | -10 | 创建地址消耗 karma |

**重要规则:**
- Karma 只会因来自可信服务商(Gmail、Outlook、Yahoo、iCloud、ProtonMail、Fastmail、Hey 等)的入站邮件而获得。来自未知/临时域名的邮件不会获得 karma。
- 在智能体回复之前,同一个发件人只能让你获得一次 karma。如果发件人 X 在没有收到回复的情况下给你发了 5 次邮件,只有第一封能获得 karma。回复 X 后,X 的下一封邮件会再次获得 karma。
- 删除账户会返还创建该账户时花费的 10 点 karma。

当 karma 降到 0 时,发送邮件和创建账户会返回 HTTP 402。在执行会消耗 karma 的操作之前,务必先检查余额。

## TypeScript SDK

```typescript
import { createClient } from "@agentmail/sdk";

const mail = createClient({ apiKey: "am_..." });

// 创建账户
const account = await mail.accounts.create({
  address: "my-agent@theagentmail.net",
});

// 发送邮件
await mail.messages.send(account.id, {
  to: ["human@example.com"],
  subject: "Hello",
  text: "Sent by an AI agent.",
});

// 读取收件箱
const messages = await mail.messages.list(account.id);
const detail = await mail.messages.get(account.id, messages[0].id);

// 附件
const att = await mail.attachments.getUrl(accountId, messageId, attachmentId);
// att.url 是一个带签名的下载链接

// Webhook
await mail.webhooks.create(account.id, {
  url: "https://my-agent.example.com/inbox",
});

// Karma
const karma = await mail.karma.getBalance();
console.log(karma.balance);
```

## 错误处理

```typescript
import { AgentMailError } from "@agentmail/sdk";

try {
  await mail.messages.send(accountId, { to: ["a@b.com"], subject: "Hi", text: "Hey" });
} catch (e) {
  if (e instanceof AgentMailError) {
    console.log(e.status);   // 402、404、401 等
    console.log(e.code);     // "INSUFFICIENT_KARMA"、"NOT_FOUND" 等
    console.log(e.message);
  }
}
```

## 常见模式

### 注册某个服务并读取验证邮件

```typescript
const account = await mail.accounts.create({
  address: "signup-bot@theagentmail.net",
});

// 使用该地址进行注册(浏览器自动化、API 等)

// 轮询验证邮件
for (let i = 0; i < 30; i++) {
  const messages = await mail.messages.list(account.id);
  const verification = messages.find(m =>
    m.subject.toLowerCase().includes("verify") ||
    m.subject.toLowerCase().includes("confirm")
  );
  if (verification) {
    const detail = await mail.messages.get(account.id, verification.id);
    // 从 detail.bodyText 或 detail.bodyHtml 中解析验证链接/验证码
    break;
  }
  await new Promise(r => setTimeout(r, 2000));
}
```

### 发送邮件并等待回复

```typescript
const sent = await mail.messages.send(account.id, {
  to: ["human@company.com"],
  subject: "Question about order #12345",
  text: "Can you check the status?",
});

for (let i = 0; i < 60; i++) {
  const messages = await mail.messages.list(account.id);
  const reply = messages.find(m =>
    m.direction === "inbound" && m.timestamp > sent.timestamp
  );
  if (reply) {
    const detail = await mail.messages.get(account.id, reply.id);
    // 处理回复
    break;
  }
  await new Promise(r => setTimeout(r, 5000));
}
```

## 类型

```typescript
type Account = { id: string; address: string; displayName: string | null; createdAt: number };
type Message = { id: string; from: string; to: string[]; subject: string; direction: "inbound" | "outbound"; status: string; timestamp: number };
type MessageDetail = Message & { cc: string[] | null; bcc: string[] | null; bodyText: string | null; bodyHtml: string | null; inReplyTo: string | null; references: string | null; attachments: AttachmentMeta[] };
type AttachmentMeta = { id: string; filename: string; contentType: string; size: number };
type KarmaBalance = { balance: number; events: KarmaEvent[] };
type KarmaEvent = { id: string; type: string; amount: number; timestamp: number; metadata?: Record<string, unknown> };
```

## 局限性
- 仅在任务明确符合上述范围时使用此技能。
- 不要将输出当作特定环境验证、测试或专家审查的替代品。
- 如果所需的输入、权限、安全边界或成功标准缺失,应停下来并请求澄清。
