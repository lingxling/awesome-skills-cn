---
name: pymatgen
description: 材料科学工具包。晶体结构（CIF、POSCAR）、相图、能带结构、态密度、Materials Project集成、格式转换，用于计算材料科学。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# Pymatgen - Python Materials Genomics

## 概述

Pymatgen是一个全面的Python材料分析库，为Materials Project提供支持。创建、分析和操作晶体结构和分子，计算相图和热力学性质，分析电子结构（能带结构、态密度），生成表面和界面，并访问Materials Project的计算材料数据库。支持来自各种计算代码的100+文件格式。

## 使用场景

当您需要以下操作时使用此技能：
- 处理材料科学中的晶体结构或分子系统
- 在结构文件格式之间转换（CIF、POSCAR、XYZ等）
- 分析对称性、空间群或配位环境
- 计算相图或评估热力学稳定性
- 分析电子结构数据（带隙、态密度、能带结构）
- 生成表面、平板或研究界面
- 以编程方式访问Materials Project数据库
- 设置高通量计算工作流程
- 分析扩散、磁性或机械性能
- 使用VASP、Gaussian、Quantum ESPRESSO或其他计算代码

## 快速入门指南

### 安装

```bash
# 核心pymatgen
uv pip install pymatgen

# 带Materials Project API访问
uv pip install pymatgen mp-api

# 扩展功能的可选依赖
uv pip install pymatgen[analysis]  # 额外分析工具
uv pip install pymatgen[vis]       # 可视化工具
```

### 基本结构操作

```python
from pymatgen.core import Structure, Lattice

# 从文件读取结构（自动格式检测）
struct = Structure.from_file("POSCAR")

# 从头创建结构
lattice = Lattice.cubic(3.84)
struct = Structure(lattice, ["Si", "Si"], [[0,0,0], [0.25,0.25,0.25]])

# 写入不同格式
struct.to(filename="structure.cif")

# 基本属性
print(f"Formula: {struct.composition.reduced_formula}")
print(f"Space group: {struct.get_space_group_info()}")
print(f"Density: {struct.density:.2f} g/cm³")
```

### Materials Project集成

```bash
# 设置API密钥
export MP_API_KEY="your_api_key_here"
```

```python
from mp_api.client import MPRester

with MPRester() as mpr:
    # 通过材料ID获取结构
    struct = mpr.get_structure_by_material_id("mp-149")

    # 搜索材料
    materials = mpr.materials.summary.search(
        formula="Fe2O3",
        energy_above_hull=(0, 0.05)
    )
```

## 核心功能

### 1. 结构创建和操作

使用各种方法创建结构并执行转换。

**从文件：**
```python
# 自动格式检测
struct = Structure.from_file("structure.cif")
struct = Structure.from_file("POSCAR")
mol = Molecule.from_file("molecule.xyz")
```

**从头创建：**
```python
from pymatgen.core import Structure, Lattice

# 使用晶格参数
lattice = Lattice.from_parameters(a=3.84, b=3.84, c=3.84,
                                  alpha=120, beta=90, gamma=60)
coords = [[0, 0, 0], [0.75, 0.5, 0.75]]
struct = Structure(lattice, ["Si", "Si"], coords)

# 从空间群
struct = Structure.from_spacegroup(
    "Fm-3m",
    Lattice.cubic(3.5),
    ["Si"],
    [[0, 0, 0]]
)
```

**转换：**
```python
from pymatgen.transformations.standard_transformations import (
    SupercellTransformation,
    SubstitutionTransformation,
    PrimitiveCellTransformation
)

# 创建超胞
trans = SupercellTransformation([[2,0,0],[0,2,0],[0,0,2]])
supercell = trans.apply_transformation(struct)

# 替换元素
trans = SubstitutionTransformation({"Fe": "Mn"})
new_struct = trans.apply_transformation(struct)

# 获取原胞
trans = PrimitiveCellTransformation()
primitive = trans.apply_transformation(struct)
```

**参考：** 有关Structure、Lattice、Molecule和相关类的综合文档，请参见`references/core_classes.md`。

### 2. 文件格式转换

在100+文件格式之间转换，具有自动格式检测。

**使用便捷方法：**
```python
# 读取任何格式
struct = Structure.from_file("input_file")

# 写入任何格式
struct.to(filename="output.cif")
struct.to(filename="POSCAR")
struct.to(filename="output.xyz")
```

**使用转换脚本：**
```bash
# 单个文件转换
python scripts/structure_converter.py POSCAR structure.cif

# 批量转换
python scripts/structure_converter.py *.cif --output-dir ./poscar_files --format poscar
```

**参考：** 有关所有支持的格式和代码集成的详细文档，请参见`references/io_formats.md`。

### 3. 结构分析和对称性

分析结构的对称性、配位和其他性质。

**对称性分析：**
```python
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

sga = SpacegroupAnalyzer(struct)

# 获取空间群信息
print(f"Space group: {sga.get_space_group_symbol()}")
print(f"Number: {sga.get_space_group_number()}")
print(f"Crystal system: {sga.get_crystal_system()}")

# 获取惯用/原胞
conventional = sga.get_conventional_standard_structure()
primitive = sga.get_primitive_standard_structure()
```

**配位环境：**
```python
from pymatgen.analysis.local_env import CrystalNN

cnn = CrystalNN()
neighbors = cnn.get_nn_info(struct, n=0)  # 位点0的邻居

print(f"Coordination number: {len(neighbors)}")
for neighbor in neighbors:
    site = struct[neighbor['site_index']]
    print(f"  {site.species_string} at {neighbor['weight']:.3f} Å")
```

**使用分析脚本：**
```bash
# 综合分析
python scripts/structure_analyzer.py POSCAR --symmetry --neighbors

# 导出结果
python scripts/structure_analyzer.py structure.cif --symmetry --export json
```

**参考：** 有关所有分析功能的详细文档，请参见`references/analysis_modules.md`。

### 4. 相图和热力学

构建相图并分析热力学稳定性。

**相图构建：**
```python
from mp_api.client import MPRester
from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter

# 从Materials Project获取条目
with MPRester() as mpr:
    entries = mpr.get_entries_in_chemsys("Li-Fe-O")

# 构建相图
pd = PhaseDiagram(entries)

# 检查稳定性
from pymatgen.core import Composition
comp = Composition("LiFeO2")

# 查找组成的条目
for entry in entries:
    if entry.composition.reduced_formula == comp.reduced_formula:
        e_above_hull = pd.get_e_above_hull(entry)
        print(f"Energy above hull: {e_above_hull:.4f} eV/atom")

        if e_above_hull > 0.001:
            # 获取分解
            decomp = pd.get_decomposition(comp)
            print("Decomposes to:", decomp)

# 绘制
plotter = PDPlotter(pd)
plotter.show()
```

**使用相图脚本：**
```bash
# 生成相图
python scripts/phase_diagram_generator.py Li-Fe-O --output li_fe_o.png

# 分析特定组成
python scripts/phase_diagram_generator.py Li-Fe-O --analyze "LiFeO2" --show
```

**参考：** 有关详细示例，请参见`references/analysis_modules.md`（相图部分）和`references/transformations_workflows.md`（工作流2）。

### 5. 电子结构分析

分析能带结构、态密度和电子性质。

**能带结构：**
```python
from pymatgen.io.vasp import Vasprun
from pymatgen.electronic_structure.plotter import BSPlotter

# 从VASP计算读取
vasprun = Vasprun("vasprun.xml")
bs = vasprun.get_band_structure()

# 分析
band_gap = bs.get_band_gap()
print(f"Band gap: {band_gap['energy']:.3f} eV")
print(f"Direct: {band_gap['direct']}")
print(f"Is metal: {bs.is_metal()}")

# 绘制
plotter = BSPlotter(bs)
plotter.save_plot("band_structure.png")
```

**态密度：**
```python
from pymatgen.electronic_structure.plotter import DosPlotter

dos = vasprun.complete_dos

# 获取元素投影态密度
element_dos = dos.get_element_dos()
for element, element_dos_obj in element_dos.items():
    print(f"{element}: {element_dos_obj.get_gap():.3f} eV")

# 绘制
plotter = DosPlotter()
plotter.add_dos("Total DOS", dos)
plotter.show()
```

**参考：** 有关详细信息，请参见`references/analysis_modules.md`（电子结构部分）和`references/io_formats.md`（VASP部分）。

### 6. 表面和界面分析

生成平板，分析表面，研究界面。

**平板生成：**
```python
from pymatgen.core.surface import SlabGenerator

# 为特定米勒指数生成平板
slabgen = SlabGenerator(
    struct,
    miller_index=(1, 1, 1),
    min_slab_size=10.0,      # Å
    min_vacuum_size=10.0,    # Å
    center_slab=True
)

slabs = slabgen.get_slabs()

# 写入平板
for i, slab in enumerate(slabs):
    slab.to(filename=f"slab_{i}.cif")
```

**Wulff形状构建：**
```python
from pymatgen.analysis.wulff import WulffShape

# 定义表面能
surface_energies = {
    (1, 0, 0): 1.0,
    (1, 1, 0): 1.1,
    (1, 1, 1): 0.9,
}

wulff = WulffShape(struct.lattice, surface_energies)
print(f"Surface area: {wulff.surface_area:.2f} Ų")
print(f"Volume: {wulff.volume:.2f} ų")

wulff.show()
```

**吸附位点查找：**
```python
from pymatgen.analysis.adsorption import AdsorbateSiteFinder
from pymatgen.core import Molecule

asf = AdsorbateSiteFinder(slab)

# 查找位点
ads_sites = asf.find_adsorption_sites()
print(f"On-top sites: {len(ads_sites['ontop'])}")
print(f"Bridge sites: {len(ads_sites['bridge'])}")
print(f"Hollow sites: {len(ads_sites['hollow'])}")

# 添加吸附物
adsorbate = Molecule("O", [[0, 0, 0]])
ads_struct = asf.add_adsorbate(adsorbate, ads_sites["ontop"][0])
```

**参考：** 有关详细信息，请参见`references/analysis_modules.md`（表面和界面部分）和`references/transformations_workflows.md`（工作流3和9）。

### 7. Materials Project数据库访问

以编程方式访问Materials Project数据库。

**设置：**
1. 从https://next-gen.materialsproject.org/获取API密钥
2. 设置环境变量：`export MP_API_KEY="your_key_here"`

**搜索和检索：**
```python
from mp_api.client import MPRester

with MPRester() as mpr:
    # 按分子式搜索
    materials = mpr.materials.summary.search(formula="Fe2O3")

    # 按化学系统搜索
    materials = mpr.materials.summary.search(chemsys="Li-Fe-O")

    # 按属性过滤
    materials = mpr.materials.summary.search(
        chemsys="Li-Fe-O",
        energy_above_hull=(0, 0.05),  # 稳定/亚稳定
        band_gap=(1.0, 3.0)            # 半导体
    )

    # 获取结构
    struct = mpr.get_structure_by_material_id("mp-149")

    # 获取能带结构
    bs = mpr.get_bandstructure_by_material_id("mp-149")

    # 获取相图条目
    entries = mpr.get_entries_in_chemsys("Li-Fe-O")
```

**参考：** 有关综合API文档和示例，请参见`references/materials_project_api.md`。

### 8. 计算工作流设置

为各种电子结构代码设置计算。

**VASP输入生成：**
```python
from pymatgen.io.vasp.sets import MPRelaxSet, MPStaticSet, MPNonSCFSet

# 弛豫
relax = MPRelaxSet(struct)
relax.write_input("./relax_calc")

# 静态计算
static = MPStaticSet(struct)
static.write_input("./static_calc")

# 能带结构（非自洽）
nscf = MPNonSCFSet(struct, mode="line")
nscf.write_input("./bandstructure_calc")

# 自定义参数
custom = MPRelaxSet(struct, user_incar_settings={"ENCUT": 600})
custom.write_input("./custom_calc")
```

**其他代码：**
```python
# Gaussian
from pymatgen.io.gaussian import GaussianInput

gin = GaussianInput(
    mol,
    functional="B3LYP",
    basis_set="6-31G(d)",
    route_parameters={"Opt": None}
)
gin.write_file("input.gjf")

# Quantum ESPRESSO
from pymatgen.io.pwscf import PWInput

pwin = PWInput(struct, control={"calculation": "scf"})
pwin.write_file("pw.in")
```

**参考：** 有关工作流示例，请参见`references/io_formats.md`（电子结构代码I/O部分）和`references/transformations_workflows.md`。

### 9. 高级分析

**衍射图案：**
```python
from pymatgen.analysis.diffraction.xrd import XRDCalculator

xrd = XRDCalculator()
pattern = xrd.get_pattern(struct)

# 获取峰
for peak in pattern.hkls:
    print(f"2θ = {peak['2theta']:.2f}°, hkl = {peak['hkl']}")

pattern.plot()
```

**弹性性质：**
```python
from pymatgen.analysis.elasticity import ElasticTensor

# 从弹性张量矩阵
elastic_tensor = ElasticTensor.from_voigt(matrix)

print(f"Bulk modulus: {elastic_tensor.k_voigt:.1f} GPa")
print(f"Shear modulus: {elastic_tensor.g_voigt:.1f} GPa")
print(f"Young's modulus: {elastic_tensor.y_mod:.1f} GPa")
```

**磁有序：**
```python
from pymatgen.transformations.advanced_transformations import MagOrderingTransformation

# 枚举磁有序
trans = MagOrderingTransformation({"Fe": 5.0})
mag_structs = trans.apply_transformation(struct, return_ranked_list=True)

# 获取最低能量磁结构
lowest_energy_struct = mag_structs[0]['structure']
```

**参考：** 有关综合分析模块文档，请参见`references/analysis_modules.md`。

## 捆绑资源

### 脚本 (`scripts/`)

用于常见任务的可执行Python脚本：

- **`structure_converter.py`**：在结构文件格式之间转换
  - 支持批量转换和自动格式检测
  - 使用方法：`python scripts/structure_converter.py POSCAR structure.cif`

- **`structure_analyzer.py`**：综合结构分析
  - 对称性、配位、晶格参数、距离矩阵
  - 使用方法：`python scripts/structure_analyzer.py structure.cif --symmetry --neighbors`

- **`phase_diagram_generator.py`**：从Materials Project生成相图
  - 稳定性分析和热力学性质
  - 使用方法：`python scripts/phase_diagram_generator.py Li-Fe-O --analyze "LiFeO2"`

所有脚本都包含详细帮助：`python scripts/script_name.py --help`

### 参考 (`references/`)

根据需要加载到上下文中的综合文档：

- **`core_classes.md`**：Element、Structure、Lattice、Molecule、Composition类
- **`io_formats.md`**：文件格式支持和代码集成（VASP、Gaussian等）
- **`analysis_modules.md`**：相图、表面、电子结构、对称性
- **`materials_project_api.md`**：完整的Materials Project API指南
- **`transformations_workflows.md`**：转换框架和常见工作流

当需要有关特定模块或工作流的详细信息时加载参考。

## 常见工作流

### 高通量结构生成

```python
from pymatgen.transformations.standard_transformations import SubstitutionTransformation
from pymatgen.io.vasp.sets import MPRelaxSet

# 生成掺杂结构
base_struct = Structure.from_file("POSCAR")
dopants = ["Mn", "Co", "Ni", "Cu"]

for dopant in dopants:
    trans = SubstitutionTransformation({"Fe": dopant})
    doped_struct = trans.apply_transformation(base_struct)

    # 生成VASP输入
    vasp_input = MPRelaxSet(doped_struct)
    vasp_input.write_input(f"./calcs/Fe_{dopant}")
```

### 能带结构计算工作流

```python
# 1. 弛豫
relax = MPRelaxSet(struct)
relax.write_input("./1_relax")

# 2. 静态（弛豫后）
relaxed = Structure.from_file("1_relax/CONTCAR")
static = MPStaticSet(relaxed)
static.write_input("./2_static")

# 3. 能带结构（非自洽）
nscf = MPNonSCFSet(relaxed, mode="line")
nscf.write_input("./3_bandstructure")

# 4. 分析
from pymatgen.io.vasp import Vasprun
vasprun = Vasprun("3_bandstructure/vasprun.xml")
bs = vasprun.get_band_structure()
bs.get_band_gap()
```

### 表面能计算

```python
# 1. 获取体相能量
bulk_vasprun = Vasprun("bulk/vasprun.xml")
bulk_E_per_atom = bulk_vasprun.final_energy / len(bulk)

# 2. 生成并计算平板
slabgen = SlabGenerator(bulk, (1,1,1), 10, 15)
slab = slabgen.get_slabs()[0]

MPRelaxSet(slab).write_input("./slab_calc")

# 3. 计算表面能（计算后）
slab_vasprun = Vasprun("slab_calc/vasprun.xml")
E_surf = (slab_vasprun.final_energy - len(slab) * bulk_E_per_atom) / (2 * slab.surface_area)
E_surf *= 16.021766  # 转换eV/Ų为J/m²
```

**更多工作流：** 有关10个详细工作流示例，请参见`references/transformations_workflows.md`。

## 最佳实践

### 结构处理

1. **使用自动格式检测**：`Structure.from_file()`处理大多数格式
2. **偏好不可变结构**：当结构不应更改时使用`IStructure`
3. **检查对称性**：使用`SpacegroupAnalyzer`减少到原胞
4. **验证结构**：检查重叠原子或不合理的键长

### 文件I/O

1. **使用便捷方法**：`from_file()`和`to()`是首选
2. **显式指定格式**：当自动检测失败时
3. **处理异常**：将文件I/O包装在try-except块中
4. **使用序列化**：`as_dict()`/`from_dict()`用于版本安全存储

### Materials Project API

1. **使用上下文管理器**：始终使用`with MPRester() as mpr:`
2. **批量查询**：一次请求多个项目
3. **缓存结果**：在本地保存常用数据
4. **有效过滤**：使用属性过滤器减少数据传输

### 计算工作流

1. **使用输入集**：偏好`MPRelaxSet`、`MPStaticSet`而非手动INCAR
2. **检查收敛**：始终验证计算收敛
3. **跟踪转换**：使用`TransformedStructure`进行溯源
4. **组织计算**：使用清晰的目录结构

### 性能

1. **减少对称性**：尽可能使用原胞
2. **限制邻居搜索**：指定合理的截断半径
3. **使用适当的方法**：不同的分析工具具有不同的速度/精度权衡
4. **尽可能并行化**：许多操作可以并行化

## 单位和约定

Pymatgen在整个过程中使用原子单位：
- **长度**：埃（Å）
- **能量**：电子伏特（eV）
- **角度**：度（°）
- **磁矩**：玻尔磁子（μB）
- **时间**：飞秒（fs）

需要时使用`pymatgen.core.units`转换单位。

## 与其他工具的集成

Pymatgen与以下工具无缝集成：
- **ASE**（原子模拟环境）
- **Phonopy**（声子计算）
- **BoltzTraP**（输运性质）
- **Atomate/Fireworks**（工作流管理）
- **AiiDA**（溯源跟踪）
- **Zeo++**（孔分析）
- **OpenBabel**（分子转换）

## 故障排除

**导入错误**：安装缺少的依赖项
```bash
uv pip install pymatgen[analysis,vis]
```

**API密钥未找到**：设置MP_API_KEY环境变量
```bash
export MP_API_KEY="your_key_here"
```

**结构读取失败**：检查文件格式和语法
```python
# 尝试显式格式规范
struct = Structure.from_file("file.txt", fmt="cif")
```

**对称性分析失败**：结构可能存在数值精度问题
```python
# 增加容差
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
sga = SpacegroupAnalyzer(struct, symprec=0.1)
```

## 其他资源

- **文档**：https://pymatgen.org/
- **Materials Project**：https://materialsproject.org/
- **GitHub**：https://github.com/materialsproject/pymatgen
- **论坛**：https://matsci.org/
- **示例笔记本**：https://matgenb.materialsvirtuallab.org/

## 版本说明

此技能设计用于pymatgen 2024.x及更高版本。对于Materials Project API，使用`mp-api`包（与旧版`pymatgen.ext.matproj`分开）。

要求：
- Python 3.10或更高版本
- pymatgen >= 2023.x
- mp-api（用于Materials Project访问）