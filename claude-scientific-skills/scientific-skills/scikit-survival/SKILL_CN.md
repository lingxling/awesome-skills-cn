---
name: scikit-survival
description: 用于Python中生存分析和时间事件建模的综合工具包，基于scikit-survival。当处理截尾生存数据、执行时间事件分析、拟合Cox模型、随机生存森林、梯度提升模型或生存SVM、使用一致性指数或Brier评分评估生存预测、处理竞争风险或使用scikit-survival库实现任何生存分析工作流时，使用此技能。
license: GPL-3.0 license
metadata:
    skill-author: K-Dense Inc.
---

# scikit-survival: Python中的生存分析

## 概述

scikit-survival是一个基于scikit-learn构建的Python生存分析库。它提供专门的工具用于时间事件分析，处理截尾数据的独特挑战，其中一些观察值仅部分已知。

生存分析旨在建立协变量与事件时间之间的联系，同时考虑截尾记录（特别是来自研究的右截尾数据，其中参与者在观察期间未经历事件）。

## 何时使用此技能

当以下情况时使用此技能：
- 执行生存分析或时间事件建模
- 处理截尾数据（右截尾、左截尾或区间截尾）
- 拟合Cox比例风险模型（标准或 penalized）
- 构建集成生存模型（随机生存森林、梯度提升）
- 训练生存支持向量机
- 评估生存模型性能（一致性指数、Brier评分、时间依赖性AUC）
- 估计Kaplan-Meier或Nelson-Aalen曲线
- 分析竞争风险
- 预处理生存数据或处理生存数据集中的缺失值
- 使用scikit-survival库进行任何分析

## 核心功能

### 1. 模型类型与选择

scikit-survival提供多种模型系列，每种适合不同场景：

#### Cox比例风险模型
**用途**：具有可解释系数的标准生存分析
- `CoxPHSurvivalAnalysis`：基本Cox模型
- `CoxnetSurvivalAnalysis`：用于高维数据的弹性网惩罚Cox模型
- `IPCRidge`：用于加速失效时间模型的岭回归

**参考**：`references/cox-models.md` 提供关于Cox模型、正则化和解释的详细指南

#### 集成方法
**用途**：处理复杂非线性关系的高预测性能
- `RandomSurvivalForest`：稳健的非参数集成方法
- `GradientBoostingSurvivalAnalysis`：基于树的提升以获得最佳性能
- `ComponentwiseGradientBoostingSurvivalAnalysis`：具有特征选择的线性提升
- `ExtraSurvivalTrees`：用于额外正则化的极端随机树

**参考**：`references/ensemble-models.md` 提供关于集成方法、超参数调优以及何时使用每种模型的综合指南

#### 生存支持向量机
**用途**：使用基于边际学习的中等大小数据集
- `FastSurvivalSVM`：为速度优化的线性SVM
- `FastKernelSurvivalSVM`：用于非线性关系的核SVM
- `HingeLossSurvivalSVM`：带铰链损失的SVM
- `ClinicalKernelTransform`：用于临床+分子数据的专用核

**参考**：`references/svm-models.md` 提供关于SVM指南、核选择和超参数调优的详细信息

#### 模型选择决策树

```
开始
├─ 高维数据 (p > n)?
│  ├─ 是 → CoxnetSurvivalAnalysis (弹性网)
│  └─ 否 → 继续
│
├─ 需要可解释系数?
│  ├─ 是 → CoxPHSurvivalAnalysis 或 ComponentwiseGradientBoostingSurvivalAnalysis
│  └─ 否 → 继续
│
├─ 预期存在复杂非线性关系?
│  ├─ 是
│  │  ├─ 大型数据集 (n > 1000) → GradientBoostingSurvivalAnalysis
│  │  ├─ 中型数据集 → RandomSurvivalForest 或 FastKernelSurvivalSVM
│  │  └─ 小型数据集 → RandomSurvivalForest
│  └─ 否 → CoxPHSurvivalAnalysis 或 FastSurvivalSVM
│
└─ 为获得最佳性能 → 尝试多个模型并比较
```

### 2. 数据准备与预处理

建模前，正确准备生存数据：

#### 创建生存结果
```python
from sksurv.util import Surv

# 从单独的数组

y = Surv.from_arrays(event=event_array, time=time_array)

# 从DataFrame

y = Surv.from_dataframe('event', 'time', df)
```

#### 基本预处理步骤
1. **处理缺失值**：特征的插补策略
2. **编码分类变量**：独热编码或标签编码
3. **标准化特征**：对SVM和正则化Cox模型至关重要
4. **验证数据质量**：检查负时间、每个特征的足够事件数
5. **训练-测试分割**：在分割中保持相似的截尾率

**参考**：`references/data-handling.md` 提供完整的预处理工作流、数据验证和最佳实践

### 3. 模型评估

适当的评估对生存模型至关重要。使用考虑截尾的适当指标：

#### 一致性指数（C-index）
用于排序/区分的主要指标：
- **Harrell的C-index**：用于低截尾（<40%）
- **Uno的C-index**：用于中等至高截尾（>40%）- 更稳健

```python
from sksurv.metrics import concordance_index_censored, concordance_index_ipcw

# Harrell的C-index
c_harrell = concordance_index_censored(y_test['event'], y_test['time'], risk_scores)[0]

# Uno的C-index（推荐）
c_uno = concordance_index_ipcw(y_train, y_test, risk_scores)[0]
```

#### 时间依赖性AUC
评估特定时间点的区分能力：

```python
from sksurv.metrics import cumulative_dynamic_auc

times = [365, 730, 1095]  # 1, 2, 3年
auc, mean_auc = cumulative_dynamic_auc(y_train, y_test, risk_scores, times)
```

#### Brier评分
评估区分和校准：

```python
from sksurv.metrics import integrated_brier_score

ibs = integrated_brier_score(y_train, y_test, survival_functions, times)
```

**参考**：`references/evaluation-metrics.md` 提供综合评估指南、指标选择以及在交叉验证中使用评分器

### 4. 竞争风险分析

处理具有多个互斥事件类型的情况：

```python
from sksurv.nonparametric import cumulative_incidence_competing_risks

# 估计每种事件类型的累积发生率
time_points, cif_event1, cif_event2 = cumulative_incidence_competing_risks(y)
```

**使用竞争风险当**：
- 存在多个互斥事件类型（例如，不同原因的死亡）
- 一个事件的发生阻止其他事件
- 需要特定事件类型的概率估计

**参考**：`references/competing-risks.md` 提供关于竞争风险方法、特定原因风险模型和解释的详细信息

### 5. 非参数估计

无参数假设地估计生存函数：

#### Kaplan-Meier估计器
```python
from sksurv.nonparametric import kaplan_meier_estimator

time, survival_prob = kaplan_meier_estimator(y['event'], y['time'])
```

#### Nelson-Aalen估计器
```python
from sksurv.nonparametric import nelson_aalen_estimator

time, cumulative_hazard = nelson_aalen_estimator(y['event'], y['time'])
```

## 典型工作流

### 工作流1：标准生存分析

```python
from sksurv.datasets import load_breast_cancer
from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.metrics import concordance_index_ipcw
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1. 加载和准备数据
X, y = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. 预处理
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 3. 拟合模型
estimator = CoxPHSurvivalAnalysis()
estimator.fit(X_train_scaled, y_train)

# 4. 预测
risk_scores = estimator.predict(X_test_scaled)

# 5. 评估
c_index = concordance_index_ipcw(y_train, y_test, risk_scores)[0]
print(f"C-index: {c_index:.3f}")
```

### 工作流2：带特征选择的高维数据

```python
from sksurv.linear_model import CoxnetSurvivalAnalysis
from sklearn.model_selection import GridSearchCV
from sksurv.metrics import as_concordance_index_ipcw_scorer

# 1. 使用惩罚Cox进行特征选择
estimator = CoxnetSurvivalAnalysis(l1_ratio=0.9)  # 类Lasso

# 2. 用交叉验证调整正则化
param_grid = {'alpha_min_ratio': [0.01, 0.001]}
cv = GridSearchCV(estimator, param_grid,
                  scoring=as_concordance_index_ipcw_scorer(), cv=5)
cv.fit(X, y)

# 3. 识别选定的特征
best_model = cv.best_estimator_
selected_features = np.where(best_model.coef_ != 0)[0]
```

### 工作流3：获得最佳性能的集成方法

```python
from sksurv.ensemble import GradientBoostingSurvivalAnalysis
from sklearn.model_selection import GridSearchCV

# 1. 定义参数网格
param_grid = {
    'learning_rate': [0.01, 0.05, 0.1],
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 5, 7]
}

# 2. 网格搜索
gbs = GradientBoostingSurvivalAnalysis()
cv = GridSearchCV(gbs, param_grid, cv=5,
                  scoring=as_concordance_index_ipcw_scorer(), n_jobs=-1)
cv.fit(X_train, y_train)

# 3. 评估最佳模型
best_model = cv.best_estimator_
risk_scores = best_model.predict(X_test)
c_index = concordance_index_ipcw(y_train, y_test, risk_scores)[0]
```

### 工作流4：综合模型比较

```python
from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.ensemble import RandomSurvivalForest, GradientBoostingSurvivalAnalysis
from sksurv.svm import FastSurvivalSVM
from sksurv.metrics import concordance_index_ipcw, integrated_brier_score

# 定义模型
models = {
    'Cox': CoxPHSurvivalAnalysis(),
    'RSF': RandomSurvivalForest(n_estimators=100, random_state=42),
    'GBS': GradientBoostingSurvivalAnalysis(random_state=42),
    'SVM': FastSurvivalSVM(random_state=42)
}

# 评估每个模型
results = {}
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    risk_scores = model.predict(X_test_scaled)
    c_index = concordance_index_ipcw(y_train, y_test, risk_scores)[0]
    results[name] = c_index
    print(f"{name}: C-index = {c_index:.3f}")

# 选择最佳模型
best_model_name = max(results, key=results.get)
print(f"\n最佳模型: {best_model_name}")
```

## 与scikit-learn集成

scikit-survival完全集成到scikit-learn的生态系统中：

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score, GridSearchCV

# 使用管道
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', CoxPHSurvivalAnalysis())
])

# 使用交叉验证
scores = cross_val_score(pipeline, X, y, cv=5,
                         scoring=as_concordance_index_ipcw_scorer())

# 使用网格搜索
param_grid = {'model__alpha': [0.1, 1.0, 10.0]}
cv = GridSearchCV(pipeline, param_grid, cv=5)
cv.fit(X, y)
```

## 最佳实践

1. **始终标准化特征**用于SVM和正则化Cox模型
2. **当截尾> 40%时使用Uno的C-index**而不是Harrell的
3. **报告多个评估指标**（C-index、集成Brier评分、时间依赖性AUC）
4. **检查Cox模型的比例风险假设**
5. **使用交叉验证**通过适当的评分器进行超参数调优
6. **建模前验证数据质量**（检查负时间、每个特征的足够事件数）
7. **比较多种模型类型**以找到最佳性能
8. **对随机生存森林使用排列重要性**（非内置重要性）
9. **当存在多种事件类型时考虑竞争风险**
10. **在分析中记录截尾机制**和率

## 常见陷阱避免

1. **使用Harrell的C-index处理高截尾** → 使用Uno的C-index
2. **不为SVM标准化特征** → 始终标准化
3. **忘记将y_train传递给concordance_index_ipcw** → IPCW计算所需
4. **将竞争事件视为截尾** → 使用竞争风险方法
5. **不检查每个特征的足够事件数** → 经验法则：每个特征10+事件
6. **对RSF使用内置特征重要性** → 使用排列重要性
7. **忽略比例风险假设** → 验证或使用替代模型
8. **在交叉验证中不使用适当的评分器** → 使用as_concordance_index_ipcw_scorer()

## 参考文件

此技能包含特定主题的详细参考文件：

- **`references/cox-models.md`**：Cox比例风险模型、惩罚Cox（CoxNet）、IPCRidge、正则化策略和解释的完整指南
- **`references/ensemble-models.md`**：随机生存森林、梯度提升、超参数调优、特征重要性和模型选择
- **`references/evaluation-metrics.md`**：一致性指数（Harrell vs Uno）、时间依赖性AUC、Brier评分、综合评估管道
- **`references/data-handling.md`**：数据加载、预处理工作流、处理缺失数据、特征编码、验证检查
- **`references/svm-models.md`**：生存支持向量机、核选择、临床核变换、超参数调优
- **`references/competing-risks.md`**：竞争风险分析、累积发生率函数、特定原因风险模型

当需要特定任务的详细信息时，加载这些参考文件。

## 其他资源

- **官方文档**：https://scikit-survival.readthedocs.io/
- **GitHub仓库**：https://github.com/sebp/scikit-survival
- **内置数据集**：使用`sksurv.datasets`获取练习数据集（GBSG2、WHAS500、退伍军人肺癌等）
- **API参考**：完整的类和函数列表，位于https://scikit-survival.readthedocs.io/en/stable/api/index.html

## 快速参考：关键导入

```python
# 模型
from sksurv.linear_model import CoxPHSurvivalAnalysis, CoxnetSurvivalAnalysis, IPCRidge
from sksurv.ensemble import RandomSurvivalForest, GradientBoostingSurvivalAnalysis
from sksurv.svm import FastSurvivalSVM, FastKernelSurvivalSVM
from sksurv.tree import SurvivalTree

# 评估指标
from sksurv.metrics import (
    concordance_index_censored,
    concordance_index_ipcw,
    cumulative_dynamic_auc,
    brier_score,
    integrated_brier_score,
    as_concordance_index_ipcw_scorer,
    as_integrated_brier_score_scorer
)

# 非参数估计
from sksurv.nonparametric import (
    kaplan_meier_estimator,
    nelson_aalen_estimator,
    cumulative_incidence_competing_risks
)

# 数据处理
from sksurv.util import Surv
from sksurv.preprocessing import OneHotEncoder, encode_categorical
from sksurv.datasets import load_gbsg2, load_breast_cancer, load_veterans_lung_cancer

# 核
from sksurv.kernels import ClinicalKernelTransform
```