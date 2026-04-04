# Awesome Skills 中文翻译项目

## 项目简介

本项目致力于将优秀的 SKILL 翻译成中文，方便中文用户学习和使用。

本项目集成了以下 SKILL 项目：

- [**Anthropic Skills**](https://github.com/anthropics/skills) ([中文学习版](anthropics-skills/)) [![GitHub Stars](https://badgen.net/github/stars/anthropics/skills)](https://github.com/anthropics/skills) - Anthropic 官方技能仓库，包含文档处理（DOCX、PDF、PPTX、XLSX）、品牌指南、内部沟通等（17个技能，已全部翻译）
- [**Awesome OpenClaw Skills**](https://github.com/VoltAgent/awesome-openclaw-skills) ([中文学习版](awesome-openclaw-skills/)) [![GitHub Stars](https://badgen.net/github/stars/VoltAgent/awesome-openclaw-skills)](https://github.com/VoltAgent/awesome-openclaw-skills) - OpenClaw 技能集合，涵盖 AI/LLM、浏览器自动化、开发工具、数据分析等领域（5816个技能，已全部翻译）
- [**Antigravity Awesome Skills**](https://github.com/sickn33/antigravity-awesome-skills) ([中文学习版](antigravity-awesome-skills/)) [![GitHub Stars](https://badgen.net/github/stars/sickn33/antigravity-awesome-skills)](https://github.com/sickn33/antigravity-awesome-skills) - 968+ 通用代理技能集合（968个技能）
- [**Claude Scientific Skills**](https://github.com/K-Dense-AI/claude-scientific-skills) ([中文学习版](claude-scientific-skills/)) [![GitHub Stars](https://badgen.net/github/stars/K-Dense-AI/claude-scientific-skills)](https://github.com/K-Dense-AI/claude-scientific-skills) - 科学研究技能集合，涵盖生物信息学、化学、医学、机器学习等领域（179个技能，已全部翻译）
- [**Composio Awesome Claude Skills**](https://github.com/ComposioHQ/awesome-claude-skills) ([中文学习版](composiohq-awesome-claude-skills/)) [![GitHub Stars](https://badgen.net/github/stars/ComposioHQ/awesome-claude-skills)](https://github.com/ComposioHQ/awesome-claude-skills) - Claude 技能集合，包含文档处理、开发工具、数据分析、业务营销等（800+个技能，已全部翻译）
- [**Hugging Face Skills**](https://github.com/huggingface/skills) ([中文学习版](huggingface-skills/)) [![GitHub Stars](https://badgen.net/github/stars/huggingface/skills)](https://github.com/huggingface/skills) - Hugging Face AI/ML 任务技能（11个技能，已全部翻译）
- [**Obsidian Skills**](https://github.com/kepano/obsidian-skills) ([中文学习版](obsidian-skills/)) [![GitHub Stars](https://badgen.net/github/stars/kepano/obsidian-skills)](https://github.com/kepano/obsidian-skills) - Obsidian 笔记应用技能集合，包含 Markdown 编辑、Bases 数据库、JSON Canvas、CLI 交互等（5个技能，已全部翻译）
- [**OpenAI Skills**](https://github.com/openai/skills) ([中文学习版](openai-skills/)) [![GitHub Stars](https://badgen.net/github/stars/openai/skills)](https://github.com/openai/skills) - OpenAI Codex 技能目录（38个技能，已全部翻译）
- [**UI/UX Pro Max Skill**](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) ([中文学习版](ui-ux-pro-max-skill/)) [![GitHub Stars](https://badgen.net/github/stars/nextlevelbuilder/ui-ux-pro-max-skill)](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) - 专业的 UI/UX 设计技能（7个技能，已全部翻译）
- [**Vercel Labs Agent Skills**](https://github.com/vercel-labs/agent-skills) ([中文学习版](vercel-labs-agent-skills/)) [![GitHub Stars](https://badgen.net/github/stars/vercel-labs/agent-skills)](https://github.com/vercel-labs/agent-skills) - Vercel Labs 官方技能仓库，包含 React 最佳实践、Web 设计指南、React Native 技能等（7个技能，6个已翻译）
- [**Vercel Labs Skills**](https://github.com/vercel-labs/skills) ([中文学习版](vercel-labs-skills/)) [![GitHub Stars](https://badgen.net/github/stars/vercel-labs/skills)](https://github.com/vercel-labs/skills) - Vercel Labs 官方技能仓库，包含 Skills CLI 工具（1个技能，已全部翻译）

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
├── anthropics-skills/           # anthropics-skills 项目
│   ├── README_CN.md             # 项目说明文档中文翻译
│   └── skills/
│       ├── algorithmic-art/
│       │   └── SKILL_CN.md    # 算法艺术生成
│       ├── brand-guidelines/
│       │   └── SKILL_CN.md    # 品牌指南
│       ├── canvas-design/
│       │   └── SKILL_CN.md    # Canvas 设计
│       ├── claude-api/
│       │   └── SKILL_CN.md    # Claude API 和 Agent SDK
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
├── antigravity-awesome-skills/  # antigravity-awesome-skills 项目
│   └── skills/               # (共 968 个技能，详见项目目录)
├── awesome-openclaw-skills/  # awesome-openclaw-skills 项目
│   └── categories/               # (共 5816 个技能，详见项目目录)
│   └── categories_cn/            # (5816个你能中文翻译，详见项目目录)
├── claude-scientific-skills/   # claude-scientific-skills 项目
│   └── scientific-skills/     # (共 179 个技能，详见项目目录)
│       ├── adaptyv/
│       │   └── SKILL_CN.md    # Adaptyv 蛋白质设计平台
│       ├── alphafold-database/
│       │   └── SKILL_CN.md    # AlphaFold 蛋白质结构数据库
│       ├── biopython/
│       │   └── SKILL_CN.md    # Biopython 生物信息学工具
│       ├── deepchem/
│       │   └── SKILL_CN.md    # DeepChem 分子机器学习
│       ├── geopandas/
│       │   └── SKILL_CN.md    # GeoPandas 地理空间数据处理
│       ├── neurokit2/
│       │   └── SKILL_CN.md    # NeuroKit2 神经科学数据分析
│       ├── pdb-database/
│       │   └── SKILL_CN.md    # PDB 蛋白质结构数据库
│       ├── pubmed-database/
│       │   └── SKILL_CN.md    # PubMed 医学文献数据库
│       └── ...                # 更多技能（共 179 个，详见项目目录）
├── composiohq-awesome-claude-skills/  # composiohq-awesome-claude-skills 项目
│   ├── artifacts-builder/
│   │   └── SKILL_CN.md    # 工件构建器
│   ├── brand-guidelines/
│   │   └── SKILL_CN.md    # 品牌指南
│   ├── canvas-design/
│   │   └── SKILL_CN.md    # 画布设计
│   ├── changelog-generator/
│   │   └── SKILL_CN.md    # 变更日志生成器
│   ├── competitive-ads-extractor/
│   │   └── SKILL_CN.md    # 竞争广告提取器
│   ├── connect/
│   │   └── SKILL_CN.md    # 连接工具
│   ├── connect-apps/
│   │   └── SKILL_CN.md    # 应用连接
│   ├── content-research-writer/
│   │   └── SKILL_CN.md    # 内容研究与写作
│   ├── developer-growth-analysis/
│   │   └── SKILL_CN.md    # 开发者增长分析
│   ├── document-skills/
│   │   ├── docx/SKILL_CN.md    # Word 文档处理
│   │   ├── pdf/SKILL_CN.md     # PDF 处理
│   │   ├── pptx/SKILL_CN.md    # PowerPoint 处理
│   │   └── xlsx/SKILL_CN.md    # Excel 处理
│   ├── domain-name-brainstormer/
│   │   └── SKILL_CN.md    # 域名创意生成器
│   ├── file-organizer/
│   │   └── SKILL_CN.md    # 文件整理器
│   ├── image-enhancer/
│   │   └── SKILL_CN.md    # 图像增强器
│   ├── internal-comms/
│   │   └── SKILL_CN.md    # 内部沟通
│   ├── invoice-organizer/
│   │   └── SKILL_CN.md    # 发票整理器
│   ├── langsmith-fetch/
│   │   └── SKILL_CN.md    # LangSmith 数据获取
│   ├── lead-research-assistant/
│   │   └── SKILL_CN.md    # 潜在客户研究助手
│   ├── mcp-builder/
│   │   └── SKILL_CN.md    # MCP 构建器
│   ├── meeting-insights-analyzer/
│   │   └── SKILL_CN.md    # 会议洞察分析器
│   ├── raffle-winner-picker/
│   │   └── SKILL_CN.md    # 抽奖获奖者选择器
│   ├── skill-creator/
│   │   └── SKILL_CN.md    # Skill 创建器
│   ├── skill-share/
│   │   └── SKILL_CN.md    # Skill 分享
│   ├── tailored-resume-generator/
│   │   └── SKILL_CN.md    # 定制简历生成器
│   ├── template-skill/
│   │   └── SKILL_CN.md    # Skill 模板
│   ├── theme-factory/
│   │   └── SKILL_CN.md    # 主题工厂
│   ├── twitter-algorithm-optimizer/
│   │   └── SKILL_CN.md    # Twitter 算法优化器
│   ├── video-downloader/
│   │   └── SKILL_CN.md    # 视频下载器
│   ├── webapp-testing/
│   │   └── SKILL_CN.md    # Web 应用测试
│   └── composio-skills/        # 第三方服务自动化集成技能集合 (833个)
│       ├── ably-automation/SKILL_CN.md      # Ably 自动化
│       ├── adobe-automation/SKILL_CN.md     # Adobe 自动化
│       ├── amara-automation/SKILL_CN.md     # Amara 自动化
│       └── ...                # 更多第三方自动化技能 (830个未翻译)
├── huggingface-skills/         # huggingface/skills 项目
│   ├── README_CN.md            # 项目说明文档中文翻译
│   └── skills/
│       ├── hf-cli/
│       │   └── SKILL_CN.md    # Hugging Face Hub CLI
│       ├── huggingface-community-evals/
│       │   └── SKILL_CN.md    # Hugging Face 社区评估
│       ├── huggingface-datasets/
│       │   └── SKILL_CN.md    # 数据集创建和管理
│       ├── huggingface-gradio/
│       │   └── SKILL_CN.md    # Gradio Web UI 构建
│       ├── huggingface-jobs/
│       │   └── SKILL_CN.md    # Hugging Face Jobs 计算任务
│       ├── huggingface-llm-trainer/
│       │   └── SKILL_CN.md    # LLM 模型训练和微调
│       ├── huggingface-paper-publisher/
│       │   └── SKILL_CN.md    # 研究论文发布
│       ├── huggingface-papers/
│       │   └── SKILL_CN.md    # 论文管理
│       ├── huggingface-trackio/
│       │   └── SKILL_CN.md    # ML 实验跟踪
│       ├── huggingface-vision-trainer/
│       │   └── SKILL_CN.md    # 视觉模型训练
│       └── transformers-js/
│           └── SKILL_CN.md    # Transformers.js 机器学习
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
│   └── skills/
│       ├── .curated/
│       │   ├── aspnet-core/
│       │   │   └── SKILL_CN.md    # ASP.NET Core 应用开发
│       │   ├── chatgpt-apps/
│       │   │   └── SKILL_CN.md    # ChatGPT 应用开发
│       │   ├── cloudflare-deploy/
│       │   │   └── SKILL_CN.md    # Cloudflare 部署工具
│       │   ├── develop-web-game/
│       │   │   └── SKILL_CN.md    # Web 游戏开发
│       │   ├── doc/
│       │   │   └── SKILL_CN.md    # DOCX 文档处理
│       │   ├── figma/
│       │   │   └── SKILL_CN.md    # Figma 设计工具
│       │   ├── figma-implement-design/
│       │   │   └── SKILL_CN.md    # Figma 设计实现
│       │   ├── gh-address-comments/
│       │   │   └── SKILL_CN.md    # GitHub 评论处理
│       │   ├── gh-fix-ci/
│       │   │   └── SKILL_CN.md    # GitHub CI 修复
│       │   ├── imagegen/
│       │   │   └── SKILL_CN.md    # 图像生成
│       │   ├── jupyter-notebook/
│       │   │   └── SKILL_CN.md    # Jupyter 笔记本
│       │   ├── linear/
│       │   │   └── SKILL_CN.md    # Linear 项目管理
│       │   ├── netlify-deploy/
│       │   │   └── SKILL_CN.md    # Netlify 部署
│       │   ├── notion-knowledge-capture/
│       │   │   └── SKILL_CN.md    # Notion 知识捕获
│       │   ├── notion-meeting-intelligence/
│       │   │   └── SKILL_CN.md    # Notion 会议智能
│       │   ├── notion-research-documentation/
│       │   │   └── SKILL_CN.md    # Notion 研究文档
│       │   ├── notion-spec-to-implementation/
│       │   │   └── SKILL_CN.md    # Notion 规格到实施
│       │   ├── openai-docs/
│       │   │   └── SKILL_CN.md    # OpenAI 文档查询
│       │   ├── pdf/
│       │   │   └── SKILL_CN.md    # PDF 处理
│       │   ├── playwright/
│       │   │   └── SKILL_CN.md    # Playwright 浏览器自动化
│       │   ├── playwright-interactive/
│       │   │   └── SKILL_CN.md    # Playwright 交互式调试
│       │   ├── render-deploy/
│       │   │   └── SKILL_CN.md    # Render 部署
│       │   ├── screenshot/
│       │   │   └── SKILL_CN.md    # 屏幕截图
│       │   ├── security-best-practices/
│       │   │   └── SKILL_CN.md    # 安全最佳实践
│       │   ├── security-ownership-map/
│       │   │   └── SKILL_CN.md    # 安全所有权映射
│       │   ├── security-threat-model/
│       │   │   └── SKILL_CN.md    # 安全威胁建模
│       │   ├── sentry/
│       │   │   └── SKILL_CN.md    # Sentry 监控
│       │   ├── slides/
│       │   │   └── SKILL_CN.md    # 演示文稿创建
│       │   ├── sora/
│       │   │   └── SKILL_CN.md    # Sora 视频生成
│       │   ├── speech/
│       │   │   └── SKILL_CN.md    # 语音生成
│       │   ├── spreadsheet/
│       │   │   └── SKILL_CN.md    # 电子表格处理
│       │   ├── transcribe/
│       │   │   └── SKILL_CN.md    # 音频转录
│       │   ├── vercel-deploy/
│       │   │   └── SKILL_CN.md    # Vercel 部署
│       │   ├── winui-app/
│       │   │   └── SKILL_CN.md    # WinUI 3 应用开发
│       │   └── yeet/
│       │       └── SKILL_CN.md    # Git 提交流程
│       └── .system/
│           ├── openai-docs/
│           │   └── SKILL_CN.md    # OpenAI 文档查询（系统级）
│           ├── skill-creator/
│           │   └── SKILL_CN.md    # 技能创建器
│           └── skill-installer/
│               └── SKILL_CN.md    # 技能安装器
├── ui-ux-pro-max-skill/        # ui-ux-pro-max-skill 项目
│   ├── README_CN.md            # 项目说明文档中文翻译
│   └── .claude/skills/
│       ├── banner-design/
│       │   └── SKILL_CN.md    # 横幅设计
│       ├── design/
│       │   └── SKILL_CN.md    # 设计
│       ├── design-system/
│       │   └── SKILL_CN.md    # 设计系统
│       ├── slides/
│       │   └── SKILL_CN.md    # 幻灯片
│       ├── ui-styling/
│       │   └── SKILL_CN.md    # UI样式
│       └── ui-ux-pro-max/
│           └── SKILL_CN.md    # UI/UX 专业技能
├── vercel-labs-agent-skills/    # vercel-labs/agent-skills 项目
│   ├── README_CN.md            # 项目说明文档中文翻译
│   └── skills/
│       ├── claude.ai/
│       │   └── vercel-deploy-claimable/
│       │       └── SKILL_CN.md    # Vercel 部署工具
│       ├── composition-patterns/
│       │   └── SKILL_CN.md    # 组合模式
│       ├── deploy-to-vercel/
│       │   └── SKILL_CN.md    # 部署到Vercel
│       ├── react-best-practices/
│       │   └── SKILL_CN.md    # React 最佳实践
│       ├── react-native-skills/
│       │   └── SKILL_CN.md    # React Native 技能
│       └── web-design-guidelines/
│           └── SKILL_CN.md    # Web 设计指南
└── vercel-labs-skills/         # vercel-labs/skills 项目
    ├── README_CN.md            # 项目说明文档中文翻译
    └── skills/find-skills/
        └── SKILL_CN.md        # SKILL 发现工具
```

**翻译方式说明：**
- 中文翻译文件直接在原项目的 SKILL.md 所在目录下新增 SKILL_CN.md
- 项目说明文档的中文翻译为 README_CN.md，与原 README.md 同级
- 原项目保持完整，翻译文件作为补充存在

## 翻译进度

| 来源仓库 | SKILL 数量 | README 翻译 | SKILL 翻译 | 状态 |
|---------|-----------|------------|-----------|------|
| anthropics-skills | 17 | ✓ | 17/17 | 已完成 |
| antigravity-awesome-skills | 968 | - | 0/968 | 未开始 |
| awesome-openclaw-skills | 5816 | ✓ | 5816/5816 | 已完成 |
| claude-scientific-skills | 179 | ✓ | 179/179 | 已完成 |
| composio-skills | 832 | ✓ | 832/832 | 已完成 |
| huggingface-skills | 11 | ✓ | 11/11 | 已完成 |
| obsidian-skills | 5 | ✓ | 5/5 | 已完成 |
| openai-skills | 38 | ✓ | 38/38 | 已完成 |
| ui-ux-pro-max-skill | 7 | ✓ | 7/7 | 已完成 |
| vercel-labs-agent-skills | 7 | ✓ | 7/7 | 已完成 |
| vercel-labs-skills | 1 | ✓ | 1/1 | 已完成 |
| **总计** | **7930** | **75** | **6271/7930** | **已完成** |


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

### antigravity-awesome-skills (968个)

- [ ] 00-andruia-consultant
- [ ] 10-andruia-skill-smith
- [ ] 20-andruia-niche-intelligence
- [ ] 3d-web-experience
- [ ] ab-test-setup
- [ ] ... (共 968 个技能，详见项目目录)

### awesome-openclaw-skills (5816个)

- [x] [README_CN.md](awesome-openclaw-skills/README_CN.md) - 项目说明文档中文翻译
- [x] [ai-and-llms](awesome-openclaw-skills/categories_cn/ai-and-llms.md) (184个技能)
- [x] [apple-apps-and-services](awesome-openclaw-skills/categories_cn/apple-apps-and-services.md) (44个技能)
- [x] [browser-and-automation](awesome-openclaw-skills/categories_cn/browser-and-automation.md) (320个技能)
- [x] [calendar-and-scheduling](awesome-openclaw-skills/categories_cn/calendar-and-scheduling.md) (65个技能)
- [x] [clawdbot-tools](awesome-openclaw-skills/categories_cn/clawdbot-tools.md) (36个技能)
- [x] [cli-utilities](awesome-openclaw-skills/categories_cn/cli-utilities.md) (180个技能)
- [x] [coding-agents-and-ides](awesome-openclaw-skills/categories_cn/coding-agents-and-ides.md) (1200个技能)
- [x] [communication](awesome-openclaw-skills/categories_cn/communication.md) (145个技能)
- [x] [data-and-analytics](awesome-openclaw-skills/categories_cn/data-and-analytics.md) (41个技能)
- [x] [devops-and-cloud](awesome-openclaw-skills/categories_cn/devops-and-cloud.md) (392个技能)
- [x] [gaming](awesome-openclaw-skills/categories_cn/gaming.md) (35个技能)
- [x] [git-and-github](awesome-openclaw-skills/categories_cn/git-and-github.md) (166个技能)
- [x] [health-and-fitness](awesome-openclaw-skills/categories_cn/health-and-fitness.md) (84个技能)
- [x] [image-and-video-generation](awesome-openclaw-skills/categories_cn/image-and-video-generation.md) (169个技能)
- [x] [ios-and-macos-development](awesome-openclaw-skills/categories_cn/ios-and-macos-development.md) (29个技能)
- [x] [marketing-and-sales](awesome-openclaw-skills/categories_cn/marketing-and-sales.md) (103个技能)
- [x] [media-and-streaming](awesome-openclaw-skills/categories_cn/media-and-streaming.md) (84个技能)
- [x] [moltbook](awesome-openclaw-skills/categories_cn/moltbook.md) (44个技能)
- [x] [notes-and-pkm](awesome-openclaw-skills/categories_cn/notes-and-pkm.md) (71个技能)
- [x] [pdf-and-documents](awesome-openclaw-skills/categories_cn/pdf-and-documents.md) (110个技能)
- [x] [personal-development](awesome-openclaw-skills/categories_cn/personal-development.md) (51个技能)
- [x] [productivity-and-tasks](awesome-openclaw-skills/categories_cn/productivity-and-tasks.md) (204个技能)
- [x] [search-and-research](awesome-openclaw-skills/categories_cn/search-and-research.md) (352个技能)
- [x] [security-and-passwords](awesome-openclaw-skills/categories_cn/security-and-passwords.md) (54个技能)
- [x] [self-hosted-and-automation](awesome-openclaw-skills/categories_cn/self-hosted-and-automation.md) (33个技能)
- [x] [shopping-and-e-commerce](awesome-openclaw-skills/categories_cn/shopping-and-e-commerce.md) (51个技能)
- [x] [smart-home-and-iot](awesome-openclaw-skills/categories_cn/smart-home-and-iot.md) (43个技能)
- [x] [speech-and-transcription](awesome-openclaw-skills/categories_cn/speech-and-transcription.md) (45个技能)
- [x] [transportation](awesome-openclaw-skills/categories_cn/transportation.md) (110个技能)
- [x] [web-and-frontend-development](awesome-openclaw-skills/categories_cn/web-and-frontend-development.md) (925个技能)

### claude-scientific-skills (179个)

- [x] [adaptyv](claude-scientific-skills/scientific-skills/adaptyv/SKILL_CN.md) - Adaptyv 蛋白质设计平台
- [x] [alphafold-database](claude-scientific-skills/scientific-skills/alphafold-database/SKILL_CN.md) - AlphaFold 蛋白质结构数据库
- [x] [cbioportal-database](claude-scientific-skills/scientific-skills/cbioportal-database/SKILL_CN.md) - cBioPortal 癌症基因组数据库
- [x] [deepchem](claude-scientific-skills/scientific-skills/deepchem/SKILL_CN.md) - DeepChem 分子机器学习
- [x] [neuropixels-analysis](claude-scientific-skills/scientific-skills/neuropixels-analysis/SKILL_CN.md) - Neuropixels神经记录分析
- ... (共179个技能，详见项目目录)

### composiohq-awesome-claude-skills (800+个)
- [x] [artifacts-builder](composiohq-awesome-claude-skills/artifacts-builder/SKILL_CN.md) - 使用现代前端技术创建复杂 HTML 工件
- [x] [brand-guidelines](composiohq-awesome-claude-skills/brand-guidelines/SKILL_CN.md) - Anthropic 品牌样式指南
- [x] [canvas-design](composiohq-awesome-claude-skills/canvas-design/SKILL_CN.md) - 视觉艺术和设计创作
- [x] ... (共 800+ 个技能，详见项目目录)

### huggingface-skills (11个)

- [x] [hf-cli](huggingface-skills/skills/hf-cli/SKILL_CN.md) - Hugging Face Hub CLI
- [x] [huggingface-community-evals](huggingface-skills/skills/huggingface-community-evals/SKILL_CN.md) - Hugging Face 社区评估
- [x] [huggingface-datasets](huggingface-skills/skills/huggingface-datasets/SKILL_CN.md) - 数据集创建和管理
- [x] [huggingface-gradio](huggingface-skills/skills/huggingface-gradio/SKILL_CN.md) - Gradio Web UI 构建
- [x] [huggingface-jobs](huggingface-skills/skills/huggingface-jobs/SKILL_CN.md) - Hugging Face Jobs 计算任务
- [x] [huggingface-llm-trainer](huggingface-skills/skills/huggingface-llm-trainer/SKILL_CN.md) - LLM 模型训练和微调
- [x] [huggingface-paper-publisher](huggingface-skills/skills/huggingface-paper-publisher/SKILL_CN.md) - 研究论文发布
- [x] [huggingface-papers](huggingface-skills/skills/huggingface-papers/SKILL_CN.md) - 论文管理
- [x] [huggingface-trackio](huggingface-skills/skills/huggingface-trackio/SKILL_CN.md) - ML 实验跟踪
- [x] [huggingface-vision-trainer](huggingface-skills/skills/huggingface-vision-trainer/SKILL_CN.md) - 视觉模型训练
- [x] [transformers-js](huggingface-skills/skills/transformers-js/SKILL_CN.md) - Transformers.js 机器学习

### obsidian-skills (5个)
- [x] [obsidian-markdown](obsidian-skills/skills/obsidian-markdown/SKILL_CN.md) - 创建和编辑 Obsidian Flavored Markdown 文档
- [x] [obsidian-bases](obsidian-skills/skills/obsidian-bases/SKILL_CN.md) - 创建和编辑 Obsidian Bases 数据库
- [x] [json-canvas](obsidian-skills/skills/json-canvas/SKILL_CN.md) - 创建和编辑 JSON Canvas 文件
- [x] [obsidian-cli](obsidian-skills/skills/obsidian-cli/SKILL_CN.md) - 通过 Obsidian CLI 与 Obsidian vault 交互
- [x] [defuddle](obsidian-skills/skills/defuddle/SKILL_CN.md) - 从网页提取干净的 Markdown 内容

### openai-skills (38个)

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

### ui-ux-pro-max-skill (7个)

- [x] [ui-ux-pro-max](ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/SKILL_CN.md) - UI/UX 专业技能
- [x] [banner-design](ui-ux-pro-max-skill/.claude/skills/banner-design/SKILL_CN.md) - 横幅设计
- [x] [design](ui-ux-pro-max-skill/.claude/skills/design/SKILL_CN.md) - 设计
- [x] [design-system](ui-ux-pro-max-skill/.claude/skills/design-system/SKILL_CN.md) - 设计系统
- [x] [slides](ui-ux-pro-max-skill/.claude/skills/slides/SKILL_CN.md) - 幻灯片
- [x] [ui-styling](ui-ux-pro-max-skill/.claude/skills/ui-styling/SKILL_CN.md) - UI样式

### vercel-labs-agent-skills (7个)

- [x] [composition-patterns](vercel-labs-agent-skills/skills/composition-patterns/SKILL_CN.md) - 组合模式
- [x] [deploy-to-vercel](vercel-labs-agent-skills/skills/deploy-to-vercel/SKILL_CN.md) - 部署到Vercel
- [x] [react-best-practices](vercel-labs-agent-skills/skills/react-best-practices/SKILL_CN.md) - React 最佳实践
- [x] [react-native-skills](vercel-labs-agent-skills/skills/react-native-skills/SKILL_CN.md) - React Native 技能
- [x] [vercel-deploy-claimable](vercel-labs-agent-skills/skills/claude.ai/vercel-deploy-claimable/SKILL_CN.md) - Vercel 部署工具
- [x] [web-design-guidelines](vercel-labs-agent-skills/skills/web-design-guidelines/SKILL_CN.md) - Web 设计指南
- [x] [vercel-cli-with-tokens](vercel-labs-agent-skills/skills/vercel-cli-with-tokens/SKILL_CN.md) - Vercel CLI with Tokens

### vercel-labs-skills (1个)

- [x] [find-skills](vercel-labs-skills/skills/find-skills/SKILL_CN.md) - SKILL 发现工具

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 致谢

感谢以下原始 SKILL 仓库：

- [Antigravity Awesome Skills](https://github.com/sickn33/antigravity-awesome-skills) - 968+ 通用代理技能集合
- [Anthropic Skills](https://github.com/anthropics/skills) - Anthropic 官方技能仓库，包含文档处理（DOCX、PDF、PPTX、XLSX）、品牌指南、内部沟通等
- [Awesome OpenClaw Skills](https://github.com/VoltAgent/awesome-openclaw-skills) - OpenClaw 技能集合，涵盖 AI/LLM、浏览器自动化、开发工具、数据分析等领域
- [Claude Scientific Skills](https://github.com/K-Dense-AI/claude-scientific-skills) - 科学研究技能集合，涵盖生物信息学、化学、医学、机器学习等领域
- [Composio Awesome Claude Skills](https://github.com/ComposioHQ/awesome-claude-skills) - Claude 技能集合，包含文档处理、开发工具、数据分析、业务营销等
- [Hugging Face Skills](https://github.com/huggingface/skills) - Hugging Face AI/ML 任务技能
- [Obsidian Skills](https://github.com/kepano/obsidian-skills) - Obsidian 笔记应用技能集合，包含 Markdown 编辑、Bases 数据库、JSON Canvas、CLI 交互等
- [OpenAI Skills](https://github.com/openai/skills) - OpenAI Codex 技能目录
- [UI/UX Pro Max Skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) - 专业的 UI/UX 设计技能
- [Vercel Labs Agent Skills](https://github.com/vercel-labs/agent-skills) - Vercel Labs 官方技能仓库，包含 React 最佳实践、Web 设计指南、React Native 技能等
- [Vercel Labs Skills](https://github.com/vercel-labs/skills) - Vercel Labs 官方技能仓库，包含 Skills CLI 工具

## 联系方式

如有问题或建议，欢迎提交 Issue 或 Pull Request。
