---
name: sympy
description: 当在Python中处理符号数学时使用此技能。此技能应用于符号计算任务，包括代数求解方程、执行微积分操作（导数、积分、极限）、操作代数表达式、符号矩阵运算、物理计算、数论问题、几何计算，以及从数学表达式生成可执行代码。当用户需要精确的符号结果而不是数值近似，或处理包含变量和参数的数学公式时，应用此技能。
license: https://github.com/sympy/sympy/blob/master/LICENSE
metadata:
    skill-author: K-Dense Inc.
---

# SymPy - Python中的符号数学

## 概述

SymPy是一个Python库，用于符号数学，能够使用数学符号而不是数值近似进行精确计算。此技能提供使用SymPy执行符号代数、微积分、线性代数、方程求解、物理计算和代码生成的综合指导。

## 何时使用此技能

在以下情况使用此技能：
- 符号求解方程（代数、微分、方程组）
- 执行微积分操作（导数、积分、极限、级数）
- 操作和简化代数表达式
- 符号处理矩阵和线性代数
- 进行物理计算（力学、量子力学、矢量分析）
- 数论计算（素数、因式分解、模运算）
- 几何计算（2D/3D几何、解析几何）
- 将数学表达式转换为可执行代码（Python、C、Fortran）
- 生成LaTeX或其他格式化数学输出
- 需要精确的数学结果（例如，`sqrt(2)` 而非 `1.414...`）

## 核心能力

### 1. 符号计算基础

**创建符号和表达式：**
```python
from sympy import symbols, Symbol
x, y, z = symbols('x y z')
expr = x**2 + 2*x + 1

# 带假设
x = symbols('x', real=True, positive=True)
n = symbols('n', integer=True)
```

**简化和操作：**
```python
from sympy import simplify, expand, factor, cancel
simplify(sin(x)**2 + cos(x)**2)  # 返回 1
expand((x + 1)**3)  # x**3 + 3*x**2 + 3*x + 1
factor(x**2 - 1)    # (x - 1)*(x + 1)
```

**详细基础：** 参见 `references/core-capabilities.md`

### 2. 微积分

**导数：**
```python
from sympy import diff
diff(x**2, x)        # 2*x
diff(x**4, x, 3)     # 24*x (三阶导数)
diff(x**2*y**3, x, y)  # 6*x*y**2 (偏导数)
```

**积分：**
```python
from sympy import integrate, oo
integrate(x**2, x)              # x**3/3 (不定积分)
integrate(x**2, (x, 0, 1))      # 1/3 (定积分)
integrate(exp(-x), (x, 0, oo))  # 1 (广义积分)
```

**极限和级数：**
```python
from sympy import limit, series
limit(sin(x)/x, x, 0)  # 1
series(exp(x), x, 0, 6)  # 1 + x + x**2/2 + x**3/6 + x**4/24 + x**5/120 + O(x**6)
```

**详细微积分操作：** 参见 `references/core-capabilities.md`

### 3. 方程求解

**代数方程：**
```python
from sympy import solveset, solve, Eq
solveset(x**2 - 4, x)  # {-2, 2}
solve(Eq(x**2, 4), x)  # [-2, 2]
```

**方程组：**
```python
from sympy import linsolve, nonlinsolve
linsolve([x + y - 2, x - y], x, y)  # {(1, 1)} (线性)
nonlinsolve([x**2 + y - 2, x + y**2 - 3], x, y)  # (非线性)
```

**微分方程：**
```python
from sympy import Function, dsolve, Derivative
f = symbols('f', cls=Function)
dsolve(Derivative(f(x), x) - f(x), f(x))  # Eq(f(x), C1*exp(x))
```

**详细求解方法：** 参见 `references/core-capabilities.md`

### 4. 矩阵和线性代数

**矩阵创建和操作：**
```python
from sympy import Matrix, eye, zeros
M = Matrix([[1, 2], [3, 4]])
M_inv = M**-1  # 逆
M.det()        # 行列式
M.T            # 转置
```

**特征值和特征向量：**
```python
eigenvals = M.eigenvals()  # {特征值: 重数}
eigenvects = M.eigenvects()  # [(特征值, 重数, [特征向量])]
P, D = M.diagonalize()  # M = P*D*P^-1
```

**求解线性系统：**
```python
A = Matrix([[1, 2], [3, 4]])
b = Matrix([5, 6])
x = A.solve(b)  # 求解 Ax = b
```

**综合线性代数：** 参见 `references/matrices-linear-algebra.md`

### 5. 物理和力学

**经典力学：**
```python
from sympy.physics.mechanics import dynamicsymbols, LagrangesMethod
from sympy import symbols

# 定义系统
q = dynamicsymbols('q')
m, g, l = symbols('m g l')

# 拉格朗日量 (T - V)
L = m*(l*q.diff())**2/2 - m*g*l*(1 - cos(q))

# 应用拉格朗日方法
LM = LagrangesMethod(L, [q])
```

**矢量分析：**
```python
from sympy.physics.vector import ReferenceFrame, dot, cross
N = ReferenceFrame('N')
v1 = 3*N.x + 4*N.y
v2 = 1*N.x + 2*N.z
dot(v1, v2)  # 点积
cross(v1, v2)  # 叉积
```

**量子力学：**
```python
from sympy.physics.quantum import Ket, Bra, Commutator
psi = Ket('psi')
A = Operator('A')
comm = Commutator(A, B).doit()
```

**详细物理能力：** 参见 `references/physics-mechanics.md`

### 6. 高级数学

该技能包括对以下内容的全面支持：

- **几何：** 2D/3D解析几何、点、线、圆、多边形、变换
- **数论：** 素数、因式分解、GCD/LCM、模运算、丢番图方程
- **组合数学：** 排列、组合、分拆、群论
- **逻辑和集合：** 布尔逻辑、集合论、有限和无限集合
- **统计学：** 概率分布、随机变量、期望、方差
- **特殊函数：** Gamma、Bessel、正交多项式、超几何函数
- **多项式：** 多项式代数、根、因式分解、Groebner基

**详细高级主题：** 参见 `references/advanced-topics.md`

### 7. 代码生成和输出

**转换为可执行函数：**
```python
from sympy import lambdify
import numpy as np

expr = x**2 + 2*x + 1
f = lambdify(x, expr, 'numpy')  # 创建NumPy函数
x_vals = np.linspace(0, 10, 100)
y_vals = f(x_vals)  # 快速数值评估
```

**生成C/Fortran代码：**
```python
from sympy.utilities.codegen import codegen
[(c_name, c_code), (h_name, h_header)] = codegen(
    ('my_func', expr), 'C'
)
```

**LaTeX输出：**
```python
from sympy import latex
latex_str = latex(expr)  # 转换为LaTeX用于文档
```

**综合代码生成：** 参见 `references/code-generation-printing.md`

## 使用SymPy的最佳实践

### 1. 始终首先定义符号

```python
from sympy import symbols
x, y, z = symbols('x y z')
# 现在x, y, z可以用于表达式
```

### 2. 使用假设获得更好的简化

```python
x = symbols('x', positive=True, real=True)
sqrt(x**2)  # 返回 x（而非 Abs(x)），因为有正假设
```

常见假设：`real`, `positive`, `negative`, `integer`, `rational`, `complex`, `even`, `odd`

### 3. 使用精确算术

```python
from sympy import Rational, S
# 正确（精确）：
expr = Rational(1, 2) * x
expr = S(1)/2 * x

# 错误（浮点数）：
expr = 0.5 * x  # 创建近似值
```

### 4. 在需要时进行数值评估

```python
from sympy import pi, sqrt
result = sqrt(8) + pi
result.evalf()    # 5.96371554103586
result.evalf(50)  # 50位精度
```

### 5. 转换为NumPy以提高性能

```python
# 多次评估时较慢：
for x_val in range(1000):
    result = expr.subs(x, x_val).evalf()

# 快速：
f = lambdify(x, expr, 'numpy')
results = f(np.arange(1000))
```

### 6. 使用适当的求解器

- `solveset`：代数方程（主要）
- `linsolve`：线性系统
- `nonlinsolve`：非线性系统
- `dsolve`：微分方程
- `solve`：通用（传统，但灵活）

## 参考文件结构

此技能使用模块化参考文件来处理不同的能力：

1. **`core-capabilities.md`**：符号、代数、微积分、简化、方程求解
   - 加载时机：基本符号计算、微积分或求解方程

2. **`matrices-linear-algebra.md`**：矩阵操作、特征值、线性系统
   - 加载时机：处理矩阵或线性代数问题

3. **`physics-mechanics.md`**：经典力学、量子力学、矢量、单位
   - 加载时机：物理计算或力学问题

4. **`advanced-topics.md`**：几何、数论、组合数学、逻辑、统计学
   - 加载时机：超越基本代数和微积分的高级数学主题

5. **`code-generation-printing.md`**：Lambdify、codegen、LaTeX输出、打印
   - 加载时机：将表达式转换为代码或生成格式化输出

## 常见用例模式

### 模式1：求解和验证

```python
from sympy import symbols, solve, simplify
x = symbols('x')

# 解方程
equation = x**2 - 5*x + 6
solutions = solve(equation, x)  # [2, 3]

# 验证解
for sol in solutions:
    result = simplify(equation.subs(x, sol))
    assert result == 0
```

### 模式2：符号到数值管道

```python
# 1. 定义符号问题
x, y = symbols('x y')
expr = sin(x) + cos(y)

# 2. 符号操作
simplified = simplify(expr)
derivative = diff(simplified, x)

# 3. 转换为数值函数
f = lambdify((x, y), derivative, 'numpy')

# 4. 数值评估
results = f(x_data, y_data)
```

### 模式3：记录数学结果

```python
# 符号计算结果
integral_expr = Integral(x**2, (x, 0, 1))
result = integral_expr.doit()

# 生成文档
print(f"LaTeX: {latex(integral_expr)} = {latex(result)}")
print(f"Pretty: {pretty(integral_expr)} = {pretty(result)}")
print(f"Numerical: {result.evalf()}")
```

## 与科学工作流的集成

### 与NumPy集成

```python
import numpy as np
from sympy import symbols, lambdify

x = symbols('x')
expr = x**2 + 2*x + 1

f = lambdify(x, expr, 'numpy')
x_array = np.linspace(-5, 5, 100)
y_array = f(x_array)
```

### 与Matplotlib集成

```python
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, lambdify, sin

x = symbols('x')
expr = sin(x) / x

f = lambdify(x, expr, 'numpy')
x_vals = np.linspace(-10, 10, 1000)
y_vals = f(x_vals)

plt.plot(x_vals, y_vals)
plt.show()
```

### 与SciPy集成

```python
from scipy.optimize import fsolve
from sympy import symbols, lambdify

# 符号定义方程
x = symbols('x')
equation = x**3 - 2*x - 5

# 转换为数值函数
f = lambdify(x, equation, 'numpy')

# 用初始猜测数值求解
solution = fsolve(f, 2)
```

## 快速参考：最常用函数

```python
# 符号
from sympy import symbols, Symbol
x, y = symbols('x y')

# 基本操作
from sympy import simplify, expand, factor, collect, cancel
from sympy import sqrt, exp, log, sin, cos, tan, pi, E, I, oo

# 微积分
from sympy import diff, integrate, limit, series, Derivative, Integral

# 求解
from sympy import solve, solveset, linsolve, nonlinsolve, dsolve

# 矩阵
from sympy import Matrix, eye, zeros, ones, diag

# 逻辑和集合
from sympy import And, Or, Not, Implies, FiniteSet, Interval, Union

# 输出
from sympy import latex, pprint, lambdify, init_printing

# 工具
from sympy import evalf, N, nsimplify
```

## 入门示例

### 示例1：求解二次方程
```python
from sympy import symbols, solve, sqrt
x = symbols('x')
solution = solve(x**2 - 5*x + 6, x)
# [2, 3]
```

### 示例2：计算导数
```python
from sympy import symbols, diff, sin
x = symbols('x')
f = sin(x**2)
df_dx = diff(f, x)
# 2*x*cos(x**2)
```

### 示例3：评估积分
```python
from sympy import symbols, integrate, exp
x = symbols('x')
integral = integrate(x * exp(-x**2), (x, 0, oo))
# 1/2
```

### 示例4：矩阵特征值
```python
from sympy import Matrix
M = Matrix([[1, 2], [2, 1]])
eigenvals = M.eigenvals()
# {3: 1, -1: 1}
```

### 示例5：生成Python函数
```python
from sympy import symbols, lambdify
import numpy as np
x = symbols('x')
expr = x**2 + 2*x + 1
f = lambdify(x, expr, 'numpy')
f(np.array([1, 2, 3]))
# array([ 4,  9, 16])
```

## 常见问题排查

1. **"NameError: name 'x' is not defined"**
   - 解决方案：在使用前始终使用 `symbols()` 定义符号

2. **意外的数值结果**
   - 问题：使用 `0.5` 等浮点数而不是 `Rational(1, 2)`
   - 解决方案：使用 `Rational()` 或 `S()` 进行精确算术

3. **循环中的性能缓慢**
   - 问题：重复使用 `subs()` 和 `evalf()`
   - 解决方案：使用 `lambdify()` 创建快速数值函数

4. **"无法求解此方程"**
   - 尝试不同的求解器：`solve`、`solveset`、`nsolve`（数值）
   - 检查方程是否可代数求解
   - 如果没有闭式解，使用数值方法

5. **简化不如预期工作**
   - 尝试不同的简化函数：`simplify`、`factor`、`expand`、`trigsimp`
   - 向符号添加假设（例如，`positive=True`）
   - 使用 `simplify(expr, force=True)` 进行积极简化

## 其他资源

- 官方文档：https://docs.sympy.org/
- 教程：https://docs.sympy.org/latest/tutorials/intro-tutorial/index.html
- API参考：https://docs.sympy.org/latest/reference/index.html
- 示例：https://github.com/sympy/sympy/tree/master/examples