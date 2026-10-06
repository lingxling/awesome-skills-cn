---
name: paperzilla
description: 通过 pz CLI 读取 Paperzilla 中的项目，搜索项目动态，并获取推荐内容和经典论文。支持最近的推荐、论文详情、基于 markdown 的摘要、推荐反馈、JSON 导出以及 Atom feed URL。
license: MIT
compatibility: Requires the pz CLI, network access, and a Paperzilla account with CLI access. Source builds require Go 1.23 or later.
metadata:
  version: "1.2"
  skill-author: Paperzilla Inc
  upstream-version: "pz 0.7.1"
  last-reviewed: "2026-10-01"
---

# Paperzilla

当你想要与你的代理讨论 Paperzilla 中的项目、推荐内容和经典论文时，使用此技能。

## 你可以询问的内容

- "给我项目 X 的最新推荐。"
- "打开推荐 Y 并解释它为什么重要。"
- "以 markdown 格式获取经典论文 Z 并总结它。"
- "告诉我这篇论文与我的研究有何相关性。"
- "显示项目 X 的动态（feed）。"
- "对某条推荐留下反馈。"
- "将此论文、推荐或动态导出为 JSON。"

这是核心的 Paperzilla 技能。它让你的代理可以直接访问 Paperzilla 数据，但不强制规定工作流程或外部交付集成。

## 访问方式

使用官方的 `pz` CLI。此技能针对**0.7.1**版本，已对照
官方发行版源码和二进制文件进行了核实。命令示例中使用了占位 ID；请
将其替换为你的账户返回的实际记录。CLI 的行为已针对本地模拟服务器
测试，而非经认证的 Paperzilla 账户。

先运行 `pz --version`，然后列出项目、选择一个项目、浏览或搜索
其动态，并查看选定的推荐内容。在总结或导出时，请将项目推荐
与底层的经典论文区分开来。

## 安装

### macOS
```bash
brew install paperzilla-ai/tap/pz
```

如果 Homebrew 6 或更高版本将此 formula 视为不受信任而拒绝，官方指南建议使用
`brew trust --formula paperzilla-ai/tap/pz`，然后重试安装。只信任
该 formula。安装和升级命令已通过文档核实，但在此次审查中未实际
执行。

### Windows（Scoop）
```bash
scoop bucket add paperzilla-ai https://github.com/paperzilla-ai/scoop-bucket
scoop install pz
```

### Linux
使用官方 Linux 安装指南：

- https://docs.paperzilla.ai/guides/cli-getting-started

### 从源码构建（Go 1.23+）
有关源码构建，请参阅 CLI 存储库：

- https://github.com/paperzilla-ai/pz

## 更新

检查你的 CLI 是否最新，并获取针对特定安装方式的升级步骤：

```bash
pz update
```

如果检测结果不明确，请显式覆盖：

```bash
pz update --install-method homebrew
pz update --install-method scoop
pz update --install-method release
pz update --install-method source
```

支持的值为 `auto`、`homebrew`、`scoop`、`release` 和 `source`。

## 身份验证

```bash
pz login
```

登录会向账户邮箱发送一次性验证码，并将会话本地保存。请在运行
JSON 导出之前以交互方式完成登录：缺失或过期的凭证可能会在 stdout
上触发登录提示。CLI 会自动检查账户访问权限并刷新令牌；请报告
访问/升级错误，而不要将其当作空动态处理。

**版本相关的差异：** 在线指南描述了匿名访问经典论文的方式，但
0.7.1 版本的二进制文件即使对 `pz paper` 也要求登录并进行 CLI 访问
检查。其后续的经典论文 HTTP 请求使用的是一个公共路由。不要为
此版本承诺匿名的 CLI 工作流程。

## CLI 参考

如果当前配置使用 `pz`，以下是核心命令。

### 列出项目
```bash
pz project list
pz project list --json
```

### 显示单个项目
```bash
pz project <project-id>
pz project <project-id> --json
```

列表的 JSON 是一个包含 `id`、`name`、`mode` 和 `visibility` 的数组。
单个项目的 JSON 还包括关键词、关注的来源和分类。

### 浏览项目动态

```bash
pz feed <project-id>
```

有用的标志：
- `--must-read`
- `--since YYYY-MM-DD`
- `--limit N`
- `--offset N`（要跳过的结果数，从零开始计数）
- `--json`
- `--atom`

示例：
```bash
pz feed <project-id> --must-read --since 2026-03-01 --limit 5
pz feed <project-id> --limit 20 --offset 20 --json
pz feed <project-id> --json
pz feed <project-id> --atom
```

`--since` 筛选的是推荐内容准备就绪的时间，而不是论文的发表日期。
浏览的 JSON 包含 `items`、`total`、`limit` 和 `offset`。一条命令
只获取一页；它不会自动导出整个动态。请保留相同的
筛选条件，根据收到的条目数从返回的 offset 继续前进，并在遇到
空页或达到返回的 total 时停止。如果实时动态在翻页期间发生变化，
请按推荐 ID 去重。

动态输出可以包含现有的推荐反馈标记：

- `[↑]` 点赞
- `[↓]` 点踩
- `[★]` 星标

### 搜索完整的项目动态

```bash
pz feed search --project-id <project-id> --query "latent retrieval" --json
pz feed search --project-id <project-id> --query "retrieval" --feedback-filter starred --must-read --limit 20 --offset 20 --json
```

搜索会在整个项目动态范围内对结果进行排序。请使用一个经过修剪的、
长度为 3–200 字符的查询，以及一个正的 `--limit`（最多 100）。`--offset`
必须为非负数。反馈筛选器有 `all`、`unrated`、`liked`、`disliked`、`starred`、
`not-relevant` 和 `low-quality`；这些带连字符的筛选器与下面带下划线的
点踩原因不同。搜索不接受 `--since`。

搜索的 JSON 包含 `items`、`limit`、`offset`、`has_more` 以及 `query`，但没有
确切的 total。只在 `has_more` 为 true 时才请求下一个 offset，并保持
查询和筛选条件不变。如果出现不一致的空页，请停止并报告，而不要
无限循环。第二个示例展示了后续的一页。

### 阅读一篇经典论文
```bash
pz paper <paper-id>
pz paper <paper-id> --json
pz paper <paper-id> --markdown
pz paper <paper-id> --project <project-id>
```

### 从你的某个项目打开一条推荐
```bash
pz rec <project-paper-id>
pz rec <project-paper-id> --json
pz rec <project-paper-id> --markdown
```

### 留下推荐反馈
```bash
pz feedback <project-paper-id> upvote
pz feedback <project-paper-id> star
pz feedback <project-paper-id> downvote --reason not_relevant
pz feedback clear <project-paper-id>
```

反馈会更改账户数据；只在用户要求此更改时才使用它。
点踩原因为 `not_relevant` 或 `low_quality`，且 `--reason` 仅适用
于点踩操作。添加 `--json` 可获取反馈对象；清除反馈会返回
`{"project_paper_ref": "...", "cleared": true}`。`clear` 是一个
位于推荐 ID 之前的子命令。

## 将论文和推荐的身份区分开来

一个经典的 `paper-id` 标识一篇论文；一个 `project-paper-id` 标识它在
某个项目中的推荐。请从返回的记录中获取这两者，并在导出结果时
保留项目关联。对 `rec` 和反馈操作使用推荐 ID，即使同一篇论文
出现在多个项目中也是如此。在动态的 JSON 中，`items[].id`/`items[].short_id`
是推荐标识符；`items[].paper.id`/`items[].paper.short_id` 是经典论文
标识符。不要从 DOI 或经典论文 ID 推断推荐 ID。参见
[官方 CLI 文档](https://github.com/paperzilla-ai/pz)。

当 markdown 仍在准备中时，请报告该状态，并仅总结实际返回的
元数据或摘要。重试消息不是完整正文的证据。

## 输出与自动化

- 完成登录后，优先使用 `--json` 进行机器解析。`paper` 和 `rec`
  拒绝将 `--json` 与 `--markdown` 组合使用。
- `pz paper --markdown` 只有在 markdown 已经准备好时才返回它。
- `pz rec --markdown` 以及项目范围内的 `pz paper --project ... --markdown`
  可能会将 markdown 生成任务排队。待处理消息可能以成功状态退出；请在
  将 stdout 视为完整正文之前检查其内容。避免立即重复重试，
  并报告待处理状态。
- `--atom` 返回一个供订阅阅读器使用的个人动态 URL，并可能创建一个
  动态令牌。任何持有该 URL 的人都可以读取该动态；请不要将其令牌
  记录在日志、公开报告和存储库中。它不会返回 Atom XML 或页面 JSON，
  浏览筛选条件也不会应用于生成的 URL。
- 相关性评分表示的是项目匹配度，而不是科学有效性或效应量
  估计。请标注摘要使用的是元数据、摘要（abstract）还是实际的
  markdown 正文。缺少 PDF URL 并不意味着不存在来源落地页。

## 配置

```bash
export PZ_API_URL="https://paperzilla.ai"
```

默认值已经指向 Paperzilla；只有在使用受信任的服务或本地测试服务器时
才更改它。经认证的请求会将会话凭证发送到该地址。
`PZ_TOKENS_PATH` 可选地指定一个会话文件；默认情况下 CLI 使用
`~/.paperzilla/tokens.json`。切勿将该文件作为研究数据导出。

关于请求路由、响应结构、分页以及文档/源码之间的差异，参见
[已验证的 CLI 契约](references/cli-contracts.md)。

## 参考资料

- 文档：https://docs.paperzilla.ai/guides/cli
- 快速入门：https://docs.paperzilla.ai/guides/cli-getting-started
- 仓库：https://github.com/paperzilla-ai/pz
