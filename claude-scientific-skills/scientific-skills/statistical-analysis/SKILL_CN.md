---
name: statistical-analysis
description: 引导式统计分析，包括测试选择和报告。当您需要帮助为数据选择适当的测试、检查假设、进行功效分析以及生成APA格式结果时使用。最适合学术研究报告、测试选择指导。如需以编程方式实现特定模型，请使用statsmodels。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# 统计分析

## 概述

统计分析是一个系统化的过程，用于检验假设和量化关系。进行假设检验（t检验、方差分析、卡方检验）、回归、相关性和贝叶斯分析，包括假设检查和APA报告。将此技能应用于学术研究。

## 何时使用此技能

当以下情况时应使用此技能：
- 进行统计假设检验（t检验、方差分析、卡方检验）
- 执行回归或相关性分析
- 运行贝叶斯统计分析
- 检查统计假设和诊断
- 计算效应量并进行功效分析
- 以APA格式报告统计结果
- 分析研究的实验或观察数据

---

## 核心能力

### 1. 测试选择和规划
- 根据研究问题和数据特征选择适当的统计测试
- 进行先验功效分析以确定所需的样本量
- 规划分析策略，包括多重比较校正

### 2. 假设检查
- 在运行测试前自动验证所有相关假设
- 提供诊断可视化（Q-Q图、残差图、箱线图）
- 当假设被违反时推荐补救措施

### 3. 统计测试
- 假设检验：t检验、方差分析、卡方检验、非参数替代方法
- 回归：线性、多元、逻辑回归，带诊断
- 相关性：皮尔逊、斯皮尔曼，带置信区间
- 贝叶斯替代方法：贝叶斯t检验、方差分析、带贝叶斯因子的回归

### 4. 效应量和解释
- 为所有分析计算和解释适当的效应量
- 为效应估计提供置信区间
- 区分统计显著性和实际显著性

### 5. 专业报告
- 生成APA风格的统计报告
- 创建可发布的图表和表格
- 提供完整的解释，包括所有必需的统计数据

---

## 工作流决策树

使用此决策树确定您的分析路径：

```
开始
│
├─ 需要选择统计测试？
│  └─ 是 → 参见"测试选择指南"
│  └─ 否 → 继续
│
├─ 准备检查假设？
│  └─ 是 → 参见"假设检查"
│  └─ 否 → 继续
│
├─ 准备运行分析？
│  └─ 是 → 参见"运行统计测试"
│  └─ 否 → 继续
│
└─ 需要报告结果？
   └─ 是 → 参见"报告结果"
```

---

## 测试选择指南

### 快速参考：选择正确的测试

使用`references/test_selection_guide.md`获取全面指导。快速参考：

**比较两组：**
- 独立、连续、正态 → 独立t检验
- 独立、连续、非正态 → 曼-惠特尼U检验
- 配对、连续、正态 → 配对t检验
- 配对、连续、非正态 → 威尔科克森符号秩检验
- 二分类结果 → 卡方检验或Fisher精确检验

**比较3+组：**
- 独立、连续、正态 → 单因素方差分析
- 独立、连续、非正态 → 克鲁斯卡尔-沃利斯检验
- 配对、连续、正态 → 重复测量方差分析
- 配对、连续、非正态 → 弗里德曼检验

**关系：**
- 两个连续变量 → 皮尔逊（正态）或斯皮尔曼相关（非正态）
- 连续结果与预测变量 → 线性回归
- 二分类结果与预测变量 → 逻辑回归

**贝叶斯替代方法：**
所有测试都有贝叶斯版本，提供：
- 关于假设的直接概率陈述
- 量化证据的贝叶斯因子
- 支持零假设的能力
- 参见`references/bayesian_statistics.md`

---

## 假设检查

### 系统性假设验证

**在解释测试结果之前，始终检查假设。**

使用提供的`scripts/assumption_checks.py`模块进行自动检查：

```python
from scripts.assumption_checks import comprehensive_assumption_check

# 带可视化的全面检查
results = comprehensive_assumption_check(
    data=df,
    value_col='score',
    group_col='group',  # 可选：用于组比较
    alpha=0.05
)
```

这执行：
1. **异常值检测**（IQR和z分数方法）
2. **正态性测试**（夏皮罗-威尔克检验 + Q-Q图）
3. **方差齐性**（列文检验 + 箱线图）
4. **解释和建议**

### 单独的假设检查

对于有针对性的检查，使用单独的函数：

```python
from scripts.assumption_checks import (
    check_normality,
    check_normality_per_group,
    check_homogeneity_of_variance,
    check_linearity,
    detect_outliers
)

# 示例：带可视化的正态性检查
result = check_normality(
    data=df['score'],
    name='Test Score',
    alpha=0.05,
    plot=True
)
print(result['interpretation'])
print(result['recommendation'])
```

### 假设被违反时的处理

**正态性被违反：**
- 轻微违反 + 每组n > 30 → 继续使用参数检验（稳健）
- 中度违反 → 使用非参数替代方法
- 严重违反 → 转换数据或使用非参数检验

**方差齐性被违反：**
- 对于t检验 → 使用Welch t检验
- 对于方差分析 → 使用Welch方差分析或Brown-Forsythe方差分析
- 对于回归 → 使用稳健标准误或加权最小二乘法

**线性被违反（回归）：**
- 添加多项式项
- 转换变量
- 使用非线性模型或GAM

有关全面指导，请参见`references/assumptions_and_diagnostics.md`。

---

## 运行统计测试

### Python库

统计分析的主要库：
- **scipy.stats**：核心统计测试
- **statsmodels**：高级回归和诊断
- **pingouin**：用户友好的统计测试，带效应量
- **pymc**：贝叶斯统计建模
- **arviz**：贝叶斯可视化和诊断

### 示例分析

#### 带完整报告的T检验

```python
import pingouin as pg
import numpy as np

# 运行独立t检验
result = pg.ttest(group_a, group_b, correction='auto')

# 提取结果
t_stat = result['T'].values[0]
df = result['dof'].values[0]
p_value = result['p-val'].values[0]
cohens_d = result['cohen-d'].values[0]
ci_lower = result['CI95%'].values[0][0]
ci_upper = result['CI95%'].values[0][1]

# 报告
print(f"t({df:.0f}) = {t_stat:.2f}, p = {p_value:.3f}")
print(f"Cohen's d = {cohens_d:.2f}, 95% CI [{ci_lower:.2f}, {ci_upper:.2f}]")
```

#### 带事后检验的方差分析

```python
import pingouin as pg

# 单因素方差分析
aov = pg.anova(dv='score', between='group', data=df, detailed=True)
print(aov)

# 如果显著，进行事后检验
if aov['p-unc'].values[0] < 0.05:
    posthoc = pg.pairwise_tukey(dv='score', between='group', data=df)
    print(posthoc)

# 效应量
eta_squared = aov['np2'].values[0]  # 部分η²
print(f"Partial η² = {eta_squared:.3f}")
```

#### 带诊断的线性回归

```python
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# 拟合模型
X = sm.add_constant(X_predictors)  # 添加截距
model = sm.OLS(y, X).fit()

# 摘要
print(model.summary())

# 检查多重共线性（VIF）
vif_data = pd.DataFrame()
vif_data["Variable"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print(vif_data)

# 检查假设
residuals = model.resid
fitted = model.fittedvalues

# 残差图
import matplotlib.pyplot as plt
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 残差vs拟合值
axes[0, 0].scatter(fitted, residuals, alpha=0.6)
axes[0, 0].axhline(y=0, color='r', linestyle='--')
axes[0, 0].set_xlabel('Fitted values')
axes[0, 0].set_ylabel('Residuals')
axes[0, 0].set_title('Residuals vs Fitted')

# Q-Q图
from scipy import stats
stats.probplot(residuals, dist="norm", plot=axes[0, 1])
axes[0, 1].set_title('Normal Q-Q')

# 尺度-位置
axes[1, 0].scatter(fitted, np.sqrt(np.abs(residuals / residuals.std())), alpha=0.6)
axes[1, 0].set_xlabel('Fitted values')
axes[1, 0].set_ylabel('√|Standardized residuals|')
axes[1, 0].set_title('Scale-Location')

# 残差直方图
axes[1, 1].hist(residuals, bins=20, edgecolor='black', alpha=0.7)
axes[1, 1].set_xlabel('Residuals')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].set_title('Histogram of Residuals')

plt.tight_layout()
plt.show()
```

#### 贝叶斯T检验

```python
import pymc as pm
import arviz as az
import numpy as np

with pm.Model() as model:
    # 先验
    mu1 = pm.Normal('mu_group1', mu=0, sigma=10)
    mu2 = pm.Normal('mu_group2', mu=0, sigma=10)
    sigma = pm.HalfNormal('sigma', sigma=10)

    # 似然
    y1 = pm.Normal('y1', mu=mu1, sigma=sigma, observed=group_a)
    y2 = pm.Normal('y2', mu=mu2, sigma=sigma, observed=group_b)

    # 派生量
    diff = pm.Deterministic('difference', mu1 - mu2)

    # 采样
    trace = pm.sample(2000, tune=1000, return_inferencedata=True)

# 总结
print(az.summary(trace, var_names=['difference']))

# group1 > group2的概率
prob_greater = np.mean(trace.posterior['difference'].values > 0)
print(f"P(μ₁ > μ₂ | data) = {prob_greater:.3f}")

# 绘制后验
az.plot_posterior(trace, var_names=['difference'], ref_val=0)
```

---

## 效应量

### 始终计算效应量

**效应量量化大小，而p值仅指示效应的存在。**

有关全面指导，请参见`references/effect_sizes_and_power.md`。

### 快速参考：常见效应量

| 测试 | 效应量 | 小 | 中 | 大 |
|------|--------|----|----|----|
| T检验 | Cohen's d | 0.20 | 0.50 | 0.80 |
| 方差分析 | η²_p | 0.01 | 0.06 | 0.14 |
| 相关性 | r | 0.10 | 0.30 | 0.50 |
| 回归 | R² | 0.02 | 0.13 | 0.26 |
| 卡方检验 | Cramér's V | 0.07 | 0.21 | 0.35 |

**重要**：基准是指导方针。上下文很重要！

### 计算效应量

大多数效应量由pingouin自动计算：

```python
# T检验返回Cohen's d
result = pg.ttest(x, y)
d = result['cohen-d'].values[0]

# 方差分析返回部分η²
aov = pg.anova(dv='score', between='group', data=df)
eta_p2 = aov['np2'].values[0]

# 相关性：r本身就是效应量
corr = pg.corr(x, y)
r = corr['r'].values[0]
```

### 效应量的置信区间

始终报告CI以显示精度：

```python
from pingouin import compute_effsize_from_t

# 对于t检验
d, ci = compute_effsize_from_t(
    t_statistic,
    nx=len(group1),
    ny=len(group2),
    eftype='cohen'
)
print(f"d = {d:.2f}, 95% CI [{ci[0]:.2f}, {ci[1]:.2f}]")
```

---

## 功效分析

### 先验功效分析（研究规划）

在数据收集前确定所需的样本量：

```python
from statsmodels.stats.power import (
    tt_ind_solve_power,
    FTestAnovaPower
)

# T检验：检测d = 0.5需要多少n？
n_required = tt_ind_solve_power(
    effect_size=0.5,
    alpha=0.05,
    power=0.80,
    ratio=1.0,
    alternative='two-sided'
)
print(f"每组所需n: {n_required:.0f}")

# 方差分析：检测f = 0.25需要多少n？
anova_power = FTestAnovaPower()
n_per_group = anova_power.solve_power(
    effect_size=0.25,
    ngroups=3,
    alpha=0.05,
    power=0.80
)
print(f"每组所需n: {n_per_group:.0f}")
```

### 敏感性分析（研究后）

确定您可以检测到的效应量：

```python
# 每组n=50时，我们可以检测到什么效应？
detectable_d = tt_ind_solve_power(
    effect_size=None,  # 求解这个
    nobs1=50,
    alpha=0.05,
    power=0.80,
    ratio=1.0,
    alternative='two-sided'
)
print(f"研究可以检测到d ≥ {detectable_d:.2f}")
```

**注意**：事后功效分析（研究后计算功效）通常不推荐。请改用敏感性分析。

有关详细指导，请参见`references/effect_sizes_and_power.md`。

---

## 报告结果

### APA风格统计报告

遵循`references/reporting_standards.md`中的指南。

### 必要的报告元素

1. **描述性统计**：所有组/变量的M、SD、n
2. **测试统计**：测试名称、统计量、df、精确p值
3. **效应量**：带置信区间
4. **假设检查**：进行了哪些测试、结果、采取的行动
5. **所有计划的分析**：包括非显著结果

### 示例报告模板

#### 独立T检验

```
组A（n = 48, M = 75.2, SD = 8.5）的得分显著高于
组B（n = 52, M = 68.3, SD = 9.2），t(98) = 3.82, p < .001, d = 0.77,
95% CI [0.36, 1.18]，双侧检验。正态性（夏皮罗-威尔克：
组A W = 0.97, p = .18；组B W = 0.96, p = .12）和方差齐性
（列文检验F(1, 98) = 1.23, p = .27）假设得到满足。
```

#### 单因素方差分析

```
单因素方差分析显示治疗条件对测试得分有显著主效应，
F(2, 147) = 8.45, p < .001, η²_p = .10。使用Tukey's HSD的事后
比较表明，条件A（M = 78.2, SD = 7.3）的得分显著高于
条件B（M = 71.5, SD = 8.1, p = .002, d = 0.87）和
条件C（M = 70.1, SD = 7.9, p < .001, d = 1.07）。
条件B和C之间无显著差异（p = .52, d = 0.18）。
```

#### 多元回归

```
进行多元线性回归以从学习时间、先前GPA和出勤率预测考试分数。
整体模型显著，F(3, 146) = 45.2, p < .001, R² = .48, 调整R² = .47。
学习时间（B = 1.80, SE = 0.31, β = .35, t = 5.78, p < .001, 95% CI [1.18, 2.42]）
和先前GPA（B = 8.52, SE = 1.95, β = .28, t = 4.37, p < .001, 95% CI [4.66, 12.38]）
是显著预测因子，而出勤率不是（B = 0.15, SE = 0.12, β = .08, t = 1.25, p = .21, 95% CI [-0.09, 0.39]）。
多重共线性不是问题（所有VIF < 1.5）。
```

#### 贝叶斯分析

```
使用弱信息先验（均值差异为Normal(0, 1)）进行贝叶斯独立样本t检验。
后验分布表明组A得分高于组B（M_diff = 6.8, 95% 可信区间 [3.2, 10.4]）。
贝叶斯因子BF₁₀ = 45.3为组间差异提供了非常强的证据，
组A均值超过组B均值的后验概率为99.8%。
收敛诊断令人满意（所有R̂ < 1.01, ESS > 1000）。
```

---

## 贝叶斯统计

### 何时使用贝叶斯方法

考虑在以下情况使用贝叶斯方法：
- 您有先验信息要纳入
- 您想要关于假设的直接概率陈述
- 样本量小或计划序贯数据收集
- 您需要量化对零假设的证据
- 模型复杂（层次结构、缺失数据）

有关全面指导，请参见`references/bayesian_statistics.md`：
- 贝叶斯定理和解释
- 先验指定（信息性、弱信息性、非信息性）
- 使用贝叶斯因子的贝叶斯假设检验
- 可信区间与置信区间
- 贝叶斯t检验、方差分析、回归和层次模型
- 模型收敛检查和后验预测检查

### 关键优势

1. **直观解释**："给定数据，参数在这个区间内的概率为95%"
2. **对零假设的证据**：可以量化对无效应的支持
3. **灵活性**：无p值操纵担忧；可以在数据到达时进行分析
4. **不确定性量化**：完整的后验分布

---

## 资源

此技能包含全面的参考材料：

### 参考目录

- **test_selection_guide.md**：选择适当统计测试的决策树
- **assumptions_and_diagnostics.md**：关于检查和处理假设违反的详细指导
- **effect_sizes_and_power.md**：计算、解释和报告效应量；进行功效分析
- **bayesian_statistics.md**：贝叶斯分析方法的完整指南
- **reporting_standards.md**：带示例的APA风格报告指南

### 脚本目录

- **assumption_checks.py**：带可视化的自动假设检查
  - `comprehensive_assumption_check()`：完整工作流
  - `check_normality()`：带Q-Q图的正态性测试
  - `check_homogeneity_of_variance()`：带箱线图的列文检验
  - `check_linearity()`：回归线性检查
  - `detect_outliers()`：IQR和z分数异常值检测

---

## 最佳实践

1. **预注册分析**（如果可能）以区分验证性和探索性
2. **始终检查假设**在解释结果之前
3. **报告效应量**带置信区间
4. **报告所有计划的分析**包括非显著结果
5. **区分统计显著性和实际显著性**
6. **可视化数据**在分析前后
7. **检查回归/方差分析的诊断**（残差图、VIF等）
8. **进行敏感性分析**以评估稳健性
9. **共享数据和代码**以提高可重复性
10. **透明**关于违反、转换和决策

---

## 要避免的常见陷阱

1. **P值操纵**：不要测试多种方法直到有显著结果
2. **HARKing**：不要将探索性发现呈现为验证性
3. **忽略假设**：检查它们并报告违反情况
4. **混淆显著性和重要性**：p < .05 ≠ 有意义的效应
5. **不报告效应量**：解释所必需的
6. **选择性报告结果**：报告所有计划的分析
7. **误解p值**：它们不是假设为真的概率
8. **多重比较**：适当时校正族-wise错误
9. **忽略缺失数据**：了解机制（MCAR、MAR、MNAR）
10. **过度解释非显著结果**：证据缺失 ≠ 缺失证据

---

## 入门清单

开始统计分析时：

- [ ] 定义研究问题和假设
- [ ] 确定适当的统计测试（使用test_selection_guide.md）
- [ ] 进行功效分析以确定样本量
- [ ] 加载并检查数据
- [ ] 检查缺失数据和异常值
- [ ] 使用assumption_checks.py验证假设
- [ ] 运行主要分析
- [ ] 计算带置信区间的效应量
- [ ] 如需要进行事后检验（带校正）
- [ ] 创建可视化
- [ ] 按照reporting_standards.md撰写结果
- [ ] 进行敏感性分析
- [ ] 共享数据和代码

---

## 支持和进一步阅读

关于以下问题：
- **测试选择**：参见references/test_selection_guide.md
- **假设**：参见references/assumptions_and_diagnostics.md
- **效应量**：参见references/effect_sizes_and_power.md
- **贝叶斯方法**：参见references/bayesian_statistics.md
- **报告**：参见references/reporting_standards.md

**关键教科书**：
- Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences*
- Field, A. (2013). *Discovering Statistics Using IBM SPSS Statistics*
- Gelman, A., & Hill, J. (2006). *Data Analysis Using Regression and Multilevel/Hierarchical Models*
- Kruschke, J. K. (2014). *Doing Bayesian Data Analysis*

**在线资源**：
- APA风格指南：https://apastyle.apa.org/
- 统计咨询：Cross Validated (stats.stackexchange.com)