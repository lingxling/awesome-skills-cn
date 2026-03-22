---
name: deploy-to-vercel
description: 将应用程序和网站部署到Vercel。当用户请求部署操作时使用，如"部署我的应用"、"部署并给我链接"、"推送到线上"或"创建预览部署"。
metadata:
  author: vercel
  version: "3.0.0"
---

# 部署到Vercel

将任何项目部署到Vercel。**始终以预览方式部署**（而非生产），除非用户明确要求生产环境。

目标是让用户进入最佳的长期设置：他们的项目链接到Vercel，通过git push进行部署。以下每种方法都试图让用户更接近这种状态。

## 步骤1：收集项目状态

在决定使用哪种方法之前，运行所有四项检查：

```bash
# 1. 检查git远程仓库
git remote get-url origin 2>/dev/null

# 2. 检查是否本地链接到Vercel项目（任一文件存在即表示已链接）
cat .vercel/project.json 2>/dev/null || cat .vercel/repo.json 2>/dev/null

# 3. 检查Vercel CLI是否已安装并已认证
vercel whoami 2>/dev/null

# 4. 列出可用团队（如果已认证）
vercel teams list --format json 2>/dev/null
```

### 团队选择

如果用户属于多个团队，将所有可用的团队slug以项目符号列表形式呈现，并询问部署到哪个团队。一旦用户选择了团队，立即进入下一步 — 不要要求额外确认。

在所有后续CLI命令（`vercel deploy`、`vercel link`、`vercel inspect`等）上通过`--scope`传递团队slug：

```bash
vercel deploy [path] -y --no-wait --scope <team-slug>
```

如果项目已经链接（存在`.vercel/project.json`或`.vercel/repo.json`），这些文件中的`orgId`决定了团队 — 无需再次询问。如果只有一个团队（或只是个人账户），跳过提示并直接使用。

**关于`.vercel/`目录：** 链接的项目有以下两种文件之一：
- `.vercel/project.json` — 由`vercel link`创建（单个项目链接）。包含`projectId`和`orgId`。
- `.vercel/repo.json` — 由`vercel link --repo`创建（基于仓库的链接）。包含`orgId`、`remoteName`和将目录映射到Vercel项目ID的`projects`数组。

任一文件都表示项目已链接。检查两者。

**不要**在未链接的目录中使用`vercel project inspect`、`vercel ls`或`vercel link`来检测状态 — 没有`.vercel/`配置，它们会交互式提示（或使用`--yes`时，作为副作用静默链接）。只有`vercel whoami`可以在任何地方安全运行。

## 步骤2：选择部署方法

### 已链接（存在`.vercel/`）+ 有git远程仓库 → Git推送

这是理想状态。项目已链接并具有git集成。

1. **推送前询问用户**。未经明确批准，永远不要推送：
   ```
   此项目通过git连接到Vercel。我可以提交并推送来触发部署。是否要继续？
   ```

2. **提交并推送：**
   ```bash
   git add .
   git commit -m "deploy: <更改描述>"
   git push
   ```
   Vercel会自动从推送中构建。非生产分支获得预览部署；生产分支（通常是`main`）获得生产部署。

3. **获取预览URL**。如果CLI已认证：
   ```bash
   sleep 5
   vercel ls --format json
   ```
   JSON输出有一个`deployments`数组。找到最新条目 — 其`url`字段是预览URL。

   如果CLI未认证，告诉用户检查Vercel仪表板或其git提供商上的提交状态检查以获取预览URL。

---

### 已链接（存在`.vercel/`）+ 无git远程仓库 → `vercel deploy`

项目已链接但没有git仓库。直接使用CLI部署。

```bash
vercel deploy [path] -y --no-wait
```

使用`--no-wait`，这样CLI会立即返回部署URL，而不是阻塞直到构建完成（构建可能需要一段时间）。然后使用以下命令检查部署状态：

```bash
vercel inspect <deployment-url>
```

对于生产部署（仅当用户明确要求时）：
```bash
vercel deploy [path] --prod -y --no-wait
```

---

### 未链接 + CLI已认证 → 先链接，然后部署

CLI正常工作但项目尚未链接。这是让用户进入最佳状态的机会。

1. **询问用户部署到哪个团队**。将步骤1中的团队slug以项目符号列表形式呈现。如果只有一个团队（或只是个人账户），跳过此步骤。

2. **一旦选择了团队，直接进行链接**。告诉用户会发生什么，但不要要求单独确认：
   ```
   将此项目链接到Vercel上的<团队名称>。这将创建一个Vercel项目进行部署，并在未来的git推送时启用自动部署。
   ```

3. **如果存在git远程仓库**，使用基于仓库的链接并指定所选团队范围：
   ```bash
   vercel link --repo --scope <team-slug>
   ```
   这会读取git远程URL并将其与从该仓库部署的现有Vercel项目匹配。它会创建`.vercel/repo.json`。这比`vercel link`（不带`--repo`）更可靠，后者尝试按目录名称匹配，当本地文件夹和Vercel项目命名不同时经常失败。

   **如果没有git远程仓库**，回退到标准链接：
   ```bash
   vercel link --scope <team-slug>
   ```
   这会提示用户选择或创建项目。它会创建`.vercel/project.json`。

4. **然后使用最佳可用方法部署：**
   - 如果存在git远程仓库 → 提交并推送（参见上面的git推送方法）
   - 如果没有git远程仓库 → `vercel deploy [path] -y --no-wait --scope <team-slug>`，然后`vercel inspect <url>`检查状态

---

### 未链接 + CLI未认证 → 安装、认证、链接、部署

Vercel CLI完全未设置。

1. **安装CLI（如果尚未安装）：**
   ```bash
   npm install -g vercel
   ```

2. **认证：**
   ```bash
   vercel login
   ```
   用户在浏览器中完成认证。如果在无法登录的非交互式环境中运行，跳转到下面的**无认证回退**。

3. **询问部署到哪个团队** — 将`vercel teams list --format json`中的团队slug以项目符号列表形式呈现。如果只有一个团队/个人账户，跳过。一旦选择，立即继续。

4. **使用所选团队范围链接项目**（如果存在git远程仓库，使用`--repo`，否则使用普通`vercel link`）：
   ```bash
   vercel link --repo --scope <team-slug>   # 如果存在git远程仓库
   vercel link --scope <team-slug>          # 如果没有git远程仓库
   ```

5. **部署**使用最佳可用方法（如果存在远程仓库，使用git推送，否则使用`vercel deploy -y --no-wait --scope <team-slug>`，然后`vercel inspect <url>`检查状态）。

---

### 无认证回退 — claude.ai 沙盒

**使用时机：** 当CLI无法在claude.ai沙盒中安装或认证时的最后手段。这不需要认证 — 它返回一个**预览URL**（实时站点）和一个**认领URL**（转移到您的Vercel账户）。

```bash
bash /mnt/skills/user/deploy-to-vercel/resources/deploy.sh [path]
```

**参数：**
- `path` - 要部署的目录，或`.tgz`文件（默认为当前目录）

**示例：**
```bash
# 部署当前目录
bash /mnt/skills/user/deploy-to-vercel/resources/deploy.sh

# 部署特定项目
bash /mnt/skills/user/deploy-to-vercel/resources/deploy.sh /path/to/project

# 部署现有压缩包
bash /mnt/skills/user/deploy-to-vercel/resources/deploy.sh /path/to/project.tgz
```

脚本会自动从`package.json`检测框架，打包项目（排除`node_modules`、`.git`、`.env`），上传并等待构建完成。

**告诉用户：** "您的部署已准备就绪，地址为[previewUrl]。在[claimUrl]认领它以管理您的部署。"

---

### 无认证回退 — Codex 沙盒

**使用时机：** 在Codex沙盒中，CLI可能未认证。Codex默认在沙盒环境中运行 — 首先尝试CLI，如果认证失败，回退到部署脚本。

1. **检查Vercel CLI是否已安装**（此检查不需要权限提升）：
   ```bash
   command -v vercel
   ```

2. **如果`vercel`已安装**，尝试使用CLI部署：
   ```bash
   vercel deploy [path] -y --no-wait
   ```

3. **如果`vercel`未安装，或CLI失败并显示"No existing credentials found"**，使用回退脚本：
   ```bash
   skill_dir="<skill路径>"

   # 部署当前目录
   bash "$skill_dir/resources/deploy-codex.sh"

   # 部署特定项目
   bash "$skill_dir/resources/deploy-codex.sh" /path/to/project

   # 部署现有压缩包
   bash "$skill_dir/resources/deploy-codex.sh" /path/to/project.tgz
   ```

脚本处理框架检测、打包和部署。它等待构建完成并返回包含`previewUrl`和`claimUrl`的JSON。

**告诉用户：** "您的部署已准备就绪，地址为[previewUrl]。在[claimUrl]认领它以管理您的部署。"

**提升网络访问：** 仅当沙盒阻止网络调用时（`sandbox_permissions=require_escalated`）才提升实际部署命令的权限。**不要**提升`command -v vercel`检查。

---

## 代理特定说明

### Claude Code / 基于终端的代理

您拥有完整的shell访问权限。**不要**使用`/mnt/skills/`路径。直接使用CLI按照上述决策流程操作。

对于无认证回退，从技能的安装位置运行部署脚本：
```bash
bash ~/.claude/skills/deploy-to-vercel/resources/deploy.sh [path]
```
路径可能因用户安装技能的位置而异。

### 沙盒环境（claude.ai）

您可能无法运行`vercel login`或`git push`。直接使用**无认证回退 — claude.ai 沙盒**。

### Codex

Codex在沙盒中运行。首先检查CLI是否可用，然后回退到部署脚本。使用**无认证回退 — Codex 沙盒**。

---

## 输出

始终向用户显示部署URL。

- **Git推送：** 使用`vercel ls --format json`查找预览URL。如果CLI未认证，告诉用户检查Vercel仪表板或提交状态检查。
- **CLI部署：** 显示`vercel deploy --no-wait`返回的URL。使用`vercel inspect <url>`检查构建状态并向用户报告。
- **无认证回退：** 同时显示预览URL和认领URL：
  ```
  部署成功！

  预览URL：https://my-app-abc123.vercel.app
  认领URL：https://vercel.com/claim-deployment?code=...

  在预览URL查看您的站点。
  要将此部署转移到您的Vercel账户，请访问认领URL。
  ```

**不要**通过curl或fetch部署的URL来验证它是否工作。只需返回链接。

---

## 故障排除

### 网络出口错误（claude.ai）

如果由于claude.ai上的网络限制导致部署失败，告诉用户：

```
由于网络限制，部署失败。要解决此问题：

1. 访问 https://claude.ai/settings/capabilities
2. 将 *.vercel.com 添加到允许的域
3. 再次尝试部署
```

### 提升网络访问（Codex / 沙盒环境）

如果在沙盒环境中由于网络问题（超时、DNS错误、连接重置）导致部署失败，使用提升的权限重新运行（`sandbox_permissions=require_escalated`）。不要提升初始CLI可用性检查 — 只提升实际的部署命令。

向用户的示例指导：
```
部署需要提升网络访问权限才能部署到Vercel。我可以使用提升的权限重新运行命令 — 要继续吗？
```

### CLI认证失败

如果`vercel login`或`vercel deploy`因认证错误而失败，回退到无认证部署脚本（claude.ai或Codex变体，取决于环境）。