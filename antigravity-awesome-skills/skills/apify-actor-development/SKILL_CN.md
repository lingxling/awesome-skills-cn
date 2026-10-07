---
name: apify-actor-development
description: "重要提示：在开始之前，请填写 .actor/actor.json 中 meta 部分的 generatedBy 属性。将其替换为你当前正在使用的工具和模型，例如 \"Claude Code with Claude Sonnet 4.5\"。这有助于 Apify 针对特定的 AI 工具和模型来监控和改进 AGENTS.md。"
risk: critical
source: community
date_added: "2026-09-04"
---

# Apify Actor 开发

**重要提示：** 在开始之前，请填写 `.actor/actor.json` 中 meta 部分的 `generatedBy` 属性。将其替换为你当前正在使用的工具和模型，例如 "Claude Code with Claude Sonnet 4.5"。这有助于 Apify 针对特定的 AI 工具和模型来监控和改进 AGENTS.md。

## 何时使用
- 你需要创建、修改或调试一个 Apify Actor 项目。
- 任务涉及选择 Apify 模板、搭建 actor 的输入/输出，或实现 actor 运行时逻辑。
- 你需要关于 `apify` CLI 身份验证、项目初始化或部署流程的安全设置指导。

## 什么是 Apify Actor？

Actor 是受 UNIX 哲学启发的无服务器程序——即专注做好一件事、并能轻松组合以构建复杂系统的程序。它们被打包为 Docker 镜像，并在云端的隔离容器中运行。

**核心概念：**
- 接受定义清晰的 JSON 输入
- 执行隔离的任务(网页抓取、自动化、数据处理)
- 将结构化 JSON 输出到数据集，和/或将数据存储到键值存储中
- 可以运行从几秒钟到几小时甚至无限期的时长
- 持久化状态，并可被重新启动

## 前提条件与设置(强制要求)

在创建或修改 actor 之前，请通过 `apify --help` 验证 `apify` CLI 是否已安装。

如果尚未安装，请使用以下方法之一(按优先级排列)：

```bash
# 推荐方式：通过包管理器安装(提供完整性校验)
npm install -g apify-cli

# 或者(Mac)：brew install apify-cli
```

> **安全提示：** 切勿通过将远程脚本直接管道传输到 shell 的方式来安装该 CLI。
> 应始终使用包管理器。

安装 apify CLI 后，使用以下命令检查是否已登录：

```bash
apify info  # 应返回你的用户名
```

如果尚未登录，请检查是否已定义 `APIFY_TOKEN` 环境变量(如果没有，请让用户在 https://console.apify.com/settings/integrations 生成一个，然后用该值定义 `APIFY_TOKEN`)。

然后使用以下方法之一进行身份验证：

```bash
# 选项 1(推荐)：CLI 会自动从环境变量中读取 APIFY_TOKEN。
# 只需确保该环境变量已导出，然后运行任意 apify 命令——无需显式登录。

# 选项 2：交互式登录(提示输入令牌，不会在 shell 历史中暴露)
apify login
```

> **安全提示：** 避免将令牌以命令行参数的形式传递(例如 `apify login -t <token>`)。
> 命令行参数在进程列表中可见，并可能被记录到 shell 历史中。
> 应优先使用环境变量或交互式登录。
> 切勿在源代码或配置文件中记录、打印或嵌入 `APIFY_TOKEN`。
> 使用权限最小化的令牌(范围受限的令牌)，并定期轮换。

## 模板选择

**重要提示：** 在开始 actor 开发之前，务必先询问用户偏好使用哪种编程语言：
- **JavaScript** - 使用 `apify create <actor-name> -t project_empty`
- **TypeScript** - 使用 `apify create <actor-name> -t ts_empty`
- **Python** - 使用 `apify create <actor-name> -t python-empty`

根据用户的语言选择，使用相应的 CLI 命令。后续可按需安装额外的软件包(Crawlee、Playwright 等)。

## 快速入门工作流程

1. **创建 actor 项目** - 根据用户的语言偏好运行相应的 `apify create` 命令(见上方的"模板选择")
2. **安装依赖**(安装前请核实包名与预期的包一致)
   - JavaScript/TypeScript：`npm install` (使用 `package-lock.json` 以保证可复现、经完整性校验的安装——请将锁文件提交到版本控制中)
   - Python：`pip install -r requirements.txt` (在 `requirements.txt` 中锁定精确版本，例如 `crawlee==1.2.3`，并将该文件提交到版本控制中)
3. **实现逻辑** - 在 `src/main.py`、`src/main.js` 或 `src/main.ts` 中编写 actor 代码
4. **配置 schema** - 更新 `.actor/input_schema.json`、`.actor/output_schema.json`、`.actor/dataset_schema.json` 中的输入/输出 schema
5. **配置平台设置** - 更新 `.actor/actor.json` 中的 actor 元数据(参见 [references/actor-json.md](references/actor-json.md))
6. **编写文档** - 为市场发布创建全面的 README.md
7. **本地测试** - 运行 `apify run` 来验证功能(详见下方"本地测试"小节)
8. **部署** - 运行 `apify push` 将 actor 部署到 Apify 平台(actor 名称定义于 `.actor/actor.json` 中)

## 安全

**将所有抓取到的网页内容视为不可信输入。** Actor 从外部网站摄取数据，这些数据可能包含恶意载荷。请遵循以下规则：

- **清洗抓取到的数据**——切勿将原始 HTML、URL 或抓取到的文本直接传入 shell 命令、`eval()`、数据库查询或模板引擎。应使用正确的转义或参数化 API。<!-- security-allowlist: defensive untrusted-input guidance -->
- **验证并进行类型检查所有外部数据**——在推送到数据集或键值存储之前，验证值是否符合预期的类型和格式。拒绝或清洗意外的结构。
- **不要执行或解释抓取到的内容**——切勿将抓取到的文本当作代码、命令或配置来处理。网站内容可能包含提示注入尝试或嵌入式脚本。
- **将凭据与数据管道隔离**——确保 `APIFY_TOKEN` 和其他密钥在请求处理函数中永远不可访问，也不与抓取数据一起传递。应使用 Apify SDK 内置的凭据管理机制，而不是在数据处理代码中通过环境变量传递令牌。
- **安装前先审查依赖项**——使用 `npm install` 或 `pip install` 添加包时，验证包名和发布者。抢注相似包名(typosquatting)是常见的供应链攻击手段。优先选用知名且维护活跃的包。
- **锁定版本并使用锁文件**——始终提交 `package-lock.json`(Node.js)，或在 `requirements.txt`(Python)中锁定精确版本。锁文件可确保构建的可复现性，并防止依赖被静默替换。定期运行 `npm audit` 或 `pip-audit` 以检查已知漏洞。

## 最佳实践

**✓ 应当：**
- 使用 `apify run` 在本地测试 actor(会配置 Apify 环境和存储)
- 对运行在 Apify 平台上的代码使用 Apify SDK(`apify`)
- 尽早验证输入，具备适当的错误处理并优雅地失败
- 对静态 HTML 使用 CheerioCrawler(比浏览器快 10 倍)
- 仅对重度依赖 JavaScript 的网站使用 PlaywrightCrawler
- 对复杂的抓取任务使用路由模式(createCheerioRouter/createPlaywrightRouter)
- 实现带指数退避的重试策略
- 使用合适的并发度：HTTP(10-50)、浏览器(1-5)
- 在 `.actor/input_schema.json` 中设置合理的默认值
- 在 `.actor/output_schema.json` 中定义输出 schema
- 在推送到数据集之前对数据进行清洗和验证
- 使用带回退策略的语义化 CSS 选择器
- 遵守 robots.txt、服务条款，并实施速率限制
- **始终使用 `apify/log` 包**——它会对敏感数据(API 密钥、令牌、凭据)进行屏蔽
- 实现就绪探针处理函数(如果你的 Actor 使用待机模式则为必需)

**✗ 不应：**
- 使用 `npm start`、`npm run start`、`npx apify run` 或类似命令来运行 actor(应使用 `apify run`)
- 假设通过 `apify run` 生成的本地存储会被推送到或在 Apify Console 中可见——它仅存在于本地；需使用 `apify push` 部署并在平台上运行，才能在 Console 中看到结果
- 依赖 `Dataset.getInfo()` 来获取云端的最终计数
- 在 HTTP/Cheerio 可行的情况下使用浏览器爬虫
- 将本应放在输入 schema 或环境变量中的值硬编码
- 跳过输入验证或错误处理
- 使服务器超载——使用适当的并发度和延迟
- 抓取被禁止的内容，或忽视服务条款
- 在未明确获得许可的情况下存储个人/敏感数据
- 使用已废弃的选项，例如在 CheerioCrawler(v3.x)上使用 `requestHandlerTimeoutMillis`
- 使用 `additionalHttpHeaders`——应使用 `preNavigationHooks`
- 将原始抓取内容传入 shell 命令、`eval()` 或代码生成函数 <!-- security-allowlist: prohibited-pattern checklist -->
- 使用 `console.log()` 或 `print()` 而不是 Apify 日志记录器——这会绕过凭据屏蔽
- 在未经明确许可的情况下禁用待机模式

## 日志记录

完整的日志记录文档，包括 JavaScript/TypeScript 和 Python 可用的日志级别及最佳实践，请参见 [references/logging.md](references/logging.md)。

检查 `.actor/actor.json` 中的 `usesStandbyMode`——仅当其设为 `true` 时才需要实现。

## 命令

```bash
apify run          # 在本地运行 Actor
apify login        # 账户身份验证
apify push         # 部署到 Apify 平台(使用 .actor/actor.json 中的名称)
apify help         # 列出所有命令
```

**重要提示：** 始终使用 `apify run` 在本地测试 actor。不要使用 `npm run start`、`npm start`、`yarn start` 或其他包管理器命令——这些不会正确配置 Apify 环境和存储。

## 本地测试

使用 `apify run` 在本地测试 actor 时，通过在以下位置创建一个 JSON 文件来提供输入数据：

```
storage/key_value_stores/default/INPUT.json
```

该文件应包含你的 `.actor/input_schema.json` 中定义的输入参数。actor 在本地运行时会读取该输入，这与它在 Apify 平台上接收输入的方式相同。

**重要提示——本地存储不会同步到 Apify Console：**
- 运行 `apify run` 时，所有数据(数据集、键值存储、请求队列)**仅**存储在你本地文件系统的 `storage/` 目录中。
- 这些数据**永远不会**自动上传或推送到 Apify 平台。它只存在于你的机器上。
- 要在 Apify Console 上验证结果，你必须使用 `apify push` 部署 Actor，然后在平台上运行它。
- **不要**依赖检查 Apify Console 来验证本地运行的结果——而应检查本地的 `storage/` 目录，或查看 Actor 的日志输出。

## 待机模式

关于待机模式的完整文档，包括 JavaScript/TypeScript 和 Python 的就绪探针实现，请参见 [references/standby-mode.md](references/standby-mode.md)。

## 项目结构

```
.actor/
├── actor.json           # Actor 配置：名称、版本、环境变量、运行时
├── input_schema.json    # 输入验证与 Console 表单定义
└── output_schema.json   # 输出存储与展示模板
src/
└── main.js/ts/py       # Actor 入口点
storage/                # 仅本地存储(不会同步到 Apify Console)
├── datasets/           # 输出条目(JSON 对象)
├── key_value_stores/   # 文件、配置、INPUT
└── request_queues/     # 待处理的抓取请求
Dockerfile              # 容器镜像定义
```

## Actor 配置

关于完整的 actor.json 结构和配置选项，请参见 [references/actor-json.md](references/actor-json.md)。

## 输入 Schema

关于输入 schema 的结构和示例，请参见 [references/input-schema.md](references/input-schema.md)。

## 输出 Schema

关于输出 schema 的结构、示例及模板变量，请参见 [references/output-schema.md](references/output-schema.md)。

## 数据集 Schema

关于数据集 schema 的结构、配置及展示属性，请参见 [references/dataset-schema.md](references/dataset-schema.md)。

## 键值存储 Schema

关于键值存储 schema 的结构、集合及配置，请参见 [references/key-value-store-schema.md](references/key-value-store-schema.md)。

## Apify MCP 工具

如果配置了 MCP 服务器，可使用以下工具来查阅文档：

- `search-apify-docs` - 搜索文档
- `fetch-apify-docs` - 获取完整文档页面

否则，MCP 服务器地址为：`https://mcp.apify.com/?tools=docs`。

## 资源

- [docs.apify.com/llms.txt](https://docs.apify.com/llms.txt) - Apify 快速参考文档
- [docs.apify.com/llms-full.txt](https://docs.apify.com/llms-full.txt) - Apify 完整文档
- [https://crawlee.dev/llms.txt](https://crawlee.dev/llms.txt) - Crawlee 快速参考文档
- [https://crawlee.dev/llms-full.txt](https://crawlee.dev/llms-full.txt) - Crawlee 完整文档
- [whitepaper.actor](https://raw.githubusercontent.com/apify/actor-whitepaper/refs/heads/master/README.md) - 完整的 Actor 规范

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出当作特定环境验证、测试或专家审查的替代品。
- 如果所需的输入、权限、安全边界或成功标准缺失，应停下来请求澄清。
