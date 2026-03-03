---
name: vercel-deploy
description: 将应用程序和网站部署到 Vercel。当用户请求部署操作时使用，例如"部署我的应用程序"、"部署并给我链接"、"上线"或"创建预览部署"。
---

# Vercel 部署

立即将任何项目部署到 Vercel。**始终部署为预览**（而非生产环境），除非用户明确要求生产环境。

## 前置条件

- 检查是否安装了 Vercel CLI，**不**使用提升权限（例如，`command -v vercel`）。
- 仅当沙盒阻止部署网络调用（`sandbox_permissions=require_escalated`）时，才提升实际部署命令。
- 部署可能需要几分钟。使用适当的超时值。

## 快速开始

1. 检查是否安装了 Vercel CLI（不提升此检查）：

```bash
command -v vercel
```

2. 如果安装了 `vercel`，运行此命令（超时 10 分钟）：
```bash
vercel deploy [path] -y
```

**重要：**为部署命令使用 10 分钟（600000ms）超时，因为构建可能需要一段时间。

3. 如果未安装 `vercel`，或者 CLI 因"No existing credentials found"而失败，请使用下面的回退方法。

## 回退（无身份验证）

如果 CLI 因身份验证错误而失败，请使用部署脚本：

```bash
skill_dir="<path-to-skill>"

# 部署当前目录
bash "$skill_dir/scripts/deploy.sh"

# 部署特定项目
bash "$skill_dir/scripts/deploy.sh" /path/to/project

# 部署现有 tarball
bash "$skill_dir/scripts/deploy.sh" /path/to/project.tgz
```

该脚本处理框架检测、打包和部署。它等待构建完成并返回带有 `previewUrl` 和 `claimUrl` 的 JSON。

**告诉用户：**"您的部署已准备就绪，位于 [previewUrl]。在 [claimUrl] 认领以管理您的部署。"

## 生产部署

仅当用户明确要求时：
```bash
vercel deploy [path] --prod -y
```

## 输出

向用户显示部署 URL。对于回退部署，还显示认领 URL。

**不要** curl 或获取部署的 URL 以验证它是否工作。只需返回链接。

## 故障排除

### 提升网络访问权限

如果部署因网络问题（超时、DNS 错误、连接重置）而失败，请使用提升权限重新运行实际部署命令（使用 `sandbox_permissions=require_escalated`）。不要提升 `command -v vercel` 安装检查。当沙盒网络阻止出站请求时，部署需要提升网络访问权限。

向用户的示例指导：

```
部署需要提升网络访问权限才能部署到 Vercel。我可以使用提升权限重新运行命令——您想让我继续吗？
```
