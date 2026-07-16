---
name: statistical-analysis
description: 面向研究数据的引导式统计分析——检验选择、假设检查、效应量、功效分析、贝叶斯替代方法和APA格式报告。当用户想要比较组别、检验假设、分析实验或调查数据、检查统计假设、计算所需样本量或撰写结果报告时使用——即使用户没有指明具体的检验方法。涵盖t检验、方差分析、卡方检验、相关性、回归、非参数方法和贝叶斯方法。对于底层模型API，请参见statsmodels和pymc技能。
license: MIT license
metadata: {"version": "1.1", "skill-author": "K-Dense Inc."}
---

# 统计分析

## 概述

进行假设检验（t检验、方差分析、卡方检验）、回归、相关性和贝叶斯分析，并系统地检查假设、计算效应量并撰写APA风格的报告。目标是产出一份评审者挑不出毛病的分析：正确的检验方法、经过验证的假设、如实报告的效应量，以及完整的撰写。

## 何时使用此技能

在以下情况下使用此技能：
- 进行统计假设检验（t检验、方差分析、卡方检验、非参数检验）
- 执行回归或相关性分析
- 运行贝叶斯统计分析
- 检查统计假设和诊断
- 计算效应量并进行功效分析
- 以APA格式报告统计结果
- 分析研究的实验或观察数据

---

## 安装

使用 **uv** 安装本技能所用的库。生产环境中请固定版本号；探索阶段不固定版本也可以。

```bash
# 核心频率派工具栈（Python 3.10+；推荐3.12+以使用最新的SciPy/ArviZ）
uv pip install "pingouin>=0.6" "scipy>=1.11" "statsmodels>=0.14.6" pandas matplotlib seaborn

# 贝叶斯建模（PyMC 5 + ArviZ）
uv pip install "pymc>=5.0" "arviz>=1.0"
```

**兼容性说明（已针对 pingouin 0.6.1、statsmodels 0.14.6、arviz 1.2 验证，2026年）：**

- **Pingouin 0.6.0** 重命名了输出列名以去除特殊字符：`p_val`、`cohen_d`、`CI95`、`p_unc`（在0.5.x中此前分别为`p-val`、`cohen-d`、`CI95%`、`p-unc`）。下文示例使用当前列名；如果仍在使用0.5.x，请改用带连字符的旧写法。
- **statsmodels + SciPy**：使用 `statsmodels>=0.14.6` 搭配 `scipy>=1.11`，以避免在SciPy 1.16+上出现`_lazywhere`导入错误。
- **ArviZ 1.x**：`az.summary()` 现在默认输出**89%区间**（`eti89`列），且区间宽度参数改为 `ci_prob`（而不是`hdi_prob`）。要报告常规的95%可信区间，需显式传入 `az.summary(trace, ci_prob=0.95)`。
- **单侧贝叶斯因子已从Pingouin中移除**：`pg.ttest(..., alternative='greater')` 会静默丢弃 `BF10` 列，`pg.bayesfactor_ttest` 在单侧备择假设下会报错。对于单侧贝叶斯检验，请直接使用PyMC（计算方向性假设的后验概率）或JASP/R的BayesFactor包。

有关特定模型的API（OLS、GLM、ARIMA），请参见 **statsmodels** 技能。有关PyMC工作流，请参见 **pymc** 技能。

---

## 分析工作流

每一次严谨的分析都遵循相同的路径。跳过步骤正是分析最终被撤稿的原因，因此请按顺序逐一完成，并说明在每一步做了什么。

1. **先明确问题，再动数据。** 说明假设、结局变量和预测变量，以及设计类型（独立还是配对、组数）。现在就确定计划采用的检验方法——在看过结果之后再选择检验方法，即使是无意为之，也是p值操纵（p-hacking）。
2. **检查数据。** 按组统计：n、均值、标准差、中位数、缺失值。在进行任何检验之前先绘制原始数据（直方图或箱线图）。组间样本量不均、缺失数据、地板/天花板效应和异常值都会改变适用的检验方法——应向用户明确指出这些问题，而不是悄悄地绕过它们。
3. **选择检验方法**，可使用下面的快速参考，或参考`references/test_selection_guide.md`了解基础方法之外的设计（计数、时间-事件、信度、析因设计）。
4. **用`scripts/assumption_checks.py`检查假设。** 如果某个假设不成立，改用补救性检验方法（见下表），并同时报告原计划和所做的更改。
5. **运行检验**，并始终同时计算效应量——p值只能说明效应是否存在；效应量才能说明是否值得关注。
6. **撰写报告**，使用下面的APA模板，包括描述性统计、精确的统计量、带置信区间的效应量，以及所执行的假设检查。

如果用户只需要其中一个步骤（例如"我需要多少参与者？"），可以直接跳到相应部分——但仍需确认该计算所依赖的设计假设。

---

## 检验选择指南

### 快速参考：选择正确的检验

有关计数数据、生存分析、信度、析因设计等全面指导，请使用`references/test_selection_guide.md`。快速参考：

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
所有检验都有贝叶斯版本，可提供关于假设的直接概率陈述、量化证据的贝叶斯因子，以及支持零假设的能力。参见`references/bayesian_statistics.md`。

---

## 假设检查

**始终在解释检验结果之前检查假设**，并报告检查过程——评审者会关注这些内容。

使用内置的`scripts/assumption_checks.py`模块。从技能目录（`skills/statistical-analysis/`）运行Python，或将`scripts/`添加到`sys.path`：

```python
from assumption_checks import comprehensive_assumption_check

# 异常值 + 正态性（按组）+ 方差齐性检验，附带图表
results = comprehensive_assumption_check(
    data=df,
    value_col='score',
    group_col='group',  # 可选：用于组比较
    alpha=0.05
)
```

对于有针对性的检查，可导入单独的函数：

```python
from assumption_checks import (
    check_normality,                # 夏皮罗-威尔克检验 + Q-Q图 + 直方图
    check_normality_per_group,
    check_homogeneity_of_variance,  # 列文检验 + 箱线图
    check_linearity,                # 简单回归的散点图 + 残差图
    check_regression_diagnostics,   # 完整的OLS诊断（见下文回归部分）
    detect_outliers                 # IQR或z分数方法
)

result = check_normality(data=df['score'], name='Test Score', alpha=0.05, plot=True)
print(result['interpretation'])
print(result['recommendation'])
```

### 假设被违反时的处理

**正态性被违反：**
- 轻微违反 + 每组n > 30 → 继续使用参数检验（稳健）
- 中度违反 → 使用非参数替代方法
- 严重违反 → 转换数据或使用非参数检验

**方差齐性被违反：**
- 对于t检验 → 使用Welch t检验（`pg.ttest`在`correction='auto'`下会自动应用）
- 对于方差分析 → 使用Welch方差分析（`pg.welch_anova`）或Brown-Forsythe检验
- 对于回归 → 使用稳健标准误或加权最小二乘法

**线性被违反（回归）：**
- 添加多项式项、转换变量，或使用非线性模型/GAM

正式检验会随着n的增大而变得过于敏感：当n ≥ 100时，应更重视Q-Q图而不是夏皮罗-威尔克检验的p值。有关全面指导，请参见`references/assumptions_and_diagnostics.md`。

---

## 运行统计检验

主要使用的库：
- **pingouin**：用户友好的检验方法，默认返回效应量——标准检验优先使用它
- **scipy.stats**：核心统计检验
- **statsmodels**：回归、诊断、功效分析
- **pymc** + **arviz**：贝叶斯建模和诊断

### 带完整报告的T检验

```python
import pingouin as pg

# correction='auto' 在方差不齐时会自动应用Welch校正
result = pg.ttest(group_a, group_b, correction='auto')

# Pingouin >= 0.6 的列名
t_stat = result['T'].values[0]
df = result['dof'].values[0]
p_value = result['p_val'].values[0]
cohens_d = result['cohen_d'].values[0]
ci_lower, ci_upper = result['CI95'].values[0]  # 均值差的置信区间

print(f"t({df:.0f}) = {t_stat:.2f}, p = {p_value:.3f}, d = {cohens_d:.2f}")
```

### 带事后检验的方差分析

```python
import pingouin as pg

aov = pg.anova(dv='score', between='group', data=df, detailed=True)
print(aov)

# 效应量：部分η²
eta_p2 = aov['np2'].values[0]

# 如果显著，进行事后检验（Tukey HSD控制族错误率）
if aov['p_unc'].values[0] < 0.05:
    posthoc = pg.pairwise_tukey(dv='score', between='group', data=df)
    print(posthoc)  # 包含每对比较的Hedges' g
```

### 带诊断的线性回归

```python
import statsmodels.api as sm
from assumption_checks import check_regression_diagnostics

X = sm.add_constant(X_predictors)  # 添加截距
model = sm.OLS(y, X).fit()
print(model.summary())

# 4面板残差图 + 夏皮罗-威尔克检验、Breusch-Pagan检验、Durbin-Watson检验、VIF
diag = check_regression_diagnostics(model)
print(diag['interpretation'])
print(diag['vif'])

# 如果标记出异方差性，改为报告稳健标准误
robust = model.get_robustcov_results('HC3')
```

### 贝叶斯T检验

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

    trace = pm.sample(2000, tune=1000)

# ArviZ 1.x默认使用89%区间；报告时需显式请求95%
print(az.summary(trace, var_names=['difference'], ci_prob=0.95))

# 直接的概率陈述（这正是单侧问题所转化成的结果）
prob_greater = np.mean(trace.posterior['difference'].values > 0)
print(f"P(mu1 > mu2 | data) = {prob_greater:.3f}")

# ArviZ 1.x已移除az.plot_posterior；改用plot_dist（在0.x版本中plot_posterior仍可用）
az.plot_dist(trace, var_names=['difference'], ci_prob=0.95)
```

先验的尺度应与数据相匹配（例如，`sigma=10`适合标准差接近10的结局变量；可用观测到的标准差作为参考），并在报告中说明所用的先验。

---

## 效应量

**效应量量化效应大小；p值只能说明效应是否存在。** 每次检验都应报告一个效应量。完整指南参见`references/effect_sizes_and_power.md`。

### 快速参考：常见效应量

| 检验 | 效应量 | 小 | 中 | 大 |
|------|--------|----|----|----|
| T检验 | Cohen's d | 0.20 | 0.50 | 0.80 |
| 方差分析 | η²_p | 0.01 | 0.06 | 0.14 |
| 相关性 | r | 0.10 | 0.30 | 0.50 |
| 回归 | R² | 0.02 | 0.13 | 0.26 |
| 卡方检验 | Cramér's V | 0.07 | 0.21 | 0.35 |

这些基准是约定俗成的惯例，不是铁律——一个"小"效应可能极为重要（如药物副作用），而一个"大"效应也可能无关紧要。应结合具体情境解读。

### 计算效应量

Pingouin会在检验结果中一并返回效应量（`pg.ttest`的`cohen_d`、`pg.anova`的`np2`、`pg.pairwise_tukey`的`hedges`；`pg.corr`返回的`r`本身就是一种效应量）。

### 效应量的置信区间

应报告效应量的置信区间以体现其精度。使用`pg.compute_esci`（注意：`pg.compute_effsize_from_t`只返回点估计——它**不会**返回置信区间）：

```python
import pingouin as pg

d = pg.compute_effsize(group_a, group_b, eftype='cohen')
ci_lower, ci_upper = pg.compute_esci(stat=d, nx=len(group_a), ny=len(group_b),
                                     eftype='cohen', confidence=0.95)
print(f"d = {d:.2f}, 95% CI [{ci_lower:.2f}, {ci_upper:.2f}]")
```

---

## 功效分析

### 先验功效分析（研究规划）

在数据收集前确定所需的样本量：

```python
from statsmodels.stats.power import tt_ind_solve_power, FTestAnovaPower

# T检验：检测d = 0.5需要每组多少n？
n_required = tt_ind_solve_power(
    effect_size=0.5,
    alpha=0.05,
    power=0.80,
    ratio=1.0,
    alternative='two-sided'
)
print(f"每组所需n: {n_required:.0f}")

# 单因素方差分析：检测Cohen's f = 0.25需要多少n？
# 注意：参数名是k_groups；effect_size是Cohen's f（f = sqrt(eta2/(1-eta2)));
# 且solve_power返回的是总样本量，而不是每组的n。
import math
anova_power = FTestAnovaPower()
n_total = anova_power.solve_power(
    effect_size=0.25,
    k_groups=3,
    alpha=0.05,
    power=0.80
)
print(f"所需总样本量: {math.ceil(n_total)}（每组约{math.ceil(n_total / 3)}）")
```

### 敏感性分析（研究后）

确定该研究能够检测到的效应量：

```python
# 每组n=50时，在80%功效下我们可以检测到什么效应？
detectable_d = tt_ind_solve_power(
    effect_size=None,  # 求解这个
    nobs1=50,
    alpha=0.05,
    power=0.80,
    ratio=1.0,
    alternative='two-sided'
)
print(f"研究可以检测到d >= {detectable_d:.2f}")
```

**注意**：事后的"观测功效"（根据观测到的效应量计算功效）是循环论证且具有误导性的——它其实是p值的确定性函数。如果研究已经完成，有人询问功效问题，应改为进行敏感性分析。

有关详细指导，请参见`references/effect_sizes_and_power.md`。

---

## 报告结果

遵循`references/reporting_standards.md`中的APA风格指南。每份报告都需要包含：

1. **描述性统计**：所有组/变量的M、SD、n
2. **检验统计量**：检验名称、统计量、df、精确p值（写作`p = .034`，而不是`p < .05`；只有p值低于.001时才使用`p < .001`）
3. **效应量**：附带置信区间
4. **假设检查**：进行了哪些检验、结果如何、采取了什么行动
5. **所有计划的分析**：包括不显著的结果——省略它们就是选择性报告

### 示例报告模板

#### 独立T检验

```
组A（n = 48, M = 75.2, SD = 8.5）的得分显著高于
组B（n = 52, M = 68.3, SD = 9.2），t(98) = 3.82, p < .001, d = 0.77,
95% CI [0.36, 1.18]，双侧检验。正态性假设（夏皮罗-威尔克检验：
组A W = 0.97, p = .18；组B W = 0.96, p = .12）和方差齐性假设
（列文检验F(1, 98) = 1.23, p = .27）均得到满足。
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
使用弱信息先验（组均值为Normal(0, 10)）进行贝叶斯独立样本t检验。
后验分布表明组A得分高于组B
（M_diff = 6.8, 95% 可信区间 [3.2, 10.4]），
组A均值超过组B均值的后验概率为99.8%。
收敛诊断令人满意（所有R-hat < 1.01, ESS > 1000）。
```

如果使用了非参数检验，应报告中位数而不是均值、报告U/W/H统计量，以及基于秩的效应量（例如秩双列相关系数，`pg.mwu`会以`RBC`列返回该值）。

---

## 贝叶斯统计

在以下情况下考虑使用贝叶斯方法：
- 有先验信息需要纳入分析
- 想要关于假设的直接概率陈述（"该效应有95%的概率落在此区间内"）
- 样本量较小，或数据收集是序贯进行的（无需为可选停止校正）
- 需要量化*支持*零假设的证据
- 模型较为复杂（层次结构、缺失数据）

有关先验设定、贝叶斯因子、可信区间、层次模型以及收敛检查（R-hat < 1.01、充足的ESS、后验预测检查），请参见`references/bayesian_statistics.md`。

---

## 捆绑资源

### 参考文档（`references/`）

- **test_selection_guide.md**：涵盖组间比较、关系分析、计数数据、时间-事件分析、一致性/信度和分类分析的决策树
- **assumptions_and_diagnostics.md**：关于检查和处理假设违反情况的详细指导
- **effect_sizes_and_power.md**：计算、解释和报告效应量；功效分析
- **bayesian_statistics.md**：先验、贝叶斯因子、可信区间、层次模型、诊断
- **reporting_standards.md**：带实例的APA风格报告指南

### 脚本（`scripts/`）

- **assumption_checks.py**：带可视化的自动假设检查
  - `comprehensive_assumption_check()`：一次调用完成异常值 + 正态性 + 方差齐性检验
  - `check_normality()`、`check_normality_per_group()`：带Q-Q图的夏皮罗-威尔克检验
  - `check_homogeneity_of_variance()`：带箱线图的列文检验
  - `check_regression_diagnostics()`：针对已拟合OLS模型的4面板残差图 + 夏皮罗-威尔克检验、Breusch-Pagan检验、Durbin-Watson检验、VIF
  - `check_linearity()`、`detect_outliers()`

---

## 统计诚信

以下是让一份分析经得起推敲的实践。它们之所以重要，是因为最常见的统计错误并非计算失误——而是悄悄的"灵活性"（不断尝试直到得出想要的结果）和选择性报告。

1. **区分验证性分析和探索性分析。** 在运行分析之前就说明计划采用的分析方法；将过程中发现的任何结果标注为探索性发现。
2. **不要为了追求显著性而反复尝试。** 如果计划中的检验结果不显著，那就是结果本身。反复尝试不同的检验方法、子组或异常值剔除方案直到p < .05，会使该p值失去意义。
3. **在运行一系列检验时，应校正多重比较**（事后方差分析用Tukey HSD；其他系列检验用Holm或Benjamini-Hochberg FDR校正），并说明使用了哪种校正方法。
4. **不显著的结果不等于没有效应的证据。** 在样本量较小的情况下，研究可能只是功效不足——应运行敏感性分析，或使用贝叶斯分析/等效性检验来真正量化对零假设的支持程度。
5. **统计显著性不等于实际重要性。** 在样本量较大时，微不足道的效应也能达到p < .001。解读时应以效应量为主导。
6. **在删除行之前先理解缺失数据的机制。** 列表式删除（listwise deletion）只有在数据完全随机缺失（MCAR）时才是安全的；否则应考虑多重插补，并说明所采取的处理方式。
7. **保证可复现性。** 设置随机种子，对基于模拟的方法报告所用的库版本，并将分析保存为可运行的脚本。
