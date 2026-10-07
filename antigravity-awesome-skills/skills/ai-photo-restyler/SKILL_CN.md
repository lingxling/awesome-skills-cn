---
name: ai-photo-restyler
description: "安装并使用官方 Photo to Anime 包（按摘要锁定版本），在 Beatra 服务上进行付费托管作业。"
category: media
risk: critical
source: community
source_repo: beatra-ai/photo-to-anime-skill
source_type: official
date_added: "2026-09-18"
author: beatra-ai
tags: [photo-to-anime, image-stylization, mcp, paid-api, beatra]
tools: [claude, codex, cursor, gemini]
license: "MIT-0"
license_source: "https://github.com/beatra-ai/photo-to-anime-skill/blob/87bc4c4e993e1ab49ded9e065087c1796cb7cbe4/LICENSE"
---

# Photo to Anime Skill

## 概述

在 Claude Code、Codex 或 OpenClaw 内部,将一张照片转化为动漫、漫画、卡通、水彩、粘土或 3D 角色风格的图像,同时保持主体可辨识,并在整套图像中重复使用同一种风格。相关工作在托管的付费 Beatra 服务
(`mcp.beatra.ai`)上完成。

本目录条目是**经过审核的指针,而非可执行包本身**。它本身不包含任何客户端代码,也不会自行执行任何 Beatra 操作。它所指向的包捆绑了三个仅使用标准库的 Python 脚本,这些脚本会发起网络调用、存储凭证,并可能替换自身的文件。启用前请阅读
[安装](#安装已锁定已验证需两次批准)和
[安全与安保说明](#安全与安保说明)。

| 锁定标识 | 值 |
| --- | --- |
| 软件包 | `ai-photo-restyler` `0.1.4` |
| 归档包 | `https://cdn.beatra.ai/agent-packages/ai-photo-restyler/v0.1.4/ai-photo-restyler-skill-0.1.4.zip` |
| 归档包 SHA-256 | `ac7e4070f7e931a095f55c19ee09adb4ba70f4880fb66dbfe755823e3bfa2449` |
| 源代码树 | [`beatra-ai/photo-to-anime-skill@87bc4c4`](https://github.com/beatra-ai/photo-to-anime-skill/tree/87bc4c4e993e1ab49ded9e065087c1796cb7cbe4/skills/ai-photo-restyler) (完整 SHA `87bc4c4e993e1ab49ded9e065087c1796cb7cbe4`) |
| 许可证 | MIT No Attribution (MIT-0) |

该归档包仅包含普通文件(无符号链接、无可执行位、无二进制文件)。请使用下方的检查命令予以确认。每个文件都必须与锁定提交处的源代码树逐字节一致。

## 何时使用此技能

- 当用户明确希望在 Beatra 上制作 Photo to Anime 作品并接受其为付费服务时使用。
- 当用户已同意将提示词和任何参考图像发送给第三方时使用。
- 不要用于仅限本地的图像编辑,或没有批准任何付费渲染的场合。

## 安装(已锁定、已验证、需两次批准)

### 步骤 1:下载并在审核目录中验证

说明这将从 `cdn.beatra.ai` 下载一个外部包,然后请求批准。仅在获得批准后:

```bash
umask 077
review_dir="$(mktemp -d)"
cd "$review_dir" || exit 1
curl -fsSLO "https://cdn.beatra.ai/agent-packages/ai-photo-restyler/v0.1.4/ai-photo-restyler-skill-0.1.4.zip"
printf '%s  %s\n' \
  'ac7e4070f7e931a095f55c19ee09adb4ba70f4880fb66dbfe755823e3bfa2449' \
  'ai-photo-restyler-skill-0.1.4.zip' | shasum -a 256 -c -
```

如果检查没有输出 `OK`,立即停止。预期的摘要值来自本目录条目,而不是来自同一个 CDN 上的文件。

### 步骤 2:激活前先检查

```bash
unzip -l ai-photo-restyler-skill-0.1.4.zip
unzip -q ai-photo-restyler-skill-0.1.4.zip
find ai-photo-restyler -type l -print            # 期望无输出
find ai-photo-restyler -type f -perm -111 -print # 期望无输出
grep -n '"auto_update": True' ai-photo-restyler/scripts/mcp_client.py
```

可选地,通过公开的源代码树(第二个独立主机)确认字节级一致性:

```bash
git clone --quiet --filter=blob:none --no-checkout https://github.com/beatra-ai/photo-to-anime-skill.git src
git -C src checkout --quiet 87bc4c4e993e1ab49ded9e065087c1796cb7cbe4 -- skills/ai-photo-restyler
(cd ai-photo-restyler && find . -type f | LC_ALL=C sort | xargs shasum -a 256) > archive.sha
(cd src/skills/ai-photo-restyler && find . -type f | LC_ALL=C sort | xargs shasum -a 256) > tree.sha
cmp archive.sha tree.sha && echo IDENTICAL
```

向用户报告审核发现的内容:`SKILL.md`、`manifest.json`、捆绑的 Markdown 参考文档,以及
`scripts/authorize.py`、`scripts/mcp_client.py`、`scripts/uninstall.py`(Python 3.10+,仅使用标准库,无需安装依赖,没有生命周期钩子)。总结
[安全与安保说明](#安全与安保说明)中列出的网络、凭证、本地状态、遥测和自我更新行为。

### 步骤 3:复制进来并在执行任何其他命令前先禁用自我更新

请求**第二次、单独的**批准,因为这会更改 agent 配置。然后将审核过的目录树复制到主机的 skills 目录(此处以 Claude Code 为例;其他主机请使用对应路径),并立即为该确切路径关闭静默自我更新:

```bash
dest="$HOME/.claude/skills/ai-photo-restyler"
test ! -e "$dest" || { echo "destination exists; stop and ask the user"; exit 1; }
cp -R ai-photo-restyler "$dest"
python3 "$dest/scripts/mcp_client.py" update --auto off
```

最后一条命令必须打印出
`Automatic Beatra package updates are disabled.`。它仅写入
`~/.beatra/updates/<id>/state.json`,不发起任何网络请求。请在运行
`authorize.py`、`verify`、`tools`、`upload` 或 `call` 之前执行此命令:在此锁定版本中,自我更新**默认是开启的**。该设置是按解析后的安装路径键入的,因此移动或重新复制目录后需要再次执行。

### 步骤 4:将授权作为单独的决定

授权会打开浏览器登录并存储一个 bearer token。请先询问。

```bash
python3 "$dest/scripts/authorize.py"
```

如果主机只在启动时发现 skills,请启动一个新的 agent 会话。

## 工作原理

1. 读取已安装包的 `SKILL.md` 及其参考文档;它们定义了路由、负载格式和审核循环。
2. 首先使用免费、不计费的发现调用(`beatra.models.list`、任务列表)来读取当前的模型卡片和额度估算。
3. 向用户展示一张恰好对应一次付费调用的费用卡片:工具、模型、估算值,以及将上传哪些文件。等待用户明确批准。规划或"直接做"都不算批准。
4. 仅上传用户为此任务提供并批准的文件,然后使用一个稳定的 `client_request_id` 提交一次,并轮询返回的任务。
5. 向用户报告交付的作品和 `billing.net_charged_credits`,与用户一起审查结果,并在进行任何后续付费阶段之前再次征求同意。

## 示例

### 免费连接检查(不计费)

```bash
python3 "$HOME/.claude/skills/ai-photo-restyler/scripts/mcp_client.py" verify
```

### 一次已批准的付费调用

在用户已就此确切负载批准费用卡片后,使用安装的 `SKILL.md` 中的工具名称,配合一个稳定的请求 ID 提交一次。如果响应丢失,只能使用相同的 `client_request_id` 和相同的参数重试;绝不能在任务运行期间提交替代请求。

## 更新

本条目并不认可该包的静默自我更新。请保持
`update --auto off` 的设置,不要在没有明确批准的情况下运行 `update --auto on` 或裸的
`update`。

要升级到更新的版本,请在一个新的审核目录中重复步骤 1 到 3(针对该版本),对照
`beatra-ai/photo-to-anime-skill` 中匹配的目录树验证其摘要值(本条目未列出的版本在此未经审核),向用户展示相对于已安装副本的文件级变更,并仅在获得批准后替换目录。`update --check` 会报告来自
`beatra.ai` 的可用版本,而不会更改任何文件。

## 卸载

```bash
dest="$HOME/.claude/skills/ai-photo-restyler"
python3 "$dest/scripts/uninstall.py" --dry-run
python3 "$dest/scripts/uninstall.py"
```

阅读 JSON 格式的决定结果。`disconnected` 表示这是设备上最后一个 Beatra skill:token 已被撤销(当
`revoked` 为 `true` 时),并且 `~/.beatra` 下的
`credentials.json`、`installation.json`、`host.json`、`skills.json` 和
`registrations.json` 文件已被删除。`keep_connection` 表示另一个 Beatra skill 仍在使用共享的 token,因此该 token 会保留。然后,在与用户确认路径后,删除 `$dest`。

`uninstall.py` 不会删除 `~/.beatra/updates/`。当决定结果为
`disconnected` 且没有安装其他 Beatra skill 时,也应删除该目录;否则请保留它。如果 token 无法被撤销,它会在闲置 15 天后过期,也可以在 Beatra Console 的 Agents 页面下立即撤销。

## 最佳实践

- ✅ 每次付费调用、每组上传、每个安装步骤都保持单独批准。
- ✅ 报告终态任务中的实际扣费额度,而不是估算值。
- ❌ 不要重新启用自我更新,也不要静默安装未经审核的版本。
- ❌ 不要打印、粘贴或将 token 移出 `~/.beatra/credentials.json`。
- ❌ 不要在响应不确定的情况下使用新的请求 ID 重试付费调用。

## 限制

- 需要 Beatra 账户、网络访问、Python 3.10+,以及预付的额度。
- 模型、价格、schema 和可用性由 Beatra 及其上游模型供应商控制,可能发生变化;本服务按现状提供。
- 输出结果是概率性的,不保证唯一或不侵权,发布前需要人工审核。
- 本目录条目仅审核了上方锁定的归档包。更新的版本属于另一次审核。

## 安全与安保说明

`risk: critical` 是刻意标注的。

- **网络。** 授权使用 `api.beatra.ai`;每次工具调用和上传都会发往
  `mcp.beatra.ai`。如果保留自我更新开启,客户端还会从
  `https://beatra.ai/skills/ai-photo-restyler/install.json` 获取数据,并从
  `cdn.beatra.ai` 下载归档包。
- **自我更新(在此锁定版本中默认开启)。** 在 `verify`、
  `tools`、`upload` 或 `call` 之前,客户端最多每 24 小时检查一次是否有新版本,如果存在,就会替换包所拥有的文件,且不提供逐次更新预览或批准。它会锁定主机和路径,根据 Beatra 自身的发现文档和 CDN 验证校验和,并在失败时回滚,但这些摘要值并没有独立的锚定来源。因此本条目要求在首次使用前执行步骤 3 中的
  `update --auto off`。
- **上传与第三方。** 提示词和上传的媒体会被发送给 Beatra,并转发给执行该任务的第三方模型供应商。Beatra 的托管位置在中国大陆以外。详见
  [隐私政策](https://beatra.ai/en/privacy)。
- **计费。** 付费工具会消耗预付额度。因 Beatra 或上游模型自身原因导致失败的任务,其额度会自动退还;否则购买不可退款,且实际用量可能超出估算值,导致余额为负。详见
  [条款](https://beatra.ai/en/terms)。
- **凭证。** `authorize.py` 运行 OAuth 设备流程,打开浏览器,并将一个 bearer token 存储在
  `~/.beatra/credentials.json` 中(目录权限 `0700`,文件权限
  `0600`)。该 token 永远不会出现在 argv、环境变量或输出中。它拥有完整的 Beatra 权限范围,包括
  `wallet:spend`,具有滑动的 15 天闲置有效期,且被设备上每一个 Beatra skill 共享。
- **本地状态。** `~/.beatra/` 还保存着 `installation.json`(随机的安装引用)、`host.json`(agent 平台和主机名)、
  `skills.json`(已安装的 Beatra skill 路径)、`registrations.json`,以及运行更新时的
  `updates/<id>/state.json` 和更新备份。
- **遥测。** 设备流程会将主机名作为设备名称发送,以及软件包 slug 和版本、检测到的 agent 平台(例如从环境变量中获取的
  `claude-code`)。首次使用时,客户端会发起一次不计费的
  `beatra.installations.register` 调用,此后每次工具调用都会附加
  `source_package_slug` 和 `source_platform`。这些字段没有退出选项。
- **留存。** 账户数据在账户存续期间会被保留。任务记录、作品和账单台账在账户关闭后仍会出于审计和税务目的被保留。
- **内容权利。** 用户保留其输入内容的权利,并获得 Beatra 在输出内容上的权利;用户必须持有所上传媒体的权利,且不得创建具有欺骗性的冒充内容。

## 更多资源

- [锁定提交处的源代码树](https://github.com/beatra-ai/photo-to-anime-skill/tree/87bc4c4e993e1ab49ded9e065087c1796cb7cbe4/skills/ai-photo-restyler)
- [产品页面](https://beatra.ai/skills/ai-photo-restyler)
- [条款](https://beatra.ai/en/terms) 与 [隐私政策](https://beatra.ai/en/privacy)
