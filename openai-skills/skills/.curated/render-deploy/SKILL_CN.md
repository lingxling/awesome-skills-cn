---
name: render-deploy
description: 通过分析代码库、生成 render.yaml 蓝图和提供仪表板深度链接，将应用程序部署到 Render。当用户想要在 Render 的云平台上部署、托管、发布或设置其应用程序时使用。
---

# 部署到 Render

Render 支持 **基于 Git** 的服务和 **预构建 Docker 镜像**服务。

此技能涵盖 **基于 Git** 的流程：
1. **蓝图方法** - 生成 render.yaml 以进行基础设施即代码部署
2. **直接创建** - 通过 MCP 工具即时创建服务

蓝图还可以通过使用 `runtime: image` 运行 **预构建 Docker 镜像**，但 `render.yaml` 仍必须位于 Git 仓库中。

如果没有 Git 远程，请停止并要求用户：
- 创建/推送 Git 远程（如果只需要蓝图，可以是最小的），或
- 使用 Render 仪表板/API 部署预构建 Docker 镜像（MCP 无法创建基于镜像的服务）。

## 前置条件

- 当沙盒阻止部署网络调用时，使用 `sandbox_permissions=require_escalated` 重新运行。
- 部署可能需要几分钟。使用适当的超时值。

## 何时使用此技能

当用户想要以下内容时激活此技能：
- 将应用程序部署到 Render
- 创建 render.yaml 蓝图文件
- 为其项目设置 Render 部署
- 在 Render 的云平台上托管或发布其应用程序
- 创建数据库、cron 作业或其他 Render 资源

## 快乐路径（新用户）

在深入分析之前使用此简短提示序列以减少摩擦：
1. 询问他们想从 Git 仓库还是预构建 Docker 镜像部署。
2. 询问 Render 是否应该提供应用程序所需的一切（根据用户描述可能的内容）或仅提供应用程序，而他们带来自己的基础设施。如果依赖项不清楚，请询问一个简短的后续问题以确认他们是否需要数据库、worker、cron 或其他服务。

然后继续使用下面的适当方法。

## 选择您的源路径

**Git 仓库路径**：蓝图和直接创建都需要。仓库必须推送到 GitHub、GitLab 或 Bitbucket。

**预构建 Docker 镜像路径**：Render 通过基于镜像的服务支持。这**不**受 MCP 支持；使用仪表板/API。询问：
- 镜像 URL（注册表 + 标签）
- 注册表身份验证（如果是私有的）
- 服务类型（web/worker）和端口

如果用户选择 Docker 镜像，请引导他们到 Render 仪表板镜像部署流程，或要求他们添加 Git 远程（以便您可以使用带有 `runtime: image` 的蓝图）。

## 选择您的部署方法（Git 仓库）

两种方法都需要推送到 GitHub、GitLab 或 Bitbucket 的 Git 仓库。（如果使用 `runtime: image`，仓库可以是最小的，并且仅包含 `render.yaml`。）

| 方法 | 最适合 | 优点 |
|--------|----------|------|
| **蓝图** | 多服务应用、IaC 工作流程 | 版本控制、可重现、支持复杂设置 |
| **直接创建** | 单个服务、快速部署 | 即时创建、不需要 render.yaml 文件 |

### 方法选择启发式

除非用户请求特定方法，否则默认使用此决策规则。首先分析代码库；仅当部署意图不清楚时（例如，数据库、worker、cron）才询问。

**当所有条件都为真时使用直接创建 (MCP)：**
- 单个服务（一个 Web 应用或一个静态站点）
- 没有单独的 worker/cron 服务
- 没有附加的数据库或键值存储
- 仅简单的环境变量（没有共享的环境组）
如果此路径适合且尚未配置 MCP，请停止并在继续之前引导 MCP 设置。

**当任何条件为真时使用蓝图：**
- 多个服务（web + worker、API + 前端等）
- 需要数据库、Redis/键值存储或其他数据存储
- Cron 作业、后台 worker 或私有服务
- 您想要可重现的 IaC 或提交到仓库的 render.yaml
- 需要一致配置的单仓库或多环境设置

如果不确定，请询问一个简短的澄清问题，但为了安全起见，默认使用蓝图。对于单个服务，强烈更喜欢通过 MCP 直接创建，并在需要时引导 MCP 设置。

## 前置条件检查

开始部署时，按顺序验证这些要求：

**1. 确认源路径（Git vs Docker）**

如果使用基于 Git 的方法（蓝图或直接创建），仓库必须推送到 GitHub/GitLab/Bitbucket。引用预构建镜像的蓝图仍然需要带有 `render.yaml` 的 Git 仓库。

```bash
git remote -v
```

- 如果不存在远程，请停止并要求用户创建/推送远程**或**切换到 Docker 镜像部署。

**2. 检查 MCP 工具可用性（单个服务的首选）**

MCP 工具提供最佳体验。通过尝试检查是否可用：
```
list_services()
```

如果 MCP 工具可用，您可以跳过大多数操作的 CLI 安装。

**3. 检查 Render CLI 安装（用于蓝图验证）**
```bash
render --version
```
如果未安装，请提供安装：
- macOS：`brew install render`
- Linux/macOS：`curl -fsSL https://raw.githubusercontent.com/render-oss/cli/main/bin/install.sh | sh`

**4. MCP 设置（如果尚未配置 MCP）**

如果 `list_services()` 因 MCP 未配置而失败，请询问他们是否想设置 MCP（首选）或继续使用 CLI 回退。如果他们选择 MCP，请询问他们使用的是哪个 AI 工具，然后提供下面匹配的说明。始终使用他们的 API 密钥。

### Cursor

引导用户完成这些步骤：

1) 获取 Render API 密钥：
```
https://dashboard.render.com/u/*/settings#api-keys
```

2) 将此添加到 `~/.cursor/mcp.json`（替换 `<YOUR_API_KEY>`）：
```json
{
  "mcpServers": {
    "render": {
      "url": "https://mcp.render.com/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_API_KEY>"
      }
    }
  }
}
```

3) 重启 Cursor，然后重试 `list_services()`。

### Claude Code

引导用户完成这些步骤：

1) 获取 Render API 密钥：
```
https://dashboard.render.com/u/*/settings#api-keys
```

2) 使用 Claude Code 添加 MCP 服务器（替换 `<YOUR_API_KEY>`）：
```bash
claude mcp add --transport http render https://mcp.render.com/mcp --header "Authorization: Bearer <YOUR_API_KEY>"
```

3) 重启 Claude Code，然后重试 `list_services()`。

### Codex

引导用户完成这些步骤：

1) 获取 Render API 密钥：
```
https://dashboard.render.com/u/*/settings#api-keys
```

2) 在他们的 shell 中设置：
```bash
export RENDER_API_KEY="<YOUR_API_KEY>"
```

3) 使用 Codex CLI 添加 MCP 服务器：
```bash
codex mcp add render --url https://mcp.render.com/mcp --bearer-token-env-var RENDER_API_KEY
```

4) 重启 Codex，然后重试 `list_services()`。

### 其他工具

如果用户使用另一个 AI 应用，请引导他们到该工具的 Render MCP 文档以获取设置步骤和安装方法。

### 工作区选择

配置 MCP 后，让用户使用如下提示设置活动的 Render 工作区：

```
将我的 Render 工作区设置为 [WORKSPACE_NAME]
```

**5. 检查身份验证（仅 CLI 回退）**

如果 MCP 不可用，请改用 CLI 并验证您可以访问您的帐户：
```bash
# 检查用户是否登录（使用 -o json 进行非交互模式）
render whoami -o json
```

如果 `render whoami` 失败或返回空数据，则 CLI 未通过身份验证。CLI 不会总是自动提示，因此明确提示用户进行身份验证：

如果两者都未配置，请询问用户更喜欢哪种方法：
- **API 密钥 (CLI)**：`export RENDER_API_KEY="rnd_xxxxx"`（从 https://dashboard.render.com/u/*/settings#api-keys 获取）
- **登录**：`render login`（打开浏览器进行 OAuth）

**6. 检查工作区上下文**

验证活动工作区：
```
get_selected_workspace()
```

或通过 CLI：
```bash
render workspace current -o json
```

要列出可用工作区：
```
list_workspaces()
```

如果用户需要切换工作区，他们必须通过仪表板或 CLI（`render workspace set`）进行。

一旦满足前置条件，请继续部署工作流程。

---

# 方法 1：蓝图部署（推荐用于复杂应用）

## 蓝图工作流程

### 步骤 1：分析代码库

分析代码库以确定框架/运行时、构建和启动命令、所需的环境变量、数据存储和端口绑定。使用 [references/codebase-analysis.md](references/codebase-analysis.md) 中的详细检查清单。

### 步骤 2：生成 render.yaml

按照蓝图规范创建 `render.yaml` 蓝图文件。

完整规范：[references/blueprint-spec.md](references/blueprint-spec.md)

**关键点：**
- 始终使用 `plan: free`，除非用户另有说明
- 包括应用程序需要的所有环境变量
- 使用 `sync: false` 标记机密（用户在仪表板中填写）
- 使用适当的服务类型：`web`、`worker`、`cron`、`static` 或 `pserv`
- 使用适当的运行时：[references/runtimes.md](references/runtimes.md)

**基本结构：**
```yaml
services:
  - type: web
    name: my-app
    runtime: node
    plan: free
    buildCommand: npm ci
    startCommand: npm start
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: postgres
          property: connectionString
      - key: JWT_SECRET
        sync: false  # 用户在仪表板中填写

databases:
  - name: postgres
    databaseName: myapp_db
    plan: free
```

**服务类型：**
- `web`：HTTP 服务、API、Web 应用程序（可公开访问）
- `worker`：后台作业处理器（不可公开访问）
- `cron`：按 cron 计划运行的计划任务
- `static`：静态站点（通过 CDN 提供的 HTML/CSS/JS）
- `pserv`：私有服务（仅内部，在同一帐户内）

服务类型详细信息：[references/service-types.md](references/service-types.md)
运行时选项：[references/runtimes.md](references/runtimes.md)
模板示例：[assets/](assets/)

### 步骤 2.5：立即后续步骤（始终提供）

创建 `render.yaml` 后，始终为用户提供一个简短的、明确的检查清单，并在 CLI 可用时立即运行验证：
1. **身份验证 (CLI)**：运行 `render whoami -o json`（如果未登录，运行 `render login` 或设置 `RENDER_API_KEY`）
2. **验证（推荐）**：运行 `render blueprints validate`
   - 如果未安装 CLI，请提供安装命令。
3. **提交 + 推送**：`git add render.yaml && git commit -m "Add Render deployment configuration" && git push origin main`
4. **打开仪表板**：使用蓝图深度链接并在提示时完成 Git OAuth
5. **填写机密**：设置标记为 `sync: false` 的环境变量
6. **部署**：单击"应用"并监控部署

### 步骤 3：验证配置

在部署之前验证 render.yaml 文件以尽早捕获错误。如果安装了 CLI，请直接运行命令；仅在 CLI 缺失时提示用户：

```bash
render whoami -o json  # 确保 CLI 已通过身份验证（不会总是提示）
render blueprints validate
```

在继续之前修复任何验证错误。常见问题：
- 缺少必需字段（`name`、`type`、`runtime`）
- 无效的运行时值
- 不正确的 YAML 语法
- 无效的环境变量引用

配置指南：[references/configuration-guide.md](references/configuration-guide.md)

### 步骤 4：提交和推送

**重要：**您必须在部署之前将 `render.yaml` 文件合并到您的仓库中。

确保 `render.yaml` 文件已提交并推送到您的 Git 远程：

```bash
git add render.yaml
git commit -m "Add Render deployment configuration"
git push origin main
```

如果还没有 Git 远程，请在此停止并引导用户创建 GitHub/GitLab/Bitbucket 仓库，将其添加为 `origin`，并在继续之前推送。

**为什么这很重要：**仪表板深度链接将从您的仓库读取 render.yaml。如果文件未合并和推送，Render 将找不到配置，部署将失败。

在继续下一步之前，验证文件在您的远程仓库中。

### 步骤 5：生成深度链接

获取 Git 仓库 URL：

```bash
git remote get-url origin
```

这将返回来自您的 Git 提供商的 URL。**如果 URL 是 SSH 格式，请将其转换为 HTTPS：**

| SSH 格式 | HTTPS 格式 |
|------------|--------------|
| `git@github.com:user/repo.git` | `https://github.com/user/repo` |
| `git@gitlab.com:user/repo.git` | `https://gitlab.com/user/repo` |
| `git@bitbucket.org:user/repo.git` | `https://bitbucket.org/user/repo` |

**转换模式：**将 `git@<host>:` 替换为 `https://<host>/` 并删除 `.git` 后缀。

使用 HTTPS 仓库 URL 格式化仪表板深度链接：
```
https://dashboard.render.com/blueprint/new?repo=<REPOSITORY_URL>
```

示例：
```
https://dashboard.render.com/blueprint/new?repo=https://github.com/username/repo-name
```

### 步骤 6：引导用户

**关键：**确保用户在单击深度链接之前已将 render.yaml 文件合并并推送到其仓库。如果文件不在仓库中，Render 无法读取蓝图配置，部署将失败。

向用户提供深度链接和这些说明：

1. **验证 render.yaml 已合并** - 确认文件在 GitHub/GitLab/Bitbucket 上的仓库中存在
2. 单击深度链接打开 Render 仪表板
3. 如果提示，完成 Git 提供商 OAuth
4. 命名蓝图（或使用 render.yaml 中的默认值）
5. 填写机密环境变量（标记为 `sync: false`）
6. 查看服务和数据库配置
7. 单击"应用"进行部署

部署将自动开始。用户可以在 Render 仪表板中监控进度。

### 步骤 7：验证部署

用户通过仪表板部署后，验证一切正常工作。

**通过 MCP 检查部署状态：**
```
list_deploys(serviceId: "<service-id>", limit: 1)
```
查找 `status: "live"` 以确认成功部署。

**检查运行时错误（部署后等待 2-3 分钟）：**
```
list_logs(resource: ["<service-id>"], level: ["error"], limit: 20)
```

**检查服务运行状况指标：**
```
get_metrics(
  resourceId: "<service-id>",
  metricTypes: ["http_request_count", "cpu_usage", "memory_usage"]
)
```

如果发现错误，请继续下面的**部署后验证和基本分流**部分。

---

# 方法 2：直接服务创建（快速单服务部署）

对于没有基础设施即代码的简单部署，通过 MCP 工具直接创建服务。

## 何时使用直接创建

- 单个 Web 服务或静态站点
- 快速原型或演示
- 当您不需要仓库中的 render.yaml 文件时
- 向现有项目添加数据库或 cron 作业

## 直接创建的前置条件

**仓库必须推送到 Git 提供商。**Render 克隆您的仓库以构建和部署服务。

```bash
git remote -v  # 验证远程存在
git push origin main  # 确保代码已推送
```

支持的提供商：GitHub、GitLab、Bitbucket

如果不存在远程，请停止并要求用户创建/推送远程或切换到 Docker 镜像部署。

**注意：**MCP 不支持创建基于镜像的服务。使用仪表板/API 进行预构建 Docker 镜像部署。

## 直接创建工作流程

使用下面的简明步骤，并参阅 [references/direct-creation.md](references/direct-creation.md) 以获取完整的 MCP 命令示例和后续配置。

### 步骤 1：分析代码库
使用 [references/codebase-analysis.md](references/codebase-analysis.md) 确定运行时、构建/启动命令、环境变量和数据存储。

### 步骤 2：通过 MCP 创建资源
创建服务（Web 或静态）和任何所需的数据库或键值存储。请参阅 [references/direct-creation.md](references/direct-creation.md)。

如果 MCP 返回关于缺少 Git 凭据或仓库访问的错误，请停止并引导用户在 Render 仪表板中连接其 Git 提供商，然后重试。

### 步骤 3：配置环境变量
创建后通过 MCP 添加所需的环境变量。请参阅 [references/direct-creation.md](references/direct-creation.md)。

提醒用户，如果他们不想通过 MCP 传递机密，可以在仪表板中设置机密。

### 步骤 4：验证部署
检查部署状态、日志和指标。请参阅 [references/direct-creation.md](references/direct-creation.md)。

---

对于服务发现、配置详细信息、快速命令和常见问题，请参阅 [references/deployment-details.md](references/deployment-details.md)。

---

# 部署后验证和基本分流（所有方法）

保持此简短且可重复。如果任何检查失败，请在重新部署之前修复它。

1. 确认最新部署是 `live` 并正在服务流量
2. 访问运行状况端点（或根）并验证 200 响应
3. 扫描最近的错误日志以查找明确的失败签名
4. 验证所需的环境变量和端口绑定（`0.0.0.0:$PORT`）

详细检查清单和命令：[references/post-deploy-checks.md](references/post-deploy-checks.md)

如果服务无法启动或运行状况检查超时，请使用基本分流指南：
[references/troubleshooting-basics.md](references/troubleshooting-basics.md)

## 故障排除

### 提升网络访问权限

如果部署因网络问题（超时、DNS 错误、连接重置）而失败，请使用提升权限重新运行部署（使用 `sandbox_permissions=require_escalated`）。当沙盒网络阻止出站请求时，部署需要提升网络访问权限。

向用户的示例指导：

```
部署需要提升网络访问权限才能部署到 Render。我可以使用提升权限重新运行命令——您想让我继续吗？
```

可选：如果您需要更深入的诊断（指标/数据库检查/错误目录），建议安装 `render-debug` 技能。它不是核心部署流程所必需的。
