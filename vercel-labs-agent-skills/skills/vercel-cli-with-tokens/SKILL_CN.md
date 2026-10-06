---
name: vercel-cli-with-tokens
description: 使用基于令牌的身份验证在 Vercel 上部署和管理项目。适用于使用访问令牌而非交互式登录来操作 Vercel CLI 的场景——例如"部署到 vercel"、"设置 vercel"、"向 vercel 添加环境变量"。
metadata:
  author: vercel
  version: "1.0.0"
---

# 使用令牌的 Vercel CLI

使用基于令牌身份验证的 CLI 在 Vercel 上部署和管理项目，而无需依赖 `vercel login`。

## 步骤 1：定位 Vercel 令牌

在运行任何 Vercel CLI 命令之前，先确定令牌的来源。请按顺序依次处理以下场景：

### A) 环境中已设置 `VERCEL_TOKEN`

```bash
printenv VERCEL_TOKEN
```

如果返回了值，就可以继续了。跳到步骤 2。

### B) 令牌位于 `.env` 文件中的 `VERCEL_TOKEN` 下

```bash
grep '^VERCEL_TOKEN=' .env 2>/dev/null
```

如果找到，则将其导出：

```bash
export VERCEL_TOKEN=$(grep '^VERCEL_TOKEN=' .env | cut -d= -f2-)
```

### C) 令牌位于 `.env` 文件中，但变量名不同

查找任何看起来像 Vercel 令牌的变量（Vercel 令牌通常以 `vca_` 开头）：

```bash
grep -i 'vercel' .env 2>/dev/null
```

检查输出以确定哪个变量保存着令牌，然后将其导出为 `VERCEL_TOKEN`：

```bash
export VERCEL_TOKEN=$(grep '^<VARIABLE_NAME>=' .env | cut -d= -f2-)
```

### D) 未找到令牌——询问用户

如果以上都没有找到令牌，请让用户提供一个。他们可以在 vercel.com/account/tokens 创建 Vercel 访问令牌。

---

**重要：**一旦 `VERCEL_TOKEN` 被导出为环境变量，Vercel CLI 就会原生读取它——**不要将其作为 `--token` 标志传递**。将密钥放在命令行参数中会使其暴露在 shell 历史记录和进程列表中。

```bash
# Bad — token visible in shell history and process listings
vercel deploy --token "vca_abc123"

# Good — CLI reads VERCEL_TOKEN from the environment
export VERCEL_TOKEN="vca_abc123"
vercel deploy
```

## 步骤 2：定位项目和团队

同样地，检查项目 ID 和团队范围（scope）。这使 CLI 无需 `vercel link` 即可定位到正确的项目。

```bash
# Check environment
printenv VERCEL_PROJECT_ID
printenv VERCEL_ORG_ID

# Or check .env
grep -i 'vercel' .env 2>/dev/null
```

**如果你有项目 URL**（例如 `https://vercel.com/my-team/my-project`），请提取团队 slug：

```bash
# e.g. "my-team" from "https://vercel.com/my-team/my-project"
echo "$PROJECT_URL" | sed 's|https://vercel.com/||' | cut -d/ -f1
```

**如果你的环境中同时有 `VERCEL_ORG_ID` 和 `VERCEL_PROJECT_ID`**，请将它们导出——CLI 会自动使用它们并跳过任何 `.vercel/` 目录：

```bash
export VERCEL_ORG_ID="<org-id>"
export VERCEL_PROJECT_ID="<project-id>"
```

注意：`VERCEL_ORG_ID` 和 `VERCEL_PROJECT_ID` 必须同时设置——只设置其中一个会导致错误。

## CLI 设置

确保已安装 Vercel CLI 且为最新版本：

```bash
npm install -g vercel
vercel --version
```

## 部署项目

除非用户明确要求生产环境，否则始终以**预览（preview）**方式部署。根据你手头可用的条件选择一种方法。

### 快速部署（已有项目 ID——无需关联）

当环境中设置了 `VERCEL_TOKEN` 和 `VERCEL_PROJECT_ID` 时，直接部署：

```bash
vercel deploy -y --no-wait
```

带团队范围（通过 `VERCEL_ORG_ID` 或 `--scope`）：

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

### 完整部署流程（无项目 ID——需要关联）

当你有令牌和团队，但没有现成的项目 ID 时使用此流程。

#### 先检查项目状态

```bash
# Does the project have a git remote?
git remote get-url origin 2>/dev/null

# Is it already linked to a Vercel project?
cat .vercel/project.json 2>/dev/null || cat .vercel/repo.json 2>/dev/null
```

#### 关联项目

**有 git 远程仓库（首选）：**

```bash
vercel link --repo --scope <team-slug> -y
```

读取 git 远程仓库并连接到匹配的 Vercel 项目。创建 `.vercel/repo.json`。比普通的 `vercel link`（按目录名匹配）更可靠。

**没有 git 远程仓库：**

```bash
vercel link --scope <team-slug> -y
```

创建 `.vercel/project.json`。

**按名称关联到特定项目：**

```bash
vercel link --project <project-name> --scope <team-slug> -y
```

如果项目已经关联，请检查 `.vercel/project.json` 或 `.vercel/repo.json` 中的 `orgId`，以验证其与目标团队相符。

#### 关联后部署

**A) Git 推送部署——有 git 远程仓库（首选）**

Git 推送会触发 Vercel 的自动部署。

1. **推送前先询问用户。**未经明确批准绝不推送。
2. 提交并推送：
   ```bash
   git add .
   git commit -m "deploy: <description of changes>"
   git push
   ```
3. Vercel 会自动构建。非生产分支会获得预览部署。
4. 获取部署 URL：
   ```bash
   sleep 5
   vercel ls --format json --scope <team-slug>
   ```
   在 `deployments` 数组中找到最新的条目。

**B) CLI 部署——没有 git 远程仓库**

```bash
vercel deploy --scope <team-slug> -y --no-wait
```

检查状态：

```bash
vercel inspect <deployment-url>
```

### 从远程仓库部署（代码未克隆到本地）

1. 克隆仓库：
   ```bash
   git clone <repo-url>
   cd <repo-name>
   ```
2. 关联到 Vercel：
   ```bash
   vercel link --repo --scope <team-slug> -y
   ```
3. 通过 git 推送部署（如果你有推送权限）或使用 CLI 部署。

### 关于 `.vercel/` 目录

已关联的项目具有以下之一：
- `.vercel/project.json` — 来自 `vercel link`。包含 `projectId` 和 `orgId`。
- `.vercel/repo.json` — 来自 `vercel link --repo`。包含 `orgId`、`remoteName` 以及一个 `projects` 映射。

当环境中同时设置了 `VERCEL_ORG_ID` + `VERCEL_PROJECT_ID` 时则不需要。

**不要**在未关联的目录中运行 `vercel project inspect` 或 `vercel link` 来检测状态——它们会交互式地提示，或作为副作用悄悄地完成关联。`vercel ls` 是安全的（在未关联的目录中，它默认显示该范围内的所有部署）。`vercel whoami` 在任何位置都是安全的。

## 管理环境变量

```bash
# Set for all environments
echo "value" | vercel env add VAR_NAME --scope <team-slug>

# Set for a specific environment (production, preview, development)
echo "value" | vercel env add VAR_NAME production --scope <team-slug>

# List environment variables
vercel env ls --scope <team-slug>

# Pull env vars to local .env.local file
vercel env pull --scope <team-slug>

# Remove a variable
vercel env rm VAR_NAME --scope <team-slug> -y
```

## 检查部署

```bash
# List recent deployments
vercel ls --format json --scope <team-slug>

# Inspect a specific deployment
vercel inspect <deployment-url>

# View build logs (requires Vercel CLI v35+)
vercel inspect <deployment-url> --logs

# View runtime request logs (follows live by default; add --no-follow for a one-shot snapshot)
vercel logs <deployment-url>
```

## 管理域名

```bash
# List domains
vercel domains ls --scope <team-slug>

# Add a domain to the project — linked or env-linked directory (1 arg)
vercel domains add <domain> --scope <team-slug>

# Add a domain — unlinked directory (requires <project> positional)
vercel domains add <domain> <project> --scope <team-slug>
```

## Stripe Projects 套餐变更

如果该项目由 Stripe Projects 管理。**在执行任何付费或破坏性的套餐变更之前，先询问用户**——升级会向真实银行卡收费，降级会移除席位。

首先运行 `stripe projects status --json` 以确认 Vercel 资源的本地名称。下面的示例假定使用默认名称（`vercel-plan`）；如果在 `stripe projects add` 时被重命名，请替换为实际名称。

- **升级到 Pro：**`stripe projects add vercel/pro`（或 `stripe projects upgrade vercel-plan pro`）
- **降级到 Hobby：**`stripe projects downgrade vercel-plan hobby`

### Pro 提供的内容

- 每月 20 美元的平台费用，包含每月 20 美元的用量额度。
- 新项目默认使用 Turbo 构建机器（30 个 vCPU、60 GB 内存）——构建速度明显快于 Hobby。
- 1 个部署席位 + 不限数量的免费 Viewer 席位（只读协作者、预览评论）。
- 更高的包含额度（每月 1 TB Fast Data Transfer、1000 万次 Edge Requests）。
- 可选的付费附加组件：SAML SSO、HIPAA BAA、Flags Explorer、Observability Plus、Speed Insights、Web Analytics Plus。

完整详情：https://vercel.com/docs/plans/pro-plan

## 工作约定

- **绝不将 `VERCEL_TOKEN` 作为 `--token` 标志传递。**将其导出为环境变量，让 CLI 原生读取。
- **在询问用户之前先检查环境中的令牌。**首先查看当前环境和 `.env` 文件。
- **默认使用预览部署。**仅在明确要求时才部署到生产环境。
- **推送到 git 之前先询问。**未经用户批准绝不推送提交。
- **不要直接修改 `.vercel/` 文件。**该目录由 CLI 管理。读取它们（例如验证 `orgId`）是可以的。
- **不要通过 curl/fetch 访问已部署的 URL 来验证。**只需将链接返回给用户。
- 当结构化输出有助于后续步骤时，**使用 `--format json`**。
- 对会提示确认的命令**使用 `-y`**，以避免交互式阻塞。

## 故障排查

### 未找到令牌

检查环境以及存在的任何 `.env` 文件：

```bash
printenv | grep -i vercel
grep -i vercel .env 2>/dev/null
```

### 身份验证错误

如果 CLI 因 `Authentication required` 而失败：
- 令牌可能已过期或无效。
- 验证：`vercel whoami`（使用环境中的 `VERCEL_TOKEN`）。
- 向用户索取新的令牌。

### 团队错误

验证范围是否正确：

```bash
vercel whoami --scope <team-slug>
```

### 构建失败

查看构建日志：

```bash
vercel inspect <deployment-url> --logs
```

常见原因：
- 缺少依赖项——确保 `package.json` 完整并已提交。
- 缺少环境变量——使用 `vercel env add` 添加。
- 框架配置错误——检查 `vercel.json`。Vercel 会从 `package.json` 自动检测框架（Next.js、Remix、Vite 等）；如果检测有误，可通过 `vercel.json` 覆盖。

### 未安装 CLI

```bash
npm install -g vercel
```
