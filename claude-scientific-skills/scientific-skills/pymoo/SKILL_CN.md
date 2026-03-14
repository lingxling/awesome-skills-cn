---
name: pymoo
description: 多目标优化框架。NSGA-II、NSGA-III、MOEA/D、帕累托前沿、约束处理、基准测试（ZDT、DTLZ），用于工程设计和优化问题。
license: Apache-2.0 license
metadata:
    skill-author: K-Dense Inc.
---

# Pymoo - Python中的多目标优化

## 概述

Pymoo是一个全面的Python优化框架，重点关注多目标问题。使用最先进的算法（NSGA-II/III、MOEA/D）、基准测试问题（ZDT、DTLZ）、可定制的遗传算子和多准则决策方法来解决单目标和多目标优化问题。擅长为具有冲突目标的问题找到权衡解决方案（帕累托前沿）。

## 使用场景

当您需要以下操作时使用此技能：
- 解决具有一个或多个目标的优化问题
- 寻找帕累托最优解并分析权衡
- 实现进化算法（GA、DE、PSO、NSGA-II/III）
- 处理约束优化问题
- 在标准测试问题上基准测试算法（ZDT、DTLZ、WFG）
- 定制遗传算子（交叉、变异、选择）
- 可视化高维优化结果
- 从多个竞争解决方案中做出决策
- 处理二元、离散、连续或混合变量问题

## 核心概念

### 统一接口

Pymoo使用一致的`minimize()`函数处理所有优化任务：

```python
from pymoo.optimize import minimize

result = minimize(
    problem,        # 优化什么
    algorithm,      # 如何优化
    termination,    # 何时停止
    seed=1,
    verbose=True
)
```

**结果对象包含：**
- `result.X`：最优解的决策变量
- `result.F`：最优解的目标值
- `result.G`：约束违反（如果有约束）
- `result.algorithm`：带历史记录的算法对象

### 问题类型

**单目标：** 一个需要最小化/最大化的目标
**多目标：** 2-3个冲突目标 → 帕累托前沿
**多目标（高维）：** 4+个目标 → 高维帕累托前沿
**约束：** 目标 + 不等式/等式约束
**动态：** 时变目标或约束

## 快速开始工作流

### 工作流1：单目标优化

**适用场景：** 优化一个目标函数

**步骤：**
1. 定义或选择问题
2. 选择单目标算法（GA、DE、PSO、CMA-ES）
3. 配置终止准则
4. 运行优化
5. 提取最佳解

**示例：**
```python
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.problems import get_problem
from pymoo.optimize import minimize

# 内置问题
problem = get_problem("rastrigin", n_var=10)

# 配置遗传算法
algorithm = GA(
    pop_size=100,
    eliminate_duplicates=True
)

# 优化
result = minimize(
    problem,
    algorithm,
    ('n_gen', 200),
    seed=1,
    verbose=True
)

print(f"Best solution: {result.X}")
print(f"Best objective: {result.F[0]}")
```

**请参见：** `scripts/single_objective_example.py` 获取完整示例

### 工作流2：多目标优化（2-3个目标）

**适用场景：** 优化2-3个冲突目标，需要帕累托前沿

**算法选择：** NSGA-II（标准的双/三目标算法）

**步骤：**
1. 定义多目标问题
2. 配置NSGA-II
3. 运行优化以获得帕累托前沿
4. 可视化权衡
5. 应用决策（可选）

**示例：**
```python
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter

# 双目标基准问题
problem = get_problem("zdt1")

# NSGA-II算法
algorithm = NSGA2(pop_size=100)

# 优化
result = minimize(problem, algorithm, ('n_gen', 200), seed=1)

# 可视化帕累托前沿
plot = Scatter()
plot.add(result.F, label="Obtained Front")
plot.add(problem.pareto_front(), label="True Front", alpha=0.3)
plot.show()

print(f"Found {len(result.F)} Pareto-optimal solutions")
```

**请参见：** `scripts/multi_objective_example.py` 获取完整示例

### 工作流3：多目标优化（4+个目标）

**适用场景：** 优化4个或更多目标

**算法选择：** NSGA-III（专为多目标设计）

**关键区别：** 必须提供参考方向以指导种群

**步骤：**
1. 定义多目标问题
2. 生成参考方向
3. 配置带有参考方向的NSGA-III
4. 运行优化
5. 使用平行坐标图可视化

**示例：**
```python
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.visualization.pcp import PCP

# 多目标问题（5个目标）
problem = get_problem("dtlz2", n_obj=5)

# 生成参考方向（NSGA-III必需）
ref_dirs = get_reference_directions("das-dennis", n_dim=5, n_partitions=12)

# 配置NSGA-III
algorithm = NSGA3(ref_dirs=ref_dirs)

# 优化
result = minimize(problem, algorithm, ('n_gen', 300), seed=1)

# 使用平行坐标可视化
plot = PCP(labels=[f"f{i+1}" for i in range(5)])
plot.add(result.F, alpha=0.3)
plot.show()
```

**请参见：** `scripts/many_objective_example.py` 获取完整示例

### 工作流4：自定义问题定义

**适用场景：** 解决特定领域的优化问题

**步骤：**
1. 扩展`ElementwiseProblem`类
2. 在`__init__`中定义问题维度和边界
3. 实现`_evaluate`方法用于目标（和约束）
4. 与任何算法一起使用

**无约束示例：**
```python
from pymoo.core.problem import ElementwiseProblem
import numpy as np

class MyProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2,              # 变量数量
            n_obj=2,              # 目标数量
            xl=np.array([0, 0]),  # 下界
            xu=np.array([5, 5])   # 上界
        )

    def _evaluate(self, x, out, *args, **kwargs):
        # 定义目标
        f1 = x[0]**2 + x[1]**2
        f2 = (x[0]-1)**2 + (x[1]-1)**2

        out["F"] = [f1, f2]
```

**有约束示例：**
```python
class ConstrainedProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2,
            n_obj=2,
            n_ieq_constr=2,        # 不等式约束
            n_eq_constr=1,         # 等式约束
            xl=np.array([0, 0]),
            xu=np.array([5, 5])
        )

    def _evaluate(self, x, out, *args, **kwargs):
        # 目标
        out["F"] = [f1, f2]

        # 不等式约束 (g <= 0)
        out["G"] = [g1, g2]

        # 等式约束 (h = 0)
        out["H"] = [h1]
```

**约束公式规则：**
- 不等式：表示为 `g(x) <= 0`（当 ≤ 0 时可行）
- 等式：表示为 `h(x) = 0`（当 = 0 时可行）
- 将 `g(x) >= b` 转换为 `-(g(x) - b) <= 0`

**请参见：** `scripts/custom_problem_example.py` 获取完整示例

### 工作流5：约束处理

**适用场景：** 问题具有可行性约束

**方法选项：**

**1. 可行性优先（默认 - 推荐）**
```python
from pymoo.algorithms.moo.nsga2 import NSGA2

# 自动处理约束问题
algorithm = NSGA2(pop_size=100)
result = minimize(problem, algorithm, termination)

# 检查可行性
feasible = result.CV[:, 0] == 0  # CV = 约束违反
print(f"Feasible solutions: {np.sum(feasible)}")
```

**2. 惩罚方法**
```python
from pymoo.constraints.as_penalty import ConstraintsAsPenalty

# 将约束包装为惩罚
problem_penalized = ConstraintsAsPenalty(problem, penalty=1e6)
```

**3. 约束作为目标**
```python
from pymoo.constraints.as_obj import ConstraintsAsObjective

# 将约束违反作为附加目标
problem_with_cv = ConstraintsAsObjective(problem)
```

**4. 专门算法**
```python
from pymoo.algorithms.soo.nonconvex.sres import SRES

# SRES 内置约束处理
algorithm = SRES()
```

**请参见：** `references/constraints_mcdm.md` 获取综合约束处理指南

### 工作流6：从帕累托前沿做出决策

**适用场景：** 有帕累托前沿，需要选择首选解决方案

**步骤：**
1. 运行多目标优化
2. 将目标归一化到 [0, 1]
3. 定义偏好权重
4. 应用MCDM方法
5. 可视化所选解决方案

**使用伪权重的示例：**
```python
from pymoo.mcdm.pseudo_weights import PseudoWeights
import numpy as np

# 从多目标优化获得结果后
# 归一化目标
F_norm = (result.F - result.F.min(axis=0)) / (result.F.max(axis=0) - result.F.min(axis=0))

# 定义偏好（必须总和为1）
weights = np.array([0.3, 0.7])  # 30% f1, 70% f2

# 应用决策
 dm = PseudoWeights(weights)
selected_idx = dm.do(F_norm)

# 获取所选解决方案
best_solution = result.X[selected_idx]
best_objectives = result.F[selected_idx]

print(f"Selected solution: {best_solution}")
print(f"Objective values: {best_objectives}")
```

**其他MCDM方法：**
- 折衷编程：选择最接近理想点的解
- 拐点：找到平衡的权衡解决方案
- 超体积贡献：选择最多样化的子集

**请参见：**
- `scripts/decision_making_example.py` 获取完整示例
- `references/constraints_mcdm.md` 获取详细的MCDM方法

### 工作流7：可视化

**根据目标数量选择可视化：**

**2个目标：散点图**
```python
from pymoo.visualization.scatter import Scatter

plot = Scatter(title="Bi-objective Results")
plot.add(result.F, color="blue", alpha=0.7)
plot.show()
```

**3个目标：3D散点**
```python
plot = Scatter(title="Tri-objective Results")
plot.add(result.F)  # 自动以3D渲染
plot.show()
```

**4+个目标：平行坐标图**
```python
from pymoo.visualization.pcp import PCP

plot = PCP(
    labels=[f"f{i+1}" for i in range(n_obj)],
    normalize_each_axis=True
)
plot.add(result.F, alpha=0.3)
plot.show()
```

**解决方案比较：花瓣图**
```python
from pymoo.visualization.petal import Petal

plot = Petal(
    bounds=[result.F.min(axis=0), result.F.max(axis=0)],
    labels=["Cost", "Weight", "Efficiency"]
)
plot.add(solution_A, label="Design A")
plot.add(solution_B, label="Design B")
plot.show()
```

**请参见：** `references/visualization.md` 获取所有可视化类型和用法

## 算法选择指南

### 单目标问题

| 算法 | 最适合 | 关键特性 |
|------|--------|----------|
| **GA** | 通用 | 灵活，可定制算子 |
| **DE** | 连续优化 | 良好的全局搜索 |
| **PSO** | 平滑景观 | 快速收敛 |
| **CMA-ES** | 困难/噪声问题 | 自适应 |

### 多目标问题（2-3个目标）

| 算法 | 最适合 | 关键特性 |
|------|--------|----------|
| **NSGA-II** | 标准基准 | 快速，可靠，经过充分测试 |
| **R-NSGA-II** | 偏好区域 | 参考点指导 |
| **MOEA/D** | 可分解问题 | 标量化方法 |

### 多目标问题（4+个目标）

| 算法 | 最适合 | 关键特性 |
|------|--------|----------|
| **NSGA-III** | 4-15个目标 | 基于参考方向 |
| **RVEA** | 自适应搜索 | 参考向量进化 |
| **AGE-MOEA** | 复杂景观 | 自适应几何 |

### 约束问题

| 方法 | 算法 | 何时使用 |
|------|------|----------|
| 可行性优先 | 任何算法 | 大可行区域 |
| 专门 | SRES, ISRES | 重约束 |
| 惩罚 | GA + 惩罚 | 算法兼容性 |

**请参见：** `references/algorithms.md` 获取综合算法参考

## 基准问题

### 快速问题访问：
```python
from pymoo.problems import get_problem

# 单目标
problem = get_problem("rastrigin", n_var=10)
problem = get_problem("rosenbrock", n_var=10)

# 多目标
problem = get_problem("zdt1")        # 凸前沿
problem = get_problem("zdt2")        # 非凸前沿
problem = get_problem("zdt3")        # 不连续前沿

# 多目标（高维）
problem = get_problem("dtlz2", n_obj=5, n_var=12)
problem = get_problem("dtlz7", n_obj=4)
```

**请参见：** `references/problems.md` 获取完整测试问题参考

## 遗传算子定制

### 标准算子配置：
```python
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM

algorithm = GA(
    pop_size=100,
    crossover=SBX(prob=0.9, eta=15),
    mutation=PM(eta=20),
    eliminate_duplicates=True
)
```

### 按变量类型选择算子：

**连续变量：**
- 交叉：SBX（模拟二进制交叉）
- 变异：PM（多项式变异）

**二元变量：**
- 交叉：TwoPointCrossover, UniformCrossover
- 变异：BitflipMutation

**排列（TSP、调度）：**
- 交叉：OrderCrossover (OX)
- 变异：InversionMutation

**请参见：** `references/operators.md` 获取综合算子参考

## 性能和故障排除

### 常见问题和解决方案：

**问题：算法不收敛**
- 增加种群大小
- 增加代数
- 检查问题是否为多模态（尝试不同算法）
- 验证约束是否正确制定

**问题：帕累托前沿分布差**
- 对于NSGA-III：调整参考方向
- 增加种群大小
- 检查重复消除
- 验证问题缩放

**问题：可行解少**
- 使用约束作为目标的方法
- 应用修复算子
- 尝试SRES/ISRES处理约束问题
- 检查约束公式（应为g <= 0）

**问题：计算成本高**
- 减少种群大小
- 减少代数
- 使用更简单的算子
- 启用并行化（如果问题支持）

### 最佳实践：

1. **当尺度差异显著时归一化目标**
2. **设置随机种子**以确保可重现性
3. **保存历史**以分析收敛：`save_history=True`
4. **可视化结果**以了解解决方案质量
5. **与真实帕累托前沿比较**（如果可用）
6. **使用适当的终止准则**（代数、评估、容差）
7. **根据问题特征调整算子参数**

## 资源

此技能包括综合参考文档和可执行示例：

### references/
深入理解的详细文档：

- **algorithms.md**：完整的算法参考，包含参数、用法和选择指南
- **problems.md**：基准测试问题（ZDT、DTLZ、WFG）及其特征
- **operators.md**：遗传算子（采样、选择、交叉、变异）及其配置
- **visualization.md**：所有可视化类型，包含示例和选择指南
- **constraints_mcdm.md**：约束处理技术和多准则决策方法

**参考搜索模式：**
- 算法详情：`grep -r "NSGA-II\|NSGA-III\|MOEA/D" references/`
- 约束方法：`grep -r "Feasibility First\|Penalty\|Repair" references/`
- 可视化类型：`grep -r "Scatter\|PCP\|Petal" references/`

### scripts/
演示常见工作流的可执行示例：

- **single_objective_example.py**：使用GA的基本单目标优化
- **multi_objective_example.py**：使用NSGA-II的多目标优化，带可视化
- **many_objective_example.py**：使用NSGA-III的多目标优化，带参考方向
- **custom_problem_example.py**：定义自定义问题（有约束和无约束）
- **decision_making_example.py**：具有不同偏好的多准则决策

**运行示例：**
```bash
python3 scripts/single_objective_example.py
python3 scripts/multi_objective_example.py
python3 scripts/many_objective_example.py
python3 scripts/custom_problem_example.py
python3 scripts/decision_making_example.py
```

## 其他说明

**安装：**
```bash
uv pip install pymoo
```

**依赖：** NumPy, SciPy, matplotlib, autograd（梯度基于方法的可选依赖）

**文档：** https://pymoo.org/

**版本：** 此技能基于pymoo 0.6.x

**常见模式：**
- 始终使用`ElementwiseProblem`处理自定义问题
- 约束公式为`g(x) <= 0`和`h(x) = 0`
- NSGA-III需要参考方向
- MCDM前归一化目标
- 使用适当的终止：`('n_gen', N)`或`get_termination("f_tol", tol=0.001)`