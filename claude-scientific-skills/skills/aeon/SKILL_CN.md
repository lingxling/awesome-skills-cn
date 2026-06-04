---
name: aeon
description: 此技能应用于时间序列机器学习任务，包括分类、回归、聚类、预测、异常检测、分割和相似性搜索。当处理时间数据、序列模式或需要标准机器学习方法之外的专业算法的时间索引观察时使用。特别适合使用与scikit-learn兼容API的单变量和多变量时间序列分析。
license: BSD-3-Clause license
allowed-tools: Read Write Edit Bash
compatibility: Requires Python 3.10+ and the aeon package (uv pip install). Optional aeon[all_extras] for deep learning and extended dependencies.
metadata:
  version: "1.0"
  skill-author: K-Dense Inc.
---






# Aeon 时间序列机器学习

## 概述

Aeon 是一个与 scikit-learn 兼容的 Python 时间序列机器学习工具包（[aeon-toolkit.org](https://www.aeon-toolkit.org/)）。它提供分类、回归、聚类、预测、异常检测、分割、相似性搜索、距离、转换、基准测试和可视化的算法——具有一致的估算器 API。

**版本说明：** 示例针对 **aeon 1.x**（稳定文档：v1.4.0，2026年3月）。v1.0 版本重新设计了预测和转换；导入路径与 aeon 0.x/sktime 时代的代码不同。

## 何时使用此技能

在以下情况下应用此技能：
- 对时间序列数据进行分类或预测
- 检测时间序列中的异常或变化点
- 对相似的时间序列模式进行聚类
- 预测未来值
- 查找重复模式（motif）或异常子序列（discords）
- 使用专门的距离度量比较时间序列
- 从时间数据中提取特征

## 安装

需要 **Python 3.10+**（推荐 3.11+）。为可重现性锁定 1.x 版本：

```bash
uv pip install "aeon>=1.4,<2"
```

用于深度学习预测器/分类器和其他可选估算器：

```bash
uv pip install "aeon[all_extras]>=1.4,<2"
```

在 zsh 中，给 extras 加引号：`uv pip install "aeon[all_extras]>=1.4,<2"`。

### 实验模块

上游将 **预测**、**异常检测**、**分割**、**相似性搜索** 和 **可视化** 视为实验模块——接口可能在次版本之间变化。在生产管道中优先使用稳定模块（分类、回归、聚类、距离、转换），除非您需要这些任务。

## 核心能力

### 1. 时间序列分类

将时间序列分类到预定义类别中。参见 `references/classification.md` 获取完整的算法目录。

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
- **最高准确度**：`HIVECOTEV2`、`InceptionTimeClassifier`
- **可解释性**：`ShapeletTransformClassifier`、`Catch22Classifier`
- **小数据集**：`KNeighborsTimeSeriesClassifier` 配合 DTW 距离

### 2. 时间序列回归

从时间序列预测连续值。参见 `references/regression.md` 获取算法。

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

在没有标签的情况下对相似的时间序列进行分组。参见 `references/clustering.md` 获取方法。

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

预测未来的时间序列值（aeon 1.x 中的实验模块）。参见 `references/forecasting.md` 获取预测器。

**快速开始：**
```python
import numpy as np
from aeon.forecasting import NaiveForecaster
from aeon.forecasting.stats import ARIMA

y_train = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])

# 在构造函数中设置 horizon；predict 传递序列用于预测
naive = NaiveForecaster(strategy="last", horizon=5)
naive.fit(y_train)
y_pred = naive.predict(y_train)

# ARIMA 使用 p/d/q（不是 order=）；通过 iterative_forecast 进行多步预测
arima = ARIMA(p=1, d=1, q=1)
arima.fit(y_train)
y_pred = arima.iterative_forecast(y_train, prediction_horizon=5)
```

### 5. 异常检测

识别异常模式或离群值。参见 `references/anomaly_detection.md` 获取检测器。

**快速开始：**
```python
from aeon.anomaly_detection import STOMP

detector = STOMP(window_size=50)
anomaly_scores = detector.fit_predict(y)

# 分数越高表示异常
threshold = np.percentile(anomaly_scores, 95)
anomalies = anomaly_scores > threshold
```

### 6. 分割

用变化点将时间序列分割成区域。参见 `references/segmentation.md`。

**快速开始：**
```python
from aeon.segmentation import ClaSPSegmenter

segmenter = ClaSPSegmenter()
change_points = segmenter.fit_predict(y)
```

### 7. 相似性搜索

在时间序列内或之间找到相似的模式。参见 `references/similarity_search.md`。

**快速开始：**
```python
from aeon.similarity_search import StompMotif

# 查找重复模式
motif_finder = StompMotif(window_size=50, k=3)
motifs = motif_finder.fit_predict(y)
```

## 特征提取和转换

转换时间序列进行特征工程。参见 `references/transformations.md`。

**ROCKET 特征：**
```python
from aeon.transformations.collection.convolution_based import RocketTransformer

rocket = RocketTransformer()
X_features = rocket.fit_transform(X_train)

# 使用特征与任何 sklearn 分类器
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

scaler = Normalizer()  # Z-归一化
X_normalized = scaler.fit_transform(X_train)
```

## 距离度量

专门的时间距离度量。参见 `references/distances.md` 获取完整的目录。

**用法：**
```python
from aeon.distances import dtw_distance, dtw_pairwise_distance

# 单个距离
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
- **锁定步**：欧几里得、曼哈顿、明可夫斯基
- **基于形状**：Shape DTW、SBD

## 深度学习网络

时间序列的神经网络架构。参见 `references/networks.md`。

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

加载标准基准并评估性能。参见 `references/datasets_benchmarking.md`。

**加载数据集：**
```python
from aeon.datasets import load_classification, load_gunpoint, load_regression

# 分类（通用加载器或数据集特定辅助函数）
X_train, y_train = load_classification("GunPoint", split="train")
X_train, y_train = load_gunpoint(split="train")  # 相同的 UCR 数据集

# 回归
X_train, y_train = load_regression("Covid3Month", split="train")
```

**基准测试：**
```python
from aeon.benchmarking import get_estimator_results

# 与已发布结果比较
published = get_estimator_results("ROCKET", "GunPoint")
```

## 常见工作流程

### 分类管道

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

1. **归一化**：大多数算法受益于 z-归一化
   ```python
   from aeon.transformations.collection import Normalizer
   normalizer = Normalizer()
   X_train = normalizer.fit_transform(X_train)
   X_test = normalizer.transform(X_test)
   ```

2. **处理缺失值**：在分析前进行插补
   ```python
   from aeon.transformations.collection import SimpleImputer
   imputer = SimpleImputer(strategy='mean')
   X_train = imputer.fit_transform(X_train)
   ```

### 模型选择

1. **从简单开始**：先尝试基线模型（如朴素分类器）
2. **考虑数据特性**：根据时间序列的长度、维度和特征选择
3. **交叉验证**：使用时间序列交叉验证确保可靠性
4. **评估指标**：根据任务选择合适的指标（准确率、F1、AUC等）

### 算法选择指南

| 任务 | 推荐算法 |
|------|----------|
| 分类 | TimeSeriesForest, RocketClassifier, InceptionTime |
| 回归 | DummyRegressor, RandomForest, XGBoost |
| 聚类 | TimeSeriesKMeans, KernelKMeans |
| 预测 | ARIMA, ExponentialSmoothing, Theta |
| 异常检测 | IsolationForest, OneClassSVM |
| 分割 | ClaSP, WindowSegmenter |

## 参考文档

- [aeon 文档](https://www.aeon-toolkit.org/)
- [API 参考](https://aeon-toolkit.org/en/latest/api.html)
- [示例笔记本](https://aeon-toolkit.org/en/latest/examples.html)

## 其他资源

- [GitHub 仓库](https://github.com/aeon-toolkit/aeon)
- [论文和引用](https://aeon-toolkit.org/en/latest/refs.html)
- [贡献指南](https://aeon-toolkit.org/en/latest/contributing.html)
