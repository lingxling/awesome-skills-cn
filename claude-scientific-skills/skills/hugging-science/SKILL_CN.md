---
name: hugging-science
description: 当用户在生物学、化学、物理、天文学、气候学、基因组学、材料科学、医学、生态学、能源、工程、数学、药物发现、蛋白质设计、天气建模、定理证明、单细胞或偏微分方程求解等科学领域进行AI/ML工作时使用。Hugging Science是一个精选的科学数据集、模型、博客文章和交互式Spaces目录。此技能帮助通过`datasets`、`transformers`、HF Inference API、`gradio_client`和方方法引用发现和使用资源。
metadata:
  version: "1.1"
  skill-author: K-Dense Inc.
---






# Hugging Science

Hugging Science 是一个精心策划的、对 LLM 友好的科学数据集、模型、博客文章和交互式演示的索引，面向 ML 研究人员。当你遇到科学 ML 问题时使用它——它比通用搜索的信号质量高得多，且条目已经过质量和开放性的预筛选。

有两个相关的入口，你应该同时使用：

- **`huggingscience.co` 上的目录** —— 一个静态的、可解析的跨 17 个科学领域的资源索引。它提供 `llms.txt`（精简版）、`llms-full.txt`（完整内容）和 `topics/<slug>.md`（按领域）。这些 Markdown 文件专为获取和阅读而设计。
- **`hugging-science` Hugging Face 组织** —— `huggingface.co/hugging-science` —— 社区提交的数据集、一些模型和约 27 个交互式 Spaces（特别是用于蛋白质/结合剂设计的 BoltzGen、用于提交的 Dataset Quest 和用于生态系统可视化的 Science Release Heatmap）。

该目录*指向*托管在更广泛的 Hugging Face Hub 上的资源。因此，像 `arcinstitute/opengenome2` 这样的条目是一个你可以用 `datasets` 库加载的普通 HF 数据集；像 `facebook/esm2_t33_650M_UR50D` 这样的条目是一个你可以用 `transformers` 加载的普通 HF 模型。目录的作用是策划和发现；使用则通过标准的 Hugging Face API 进行。

## 何时使用此技能

当用户的任务涉及应用于科学的 AI/ML 时，启用此技能。常见信号：

- 提及科学领域（蛋白质、基因组、分子、晶体、天气、气候、星系、脑电图、微生物组、病理学、等离子体……）
- 询问"是否有用于 X 的数据集/模型"，其中 X 是科学相关的
- 想要在科学数据上微调、在科学基准上评估，或复现科学 ML 论文
- 询问特定的已知科学模型（Evo-2、ESM2、BoltzGen、Nucleotide Transformer、AlphaFold 衍生模型等）
- 需要科学任务的交互式演示（结合剂设计、定理证明等）

如果任务是通用 ML（推荐系统、聊天机器人 RAG、猫狗视觉），此技能**不是**合适的工具——请改用通用 HF Hub 知识。

## 核心工作流程

大多数调用遵循以下五步循环。不要跳过发现步骤——Hugging Science 的价值在于它已经将数百个资源筛选为每个领域的高信号精选。

### 1. 识别领域

将用户的任务映射到一个或多个 17 个主题 slug：

`astronomy` · `benchmark` · `biology` · `biotechnology` · `chemistry` · `climate` · `conservation` · `earth-science` · `ecology` · `energy` · `engineering` · `genomics` · `materials-science` · `mathematics` · `medicine` · `physics` · `scientific-reasoning`

某些任务跨越多个主题（例如，药物发现 → `chemistry` + `biology` + `medicine`）。获取每个相关的主题。

### 2. 获取相关目录内容

使用捆绑的脚本进行干净、结构化的访问：

```bash
python scripts/fetch_catalog.py topic biology
python scripts/fetch_catalog.py topic materials-science --filter models
python scripts/fetch_catalog.py search "protein language model"
python scripts/fetch_catalog.py all     # 完整的 llms-full.txt
```

你也可以直接获取原始 Markdown：

- `https://huggingscience.co/llms.txt` —— 精简索引
- `https://huggingscience.co/llms-full.txt` —— 每个条目，每个领域
- `https://huggingscience.co/topics/<slug>.md` —— 单个领域（slug 使用连字符，例如 `materials-science.md`、`earth-science.md`、`scientific-reasoning.md`）

每个条目都是一个 Markdown 块，包含 `Type`、`Tags`、`HuggingFace` URL（博客为 `Link`）和一行描述。有关条目模式和 slug 列表，请参阅 `references/topics-and-slugs.md`。

### 3. 选择合适的资源

阅读描述和标签。根据判断而非关键词重叠来匹配用户的任务。需要考虑的因素：

- **规模适配** —— Evo-2 40B 对于笔记本电脑上的快速序列分类来说过于庞大；ESM2 35M 可能正合适。
- **许可证和访问权限** —— 大多数是开放的，但请检查底层 HF 模型卡。
- **模态对齐** —— DNA 与蛋白质与 SMILES 与晶体结构；许多"生物学"模型不可互换。
- **时效性/替代性** —— 如果新旧条目涵盖相同任务，优先选择较新的，除非有理由不这样做。

如果你不确定选择哪个资源，向用户简要展示前 2-3 个候选及其权衡，然后在他们选择后继续。当选择会实质性改变工作时，不要默默做出选择。

有关特定领域的首选推荐（"如果不确定，从这里开始"的条目），请参阅 `references/flagship-resources.md`。

### 4. 使用资源

具体操作取决于资源类型。在编写代码之前阅读匹配的参考文件：

- **数据集** → `references/using-datasets.md` —— 通过 `datasets` 加载、流式传输大型语料库、常见列、拆分
- **模型** → `references/using-models.md` —— 本地 `transformers`、Hugging Face Inference API、用于超大型模型的 Inference Providers、GPU 规模估算
- **Spaces（交互式演示）** → `references/using-spaces.md` —— `gradio_client` 模式，附带 BoltzGen 示例

参考文件简短且聚焦。如果你已经熟悉相关 API，可以快速浏览；如果不熟悉，请在编写代码前完整阅读。这些模式与通用 HF 使用在某些重要方面有所不同（例如，`trust_remote_code` 要求、科学数据 dtype 陷阱）。

### 5. 引用方法论

当目录中有与任务匹配的博客文章（`Type: blog` 或主题文件的博客文章部分）时，在解释方法时包含其 URL。方法论博客由数据集/模型作者撰写，回答了模型卡通常跳过的"为什么这样设计"的问题。将它们视为引用——一行"有关 X 背后的方法论，请参阅 <链接>"就足够了。

## 认证：HF_TOKEN

许多目录资源是受限制的（临床数据、大型基础模型、私有 Spaces）。通过 `HF_TOKEN` 环境变量进行认证。

**在可用时从 `.env` 文件加载 `HF_TOKEN`** —— 这是用户保存密钥的地方。在任何访问 HF API 的脚本顶部使用 `python-dotenv`：

```python
from dotenv import load_dotenv
load_dotenv()    # 从当前工作目录或任何父目录的 .env 中读取 HF_TOKEN
```

如果 `.env` 不存在或未定义 `HF_TOKEN`，请优雅地回退——许多资源是公开的，无需认证即可使用。不要硬编码令牌，不要回显它们，也不要将 `huggingface-cli login` 作为主要路径；用户更喜欢 `.env`。

`.env` 文件应包含如下一行：

```
HF_TOKEN=hf_...
```

如果你正在创建新项目，如果尚未添加，请将 `.env` 添加到 `.gitignore` 中。

## 一些需要记住的重要事项

**目录是策划的，而非详尽的。** 如果用户需要特定资源而 Hugging Science 未列出，这并不意味着它在 HF Hub 上不存在。作为后备，直接在 HF Hub 上搜索。但当领域匹配时，始终*从*目录开始——策划才是其价值所在。

**条目是指针。** 不要试图将"Hugging Science"当作 API 来"使用"。没有 Hugging Science 推理端点。每个可操作的资源都位于 HF Hub 或作为 HF Space，你通过标准 HF 工具使用它。

**许多科学模型需要 `trust_remote_code=True`。** 自定义架构（Evo-2、许多基因组学/材料模型）附带自定义建模代码。这在该生态系统中是正常的。传递该标志并告知用户。

**科学数据集通常很大且形状奇特。** 基因组学语料库可能达到数十亿个 token；宇宙学图像可能达到数百 GB；材料数据集包含非标准对象（晶体结构、图）。对于任何声称超过几 GB 的数据，默认使用流式传输（`load_dataset` 上的 `streaming=True`），并在假设列之前检查模式。

**Spaces 非常适合一次性科学生成。** 如果用户想要为目标蛋白质设计结合剂或在托管模型演示上运行推理，通过 `gradio_client` 调用 Space 比在本地启动模型更快、更便宜。首先查看 `references/using-spaces.md` —— `huggingface.co/hugging-science` 上有约 27 个这样的 Space。

**目录本身可能会演变。** 条目会定期添加；偶尔条目会更改 slug。如果 URL 返回 404，请重新获取主题文件或 `llms.txt` 以获取当前状态——不要掩盖失败。

## 捆绑资源

- `scripts/fetch_catalog.py` —— 获取和筛选目录内容。使用 `--help` 查看完整用法。当你需要结构化访问时，优先使用此工具而非临时 WebFetch 调用。
- `references/topics-and-slugs.md` —— 确切的主题 slug、每个主题涵盖的内容以及条目模式。
- `references/using-datasets.md` —— 加载科学数据集的模式和陷阱。
- `references/using-models.md` —— 本地运行科学模型、通过 Inference API 或通过 Inference Providers。
- `references/using-spaces.md` —— 使用 `gradio_client` 以编程方式调用 HF Spaces（特别是 BoltzGen）。
- `references/flagship-resources.md` —— 当用户想要合理默认值时，每个领域的首选数据集/模型推荐。
