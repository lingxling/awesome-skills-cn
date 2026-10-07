---
name: templates
description: "用于新应用的项目脚手架模板。创建新项目时使用。包含 12 个用于各种技术栈的模板。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 项目模板

> 用于搭建新项目脚手架的快速启动模板。

---

## 🎯 选择性阅读规则

**仅读取与用户项目类型匹配的模板！**

| 模板 | 技术栈 | 何时使用 |
|----------|------------|-------------|
| [nextjs-fullstack](nextjs-fullstack/TEMPLATE.md) | Next.js + Prisma | 全栈 Web 应用 |
| [nextjs-saas](nextjs-saas/TEMPLATE.md) | Next.js + Stripe | SaaS 产品 |
| [nextjs-static](nextjs-static/TEMPLATE.md) | Next.js + Framer | 落地页 |
| [express-api](express-api/TEMPLATE.md) | Express + JWT | REST API |
| [python-fastapi](python-fastapi/TEMPLATE.md) | FastAPI | Python API |
| [react-native-app](react-native-app/TEMPLATE.md) | Expo + Zustand | 移动应用 |
| [flutter-app](flutter-app/TEMPLATE.md) | Flutter + Riverpod | 跨平台应用 |
| [electron-desktop](electron-desktop/TEMPLATE.md) | Electron + React | 桌面应用 |
| [chrome-extension](chrome-extension/TEMPLATE.md) | Chrome MV3 | 浏览器扩展 |
| [cli-tool](cli-tool/TEMPLATE.md) | Node.js + Commander | CLI 应用 |
| [monorepo-turborepo](monorepo-turborepo/TEMPLATE.md) | Turborepo + pnpm | 单体仓库 |
| [astro-static](astro-static/TEMPLATE.md) | Astro + MDX | 博客 / 文档 |

---

## 使用方法

1. 用户说"创建 [类型] 应用"
2. 匹配到相应的模板
3. 仅读取该模板的 TEMPLATE.md
4. 按照其技术栈和结构

## 何时使用

此技能适用于执行概述中描述的工作流或操作。

## 限制

- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
