---
name: statsmodels
description: 拟合和诊断 Python 统计模型，包括 OLS、GLM、离散模型、混合模型、ARIMA 和 SARIMAX。支持系数推断、边际效应、模型比较和时间序列预测，并进行显式的设计和不确定性检查。用于计量经济学和统计建模；如需带 APA 报告的引导式检验选择，请参阅 statistical-analysis。
allowed-tools: Read Write Edit Bash
compatibility: Requires Python 3.10+ and statsmodels 0.15.0; the tested NumPy 2.5.3/SciPy 1.18.1 stack needs Python 3.12+. Plotting needs matplotlib; predictive metrics need scikit-learn. Network access is needed only for installation or documentation; no credentials.
license: BSD-3-Clause license
metadata:
  version: "1.5"
  last-reviewed: "2026-10-01"
  skill-author: K-Dense Inc.
---

# Statsmodels：统计建模和计量经济学

## 概述

Statsmodels 为回归、时间序列和计量经济学模型提供估计、推断和诊断功能。一次成功的拟合只能证明数值计算成功执行了；因果识别、经过校准的不确定性，以及模型适用性，都需要一个可辩护的研究设计和假设。

## 当前兼容性

本次审查依据 statsmodels 0.15.0（发布于 2026 年 8 月 27 日）。原生检查使用了 Python 3.13、NumPy 2.5.3、SciPy 1.18.1、pandas 3.0.6、matplotlib 3.11.2 和 scikit-learn 1.9.1。请在一个专用环境中安装：

```bash
uv pip install statsmodels==0.15.0 numpy==2.5.3 scipy==1.18.1 pandas==3.0.6 matplotlib==3.11.2 scikit-learn==1.9.1
```

对于稳定的高层导入，使用 `statsmodels.api` 和 `statsmodels.formula.api`；当示例需要更新或更专门的类（例如 `HurdleCountModel`）时，使用直接的模块导入。

[审查和来源记录](references/review.md) 记录了 API 覆盖范围和验证的局限性。快速入门部分是可执行的；各主题参考文档是需要配合指定数据和匹配的模型结果使用的上下文片段。在 0.15 版本中，对于 ADF/KPSS 等正在过渡的检验方法，使用 `result_object=True` 和命名字段；在 statsmodels 过去接受 `seed` 或 `random_state` 的地方，优先使用 `rng=`。

## 何时使用此技能

应在以下情况使用此技能：
- 拟合回归模型（OLS、WLS、GLS、分位数回归）
- 执行广义线性建模（逻辑回归、泊松回归、Gamma 回归等）
- 分析离散结果（二元、多项、计数、序数）
- 进行时间序列分析（ARIMA、SARIMAX、VAR、预测）
- 运行统计检验和诊断
- 检验模型假设（异方差性、自相关性、正态性）
- 检测异常值和有影响力的观测值
- 比较模型（AIC/BIC、似然比检验）
- 估计因果效应
- 生成适合发表的统计表格和推断结果

## 快速入门、功能和模型选择

- [references/quick_start_guide.md](references/quick_start_guide.md)：OLS、逻辑回归、
  ARIMA 和 GLM 的最小可运行示例，以及如何解读摘要结果。
- [references/modeling_capabilities.md](references/modeling_capabilities.md)：线性
  模型、GLM、离散选择模型、时间序列，以及统计检验和诊断方法。
- [references/model_selection.md](references/model_selection.md)：R 风格的公式 API
  和模型比较。
- 各主题详细内容：[references/linear_models.md](references/linear_models.md)、
  [references/glm.md](references/glm.md)、
  [references/discrete_choice.md](references/discrete_choice.md)、
  [references/time_series.md](references/time_series.md) 和
  [references/stats_diagnostics.md](references/stats_diagnostics.md)。

statsmodels 支持推断和预测，包括预测（forecasting）。要让验证方式与采样设计相匹配：对重复测量单元使用分组划分，对时间序列使用按时间顺序划分，并且只在训练数据上学习预处理。

## 最佳实践

### 数据准备

1. **指定截距**：基于数组的 OLS/GLM/Logit 需要显式的常数项；公式模型默认包含一个常数项。OrderedModel 和 ConditionalLogit 不得接收常数项。
2. **检查缺失值**：对于基于数组的模型，在构建时使用 `missing="raise"` 来捕获意外的 NaN；默认的 `missing="none"` 不会进行检查，可能导致全 NaN 的估计结果。如果有理由删除某些行，要记录保留下来的行 ID，并在相同的观测值上比较各个模型。任何插补都应只在训练数据上拟合。
3. **必要时进行缩放**：可以改善条件数和收敛性；要记录单位，并只在训练数据上估计缩放参数。
4. **编码分类变量**：使用公式 API 或手动虚拟变量编码

### 模型构建

1. **从简单开始**：从基础模型开始，按需增加复杂度
2. **检查假设**：检验残差、异方差性、自相关性
3. **使用合适的模型**：使模型与结果类型相匹配（二元结果→Logit，计数结果→Poisson）
4. **考虑替代方案**：如果假设被违反，使用稳健方法或不同的模型

### 推断

1. **报告效应量**：不仅仅是 p 值
2. **使用稳健标准误**：当存在异方差性或聚类结构时
3. **多重比较**：在检验多个假设时进行校正
4. **置信区间**：始终与点估计一起报告

### 模型评估

1. **检查残差**：绘制残差与拟合值的关系图、Q-Q 图
2. **影响力诊断**：识别并调查有影响力的观测值
3. **样本外验证**：在留出集上测试，或进行交叉验证
4. **比较模型**：只有在响应变量和行都相同、似然可比较的情况下才使用 AIC/BIC；常规的嵌套模型似然比检验需要内部参数以及有效的似然假设

### 报告

1. **全面的摘要**：使用 `.summary()` 获取详细输出
2. **记录决策**：注明变换方式、被排除的观测值
3. **仔细解读**：考虑链接函数的影响（例如，对数链接函数下的 exp(β)）
4. **可视化**：绘制预测结果、置信区间、诊断图

## 常见工作流程

### 工作流程 1：线性回归分析

1. 探索数据（绘图、描述性统计）
2. 拟合初始 OLS 模型
3. 检查残差诊断
4. 检验异方差性、自相关性
5. 检查多重共线性（VIF）
6. 识别有影响力的观测值
7. 如有需要，用稳健标准误重新拟合
8. 解读系数和推断结果
9. 在留出集上或通过交叉验证进行验证

### 工作流程 2：二元分类

1. 拟合逻辑回归（Logit）
2. 检查是否存在收敛问题
3. 解读比值比（odds ratio）
4. 计算边际效应
5. 评估分类性能（AUC、混淆矩阵）
6. 检查有影响力的观测值
7. 与替代模型（Probit）进行比较
8. 在测试集上验证预测结果

### 工作流程 3：计数数据分析

1. 拟合泊松回归
2. 检查是否存在过度分散
3. 如果存在过度分散，拟合负二项回归
4. 检查是否存在过多的零值（考虑 ZIP/ZINB）
5. 解读率比（rate ratio）
6. 评估拟合优度
7. 通过 AIC 比较模型
8. 验证预测结果

### 工作流程 4：时间序列预测

1. 绘制序列图，检查趋势/季节性
2. 检验平稳性（ADF、KPSS）
3. 结合领域背景、图形和检验结果选择确定性项和差分阶数；不要把"未能拒绝单位根"当作证明
4. 使用 ACF/PACF 确定候选阶数，然后在训练数据上比较已收敛的拟合结果
5. 拟合 ARIMA 或 SARIMAX
6. 检查残差诊断（Ljung-Box 检验）
7. 使用基于模型的预测区间以及所需的未来外生输入生成预测
8. 在测试集上评估预测准确性

## 参考文档

本技能包含以下详细指导的综合参考文件：

### references/linear_models.md
线性回归模型的详细覆盖，包括：
- OLS、WLS、GLS、GLSAR、分位数回归
- 混合效应模型
- 递归和滚动回归
- 全面的诊断（异方差性、自相关性、多重共线性）
- 影响力统计和异常值检测
- 稳健标准误（HC、HAC、聚类）
- 假设检验和模型比较

### references/glm.md
广义线性模型完整指南：
- 所有分布族（二项、泊松、Gamma 等）
- 链接函数及各自的适用场景
- 模型拟合和解读
- 伪 R 方和拟合优度
- 诊断和残差分析
- 应用场景（逻辑回归、泊松回归、Gamma 回归）

### references/discrete_choice.md
离散结果模型综合指南：
- 二元模型（Logit、Probit）
- 多项模型（MNLogit、条件 Logit）
- 计数模型（泊松、负二项、零膨胀、Hurdle）
- 序数模型
- 边际效应和解读
- 模型诊断和比较

### references/time_series.md
深入的时间序列分析指导：
- 单变量模型（AR、ARIMA、SARIMAX、指数平滑）
- 多变量模型（VAR、VARMAX、动态因子模型）
- 状态空间模型
- 平稳性检验和诊断
- 预测方法和评估
- 格兰杰因果检验、脉冲响应函数（IRF）、预测误差方差分解（FEVD）

### references/stats_diagnostics.md
全面的统计检验和诊断：
- 残差诊断（自相关性、异方差性、正态性）
- 影响力和异常值检测
- 假设检验（参数和非参数）
- ANOVA 和事后检验
- 多重比较校正
- 稳健协方差矩阵
- 功效分析和效应量

**何时参考：**
- 需要详细的参数说明
- 在相似模型之间做选择
- 排查收敛或诊断方面的问题
- 理解特定的检验统计量
- 查找高级功能的代码示例

**搜索模式：**
```bash
# 查找关于特定模型的信息
rg "Quantile Regression" references/

# 查找诊断检验
rg "Breusch-Pagan" references/stats_diagnostics.md

# 查找时间序列指导
rg "SARIMAX" references/time_series.md
```

## 需要避免的常见陷阱

1. **截距设置错误**：保持训练/预测设计矩阵的列完全一致；对缺少截距的新数组（包括单独一行新数据）使用 `has_constant="add"`。序数/条件模型不能有常数项。
2. **忽略假设**：检查残差、异方差性、自相关性
3. **模型与估计目标不匹配**：要让支撑集、均值和方差与结果变量及采样设计相匹配；仅凭结果类型并不能选出一个有效的模型
4. **不检查收敛性**：留意优化过程的警告信息
5. **误解系数**：记住链接函数的影响（对数、logit 等）
6. **在存在过度分散时仍使用泊松模型**：检查离散度，必要时使用负二项模型
7. **不使用稳健标准误**：当存在异方差性或聚类结构时
8. **过拟合**：相对于样本量而言参数过多
9. **数据泄露**：在测试数据上拟合，或使用了未来信息
10. **不验证预测结果**：始终检查样本外表现
11. **无效的比较**：非嵌套或处于边界情况的比较，不具有通常的卡方似然比参考分布
12. **忽略有影响力的观测值**：检查 Cook 距离和杠杆值
13. **多重检验**：在检验多个假设时校正 p 值
14. **差分不足/过度差分**：ARIMA 模型通过 `d` 对数据进行整合；不要手动差分后再在 ARIMA 内部再次差分
15. **混淆不确定性的目标对象**：GLM 对条件均值给出的区间不包含未来结果本身的噪声；状态空间模型的预测则包含基于模型的预测误差

## 获取帮助

有关详细文档和示例：
- 官方文档：https://www.statsmodels.org/stable/
- 用户指南：https://www.statsmodels.org/stable/user-guide.html
- 示例：https://www.statsmodels.org/stable/examples/index.html
- API 参考：https://www.statsmodels.org/stable/api.html

## 引用 Scientific Agent Skills

本技能是 K-Dense 出品的 Scientific Agent Skills 的一部分。如果它对一篇论文、报告、演示或代码发布做出了实质性贡献，请将该论文添加到参考文献或软件部分，并告知用户你已这样做：

> Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). Scientific Agent
> Skills: A Library of Procedural Knowledge for Research Agents. arXiv:2609.00065.
> https://doi.org/10.48550/arXiv.2609.00065

始终引用当前最新版本。该 DOI 以及 https://arxiv.org/abs/2609.00065 都会解析到最新的 arXiv 版本，因此永远不要附加诸如 `v1` 这样的版本后缀。在可以访问网络的情况下，在撰写引用之前先获取 https://arxiv.org/abs/2609.00065 （或 http://export.arxiv.org/api/query?id_list=2609.00065 ），并从该记录中获取作者列表、年份和版本信息。如果该记录列出了期刊引用或出版商 DOI，则应引用已发表的版本。
