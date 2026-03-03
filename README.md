# Awesome Skills 中文翻译项目

## 项目简介

本项目致力于将优秀的英文 SKILL 翻译成中文，方便中文用户学习和使用。SKILL 是一种模块化的 AI 能力扩展包，可以为支持 SKILL 配置的 AI IDE 提供专业的领域知识、工作流程和工具集成。

本翻译项目囊括了以下优秀的 SKILL 项目：

- [**Anthropic Skills**](https://github.com/anthropics/skills) - Anthropic 官方技能仓库，包含文档处理（DOCX、PDF、PPTX、XLSX）、品牌指南、内部沟通等（16个技能）
- [**UI/UX Pro Max Skill**](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) - 专业的 UI/UX 设计技能（1个技能）
- [**Vercel Labs Skills**](https://github.com/vercel-labs/skills) - Vercel Labs 官方技能仓库，包含 Skills CLI 工具（1个技能）
- [**Vercel Labs Agent Skills**](https://github.com/vercel-labs/agent-skills) - Vercel Labs 官方技能仓库，包含 React 最佳实践、Web 设计指南、React Native 技能等（5个技能）
- [**Antigravity Awesome Skills**](https://github.com/sickn33/antigravity-awesome-skills) - 968+ 通用代理技能集合（968个技能）
- [**Hugging Face Skills**](https://github.com/huggingface/skills) - Hugging Face AI/ML 任务技能（9个技能）
- [**OpenAI Skills**](https://github.com/openai/skills) - OpenAI Codex 技能目录（30个技能）

## SKILL 是什么

SKILL 是一种模块化、自包含的扩展包，通过提供专业的领域知识、工作流程和工具来增强 AI 的能力。你可以将它们视为特定领域或任务的"入职指南"——它们将通用 AI 助手转变为具备程序化知识的专业助手。

### SKILL 提供什么

1. **专业工作流程** - 针对特定领域的多步骤程序
2. **工具集成** - 处理特定文件格式或 API 的说明
3. **领域专业知识** - 公司特定的知识、架构、业务逻辑
4. **捆绑资源** - 脚本、参考资料和资产，用于复杂和重复性任务

### SKILL 的结构

每个 SKILL 由必需的 SKILL.md 文件和可选的捆绑资源组成：

```
skill-name/
├── SKILL.md (必需)
│   ├── YAML frontmatter 元数据 (必需)
│   │   ├── name: (必需)
│   │   ├── description: (必需)
│   │   └── license: (可选)
│   └── Markdown 说明 (必需)
└── 捆绑资源 (可选)
    ├── scripts/          - 可执行代码 (Python/Bash等)
    ├── references/       - 需要时加载到上下文的文档
    └── assets/           - 输出中使用的文件 (模板、图标、字体等)
```

SKILL.md示例
```Markdown
---
name: frontend-design
description: ...
---

skill details.
```

## 项目结构

```
awesome-skills-cn/
├── README.md                    # 项目说明文档
├── LICENSE                      # MIT 许可证
├── CHANGELOG.md                 # 更新日志
├── .gitignore                   # Git 忽略文件
├── anthropics-skills/           # claude-code-skills 原项目
│   ├── README_CN.md            # 项目说明文档中文翻译
│   └── skills/
│       ├── algorithmic-art/
│       │   └── SKILL_CN.md    # 算法艺术生成
│       ├── brand-guidelines/
│       │   └── SKILL_CN.md    # 品牌指南
│       ├── canvas-design/
│       │   └── SKILL_CN.md    # Canvas 设计
│       ├── doc-coauthoring/
│       │   └── SKILL_CN.md    # 文档协作
│       ├── docx/
│       │   └── SKILL_CN.md    # Word 文档处理
│       ├── frontend-design/
│       │   └── SKILL_CN.md    # 前端设计
│       ├── internal-comms/
│       │   └── SKILL_CN.md    # 内部沟通
│       ├── mcp-builder/
│       │   └── SKILL_CN.md    # MCP 服务器开发指南
│       ├── pdf/
│       │   └── SKILL_CN.md    # PDF 处理
│       ├── pptx/
│       │   └── SKILL_CN.md    # PowerPoint 处理
│       ├── skill-creator/
│       │   └── SKILL_CN.md    # SKILL 创建指南
│       ├── slack-gif-creator/
│       │   └── SKILL_CN.md    # Slack GIF 创建器
│       ├── theme-factory/
│       │   └── SKILL_CN.md    # 主题工厂
│       ├── web-artifacts-builder/
│       │   └── SKILL_CN.md    # Web 构建器
│       ├── webapp-testing/
│       │   └── SKILL_CN.md    # Web 应用测试
│       └── xlsx/
│           └── SKILL_CN.md    # Excel 处理
├── ui-ux-pro-max-skill/        # ui-ux-pro-max-skill 原项目
│   ├── README_CN.md            # 项目说明文档中文翻译
│   └── .claude/skills/ui-ux-pro-max/
│       └── SKILL_CN.md        # UI/UX Pro Max 技能
├── vercel-labs-skills/         # vercel-labs/skills 原项目
│   ├── README_CN.md            # 项目说明文档中文翻译
│   └── skills/find-skills/
│       └── SKILL_CN.md        # SKILL 发现工具
├── vercel-labs-agent-skills/    # vercel-labs/agent-skills 原项目
│   ├── README_CN.md            # 项目说明文档中文翻译
│   └── skills/
│       ├── composition-patterns/
│       │   └── SKILL_CN.md    # 组合模式
│       ├── react-best-practices/
│       │   └── SKILL_CN.md    # React 最佳实践
│       ├── react-native-skills/
│       │   └── SKILL_CN.md    # React Native 技能
│       ├── claude.ai/vercel-deploy-claimable/
│       │   └── SKILL_CN.md    # Vercel 部署工具
│       └── web-design-guidelines/
│           └── SKILL_CN.md    # Web 设计指南
├── huggingface-skills/         # huggingface/skills 原项目
│   ├── README_CN.md            # 项目说明文档中文翻译
│   └── skills/
│       ├── huggingface-gradio/
│       │   └── SKILL_CN.md    # Gradio Web UI 构建
│       ├── hugging-face-cli/
│       │   └── SKILL_CN.md    # Hugging Face CLI 操作
│       ├── hugging-face-datasets/
│       │   └── SKILL_CN.md    # 数据集创建和管理
│       ├── hugging-face-evaluation/
│       │   └── SKILL_CN.md    # 模型评估管理
│       ├── hugging-face-jobs/
│       │   └── SKILL_CN.md    # Hugging Face Jobs 计算任务
│       ├── hugging-face-model-trainer/
│       │   └── SKILL_CN.md    # 模型训练和微调
│       ├── hugging-face-paper-publisher/
│       │   └── SKILL_CN.md    # 研究论文发布
│       ├── hugging-face-tool-builder/
│       │   └── SKILL_CN.md    # API 工具构建
│       └── hugging-face-trackio/
│           └── SKILL_CN.md    # ML 实验跟踪
...
```

**翻译方式说明：**
- 中文翻译文件直接在原项目的 SKILL.md 所在目录下新增 SKILL_CN.md
- 项目说明文档的中文翻译为 README_CN.md，与原 README.md 同级
- 原项目保持完整，翻译文件作为补充存在

## 翻译进度

| 来源仓库 | SKILL 数量 | README 翻译 | SKILL 翻译 | 状态 |
|---------|-----------|------------|-----------|------|
| anthropics-skills | 16 | ✓ | 16/16 | 已完成 |
| ui-ux-pro-max-skill | 1 | ✓ | 1/1 | 已完成 |
| vercel-labs-skills | 1 | ✓ | 1/1 | 已完成 |
| huggingface-skills | 9 | ✓ | 9/9 | 已完成 |
| vercel-labs-agent-skills | 5 | ✓ | 5/5 | 已完成 |
| antigravity-awesome-skills | 968 | - | 0/968 | 未开始 |
| openai-skills | 30 | - | 0/30 | 未开始 |
| **总计** | **1030** | **5** | **32/1030** | **进行中** |

### anthropics-skills (16个)

- [x] [algorithmic-art](anthropics-skills/skills/algorithmic-art/SKILL_CN.md) - 算法艺术生成
- [x] [brand-guidelines](anthropics-skills/skills/brand-guidelines/SKILL_CN.md) - 品牌指南
- [x] [canvas-design](anthropics-skills/skills/canvas-design/SKILL_CN.md) - Canvas 设计
- [x] [doc-coauthoring](anthropics-skills/skills/doc-coauthoring/SKILL_CN.md) - 文档协作
- [x] [docx](anthropics-skills/skills/docx/SKILL_CN.md) - Word 文档处理
- [x] [frontend-design](anthropics-skills/skills/frontend-design/SKILL_CN.md) - 前端设计
- [x] [internal-comms](anthropics-skills/skills/internal-comms/SKILL_CN.md) - 内部沟通
- [x] [mcp-builder](anthropics-skills/skills/mcp-builder/SKILL_CN.md) - MCP 服务器开发指南
- [x] [pdf](anthropics-skills/skills/pdf/SKILL_CN.md) - PDF 处理
- [x] [pptx](anthropics-skills/skills/pptx/SKILL_CN.md) - PowerPoint 处理
- [x] [skill-creator](anthropics-skills/skills/skill-creator/SKILL_CN.md) - SKILL 创建指南
- [x] [slack-gif-creator](anthropics-skills/skills/slack-gif-creator/SKILL_CN.md) - Slack GIF 创建器
- [x] [theme-factory](anthropics-skills/skills/theme-factory/SKILL_CN.md) - 主题工厂
- [x] [web-artifacts-builder](anthropics-skills/skills/web-artifacts-builder/SKILL_CN.md) - Web 构建器
- [x] [webapp-testing](anthropics-skills/skills/webapp-testing/SKILL_CN.md) - Web 应用测试
- [x] [xlsx](anthropics-skills/skills/xlsx/SKILL_CN.md) - Excel 处理

### ui-ux-pro-max-skill (1个)

- [x] [ui-ux-pro-max](ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/SKILL_CN.md) - UI/UX 专业技能

### vercel-labs-skills (1个)

- [x] [find-skills](vercel-labs-skills/skills/find-skills/SKILL_CN.md) - SKILL 发现工具

### vercel-labs-agent-skills (5个)

- [x] [composition-patterns](vercel-labs-agent-skills/skills/composition-patterns/SKILL_CN.md) - 组合模式
- [x] [react-best-practices](vercel-labs-agent-skills/skills/react-best-practices/SKILL_CN.md) - React 最佳实践
- [x] [react-native-skills](vercel-labs-agent-skills/skills/react-native-skills/SKILL_CN.md) - React Native 技能
- [x] [vercel-deploy-claimable](vercel-labs-agent-skills/skills/claude.ai/vercel-deploy-claimable/SKILL_CN.md) - Vercel 部署工具
- [x] [web-design-guidelines](vercel-labs-agent-skills/skills/web-design-guidelines/SKILL_CN.md) - Web 设计指南

### antigravity-awesome-skills (968个)

- [ ] 00-andruia-consultant
- [ ] 10-andruia-skill-smith
- [ ] 20-andruia-niche-intelligence
- [ ] 3d-web-experience
- [ ] ab-test-setup
- [ ] ... (共 968 个技能，详见项目目录)

### huggingface-skills (9个)

- [x] [huggingface-gradio](huggingface-skills/skills/huggingface-gradio/SKILL_CN.md) - Gradio Web UI 构建
- [x] [hugging-face-cli](huggingface-skills/skills/hugging-face-cli/SKILL_CN.md) - Hugging Face CLI 操作
- [x] [hugging-face-datasets](huggingface-skills/skills/hugging-face-datasets/SKILL_CN.md) - 数据集创建和管理
- [x] [hugging-face-evaluation](huggingface-skills/skills/hugging-face-evaluation/SKILL_CN.md) - 模型评估管理
- [x] [hugging-face-jobs](huggingface-skills/skills/hugging-face-jobs/SKILL_CN.md) - Hugging Face Jobs 计算任务
- [x] [hugging-face-model-trainer](huggingface-skills/skills/hugging-face-model-trainer/SKILL_CN.md) - 模型训练和微调
- [x] [hugging-face-paper-publisher](huggingface-skills/skills/hugging-face-paper-publisher/SKILL_CN.md) - 研究论文发布
- [x] [hugging-face-tool-builder](huggingface-skills/skills/hugging-face-tool-builder/SKILL_CN.md) - API 工具构建
- [x] [hugging-face-trackio](huggingface-skills/skills/hugging-face-trackio/SKILL_CN.md) - ML 实验跟踪

### openai-skills (30个)

- [ ] cloudflare-deploy
- [ ] develop-web-game
- [ ] doc
- [ ] figma
- [ ] figma-implement-design
- [ ] gh-address-comments
- [ ] gh-fix-ci
- [ ] imagegen
- [ ] jupyter-notebook
- [ ] linear
- [ ] netlify-deploy
- [ ] notion-knowledge-capture
- [ ] notion-meeting-intelligence
- [ ] notion-research-documentation
- [ ] notion-spec-to-implementation
- [ ] openai-docs
- [ ] pdf
- [ ] playwright
- [ ] render-deploy
- [ ] screenshot
- [ ] security-best-practices
- [ ] security-ownership-map
- [ ] security-threat-model
- [ ] sentry
- [ ] sora
- [ ] speech
- [ ] spreadsheet
- [ ] transcribe
- [ ] vercel-deploy
- [ ] yeet


## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 致谢

感谢以下原始 SKILL 仓库：

- [Anthropic Skills](https://github.com/anthropics/skills) - Anthropic 官方技能仓库，包含文档处理（DOCX、PDF、PPTX、XLSX）、品牌指南、内部沟通等
- [UI/UX Pro Max Skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) - 专业的 UI/UX 设计技能
- [Vercel Labs Skills](https://github.com/vercel-labs/skills) - Vercel Labs 官方技能仓库，包含 Skills CLI 工具
- [Vercel Labs Agent Skills](https://github.com/vercel-labs/agent-skills) - Vercel Labs 官方技能仓库，包含 React 最佳实践、Web 设计指南、React Native 技能等
- [Antigravity Awesome Skills](https://github.com/sickn33/antigravity-awesome-skills) - 968+ 通用代理技能集合
- [Hugging Face Skills](https://github.com/huggingface/skills) - Hugging Face AI/ML 任务技能
- [OpenAI Skills](https://github.com/openai/skills) - OpenAI Codex 技能目录

## 联系方式

如有问题或建议，欢迎提交 Issue 或 Pull Request。
