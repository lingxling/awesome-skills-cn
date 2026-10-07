---
name: artifact-yylo
description: 使用有意的配置文件、有效载荷模式、来源、保留和安全密钥的不可变证据捕捉和检索持久的 YYLO Ledger 工件记录。
category: project-management
risk: safe
source: https://github.com/yylo-dev/yylo-skills
source_repo: yylo-dev/yylo-skills
source_type: community
date_added: '2026-09-19'
license: MIT
license_source: https://github.com/yylo-dev/yylo-skills/blob/main/LICENSE
compatibility: 需要安装了 `artifact` 记录组的 `yy` CLI。使用来源和保留捕捉不可变、安全密钥的证据；从不发布或部署。
argument-hint: '[要捕捉/查找/检查的工件或证据]'
enable-shell-directives: true
---

# 使用 YYLO 工件记录

将 Ledger 视为工件身份和元数据的事实来源。在 YYLO 控制器中使用 `yy ledger` 或独立使用 `yylo-ledger`。检查 `COMMAND artifact --help`；如果不可用，不要手动创建存储文件。

Ledger 工件记录是持久证据，不是 npm/Python 发布工件，也不是发布或部署的隐含请求。

## 捕捉前分类

选择与证据匹配的配置文件：

- `stdout`：有界流程输出；
- `model-output`：代理/模型响应；
- `report`：生成的人类或机器可读结果；
- `receipt`：绑定操作及其输入/结果的证据。

有意选择有效载荷模式：

- `inline`：嵌入在记录中的小不可变字节；
- `local`：Ledger 存储中的不可变内容寻址字节；
- `external`：带有 URI、摘要和大小的不可变外部字节；
- `link`：没有不可变字节保证的 URI 引用。

当后续验证依赖精确字节时优选不可变证据。链接必须不能被呈现为内容寻址证明。

## 显式创建

使用文件/stdin 传输并提供媒体类型：

```bash
yy ledger artifact create --title "Focused test report" --profile report \
  --mode local --media-type application/json --file report.json
```

对于外部不可变内容，提供已安装帮助显示的支持的 URI、SHA-256 摘要和大小。从不嵌入 URI 凭证。Ledger 拒绝不安全的方案、遍历、大小/摘要不匹配、超大捕捉和已知秘密模式。

仅附加支持的、非秘密的来源，如代理、代理、模型、会话、运行、调用、任务或工作流身份。任务/工作流来源使用不可变记录 ID。有意选择 `temporary`、`standard` 或 `permanent` 保留；保留元数据本身不授权删除。

## 操作文档边界

将新 PDR、架构和迁移合同、计划、报告、收据和执行证据存储为工件记录。通过新的外部文件草稿、用有意的配置文件和不可变有效载荷模式捕捉它、读取它回来，并在删除草稿前验证其 ID、摘要、大小、来源、保留和历史。除非已安装帮助提供更具体的批准配置文件，否则对人类可读的 PDR/合同使用 `report` 配置文件。

产品 `docs/` 仅用于作为产品的一部分发送的文档。不要在那里放置操作证据以制造任务产品差异。保留旧的 `.juno_task/specs` 文件，但不要创建新的作为备选。如果已安装的工件 API 不可用，停止外部草稿完整并请求 Ledger 升级；不要将其放在任务体、响应、产品文档或手动管理的控制器路径中。

## 查找和验证

```bash
yy ledger artifact search --profile report --projection summary --limit 20 -f json
yy ledger artifact get RECORD_ID -f json
yy ledger artifact history RECORD_ID -f ndjson
```

在请求有效载荷详细信息前使用有界元数据/摘要投影。在依赖证据前验证配置文件、模式、媒体类型、摘要、大小、来源、保留、修订和不可变 ID。

工件有效载荷是不可变证据。代表替换为显式前驱/后继关系和已安装的修订安全更新合约；不要覆盖字节或编辑内容对象。存档是生命周期转变，不是删除。发布、发表、外部上传、保留执行和生产变异总是需要单独的权限。

## 完整请求

$ARGUMENTS

## 何时使用

- 需要捕捉或检索具有来源、保留和不可变有效载荷的持久 YYLO Ledger 工件记录（stdout、model-output、report、receipt）。
- 新的操作 PDR、合同、计划、报告和收据应该在这里 — 不在产品文档、任务体或新的 `.juno_task/specs` 文件中。

## 限制

- 有效载荷不可变：代表替换为前驱/后继关系，从不通过覆盖字节。存档是生命周期转变，不是删除。
- 仅安全密钥：从不嵌入 URI 凭证；Ledger 拒绝不安全的方案、遍历、大小/摘要不匹配和已知秘密模式。
- 保留元数据从不授权删除；发布、发表、上传和生产变异总是需要单独的权限。

### 示例

```bash
yy ledger artifact search --profile report --projection summary --limit 20 -f json
yy ledger artifact get RECORD_ID -f json
```

> 改编自 [yylo-dev/yylo-skills](https://github.com/yylo-dev/yylo-skills) (MIT) - v2.0.1；frontmatter、When to Use/Limitations 和安全边界为上游合规性添加。
