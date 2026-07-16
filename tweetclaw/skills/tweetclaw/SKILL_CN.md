---
name: tweetclaw
description: "TweetClaw 的中文学习说明。TweetClaw 是 @xquik/tweetclaw OpenClaw 插件，用于安全执行 X/Twitter 搜索、回复搜索、发推、回复、关注者导出、用户查询、媒体处理、私信、监控、webhook 和抽奖。"
homepage: https://xquik.com
license: MIT-0
---

# TweetClaw

TweetClaw 是 Xquik 提供的 OpenClaw 插件，用于把 X/Twitter 自动化接入代理工作流。

```bash
openclaw plugins install @xquik/tweetclaw
```

安装后即使还没有配置凭据，也可以使用 `explore` 免费浏览端点目录。真实 Xquik API 调用需要 Xquik API 凭据或 MPP 签名凭据。

## 什么时候使用

当用户需要以下任务时使用 TweetClaw：

- 搜索推文或搜索推文回复
- 发布推文、发布回复或删除推文
- 点赞、转推、关注或取关
- 发送 X/Twitter 私信
- 上传媒体并带图发推
- 查询用户资料、用户推文、喜欢列表或媒体时间线
- 查看书签、通知、时间线或私信历史
- 批量导出关注者、回复、引用、互动用户或社群成员
- 从推文回复或互动中运行抽奖
- 监控账号新活动并发送 webhook
- 查询 X/Twitter 趋势、文章、列表和社群内容

不要把 TweetClaw 用作浏览器里的 X/Twitter 操作工具、广告管理工具或计划发布系统。

## 安全规则

只在用户授权的 X/Twitter 工作流中使用 TweetClaw。不要用于垃圾信息、骚扰、冒充、欺骗性互动、凭据收集、规避平台限制、批量未请求私信，或批量关注、点赞、转推活动。

在任何公开可见、会修改状态、会产生费用或会重复执行的动作前，先总结精确目标、账号、动作、文本、媒体、范围和可能的费用，再等待用户明确确认。此规则适用于发推、回复、删除、点赞、转推、关注、取关、私信、修改资料、上传媒体、创建 webhook、创建监控、运行抽奖和启动批量导出。

读取书签、通知、时间线、私信、已连接账号和用量等账号级数据前，确认用户拥有或被授权访问该账号。展示结果时避免泄露凭据和敏感个人数据。

批量导出、抽奖或监控请求默认使用较小范围。说明请求范围、结果上限和通知行为。用户扩大范围、变更目标或要求持续监控时，需要重新确认。

发布内容前展示最终文本和媒体列表。不要添加用户没有要求的链接、话题、提及或事实主张。

MPP 模式仅用于只读端点。只有 MPP 配置时，不要尝试发推、回复、私信、上传、监控、webhook、账号资料修改或其他账号级写入。

## 配置

推荐通过环境变量把凭据写入 OpenClaw 插件配置，避免把凭据粘贴到聊天、文档、shell 历史或 issue 中。

### Xquik API 凭据模式

从 [dashboard.xquik.com](https://dashboard.xquik.com/) 创建凭据后配置：

```bash
openclaw config set plugins.entries.tweetclaw.config.apiKey "$XQUIK_API_KEY"
```

### MPP 只读按次付费模式

MPP 可以在没有 Xquik 账号的情况下访问只读端点。签名凭据只保存在本地配置中，用于签名支付证明。

```bash
npm i mppx viem
openclaw config set plugins.entries.tweetclaw.config.tempoSigningKey "$MPP_SIGNING_KEY"
```

只在自托管兼容 API 时修改 `baseUrl`，并且必须使用 HTTPS URL。

## 工具

### `explore`

读取本地端点目录，不发起网络请求。适合先查找可用端点、参数和响应结构。

### `tweetclaw`

调用目录内允许的 Xquik API 端点。代理选择端点并提供路径参数、查询参数和 JSON body，运行时负责注入凭据并返回解析后的 JSON。

限制：

- 只能调用目录中列出的端点
- 只能访问配置的 HTTPS Xquik 兼容 API base URL
- 不能执行任意命令
- 不能访问文件系统
- 不能访问任意第三方网络

如果代理能看到技能但不能调用工具，将 `explore` 和 `tweetclaw` 加入 OpenClaw 工具 allowlist：

```bash
openclaw config set tools.alsoAllow '["explore", "tweetclaw"]'
```

## 命令

| 命令 | 作用 |
| --- | --- |
| `/xstatus` | 查看账号信息、订阅状态、用量和余额 |
| `/xtrends` | 查看趋势主题 |
| `/xtrends tech` | 查看技术分类趋势 |

## 常见工作流

### 搜索推文

```text
用户：搜索关于 AI agents 的推文
代理：先用 explore 找到搜索端点，再用 tweetclaw 查询结果
```

### 发布推文

```text
用户：发一条推文说 Hello from TweetClaw!
代理：展示账号和最终文本，等用户确认后发布
```

### 回复推文

```text
用户：回复这条推文说 Great thread!
代理：确认 tweet ID、账号和回复文本后发布回复
```

### 导出关注者

```text
用户：导出 @example 最近 1000 个关注者
代理：说明目标、数量和范围，确认后创建导出任务
```

### 运行抽奖

```text
用户：从这条推文的回复里抽 3 位获奖者
代理：确认推文、过滤条件和获奖人数后创建抽奖
```

### 创建监控

```text
用户：监控 @example 的新推文、回复和转推
代理：确认目标账号、事件类型和轮询行为后创建监控
```

## 文档

- [TweetClaw GitHub](https://github.com/Xquik-dev/tweetclaw)
- [npm 包 @xquik/tweetclaw](https://www.npmjs.com/package/@xquik/tweetclaw)
- [Skills.sh 页面](https://skills.sh/xquik-dev/tweetclaw)
- [Xquik API 文档](https://docs.xquik.com)
- [OpenClaw](https://github.com/openclaw/openclaw)
