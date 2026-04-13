---
name: paperzilla
description: 与您的代理讨论 Paperzilla 中的项目、推荐和经典论文。当用户询问最近的项目推荐、经典论文详细信息、基于 markdown 的摘要、推荐反馈、 feed 导出或 Atom feed URL 时使用。
license: MIT
metadata:
  skill-author: "Paperzilla Inc"
---

# Paperzilla

当您想要与您的代理讨论 Paperzilla 中的项目、推荐和经典论文时，使用此技能。

## 您可以询问的内容

- "给我项目 X 的最新推荐。"
- "打开推荐 Y 并解释它为什么重要。"
- "以 markdown 格式获取经典论文 Z 并总结它。"
- "告诉我这篇论文与我的研究有何相关。"
- "显示项目 X 的 feed。"
- "对推荐留下反馈。"
- "将此论文、推荐或 feed 导出为 JSON。"

这是核心 Paperzilla 技能。它使您的代理可以直接访问 Paperzilla 数据，但不强制执行工作流或外部交付集成。

## 访问方法

此 repo 中的大多数当前配置文件使用 `pz` CLI。

如果当前配置文件附带特定于代理的额外指令，也请遵循这些指令。

## 安装

### macOS
```bash
brew install paperzilla-ai/tap/pz
```

### Windows (Scoop)
```bash
scoop bucket add paperzilla-ai https://github.com/paperzilla-ai/scoop-bucket
scoop install pz
```

### Linux
使用官方 Linux 安装指南：

- https://docs.paperzilla.ai/guides/cli-getting-started

### 从源码构建（Go 1.23+）
请参阅 CLI 存储库了解源码构建：

- https://github.com/paperzilla-ai/pz

## 更新

检查您的 CLI 是否最新并获取特定于安装的升级步骤：

```bash
pz update
```

如果检测不明确，明确覆盖：

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

## CLI 参考

如果当前配置文件使用 `pz`，这些是核心命令。

### 列出项目
```bash
pz project list
```

### 显示一个项目
```bash
pz project <project-id>
```

### 浏览项目 feed
```bash
pz feed <project-id>
```

有用的标志：
- `--must-read`
- `--since YYYY-MM-DD`
- `--limit N`
- `--json`
- `--atom`

示例：
```bash
pz feed <project-id> --must-read --since 2026-03-01 --limit 5
pz feed <project-id> --json
pz feed <project-id> --atom
```

Feed 输出可以包含现有的推荐反馈标记：

- `[↑]` 点赞
- `[↓]` 点踩
- `[★]` 星标

### 阅读经典论文
```bash
pz paper <paper-id>
pz paper <paper-id> --json
pz paper <paper-id> --markdown
pz paper <paper-id> --project <project-id>
```

### 打开来自您项目的推荐
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

## 输出和自动化

- 机器解析首选 `--json`。
- `pz paper --markdown` 仅在已准备好时返回 markdown。
- `pz rec --markdown` 可以排队生成 markdown 并在仍在准备时打印友好的重试消息。
- `--atom` 返回用于 feed 阅读器的个人 feed URL。

## 配置

```bash
export PZ_API_URL="https://paperzilla.ai"
```

## 参考

- 文档：https://docs.paperzilla.ai/guides/cli
- 快速入门：https://docs.paperzilla.ai/guides/cli-getting-started
- 存储库：https://github.com/paperzilla-ai/pz