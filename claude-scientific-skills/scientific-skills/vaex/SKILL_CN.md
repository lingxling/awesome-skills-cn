---
name: vaex
description: 使用此技能处理和分析超出可用RAM的大型表格数据集（数十亿行）。Vaex擅长核心外DataFrame操作、延迟评估、快速聚合、大数据的高效可视化以及大型数据集上的机器学习。当用户需要处理大型CSV/HDF5/Arrow/Parquet文件、对海量数据集执行快速统计、创建大数据的可视化或构建不适合内存的ML管道时应用。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# Vaex

## 概述

Vaex是一个高性能Python库，专为延迟、核心外DataFrame设计，用于处理和可视化太大而无法放入RAM的表格数据集。Vaex可以每秒处理超过十亿行数据，支持对拥有数十亿行的数据集进行交互式数据探索和分析。

## 何时使用此技能

在以下情况下使用Vaex：
- 处理大于可用RAM的表格数据集（从千兆字节到太字节）
- 对海量数据集执行快速统计聚合
- 创建大型数据集的可视化和热图
- 在大数据上构建机器学习管道
- 在不同数据格式之间转换（CSV、HDF5、Arrow、Parquet）
- 需要延迟评估和虚拟列以避免内存开销
- 处理天文数据、金融时间序列或其他大规模科学数据集

## 核心功能

Vaex提供六个主要功能领域，每个领域在参考目录中都有详细记录：

### 1. DataFrames和数据加载

从各种来源加载和创建Vaex DataFrames，包括文件（HDF5、CSV、Arrow、Parquet）、pandas DataFrames、NumPy数组和字典。参考`references/core_dataframes.md`了解：
- 高效打开大型文件
- 从pandas/NumPy/Arrow转换
- 使用示例数据集
- 理解DataFrame结构

### 2. 数据处理和操作

执行过滤、创建虚拟列、使用表达式和聚合数据，而无需将所有内容加载到内存中。参考`references/data_processing.md`了解：
- 过滤和选择
- 虚拟列和表达式
- 分组操作和聚合
- 字符串操作和日期时间处理
- 处理缺失数据

### 3. 性能和优化

利用Vaex的延迟评估、缓存策略和内存高效操作。参考`references/performance.md`了解：
- 理解延迟评估
- 使用`delay=True`进行批处理操作
- 在需要时实例化列
- 缓存策略
- 异步操作

### 4. 数据可视化

创建大型数据集的交互式可视化，包括热图、直方图和散点图。参考`references/visualization.md`了解：
- 创建1D和2D图表
- 热图可视化
- 处理选择
- 自定义图表和子图

### 5. 机器学习集成

使用转换器、编码器和与scikit-learn、XGBoost和其他框架的集成构建ML管道。参考`references/machine_learning.md`了解：
- 特征缩放和编码
- PCA和维度减少
- K-means聚类
- 与scikit-learn/XGBoost/CatBoost集成
- 模型序列化和部署

### 6. I/O操作

以最佳性能高效读写各种格式的数据。参考`references/io_operations.md`了解：
- 文件格式建议
- 导出策略
- 使用Apache Arrow
- 处理大型文件的CSV
- 服务器和远程数据访问

## 快速入门模式

对于大多数Vaex任务，遵循以下模式：

```python
import vaex

# 1. 打开或创建DataFrame
df = vaex.open('large_file.hdf5')  # 或 .csv, .arrow, .parquet
# 或
df = vaex.from_pandas(pandas_df)

# 2. 探索数据
print(df)  # 显示首/尾行和列信息
df.describe()  # 统计摘要

# 3. 创建虚拟列（无内存开销）
df['new_column'] = df.x ** 2 + df.y

# 4. 用选择进行过滤
df_filtered = df[df.age > 25]

# 5. 计算统计信息（快速，延迟评估）
mean_val = df.x.mean()
stats = df.groupby('category').agg({'value': 'sum'})

# 6. 可视化
df.plot1d(df.x, limits=[0, 100])
df.plot(df.x, df.y, limits='99.7%')

# 7. 必要时导出
df.export_hdf5('output.hdf5')
```

## 使用参考

参考文件包含每个功能领域的详细信息。根据具体任务将参考加载到上下文中：

- **基本操作**：从`references/core_dataframes.md`和`references/data_processing.md`开始
- **性能问题**：查看`references/performance.md`
- **可视化任务**：使用`references/visualization.md`
- **ML管道**：参考`references/machine_learning.md`
- **文件I/O**：查阅`references/io_operations.md`

## 最佳实践

1. **使用HDF5或Apache Arrow格式**以获得大型数据集的最佳性能
2. **利用虚拟列**而非实例化数据以节省内存
3. **使用`delay=True`**在执行多个计算时批处理操作
4. **导出到高效格式**而不是将数据保存在CSV中
5. **使用表达式**进行复杂计算，无需中间存储
6. **使用`df.stat()`进行分析**以了解内存使用情况并优化操作

## 常见模式

### 模式：将大型CSV转换为HDF5
```python
import vaex

# 打开大型CSV（自动分块处理）
df = vaex.from_csv('large_file.csv')

# 导出到HDF5以便将来更快访问
df.export_hdf5('large_file.hdf5')

# 将来加载是即时的
df = vaex.open('large_file.hdf5')
```

### 模式：高效聚合
```python
# 使用delay=True批处理多个操作
mean_x = df.x.mean(delay=True)
std_y = df.y.std(delay=True)
sum_z = df.z.sum(delay=True)

# 一次性执行所有操作
results = vaex.execute([mean_x, std_y, sum_z])
```

### 模式：用于特征工程的虚拟列
```python
# 无内存开销 - 即时计算
df['age_squared'] = df.age ** 2
df['full_name'] = df.first_name + ' ' + df.last_name
df['is_adult'] = df.age >= 18
```

## 资源

此技能在`references/`目录中包含参考文档：

- `core_dataframes.md` - DataFrame创建、加载和基本结构
- `data_processing.md` - 过滤、表达式、聚合和转换
- `performance.md` - 优化策略和延迟评估
- `visualization.md` - 绘图和交互式可视化
- `machine_learning.md` - ML管道和模型集成
- `io_operations.md` - 文件格式和数据导入/导出