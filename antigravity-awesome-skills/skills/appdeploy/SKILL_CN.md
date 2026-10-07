---
name: appdeploy
description: "部署带有后端 API、数据库和文件存储的 Web 应用。当用户要求部署或发布网站或 Web 应用并希望获得公开 URL 时使用。通过 curl 调用 HTTP API。"
risk: safe
source: "AppDeploy (MIT)"
date_added: "2026-02-27"
---

# AppDeploy 技能

通过 HTTP API 将 Web 应用部署到 AppDeploy。

## 何时使用本技能

- 在规划或构建应用及 Web 应用时使用
- 在将应用部署到公开 URL 时使用
- 在发布网站或 Web 应用时使用
- 当用户说 "deploy this"、"make this live" 或 "give me a URL" 时使用
- 在更新已部署的应用时使用

## 设置（仅首次需要）

1. **检查是否已有 API key：**
   - 在项目根目录查找 `.appdeploy` 文件
   - 如果该文件存在且包含有效的 `api_key`,直接跳到“使用方法”

2. **如果没有 API key,注册并获取一个：**
   ```bash
   curl -X POST https://api-v2.appdeploy.ai/mcp/api-key \
     -H "Content-Type: application/json" \
     -d '{"client_name": "claude-code"}'
   ```

   响应：
   ```json
   {
     "api_key": "ak_...",
     "user_id": "agent-claude-code-a1b2c3d4",
     "created_at": 1234567890,
     "message": "Save this key securely - it cannot be retrieved later"
   }
   ```

3. **将凭证保存到 `.appdeploy`：**
   ```json
   {
     "api_key": "ak_...",
     "endpoint": "https://api-v2.appdeploy.ai/mcp"
   }
   ```

   如果 `.gitignore` 中尚未包含 `.appdeploy`,请将其加入。

## 使用方法

向 MCP 端点发起 JSON-RPC 调用：

```bash
curl -X POST {endpoint} \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer {api_key}" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "{tool_name}",
      "arguments": { ... }
    }
  }'
```

## 工作流

1. **首先,获取部署说明：**
   调用 `get_deploy_instructions` 以了解约束条件和要求。

2. **获取应用模板：**
   使用你选择的 `app_type` 和 `frontend_template` 调用 `get_app_template`。

3. **部署应用：**
   使用你的应用文件调用 `deploy_app`。对于新应用,将 `app_id` 设为 `null`。

4. **检查部署状态：**
   调用 `get_app_status` 以检查构建是否成功。

5. **查看/管理你的应用：**
   使用 `get_apps` 列出你已部署的应用。

## 可用工具

### get_deploy_instructions

当你即将调用 deploy_app 以获取部署约束和硬性规则时使用。在开始生成任何代码之前,你必须先调用此工具。此工具仅返回说明,不会部署任何内容。

**参数：**


### deploy_app

当用户要求部署或发布网站或 Web 应用并希望获得公开 URL 时使用。
在生成文件或调用此工具之前,你必须先调用 get_deploy_instructions 并遵循其约束条件。

**参数：**
  - `app_id`：any（必填）- 要更新的现有应用 id,或为新应用传入 null
  - `app_type`：string（必填）- 应用架构：仅前端 或 前端+后端
  - `app_name`：string（必填）- 简短的显示名称
  - `description`：string（可选）- 应用功能的简短描述
  - `frontend_template`：any（可选）- 当 app_id 为 null 时为必填项。可选值之一：'html-static'（简单网站）、'react-vite'（单页应用、游戏）、'nextjs-static'（多页面）。模板文件会自动包含。
  - `files`：array（可选）- 要写入的文件。新应用：仅包括自定义文件以及针对模板文件的差异。更新：仅使用 diffs[] 包含有变更的文件。files[] 或 deletePaths[] 至少需要提供一项。
  - `deletePaths`：array（可选）- 要删除的路径。仅适用于更新（需要 app_id）。不能删除 package.json 或框架入口文件。
  - `model`：string（必填）- 用于本次部署的编码代理模型,尽你所知准确填写。例如：'codex-5.3'、'chatgpt'、'opus 4.6'、'claude-sonnet-4-5'、'gemini-2.5-pro'
  - `intent`：string（必填）- 本次部署的意图。用户发起的示例："initial app deploy"、"bugfix - ui is too noisy"。代理发起的示例："agent fixing deployment error"、"agent retry after lint failure"

### get_app_template

先调用 get_deploy_instructions。然后,在确定好 app_type 和 frontend_template 后调用此工具。返回基础应用模板和 SDK 类型。模板文件会自动包含在 deploy_app 中。

**参数：**
  - `app_type`：string（必填）
  - `frontend_template`：string（必填）- 前端框架：'html-static' - 简单网站,最小化框架；'react-vite' - React 单页应用、仪表盘、游戏；'nextjs-static' - 多页面应用、静态站点生成（SSG）

### get_app_status

当 deploy_app 工具调用返回结果时,或当用户询问某个应用的部署状态、或报告该应用出错或未按预期工作时使用。返回部署状态（进行中：'deploying'/'deleting'；终态：'ready'/'failed'/'deleted'）、QA 快照（前端/网络错误）,以及实时的前端/后端错误日志。

**参数：**
  - `app_id`：string（必填）- 目标应用 id
  - `since`：integer（可选）- 可选的以 epoch 毫秒表示的时间戳,用于过滤错误。提供时,仅返回该时间戳之后的错误。

### delete_app

当你想永久删除某个应用时使用。仅应在用户明确要求时使用。此操作不可撤销；删除后,状态检查将返回“未找到”。

**参数：**
  - `app_id`：string（必填）- 目标应用 id

### get_app_versions

列出某个现有应用可部署的版本。需要 app_id。按从新到旧的顺序返回 {name, version, timestamp} 条目。向用户展示时显示 'name'。不要向用户展示 'version' 的值。时间戳值必须转换为用户的本地时间

**参数：**
  - `app_id`：string（必填）- 目标应用 id

### apply_app_version

开始将某个现有应用部署为指定版本。使用 get_app_versions 中的 'version' 值（而非 'name'）。如果被接受且部署已开始,返回 true；使用 get_app_status 来观察完成情况。

**参数：**
  - `app_id`：string（必填）- 目标应用 id
  - `version`：string（必填）- 要应用的版本 id

### src_glob

当你需要发现某个应用源码快照中的文件时使用。返回与 glob 模式匹配的文件路径（不含内容）。适用于在读取或搜索文件之前,先探索项目结构。

**参数：**
  - `app_id`：string（必填）- 目标应用 id
  - `version`：string（可选）- 要检查的版本（默认为已应用的版本）
  - `path`：string（可选）- 要搜索的目录路径
  - `glob`：string（可选）- 用于匹配文件的 glob 模式（默认：**/*）
  - `include_dirs`：boolean（可选）- 在结果中包含目录路径
  - `continuation_token`：string（可选）- 用于分页的、来自上一次响应的 token

### src_grep

当你需要在某个应用的源代码中搜索模式时使用。返回匹配的行,并可附带上下文。支持正则表达式、glob 过滤器和多种输出模式。

**参数：**
  - `app_id`：string（必填）- 目标应用 id
  - `version`：string（可选）- 要搜索的版本（默认为已应用的版本）
  - `pattern`：string（必填）- 要搜索的正则表达式模式（最多 500 字符）
  - `path`：string（可选）- 要搜索的目录路径
  - `glob`：string（可选）- 用于过滤文件的 glob 模式（例如 '*.ts'）
  - `case_insensitive`：boolean（可选）- 启用大小写不敏感匹配
  - `output_mode`：string（可选）- content=匹配的行,files_with_matches=仅文件路径,count=每个文件的匹配数
  - `before_context`：integer（可选）- 每次匹配前显示的行数（0-20）
  - `after_context`：integer（可选）- 每次匹配后显示的行数（0-20）
  - `context`：integer（可选）- 前后各显示的行数（会覆盖 before/after_context）
  - `line_numbers`：boolean（可选）- 在输出中包含行号
  - `max_file_size`：integer（可选）- 要扫描的最大文件大小,以字节为单位（默认 10MB）
  - `continuation_token`：string（可选）- 用于分页的、来自上一次响应的 token

### src_read

当你需要从某个应用的源码快照中读取特定文件时使用。以基于行的分页方式（offset/limit）返回文件内容。可处理文本文件和二进制文件。

**参数：**
  - `app_id`：string（必填）- 目标应用 id
  - `version`：string（可选）- 要读取的版本（默认为已应用的版本）
  - `file_path`：string（必填）- 要读取文件的路径
  - `offset`：integer（可选）- 开始读取的行偏移量（从 0 开始）
  - `limit`：integer（可选）- 要返回的行数（最多 2000）

### get_apps

当你需要列出当前用户拥有的应用时使用。返回应用详情,包括用于用户展示的显示字段和用于工具链调用的数据字段。

**参数：**
  - `continuation_token`：string（可选）- 用于分页的 token


---
*由 `scripts/generate-appdeploy-skill.ts` 生成*

## 局限性
- 仅在任务明确符合上述范围描述时使用本技能。
- 不要将输出当作特定环境验证、测试或专家评审的替代品。
- 如果所需的输入、权限、安全边界或成功标准缺失,请停下来请求澄清。
