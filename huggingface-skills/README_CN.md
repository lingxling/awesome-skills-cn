# Hugging Face Skills 中文翻译

> 本文档是 [Hugging Face Skills](https://github.com/huggingface/skills) 项目的中文翻译版本。

## 关于本翻译

### 原项目介绍

**Hugging Face Skills** 是 Hugging Face 为 AI/ML 任务(如数据集创建、模型训练和评估)提供的技能定义。它们与所有主要的编码代理工具兼容,包括 OpenAI Codex、Anthropic 的 Claude Code、Google DeepMind 的 Gemini CLI 和 Cursor。

此仓库中的技能遵循标准化的 [Agent Skills](https://agentskills.io/home) 格式。

每个技能都是自包含的文件夹,将指令、脚本和资源打包在一起,供 AI 代理在特定用例中使用。每个文件夹包含一个 `SKILL.md` 文件,其中包含 YAML 前置数据(名称和描述),后跟随着技能激活时您的编码代理遵循的指导。

### 翻译说明

本翻译项目致力于将 Hugging Face Skills 项目的文档和技能翻译成中文,使其更易于中文用户理解和使用。

### 原项目链接

- [GitHub 仓库](https://github.com/huggingface/skills)
- [Agent Skills 规范](https://agentskills.io/home)

### 翻译项目

本翻译属于 [awesome-skills-cn](https://github.com/lingxling/awesome-skills-cn) 项目的一部分,致力于将优秀的英文 SKILL 翻译成中文。

---

> **注意:** 本仓库包含 Hugging Face 为 AI/ML 任务提供的技能定义。有关 Agent Skills 标准的信息,请参阅 [agentskills.io](https://agentskills.io/home)。

# Hugging Face Skills

Hugging Face Skills 是 AI/ML 任务(如数据集创建、模型训练和评估)的定义。它们与所有主要的编码代理工具兼容,包括 OpenAI Codex、Anthropic 的 Claude Code、Google DeepMind 的 Gemini CLI 和 Cursor。

此仓库中的技能遵循标准化的 [Agent Skills](https://agentskills.io/home) 格式。

## Skills 如何工作?

在实践中,技能是自包含的文件夹,将指令、脚本和资源打包在一起,供 AI 代理在特定用例中使用。每个文件夹包含一个 `SKILL.md` 文件,其中包含 YAML 前置数据(名称和描述),后跟随着技能激活时您的编码代理遵循的指导。

> [!NOTE]
> 'Skills' 实际上是 Anthropic 在 Claude AI 和 Claude Code 中使用的术语,并未被其他代理工具采用,但我们很喜欢它! OpenAI Codex 使用开放的 [Agent Skills](https://agentskills.io/specification) 格式,其中每个技能是一个包含 `SKILL.md` 文件的目录,Codex 从 [Codex Skills 指南](https://developers.openai.com/codex/skills/) 中记录的标准 `.agents/skills` 位置发现该文件。Codex 也可以使用 `AGENTS.md` 文件。Google Gemini 使用 'extensions' 在 `gemini-extension.json` 文件中为您的编码代理定义指令。**此仓库与所有这些都兼容,甚至更多!**

> [!TIP]
> 如果您的代理不支持技能,您可以直接使用 [`agents/AGENTS.md`](agents/AGENTS.md) 作为备用。

## 安装

Hugging Face 技能与 Claude Code、Codex、Gemini CLI 和 Cursor 兼容。

### Claude Code

1. 将仓库注册为插件市场:  

```
/plugin marketplace add huggingface/skills
```

2. 要安装技能,请运行:  

```
/plugin install <skill-name>@huggingface/skills
```

例如:  

```
/plugin install hf-cli@huggingface/skills
```

### Codex

1. 将您要使用的任何技能从此仓库的 `skills/` 目录复制或符号链接到 Codex 的标准 `.agents/skills` 位置之一(例如,`$REPO_ROOT/.agents/skills` 或 `$HOME/.agents/skills`),如 [Codex Skills 指南](https://developers.openai.com/codex/skills/) 中所述。

2. 一旦技能在这些位置之一可用,Codex 将使用 Agent Skills 标准发现它,并在它决定使用该技能或当您显式调用它时加载 `SKILL.md` 指令。

3. 如果您的 Codex 设置仍然依赖 `AGENTS.md`,您可以使用此仓库中生成的 [`agents/AGENTS.md`](agents/AGENTS.md) 文件作为指令的备用包。

### Gemini CLI

1. 此仓库包含 `gemini-extension.json` 以与 Gemini CLI 集成。

2. 本地安装:  

```
gemini extensions install . --consent
```

或使用 GitHub URL:
```
gemini extensions install https://github.com/huggingface/skills.git --consent
```

4. 有关更多帮助,请参阅 [Gemini CLI 扩展文档](https://geminicli.com/docs/extensions/#installing-an-extension)。

### Cursor

此仓库包含 Cursor 插件清单:
- `.cursor-plugin/plugin.json`
- `.mcp.json`(配置了 Hugging Face MCP 服务器 URL)

通过 Cursor 插件流程从仓库 URL(或本地签出)安装。

对于贡献者,使用以下命令重新生成清单:
```bash
./scripts/publish.sh
```

## Skills

此仓库包含一些技能以帮助您入门。您也可以将自己的技能贡献到仓库。

### 可用技能

<!-- 此表由 scripts/generate_agents.py 自动生成。请勿手动编辑。 -->
<!-- BEGIN_SKILLS_TABLE -->
| 名称 | 描述 | 文档 |
|------|-------------|---------------|
| `hf-cli` | 使用 hf CLI 执行 Hugging Face Hub 操作。下载模型/数据集、上传文件、管理存储库以及运行云计算作业。 | [SKILL.md](skills/hf-cli/SKILL.md) |
| `huggingface-community-evals` | 在 Hugging Face 模型卡片中添加和管理评估结果。支持从 README 内容中提取评估表、从 Artificial Analysis API 导入分数,以及使用 vLLM/lighteval 运行自定义评估。 | [SKILL.md](skills/huggingface-community-evals/SKILL.md) |
| `huggingface-datasets` | 使用 Dataset Viewer REST API 和 npx 工具探索、查询和提取任何 Hugging Face 数据集。零 Python 依赖项 — 涵盖拆分/配置发现、行分页、文本搜索、过滤、通过 parquetlens 进行 SQL 操作,以及通过 CLI 进行数据集上传。 | [SKILL.md](skills/huggingface-datasets/SKILL.md) |
| `huggingface-gradio` | 使用 Python 构建 Gradio Web UI 和演示。在创建或编辑 Gradio 应用、组件、事件监听器、布局或聊天机器人时使用。 | [SKILL.md](skills/huggingface-gradio/SKILL.md) |
| `huggingface-jobs` | 在 Hugging Face 基础设施上运行计算作业。执行 Python 脚本、管理计划作业以及监控作业状态。 | [SKILL.md](skills/huggingface-jobs/SKILL.md) |
| `huggingface-llm-trainer` | 使用 TRL 在 Hugging Face Jobs 基础设施上训练或微调语言模型。涵盖 SFT、DPO、GRPO 和奖励建模训练方法,以及用于本地部署的 GGUF 转换。包括硬件选择、成本估算、Trackio 监控和 Hub 持久化。 | [SKILL.md](skills/huggingface-llm-trainer/SKILL.md) |
| `huggingface-paper-publisher` | 在 Hugging Face Hub 上发布和管理研究论文。支持创建论文页面、将论文链接到模型/数据集、声明作者身份以及生成专业的基于 markdown 的研究文章。 | [SKILL.md](skills/huggingface-paper-publisher/SKILL.md) |
| `huggingface-papers` | 以 markdown 格式查找和阅读 Hugging Face 论文页面,并在需要时使用论文 API 获取结构化元数据,如作者、链接的模型、数据集、Spaces 和媒体 URL。 | [SKILL.md](skills/huggingface-papers/SKILL.md) |
| `huggingface-tool-builder` | 为 Hugging Face Hub 和 API 工作流构建可重用脚本。适用于链接 API 调用、丰富 Hub 元数据或自动化重复任务。 | [SKILL.md](skills/huggingface-tool-builder/SKILL.md) |
| `huggingface-trackio` | 使用 Trackio 跟踪和可视化 ML 训练实验。通过 Python API 记录指标并通过 CLI 检索它们。支持与 HF Spaces 同步的实时仪表板。 | [SKILL.md](skills/huggingface-trackio/SKILL.md) |
| `huggingface-vision-trainer` | 使用 Transformers Trainer API 在 Hugging Face Jobs 基础设施或本地训练和微调目标检测模型(RTDETRv2、YOLOS、DETR 等)和图像分类模型(timm 和 transformers 模型 — MobileNetV3、MobileViT、ResNet、ViT/DINOv3)。包括 COCO 数据集格式支持、Albumentations 增强、mAP/mAR 指标、trackio 跟踪、硬件选择和 Hub 持久化。 | [SKILL.md](skills/huggingface-vision-trainer/SKILL.md) |
| `transformers-js` | 直接在 JavaScript/TypeScript 中运行最先进的机器学习模型,用于 NLP、计算机视觉、音频处理和多模态任务。使用 Hugging Face 模型在 Node.js 和带有 WebGPU/WASM 的浏览器中工作。 | [SKILL.md](skills/transformers-js/SKILL.md) |
<!-- END_SKILLS_TABLE -->

### 在编码代理中使用技能

安装技能后,在给编码代理指令时直接提及它:
- "使用 HF LLM trainer 技能来估计 70B 模型运行所需的 GPU 内存。"
- "使用 HF model evaluation 技能在最新检查点上启动 `run_eval_job.py`。"
- "使用 HF dataset creator 技能来起草新的少样本分类模板。"
- "使用 HF paper publisher 技能来索引我的 arXiv 论文并将其链接到我的模型。"

您的编码代理在完成任务时自动加载相应的 `SKILL.md` 指令和辅助脚本。

### 贡献或自定义技能

1. 复制现有的技能文件夹之一(例如,`hf-datasets/`)并重命名它。
2. 更新新文件夹的 `SKILL.md` 前置数据:
   ```markdown
   ---
   name: my-skill-name
   description: 描述技能的作用以及何时使用它
   ---

   # Skill Title
   指导 + 示例 + 保护措施
   ```
3. 添加或编辑您的指令引用的支持脚本、模板和文档。
4. 在 `.claude-plugin/marketplace.json` 中添加一个条目,并带有简洁的、人类可读的描述。
5. 运行:
   ```bash
   ./scripts/publish.sh
   ```
   以重新生成并验证所有生成的元数据。
6. 在您的编码代理中重新安装或重新加载技能包,以便更新的文件夹可用。

### Marketplace

`.claude-plugin/marketplace.json` 文件列出了技能,并带有插件市场的人类可读描述。CI 验证技能名称和路径在 `SKILL.md` 文件和 `marketplace.json` 之间是否匹配,但描述是单独维护的:`SKILL.md` 描述指导 Claude 何时激活技能,而市场描述是为浏览可用技能的人类编写的。

### 其他参考

- 直接在 [huggingface/skills](https://github.com/huggingface/skills) 浏览最新的指令、脚本和模板。
- 查看您在每个技能中引用的特定库或工作流程的 Hugging Face 文档。

---

## 原项目文档

如需查看原项目的完整英文文档,请访问:

- [README.md (英文原版)](README.md) - 原项目的完整说明文档

原项目由 [Hugging Face](https://github.com/huggingface) 维护。