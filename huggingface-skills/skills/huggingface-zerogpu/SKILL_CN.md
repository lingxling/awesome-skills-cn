---
name: huggingface-zerogpu
description: 基于 Gradio Spaces 和 Hugging Face Spaces ZeroGPU 的 AI 演示与 GPU 计算。在编写或审查使用 `@spaces.GPU` 的代码、为 ZeroGPU Space 配置 `python_version` 或 `requirements.txt`，或处理 ZeroGPU 特有的代码约束时使用——包括基于 pickle 的进程隔离、`gr.State` 跨 worker 边界的语义、不支持 `torch.compile`（改用 AoTI）、仅支持 CUDA wheel 的构建（构建时和运行时均无 `nvcc`）、large 与 xlarge 规格选择，以及动态 duration 可调用对象。只要用户提到 ZeroGPU、`@spaces.GPU` 或 `spaces` Python 包，或遇到 ZeroGPU 特有的代码错误（例如跨 worker 边界的 `PicklingError`、`illegal duration` 或 `flash-attn` wheel 构建失败），即使用户没有明确要求 ZeroGPU 编码指导，也务必使用本技能。在代码中出现 `import spaces` 或 `@spaces.GPU` 时触发。
---

# Hugging Face ZeroGPU

在使用 **ZeroGPU** 硬件的 Hugging Face Spaces 上构建 ML 演示的规则和模式。涵盖 `@spaces.GPU`、duration 与配额调优、进程隔离、CUDA 可用性模型、并发安全以及 CUDA 构建约束。

## 适用范围

本技能适用于**使用 ZeroGPU 硬件的 Gradio SDK Spaces**。Docker 和 Static Spaces 无法调度到 ZeroGPU 上，而 Streamlit 应用现在以 Docker Spaces 形式运行——因此本技能仅适用于 Gradio。关于一般的 Gradio 编码（组件、布局、事件监听器），请参阅本仓库中的 `huggingface-gradio` 技能。权威的 ZeroGPU 文档位于 https://huggingface.co/docs/hub/spaces-zerogpu ——请参考它来了解当前的后端 GPU、运行时版本列表和层级阈值，这些都会随时间变化。

## 参考文件

| 参考文件 | 何时阅读 |
|-----------|--------------|
| `references/concurrency.md` | 编写 ZeroGPU 代码时始终与 SKILL.md 一起阅读——处理函数默认并行运行 |
| `references/how-zerogpu-works.md` | 在推理冷启动、worker 复用、为什么模块作用域的预热不会延续到请求，或为什么返回 CUDA 张量会挂起时阅读 |
| `references/how-quota-works.md` | 在选择 `duration` 值、调试 `illegal duration` 与 `quota exceeded` 错误，或解释为什么默认 60s 会阻塞短任务时阅读 |
| `references/cuda-and-deps.md` | 在安装依赖 CUDA 的包（例如 `flash-attn`）、固定 torch 配套包版本，或解读 wheel 文件名标签时阅读 |

## 硬件

ZeroGPU 提供两种 GPU 规格，分别对应后端显卡的一部分：

| `size` | 后端 GPU 的份额 | 配额消耗 |
|--------|----------------------|------------|
| `large` *（默认）* | 一半 | 1x |
| `xlarge` | 完整 | 2x |

默认的 `large` 提供半张物理 GPU，因此内存带宽和算力明显低于整卡规格。只有当工作负载确实需要额外的显存或算力时才使用 `xlarge`。

> **后端 GPU 会在不另行通知的情况下变更。** ZeroGPU 已经多次跨 GPU 代际迁移；较早的文章可能会提到 A100 或 H200，但这些都已过时。在为工作负载选择规格之前，请务必查阅 [ZeroGPU 文档](https://huggingface.co/docs/hub/spaces-zerogpu) 以了解当前的后端 GPU 和各规格的确切显存。

## 基本模式

```python
import spaces
import torch
from transformers import pipeline

pipe = pipeline("text-generation", model="...", device="cuda")

@spaces.GPU
def generate(prompt: str) -> str:
    return pipe(prompt, max_new_tokens=100)[0]["generated_text"]
```

关键规则：

1. **在模块作用域实例化模型**，并立即调用 `.to("cuda")`。ZeroGPU 会透明地处理实际的设备映射（参见下文的 CUDA 可用性模型）。
2. **用 `@spaces.GPU` 装饰 GPU 函数**。该装饰器在 ZeroGPU 之外是空操作，因此可以安全地在所有环境中保留。
3. **将 `duration` 设置为符合实际的最坏情况工作负载**（默认 60s）。平台会将 `requested duration` 与用户的 `remaining quota` 进行预检查——而不是与实际运行时间比较——因此一个保留默认 60s 的 10 秒任务，一旦用户剩余配额低于 60s 就会以 `quota exceeded` 失败。较小的声明 `duration` 在节点级队列中的排名也更靠前。参见下文的“Duration 与配额”。
4. **不支持 `torch.compile`。** 请改用 PyTorch [提前编译（AoTI）](https://huggingface.co/blog/zerogpu-aoti)（torch 2.8+）。
5. **谨慎使用 `size="xlarge"`。** 它会分配完整的后端 GPU，但消耗 2 倍配额，并且排队时间往往更长。

```python
@spaces.GPU(duration=120)
def generate_image(prompt: str):
    return pipe(prompt).images[0]
```

## CUDA 可用性模型

真实的 GPU 访问**只**在被 `@spaces.GPU` 装饰的函数内部可用。在这些函数之外，GPU 并未连接到进程。

但是，`import spaces` 会**对 `torch` 进行猴子补丁（monkey-patch）**，使得：

- `torch.cuda.is_available()` 在全局返回 `True`。
- 模块作用域中的 `.to("cuda")` / `device="cuda"` 调用可以成功执行而不报错。

这是有意为之。模块作用域的 `model.to("cuda")` 调用会向 ZeroGPU 后端注册张量，后端在启动时的“打包（pack）”步骤将其写入磁盘卸载目录，并释放相应的内存。当一个 `@spaces.GPU` 调用到来时，派生出的 GPU worker 进程通过锁页内存（pinned-memory）流水线将这些权重从磁盘流式加载到显存。热 worker（在同一 GPU 槽位上跨请求复用）会让权重常驻 GPU，从而跳过磁盘 → 显存这一步。面向用户的规则是：在模块作用域写 `device="cuda"` 即可正常工作——完整生命周期请参见 `references/how-zerogpu-works.md`。

| 操作 | 位置 | 原因 |
|--------|-------|-----|
| `model.to("cuda")` / `pipe(..., device="cuda")` | **模块作用域** | ZeroGPU 注册张量并管理设备迁移 |
| 实际的 CUDA 计算（推理等） | **在 `@spaces.GPU` 内部** | 真实 GPU 只在被装饰的调用期间连接 |
| 根据 `torch.cuda.is_available()` 进行分支 | 避免依赖它 | 由于猴子补丁，它总是返回 `True` |

不要在模块作用域运行推理或 CUDA 内核——真实 GPU 并未连接，因此操作要么静默地在 CPU 上运行，要么失败。

### 设备选择惯用写法仍然有效

在 ZeroGPU 下，标准惯用写法仍然正确：

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModel.from_pretrained("...").to(device)
```

- **ZeroGPU** —— `is_available()` 为 `True`（被猴子补丁修改），因此模型会被注册以进行自动设备迁移。
- **专用 GPU Spaces / 本地 GPU** —— `is_available()` 确实为 `True`。
- **CPU Spaces / 本地 CPU** —— 解析为 `"cpu"`。

不要硬编码 `device="cuda"`——它在仅有 CPU 的环境中会出错。

### 立即加载是正确的默认做法

在模块作用域加载模型，而不是在首次请求时延迟加载。Space 进程会在任何用户到来之前启动，因此冷启动成本只需支付一次。延迟加载（`global model; if model is None: ...`、`@lru_cache` 包装器、在首次调用时实例化的工厂函数）只会把这一成本推给第一个用户。

## 本地开发：直接安装 `spaces`

**不要**把 `import spaces` 包在 `try/except` 中，并为本地运行将 `spaces.GPU` 重新定义为空操作回退。在 ZeroGPU 之外，`spaces` 包本身就已经是真正的空操作：

- 重量级行为（CUDA 猴子补丁、客户端初始化、启动钩子）受 `SPACES_ZERO_GPU` 环境变量控制，该变量只在 ZeroGPU 上设置。
- 在 ZeroGPU 之外，`@spaces.GPU` 会原样返回未装饰的函数。
- 顶层的 `import spaces` 只执行轻量级导入。

Gradio SDK 基础镜像在每个硬件层级上都会安装 `spaces`。因此，即使将 Space 复制到专用 GPU（T4、L4、A10G 等）或 CPU basic 上，也无需修改代码——`import spaces` 仍然成功，`@spaces.GPU` 会变为透明的直通。

### 反模式

```python
try:
    import spaces
except ImportError:
    class spaces:  # type: ignore
        @staticmethod
        def GPU(func=None, **kwargs):
            return func if func else (lambda f: f)
```

问题：

1. 该回退必须模仿 `@spaces.GPU` 的每一种调用形式——裸装饰器、`duration=...`、`size=...`、生成器、`aoti_*` 辅助函数——并且会随着 `spaces` API 的扩展而逐渐偏离。
2. 它把 `spaces` 从 `requirements.txt` 中隐藏了，尽管 Space 在部署时需要它。
3. 它解决的是一个不存在的问题：真实的包在本地已经是空操作。

### 应当这样做

将 `spaces` 添加到依赖中，并无条件地导入它：

```python
import spaces

@spaces.GPU
def generate(prompt: str) -> str:
    ...
```

## Duration 与配额

当你声明 `@spaces.GPU(duration=N)` 时，会发生三件事：

1. **层级上限检查** —— 每个访客层级都有单次调用的 `duration` 上限。声明的 `duration` 超过上限会立即以 `ZeroGPU illegal duration` 失败，与剩余配额无关。（层级数值会随时间变化——参见 [ZeroGPU 文档](https://huggingface.co/docs/hub/spaces-zerogpu)。）
2. **配额预检查** —— 平台将 `requested duration` 与用户的 `remaining quota` 进行比较。如果 `remaining < requested`，调用会以 `ZeroGPU quota exceeded` 失败——即使实际工作本可以放得下。错误消息会显示明确的数字，例如 `"60s requested vs. 30s left"`。因此，一个保留默认 60s 的 10 秒任务，一旦用户的剩余配额低于 60s，就会阻塞该用户。
3. **队列优先级** —— 队列是节点级的（同一节点上所有 Spaces 的请求竞争 GPU 槽位），声明的 `duration` 越短，排名越靠前。

这三点都倾向于声明最小的符合实际的 `duration`——包括对于短任务。对一个 10 秒任务显式声明 `@spaces.GPU(duration=15)`，可以避免过早的 `quota exceeded` 拒绝，并在队列中排名更靠前。

> **`xlarge` 会使请求翻倍。** 当 `size="xlarge"` 时，`requested = N * 2`，这同时适用于层级上限检查和配额预检查。因此 `@spaces.GPU(duration=60, size="xlarge")` 在内部是一个 120s 的请求。

### 针对可变工作负载的动态 duration

对于运行时间取决于输入的工作负载，传入一个按请求进行估算的可调用对象。静态的高 `duration` 会把低层级用户拒之门外（他们的层级上限可能小于该静态值），并为轻量输入不必要地预留配额。

```python
def estimate_duration(prompt, steps):
    return int(steps * 3.5)

@spaces.GPU(duration=estimate_duration)
def generate(prompt, steps):
    return pipe(prompt, num_inference_steps=steps).images[0]
```

关于 `illegal duration` 与 `quota exceeded` 的完整区别、每日运行次数限制、24 小时配额窗口以及按量付费计费，请参见 `references/how-quota-works.md`。

## 进程隔离与 Pickle

被 `@spaces.GPU` 装饰的函数在由 ZeroGPU 调度器管理的**独立进程**中运行。参数和返回值通过 **pickle 序列化**跨越进程边界。

后果：

- **只有可 pickle 的对象**才能传入或返回。打开的文件句柄、数据库连接、锁、lambda 以及闭包中包含不可 pickle 状态的对象都会引发 `PicklingError`。
- **不要直接返回 CUDA 张量。** 在主进程中反序列化 CUDA 张量会触发 `torch.cuda._lazy_init()`，而 ZeroGPU 会阻止它。请先转换到 CPU：返回 `tensor.cpu()` 或 `tensor.cpu().numpy()`。
- CPU 张量、numpy 数组、PIL Image 和普通 Python 对象都可以正常工作。
- 大型对象会带来序列化开销。优先返回轻量的结果（张量、数组、文件路径、base64 字符串），而不是复杂的对象图。

### `gr.State` 跨边界的语义

由于处理函数在独立进程中运行，`gr.State` 的值**在每次 yield 时都会被 pickle**——它们并不是按引用共享的。

- 生成器接收到的是状态的一个**副本**（`id()` 与调用方的不同）。
- 在生成器内部进行的原地修改，在被修改的状态被显式 yield 回去之前，对其他处理函数是**不可见的**。
- 为 `gr.State` 槽位 yield `gr.update()` 会**跳过更新**——其他处理函数继续看到 yield 之前的值。
- 每次返回状态对象的 yield 都会通过 pickle 创建一个**新副本**。

实践指导：

- 在 ZeroGPU 上**不要假设 `gr.State` 具有引用语义**。在生成器中修改状态并期望另一个处理函数看到这些修改的代码，将会静默地使用过时的数据。
- **每个包含 `gr.State` 值的 yield 都会触发一次完整的 pickle 往返。** 对于大型状态（模型会话、帧缓冲区），尽量减少 yield 它的次数——理想情况下只在结束时 yield 一次。在中间的 yield 中为状态槽位使用 `gr.update()`。
- **状态中的 CUDA 张量必须在 yield 之前移动到 CPU**——原因与上文 `torch.cuda._lazy_init()` 的问题相同。

## 并发

在 ZeroGPU 上，处理函数**默认并发运行**。这不是可选开启的。在单用户测试中正常工作的代码，在生产环境中可能会静默地破坏或泄露数据。

三条规则。完整的说明及示例见 `references/concurrency.md`。

1. **不要使用可变的全局状态。** 并发请求会相互覆盖。
2. **不要为输出使用固定的文件路径。** 并发请求会覆盖同一个文件。使用 `tempfile` 生成唯一路径。
3. **只读的全局变量是安全的。** 在启动时加载一次、并且在请求期间只读取的模型对象、分词器和配置是安全的，并且推荐这样做。

## 调用粒度

每次进入 `@spaces.GPU` 函数都会带来不小的成本——跨进程边界的 pickle 往返、worker 预热、CUDA 重新连接，以及重新经过一次节点级队列。在热循环内部调用被装饰的函数会成倍放大这些成本，并增加一种新的失败模式：后面的某次迭代可能无法获取 GPU 槽位，导致整个任务中途停滞。

应装饰拥有该循环的外层函数，而不是每次迭代的 worker：

```python
# 避免 —— N 帧对应 N 次 GPU 进入
def process_video(frames):
    return [process_frame(f) for f in frames]

@spaces.GPU(duration=...)
def process_frame(frame):
    ...

# 推荐 —— 整个视频只进入一次 GPU
@spaces.GPU(duration=...)
def process_video(frames):
    return [process_frame(f) for f in frames]

def process_frame(frame):
    ...
```

如果循环中混合了繁重的 CPU 工作和 GPU 工作，包装整个循环会把这些 CPU 时间计入用户配额。当这一成本较大时，对 GPU 工作进行批处理、让 CPU 预处理/后处理留在装饰器之外，是一种视情况而定的优化——而不是默认做法。

## CUDA 构建约束

HF Spaces 在仅有 CPU 的环境中构建 Docker 镜像。**在 ZeroGPU 上，构建阶段没有 `nvcc`**，因为基础镜像是 `python:3.13`（专用 GPU 的 Spaces 使用 `nvidia/cuda:*-devel-*`，在构建时有 `nvcc`）。因此，一个仅以 sdist 形式分发的依赖 CUDA 的包——例如裸的 `flash-attn`——无法在 ZeroGPU 上通过 `requirements.txt` 安装。只有预构建的 wheel 才能工作。

ZeroGPU 的**运行时**确实提供 `nvcc`，自 2025-07 起从 CUDA devel 镜像挂载到 `/cuda-image`（最初是为了支持 AoTI 而添加的）。这使得在 `@spaces.GPU` 调用内部使用 `torch.export` / AoTI 工作流成为可能。

**结论**：从预构建的 wheel 安装每一个依赖 CUDA 的包。如果 PyPI 上没有可用的 wheel，就在外部构建一个（例如托管在 HF Hub 上）并固定其 URL。对于 `flash-attn`，上游的 releases 页面提供了相当完整的 wheel 矩阵，覆盖了大多数 Python × CUDA × torch 组合。

关于解读 wheel 标签（cxx11 ABI、`cu12torch2.X`、`cp3XX`）、torch 系列配套包的版本漂移以及 kernels-community 回退方案，请参见 `references/cuda-and-deps.md`。

## 示例缓存

`gr.Examples` 的行为取决于环境。具体在 ZeroGPU 上：

- `cache_examples` 默认为 `True`（Spaces 设置了 `GRADIO_CACHE_EXAMPLES=true`）。
- `cache_mode` 默认为 `"lazy"`（Spaces 仅在 ZeroGPU 上设置 `GRADIO_CACHE_MODE=lazy`）。

ZeroGPU 默认使用 `lazy`，因为立即缓存会在应用启动时预先运行每个示例，但 ZeroGPU **在启动时没有连接 GPU**——只有在处理请求时才有。对依赖 GPU 的示例进行立即缓存会在那里失败。

当 `cache_examples=True` 时，`run_on_click` / `run_examples_on_click` 参数会被静默忽略。如果你的应用依赖“点击仅填充”的行为，请显式设置 `cache_examples=False` 以保留该行为。

在本地重现 ZeroGPU 的示例缓存行为：

```bash
GRADIO_CACHE_EXAMPLES=true GRADIO_CACHE_MODE=lazy python app.py
```

## 依赖管理

### 在 README frontmatter 中固定 `python_version`

对于 ZeroGPU，固定 `python_version` **实际上是必需的**。当前运行时默认是 Python 3.10，因此如果本地环境使用 3.11+，在没有显式固定版本的情况下将无法在 Space 上安装。请固定到 ZeroGPU 支持的版本（3.12 是一个合理的默认值）；权威的支持列表位于 [ZeroGPU 文档](https://huggingface.co/docs/hub/spaces-zerogpu) 中——不要硬编码完整列表，请参考文档。

```yaml
# README.md frontmatter
python_version: "3.12"
```

`"3.12"` 和 `"3.12.12"` 两种形式都被接受。

### 不要在 `requirements.txt` 中固定 `spaces`

Space 平台会固定其自身的 `spaces` 版本。`requirements.txt` 中有冲突的固定版本会导致 pip 在构建时解析失败。

> **规则**：不要在 `requirements.txt` 中包含 `spaces`。

如何实现取决于你的工具：

- **手写的 `requirements.txt`**：直接省略 `spaces`。
- **uv**（由 `pyproject.toml` 管理）：在 `pyproject.toml` 中声明 `spaces`，以便 uv 共同解析传递性约束（特别是 `spaces` 所固定的 `psutil`），然后在导出时将其排除：
  ```bash
  uv export --no-hashes --no-dev --no-emit-package spaces -o requirements.txt
  ```
  如果 `pyproject.toml` 中没有 `spaces`，uv 就看不到它的传递性约束，可能会在构建时解析出不兼容的版本。
- **pip-tools**（`pip-compile`）/ **Poetry**：使用等效的排除机制。

### 固定 `torch` 以匹配 wheel 标签

如果你通过直接 URL 安装依赖 CUDA 的 wheel，wheel 文件名中会编码其构建时所针对的 `torch` 主.次版本（例如 `cu12torch2.8`）。在 `requirements.txt` 中固定 `torch==X.Y.Z` 以与之匹配——否则 pip 可能会将 `torch` 解析为不同的版本，导致 Space 在首次导入时失败。详细信息以及 kernels-community 替代方案见 `references/cuda-and-deps.md`。
