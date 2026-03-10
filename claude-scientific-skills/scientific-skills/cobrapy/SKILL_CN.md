---
name: cobrapy
description: 用于基因组尺度代谢网络建模的 COBRApy。重建、模拟和分析代谢模型,执行 FBA、FVA、基因删除和通量采样。最适合系统生物学、代谢工程和微生物组研究。
license: LGPL-3.0 许可证
metadata:
    skill-author: K-Dense Inc.
---

# COBRApy - 基因组尺度代谢建模

## 概述

COBRApy 是用于基因组尺度代谢网络重建和分析的 Python 包。它为构建、模拟和分析代谢模型提供了全面框架,包括通量平衡分析(FBA)、通量变异性分析(FVA)、基因删除模拟和通量采样。

COBRApy 是 COBRA(约束基础重建和分析)方法学生态系统的一部分,与 MATLAB COBRA Toolbox 兼容,并与 OptFlux、RAVEN 和其他工具互操作。

## 何时使用此技能

在以下情况下使用此技能:

- **FBA 分析**: 执行通量平衡分析以预测生长速率和代谢通量
- **基因删除**: 模拟基因敲除以识别必需基因
- **反应删除**: 确定对生长至关重要的反应
- **通量采样**: 采样通量空间以了解代谢能力
- **代谢工程**: 识别过表达/删除目标以增强产物形成
- **微生物组研究**: 分析群落代谢模型
- **药物靶点识别**: 发现病原体中的必需基因
- **比较基因组学**: 比较不同生物的代谢网络
- **约束分析**: 执行 FVA 以确定通量范围
- **模型重建**: 从基因组注释构建代谢模型

## 安装

### 基本安装

```bash
uv pip install cobra
```

### 可选依赖

对于特定求解器和额外功能:

```bash
# GLPK 求解器(免费,开源)
uv pip install glpk

# CPLEX 求解器(商业)
uv pip install cplex

# Gurobi 求解器(商业)
uv pip install gurobipy

# Optlang-GLPK 接口
uv pip install optlang-glpk

# 用于绘图的可视化
uv pip install matplotlib
```

### 验证安装

```python
import cobra
print(cobra.__version__)
```

## 核心功能

### 1. 加载和创建模型

#### 加载现有模型

COBRApy 支持多种模型格式:

```python
import cobra

# 加载 SBML 模型
model = cobra.io.read_sbml_model("model.xml")

# 加载 JSON 格式
model = cobra.io.load_json_model("model.json")

# 加载 MATLAB 格式
model = cobra.io.load_matlab_model("model.mat")
```

#### 创建新模型

```python
from cobra import Model, Reaction, Metabolite

# 创建模型
model = Model("my_model")

# 添加代谢物
glc__D_e = Metabolite("glc__D_e", name="D-Glucose", compartment="e")
pyr_c = Metabolite("pyr_c", name="Pyruvate", compartment="c")

# 添加反应
EX_glc_e = Reaction("EX_glc_e")
EX_glc_e.add_metabolites({glc__D_e: -1})
EX_glc_e.lower_bound = -10  # 摄取
EX_glc_e.upper_bound = 1000

# 将反应添加到模型
model.add_reactions([EX_glc_e])
```

### 2. 通量平衡分析(FBA)

FBA 预测稳态下最大化目标函数(通常是生物量)的通量分布。

```python
# 执行 FBA
solution = model.optimize()

# 查看目标值(生长速率)
print(f"Growth rate: {solution.objective_value}")

# 查看通量
print(f"Glucose uptake: {solution.fluxes['EX_glc_e']}")
print(f"Biomass production: {solution.fluxes['BIOMASS']}")
```

#### 设置目标

```python
# 设置目标反应
model.objective = "BIOMASS"

# 设置多个目标(线性组合)
model.objective = {"BIOMASS": 1.0, "PROD": 0.5}

# 查看当前目标
print(model.objective)
```

#### 修改边界

```python
# 限制葡萄糖摄取
model.reactions.EX_glc_e.lower_bound = -5  # 最大摄取 5 mmol/gDW/h

# 设置反应为不可逆
model.reactions.R1.lower_bound = 0

# 完全关闭反应
model.reactions.R2.lower_bound = 0
model.reactions.R2.upper_bound = 0
```

### 3. 通量变异性分析(FVA)

FVA 确定给定目标值下每个反应的最小和最大可能通量。

```python
from cobra.flux_analysis import flux_variability_analysis

# 执行 FVA
fva_result = flux_variability_analysis(model)

# 查看结果
print(fva_result.head())

# 查看特定反应
print(f"Glucose uptake range: {fva_result.loc['EX_glc_e']}")
```

#### 带循环的 FVA

```python
# 带循环的 FVA(计算量更大但更准确)
fva_result = flux_variability_analysis(
    model,
    loopless=True,
    fraction_of_optimum=0.9  # 90% 最优
)
```

### 4. 基因删除分析

模拟基因敲除以识别必需基因。

```python
from cobra.flux_analysis import single_gene_deletion

# 单基因删除
deletion_results = single_gene_deletion(model)

# 查看必需基因
essential_genes = deletion_results[deletion_results["growth"] < 0.01]
print(f"Essential genes: {essential_genes.index.tolist()}")
```

#### 双基因删除

```python
from cobra.flux_analysis import double_gene_deletion

# 双基因删除(计算量大)
double_deletion = double_gene_deletion(model)

# 查看合成致死对
synthetic_lethal = double_deletion[double_deletion["growth"] < 0.01]
```

### 5. 反应删除分析

模拟反应敲除以识别必需反应。

```python
from cobra.flux_analysis import single_reaction_deletion

# 单反应删除
reaction_deletion = single_reaction_deletion(model)

# 查看必需反应
essential_reactions = reaction_deletion[reaction_deletion["growth"] < 0.01]
```

### 6. 通量采样

从通量空间采样以了解代谢能力。

```python
from cobra.sampling import sample

# 采样通量分布
samples = sample(model, n=1000)

# 分析采样结果
print(samples.describe())

# 绘制通量分布
import matplotlib.pyplot as plt
samples["EX_glc_e"].hist()
plt.xlabel("Glucose uptake flux")
plt.ylabel("Frequency")
plt.show()
```

#### ACHR 采样

```python
# 使用 ACHR 算法采样(更快)
samples = sample(model, n=1000, method="achr")
```

### 7. 模型操纵

#### 添加反应

```python
# 创建新反应
reaction = Reaction("NEW_RXN")
reaction.add_metabolites({
    "A_c": -1,
    "B_c": 1
})
reaction.lower_bound = -1000
reaction.upper_bound = 1000

# 添加到模型
model.add_reactions([reaction])
```

#### 删除反应

```python
# 删除反应
model.remove_reactions(["R1", "R2"])
```

#### 修改化学计量

```python
# 修改反应化学计量
reaction = model.reactions.R1
reaction.add_metabolites({"A_c": 1})  # 添加 A_c 作为产物
reaction.add_metabolites({"B_c": -1})  # 添加 B_c 作为反应物
```

### 8. 模型分析和可视化

#### 模型摘要

```python
# 查看模型摘要
model.summary()

# 查看代谢物摘要
model.metabolites.glc__D_e.summary()
```

#### 通量可视化

```python
import matplotlib.pyplot as plt

# 绘制通量分布
solution.fluxes.plot(kind="bar")
plt.xlabel("Reaction")
plt.ylabel("Flux")
plt.show()
```

#### 通路分析

```python
# 按通路分组反应
from cobra.flux_analysis import flux_variability_analysis

fva_result = flux_variability_analysis(model)

# 计算通路通量
pathway_fluxes = {}
for pathway, reactions in model.groups.items():
    pathway_fluxes[pathway] = fva_result.loc[reactions].sum()

print(pathway_fluxes)
```

### 9. 模型比较

比较不同条件或生物的模型。

```python
# 加载两个模型
model1 = cobra.io.read_sbml_model("model1.xml")
model2 = cobra.io.read_sbml_model("model2.xml")

# 比较反应
reactions_in_1_not_2 = set(model1.reactions) - set(model2.reactions)
reactions_in_2_not_1 = set(model2.reactions) - set(model1.reactions)

print(f"Reactions unique to model 1: {len(reactions_in_1_not_2)}")
print(f"Reactions unique to model 2: {len(reactions_in_2_not_1)}")
```

### 10. 约束建模

添加自定义约束到模型。

```python
from cobra import Model, Reaction, Metabolite

# 添加约束: 反应 A + 反应 B <= 10
constraint = Reaction("constraint")
constraint.add_metabolites({
    "A_c": 1,
    "B_c": 1
})
constraint.upper_bound = 10

model.add_reactions([constraint])
```

## 高级功能

### 1. 动态 FBA

模拟随时间变化的代谢。

```python
from cobra.flux_analysis import dynamic_fba

# 动态 FBA 模拟
result = dynamic_fba(model, time_points=[0, 1, 2, 3, 4, 5])

# 绘制生长曲线
result["biomass"].plot()
plt.xlabel("Time")
plt.ylabel("Biomass")
plt.show()
```

### 2. 基因表达整合

整合基因表达数据与代谢模型。

```python
# 基于表达数据设置反应边界
expression_data = {"R1": 10, "R2": 5, "R3": 0}

for reaction, expression in expression_data.items():
    if expression == 0:
        model.reactions[reaction].lower_bound = 0
        model.reactions[reaction].upper_bound = 0
```

### 3. 代谢工程

识别代谢工程靶点。

```python
from cobra.flux_analysis import (
    flux_variability_analysis,
    single_gene_deletion
)

# 识别过表达靶点
fva_result = flux_variability_analysis(model)
high_flux_reactions = fva_result[fva_result["maximum"] > 100]

# 识别删除靶点
essential_genes = single_gene_deletion(model)
essential_genes = essential_genes[essential_genes["growth"] < 0.01]
```

### 4. 微生物组建模

分析群落代谢模型。

```python
# 创建群落模型
from cobra import Model

community = Model("community")

# 添加多个生物的代谢物
# (需要协调交换反应)
```

## 最佳实践

### 1. 模型质量

- **验证模型**: 使用 `model.sanity_check()` 检查模型一致性
- **检查质量平衡**: 确保反应是质量平衡的
- **验证边界**: 确保边界合理
- **检查可解性**: 确保模型有可行解

### 2. 求解器选择

- **GLPK**: 免费、开源,适合小型模型
- **CPLEX/Gurobi**: 商业求解器,更快,适合大型模型
- **Optlang**: 统一求解器接口,推荐用于新项目

### 3. 性能优化

- **使用稀疏矩阵**: 大型模型使用稀疏矩阵表示
- **缓存结果**: 缓存 FBA/FVA 结果以避免重复计算
- **并行计算**: 使用并行处理进行删除分析
- **简化模型**: 删除不必要的反应和代谢物

### 4. 数据管理

- **版本控制**: 使用 Git 跟踪模型更改
- **文档记录**: 记录模型来源和修改
- **备份模型**: 定期备份模型文件
- **使用标准格式**: 使用 SBML 格式以确保互操作性

## 常见问题

### 模型无解

```python
# 检查模型是否有可行解
solution = model.optimize()
if solution.status == "infeasible":
    print("Model is infeasible")
    # 检查约束
    model.sanity_check()
```

### 求解器错误

```python
# 更改求解器
from cobra import Configuration
config = Configuration()
config.solver = "glpk"
```

### 内存问题

```python
# 使用稀疏矩阵
from scipy import sparse
# (COBRApy 自动使用稀疏矩阵)

# 减少模型大小
model.remove_reactions([r for r in model.reactions if r.fluxes == 0])
```

## 资源

### 官方文档

- COBRApy 文档: https://cobrapy.readthedocs.io/
- COBRA Toolbox: https://opencobra.github.io/cobratoolbox/
- BiGG Models 数据库: http://bigg.ucsd.edu/

### 教程和示例

- COBRApy 教程: https://cobrapy.readthedocs.io/en/latest/tutorial.html
- 示例笔记本: https://github.com/opencobra/cobrapy/tree/master/documentation/build/html/examples

### 社区资源

- COBRA 邮件列表: https://groups.google.com/g/cobra-toolbox
- GitHub 仓库: https://github.com/opencobra/cobrapy
- 论坛: https://groups.google.com/g/cobra-toolbox

## 依赖项

### 必需依赖

- Python >= 3.6
- optlang >= 1.4.0
- pandas >= 1.0.0
- future >= 0.18.0
- swiglpk >= 1.4.0(或 glpk)

### 可选依赖

- matplotlib(可视化)
- scipy(高级分析)
- numpy(数值计算)
- cplex/gurobi(商业求解器)
- libsbml(SBML 解析)

## 示例工作流程

### 示例 1: 基因组尺度 FBA

```python
import cobra

# 加载模型
model = cobra.io.read_sbml_model("e_coli_core.xml")

# 执行 FBA
solution = model.optimize()

# 查看结果
print(f"Growth rate: {solution.objective_value}")
print(f"Glucose uptake: {solution.fluxes['EX_glc_e']}")
print(f"Biomass: {solution.fluxes['BIOMASS_Ec_iJO1366_core_53p95M']}")
```

### 示例 2: 识别必需基因

```python
from cobra.flux_analysis import single_gene_deletion

# 单基因删除
deletion_results = single_gene_deletion(model)

# 查看必需基因
essential_genes = deletion_results[deletion_results["growth"] < 0.01]
print(f"Essential genes: {essential_genes.index.tolist()}")
```

### 示例 3: 通量变异性分析

```python
from cobra.flux_analysis import flux_variability_analysis

# 执行 FVA
fva_result = flux_variability_analysis(model)

# 查看高变异性反应
high_variability = fva_result[
    (fva_result["maximum"] - fva_result["minimum"]) > 10
]
print(f"High variability reactions: {high_variability.index.tolist()}")
```

### 示例 4: 代谢工程

```python
# 识别过表达靶点
fva_result = flux_variability_analysis(model)
high_flux_reactions = fva_result[fva_result["maximum"] > 100]

# 识别删除靶点
essential_genes = single_gene_deletion(model)
non_essential = essential_genes[essential_genes["growth"] > 0.01]

# 组合结果
engineering_targets = set(high_flux_reactions.index) & set(non_essential.index)
print(f"Engineering targets: {engineering_targets}")
```

## 摘要

COBRApy 是用于基因组尺度代谢建模的强大 Python 包,提供:

1. **全面的 FBA 分析**: 通量平衡分析和优化
2. **基因/反应删除**: 识别必需基因和反应
3. **通量变异性分析**: 确定通量范围
4. **通量采样**: 采样通量空间
5. **模型操纵**: 添加/删除/修改反应
6. **高级功能**: 动态 FBA、基因表达整合、代谢工程
7. **互操作性**: 与 COBRA Toolbox 和其他工具兼容

使用 COBRApy 进行系统生物学、代谢工程和微生物组研究。
