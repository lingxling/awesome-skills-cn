---
name: ai-image-generation-studio
description: "安装并使用官方 AI Image Generator 软件包（按摘要固定版本），用于 Beatra 服务上的付费托管工作。"
category: media
risk: critical
source: community
source_repo: beatra-ai/ai-image-generator-skill
source_type: official
date_added: "2026-09-18"
author: beatra-ai
tags: [image-generation, text-to-image, mcp, paid-api, beatra]
tools: [claude, codex, cursor, gemini]
license: "MIT-0"
license_source: "https://github.com/beatra-ai/ai-image-generator-skill/blob/13c7b9b2a2197fb91deb6a3a1466124db620c3d1/LICENSE"
---

# AI Image Generator Skill

## 概述

在 Claude Code、Codex 或 OpenClaw 内部生成、合成和编辑产品图片、品牌视觉、海报、社交图形、插画和照片变体。这些工作在托管的付费 Beatra 服务（`mcp.beatra.ai`）上完成。

此目录条目是一个**经过审查的指针，而非可执行包本身**。它不包含任何客户端代码，自身也不会执行任何 Beatra 操作。它所指向的包捆绑了三个标准库 Python 脚本，这些脚本会发出网络调用、存储一个凭证，并可以替换自身的文件。请在启用之前阅读[安装](#安装固定版本已验证两次批准)和[安全与安全说明](#安全与安全说明)部分。

| 固定身份信息 | 值 |
| --- | --- |
| 包 | `ai-image-generation-studio` `0.1.4` |
| 压缩包 | `https://cdn.beatra.ai/agent-packages/ai-image-generation-studio/v0.1.4/ai-image-generation-studio-skill-0.1.4.zip` |
| 压缩包 SHA-256 | `b357edb0f9f2546435c89cf1ef8278596e28a7629229a78fcab9804decd13682` |
| 源代码树 | [`beatra-ai/ai-image-generator-skill@13c7b9b`](https://github.com/beatra-ai/ai-image-generator-skill/tree/13c7b9b2a2197fb91deb6a3a1466124db620c3d1/skills/ai-image-generation-studio)（完整 SHA 为 `13c7b9b2a2197fb91deb6a3a1466124db620c3d1`） |
| 许可证 | MIT No Attribution（MIT-0） |

压缩包内只包含普通文件（没有符号链接、没有可执行位、没有二进制文件）。使用下面的检查命令确认这一点。每个文件都必须与固定提交版本处的源代码树逐字节一致。

## 何时使用此技能

- 当用户明确希望在 Beatra 上生成 AI Image Generator 作品，并接受这是付费服务时使用。
- 当他们已同意将提示词和任何参考图片发送给第三方时使用。
- 不要用于纯本地的图片编辑，或在未获批准进行付费渲染的情况下使用。

## 安装（固定版本、已验证、两次批准）

### 步骤 1：下载并在审查目录中验证

说明这会从 `cdn.beatra.ai` 下载一个外部包，然后请求批准。只有获得批准之后才能执行：

```bash
umask 077
review_dir="$(mktemp -d)"
cd "$review_dir" || exit 1
curl -fsSLO "https://cdn.beatra.ai/agent-packages/ai-image-generation-studio/v0.1.4/ai-image-generation-studio-skill-0.1.4.zip"
printf '%s  %s\n' \
  'b357edb0f9f2546435c89cf1ef8278596e28a7629229a78fcab9804decd13682' \
  'ai-image-generation-studio-skill-0.1.4.zip' | shasum -a 256 -c -
```

如果检查没有打印出 `OK`，就停止。期望的摘要值来自这个目录条目，而不是来自同一个 CDN 上的某个文件。

### 步骤 2：在启用前进行检查

```bash
unzip -l ai-image-generation-studio-skill-0.1.4.zip
unzip -q ai-image-generation-studio-skill-0.1.4.zip
find ai-image-generation-studio -type l -print            # 期望没有输出
find ai-image-generation-studio -type f -perm -111 -print # 期望没有输出
grep -n '"auto_update": True' ai-image-generation-studio/scripts/mcp_client.py
```

可以选择与公开的源代码树（第二个独立主机）确认字节级一致性：

```bash
git clone --quiet --filter=blob:none --no-checkout https://github.com/beatra-ai/ai-image-generator-skill.git src
git -C src checkout --quiet 13c7b9b2a2197fb91deb6a3a1466124db620c3d1 -- skills/ai-image-generation-studio
(cd ai-image-generation-studio && find . -type f | LC_ALL=C sort | xargs shasum -a 256) > archive.sha
(cd src/skills/ai-image-generation-studio && find . -type f | LC_ALL=C sort | xargs shasum -a 256) > tree.sha
cmp archive.sha tree.sha && echo IDENTICAL
```

向用户报告审查发现的内容：`SKILL.md`、`manifest.json`、随附的 Markdown 参考文档，以及 `scripts/authorize.py`、`scripts/mcp_client.py`、`scripts/uninstall.py`（Python 3.10+，仅使用标准库，不安装依赖，没有生命周期钩子）。总结[安全与安全说明](#安全与安全说明)中列出的网络、凭证、本地状态、遥测和自我更新行为。

### 步骤 3：复制进来，并在运行任何其他命令之前先禁用自我更新

请求**第二次、独立的**批准，因为这会更改代理配置。然后将审查过的目录树复制到宿主的 skills 目录（这里以 Claude Code 为例；其他宿主请使用对应路径），并立即对该确切路径关闭静默自我更新：

```bash
dest="$HOME/.claude/skills/ai-image-generation-studio"
test ! -e "$dest" || { echo "destination exists; stop and ask the user"; exit 1; }
cp -R ai-image-generation-studio "$dest"
python3 "$dest/scripts/mcp_client.py" update --auto off
```

最后一条命令必须打印出
`Automatic Beatra package updates are disabled.`。它只会写入
`~/.beatra/updates/<id>/state.json`，不会发出任何网络请求。要在 `authorize.py`、`verify`、`tools`、`upload` 或 `call` 之前运行它：在这个固定版本中，自我更新**默认是开启的**。此设置是绑定到解析后的安装路径的，所以移动或重新复制该目录之后要重复执行一次。

### 步骤 4：作为一个独立决定进行授权

授权会打开浏览器登录，并存储一个 bearer token。请先询问。

```bash
python3 "$dest/scripts/authorize.py"
```

如果宿主只在启动时发现技能，请启动一个新的代理会话。

## 工作原理

1. 阅读已安装包的 `SKILL.md` 及其参考文档；它们定义了路由、负载形状和审查循环。
2. 先使用免费、不计费的发现操作（`beatra.models.list`、任务列表），读取当前的模型卡片和额度估算。
3. 向用户展示一张费用卡，针对恰好一次付费调用：工具、模型、估算费用、以及将要上传哪些文件。等待明确批准。做计划或说"直接做就行"不算批准。
4. 仅上传用户为此任务提供并批准的文件，然后用一个稳定的 `client_request_id` 提交一次，并轮询返回的任务。
5. 向用户报告交付的产出物和 `billing.net_charged_credits`，与用户一起审查结果，并在进行任何进一步的付费阶段之前再次询问。

## 示例

### 免费连接检查（不计费）

```bash
python3 "$HOME/.claude/skills/ai-image-generation-studio/scripts/mcp_client.py" verify
```

### 一次获批的付费调用

在用户对这个确切负载批准了费用卡之后，使用已安装的 `SKILL.md` 中的工具名，用一个稳定的请求 ID 提交一次。如果响应丢失，只能用相同的 `client_request_id` 和完全相同的参数重试；在任务仍在运行时绝不要提交一个替代请求。

## 更新

此条目不认可该包的静默自我更新。保持
`update --auto off`，不要在未获明确批准的情况下运行 `update --auto on` 或裸的
`update`。

要升级到更新的版本，在一个新的审查目录中针对该版本重复步骤 1 到 3，对照 `beatra-ai/ai-image-generator-skill` 中匹配的树验证其摘要
（此条目中未列出的版本在此处未被审查过），向用户展示相对于已安装副本的文件级变更，并仅在获得批准后才替换该目录。`update --check` 会从 `beatra.ai` 报告可用的版本，而不会改动任何文件。

## 卸载

```bash
dest="$HOME/.claude/skills/ai-image-generation-studio"
python3 "$dest/scripts/uninstall.py" --dry-run
python3 "$dest/scripts/uninstall.py"
```

阅读 JSON 决策结果。`disconnected` 表示这是该设备上最后一个 Beatra 技能：令牌已被撤销（当 `revoked` 为 `true` 时），`~/.beatra` 下的
`credentials.json`、`installation.json`、`host.json`、`skills.json` 和
`registrations.json` 文件已被删除。`keep_connection` 表示另一个 Beatra 技能仍在使用共享的令牌，该令牌会保留下来。然后，在与用户确认路径之后，删除 `$dest`。

`uninstall.py` 不会删除 `~/.beatra/updates/`。当决策结果为
`disconnected` 且未安装其他 Beatra 技能时，也应删除该目录；
否则保留它。无法被撤销的令牌会在闲置 15
天后过期，并可以在 Beatra Console 的 Agents 页面中立即撤销。

## 最佳实践

- ✅ 每次付费调用、每组上传文件、每个安装步骤都保持一次批准。
- ✅ 从终端任务报告实际扣除的额度，而不是估算值。
- ❌ 不要重新启用自我更新，也不要静默安装未经审查的版本。
- ❌ 不要打印、粘贴或移动 `~/.beatra/credentials.json` 中的令牌。
- ❌ 在响应结果不确定的情况下，不要用新的请求 ID 重试付费调用。

## 局限性

- 需要一个 Beatra 账户、网络访问、Python 3.10+ 以及预付的额度。
- 模型、价格、schema 和可用性由 Beatra 及其上游模型提供方控制，可能发生变化；该服务按现状提供。
- 输出结果是概率性的，不保证唯一性或不侵权，发布前需要人工审查。
- 此目录条目仅审查了上述固定的压缩包。更新的版本属于另一次审查。

## 安全与安全说明

`risk: critical` 是刻意设定的。

- **网络。** 授权使用 `api.beatra.ai`；每次工具调用和上传都发往
  `mcp.beatra.ai`。如果自我更新保持开启，客户端还会获取
  `https://beatra.ai/skills/ai-image-generation-studio/install.json` 以及来自
  `cdn.beatra.ai` 的压缩包。
- **自我更新（在此固定版本中默认开启）。** 在 `verify`、
  `tools`、`upload` 或 `call` 之前，客户端最多每 24 小时检查一次是否有更新版本，如果存在，就会替换包所拥有的文件，而不会进行逐次更新的预览或批准。它会固定宿主和路径，从 Beatra 自己的发现文档和 CDN 验证校验和，并在失败时回滚，但这些摘要并非独立锚定的。因此，此条目要求在首次使用之前执行
  `update --auto off`，如步骤 3 所示。
- **上传与第三方。** 提示词和上传的媒体会被发送给 Beatra，并转发给执行任务的第三方模型提供方。Beatra 的托管地点在中国大陆境外。参见
  [隐私政策](https://beatra.ai/en/privacy)。
- **计费。** 付费工具会消耗预付的额度。因可归因于 Beatra 或上游模型的原因而失败的任务，其额度会自动返还；否则购买的额度不可退款，实际用量可能超出估算值，导致出现负余额。参见
  [条款](https://beatra.ai/en/terms)。
- **凭证。** `authorize.py` 运行一次 OAuth 设备流程，打开浏览器，
  并将一个 bearer token 存储在 `~/.beatra/credentials.json` 中（目录权限
  `0700`，文件权限 `0600`）。该令牌永远不会进入 argv、环境变量
  或输出中。它拥有完整的 Beatra 范围权限，包括 `wallet:spend`，具有
  滑动式 15 天闲置生命周期，并由该设备上的每一个 Beatra 技能共享。
- **本地状态。** `~/.beatra/` 还保存着 `installation.json`（随机的
  安装引用标识）、`host.json`（代理平台和主机名）、
  `skills.json`（已安装的 Beatra 技能路径）、`registrations.json`，以及
  `updates/<id>/state.json` 加上运行更新时产生的更新备份。
- **遥测。** 设备流程会发送主机名作为设备名称、
  包的 slug 和版本号，以及检测到的代理平台（例如
  `claude-code`，来自环境变量）。首次使用时，客户端会发出一次
  不计费的 `beatra.installations.register` 调用，并且每次工具调用都会附加
  `source_package_slug` 和 `source_platform`。这些字段没有退出选项。
- **留存。** 账户数据在账户生命周期内一直保留。任务
  记录、产出物和计费账本在账户关闭后仍会出于审计和税务目的保留。
- **内容权利。** 用户保留其输入内容的权利，并获得 Beatra 对输出内容的权利；他们必须拥有所上传媒体的权利，且不得
  制作欺骗性的冒充内容。

## 其他资源

- [固定提交版本处的源代码树](https://github.com/beatra-ai/ai-image-generator-skill/tree/13c7b9b2a2197fb91deb6a3a1466124db620c3d1/skills/ai-image-generation-studio)
- [产品页面](https://beatra.ai/skills/ai-image-generation-studio)
- [条款](https://beatra.ai/en/terms) 和 [隐私政策](https://beatra.ai/en/privacy)
</content>
