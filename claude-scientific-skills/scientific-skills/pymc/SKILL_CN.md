---
name: pymc
description: 使用PyMC进行贝叶斯建模。构建层次模型、MCMC（NUTS）、变分推断、LOO/WAIC比较、后验检查，用于概率编程和推断。
license: Apache License, Version 2.0
metadata:
    skill-author: K-Dense Inc.
---

# PyMC 贝叶斯建模

## 概述

PyMC是一个用于贝叶斯建模和概率编程的Python库。使用PyMC的现代API（5.x+版本）构建、拟合、验证和比较贝叶斯模型，包括层次模型、MCMC采样（NUTS）、变分推断和模型比较（LOO、WAIC）。

## 使用场景

当您需要以下操作时使用此技能：
- 构建贝叶斯模型（线性/逻辑回归、层次模型、时间序列等）
- 执行MCMC采样或变分推断
- 进行先验/后验预测检查
- 诊断采样问题（发散、收敛、ESS）
- 使用信息准则（LOO、WAIC）比较多个模型
- 通过贝叶斯方法实现不确定性量化
- 处理层次/多级数据结构
- 以原则性方式处理缺失数据或测量误差

## 标准贝叶斯工作流

按照以下工作流构建和验证贝叶斯模型：

### 1. 数据准备

```python
import pymc as pm
import arviz as az
import numpy as np

# 加载和准备数据
X = ...  # 预测变量
y = ...  # 结果变量

# 标准化预测变量以提高采样效率
X_mean = X.mean(axis=0)
X_std = X.std(axis=0)
X_scaled = (X - X_mean) / X_std
```

**关键实践：**
- 标准化连续预测变量（提高采样效率）
- 尽可能中心化结果变量
- 明确处理缺失数据（将其视为参数）
- 使用带有`coords`的命名维度以提高清晰度

### 2. 模型构建

```python
coords = {
    'predictors': ['var1', 'var2', 'var3'],
    'obs_id': np.arange(len(y))
}

with pm.Model(coords=coords) as model:
    # 先验
    alpha = pm.Normal('alpha', mu=0, sigma=1)
    beta = pm.Normal('beta', mu=0, sigma=1, dims='predictors')
    sigma = pm.HalfNormal('sigma', sigma=1)

    # 线性预测器
    mu = alpha + pm.math.dot(X_scaled, beta)

    # 似然
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y, dims='obs_id')
```

**关键实践：**
- 使用弱信息先验（非平坦先验）
- 对尺度参数使用`HalfNormal`或`Exponential`
- 尽可能使用命名维度（`dims`）而非`shape`
- 对将用于预测的值使用`pm.Data()`

### 3. 先验预测检查

**拟合前务必验证先验：**

```python
with model:
    prior_pred = pm.sample_prior_predictive(samples=1000, random_seed=42)

# 可视化
az.plot_ppc(prior_pred, group='prior')
```

**检查：**
- 先验预测是否涵盖合理值？
- 给定领域知识，极端值是否合理？
- 如果先验生成不合理数据，调整并重新检查

### 4. 拟合模型

```python
with model:
    # 可选：使用ADVI进行快速探索
    # approx = pm.fit(n=20000)

    # 完整MCMC推断
    idata = pm.sample(
        draws=2000,
        tune=1000,
        chains=4,
        target_accept=0.9,
        random_seed=42,
        idata_kwargs={'log_likelihood': True}  # 用于模型比较
    )
```

**关键参数：**
- `draws=2000`：每条链的样本数
- `tune=1000`：预热样本（丢弃）
- `chains=4`：运行4条链用于收敛检查
- `target_accept=0.9`：对于困难的后验分布更高（0.95-0.99）
- 包含`log_likelihood=True`用于模型比较

### 5. 检查诊断

**使用诊断脚本：**

```python
from scripts.model_diagnostics import check_diagnostics

results = check_diagnostics(idata, var_names=['alpha', 'beta', 'sigma'])
```

**检查：**
- **R-hat < 1.01**：链已收敛
- **ESS > 400**：有效样本足够
- **无发散**：NUTS采样成功
- **迹图**：链应该混合良好（模糊的毛毛虫）

**如果出现问题：**
- 发散 → 增加`target_accept=0.95`，使用非中心化参数化
- 低ESS → 采样更多样本，重新参数化以减少相关性
- 高R-hat → 运行更长时间，检查多模态性

### 6. 后验预测检查

**验证模型拟合：**

```python
with model:
    pm.sample_posterior_predictive(idata, extend_inferencedata=True, random_seed=42)

# 可视化
az.plot_ppc(idata)
```

**检查：**
- 后验预测是否捕捉到观察数据模式？
- 是否有系统性偏差（模型错误指定）？
- 如果拟合不佳，考虑替代模型

### 7. 分析结果

```python
# 汇总统计
print(az.summary(idata, var_names=['alpha', 'beta', 'sigma']))

# 后验分布
az.plot_posterior(idata, var_names=['alpha', 'beta', 'sigma'])

# 系数估计
az.plot_forest(idata, var_names=['beta'], combined=True)
```

### 8. 进行预测

```python
X_new = ...  # 新的预测变量值
X_new_scaled = (X_new - X_mean) / X_std

with model:
    pm.set_data({'X_scaled': X_new_scaled})
    post_pred = pm.sample_posterior_predictive(
        idata.posterior,
        var_names=['y_obs'],
        random_seed=42
    )

# 提取预测区间
y_pred_mean = post_pred.posterior_predictive['y_obs'].mean(dim=['chain', 'draw'])
y_pred_hdi = az.hdi(post_pred.posterior_predictive, var_names=['y_obs'])
```

## 常见模型模式

### 线性回归

对于具有线性关系的连续结果：

```python
with pm.Model() as linear_model:
    alpha = pm.Normal('alpha', mu=0, sigma=10)
    beta = pm.Normal('beta', mu=0, sigma=10, shape=n_predictors)
    sigma = pm.HalfNormal('sigma', sigma=1)

    mu = alpha + pm.math.dot(X, beta)
    y = pm.Normal('y', mu=mu, sigma=sigma, observed=y_obs)
```

**使用模板：** `assets/linear_regression_template.py`

### 逻辑回归

对于二元结果：

```python
with pm.Model() as logistic_model:
    alpha = pm.Normal('alpha', mu=0, sigma=10)
    beta = pm.Normal('beta', mu=0, sigma=10, shape=n_predictors)

    logit_p = alpha + pm.math.dot(X, beta)
    y = pm.Bernoulli('y', logit_p=logit_p, observed=y_obs)
```

### 层次模型

对于分组数据（使用非中心化参数化）：

```python
with pm.Model(coords={'groups': group_names}) as hierarchical_model:
    # 超先验
    mu_alpha = pm.Normal('mu_alpha', mu=0, sigma=10)
    sigma_alpha = pm.HalfNormal('sigma_alpha', sigma=1)

    # 组级（非中心化）
    alpha_offset = pm.Normal('alpha_offset', mu=0, sigma=1, dims='groups')
    alpha = pm.Deterministic('alpha', mu_alpha + sigma_alpha * alpha_offset, dims='groups')

    # 观测级
    mu = alpha[group_idx]
    sigma = pm.HalfNormal('sigma', sigma=1)
    y = pm.Normal('y', mu=mu, sigma=sigma, observed=y_obs)
```

**使用模板：** `assets/hierarchical_model_template.py`

**关键：** 对于层次模型，始终使用非中心化参数化以避免发散。

### 泊松回归

对于计数数据：

```python
with pm.Model() as poisson_model:
    alpha = pm.Normal('alpha', mu=0, sigma=10)
    beta = pm.Normal('beta', mu=0, sigma=10, shape=n_predictors)

    log_lambda = alpha + pm.math.dot(X, beta)
    y = pm.Poisson('y', mu=pm.math.exp(log_lambda), observed=y_obs)
```

对于过度分散的计数，使用`NegativeBinomial`代替。

### 时间序列

对于自回归过程：

```python
with pm.Model() as ar_model:
    sigma = pm.HalfNormal('sigma', sigma=1)
    rho = pm.Normal('rho', mu=0, sigma=0.5, shape=ar_order)
    init_dist = pm.Normal.dist(mu=0, sigma=sigma)

    y = pm.AR('y', rho=rho, sigma=sigma, init_dist=init_dist, observed=y_obs)
```

## 模型比较

### 比较模型

使用LOO或WAIC进行模型比较：

```python
from scripts.model_comparison import compare_models, check_loo_reliability

# 拟合带有log_likelihood的模型
models = {
    'Model1': idata1,
    'Model2': idata2,
    'Model3': idata3
}

# 使用LOO比较
comparison = compare_models(models, ic='loo')

# 检查可靠性
check_loo_reliability(models)
```

**解释：**
- **Δloo < 2**：模型相似，选择更简单的模型
- **2 < Δloo < 4**：更好模型的弱证据
- **4 < Δloo < 10**：中等证据
- **Δloo > 10**：更好模型的强证据

**检查Pareto-k值：**
- k < 0.7：LOO可靠
- k > 0.7：考虑WAIC或k折CV

### 模型平均

当模型相似时，平均预测：

```python
from scripts.model_comparison import model_averaging

averaged_pred, weights = model_averaging(models, var_name='y_obs')
```

## 分布选择指南

### 用于先验

**尺度参数** (σ, τ)：
- `pm.HalfNormal('sigma', sigma=1)` - 默认选择
- `pm.Exponential('sigma', lam=1)` - 替代选择
- `pm.Gamma('sigma', alpha=2, beta=1)` - 更具信息性

**无界参数**：
- `pm.Normal('theta', mu=0, sigma=1)` - 对于标准化数据
- `pm.StudentT('theta', nu=3, mu=0, sigma=1)` - 对异常值鲁棒

**正参数**：
- `pm.LogNormal('theta', mu=0, sigma=1)`
- `pm.Gamma('theta', alpha=2, beta=1)`

**概率**：
- `pm.Beta('p', alpha=2, beta=2)` - 弱信息
- `pm.Uniform('p', lower=0, upper=1)` - 非信息（谨慎使用）

**相关矩阵**：
- `pm.LKJCorr('corr', n=n_vars, eta=2)` - eta=1 均匀，eta>1 偏好单位矩阵

### 用于似然

**连续结果**：
- `pm.Normal('y', mu=mu, sigma=sigma)` - 连续数据的默认选择
- `pm.StudentT('y', nu=nu, mu=mu, sigma=sigma)` - 对异常值鲁棒

**计数数据**：
- `pm.Poisson('y', mu=lambda)` - 等分散计数
- `pm.NegativeBinomial('y', mu=mu, alpha=alpha)` - 过度分散计数
- `pm.ZeroInflatedPoisson('y', psi=psi, mu=mu)` - 过多零值

**二元结果**：
- `pm.Bernoulli('y', p=p)` 或 `pm.Bernoulli('y', logit_p=logit_p)`

**分类结果**：
- `pm.Categorical('y', p=probs)`

**请参见：** `references/distributions.md` 以获取综合分布参考

## 采样和推断

### 使用NUTS的MCMC

对于大多数模型的默认推荐：

```python
idata = pm.sample(
    draws=2000,
    tune=1000,
    chains=4,
    target_accept=0.9,
    random_seed=42
)
```

**需要时调整：**
- 发散 → `target_accept=0.95` 或更高
- 采样缓慢 → 使用ADVI进行初始化
- 离散参数 → 对离散变量使用`pm.Metropolis()`

### 变分推断

用于探索或初始化的快速近似：

```python
with model:
    approx = pm.fit(n=20000, method='advi')

    # 用于初始化
    start = approx.sample(return_inferencedata=False)[0]
    idata = pm.sample(start=start)
```

**权衡：**
- 比MCMC快得多
- 近似（可能低估不确定性）
- 适合大型模型或快速探索

**请参见：** `references/sampling_inference.md` 以获取详细采样指南

## 诊断脚本

### 综合诊断

```python
from scripts.model_diagnostics import create_diagnostic_report

create_diagnostic_report(
    idata,
    var_names=['alpha', 'beta', 'sigma'],
    output_dir='diagnostics/'
)
```

创建：
- 迹图
- 秩图（混合检查）
- 自相关图
- 能量图
- ESS演化
- 汇总统计CSV

### 快速诊断检查

```python
from scripts.model_diagnostics import check_diagnostics

results = check_diagnostics(idata)
```

检查R-hat、ESS、发散和树深度。

## 常见问题和解决方案

### 发散

**症状：** `idata.sample_stats.diverging.sum() > 0`

**解决方案：**
1. 增加 `target_accept=0.95` 或 `0.99`
2. 使用非中心化参数化（层次模型）
3. 添加更强的先验以约束参数
4. 检查模型错误指定

### 有效样本量低

**症状：** `ESS < 400`

**解决方案：**
1. 采样更多样本：`draws=5000`
2. 重新参数化以减少后验相关性
3. 对具有相关预测变量的回归使用QR分解

### 高R-hat

**症状：** `R-hat > 1.01`

**解决方案：**
1. 运行更长的链：`tune=2000, draws=5000`
2. 检查多模态性
3. 使用ADVI改进初始化

### 采样缓慢

**解决方案：**
1. 使用ADVI初始化
2. 降低模型复杂度
3. 增加并行化：`cores=8, chains=8`
4. 在适当情况下使用变分推断

## 最佳实践

### 模型构建

1. **始终标准化预测变量**以提高采样效率
2. **使用弱信息先验**（非平坦）
3. **使用命名维度**（`dims`）以提高清晰度
4. **对层次模型使用非中心化参数化**
5. **拟合前检查先验预测**

### 采样

1. **运行多条链**（至少4条）用于收敛
2. **使用`target_accept=0.9`**作为基线（必要时更高）
3. **包含`log_likelihood=True`**用于模型比较
4. **设置随机种子**以确保可重现性

### 验证

1. **解释前检查诊断**（R-hat、ESS、发散）
2. **后验预测检查**用于模型验证
3. **适当时比较多个模型**
4. **报告不确定性**（HDI区间，而不仅仅是点估计）

### 工作流

1. 从简单开始，逐渐增加复杂度
2. 先验预测检查 → 拟合 → 诊断 → 后验预测检查
3. 基于检查迭代模型规范
4. 记录假设和先验选择

## 资源

此技能包括：

### 参考 (`references/`)

- **`distributions.md`**：按类别（连续、离散、多元、混合、时间序列）组织的PyMC分布综合目录。选择先验或似然时使用。

- **`sampling_inference.md`**：采样算法（NUTS、Metropolis、SMC）、变分推断（ADVI、SVGD）和处理采样问题的详细指南。遇到收敛问题或选择推断方法时使用。

- **`workflows.md`**：常见模型类型、数据准备、先验选择和模型验证的完整工作流示例和代码模式。作为标准贝叶斯分析的食谱使用。

### 脚本 (`scripts/`)

- **`model_diagnostics.py`**：自动诊断检查和报告生成。函数：`check_diagnostics()`用于快速检查，`create_diagnostic_report()`用于带图的综合分析。

- **`model_comparison.py`**：使用LOO/WAIC的模型比较工具。函数：`compare_models()`、`check_loo_reliability()`、`model_averaging()`。

### 模板 (`assets/`)

- **`linear_regression_template.py`**：贝叶斯线性回归的完整模板，包含完整工作流（数据准备、先验检查、拟合、诊断、预测）。

- **`hierarchical_model_template.py`**：层次/多级模型的完整模板，包含非中心化参数化和组级分析。

## 快速参考

### 模型构建
```python
with pm.Model(coords={'var': names}) as model:
    # 先验
    param = pm.Normal('param', mu=0, sigma=1, dims='var')
    # 似然
    y = pm.Normal('y', mu=..., sigma=..., observed=data)
```

### 采样
```python
idata = pm.sample(draws=2000, tune=1000, chains=4, target_accept=0.9)
```

### 诊断
```python
from scripts.model_diagnostics import check_diagnostics
check_diagnostics(idata)
```

### 模型比较
```python
from scripts.model_comparison import compare_models
compare_models({'m1': idata1, 'm2': idata2}, ic='loo')
```

### 预测
```python
with model:
    pm.set_data({'X': X_new})
    pred = pm.sample_posterior_predictive(idata.posterior)
```

## 其他说明

- PyMC与ArviZ集成用于可视化和诊断
- 使用`pm.model_to_graphviz(model)`可视化模型结构
- 使用`idata.to_netcdf('results.nc')`保存结果
- 使用`az.from_netcdf('results.nc')`加载
- 对于非常大的模型，考虑小批量ADVI或数据子采样