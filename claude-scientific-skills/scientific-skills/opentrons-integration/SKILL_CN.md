---
name: opentrons-integration
description: 适用于 OT-2 和 Flex 机器人的官方 Opentrons 协议 API。当专门为 Opentrons 硬件编写协议并完全访问 Protocol API v2 功能时使用。最适合生产级 Opentrons 协议，官方 API 兼容性。对于多厂商自动化或更广泛的设备控制，请使用 pylabrobot。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# Opentrons 集成

## 概述

Opentrons 是一个基于 Python 的实验室自动化平台，用于 Flex 和 OT-2 机器人。编写 Protocol API v2 协议用于液体处理、控制硬件模块（加热振荡器、热循环仪）、管理实验器皿、用于自动化移液工作流程。

## 何时使用此技能

此技能应在以下情况使用：
- 在 Python 中编写 Opentrons Protocol API v2 协议
- 在 Flex 或 OT-2 机器人上自动化液体处理工作流程
- 控制硬件模块（温度、磁力、加热振荡器、热循环仪）
- 设置实验器皿配置和工作台布局
- 实现复杂的移液操作（系列稀释、平板复制、PCR 设置）
- 管理吸头使用并优化协议效率
- 使用多通道移液器进行 96 孔板操作
- 在机器人执行前模拟和测试协议

## 核心功能

### 1. 协议结构和元数据

每个 Opentrons 协议都遵循标准结构：

```python
from opentrons import protocol_api

# 元数据
metadata = {
    'protocolName': 'My Protocol',
    'author': 'Name <email@example.com>',
    'description': 'Protocol description',
    'apiLevel': '2.19'  # 使用最新可用的 API 版本
}

# 要求（可选）
requirements = {
    'robotType': 'Flex',  # 或 'OT-2'
    'apiLevel': '2.19'
}

# 运行函数
def run(protocol: protocol_api.ProtocolContext):
    # 协议命令在这里
    pass
```

**关键元素：**
- 从 `opentrons` 导入 `protocol_api`
- 定义带有 protocolName、author、description、apiLevel 的 `metadata` 字典
- 可选的 `requirements` 字典，用于机器人类型和 API 版本
- 实现接收 `ProtocolContext` 作为参数的 `run()` 函数
- 所有协议逻辑都在 `run()` 函数内部

### 2. 加载硬件

**加载仪器（移液器）：**

```python
def run(protocol: protocol_api.ProtocolContext):
    # 在特定安装位置加载移液器
    left_pipette = protocol.load_instrument(
        'p1000_single_flex',  # 仪器名称
        'left',               # 安装位置: 'left' 或 'right'
        tip_racks=[tip_rack]  # 吸头架实验器皿对象列表
    )
```

常见移液器名称：
- Flex: `p50_single_flex`, `p1000_single_flex`, `p50_multi_flex`, `p1000_multi_flex`
- OT-2: `p20_single_gen2`, `p300_single_gen2`, `p1000_single_gen2`, `p20_multi_gen2`, `p300_multi_gen2`

**加载实验器皿：**

```python
# 直接在工作台上加载实验器皿
plate = protocol.load_labware(
    'corning_96_wellplate_360ul_flat',  # 实验器皿 API 名称
    'D1',                                # 工作台槽位 (Flex: A1-D3, OT-2: 1-11)
    label='Sample Plate'                 # 可选显示标签
)

# 加载吸头架
tip_rack = protocol.load_labware('opentrons_flex_96_tiprack_1000ul', 'C1')

# 在适配器上加载实验器皿
adapter = protocol.load_adapter('opentrons_flex_96_tiprack_adapter', 'B1')
tips = adapter.load_labware('opentrons_flex_96_tiprack_200ul')
```

**加载模块：**

```python
# 温度模块
temp_module = protocol.load_module('temperature module gen2', 'D3')
temp_plate = temp_module.load_labware('corning_96_wellplate_360ul_flat')

# 磁力模块
mag_module = protocol.load_module('magnetic module gen2', 'C2')
mag_plate = mag_module.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')

# 加热振荡器模块
hs_module = protocol.load_module('heaterShakerModuleV1', 'D1')
hs_plate = hs_module.load_labware('corning_96_wellplate_360ul_flat')

# 热循环仪模块（自动占用特定槽位）
tc_module = protocol.load_module('thermocyclerModuleV2')
tc_plate = tc_module.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')
```

### 3. 液体处理操作

**基本操作：**

```python
# 拾取吸头
pipette.pick_up_tip()

# 吸取（吸入液体）
pipette.aspirate(
    volume=100,           # 体积（微升）
    location=source['A1'] # 孔或位置对象
)

# 分配（排出液体）
pipette.dispense(
    volume=100,
    location=dest['B1']
)

# 丢弃吸头
pipette.drop_tip()

# 将吸头返回吸头架
pipette.return_tip()
```

**复杂操作：**

```python
# 转移（组合拾取、吸取、分配、丢弃吸头）
pipette.transfer(
    volume=100,
    source=source_plate['A1'],
    dest=dest_plate['B1'],
    new_tip='always'  # 'always', 'once', 或 'never'
)

# 分发（一个源到多个目标）
pipette.distribute(
    volume=50,
    source=reservoir['A1'],
    dest=[plate['A1'], plate['A2'], plate['A3']],
    new_tip='once'
)

# 合并（多个源到一个目标）
pipette.consolidate(
    volume=50,
    source=[plate['A1'], plate['A2'], plate['A3']],
    dest=reservoir['A1'],
    new_tip='once'
)
```

**高级技术：**

```python
# 混合（在同一位置吸取和分配）
pipette.mix(
    repetitions=3,
    volume=50,
    location=plate['A1']
)

# 空气间隙（防止滴液）
pipette.aspirate(100, source['A1'])
pipette.air_gap(20)  # 20µL 空气间隙
pipette.dispense(120, dest['A1'])

# 吹出（排出剩余液体）
pipette.blow_out(location=dest['A1'].top())

# 触碰吸头（移除吸头外部的液滴）
pipette.touch_tip(location=plate['A1'])
```

**流速控制：**

```python
# 设置流速（微升/秒）
pipette.flow_rate.aspirate = 150
pipette.flow_rate.dispense = 300
pipette.flow_rate.blow_out = 400
```

### 4. 访问孔和位置

**孔访问方法：**

```python
# 按名称
well_a1 = plate['A1']

# 按索引
first_well = plate.wells()[0]

# 所有孔
all_wells = plate.wells()  # 返回列表

# 按行
rows = plate.rows()  # 返回列表的列表
row_a = plate.rows()[0]  # 行 A 中的所有孔

# 按列
columns = plate.columns()  # 返回列表的列表
column_1 = plate.columns()[0]  # 列 1 中的所有孔

# 按名称访问孔（字典）
wells_dict = plate.wells_by_name()  # {'A1': Well, 'A2': Well, ...}
```

**位置方法：**

```python
# 孔顶部（默认：顶部下方 1mm）
pipette.aspirate(100, well.top())
pipette.aspirate(100, well.top(z=5))  # 顶部上方 5mm

# 孔底部（默认：底部上方 1mm）
pipette.aspirate(100, well.bottom())
pipette.aspirate(100, well.bottom(z=2))  # 底部上方 2mm

# 孔中心
pipette.aspirate(100, well.center())
```

### 5. 硬件模块控制

**温度模块：**

```python
# 设置温度
temp_module.set_temperature(celsius=4)

# 等待温度
temp_module.await_temperature(celsius=4)

# 停用
temp_module.deactivate()

# 检查状态
current_temp = temp_module.temperature  # 当前温度
target_temp = temp_module.target  # 目标温度
```

**磁力模块：**

```python
# 接合（升起磁铁）
mag_module.engage(height_from_base=10)  # 距离实验器皿底部的毫米数

# 分离（降下磁铁）
mag_module.disengage()

# 检查状态
is_engaged = mag_module.status  # 'engaged' 或 'disengaged'
```

**加热振荡器模块：**

```python
# 设置温度
hs_module.set_target_temperature(celsius=37)

# 等待温度
hs_module.wait_for_temperature()

# 设置振荡速度
hs_module.set_and_wait_for_shake_speed(rpm=500)

# 关闭实验器皿闩锁
hs_module.close_labware_latch()

# 打开实验器皿闩锁
hs_module.open_labware_latch()

# 停用加热器
hs_module.deactivate_heater()

# 停用振荡器
hs_module.deactivate_shaker()
```

**热循环仪模块：**

```python
# 打开盖子
tc_module.open_lid()

# 关闭盖子
tc_module.close_lid()

# 设置盖子温度
tc_module.set_lid_temperature(celsius=105)

# 设置模块温度
tc_module.set_block_temperature(
    temperature=95,
    hold_time_seconds=30,
    hold_time_minutes=0.5,
    block_max_volume=50  # 每孔微升
)

# 执行配置文件（PCR 循环）
profile = [
    {'temperature': 95, 'hold_time_seconds': 30},
    {'temperature': 57, 'hold_time_seconds': 30},
    {'temperature': 72, 'hold_time_seconds': 60}
]
tc_module.execute_profile(
    steps=profile,
    repetitions=30,
    block_max_volume=50
)

# 停用
tc_module.deactivate_lid()
tc_module.deactivate_block()
```

**吸光度读板仪：**

```python
# 初始化并读取
result = plate_reader.read(wavelengths=[450, 650])

# 访问读数
absorbance_data = result  # 带有波长键的字典
```

### 6. 液体跟踪和标记

**定义液体：**

```python
# 定义液体类型
water = protocol.define_liquid(
    name='Water',
    description='Ultrapure water',
    display_color='#0000FF'  # 十六进制颜色代码
)

sample = protocol.define_liquid(
    name='Sample',
    description='Cell lysate sample',
    display_color='#FF0000'
)
```

**将液体加载到孔中：**

```python
# 将液体加载到特定孔中
reservoir['A1'].load_liquid(liquid=water, volume=50000)  # 微升
plate['A1'].load_liquid(liquid=sample, volume=100)

# 将孔标记为空
plate['B1'].load_empty()
```

### 7. 协议控制和实用程序

**执行控制：**

```python
# 暂停协议
protocol.pause(msg='Replace tip box and resume')

# 延迟
protocol.delay(seconds=60)
protocol.delay(minutes=5)

# 注释（出现在日志中）
protocol.comment('Starting serial dilution')

# 机器人归位
protocol.home()
```

**条件逻辑：**

```python
# 检查是否在模拟
if protocol.is_simulating():
    protocol.comment('Running in simulation mode')
else:
    protocol.comment('Running on actual robot')
```

**轨道灯（仅 Flex）：**

```python
# 打开灯
protocol.set_rail_lights(on=True)

# 关闭灯
protocol.set_rail_lights(on=False)
```

### 8. 多通道和 8 通道移液

使用多通道移液器时：

```python
# 加载 8 通道移液器
multi_pipette = protocol.load_instrument(
    'p300_multi_gen2',
    'left',
    tip_racks=[tips]
)

# 用单个孔引用访问整个列
multi_pipette.transfer(
    volume=100,
    source=source_plate['A1'],  # 访问整个列 1
    dest=dest_plate['A1']       # 分配到整个列 1
)

# 使用 rows() 进行行操作
for row in plate.rows():
    multi_pipette.transfer(100, reservoir['A1'], row[0])
```

### 9. 常见协议模式

**系列稀释：**

```python
def run(protocol: protocol_api.ProtocolContext):
    # 加载实验器皿
    tips = protocol.load_labware('opentrons_flex_96_tiprack_200ul', 'D1')
    reservoir = protocol.load_labware('nest_12_reservoir_15ml', 'D2')
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 'D3')

    # 加载移液器
    p300 = protocol.load_instrument('p300_single_flex', 'left', tip_racks=[tips])

    # 除第一个孔外，向所有孔添加稀释剂
    p300.transfer(100, reservoir['A1'], plate.rows()[0][1:])

    # 跨行进行系列稀释
    p300.transfer(
        100,
        plate.rows()[0][:11],  # 源：孔 0-10
        plate.rows()[0][1:],   # 目标：孔 1-11
        mix_after=(3, 50),     # 分配后混合 3 次，每次 50µL
        new_tip='always'
    )
```

**平板复制：**

```python
def run(protocol: protocol_api.ProtocolContext):
    # 加载实验器皿
    tips = protocol.load_labware('opentrons_flex_96_tiprack_1000ul', 'C1')
    source = protocol.load_labware('corning_96_wellplate_360ul_flat', 'D1')
    dest = protocol.load_labware('corning_96_wellplate_360ul_flat', 'D2')

    # 加载移液器
    p1000 = protocol.load_instrument('p1000_single_flex', 'left', tip_racks=[tips])

    # 从源中的所有孔转移到目标
    p1000.transfer(
        100,
        source.wells(),
        dest.wells(),
        new_tip='always'
    )
```

**PCR 设置：**

```python
def run(protocol: protocol_api.ProtocolContext):
    # 加载热循环仪
    tc_mod = protocol.load_module('thermocyclerModuleV2')
    tc_plate = tc_mod.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')

    # 加载吸头和试剂
    tips = protocol.load_labware('opentrons_flex_96_tiprack_200ul', 'C1')
    reagents = protocol.load_labware('opentrons_24_tuberack_nest_1.5ml_snapcap', 'D1')

    # 加载移液器
    p300 = protocol.load_instrument('p300_single_flex', 'left', tip_racks=[tips])

    # 打开热循环仪盖子
    tc_mod.open_lid()

    # 分发主混合液
    p300.distribute(
        20,
        reagents['A1'],
        tc_plate.wells(),
        new_tip='once'
    )

    # 添加样本（前 8 个孔的示例）
    for i, well in enumerate(tc_plate.wells()[:8]):
        p300.transfer(5, reagents.wells()[i+1], well, new_tip='always')

    # 运行 PCR
    tc_mod.close_lid()
    tc_mod.set_lid_temperature(105)

    # PCR 配置文件
    tc_mod.set_block_temperature(95, hold_time_seconds=180)

    profile = [
        {'temperature': 95, 'hold_time_seconds': 15},
        {'temperature': 60, 'hold_time_seconds': 30},
        {'temperature': 72, 'hold_time_seconds': 30}
    ]
    tc_mod.execute_profile(steps=profile, repetitions=35, block_max_volume=25)

    tc_mod.set_block_temperature(72, hold_time_minutes=5)
    tc_mod.set_block_temperature(4)

    tc_mod.deactivate_lid()
    tc_mod.open_lid()
```

## 最佳实践

1. **始终指定 API 级别**：在元数据中使用最新的稳定 API 版本
2. **使用有意义的标签**：为实验器皿添加标签以便在日志中更容易识别
3. **检查吸头可用性**：确保有足够的吸头完成协议
4. **添加注释**：使用 `protocol.comment()` 进行调试和日志记录
5. **先模拟**：在机器人上运行前始终在模拟中测试协议
6. **优雅处理错误**：在需要时添加暂停以便手动干预
7. **考虑时间**：当协议需要孵育期时使用延迟
8. **跟踪液体**：使用液体跟踪进行更好的设置验证
9. **优化吸头使用**：在适当的情况下使用 `new_tip='once'` 以节省吸头
10. **控制流速**：为粘性或挥发性液体调整流速

## 故障排除

**常见问题：**

- **吸头用完**：验证吸头架容量是否与协议要求匹配
- **实验器皿碰撞**：检查工作台布局是否存在空间冲突
- **体积错误**：确保体积不超过孔或移液器容量
- **模块无响应**：验证模块是否正确连接且固件已更新
- **体积不准确**：校准移液器并检查是否有气泡
- **协议在模拟中失败**：检查 API 版本兼容性和实验器皿定义

## 资源

有关详细的 API 文档，请参阅此技能目录中的 `references/api_reference.md`。

有关示例协议模板，请参阅 `scripts/` 目录。