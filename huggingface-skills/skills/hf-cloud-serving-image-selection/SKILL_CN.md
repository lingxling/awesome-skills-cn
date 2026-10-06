---
name: hf-cloud-serving-image-selection
description: '为 SageMaker 模型部署选择合适的服务容器，并找到其当前的镜像 URI。每当即将把模型部署到 SageMaker 端点且需要选择镜像 URI 时，都应使用此技能——包括用户说"部署这个 LLM"、"托管这个 HuggingFace 模型"、"为这个微调模型提供服务"、"部署这个嵌入模型"、"托管一个重排序器"、"为一个 sentence-transformers 模型提供服务"，或即将在部署代码中硬编码任何容器 URI 时。始终优先选择 HuggingFace 精选的 Deep Learning Containers：HuggingFace vLLM（LLM 和生成式重排序器）、HuggingFace vLLM-Omni（多模态）、TEI（嵌入/交叉编码器重排序器）、HF Inference Toolkit（其他 transformers 模型）。仅当没有兼容的 HuggingFace 镜像时才使用通用镜像（AWS vLLM、DJL-LMI、SGLang）——绝不能仅仅因为它们版本更新就使用。切勿凭记忆硬编码容器 URI，也切勿默认使用 TGI。可防止镜像过时导致的失败和区域错误的 URI。'
---

# 服务镜像选择

服务容器是最有可能让一个"纸面上看起来正确"的 SageMaker 部署失败的那一个因素。容器选错、标签过时或 AMI 错误——都会产生同样不透明的 `Failed to pass health check` 错误。

## 第零条规则：HuggingFace 镜像始终优先

当 HuggingFace 精选系列（`huggingface-vllm`、`huggingface-vllm-omni`、`huggingface-sglang`、`tei`、`huggingface-pytorch-inference`）和通用系列（`vllm`、`vllm-omni`、`sglang`、`djl-inference`）都能为该模型提供服务时，**HuggingFace 镜像是强制要求，而不仅是优先选择**。使用通用镜像的唯一合理理由是：

1. **已验证的不兼容** — 模型需要的架构/模态/功能没有任何可用的 HuggingFace 标签支持，并已对照目录确认（而非假设）。
2. **目标区域中不存在 HuggingFace 标签**，且无法进行镜像同步。
3. **该 HuggingFace 镜像位于下文的"已知损坏的镜像"中。**

**通用仓库的版本号更新并不是理由。**AWS `vllm` 仓库发布的 vLLM 版本常常高于 `huggingface-vllm`；较旧但兼容的 `huggingface-vllm` 标签仍然胜出。"最新的 vLLM"不是任何人提出的需求——与模型的兼容性才是。如果你回退到通用镜像，请在部署日志中记录适用的是上述三条理由中的哪一条。

## 镜像 URI 从哪里获取

**主要来源：AWS 官方 Deep Learning Containers 目录。**

URL：https://aws.github.io/deep-learning-containers/reference/available_images/

此页面由 AWS 维护，列出了每个镜像系列的示例 URI、标签、CUDA 版本、Python 版本和平台（SageMaker 与 EC2/ECS/EKS）。为部署选择 URI 时，**直接从此页面读取**——复制示例 URL，将 `<region>` 替换为用户的区域，然后传给 `deploy.py --image-uri`。

示例 URL 中大多数区域使用 `763104351884` 作为账户 ID。少数区域使用不同的账户（例如 `eu-south-1` 使用 `692866216735`）。如有疑问，请查看 [Region Availability 页面](https://aws.github.io/deep-learning-containers/reference/region_availability/)。

**例外：目前没有。**此工作流使用的每个镜像系列现在都在 AWS 目录页面上（TEI 于 2026 年末加入）。如果遇到不在其中的新系列，请通过 `mirror_image.py` 进行镜像同步，并直接传入生成的 URI。

## 快速决策

| 模型 | 容器系列 | 如何获取 URI |
|---|---|---|
| HuggingFace 文本生成 LLM（Llama、Qwen、Mistral 等） | **HuggingFace vLLM** | AWS 目录 → "HuggingFace vLLM Inference"（ECR 仓库 `huggingface-vllm`） |
| 同上，多模态 | **HuggingFace vLLM-Omni** | AWS 目录 → "HuggingFace vLLM-Omni Inference"（ECR 仓库 `huggingface-vllm-omni`） |
| HuggingFace 嵌入模型 | TEI | AWS 目录 → "HuggingFace Text Embeddings Inference" |
| 编码器 / 交叉编码器重排序器（BERT 系列 `*ForSequenceClassification`） | TEI | 同嵌入模型 |
| **生成式重排序器**（因果语言模型，例如 Qwen3-Reranker） | HuggingFace vLLM | 同文本生成 LLM — **不是 TEI**，参见"重排序器：TEI 还是 vLLM？" |
| 文生图 / 扩散模型（Stable Diffusion、FLUX） | DJL Inference | AWS 目录 → "DJL Inference" — **不是** HF Inference Toolkit，参见"已知损坏的镜像" |
| HuggingFace 分类器、NER、问答、摘要 | HF Inference Toolkit（CPU） | AWS 目录 → "HuggingFace PyTorch Inference"；GPU 标签目前已损坏 — 参见"已知损坏的镜像" |
| 用户明确想要 SGLang | HuggingFace SGLang | AWS 目录 → "HuggingFace SGLang Inference" |
| 没有兼容的 `huggingface-vllm` 标签（已验证的不兼容或区域缺失 — 参见"第零条规则"） | vLLM（AWS） | AWS 目录 → "vLLM" 部分 — 仅作回退，绝不为追求版本新鲜度而使用 |
| 用户明确想要 DJL-LMI | DJL Inference | AWS 目录 → "DJL Inference" |
| Amazon Nova | SageMaker JumpStart | 使用 JumpStart，而不是直接创建端点 |
| 自定义推理代码 | BYOC | 由用户提供 URI |

**当存在兼容的 HuggingFace 精选 DLC 时，必须使用它（参见"第零条规则"）。**`huggingface-vllm` 直接构建在 AWS vLLM DLC 之上——**完全相同的 `SM_VLLM_*` 环境变量约定和同样的 cu130 AMI 规则**——并增加了最新的 `transformers`、最新的 `huggingface_hub` + `hf_xet`（避免旧镜像会遇到的 XET-CDN 403 下载失败）以及 HF 性能默认设置。它也是 SageMaker SDK v3 自动路由的目标。AWS `vllm` 镜像只是兼容性的应急出口；它显示的 vLLM 版本通常高于 `huggingface-vllm`，但这不是选择它的理由。

**不要使用 TGI。**Text Generation Inference 已被归档。归档之后发布的模型（最著名的是 Qwen3）在 TGI 上无法通过 ping 健康检查。请改用 vLLM。（SageMaker SDK v3 也是这么做的：自 2026 年 6 月的 [PR #5960](https://github.com/aws/sagemaker-python-sdk/pull/5960) 起，其 `ModelBuilder` 会将 `text-generation` 自动路由到 HuggingFace vLLM DLC，将多模态任务路由到 HuggingFace vLLM-Omni。）

每个系列的完整理由见 `references/model-to-image.md`。

## 重排序器：TEI 还是 vLLM？

"重排序器"涵盖两种截然不同的架构，选错会在 TEI 拒绝该模型之前浪费一个完整的端点创建周期（约 20 分钟）：

- **编码器交叉编码器**（BAAI/bge-reranker-*、mixedbread、大多数 `sentence-transformers` 重排序器）— 带分类头的 BERT 系列模型。`config.json` 中在 TEI 支持的编码器类型上有 `architectures: [..ForSequenceClassification]`。→ **TEI**。
- **生成式重排序器**（Qwen/Qwen3-Reranker-* 以及类似的因果语言模型评判器）— 通过 yes/no token 的 logprob 对相关性打分的解码器 LLM。`config.json` 中有 `architectures: [..ForCausalLM]`。→ **HuggingFace vLLM**，与文本生成 LLM 的部署方式完全相同。TEI 会加载该架构，然后拒绝 `classifier` 模型类型（TEI 对 Qwen3 的支持*仅限嵌入*）。调用模式（原始 completions API、`max_tokens=1`、logprobs 打分）见 `hf-cloud-sagemaker-production-defaults`。

**在创建任何资源之前进行预检**——一次 HTTP GET 即可确定：

```bash
curl -s https://huggingface.co/<model-id>/raw/main/config.json
# "architectures": ["Qwen3ForCausalLM"]              → vLLM
# "architectures": ["XLMRobertaForSequenceClassification"] → TEI
```

对于 TEI，还要确认 *(架构, 任务)* 组合：某个架构出现在 TEI 的支持列表中意味着支持嵌入，但不一定支持分类/重排序。

提醒：SageMaker SDK v3（PR #5960）会**无条件地**将 `text-ranking` 任务路由到 TEI——这对交叉编码器是正确的，对生成式重排序器则是错误的。不要把 SDK 的路由当作 TEI 能为某个重排序器提供服务的证据。

## 工作流

对于每个系列：**从 AWS 目录页面读取 URI**。

1. 打开 https://aws.github.io/deep-learning-containers/reference/available_images/
2. 找到对应系列的部分（例如 HuggingFace LLM 对应 "HuggingFace vLLM Inference"，嵌入对应 "HuggingFace Text Embeddings Inference"）
3. 选择平台列标记为 `SageMaker` 的最新一行——是**该系列内**的最新版本。不要因为其他系列的部分列出了更高的引擎版本就切换过去（参见"第零条规则"）
4. 将 `<region>` 替换为用户的区域（来自 `hf-cloud-aws-context-discovery`）
5. 对于 vLLM：还要检查 AMI 要求（参见下文"vLLM AMI 要求"）
6. 将 URI 传给 `deploy.py --image-uri`（实时）或 `deploy_async.py --image-uri`（异步）

### TEI：选择正确的变体

TEI 目录行列出了两个 URI——GPU（`tei` 仓库）和 CPU（`tei-cpu` 仓库）。根据实例类型选择：

- `ml.g*`、`ml.p*`、`ml.inf*` → GPU 变体
- `ml.c*`、`ml.m*`、`ml.t*` → CPU 变体

混用会失败：GPU 实例上运行 CPU 镜像会浪费硬件，CPU 实例上运行 GPU 镜像会无法启动。

**关于 TEI 账户 ID 的说明**：目录页面显示 `683313688378` 作为示例账户，但 TEI 是从与主要 AWS DLC 不同的账户命名空间发布的，并且各区域的账户 ID 各不相同。如果在 us-east-1 以外的区域，`683313688378.dkr.ecr.<region>.amazonaws.com/tei:...` 返回 ECR 拉取错误，请查看 [Region Availability 页面](https://aws.github.io/deep-learning-containers/reference/region_availability/) 获取该区域的正确账户 ID。

## vLLM AMI 要求

**CUDA 13 或更高版本**（当前默认：`cu130`）的 vLLM DLC 镜像需要在 ProductionVariant 上设置 `InferenceAmiVersion=al2-ami-sagemaker-inference-gpu-3-1`。这同样适用于 `huggingface-vllm` 和 `huggingface-vllm-omni`（构建在相同的 cu130 基础之上）以及 AWS `vllm` 仓库。如果不设置，容器会在启动时死亡，并且从不创建任何 CloudWatch 日志。这种失败看起来与许多其他问题（账户层面问题、配额、网络）完全相同，经常把人引向错误的诊断方向。

查找表：

| 标签包含 | 要传入的 InferenceAmiVersion |
|---|---|
| `cu130`（或更高） | `al2-ami-sagemaker-inference-gpu-3-1` |
| `cu129` 或更低 | （省略该标志；默认 AMI 即可工作） |

经验法则：如果你选择的 vLLM 标签包含 `cu130` 或更高版本，请向 `deploy.py` 传入 `--inference-ami-version al2-ami-sagemaker-inference-gpu-3-1`。如果未来的 CUDA 版本（cu140+）需要不同的 AMI，请在 AWS 发布新镜像时向表中添加一行。

这是 vLLM 特有的问题。TEI 和 HF Inference Toolkit 镜像不需要覆盖 AMI。

## 配置 vLLM DLC（HuggingFace vLLM 和 AWS vLLM）

两个镜像共享同一约定：配置以环境变量形式写在 SageMaker 模型定义上，`SM_VLLM_*` 映射到 vLLM CLI 标志。`huggingface-vllm` 的入口点在未设置 `SM_VLLM_MODEL` 时还会自动检测模型——如果挂载了 S3 制品则从 `/opt/ml/model` 检测，否则从 `HF_MODEL_ID` 检测。在生产环境中，请将 `SM_VLLM_MODEL` 指向 `/opt/ml/model`；在运行时直接从 Hub 加载属于例外情况。

### 每个 HuggingFace LLM 部署都必需

| 环境变量 | 用途 | 说明 |
|---|---|---|
| `SM_VLLM_MODEL` | HF 模型 ID（例如 `Qwen/Qwen3-0.6B`），从 S3 加载时为 `/opt/ml/model` | — |
| `SM_VLLM_HOST` | **必须为 `0.0.0.0`** | 否则 vLLM 只绑定 localhost，ping 失败，容器在产生日志之前就会死亡。这是该镜像出现神秘失败的首要原因。 |
| `SM_VLLM_TRUST_REMOTE_CODE` | 模型制品是否可以执行自定义 Python 代码 | **默认 `false`。**仅当某个特定架构没有其仓库代码就无法加载时，并在审查和固定这些制品之后，才设为 `true`。启用它会允许模型提供的代码在容器内运行。 |
| `HUGGING_FACE_HUB_TOKEN` | HF token | 受限模型必需。 |

将生产模型制品放置在账户控制的 S3 存储桶中，将其 URI 作为 `--model-s3-uri` 传入，并使用 `SM_VLLM_MODEL=/opt/ml/model`。这样可以避免在运行时下载或执行仓库代码。仅当明确需要运行时访问 Hub 时才使用 Hub 模型 ID；除非该架构需要经过审查的自定义代码，否则保持 `SM_VLLM_TRUST_REMOTE_CODE=false`。

### 调优（可选）

| 环境变量 | 用途 |
|---|---|
| `SM_VLLM_MAX_MODEL_LEN` | 最大序列长度 — 请设置此项；默认值对微调模型可能是错误的 |
| `SM_VLLM_GPU_MEMORY_UTILIZATION` | 0.0–1.0 之间的浮点数，~0.9 较为合理 |
| `SM_VLLM_TENSOR_PARALLEL_SIZE` | 多 GPU 实例的 GPU 数量 |
| `SM_VLLM_DTYPE` | `auto`、`bfloat16`、`float16` |

任何 vLLM CLI 标志都可以使用——转为大写，将短横线替换为下划线，并加上前缀 `SM_VLLM_`。

## 配置 TEI

环境变量约定比 vLLM 更简单：

| 环境变量 | 用途 | 是否必需 |
|---|---|---|
| `HF_MODEL_ID` | HF 模型 ID（例如 `BAAI/bge-large-en-v1.5`）或 `/opt/ml/model` | 是 |
| `HF_TOKEN` | HF 认证 token | 仅受限模型需要 |
| `MAX_BATCH_TOKENS` | 每批次最大 token 数（默认 16384） | 否 |
| `MAX_CLIENT_BATCH_SIZE` | 每个客户端批次的最大请求数（默认 32） | 否 |

无需配置主机绑定，也没有 trust-remote-code 标志。TEI 支持的架构（BERT、CamemBERT、RoBERTa、XLM-RoBERTa、NomicBert、JinaBert、JinaCodeBert、Mistral、Qwen2/3、Gemma2/3、ModernBert）已内置在镜像中。

## CUDA / 实例兼容性

至关重要且容易出错：

| 镜像标签中的 CUDA | 默认 AMI | 使用 `al2-ami-sagemaker-inference-gpu-3-1` 时 |
|---|---|---|
| cu124 / cu128 | g5、g6、p5 均可工作 | （不需要） |
| cu129 | g6、p5；g5 失败（驱动不匹配 → CannotStartContainerError） | 预计可修复 g5（未验证） |
| cu130+ | 在任何地方都失败 — AMI 标志是强制的 | g5、g6、p5 均可工作（cu130 在 g5 上已于 2026 年 6 月验证） |

驱动来自主机 AMI，而不是实例系列——因此传入 gpu-3-1 AMI（vLLM cu130 镜像本来就需要）也能让 `ml.g5.*` 适用于 cu129+ 镜像。

## VPC / NAT 网关问题

位于**没有** NAT 网关的 VPC 中的 SageMaker 端点无法从 `public.ecr.aws` 拉取镜像。部署会以镜像拉取错误失败，而错误信息中不会提及 "VPC" 或 "egress"。

对于 AWS 区域 ECR 上的镜像（目录中的所有镜像）：SageMaker 通过内置路由访问它们，不需要 NAT。使用区域 URI 格式（`<account>.dkr.ecr.<region>.amazonaws.com/...`），而不是 `public.ecr.aws/...` 格式。

对于需要访问 `public.ecr.aws` 的镜像（不太常见）：使用 `scripts/mirror_image.py`（跨平台；需要 Docker + `aws` CLI）将其镜像同步到你账户中的私有 ECR 仓库。在 AWS CLI 可用的 shell 中运行它。

```bash
# macOS / Linux
PRIVATE_URI=$(python3 scripts/mirror_image.py \
    public.ecr.aws/deep-learning-containers/vllm:<tag> \
    vllm-mirror)
```

```powershell
# Windows (PowerShell) — 将 stdout 捕获到变量中
$PRIVATE_URI = python scripts\mirror_image.py `
    public.ecr.aws/deep-learning-containers/vllm:<tag> vllm-mirror
```

## 当目录页面无法渲染、内容过时或有误时

**页面无法渲染 / 获取返回无用内容**：目录页面大量依赖 JavaScript，某些获取工具只能拿到空壳。回退方案依次为：

1. **GitHub 上目录的源数据** — 该页面由每个版本一个 YAML 文件生成，列出了确切的标签、CUDA 和 Python 版本。列出某个系列的文件，然后获取最新的：
   ```bash
   curl -s https://api.github.com/repos/aws/deep-learning-containers/contents/docs/src/data/huggingface-vllm
   curl -s https://raw.githubusercontent.com/aws/deep-learning-containers/main/docs/src/data/huggingface-vllm/0.21.0-gpu-sagemaker.yml
   ```
   目录名与 ECR 仓库一致（`huggingface-vllm`、`huggingface-vllm-omni`、`huggingface-tei`、`vllm`、`djl-inference`……）。
2. **直接查询 ECR**，获取目标区域中的当前标签（需要能读取 DLC 注册表的凭证；如果返回 AccessDenied，请使用 YAML 文件）：
   ```bash
   aws ecr describe-images --registry-id 763104351884 --repository-name huggingface-vllm \
       --region <region> --query 'sort_by(imageDetails,&imagePushedAt)[-5:].imageTags' --output json
   ```
3. [DLC GitHub 仓库上的发布说明](https://github.com/aws/deep-learning-containers/releases)。

**某个标签刚刚发布，还没有出现在页面上**：这种情况很少见；AWS 在每次发布时都会更新页面。请查看上面的发布说明。

**你需要的架构尚未被所列镜像支持**：特别是对于 TEI，你可以将 GHCR 上的上游镜像（`ghcr.io/huggingface/text-embeddings-inference:<version>`）镜像同步到私有 ECR，并将生成的 URI 直接传给 `deploy.py --image-uri`。使用同一个 `mirror_image.py` 脚本。

## 已知损坏的镜像（最后检查于 2026 年 7 月）

| 镜像 | 缺陷 | 改用 |
|---|---|---|
| `huggingface-pytorch-inference` **GPU** 标签 — 测试过的所有近期标签（PT 2.3–2.6、cu121/cu124、transformers 4.48–5.5.3） | 在 `import torch` 时出现 `ImportError: libtorch_cuda.so: undefined symbol: ncclCommResume`。镜像中捆绑的 NCCL 比 torch 链接所需的版本旧——这是*容器内部*的打包缺陷，在 g5 **和** g6 上都存在，与 AMI、模型或推理代码无关。MMS Java 前端会持续响应 `/ping`，因此端点可以达到 InService，而 Python worker 却在崩溃循环、什么都不提供。 | DJL Inference（捆绑了自己完整的 CUDA/NCCL 栈）或 BYOC。CPU 标签不受影响。 |

当 AWS 发布新的 `huggingface-pytorch-inference` GPU 标签时请重新检查——一旦确认镜像已修复，就删除这一行。

**通用回退规则**：当 HF DLC 因 CUDA/NCCL 链接器错误而失败时，切换到 DJL Inference，而不是在同系列的各个标签之间反复尝试——这类缺陷是按仓库存在的，而不是按标签（上述情况尝试了三个不同的标签，全部损坏）。

**相关的 HF Hub 陷阱**：较旧的 DLC 在下载模型时可能会从 HF 的 XET CDN 收到 `403 Forbidden`（它们捆绑的 `huggingface_hub` 早于 XET 认证）。设置 `HF_HUB_ENABLE_HF_TRANSFER=0` 以强制使用标准下载路径，或将权重预先放到 S3 中。

## 首次启动时的 Hub 下载时间

从 HF Hub 加载模型发生在*端点启动后的容器内部*——即使是小模型，也预计需要 **5–15 分钟以上**才能达到 InService，数 GB 的模型则更久。首次启动缓慢并不是失败；在部署脚本的 30 分钟等待到期之前，不要拆除或重新诊断。

对于生产或重复部署，请将权重预先放到 S3 中并向 `deploy.py` 传入 `--model-s3-uri`（模型随后从 `/opt/ml/model` 加载）——速度更快，不受 Hub 速率限制/故障影响，并且运行时不需要 `HUGGING_FACE_HUB_TOKEN`。
