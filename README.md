# Awesome Skills 中文翻译项目

## 项目简介

本项目致力于将优秀的英文 SKILL 翻译成中文，方便中文用户学习和使用。SKILL 是一种模块化的 AI 能力扩展包，可以为支持 SKILL 配置的 AI IDE 提供专业的领域知识、工作流程和工具集成。

本翻译项目囊括了以下优秀的 SKILL 项目：

- [**Anthropic Skills**](https://github.com/anthropics/skills) [![GitHub Stars](https://badgen.net/github/stars/anthropics/skills)](https://github.com/anthropics/skills) - Anthropic 官方技能仓库，包含文档处理（DOCX、PDF、PPTX、XLSX）、品牌指南、内部沟通等（17个技能）
- [**UI/UX Pro Max Skill**](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) [![GitHub Stars](https://badgen.net/github/stars/nextlevelbuilder/ui-ux-pro-max-skill)](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) - 专业的 UI/UX 设计技能（1个技能）
- [**Vercel Labs Skills**](https://github.com/vercel-labs/skills) [![GitHub Stars](https://badgen.net/github/stars/vercel-labs/skills)](https://github.com/vercel-labs/skills) - Vercel Labs 官方技能仓库，包含 Skills CLI 工具（1个技能）
- [**Vercel Labs Agent Skills**](https://github.com/vercel-labs/agent-skills) [![GitHub Stars](https://badgen.net/github/stars/vercel-labs/agent-skills)](https://github.com/vercel-labs/agent-skills) - Vercel Labs 官方技能仓库，包含 React 最佳实践、Web 设计指南、React Native 技能等（5个技能）
- [**Antigravity Awesome Skills**](https://github.com/sickn33/antigravity-awesome-skills) [![GitHub Stars](https://badgen.net/github/stars/sickn33/antigravity-awesome-skills)](https://github.com/sickn33/antigravity-awesome-skills) - 968+ 通用代理技能集合（968个技能）
- [**Hugging Face Skills**](https://github.com/huggingface/skills) [![GitHub Stars](https://badgen.net/github/stars/huggingface/skills)](https://github.com/huggingface/skills) - Hugging Face AI/ML 任务技能（10个技能）
- [**OpenAI Skills**](https://github.com/openai/skills) [![GitHub Stars](https://badgen.net/github/stars/openai/skills)](https://github.com/openai/skills) - OpenAI Codex 技能目录（31个技能）
- [**Claude Scientific Skills**](https://github.com/K-Dense-AI/claude-scientific-skills) [![GitHub Stars](https://badgen.net/github/stars/K-Dense-AI/claude-scientific-skills)](https://github.com/K-Dense-AI/claude-scientific-skills) - 科学研究技能集合，涵盖生物信息学、化学、医学、机器学习等领域（170个技能）
- [**Composio Awesome Claude Skills**](https://github.com/ComposioHQ/awesome-claude-skills) [![GitHub Stars](https://badgen.net/github/stars/ComposioHQ/awesome-claude-skills)](https://github.com/ComposioHQ/awesome-claude-skills) - Claude 技能集合，包含文档处理、开发工具、数据分析、业务营销等（200+个技能）
- [**Voltagent Awesome OpenClaw Skills**](https://github.com/voltagent/awesome-openclaw-skills) [![GitHub Stars](https://badgen.net/github/stars/voltagent/awesome-openclaw-skills)](https://github.com/voltagent/awesome-openclaw-skills) - OpenClaw 技能集合，涵盖 AI/LLM、浏览器自动化、开发工具、数据分析等领域（5816个技能）
- [**Obsidian Skills**](https://github.com/kepano/obsidian-skills) [![GitHub Stars](https://badgen.net/github/stars/kepano/obsidian-skills)](https://github.com/kepano/obsidian-skills) - Obsidian 笔记应用技能集合，包含 Markdown 编辑、Bases 数据库、JSON Canvas、CLI 交互等（5个技能）

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
├── anthropics-skills/           # anthrpics-skills 项目
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
├── huggingface-skills/         # huggingface/skills 项目
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
├── obsidian-skills/            # obsidian-skills 项目
│   ├── README_CN.md            # 项目说明文档中文翻译
│   └── skills/
│       ├── defuddle/
│       │   └── SKILL_CN.md    # 从网页提取干净的 Markdown 内容
│       ├── json-canvas/
│       │   └── SKILL_CN.md    # 创建和编辑 JSON Canvas 文件
│       ├── obsidian-bases/
│       │   └── SKILL_CN.md    # 创建和编辑 Obsidian Bases 数据库
│       ├── obsidian-cli/
│       │   └── SKILL_CN.md    # 通过 Obsidian CLI 与 Obsidian vault 交互
│       └── obsidian-markdown/
│           └── SKILL_CN.md    # 创建和编辑 Obsidian Flavored Markdown 文档
├── openai-skills/              # openai/skills 项目
│   ├── README_CN.md            # 项目说明文档中文翻译
│   └── skills/.curated/
│       ├── cloudflare-deploy/
│       │   └── SKILL_CN.md    # Cloudflare 部署工具
│       ├── develop-web-game/
│       │   └── SKILL_CN.md    # Web 游戏开发
│       ├── doc/
│       │   └── SKILL_CN.md    # DOCX 文档处理
│       ├── figma/
│       │   └── SKILL_CN.md    # Figma 设计工具
│       ├── figma-implement-design/
│       │   └── SKILL_CN.md    # Figma 设计实现
│       └── gh-address-comments/
│           └── SKILL_CN.md    # GitHub 评论处理
├── ui-ux-pro-max-skill/        # ui-ux-pro-max-skill 项目
│   ├── README_CN.md            # 项目说明文档中文翻译
│   └── .claude/skills/ui-ux-pro-max/
│       └── SKILL_CN.md        # UI/UX Pro Max 技能
├── vercel-labs-agent-skills/    # vercel-labs/agent-skills 项目
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
├── vercel-labs-skills/         # vercel-labs/skills 项目
│   ├── README_CN.md            # 项目说明文档中文翻译
│   └── skills/find-skills/
│       └── SKILL_CN.md        # SKILL 发现工具
├── antigravity-awesome-skills/  # antigravity-awesome-skills 项目
│   └── skills/               # (共 968 个技能，详见项目目录)
├── claude-scientific-skills/   # claude-scientific-skills 项目
│   └── docs/                 # (共 170 个技能，详见项目目录)
├── composiohq-awesome-claude-skills/  # composiohq-awesome-claude-skills 项目
│   └── connect/              # (共 200+ 个技能，详见项目目录)
└── voltagent-awesome-openclaw-skills/  # voltagent-awesome-openclaw-skills 项目
    └── skills/               # (共 5816 个技能，详见项目目录)
```

**翻译方式说明：**
- 中文翻译文件直接在原项目的 SKILL.md 所在目录下新增 SKILL_CN.md
- 项目说明文档的中文翻译为 README_CN.md，与原 README.md 同级
- 原项目保持完整，翻译文件作为补充存在

## 翻译进度

| 来源仓库 | SKILL 数量 | README 翻译 | SKILL 翻译 | 状态 |
|---------|-----------|------------|-----------|------|
| anthropics-skills | 17 | ✓ | 17/17 | 已完成 |
| ui-ux-pro-max-skill | 7 | ✓ | 1/7 | 进行中 |
| vercel-labs-skills | 1 | ✓ | 1/1 | 已完成 |
| huggingface-skills | 14 | ✓ | 10/14 | 进行中 |
| openai-skills | 37 | ✓ | 37/37 | 已完成 |
| vercel-labs-agent-skills | 6 | ✓ | 5/6 | 进行中 |
| obsidian-skills | 5 | ✗ | 5/5 | 进行中 |
| antigravity-awesome-skills | 968 | - | 0/968 | 未开始 |
| claude-scientific-skills | 175 | - | 46/175 | 进行中 |
| composiohq-awesome-claude-skills | 200+ | - | 0/200+ | 未开始 |
| voltagent-awesome-openclaw-skills | 5816 | - | 0/5816 | 未开始 |
| **总计** | **7229+** | **75** | **122/7229+** | **进行中** |

### anthropics-skills (17个)

- [x] [algorithmic-art](anthropics-skills/skills/algorithmic-art/SKILL_CN.md) - 算法艺术生成
- [x] [brand-guidelines](anthropics-skills/skills/brand-guidelines/SKILL_CN.md) - 品牌指南
- [x] [canvas-design](anthropics-skills/skills/canvas-design/SKILL_CN.md) - Canvas 设计
- [x] [claude-api](anthropics-skills/skills/claude-api/SKILL_CN.md) - Claude API 和 Agent SDK
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

### huggingface-skills (10个)

- [x] [huggingface-gradio](huggingface-skills/skills/huggingface-gradio/SKILL_CN.md) - Gradio Web UI 构建
- [x] [hugging-face-cli](huggingface-skills/skills/hugging-face-cli/SKILL_CN.md) - Hugging Face CLI 操作
- [x] [hugging-face-datasets](huggingface-skills/skills/hugging-face-datasets/SKILL_CN.md) - 数据集创建和管理
- [x] [hugging-face-dataset-viewer](huggingface-skills/skills/hugging-face-dataset-viewer/SKILL_CN.md) - 数据集查看器 API 工作流
- [x] [hugging-face-evaluation](huggingface-skills/skills/hugging-face-evaluation/SKILL_CN.md) - 模型评估管理
- [x] [hugging-face-jobs](huggingface-skills/skills/hugging-face-jobs/SKILL_CN.md) - Hugging Face Jobs 计算任务
- [x] [hugging-face-model-trainer](huggingface-skills/skills/hugging-face-model-trainer/SKILL_CN.md) - 模型训练和微调
- [x] [hugging-face-paper-publisher](huggingface-skills/skills/hugging-face-paper-publisher/SKILL_CN.md) - 研究论文发布
- [x] [hugging-face-tool-builder](huggingface-skills/skills/hugging-face-tool-builder/SKILL_CN.md) - API 工具构建
- [x] [hugging-face-trackio](huggingface-skills/skills/hugging-face-trackio/SKILL_CN.md) - ML 实验跟踪

### openai-skills (37个)

- [x] [skill-installer](openai-skills/skills/.system/skill-installer/SKILL_CN.md) - 技能安装器
- [x] [skill-creator](openai-skills/skills/.system/skill-creator/SKILL_CN.md) - 技能创建器
- [x] [openai-docs](openai-skills/skills/.system/openai-docs/SKILL_CN.md) - OpenAI 文档查询（系统级）
- [x] [aspnet-core](openai-skills/skills/.curated/aspnet-core/SKILL_CN.md) - ASP.NET Core 应用开发
- [x] [chatgpt-apps](openai-skills/skills/.curated/chatgpt-apps/SKILL_CN.md) - ChatGPT 应用开发
- [x] [cloudflare-deploy](openai-skills/skills/.curated/cloudflare-deploy/SKILL_CN.md) - Cloudflare 部署工具
- [x] [develop-web-game](openai-skills/skills/.curated/develop-web-game/SKILL_CN.md) - Web 游戏开发
- [x] [doc](openai-skills/skills/.curated/doc/SKILL_CN.md) - DOCX 文档处理
- [x] [figma](openai-skills/skills/.curated/figma/SKILL_CN.md) - Figma 设计工具
- [x] [figma-implement-design](openai-skills/skills/.curated/figma-implement-design/SKILL_CN.md) - Figma 设计实现
- [x] [gh-address-comments](openai-skills/skills/.curated/gh-address-comments/SKILL_CN.md) - GitHub 评论处理
- [x] [gh-fix-ci](openai-skills/skills/.curated/gh-fix-ci/SKILL_CN.md) - GitHub CI 修复
- [x] [imagegen](openai-skills/skills/.curated/imagegen/SKILL_CN.md) - 图像生成
- [x] [jupyter-notebook](openai-skills/skills/.curated/jupyter-notebook/SKILL_CN.md) - Jupyter 笔记本
- [x] [linear](openai-skills/skills/.curated/linear/SKILL_CN.md) - Linear 项目管理
- [x] [netlify-deploy](openai-skills/skills/.curated/netlify-deploy/SKILL_CN.md) - Netlify 部署
- [x] [notion-knowledge-capture](openai-skills/skills/.curated/notion-knowledge-capture/SKILL_CN.md) - Notion 知识捕获
- [x] [notion-meeting-intelligence](openai-skills/skills/.curated/notion-meeting-intelligence/SKILL_CN.md) - Notion 会议智能
- [x] [notion-research-documentation](openai-skills/skills/.curated/notion-research-documentation/SKILL_CN.md) - Notion 研究文档
- [x] [notion-spec-to-implementation](openai-skills/skills/.curated/notion-spec-to-implementation/SKILL_CN.md) - Notion 规格到实施
- [x] [openai-docs](openai-skills/skills/.curated/openai-docs/SKILL_CN.md) - OpenAI 文档查询
- [x] [pdf](openai-skills/skills/.curated/pdf/SKILL_CN.md) - PDF 处理
- [x] [playwright](openai-skills/skills/.curated/playwright/SKILL_CN.md) - Playwright 浏览器自动化
- [x] [playwright-interactive](openai-skills/skills/.curated/playwright-interactive/SKILL_CN.md) - Playwright 交互式调试
- [x] [render-deploy](openai-skills/skills/.curated/render-deploy/SKILL_CN.md) - Render 部署
- [x] [screenshot](openai-skills/skills/.curated/screenshot/SKILL_CN.md) - 屏幕截图
- [x] [security-best-practices](openai-skills/skills/.curated/security-best-practices/SKILL_CN.md) - 安全最佳实践
- [x] [security-ownership-map](openai-skills/skills/.curated/security-ownership-map/SKILL_CN.md) - 安全所有权映射
- [x] [security-threat-model](openai-skills/skills/.curated/security-threat-model/SKILL_CN.md) - 安全威胁建模
- [x] [sentry](openai-skills/skills/.curated/sentry/SKILL_CN.md) - Sentry 监控
- [x] [slides](openai-skills/skills/.curated/slides/SKILL_CN.md) - 演示文稿创建
- [x] [sora](openai-skills/skills/.curated/sora/SKILL_CN.md) - Sora 视频生成
- [x] [speech](openai-skills/skills/.curated/speech/SKILL_CN.md) - 语音生成
- [x] [spreadsheet](openai-skills/skills/.curated/spreadsheet/SKILL_CN.md) - 电子表格处理
- [x] [transcribe](openai-skills/skills/.curated/transcribe/SKILL_CN.md) - 音频转录
- [x] [vercel-deploy](openai-skills/skills/.curated/vercel-deploy/SKILL_CN.md) - Vercel 部署
- [x] [winui-app](openai-skills/skills/.curated/winui-app/SKILL_CN.md) - WinUI 3 应用开发
- [x] [yeet](openai-skills/skills/.curated/yeet/SKILL_CN.md) - Git 提交流程

### obsidian-skills (5个)

- [x] [obsidian-markdown](obsidian-skills/skills/obsidian-markdown/SKILL_CN.md) - 创建和编辑 Obsidian Flavored Markdown 文档
- [x] [obsidian-bases](obsidian-skills/skills/obsidian-bases/SKILL_CN.md) - 创建和编辑 Obsidian Bases 数据库
- [x] [json-canvas](obsidian-skills/skills/json-canvas/SKILL_CN.md) - 创建和编辑 JSON Canvas 文件
- [x] [obsidian-cli](obsidian-skills/skills/obsidian-cli/SKILL_CN.md) - 通过 Obsidian CLI 与 Obsidian vault 交互
- [x] [defuddle](obsidian-skills/skills/defuddle/SKILL_CN.md) - 从网页提取干净的 Markdown 内容

### claude-scientific-skills (175个)

- [x] [adaptyv](claude-scientific-skills/scientific-skills/adaptyv/SKILL_CN.md) - Adaptyv 蛋白质设计平台
- [x] [alphafold-database](claude-scientific-skills/scientific-skills/alphafold-database/SKILL_CN.md) - AlphaFold 蛋白质结构数据库
- [x] [cbioportal-database](claude-scientific-skills/scientific-skills/cbioportal-database/SKILL_CN.md) - cBioPortal 癌症基因组数据库
- [x] [deepchem](claude-scientific-skills/scientific-skills/deepchem/SKILL_CN.md) - DeepChem 分子机器学习
- [x] [document-skills/docx](claude-scientific-skills/scientific-skills/document-skills/docx/SKILL_CN.md) - DOCX 文档处理（document-skills）
- [x] [neuropixels-analysis](claude-scientific-skills/scientific-skills/neuropixels-analysis/SKILL_CN.md) - Neuropixels神经记录分析
- [x] [neurokit2](claude-scientific-skills/scientific-skills/neurokit2/SKILL_CN.md) - 生理信号处理工具包
- [x] [networkx](claude-scientific-skills/scientific-skills/networkx/SKILL_CN.md) - 复杂网络和图分析工具包
- ... (更多已翻译技能详见项目目录)

- [ ] fda-database
- [ ] matplotlib
- [ ] networkx
- [ ] pandas
- [ ] plotly
- ... (更多未翻译技能详见项目目录)

### composiohq-awesome-claude-skills (200+个)

- [ ] active-campaign-automation
- [ ] adobe-automation
- [ ] ... (共 200+ 个技能，详见项目目录)

### voltagent-awesome-openclaw-skills (5816个)

- [ ] ai-and-llms (196个技能)
- [ ] browser-and-automation (335个技能)
- [ ] coding-agents-and-ides (1222个技能)
- [ ] ... (共 5816 个技能，详见项目目录)

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
- [Claude Scientific Skills](https://github.com/K-Dense-AI/claude-scientific-skills) - 科学研究技能集合，涵盖生物信息学、化学、医学、机器学习等领域
- [Composio Awesome Claude Skills](https://github.com/ComposioHQ/awesome-claude-skills) - Claude 技能集合，包含文档处理、开发工具、数据分析、业务营销等
- [Voltagent Awesome OpenClaw Skills](https://github.com/voltagent/awesome-openclaw-skills) - OpenClaw 技能集合，涵盖 AI/LLM、浏览器自动化、开发工具、数据分析等领域
- [Obsidian Skills](https://github.com/kepano/obsidian-skills) - Obsidian 笔记应用技能集合，包含 Markdown 编辑、Bases 数据库、JSON Canvas、CLI 交互等

## 联系方式

如有问题或建议，欢迎提交 Issue 或 Pull Request。
