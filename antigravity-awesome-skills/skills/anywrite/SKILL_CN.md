---
name: anywrite
description: "编译的 CLI 涵盖 Anytype 本地 API 的全部 52 个端点——对象、属性、标签、搜索、聊天、文件——一个二进制文件，无需 MCP 服务器。"
category: productivity
risk: critical
source: community
source_repo: Antheurus/anywrite
source_type: community
date_added: "2026-07-15"
author: Antheurus
tags: [anytype, cli, pkm, notes, api-integration, productivity, knowledge-management]
tools: [claude, cursor, gemini, codex]
license: "MIT"
license_source: "https://github.com/Antheurus/anywrite/blob/main/LICENSE"
plugin:
  targets:
    codex: blocked
    claude: blocked
  setup:
    type: manual
    summary: "需要在显式绝对路径上单独安装且经用户批准的 anywrite 可执行文件。"
    docs: SKILL.md
---

# anywrite

## 概述

`anywrite` 是 [Anytype](https://anytype.io) 桌面应用程序本地 HTTP API 的单个编译 Bun/TypeScript CLI——**全部 52 个端点**，跨越空间、对象、属性、标签、类型、模板、列表、聊天、文件、成员、搜索和身份验证——作为一个二进制文件，零运行时依赖。它作为 Anytype 官方 MCP 服务器的低上下文替代存在：而不是向每个代理会话公开 52 个始终加载的工具，`anywrite` 是一个正常的 CLI，作为技能连接，在实际调用之前代价为零上下文，并且可从终端或任何脚本同样使用。

## 何时使用此技能

- 当用户提到 Anytype 或要求创建、更新、搜索或组织笔记、任务或 PKM 对象时使用。
- 在使用 Anytype 空间、属性、标签、类型、模板或列表（集和集合）时使用。
- 当用户要求将文件上传到空间、在空间内聊天或以编程方式读取/写入结构化对象时使用。

## 工作原理

### 步骤 1：确保 Anytype 桌面正在运行并已认证

此存储库不附带 `anywrite` 可执行文件。用户必须在当前工作区外安装或构建经过审查的上游版本，并提供其显式绝对路径。使用前，验证该路径是可执行的常规文件，不是符号链接，不是工作区相对的 `dist/` 工件。永远不要从正在处理的存储库自动发现或执行 `./dist/anywrite`。

Anytype 桌面应用程序必须在本地运行（默认 `http://localhost:31009`）。认证一次：

```bash
"/absolute/path/to/anywrite" auth --status        # 显示已配置是/否以及密钥来自何处
"/absolute/path/to/anywrite" auth                 # 质询流程——在应用中显示一个 4 位代码
"/absolute/path/to/anywrite" auth --code 1234     # 相同交换的非交互形式
```

密钥被写入 `~/.anywrite/config.json`，任何命令都不会打印。

### 步骤 2：调用资源 + 操作

```
anywrite <resource> <action> [positionals] [--flag value]
```

资源：`spaces`、`objects`、`properties`、`tags`、`types`、`templates`、`lists`、`files`、`members`、`search`、`chat`、`auth`。输出默认为 JSON；添加 `--pretty` 以获得人类视图，`--json` 作为任何类型标志尚未建模的逃生舱。`space`/`type`/`property` 正值接受名称或 id——名称自动解析为 id。

## 示例

### 示例 1：创建和更新对象

```bash
"/absolute/path/to/anywrite" objects create <space> --type task --name "Buy milk"
"/absolute/path/to/anywrite" objects update <space> <object_id> --status "Done"
```

### 示例 2：搜索和上传文件

```bash
"/absolute/path/to/anywrite" search global --query "task" --types task
"/absolute/path/to/anywrite" files upload <space> --file ./image.png
```

### 示例 3：读取聊天消息

```bash
"/absolute/path/to/anywrite" chat messages <space> <chat_id> --all
```

## 最佳实践

- ✅ 传递 `space`/`type`/`property` 的名称并让 CLI 将它们解析为 id。
- ✅ 使用默认 JSON 输出进行脚本编制，使用 `--pretty` 进行人类审查。
- ✅ 当品牌新的 API 字段尚未被类型标志覆盖时伸手拿 `--json`。
- ❌ 不要设置空字符串表情符号 `--icon`；改为完全省略该标志。
- ❌ 不要期望 `lists add`/`remove` 在集上工作——它们仅适用于集合。

## 限制

- 此技能不能替代环境特定的验证、测试或专家审核。
- 如果缺少必需的输入、权限或安全边界，请停止并要求澄清。
- 受 Anytype 本地 API 本身的限制：无块级编辑（body 仅是整个 markdown 替换）、无成员邀请/角色管理、无模板创建/更新/删除、无空间删除。
- 对象主体字段在创建时命名为 `--body`，但在更新时命名为 `--markdown`。

## 安全与安全说明

- API 密钥存储在本地的 `~/.anywrite/config.json` 中，任何命令（包括 `auth --status`）都不会打印。
- 运行时配置优先级：`ANYTYPE_API_KEY` 环境变量，然后是 `~/.anywrite/config.json`，然后是对现有 `~/.anytype-cli/config.yaml` 的只读回退。
- 所有操作都针对本地运行的 Anytype 桌面实例；没有数据被发送到第三方服务器。
- 删除在任何地方都是软存档并是幂等的——重复删除保持 `200`，永远不会 `410`。

## 常见陷阱

- **问题：** `lists add`/`remove` 在集上无声地什么都不做。
  **解决方案：** 这些仅适用于集合，不适用于集。
- **问题：** 重新上传相同的文件返回现有对象 id 而不是新的。
  **解决方案：** 这是有意的——文件上传按内容哈希去重。
- **问题：** 聊天消息不像其他所有内容那样分页。
  **解决方案：** 聊天按光标分页；其他所有资源按偏移分页。

## 相关技能

- `@docx` - 当可交付成果是 Word 文档而不是 Anytype 对象时。
