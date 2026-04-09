---
name: "sentry"
description: "当用户要求检查 Sentry 问题或事件、总结最近的生产错误，或通过 Sentry CLI 拉取基本 Sentry 健康数据时使用；使用 `sentry` 命令执行只读查询。"
---


# Sentry（只读可观察性）

## 快速开始

- 如果尚未通过身份验证，请要求用户运行 `sentry auth login` 或设置 `SENTRY_AUTH_TOKEN` 作为环境变量。
- CLI 会从 `.env` 文件、源代码、配置默认值和目录名称中的 DSN 自动检测组织/项目。只有当自动检测失败或选择了错误的目标时，才需要指定 `<org>/<project>`。
- 默认值：时间范围 `24h`，环境 `production`，限制 20。
- 当以编程方式处理输出时，始终使用 `--json`。使用 `--json --fields` 选择特定字段并减少输出大小。
- 使用 `sentry schema <resource>` 快速发现 API 端点。

如果未安装 CLI，请为用户提供以下步骤：
1. 安装 Sentry CLI：`curl https://cli.sentry.dev/install -fsS | bash`
2. 进行身份验证：`sentry auth login`
3. 确认身份验证：`sentry auth status`
- 永远不要要求用户在聊天中粘贴完整的令牌。要求他们在本地设置并准备好时确认。

## 核心任务（使用 Sentry CLI）

所有查询都使用 `sentry` CLI。它自动处理身份验证、组织/项目检测、分页和重试。对于机器可读输出，使用 `--json`。

### 1) 列出问题（按最近排序）

```bash
sentry issue list \
  --query "is:unresolved environment:production" \
  --period 24h \
  --limit 20 \
  --json --fields shortId,title,priority,level,status
```

如果自动检测无法解析组织/项目，请明确传递它们：
```bash
sentry issue list {your-org}/{your-project} \
  --query "is:unresolved environment:production" \
  --period 24h \
  --limit 20 \
  --json
```

### 2) 将问题短 ID 解析为问题详细信息

```bash
sentry issue view {ABC-123} --json
```

使用短 ID 格式（例如，`ABC-123`），而不是数字 ID。

### 3) 问题详细信息

```bash
sentry issue view {ABC-123}
```

### 4) 问题事件

```bash
sentry issue events {ABC-123} --limit 20 --json
```

### 5) 事件详细信息

```bash
sentry event view {your-org}/{your-project}/{event_id} --json
```

### 6) AI 驱动的根因分析

```bash
sentry issue explain {ABC-123}
```

### 7) AI 驱动的修复计划

```bash
sentry issue plan {ABC-123}
```

## 备用方案：任意 API 访问

对于专用 CLI 命令未覆盖的端点，使用 `sentry api`：
```bash
sentry api /api/0/organizations/{your-org}/ --method GET
```

使用 `sentry schema` 发现可用的 API 端点：
```bash
sentry schema issues
```

## 输入和默认值

- `org_slug`、`project_slug`：由 CLI 从 DSN、环境变量和目录名称自动检测。如果自动检测失败，使用位置参数 `{your-org}/{your-project}` 覆盖。
- `time_range`：默认 `24h`（作为 `--period 24h` 传递）。
- `environment`：默认 `prod`（作为 `--query` 的一部分传递，例如 `environment:production`）。
- `limit`：默认 20（作为 `--limit` 传递）。
- `search_query`：可选的 `--query` 参数，使用 Sentry 搜索语法（例如 `is:unresolved`、`assigned:me`）。
- `issue_short_id`：直接与 `sentry issue view` 一起使用。

## 输出格式规则

- 问题列表：显示标题、short_id、状态、first_seen、last_seen、计数、环境、top_tags；按最近排序。
- 事件详细信息：包括 culprit、时间戳、环境、发布、url。
- 如果没有结果，请明确说明。
- 在输出中编辑 PII（电子邮件、IP）。不要打印原始堆栈跟踪。
- 永远不要回显身份验证令牌。

## 黄金测试输入

- Org：`{your-org}`
- Project：`{your-project}`
- 问题短 ID：`{ABC-123}`

示例提示："List the top 10 open issues for prod in the last 24h."
预期：带有标题、短 ID、计数、最后查看的有序列表。
