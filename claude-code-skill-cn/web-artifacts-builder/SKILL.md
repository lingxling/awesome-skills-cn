---
name: web-artifacts-builder
description: 使用现代前端Web技术（React、Tailwind CSS、shadcn/ui）创建复杂、多组件claude.ai HTML工件的工具套件。用于需要状态管理、路由或shadcn/ui组件的复杂工件——不用于简单的单文件HTML/JSX工件。
license: 完整条款见LICENSE.txt
---

# Web 工件构建器

要构建强大的前端claude.ai工件，请按照以下步骤操作：
1. 使用`scripts/init-artifact.sh`初始化前端仓库
2. 通过编辑生成的代码开发工件
3. 使用`scripts/bundle-artifact.sh`将所有代码打包到单个HTML文件中
4. 向用户显示工件
5. （可选）测试工件

**技术栈**：React 18 + TypeScript + Vite + Parcel（打包） + Tailwind CSS + shadcn/ui

## 设计和样式指南

非常重要：为了避免通常被称为"AI垃圾"的东西，避免使用过度的居中布局、紫色渐变、统一的圆角和Inter字体。

## 快速开始

### 步骤1：初始化项目

运行初始化脚本以创建新的React项目：
```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

这将创建一个完全配置的项目，具有：
- ✅ React + TypeScript（通过Vite）
- ✅ Tailwind CSS 3.4.1，带有shadcn/ui主题系统
- ✅ 路径别名（`@/`）已配置
- ✅ 40+个shadcn/ui组件预安装
- ✅ 包含所有Radix UI依赖项
- ✅ Parcel配置用于打包（通过.parcelrc）
- ✅ Node 18+兼容性（自动检测并固定Vite版本）

### 步骤2：开发工件

要构建工件，编辑生成的文件。有关指导，请参阅下面的**常见开发任务**。

### 步骤3：打包到单个HTML文件

要将React应用打包到单个HTML工件：
```bash
bash scripts/bundle-artifact.sh
```

这将创建`bundle.html` - 一个自包含的工件，所有JavaScript、CSS和依赖项都内联。此文件可以在Claude对话中直接作为工件共享。

**要求**：您的项目必须在根目录中有一个`index.html`。

**脚本的作用**：
- 安装打包依赖项（parcel、@parcel/config-default、parcel-resolver-tspaths、html-inline）
- 创建支持路径别名的`.parcelrc`配置
- 使用Parcel构建（无源映射）
- 使用html-inline将所有资产内联到单个HTML中

### 步骤4：与用户共享工件

最后，在对话中与用户共享打包的HTML文件，以便他们可以将其作为工件查看。

### 步骤5：测试/可视化工件（可选）

注意：这是一个完全可选的步骤。仅在必要时或请求时执行。

要测试/可视化工件，使用可用工具（包括其他技能或内置工具，如Playwright或Puppeteer）。通常，避免预先测试工件，因为它会在请求和可以看到完成的工件之间增加延迟。如果请求或出现问题，请在展示工件后进行测试。

## 参考

- **shadcn/ui组件**：https://ui.shadcn.com/docs/components
