---
name: umap-learn
description: UMAP降维。用于2D/3D可视化、聚类预处理（HDBSCAN）、监督/参数化UMAP的快速非线性流形学习，适用于高维数据。
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# UMAP-Learn

## 概述

UMAP（Uniform Manifold Approximation and Projection）是一种用于可视化和一般非线性降维的降维技术。应用此技能可获得快速、可扩展的嵌入，保留局部和全局结构，支持监督学习和聚类预处理。

## 快速开始

### 安装

```bash
uv pip install umap-learn
```

### 基本用法

UMAP遵循scikit-learn约定，可作为t-SNE或PCA的直接替代品使用。

```python
import umap
from sklearn.preprocessing import StandardScaler

# 准备数据（标准化至关重要）
scaled_data = StandardScaler().fit_transform(data)

# 方法1：单步（拟合和转换）
embedding = umap.UMAP().fit_transform(scaled_data)

# 方法2：分开步骤（用于重用训练模型）
reducer = umap.UMAP(random_state=42)
reducer.fit(scaled_data)
embedding = reducer.embedding_  # 访问训练后的嵌入
```

**关键预处理要求：** 在应用UMAP之前，始终将特征标准化到可比较的尺度，以确保跨维度的平等权重。

### 典型工作流程

```python
import umap
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# 1. 预处理数据
scaler = StandardScaler()
scaled_data = scaler.fit_transform(raw_data)

# 2. 创建并拟合UMAP
reducer = umap.UMAP(
    n_neighbors=15,
    min_dist=0.1,
    n_components=2,
    metric='euclidean',
    random_state=42
)
embedding = reducer.fit_transform(scaled_data)

# 3. 可视化
plt.scatter(embedding[:, 0], embedding[:, 1], c=labels, cmap='Spectral', s=5)
plt.colorbar()
plt.title('UMAP Embedding')
plt.show()
```

## 参数调优指南

UMAP有四个主要参数控制嵌入行为。理解这些参数对于有效使用至关重要。

### n_neighbors（默认：15）

**目的：** 平衡嵌入中的局部与全局结构。

**工作原理：** 控制UMAP在学习流形结构时检查的局部邻域大小。

**不同值的效果：**
- **低值（2-5）：** 强调精细的局部细节，但可能将数据分割为不相连的组件
- **中等值（15-20）：** 平衡局部结构和全局关系（推荐起点）
- **高值（50-200）：** 优先考虑广泛的拓扑结构，牺牲细粒度细节

**建议：** 从15开始，根据结果调整。增加以获得更多全局结构，减少以获得更多局部细节。

### min_dist（默认：0.1）

**目的：** 控制低维空间中点的聚集程度。

**工作原理：** 设置输出表示中点之间允许的最小距离。

**不同值的效果：**
- **低值（0.0-0.1）：** 创建用于聚类的聚集嵌入；揭示精细的拓扑细节
- **高值（0.5-0.99）：** 防止紧密堆积；强调广泛的拓扑保存而非局部结构

**建议：** 聚类应用使用0.0，可视化使用0.1-0.3，松散结构使用0.5+。

### n_components（默认：2）

**目的：** 确定嵌入输出空间的维度。

**关键特性：** 与t-SNE不同，UMAP在嵌入维度上扩展性良好，可用于超出可视化的场景。

**常见用途：**
- **2-3维：** 可视化
- **5-10维：** 聚类预处理（比2D更好地保留密度）
- **10-50维：** 下游ML模型的特征工程

**建议：** 可视化使用2，聚类使用5-10，ML管道使用更高维度。

### metric（默认：'euclidean'）

**目的：** 指定输入数据点之间距离的计算方式。

**支持的度量：**
- **Minkowski变体：** euclidean, manhattan, chebyshev
- **空间度量：** canberra, braycurtis, haversine
- **相关度量：** cosine, correlation（适用于文本/文档嵌入）
- **二进制数据度量：** hamming, jaccard, dice, russellrao, kulsinski, rogerstanimoto, sokalmichener, sokalsneath, yule
- **自定义度量：** 通过Numba的用户定义距离函数

**建议：** 数值数据使用euclidean，文本/文档向量使用cosine，二进制数据使用hamming。

### 参数调优示例

```python
# 强调局部结构的可视化
umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2, metric='euclidean')

# 聚类预处理
umap.UMAP(n_neighbors=30, min_dist=0.0, n_components=10, metric='euclidean')

# 文档嵌入
umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2, metric='cosine')

# 保存全局结构
umap.UMAP(n_neighbors=100, min_dist=0.5, n_components=2, metric='euclidean')
```

## 监督和半监督降维

UMAP支持合并标签信息以指导嵌入过程，实现类分离同时保留内部结构。

### 监督UMAP

拟合时通过`y`参数传递目标标签：

```python
# 监督降维
embedding = umap.UMAP().fit_transform(data, y=labels)
```

**关键优势：**
- 实现清晰分离的类
- 保留每个类内的内部结构
- 维护类之间的全局关系

**使用场景：** 当你有标记数据并希望分离已知类同时保持有意义的点嵌入时。

### 半监督UMAP

对于部分标签，按照scikit-learn约定用`-1`标记未标记点：

```python
# 创建半监督标签
semi_labels = labels.copy()
semi_labels[unlabeled_indices] = -1

# 用部分标签拟合
embedding = umap.UMAP().fit_transform(data, y=semi_labels)
```

**使用场景：** 当标记成本高或你有比标签更多的数据时。

### 使用UMAP进行度量学习

在标记数据上训练监督嵌入，然后应用于新的未标记数据：

```python
# 在标记数据上训练
mapper = umap.UMAP().fit(train_data, train_labels)

# 转换未标记的测试数据
test_embedding = mapper.transform(test_data)

# 用作下游分类器的特征工程
from sklearn.svm import SVC
clf = SVC().fit(mapper.embedding_, train_labels)
predictions = clf.predict(test_embedding)
```

**使用场景：** 用于机器学习管道中的监督特征工程。

## UMAP用于聚类

UMAP作为基于密度的聚类算法（如HDBSCAN）的有效预处理，克服了维度灾难。

### 聚类最佳实践

**关键原则：** 为聚类配置UMAP与为可视化配置不同。

**推荐参数：**
- **n_neighbors：** 增加到~30（默认15过于局部，可能创建人工细粒度聚类）
- **min_dist：** 设置为0.0（将点密集地打包在聚类内以获得更清晰的边界）
- **n_components：** 使用5-10维（保持性能同时比2D更好地保留密度）

### 聚类工作流程

```python
import umap
import hdbscan
from sklearn.preprocessing import StandardScaler

# 1. 预处理数据
scaled_data = StandardScaler().fit_transform(data)

# 2. 使用聚类优化参数的UMAP
reducer = umap.UMAP(
    n_neighbors=30,
    min_dist=0.0,
    n_components=10,  # 高于2以更好地保留密度
    metric='euclidean',
    random_state=42
)
embedding = reducer.fit_transform(scaled_data)

# 3. 应用HDBSCAN聚类
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=15,
    min_samples=5,
    metric='euclidean'
)
labels = clusterer.fit_predict(embedding)

# 4. 评估
from sklearn.metrics import adjusted_rand_score
score = adjusted_rand_score(true_labels, labels)
print(f"Adjusted Rand Score: {score:.3f}")
print(f"Number of clusters: {len(set(labels)) - (1 if -1 in labels else 0)}")
print(f"Noise points: {sum(labels == -1)}")
```

### 聚类后的可视化

```python
# 创建用于可视化的2D嵌入（与聚类分开）
vis_reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2, random_state=42)
vis_embedding = vis_reducer.fit_transform(scaled_data)

# 用聚类标签绘图
import matplotlib.pyplot as plt
plt.scatter(vis_embedding[:, 0], vis_embedding[:, 1], c=labels, cmap='Spectral', s=5)
plt.colorbar()
plt.title('UMAP Visualization with HDBSCAN Clusters')
plt.show()
```

**重要警告：** UMAP不完全保留密度，可能会创建人工聚类划分。始终验证和探索结果聚类。

## 转换新数据

UMAP通过其`transform()`方法实现新数据的预处理，允许训练模型将未见过的数据投影到学习的嵌入空间中。

### 基本转换用法

```python
# 在训练数据上训练
trans = umap.UMAP(n_neighbors=15, random_state=42).fit(X_train)

# 转换测试数据
test_embedding = trans.transform(X_test)
```

### 与机器学习管道集成

```python
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import umap

# 分割数据
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2)

# 预处理
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 训练UMAP
reducer = umap.UMAP(n_components=10, random_state=42)
X_train_embedded = reducer.fit_transform(X_train_scaled)
X_test_embedded = reducer.transform(X_test_scaled)

# 在嵌入上训练分类器
clf = SVC()
clf.fit(X_train_embedded, y_train)
accuracy = clf.score(X_test_embedded, y_test)
print(f"Test accuracy: {accuracy:.3f}")
```

### 重要考虑因素

**数据一致性：** 转换方法假设高维空间中的整体分布在训练和测试数据之间是一致的。当此假设不成立时，考虑使用参数化UMAP。

**性能：** 转换操作效率高（通常<1秒），尽管由于Numba JIT编译，初始调用可能较慢。

**Scikit-learn兼容性：** UMAP遵循标准sklearn约定，在管道中无缝工作：

```python
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('umap', umap.UMAP(n_components=10)),
    ('classifier', SVC())
])

pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)
```

## 高级功能

### 参数化UMAP

参数化UMAP用学习的神经网络映射函数替换直接嵌入优化。

**与标准UMAP的关键区别：**
- 使用TensorFlow/Keras训练编码器网络
- 实现新数据的高效转换
- 支持通过解码器网络重建（逆变换）
- 允许自定义架构（图像的CNN，序列的RNN）

**安装：**
```bash
uv pip install umap-learn[parametric_umap]
# 需要TensorFlow 2.x
```

**基本用法：**
```python
from umap.parametric_umap import ParametricUMAP

# 默认架构（3层100神经元全连接网络）
embedder = ParametricUMAP()
embedding = embedder.fit_transform(data)

# 高效转换新数据
new_embedding = embedder.transform(new_data)
```

**自定义架构：**
```python
import tensorflow as tf

# 定义自定义编码器
encoder = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(input_dim,)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(2)  # 输出维度
])

embedder = ParametricUMAP(encoder=encoder, dims=(input_dim,))
embedding = embedder.fit_transform(data)
```

**何时使用参数化UMAP：**
- 需要训练后新数据的高效转换
- 需要重建能力（逆变换）
- 想要将UMAP与自编码器结合
- 处理受益于专门架构的复杂数据类型（图像、序列）

**何时使用标准UMAP：**
- 需要简单性和快速原型设计
- 数据集小且计算效率不关键
- 不需要为未来数据学习变换

### 逆变换

逆变换允许从低维嵌入重建高维数据。

**基本用法：**
```python
reducer = umap.UMAP()
embedding = reducer.fit_transform(data)

# 从嵌入坐标重建高维数据
reconstructed = reducer.inverse_transform(embedding)
```

**重要限制：**
- 计算密集型操作
- 在嵌入凸包外效果差
- 在聚类之间有间隙的区域精度降低

**用例：**
- 理解嵌入数据的结构
- 可视化聚类之间的平滑过渡
- 探索数据点之间的插值
- 在嵌入空间中生成合成样本

**示例：探索嵌入空间：**
```python
import numpy as np

# 在嵌入空间创建点网格
x = np.linspace(embedding[:, 0].min(), embedding[:, 0].max(), 10)
y = np.linspace(embedding[:, 1].min(), embedding[:, 1].max(), 10)
xx, yy = np.meshgrid(x, y)
grid_points = np.c_[xx.ravel(), yy.ravel()]

# 从网格重建样本
reconstructed_samples = reducer.inverse_transform(grid_points)
```

### AlignedUMAP

用于分析时间或相关数据集（例如，时间序列实验、批次数据）：

```python
from umap import AlignedUMAP

# 相关数据集列表
datasets = [day1_data, day2_data, day3_data]

# 创建对齐的嵌入
mapper = AlignedUMAP().fit(datasets)
aligned_embeddings = mapper.embeddings_  # 嵌入列表
```

**使用场景：** 比较相关数据集的嵌入，同时保持一致的坐标系。

## 可重现性

为确保可重现的结果，始终设置`random_state`参数：

```python
reducer = umap.UMAP(random_state=42)
```

UMAP使用随机优化，因此没有固定随机状态的情况下，运行之间的结果会略有不同。

## 常见问题和解决方案

**问题：** 断开的组件或碎片化的聚类
- **解决方案：** 增加`n_neighbors`以强调更多全局结构

**问题：** 聚类过于分散或分离不良
- **解决方案：** 减少`min_dist`以允许更紧密的堆积

**问题：** 聚类结果不佳
- **解决方案：** 使用聚类特定参数（n_neighbors=30, min_dist=0.0, n_components=5-10）

**问题：** 转换结果与训练显著不同
- **解决方案：** 确保测试数据分布与训练匹配，或使用参数化UMAP

**问题：** 大型数据集上性能缓慢
- **解决方案：** 设置`low_memory=True`（默认），或考虑先使用PCA进行降维

**问题：** 所有点折叠到单个聚类
- **解决方案：** 检查数据预处理（确保适当缩放），增加`min_dist`

## 资源

### references/

包含详细的API文档：
- `api_reference.md`：完整的UMAP类参数和方法

当需要详细的参数信息或高级方法使用时，加载这些参考资料。