---
name: apify-actorization
description: "Actorization 将现有软件转换为与 Apify 平台兼容的可重用无服务器应用程序。Actor 是打包为 Docker 镜像的程序，接受明确定义的 JSON 输入、执行操作并可选地生成结构化 JSON 输出。"
risk: critical
source: community
date_added: "2026-09-04"
---

# Apify Actorization

Actorization 将现有软件转换为与 Apify 平台兼容的可重用无服务器应用程序。Actor 是打包为 Docker 镜像的程序，接受明确定义的 JSON 输入、执行操作并可选地生成结构化 JSON 输出。

## 快速入门

1. 在项目根目录中运行 `apify init`
2. 使用 SDK 生命周期包装代码（请参见下面的语言特定部分）
3. 配置 `.actor/input_schema.json`
4. 使用 `apify run --input '{"key": "value"}'` 进行测试
5. 使用 `apify push` 部署

## 何时使用此技能

- 将现有项目转换为在 Apify 平台上运行
- 向项目添加 Apify SDK 集成
- 将 CLI 工具或脚本包装为 Actor
- 将 Crawlee 项目迁移到 Apify

## 先决条件

验证是否安装了 `apify` CLI：

```bash
apify --help
```

如果未安装：

```bash
brew install apify-cli

# 或: npm install -g apify-cli
# 或从您的操作系统包管理器验证的官方发布包中安装
```

验证 CLI 是否已登录：

```bash
apify info  # 应返回您的用户名
```

如果未登录，检查是否定义了 `APIFY_TOKEN` 环境变量。如果没有，要求用户在 https://console.apify.com/settings/integrations 生成一个，将其添加到他们的 shell 或秘密管理器而不在命令历史记录中放置字面令牌，然后运行：

```bash
apify login
```

## Actorization 检查清单

复制此检查清单以跟踪进度：

- [ ] 步骤 1：分析项目（语言、入口点、输入、输出）
- [ ] 步骤 2：运行 `apify init` 创建 Actor 结构
- [ ] 步骤 3：应用特定于语言的 SDK 集成
- [ ] 步骤 4：配置 `.actor/input_schema.json`
- [ ] 步骤 5：配置 `.actor/output_schema.json`（如适用）
- [ ] 步骤 6：更新 `.actor/actor.json` 元数据
- [ ] 步骤 7：使用 `apify run` 进行本地测试
- [ ] 步骤 8：使用 `apify push` 部署

## 步骤 1：分析项目

在进行更改之前，先了解项目：

1. **识别语言** - JavaScript/TypeScript、Python 或其他
2. **找到入口点** - 开始执行的主文件
3. **识别输入** - 命令行参数、环境变量、配置文件
4. **识别输出** - 文件、控制台输出、API 响应
5. **检查状态** - 是否需要在运行之间持久化数据？

## 步骤 2：初始化 Actor 结构

在项目根目录中运行：

```bash
apify init
```

这将创建：
- `.actor/actor.json` - Actor 配置和元数据
- `.actor/input_schema.json` - Apify 控制台的输入定义
- `Dockerfile`（如果不存在）- 容器镜像定义

## 步骤 3：应用语言特定的更改

根据项目的语言进行选择：

- **JavaScript/TypeScript**：请参见 [js-ts-actorization.md](references/js-ts-actorization.md)
- **Python**：请参见 [python-actorization.md](references/python-actorization.md)
- **其他语言（基于 CLI）**：请参见 [cli-actorization.md](references/cli-actorization.md)

### 快速参考

| 语言 | 安装 | 包装代码 |
|----------|---------|-----------|
| JS/TS | `npm install apify` | `await Actor.init()` ... `await Actor.exit()` |
| Python | `pip install apify` | `async with Actor:` |
| 其他 | 在包装脚本中使用 CLI | `apify actor:get-input` / `apify actor:push-data` |

## 步骤 4-6：配置模式

请参见 [schemas-and-output.md](references/schemas-and-output.md) 以详细配置：
- 输入模式（`.actor/input_schema.json`）
- 输出模式（`.actor/output_schema.json`）
- Actor 配置（`.actor/actor.json`）
- 状态管理（请求队列、键值存储）

根据 `@apify/json_schemas` npm 包验证模式。

## 步骤 7：本地测试

使用内联输入运行 actor（适用于 JS/TS 和 Python actor）：

```bash
apify run --input '{"startUrl": "https://example.com", "maxItems": 10}'
```

或使用输入文件：

```bash
apify run --input-file ./test-input.json
```

**重要：** 始终使用 `apify run`，而不是 `npm start` 或 `python main.py`。CLI 会设置正确的环境和存储。

## 步骤 8：部署

```bash
apify push
```

这会在 Apify 平台上上传并构建您的 actor。

## 货币化（可选）

部署后，您可以在 Apify Store 中使用您的 actor 进行货币化。推荐的模式是**按事件付费 (PPE)**：

- 每个结果/抓取的项
- 每页已处理
- 每个 API 调用

在 Apify 控制台中的 Actor > 货币化下配置 PPE。在代码中使用 `await Actor.charge('result')` 对事件收费。

其他选项：**租赁**（月度订阅）或**免费**（开源）。

## 部署前检查清单

- [ ] `.actor/actor.json` 存在，名称和描述正确
- [ ] `.actor/actor.json` 针对 `@apify/json_schemas`（`actor.schema.json`）进行验证
- [ ] `.actor/input_schema.json` 定义所有必需的输入
- [ ] `.actor/input_schema.json` 针对 `@apify/json_schemas`（`input.schema.json`）进行验证
- [ ] `.actor/output_schema.json` 定义输出结构（如适用）
- [ ] `.actor/output_schema.json` 针对 `@apify/json_schemas`（`output.schema.json`）进行验证
- [ ] `Dockerfile` 存在且构建成功
- [ ] `Actor.init()` / `Actor.exit()` 包装主代码 (JS/TS)
- [ ] `async with Actor:` 包装主代码 (Python)
- [ ] 输入通过 `Actor.getInput()` / `Actor.get_input()` 读取
- [ ] 输出使用 `Actor.pushData()` 或键值存储
- [ ] `apify run` 使用测试输入成功执行
- [ ] `generatedBy` 在 actor.json 元部分中设置

## Apify MCP 工具

如果配置了 MCP 服务器，请使用这些工具进行文档：

- `search-apify-docs` - 搜索文档
- `fetch-apify-docs` - 获取完整的文档页面

否则，MCP 服务器 URL：`https://mcp.apify.com/?tools=docs`。

## 资源

- [Actorization Academy](https://docs.apify.com/academy/actorization) - 综合指南
- [Apify SDK for JavaScript](https://docs.apify.com/sdk/js) - 完整 SDK 参考
- [Apify SDK for Python](https://docs.apify.com/sdk/python) - 完整 SDK 参考
- [Apify CLI 参考](https://docs.apify.com/cli) - CLI 命令
- [Actor 规范](https://raw.githubusercontent.com/apify/actor-whitepaper/refs/heads/master/README.md) - 完整规范

## 限制
- 仅在任务明确与上述描述的范围相匹配时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并寻求澄清。
