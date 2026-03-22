---
name: "sentry"
description: "当用户要求检查 Sentry 问题或事件、总结最近的生产错误，或通过 Sentry API 拉取基本 Sentry 健康数据时使用；使用捆绑的脚本执行只读查询并需要 `SENTRY_AUTH_TOKEN`。"
---


# Sentry（只读可观察性）

## 快速开始

- 如果尚未通过身份验证，请要求用户提供有效的 `SENTRY_AUTH_TOKEN`（只读范围，如 `project:read`、`event:read`）或在运行命令之前登录并创建一个。
- 将 `SENTRY_AUTH_TOKEN` 设置为环境变量。
- 可选默认值：`SENTRY_ORG`、`SENTRY_PROJECT`、`SENTRY_BASE_URL`。
- 默认值：org/项目 `{your-org}`/`{your-project}`、时间范围 `24h`、环境 `prod`、限制 20（最大 50）。
- 始终调用 Sentry API（无启发式，无缓存）。

如果缺少令牌，请为用户提供这些步骤：
1. 创建 Sentry 身份验证令牌：https://sentry.io/settings/account/api/auth-tokens/
2. 创建一个带有只读范围的令牌，如 `project:read`、`event:read` 和 `org:read`。
3. 在他们的系统中将 `SENTRY_AUTH_TOKEN` 设置为环境变量。
4. 如果需要，提供引导他们为其操作系统/shell 设置环境变量的指导。
- 永远不要要求用户在聊天中粘贴完整的令牌。要求他们在本地设置并准备好时确认。

## 核心任务（使用捆绑的脚本）
使用 `scripts/sentry_api.py` 进行确定性 API 调用。它处理分页并在瞬态错误时重试一次。

## 技能路径（设置一次）

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export SENTRY_API="$CODEX_HOME/skills/sentry/scripts/sentry_api.py"
```

用户范围的技能安装在 `$CODEX_HOME/skills` 下（默认：`~/.codex/skills`）。

### 1) 列出问题（按最近排序）

```bash
python3 "$SENTRY_API" \
  list-issues \
  --org {your-org} \
  --project {your-project} \
  --environment prod \
  --time-range 24h \
  --limit 20 \
  --query "is:unresolved"
```

### 2) 将问题短 ID 解析为问题 ID

```bash
python3 "$SENTRY_API" \
  list-issues \
  --org {your-org} \
  --project {your-project} \
  --query "ABC-123" \
  --limit 1
```

使用返回的 `id` 获取问题详细信息或事件。

### 3) 问题详细信息

```bash
python3 "$SENTRY_API" \
  issue-detail \
  1234567890
```

### 4) 问题事件

```bash
python3 "$SENTRY_API" \
  issue-events \
  1234567890 \
  --limit 20
```

### 5) 事件详细信息（默认无堆栈跟踪）

```bash
python3 "$SENTRY_API" \
  event-detail \
  --org {your-org} \
  --project {your-project} \
  abcdef1234567890
```

## API 要求

始终使用这些端点（仅 GET）：

- 列出问题：`/api/0/projects/{org_slug}/{project_slug}/issues/`
- 问题详细信息：`/api/0/issues/{issue_id}/`
- 问题的事件：`/api/0/issues/{issue_id}/events/`
- 事件详细信息：`/api/0/projects/{org_slug}/{project_slug}/events/{event_id}/`

## 输入和默认值

- `org_slug`、`project_slug`：默认为 `{your-org}`/`{your-project}`（避免非生产 org）。
- `time_range`：默认 `24h`（作为 `statsPeriod` 传递）。
- `environment`：默认 `prod`。
- `limit`：默认 20，最大 50（分页直到达到限制）。
- `search_query`：可选的 `query` 参数。
- `issue_short_id`：首先通过 list-issues 查询解析。

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
