---
name: huggingface-spaces
description: 在 Hugging Face Spaces 上构建、部署和维护应用程序 —— Gradio / Docker / Static SDK、ZeroGPU 与专用硬件、模型加载、调试、存储桶（buckets）、推理提供方（inference providers）、社区资助。当用户要求在 Hugging Face 上创建或托管应用、将代码移植到 ZeroGPU、修复无法构建或运行的 Space，或需要使用 `hf spaces …`、`@spaces.GPU`、Space README 的 frontmatter 或 `spaces` Python 包时使用。
---

# Hugging Face Spaces

Hugging Face Spaces 用于托管机器学习应用。目前已有超过 100 万个；每个 Space 都是一个 git 仓库。本技能涵盖创建、构建、调试和维护它们。

## 0. 准备工作

在做任何事之前：

1. 检查是否安装了 `hf` CLI：`which hf`。如果没有，执行 `pip install -U huggingface_hub`。
2. 检查用户是否已登录：`hf auth whoami`。如果没有，运行 `hf auth login` —— 它会打印一个 URL 和一次性代码；请用户打开该 URL 并输入代码，登录会自动完成（OAuth，无需 token）。也可以用 `--token` 传入一个来自 https://huggingface.co/settings/tokens 的具有写权限的 token。
3. 记下 `whoami` 的 `canPay` 和 `isPro` 标志 —— 它们决定了下面可选的硬件。免费账户（`isPro=False`）只能托管 Static Spaces 和最多 2 个 ZeroGPU Spaces。

`hf-cli` 技能教会 agent 每一个 `hf` 命令，是本技能推荐的配套技能。通过 `hf skills add hf-cli` 安装（加上 `--claude --global` 可同时为 Claude Code 在用户级别安装）。

## 1. 什么是 Space

Space 是一个 git 仓库，有三种可能的 SDK：

- **Gradio** —— 最常见的 Space。Python，迭代速度快，支持 ZeroGPU。
- **Docker** —— 任意容器。当你需要非 Python 技术栈或预构建模板（Streamlit、Argilla、Shiny 等 —— 完整列表见 https://huggingface.co/docs/hub/spaces-sdks-docker）时使用。**不**支持 ZeroGPU。
- **Static** —— 纯 HTML，或在部署时构建的 React/Svelte/Vue 项目。用于浏览器内 ML（transformers.js / WebGPU / WebAssembly / onnxruntime-web）、项目主页、交互式报告，或编排其他 Space 的 Space。不需要硬件。

### 硬件等级

Static Spaces 对所有人免费，不需要硬件。**Gradio 和 Docker Spaces 运行在计算资源上，创建时需要付费计划** —— 个人账户需要 PRO，组织账户需要 Team 或 Enterprise —— 但有一个例外：**信誉良好的免费个人账户（已验证邮箱、账户创建超过 30 天）可以托管最多 2 个 ZeroGPU Spaces。**

所以在免费账户上，ZeroGPU 是托管 Gradio Space 的*唯一*方式。`cpu-basic` 已不再是过去那种安全的后备选项 —— 它同样需要付费权限。

**ZeroGPU（`zero-a10g`）** —— 在 NVIDIA RTX PRO 6000 Blackwell（sm_120）上按请求动态分配 GPU。两种规格：`large`（半个 MIG，48 GB，占用 1× 配额）和 `xlarge`（完整,96 GB，占用 2× 配额）。对 Space 创建者免费；访问 Space 的用户消耗自己的每日配额（约免费 5 分钟 / Pro 40 分钟 / Enterprise 60 分钟）。**仅支持 Gradio**，**以 PyTorch 为主**。每账户的托管上限：免费个人账户 **2 个**，PRO **10 个**，Team / Enterprise 组织 **50 个**。

**`cpu-basic`** —— 2 vCPU / 16 GB，没有按小时计费，但需要付费计划。适用于数据可视化、API 代理 Space、小型 CPU 密集模型。

**专用 GPU**（T4、L4、A10G、L40S、A100、H200）—— 按小时计费给 Space 创建者。列表与定价：`hf spaces hardware`。只有创建者可以挂载这些硬件，且前提是 `canPay=True`。当 ZeroGPU 确实不适用时使用 —— 例如主模型为非 PyTorch 且初始化开销大、超大模型的长上下文推理等。

如果用户需要无法支付的硬件 —— 专用 GPU，或超出免费 2 个 ZeroGPU 上限的 Gradio Space —— 他们仍可以创建一个**Static** Space（对所有人免费），把应用推送上去，并申请社区资助。详见 [`references/grants.md`](references/grants.md)。

权威参考：https://huggingface.co/docs/hub/spaces-overview

## 2. 先查找现有的演示

在决定如何构建任何东西之前，先搜索已有的实现：

```bash
hf spaces search "<model name or task>" --sdk gradio --limit 10
```

如果有人已经构建了类似的 Space，阅读它的 `app.py` 和 `requirements.txt` —— 这会给你一个可用的模式，节省大量盲目迭代的时间。在确定方案之前，把你的发现告诉用户。

## 3. 确定 SDK 和硬件

首先遵循用户的明确要求。如果他们的要求比较含糊：

- **公开 ML 演示的默认选择**：Gradio + ZeroGPU。除非下面的情况适用，否则使用这个。
- **模型唯一的推理路径是非 PyTorch**（ONNX / TF / JAX / vLLM 作为主模型，初始化开销很大）：使用专用 GPU。
  - 但是：torch 主流程中少量非 torch 的工具（一个小型 ONNX 预处理器、一个 TF 工具）在 ZeroGPU 上没问题。劫持（hijack）只打补丁给 torch；在 `@spaces.GPU` 内部初始化非 torch 库，并承担每次调用较短的初始化开销。
- **微小 / CPU 密集模型，或 API 代理 Space**：使用 `cpu-basic` —— 但它需要付费计划。在免费账户上，把它放在 `zero-a10g` 上，用一个空操作（no-op）的被装饰函数（ZeroGPU 需要至少一个），并把真正的工作放在它之外 —— 这样永远不会真正请求 GPU，也就不会消耗配额。参见 [`references/inference-providers.md`](references/inference-providers.md)。
- **浏览器端 ML 或项目主页**：使用 Static。
- **非 Python 技术栈的容器**：使用 Docker。

### 寻找模型来源

- **GitHub 仓库** —— 克隆到本地阅读结构。如果已经有 Gradio 演示，最小可行路径是将其改造以适配 ZeroGPU（见 [`references/zerogpu.md`](references/zerogpu.md)）。否则：阅读 README 和推理代码，优先选择 PyTorch 路径，估算显存（bf16 ≈ `params_B × 2` GB；48 GB 可容纳 ≤24B 参数的 bf16 模型，量化后可容纳更大模型 —— 关于 ZeroGPU 上的量化见 [`references/zerogpu.md`](references/zerogpu.md)）。
- **HF 模型仓库** —— 阅读其 README，跟进任何链接的 GitHub。
- **论文 / 博客文章** —— 寻找官方或非官方实现。除非实现很简单或用户明确要求，否则不要自己重新实现。
- **模糊的请求** —— 先搜索 Spaces；呈现搜索结果。

如果模型确实放不下，可以考虑**推理提供方（Inference Providers）**作为替代方案：参见 [`references/inference-providers.md`](references/inference-providers.md)。这样可以完全避免托管模型。

## 4. 创建 Space

```bash
hf repos create <namespace>/<name> --type space --space-sdk <gradio|docker|static> \
    [--flavor zero-a10g|cpu-basic|<paid-flavor>] \
    [--secrets KEY=val] [--env KEY=val] \
    --public|--private|--protected \
    --exist-ok
```

- `--space-sdk` 是必需的。
- `--flavor` 选择硬件。`zero-a10g` 是 ZeroGPU 的（旧式）标识符。省略它会得到 `cpu-basic` —— 这本身也需要付费计划，所以在免费账户上要显式传入 `--flavor zero-a10g`。运行 `hf spaces hardware` 查看完整的付费列表与定价。
- 可见性：`--public`（任何人可查看）、`--private`（仅你本人）、`--protected`（应用可访问，但 git 仓库 / Files 标签页是私有的）。
- `--secrets KEY=val` 会成为 Space 内部的环境变量，访问者**看不到**。用于 API 密钥、受限仓库的 token（`HF_TOKEN=hf_…`）等。也可以稍后通过 `hf spaces secrets set <id> KEY=val` 设置。
- `--env KEY=val` **对访问者可见** —— 仅用于非敏感配置（`GRADIO_SSR_MODE=false`、`PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` 等）。

> 注意：README YAML 中的 `hardware:` 会被静默忽略 —— 硬件只能在创建时通过 `--flavor` 设置，或之后通过 `hf spaces settings <id> --hardware <name>` 设置。

## 5. 构建应用

Space 现已存在于 `https://huggingface.co/spaces/<namespace>/<name>`，但是空的。

### README.md 的 frontmatter

始终必需：

```yaml
---
title: ...
emoji: 🚀                # 选一个有代表性的
colorFrom: blue          # red|yellow|green|blue|indigo|purple|pink|gray（只能用这些）
colorTo: indigo
sdk: gradio              # gradio | docker | static
sdk_version: 6.15.1      # 除非有理由，否则使用最新稳定版*
app_file: app.py         # 仅 gradio 需要（docker / static 使用 Dockerfile / index.html）
short_description: ...   # ≤ 60 字符（服务器会拒绝超长的）
python_version: "3.12"   # ZeroGPU 官方支持 3.10.13 和 3.12.12
startup_duration_timeout: 30m   # 默认值；大型 LLM / 繁重下载时可调到 1h
---
```

\* 默认使用当前最新的稳定版，并**查清楚那是什么版本**（`pip index versions gradio`，或新创建的 Space 默认采用的版本）—— 上面的数字只是一个会过时的占位符，不要照搬。只有在最新版本确实对该 Space 不适用时才锚定旧版本：某个自定义组件锚定了它，或者你在适配一个现有演示而不想为 5.x→6.x 的破坏性变更重写代码。如果需要 5.x 版本，选 `5.50.0`（该系列的最新版，仍支持自定义组件）。

所有 frontmatter 选项：https://huggingface.co/docs/hub/spaces-config-reference

### 最简的 ZeroGPU Gradio 应用

```python
import spaces           # 必须在 torch / diffusers / transformers 之前导入
import torch
import gradio as gr
from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained("<repo>", torch_dtype=torch.bfloat16).to("cuda")

@spaces.GPU(duration=60)
def generate(prompt: str):
    """Generate an image from a text prompt."""   # docstring → API / MCP 工具描述
    return pipe(prompt).images[0]

gr.Interface(fn=generate, inputs=gr.Text(), outputs=gr.Image()).launch(mcp_server=True)
```

三条规则 —— 完整说明见 [`references/zerogpu.md`](references/zerogpu.md)：

1. **`import spaces` 必须在 torch / 任何涉及 CUDA 的导入之前。** 它会对 `torch.cuda.*` 做猴子补丁（monkey-patch）；一旦主进程中 CUDA 已被初始化，就为时已晚。
2. **在模块级别加载模型，急切地 `.to("cuda")`。** ZeroGPU 会拦截该调用，将权重打包到磁盘，并在首次进入 `@spaces.GPU` 时将它们流式加载进显存。在装饰器内部延迟加载会让每个用户都承担这个开销。
3. **装饰 Gradio 绑定的那个函数。** 将 `duration` 估计为实际的最坏情况（越小意味着更高的队列优先级和更严格的配额检查）。对于运行时长取决于输入的情况，传入一个可调用对象。

### 示例、docstring 与 MCP

- **只要合理就添加 `gr.Examples`**（应用接受输入，且存在有代表性的输入）—— 优先使用模型/仓库自带的官方示例。示例行只保留用户实际会改动的少数输入（prompt、image），其余参数（steps、seed、guidance）在处理函数里给默认值，这样一行示例是 `["a prompt"]`，而不是一堆旋钮。使用 `cache_examples=True, cache_mode="lazy"`。参见 [`references/gradio.md`](references/gradio.md)。
- **为每个通过 API 触发的函数编写 docstring 和类型提示。** 每个 Gradio 事件处理函数都会通过 API 暴露；docstring + 函数签名正是调用方 —— 以及 MCP 工具 schema —— 所看到的内容。
- **用 `demo.launch(mcp_server=True)` 启动**（Gradio 5+），这样 Space 就同时充当 MCP 服务器：每个 API 函数都会成为一个由其 docstring 和类型提示描述的 MCP 工具。

### requirements.txt

简要说明：

- **不要列出**：`gradio`、`spaces`、`huggingface_hub`（已预装且由平台管理；锚定它们的版本会导致依赖解析失败或悄悄破坏 ZeroGPU 运行时）。
- **如果用到了就要列出**：`torchvision`、`torchaudio`（未预装），以及其他所有依赖（`diffusers`、`transformers`、`accelerate`、`sentencepiece` 等）。
- ZeroGPU 只接受 torch `2.8.0`、`2.9.1`、`2.10.0`、`2.11.0`。默认不锚定 torch 版本（运行时会预装最新版）。只有当某个依赖强制要求时才锚定。
- 对于预构建的 CUDA 扩展 wheel（`flash_attn`、`xformers`、`pytorch3d`、`nvdiffrast`、`diff_gaussian_rasterization`、`torchmcubes`）：使用 `https://huggingface.co/datasets/multimodalart/zerogpu-blackwell-wheels/tree/main/wheels` 上预构建的 Blackwell wheel。完整映射与注意事项见 [`references/requirements.md`](references/requirements.md)。

### 各 SDK 的深入细节

- **Gradio 模式**（主题、`gr.Examples`、流式输出、自定义 HTML 组件、`gr.Server`）：[`references/gradio.md`](references/gradio.md)。
- **Docker**：https://huggingface.co/docs/hub/spaces-sdks-docker。示例：`hf spaces list --filter docker`。
- **Static**：https://huggingface.co/docs/hub/spaces-sdks-static。对于构建型 SPA，在 frontmatter 中设置 `app_build_command: npm run build` 和 `app_file: dist/index.html`。
- **ZeroGPU 细节**（装饰器语义、规格选择、AoTI、生成器、并发、worker 边界上的 pickle / `gr.State`）：[`references/zerogpu.md`](references/zerogpu.md) —— 只要 Space 面向 ZeroGPU，就要阅读此文档。


## 6. 在 Space 上迭代，而非本地

尝试根据用户的需求本地构建一个候选版本并推送上去 —— 然后把线上 URL 当作测试循环。Space 环境才是唯一重要的环境；不要尝试本地测试。推送前值得做的本地检查最多是 `python3 -m py_compile app.py`。

使用 `hf upload <namespace>/<name> . --repo-type space` 推送文件。**`--repo-type space` 是必需的** —— `hf upload` 默认指向*模型*仓库，否则会悄悄上传到（并创建）一个同名的模型仓库。加上 `--exclude "**/__pycache__/**"`，避免把本地字节码缓存提交进 Space。

推送之后，为每种改动选用最低成本的更新机制 —— 纯 Python 编辑用热重载，热重载无法处理的纯代码文件用 `hf upload`，只有当 `requirements.txt` / `Dockerfile` / README frontmatter 确实发生变化时才完全重建。完整的层级与陷阱（热重载污染导致的工厂重启、runtime.sha 延迟等）见 [`references/debugging.md`](references/debugging.md)。

## 7. 验证

不要只信任 `RUNNING` 状态 —— 应用可能正在运行但已损坏。按顺序执行四步：

**A. 存活吗？** 阶段 + 硬件：
```bash
hf spaces info <ns>/<name> --expand runtime
```

**B. 启动后日志干净吗？** 阅读运行日志，确认启动完成且没有警告或静默回退：
```bash
hf spaces logs <ns>/<name> --tail 200
```
留意模型加载完成的提示、没有导入警告、没有"falling back to CPU" / dtype 降级的消息、没有被 `RUNNING` 掩盖的半损坏应用。

**C. API 真的能响应。** 在另一个终端保持日志跟随（`hf spaces logs <ns>/<name> --follow`）的同时，调用接口：
```python
from gradio_client import Client, handle_file
import os
c = Client("<ns>/<name>", token=os.environ["HF_TOKEN"], httpx_kwargs={"timeout": 600})
print(c.view_api())                    # 发现端点 —— 不要猜
result = c.predict(..., api_name="/generate")
```

**D. 嗅探输出和日志。** HTTP 200 不等于输出正确。两者都要检查：
```python
head = open(result, "rb").read(16)
# glTF / \x89PNG / RIFF…WEBP / RIFF…WAVE / [4:8]==b"ftyp" → png/jpg/webp/wav/mp4
```
并查看调用期间产生的运行日志 —— 静默的回退（模型自动改变尺寸、缺少可选依赖、dtype 降级）只会在那里出现。

完整的烟雾测试模式（流式端点、OAuth 门控的 Space、`gr.Server` 自定义路由）：见 [`references/debugging.md`](references/debugging.md)。

## 8. 持久化存储（存储桶）

Space 是无状态的 —— `/data` 在重启时会被清空。如果 Space 需要持久化用户上传、生成内容、日志，或与长期存储交互，请挂载一个**存储桶（bucket）**：

```bash
hf buckets create <ns>/<bucket-name>                                          # --private 可选
hf spaces volumes set <ns>/<space> -v hf://buckets/<ns>/<bucket-name>:/data   # 在 /data 处读写
```

存储桶是付费存储；请检查 `canPay` 并与用户确认。完整模式（读快 / 写持久、公开存储桶 URL、模型缓存的反模式）见 [`references/buckets.md`](references/buckets.md)。

## 9. 当出现问题时

操作顺序：

1. 阅读日志：`hf spaces logs <id> --build --follow`（构建错误）或 `hf spaces logs <id> --follow`（运行时错误）。找到**第一个**错误，而不是最后一个。
2. 在 [`references/known-errors.md`](references/known-errors.md) 中检索该错误字符串。在尝试自己的修复方案之前，先检查这是否是已知问题 —— 大多数常见的 ZeroGPU / Gradio / 依赖错误在那里都有 1-2 行的修复方法。
3. 使用 [`references/debugging.md`](references/debugging.md) 中成本最低的阶梯进行迭代。绝大多数问题通过"读日志 + 烟雾测试"循环就能解决；交互式开发模式 + SSH 是重磅的最后手段。

如果你解决了一个不在已知错误列表中的问题，建议用户把它提交回本技能的 PR，让以后的运行也能受益。

---

## 参考文件索引

| 何时阅读 | 文件 |
|---|---|
| **ZeroGPU 的工作原理**以及正确的模式（装饰器、规格选择、pickle、生成器、实时性、AoTI） | [`references/zerogpu.md`](references/zerogpu.md) |
| **迭代与调试**：日志、阶梯排序、烟雾测试（以及作为最后手段的开发模式 + SSH） | [`references/debugging.md`](references/debugging.md) |
| **错误字符串查询** —— 所有错误症状的唯一入口（Spaces、ZeroGPU、Gradio、依赖） | [`references/known-errors.md`](references/known-errors.md) |
| 锚定依赖、选择 wheel、torch 系列版本对齐 | [`references/requirements.md`](references/requirements.md) |
| `gr.Examples`（在合适时添加）、主题、自定义 HTML 组件、`gr.Server`、MCP 服务器（`mcp_server=True`） | [`references/gradio.md`](references/gradio.md) |
| 持久化存储、公开存储桶 URL | [`references/buckets.md`](references/buckets.md) |
| 社区资助申请（用户无法支付的硬件） | [`references/grants.md`](references/grants.md) |
| 提供方代理（通过 Cerebras / Fireworks / Together 等实现零显存的大型 LLM） | [`references/inference-providers.md`](references/inference-providers.md) |
| **3D Space：生成、CUDA 扩展、输出格式与模型配方（包括高斯溅射）** | [`references/3d-generation.md`](references/3d-generation.md) |
