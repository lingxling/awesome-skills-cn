---
name: flowio
description: 解析FCS（流式细胞术标准）文件v2.0-3.1。将事件提取为NumPy数组、读取元数据/通道、转换为CSV/DataFrame，用于流式细胞术数据预处理。
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# FlowIO: 流式细胞术标准文件处理器

## 概述

FlowIO是一个轻量级Python库，用于读取和写入流式细胞术标准（FCS）文件。解析FCS元数据、提取事件数据，并使用最少的依赖项创建新的FCS文件。该库支持FCS 2.0、3.0和3.1版本，非常适合后端服务、数据管道和基本细胞术文件操作。

## 何时使用此技能

此技能应在以下情况下使用：

- 需要解析或提取元数据的FCS文件
- 需要转换为NumPy数组的流式细胞术数据
- 需要导出为FCS格式的事件数据
- 需要分离的多数据集FCS文件
- 需要通道信息提取（散射光、荧光、时间）
- 需要细胞术文件验证或检查
- 高级分析前的预处理工作流

**相关工具：** 对于高级流式细胞术分析（包括补偿、门控和FlowJo/GatingML支持），建议将FlowKit库作为FlowIO的配套工具。

## 安装

```bash
uv pip install flowio
```

需要Python 3.9或更高版本。

## 快速开始

### 基本文件读取

```python
from flowio import FlowData

# 读取FCS文件
flow_data = FlowData('experiment.fcs')

# 访问基本信息
print(f"FCS版本: {flow_data.version}")
print(f"事件数: {flow_data.event_count}")
print(f"通道数: {flow_data.pnn_labels}")

# 获取事件数据为NumPy数组
events = flow_data.as_array()  # 形状：（事件，通道）
```

### 创建FCS文件

```python
import numpy as np
from flowio import create_fcs

# 准备数据
data = np.array([[100, 200, 50], [150, 180, 60]])  # 2个事件，3个通道
channels = ['FSC-A', 'SSC-A', 'FL1-A']

# 创建FCS文件
create_fcs('output.fcs', data, channels)
```

## 核心工作流

### 读取和解析FCS文件

FlowData类提供读取FCS文件的主要接口。

**标准读取：**

```python
from flowio import FlowData

# 基本读取
flow = FlowData('sample.fcs')

# 访问属性
version = flow.version              # '3.0', '3.1'等
event_count = flow.event_count      # 事件数
channel_count = flow.channel_count  # 通道数
pnn_labels = flow.pnn_labels        # 短通道名称
pns_labels = flow.pns_labels        # 描述性染色名称

# 获取事件数据
events = flow.as_array()            # 预处理（应用增益、对数缩放）
raw_events = flow.as_array(preprocess=False)  # 原始数据
```

**内存高效的元数据读取：**

当只需要元数据（不需要事件数据）时：

```python
# 仅解析TEXT段，跳过DATA和ANALYSIS
flow = FlowData('sample.fcs', only_text=True)

# 访问元数据
metadata = flow.text  # TEXT段关键字的字典
print(metadata.get('$DATE'))  # 获取日期
print(metadata.get('$CYT'))   # 仪器名称
```

**处理问题文件：**

某些FCS文件存在偏移量差异或错误：

```python
# 忽略HEADER和TEXT段之间的偏移量差异
flow = FlowData('problematic.fcs', ignore_offset_discrepancy=True)

# 使用HEADER偏移量而不是TEXT偏移量
flow = FlowData('problematic.fcs', use_header_offsets=True)

# 完全忽略偏移错误
flow = FlowData('problematic.fcs', ignore_offset_error=True)
```

**排除空通道：**

```python
# 在解析期间排除特定通道
flow = FlowData('sample.fcs', null_channel_list=['Time', 'Null'])
```

### 提取元数据和通道信息

FCS文件在TEXT段中包含丰富的元数据。

**常见元数据关键字：**

```python
flow = FlowData('sample.fcs')

# 文件级元数据
text_dict = flow.text
acquisition_date = text_dict.get('$DATE', 'Unknown')
instrument = text_dict.get('$CYT', 'Unknown')
data_type = flow.data_type  # 'I', 'F', 'D', 'A'

# 通道元数据
for i in range(flow.channel_count):
    pnn = flow.pnn_labels[i]      # 短名称（例如'FSC-A'）
    pns = flow.pns_labels[i]      # 描述性名称（例如'前向散射光'）
    pnr = flow.pnr_values[i]      # 范围/最大值
    print(f"通道 {i}: {pnn} ({pns}), 范围: {pnr}")
```

**通道类型识别：**

FlowIO自动分类通道：

```python
# 按通道类型获取索引
scatter_idx = flow.scatter_indices    # [0, 1]用于FSC、SSC
fluoro_idx = flow.fluoro_indices      # [2, 3, 4]用于FL通道
time_idx = flow.time_index            # 时间通道的索引（或None）

# 访问特定通道类型
events = flow.as_array()
scatter_data = events[:, scatter_idx]
fluorescence_data = events[:, fluoro_idx]
```

**ANALYSIS段：**

如果存在，访问处理结果：

```python
if flow.analysis:
    analysis_keywords = flow.analysis  # ANALYSIS关键字的字典
    print(analysis_keywords)
```

### 创建新的FCS文件

从NumPy数组或其他数据源生成FCS文件。

**基本创建：**

```python
import numpy as np
from flowio import create_fcs

# 创建事件数据（行=事件，列=通道）
events = np.random.rand(10000, 5) * 1000

# 定义通道名称
channel_names = ['FSC-A', 'SSC-A', 'FL1-A', 'FL2-A', 'Time']

# 创建FCS文件
create_fcs('output.fcs', events, channel_names)
```

**带描述性通道名称：**

```python
# 添加可选的描述性名称（PnS）
channel_names = ['FSC-A', 'SSC-A', 'FL1-A', 'FL2-A', 'Time']
descriptive_names = ['前向散射光', '侧向散射光', 'FITC', 'PE', '时间']

create_fcs('output.fcs',
           events,
           channel_names,
           opt_channel_names=descriptive_names)
```

**带自定义元数据：**

```python
# 添加TEXT段元数据
metadata = {
    '$SRC': 'Python脚本',
    '$DATE': '19-OCT-2025',
    '$CYT': '合成仪器',
    '$INST': '实验室A'
}

create_fcs('output.fcs',
           events,
           channel_names,
           opt_channel_names=descriptive_names,
           metadata=metadata)
```

**注意：** FlowIO导出为FCS 3.1，使用单精度浮点数据。

### 导出修改后的数据

修改现有FCS文件并重新导出。

**方法1：使用write_fcs()方法：**

```python
from flowio import FlowData

# 读取原始文件
flow = FlowData('original.fcs')

# 使用更新的元数据写入
flow.write_fcs('modified.fcs', metadata={'$SRC': '修改后的数据'})
```

**方法2：提取、修改和重新创建：**

用于修改事件数据：

```python
from flowio import FlowData, create_fcs

# 读取并提取数据
flow = FlowData('original.fcs')
events = flow.as_array(preprocess=False)

# 修改事件数据
events[:, 0] = events[:, 0] * 1.5  # 缩放第一个通道

# 使用修改后的数据创建新的FCS文件
create_fcs('modified.fcs',
           events,
           flow.pnn_labels,
           opt_channel_names=flow.pns_labels,
           metadata=flow.text)
```

### 处理多数据集FCS文件

某些FCS文件在单个文件中包含多个数据集。

**检测多数据集文件：**

```python
from flowio import FlowData, MultipleDataSetsError

try:
    flow = FlowData('sample.fcs')
except MultipleDataSetsError:
    print("文件包含多个数据集")
    # 改用read_multiple_data_sets()
```

**读取所有数据集：**

```python
from flowio import read_multiple_data_sets

# 从文件读取所有数据集
datasets = read_multiple_data_sets('multi_dataset.fcs')

print(f"找到 {len(datasets)} 个数据集")

# 处理每个数据集
for i, dataset in enumerate(datasets):
    print(f"\n数据集 {i}:")
    print(f"  事件数: {dataset.event_count}")
    print(f"  通道数: {dataset.pnn_labels}")

    # 获取此数据集的事件数据
    events = dataset.as_array()
    print(f"  形状: {events.shape}")
    print(f"  平均值: {events.mean(axis=0)}")
```

**读取特定数据集：**

```python
from flowio import FlowData

# 读取第一个数据集（nextdata_offset=0）
first_dataset = FlowData('multi.fcs', nextdata_offset=0)

# 使用第一个数据集中的NEXTDATA偏移量读取第二个数据集
next_offset = int(first_dataset.text['$NEXTDATA'])
if next_offset > 0:
    second_dataset = FlowData('multi.fcs', nextdata_offset=next_offset)
```

## 数据预处理

当`preprocess=True`时，FlowIO应用标准FCS预处理转换。

**预处理步骤：**

1. **增益缩放：** 将值乘以PnG（增益）关键字
2. **对数转换：** 如果存在，应用PnE指数转换
   - 公式：`value = a * 10^(b * raw_value)`，其中PnE = "a,b"
3. **时间缩放：** 将时间值转换为适当单位

**控制预处理：**

```python
# 预处理数据（默认）
preprocessed = flow.as_array(preprocess=True)

# 原始数据（无转换）
raw = flow.as_array(preprocess=False)
```

## 错误处理

适当处理常见的FlowIO异常。

```python
from flowio import (
    FlowData,
    FCSParsingError,
    DataOffsetDiscrepancyError,
    MultipleDataSetsError
)

try:
    flow = FlowData('sample.fcs')
    events = flow.as_array()

except FCSParsingError as e:
    print(f"解析FCS文件失败: {e}")
    # 尝试使用宽松的解析
    flow = FlowData('sample.fcs', ignore_offset_error=True)

except DataOffsetDiscrepancyError as e:
    print(f"检测到偏移量差异: {e}")
    # 使用ignore_offset_discrepancy参数
    flow = FlowData('sample.fcs', ignore_offset_discrepancy=True)

except MultipleDataSetsError as e:
    print(f"检测到多个数据集: {e}")
    # 改用read_multiple_data_sets
    from flowio import read_multiple_data_sets
    datasets = read_multiple_data_sets('sample.fcs')

except Exception as e:
    print(f"意外错误: {e}")
```

## 常见用例

### 检查FCS文件内容

快速探索FCS文件结构：

```python
from flowio import FlowData

flow = FlowData('unknown.fcs')

print("=" * 50)
print(f"文件: {flow.name}")
print(f"版本: {flow.version}")
print(f"大小: {flow.file_size:,} 字节")
print("=" * 50)

print(f"\n事件数: {flow.event_count:,}")
print(f"通道数: {flow.channel_count}")

print("\n通道信息:")
for i, (pnn, pns) in enumerate(zip(flow.pnn_labels, flow.pns_labels)):
    ch_type = "散射光" if i in flow.scatter_indices else \
              "荧光" if i in flow.fluoro_indices else \
              "时间" if i == flow.time_index else "其他"
    print(f"  [{i}] {pnn:10s} | {pns:30s} | {ch_type}")

print("\n关键元数据:")
for key in ['$DATE', '$BTIM', '$ETIM', '$CYT', '$INST', '$SRC']:
    value = flow.text.get(key, 'N/A')
    print(f"  {key:15s}: {value}")
```

### 批量处理多个文件

处理目录中的FCS文件：

```python
from pathlib import Path
from flowio import FlowData
import pandas as pd

# 查找所有FCS文件
fcs_files = list(Path('data/').glob('*.fcs'))

# 提取摘要信息
summaries = []
for fcs_path in fcs_files:
    try:
        flow = FlowData(str(fcs_path), only_text=True)
        summaries.append({
            'filename': fcs_path.name,
            'version': flow.version,
            'events': flow.event_count,
            'channels': flow.channel_count,
            'date': flow.text.get('$DATE', 'N/A')
        })
    except Exception as e:
        print(f"处理 {fcs_path.name} 时出错: {e}")

# 创建摘要DataFrame
df = pd.DataFrame(summaries)
print(df)
```

### 将FCS转换为CSV

将事件数据导出为CSV格式：

```python
from flowio import FlowData
import pandas as pd

# 读取FCS文件
flow = FlowData('sample.fcs')

# 转换为DataFrame
df = pd.DataFrame(
    flow.as_array(),
    columns=flow.pnn_labels
)

# 将元数据添加为属性
df.attrs['fcs_version'] = flow.version
df.attrs['instrument'] = flow.text.get('$CYT', 'Unknown')

# 导出为CSV
df.to_csv('output.csv', index=False)
print(f"已导出 {len(df)} 个事件到CSV")
```

### 过滤事件并重新导出

应用过滤器并保存过滤后的数据：

```python
from flowio import FlowData, create_fcs
import numpy as np

# 读取原始文件
flow = FlowData('sample.fcs')
events = flow.as_array(preprocess=False)

# 应用过滤器（示例：第一个通道的阈值）
fsc_idx = 0
threshold = 500
mask = events[:, fsc_idx] > threshold
filtered_events = events[mask]

print(f"原始事件数: {len(events)}")
print(f"过滤后事件数: {len(filtered_events)}")

# 使用过滤后的数据创建新的FCS文件
create_fcs('filtered.fcs',
           filtered_events,
           flow.pnn_labels,
           opt_channel_names=flow.pns_labels,
           metadata={**flow.text, '$SRC': '过滤后的数据'})
```

### 提取特定通道

提取和处理特定通道：

```python
from flowio import FlowData
import numpy as np

flow = FlowData('sample.fcs')
events = flow.as_array()

# 仅提取荧光通道
fluoro_indices = flow.fluoro_indices
fluoro_data = events[:, fluoro_indices]
fluoro_names = [flow.pnn_labels[i] for i in fluoro_indices]

print(f"荧光通道: {fluoro_names}")
print(f"形状: {fluoro_data.shape}")

# 计算每个通道的统计信息
for i, name in enumerate(fluoro_names):
    channel_data = fluoro_data[:, i]
    print(f"\n{name}:")
    print(f"  平均值: {channel_data.mean():.2f}")
    print(f"  中位数: {np.median(channel_data):.2f}")
    print(f"  标准差: {channel_data.std():.2f}")
```

## 最佳实践

1. **内存效率：** 当不需要事件数据时使用`only_text=True`
2. **错误处理：** 将文件操作包装在try-except块中以实现健壮的代码
3. **多数据集检测：** 检查MultipleDataSetsError并使用适当的函数
4. **预处理控制：** 根据分析需求显式设置`preprocess`参数
5. **偏移问题：** 如果解析失败，尝试`ignore_offset_discrepancy=True`参数
6. **通道验证：** 在处理之前验证通道计数和名称是否符合预期
7. **元数据保留：** 修改文件时，保留原始TEXT段关键字

## 高级主题

### 理解FCS文件结构

FCS文件由四个段组成：

1. **HEADER：** FCS版本和其他段的字节偏移量
2. **TEXT：** 键值元数据对（分隔符分隔）
3. **DATA：** 原始事件数据（二进制/浮点/ASCII格式）
4. **ANALYSIS**（可选）：数据处理结果

通过FlowData属性访问这些段：
- `flow.header` - HEADER段
- `flow.text` - TEXT段关键字
- `flow.events` - DATA段（作为字节）
- `flow.analysis` - ANALYSIS段关键字（如果存在）

### 详细API参考

有关全面的API文档，包括所有参数、方法、异常和FCS关键字参考，请查阅详细的参考文件：

**阅读：** `references/api_reference.md`

该参考包括：
- 完整的FlowData类文档
- 所有实用函数（read_multiple_data_sets、create_fcs）
- 异常类和处理
- FCS文件结构详细信息
- 常见TEXT段关键字
- 扩展示例工作流

在处理复杂的FCS操作或遇到不寻常的文件格式时，加载此参考以获取详细指导。

## 集成说明

**NumPy数组：** 所有事件数据作为形状为（事件，通道）的NumPy ndarrays返回

**Pandas DataFrames：** 轻松转换为DataFrames以进行分析：
```python
import pandas as pd
df = pd.DataFrame(flow.as_array(), columns=flow.pnn_labels)
```

**FlowKit集成：** 对于高级分析（补偿、门控、FlowJo支持），使用构建在FlowIO解析功能之上的FlowKit库

**Web应用程序：** FlowIO的最少依赖项使其成为处理FCS上传的Web后端服务的理想选择

## 故障排除

**问题：** "偏移量差异错误"
**解决方案：** 使用`ignore_offset_discrepancy=True`参数

**问题：** "多个数据集错误"
**解决方案：** 改用`read_multiple_data_sets()`函数而不是FlowData构造函数

**问题：** 大文件内存不足
**解决方案：** 对仅元数据操作使用`only_text=True`，或分块处理事件

**问题：** 意外的通道计数
**解决方案：** 检查空通道；使用`null_channel_list`参数排除它们

**问题：** 无法就地修改事件数据
**解决方案：** FlowIO不支持直接修改；提取数据，修改，然后使用`create_fcs()`保存

## 摘要

FlowIO为流式细胞术工作流提供基本的FCS文件处理能力。使用它进行解析、元数据提取和文件创建。对于简单的文件操作和数据提取，FlowIO就足够了。对于包括补偿和门控的复杂分析，与FlowKit或其他专用工具集成。
