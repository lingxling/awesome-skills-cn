---
name: pylabrobot
description: 厂商无关的实验室自动化框架。用于控制多种设备类型（Hamilton、Tecan、Opentrons、读板机、泵）或需要跨不同厂商的统一编程。最适合复杂工作流程、多厂商设置、模拟。对于使用官方API的仅Opentrons协议，opentrons-integration可能更简单。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# PyLabRobot

## 概述

PyLabRobot是一个硬件无关的纯Python软件开发工具包，用于自动化和自主实验室。使用此技能通过统一的Python接口控制液体处理机器人、读板机、泵、加热振荡器、培养箱、离心机和其他实验室自动化设备，可跨平台（Windows、macOS、Linux）工作。

## 使用场景

当您需要以下操作时使用此技能：
- 编程液体处理机器人（Hamilton STAR/STARlet、Opentrons OT-2、Tecan EVO）
- 自动化涉及移液、样品制备或分析测量的实验室工作流程
- 管理工作台布局和实验室资源（板、吸头、容器、槽）
- 集成多个实验室设备（液体处理器、读板机、加热振荡器、泵）
- 创建具有状态管理的可重现实验室协议
- 在物理硬件上运行前模拟协议
- 使用BMG CLARIOstar或其他支持的读板机读取板
- 控制温度、振荡、离心或其他材料处理操作
- 在Python中进行实验室自动化

## 核心功能

PyLabRobot通过六个主要功能领域提供全面的实验室自动化，每个领域在references/目录中详细说明：

### 1. 液体处理 (`references/liquid-handling.md`)

控制液体处理机器人进行吸液、分液和液体转移。关键操作包括：
- **基本操作**：吸液、分液、在孔之间转移液体
- **吸头管理**：自动拾取、丢弃和跟踪移液器吸头
- **高级技术**：多通道移液、系列稀释、板复制
- **体积跟踪**：自动跟踪孔中的液体体积
- **硬件支持**：Hamilton STAR/STARlet、Opentrons OT-2、Tecan EVO等

### 2. 资源管理 (`references/resources.md`)

在分层系统中管理实验室资源：
- **资源类型**：板、吸头盒、槽、试管、载体和自定义实验室器具
- **工作台布局**：通过坐标系将资源分配到工作台位置
- **状态管理**：跟踪吸头存在、液体体积和资源状态
- **序列化**：从JSON文件保存和加载工作台布局和状态
- **资源发现**：通过直观的API访问孔、吸头和容器

### 3. 硬件后端 (`references/hardware-backends.md`)

通过后端抽象连接到各种实验室设备：
- **液体处理器**：Hamilton STAR（完全支持）、Opentrons OT-2、Tecan EVO
- **模拟**：ChatterboxBackend用于无硬件的协议测试
- **平台支持**：在Windows、macOS、Linux和树莓派上工作
- **后端切换**：通过交换后端更改机器人，无需重写协议

### 4. 分析设备 (`references/analytical-equipment.md`)

集成读板机和分析仪器：
- **读板机**：BMG CLARIOstar用于吸光度、发光、荧光
- **天平**：Mettler Toledo集成用于质量测量
- **集成模式**：将液体处理器与分析设备结合
- **自动化工作流程**：自动在设备之间移动板

### 5. 材料处理 (`references/material-handling.md`)

控制环境和材料处理设备：
- **加热振荡器**：Hamilton HeaterShaker、Inheco ThermoShake
- **培养箱**：具有温度控制的Inheco和Thermo Fisher培养箱
- **离心机**：Agilent VSpin，具有桶定位和旋转控制
- **泵**：Cole Parmer Masterflex用于流体泵送操作
- **温度控制**：在协议期间设置和监控温度

### 6. 可视化和模拟 (`references/visualization.md`)

可视化和模拟实验室协议：
- **浏览器可视化器**：工作台状态的实时3D可视化
- **模拟模式**：无需物理硬件测试协议
- **状态跟踪**：可视化监控吸头存在和液体体积
- **工作台编辑器**：用于设计工作台布局的图形工具
- **协议验证**：在硬件上运行前验证协议

## 快速开始

要开始使用PyLabRobot，安装包并初始化液体处理器：

```python
# 安装PyLabRobot
# uv pip install pylabrobot

# 基本液体处理设置
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import STAR
from pylabrobot.resources import STARLetDeck

# 初始化液体处理器
lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
await lh.setup()

# 基本操作
await lh.pick_up_tips(tip_rack["A1:H1"])
await lh.aspirate(plate["A1"], vols=100)
await lh.dispense(plate["A2"], vols=100)
await lh.drop_tips()
```

## 使用参考

此技能在多个参考文件中组织详细信息。在以下情况下加载相关参考：
- **液体处理**：编写移液协议、吸头管理、转移
- **资源**：定义工作台布局、管理板/吸头、自定义实验室器具
- **硬件后端**：连接到特定机器人、切换平台
- **分析设备**：集成读板机、天平或分析设备
- **材料处理**：使用加热振荡器、培养箱、离心机、泵
- **可视化**：模拟协议、可视化工作台状态

所有参考文件都可以在`references/`目录中找到，包含全面的示例、API使用模式和最佳实践。

## 最佳实践

使用PyLabRobot创建实验室自动化协议时：

1. **从模拟开始**：使用ChatterboxBackend和可视化器在硬件上运行前测试协议
2. **启用跟踪**：开启吸头跟踪和体积跟踪以实现准确的状态管理
3. **资源命名**：为所有资源（板、吸头盒、容器）使用清晰、描述性的名称
4. **状态序列化**：将工作台布局和状态保存到JSON以实现可重现性
5. **错误处理**：为硬件操作实现适当的异步错误处理
6. **温度控制**：提前设置温度，因为加热/冷却需要时间
7. **模块化协议**：将复杂工作流程分解为可重用函数
8. **文档**：参考官方文档 https://docs.pylabrobot.org 获取最新功能

## 常见工作流程

### 液体转移协议

```python
# 设置
lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
await lh.setup()

# 定义资源
tip_rack = TIP_CAR_480_A00(name="tip_rack")
source_plate = Cos_96_DW_1mL(name="source")
dest_plate = Cos_96_DW_1mL(name="dest")

lh.deck.assign_child_resource(tip_rack, rails=1)
lh.deck.assign_child_resource(source_plate, rails=10)
lh.deck.assign_child_resource(dest_plate, rails=15)

# 转移协议
await lh.pick_up_tips(tip_rack["A1:H1"])
await lh.transfer(source_plate["A1:H12"], dest_plate["A1:H12"], vols=100)
await lh.drop_tips()
```

### 读板工作流程

```python
# 设置读板机
from pylabrobot.plate_reading import PlateReader
from pylabrobot.plate_reading.clario_star_backend import CLARIOstarBackend

pr = PlateReader(name="CLARIOstar", backend=CLARIOstarBackend())
await pr.setup()

# 设置温度并读取
await pr.set_temperature(37)
await pr.open()
# (手动或机器人加载板)
await pr.close()
data = await pr.read_absorbance(wavelength=450)
```

## 其他资源

- **官方文档**：https://docs.pylabrobot.org
- **GitHub仓库**：https://github.com/PyLabRobot/pylabrobot
- **社区论坛**：https://discuss.pylabrobot.org
- **PyPI包**：https://pypi.org/project/PyLabRobot/

有关特定功能的详细使用方法，请参考`references/`目录中相应的参考文件。