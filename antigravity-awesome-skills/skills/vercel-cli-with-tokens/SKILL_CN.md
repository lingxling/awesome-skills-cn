---
name: vercel-cli-with-tokens
description: "使用基于令牌的身份验证在 Vercel 上部署和管理项目。当使用访问令牌而不是交互式登录来处理 Vercel CLI 时使用——例如\"部署到 vercel\"、\"设置 vercel\"、\"添加环境变量到 vercel\"。"
risk: safe
source: "https://github.com/vercel-labs/agent-skills"
date_added: "2026-06-02"
---

# 带令牌的 Vercel CLI

使用带有基于令牌的身份验证的 CLI 在 Vercel 上部署和管理项目，无需依赖 `vercel login`。

## 何时使用
- 当任务符合此描述时使用此技能：使用基于令牌的身份验证在 Vercel 上部署和管理项目。当使用访问令牌而不是交互式登录来处理 Vercel CLI 时使用——例如"部署到 vercel"、"设置 vercel"、"添加环境变量到 vercel"。

## 第 1 步：定位 Vercel 令牌

在运行任何 Vercel CLI 命令之前，确定令牌来自何处。按顺序执行以下场景：

### A) 环境中已设置 `VERCEL_TOKEN`

```bash
[ -n "${VERCEL_TOKEN:-}" ] && printf 'VERCEL_TOKEN is set\n'
```

如果这报告了配置的令牌，您已准备好。跳到第 2 步。

### B) 令牌在 `.env` 文件的 `VERCEL_TOKEN` 下

```bash
grep -q '^VERCEL_TOKEN=' .env 2>/dev/null && printf 'VERCEL_TOKEN is present in .env\n'
```

如果找到，导出它：

```bash
VERCEL_TOKEN="$(sed -n 's/^VERCEL_TOKEN=//p' .env | tail -n 1)"
export VERCEL_TOKEN
```

### C) 令牌在 `.env` 文件中但名称不同

查找看起来像 Vercel 令牌的任何变量 (Vercel 令牌通常以 `vca_` 开头)：

```bash
grep -Eio '^[A-Z0-9_]*VERCEL[A-Z0-9_]*(?==)' .env 2>/dev/null
```

检查输出以识别哪个变量持有令牌，然后将其导出为 `VERCEL_TOKEN`：

```bash
vercel_var="<VARIABLE_NAME>"
VERCEL_TOKEN="$(sed -n "s/^${vercel_var}=//p" .env | tail -n 1)"
export VERCEL_TOKEN
```

### D) 未找到令牌——询问用户

如果上述任何方法都没有产生令牌，请要求用户提供一个。他们可以在 vercel.com/account/tokens 创建 Vercel 访问令牌。

---

**重要**：一旦 `VERCEL_TOKEN` 导出为环境变量，Vercel CLI 原生读取它——**不要将其作为 `--token` 标志传递**。将机密放在命令行参数中会在 shell 历史和进程列表中暴露它们。

```bash
# 不好——令牌在 shell 历史和进程列表中可见
vercel deploy --token "vca_abc123"

# 好——CLI 从环境中读取 VERCEL_TOKEN
[ -n "${VERCEL_TOKEN:-}" ] || { echo "Set VERCEL_TOKEN first" >&2; exit 1; }
vercel deploy
```

## 第 2 步：定位项目和团队

类似地，检查项目 ID 和团队范围。这些允许 CLI 定位正确的项目而无需 `vercel link`。

```bash
# 检查环境
[ -n "${VERCEL_PROJECT_ID:-}" ] && printf 'VERCEL_PROJECT_ID is set\n'
[ -n "${VERCEL_ORG_ID:-}" ] && printf 'VERCEL_ORG_ID is set\n'

# 或检查 .env
grep -Eio '^[A-Z0-9_]*VERCEL[A-Z0-9_]*(?==)' .env 2>/dev/null
```

**如果您有项目 URL** (例如 `https://vercel.com/my-team/my-project`)，提取团队 slug：

```bash
# 例如从 "https://vercel.com/my-team/my-project" 中提取 "my-team"
echo "$PROJECT_URL" | sed 's|https://vercel.com/||' | cut -d/ -f1
```

**如果您的环境中同时拥有 `VERCEL_ORG_ID` 和 `VERCEL_PROJECT_ID`**，导出它们——CLI 将自动使用这些并跳过任何 `.vercel/` 目录：

```bash
export VERCEL_ORG_ID="<org-id>"
export VERCEL_PROJECT_ID="<project-id>"
```

注意：`VERCEL_ORG_ID` 和 `VERCEL_PROJECT_ID` 必须一起设置——仅设置其中一个会导致错误。

## CLI 设置

确保安装了 Vercel CLI 并且是最新的：

```bash
npm install -g vercel
vercel --version
```

## 部署项目

除非用户明确请求生产，否则始终部署为**预览**。根据可用内容选择方法。

### 快速部署 (拥有项目 ID——无需链接)

当环境中设置了 `VERCEL_TOKEN` 和 `VERCEL_PROJECT_ID` 时，直接部署：

```bash
vercel deploy -y --no-wait
```

使用团队范围 (通过 `VERCEL_ORG_ID` 或 `--scope`)：

```bash
vercel deploy --scope <team-slug> -y --no-wait
```

生产 (仅在明确请求时)：

```bash
vercel deploy --prod --scope <team-slug> -y --no-wait
```

检查状态：

```bash
vercel inspect <deployment-url>
```

### 完整部署流程 (无项目 ID——需要链接)

当您拥有令牌和团队但没有预先存在的项目 ID 时，使用此方法。

#### 首先检查项目状态

```bash
# 项目是否有 git 远程？
git remote get-url origin 2>/dev/null

# 它是否已链接到 Vercel 项目？
cat .vercel/project.json 2>/dev/null || cat .vercel/repo.json 2>/dev/null
```

#### 链接项目

**使用 git 远程 (首选)：**

```bash
vercel link --repo --scope <team-slug> -y
```

读取 git 远程并连接到匹配的 Vercel 项目。创建 `.vercel/repo.json`。比普通 `vercel link` 更可靠，后者通过目录名称匹配。

**不使用 git 远程：**

```bash
vercel link --scope <team-slug> -y
```

创建 `.vercel/project.json`。

**按名称链接到特定项目：**

```bash
vercel link --project <project-name> --scope <team-slug> -y
```

如果项目已链接，检查 `.vercel/project.json` 或 `.vercel/repo.json` 中的 `orgId` 以验证它是否与预期的团队匹配。

#### 链接后部署

**A) Git 推送部署——有 git 远程 (首选)**

Git 推送触发自动 Vercel 部署。

1. **在推送前询问用户。** 永远不要在没有明确批准的情况下推送。
2. 提交并推送：
   ```bash
   git add .
   git commit -m "deploy: <description of changes>"
   git push
   ```
3. Vercel 自动构建。非生产分支获得预览部署。
4. 检索部署 URL：
   ```bash
   sleep 5
   vercel ls --format json --scope <team-slug>
   ```
   在 `deployments` 数组中查找最新条目。

**B) CLI 部署——无 git 远程**

```bash
vercel deploy --scope <team-slug> -y --no-wait
```

检查状态：

```bash
vercel inspect <deployment-url>
```

### 从远程存储库部署 (代码未在本地克隆)

1. 克隆存储库：
   ```bash
   git clone <repo-url>
   cd <repo-name>
   ```
2. 链接到 Vercel：
   ```bash
   vercel link --repo --scope <team-slug> -y
   ```
3. 通过 git 推送 (如果您有推送访问权限) 或 CLI 部署进行部署。

### 关于 `.vercel/` 目录

链接的项目具有以下之一：
- `.vercel/project.json` — 来自 `vercel link`。包含 `projectId` 和 `orgId`。
- `.vercel/repo.json` — 来自 `vercel link --repo`。包含 `orgId`、`remoteName` 和 `projects` 映射。

当环境中设置了 `VERCEL_ORG_ID` + `VERCEL_PROJECT_ID` 时不需要。

**不要**在未链接的目录中运行 `vercel project inspect` 或 `vercel link` 来检测状态——它们会以交互方式提示或作为副作用无声地链接。`vercel ls` 是安全的 (在未链接的目录中，默认显示范围内所有部署)。`vercel whoami` 在任何地方都是安全的。

## 管理环境变量

```bash
# 为所有环境设置
echo "value" | vercel env add VAR_NAME --scope <team-slug>

# 为特定环境设置 (production、preview、development)
echo "value" | vercel env add VAR_NAME production --scope <team-slug>

# 列出环境变量
vercel env ls --scope <team-slug>

# 将环境变量拉到本地 .env.local 文件
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

# 查看构建日志 (需要 Vercel CLI v35+)
vercel inspect <deployment-url> --logs

# 查看运行时请求日志 (默认实时跟踪；添加 --no-follow 以获得一次性快照)
vercel logs <deployment-url>
```

## 管理域

```bash
# 列出域
vercel domains ls --scope <team-slug>

# 将域添加到项目——链接或环境链接目录 (1 个参数)
vercel domains add <domain> --scope <team-slug>

# 添加域——未链接目录 (需要 <project> 位置参数)
vercel domains add <domain> <project> --scope <team-slug>
```

## Stripe 项目计划变更

如果此项目由 Stripe Projects 管理。**在运行任何付费或破坏性计划变更前询问用户**——升级会向真实卡计费，降级会删除席位。

首先运行 `stripe projects status --json` 以确认 Vercel 资源的本地名称。以下示例假设默认值 (`vercel-plan`)；如果在 `stripe projects add` 时重命名，则替换实际名称。

- **升级到 Pro**：`stripe projects add vercel/pro` (或 `stripe projects upgrade vercel-plan pro`)
- **降级到 Hobby**：`stripe projects downgrade vercel-plan hobby`

### Pro 提供的功能

- $20/月平台费，包括 $20/月使用信用。
- 新项目默认使用 Turbo 构建机器 (30 vCPU、60 GB 内存)——比 Hobby 快得多的构建。
- 1 个部署席位 + 无限免费查看者席位 (只读协作者、预览评论)。
- 更高的包含分配 (1 TB 快速数据传输、每月 1000 万个边缘请求)。
- 付费附加服务可用：SAML SSO、HIPAA BAA、Flags Explorer、Observability Plus、Speed Insights、Web Analytics Plus。

完整详情：https://vercel.com/docs/plans/pro-plan

## 工作协议

- **永远不要将 `VERCEL_TOKEN` 作为 `--token` 标志传递。** 将其导出为环境变量并让 CLI 原生读取它。
- **在询问用户前检查环境中的令牌。** 首先查看当前环境和 `.env` 文件。
- **默认为预览部署。** 仅在明确要求时部署到生产。
- **在推送到 git 前询问。** 永远不要在没有用户批准的情况下推送提交。
- **不要直接修改 `.vercel/` 文件。** CLI 管理此目录。读取它们 (例如验证 `orgId`) 是可以的。
- **不要 curl/fetch 已部署的 URL 来验证。** 只是将链接返回给用户。
- **使用 `--format json`** 当结构化输出将帮助后续步骤时。
- **在提示确认的命令中使用 `-y`** 以避免交互式阻塞。

## 故障排除

### 未找到令牌

检查环境和任何存在的 `.env` 文件：

```bash
env | grep -Eio '^[A-Z0-9_]*VERCEL[A-Z0-9_]*(?==)'
grep -Eio '^[A-Z0-9_]*VERCEL[A-Z0-9_]*(?==)' .env 2>/dev/null
```

### 身份验证错误

如果 CLI 失败并出现 `Authentication required`：
- 令牌可能已过期或无效。
- 验证：`vercel whoami` (使用环境中的 `VERCEL_TOKEN`)。
- 向用户要求新令牌。

### 错误的团队

验证范围是否正确：

```bash
vercel whoami --scope <team-slug>
```

### 构建失败

检查构建日志：

```bash
vercel inspect <deployment-url> --logs
```

常见原因：
- 缺少依赖——确保 `package.json` 完整且已提交。
- 缺少环境变量——使用 `vercel env add` 添加。
- 框架配置错误——检查 `vercel.json`。Vercel 从 `package.json` 自动检测框架 (Next.js、Remix、Vite 等)；如果检测错误，使用 `vercel.json` 覆盖。

### CLI 未安装

```bash
npm install -g vercel
```

## 限制
- 仅当任务明确符合上述范围时，才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并要求澄清。
