# Awesome Skills 中文翻译项目

## 项目简介

本项目致力于将优秀的英文 SKILL 翻译成中文，方便中文用户学习和使用。SKILL 是一种模块化的 AI 能力扩展包，可以为支持 SKILL 配置的 AI IDE 提供专业的领域知识、工作流程和工具集成。

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

## 项目结构

```
awesome-skills-cn/
├── README.md                    # 项目说明文档
├── LICENSE                      # MIT 许可证
├── .gitignore                   # Git 忽略文件
├── claude-code-skill-cn/        # claude-code-skill 的中文翻译
│   ├── algorithmic-art/       # 算法艺术生成
│   ├── brand-guidelines/      # 品牌指南
│   ├── canvas-design/        # Canvas 设计
│   ├── doc-coauthoring/      # 文档协作
│   ├── docx/                # Word 文档处理
│   ├── frontend-design/      # 前端设计
│   ├── internal-comms/       # 内部沟通
│   ├── mcp-builder/         # MCP服务器开发指南
│   ├── pdf/                # PDF 处理
│   ├── pptx/               # PowerPoint 处理
│   ├── skill-creator/       # SKILL 创建指南
│   ├── slack-gif-creator/   # Slack GIF 创建器
│   ├── theme-factory/       # 主题工厂
│   ├── web-artifacts-builder/# Web 构建器
│   ├── webapp-testing/      # Web 应用测试
│   └── xlsx/               # Excel 处理
├── vercel-agent-skills-cn/      # vercel-agent-skills 的中文翻译
│   ├── composition-patterns/  # 组合模式
│   ├── react-best-practices/ # React 最佳实践
│   ├── react-native-skills/   # React Native 技能
│   ├── vercel-deploy-claimable/ # Vercel部署工具
│   └── web-design-guidelines/ # Web 设计指南
├── vercel-skills-cn/           # vercel-skills 的中文翻译
│   └── find-skills/         # SKILL 发现工具
└── ui-ux-pro-max-skill-cn/    # ui-ux-pro-max-skill 的中文翻译
└── [原始仓库目录]               # 原始英文仓库（不提交）
```

## 翻译进度

| 来源仓库 | SKILL 数量 | 翻译进度 | 状态 |
|---------|-----------|---------|------|
| claude-code-skill | 16 | 16/16 | 已完成 |
| vercel-agent-skills | 5 | 5/5 | 已完成 |
| vercel-skills | 1 | 1/1 | 已完成 |
| ui-ux-pro-max-skill | 1 | 1/1 | 已完成 |
| **总计** | **23** | **23/23** | **已完成** |

### claude-code-skill (16个)

- [x] algorithmic-art - 算法艺术生成
- [x] brand-guidelines - 品牌指南
- [x] canvas-design - Canvas 设计
- [x] doc-coauthoring - 文档协作
- [x] docx - Word 文档处理
- [x] frontend-design - 前端设计
- [x] internal-comms - 内部沟通
- [x] mcp-builder - MCP服务器开发指南
- [x] pdf - PDF 处理
- [x] pptx - PowerPoint 处理
- [x] skill-creator - SKILL 创建指南
- [x] slack-gif-creator - Slack GIF 创建器
- [x] theme-factory - 主题工厂
- [x] web-artifacts-builder - Web 构建器
- [x] webapp-testing - Web 应用测试
- [x] xlsx - Excel 处理

### vercel-agent-skills (5个)

- [x] react-best-practices - React 最佳实践
- [x] react-native-skills - React Native 技能
- [x] composition-patterns - 组合模式
- [x] vercel-deploy-claimable - Vercel部署工具
- [x] web-design-guidelines - Web 设计指南

### vercel-skills (1个)

- [x] find-skills - SKILL 发现工具

### ui-ux-pro-max-skill (1个)

- [x] ui-ux-pro-max - UI/UX 专业技能

## 如何使用

### 安装 SKILL

1. 确保你的 AI IDE 支持 SKILL 配置
2. 将 SKILL 文件复制到你的 IDE 的 skills 目录，或者直接按照IDE页面提示新增SKILL。
3. 重启 IDE 或重新加载配置

### 使用 SKILL

SKILL 会在特定场景下自动触发，例如：

- 当你提到处理 PDF 文件时，pdf SKILL 会自动加载
- 当你询问 React 最佳实践时，react-best-practices SKILL 会自动加载
- 当你需要创建新的 SKILL 时，skill-creator SKILL 会提供指导

你也可以手动指定使用某个 SKILL，具体方式取决于你使用的 AI IDE。

### 使用示例：find-skills

**find-skills** 是一个帮助你发现和安装其他 SKILL 的工具。当你需要扩展 AI 能力时，可以使用它来搜索生态系统中可用的 SKILL。

**使用场景：**

- 问"如何做X"，其中X可能是已有skill的常见任务
- 说"找一个X的skill"或"有没有一个X的skill"
- 问"你能做X吗"，其中X是专业能力
- 表达对扩展agent能力的兴趣

**使用方法：**

使用 Skills CLI 搜索相关 SKILL：

```bash
npx skills find [query]
```

**示例：**

- 用户问"如何让我的React应用更快？" → `npx skills find react performance`
- 用户问"你能帮我审查PR吗？" → `npx skills find pr review`
- 用户问"我需要创建一个变更日志" → `npx skills find changelog`

**安装 SKILL：**

找到想要的 SKILL 后，使用以下命令安装：

```bash
npx skills add <owner/repo@skill>
```

例如：

```bash
npx skills add vercel-labs/agent-skills@vercel-react-best-practices
```

**常用命令：**

- `npx skills find [query]` - 交互式或按关键词搜索skills
- `npx skills add <package>` - 从GitHub或其他来源安装skill
- `npx skills check` - 检查skill更新
- `npx skills update` - 更新所有已安装的skills

**浏览 SKILL：** https://skills.sh/

## 贡献指南

欢迎参与翻译工作！贡献方式：

1. Fork 本项目
2. 选择一个未翻译的 SKILL
3. 翻译 SKILL.md 文件，保持 YAML frontmatter 中的 name 字段为英文，翻译 description 字段为中文
4. 保持代码示例不变，只翻译说明文字
5. 对于包含 scripts/、references/、assets/ 的 SKILL，翻译其中的文档文件，代码文件保持不变
6. 提交 Pull Request

### 翻译规范

- 保持专业术语的准确性
- 保持代码示例的完整性
- 保持文件名和目录名不变
- 保持 YAML frontmatter 格式正确
- 使用简体中文

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 致谢

感谢以下原始 SKILL 仓库：

- [claude-code-skill](https://github.com/anthropics/claude-code-skill)
- [vercel-agent-skills](https://github.com/vercel-labs/agent-skills)
- [vercel-skills](https://github.com/vercel-labs/skills)
- [ui-ux-pro-max-skill](https://github.com/ComposioHQ/awesome-claude-skills)

## 联系方式

如有问题或建议，欢迎提交 Issue 或 Pull Request。
