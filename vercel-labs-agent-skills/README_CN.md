# Agent Skills

> 本文档是 [Vercel Labs Agent Skills](https://github.com/vercel-labs/agent-skills) 项目的中文翻译版本。

## 关于本翻译

### 原项目介绍

**Agent Skills** 是一个为 AI 编码智能体设计的技能集合。技能是打包的指令和脚本，用于扩展智能体的能力。

技能遵循 [Agent Skills](https://agentskills.io/) 格式。

### 翻译说明

本翻译将原项目的英文文档翻译成中文，包括：

- **README.md** → **README_CN.md** - 项目说明文档的中文翻译
- **SKILL.md** → **SKILL_CN.md** - 技能文档的中文翻译

翻译保持了原文档的结构和技术术语的准确性，便于中文用户理解和使用。

### 原项目链接

- [GitHub 仓库](https://github.com/vercel-labs/agent-skills)

### 翻译项目

本翻译属于 [awesome-skills-cn](https://github.com/lingxling/awesome-skills-cn) 项目的一部分，致力于将优秀的英文 SKILL 翻译成中文。

---

## 可用的技能

### react-best-practices

来自 Vercel 工程团队的 React 和 Next.js 性能优化指南。包含 8 个类别的 40+ 条规则，按影响程度优先排序。

**使用场景：**
- 编写新的 React 组件或 Next.js 页面
- 实现数据获取（客户端或服务端）
- 审查代码的性能问题
- 优化包大小或加载时间

**涵盖的类别：**
- 消除瀑布流（关键）
- 包大小优化（关键）
- 服务端性能（高）
- 客户端数据获取（中高）
- 重渲染优化（中）
- 渲染性能（中）
- JavaScript 微优化（低中）

### web-design-guidelines

审查 UI 代码是否符合 Web 界面最佳实践。审计您的代码是否符合 100+ 条规则，涵盖可访问性、性能和 UX。

**使用场景：**
- "审查我的 UI"
- "检查可访问性"
- "审计设计"
- "审查 UX"
- "根据最佳实践检查我的站点"

**涵盖的类别：**
- 可访问性（aria-labels、语义化 HTML、键盘处理程序）
- 焦点状态（可见焦点、focus-visible 模式）
- 表单（自动完成、验证、错误处理）
- 动画（prefers-reduced-motion、合成器友好的变换）
- 排版（弯引号、省略号、tabular-nums）
- 图像（尺寸、延迟加载、alt 文本）
- 性能（虚拟化、布局抖动、预连接）
- 导航和状态（URL 反映状态、深度链接）
- 深色模式和主题（color-scheme、theme-color meta）
- 触摸和交互（touch-action、tap-highlight）
- 语言环境和 i18n（Intl.DateTimeFormat、Intl.NumberFormat）

### react-native-guidelines

为 AI 智能体优化的 React Native 最佳实践。包含 7 个部分的 16 条规则，涵盖性能、架构和平台特定模式。

**使用场景：**
- 构建 React Native 或 Expo 应用
- 优化移动性能
- 实现动画或手势
- 使用原生模块或平台 API

**涵盖的类别：**
- 性能（关键）- FlashList、记忆化、繁重计算
- 布局（高）- flex 模式、安全区域、键盘处理
- 动画（高）- Reanimated、手势处理
- 图像（中）- expo-image、缓存、延迟加载
- 状态管理（中）- Zustand 模式、React Compiler
- 架构（中）- monorepo 结构、导入
- 平台（中）- iOS/Android 特定模式

### composition-patterns

可扩展的 React 组合模式。通过复合组件、状态提升和内部组合帮助避免布尔属性泛滥。

**使用场景：**
- 重构具有许多布尔属性的组件
- 构建可重用的组件库
- 设计灵活的 API
- 审查组件架构

**涵盖的模式：**
- 提取复合组件
- 提升状态以减少 props
- 组合内部以获得灵活性
- 避免 props 钻取

### vercel-deploy-claimable

立即将应用程序和网站部署到 Vercel。专为与 claude.ai 和 Claude Desktop 一起使用而设计，可直接从对话中启用部署。部署是"可认领的" - 用户可以将所有权转移到自己的 Vercel 账户。

**使用场景：**
- "部署我的应用"
- "将其部署到生产环境"
- "上线"
- "部署并提供链接"

**功能：**
- 从 `package.json` 自动检测 40+ 个框架
- 返回预览 URL（实时站点）和认领 URL（转移所有权）
- 自动处理静态 HTML 项目
- 上传时排除 `node_modules` 和 `.git`

**工作原理：**
1. 将项目打包成 tarball
2. 检测框架（Next.js、Vite、Astro 等）
3. 上传到部署服务
4. 返回预览 URL 和认领 URL

**输出：**
```
部署成功！

预览 URL：https://skill-deploy-abc123.vercel.app
认领 URL：https://vercel.com/claim-deployment?code=...
```

## 安装

```bash
npx skills add vercel-labs/agent-skills
```

## 使用方法

安装后技能自动可用。当检测到相关任务时，智能体将使用它们。

**示例：**
```
部署我的应用
```
```
审查此 React 组件的性能问题
```
```
帮我优化这个 Next.js 页面
```

## 技能结构

每个技能包含：
- `SKILL.md` - 智能体指令
- `scripts/` - 自动化辅助脚本（可选）
- `references/` - 支持文档（可选）

## 许可证

MIT

---

## 原项目文档

如需查看原项目的英文文档，请访问：

- [README.md (英文原版)](README.md) - 原项目的完整说明文档

原项目由 [Vercel Labs](https://github.com/vercel-labs) 维护。
