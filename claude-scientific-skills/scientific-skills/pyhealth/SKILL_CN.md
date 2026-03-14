---
name: pyhealth
description: 用于开发、测试和部署临床数据机器学习模型的综合医疗AI工具包。当处理电子健康记录（EHR）、临床预测任务（死亡率、再入院、药物推荐）、医疗编码系统（ICD、NDC、ATC）、生理信号（EEG、ECG）、医疗数据集（MIMIC-III/IV、eICU、OMOP）或为医疗应用实现深度学习模型（RETAIN、SafeDrug、Transformer、GNN）时使用此技能。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# PyHealth: 医疗AI工具包

## 概述

PyHealth是一个用于医疗AI的综合Python库，提供专门的工具、模型和数据集用于临床机器学习。当开发医疗预测模型、处理临床数据、使用医疗编码系统或在医疗环境中部署AI解决方案时使用此技能。

## 使用场景

当以下情况时调用此技能：

- **处理医疗数据集**：MIMIC-III、MIMIC-IV、eICU、OMOP、睡眠EEG数据、医疗图像
- **临床预测任务**：死亡率预测、医院再入院、住院时间、药物推荐
- **医疗编码**：在ICD-9/10、NDC、RxNorm、ATC编码系统之间转换
- **处理临床数据**：顺序事件、生理信号、临床文本、医疗图像
- **实现医疗模型**：RETAIN、SafeDrug、GAMENet、StageNet、EHR的Transformer
- **评估临床模型**：公平性指标、校准、可解释性、不确定性量化

## 核心功能

PyHealth通过为医疗AI优化的模块化5阶段管道运行：

1. **数据加载**：访问10+医疗数据集，具有标准化接口
2. **任务定义**：应用20+预定义的临床预测任务或创建自定义任务
3. **模型选择**：从33+模型中选择（基线、深度学习、医疗特定）
4. **训练**：通过自动检查点、监控和评估进行训练
5. **部署**：校准、解释和验证以用于临床使用

**性能**：医疗数据处理速度比pandas快3倍

## 快速开始工作流程

```python
from pyhealth.datasets import MIMIC4Dataset
from pyhealth.tasks import mortality_prediction_mimic4_fn
from pyhealth.datasets import split_by_patient, get_dataloader
from pyhealth.models import Transformer
from pyhealth.trainer import Trainer

# 1. 加载数据集并设置任务
dataset = MIMIC4Dataset(root="/path/to/data")
sample_dataset = dataset.set_task(mortality_prediction_mimic4_fn)

# 2. 分割数据
train, val, test = split_by_patient(sample_dataset, [0.7, 0.1, 0.2])

# 3. 创建数据加载器
train_loader = get_dataloader(train, batch_size=64, shuffle=True)
val_loader = get_dataloader(val, batch_size=64, shuffle=False)
test_loader = get_dataloader(test, batch_size=64, shuffle=False)

# 4. 初始化并训练模型
model = Transformer(
    dataset=sample_dataset,
    feature_keys=["diagnoses", "medications"],
    mode="binary",
    embedding_dim=128
)

trainer = Trainer(model=model, device="cuda")
trainer.train(
    train_dataloader=train_loader,
    val_dataloader=val_loader,
    epochs=50,
    monitor="pr_auc_score"
)

# 5. 评估
results = trainer.evaluate(test_loader)
```

## 详细文档

此技能包含按功能组织的综合参考文档。根据需要阅读特定参考文件：

### 1. 数据集和数据结构

**文件**：`references/datasets.md`

**阅读时机**：
- 加载医疗数据集（MIMIC、eICU、OMOP、睡眠EEG等）
- 理解Event、Patient、Visit数据结构
- 处理不同数据类型（EHR、信号、图像、文本）
- 分割数据用于训练/验证/测试
- 使用SampleDataset进行任务特定格式化

**关键主题**：
- 核心数据结构（Event、Patient、Visit）
- 10+可用数据集（EHR、生理信号、成像、文本）
- 数据加载和迭代
- 训练/验证/测试分割策略
- 大型数据集的性能优化

### 2. 医疗编码转换

**文件**：`references/medical_coding.md`

**阅读时机**：
- 在医疗编码系统之间转换
- 处理诊断代码（ICD-9-CM、ICD-10-CM、CCS）
- 处理药物代码（NDC、RxNorm、ATC）
- 标准化程序代码（ICD-9-PROC、ICD-10-PROC）
- 将代码分组为临床类别
- 处理分层药物分类

**关键主题**：
- InnerMap用于系统内查找
- CrossMap用于跨系统转换
- 支持的编码系统（ICD、NDC、ATC、CCS、RxNorm）
- 代码标准化和层次结构遍历
- 按治疗类别分类药物
- 与数据集集成

### 3. 临床预测任务

**文件**：`references/tasks.md`

**阅读时机**：
- 定义临床预测目标
- 使用预定义任务（死亡率、再入院、药物推荐）
- 处理基于EHR、信号、成像或文本的任务
- 创建自定义预测任务
- 为模型设置输入/输出模式
- 应用任务特定的过滤逻辑

**关键主题**：
- 20+预定义临床任务
- EHR任务（死亡率、再入院、住院时间、药物推荐）
- 信号任务（睡眠分期、EEG分析、癫痫检测）
- 成像任务（COVID-19胸部X光分类）
- 文本任务（医疗编码、专科分类）
- 自定义任务创建模式

### 4. 模型和架构

**文件**：`references/models.md`

**阅读时机**：
- 为临床预测选择模型
- 理解模型架构和能力
- 在通用模型和医疗特定模型之间选择
- 实现可解释模型（RETAIN、AdaCare）
- 处理药物推荐（SafeDrug、GAMENet）
- 使用图神经网络用于医疗
- 配置模型超参数

**关键主题**：
- 33+可用模型
- 通用：逻辑回归、MLP、CNN、RNN、Transformer、GNN
- 医疗特定：RETAIN、SafeDrug、GAMENet、StageNet、AdaCare
- 按任务类型和数据类型选择模型
- 可解释性考虑
- 计算要求
- 超参数调优指南

### 5. 数据预处理

**文件**：`references/preprocessing.md`

**阅读时机**：
- 为模型预处理临床数据
- 处理顺序事件和时间序列数据
- 处理生理信号（EEG、ECG）
- 标准化实验室值和生命体征
- 为不同任务类型准备标签
- 构建特征词汇表
- 管理缺失数据和异常值

**关键主题**：
- 15+处理器类型
- 序列处理（填充、截断）
- 信号处理（过滤、分割）
- 特征提取和编码
- 标签处理器（二分类、多分类、多标签、回归）
- 文本和图像预处理
- 常见预处理工作流程

### 6. 训练和评估

**文件**：`references/training_evaluation.md`

**阅读时机**：
- 使用Trainer类训练模型
- 评估模型性能
- 计算临床指标
- 评估跨人口统计的模型公平性
- 校准预测以提高可靠性
- 量化预测不确定性
- 解释模型预测
- 为临床部署准备模型

**关键主题**：
- Trainer类（训练、评估、推理）
- 二分类、多分类、多标签、回归任务的指标
- 用于偏差评估的公平性指标
- 校准方法（Platt缩放、温度缩放）
- 不确定性量化（保形预测、MC dropout）
- 可解释性工具（注意力可视化、SHAP、ChEFER）
- 完整训练管道示例

## 安装

```bash
uv pip install pyhealth
```

**要求**：
- Python ≥ 3.7
- PyTorch ≥ 1.8
- NumPy, pandas, scikit-learn

## 常见用例

### 用例1：ICU死亡率预测

**目标**：预测重症监护病房患者死亡率

**方法**：
1. 加载MIMIC-IV数据集 → 阅读 `references/datasets.md`
2. 应用死亡率预测任务 → 阅读 `references/tasks.md`
3. 选择可解释模型（RETAIN） → 阅读 `references/models.md`
4. 训练和评估 → 阅读 `references/training_evaluation.md`
5. 解释预测以用于临床 → 阅读 `references/training_evaluation.md`

### 用例2：安全药物推荐

**目标**：推荐药物同时避免药物-药物相互作用

**方法**：
1. 加载EHR数据集（MIMIC-IV或OMOP） → 阅读 `references/datasets.md`
2. 应用药物推荐任务 → 阅读 `references/tasks.md`
3. 使用带DDI约束的SafeDrug模型 → 阅读 `references/models.md`
4. 预处理药物代码 → 阅读 `references/medical_coding.md`
5. 使用多标签指标评估 → 阅读 `references/training_evaluation.md`

### 用例3：医院再入院预测

**目标**：识别有30天再入院风险的患者

**方法**：
1. 加载多站点EHR数据（eICU或OMOP） → 阅读 `references/datasets.md`
2. 应用再入院预测任务 → 阅读 `references/tasks.md`
3. 在预处理中处理类别不平衡 → 阅读 `references/preprocessing.md`
4. 训练Transformer模型 → 阅读 `references/models.md`
5. 校准预测并评估公平性 → 阅读 `references/training_evaluation.md`

### 用例4：睡眠障碍诊断

**目标**：从EEG信号分类睡眠阶段

**方法**：
1. 加载睡眠EEG数据集（SleepEDF、SHHS） → 阅读 `references/datasets.md`
2. 应用睡眠分期任务 → 阅读 `references/tasks.md`
3. 预处理EEG信号（过滤、分割） → 阅读 `references/preprocessing.md`
4. 训练CNN或RNN模型 → 阅读 `references/models.md`
5. 评估每阶段性能 → 阅读 `references/training_evaluation.md`

### 用例5：医疗代码转换

**目标**：跨不同编码系统标准化诊断

**方法**：
1. 阅读 `references/medical_coding.md` 获取综合指导
2. 使用CrossMap在ICD-9、ICD-10、CCS之间转换
3. 将代码分组为临床有意义的类别
4. 与数据集处理集成

### 用例6：临床文本到ICD编码

**目标**：从临床笔记自动分配ICD代码

**方法**：
1. 加载带有临床文本的MIMIC-III → 阅读 `references/datasets.md`
2. 应用ICD编码任务 → 阅读 `references/tasks.md`
3. 预处理临床文本 → 阅读 `references/preprocessing.md`
4. 使用TransformersModel（ClinicalBERT） → 阅读 `references/models.md`
5. 使用多标签指标评估 → 阅读 `references/training_evaluation.md`

## 最佳实践

### 数据处理

1. **始终按患者分割**：确保没有患者出现在多个分割中，防止数据泄露
   ```python
   from pyhealth.datasets import split_by_patient
   train, val, test = split_by_patient(dataset, [0.7, 0.1, 0.2])
   ```

2. **检查数据集统计信息**：在建模前了解您的数据
   ```python
   print(dataset.stats())  # 患者、就诊、事件、代码分布
   ```

3. **使用适当的预处理**：将处理器与数据类型匹配（见 `references/preprocessing.md`）

### 模型开发

1. **从基线开始**：使用简单模型建立基线性能
   - 二分类/多分类任务使用逻辑回归
   - 初始深度学习基线使用MLP

2. **选择适合任务的模型**：
   - 需要可解释性 → RETAIN、AdaCare
   - 药物推荐 → SafeDrug、GAMENet
   - 长序列 → Transformer
   - 图关系 → GNN

3. **监控验证指标**：使用适合任务的指标并处理类别不平衡
   - 二分类：AUROC、AUPRC（特别是对于罕见事件）
   - 多分类：macro-F1（对于不平衡）、weighted-F1
   - 多标签：Jaccard、example-F1
   - 回归：MAE、RMSE

### 临床部署

1. **校准预测**：确保概率可靠（见 `references/training_evaluation.md`）

2. **评估公平性**：跨人口统计群体评估以检测偏差

3. **量化不确定性**：为预测提供置信度估计

4. **解释预测**：使用注意力权重、SHAP或ChEFER以获得临床信任

5. **彻底验证**：使用来自不同时间段或站点的保留测试集

## 限制和注意事项

### 数据要求

- **大型数据集**：深度学习模型需要足够的数据（数千名患者）
- **数据质量**：缺失数据和编码错误影响性能
- **时间一致性**：需要时确保训练/测试分割尊重时间顺序

### 临床验证

- **外部验证**：在来自不同医院/系统的数据上测试
- **前瞻性评估**：部署前在真实临床环境中验证
- **临床审查**：让临床医生审查预测和解释
- **伦理考虑**：解决隐私（HIPAA/GDPR）、公平性和安全性

### 计算资源

- **推荐GPU**：有效训练深度学习模型
- **内存要求**：大型数据集可能需要16GB+ RAM
- **存储**：医疗数据集可以是10-100GB

## 故障排除

### 常见问题

**数据集导入错误**：
- 确保数据集文件已下载且路径正确
- 检查PyHealth版本兼容性

**内存不足**：
- 减少批量大小
- 减少序列长度（`max_seq_length`）
- 使用梯度累积
- 分块处理数据

**性能差**：
- 检查类别不平衡并使用适当的指标（AUPRC vs AUROC）
- 验证预处理（标准化、缺失数据处理）
- 增加模型容量或训练轮数
- 检查训练/测试分割中的数据泄露

**训练缓慢**：
- 使用GPU（`device="cuda"`）
- 增加批量大小（如果内存允许）
- 减少序列长度
- 使用更高效的模型（CNN vs Transformer）

### 获取帮助

- **文档**：https://pyhealth.readthedocs.io/
- **GitHub问题**：https://github.com/sunlabuiuc/PyHealth/issues
- **教程**：在线提供7个核心教程 + 5个实用管道

## 示例：完整工作流程

```python
# 完整的死亡率预测管道
from pyhealth.datasets import MIMIC4Dataset
from pyhealth.tasks import mortality_prediction_mimic4_fn
from pyhealth.datasets import split_by_patient, get_dataloader
from pyhealth.models import RETAIN
from pyhealth.trainer import Trainer

# 1. 加载数据集
print("Loading MIMIC-IV dataset...")
dataset = MIMIC4Dataset(root="/data/mimic4")
print(dataset.stats())

# 2. 定义任务
print("Setting mortality prediction task...")
sample_dataset = dataset.set_task(mortality_prediction_mimic4_fn)
print(f"Generated {len(sample_dataset)} samples")

# 3. 分割数据（按患者分割以防止泄露）
print("Splitting data...")
train_ds, val_ds, test_ds = split_by_patient(
    sample_dataset, ratios=[0.7, 0.1, 0.2], seed=42
)

# 4. 创建数据加载器
train_loader = get_dataloader(train_ds, batch_size=64, shuffle=True)
val_loader = get_dataloader(val_ds, batch_size=64)
test_loader = get_dataloader(test_ds, batch_size=64)

# 5. 初始化可解释模型
print("Initializing RETAIN model...")
model = RETAIN(
    dataset=sample_dataset,
    feature_keys=["diagnoses", "procedures", "medications"],
    mode="binary",
    embedding_dim=128,
    hidden_dim=128
)

# 6. 训练模型
print("Training model...")
trainer = Trainer(model=model, device="cuda")
trainer.train(
    train_dataloader=train_loader,
    val_dataloader=val_loader,
    epochs=50,
    optimizer="Adam",
    learning_rate=1e-3,
    weight_decay=1e-5,
    monitor="pr_auc_score",  # 对不平衡数据使用AUPRC
    monitor_criterion="max",
    save_path="./checkpoints/mortality_retain"
)

# 7. 在测试集上评估
print("Evaluating on test set...")
test_results = trainer.evaluate(
    test_loader,
    metrics=["accuracy", "precision", "recall", "f1_score",
             "roc_auc_score", "pr_auc_score"]
)

print("\nTest Results:")
for metric, value in test_results.items():
    print(f"  {metric}: {value:.4f}")

# 8. 获取带注意力的预测以进行解释
predictions = trainer.inference(
    test_loader,
    additional_outputs=["visit_attention", "feature_attention"],
    return_patient_ids=True
)

# 9. 分析高风险患者
high_risk_idx = predictions["y_pred"].argmax()
patient_id = predictions["patient_ids"][high_risk_idx]
visit_attn = predictions["visit_attention"][high_risk_idx]
feature_attn = predictions["feature_attention"][high_risk_idx]

print(f"\nHigh-risk patient: {patient_id}")
print(f"Risk score: {predictions['y_pred'][high_risk_idx]:.3f}")
print(f"Most influential visit: {visit_attn.argmax()}")
print(f"Most important features: {feature_attn[visit_attn.argmax()].argsort()[-5:]}")

# 10. 保存模型以进行部署
trainer.save("./models/mortality_retain_final.pt")
print("\nModel saved successfully!")
```

## 资源

有关每个组件的详细信息，请参考`references/`目录中的综合参考文件：

- **datasets.md**：数据结构、加载和分割（4,500字）
- **medical_coding.md**：代码转换和标准化（3,800字）
- **tasks.md**：临床预测任务和自定义任务创建（4,200字）
- **models.md**：模型架构和选择指南（5,100字）
- **preprocessing.md**：数据处理器和预处理工作流程（4,600字）
- **training_evaluation.md**：训练、指标、校准、可解释性（5,900字）

**综合文档总计**：跨模块化参考文件约28,000字。