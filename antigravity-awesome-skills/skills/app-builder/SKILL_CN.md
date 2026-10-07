---
name: app-builder
description: "主应用构建编排器。从自然语言请求创建全栈应用。确定项目类型、选择技术栈、协调代理。"
risk: critical
source: community
date_added: "2026-02-27"
---

# App Builder - 应用构建编排器

> 分析用户请求、确定技术栈、规划结构并协调代理。

## 🎯 选择性阅读规则

**仅读取与请求相关的文件！** 检查内容地图，找到你需要的内容。

| 文件 | 说明 | 何时阅读 |
|------|-------------|--------------|
| `project-detection.md` | 关键词矩阵、项目类型检测 | 开始新项目 |
| `tech-stack.md` | 2025 年默认栈、替代方案 | 选择技术 |
| `agent-coordination.md` | 代理管道、执行顺序 | 协调多代理工作 |
| `scaffolding.md` | 目录结构、核心文件 | 创建项目结构 |
| `feature-building.md` | 特性分析、错误处理 | 向现有项目添加特性 |
| `templates/SKILL.md` | **项目模板** | 为新项目搭建脚手架 |

---

## 📦 模板（13 个）

新项目的快速启动脚手架。**仅读取匹配的模板！**

| 模板 | 技术栈 | 何时使用 |
|----------|------------|-------------|
| [nextjs-fullstack](templates/nextjs-fullstack/TEMPLATE.md) | Next.js + Prisma | 全栈 Web 应用 |
| [nextjs-saas](templates/nextjs-saas/TEMPLATE.md) | Next.js + Stripe | SaaS 产品 |
| [nextjs-static](templates/nextjs-static/TEMPLATE.md) | Next.js + Framer | 落地页 |
| [nuxt-app](templates/nuxt-app/TEMPLATE.md) | Nuxt 3 + Pinia | Vue 全栈应用 |
| [express-api](templates/express-api/TEMPLATE.md) | Express + JWT | REST API |
| [python-fastapi](templates/python-fastapi/TEMPLATE.md) | FastAPI | Python API |
| [react-native-app](templates/react-native-app/TEMPLATE.md) | Expo + Zustand | 移动应用 |
| [flutter-app](templates/flutter-app/TEMPLATE.md) | Flutter + Riverpod | 跨平台移动应用 |
| [electron-desktop](templates/electron-desktop/TEMPLATE.md) | Electron + React | 桌面应用 |
| [chrome-extension](templates/chrome-extension/TEMPLATE.md) | Chrome MV3 | 浏览器扩展 |
| [cli-tool](templates/cli-tool/TEMPLATE.md) | Node.js + Commander | CLI 应用 |
| [monorepo-turborepo](templates/monorepo-turborepo/TEMPLATE.md) | Turborepo + pnpm | 单体仓库 |

---

## 🔗 相关代理

| 代理 | 角色 |
|-------|------|
| `project-planner` | 任务分解、依赖关系图 |
| `frontend-specialist` | UI 组件、页面 |
| `backend-specialist` | API、业务逻辑 |
| `database-architect` | 架构、迁移 |
| `devops-engineer` | 部署、预览 |

---

## 使用示例

```
用户："制作一个 Instagram 克隆，带有照片分享和点赞功能"

App Builder 流程：
1. 项目类型：社交媒体应用
2. 技术栈：Next.js + Prisma + Cloudinary + Clerk
3. 创建计划：
   ├─ 数据库架构（用户、帖子、点赞、关注）
   ├─ API 路由（12 个端点）
   ├─ 页面（动态源、个人资料、上传）
   └─ 组件（PostCard、Feed、LikeButton）
4. 协调代理
5. 报告进度
6. 启动预览
```

## 何时使用

此技能适用于执行概述中描述的工作流或操作。

## 限制

- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
