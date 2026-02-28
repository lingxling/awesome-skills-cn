---
name: vercel-deploy
description: 将应用程序和网站部署到Vercel。当用户请求部署操作时使用此技能，例如"部署我的应用"、"部署到生产环境"、"创建预览部署"、"部署并给我链接"或"上线这个"。无需身份验证 - 返回预览URL和可声明的部署链接。
metadata:
  author: vercel
  version: "1.0.0"
---

# Vercel部署

将任何项目立即部署到Vercel。无需身份验证。

## 工作原理

1. 将您的项目打包成tarball（排除`node_modules`和`.git`）
2. 从`package.json`自动检测框架
3. 上传到部署服务
4. 返回**预览URL**（实时站点）和**声明URL**（转移到您的Vercel账户）

## 使用

```bash
bash /mnt/skills/user/vercel-deploy/scripts/deploy.sh [path]
```

**参数：**
- `path` - 要部署的目录，或`.tgz`文件（默认为当前目录）

**示例：**

```bash
# 部署当前目录
bash /mnt/skills/user/vercel-deploy/scripts/deploy.sh

# 部署特定项目
bash /mnt/skills/user/vercel-deploy/scripts/deploy.sh /path/to/project

# 部署现有tarball
bash /mnt/skills/user/vercel-deploy/scripts/deploy.sh /path/to/project.tgz
```

## 输出

```
准备部署...
检测到的框架：nextjs
创建部署包...
部署中...
✅ 部署成功！

预览URL： https://skill-deploy-abc123.vercel.app
声明URL：   https://vercel.com/claim-deployment?code=...
```

脚本还会输出JSON到stdout以供程序使用：

```json
{
  "previewUrl": "https://skill-deploy-abc123.vercel.app",
  "claimUrl": "https://vercel.com/claim-deployment?code=...",
  "deploymentId": "dpl_...",
  "projectId": "prj_..."
}
```

## 框架检测

脚本从`package.json`自动检测框架。支持的框架包括：

- **React：** Next.js、Gatsby、Create React App、Remix、React Router
- **Vue：** Nuxt、Vitepress、Vuepress、SvelteKit、Sapper
- **Svelte：** SvelteKit、Svelte、Sapper
- **其他前端：** Astro、Solid Start、Angular、Ember、Preact、Docusaurus
- **后端：** Express、Hono、Fastify、NestJS、Elysia、h3、Nitro
- **构建工具：** Vite、Parcel
- **以及更多：** Blitz、Hydrogen、RedwoodJS、Storybook、Sanity等

对于静态HTML项目（没有`package.json`），框架设置为`null`。

## 静态HTML项目

对于没有`package.json`的项目：
- 如果有一个`.html`文件未命名为`index.html`，它会自动重命名
- 这确保页面在根URL（`/`）提供服务

## 向用户展示结果

始终显示两个URL：

```
✅ 部署成功！

预览URL： https://skill-deploy-abc123.vercel.app
声明URL：   https://vercel.com/claim-deployment?code=...

在预览URL查看您的站点。
要将此部署转移到您的Vercel账户，请访问声明URL。
```

## 故障排除

### 网络限制错误

如果部署由于网络限制（在claude.ai上常见）而失败，请告诉用户：

```
部署由于网络限制而失败。要解决此问题：

1. 访问 https://claude.ai/settings/capabilities
2. 将 *.vercel.com 添加到允许的域名
3. 再次尝试部署
```
