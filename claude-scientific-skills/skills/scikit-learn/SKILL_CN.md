---
name: scikit-learn
description: 使用scikit-learn进行Python机器学习。当使用监督学习（分类、回归）、无监督学习（聚类、降维）、模型评估、超参数调优、预处理或构建ML管道时使用。提供算法、预处理技术、管道和最佳实践的综合参考文档。
license: BSD-3-Clause license
allowed-tools: Read Write Edit Bash
compatibility: Requires Python 3.11+ and scikit-learn 1.7+. NumPy and SciPy are required dependencies. Optional matplotlib/seaborn for bundled example scripts that save plots.
metadata:
  version: "1.1"
  skill-author: K-Dense Inc.
---






# Scikit-learn

## 概述

本技能提供使用 scikit-learn 进行机器学习任务的全面指导，scikit-learn 是业界标准的 Python 经典机器学习库。适用于分类、回归、聚类、降维、预处理、模型评估以及构建生产级 ML 流水线。

## 安装

```bash
# 使用 uv 安装 scikit-learn
uv pip install scikit-learn

# 可选：安装可视化依赖
uv pip install matplotlib seaborn

# 通常与以下库一起使用
uv pip install pandas numpy
```

## 何时使用本技能

在以下情况下使用 scikit-learn 技能：

- 构建分类或回归模型
- 执行聚类或降维
- 为机器学习预处理和转换数据
- 使用交叉验证评估模型性能
- 使用网格搜索或随机搜索进行超参数调优
- 为生产工作流创建 ML 流水线
- 为某项任务比较不同算法
- 处理结构化（表格）数据和文本数据
- 需要可解释的经典机器学习方法

## 快速入门

### 分类示例

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# 划分数据
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 预处理
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 训练模型
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# 评估
y_pred = model.predict(X_test_scaled)
print(classification_report(y_test, y_pred))
```

### 混合数据完整流水线

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingClassifier

# 定义特征类型
numeric_features = ['age', 'income']
categorical_features = ['gender', 'occupation']

# 创建预处理流水线
numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# 组合转换器
preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features)
])

# 完整流水线
model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', GradientBoostingClassifier(random_state=42))
])

# 拟合与预测
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
```

## 核心能力

### 1. 监督学习

用于分类和回归任务的全面算法。

**关键算法：**
- **线性模型**：Logistic Regression、Linear Regression、Ridge、Lasso、ElasticNet
- **树模型**：Decision Trees、Random Forest、Gradient Boosting
- **支持向量机**：SVC、SVR（支持多种核函数）
- **集成方法**：AdaBoost、Voting、Stacking
- **神经网络**：MLPClassifier、MLPRegressor
- **其他**：Naive Bayes、K-Nearest Neighbors

**适用场景：**
- 分类：预测离散类别（垃圾邮件检测、图像分类、欺诈检测）
- 回归：预测连续值（价格预测、需求预测）

**参见：** `references/supervised_learning.md` 获取详细算法文档、参数和用法示例。

### 2. 无监督学习

通过聚类和降维发现无标签数据中的模式。

**聚类算法：**
- **基于划分**：K-Means、MiniBatchKMeans
- **基于密度**：DBSCAN、HDBSCAN、OPTICS
- **层次聚类**：AgglomerativeClustering
- **概率模型**：Gaussian Mixture Models
- **其他**：MeanShift、SpectralClustering、BIRCH

**降维：**
- **线性方法**：PCA、TruncatedSVD、NMF
- **流形学习**：t-SNE、UMAP、Isomap、LLE
- **特征提取**：FastICA、LatentDirichletAllocation

**适用场景：**
- 客户细分、异常检测、数据可视化
- 降低特征维度、探索性数据分析
- 主题建模、图像压缩

**参见：** `references/unsupervised_learning.md` 获取详细文档。

### 3. 模型评估与选择

用于稳健模型评估、交叉验证和超参数调优的工具。

**交叉验证策略：**
- KFold、StratifiedKFold（分类）
- TimeSeriesSplit（时序数据）
- GroupKFold（分组样本）

**超参数调优：**
- GridSearchCV（穷举搜索）
- RandomizedSearchCV（随机采样）
- HalvingGridSearchCV（逐次折半）

**评估指标：**
- **分类**：accuracy、precision、recall、F1-score、ROC AUC、confusion matrix
- **回归**：MSE、RMSE、MAE、R²、MAPE
- **聚类**：silhouette score、Calinski-Harabasz、Davies-Bouldin

**适用场景：**
- 客观比较模型性能
- 寻找最优超参数
- 通过交叉验证防止过拟合
- 使用学习曲线理解模型行为

**参见：** `references/model_evaluation.md` 获取全面的指标和调优策略。

### 4. 数据预处理

将原始数据转换为适合机器学习的格式。

**缩放与归一化：**
- StandardScaler（零均值，单位方差）
- MinMaxScaler（有界范围）
- RobustScaler（对异常值稳健）
- Normalizer（样本级归一化）

**编码分类变量：**
- OneHotEncoder（名义类别）
- OrdinalEncoder（有序类别）
- LabelEncoder（目标编码）

**处理缺失值：**
- SimpleImputer（均值、中位数、众数）
- KNNImputer（K 近邻）
- IterativeImputer（多元插补）

**特征工程：**
- PolynomialFeatures（交互项）
- KBinsDiscretizer（分箱）
- 特征选择（RFE、SelectKBest、SelectFromModel）

**适用场景：**
- 训练任何需要缩放特征的算法之前（SVM、KNN、Neural Networks）
- 将分类变量转换为数值格式
- 系统性地处理缺失数据
- 为线性模型创建非线性特征

**参见：** `references/preprocessing.md` 获取详细预处理技术。

### 5. 流水线与组合

构建可复现、生产级的 ML 工作流。

**关键组件：**
- **Pipeline**：按顺序链接转换器和估计器
- **ColumnTransformer**：对不同列应用不同的预处理
- **FeatureUnion**：并行组合多个转换器
- **TransformedTargetRegressor**：转换目标变量

**优势：**
- 防止交叉验证中的数据泄漏
- 简化代码并提高可维护性
- 支持联合超参数调优
- 确保训练与预测之间的一致性

**适用场景：**
- 生产工作流始终使用 Pipeline
- 混合数值和分类特征时（使用 ColumnTransformer）
- 在交叉验证中包含预处理步骤时
- 超参数调优包含预处理参数时

**参见：** `references/pipelines_and_composition.md` 获取全面的流水线模式。

## 示例脚本

### 分类流水线

运行包含预处理、模型比较、超参数调优和评估的完整分类工作流：

```bash
python scripts/classification_pipeline.py
```

该脚本演示：
- 处理混合数据类型（数值和分类）
- 使用交叉验证进行模型比较
- 使用 GridSearchCV 进行超参数调优
- 使用多个指标进行全面评估
- 特征重要性分析

### 聚类分析

执行聚类分析并进行算法比较和可视化：

```bash
python scripts/clustering_analysis.py
```

该脚本演示：
- 寻找最优聚类数（肘部法、轮廓分析）
- 比较多种聚类算法（K-Means、DBSCAN、Agglomerative、Gaussian Mixture）
- 在无真实标签的情况下评估聚类质量
- 使用 PCA 投影可视化结果

## 参考文档

本技能包含全面的参考文件，用于深入特定主题：

### 快速参考
**文件：** `references/quick_reference.md`
- 常见导入模式和安装说明
- 常见任务的快速工作流模板
- 算法选择速查表
- 常见模式和注意事项
- 性能优化技巧

### 监督学习
**文件：** `references/supervised_learning.md`
- 线性模型（回归和分类）
- 支持向量机
- 决策树和集成方法
- K-Nearest Neighbors、Naive Bayes、Neural Networks
- 算法选择指南

### 无监督学习
**文件：** `references/unsupervised_learning.md`
- 所有聚类算法及其参数和用例
- 降维技术
- 异常和新奇检测
- Gaussian Mixture Models
- 方法选择指南

### 模型评估
**文件：** `references/model_evaluation.md`
- 交叉验证策略
- 超参数调优方法
- 分类、回归和聚类指标
- 学习和验证曲线
- 模型选择最佳实践

### 预处理
**文件：** `references/preprocessing.md`
- 特征缩放和归一化
- 编码分类变量
- 缺失值插补
- 特征工程技术
- 自定义转换器

### 流水线与组合
**文件：** `references/pipelines_and_composition.md`
- Pipeline 构建与使用
- 用于混合数据类型的 ColumnTransformer
- 用于并行转换的 FeatureUnion
- 完整的端到端示例
- 最佳实践

## 常见工作流

### 构建分类模型

1. **加载并探索数据**
   ```python
   import pandas as pd
   df = pd.read_csv('data.csv')
   X = df.drop('target', axis=1)
   y = df['target']
   ```

2. **使用分层划分数据**
   ```python
   from sklearn.model_selection import train_test_split
   X_train, X_test, y_train, y_test = train_test_split(
       X, y, test_size=0.2, stratify=y, random_state=42
   )
   ```

3. **创建预处理流水线**
   ```python
   from sklearn.pipeline import Pipeline
   from sklearn.preprocessing import StandardScaler
   from sklearn.compose import ColumnTransformer

   # 分别处理数值和分类特征
   preprocessor = ColumnTransformer([
       ('num', StandardScaler(), numeric_features),
       ('cat', OneHotEncoder(), categorical_features)
   ])
   ```

4. **构建完整流水线**
   ```python
   model = Pipeline([
       ('preprocessor', preprocessor),
       ('classifier', RandomForestClassifier(random_state=42))
   ])
   ```

5. **调优超参数**
   ```python
   from sklearn.model_selection import GridSearchCV

   param_grid = {
       'classifier__n_estimators': [100, 200],
       'classifier__max_depth': [10, 20, None]
   }

   grid_search = GridSearchCV(model, param_grid, cv=5)
   grid_search.fit(X_train, y_train)
   ```

6. **在测试集上评估**
   ```python
   from sklearn.metrics import classification_report

   best_model = grid_search.best_estimator_
   y_pred = best_model.predict(X_test)
   print(classification_report(y_test, y_pred))
   ```

### 执行聚类分析

1. **预处理数据**
   ```python
   from sklearn.preprocessing import StandardScaler

   scaler = StandardScaler()
   X_scaled = scaler.fit_transform(X)
   ```

2. **寻找最优聚类数**
   ```python
   from sklearn.cluster import KMeans
   from sklearn.metrics import silhouette_score

   scores = []
   for k in range(2, 11):
       kmeans = KMeans(n_clusters=k, random_state=42)
       labels = kmeans.fit_predict(X_scaled)
       scores.append(silhouette_score(X_scaled, labels))

   optimal_k = range(2, 11)[np.argmax(scores)]
   ```

3. **应用聚类**
   ```python
   model = KMeans(n_clusters=optimal_k, random_state=42)
   labels = model.fit_predict(X_scaled)
   ```

4. **使用降维可视化**
   ```python
   from sklearn.decomposition import PCA

   pca = PCA(n_components=2)
   X_2d = pca.fit_transform(X_scaled)

   plt.scatter(X_2d[:, 0], X_2d[:, 1], c=labels, cmap='viridis')
   ```

## 最佳实践

### 始终使用 Pipeline
Pipeline 可防止数据泄漏并确保一致性：
```python
# 良好：在流水线中进行预处理
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression())
])

# 不良：在流水线外预处理（可能导致信息泄漏）
X_scaled = StandardScaler().fit_transform(X)
```

### 仅在训练数据上拟合
切勿在测试数据上拟合：
```python
# 良好
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # 仅转换

# 不良
scaler = StandardScaler()
X_all_scaled = scaler.fit_transform(np.vstack([X_train, X_test]))
```

### 对分类任务使用分层划分
保持类别分布：
```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
```

### 设置随机种子以确保可复现性
```python
model = RandomForestClassifier(n_estimators=100, random_state=42)
```

### 选择合适的评估指标
- 平衡数据：Accuracy、F1-score
- 不平衡数据：Precision、Recall、ROC AUC、Balanced Accuracy
- 成本敏感：定义自定义评分器

### 在需要时缩放特征
需要特征缩放的算法：
- SVM、KNN、Neural Networks
- PCA、带正则化的 Linear/Logistic Regression
- K-Means 聚类

不需要缩放的算法：
- 树模型（Decision Trees、Random Forest、Gradient Boosting）
- Naive Bayes

## 常见问题排查

### ConvergenceWarning
**问题：** 模型未收敛
**解决方案：** 增加 `max_iter` 或缩放特征
```python
model = LogisticRegression(max_iter=1000)
```

### 测试集性能差
**问题：** 过拟合
**解决方案：** 使用正则化、交叉验证或更简单的模型
```python
# 添加正则化
model = Ridge(alpha=1.0)

# 使用交叉验证
scores = cross_val_score(model, X, y, cv=5)
```

### 大数据集内存错误
**解决方案：** 使用专为大数据设计的算法
```python
# 大数据集使用 SGD
from sklearn.linear_model import SGDClassifier
model = SGDClassifier()

# 或聚类使用 MiniBatchKMeans
from sklearn.cluster import MiniBatchKMeans
model = MiniBatchKMeans(n_clusters=8, batch_size=100)
```

## 额外资源

- 官方文档：https://scikit-learn.org/stable/
- 用户指南：https://scikit-learn.org/stable/user_guide.html
- API 参考：https://scikit-learn.org/stable/api/index.html
- 示例库：https://scikit-learn.org/stable/auto_examples/index.html
