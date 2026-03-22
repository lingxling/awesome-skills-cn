---
name: geniml
description: 使用基因组区间数据训练机器学习模型，包括基因组区间标记化、数据增强、模型训练和推理。用于预测基因组特征、分析染色质可及性、预测基因表达、识别调控元件或任何涉及基因组区间和序列的机器学习任务。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# GeniML

GeniML是一个用于基因组区间机器学习的Python库，提供标记化、数据增强、模型训练和推理功能。它专门设计用于处理基因组区间数据，如ChIP-seq峰、ATAC-seq峰和增强子区域。

## 安装

```bash
uv pip install geniml
```

### 可选依赖项

```bash
# 用于GPU加速
uv pip install torch torchvision

# 用于可视化
uv pip install matplotlib seaborn

# 用于数据处理
uv pip install pandas numpy
```

## 快速开始

```python
from geniml import GeniML

# 初始化GeniML
geniml = GeniML()

# 加载基因组区间数据
intervals = geniml.load_intervals("peaks.bed")

# 标记化区间
tokens = geniml.tokenize(intervals)

# 训练模型
model = geniml.train(tokens, labels)

# 预测
predictions = geniml.predict(model, new_intervals)
```

## 核心功能

### 1. 基因组区间标记化

```python
from geniml import GeniML

geniml = GeniML()

# 加载区间数据
intervals = geniml.load_intervals("peaks.bed")

# 标记化区间
tokens = geniml.tokenize(
    intervals,
    window_size=1000,  # 窗口大小
    stride=500,        # 步长
    include_sequence=True,  # 包含序列信息
    include_chromatin=True  # 包含染色质信息
)
```

### 2. 数据增强

```python
# 随机平移
augmented = geniml.augment_shift(intervals, shift_range=100)

# 随机缩放
augmented = geniml.augment_scale(intervals, scale_range=(0.8, 1.2))

# 随机翻转
augmented = geniml.augment_flip(intervals)

# 组合增强
augmented = geniml.augment(intervals, methods=['shift', 'scale', 'flip'])
```

### 3. 模型训练

```python
# 准备数据
tokens = geniml.tokenize(intervals)
labels = geniml.load_labels("labels.txt")

# 分割数据
train_tokens, test_tokens, train_labels, test_labels = geniml.split_data(
    tokens, labels, test_size=0.2
)

# 训练模型
model = geniml.train(
    train_tokens,
    train_labels,
    model_type="cnn",  # 可选: cnn, rnn, transformer
    epochs=100,
    batch_size=32,
    learning_rate=0.001
)
```

### 4. 模型推理

```python
# 加载训练好的模型
model = geniml.load_model("model.pth")

# 预测新数据
new_intervals = geniml.load_intervals("new_peaks.bed")
new_tokens = geniml.tokenize(new_intervals)
predictions = geniml.predict(model, new_tokens)

# 获取概率
probabilities = geniml.predict_proba(model, new_tokens)
```

### 5. 模型评估

```python
# 评估模型
metrics = geniml.evaluate(model, test_tokens, test_labels)

# 计算准确率
accuracy = metrics['accuracy']

# 计算精确率和召回率
precision = metrics['precision']
recall = metrics['recall']

# 计算F1分数
f1_score = metrics['f1_score']

# 生成混淆矩阵
confusion_matrix = geniml.confusion_matrix(model, test_tokens, test_labels)
```

### 6. 可视化

```python
# 绘制训练曲线
geniml.plot_training_history(model)

# 绘制ROC曲线
geniml.plot_roc_curve(model, test_tokens, test_labels)

# 绘制混淆矩阵
geniml.plot_confusion_matrix(model, test_tokens, test_labels)

# 绘制特征重要性
geniml.plot_feature_importance(model)
```

## 高级功能

### 1. 自定义标记化器

```python
from geniml.tokenizers import CustomTokenizer

# 创建自定义标记化器
tokenizer = CustomTokenizer(
    window_size=2000,
    stride=1000,
    include_sequence=True,
    include_chromatin=True,
    sequence_encoding='onehot',  # 可选: onehot, embedding
    chromatin_features=['ATAC', 'H3K27ac', 'H3K4me3']
)

# 使用自定义标记化器
tokens = tokenizer.tokenize(intervals)
```

### 2. 自定义模型

```python
from geniml.models import CustomModel

# 创建自定义模型
model = CustomModel(
    input_size=1000,
    hidden_sizes=[512, 256, 128],
    output_size=2,
    dropout_rate=0.5
)

# 训练自定义模型
geniml.train_model(
    model,
    train_tokens,
    train_labels,
    epochs=100,
    batch_size=32
)
```

### 3. 迁移学习

```python
# 加载预训练模型
pretrained_model = geniml.load_pretrained_model("pretrained_model.pth")

# 微调模型
finetuned_model = geniml.finetune(
    pretrained_model,
    new_tokens,
    new_labels,
    epochs=50,
    learning_rate=0.0001
)
```

### 4. 集成学习

```python
# 训练多个模型
model1 = geniml.train(train_tokens, train_labels, model_type="cnn")
model2 = geniml.train(train_tokens, train_labels, model_type="rnn")
model3 = geniml.train(train_tokens, train_labels, model_type="transformer")

# 集成预测
predictions = geniml.ensemble_predict(
    [model1, model2, model3],
    test_tokens,
    method='voting'  # 可选: voting, averaging, stacking
)
```

### 5. 超参数调优

```python
# 定义超参数网格
param_grid = {
    'learning_rate': [0.001, 0.0001, 0.00001],
    'batch_size': [16, 32, 64],
    'hidden_size': [128, 256, 512],
    'dropout_rate': [0.3, 0.5, 0.7]
}

# 执行网格搜索
best_model, best_params = geniml.grid_search(
    train_tokens,
    train_labels,
    param_grid,
    cv=5
)

# 执行随机搜索
best_model, best_params = geniml.random_search(
    train_tokens,
    train_labels,
    param_grid,
    n_iter=50,
    cv=5
)
```

## 常见工作流

### 工作流1：ChIP-seq峰分类

```python
from geniml import GeniML

# 初始化
geniml = GeniML()

# 加载数据
peaks = geniml.load_intervals("chip_peaks.bed")
labels = geniml.load_labels("chip_labels.txt")

# 标记化
tokens = geniml.tokenize(peaks)

# 分割数据
train_tokens, test_tokens, train_labels, test_labels = geniml.split_data(
    tokens, labels, test_size=0.2
)

# 训练模型
model = geniml.train(
    train_tokens,
    train_labels,
    model_type="cnn",
    epochs=100
)

# 评估
metrics = geniml.evaluate(model, test_tokens, test_labels)
print(f"Accuracy: {metrics['accuracy']}")
```

### 工作流2：ATAC-seq可及性预测

```python
from geniml import GeniML

# 初始化
geniml = GeniML()

# 加载ATAC-seq数据
atac_peaks = geniml.load_intervals("atac_peaks.bed")
atac_signal = geniml.load_signal("atac_signal.bw")

# 标记化
tokens = geniml.tokenize(
    atac_peaks,
    include_signal=True,
    signal_file=atac_signal
)

# 训练回归模型
model = geniml.train_regression(
    tokens,
    atac_signal,
    model_type="cnn",
    epochs=100
)

# 预测
new_peaks = geniml.load_intervals("new_peaks.bed")
new_tokens = geniml.tokenize(new_peaks)
predictions = geniml.predict(model, new_tokens)
```

### 工作流3：增强子识别

```python
from geniml import GeniML

# 初始化
geniml = GeniML()

# 加载增强子数据
enhancers = geniml.load_intervals("enhancers.bed")
non_enhancers = geniml.load_intervals("non_enhancers.bed")

# 合并数据
all_intervals = geniml.merge_intervals(enhancers, non_enhancers)
labels = geniml.create_labels(enhancers, non_enhancers)

# 标记化
tokens = geniml.tokenize(all_intervals)

# 数据增强
augmented_tokens = geniml.augment(tokens, methods=['shift', 'scale'])

# 训练模型
model = geniml.train(
    augmented_tokens,
    labels,
    model_type="transformer",
    epochs=100
)

# 预测新区域
new_regions = geniml.load_intervals("new_regions.bed")
new_tokens = geniml.tokenize(new_regions)
predictions = geniml.predict(model, new_tokens)
```

## 最佳实践

1. **数据预处理**：在标记化之前清理和标准化区间数据
2. **数据增强**：使用数据增强提高模型泛化能力
3. **交叉验证**：使用交叉验证评估模型性能
4. **超参数调优**：使用网格搜索或随机搜索优化超参数
5. **模型保存**：保存训练好的模型以供将来使用
6. **可视化**：使用可视化工具理解模型行为
7. **文档记录**：记录所有实验和结果以实现可重现性

## 与其他工具集成

### 与gtars集成

```python
import gtars
from geniml import GeniML

# 使用gtars处理区间
igd = gtars.igd.build_index("regions.bed")
overlaps = igd.query("chr1", 1000, 2000)

# 使用geniml训练模型
geniml = GeniML()
tokens = geniml.tokenize(overlaps)
model = geniml.train(tokens, labels)
```

### 与scikit-learn集成

```python
from geniml import GeniML
from sklearn.ensemble import RandomForestClassifier

# 标记化数据
geniml = GeniML()
tokens = geniml.tokenize(intervals)

# 使用scikit-learn模型
model = RandomForestClassifier(n_estimators=100)
model.fit(tokens, labels)

# 预测
predictions = model.predict(new_tokens)
```

### 与PyTorch集成

```python
import torch
from geniml import GeniML

# 标记化数据
geniml = GeniML()
tokens = geniml.tokenize(intervals)

# 转换为PyTorch张量
tokens_tensor = torch.tensor(tokens, dtype=torch.float32)
labels_tensor = torch.tensor(labels, dtype=torch.long)

# 定义PyTorch模型
class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = torch.nn.Linear(1000, 512)
        self.fc2 = torch.nn.Linear(512, 256)
        self.fc3 = torch.nn.Linear(256, 2)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# 训练模型
model = Net()
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(100):
    optimizer.zero_grad()
    outputs = model(tokens_tensor)
    loss = criterion(outputs, labels_tensor)
    loss.backward()
    optimizer.step()
```

## 故障排除

**问题：标记化失败**
- 解决方案：检查区间格式，确保使用BED格式

**问题：模型训练很慢**
- 解决方案：使用GPU加速，减少batch size，或使用更简单的模型

**问题：过拟合**
- 解决方案：使用数据增强，增加dropout，或使用正则化

**问题：内存不足**
- 解决方案：减少batch size，使用更小的窗口大小，或使用数据流

**问题：预测不准确**
- 解决方案：增加训练数据，调整超参数，或尝试不同的模型架构

## 其他资源

- **GeniML文档**: https://geniml.readthedocs.io/
- **GeniML GitHub**: https://github.com/geniml/geniml
- **基因组机器学习教程**: https://www.genomeml.org/tutorials/
- **深度学习与基因组学**: https://www.deepgenomics.com/
