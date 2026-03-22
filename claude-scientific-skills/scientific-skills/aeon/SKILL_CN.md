---
name: aeon
description: 此技能应用于时间序列机器学习任务，包括分类、回归、聚类、预测、异常检测、分割和相似性搜索。在处理时间数据、序列模式或需要专门算法超出标准 ML 方法的时间索引观测时使用。特别适用于具有 scikit-learn 兼容 API 的单变量和多变量时间序列分析。
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# Aeon 时间序列机器学习

## 概述

Aeon 是一个与 scikit-learn 兼容的 Python 工具包，用于时间序列机器学习。它为分类、回归、聚类、预测、异常检测、分割和相似性搜索提供了最先进的算法。

## 何时使用此技能

在以下情况下应用此技能：
- 对时间序列数据进行分类或预测
- 检测时间序列中的异常或变化点
- 聚类相似的时间序列模式
- 预测未来值
- 查找重复模式（motif）或异常子序列（discord）
- 使用专门的距离度量比较时间序列
- 从时间数据中提取特征

## 安装

```bash
uv pip install aeon
```

## 核心功能

### 1. 时间序列分类

将时间序列分类为预定义的类别。有关完整的算法目录，请参阅 `references/classification.md`。

**快速开始：**
```python
from aeon.classification.convolution_based import RocketClassifier
from aeon.datasets import load_classification

# 加载数据
X_train, y_train = load_classification("GunPoint", split="train")
X_test, y_test = load_classification("GunPoint", split="test")

# 训练分类器
clf = RocketClassifier(n_kernels=10000)
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)
```

**算法选择：**
- **速度 + 性能**：`MiniRocketClassifier`、`Arsenal`
- **最大精度**：`HIVECOTEV2`、`InceptionTimeClassifier`
- **可解释性**：`ShapeletTransformClassifier`、`Catch22Classifier`
- **小数据集**：使用 DTW 距离的 `KNeighborsTimeSeriesClassifier`

### 2. 时间序列回归

从时间序列预测连续值。有关算法，请参阅 `references/regression.md`。

**快速开始：**
```python
from aeon.regression.convolution_based import RocketRegressor
from aeon.datasets import load_regression

X_train, y_train = load_regression("Covid3Month", split="train")
X_test, y_test = load_regression("Covid3Month", split="test")

reg = RocketRegressor()
reg.fit(X_train, y_train)
predictions = reg.predict(X_test)
```

### 3. 时间序列聚类

在没有标签的情况下对相似的时间序列进行分组。有关方法，请参阅 `references/clustering.md`。

**快速开始：**
```python
from aeon.clustering import TimeSeriesKMeans

clusterer = TimeSeriesKMeans(
    n_clusters=3,
    distance="dtw",
    averaging_method="ba"
)
labels = clusterer.fit_predict(X_train)
centers = clusterer.cluster_centers_
```

### 4. 预测

预测未来时间序列值。有关预测器，请参阅 `references/forecasting.md`。

**快速开始：**
```python
from aeon.forecasting.arima import ARIMA

forecaster = ARIMA(order=(1, 1, 1))
forecaster.fit(y_train)
y_pred = forecaster.predict(fh=[1, 2, 3, 4, 5])
```

### 5. 异常检测

识别异常模式或离群值。有关检测器，请参阅 `references/anomaly_detection.md`。

**快速开始：**
```python
from aeon.anomaly_detection import STOMP

detector = STOMP(window_size=50)
anomaly_scores = detector.fit_predict(y)

# 较高的分数表示异常
threshold = np.percentile(anomaly_scores, 95)
anomalies = anomaly_scores > threshold
```

### 6. 分割

将时间序列划分为具有变化点的区域。请参阅 `references/segmentation.md`。

**快速开始：**
```python
from aeon.segmentation import ClaSPSegmenter

segmenter = ClaSPSegmenter()
change_points = segmenter.fit_predict(y)
```

### 7. 相似性搜索

在时间序列内或跨时间序列查找相似模式。请参阅 `references/similarity_search.md`。

**快速开始：**
```python
from aeon.similarity_search import StompMotif

# 查找重复模式
motif_finder = StompMotif(window_size=50, k=3)
motifs = motif_finder.fit_predict(y)
```

## 特征提取和转换

转换时间序列以进行特征工程。请参阅 `references/transformations.md`。

**ROCKET 特征：**
```python
from aeon.transformations.collection.convolution_based import RocketTransformer

rocket = RocketTransformer()
X_features = rocket.fit_transform(X_train)

# 使用任何 sklearn 分类器的特征
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier()
clf.fit(X_features, y_train)
```

**统计特征：**
```python
from aeon.transformations.collection.feature_based import Catch22

catch22 = Catch22()
X_features = catch22.fit_transform(X_train)
```

**预处理：**
```python
from aeon.transformations.collection import MinMaxScaler, Normalizer

scaler = Normalizer()  # Z 标准化
X_normalized = scaler.fit_transform(X_train)
```

## 距离度量

专门的时间距离度量。有关完整目录，请参阅 `references/distances.md`。

**用法：**
```python
from aeon.distances import dtw_distance, dtw_pairwise_distance

# 单一距离
distance = dtw_distance(x, y, window=0.1)

# 成对距离
distance_matrix = dtw_pairwise_distance(X_train)

# 与分类器一起使用
from aeon.classification.distance_based import KNeighborsTimeSeriesClassifier

clf = KNeighborsTimeSeriesClassifier(
    n_neighbors=5,
    distance="dtw",
    distance_params={"window": 0.2}
)
```

**可用距离：**
- **弹性**：DTW、DDTW、WDTW、ERP、EDR、LCSS、TWE、MSM
- **锁定步长**：欧几里得、曼哈顿、闵可夫斯基
- **基于形状**：Shape DTW、SBD

## 深度学习网络

用于时间序列的神经架构。请参阅 `references/networks.md`。

**架构：**
- 卷积：`FCNClassifier`、`ResNetClassifier`、`InceptionTimeClassifier`
- 循环：`RecurrentNetwork`、`TCNNetwork`
- 自编码器：`AEFCNClusterer`、`AEResNetClusterer`

**用法：**
```python
from aeon.classification.deep_learning import InceptionTimeClassifier

clf = InceptionTimeClassifier(n_epochs=100, batch_size=32)
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
```

## 数据集和基准测试

加载标准基准并评估性能。请参阅 `references/datasets_benchmarking.md`。

**加载数据集：**
```python
from aeon.datasets import load_classification, load_regression

# 分类
X_train, y_train = load_classification("ArrowHead", split="train")

# 回归
X_train, y_train = load_regression("Covid3Month", split="train")
```

**基准测试：**
```python
from aeon.benchmarking import get_estimator_results

# 与已发布的结果比较
published = get_estimator_results("ROCKET", "GunPoint")
```

## 常见工作流程

### 分类流水线

```python
from aeon.transformations.collection import Normalizer
from aeon.classification.convolution_based import RocketClassifier
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('normalize', Normalizer()),
    ('classify', RocketClassifier())
])

pipeline.fit(X_train, y_train)
accuracy = pipeline.score(X_test, y_test)
```

### 特征提取 + 传统机器学习

```python
from aeon.transformations.collection import RocketTransformer
from sklearn.ensemble import GradientBoostingClassifier

# 提取特征
rocket = RocketTransformer()
X_train_features = rocket.fit_transform(X_train)
X_test_features = rocket.transform(X_test)

# 训练传统机器学习
clf = GradientBoostingClassifier()
clf.fit(X_train_features, y_train)
predictions = clf.predict(X_test_features)
```

### 异常检测与可视化

```python
from aeon.anomaly_detection import STOMP
import matplotlib.pyplot as plt

detector = STOMP(window_size=50)
scores = detector.fit_predict(y)

plt.figure(figsize=(15, 5))
plt.subplot(2, 1, 1)
plt.plot(y, label='Time Series')
plt.subplot(2, 1, 2)
plt.plot(scores, label='Anomaly Scores', color='red')
plt.axhline(np.percentile(scores, 95), color='k', linestyle='--')
plt.show()
```

## 最佳实践

### 数据准备

1. **标准化**：大多数算法受益于 z 标准化
   ```python
   from aeon.transformations.collection import Normalizer
   normalizer = Normalizer()
   X_train = normalizer.fit_transform(X_train)
   X_test = normalizer.transform(X_test)
   ```

2. **处理缺失值**：分析前进行插补
   ```python
   from aeon.transformations.collection import SimpleImputer
   imputer = SimpleImputer(strategy='mean')
   X_train = imputer.fit_transform(X_train)
   ```

3. **检查数据格式**：Aeon 期望形状为 `(n_samples, n_channels, n_timepoints)`

### 模型选择

1. **从简单开始**：在深度学习之前从 ROCKET 变体开始
2. **使用验证**：拆分训练数据以进行超参数调整
3. **比较基线**：与简单方法（1-NN 欧几里得、朴素）进行测试
4. **考虑资源**：ROCKET 用于速度，如果可用 GPU 则使用深度学习

### 算法选择指南

**用于快速原型设计：**
- 分类：`MiniRocketClassifier`
- 回归：`MiniRocketRegressor`
- 聚类：使用欧几里得的 `TimeSeriesKMeans`

**用于最大精度：**
- 分类：`HIVECOTEV2`、`InceptionTimeClassifier`
- 回归：`InceptionTimeRegressor`
- 预测：`ARIMA`、`TCNForecaster`

**用于可解释性：**
- 分类：`ShapeletTransformClassifier`、`Catch22Classifier`
- 特征：`Catch22`、`TSFresh`

**用于小数据集：**
- 基于距离：使用 DTW 的 `KNeighborsTimeSeriesClassifier`
- 避免：深度学习（需要大数据）

## 参考文档

`references/` 中提供详细信息：
- `classification.md` - 所有分类算法
- `regression.md` - 回归方法
- `clustering.md` - 聚类算法
- `forecasting.md` - 预测方法
- `anomaly_detection.md` - 异常检测方法
- `segmentation.md` - 分割算法
- `similarity_search.md` - 模式匹配和 motif 发现
- `transformations.md` - 特征提取和预处理
- `distances.md` - 时间序列距离度量
- `networks.md` - 深度学习架构
- `datasets_benchmarking.md` - 数据加载和评估工具

## 其他资源

- 文档：https://www.aeon-toolkit.org/
- GitHub：https://github.com/aeon-toolkit/aeon
- 示例：https://www.aeon-toolkit.org/en/stable/examples.html
- API 参考：https://www.aeon-toolkit.org/en/stable/api_reference.html
