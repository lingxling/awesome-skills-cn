---
name: dask
description: 用于大于内存的 pandas/NumPy 工作流的分布式计算。当需要将现有的 pandas/NumPy 代码扩展到超出内存范围或跨集群时使用。最适合并行文件处理、分布式机器学习、与现有 pandas 代码集成。对于单机上的核外分析使用 vaex；对于内存速度使用 polars。
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# Dask

## 概述

Dask 是一个用于并行和分布式计算的 Python 库，它提供了三个关键能力：
- **大于内存的执行**，用于在单台机器上处理超过可用 RAM 的数据
- **并行处理**，通过多个核心提高计算速度
- **分布式计算**，支持跨多台机器的太字节级数据集

Dask 可以从笔记本电脑（处理约 100 GiB）扩展到集群（处理约 100 TiB），同时保持熟悉的 Python API。

## 何时使用此技能

此技能应在以下情况下使用：
- 处理超过可用 RAM 的数据集
- 将 pandas 或 NumPy 操作扩展到更大的数据集
- 并行化计算以提高性能
- 高效处理多个文件（CSV、Parquet、JSON、文本日志）
- 使用任务依赖关系构建自定义并行工作流
- 跨多个核心或机器分发工作负载

## 核心能力

Dask 提供五个主要组件，每个组件适用于不同的用例：

### 1. DataFrames - 并行 Pandas 操作

**用途**：通过并行处理将 pandas 操作扩展到更大的数据集。

**何时使用**：
- 表格数据超过可用 RAM
- 需要一起处理多个 CSV/Parquet 文件
- Pandas 操作缓慢且需要并行化
- 从 pandas 原型扩展到生产环境

**参考文档**：有关 Dask DataFrames 的综合指南，请参阅 `references/dataframes.md`，其中包括：
- 读取数据（单个文件、多个文件、glob 模式）
- 常见操作（过滤、groupby、连接、聚合）
- 使用 `map_partitions` 的自定义操作
- 性能优化技巧
- 常见模式（ETL、时间序列、多文件处理）

**快速示例**：
```python
import dask.dataframe as dd

# 将多个文件读取为单个 DataFrame
ddf = dd.read_csv('data/2024-*.csv')

# 操作是惰性的，直到调用 compute()
filtered = ddf[ddf['value'] > 100]
result = filtered.groupby('category').mean().compute()
```

**关键点**：
- 操作是惰性的（构建任务图），直到调用 `.compute()`
- 使用 `map_partitions` 进行高效的自定义操作
- 从其他来源处理结构化数据时，尽早转换为 DataFrame

### 2. Arrays - 并行 NumPy 操作

**用途**：使用分块算法将 NumPy 功能扩展到大于内存的数据集。

**何时使用**：
- 数组超过可用 RAM
- NumPy 操作需要并行化
- 处理科学数据集（HDF5、Zarr、NetCDF）
- 需要并行线性代数或数组操作

**参考文档**：有关 Dask Arrays 的综合指南，请参阅 `references/arrays.md`，其中包括：
- 创建数组（从 NumPy、随机、磁盘）
- 分块策略和优化
- 常见操作（算术、归约、线性代数）
- 使用 `map_blocks` 的自定义操作
- 与 HDF5、Zarr 和 XArray 集成

**快速示例**：
```python
import dask.array as da

# 创建带分块的大型数组
x = da.random.random((100000, 100000), chunks=(10000, 10000))

# 操作是惰性的
y = x + 100
z = y.mean(axis=0)

# 计算结果
result = z.compute()
```

**关键点**：
- 分块大小至关重要（每个分块约 100 MB）
- 操作在分块上并行执行
- 需要时重新分块数据以实现高效操作
- 使用 `map_blocks` 处理 Dask 中不可用的操作

### 3. Bags - 非结构化数据的并行处理

**用途**：使用函数操作处理非结构化或半结构化数据（文本、JSON、日志）。

**何时使用**：
- 处理文本文件、日志或 JSON 记录
- 结构化分析之前的数据清理和 ETL
- 处理不符合数组/dataframe 格式的 Python 对象
- 需要内存高效的流式处理

**参考文档**：有关 Dask Bags 的综合指南，请参阅 `references/bags.md`，其中包括：
- 读取文本和 JSON 文件
- 函数操作（map、filter、fold、groupby）
- 转换为 DataFrames
- 常见模式（日志分析、JSON 处理、文本处理）
- 性能考虑

**快速示例**：
```python
import dask.bag as db
import json

# 读取并解析 JSON 文件
bag = db.read_text('logs/*.json').map(json.loads)

# 过滤和转换
valid = bag.filter(lambda x: x['status'] == 'valid')
processed = valid.map(lambda x: {'id': x['id'], 'value': x['value']})

# 转换为 DataFrame 进行分析
ddf = processed.to_dataframe()
```

**关键点**：
- 用于初始数据清理，然后转换为 DataFrame/Array
- 使用 `foldby` 而不是 `groupby` 以获得更好的性能
- 操作是流式的且内存高效
- 转换为结构化格式（DataFrame）以进行复杂操作

### 4. Futures - 基于任务的并行化

**用途**：构建自定义并行工作流，对任务执行和依赖关系进行细粒度控制。

**何时使用**：
- 构建动态、演进的工作流
- 需要立即执行任务（非惰性）
- 计算依赖于运行时条件
- 实现自定义并行算法
- 需要有状态的计算

**参考文档**：有关 Dask Futures 的综合指南，请参阅 `references/futures.md`，其中包括：
- 设置分布式客户端
- 提交任务和使用 futures
- 任务依赖关系和数据移动
- 高级协调（队列、锁、事件、参与者）
- 常见模式（参数扫描、动态任务、迭代算法）

**快速示例**：
```python
from dask.distributed import Client

client = Client()  # 创建本地集群

# 提交任务（立即执行）
def process(x):
    return x ** 2

futures = client.map(process, range(100))

# 收集结果
results = client.gather(futures)

client.close()
```

**关键点**：
- 需要分布式客户端（即使是单台机器）
- 任务在提交时立即执行
- 预先分散大数据以避免重复传输
- 每个任务约 1ms 开销（不适合数百万个微小任务）
- 使用参与者进行有状态的工作流

### 5. Schedulers - 执行后端

**用途**：控制 Dask 任务的执行方式和位置（线程、进程、分布式）。

**何时选择调度器**：
- **线程**（默认）：NumPy/Pandas 操作、释放 GIL 的库、共享内存受益
- **进程**：纯 Python 代码、文本处理、受 GIL 限制的操作
- **同步**：使用 pdb 调试、性能分析、理解错误
- **分布式**：需要仪表板、多机器集群、高级功能

**参考文档**：有关 Dask Schedulers 的综合指南，请参阅 `references/schedulers.md`，其中包括：
- 详细的调度器描述和特征
- 配置方法（全局、上下文管理器、每次计算）
- 性能考虑和开销
- 常见模式和故障排除
- 线程配置以获得最佳性能

**快速示例**：
```python
import dask
import dask.dataframe as dd

# 使用线程处理 DataFrame（默认，适合数值计算）
ddf = dd.read_csv('data.csv')
result1 = ddf.mean().compute()  # 使用线程

# 使用进程处理繁重的 Python 工作
import dask.bag as db
bag = db.read_text('logs/*.txt')
result2 = bag.map(python_function).compute(scheduler='processes')

# 使用同步进行调试
dask.config.set(scheduler='synchronous')
result3 = problematic_computation.compute()  # 可以使用 pdb

# 使用分布式进行监控和扩展
from dask.distributed import Client
client = Client()
result4 = computation.compute()  # 使用带有仪表板的分布式
```

**关键点**：
- 线程：最低开销（约 10 µs/任务），最适合数值工作
- 进程：避免 GIL（约 10 ms/任务），最适合 Python 工作
- 分布式：监控仪表板（约 1 ms/任务），扩展到集群
- 可以按计算或全局切换调度器

## 最佳实践

有关全面的性能优化指南、内存管理策略和要避免的常见陷阱，请参阅 `references/best-practices.md`。关键原则包括：

### 从更简单的解决方案开始

在使用 Dask 之前，探索：
- 更好的算法
- 高效的文件格式（Parquet 而不是 CSV）
- 编译代码（Numba、Cython）
- 数据采样

### 关键性能规则

**1. 不要在本地加载数据然后交给 Dask**
```python
# 错误：首先将所有数据加载到内存中
import pandas as pd
df = pd.read_csv('large.csv')
ddf = dd.from_pandas(df, npartitions=10)

# 正确：让 Dask 处理加载
import dask.dataframe as dd
ddf = dd.read_csv('large.csv')
```

**2. 避免重复的 compute() 调用**
```python
# 错误：每次 compute 都是独立的
for item in items:
    result = dask_computation(item).compute()

# 正确：所有操作的单一 compute
computations = [dask_computation(item) for item in items]
results = dask.compute(*computations)
```

**3. 不要构建过大的任务图**
- 如果有数百万个任务，增加分块大小
- 使用 `map_partitions`/`map_blocks` 融合操作
- 检查任务图大小：`len(ddf.__dask_graph__())`

**4. 选择适当的分块大小**
- 目标：每个分块约 100 MB（或 worker 内存中每个核心 10 个分块）
- 太大：内存溢出
- 太小：调度开销

**5. 使用仪表板**
```python
from dask.distributed import Client
client = Client()
print(client.dashboard_link)  # 监控性能，识别瓶颈
```

## 常见工作流模式

### ETL 管道
```python
import dask.dataframe as dd

# 提取：读取数据
ddf = dd.read_csv('raw_data/*.csv')

# 转换：清理和处理
ddf = ddf[ddf['status'] == 'valid']
ddf['amount'] = ddf['amount'].astype('float64')
ddf = ddf.dropna(subset=['important_col'])

# 加载：聚合和保存
summary = ddf.groupby('category').agg({'amount': ['sum', 'mean']})
summary.to_parquet('output/summary.parquet')
```

### 非结构化到结构化管道路径
```python
import dask.bag as db
import json

# 从 Bag 开始处理非结构化数据
bag = db.read_text('logs/*.json').map(json.loads)
bag = bag.filter(lambda x: x['status'] == 'valid')

# 转换为 DataFrame 进行结构化分析
ddf = bag.to_dataframe()
result = ddf.groupby('category').mean().compute()
```

### 大规模数组计算
```python
import dask.array as da

# 加载或创建大型数组
x = da.from_zarr('large_dataset.zarr')

# 分块处理
normalized = (x - x.mean()) / x.std()

# 保存结果
da.to_zarr(normalized, 'normalized.zarr')
```

### 自定义并行工作流
```python
from dask.distributed import Client

client = Client()

# 一次分散大型数据集
data = client.scatter(large_dataset)

# 带依赖关系的并行处理
futures = []
for param in parameters:
    future = client.submit(process, data, param)
    futures.append(future)

# 收集结果
results = client.gather(futures)
```

## 选择正确的组件

使用此决策指南选择适当的 Dask 组件：

**数据类型**：
- 表格数据 → **DataFrames**
- 数值数组 → **Arrays**
- 文本/JSON/日志 → **Bags**（然后转换为 DataFrame）
- 自定义 Python 对象 → **Bags** 或 **Futures**

**操作类型**：
- 标准 pandas 操作 → **DataFrames**
- 标准 NumPy 操作 → **Arrays**
- 自定义并行任务 → **Futures**
- 文本处理/ETL → **Bags**

**控制级别**：
- 高级、自动 → **DataFrames/Arrays**
- 低级、手动 → **Futures**

**工作流类型**：
- 静态计算图 → **DataFrames/Arrays/Bags**
- 动态、演进 → **Futures**

## 集成考虑

### 文件格式
- **高效**：Parquet、HDF5、Zarr（列式、压缩、并行友好）
- **兼容但较慢**：CSV（仅用于初始摄取）
- **对于数组**：HDF5、Zarr、NetCDF

### 集合之间的转换
```python
# Bag → DataFrame
ddf = bag.to_dataframe()

# DataFrame → Array（对于数值数据）
arr = ddf.to_dask_array(lengths=True)

# Array → DataFrame
ddf = dd.from_dask_array(arr, columns=['col1', 'col2'])
```

### 与其他库集成
- **XArray**：用标记维度包装 Dask 数组（地理空间、成像）
- **Dask-ML**：使用与 scikit-learn 兼容的 API 进行机器学习
- **Distributed**：高级集群管理和监控

## 调试和开发

### 迭代开发工作流

1. **使用同步调度器在小数据上测试**：
```python
dask.config.set(scheduler='synchronous')
result = computation.compute()  # 可以使用 pdb，易于调试
```

2. **在线本上使用线程进行验证**：
```python
sample = ddf.head(1000)  # 小样本
# 测试逻辑，然后扩展到完整数据集
```

3. **使用分布式进行监控和扩展**：
```python
from dask.distributed import Client
client = Client()
print(client.dashboard_link)  # 监控性能
result = computation.compute()
```

### 常见问题

**内存错误**：
- 减小分块大小
- 策略性地使用 `persist()` 并在完成后删除
- 检查自定义函数中的内存泄漏

**启动缓慢**：
- 任务图太大（增加分块大小）
- 使用 `map_partitions` 或 `map_blocks` 减少任务

**并行化不良**：
- 分块太大（增加分区数）
- 对 Python 代码使用线程（切换到进程）
- 数据依赖关系阻止并行化

## 参考文件

所有参考文档文件可根据需要读取以获取详细信息：

- `references/dataframes.md` - 完整的 Dask DataFrame 指南
- `references/arrays.md` - 完整的 Dask Array 指南
- `references/bags.md` - 完整的 Dask Bag 指南
- `references/futures.md` - 完整的 Dask Futures 和分布式计算指南
- `references/schedulers.md` - 完整的调度器选择和配置指南
- `references/best-practices.md` - 全面的性能优化和故障排除

当用户需要有关特定 Dask 组件、操作或模式的详细信息时，请加载这些文件。
