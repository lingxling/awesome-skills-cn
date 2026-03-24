---
name: huggingface-vision-trainer
description: 使用 Hugging Face Transformers 在 Hugging Face Jobs 云 GPU 上训练和微调用于目标检测（D-FINE、RT-DETR v2、DETR、YOLOS）、图像分类（timm 模型 — MobileNetV3、MobileViT、ResNet、ViT/DINOv3 — 以及任何 Transformers 分类器）和 SAM/SAM2 分割的视觉模型。涵盖 COCO 格式数据集准备、Albumentations 增强、mAP/mAR 评估、准确率指标、带有 bbox/点提示的 SAM 分割、DiceCE 损失、硬件选择、成本估算、Trackio 监控和 Hub 持久性。当用户提到在 Hugging Face Jobs 上训练目标检测、图像分类、SAM、SAM2、分割、图像抠图、DETR、D-FINE、RT-DETR、ViT、timm、MobileNet、ResNet、边界框模型或微调视觉模型时使用。
---

# Hugging Face Jobs 上的视觉模型训练

在托管云 GPU 上训练目标检测、图像分类和 SAM/SAM2 分割模型。无需本地 GPU 设置—结果自动保存到 Hugging Face Hub。

## 何时使用此技能

当用户想要：
- 在云 GPU 或本地微调目标检测模型（D-FINE、RT-DETR v2、DETR、YOLOS）
- 在云 GPU 或本地微调图像分类模型（timm：MobileNetV3、MobileViT、ResNet、ViT/DINOv3 或任何 Transformers 分类器）
- 使用 bbox 或点提示微调 SAM 或 SAM2 模型进行分割/图像抠图
- 在自定义数据集上训练边界框检测器
- 在自定义数据集上训练图像分类器
- 在带有提示的自定义掩码数据集上训练分割模型
- 在 Hugging Face Jobs 基础设施上运行视觉训练作业
- 确保训练的视觉模型永久保存到 Hub

## 相关技能

- **`hugging-face-jobs`** — 通用 HF Jobs 基础设施：令牌认证、硬件类型、超时管理、成本估算、密钥、环境变量、计划作业和结果持久性。**有关任何非训练特定的 Jobs 问题**（例如，"密钥如何工作？"、"有哪些硬件可用？"、"如何传递令牌？"），请参考 Jobs 技能。
- **`hugging-face-model-trainer`** — 基于 TRL 的语言模型训练（SFT、DPO、GRPO）。使用该技能进行文本/语言模型微调。

## 本地脚本执行

辅助脚本使用 PEP 723 内联依赖。使用 `uv run` 运行它们：
```bash
uv run scripts/dataset_inspector.py --dataset username/dataset-name --split train
uv run scripts/estimate_cost.py --help
```

## 先决条件检查清单

在开始任何训练作业之前，验证：

### 账户和认证
- 具有 [Pro](https://hf.co/pro)、[Team](https://hf.co/enterprise) 或 [Enterprise](https://hf.co/enterprise) 计划的 Hugging Face 账户（Jobs 需要付费计划）
- 已认证登录：使用 `hf_whoami()`（工具）或 `hf auth whoami`（终端）检查
- 令牌具有 **写入** 权限
- **必须在作业密钥中传递令牌** — 有关语法（MCP 工具 vs Python API），请参见下面的指令 #3

### 数据集要求 — 目标检测
- 数据集必须存在于 Hub 上
- 注释必须使用带有 `bbox`、`category`（可选 `area`）子字段的 `objects` 列
- Bbox 可以采用 **xywh (COCO)** 或 **xyxy (Pascal VOC)** 格式 — 自动检测和转换
- 类别可以是 **整数或字符串** — 字符串会自动重新映射为整数 ID
- `image_id` 列是 **可选的** — 如果缺失会自动生成
- **在 GPU 训练前始终验证未知数据集**（见数据集验证部分）

### 数据集要求 — 图像分类
- 数据集必须存在于 Hub 上
- 必须有 **`image` 列**（PIL 图像）和 **`label` 列**（整数类 ID 或字符串）
- 标签列可以是 `ClassLabel` 类型（带名称）或普通整数/字符串 — 字符串会自动重新映射
- 常见列名自动检测：`label`、`labels`、`class`、`fine_label`
- **在 GPU 训练前始终验证未知数据集**（见数据集验证部分）

### 数据集要求 — SAM/SAM2 分割
- 数据集必须存在于 Hub 上
- 必须有 **`image` 列**（PIL 图像）和 **`mask` 列**（二进制真值分割掩码）
- 必须有 **提示** — 要么：
  - 包含 JSON 的 **`prompt` 列**，包含 `{"bbox": [x0,y0,x1,y1]}` 或 `{"point": [x,y]}`
  - 或专用的 **`bbox`** 列，包含 `[x0,y0,x1,y1]` 值
  - 或专用的 **`point`** 列，包含 `[x,y]` 或 `[[x,y],...]` 值
- Bboxes 应该采用 **xyxy** 格式（绝对像素坐标）
- 示例数据集：`merve/MicroMat-mini`（带 bbox 提示的图像抠图）
- **在 GPU 训练前始终验证未知数据集**（见数据集验证部分）

### 关键设置
- **超时必须超过预期训练时间** — 默认 30 分钟太短。请参见指令 #6 了解推荐值。
- **必须启用 Hub 推送** — `push_to_hub=True`，`hub_model_id="username/model-name"`，令牌在 `secrets` 中

## 数据集验证

**在启动 GPU 训练之前验证数据集格式，以防止训练失败的 #1 原因：格式不匹配。**

**始终验证**未知/自定义数据集或任何您之前未训练过的数据集。**跳过** `cppe-5`（训练脚本中的默认值）。

### 运行检查器

**选项 1：通过 HF Jobs（推荐 — 避免本地 SSL/依赖问题）：**
```python
hf_jobs("uv", {
    "script": "path/to/dataset_inspector.py",
    "script_args": ["--dataset", "username/dataset-name", "--split", "train"]
})
```

**选项 2：本地：**
```bash
uv run scripts/dataset_inspector.py --dataset username/dataset-name --split train
```

**选项 3：通过 `HfApi().run_uv_job()`（如果 hf_jobs MCP 不可用）：**
```python
from huggingface_hub import HfApi
api = HfApi()
api.run_uv_job(
    script="scripts/dataset_inspector.py",
    script_args=["--dataset", "username/dataset-name", "--split", "train"],
    flavor="cpu-basic",
    timeout=300,
)
```

### 阅读结果

- **`✓ READY`** — 数据集兼容，直接使用
- **`✗ NEEDS FORMATTING`** — 需要预处理（输出中提供映射代码）

## 自动 Bbox 预处理

目标检测训练脚本 (`scripts/object_detection_training.py`) 自动处理 bbox 格式检测（xyxy→xywh 转换）、bbox 清理、`image_id` 生成、字符串类别→整数重新映射和数据集截断。**无需手动预处理** — 只需确保数据集有 `objects.bbox` 和 `objects.category` 列。

## 训练工作流程

复制此清单并跟踪进度：

```
训练进度：
- [ ] 步骤 1：验证先决条件（账户、令牌、数据集）
- [ ] 步骤 2：验证数据集格式（运行 dataset_inspector.py）
- [ ] 步骤 3：询问用户关于数据集大小和验证分割
- [ ] 步骤 4：准备训练脚本（OD：scripts/object_detection_training.py，IC：scripts/image_classification_training.py，SAM：scripts/sam_segmentation_training.py）
- [ ] 步骤 5：保存脚本本地，提交作业，并报告详细信息
```

**步骤 1：验证先决条件**

按照上面的先决条件清单。

**步骤 2：验证数据集**

在花费 GPU 时间之前运行数据集检查器。参见上面的"数据集验证"部分。

**步骤 3：询问用户偏好**

始终使用带有选项样式格式的 AskUserQuestion 工具：

```python
AskUserQuestion({
    "questions": [
        {
            "question": "您是否想先使用数据子集运行快速测试？",
            "header": "数据集大小",
            "options": [
                {"label": "快速测试运行（10% 的数据）", "description": "更快，更便宜（~30-60 分钟，~$2-5）以验证设置"},
                {"label": "完整数据集（推荐）", "description": "完整训练以获得最佳模型质量"}
            ],
            "multiSelect": false
        },
        {
            "question": "您是否想从训练数据中创建验证分割？",
            "header": "分割数据",
            "options": [
                {"label": "是（推荐）", "description": "自动分割 15% 的训练数据用于验证"},
                {"label": "否", "description": "使用数据集中现有的验证分割"}
            ],
            "multiSelect": false
        },
        {
            "question": "您想使用哪种 GPU 硬件？",
            "header": "硬件类型",
            "options": [
                {"label": "t4-small ($0.40/小时)", "description": "1x T4，16 GB VRAM — 足以支持所有 100M 参数以下的 OD 模型"},
                {"label": "l4x1 ($0.80/小时)", "description": "1x L4，24 GB VRAM — 更大的图像或批量大小有更多余量"},
                {"label": "a10g-large ($1.50/小时)", "description": "1x A10G，24 GB VRAM — 更快的训练，更多 CPU/RAM"},
                {"label": "a100-large ($2.50/小时)", "description": "1x A100，80 GB VRAM — 最快，用于非常大的数据集或图像大小"}
            ],
            "multiSelect": false
        }
    ]
})
```

**步骤 4：准备训练脚本**

对于目标检测，使用 [scripts/object_detection_training.py](scripts/object_detection_training.py) 作为生产就绪模板。对于图像分类，使用 [scripts/image_classification_training.py](scripts/image_classification_training.py)。对于 SAM/SAM2 分割，使用 [scripts/sam_segmentation_training.py](scripts/sam_segmentation_training.py)。所有脚本使用 `HfArgumentParser` — 所有配置通过 `script_args` 中的 CLI 参数传递，而不是通过编辑 Python 变量。有关 timm 模型详细信息，请参见 [references/timm_trainer.md](references/timm_trainer.md)。有关 SAM2 训练详细信息，请参见 [references/finetune_sam2_trainer.md](references/finetune_sam2_trainer.md)。

**步骤 5：保存脚本，提交作业，并报告**

1. **将脚本保存到本地** 工作区根目录的 `submitted_jobs/`（如有需要创建），使用描述性名称，如 `training_<dataset>_<YYYYMMDD_HHMMSS>.py`。告诉用户路径。
2. **提交** 使用 `hf_jobs` MCP 工具（首选）或 `HfApi().run_uv_job()` — 有关两种方法，请参见指令 #1。通过 `script_args` 传递所有配置。
3. **报告** 作业 ID（来自 `.id` 属性）、监控 URL、Trackio 仪表板（`https://huggingface.co/spaces/{username}/trackio`）、预计时间和估计成本。
4. **等待用户** 请求状态检查 — 不要自动轮询。训练作业异步运行，可能需要数小时。

## 关键指令

这些规则防止常见故障。请严格遵循。

### 1. 作业提交：`hf_jobs` MCP 工具 vs Python API

**`hf_jobs()` 是 MCP 工具，不是 Python 函数。** 不要尝试从 `huggingface_hub` 导入它。作为工具调用：

```
hf_jobs("uv", {"script": training_script_content, "flavor": "a10g-large", "timeout": "4h", "secrets": {"HF_TOKEN": "$HF_TOKEN"}})
```

**如果 `hf_jobs` MCP 工具不可用**，直接使用 Python API：

```python
from huggingface_hub import HfApi, get_token
api = HfApi()
job_info = api.run_uv_job(
    script="path/to/training_script.py",  # 文件路径，不是内容
    script_args=["--dataset_name", "cppe-5", ...],
    flavor="a10g-large",
    timeout=14400,  # 秒（4 小时）
    env={"PYTHONUNBUFFERED": "1"},
    secrets={"HF_TOKEN": get_token()},  # 必须使用 get_token()，不是 "$HF_TOKEN"
)
print(f"Job ID: {job_info.id}")
```

**两种方法之间的关键区别：**

| | `hf_jobs` MCP 工具 | `HfApi().run_uv_job()` |
|---|---|---|
| `script` 参数 | Python 代码字符串或 URL（不是本地路径） | `.py` 文件的文件路径（不是内容） |
| 密钥中的令牌 | `"$HF_TOKEN"`（自动替换） | `get_token()`（实际令牌值） |
| 超时格式 | 字符串（`"4h"`） | 秒（`14400`） |

**两种方法的规则：**
- 训练脚本必须包含带有依赖项的 PEP 723 内联元数据
- 不要使用 `image` 或 `command` 参数（这些属于 `run_job()`，不是 `run_uv_job()`）

### 2. 通过作业密钥 + 显式 hub_token 注入进行认证

**作业配置** 必须在密钥中包含令牌 — 语法取决于提交方法（见上表）。

**训练脚本要求：** 当 `push_to_hub=True` 时，Transformers `Trainer` 在 `__init__()` 期间调用 `create_repo(token=self.args.hub_token)`。训练脚本必须在解析参数之后但在创建 `Trainer` 之前将 `HF_TOKEN` 注入 `training_args.hub_token`。模板 `scripts/object_detection_training.py` 已经包含了这个：

```python
hf_token = os.environ.get("HF_TOKEN")
if training_args.push_to_hub and not training_args.hub_token:
    if hf_token:
        training_args.hub_token = hf_token
```

如果您编写自定义脚本，必须在 `Trainer(...)` 调用之前包含此令牌注入。

- 不要在自定义脚本中调用 `login()`，除非复制 `scripts/object_detection_training.py` 中的完整模式
- 不要依赖隐式令牌解析（`hub_token=None`）— 在 Jobs 中不可靠
- 有关完整详细信息，请参见 `hugging-face-jobs` 技能 → *令牌使用指南*

### 3. JobInfo 属性

使用 `.id` 访问作业标识符（不是 `.job_id` 或 `.name` — 这些不存在）：

```python
job_info = api.run_uv_job(...)  # 或 hf_jobs("uv", {...})
job_id = job_info.id  # 正确 — 返回类似 "687fb701029421ae5549d998" 的字符串
```

### 4. 必需的训练标志和 HfArgumentParser 布尔语法

`scripts/object_detection_training.py` 使用 `HfArgumentParser` — 所有配置通过 `script_args` 传递。布尔参数有两种语法：

- **`bool` 字段**（例如 `push_to_hub`、`do_train`）：使用裸标志（`--push_to_hub`）或使用 `--no_` 前缀否定（`--no_remove_unused_columns`）
- **`Optional[bool]` 字段**（例如 `greater_is_better`）：必须传递显式值（`--greater_is_better True`）。裸 `--greater_is_better` 会导致 `error: expected one argument`

目标检测的必需标志：

```
--no_remove_unused_columns          # 必须：保留图像列用于 pixel_values
--no_eval_do_concat_batches         # 必须：图像有不同数量的目标框
--push_to_hub                       # 必须：环境是临时的
--hub_model_id username/model-name
--metric_for_best_model eval_map
--greater_is_better True            # 必须显式传递 "True"（Optional[bool]）
--do_train
--do_eval
```

图像分类的必需标志：

```
--no_remove_unused_columns          # 必须：保留图像列用于 pixel_values
--push_to_hub                       # 必须：环境是临时的
--hub_model_id username/model-name
--metric_for_best_model eval_accuracy
--greater_is_better True            # 必须显式传递 "True"（Optional[bool]）
--do_train
--do_eval
```

SAM/SAM2 分割的必需标志：

```
--remove_unused_columns False       # 必须：保留 input_boxes/input_points
--push_to_hub                       # 必须：环境是临时的
--hub_model_id username/model-name
--do_train
--prompt_type bbox                  # 或 "point"
--dataloader_pin_memory False       # 必须：避免自定义 collator 的 pin_memory 问题
```

### 5. 超时管理

默认 30 分钟对目标检测来说太短。设置最少 2-4 小时。为模型加载、预处理和 Hub 推送添加 30% 的缓冲区。

| 场景 | 超时 |
|----------|---------|
| 快速测试（100-200 图像，5-10 轮） | 1小时 |
| 开发（500-1K 图像，15-20 轮） | 2-3小时 |
| 生产（1K-5K 图像，30 轮） | 4-6小时 |
| 大型数据集（5K+ 图像） | 6-12小时 |

### 6. Trackio 监控

Trackio 在目标检测训练脚本中 **始终启用** — 它自动调用 `trackio.init()` 和 `trackio.finish()`。无需传递 `--report_to trackio`。项目名称取自 `--output_dir`，运行名称取自 `--run_name`。对于图像分类，在 `TrainingArguments` 中传递 `--report_to trackio`。

仪表板地址：`https://huggingface.co/spaces/{username}/trackio`

## 模型和硬件选择

### 推荐的目标检测模型

| 模型 | 参数 | 用例 |
|-------|--------|----------|
| `ustc-community/dfine-small-coco` | 10.4M | 最佳起点 — 快速，便宜，SOTA 质量 |
| `PekingU/rtdetr_v2_r18vd` | 20.2M | 轻量级实时检测器 |
| `ustc-community/dfine-large-coco` | 31.4M | 更高准确率，仍然高效 |
| `PekingU/rtdetr_v2_r50vd` | 43M | 强大的实时基线 |
| `ustc-community/dfine-xlarge-obj365` | 63.5M | 最佳准确率（在 Objects365 上预训练） |
| `PekingU/rtdetr_v2_r101vd` | 76M | 最大的 RT-DETR v2 变体 |

从 `ustc-community/dfine-small-coco` 开始快速迭代。移动到 D-FINE Large 或 RT-DETR v2 R50 以获得更好的准确率。

### 推荐的图像分类模型

所有 `timm/` 模型通过 `AutoModelForImageClassification` 开箱即用（加载为 `TimmWrapperForImageClassification`）。有关详细信息，请参见 [references/timm_trainer.md](references/timm_trainer.md)。

| 模型 | 参数 | 用例 |
|-------|--------|----------|
| `timm/mobilenetv3_small_100.lamb_in1k` | 2.5M | 超轻量级 — 移动/边缘，最快训练 |
| `timm/mobilevit_s.cvnets_in1k` | 5.6M | 移动 transformer — 良好的准确率/速度权衡 |
| `timm/resnet50.a1_in1k` | 25.6M | 强大的 CNN 基线 — 可靠，研究充分 |
| `timm/vit_base_patch16_dinov3.lvd1689m` | 86.6M | 最佳准确率 — DINOv3 自监督 ViT |

从 `timm/mobilenetv3_small_100.lamb_in1k` 开始快速迭代。移动到 `timm/resnet50.a1_in1k` 或 `timm/vit_base_patch16_dinov3.lvd1689m` 以获得更好的准确率。

### 推荐的 SAM/SAM2 分割模型

| 模型 | 参数 | 用例 |
|-------|--------|----------|
| `facebook/sam2.1-hiera-tiny` | 38.9M | 最快的 SAM2 — 适合快速实验 |
| `facebook/sam2.1-hiera-small` | 46.0M | 最佳起点 — 良好的质量/速度平衡 |
| `facebook/sam2.1-hiera-base-plus` | 80.8M | 更高容量，用于复杂分割 |
| `facebook/sam2.1-hiera-large` | 224.4M | 最佳 SAM2 准确率 — 需要更多 VRAM |
| `facebook/sam-vit-base` | 93.7M | 原始 SAM — ViT-B 主干 |
| `facebook/sam-vit-large` | 312.3M | 原始 SAM — ViT-L 主干 |
| `facebook/sam-vit-huge` | 641.1M | 原始 SAM — ViT-H，最佳 SAM v1 准确率 |

从 `facebook/sam2.1-hiera-small` 开始快速迭代。SAM2 模型通常比类似质量的 SAM v1 更高效。默认情况下，只有掩码解码器被训练（视觉和提示编码器被冻结）。

### 硬件推荐

所有推荐的 OD 和 IC 模型都在 100M 参数以下 — **`t4-small`（16 GB VRAM，$0.40/小时）对所有这些模型都足够了。** 图像分类模型通常比目标检测模型更小、更快 — `t4-small` 甚至可以舒适地处理 ViT-Base。对于 up to `hiera-base-plus` 的 SAM2 模型，`t4-small` 足够，因为只有掩码解码器被训练。对于 `sam2.1-hiera-large` 或 SAM v1 模型，使用 `l4x1` 或 `a10g-large`。只有在因大批量大小而遇到 OOM 时才升级 — 在切换硬件之前先减少批量大小。常见的升级路径：`t4-small` → `l4x1`（$0.80/小时，24 GB）→ `a10g-large`（$1.50/小时，24 GB）。

有关完整的硬件类型列表：请参考 `hugging-face-jobs` 技能。有关成本估算：运行 `scripts/estimate_cost.py`。

## 快速开始 — 目标检测

下面的 `script_args` 对两种提交方法都相同。有关它们之间的关键区别，请参见指令 #1。

```python
OD_SCRIPT_ARGS = [
    "--model_name_or_path", "ustc-community/dfine-small-coco",
    "--dataset_name", "cppe-5",
    "--image_square_size", "640",
    "--output_dir", "dfine_finetuned",
    "--num_train_epochs", "30",
    "--per_device_train_batch_size", "8",
    "--learning_rate", "5e-5",
    "--eval_strategy", "epoch",
    "--save_strategy", "epoch",
    "--save_total_limit", "2",
    "--load_best_model_at_end",
    "--metric_for_best_model", "eval_map",
    "--greater_is_better", "True",
    "--no_remove_unused_columns",
    "--no_eval_do_concat_batches",
    "--push_to_hub",
    "--hub_model_id", "username/model-name",
    "--do_train",
    "--do_eval",
]
```

```python
from huggingface_hub import HfApi, get_token
api = HfApi()
job_info = api.run_uv_job(
    script="scripts/object_detection_training.py",
    script_args=OD_SCRIPT_ARGS,
    flavor="t4-small",
    timeout=14400,
    env={"PYTHONUNBUFFERED": "1"},
    secrets={"HF_TOKEN": get_token()},
)
print(f"Job ID: {job_info.id}")
```

### 关键 OD `script_args`

- `--model_name_or_path` — 推荐：`"ustc-community/dfine-small-coco"`（见上面的模型表）
- `--dataset_name` — Hub 数据集 ID
- `--image_square_size` — 480（快速迭代）或 800（更好的准确率）
- `--hub_model_id` — `"username/model-name"` 用于 Hub 持久性
- `--num_train_epochs` — 30 通常用于收敛
- `--train_val_split` — 用于验证的分割比例（默认 0.15），如果数据集缺少验证分割则设置
- `--max_train_samples` — 截断训练集（用于快速测试运行，例如 `"785"` 用于 ~10% 的 7.8K 数据集）
- `--max_eval_samples` — 截断评估集

## 快速开始 — 图像分类

```python
IC_SCRIPT_ARGS = [
    "--model_name_or_path", "timm/mobilenetv3_small_100.lamb_in1k",
    "--dataset_name", "ethz/food101",
    "--output_dir", "food101_classifier",
    "--num_train_epochs", "5",
    "--per_device_train_batch_size", "32",
    "--per_device_eval_batch_size", "32",
    "--learning_rate", "5e-5",
    "--eval_strategy", "epoch",
    "--save_strategy", "epoch",
    "--save_total_limit", "2",
    "--load_best_model_at_end",
    "--metric_for_best_model", "eval_accuracy",
    "--greater_is_better", "True",
    "--no_remove_unused_columns",
    "--push_to_hub",
    "--hub_model_id", "username/food101-classifier",
    "--do_train",
    "--do_eval",
]
```

```python
from huggingface_hub import HfApi, get_token
api = HfApi()
job_info = api.run_uv_job(
    script="scripts/image_classification_training.py",
    script_args=IC_SCRIPT_ARGS,
    flavor="t4-small",
    timeout=7200,
    env={"PYTHONUNBUFFERED": "1"},
    secrets={"HF_TOKEN": get_token()},
)
print(f"Job ID: {job_info.id}")
```

### 关键 IC `script_args`

- `--model_name_or_path` — 任何 `timm/` 模型或 Transformers 分类模型（见上面的模型表）
- `--dataset_name` — Hub 数据集 ID
- `--image_column_name` — 包含 PIL 图像的列（默认：`"image"`）
- `--label_column_name` — 包含类标签的列（默认：`"label"`）
- `--hub_model_id` — `"username/model-name"` 用于 Hub 持久性
- `--num_train_epochs` — 3-5 通常用于分类（少于 OD）
- `--per_device_train_batch_size` — 16-64（分类模型比 OD 使用更少的内存）
- `--train_val_split` — 用于验证的分割比例（默认 0.15），如果数据集缺少验证分割则设置
- `--max_train_samples` / `--max_eval_samples` — 截断用于快速测试

## 快速开始 — SAM/SAM2 分割

```python
SAM_SCRIPT_ARGS = [
    "--model_name_or_path", "facebook/sam2.1-hiera-small",
    "--dataset_name", "merve/MicroMat-mini",
    "--prompt_type", "bbox",
    "--prompt_column_name", "prompt",
    "--output_dir", "sam2-finetuned",
    "--num_train_epochs", "30",
    "--per_device_train_batch_size", "4",
    "--learning_rate", "1e-5",
    "--logging_steps", "1",
    "--save_strategy", "epoch",
    "--save_total_limit", "2",
    "--remove_unused_columns", "False",
    "--dataloader_pin_memory", "False",
    "--push_to_hub",
    "--hub_model_id", "username/sam2-finetuned",
    "--do_train",
    "--report_to", "trackio",
]
```

```python
from huggingface_hub import HfApi, get_token
api = HfApi()
job_info = api.run_uv_job(
    script="scripts/sam_segmentation_training.py",
    script_args=SAM_SCRIPT_ARGS,
    flavor="t4-small",
    timeout=7200,
    env={"PYTHONUNBUFFERED": "1"},
    secrets={"HF_TOKEN": get_token()},
)
print(f"Job ID: {job_info.id}")
```

### 关键 SAM `script_args`

- `--model_name_or_path` — SAM 或 SAM2 模型（见上面的模型表）；自动检测 SAM vs SAM2
- `--dataset_name` — Hub 数据集 ID（例如，`"merve/MicroMat-mini"`）
- `--prompt_type` — `"bbox"` 或 `"point"` — 数据集中提示的类型
- `--prompt_column_name` — 带有 JSON 编码提示的列（默认：`"prompt"`）
- `--bbox_column_name` — 专用的 bbox 列（JSON 提示列的替代方案）
- `--point_column_name` — 专用的点列（JSON 提示列的替代方案）
- `--mask_column_name` — 带有真值掩码的列（默认：`"mask"`）
- `--hub_model_id` — `"username/model-name"` 用于 Hub 持久性
- `--num_train_epochs` — 20-30 通常用于 SAM 微调
- `--per_device_train_batch_size` — 2-4（SAM 模型使用大量内存）
- `--freeze_vision_encoder` / `--freeze_prompt_encoder` — 冻结编码器权重（默认：两者都冻结，只有掩码解码器训练）
- `--train_val_split` — 用于验证的分割比例（默认 0.1）

## 检查作业状态

**MCP 工具（如果可用）：**
```
hf_jobs("ps")                                   # 列出所有作业
hf_jobs("logs", {"job_id": "your-job-id"})      # 查看日志
hf_jobs("inspect", {"job_id": "your-job-id"})   # 作业详情
```

**Python API 回退：**
```python
from huggingface_hub import HfApi
api = HfApi()
api.list_jobs()                                  # 列出所有作业
api.get_job_logs(job_id="your-job-id")           # 查看日志
api.get_job(job_id="your-job-id")                # 作业详情
```

## 常见失败模式

### OOM（CUDA 内存不足）
减少 `per_device_train_batch_size`（尝试 4，然后 2），减少 `IMAGE_SIZE`，或升级硬件。

### 数据集格式错误
首先运行 `scripts/dataset_inspector.py`。训练脚本自动检测 xyxy vs xywh，将字符串类别转换为整数 ID，并在缺失时添加 `image_id`。确保 `objects.bbox` 包含 4 值坐标列表（绝对像素），`objects.category` 包含整数 ID 或字符串标签。

### Hub 推送失败（401）
验证：(1) 作业密钥包含令牌（见指令 #2），(2) 脚本在创建 `Trainer` 之前设置 `training_args.hub_token`，(3) 设置 `push_to_hub=True`，(4) 正确的 `hub_model_id`，(5) 令牌具有写入权限。

### 作业超时
增加超时（见指令 #5 表），减少轮数/数据集，或使用带有 `hub_strategy="every_save"` 的检查点策略。

### KeyError: 'test'（缺少测试分割）
目标检测训练脚本优雅地处理这个问题 — 它回退到 `validation` 分割。确保您使用最新的 `scripts/object_detection_training.py`。

### 单类数据集："iteration over a 0-d tensor"
当只有一个类时，`torchmetrics.MeanAveragePrecision` 为每类指标返回标量（0-d）张量。模板 `scripts/object_detection_training.py` 通过对这些张量调用 `.unsqueeze(0)` 来处理这个问题。确保您使用最新的模板。

### 检测性能差（mAP < 0.15）
增加轮数（30-50），确保 500+ 图像，检查不平衡类的每类 mAP，尝试不同的学习率（1e-5 到 1e-4），增加图像大小。

有关全面的故障排除：请参见 [references/reliability_principles.md](references/reliability_principles.md)

## 参考文件

- [scripts/object_detection_training.py](scripts/object_detection_training.py) — 生产就绪的目标检测训练脚本
- [scripts/image_classification_training.py](scripts/image_classification_training.py) — 生产就绪的图像分类训练脚本（支持 timm 模型）
- [scripts/sam_segmentation_training.py](scripts/sam_segmentation_training.py) — 生产就绪的 SAM/SAM2 分割训练脚本（bbox 和点提示）
- [scripts/dataset_inspector.py](scripts/dataset_inspector.py) — 验证 OD、分类和 SAM 分割的数据集格式
- [scripts/estimate_cost.py](scripts/estimate_cost.py) — 估算任何视觉模型的训练成本（包括 SAM/SAM2）
- [references/object_detection_training_notebook.md](references/object_detection_training_notebook.md) — 目标检测训练工作流程、增强策略和训练模式
- [references/image_classification_training_notebook.md](references/image_classification_training_notebook.md) — 带有 ViT、预处理和评估的图像分类训练工作流程
- [references/finetune_sam2_trainer.md](references/finetune_sam2_trainer.md) — SAM2 微调用 MicroMat 数据集、DiceCE 损失和 Trainer 集成的演练
- [references/timm_trainer.md](references/timm_trainer.md) — 将 timm 模型与 HF Trainer 一起使用（TimmWrapper、transforms、完整示例）
- [references/hub_saving.md](references/hub_saving.md) — 详细的 Hub 持久性指南和验证清单
- [references/reliability_principles.md](references/reliability_principles.md) — 来自生产经验的故障预防原则

## 外部链接

- [Transformers 目标检测指南](https://huggingface.co/docs/transformers/tasks/object_detection)
- [Transformers 图像分类指南](https://huggingface.co/docs/transformers/tasks/image_classification)
- [DETR 模型文档](https://huggingface.co/docs/transformers/model_doc/detr)
- [ViT 模型文档](https://huggingface.co/docs/transformers/model_doc/vit)
- [HF Jobs 指南](https://huggingface.co/docs/huggingface_hub/guides/jobs) — 主要 Jobs 文档
- [HF Jobs 配置](https://huggingface.co/docs/hub/en/jobs-configuration) — 硬件、密钥、超时、命名空间
- [HF Jobs CLI 参考](https://huggingface.co/docs/huggingface_hub/guides/cli#hf-jobs) — 命令行界面
- [目标检测模型](https://huggingface.co/models?pipeline_tag=object-detection)
- [图像分类模型](https://huggingface.co/models?pipeline_tag=image-classification)
- [SAM2 模型文档](https://huggingface.co/docs/transformers/model_doc/sam2)
- [SAM 模型文档](https://huggingface.co/docs/transformers/model_doc/sam)
- [目标检测数据集](https://huggingface.co/datasets?task_categories=task_categories:object-detection)
- [图像分类数据集](https://huggingface.co/datasets?task_categories=task_categories:image-classification)