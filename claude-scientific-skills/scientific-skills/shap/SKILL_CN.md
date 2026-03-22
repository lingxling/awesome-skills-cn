---
name: shap
description: 使用 SHAP（SHapley 加性解释）进行模型可解释性和可解释性分析。当解释机器学习模型预测、计算特征重要性、生成 SHAP 图（瀑布图、蜂群图、条形图、散点图、力图、热力图）、调试模型、分析模型偏见或公平性、比较模型或实现可解释 AI 时，使用此技能。适用于基于树的模型（XGBoost、LightGBM、随机森林）、深度学习（TensorFlow、PyTorch）、线性模型和任何黑盒模型。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# SHAP (SHapley Additive exPlanations)

## 概述

SHAP 是一种使用合作博弈论中的 Shapley 值来解释机器学习模型输出的统一方法。此技能提供全面的指导，包括：

- 计算任何模型类型的 SHAP 值
- 创建可视化以理解特征重要性
- 调试和验证模型行为
- 分析公平性和偏见
- 在生产中实现可解释 AI

SHAP 适用于所有模型类型：基于树的模型（XGBoost、LightGBM、CatBoost、随机森林）、深度学习模型（TensorFlow、PyTorch、Keras）、线性模型和黑盒模型。

## 何时使用此技能

**当用户询问以下内容时触发此技能**：
- "解释我的模型中哪些特征最重要"
- "生成 SHAP 图"（瀑布图、蜂群图、条形图、散点图、力图、热力图等）
- "为什么我的模型做出这个预测？"
- "为我的模型计算 SHAP 值"
- "使用 SHAP 可视化特征重要性"
- "调试我的模型行为" 或 "验证我的模型"
- "检查我的模型是否有偏见" 或 "分析公平性"
- "比较模型间的特征重要性"
- "实现可解释 AI" 或 "为我的模型添加解释"
- "理解特征交互"
- "创建模型解释仪表板"

## 快速入门指南

### 步骤 1：选择正确的解释器

**决策树**：

1. **基于树的模型？**（XGBoost、LightGBM、CatBoost、随机森林、梯度提升）
   - 使用 `shap.TreeExplainer`（快速，精确）

2. **深度神经网络？**（TensorFlow、PyTorch、Keras、CNN、RNN、Transformer）
   - 使用 `shap.DeepExplainer` 或 `shap.GradientExplainer`

3. **线性模型？**（线性/逻辑回归、GLM）
   - 使用 `shap.LinearExplainer`（极快）

4. **其他模型？**（SVM、自定义函数、黑盒模型）
   - 使用 `shap.KernelExplainer`（与模型无关但较慢）

5. **不确定？**
   - 使用 `shap.Explainer`（自动选择最佳算法）

**有关所有解释器类型的详细信息，请参阅 `references/explainers.md`。**

### 步骤 2：计算 SHAP 值

```python
import shap

# 基于树的模型示例（XGBoost）
import xgboost as xgb

# 训练模型
model = xgb.XGBClassifier().fit(X_train, y_train)

# 创建解释器
explainer = shap.TreeExplainer(model)

# 计算 SHAP 值
shap_values = explainer(X_test)

# shap_values 对象包含：
# - values: SHAP 值（特征归因）
# - base_values: 预期模型输出（基线）
# - data: 原始特征值
```

### 步骤 3：可视化结果

**全局理解**（整个数据集）：
```python
# 蜂群图 - 显示特征重要性和值分布
shap.plots.beeswarm(shap_values, max_display=15)

# 条形图 - 特征重要性的清晰摘要
shap.plots.bar(shap_values)
```

**单个预测**：
```python
# 瀑布图 - 单个预测的详细分解
shap.plots.waterfall(shap_values[0])

# 力图 - 加性力可视化
shap.plots.force(shap_values[0])
```

**特征关系**：
```python
# 散点图 - 特征-预测关系
shap.plots.scatter(shap_values[:, "Feature_Name"])

# 按另一个特征着色以显示交互
shap.plots.scatter(shap_values[:, "Age"], color=shap_values[:, "Education"])
```

**有关所有绘图类型的综合指南，请参阅 `references/plots.md`。**

## 核心工作流

此技能支持几种常见工作流。选择与当前任务匹配的工作流。

### 工作流 1：基本模型解释

**目标**：了解驱动模型预测的因素

**步骤**：
1. 训练模型并创建适当的解释器
2. 计算测试集的 SHAP 值
3. 生成全局重要性图（蜂群图或条形图）
4. 检查顶部特征关系（散点图）
5. 解释特定预测（瀑布图）

**示例**：
```python
# 步骤 1-2：设置
explainer = shap.TreeExplainer(model)
shap_values = explainer(X_test)

# 步骤 3：全局重要性
shap.plots.beeswarm(shap_values)

# 步骤 4：特征关系
shap.plots.scatter(shap_values[:, "Most_Important_Feature"])

# 步骤 5：单个解释
shap.plots.waterfall(shap_values[0])
```

### 工作流 2：模型调试

**目标**：识别并修复模型问题

**步骤**：
1. 计算 SHAP 值
2. 识别预测错误
3. 解释错误分类的样本
4. 检查意外的特征重要性（数据泄漏）
5. 验证特征关系是否合理
6. 检查特征交互

**有关详细的调试工作流，请参阅 `references/workflows.md`。**

### 工作流 3：特征工程

**目标**：使用 SHAP 见解改进特征

**步骤**：
1. 计算基线模型的 SHAP 值
2. 识别非线性关系（转换候选）
3. 识别特征交互（交互项候选）
4. 设计新特征
5. 重新训练并比较 SHAP 值
6. 验证改进

**有关详细的特征工程工作流，请参阅 `references/workflows.md`。**

### 工作流 4：模型比较

**目标**：比较多个模型以选择最佳可解释选项

**步骤**：
1. 训练多个模型
2. 为每个模型计算 SHAP 值
3. 比较全局特征重要性
4. 检查特征排名的一致性
5. 分析跨模型的特定预测
6. 基于准确性、可解释性和一致性选择

**有关详细的模型比较工作流，请参阅 `references/workflows.md`。**

### 工作流 5：公平性和偏见分析

**目标**：检测和分析人口统计群体间的模型偏见

**步骤**：
1. 识别受保护的属性（性别、种族、年龄等）
2. 计算 SHAP 值
3. 比较群体间的特征重要性
4. 检查受保护属性的 SHAP 重要性
5. 识别代理特征
6. 如果发现偏见，实施缓解策略

**有关详细的公平性分析工作流，请参阅 `references/workflows.md`。**

### 工作流 6：生产部署

**目标**：将 SHAP 解释集成到生产系统中

**步骤**：
1. 训练并保存模型
2. 创建并保存解释器
3. 构建解释服务
4. 为带解释的预测创建 API 端点
5. 实现缓存和优化
6. 监控解释质量

**有关详细的生产部署工作流，请参阅 `references/workflows.md`。**

## 关键概念

### SHAP 值

**定义**：SHAP 值量化每个特征对预测的贡献，测量为与预期模型输出（基线）的偏差。

**属性**：
- **可加性**：SHAP 值总和等于预测与基线的差
- **公平性**：基于博弈论中的 Shapley 值
- **一致性**：如果特征变得更重要，其 SHAP 值会增加

**解释**：
- 正 SHAP 值 → 特征推动预测更高
- 负 SHAP 值 → 特征推动预测更低
- 幅度 → 特征影响的强度
- SHAP 值之和 → 从基线开始的总预测变化

**示例**：
```
基线（预期值）：0.30
特征贡献（SHAP 值）：
  年龄：+0.15
  收入：+0.10
  教育：-0.05
最终预测：0.30 + 0.15 + 0.10 - 0.05 = 0.50
```

### 背景数据 / 基线

**目的**：代表"典型"输入以建立基线期望

**选择**：
- 从训练数据中随机采样（50-1000 个样本）
- 或使用 kmeans 选择代表性样本
- 对于 DeepExplainer/KernelExplainer：100-1000 个样本平衡准确性和速度

**影响**：基线影响 SHAP 值的幅度但不影响相对重要性

### 模型输出类型

**关键考虑**：了解模型输出的内容

- **原始输出**：用于回归或树的边际
- **概率**：用于分类概率
- **对数几率**：用于逻辑回归（sigmoid 之前）

**示例**：XGBoost 分类器默认解释边际输出（对数几率）。要解释概率，在 TreeExplainer 中使用 `model_output="probability"`。

## 常见模式

### 模式 1：完整模型分析

```python
# 1. 设置
explainer = shap.TreeExplainer(model)
shap_values = explainer(X_test)

# 2. 全局重要性
shap.plots.beeswarm(shap_values)
shap.plots.bar(shap_values)

# 3. 顶部特征关系
top_features = X_test.columns[np.abs(shap_values.values).mean(0).argsort()[-5:]]
for feature in top_features:
    shap.plots.scatter(shap_values[:, feature])

# 4. 示例预测
for i in range(5):
    shap.plots.waterfall(shap_values[i])
```

### 模式 2：队列比较

```python
# 定义队列
cohort1_mask = X_test['Group'] == 'A'
cohort2_mask = X_test['Group'] == 'B'

# 比较特征重要性
shap.plots.bar({
    "Group A": shap_values[cohort1_mask],
    "Group B": shap_values[cohort2_mask]
})
```

### 模式 3：调试错误

```python
# 查找错误
errors = model.predict(X_test) != y_test
error_indices = np.where(errors)[0]

# 解释错误
for idx in error_indices[:5]:
    print(f"样本 {idx}:")
    shap.plots.waterfall(shap_values[idx])

    # 调查关键特征
    shap.plots.scatter(shap_values[:, "Suspicious_Feature"])
```

## 性能优化

### 速度考虑

**解释器速度**（从快到慢）：
1. `LinearExplainer` - 几乎即时
2. `TreeExplainer` - 非常快
3. `DeepExplainer` - 对神经网络快速
4. `GradientExplainer` - 对神经网络快速
5. `KernelExplainer` - 慢（仅在必要时使用）
6. `PermutationExplainer` - 非常慢但准确

### 优化策略

**对于大型数据集**：
```python
# 为子集计算 SHAP
shap_values = explainer(X_test[:1000])

# 或使用批处理
batch_size = 100
all_shap_values = []
for i in range(0, len(X_test), batch_size):
    batch_shap = explainer(X_test[i:i+batch_size])
    all_shap_values.append(batch_shap)
```

**对于可视化**：
```python
# 为图采样子集
shap.plots.beeswarm(shap_values[:1000])

# 为密集图调整透明度
shap.plots.scatter(shap_values[:, "Feature"], alpha=0.3)
```

**对于生产**：
```python
# 缓存解释器
import joblib
joblib.dump(explainer, 'explainer.pkl')
explainer = joblib.load('explainer.pkl')

# 为批量预测预计算
# 仅为 API 响应计算前 N 个特征
```

## 故障排除

### 问题：解释器选择错误
**问题**：对树模型使用 KernelExplainer（缓慢且不必要）
**解决方案**：始终对基于树的模型使用 TreeExplainer

### 问题：背景数据不足
**问题**：DeepExplainer/KernelExplainer 背景样本太少
**解决方案**：使用 100-1000 个代表性样本

### 问题：单位混淆
**问题**：将对数几率解释为概率
**解决方案**：检查模型输出类型；了解值是概率、对数几率还是原始输出

### 问题：图不显示
**问题**：Matplotlib 后端问题
**解决方案**：确保后端设置正确；必要时使用 `plt.show()`

### 问题：太多特征使图混乱
**问题**：默认 max_display=10 可能太多或太少
**解决方案**：调整 `max_display` 参数或使用特征聚类

### 问题：计算缓慢
**问题**：为非常大的数据集计算 SHAP
**解决方案**：采样子集，使用批处理，或确保使用专用解释器（非 KernelExplainer）

## 与其他工具的集成

### Jupyter 笔记本
- 交互式力图无缝工作
- 内联图显示，`show=True`（默认）
- 与 markdown 结合用于叙述性解释

### MLflow / 实验跟踪
```python
import mlflow

with mlflow.start_run():
    # 训练模型
    model = train_model(X_train, y_train)

    # 计算 SHAP
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(X_test)

    # 记录图
    shap.plots.beeswarm(shap_values, show=False)
    mlflow.log_figure(plt.gcf(), "shap_beeswarm.png")
    plt.close()

    # 记录特征重要性指标
    mean_abs_shap = np.abs(shap_values.values).mean(axis=0)
    for feature, importance in zip(X_test.columns, mean_abs_shap):
        mlflow.log_metric(f"shap_{feature}", importance)
```

### 生产 API
```python
class ExplanationService:
    def __init__(self, model_path, explainer_path):
        self.model = joblib.load(model_path)
        self.explainer = joblib.load(explainer_path)

    def predict_with_explanation(self, X):
        prediction = self.model.predict(X)
        shap_values = self.explainer(X)

        return {
            'prediction': prediction[0],
            'base_value': shap_values.base_values[0],
            'feature_contributions': dict(zip(X.columns, shap_values.values[0]))
        }
```

## 参考文档

此技能包含按主题组织的综合参考文档：

### references/explainers.md
所有解释器类的完整指南：
- `TreeExplainer` - 基于树模型的快速、精确解释
- `DeepExplainer` - 深度学习模型（TensorFlow、PyTorch）
- `KernelExplainer` - 与模型无关（适用于任何模型）
- `LinearExplainer` - 线性模型的快速解释
- `GradientExplainer` - 基于梯度的神经网络解释
- `PermutationExplainer` - 对任何模型精确但缓慢

包括：构造函数参数、方法、支持的模型、何时使用、示例、性能考虑。

### references/plots.md
综合可视化指南：
- **瀑布图** - 单个预测分解
- **蜂群图** - 全局重要性与值分布
- **条形图** - 清晰的特征重要性摘要
- **散点图** - 特征-预测关系和交互
- **力图** - 交互式加性力可视化
- **热力图** - 多样本比较网格
- **小提琴图** - 关注分布的替代方案
- **决策图** - 多类预测路径

包括：参数、用例、示例、最佳实践、图选择指南。

### references/workflows.md
详细工作流和最佳实践：
- 基本模型解释工作流
- 模型调试和验证
- 特征工程指南
- 模型比较和选择
- 公平性和偏见分析
- 深度学习模型解释
- 生产部署
- 时间序列模型解释
- 常见陷阱和解决方案
- 高级技术
- MLOps 集成

包括：分步说明、代码示例、决策标准、故障排除。

### references/theory.md
理论基础：
- 博弈论中的 Shapley 值
- 数学公式和属性
- 与其他解释方法的连接（LIME、DeepLIFT 等）
- SHAP 计算算法（Tree SHAP、Kernel SHAP 等）
- 条件期望和基线选择
- 解释 SHAP 值
- 交互值
- 理论限制和考虑

包括：数学基础、证明、比较、高级主题。

## 使用指南

**何时加载参考文件**：
- 当用户需要有关特定解释器类型或参数的详细信息时，加载 `explainers.md`
- 当用户需要详细的可视化指导或探索绘图选项时，加载 `plots.md`
- 当用户有复杂的多步骤任务（调试、公平性分析、生产部署）时，加载 `workflows.md`
- 当用户询问理论基础、Shapley 值或数学细节时，加载 `theory.md`

**默认方法**（不加载参考）：
- 使用此 SKILL.md 进行基本解释和快速入门
- 提供标准工作流和常见模式
- 如果需要更多细节，可使用参考文件

**加载参考**：
```python
# 要加载参考文件，请使用 Read 工具和适当的文件路径：
# /path/to/shap/references/explainers.md
# /path/to/shap/references/plots.md
# /path/to/shap/references/workflows.md
# /path/to/shap/references/theory.md
```

## 最佳实践摘要

1. **选择正确的解释器**：尽可能使用专用解释器（TreeExplainer、DeepExplainer、LinearExplainer）；除非必要，否则避免使用 KernelExplainer

2. **从全局开始，然后到局部**：从蜂群图/条形图开始获得整体理解，然后深入到瀑布图/散点图获取细节

3. **使用多种可视化**：不同的图揭示不同的见解；结合全局（蜂群图）+ 局部（瀑布图）+ 关系（散点图）视图

4. **选择适当的背景数据**：使用来自训练数据的 50-1000 个代表性样本

5. **了解模型输出单位**：知道是否解释概率、对数几率或原始输出

6. **使用领域知识验证**：SHAP 显示模型行为；使用领域专业知识解释和验证

7. **优化性能**：为可视化采样子集，为大型数据集批处理，在生产中缓存解释器

8. **检查数据泄漏**：异常高的特征重要性可能表明数据质量问题

9. **考虑特征相关性**：使用 TreeExplainer 的相关性感知选项或特征聚类处理冗余特征

10. **记住 SHAP 显示关联，而非因果关系**：使用领域知识进行因果解释

## 安装

```bash
# 基本安装
uv pip install shap

# 带可视化依赖
uv pip install shap matplotlib

# 最新版本
uv pip install -U shap
```

**依赖**：numpy、pandas、scikit-learn、matplotlib、scipy

**可选**：xgboost、lightgbm、tensorflow、torch（取决于模型类型）

## 其他资源

- **官方文档**：https://shap.readthedocs.io/
- **GitHub 仓库**：https://github.com/slundberg/shap
- **原始论文**：Lundberg & Lee (2017) - "A Unified Approach to Interpreting Model Predictions"
- **Nature MI 论文**：Lundberg et al. (2020) - "From local explanations to global understanding with explainable AI for trees"

此技能提供了 SHAP 在所有用例和模型类型中的模型可解释性的全面覆盖。