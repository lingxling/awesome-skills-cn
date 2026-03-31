---
name: vercel-cli-with-tokens
description: 使用基于令牌的身份验证在 Vercel 上部署和管理项目。在使用 Vercel CLI 使用访问令牌而非交互式登录时使用 — 例如 "部署到 vercel"、"设置 vercel"、"添加环境变量到 vercel"。
metadata:
  author: vercel
  version: "1.0.0"
---

# Vercel CLI with Tokens

使用 CLI 和基于令牌的身份验证在 Vercel 上部署和管理项目，无需依赖 `vercel login`。

## 步骤 1：定位 Vercel 令牌

在运行任何 Vercel CLI 命令之前，确定令牌的来源。按顺序检查以下场景：

### A) `VERCEL_TOKEN` 已在环境中设置

```bash
printenv VERCEL_TOKEN
```

如果返回了值，则准备就绪。跳转到步骤 2。

### B) 令牌在 `.env` 文件中，变量名为 `VERCEL_TOKEN`

```bash
grep '^VERCEL_TOKEN=' .env 2>/dev/null
```

如果找到，导出它：

```bash
export VERCEL_TOKEN=$(grep '^VERCEL_TOKEN=' .env | cut -d= -f2-)
```

### C) 令牌在 `.env` 文件中，但使用不同的变量名

查找任何看起来像 Vercel 令牌的变量（Vercel 令牌通常以 `vca_` 开头）：

```bash
grep -i 'vercel' .env 2>/dev/null
```

检查输出以确定哪个变量持有令牌，然后将其导出为 `VERCEL_TOKEN`：

```bash
export VERCEL_TOKEN=$(grep '^<VARIABLE_NAME>=' .env | cut -d= -f2-)
```

### D) 未找到令牌 — 询问用户

如果以上方法都没有找到令牌，请用户提供一个。他们可以在 vercel.com/account/tokens 创建 Vercel 访问令牌。

---

**重要提示：** 一旦 `VERCEL_TOKEN` 作为环境变量导出，Vercel CLI 会自动读取它 — **不要将其作为 `--token` 标志传递**。将机密信息放在命令行参数中会暴露在 shell 历史记录和进程列表中。

```bash
# 错误 — 令牌在 shell 历史记录和进程列表中可见
vercel deploy --token "vca_abc123"

# 正确 — CLI 从环境中读取 VERCEL_TOKEN
export VERCEL_TOKEN="vca_abc123"
vercel deploy
```

## 步骤 2：定位项目和团队

同样，检查项目 ID 和团队范围。这些让 CLI 能够定位正确的项目，而无需 `vercel link`。

```bash
# 检查环境
printenv VERCEL_PROJECT_ID
printenv VERCEL_ORG_ID

# 或检查 .env
grep -i 'vercel' .env 2>/dev/null
```

**如果你有项目 URL**（例如 `https://vercel.com/my-team/my-project`），提取团队标识：

```bash
# 例如从 "https://vercel.com/my-team/my-project" 提取 "my-team"
echo "$PROJECT_URL" | sed 's|https://vercel.com/||' | cut -d/ -f1
```

**如果你的环境中同时有 `VERCEL_ORG_ID` 和 `VERCEL_PROJECT_ID`**，导出它们 — CLI 将自动使用这些并跳过任何 `.vercel/` 目录：

```bash
export VERCEL_ORG_ID="<org-id>"
export VERCEL_PROJECT_ID="<project-id>"
```

注意：`VERCEL_ORG_ID` 和 `VERCEL_PROJECT_ID` 必须一起设置 — 只设置其中一个会导致错误。

## CLI 设置

确保已安装 Vercel CLI：

```bash
npm install -g vercel
vercel --version
```

## 部署项目

除非用户明确要求生产环境，否则始终部署为 **预览** 版本。根据你拥有的资源选择方法。

### 快速部署（有项目 ID — 无需链接）

当环境中设置了 `VERCEL_TOKEN` 和 `VERCEL_PROJECT_ID` 时，直接部署：

```bash
vercel deploy -y --no-wait
```

使用团队范围（通过 `VERCEL_ORG_ID` 或 `--scope`）：

```bash
vercel deploy --scope <team-slug> -y --no-wait
```

生产环境（仅在明确要求时）：

```bash
vercel deploy --prod --scope <team-slug> -y --no-wait
```

检查状态：

```bash
vercel inspect <deployment-url>
```

### 完整部署流程（无项目 ID — 需要链接）

当你有令牌和团队但没有预先存在的项目 ID 时使用此方法。

#### 首先检查项目状态

```bash
# 项目是否有 git 远程仓库？
git remote get-url origin 2>/dev/null

# 是否已链接到 Vercel 项目？
cat .vercel/project.json 2>/dev/null || cat .vercel/repo.json 2>/dev/null
```

#### 链接项目

**有 git 远程仓库（推荐）：**

```bash
vercel link --repo --scope <team-slug> -y
```

读取 git 远程仓库并连接到匹配的 Vercel 项目。创建 `.vercel/repo.json`。比普通的 `vercel link` 更可靠，后者按目录名匹配。

**没有 git 远程仓库：**

```bash
vercel link --scope <team-slug> -y
```

创建 `.vercel/project.json`。

**按名称链接到特定项目：**

```bash
vercel link --project <project-name> --scope <team-slug> -y
```

如果项目已链接，检查 `.vercel/project.json` 或 `.vercel/repo.json` 中的 `orgId` 以验证它是否匹配预期的团队。

#### 链接后部署

**A) Git 推送部署 — 有 git 远程仓库（推荐）**

Git 推送会触发自动 Vercel 部署。

1. **推送前询问用户。** 未经明确批准切勿推送。
2. 提交并推送：
   ```bash
   git add .
   git commit -m "deploy: <更改描述>"
   git push
   ```
3. Vercel 自动构建。非生产分支获得预览部署。
4. 获取部署 URL：
   ```bash
   sleep 5
   vercel ls --format json --scope <team-slug>
   ```
   在 `deployments` 数组中找到最新条目。

**B) CLI 部署 — 无 git 远程仓库**

```bash
vercel deploy --scope <team-slug> -y --no-wait
```

检查状态：

```bash
vercel inspect <deployment-url>
```

### 从远程仓库部署（代码未在本地克隆）

1. 克隆仓库：
   ```bash
   git clone <repo-url>
   cd <repo-name>
   ```
2. 链接到 Vercel：
   ```bash
   vercel link --repo --scope <team-slug> -y
   ```
3. 通过 git 推送（如果你有推送权限）或 CLI 部署。

### 关于 `.vercel/` 目录

链接的项目具有以下之一：
- `.vercel/project.json` — 来自 `vercel link`。包含 `projectId` 和 `orgId`。
- `.vercel/repo.json` — 来自 `vercel link --repo`。包含 `orgId`、`remoteName` 和 `projects` 映射。

当环境中同时设置了 `VERCEL_ORG_ID` + `VERCEL_PROJECT_ID` 时不需要。

**不要**在未链接的目录中运行 `vercel ls`、`vercel project inspect` 或 `vercel link` 来检测状态 — 它们会交互式提示或作为副作用静默链接。只有 `vercel whoami` 可以在任何地方安全运行。

## 管理环境变量

```bash
# 为所有环境设置
echo "value" | vercel env add VAR_NAME --scope <team-slug>

# 为特定环境设置（production、preview、development）
echo "value" | vercel env add VAR_NAME production --scope <team-slug>

# 列出环境变量
vercel env ls --scope <team-slug>

# 将环境变量拉取到本地 .env 文件
vercel env pull --scope <team-slug>

# 删除变量
vercel env rm VAR_NAME --scope <team-slug> -y
```

## 检查部署

```bash
# 列出最近的部署
vercel ls --format json --scope <team-slug>

# 检查特定部署
vercel inspect <deployment-url>

# 查看构建日志
vercel logs <deployment-url>
```

## 管理域名

```bash
# 列出域名
vercel domains ls --scope <team-slug>

# 将域名添加到项目
vercel domains add <domain> --scope <team-slug>
```

## 工作协议

- **永远不要将 `VERCEL_TOKEN` 作为 `--token` 标志传递。** 将其导出为环境变量，让 CLI 原生读取它。
- **在询问用户之前先检查环境中的令牌。** 首先查看当前环境和 `.env` 文件。
- **默认为预览部署。** 仅在明确要求时部署到生产环境。
- **推送到 git 之前先询问。** 未经用户批准切勿推送提交。
- **不要直接读取或修改 `.vercel/` 文件。** CLI 管理此目录。
- **不要 curl/fetch 已部署的 URL 来验证。** 只需将链接返回给用户。
- **使用 `--format json`** 当结构化输出有助于后续步骤时。
- **使用 `-y`** 在提示确认的命令上以避免交互式阻塞。

## 故障排除

### 未找到令牌

检查环境和任何存在的 `.env` 文件：

```bash
printenv | grep -i vercel
grep -i vercel .env 2>/dev/null
```

### 身份验证错误

如果 CLI 失败并显示 `Authentication required`：
- 令牌可能已过期或无效。
- 验证：`vercel whoami`（使用环境中的 `VERCEL_TOKEN`）。
- 向用户索取新的令牌。

### 错误的团队

验证范围是否正确：

```bash
vercel whoami --scope <team-slug>
```

### 构建失败

检查构建日志：

```bash
vercel logs <deployment-url>
```

常见原因：
- 缺少依赖 — 确保 `package.json` 完整并已提交。
- 缺少环境变量 — 使用 `vercel env add` 添加。
- 框架配置错误 — 检查 `vercel.json`。Vercel 从 `package.json` 自动检测框架（Next.js、Remix、Vite 等）；如果检测错误，使用 `vercel.json` 覆盖。

### CLI 未安装

```bash
npm install -g vercel
```
