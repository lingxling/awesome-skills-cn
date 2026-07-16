# TweetClaw 中文学习版

[TweetClaw](https://github.com/Xquik-dev/tweetclaw) 是 Xquik 提供的 OpenClaw 插件，用于在代理工作流中执行结构化 X/Twitter 自动化。它面向需要搜索推文、搜索推文回复、发布推文、发布回复、导出关注者、查询用户、处理媒体、发送私信、监控推文、发送 webhook 和运行抽奖的场景。

## 安装

OpenClaw 插件运行时使用 npm 包作为 canonical 安装来源：

```bash
openclaw plugins install @xquik/tweetclaw
```

代理技能目录也可以通过 Skills.sh 发现 TweetClaw：

```bash
npx skills add xquik-dev/tweetclaw
```

ClawHub 页面可以用于浏览插件信息，但 npm 包是当前推荐的安装来源。

## 主要能力

- 搜索推文和搜索推文回复
- 发布推文和发布推文回复
- 导出关注者、关注中账号和验证关注者
- 查询用户资料、用户推文、媒体时间线和互动列表
- 上传媒体、下载已授权媒体并创建图库链接
- 发送 X/Twitter 私信
- 创建监控和 webhook，把新推文、回复、引用或转推通知到代理上下文
- 根据回复或互动数据运行抽奖
- 查询趋势、文章、列表、社群和书签等只读数据

## 配置方式

TweetClaw 可以先安装，后配置。未配置凭据时，免费的 `explore` 工具仍可浏览端点目录；真实 API 调用会返回设置提示。

常用配置方式：

1. 在 [dashboard.xquik.com](https://dashboard.xquik.com/) 创建 Xquik API 凭据。
2. 通过环境变量写入 OpenClaw 插件配置，避免把凭据粘贴到聊天或文档中。

```bash
openclaw config set plugins.entries.tweetclaw.config.apiKey "$XQUIK_API_KEY"
```

如果只需要匿名按次付费读取，可以配置 MPP 签名凭据。MPP 仅用于只读端点，不支持发推、回复、私信、监控、webhook、上传或资料修改。

```bash
npm i mppx viem
openclaw config set plugins.entries.tweetclaw.config.tempoSigningKey "$MPP_SIGNING_KEY"
```

## 工具

TweetClaw 注册 2 个结构化工具：

| 工具 | 作用 |
| --- | --- |
| `explore` | 免费读取本地端点目录，不发起网络请求 |
| `tweetclaw` | 调用目录内允许的 Xquik API 端点 |

`tweetclaw` 是可选工具。如果代理能看到技能文档但不能调用工具，可以将工具名加入 OpenClaw allowlist：

```bash
openclaw config set tools.alsoAllow '["explore", "tweetclaw"]'
```

安装或更新后可以检查运行时注册：

```bash
openclaw plugins inspect tweetclaw --runtime
openclaw skills info tweetclaw
```

## 安全边界

- 对任何公开可见、会修改状态、会产生费用或会重复执行的动作，都先向用户确认目标账号、动作、内容、媒体和范围。
- 发推、回复、删除、点赞、转推、关注、取关、私信、上传媒体、创建监控、创建 webhook、运行抽奖和启动批量导出前必须获得明确确认。
- 读取书签、通知、时间线、私信、已连接账号或用量等账号级数据前，确认用户有权访问该账号。
- 不要在聊天、日志、文档、错误输出或 issue 中展示凭据。
- MPP 模式只用于只读端点。只有 MPP 配置时，不要执行写入、上传、私信、监控、webhook 或账号修改。

## 常见工作流

### 搜索推文

```text
用户：搜索关于 AI agents 的推文
代理：用 explore 查找搜索端点，再用 tweetclaw 调用搜索接口
```

### 发布推文

```text
用户：发一条推文说 Hello from TweetClaw!
代理：展示最终文本和账号，等待确认后调用 tweetclaw 发布
```

### 搜索回复并抽奖

```text
用户：从这条推文的回复里随机抽 3 位获奖者
代理：确认推文、过滤条件、人数和范围后创建抽奖
```

### 监控账号

```text
用户：监控 @example 的新推文和回复
代理：确认目标、事件类型和轮询行为后创建监控
```

## 相关链接

- [TweetClaw GitHub](https://github.com/Xquik-dev/tweetclaw)
- [npm 包 @xquik/tweetclaw](https://www.npmjs.com/package/@xquik/tweetclaw)
- [Skills.sh 页面](https://skills.sh/xquik-dev/tweetclaw)
- [Xquik 平台](https://xquik.com)
- [Xquik API 文档](https://docs.xquik.com)
- [OpenClaw](https://github.com/openclaw/openclaw)

## 许可证

TweetClaw 主仓库使用 MIT 许可证。打包的技能文档使用 MIT-0 许可证。
