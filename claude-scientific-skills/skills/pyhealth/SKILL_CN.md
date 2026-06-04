---
name: pyhealth
description: 使用PyHealth构建临床/医疗深度学习管道——加载EHR/信号/成像数据集（MIMIC-III/IV、eICU、OMOP、SleepEDF、ChestXray14、EHRShot），定义任务（死亡率、再入院、住院时长、药物推荐、睡眠分期、ICD编码、EEG事件），实例化模型（Transformer、RETAIN、GAMENet、SafeDrug、MICRON、StageNet、AdaCare、CNN/RNN/MLP），使用PyHealth Trainer训练，计算临床指标，使用医学代码工具（ICD/ATC/NDC/RxNorm查找和交叉映射）。只要用户提到PyHealth、MIMIC、eICU、OMOP、EHR建模、临床预测、药物推荐、睡眠分期、医学代码映射、ICD/ATC代码或任何符合数据集→任务→模型→训练器→指标模式的医疗ML管道，即使没有明确提及"PyHealth"，也可以使用此技能。
metadata:
  version: "1.0"
  skill-author: K-Dense Inc.
---






# PyHealth

PyHealth（https://pyhealth.dev/）是一个用于临床深度学习的 Python 工具包。它为电子健康记录（EHR）、生理信号和医学影像提供了一个统一、模块化的流程。

该库围绕 **5 阶段流程** —— `Dataset → Task → Model → Trainer → Metrics` —— 构建，每个阶段均可替换，且阶段之间的接口稳定。遵循此流程结构的代码具有良好的组合性；绕过该结构的代码通常会与库产生冲突。

## 何时使用此技能

当用户进行临床/医疗 ML 且满足以下任一条件时，请使用此技能：

- 提及 PyHealth、MIMIC-III/IV、eICU、OMOP-CDM、EHRShot、SleepEDF、SHHS、ISRUC、COVID19-CXR、ChestX-ray14、TUEV/TUAB。
- 希望预测死亡率、再入院、住院时长、药物推荐、睡眠分期、ICD 编码、EEG 事件或去标识化。
- 需要查询或交叉映射医学编码（ICD-9-CM、ICD-10-CM、ATC、NDC、RxNorm、CCS）。
- 拥有 EHR 格式的数据，希望在不自行编写基础代码的情况下训练临床模型。

当工作流程符合其 5 个阶段时，PyHealth 是合适的工具。如果用户只是想在表格数据上使用通用 PyTorch，则不需要此技能。

## 安装（uv）

PyHealth 2.0 需要 Python ≥ 3.12，< 3.14。使用 `uv` 进行环境管理 —— 更快且可复现。

```bash
# 创建使用正确 Python 版本的项目
uv init my-pyhealth-project
cd my-pyhealth-project
uv python pin 3.12

# 添加 PyHealth（会自动安装 PyTorch 及相关依赖）
uv add pyhealth

# 在环境中运行脚本
uv run python train.py
```

对于一次性脚本（无需创建项目），使用 `uv run --with pyhealth python script.py`。对于旧版 1.x（Python 3.9+），使用 `uv add pyhealth==1.16`。详细的安装说明、MIMIC 访问方式以及 GPU/CPU 设备提示请参阅 `references/installation.md`。

## 5 阶段流程

一个完整的流程通常少于 20 行。以下是标准结构 —— 从这里开始，然后根据需要修改各部分：

```python
from pyhealth.datasets import MIMIC3Dataset, split_by_patient, get_dataloader
from pyhealth.tasks import MortalityPredictionMIMIC3
from pyhealth.models import Transformer
from pyhealth.trainer import Trainer
from pyhealth.metrics.binary import binary_metrics_fn

# 1. Dataset —— 原始患者登记库
base = MIMIC3Dataset(
    root="https://storage.googleapis.com/pyhealth/Synthetic_MIMIC-III/",
    tables=["DIAGNOSES_ICD", "PROCEDURES_ICD", "PRESCRIPTIONS"],
)

# 2. Task —— 将患者转换为有监督样本
samples = base.set_task(MortalityPredictionMIMIC3())

# 3. 划分 + DataLoaders（按患者划分以避免信息泄露）
train_ds, val_ds, test_ds = split_by_patient(samples, [0.8, 0.1, 0.1])
train_loader = get_dataloader(train_ds, batch_size=32, shuffle=True)
val_loader   = get_dataloader(val_ds,   batch_size=32, shuffle=False)
test_loader  = get_dataloader(test_ds,  batch_size=32, shuffle=False)

# 4. Model —— 必须传入 SampleDataset，而不是 BaseDataset
model = Transformer(dataset=samples)

# 5. 训练 + 评估
trainer = Trainer(model=model)
trainer.train(
    train_dataloader=train_loader,
    val_dataloader=val_loader,
    epochs=50,
    monitor="pr_auc",
)

y_true, y_prob, _ = trainer.inference(test_loader)
print(binary_metrics_fn(y_true, y_prob, metrics=["pr_auc", "roc_auc"]))
```

可直接复制使用的入门示例位于 `assets/starter_pipeline.py`。

## 关键注意事项

以下是 PyHealth 代码中最常犯的错误。在编写流程之前，请务必牢记：

1. **模型接收的是 `SampleDataset`，而不是 `BaseDataset`。** `MIMIC3Dataset(...)` 返回的是 `BaseDataset`（一个可查询的患者登记库）。只有在调用 `.set_task(task)` 之后，才会得到 `SampleDataset`，而模型、划分器和 DataLoader 都需要这个类型。如果将 `base` 传给模型，将会失败或行为异常。

2. **始终按患者（或就诊）划分，而不是按样本划分。** 随机样本级别的划分会导致信息在训练集和测试集之间泄露，因为同一个患者可能同时出现在两者中。对于患者级别预测，请使用 `split_by_patient`；仅在就诊之间相互独立时使用 `split_by_visit`。

3. **将任务与数据集匹配。** 任务是数据集特定的：`MortalityPredictionMIMIC3` 不适用于 MIMIC-IV —— 应使用 `MortalityPredictionMIMIC4` 或 `InHospitalMortalityMIMIC4`。完整的映射关系请参阅 `references/tasks.md`。

4. **为任务类型选择合适的 `monitor`。** 二分类使用 `"pr_auc"` 或 `"roc_auc"`；多标签（药物推荐）使用 `"pr_auc_samples"` 或 `"jaccard_samples"`；多分类使用 `"accuracy"` 或 `"f1_macro"`。选择错误的 monitor 会导致检查点保存了错误的 epoch。

5. **MIMIC-IV 使用 `ehr_root=`，而不是 `root=`。** 这是数据集构造器中唯一的不一致之处。

6. **为了可复现的工作，请将 `cache_dir=` 指向持久化位置。** PyHealth 会缓存解析后的数据集；如果没有 `cache_dir`，每次运行都会重新解析。

## 如何使用此技能

PyHealth 的 API 范围很广 —— 没有必要一次性全部加载。请根据用户的任务阅读相应的参考文件：

| 如果用户询问的是… | 请阅读 |
|---|---|
| 安装、环境配置、MIMIC 访问、GPU | `references/installation.md` |
| 使用哪个数据集类、加载模式、划分方式 | `references/datasets.md` |
| 选择什么预测任务（死亡率、再入院、药物推荐、睡眠…） | `references/tasks.md` |
| 选择模型架构、模型特定参数 | `references/models.md` |
| 查询或交叉映射 ICD/ATC/NDC/RxNorm/CCS 编码、分词器 | `references/medcode.md` |
| 常见场景的端到端示例 | `references/examples.md` |

对于多步骤任务（例如"在 MIMIC-IV 上构建药物推荐流程"），请同时阅读 `tasks.md`、`models.md` 和 `examples.md` —— 它们相互交叉引用。

## 风格说明

编写简洁、地道的 PyHealth 代码。该库具有明确的风格倾向；请利用其抽象，而不是用原始 PyTorch 重新实现它们。如果你发现自己正在编写自定义训练循环，请考虑 `Trainer` 是否能胜任 —— 它几乎总是可以，并且它能免费处理检查点、日志记录和最优模型选择。

当用户拥有私有 MIMIC 访问权限时，请指向本地 CSV 根目录；对于演示和学习，合成 MIMIC-III 存储桶（`https://storage.googleapis.com/pyhealth/Synthetic_MIMIC-III/`）即可，且无需认证即可使用。
