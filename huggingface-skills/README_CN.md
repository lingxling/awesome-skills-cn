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

Hugging Face Skills 是 AI/ML 任务(如数据集创建、模型训练和评估)的定义。客户端插件市场将 `hf-cli` 技能作为核心 Hub 操作的引导入口暴露出来；其他工作流技能可以通过 `hf skills add <skill-name>` 按需安装，或由支持技能的客户端通过 CLI/MCP 集成发现。

此仓库中的技能遵循标准化的 [Agent Skills](https://agentskills.io/home) 格式。

## Skills 如何工作?

在实践中,技能是自包含的文件夹,将指令、脚本和资源打包在一起,供 AI 代理在特定用例中使用。每个文件夹包含一个 `SKILL.md` 文件,其中包含 YAML 前置数据(名称和描述),后跟随着技能激活时您的编码代理遵循的指导。

> [!TIP]
> 如果您的代理不支持技能,您可以直接使用 [`agentsmd/AGENTS.md`](agentsmd/AGENTS.md) 作为备用。

此仓库中的 `hf-cli` 技能还可通过以下方式获取:
 - Cursor Marketplace (https://cursor.com/marketplace/huggingface)
 - Codex Plugins Directory (https://developers.openai.com/codex/plugins)

## 安装

Hugging Face 技能与 Claude Code、Codex、Gemini CLI 和 Cursor 兼容。

### Claude Code

1. 将仓库注册为插件市场:  
   
```
/plugin marketplace add huggingface/skills
```

2. 安装 CLI 技能:  
   
```
/plugin install hf-cli@huggingface/skills
```

3. 要安装其他 Hugging Face 技能,请使用 `hf` CLI:  

```
hf skills add <skill-name>
```

### Codex

1. 将您要使用的任何技能从此仓库的 `skills/` 目录复制或符号链接到 Codex 的标准 `.agents/skills` 位置之一(例如,`$REPO_ROOT/.agents/skills` 或 `$HOME/.agents/skills`),如 [Codex Skills 指南](https://developers.openai.com/codex/skills/) 中所述。

2. 一旦技能在这些位置之一可用,Codex 将使用 Agent Skills 标准发现它,并在它决定使用该技能或当您显式调用它时加载 `SKILL.md` 指令。

3. 如果您的 Codex 设置仍然依赖 `AGENTS.md`,您可以使用此仓库中生成的 [`agentsmd/AGENTS.md`](agentsmd/AGENTS.md) 文件作为指令的备用包。

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

通过 Cursor 插件流程从仓库 URL(或本地签出)安装。市场条目有意只限定为 `hf-cli`；使用 `hf skills add <skill-name>` 安装其他工作流技能。

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
| `hf-cli` | Hugging Face Hub CLI(`hf`),用于在 Hugging Face Hub 上下载、上传和管理模型、数据集、Spaces、存储桶、代码仓库、论文、作业等。 | [SKILL.md](skills/hf-cli/SKILL.md) |
| `hf-cloud-aws-context-discovery` | 在任何 AWS 任务开始时发现用户的本地 AWS 上下文(活动 profile、区域、账户 ID、调用者身份)。 | [SKILL.md](skills/hf-cloud-aws-context-discovery/SKILL.md) |
| `hf-cloud-python-env-setup` | 为 SageMaker / AWS 工作搭建一个隔离的 Python 环境,使用正确的 Python 版本和最新的 boto3。 | [SKILL.md](skills/hf-cloud-python-env-setup/SKILL.md) |
| `hf-cloud-sagemaker-deployment-planner` | 规划和协调将模型部署到 Amazon SageMaker AI。 | [SKILL.md](skills/hf-cloud-sagemaker-deployment-planner/SKILL.md) |
| `hf-cloud-sagemaker-iam-preflight` | 在部署或训练前确保存在可用的 SageMaker 执行角色。 | [SKILL.md](skills/hf-cloud-sagemaker-iam-preflight/SKILL.md) |
| `hf-cloud-sagemaker-production-defaults` | 创建默认启用自动扩缩容、CloudWatch 告警和标签的 SageMaker 端点(实时或异步)。 | [SKILL.md](skills/hf-cloud-sagemaker-production-defaults/SKILL.md) |
| `hf-cloud-serving-image-selection` | 为 SageMaker 模型部署选择合适的服务容器并查找其当前镜像 URI。 | [SKILL.md](skills/hf-cloud-serving-image-selection/SKILL.md) |
| `hf-mem` | 用于从 Hugging Face Hub 估算加载 Safetensors 或 GGUF 模型权重进行推理所需内存的 Hugging Face CLI。 | [SKILL.md](skills/hf-mem/SKILL.md) |
| `huggingface-best` | 当用户询问为某个任务寻找最佳、顶级或推荐的模型,想知道该使用哪个 AI 模型,或想按基准分数比较模型时使用。 | [SKILL.md](skills/huggingface-best/SKILL.md) |
| `huggingface-community-evals` | 在本地硬件上使用 inspect-ai 和 lighteval 为 Hugging Face Hub 模型运行评估。 | [SKILL.md](skills/huggingface-community-evals/SKILL.md) |
| `huggingface-datasets` | 用于 Hugging Face Dataset Viewer API 工作流,获取子集/拆分元数据、行分页、文本搜索、应用筛选器、下载 parquet URL,以及读取大小或统计信息。 | [SKILL.md](skills/huggingface-datasets/SKILL.md) |
| `huggingface-gradio` | 使用 Python 构建 Gradio Web UI 和演示。 | [SKILL.md](skills/huggingface-gradio/SKILL.md) |
| `huggingface-llm-trainer` | 使用 TRL(Transformer Reinforcement Learning)或 Unsloth 结合 Hugging Face Jobs 基础设施训练或微调语言和视觉模型。 | [SKILL.md](skills/huggingface-llm-trainer/SKILL.md) |
| `huggingface-local-models` | 用于选择使用 llama.cpp 和 GGUF 在 CPU、Mac Metal、CUDA 或 ROCm 上本地运行的模型。 | [SKILL.md](skills/huggingface-local-models/SKILL.md) |
| `huggingface-lora-space-builder` | 为用户提供的 LoRA 构建并发布 Hugging Face Spaces 上的 Gradio 演示。 | [SKILL.md](skills/huggingface-lora-space-builder/SKILL.md) |
| `huggingface-paper-publisher` | 在 Hugging Face Hub 上发布和管理研究论文。 | [SKILL.md](skills/huggingface-paper-publisher/SKILL.md) |
| `huggingface-papers` | 以 markdown 格式查找和阅读 Hugging Face 论文页面,并使用论文 API 获取结构化元数据,如作者、链接的模型/数据集/Spaces、Github 仓库和项目页面。 | [SKILL.md](skills/huggingface-papers/SKILL.md) |
| `huggingface-spaces` | 在 Hugging Face Spaces 上构建、部署和维护应用 — Gradio / Docker / Static SDK、ZeroGPU 和专用硬件、模型加载、调试、存储桶、推理提供商、社区资助。 | [SKILL.md](skills/huggingface-spaces/SKILL.md) |
| `huggingface-tool-builder` | 当用户想要构建工具/脚本,或想借助 Hugging Face API 的数据完成任务时使用此技能。 | [SKILL.md](skills/huggingface-tool-builder/SKILL.md) |
| `huggingface-trackio` | 使用 Trackio 跟踪和可视化 ML 训练实验。 | [SKILL.md](skills/huggingface-trackio/SKILL.md) |
| `huggingface-vision-trainer` | 使用 Hugging Face Transformers 在 Hugging Face Jobs 云 GPU 上训练和微调目标检测模型(D-FINE、RT-DETR v2、DETR、YOLOS)、图像分类模型(timm 模型 — MobileNetV3、MobileViT、ResNet、ViT/DINOv3 — 以及任意 Transformers 分类器)和 SAM/SAM2 分割模型。 | [SKILL.md](skills/huggingface-vision-trainer/SKILL.md) |
| `huggingface-zerogpu` | 使用 Gradio Spaces 和 Hugging Face Spaces ZeroGPU 进行 AI 演示和 GPU 计算。 | [SKILL.md](skills/huggingface-zerogpu/SKILL.md) |
| `train-sentence-transformers` | 训练或微调 `SentenceTransformer`(双编码器；密集或静态嵌入模型；用于检索、相似度、聚类、分类、释义挖掘、去重、多模态)、`CrossEncoder`(重排序器；用于两阶段检索/配对分类的配对打分)和 `SparseEncoder`(SPLADE,稀疏嵌入模型；用于学习型稀疏检索)这三种架构的 sentence-transformers 模型。 | [SKILL.md](skills/train-sentence-transformers/SKILL.md) |
| `transformers-js` | 使用 Transformers.js 直接在 JavaScript/TypeScript 中运行最先进的机器学习模型。 | [SKILL.md](skills/transformers-js/SKILL.md) |
| `trl-training` | 使用 TRL(Transformers Reinforcement Learning)训练和微调 transformer 语言模型。 | [SKILL.md](skills/trl-training/SKILL.md) |
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
4. 默认不要将该技能添加到 `.claude-plugin/marketplace.json` 中。客户端市场有意只限定为 `hf-cli`；完整的 Hub CLI 市场清单生成于 `.claude-plugin/marketplace-internal.json`。
5. 运行:
   ```bash
   ./scripts/publish.sh
   ```
   以重新生成并验证所有生成的元数据。
6. 在您的编码代理中重新安装或重新加载技能包,以便更新的文件夹可用。

### Marketplace

`.claude-plugin/marketplace.json` 和 `.cursor-plugin/marketplace.json` 文件有意只暴露 `hf-cli` 供客户端市场安装。这使安装时使用的清单聚焦于核心 Hub 操作，其余技能则引导用户使用 `hf skills add <skill-name>`。

生成的 `.claude-plugin/marketplace-internal.json` 文件包含完整的技能列表。发布自动化流程会将其作为 `marketplace.json` 上传到 Hub 存储桶，使 `hf skills list`、`hf skills add` 和 `hf skills update` 能继续看到所有可用技能。

较新的支持技能的集成也可以动态拉取能力。Hugging Face 的发现流程允许客户端搜索技能、MCP 服务器和 Spaces，而 Skills-over-MCP 相关工作正在标准化如何通过 MCP 资源发现和使用技能。

### 其他参考
- 直接在 [huggingface/skills](https://github.com/huggingface/skills) 浏览最新的指令、脚本和模板。
- 查看您在每个技能中引用的特定库或工作流程的 Hugging Face 文档。

---

## 原项目文档

如需查看原项目的完整英文文档,请访问:

- [README.md (英文原版)](README.md) - 原项目的完整说明文档

原项目由 [Hugging Face](https://github.com/huggingface) 维护。
