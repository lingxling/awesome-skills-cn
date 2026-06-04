---
name: fluidsim
description: 使用Python进行计算流体动力学模拟的框架。用于运行流体动力学模拟，包括纳维-斯托克斯方程（2D/3D）、浅水方程、分层流动，或分析湍流、涡旋动力学或地球物理流动。提供伪谱方法（FFT）、HPC支持和全面的输出分析。
license: CeCILL FREE SOFTWARE LICENSE AGREEMENT
metadata:
  version: "1.0"
  skill-author: K-Dense Inc.
---






# FluidSim

## 概述

FluidSim 是一个面向对象的 Python 框架，用于高性能计算流体动力学（CFD）模拟。它为周期性域方程提供基于 FFT 的伪谱方法求解器，在保持 Python 易用性的同时，性能可与 Fortran/C++ 相媲美。

**核心优势**：
- 多种求解器：2D/3D Navier-Stokes、浅水方程、分层流
- 高性能：Pythran/Transonic 编译、MPI 并行化
- 完整工作流：参数配置、模拟执行、输出分析
- 交互式分析：基于 Python 的后处理和可视化

## 核心能力

### 1. 安装与配置

使用 uv 安装 fluidsim，并添加适当的功能标志：

```bash
# 基础安装
uv pip install fluidsim

# 包含 FFT 支持（大多数求解器必需）
uv pip install "fluidsim[fft]"

# 包含 MPI 以支持并行计算
uv pip install "fluidsim[fft,mpi]"
```

设置输出目录的环境变量（可选）：

```bash
export FLUIDSIM_PATH=/path/to/simulation/outputs
export FLUIDDYN_PATH_SCRATCH=/path/to/working/directory
```

无需 API 密钥或身份验证。

详见 `references/installation.md` 获取完整的安装说明和环境配置。

### 2. 运行模拟

标准工作流包含五个步骤：

**步骤 1**：导入求解器
```python
from fluidsim.solvers.ns2d.solver import Simul
```

**步骤 2**：创建并配置参数
```python
params = Simul.create_default_params()
params.oper.nx = params.oper.ny = 256
params.oper.Lx = params.oper.Ly = 2 * 3.14159
params.nu_2 = 1e-3
params.time_stepping.t_end = 10.0
params.init_fields.type = "noise"
```

**步骤 3**：实例化模拟
```python
sim = Simul(params)
```

**步骤 4**：执行
```python
sim.time_stepping.start()
```

**步骤 5**：分析结果
```python
sim.output.phys_fields.plot("vorticity")
sim.output.spatial_means.plot()
```

详见 `references/simulation_workflow.md` 获取完整示例、重启模拟和集群部署说明。

### 3. 可用求解器

根据物理问题选择求解器：

**2D Navier-Stokes** (`ns2d`)：2D 湍流、涡动力学
```python
from fluidsim.solvers.ns2d.solver import Simul
```

**3D Navier-Stokes** (`ns3d`)：3D 湍流、真实流动
```python
from fluidsim.solvers.ns3d.solver import Simul
```

**分层流** (`ns2d.strat`, `ns3d.strat`)：海洋/大气流动
```python
from fluidsim.solvers.ns2d.strat.solver import Simul
params.N = 1.0  # Brunt-Väisälä 频率
```

**浅水方程** (`sw1l`)：地球物理流、旋转系统
```python
from fluidsim.solvers.sw1l.solver import Simul
params.f = 1.0  # 科里奥利参数
```

详见 `references/solvers.md` 获取完整求解器列表和选择指南。

### 4. 参数配置

参数按层次组织，通过点号表示法访问：

**域和分辨率**：
```python
params.oper.nx = 256  # 网格点数
params.oper.Lx = 2 * pi  # 域大小
```

**物理参数**：
```python
params.nu_2 = 1e-3  # 粘性系数
params.nu_4 = 0     # 超粘性（可选）
```

**时间步进**：
```python
params.time_stepping.t_end = 10.0
params.time_stepping.USE_CFL = True  # 自适应时间步长
params.time_stepping.CFL = 0.5
```

**初始条件**：
```python
params.init_fields.type = "noise"  # 或 "dipole", "vortex", "from_file", "in_script"
```

**输出设置**：
```python
params.output.periods_save.phys_fields = 1.0  # 每 1.0 时间单位保存一次
params.output.periods_save.spectra = 0.5
params.output.periods_save.spatial_means = 0.1
```

Parameters 对象会对拼写错误抛出 `AttributeError`，防止配置错误被静默忽略。

详见 `references/parameters.md` 获取全面的参数文档。

### 5. 输出与分析

FluidSim 在模拟过程中自动产生多种输出类型：

**物理场**：HDF5 格式的速度、涡量
```python
sim.output.phys_fields.plot("vorticity")
sim.output.phys_fields.plot("vx")
```

**空间平均值**：体积平均量的时间序列
```python
sim.output.spatial_means.plot()
```

**能谱**：能量和涡度能谱
```python
sim.output.spectra.plot1d()
sim.output.spectra.plot2d()
```

**加载先前模拟**：
```python
from fluidsim import load_sim_for_plot
sim = load_sim_for_plot("simulation_dir")
sim.output.phys_fields.plot()
```

**高级可视化**：在 ParaView 或 VisIt 中打开 `.h5` 文件进行 3D 可视化。

详见 `references/output_analysis.md` 获取详细分析工作流、参数化研究分析和数据导出。

### 6. 高级特性

**自定义强迫**：维持湍流或驱动特定动力学
```python
params.forcing.enable = True
params.forcing.type = "tcrandom"  # 时间相关随机强迫
params.forcing.forcing_rate = 1.0
```

**自定义初始条件**：在脚本中定义场
```python
params.init_fields.type = "in_script"
sim = Simul(params)
X, Y = sim.oper.get_XY_loc()
vx = sim.state.state_phys.get_var("vx")
vx[:] = sin(X) * cos(Y)
sim.time_stepping.start()
```

**MPI 并行化**：在多处理器上运行
```bash
mpirun -np 8 python simulation_script.py
```

**参数化研究**：使用不同参数运行多个模拟
```python
for nu in [1e-3, 5e-4, 1e-4]:
    params = Simul.create_default_params()
    params.nu_2 = nu
    params.output.sub_directory = f"nu{nu}"
    sim = Simul(params)
    sim.time_stepping.start()
```

详见 `references/advanced_features.md` 获取强迫类型、自定义求解器、集群提交和性能优化。

## 常见用例

### 2D 湍流研究

```python
from fluidsim.solvers.ns2d.solver import Simul
from math import pi

params = Simul.create_default_params()
params.oper.nx = params.oper.ny = 512
params.oper.Lx = params.oper.Ly = 2 * pi
params.nu_2 = 1e-4
params.time_stepping.t_end = 50.0
params.time_stepping.USE_CFL = True
params.init_fields.type = "noise"
params.output.periods_save.phys_fields = 5.0
params.output.periods_save.spectra = 1.0

sim = Simul(params)
sim.time_stepping.start()

# 分析能量级串
sim.output.spectra.plot1d(tmin=30.0, tmax=50.0)
```

### 分层流模拟

```python
from fluidsim.solvers.ns2d.strat.solver import Simul

params = Simul.create_default_params()
params.oper.nx = params.oper.ny = 256
params.N = 2.0  # 分层强度
params.nu_2 = 5e-4
params.time_stepping.t_end = 20.0

# 用密集层初始化
params.init_fields.type = "in_script"
sim = Simul(params)
X, Y = sim.oper.get_XY_loc()
b = sim.state.state_phys.get_var("b")
b[:] = exp(-((X - 3.14)**2 + (Y - 3.14)**2) / 0.5)
sim.state.statephys_from_statespect()

sim.time_stepping.start()
sim.output.phys_fields.plot("b")
```

### 高分辨率 3D 模拟（使用 MPI）

```python
from fluidsim.solvers.ns3d.solver import Simul

params = Simul.create_default_params()
params.oper.nx = params.oper.ny = params.oper.nz = 512
params.nu_2 = 1e-5
params.time_stepping.t_end = 10.0
params.init_fields.type = "noise"

sim = Simul(params)
sim.time_stepping.start()
```

运行方式：
```bash
mpirun -np 64 python script.py
```

### Taylor-Green 涡验证

```python
from fluidsim.solvers.ns2d.solver import Simul
import numpy as np
from math import pi

params = Simul.create_default_params()
params.oper.nx = params.oper.ny = 128
params.oper.Lx = params.oper.Ly = 2 * pi
params.nu_2 = 1e-3
params.time_stepping.t_end = 10.0
params.init_fields.type = "in_script"

sim = Simul(params)
X, Y = sim.oper.get_XY_loc()
vx = sim.state.state_phys.get_var("vx")
vy = sim.state.state_phys.get_var("vy")
vx[:] = np.sin(X) * np.cos(Y)
vy[:] = -np.cos(X) * np.sin(Y)
sim.state.statephys_from_statespect()

sim.time_stepping.start()

# 验证能量衰减
df = sim.output.spatial_means.load()
# 与解析解比较
```

## 快速参考

**导入求解器**：`from fluidsim.solvers.ns2d.solver import Simul`

**创建参数**：`params = Simul.create_default_params()`

**设置分辨率**：`params.oper.nx = params.oper.ny = 256`

**设置粘性**：`params.nu_2 = 1e-3`

**设置结束时间**：`params.time_stepping.t_end = 10.0`

**运行模拟**：`sim = Simul(params); sim.time_stepping.start()`

**绘制结果**：`sim.output.phys_fields.plot("vorticity")`

**加载模拟**：`sim = load_sim_for_plot("path/to/sim")`

## 资源

**文档**：https://fluidsim.readthedocs.io/

**参考文件**：
- `references/installation.md`：完整安装说明
- `references/solvers.md`：可用求解器和选择指南
- `references/simulation_workflow.md`：详细工作流示例
- `references/parameters.md`：全面参数文档
- `references/output_analysis.md`：输出类型和分析方法
- `references/advanced_features.md`：强迫、MPI、参数化研究、自定义求解器
