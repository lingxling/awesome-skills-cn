---
name: netlify-deploy
description: 使用 Netlify CLI（`npx netlify`）将 Web 项目部署到 Netlify。当用户要求在 Netlify 上部署、托管、发布或链接站点/仓库时使用，包括预览和生产部署。
---

# Netlify 部署技能

使用 Netlify CLI 将 Web 项目部署到 Netlify，具有智能的项目配置和部署上下文检测。

## 概述

此技能通过以下方式自动化 Netlify 部署：
- 验证 Netlify CLI 身份验证
- 检测项目配置和框架
- 链接到现有站点或创建新站点
- 部署到生产或预览环境

## 前置条件

- **Netlify CLI**：通过 npx 安装（不需要全局安装）
- **身份验证**：具有活动登录会话的 Netlify 帐户
- **项目**：当前目录中的有效 Web 项目
- 当沙盒阻止部署网络调用时，使用 `sandbox_permissions=require_escalated` 重新运行。
- 部署可能需要几分钟。使用适当的超时值。

## 身份验证模式

该技能使用**预身份验证的 Netlify CLI**方法：

1. 使用 `npx netlify status` 检查身份验证状态
2. 如果未通过身份验证，引导用户完成 `npx netlify login`
3. 如果无法建立身份验证，则优雅地失败

身份验证使用以下任一方式：
- **基于浏览器的 OAuth**（主要）：`netlify login` 打开浏览器进行身份验证
- **API 密钥**（替代）：设置 `NETLIFY_AUTH_TOKEN` 环境变量

## 工作流程

### 1. 验证 Netlify CLI 身份验证

检查用户是否登录到 Netlify：

```bash
npx netlify status
```

**预期输出模式：**
- ✅ 已通过身份验证：显示已登录的用户电子邮件和站点链接状态
- ❌ 未通过身份验证："Not logged into any site"或身份验证错误

**如果未通过身份验证**，引导用户：

```bash
npx netlify login
```

这将打开浏览器窗口进行 OAuth 身份验证。等待用户完成登录，然后再次使用 `netlify status` 验证。

**替代：API 密钥身份验证**

如果浏览器身份验证不可用，用户可以设置：

```bash
export NETLIFY_AUTH_TOKEN=your_token_here
```

可以在以下位置生成令牌：https://app.netlify.com/user/applications#personal-access-tokens

### 2. 检测站点链接状态

从 `netlify status` 输出，确定：
- **已链接**：站点已连接到 Netlify（显示站点名称/URL）
- **未链接**：需要链接或创建站点

### 3. 链接到现有站点或创建新站点

**如果已链接** → 跳到步骤 4

**如果未链接**，尝试通过 Git 远程链接：

```bash
# 检查项目是否基于 Git
git remote show origin

# 如果基于 Git，提取远程 URL
# 格式：https://github.com/username/repo 或 git@github.com:username/repo.git

# 尝试通过 Git 远程链接
npx netlify link --git-remote-url <REMOTE_URL>
```

**如果链接失败**（Netlify 上不存在站点）：

```bash
# 以交互方式创建新站点
npx netlify init
```

这将引导用户完成：
1. 选择团队/帐户
2. 设置站点名称
3. 配置构建设置
4. 如需要，创建 netlify.toml

### 4. 验证依赖项

部署之前，确保项目依赖项已安装：

```bash
# 对于 npm 项目
npm install

# 对于其他包管理器，检测并使用适当的命令
# yarn install, pnpm install 等
```

### 5. 部署到 Netlify

根据上下文选择部署类型：

**预览/草稿部署**（现有站点的默认）：

```bash
npx netlify deploy
```

这将创建一个带有用于测试的唯一 URL 的部署预览。

**生产部署**（用于新站点或明确的生产部署）：

```bash
npx netlify deploy --prod
```

这将部署到实时生产 URL。

**部署过程**：
1. CLI 检测构建设置（从 netlify.toml 或提示用户）
2. 在本地构建项目
3. 将构建的资产上传到 Netlify
4. 返回部署 URL

### 6. 报告结果

部署后，向用户报告：
- **部署 URL**：此部署的唯一 URL
- **站点 URL**：生产 URL（如果是生产部署）
- **部署日志**：Netlify 仪表板中日志的链接
- **后续步骤**：建议 `netlify open` 查看站点或仪表板

## 处理 netlify.toml

如果存在 `netlify.toml` 文件，CLI 将自动使用它。如果不存在，CLI 将提示输入：
- **构建命令**：例如，`npm run build`、`next build`
- **发布目录**：例如，`dist`、`build`、`.next`

常见框架默认值：
- **Next.js**：构建命令 `npm run build`，发布 `.next`
- **React (Vite)**：构建命令 `npm run build`，发布 `dist`
- **静态 HTML**：无构建命令，发布当前目录

该技能应尽可能从 `package.json` 检测框架并建议适当的设置。

## 完整工作流程示例

```bash
# 1. 检查身份验证
npx netlify status

# 如果未通过身份验证：
npx netlify login

# 2. 链接站点（如果需要）
# 首先尝试基于 Git 的链接
git remote show origin
npx netlify link --git-remote-url https://github.com/user/repo

# 如果不存在站点，创建新站点：
npx netlify init

# 3. 安装依赖项
npm install

# 4. 部署（用于测试的预览）
npx netlify deploy

# 5. 部署到生产（当准备好时）
npx netlify deploy --prod
```

## 错误处理

常见问题和解决方案：

**"Not logged in"**
→ 运行 `npx netlify login`

**"No site linked"**
→ 运行 `npx netlify link` 或 `npx netlify init`

**"Build failed"**
→ 检查 netlify.toml 或 CLI 提示中的构建命令和发布目录
→ 验证依赖项已安装
→ 查看构建日志以查找特定错误

**"Publish directory not found"**
→ 验证构建命令成功运行
→ 检查发布目录路径是否正确

## 故障排除

### 提升网络访问权限

如果部署因网络问题（超时、DNS 错误、连接重置）而失败，请使用提升权限重新运行部署（使用 `sandbox_permissions=require_escalated`）。当沙盒网络阻止出站请求时，部署需要提升网络访问权限。

向用户的示例指导：

```
部署需要提升网络访问权限才能部署到 Netlify。我可以使用提升权限重新运行命令——您想让我继续吗？
```

## 环境变量

对于机密和配置：

1. 永远不要将机密提交到 Git
2. 在 Netlify 仪表板中设置：站点设置 → 环境变量
3. 通过 `process.env.VARIABLE_NAME` 在构建中访问

## 提示

- 使用 `netlify deploy`（无 `--prod`）首先在生产之前进行测试
- 运行 `netlify open` 在 Netlify 仪表板中查看站点
- 运行 `netlify logs` 查看函数日志（如果使用 Netlify Functions）
- 使用 `netlify dev` 进行带有 Netlify Functions 的本地开发

## 参考

- Netlify CLI 文档：https://docs.netlify.com/cli/get-started/
- netlify.toml 参考：https://docs.netlify.com/configure-builds/file-based-configuration/

## 捆绑参考资料（根据需要加载）

- [CLI 命令](references/cli-commands.md)
- [部署模式](references/deployment-patterns.md)
- [netlify.toml 指南](references/netlify-toml.md)
