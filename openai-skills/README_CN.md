# Agent Skills

> 本文档是 [OpenAI Skills](https://github.com/openai/skills) 项目的中文翻译版本。

## 关于本翻译

### 原项目介绍

**Agent Skills** 是指令、脚本和资源的文件夹，AI 智能体可以发现并使用它们来执行特定任务。一次编写，到处使用。

Codex 使用技能来帮助打包功能，团队和个人可以用可重复的方式完成特定任务。此仓库为 Codex 的使用和分发提供技能目录。

了解更多：
- [在 Codex 中使用技能](https://developers.openai.com/codex/skills)
- [在 Codex 中创建自定义技能](https://developers.openai.com/codex/skills/create-skill)
- [Agent Skills 开放标准](https://agentskills.io)

## 安装技能

[`.system`](skills/.system/) 中的技能会自动安装到最新版本的 Codex 中。

要安装 [精选](skills/.curated/) 或 [实验](skills/.experimental/) 技能，您可以在 Codex 中使用 `$skill-installer`。

精选技能可以按名称安装（默认为 `skills/.curated`）：

```
$skill-installer gh-address-comments
```

对于实验技能，指定技能文件夹。例如：

```
$skill-installer install the create-plan skill from the .experimental folder
```

或者提供 GitHub 目录 URL：

```
$skill-installer install https://github.com/openai/skills/tree/main/skills/.experimental/create-plan
```

安装技能后，重启 Codex 以获取新技能。

## 许可证

单个技能的许可可以在技能目录内的 `LICENSE.txt` 文件中直接找到。

### 翻译说明

本翻译将原项目的英文文档翻译成中文，包括：

- **README.md** → **README_CN.md** - 项目说明文档的中文翻译
- **SKILL.md** → **SKILL_CN.md** - 技能文档的中文翻译

翻译保持了原文档的结构和技术术语的准确性，便于中文用户理解和使用。

### 原项目链接

- [GitHub 仓库](https://github.com/openai/skills)

### 翻译项目

本翻译属于 [awesome-skills-cn](https://github.com/lingxling/awesome-skills-cn) 项目的一部分，致力于将优秀的英文 SKILL 翻译成中文。

---

## 主要技能翻译

本翻译项目包含以下所有技能的中文翻译：

### .system 技能
- [SKILL_CN.md](skills/.system/skill-installer/SKILL_CN.md) - 技能安装器
- [SKILL_CN.md](skills/.system/skill-creator/SKILL_CN.md) - 技能创建器

### 部署相关技能
- [SKILL_CN.md](skills/.curated/vercel-deploy/SKILL_CN.md) - Vercel 部署
- [SKILL_CN.md](skills/.curated/netlify-deploy/SKILL_CN.md) - Netlify 部署
- [SKILL_CN.md](skills/.curated/render-deploy/SKILL_CN.md) - Render 部署

### 开发和测试
- [SKILL_CN.md](skills/.curated/develop-web-game/SKILL_CN.md) - Web 游戏开发
- [SKILL_CN.md](skills/.curated/playwright/SKILL_CN.md) - Playwright 浏览器自动化

### 文档处理
- [SKILL_CN.md](skills/.curated/pdf/SKILL_CN.md) - PDF 处理
- [SKILL_CN.md](skills/.curated/spreadsheet/SKILL_CN.md) - 电子表格处理
- [SKILL_CN.md](skills/.curated/jupyter-notebook/SKILL_CN.md) - Jupyter 笔记本

### 媒体和图像
- [SKILL_CN.md](skills/.curated/screenshot/SKILL_CN.md) - 屏幕截图
- [SKILL_CN.md](skills/.curated/imagegen/SKILL_CN.md) - 图像生成
- [SKILL_CN.md](skills/.curated/transcribe/SKILL_CN.md) - 音频转录
- [SKILL_CN.md](skills/.curated/speech/SKILL_CN.md) - 语音生成
- [SKILL_CN.md](skills/.curated/sora/SKILL_CN.md) - Sora 视频生成

### 工具和集成
- [SKILL_CN.md](skills/.curated/gh-fix-ci/SKILL_CN.md) - GitHub CI 修复
- [SKILL_CN.md](skills/.curated/openai-docs/SKILL_CN.md) - OpenAI 文档查询
- [SKILL_CN.md](skills/.curated/linear/SKILL_CN.md) - Linear 项目管理
- [SKILL_CN.md](skills/.curated/sentry/SKILL_CN.md) - Sentry 监控

### 安全相关
- [SKILL_CN.md](skills/.curated/security-best-practices/SKILL_CN.md) - 安全最佳实践
- [SKILL_CN.md](skills/.curated/security-threat-model/SKILL_CN.md) - 安全威胁建模
- [SKILL_CN.md](skills/.curated/security-ownership-map/SKILL_CN.md) - 安全所有权映射

### Notion 相关
- [SKILL_CN.md](skills/.curated/notion-knowledge-capture/SKILL_CN.md) - Notion 知识捕获
- [SKILL_CN.md](skills/.curated/notion-meeting-intelligence/SKILL_CN.md) - Notion 会议智能
- [SKILL_CN.md](skills/.curated/notion-research-documentation/SKILL_CN.md) - Notion 研究文档
- [SKILL_CN.md](skills/.curated/notion-spec-to-implementation/SKILL_CN.md) - Notion 规格到实施

### 其他
- [SKILL_CN.md](skills/.curated/yeet/SKILL_CN.md) - Git 提交流程

## 注意事项

本翻译项目已完成 openai-skills 所有 31 个技能的中文翻译。

---

## 原项目文档

如需查看原项目的英文文档，请访问：

- [README.md (英文原版)](README.md) - 原项目的完整说明文档

原项目由 [OpenAI](https://github.com/openai) 维护。
