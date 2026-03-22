---
name: deepchem
description: 具有多样化特征器和预构建数据集的分子机器学习。用于属性预测（ADMET、毒性）与传统机器学习或图神经网络一起使用，当您想要广泛的可特征化选项和 MoleculeNet 基准测试时。最适合使用预训练模型进行快速实验、多样的分子表示。对于图优先的 PyTorch 工作流使用 torchdrug；对于基准数据集使用 pytdc。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# DeepChem

## 概述

DeepChem 是一个全面的 Python 库，用于将机器学习应用于化学、材料科学和生物学。通过专门的神经网络、分子特征化方法和预训练模型，实现分子属性预测、药物发现、材料设计和生物分子分析。

## 何时使用此技能

此技能应在以下情况下使用：
- 加载和处理分子数据（SMILES 字符串、SDF 文件、蛋白质序列）
- 预测分子属性（溶解度、毒性、结合亲和力、ADMET 属性）
- 在化学/生物数据集上训练模型
- 使用 MoleculeNet 基准数据集（Tox21、BBBP、Delaney 等）
- 将分子转换为机器学习就绪的特征（指纹、图表示、描述符）
- 实现分子的图神经网络（GCN、GAT、MPNN、AttentiveFP）
- 应用预训练模型的迁移学习（ChemBERTa、GROVER、MolFormer）
- 预测晶体/材料属性（带隙、形成能）
- 分析蛋白质或 DNA 序列

## 核心能力

### 1. 分子数据加载和处理

DeepChem 为各种化学数据格式提供专门的加载器：

```python
import deepchem as dc

# 加载带 SMILES 的 CSV
featurizer = dc.feat.CircularFingerprint(radius=2, size=2048)
loader = dc.data.CSVLoader(
    tasks=['solubility', 'toxicity'],
    feature_field='smiles',
    featurizer=featurizer
)
dataset = loader.create_dataset('molecules.csv')

# 加载 SDF 文件
loader = dc.data.SDFLoader(tasks=['activity'], featurizer=featurizer)
dataset = loader.create_dataset('compounds.sdf')

# 加载蛋白质序列
loader = dc.data.FASTALoader()
dataset = loader.create_dataset('proteins.fasta')
```

**关键加载器**：
- `CSVLoader`：带有分子标识符的表格数据
- `SDFLoader`：分子结构文件
- `FASTALoader`：蛋白质/DNA 序列
- `ImageLoader`：分子图像
- `JsonLoader`：JSON 格式的数据集

### 2. 分子特征化

将分子转换为机器学习模型的数值表示。

#### 特征器选择决策树

```
模型是图神经网络吗？
├─ 是 → 使用图特征器
│   ├─ 标准 GNN → MolGraphConvFeaturizer
│   ├─ 消息传递 → DMPNNFeaturizer
│   └─ 预训练 → GroverFeaturizer
│
└─ 否 → 什么类型的模型？
    ├─ 传统机器学习（RF、XGBoost、SVM）
    │   ├─ 快速基线 → CircularFingerprint (ECFP)
    │   ├─ 可解释 → RDKitDescriptors
    │   └─ 最大覆盖 → MordredDescriptors
    │
    ├─ 深度学习（非图）
    │   ├─ 密集网络 → CircularFingerprint
    │   └─ CNN → SmilesToImage
    │
    ├─ 序列模型（LSTM、Transformer）
    │   └─ SmilesToSeq
    │
    └─ 3D 结构分析
        └─ CoulombMatrix
```

#### 特征化示例

```python
# 指纹（用于传统机器学习）
fp = dc.feat.CircularFingerprint(radius=2, size=2048)

# 描述符（用于可解释模型）
desc = dc.feat.RDKitDescriptors()

# 图特征（用于 GNN）
graph_feat = dc.feat.MolGraphConvFeaturizer()

# 应用特征化
features = fp.featurize(['CCO', 'c1ccccc1'])
```

**选择指南**：
- **小型数据集（<1K）**：CircularFingerprint 或 RDKitDescriptors
- **中型数据集（1K-100K）**：CircularFingerprint 或图特征器
- **大型数据集（>100K）**：图特征器（MolGraphConvFeaturizer、DMPNNFeaturizer）
- **迁移学习**：预训练模型特征器（GroverFeaturizer）

有关完整的特征器文档，请参阅 `references/api_reference.md`。

### 3. 数据拆分

**关键**：对于药物发现任务，使用 `ScaffoldSplitter` 防止来自训练集和测试集中相似分子结构的数据泄漏。

```python
# 骨架拆分（推荐用于分子）
splitter = dc.splits.ScaffoldSplitter()
train, valid, test = splitter.train_valid_test_split(
    dataset,
    frac_train=0.8,
    frac_valid=0.1,
    frac_test=0.1
)

# 随机拆分（用于非分子数据）
splitter = dc.splits.RandomSplitter()
train, test = splitter.train_test_split(dataset)

# 分层拆分（用于不平衡分类）
splitter = dc.splits.RandomStratifiedSplitter()
train, test = splitter.train_test_split(dataset)
```

**可用的拆分器**：
- `ScaffoldSplitter`：按分子骨架拆分（防止泄漏）
- `ButinaSplitter`：基于聚类的分子拆分
- `MaxMinSplitter`：最大化集合之间的多样性
- `RandomSplitter`：随机拆分
- `RandomStratifiedSplitter`：保留类分布

### 4. 模型选择和训练

#### 快速模型选择指南

| 数据集大小 | 任务 | 推荐模型 | 特征器 |
|-------------|------|-------------------|------------|
| < 1K 样本 | 任何 | SklearnModel (RandomForest) | CircularFingerprint |
| 1K-100K | 分类/回归 | GBDTModel 或 MultitaskRegressor | CircularFingerprint |
| > 100K | 分子属性 | GCNModel、AttentiveFPModel、DMPNNModel | MolGraphConvFeaturizer |
| 任何（小样本优先） | 迁移学习 | ChemBERTa、GROVER、MolFormer | 模型特定 |
| 晶体结构 | 材料属性 | CGCNNModel、MEGNetModel | 基于结构 |
| 蛋白质序列 | 蛋白质属性 | ProtBERT | 基于序列 |

#### 示例：传统机器学习
```python
from sklearn.ensemble import RandomForestRegressor

# 包装 scikit-learn 模型
sklearn_model = RandomForestRegressor(n_estimators=100)
model = dc.models.SklearnModel(model=sklearn_model)
model.fit(train)
```

#### 示例：深度学习
```python
# 多任务回归器（用于指纹）
model = dc.models.MultitaskRegressor(
    n_tasks=2,
    n_features=2048,
    layer_sizes=[1000, 500],
    dropouts=0.25,
    learning_rate=0.001
)
model.fit(train, nb_epoch=50)
```

#### 示例：图神经网络
```python
# 图卷积网络
model = dc.models.GCNModel(
    n_tasks=1,
    mode='regression',
    batch_size=128,
    learning_rate=0.001
)
model.fit(train, nb_epoch=50)

# 图注意力网络
model = dc.models.GATModel(n_tasks=1, mode='classification')
model.fit(train, nb_epoch=50)

# 注意力指纹
model = dc.models.AttentiveFPModel(n_tasks=1, mode='regression')
model.fit(train, nb_epoch=50)
```

### 5. MoleculeNet 基准测试

快速访问 30 多个经过策展的基准数据集，具有标准化的训练/验证/测试拆分：

```python
# 加载基准数据集
tasks, datasets, transformers = dc.molnet.load_tox21(
    featurizer='GraphConv',  # 或 'ECFP'、'Weave'、'Raw'
    splitter='scaffold',     # 或 'random'、'stratified'
    reload=False
)
train, valid, test = datasets

# 训练和评估
model = dc.models.GCNModel(n_tasks=len(tasks), mode='classification')
model.fit(train, nb_epoch=50)

metric = dc.metrics.Metric(dc.metrics.roc_auc_score)
test_score = model.evaluate(test, [metric])
```

**常见数据集**：
- **分类**：`load_tox21()`、`load_bbbp()`、`load_hiv()`、`load_clintox()`
- **回归**：`load_delaney()`、`load_freesolv()`、`load_lipo()`
- **量子属性**：`load_qm7()`、`load_qm8()`、`load_qm9()`
- **材料**：`load_perovskite()`、`load_bandgap()`、`load_mp_formation_energy()`

有关完整的数据集列表，请参阅 `references/api_reference.md`。

### 6. 迁移学习

利用预训练模型提高性能，特别是在小型数据集上：

```python
# ChemBERTa（在 77M 分子上预训练的 BERT）
model = dc.models.HuggingFaceModel(
    model='seyonec/ChemBERTa-zinc-base-v1',
    task='classification',
    n_tasks=1,
    learning_rate=2e-5  # 微调时使用较低的学习率
)
model.fit(train, nb_epoch=10)

# GROVER（在 10M 分子上预训练的图转换器）
model = dc.models.GroverModel(
    task='regression',
    n_tasks=1
)
model.fit(train, nb_epoch=20)
```

**何时使用迁移学习**：
- 小型数据集（< 1000 个样本）
- 新颖的分子骨架
- 有限的计算资源
- 需要快速原型设计

使用 `scripts/transfer_learning.py` 脚本进行引导式迁移学习工作流。

### 7. 模型评估

```python
# 定义指标
classification_metrics = [
    dc.metrics.Metric(dc.metrics.roc_auc_score, name='ROC-AUC'),
    dc.metrics.Metric(dc.metrics.accuracy_score, name='Accuracy'),
    dc.metrics.Metric(dc.metrics.f1_score, name='F1')
]

regression_metrics = [
    dc.metrics.Metric(dc.metrics.r2_score, name='R²'),
    dc.metrics.Metric(dc.metrics.mean_absolute_error, name='MAE'),
    dc.metrics.Metric(dc.metrics.root_mean_squared_error, name='RMSE')
]

# 评估
train_scores = model.evaluate(train, classification_metrics)
test_scores = model.evaluate(test, classification_metrics)
```

### 8. 进行预测

```python
# 在测试集上预测
predictions = model.predict(test)

# 预测新分子
new_smiles = ['CCO', 'c1ccccc1', 'CC(C)O']
new_features = featurizer.featurize(new_smiles)
new_dataset = dc.data.NumpyDataset(X=new_features)

# 应用与训练相同的转换
for transformer in transformers:
    new_dataset = transformer.transform(new_dataset)

predictions = model.predict(new_dataset)
```

## 典型工作流

### 工作流 A：快速基准评估

用于在标准基准上评估模型：

```python
import deepchem as dc

# 1. 加载基准
tasks, datasets, _ = dc.molnet.load_bbbp(
    featurizer='GraphConv',
    splitter='scaffold'
)
train, valid, test = datasets

# 2. 训练模型
model = dc.models.GCNModel(n_tasks=len(tasks), mode='classification')
model.fit(train, nb_epoch=50)

# 3. 评估
metric = dc.metrics.Metric(dc.metrics.roc_auc_score)
test_score = model.evaluate(test, [metric])
print(f"测试 ROC-AUC：{test_score}")
```

### 工作流 B：自定义数据预测

用于在自定义分子数据集上训练：

```python
import deepchem as dc

# 1. 加载和特征化数据
featurizer = dc.feat.CircularFingerprint(radius=2, size=2048)
loader = dc.data.CSVLoader(
    tasks=['activity'],
    feature_field='smiles',
    featurizer=featurizer
)
dataset = loader.create_dataset('my_molecules.csv')

# 2. 拆分数据（对分子使用 ScaffoldSplitter！）
splitter = dc.splits.ScaffoldSplitter()
train, valid, test = splitter.train_valid_test_split(dataset)

# 3. 归一化（可选但推荐）
transformers = [dc.trans.NormalizationTransformer(
    transform_y=True, dataset=train
)]
for transformer in transformers:
    train = transformer.transform(train)
    valid = transformer.transform(valid)
    test = transformer.transform(test)

# 4. 训练模型
model = dc.models.MultitaskRegressor(
    n_tasks=1,
    n_features=2048,
    layer_sizes=[1000, 500],
    dropouts=0.25
)
model.fit(train, nb_epoch=50)

# 5. 评估
metric = dc.metrics.Metric(dc.metrics.r2_score)
test_score = model.evaluate(test, [metric])
```

### 工作流 C：小型数据集上的迁移学习

用于利用预训练模型：

```python
import deepchem as dc

# 1. 加载数据（预训练模型通常需要原始 SMILES）
loader = dc.data.CSVLoader(
    tasks=['activity'],
    feature_field='smiles',
    featurizer=dc.feat.DummyFeaturizer()  # 模型处理特征化
)
dataset = loader.create_dataset('small_dataset.csv')

# 2. 拆分数据
splitter = dc.splits.ScaffoldSplitter()
train, test = splitter.train_test_split(dataset)

# 3. 加载预训练模型
model = dc.models.HuggingFaceModel(
    model='seyonec/ChemBERTa-zinc-base-v1',
    task='classification',
    n_tasks=1,
    learning_rate=2e-5
)

# 4. 微调
model.fit(train, nb_epoch=10)

# 5. 评估
predictions = model.predict(test)
```

有关 8 个详细工作流示例，请参阅 `references/workflows.md`，涵盖分子生成、材料科学、蛋白质分析等。

## 示例脚本

此技能在 `scripts/` 目录中包含三个生产就绪的脚本：

### 1. `predict_solubility.py`
训练和评估溶解度预测模型。适用于 Delaney 基准或自定义 CSV 数据。

```bash
# 使用 Delaney 基准
python scripts/predict_solubility.py

# 使用自定义数据
python scripts/predict_solubility.py \
    --data my_data.csv \
    --smiles-col smiles \
    --target-col solubility \
    --predict "CCO" "c1ccccc1"
```

### 2. `graph_neural_network.py`
在分子数据上训练各种图神经网络架构。

```bash
# 在 Tox21 上训练 GCN
python scripts/graph_neural_network.py --model gcn --dataset tox21

# 在自定义数据上训练 AttentiveFP
python scripts/graph_neural_network.py \
    --model attentivefp \
    --data molecules.csv \
    --task-type regression \
    --targets activity \
    --epochs 100
```

### 3. `transfer_learning.py`
在分子属性预测任务上微调预训练模型（ChemBERTa、GROVER）。

```bash
# 在 BBBP 上微调 ChemBERTa
python scripts/transfer_learning.py --model chemberta --dataset bbbp

# 在自定义数据上微调 GROVER
python scripts/transfer_learning.py \
    --model grover \
    --data small_dataset.csv \
    --target activity \
    --task-type classification \
    --epochs 20
```

## 常见模式和最佳实践

### 模式 1：对分子始终使用骨架拆分
```python
# 好：防止数据泄漏
splitter = dc.splits.ScaffoldSplitter()
train, test = splitter.train_test_split(dataset)

# 坏：训练集和测试集中的相似分子
splitter = dc.splits.RandomSplitter()
train, test = splitter.train_test_split(dataset)
```

### 模式 2：归一化特征和目标
```python
transformers = [
    dc.trans.NormalizationTransformer(
        transform_y=True,  # 也归一化目标值
        dataset=train
    )
]
for transformer in transformers:
    train = transformer.transform(train)
    test = transformer.transform(test)
```

### 模式 3：从简单开始，然后扩展
1. 从 Random Forest + CircularFingerprint 开始（快速基线）
2. 如果 RF 效果好，尝试 XGBoost/LightGBM
3. 如果有 >5K 样本，转到深度学习（MultitaskRegressor）
4. 如果有 >10K 样本，尝试 GNN
5. 对于小型数据集或新颖骨架，使用迁移学习

### 模式 4：处理不平衡数据
```python
# 选项 1：平衡转换器
transformer = dc.trans.BalancingTransformer(dataset=train)
train = transformer.transform(train)

# 选项 2：使用平衡指标
metric = dc.metrics.Metric(dc.metrics.balanced_accuracy_score)
```

### 模式 5：避免内存问题
```python
# 对大型数据集使用 DiskDataset
dataset = dc.data.DiskDataset.from_numpy(X, y, w, ids)

# 使用较小的批次大小
model = dc.models.GCNModel(batch_size=32)  # 而不是 128
```

## 常见陷阱

### 问题 1：药物发现中的数据泄漏
**问题**：使用随机拆分允许训练集和测试集中存在相似分子。
**解决方案**：对分子数据集始终使用 `ScaffoldSplitter`。

### 问题 2：GNN 性能不如指纹
**问题**：图神经网络性能比简单指纹差。
**解决方案**：
- 确保数据集足够大（通常 >10K 样本）
- 增加训练轮数（50-100）
- 尝试不同的架构（AttentiveFP、DMPNN 而不是 GCN）
- 使用预训练模型（GROVER）

### 问题 3：小型数据集上的过拟合
**问题**：模型记忆训练数据。
**解决方案**：
- 使用更强的正则化（将 dropout 增加到 0.5）
- 使用更简单的模型（Random Forest 而不是深度学习）
- 应用迁移学习（ChemBERTa、GROVER）
- 收集更多数据

### 问题 4：导入错误
**问题**：找不到模块错误。
**解决方案**：确保安装了 DeepChem 及其依赖项：
```bash
uv pip install deepchem
# 对于 PyTorch 模型
uv pip install deepchem[torch]
# 对于所有功能
uv pip install deepchem[all]
```

## 参考文档

此技能包含全面的参考文档：

### `references/api_reference.md`
完整的 API 文档，包括：
- 所有数据加载器及其用例
- 数据集类以及何时使用每个类
- 完整的特征器目录和选择指南
- 按类别组织的模型目录（50+ 个模型）
- MoleculeNet 数据集描述
- 指标和评估函数
- 常见代码模式

**何时参考**：当您需要特定的 API 详细信息、参数名称或想要探索可用选项时。

### `references/workflows.md`
八个详细的端到端工作流：
1. 从 SMILES 进行分子属性预测
2. 使用 MoleculeNet 基准
3. 超参数优化
4. 使用预训练模型的迁移学习
5. 使用 GAN 进行分子生成
6. 材料属性预测
7. 蛋白质序列分析
8. 自定义模型集成

**何时参考**：将这些工作流用作实现完整解决方案的模板。

## 安装说明

基本安装：
```bash
uv pip install deepchem
```

对于 PyTorch 模型（GCN、GAT 等）：
```bash
uv pip install deepchem[torch]
```

对于所有功能：
```bash
uv pip install deepchem[all]
```

如果出现导入错误，用户可能需要特定的依赖项。请查看 DeepChem 文档以获取详细的安装说明。

## 其他资源

- 官方文档：https://deepchem.readthedocs.io/
- GitHub 仓库：https://github.com/deepchem/deepchem
- 教程：https://deepchem.readthedocs.io/en/latest/get_started/tutorials.html
- 论文："MoleculeNet: A Benchmark for Molecular Machine Learning"
