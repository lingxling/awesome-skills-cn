---
name: exploratory-data-analysis
description: 探索性数据分析（EDA）技术。数据可视化、统计摘要、分布分析、相关性分析、异常值检测、缺失值处理、特征工程、数据清洗、假设检验、A/B 测试、时间序列分析、回归分析、分类分析、聚类分析、降维技术（PCA、t-SNE、UMAP）、高级可视化（热图、配对图、箱线图、小提琴图）。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# 探索性数据分析（EDA）

## 概述

探索性数据分析（EDA）是数据分析的关键步骤，涉及使用统计摘要和可视化技术来理解数据集的主要特征、发现模式、识别异常值和检验假设。此技能涵盖广泛的 EDA 技术，包括数据可视化、统计分析、特征工程和数据清洗。

## 何时使用此技能

此技能应在以下情况下使用：

- 对新数据集进行初步分析以了解其结构
- 创建数据可视化以探索模式和趋势
- 执行统计摘要和描述性分析
- 分析数据分布和偏度
- 检测异常值和异常值
- 处理缺失值和数据清洗
- 执行相关性分析
- 进行假设检验和统计测试
- 执行 A/B 测试分析
- 分析时间序列数据
- 进行回归分析
- 执行分类分析
- 进行聚类分析
- 应用降维技术（PCA、t-SNE、UMAP）
- 创建高级可视化（热图、配对图、箱线图、小提琴图）

## 核心能力

### 1. 数据加载和初步检查

加载数据并执行初步检查以了解数据集结构。

```python
import pandas as pd
import numpy as np

# 加载数据
df = pd.read_csv('data.csv')

# 初步检查
print(f"数据集形状：{df.shape}")
print(f"\n数据类型：\n{df.dtypes}")
print(f"\n缺失值：\n{df.isnull().sum()}")
print(f"\n基本统计：\n{df.describe()}")

# 查看前几行
print(df.head())

# 查看数据分布
print(df.info())
```

### 2. 数据可视化

使用各种可视化技术探索数据。

#### 单变量分析

**直方图：**
```python
import matplotlib.pyplot as plt
import seaborn as sns

# 直方图
plt.figure(figsize=(10, 6))
sns.histplot(df['column_name'], bins=30, kde=True)
plt.title('分布')
plt.xlabel('列名')
plt.ylabel('频率')
plt.show()
```

**箱线图：**
```python
# 箱线图
plt.figure(figsize=(10, 6))
sns.boxplot(y=df['column_name'])
plt.title('箱线图')
plt.ylabel('列名')
plt.show()
```

**小提琴图：**
```python
# 小提琴图
plt.figure(figsize=(10, 6))
sns.violinplot(y=df['column_name'])
plt.title('小提琴图')
plt.ylabel('列名')
plt.show()
```

#### 双变量分析

**散点图：**
```python
# 散点图
plt.figure(figsize=(10, 6))
sns.scatterplot(x=df['column_x'], y=df['column_y'])
plt.title('散点图')
plt.xlabel('列 X')
plt.ylabel('列 Y')
plt.show()
```

**线图（时间序列）：**
```python
# 线图
plt.figure(figsize=(10, 6))
sns.lineplot(x=df['date_column'], y=df['value_column'])
plt.title('时间序列')
plt.xlabel('日期')
plt.ylabel('值')
plt.show()
```

#### 多变量分析

**配对图：**
```python
# 配对图
sns.pairplot(df[['col1', 'col2', 'col3', 'col4']])
plt.show()
```

**热图（相关性）：**
```python
# 相关性热图
plt.figure(figsize=(12, 8))
correlation_matrix = df.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('相关性热图')
plt.show()
```

### 3. 统计分析

执行各种统计分析以了解数据特征。

#### 描述性统计

```python
# 基本统计
print(df.describe())

# 分位数
print(df.quantile([0.25, 0.5, 0.75]))

# 偏度和峰度
print(f"偏度：{df['column_name'].skew()}")
print(f"峰度：{df['column_name'].kurtosis()}")
```

#### 假设检验

**t 检验：**
```python
from scipy import stats

# 独立样本 t 检验
group1 = df[df['group'] == 'A']['value']
group2 = df[df['group'] == 'B']['value']

t_stat, p_value = stats.ttest_ind(group1, group2)
print(f"t 统计量：{t_stat}")
print(f"p 值：{p_value}")
```

**卡方检验：**
```python
# 卡方检验
contingency_table = pd.crosstab(df['column1'], df['column2'])
chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
print(f"卡方：{chi2}")
print(f"p 值：{p_value}")
```

**ANOVA：**
```python
# 单因素 ANOVA
groups = [df[df['group'] == g]['value'] for g in df['group'].unique()]
f_stat, p_value = stats.f_oneway(*groups)
print(f"F 统计量：{f_stat}")
print(f"p 值：{p_value}")
```

### 4. 相关性分析

分析变量之间的关系。

```python
# Pearson 相关性
pearson_corr = df.corr(method='pearson')

# Spearman 相关性（非参数）
spearman_corr = df.corr(method='spearman')

# Kendall 相关性
kendall_corr = df.corr(method='kendall')

# 可视化相关性
plt.figure(figsize=(12, 8))
sns.heatmap(pearson_corr, annot=True, cmap='coolwarm', center=0)
plt.title('Pearson 相关性')
plt.show()
```

### 5. 异常值检测

识别和处理异常值。

**IQR 方法：**
```python
def detect_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers

outliers = detect_outliers_iqr(df, 'column_name')
print(f"异常值数量：{len(outliers)}")
```

**Z-score 方法：**
```python
from scipy import stats

def detect_outliers_zscore(df, column, threshold=3):
    z_scores = np.abs(stats.zscore(df[column]))
    outliers = df[z_scores > threshold]
    return outliers

outliers = detect_outliers_zscore(df, 'column_name')
print(f"异常值数量：{len(outliers)}")
```

**可视化异常值：**
```python
# 箱线图显示异常值
plt.figure(figsize=(10, 6))
sns.boxplot(y=df['column_name'])
plt.title('异常值检测')
plt.ylabel('列名')
plt.show()
```

### 6. 缺失值处理

处理缺失数据。

```python
# 检查缺失值
print(df.isnull().sum())

# 缺失值比例
missing_ratio = df.isnull().sum() / len(df) * 100
print(missing_ratio)

# 删除缺失值
df_dropped = df.dropna()

# 填充缺失值
df_filled_mean = df.fillna(df.mean())
df_filled_median = df.fillna(df.median())
df_filled_mode = df.fillna(df.mode().iloc[0])

# 前向填充
df_ffill = df.fillna(method='ffill')

# 后向填充
df_bfill = df.fillna(method='bfill')

# 插值
df_interpolated = df.interpolate()
```

### 7. 特征工程

创建新特征以改进分析。

```python
# 创建新特征
df['new_feature'] = df['feature1'] / df['feature2']
df['log_feature'] = np.log(df['feature'])
df['sqrt_feature'] = np.sqrt(df['feature'])

# 二值化
df['binary_feature'] = (df['feature'] > threshold).astype(int)

# 分类编码
df = pd.get_dummies(df, columns=['categorical_column'])

# 标准化
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df['standardized'] = scaler.fit_transform(df[['feature']])

# 归一化
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
df['normalized'] = scaler.fit_transform(df[['feature']])
```

### 8. 降维技术

应用降维技术以减少数据维度。

**PCA（主成分分析）：**
```python
from sklearn.decomposition import PCA

# 准备数据（仅数值列）
numeric_cols = df.select_dtypes(include=[np.number]).columns
X = df[numeric_cols].dropna()

# 应用 PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

# 可视化
plt.figure(figsize=(10, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1])
plt.xlabel('主成分 1')
plt.ylabel('主成分 2')
plt.title('PCA')
plt.show()

# 解释方差
print(f"解释方差：{pca.explained_variance_ratio_}")
```

**t-SNE：**
```python
from sklearn.manifold import TSNE

# 应用 t-SNE
tsne = TSNE(n_components=2, random_state=42)
X_tsne = tsne.fit_transform(X)

# 可视化
plt.figure(figsize=(10, 6))
plt.scatter(X_tsne[:, 0], X_tsne[:, 1])
plt.xlabel('t-SNE 1')
plt.ylabel('t-SNE 2')
plt.title('t-SNE')
plt.show()
```

**UMAP：**
```python
from umap import UMAP

# 应用 UMAP
umap = UMAP(n_components=2, random_state=42)
X_umap = umap.fit_transform(X)

# 可视化
plt.figure(figsize=(10, 6))
plt.scatter(X_umap[:, 0], X_umap[:, 1])
plt.xlabel('UMAP 1')
plt.ylabel('UMAP 2')
plt.title('UMAP')
plt.show()
```

### 9. 聚类分析

将数据分组为相似的簇。

**K-Means 聚类：**
```python
from sklearn.cluster import KMeans

# 确定最佳簇数（肘部法则）
inertia = []
K = range(1, 11)
for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    inertia.append(kmeans.inertia_)

# 绘制肘部图
plt.figure(figsize=(10, 6))
plt.plot(K, inertia, 'bx-')
plt.xlabel('簇数')
plt.ylabel('惯性')
plt.title('肘部法则')
plt.show()

# 应用 K-Means
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X)

# 可视化
plt.figure(figsize=(10, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters)
plt.xlabel('主成分 1')
plt.ylabel('主成分 2')
plt.title('K-Means 聚类')
plt.show()
```

**层次聚类：**
```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

# 层次聚类
linkage_matrix = linkage(X, method='ward')

# 绘制树状图
plt.figure(figsize=(12, 8))
dendrogram(linkage_matrix)
plt.title('层次聚类树状图')
plt.show()

# 应用层次聚类
hierarchical = AgglomerativeClustering(n_clusters=3, linkage='ward')
clusters = hierarchical.fit_predict(X)
```

### 10. 回归分析

分析变量之间的关系。

**简单线性回归：**
```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

# 准备数据
X = df[['feature_x']].values
y = df['target'].values

# 拆分数据
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 训练模型
model = LinearRegression()
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

# 评估
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
print(f"R²：{r2}")
print(f"MSE：{mse}")

# 可视化
plt.figure(figsize=(10, 6))
plt.scatter(X_test, y_test, color='blue', label='实际')
plt.plot(X_test, y_pred, color='red', label='预测')
plt.xlabel('特征 X')
plt.ylabel('目标')
plt.title('线性回归')
plt.legend()
plt.show()
```

**多元回归：**
```python
# 多元回归
X = df[['feature1', 'feature2', 'feature3']].values
y = df['target'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

r2 = r2_score(y_test, y_pred)
print(f"R²：{r2}")
```

### 11. 分类分析

分析分类变量和预测。

**逻辑回归：**
```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# 准备数据
X = df[['feature1', 'feature2', 'feature3']].values
y = df['target_class'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 训练模型
model = LogisticRegression()
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

# 评估
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

print(f"准确率：{accuracy}")
print(f"混淆矩阵：\n{conf_matrix}")
print(f"分类报告：\n{class_report}")
```

**决策树：**
```python
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

# 训练模型
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

# 评估
accuracy = accuracy_score(y_test, y_pred)
print(f"准确率：{accuracy}")

# 可视化决策树
plt.figure(figsize=(20, 10))
tree.plot_tree(model, feature_names=['feature1', 'feature2', 'feature3'], class_names=['Class 0', 'Class 1'], filled=True)
plt.show()
```

### 12. 时间序列分析

分析时间序列数据。

```python
# 确保日期列是 datetime 类型
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')

# 时间序列可视化
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['value'])
plt.title('时间序列')
plt.xlabel('日期')
plt.ylabel('值')
plt.show()

# 滚动统计
rolling_mean = df['value'].rolling(window=7).mean()
rolling_std = df['value'].rolling(window=7).std()

plt.figure(figsize=(12, 6))
plt.plot(df.index, df['value'], label='原始')
plt.plot(df.index, rolling_mean, label='滚动均值')
plt.plot(df.index, rolling_std, label='滚动标准差')
plt.title('滚动统计')
plt.legend()
plt.show()

# 季节性分解
from statsmodels.tsa.seasonal import seasonal_decompose

decomposition = seasonal_decompose(df['value'], model='additive', period=12)
decomposition.plot()
plt.show()
```

### 13. A/B 测试分析

分析 A/B 测试结果。

```python
# 假设数据
group_a = df[df['group'] == 'A']['conversion']
group_b = df[df['group'] == 'B']['conversion']

# 转化率
conversion_a = group_a.mean()
conversion_b = group_b.mean()

print(f"组 A 转化率：{conversion_a:.4f}")
print(f"组 B 转化率：{conversion_b:.4f}")

# 显著性检验
t_stat, p_value = stats.ttest_ind(group_a, group_b)
print(f"t 统计量：{t_stat}")
print(f"p 值：{p_value}")

# 置信区间
def confidence_interval(data, confidence=0.95):
    n = len(data)
    mean = np.mean(data)
    std_err = stats.sem(data)
    h = std_err * stats.t.ppf((1 + confidence) / 2, n - 1)
    return mean - h, mean + h

ci_a = confidence_interval(group_a)
ci_b = confidence_interval(group_b)

print(f"组 A 95% CI：{ci_a}")
print(f"组 B 95% CI：{ci_b}")
```

## 安装

```bash
uv pip install pandas numpy matplotlib seaborn scipy scikit-learn umap-learn
```

## 最佳实践

1. **从数据加载和初步检查开始** - 在进行任何分析之前，先了解数据集结构
2. **使用适当的可视化** - 根据数据类型和分析目标选择合适的可视化
3. **处理缺失值** - 在分析之前决定如何处理缺失数据
4. **检测和处理异常值** - 识别异常值并决定如何处理它们
5. **验证假设** - 在进行高级分析之前验证统计假设
6. **记录所有步骤** - 确保分析的可重复性
7. **解释结果** - 始终解释分析结果的含义
8. **考虑业务背景** - 将分析结果与业务问题联系起来

## 常见工作流

### 工作流 1：完整的 EDA 流程

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 1. 加载数据
df = pd.read_csv('data.csv')

# 2. 初步检查
print(df.info())
print(df.describe())

# 3. 数据可视化
sns.pairplot(df)
plt.show()

# 4. 相关性分析
plt.figure(figsize=(12, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.show()

# 5. 异常值检测
for col in df.select_dtypes(include=[np.number]).columns:
    plt.figure(figsize=(10, 6))
    sns.boxplot(y=df[col])
    plt.title(f'{col} 的异常值')
    plt.show()

# 6. 假设检验
# 根据数据执行适当的检验
```

### 工作流 2：预测建模准备

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# 1. 处理缺失值
df = df.fillna(df.mean())

# 2. 特征工程
df['new_feature'] = df['feature1'] * df['feature2']

# 3. 编码分类变量
df = pd.get_dummies(df, columns=['categorical_column'])

# 4. 标准化
scaler = StandardScaler()
numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

# 5. 降维（可选）
pca = PCA(n_components=0.95)  # 保留 95% 的方差
X_pca = pca.fit_transform(df[numeric_cols])

# 6. 拆分数据
X_train, X_test, y_train, y_test = train_test_split(X_pca, df['target'], test_size=0.2, random_state=42)
```

## 其他资源

- **Pandas 文档**：https://pandas.pydata.org/docs/
- **NumPy 文档**：https://numpy.org/doc/
- **Matplotlib 文档**：https://matplotlib.org/stable/contents.html
- **Seaborn 文档**：https://seaborn.pydata.org/
- **Scikit-learn 文档**：https://scikit-learn.org/stable/
- **SciPy 文档**：https://docs.scipy.org/doc/scipy/
