---
name: huggingface-lora-space-builder
description: 为用户提供的 LoRA 构建并发布 Hugging Face Spaces 上的 Gradio 演示。当有人要求为某个 LoRA 创建、生成、交付或发布 Space、演示（demo）、Gradio 应用或体验场（playground）时使用——包括基于 Qwen-Image、Qwen-Image-Edit、LTX-Video、Wan、FLUX、SDXL 或其他扩散基础模型的 LoRA。当有人描述自己训练或托管在 Hub 上的 LoRA 并希望分享它时也会触发。涵盖选择合适的基础管线和 `diffusers` 推理方案、根据 LoRA 的任务和输入（Union/多任务控制、编辑、视频、图像等）量身设计 UI、遵循模型卡中的推荐设置（触发词、步数、引导系数、LoRA 缩放、示例输入），以及默认以私有 Space 形式发布到 ZeroGPU 硬件上。
---

# Gradio LoRA Space 构建器

构建并发布一个 Hugging Face Spaces 上的 Gradio 演示，使用用户提供的 LoRA 运行推理。每当有人要求为某个 LoRA 创建、生成、交付或发布"一个 Space"、"一个演示"、"一个 Gradio 应用"或"一个体验场"时使用——无论基础模型是 Qwen-Image、Qwen-Image-Edit、LTX 还是其他扩散模型。当有人描述自己训练或托管在 Hub 上的 LoRA 并希望分享它时也应使用。默认目标硬件是 ZeroGPU；当基础模型支持时，默认推理库是 `diffusers`。

产出是一个真实发布的 Space（默认私有），用户可以在浏览器中试用，而不是一个本地脚本。

## 这类演示的"好"标准是什么

演示应该让人感觉是为这个特定 LoRA 精心打造的，而不是一个硬塞进 LoRA 的通用模板。即使两个 LoRA 任务相同，也可能需要不同的演示：姿态控制视频 LoRA 和外扩（outpainting）视频 LoRA 都是输入视频、输出视频，但用户提供的输入、预处理和控件完全不同。识别这一点正是这里的核心工作。

具体来说，一个好的演示：

- 加载快、运行快——尽量少的模型加载、合理的步数、每次调用不浪费计算。
- UI 只包含该 LoRA 需要的控件，别无其他。多余的滑块是成本，而不是功能。
- 向用户展示正在发生的事情——进度、在有用时展示中间输出、所用的种子、输入缺失时给出清晰的错误。
- 遵循 LoRA 模型卡中自身的推荐：触发词、推荐步数、推荐引导系数、推荐 LoRA 缩放、示例输入。
- 在创意有帮助的地方发挥创意——交互式画布、前后对比滑块、中间处理结果的并排预览——在朴素更合适的地方保持朴素。

## 工作流程

按顺序完成以下阶段。一个阶段中收集到的信息决定下一阶段。

1. 收集选择管线和设计 UI 所需的 LoRA 信息。
2. 选择基础管线和推理方案。
3. 为这个特定 LoRA 的任务和输入设计 UI。
4. 一起编写 `app.py`、`requirements.txt` 和 `README.md`；将三者一并展示给用户，进行一次性批量审批。
5. 发布 Space（私有）。

不要跨多轮零散地提问。把问题集中在一起问。

---

## 阶段 1 — 收集 LoRA 信息

必需：Hub 上的一个 LoRA 仓库（例如 `username/my-lora`）。

**首先，尝试在不使用令牌的情况下读取仓库。** 如果成功，说明仓库是公开的——继续。如果因 401/403 失败，说明仓库是私有/受限（gated）的，你需要一个已认证的会话来读取它。**不要立即索要令牌。** 先检查用户是否已经认证。

```python
from huggingface_hub import HfApi, get_token

cached_token = get_token()  # 读取 HF_TOKEN 环境变量或缓存的 CLI 登录
if cached_token:
    try:
        info = HfApi().whoami(token=cached_token)
        username = info["name"]
        # 如适用，info 还包含细粒度令牌的权限范围信息
    except Exception:
        cached_token = None  # 令牌存在但无效/已过期
```

然后：

- 如果存在有效的缓存令牌，*并且*它能读取该仓库，就使用它。无需提示。
- 如果没有缓存令牌，或缓存令牌无法读取这个私有仓库，向用户索要令牌——只问一次，并附上以下说明。

索要令牌时（且仅在确实需要索要时）：

> 我需要一个具有 **write** 权限范围的 Hugging Face 访问令牌（用于在 LoRA 为私有/受限时读取它，以及发布 Space）。请在 https://huggingface.co/settings/tokens 创建一个，然后粘贴到这里。

同一个令牌将在最后阶段的发布中复用，所以这只需要问一次。

**然后读取仓库中的内容：**

- 列出仓库文件（`huggingface_hub.HfApi().list_repo_files(repo_id)`）。查找 `.safetensors`、`README.md`、示例图像/视频、多个检查点。
- 获取模型卡（`huggingface_hub.ModelCard.load(repo_id)`）。`data` 字典包含结构化字段；`text` 包含 README 正文。
- 如果存在多个 `.safetensors` 文件，选择正确的那个——参见 `references/zerogpu-and-publishing.md` 中的"Picking the LoRA weights file"。简而言之：README 推荐的文件优先，其次是 `pytorch_lora_weights.safetensors`，再次是最新的训练检查点，否则询问用户。

**尝试从模型卡中确定：**

- **基础模型**——`base_model` 字段，或 README 中的文字提及。通常都会有。用它来选择管线参考文件（见阶段 2）。
- **任务**——如果设置了 `pipeline_tag` 就用它，否则根据基础模型和 README 文字推断。本技能处理的五种任务：`text-to-image`、`image-to-image`、`text-to-video`、`image-to-video`、`video-to-video`。
- **触发词**——常被称为"trigger word"、"instance prompt"、"activation word"；有时嵌在示例提示词中。
- **推荐推理方案**——步数、引导系数、true CFG 系数、LoRA 缩放、分辨率。许多 LoRA 卡片包含一段 Python 代码片段；信任其中的*参数*（步数、引导、CFG、LoRA 缩放、dtype）。关于*加载机制*，参见 `adapting-to-the-lora.md`——优先使用 `pipe.load_lora_weights(...)`，而不是代码片段中使用的任何加载方式。
- **示例提示词和示例媒体**——将它们用作 UI 中的 Gradio 示例。
- **子任务/具体用例**——对于图像编辑和视频 LoRA，"这个 LoRA 实际上做什么"与任务类别同样重要。重新打光（relighting）LoRA、换脸 LoRA 和风格 LoRA 可能都是 image-to-image，但每个的 UI 都不同。

**当某些信息无法推断时，询问用户——只问一次，放在一条批量消息中。** 把问题设计得让回答尽可能简单。对于任务类别，将五个选项列为编号选项。对于子任务，给出一行描述（"这个 LoRA 做什么？例如'为人像重新打光'、'应用漫画风格'、'将视频扩展到更宽的宽高比'"）。如果你已经能从基础模型或 README 中有把握地推断出来，就不要问。

如果模型卡完全没有有用信息——没有基础模型、没有任务、没有示例——要明确指出："模型卡中没有可用信息。我需要你告诉我：(1) 基础模型，(2) 这个 LoRA 做什么，(3) 如果你知道的话，推荐的步数和引导系数。"

---

## 阶段 2 — 选择基础管线

这里需要决定两件事：加载哪个参考文件，以及使用哪个管线类。这不是同一个问题——一个基础模型家族文件（例如 `qwen-image.md`）涵盖多个变体，而同一家族中的变体并不总是共享同一个管线类。如果弄错，Space 可以加载但会产生错误的输出，或者在启动时失败。

**步骤 1 — 加载该基础模型家族的参考文件。**

- `references/base-models/qwen-image.md` — 涵盖 Qwen-Image 和 Qwen-Image-Edit 家族（text-to-image 和 image-to-image）。
- `references/base-models/ltx.md` — 涵盖 LTX 家族（text-to-video、image-to-video、video-to-video，包括 IC-LoRA）。
- `references/base-models/krea-2.md` — 涵盖 Krea 2（K2），text-to-image（在 RAW 上训练，在 Turbo 蒸馏检查点上运行推理/LoRA）。

如果基础模型不在这些文件中，说明本技能尚未对其提供一等支持。告诉用户，并询问他们是希望通过类比继续（使用最接近模型的方案并加以调整）还是停止。不要悄悄猜测。

**步骤 2 — 对照基础模型自己的模型卡核实管线类。此步骤是强制的，不是可选的。**

一个新的基础模型变体可能使用相同的管线类但仓库路径不同，也可能使用一个全新的管线类。不要只信任参考文件中的表格——它是尽力而为的，可能滞后于最近的发布。在确定之前先核实：

```python
from huggingface_hub import ModelCard
base_card = ModelCard.load(base_model_id)
# 阅读 base_card.text——找到 diffusers 推理代码片段，记下它导入的管线类。
```

基础模型卡中 diffusers 代码片段所导入的类就是事实来源。以下是这一点很重要的真实例子：

- `Qwen-Image-Edit` 使用 `QwenImageEditPipeline`。`Qwen-Image-Edit-2509` 和 `Qwen-Image-Edit-2511` 使用 `QwenImageEditPlusPipeline`——不同的类、不同的默认参数，接收的是图像列表而非单张图像。一个面向 2511 的 LoRA 加载到 `QwenImageEditPipeline` 上会产生损坏的输出。
- LTX-Video 使用 `LTXPipeline`/`LTXImageToVideoPipeline`/`LTXConditionPipeline`。LTX-2 使用来自不同模块路径的 `LTX2Pipeline`。LTX-2.3 有时需要 diffusers 之外的原生管线。

如果基础模型卡中根本没有 diffusers 代码片段，就退回使用参考文件的表格——并告诉用户你在退回使用表格，以防他们知道一些表格中没有的信息。

这种核实的成本是一次 Hub 获取和几秒钟的阅读。跳过它的代价就是上一条所描述的失败模式——一个"能运行"的 Space 却在悄悄使用错误的类。

**步骤 3 — Diffusers 还是原生管线。** 当基础模型有 diffusers 管线类时，默认使用 `diffusers`。Qwen-Image、Qwen-Image-Edit 以及大部分 LTX 都是这种情况。某些 LTX 变体（尤其是搭配某些 IC-LoRA 的 LTX-2.3）需要原生管线；LTX 参考文件会说明何时需要。Diffusers 提供标准的 `load_lora_weights` / `set_adapters` 语义；原生路径则需要特定于 LoRA 的胶水代码。

---

## 阶段 3 — 为这个 LoRA 设计 UI

不要直接套用模板。从 LoRA 的任务和输入出发推导出 UI。

阅读 `references/tasks.md` 了解各任务的基线 UI 模式（T2I、I2I、T2V、I2V、V2V 的标准输入/输出是什么样的）。

然后阅读 `references/adapting-to-the-lora.md`，它讲的是*深入思考这个特定 LoRA 需要什么*——超越任务类别。该文件是本技能中最重要的文件。同一个任务可能需要非常不同的 UI：姿态控制 LTX LoRA 需要视频输入和姿态提取预览；外扩 LTX LoRA 需要宽高比选择器和黑边预览；重新打光 Flux LoRA 需要一张图像和一个画笔画布，用于指示在哪里添加光照。这些都无法简化为"V2V 模板"或"I2I 模板"。

**编写 UI 前的自检。** 写一句话描述用户在 10 秒内用这个 Space 做什么。如果这句话无法把这个 LoRA 与同任务的任何其他 LoRA 区分开来，说明 UI 还不够有针对性。

通过自检的例子：

- "上传一段视频，选择目标宽高比，点击 Generate；模型会填充空白边缘。"
- "在想要光照的地方画上彩色笔触，选择一种照明风格，点击 Generate；模型会为照片重新打光。"
- "上传一段某人运动的视频和一张另一个角色的图像；模型生成该角色做出这些动作的视频。"

未通过自检的例子：

- "输入提示词并点击生成。"（通用 T2I——请说得更具体。）
- "上传一张图像和一条指令。"（通用编辑——什么样的编辑？）

**Gradio 组件的时效性。** Gradio 的组件集在不断演进。在默认使用普通组件之前，考虑是否有更新的组件更合适——例如用于编辑类 LoRA 前后对比的 `gr.ImageSlider`、用于持久化偏好的 `gr.BrowserState`、用于根据输入变化的 UI 的 `@gr.render`。如果你不确定某个组件是否存在或其签名是什么，请通过网络获取 https://www.gradio.app/docs 上的当前 Gradio 文档，而不是猜测。

**当内置组件和 Hub 自定义组件都不够用时——创意模式。** 如果 LoRA 的自然输入是一种没有任何 Gradio 组件（内置或 Hub 上的）能很好表达的形态——点集、笔触、轨迹、带元数据的多区域标注、3D 旋转控件、时间轴拖动条，以及任何用户需要在媒体之上操作某样东西的情况——就降级到通过 `gr.HTML` 使用自定义 HTML/JS。参见 `references/creative-mode.md` 了解 Gradio 原语（`gr.HTML`、`head=` 注入、`elem_id` 寻址、两种 JS↔Python 状态同步方法）、定义 JSON 传输格式的规范以及各种陷阱。不要仅仅因为它很酷就使用创意模式——当 LoRA 的输入形态要求时才使用。并且在完全定制之前，不要跳过上面提到的 Hub 自定义组件这一层（例如 `gradio_image_annotation`）。

**媒体输入类 Space 的 `gr.Examples`。** 当模型自己的仓库中没有合适的示例媒体时，从共享输入池中获取——按模态拆分，以便 HF 数据集查看器能渲染出正确的缩略图：图像在 [`linoyts/repo-to-space-example-inputs`](https://huggingface.co/datasets/linoyts/repo-to-space-example-inputs)，视频在 [`linoyts/repo-to-space-example-videos`](https://huggingface.co/datasets/linoyts/repo-to-space-example-videos)。两者都是 CC0 许可，带有 `categories` + 自然语言 `caption` 元数据，每个数据集的 README 中都有相同的筛选/排序方法。挑选 2–3 个适合该任务的样本，预处理成模型期望的形状，并将副本打包进 Space。设置 `cache_examples=True, cache_mode="lazy"`，这样首次点击时才进行缓存，而不会在构建时运行示例（参见 `references/zerogpu-and-publishing.md`）。

---

## 阶段 4 — 编写 Space 文件

在编写之前，具体地告诉用户将要发生什么——点出实际的文件名。不要说"我会写这三个文件"，而是类似这样：

> "现在我将编写发布 Space 所需的三个文件：**`app.py`**（Gradio 演示和推理代码）、**`requirements.txt`**（Python 依赖）以及 **`README.md`**（Space 配置，包括 ZeroGPU 硬件设置）。然后我会在发布前将三者一并展示给你审阅。"

这能让用户明确知道将要产出什么。不要只说"三个文件"而不点名——那样很含糊，显得对交付物缺乏承诺。

这三个文件紧密耦合：`requirements.txt` 由 `app.py` 导入的内容决定，而 `README.md` 的 YAML 前置元数据设置了必须相互匹配的 SDK 版本、硬件和 Space 标题。一起编写它们，然后在发布前通过**一条批量消息**将三者展示给用户审批。

阅读 `references/zerogpu-and-publishing.md` 了解 ZeroGPU 规则。其中不那么显而易见的几条：

- 模型在模块级别放到 `cuda` 上（而不是在 GPU 函数内部延迟加载）。ZeroGPU 有一个 CUDA 模拟机制，使得这在预分配阶段就能工作，并且模块级放置明显快于延迟放置。
- 运行推理的函数使用 `@spaces.GPU(duration=...)` 装饰。根据任务选择合适的时长——图像生成用短的，视频用长的。
- 不要使用 `torch.compile`——它与 ZeroGPU 的进程模型不兼容。

### `app.py`

由阶段 1–3 中确定的各部分组合而成。不要从模板粘贴。每个部分都应该是因为需要才存在：

- 导入——`gradio as gr`、`torch`、`spaces`、管线类，以及预处理所需的任何东西。
- 常量——`LORA_REPO`、`BASE_MODEL`、推荐步数、引导系数、LoRA 缩放、触发词。
- 模块级模型加载——管线 `from_pretrained`、`.to("cuda")`、`load_lora_weights`。如果 LoRA 仓库是私有的，传入 `token=os.environ["HF_TOKEN"]`。
- 预处理函数（如有）——姿态提取、填充、掩码构建等。CPU 代码可以在模块级别运行；GPU 代码需要放在 `@spaces.GPU` 函数内部。
- 推理函数——使用 `@spaces.GPU(duration=...)` 装饰。校验输入、应用触发词、构建管线关键字参数、返回输出。
- Gradio Blocks——阶段 3 中设计的 UI，连接到推理函数。

需要做对的常见事项：

- 将实际使用的种子与结果一起返回，以便用户能够复现。
- 在推理函数上使用 `gr.Progress(track_tqdm=True)` 可以显示 diffusers 内部的进度条。
- 校验输入——当必需输入缺失时抛出 `gr.Error("Please upload an image first.")`，而不是让管线以难以理解的错误失败。
- 在 `gr.Examples` 上使用 `cache_examples=True, cache_mode="lazy"`——单纯的 `cache_examples=True` 会在构建时运行示例，在 ZeroGPU 上会失败；lazy 模式会把缓存推迟到用户第一次点击时。
- 当 `gr.Examples` 设置了 `fn=` 时，点击一行会**仅**以 `inputs=` 的值按位置调用 `fn`——因此 `fn` 中每个不在 `inputs` 里的参数都需要默认值，否则点击会抛出 `TypeError: missing N required positional arguments`。运行事件连接了所有组件，所以手动测试和冒烟测试都能通过，只有点击示例时才会出错。修复方法：为额外参数设置默认值（保持 `inputs=[prompt]`），或者列出所有输入并提供完整的示例行，或者去掉 `fn`/`outputs`，让点击只是填充字段。

### `requirements.txt`

不要交付一个固定的最小列表然后听天由命。"最小"列表对普通 T2I LoRA 有效，但一旦基础模型带有视觉-语言文本编码器、视频输出或任何非平凡的预处理就会出问题。**根据 Space 实际需要推导出 `requirements.txt`**，按以下顺序：

1. **`app.py` 中每个顶层的非标准库导入。** 如果 `app.py` 执行了 `import cv2`，`requirements.txt` 中就要有 `opencv-python`。如果执行了 `from controlnet_aux import OpenposeDetector`，`requirements.txt` 中就要有 `controlnet-aux`。机械地逐个检查导入。（注意下一段中的排除项——有些导入是运行时内置的，无需列出。）
2. **基础模型参考文件中"Required dependencies"小节所列内容。** 每个基础模型文件都列出了管线会引入的、不那么显而易见的额外依赖——Qwen-Image 需要 `torchvision`（Qwen 2.5-VL 文本编码器），LTX 需要 `imageio[ffmpeg]`（视频导出），等等。全部包含进去。这些依赖无法从导入中发现，因为它们是在加载时被管线组件间接导入的。
3. **LoRA 自己的模型卡中明确提到要安装的内容。** 如果 LoRA 的 README 有自己的 `pip install` 代码块，从中提取依赖。
4. **diffusers/ML 技术栈：** `diffusers`、`transformers`、`accelerate`、`peft`、`safetensors`。默认不固定版本。如果基础模型参考文件指出该模型需要，则将 `diffusers` 改为 `git+https://github.com/huggingface/diffusers`（新发布的模型经常如此——Qwen-Image-Edit-2511 就是当前的一个例子）。

**哪些*不要*列入 `requirements.txt`：**

- **`gradio`**——由 `README.md` 的 YAML 前置元数据中的 `sdk_version:` 字段控制，而不是由 `requirements.txt` 控制。将它列入依赖，好的情况下会被忽略，坏的情况下会与 SDK 产生版本冲突。只在 README 中设置版本。
- **`torch`**——由 Space 运行时提供。仅在需要固定特定版本时才添加（很少见，并且通常意味着其他地方出了问题）。
- **`spaces`**——由 Space 运行时提供。仅在需要固定特定版本时才添加。
- **`huggingface_hub`**——由 Space 运行时提供。仅在需要固定特定版本时才添加。

这四个包在 ZeroGPU 容器中是预装的。仍然列出它们，就是那种"宁可包含也不要遗漏"的本能——这种本能对非基线依赖是对的，但对基线依赖是错的，因为固定版本会与运行时管理的版本冲突。

**其他所有依赖的倾向：不确定时宁可包含也不要遗漏。** Space 实际不使用的包只会让构建稍慢一些。缺失必需的包则会导致启动时崩溃，用户诊断起来要困难得多。这两种代价并不对称——促成这条规则的那次测试失败恰恰就是第二种情况。

**但有两个特定依赖*不能*条件反射式地添加**，因为它们在 ZeroGPU 上经常带来的问题比解决的问题还多：

- `xformers`——绑定到特定的 torch 版本，经常引发冲突。ZeroGPU 运行时附带 torch 2.8+，因此任何固定的 `xformers` 版本都必须支持它。在 Blackwell 上还有一个额外的坑：xformers 的 FA3 调度对硬件的判断有误（FA3 内核仅支持 `sm_90a` 的 Hopper，但调度器的判断条件是 `device_capability >= (9, 0)`，这也会匹配 Blackwell），并在内核启动时以 `CUDA invalid argument` 崩溃。如果一个使用 xformers 注意力的 Space 遇到这个问题，在模块加载时禁用 FA3 调度：

  ```python
  try:
      from xformers.ops.fmha import _set_use_fa3
      _set_use_fa3(False)
  except Exception:
      pass
  ```

  仅在 `app.py` 实际使用 `xformers` 时才包含它。
- `flash-attn`——需要构建步骤，经常安装失败。与 `xformers` 一样有 torch 2.8+ 版本对齐的注意事项。仅在 `app.py` 实际使用时才包含。

**仅在有理由时才固定其他版本**（例如已知的不兼容，或匹配模型卡中的方案）。

### `README.md`

Space 通过 `README.md` 顶部的 YAML 前置元数据进行配置。正是这个前置元数据选择了 ZeroGPU。

```
---
title: <human-readable title>
emoji: 🎨
colorFrom: pink
colorTo: purple
sdk: gradio
sdk_version: <current Gradio version>
app_file: app.py
pinned: false
hardware: zero-a10g
short_description: <one short line for the Space tile, ~60 chars max>
models:
  - <base model repo>
  - <lora repo>
---

# <title>

A short description with links to the LoRA and base model.
```

关键字段：

- `sdk: gradio`——ZeroGPU 必需。
- `sdk_version`——与你编写代码时所针对的 Gradio 版本一致。查找当前版本（`pip index versions gradio`，或查看 https://www.gradio.app），而不是猜测。
- `hardware: zero-a10g`——ZeroGPU 的旧版标识字符串。实际硬件是 NVIDIA RTX Pro 6000 Blackwell，但标识符是 `zero-a10g`。ZeroGPU 对 PRO、Team 和 Enterprise 账户开放；如果用户没有订阅，Space 会退回到 CPU。如果你怀疑用户不是 PRO，请提及这一点。
- `models:`——列出基础模型和 LoRA 仓库。这会启用 Hub 缓存和发现功能。
- `short_description`——显示在 Space 卡片上。**保持简短（约 60 个字符或更少）。** Hub 的 YAML 校验器会以来自 `https://huggingface.co/api/validate-yaml` 的 400 拒绝过长的值，这会在 `create_repo` 或 `upload_file` 期间表现为 `HfHubHTTPError`。服务器端的确切限制没有文档说明，并且可能变化，因此应以卡片可见长度范围为目标，而不是逼近上限。如果确实遇到了 400，修复方法几乎总是缩短这个字段。一句话描述 Space 做什么就足够了——YAML 下方的 README 正文才是写较长内容的地方。

### 一次性批量审批——操作顺序很重要

这里的规范是**先写完全部三个文件，然后在一条消息中一起展示**。而不是"写 app.py → 讨论它 → 写 requirements → 讨论它 → 写 README → 讨论它"。那种节奏即使你没有明确请求审批，也会产生三个审批时刻，因为用户在每个文件之后都被要求作出回应。

具体来说：

1. **连续编写 `app.py`、`requirements.txt` 和 `README.md`，中间不插入任何文字。** 文件之间没有评论。不说"现在我来写下一个"。不在生成每个文件时描述它的作用。只有三个文件，一个接一个。
2. **然后，在一条消息中请求一次性涵盖全部三个文件的审批。** 类似这样："这就是这个 Space——`app.py`（N 行）、`requirements.txt` 和 `README.md`。请审阅并确认发布，或告诉我需要修改什么。"
3. 用户回应一次，涵盖他们想在三个文件中任意修改的内容。

需要避免的：

- 在写完 `app.py` 之后、写其他文件之前，讲解 `app.py` 的结构或设计选择。把评论留到编写前的公告（阶段 4 开头）或三个文件都完成后的那条审批消息中。
- 问"准备好看下一个了吗？"或"要我继续写 requirements 吗？"——这些都是隐性的逐文件审批。
- 内联展示一个文件，然后提出"你准备好后再展示下一个"——同样的陷阱。
- 把三个文件中的任何一个当作可选的或后续的工作。它们是作为一个交付物一起产出的。

如果用户在看到第一个文件后带着反馈或问题打断，这没问题——回应他们——但规则仍然适用：下次产出代码时，一起产出所有剩余文件，而不是一次一个。

---

## 阶段 5 — 发布 Space

使用阶段 1 中的已认证会话。默认设为**私有**，这样用户可以在公开之前先审查 Space。在创建前与用户确认目标用户名："我将发布到 `{username}/{space_name}`——确认吗？"

```python
from huggingface_hub import HfApi, SpaceHardware

api = HfApi(token=hf_token)
username = api.whoami()["name"]
repo_id = f"{username}/{space_name}"

api.create_repo(
    repo_id=repo_id,
    repo_type="space",
    space_sdk="gradio",
    space_hardware=SpaceHardware.ZERO_A10G,
    private=True,
    exist_ok=True,
)

# 上传文件
for path in ["app.py", "requirements.txt", "README.md"]:
    api.upload_file(path_or_fileobj=path, path_in_repo=path,
                    repo_id=repo_id, repo_type="space")
```

如果 LoRA 仓库本身是私有/受限的，Space 在运行时需要令牌来下载 LoRA。将其设置为 Space 密钥（secret）：

```python
api.add_space_secret(repo_id=repo_id, key="HF_TOKEN", value=HF_TOKEN)
```

……并在 `app.py` 中使用 `token=os.environ["HF_TOKEN"]` 加载 LoRA。

**上传后**，在分享之前运行下面的冒烟测试——构建是异步运行的，静默失败（错误的 `weight_name`、缺失依赖、错误的管线类）只会在首次推理时暴露。**冒烟测试通过后**，分享 Space URL（`https://huggingface.co/spaces/{repo_id}`），并告诉用户这个 Space 是私有的——他们需要登录才能查看。注意构建需要几分钟；如果出现任何失败，日志位于 `https://huggingface.co/spaces/{repo_id}/logs/container`。

**发布时失败（构建开始前）：**

- 在 `create_repo` 或 `upload_file` 期间出现**来自 `https://huggingface.co/api/validate-yaml` 的 `HfHubHTTPError: 400 Bad Request`**。README YAML 未通过服务器端校验。到目前为止最常见的原因是 `short_description` 过长；有时是多余的字段或格式错误的值。修复：将 `short_description` 缩短到约 60 个字符后重试。如果缩短后仍未解决，检查字段名的拼写错误或无效值（例如 `colorFrom`/`colorTo` 中不支持的颜色、无效的 `hardware` 字符串）。
- 使用 `space_hardware="zero-a10g"` 时 **`create_repo` 返回 403**：用户不是 PRO/Team/Enterprise，因此无法在创建时申请 ZeroGPU。修复：不带 `space_hardware` 重试 `create_repo`，在 README YAML 中保留 `hardware: zero-a10g`——Space 会在 CPU 上创建。用户随后可以升级到 PRO（自动升级为 ZeroGPU），或申请[社区 GPU 资助](https://huggingface.co/docs/hub/spaces-gpus#community-gpu-grants)（通过 Space 的硬件设置申请）。
- **`upload_file` 返回 401/403**：令牌没有 write 权限范围。修复：向用户索要具有 write 权限的令牌。

**常见构建失败（构建开始后）：**

- `load_lora_weights` 中 LoRA `weight_name` 不匹配 → 通过 `list_repo_files` 检查实际文件名。
- 基础模型是受限的，而令牌没有被设置为 Space 密钥。
- 未分配 ZeroGPU（用户不是 PRO）→ Space 退回到 CPU，慢到无法使用。
- Diffusers 版本不识别该管线类 → 在 `requirements.txt` 中固定为 git 版 diffusers。
- 模块加载时缺失依赖 → 参见上面 `requirements.txt` 的推导规则；最常见的情况是间接依赖，例如 Qwen-Image 文本编码器所需的 `torchvision`。

如果构建失败，主动提出读取日志并提出修复方案。

---

## 阶段 6 — 对 Space 进行冒烟测试

在宣布 Space 完成并把 URL 交给用户之前，端到端地运行一次。有几种失败模式（错误的 `weight_name`、错误的管线类、缺失的间接依赖、受限基础模型的令牌问题）都能顺利构建，只在首次推理时才暴露。`gradio` Python 包附带一个 CLI，正好能做这件事——`gradio info` 返回端点签名，`gradio predict` 运行一次真实推理。两者都随 Space 本来就需要的 `gradio` pip 依赖一起提供，因此在任何运行本技能的环境中都可用。

**步骤 1 — 等待构建完成。** `create_repo` 会立即返回，但容器镜像仍在构建中。轮询 `HfApi().get_space_runtime(repo_id).stage`，直到它变为 `RUNNING`：

```python
import time
from huggingface_hub import HfApi
api = HfApi(token=hf_token)
while True:
    stage = api.get_space_runtime(repo_id).stage
    if stage == "RUNNING": break
    if stage in {"BUILD_ERROR", "RUNTIME_ERROR", "CONFIG_ERROR"}:
        raise RuntimeError(f"Build failed: {stage}. Logs: https://huggingface.co/spaces/{repo_id}/logs/container")
    time.sleep(15)
```

如果构建失败，获取容器日志（`https://huggingface.co/spaces/{repo_id}/logs/container`），阅读回溯信息，并提出修复方案。不要对未运行的 Space 执行 `gradio info`——它会挂起或返回 503。

**步骤 2 — 核实端点签名。** `gradio info {repo_id} --token {hf_token}` 返回暴露的端点及其参数类型。阅读输出并确认：(a) 端点存在（默认是 `/predict`，但 Blocks 类 Space 通常有一个来自 Python 函数名的自定义名称），(b) 参数顺序与 `app.py` 中声明的一致，(c) 文件类型的参数如预期显示为 `"type": "filepath"`。如果其中任何一项不对，面向用户的 UI 可能看起来仍然正确，但 API 调用会失败——修复后重新上传。

**步骤 3 — 运行一次真实推理。** 选择最轻量的可行输入——LoRA 卡片中最简单的示例，或某个 `gr.Examples` 条目。对于私有 Space 要传入 `--token`。对于文件输入，载荷使用 `{"path": "...", "meta": {"_type": "gradio.FileData"}}`。

```bash
# 文本生成图像：
gradio predict {repo_id} /predict '{"prompt": "...", "aspect_ratio": "1:1", ...}' --token $HF_TOKEN

# 图像生成图像（文件输入）：
gradio predict {repo_id} /predict '{"input_image": {"path": "/tmp/sample.jpg", "meta": {"_type": "gradio.FileData"}}, "prompt": "..."}' --token $HF_TOKEN
```

如果你没有用于 I2I 的本地样本图像，就从 LoRA 仓库（`hf_hub_download(repo_id, filename="example.png")`）或基础模型卡中取一张。

**创意模式 Space 的注意事项。** `gradio info` 和 `gradio predict` 只测试 Python 端点——它们无法告诉你 `gr.HTML` 组件中的自定义 JS 是否正常工作。如果 Space 使用了创意模式（参见 `references/creative-mode.md`），在 API 冒烟测试通过后，**在浏览器中打开 Space URL 并验证一次交互**，然后再分享。服务器端正常而 JS 损坏是这类 Space 最常见的失败模式。

**步骤 4 — 解读结果。**

- **成功返回且输出看起来合理** → 完成。分享 URL。
- **HTTPError 503 / "Space is sleeping"** → Space 在步骤 1 和步骤 3 之间休眠了。唤醒它（`api.restart_space(repo_id)`）后重试。
- **推理错误提到 `weight_name` / `safetensors`** → `app.py` 中的 LoRA 文件名与 LoRA 仓库中的实际文件不匹配。重新检查 `list_repo_files`，修正 `weight_name=`，重新上传 `app.py`。
- **推理错误提到缺失的管线类或属性** → diffusers 版本太旧。将 `requirements.txt` 改为 `git+https://github.com/huggingface/diffusers` 并重新上传。
- **模块加载时出现 `ImportError`** → 缺失依赖。将其添加到 `requirements.txt` 并重新上传。运行时日志（`/logs/run`）会指出缺失的包名。
- **OOM（内存不足）** → 降低默认分辨率或步数，或选择更小的基础模型变体。
- **超时/挂起** → 调高 `@spaces.GPU(duration=...)` 并重新上传。

冒烟测试的存在，是为了把这些问题从"用户发现并反馈"转变为"你在分享之前发现并修复"。不要因为构建显示绿色就跳过它——构建通过但推理损坏是具有非平凡管线的 Space 最常见的失败模式。

---

## 需要避免的事项

- 通用的"一个演示适用于所有 LoRA"模板。本技能的全部意义就在于量身定制。
- 在 GPU 函数内部延迟加载模型。在 ZeroGPU 上很慢，并且会把启动错误隐藏到第一次请求时。
- `torch.compile`。ZeroGPU 不支持。
- 在 ZeroGPU 上使用不带 `cache_mode="lazy"` 的 `cache_examples=True`。
- `inputs` 未覆盖推理函数必需参数的 `gr.Examples(fn=…)`——构建正常，然后在第一次点击示例时因缺少位置参数错误而崩溃。
- 将 LoRA 权重上传到 Space 仓库中。应在运行时从 LoRA 自己的 Hub 仓库拉取。
- 直到最后才索要 HF 令牌，结果发现 LoRA 一直是私有的，你根本无法读取模型卡。
- 暴露 diffusers 的每一个参数旋钮。为这个 LoRA 挑选最重要的 1–3 个控件。
- Space 发布后在聊天回复中写冗长的开场白。Space URL 就是交付物；收尾要简短。
