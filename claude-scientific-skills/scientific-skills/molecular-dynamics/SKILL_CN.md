---
name: molecular-dynamics
description: 分子动力学模拟和分析。使用GROMACS、AMBER、NAMD、LAMMPS、OpenMM等软件包进行分子动力学模拟。包括系统准备、能量最小化、平衡、生产运行、轨迹分析、自由能计算、增强采样、粗粒化建模和可视化。适用于蛋白质、核酸、膜蛋白、药物-配体复合物等生物分子系统。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# 分子动力学

## 概述

分子动力学（MD）模拟是一种计算方法，用于研究原子和分子随时间的运动和相互作用。该技能涵盖了使用GROMACS、AMBER、NAMD、LAMMPS、OpenMM等软件包进行分子动力学模拟的全过程，包括系统准备、能量最小化、平衡、生产运行、轨迹分析、自由能计算、增强采样、粗粒化建模和可视化。

## 核心能力

### 1. 系统准备

- **结构准备**：从PDB或其他格式获取初始结构
- **质子化**：添加氢原子，确定质子化状态
- **力场选择**：选择合适的力场（AMBER、CHARMM、OPLS、GROMOS）
- **溶剂化**：将分子放入水盒子中（TIP3P、TIP4P等）
- **离子添加**：添加离子以中和系统并达到所需离子强度
- **能量最小化**：消除结构中的不良接触

### 2. 能量最小化

- **最速下降法**：快速消除高能接触
- **共轭梯度法**：更精确的能量最小化
- **约束最小化**：在约束下最小化特定部分
- **收敛标准**：设置能量和力的收敛标准

### 3. 平衡

- **NVT平衡**：恒定温度平衡
- **NPT平衡**：恒定温度和压力平衡
- **温度耦合**：使用Berendsen、V-rescale或Nosé-Hoover恒温器
- **压力耦合**：使用Berendsen或Parrinello-Rahman恒压器
- **约束**：约束键长和键角（LINCS、SETTLE）

### 4. 生产运行

- **时间步长**：选择合适的时间步长（1-2 fs）
- **积分器**：使用Leap-Frog或Velocity Verlet积分器
- **周期性边界条件**：应用周期性边界条件
- **长程静电**：使用PME或Ewald方法
- **范德华力**：使用截断或切换函数
- **轨迹保存**：定期保存坐标、速度和能量

### 5. 轨迹分析

- **RMSD分析**：计算均方根偏差
- **RMSF分析**：计算均方根涨落
- **氢键分析**：识别和分析氢键
- **二级结构分析**：分析蛋白质二级结构
- **距离和角度**：计算原子间距离和角度
- **回转半径**：计算分子的回转半径
- **溶剂可及表面积**：计算SASA

### 6. 自由能计算

- **热力学积分**：使用TI计算自由能差
- **自由能微扰**：使用FEP计算相对结合自由能
- **伞形采样**：使用伞形采样计算PMF
- **元动力学**：使用元动力学探索自由能面
- **MM/PBSA和MM/GBSA**：使用MM/PBSA或MM/GBSA估算结合自由能

### 7. 增强采样

- **副本交换MD**：使用REMD增强采样
- **加速MD**：使用aMD提高采样效率
- **高斯加速MD**：使用GaMD增强采样
- **自适应偏置力**：使用ABF计算自由能面

### 8. 粗粒化建模

- **Martini力场**：使用Martini力场进行粗粒化模拟
- **反向映射**：将粗粒化结构映射回全原子细节
- **多尺度模拟**：结合粗粒化和全原子模拟

### 9. 可视化

- **VMD**：使用VMD可视化轨迹
- **PyMOL**：使用PyMOL可视化结构
- **Chimera**：使用Chimera或ChimeraX可视化
- **轨迹动画**：创建轨迹动画

## 何时使用此技能

在以下情况下使用此技能：
- 研究蛋白质、核酸、膜蛋白等生物分子的动力学
- 研究药物-配体结合
- 计算结合自由能
- 研究蛋白质折叠
- 研究膜蛋白功能
- 研究蛋白质-蛋白质相互作用
- 研究酶催化机制
- 研究分子识别

## 常用软件包

### GROMACS
- **特点**：高性能、开源、广泛使用
- **适用**：蛋白质、核酸、膜蛋白、药物-配体复合物
- **优势**：快速、易于使用、良好的文档

### AMBER
- **特点**：强大的力场、丰富的工具
- **适用**：蛋白质、核酸、药物分子
- **优势**：精确的力场、成熟的工具链

### NAMD
- **特点**：高性能并行计算
- **适用**：大型生物分子系统
- **优势**：良好的并行扩展性

### LAMMPS
- **特点**：通用分子动力学
- **适用**：各种分子系统
- **优势**：灵活、可扩展

### OpenMM
- **特点**：Python友好、GPU加速
- **适用**：快速原型开发、GPU计算
- **优势**：易于使用、Python API

## 使用示例

### GROMACS示例

```bash
# 1. 准备拓扑文件
gmx pdb2gmx -f protein.pdb -o processed.gro -water tip3p -ff amber99sb-ildn

# 2. 定义盒子并添加溶剂
gmx editconf -f processed.gro -o boxed.gro -c -d 1.0 -bt dodecahedron
gmx solvate -cp boxed.gro -cs spc216.gro -o solvated.gro -p topol.top

# 3. 添加离子
gmx grompp -f ions.mdp -c solvated.gro -p topol.top -o ions.tpr
gmx genion -s ions.tpr -p topol.top -pname NA -nname CL -neutral -conc 0.15

# 4. 能量最小化
gmx grompp -f minim.mdp -c ionized.gro -p topol.top -o em.tpr
gmx mdrun -deffnm em

# 5. NVT平衡
gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
gmx mdrun -deffnm nvt

# 6. NPT平衡
gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr
gmx mdrun -deffnm npt

# 7. 生产运行
gmx grompp -f md.mdp -c npt.gro -r npt.gro -t npt.cpt -p topol.top -o md.tpr
gmx mdrun -deffnm md

# 8. 分析
gmx rms -s md.tpr -f md.xtc -o rmsd.xvg -ref
gmx rmsf -s md.tpr -f md.xtc -o rmsf.xvg -res
```

### OpenMM示例

```python
from simtk.openmm import app
import simtk.openmm as mm
from simtk import unit

# 1. 加载PDB文件
pdb = app.PDBFile('protein.pdb')

# 2. 创建力场
forcefield = app.ForceField('amber99sb.xml', 'tip3p.xml')

# 3. 创建系统
system = forcefield.createSystem(pdb.topology, nonbondedMethod=app.PME,
                                 nonbondedCutoff=1.0*unit.nanometers,
                                 constraints=app.HBonds)

# 4. 创建积分器
integrator = mm.LangevinIntegrator(300*unit.kelvin, 1.0/unit.picoseconds,
                                   2.0*unit.femtoseconds)

# 5. 创建模拟
simulation = app.Simulation(pdb.topology, system, integrator)
simulation.context.setPositions(pdb.positions)

# 6. 最小化能量
simulation.minimizeEnergy()

# 7. 平衡
simulation.context.setVelocitiesToTemperature(300*unit.kelvin)
simulation.step(10000)

# 8. 生产运行
simulation.reporters.append(app.DCDReporter('trajectory.dcd', 1000))
simulation.reporters.append(app.StateDataReporter('data.csv', 1000,
    step=True, potentialEnergy=True, temperature=True))
simulation.step(100000)
```

## 最佳实践

1. **系统准备**：仔细检查初始结构，确保没有错误
2. **力场选择**：选择适合系统的力场
3. **溶剂化**：确保溶剂盒子足够大，避免周期性相互作用
4. **离子强度**：使用生理相关的离子浓度
5. **平衡**：充分平衡系统，确保温度和压力稳定
6. **时间步长**：使用合适的时间步长，避免能量漂移
7. **长程静电**：使用PME或Ewald方法处理长程静电
8. **约束**：约束键长和键角，允许更大的时间步长
9. **轨迹保存**：定期保存轨迹，避免丢失数据
10. **分析**：使用多种分析方法验证结果

## 常见问题

**Q: 如何选择合适的力场？**
A: 根据系统类型选择。蛋白质常用AMBER、CHARMM；核酸常用AMBER、CHARMM。

**Q: 平衡需要多长时间？**
A: 通常需要1-10 ns，具体取决于系统大小和复杂性。

**Q: 如何判断模拟是否收敛？**
A: 检查能量、温度、压力、RMSD等是否稳定。

**Q: 如何计算结合自由能？**
A: 使用MM/PBSA、MM/GBSA、FEP或TI等方法。

## 资源

- **GROMACS文档**：http://www.gromacs.org/documentation
- **AMBER文档**：https://ambermd.org/doc12/
- **NAMD文档**：https://www.ks.uiuc.edu/Research/namd/
- **LAMMPS文档**：https://lammps.sandia.gov/doc/
- **OpenMM文档**：http://docs.openmm.org/
