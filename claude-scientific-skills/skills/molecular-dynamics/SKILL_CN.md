---
name: molecular-dynamics
description: 使用 OpenMM 和 MDAnalysis 运行并分析分子动力学模拟。搭建蛋白质/小分子体系，定义力场，运行能量最小化和生产阶段 MD，并分析轨迹（RMSD、RMSF、接触图、自由能面）。适用于结构生物学、药物结合和生物物理学。
license: MIT
compatibility: Requires Python 3.11+ with OpenMM and MDAnalysis; matplotlib for plots. Optional PDBFixer and OpenFF need separate installation. Network access for installation; local simulation and analysis run offline.
metadata:
  version: "1.3"
  last-reviewed: "2026-10-01"
  skill-author: Kuan-lin Huang
---

# 分子动力学

## 概述

分子动力学（MD）模拟通过对牛顿运动方程进行积分，以计算方式模拟分子体系随时间的演化。本技能涵盖两个互补的工具：

- **OpenMM**（https://openmm.org/）：高性能 MD 模拟引擎，支持 GPU、提供 Python API，并灵活支持各种力场
- **MDAnalysis**（https://mdanalysis.org/）：用于读取、写入和分析来自所有主流模拟软件包的 MD 轨迹的 Python 库

**已审查的版本：** OpenMM 8.6.1 和 MDAnalysis 2.10.0。Reference 平台
冒烟检查使用的是小型合成体系；这些检查并不能证明 GPU 性能和科学意义上的收敛性。
OpenMM 最新的 API 页面对应的是开发版构建，
因此已安装的 8.6.1 API 才是可执行的参考。

**安装到专用环境中：**
```bash
uv venv --python 3.12 .venv-md
uv pip install --python .venv-md/bin/python "openmm==8.6.1" "MDAnalysis==2.10.0" matplotlib pandas
# Windows：改用 .venv-md/Scripts/python.exe
```

## 何时使用本技能

在以下情况下使用分子动力学：

- **蛋白质稳定性分析**：突变如何影响蛋白质动力学？
- **药物结合模拟**：表征配体的结合模式和停留时间
- **构象采样**：探索蛋白质的柔性和构象变化
- **蛋白质-蛋白质相互作用**：模拟界面动力学和结合能学
- **RMSD/RMSF 分析**：量化相对于参考结构的结构波动
- **自由能估算**：计算结合自由能或构象自由能
- **膜模拟**：模拟脂质双层中的蛋白质
- **内在无序蛋白**：研究 IDR 构象系综

## 核心工作流程：OpenMM 模拟

示例需要针对具体体系进行准备和验证。在参数化之前，请审查生物学
组装体、交替位置（alternate locations）、缺失的环区、末端、质子化状态、二硫键、
配体和辅因子。仅凭一条 MD 轨迹并不能
确定结合自由能或停留时间。

下面的函数构成一个 Python 模块：请将它们的导入块一起执行。
每个阶段使用新的输出前缀，以避免覆盖之前的结果。

### 1. 体系准备

```python
from openmm.app import *
from openmm import *
from openmm.unit import *

def prepare_system_from_pdb(pdb_file, forcefield_name="amber14-all.xml",
                              water_model="amber14/tip3pfb.xml", ph=7.0):
    """
    从 PDB 文件准备 OpenMM 体系。

    Args:
        pdb_file: 清理后的 PDB 文件路径（原始 PDB 文件请使用 PDBFixer 处理）
        forcefield_name: 力场 XML 文件
        water_model: 水模型 XML 文件

    Returns:
        modeller, system
    """
    # 加载 PDB
    pdb = PDBFile(pdb_file)

    # 加载力场
    forcefield = ForceField(forcefield_name, water_model)

    # 添加氢原子并溶剂化
    modeller = Modeller(pdb.topology, pdb.positions)
    modeller.addHydrogens(forcefield, pH=ph)

    # TIP3P 几何结构同样适用于 TIP3P-FB；参数由 XML 提供。
    # 10 Å 缓冲距离；添加的盐不包括用于中和电荷的反离子。
    modeller.addSolvent(
        forcefield,
        model='tip3p',
        padding=10*angstroms,
        ionicStrength=0.15*molar, neutralize=True
    )

    print(f"System: {modeller.topology.getNumAtoms()} atoms, "
          f"{modeller.topology.getNumResidues()} residues")

    # 创建体系
    system = forcefield.createSystem(
        modeller.topology,
        nonbondedMethod=PME,         # 使用粒子网格 Ewald 处理长程静电
        nonbondedCutoff=1.0*nanometer,
        constraints=HBonds,           # 约束涉及 H 的化学键（不是分子间氢键）
        rigidWater=True,
        ewaldErrorTolerance=0.0005
    )

    return modeller, system
```

### 2. 能量最小化

```python
from openmm.app import *
from openmm import *
from openmm.unit import *

def minimize_energy(modeller, system, output_pdb="minimized.pdb",
                     max_iterations=1000, tolerance=10.0, platform_name=None):
    """
    对体系进行能量最小化以消除空间位阻冲突。

    Args:
        modeller: 包含拓扑和坐标的 Modeller 对象
        system: OpenMM System
        output_pdb: 保存最小化结构的路径
        max_iterations: 最大最小化步数
        tolerance: 收敛判据，单位 kJ/mol/nm

    Returns:
        包含最小化后坐标的 simulation 对象
    """
    # 为后续的 NVT/NPT 示例保持积分器步长为 2 fs。
    integrator = LangevinMiddleIntegrator(300*kelvin, 1/picosecond, 0.002*picoseconds)

    # 自动选择平台，或指定一个经过测试的平台（例如 CPU）。
    # 已注册的 GPU 插件并不能证明设备或驱动可用。
    platform = Platform.getPlatformByName(platform_name) if platform_name else None
    simulation = Simulation(modeller.topology, system, integrator, platform)
    simulation.context.setPositions(modeller.positions)

    # 检查初始能量
    state = simulation.context.getState(getEnergy=True)
    print(f"Initial energy: {state.getPotentialEnergy()}")

    # 最小化
    simulation.minimizeEnergy(
        tolerance=tolerance*kilojoules_per_mole/nanometer,
        maxIterations=max_iterations
    )

    state = simulation.context.getState(getEnergy=True, getPositions=True)
    print(f"Minimized energy: {state.getPotentialEnergy()}")

    # 保存最小化后的结构
    with open(output_pdb, 'w') as f:
        PDBFile.writeFile(simulation.topology, state.getPositions(), f)

    return simulation
```

### 3. NVT 平衡

```python
from openmm.app import *
from openmm import *
from openmm.unit import *

def run_nvt_equilibration(simulation, n_steps=50000, temperature=300,
                            report_interval=1000, output_prefix="nvt"):
    """
    NVT 平衡：N、V、T 恒定。
    将速度平衡到目标温度。

    Args:
        simulation: OpenMM Simulation（最小化之后）
        n_steps: MD 步数（50000 × 2fs = 100 ps）
        temperature: 温度，单位开尔文
        report_interval: 两次数据报告之间的步数
        output_prefix: 轨迹和日志的文件前缀
    """
    # 本示例不含限制势；请在创建 Context 之前添加经过验证的限制势。
    if any("Barostat" in type(f).__name__ and f.getFrequency() > 0
           for f in simulation.system.getForces()):
        raise ValueError("NVT requires all barostats disabled or absent")

    # 同时设置恒温器目标温度和初始速度。
    simulation.integrator.setTemperature(temperature*kelvin)
    simulation.context.setVelocitiesToTemperature(temperature*kelvin)

    # 添加报告器
    simulation.reporters = []

    # 日志文件
    simulation.reporters.append(
        StateDataReporter(
            f"{output_prefix}_log.txt",
            report_interval,
            step=True,
            potentialEnergy=True,
            kineticEnergy=True,
            temperature=True,
            volume=True,
            speed=True
        )
    )

    # DCD 轨迹（紧凑的二进制格式）
    simulation.reporters.append(
        DCDReporter(f"{output_prefix}_traj.dcd", report_interval)
    )

    duration = (n_steps * simulation.integrator.getStepSize()).value_in_unit(picoseconds)
    print(f"Running NVT equilibration: {n_steps} steps ({duration:.1f} ps)")
    simulation.step(n_steps)
    print("NVT equilibration complete")

    return simulation
```

### 4. NPT 平衡与生产阶段

首先使用专用的 NPT 平衡前缀调用此函数。在单独进行生产阶段调用之前，检查密度、
能量、结构以及重复模拟的稳定性；
默认时长只是一个示例，而不是平衡或收敛的判据。

```python
def run_npt_production(simulation, n_steps=500000, temperature=300, pressure=1.0,
                        report_interval=5000, output_prefix="npt"):
    """
    NPT 生产阶段运行：N、P、T 恒定。

    Args:
        n_steps: 生产阶段步数（500000 × 2fs = 1 ns）
        temperature: 温度，单位开尔文
        pressure: 压力，单位 bar
        report_interval: 两次报告之间的步数
    """
    # 保持 Langevin 恒温器与恒压器处于相同温度。
    simulation.integrator.setTemperature(temperature*kelvin)
    system = simulation.system
    barostats = [f for f in system.getForces() if "Barostat" in type(f).__name__]
    if not system.usesPeriodicBoundaryConditions():
        raise ValueError("NPT requires a periodic system")
    if not barostats:
        system.addForce(MonteCarloBarostat(pressure*bar, temperature*kelvin, 25))
        simulation.context.reinitialize(preserveState=True)
    elif len(barostats) != 1 or not isinstance(barostats[0], MonteCarloBarostat):
        raise ValueError("This example supports one isotropic MonteCarloBarostat")
    else:
        barostats[0].setDefaultPressure(pressure*bar)
        barostats[0].setDefaultTemperature(temperature*kelvin)
        barostats[0].setFrequency(25)
    # 重复调用时也必须更新已有的 Context 参数。
    simulation.context.setParameter(MonteCarloBarostat.Pressure(), pressure)
    simulation.context.setParameter(MonteCarloBarostat.Temperature(), temperature)

    # 更新报告器
    simulation.reporters = []
    simulation.reporters.append(
        StateDataReporter(
            f"{output_prefix}_log.txt",
            report_interval,
            step=True,
            potentialEnergy=True,
            temperature=True,
            density=True,
            speed=True
        )
    )
    simulation.reporters.append(
        DCDReporter(f"{output_prefix}_traj.dcd", report_interval)
    )

    # 保存检查点
    simulation.reporters.append(
        CheckpointReporter(f"{output_prefix}_checkpoint.chk", 50000)
    )

    duration = (n_steps * simulation.integrator.getStepSize()).value_in_unit(nanoseconds)
    print(f"Running NPT stage: {n_steps} steps ({duration:.3f} ns)")
    simulation.step(n_steps)
    simulation.saveCheckpoint(f"{output_prefix}_checkpoint.chk")
    simulation.saveState(f"{output_prefix}_state.xml")
    print("NPT stage complete")
    return simulation
```

## 使用 MDAnalysis 进行轨迹分析

### 1. 加载轨迹

使用原子数和原子顺序与 DCD 完全一致的溶剂化拓扑（例如上面的
`minimized.pdb`），而不是原始的未溶剂化输入。MDAnalysis 默认将
长度转换为 Å、时间转换为 ps；OpenMM 的裸坐标使用 nm。保留
每帧的盒子向量和实际时间戳；不要根据帧编号推断时间。

```python
import MDAnalysis as mda
from MDAnalysis.analysis import rms, align, contacts
import numpy as np
import matplotlib.pyplot as plt

def load_trajectory(topology_file, trajectory_file):
    """
    使用 MDAnalysis 加载 MD 轨迹。

    Args:
        topology_file: PDB、PSF 或其他拓扑文件
        trajectory_file: DCD、XTC、TRR 或其他轨迹
    """
    u = mda.Universe(topology_file, trajectory_file)
    print(f"Universe: {u.atoms.n_atoms} atoms, {u.trajectory.n_frames} frames")
    first, last = u.trajectory[0].time, u.trajectory[-1].time
    print(f"Time range: {first:g} to {last:g} ps")
    u.trajectory[0]
    return u
```

### 2. RMSD 分析

```python
def compute_rmsd(u, selection="backbone", reference_frame=0):
    """
    计算所选原子相对于参考帧的 RMSD。

    Args:
        u: MDAnalysis Universe
        selection: 原子选择字符串（MDAnalysis 语法）
        reference_frame: 参考结构的帧索引

    Returns:
        numpy 数组，列为 [帧索引, 时间（ps）, RMSD（埃）]
    """
    # RMSD 会自行进行叠合；此处避免旋转存储的轨迹。
    # 分析周期性轨迹之前，先使所选分子保持完整。
    R = rms.RMSD(u, select=selection, ref_frame=reference_frame)
    R.run()

    rmsd_data = R.results.rmsd  # 列：帧、时间、RMSD
    return rmsd_data

def plot_rmsd(rmsd_data, title="RMSD over time", output_file="rmsd.png"):
    """绘制 RMSD 随模拟时间的变化。"""
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(rmsd_data[:, 1] / 1000, rmsd_data[:, 2], 'b-', linewidth=0.5)
    ax.set_xlabel("Time (ns)")
    ax.set_ylabel("RMSD (Å)")
    ax.set_title(title)
    ax.axhline(rmsd_data[:, 2].mean(), color='r', linestyle='--',
               label=f'Mean: {rmsd_data[:, 2].mean():.2f} Å')
    ax.legend()
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    return fig
```

### 3. RMSF 分析（逐残基柔性）

在计算 RMSF 之前，先使分子保持完整，并对一份单独的结构分析副本进行叠合；
RMSF 本身不做叠合。不要在盒子未随之旋转的已旋转轨迹上
运行周期性接触分析。有关叠合、PCA、DSSP、氢键以及基于布居的自由能，
参见[分析参考](references/mdanalysis_analysis.md)。

```python
def compute_rmsf(u, selection="protein and name CA", start_frame=0):
    """
    计算逐残基 RMSF（柔性）。

    Returns:
        residue_keys, rmsf_values；键为 (resindex, segid, resid, resname)
    """
    # 选择原子
    atoms = u.select_atoms(selection)

    if not len(atoms):
        raise ValueError("RMSF selection is empty")
    # 多原子选择返回的是原子 RMSF 的平均值，而不是质心 RMSF。
    R = rms.RMSF(atoms)
    R.run(start=start_frame)

    # 按残基平均
    resids = []
    rmsf_per_res = []
    for res in u.select_atoms(selection).residues:
        res_atoms = res.atoms.intersection(atoms)
        if len(res_atoms) > 0:
            resids.append((res.ix, res.segid, res.resid, res.resname))
            # RMSF 是在所选 AtomGroup 内部索引的，而不是在 Universe 中。
            rmsf_per_res.append(R.results.rmsf[atoms.resindices == res.ix].mean())

    return resids, np.array(rmsf_per_res)
```

### 4. 蛋白质-配体接触

```python
def analyze_contacts(u, protein_sel="protein", ligand_sel="resname LIG",
                      radius=4.5, start_frame=0, periodic=True):
    """
    在整条轨迹上追踪蛋白质-配体接触。

    Args:
        radius: 原子对截断距离，单位埃；任意一个原子对即可定义一个残基接触。
        periodic: 要求有盒子数据，并使用最小镜像距离。
    返回 (resindex, segid, resid, resname) 的集合，每个被分析的帧对应一个集合。
    """
    from MDAnalysis.lib.distances import distance_array

    protein = u.select_atoms(protein_sel)
    ligand = u.select_atoms(ligand_sel)

    if not len(protein) or not len(ligand):
        raise ValueError("Protein and ligand selections must both be nonempty")
    if not np.isfinite(radius) or radius <= 0:
        raise ValueError("radius must be finite and positive")
    contact_frames = []
    for ts in u.trajectory[start_frame:]:
        if periodic and (ts.dimensions is None or not np.all(np.isfinite(ts.dimensions))
                         or np.any(ts.dimensions[:3] <= 0)):
            raise ValueError("Periodic contacts require valid frame box dimensions")
        # 除非调用者只选择重原子，否则这里会包含氢原子。
        distances = contacts.contact_matrix(
            distance_array(protein.positions, ligand.positions, box=ts.dimensions if periodic else None),
            radius,
        )
        contact_residues = set()
        for i in range(distances.shape[0]):
            if distances[i].any():
                res = protein[i].residue
                contact_residues.add((res.ix, res.segid, res.resid, res.resname))
        contact_frames.append(contact_residues)

    return contact_frames
```

## 力场与体系准备

为所研究的科学体系选择一个经过验证的蛋白质/配体/水/离子组合。
工作示例保留了 AMBER14/TIP3P-FB；这并不是一个普遍适用的推荐。
当前的 OpenMM 还捆绑了 `amber19-all.xml`（ff19SB、DNA OL21、RNA OL3、lipid21），
以及带有自身 `charmm36_2024/water.xml` 的 `charmm36_2024.xml`。通用 TIP3P 与
CHARMM 修改版 TIP3P 不可互换。IDP 系综对蛋白质-水平衡
尤其敏感。与上面的三位点示例不同，四位点水模型需要额外粒子以及
相匹配的 Modeller 几何结构。

AMBER 蛋白质 XML 无法对任意配体进行参数化。请使用经过审查的 GAFF2
或 OpenFF 流程，并明确指定立体化学、质子化状态、键级、原子
映射和电荷方法。仅包含配体的 Interchange 并不是蛋白质-配体体系。
有关保守的 PDBFixer 和 OpenFF 示例、安装要求以及当前版本详情，
参见[体系准备参考](references/system_preparation.md)。

## 验证与来源记录

- 从最小化开始；有限的能量并不能证明结构有效。
- 采用分阶段的 NVT → NPT 平衡 → 生产阶段。本示例没有限制势。
- 对含 H 的化学键施加约束并使用 2 fs 步长是一个起始选择。更大的
  步长/HMR 需要针对该体系对积分器、稳定性和可观测量进行验证。
- 计算周期性距离时使用每帧的盒子。计算结构可观测量时，使用可信的键拓扑
  使分子保持完整；解包裹（unwrapping）无法推断缺失的化学键。
- 评估预热期（burn-in）、自相关、有效样本数、重复模拟和不确定性。
  短时间内稳定的温度/密度曲线并不能证明构象采样充分。
- 保存拓扑/原子顺序、System/Integrator XML、力场文件/版本、
  随机种子、平台/精度、参数以及分析所用的选择。检查点与
  平台/硬件/版本相关；XML 状态的可移植性更好，但不会
  保留全部内部随机数生成器状态。请测试实际设置下的重启。

## 其他资源

- **OpenMM 文档**：https://openmm.org/documentation.html
- **MDAnalysis 用户指南**：https://docs.mdanalysis.org/
- **GROMACS**（替代 MD 引擎）：https://manual.gromacs.org/
- **NAMD**（替代选择）：https://www.ks.uiuc.edu/Research/namd/
- **CHARMM-GUI**（基于网页的体系构建器）：https://charmm-gui.org/
- **AmberTools**（免费的 Amber 工具）：https://ambermd.org/AmberTools.php
- **OpenMM 论文**：Eastman P et al. (2017) PLOS Computational Biology. PMID: 28278240
- **MDAnalysis 论文**：Michaud-Agrawal N et al. (2011) J Computational Chemistry. PMID: 21500218
