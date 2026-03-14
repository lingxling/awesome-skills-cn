---
name: statsmodels
description: Python的统计模型库。当您需要具有详细诊断、残差和推断的特定模型类（OLS、GLM、混合模型、ARIMA）时使用。最适合计量经济学、时间序列、带有系数表的严格推断。如需带有APA报告的引导式统计测试选择，请使用statistical-analysis。
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# Statsmodels：统计建模和计量经济学

## 概述

Statsmodels是Python的首要统计建模库，提供用于各种统计方法的估计、推断和诊断工具。将此技能应用于严格的统计分析，从简单的线性回归到复杂的时间序列模型和计量经济分析。

## 何时使用此技能

当以下情况时应使用此技能：
- 拟合回归模型（OLS、WLS、GLS、分位数回归）
- 执行广义线性建模（逻辑回归、泊松、伽马等）
- 分析离散结果（二分类、多分类、计数、有序）
- 进行时间序列分析（ARIMA、SARIMAX、VAR、预测）
- 运行统计测试和诊断
- 测试模型假设（异方差性、自相关性、正态性）
- 检测异常值和有影响力的观察值
- 比较模型（AIC/BIC、似然比检验）
- 估计因果效应
- 生成可发布的统计表格和推断

## 快速入门指南

### 线性回归（OLS）

```python
import statsmodels.api as sm
import numpy as np
import pandas as pd

# 准备数据 - 始终添加常数项以获得截距
X = sm.add_constant(X_data)

# 拟合OLS模型
model = sm.OLS(y, X)
results = model.fit()

# 查看综合结果
print(results.summary())

# 关键结果
print(f"R-squared: {results.rsquared:.4f}")
print(f"Coefficients:\n{results.params}")
print(f"P-values:\n{results.pvalues}")

# 带置信区间的预测
predictions = results.get_prediction(X_new)
pred_summary = predictions.summary_frame()
print(pred_summary)  # 包含均值、CI、预测区间

# 诊断
from statsmodels.stats.diagnostic import het_breuschpagan
bp_test = het_breuschpagan(results.resid, X)
print(f"Breusch-Pagan p-value: {bp_test[1]:.4f}")

# 可视化残差
import matplotlib.pyplot as plt
plt.scatter(results.fittedvalues, results.resid)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Fitted values')
plt.ylabel('Residuals')
plt.show()
```

### 逻辑回归（二分类结果）

```python
from statsmodels.discrete.discrete_model import Logit

# 添加常数
X = sm.add_constant(X_data)

# 拟合logit模型
model = Logit(y_binary, X)
results = model.fit()

print(results.summary())

# 优势比
odds_ratios = np.exp(results.params)
print("Odds ratios:\n", odds_ratios)

# 预测概率
probs = results.predict(X)

# 二分类预测（0.5阈值）
predictions = (probs > 0.5).astype(int)

# 模型评估
from sklearn.metrics import classification_report, roc_auc_score

print(classification_report(y_binary, predictions))
print(f"AUC: {roc_auc_score(y_binary, probs):.4f}")

# 边际效应
marginal = results.get_margeff()
print(marginal.summary())
```

### 时间序列（ARIMA）

```python
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# 检查平稳性
from statsmodels.tsa.stattools import adfuller

adf_result = adfuller(y_series)
print(f"ADF p-value: {adf_result[1]:.4f}")

if adf_result[1] > 0.05:
    # 序列非平稳，差分处理
    y_diff = y_series.diff().dropna()

# 绘制ACF/PACF以识别p, q
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
plot_acf(y_diff, lags=40, ax=ax1)
plot_pacf(y_diff, lags=40, ax=ax2)
plt.show()

# 拟合ARIMA(p,d,q)
model = ARIMA(y_series, order=(1, 1, 1))
results = model.fit()

print(results.summary())

# 预测
forecast = results.forecast(steps=10)
forecast_obj = results.get_forecast(steps=10)
forecast_df = forecast_obj.summary_frame()

print(forecast_df)  # 包含均值和置信区间

# 残差诊断
results.plot_diagnostics(figsize=(12, 8))
plt.show()
```

### 广义线性模型（GLM）

```python
import statsmodels.api as sm

# 泊松回归用于计数数据
X = sm.add_constant(X_data)
model = sm.GLM(y_counts, X, family=sm.families.Poisson())
results = model.fit()

print(results.summary())

# 比率比（用于带对数链接的泊松）
rate_ratios = np.exp(results.params)
print("Rate ratios:\n", rate_ratios)

# 检查过度离散
overdispersion = results.pearson_chi2 / results.df_resid
print(f"Overdispersion: {overdispersion:.2f}")

if overdispersion > 1.5:
    # 改用负二项式
    from statsmodels.discrete.count_model import NegativeBinomial
    nb_model = NegativeBinomial(y_counts, X)
    nb_results = nb_model.fit()
    print(nb_results.summary())
```

## 核心统计建模能力

### 1. 线性回归模型

用于具有各种误差结构的连续结果的综合线性模型套件。

**可用模型：**
- **OLS**：具有i.i.d.误差的标准线性回归
- **WLS**：用于异方差误差的加权最小二乘
- **GLS**：用于任意协方差结构的广义最小二乘
- **GLSAR**：具有自回归误差的时间序列GLS
- **分位数回归**：条件分位数（对异常值稳健）
- **混合效应**：具有随机效应的层次/多级模型
- **递归/滚动**：时变参数估计

**关键特性：**
- 全面的诊断测试
- 稳健标准误（HC、HAC、聚类稳健）
- 影响力统计量（库克距离、杠杆率、DFFITS）
- 假设检验（F检验、Wald检验）
- 模型比较（AIC、BIC、似然比检验）
- 带置信和预测区间的预测

**何时使用：**连续结果变量，需要对系数进行推断，需要诊断

**参考：**有关模型选择、诊断和最佳实践的详细指导，请参见`references/linear_models.md`。

### 2. 广义线性模型（GLM）

将线性模型扩展到非正态分布的灵活框架。

**分布族：**
- **二项式**：二分类结果或比例（逻辑回归）
- **泊松**：计数数据
- **负二项式**：过度离散的计数
- **伽马**：正连续、右偏数据
- **逆高斯**：具有特定方差结构的正连续数据
- **高斯**：等同于OLS
- **Tweedie**：用于半连续数据的灵活族

**链接函数：**
- Logit、Probit、Log、Identity、Inverse、Sqrt、CLogLog、Power
- 根据解释需求和模型拟合选择

**关键特性：**
- 通过IRLS进行最大似然估计
- 偏差和皮尔逊残差
- 拟合优度统计量
- 伪R平方度量
- 稳健标准误

**何时使用：**非正态结果，需要灵活的方差和链接规范

**参考：**有关族选择、链接函数、解释和诊断的详细信息，请参见`references/glm.md`。

### 3. 离散选择模型

用于分类和计数结果的模型。

**二分类模型：**
- **Logit**：逻辑回归（优势比）
- **Probit**：Probit回归（正态分布）

**多分类模型：**
- **MNLogit**：无序类别（3+水平）
- **条件Logit**：具有替代特定变量的选择模型
- **有序模型**：有序结果（有序类别）

**计数模型：**
- **泊松**：标准计数模型
- **负二项式**：过度离散的计数
- **零膨胀**：过多零值（ZIP、ZINB）
- **障碍模型**：零值密集数据的两阶段模型

**关键特性：**
- 最大似然估计
- 均值边际效应或平均边际效应
- 通过AIC/BIC进行模型比较
- 预测概率和分类
- 拟合优度测试

**何时使用：**二分类、分类或计数结果

**参考：**有关模型选择、解释和评估的详细信息，请参见`references/discrete_choice.md`。

### 4. 时间序列分析

全面的时间序列建模和预测能力。

**单变量模型：**
- **AutoReg (AR)**：自回归模型
- **ARIMA**：自回归综合移动平均
- **SARIMAX**：带有外生变量的季节性ARIMA
- **指数平滑**：简单、Holt、Holt-Winters
- **ETS**：创新状态空间模型

**多变量模型：**
- **VAR**：向量自回归
- **VARMAX**：带有MA和外生变量的VAR
- **动态因子模型**：提取共同因子
- **VECM**：向量误差校正模型（协整）

**高级模型：**
- **状态空间**：卡尔曼滤波、自定义规范
- **政权切换**：马尔可夫切换模型
- **ARDL**：自回归分布滞后

**关键特性：**
- 用于模型识别的ACF/PACF分析
- 平稳性测试（ADF、KPSS）
- 带预测区间的预测
- 残差诊断（Ljung-Box、异方差性）
- Granger因果检验
- 脉冲响应函数（IRF）
- 预测误差方差分解（FEVD）

**何时使用：**时间有序数据、预测、理解时间动态

**参考：**有关模型选择、诊断和预测方法的详细信息，请参见`references/time_series.md`。

### 5. 统计测试和诊断

用于模型验证的广泛测试和诊断能力。

**残差诊断：**
- 自相关测试（Ljung-Box、Durbin-Watson、Breusch-Godfrey）
- 异方差性测试（Breusch-Pagan、White、ARCH）
- 正态性测试（Jarque-Bera、Omnibus、Anderson-Darling、Lilliefors）
- 规范测试（RESET、Harvey-Collier）

**影响力和异常值：**
- 杠杆率（帽子值）
- 库克距离
- DFFITS和DFBETAs
- 学生化残差
- 影响力图

**假设检验：**
- t检验（单样本、两样本、配对）
- 比例检验
- 卡方检验
- 非参数检验（Mann-Whitney、Wilcoxon、Kruskal-Wallis）
- 方差分析（单因素、双因素、重复测量）

**多重比较：**
- Tukey's HSD
- Bonferroni校正
- 错误发现率（FDR）

**效应量和功效：**
- Cohen's d、eta-squared
- t检验、比例的功效分析
- 样本量计算

**稳健推断：**
- 异方差一致性SEs（HC0-HC3）
- HAC标准误（Newey-West）
- 聚类稳健标准误

**何时使用：**验证假设、检测问题、确保稳健推断

**参考：**有关综合测试和诊断程序的详细信息，请参见`references/stats_diagnostics.md`。

## 公式API（R风格）

Statsmodels支持R风格的公式，用于直观的模型规范：

```python
import statsmodels.formula.api as smf

# 带公式的OLS
results = smf.ols('y ~ x1 + x2 + x1:x2', data=df).fit()

# 分类变量（自动哑变量编码）
results = smf.ols('y ~ x1 + C(category)', data=df).fit()

# 交互项
results = smf.ols('y ~ x1 * x2', data=df).fit()  # x1 + x2 + x1:x2

# 多项式项
results = smf.ols('y ~ x + I(x**2)', data=df).fit()

# Logit
results = smf.logit('y ~ x1 + x2 + C(group)', data=df).fit()

# Poisson
results = smf.poisson('count ~ x1 + x2', data=df).fit()

# ARIMA（不可通过公式使用，使用常规API）
```

## 模型选择和比较

### 信息准则

```python
# 使用AIC/BIC比较模型
models = {
    'Model 1': model1_results,
    'Model 2': model2_results,
    'Model 3': model3_results
}

comparison = pd.DataFrame({
    'AIC': {name: res.aic for name, res in models.items()},
    'BIC': {name: res.bic for name, res in models.items()},
    'Log-Likelihood': {name: res.llf for name, res in models.items()}
})

print(comparison.sort_values('AIC'))
# 较低的AIC/BIC表示更好的模型
```

### 似然比检验（嵌套模型）

```python
# 对于嵌套模型（一个是另一个的子集）
from scipy import stats

lr_stat = 2 * (full_model.llf - reduced_model.llf)
df = full_model.df_model - reduced_model.df_model
p_value = 1 - stats.chi2.cdf(lr_stat, df)

print(f"LR statistic: {lr_stat:.4f}")
print(f"p-value: {p_value:.4f}")

if p_value < 0.05:
    print("Full model significantly better")
else:
    print("Reduced model preferred (parsimony)")
```

### 交叉验证

```python
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error

kf = KFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = []

for train_idx, val_idx in kf.split(X):
    X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
    y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

    # 拟合模型
    model = sm.OLS(y_train, X_train).fit()

    # 预测
    y_pred = model.predict(X_val)

    # 评分
    rmse = np.sqrt(mean_squared_error(y_val, y_pred))
    cv_scores.append(rmse)

print(f"CV RMSE: {np.mean(cv_scores):.4f} ± {np.std(cv_scores):.4f}")
```

## 最佳实践

### 数据准备

1. **始终添加常数**：使用`sm.add_constant()`，除非排除截距
2. **检查缺失值**：在拟合前处理或插补
3. **如需要进行缩放**：提高收敛性、解释性（但对于树模型不是必需的）
4. **编码分类变量**：使用公式API或手动哑变量编码

### 模型构建

1. **从简单开始**：从基本模型开始，根据需要增加复杂性
2. **检查假设**：测试残差、异方差性、自相关性
3. **使用适当的模型**：匹配模型到结果类型（二分类→Logit、计数→Poisson）
4. **考虑替代方案**：如果假设被违反，使用稳健方法或不同模型

### 推断

1. **报告效应量**：不仅仅是p值
2. **使用稳健SEs**：当存在异方差性或聚类时
3. **多重比较**：测试许多假设时进行校正
4. **置信区间**：始终与点估计一起报告

### 模型评估

1. **检查残差**：绘制残差vs拟合值、Q-Q图
2. **影响力诊断**：识别和调查有影响力的观察值
3. **样本外验证**：在保留集上测试或交叉验证
4. **比较模型**：对非嵌套使用AIC/BIC，对嵌套使用LR检验

### 报告

1. **综合摘要**：使用`.summary()`获取详细输出
2. **记录决策**：注意变换、排除的观察值
3. **仔细解释**：考虑链接函数（例如，log链接的exp(β)）
4. **可视化**：绘制预测、置信区间、诊断

## 常见工作流

### 工作流1：线性回归分析

1. 探索数据（图表、描述性统计）
2. 拟合初始OLS模型
3. 检查残差诊断
4. 测试异方差性、自相关性
5. 检查多重共线性（VIF）
6. 识别有影响力的观察值
7. 如有需要，使用稳健SEs重新拟合
8. 解释系数和推断
9. 在保留集上验证或通过CV验证

### 工作流2：二分类分类

1. 拟合逻辑回归（Logit）
2. 检查收敛问题
3. 解释优势比
4. 计算边际效应
5. 评估分类性能（AUC、混淆矩阵）
6. 检查有影响力的观察值
7. 与替代模型（Probit）比较
8. 在测试集上验证预测

### 工作流3：计数数据分析

1. 拟合泊松回归
2. 检查过度离散
3. 如果过度离散，拟合负二项式
4. 检查过多零值（考虑ZIP/ZINB）
5. 解释比率比
6. 评估拟合优度
7. 通过AIC比较模型
8. 验证预测

### 工作流4：时间序列预测

1. 绘制序列，检查趋势/季节性
2. 测试平稳性（ADF、KPSS）
3. 如果非平稳，进行差分
4. 从ACF/PACF识别p, q
5. 拟合ARIMA或SARIMAX
6. 检查残差诊断（Ljung-Box）
7. 生成带置信区间的预测
8. 在测试集上评估预测准确性

## 参考文档

此技能包含详细指导的综合参考文件：

### references/linear_models.md
线性回归模型的详细覆盖，包括：
- OLS、WLS、GLS、GLSAR、分位数回归
- 混合效应模型
- 递归和滚动回归
- 综合诊断（异方差性、自相关性、多重共线性）
- 影响力统计和异常值检测
- 稳健标准误（HC、HAC、聚类）
- 假设检验和模型比较

### references/glm.md
广义线性模型的完整指南：
- 所有分布族（二项式、泊松、伽马等）
- 链接函数及何时使用
- 模型拟合和解释
- 伪R平方和拟合优度
- 诊断和残差分析
- 应用（逻辑、泊松、伽马回归）

### references/discrete_choice.md
离散结果模型的综合指南：
- 二分类模型（Logit、Probit）
- 多分类模型（MNLogit、条件Logit）
- 计数模型（泊松、负二项式、零膨胀、障碍）
- 有序模型
- 边际效应和解释
- 模型诊断和比较

### references/time_series.md
深入的时间序列分析指导：
- 单变量模型（AR、ARIMA、SARIMAX、指数平滑）
- 多变量模型（VAR、VARMAX、动态因子）
- 状态空间模型
- 平稳性测试和诊断
- 预测方法和评估
- Granger因果关系、IRF、FEVD

### references/stats_diagnostics.md
综合统计测试和诊断：
- 残差诊断（自相关性、异方差性、正态性）
- 影响力和异常值检测
- 假设检验（参数和非参数）
- 方差分析和事后检验
- 多重比较校正
- 稳健协方差矩阵
- 功效分析和效应量

**何时参考：**
- 需要详细的参数解释
- 在类似模型之间选择
- 解决收敛或诊断问题
- 理解特定测试统计量
- 寻找高级功能的代码示例

**搜索模式：**
```bash
# 查找有关特定模型的信息
grep -r "Quantile Regression" references/

# 查找诊断测试
grep -r "Breusch-Pagan" references/stats_diagnostics.md

# 查找时间序列指导
grep -r "SARIMAX" references/time_series.md
```

## 要避免的常见陷阱

1. **忘记常数项**：始终使用`sm.add_constant()`，除非不需要截距
2. **忽略假设**：检查残差、异方差性、自相关性
3. **结果类型的错误模型**：二分类→Logit/Probit，计数→Poisson/NB，不是OLS
4. **不检查收敛**：查找优化警告
5. **错误解释系数**：记住链接函数（log、logit等）
6. **使用过度离散的泊松**：检查离散度，必要时使用负二项式
7. **不使用稳健SEs**：当存在异方差性或聚类时
8. **过拟合**：参数过多相对于样本大小
9. **数据泄露**：在测试数据上拟合或使用未来信息
10. **不验证预测**：始终检查样本外性能
11. **比较非嵌套模型**：使用AIC/BIC，而不是LR检验
12. **忽略有影响力的观察值**：检查库克距离和杠杆率
13. **多重测试**：测试许多假设时校正p值
14. **不对时间序列进行差分**：在非平稳数据上拟合ARIMA
15. **混淆预测vs置信区间**：预测区间更宽

## 获取帮助

有关详细文档和示例：
- 官方文档：https://www.statsmodels.org/stable/
- 用户指南：https://www.statsmodels.org/stable/user-guide.html
- 示例：https://www.statsmodels.org/stable/examples/index.html
- API参考：https://www.statsmodels.org/stable/api.html