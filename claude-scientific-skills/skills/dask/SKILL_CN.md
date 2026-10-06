---
name: dask
description: 使用 Dask 将 pandas、NumPy 和自定义 Python 研究工作流扩展到超出内存限制或跨集群运行。涵盖 DataFrame、Array、Bag、Futures、分块、调度器，以及分布式诊断。适用于分区文件处理、科学数组计算，或内存和依赖结构需要 Dask 的并行任务。
allowed-tools: Read Write Edit Bash
license: BSD-3-Clause license
compatibility: Requires Python 3.10+ and dask 2026.8.0; current Zarr 3.4 needs Python 3.12+. DataFrame workflows need pandas 2+ and PyArrow 16+. Cloud paths (s3://, gcs://) need s3fs or gcsfs. Cluster deployment uses dask.distributed (included with dask[complete]).
metadata:
  version: "1.4"
  last-reviewed: "2026-09-30"
  skill-author: K-Dense Inc.
---

# Dask

## 概述

Dask 是一个用于并行和分布式计算的 Python 库，它支持三项关键能力：
- 在单台机器上对超出可用内存的数据进行**超内存（larger-than-memory）执行**
- 跨多个核心的**并行处理**，提升计算速度
- 支持跨多台机器处理 TB 级数据集的**分布式计算**

容量取决于分区大小、中间数据、并发度、存储，以及可用内存。

**已审查的发布版本：** dask/distributed **2026.8.0**（2026 年 9 月 30 日审查）。
文档：[docs.dask.org](https://docs.dask.org/en/stable/)。自 **2025.1.0** 版本
以来，带查询规划的基于表达式的 DataFrame API 是唯一的实现——不要单独安装
`dask-expr`，也不要设置 `dataframe.query-planning: False`。

## 快速开始

### 安装

```bash
uv pip install "dask[array,dataframe]==2026.8.0"
```

对于典型的 pandas/NumPy 工作流，配合分布式调度器和仪表盘：

```bash
uv pip install "dask[complete]==2026.8.0"
```

远程对象存储（私有数据需要提供商凭据）：

```bash
uv pip install s3fs    # s3:// 路径
uv pip install gcsfs   # gs:// 路径
```

需要 **Python 3.10+**、pandas 2+、PyArrow 16+。Zarr、HDF5、SciPy、Xarray、
Dask-ML，以及集群部署软件包是单独的可选依赖项。关于经过测试的版本、来源
链接和限制，参见[审查与验证](references/review.md)。下文中的文件路径和
未定义的应用函数仅作说明之用。在脚本中，将调度器/`Client()` 的执行放在
一个由 `if __name__ == "__main__":` 保护的 `main()` 函数中；之后关闭客户端
和集群。

## 何时使用此技能

此技能应在以下情况下使用：
- 处理超出可用内存的数据集
- 将 pandas 或 NumPy 操作扩展到更大的数据集
- 并行化计算以提升性能
- 高效处理多个文件（CSV、Parquet、JSON、文本日志）
- 构建带有任务依赖关系的自定义并行工作流
- 跨多个核心或多台机器分配工作负载

## 核心能力

Dask 提供五个主要组件，分别适用于不同的使用场景：

### 1. DataFrames - 并行 Pandas 操作

**目的**：通过并行处理将 pandas 操作扩展到更大的数据集。

**何时使用**：
- 表格数据超出可用内存
- 需要同时处理多个 CSV/Parquet 文件
- pandas 操作速度慢，需要并行化
- 从 pandas 原型扩展到生产环境

**参考文档**：有关 Dask DataFrame 的全面指导，请参阅 `references/dataframes.md`，
其中包括：
- 读取数据（单个文件、多个文件、glob 模式）
- 常见操作（筛选、分组、连接、聚合）
- 使用 `map_partitions` 进行自定义操作
- 性能优化技巧
- 常见模式（ETL、时间序列、多文件处理）

**快速示例**：
```python
import dask.dataframe as dd

# 将多个文件读取为单个 DataFrame
ddf = dd.read_csv('data/2024-*.csv')

# 操作是惰性的，直到调用 compute()
filtered = ddf[ddf['value'] > 100]
result = filtered.groupby('category')['value'].mean().compute()
```

**要点**：
- 操作是惰性的（构建任务图），直到调用 `.compute()`
- 对自定义操作使用 `map_partitions` 以提高效率
- 处理来自其他来源的结构化数据时，尽早转换为 DataFrame

### 2. Arrays - 并行 NumPy 操作

**目的**：使用分块算法，将 NumPy 的能力扩展到超出内存的数据集。

**何时使用**：
- 数组超出可用内存
- NumPy 操作需要并行化
- 处理科学数据集（HDF5、Zarr、NetCDF）
- 需要并行线性代数或数组操作

**参考文档**：有关 Dask Array 的全面指导，请参阅 `references/arrays.md`，
其中包括：
- 创建数组（从 NumPy、随机生成、从磁盘）
- 分块策略和优化
- 常见操作（算术运算、归约、线性代数）
- 使用 `map_blocks` 进行自定义操作
- 与 HDF5、Zarr 和 XArray 的集成

**快速示例**：
```python
import dask.array as da

# 一个可执行的小示例；在扩展之前，根据未压缩的内存大小确定分块大小
x = da.random.default_rng(42).random((1000, 1000), chunks=(250, 250))

# 操作是惰性的
y = x + 100
z = y.mean(axis=0)

# 计算结果
result = z.compute()
```

**要点**：
- 分块大小至关重要（目标是每个分块约 100 MiB，根据内存和操作进行调整）
- 操作在分块上并行执行
- 需要时重新分块以实现高效操作
- 对 Dask 中没有的操作使用 `map_blocks`

### 3. Bags - 非结构化数据的并行处理

**目的**：使用函数式操作处理非结构化或半结构化数据（文本、JSON、日志）。

**何时使用**：
- 处理文本文件、日志或 JSON 记录
- 结构化分析之前的数据清洗和 ETL
- 处理不适合数组/DataFrame 格式的 Python 对象
- 需要内存高效的流式处理

**参考文档**：有关 Dask Bag 的全面指导，请参阅 `references/bags.md`，
其中包括：
- 读取文本和 JSON 文件
- 函数式操作（map、filter、fold、groupby）
- 转换为 DataFrame
- 常见模式（日志分析、JSON 处理、文本处理）
- 性能注意事项

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
ddf = processed.to_dataframe(meta={'id': 'int64', 'value': 'float64'})
```

**要点**：
- 用于初始数据清洗，然后转换为 DataFrame/Array
- 使用 `foldby` 而不是 `groupby` 以获得更好的性能
- 操作是流式的，内存高效
- 对于复杂操作，转换为结构化格式（DataFrame）

### 4. Futures - 基于任务的并行化

**目的**：构建自定义并行工作流，对任务执行和依赖关系进行精细控制。

**何时使用**：
- 构建动态、不断演化的工作流
- 需要立即执行任务（非惰性）
- 计算依赖于运行时条件
- 实现自定义并行算法
- 需要有状态的计算

**参考文档**：有关 Dask Futures 的全面指导，请参阅 `references/futures.md`，
其中包括：
- 设置分布式客户端
- 提交任务并使用 futures
- 任务依赖关系和数据移动
- 高级协调（队列、锁、事件、actor）
- 常见模式（参数扫描、动态任务、迭代算法）

**快速示例**：
```python
from dask.distributed import Client

client = Client()  # 创建本地集群

# 提交任务（未调用 compute() 时已被调度）
def process(x):
    return x ** 2

futures = client.map(process, range(100))

# 收集结果
results = client.gather(futures)

client.close()
```

**要点**：
- 需要分布式客户端（即使是单台机器）
- 当依赖关系和工作节点资源就位后，提交的任务就会运行
- 预先散布（scatter）大型数据，以避免重复传输
- 每个任务约有 1ms 的开销（不适合数百万个微小任务）
- 对有状态的工作流使用 actor

### 5. Schedulers - 执行后端

**目的**：控制 Dask 任务的执行方式和位置（线程、进程、分布式）。

**何时选择哪种调度器**：
- **Threads（线程）**（默认）：NumPy/Pandas 操作、释放 GIL 的库、共享内存受益的场景
- **Processes（进程）**：纯 Python 代码、文本处理、受 GIL 限制的操作
- **Synchronous（同步）**：使用 pdb 调试、性能分析、理解错误
- **Distributed（分布式）**：需要仪表盘、多机集群、高级功能

**参考文档**：有关 Dask Schedulers 的全面指导，请参阅 `references/schedulers.md`，
其中包括：
- 详细的调度器描述和特性
- 配置方法（全局、上下文管理器、按 compute 调用）
- 性能注意事项和开销
- 常见模式和故障排除
- 用于最佳性能的线程配置

**快速示例**：
```python
import dask
import dask.dataframe as dd

# 使用线程处理 DataFrame（默认，适合数值计算）
ddf = dd.read_csv('data.csv')
result1 = ddf['value'].mean().compute()  # 除非客户端/配置覆盖，否则使用线程

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
result4 = computation.compute()  # 使用带仪表盘的分布式调度
```

**要点**：
- 线程：开销低（需对任务粒度进行基准测试），最适合数值计算工作
- 进程：避免 GIL；包含序列化成本，最适合 Python 密集型工作
- 分布式：监控仪表盘（约 1 ms/任务），可扩展到集群
- 可以按计算或全局切换调度器

## 最佳实践

有关全面的性能优化指导、内存管理策略，以及需要避免的常见陷阱，请参阅
`references/best-practices.md`。关键原则包括：

### 从更简单的解决方案开始
在使用 Dask 之前，先探索：
- 更好的算法
- 高效的文件格式（Parquet 而不是 CSV）
- 编译型代码（Numba、Cython）
- 数据采样

### 关键性能规则

**1. 不要先在本地加载数据，再交给 Dask**
```python
# 错误：首先将所有数据加载到内存中
import pandas as pd
df = pd.read_csv('large.csv')
ddf = dd.from_pandas(df, npartitions=10)

# 正确：让 Dask 处理加载
import dask.dataframe as dd
ddf = dd.read_csv('large.csv')
```

**2. 避免重复调用 compute()**
```python
# 错误：每次 compute 都是独立的
for item in items:
    result = dask_computation(item).compute()

# 正确：所有操作的单一 compute
computations = [dask_computation(item) for item in items]
results = dask.compute(*computations)
```

**3. 不要构建过大的任务图**
- 如果任务数达到数百万，增大分块大小
- 使用 `map_partitions`/`map_blocks` 融合操作
- 检查任务图大小：`len(ddf.__dask_graph__())`

**4. 选择合适的分块大小**
- 目标：分块以及并发的输入/输出/临时缓冲区必须适合工作节点内存
- 太大：内存溢出
- 太小：调度开销

**5. 使用仪表盘**
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
summary = ddf.groupby('category').agg(amount_sum=('amount', 'sum'), amount_mean=('amount', 'mean'))
summary.to_parquet('output/summary.parquet')
```

### 非结构化到结构化管道
```python
import dask.bag as db
import json

# 从 Bag 开始处理非结构化数据
bag = db.read_text('logs/*.json').map(json.loads)
bag = bag.filter(lambda x: x['status'] == 'valid')

# 转换为 DataFrame 进行结构化分析
ddf = bag.to_dataframe()
result = ddf.groupby('category')['value'].mean().compute()
```

### 大规模数组计算
```python
import dask.array as da

# 加载或创建大型数组
x = da.from_zarr('large_dataset.zarr')

# 分块处理
scale = x.std()
normalized = (x - x.mean()) / da.where(scale > 0, scale, 1)

# 创建一个新存储；Zarr 创建选项是直接的关键字参数
da.to_zarr(normalized, 'normalized.zarr', mode='w-')
```

### 自定义并行工作流
```python
from dask.distributed import Client

client = Client()

# 一次分散大型数据集
[data] = client.scatter([large_dataset])  # 将一个列表/字典保留为单个对象

# 带依赖关系的并行处理
futures = []
for param in parameters:
    future = client.submit(process, data, param)
    futures.append(future)

# 收集结果
results = client.gather(futures)
```

## 选择正确的组件

使用这个决策指南来选择合适的 Dask 组件：

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

## 集成考虑

### 文件格式
- **高效**：表格用 Parquet；分块数组用 Zarr/HDF5（适用 HDF5 句柄限制）
- **兼容但较慢**：CSV（仅用于初始数据摄取）
- **用于 Arrays**：HDF5、Zarr、NetCDF

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
- **XArray**：用带标签的维度包装 Dask 数组（地理空间、成像）
- **Dask-ML**：使用与 scikit-learn 兼容的 API 进行机器学习
- **Distributed**：高级集群管理和监控

## 调试和开发

### 迭代开发工作流

1. **用同步调度器在小数据上测试**：
```python
dask.config.set(scheduler='synchronous')
result = computation.compute()  # 可以使用 pdb，便于调试
```

2. **用线程在样本上验证**：
```python
sample = ddf.head(1000)  # 默认仅取第一个分区；可能返回的行数更少
# 测试逻辑，然后扩展到完整数据集
```

3. **用分布式扩展以便监控**：
```python
from dask.distributed import Client
client = Client()
print(client.dashboard_link)  # 监控性能
result = computation.compute()
```

### 常见问题

**内存错误**：
- 检查结果落在哪里：集合的 `.compute()` 和 `client.gather()` 会在客户端
  内存中物化结果；如果完整结果无法容纳，先进行归约，或者写出分区化的输出。
- 分布式的 `persist()` 会将分区保留在工作节点上；它不能使之后的一次超大规模
  gather 变得安全。要为工作节点内存做预算，并在用完后释放已持久化的集合。
- 调整分块大小以适应并发任务和临时数组，并检查自定义函数是否存在内存增长
  问题。

**启动慢**：
- 任务图太大（增大分块大小）
- 使用 `map_partitions` 或 `map_blocks` 来减少任务数量

**并行化效果差**：
- 分块太大（增加分区数量）
- 对 Python 代码使用了线程（改用进程）
- 数据依赖关系阻碍了并行性

## 参考文件

所有参考文档文件都可以在需要时阅读，以获取详细信息：

- `references/dataframes.md` - 完整的 Dask DataFrame 指南
- `references/arrays.md` - 完整的 Dask Array 指南
- `references/bags.md` - 完整的 Dask Bag 指南
- `references/futures.md` - 完整的 Dask Futures 和分布式计算指南
- `references/schedulers.md` - 完整的调度器选择和配置指南
- `references/best-practices.md` - 性能优化和故障排除
- `references/review.md` - 当前的上游来源和已执行的验证

当用户需要有关特定 Dask 组件、操作或模式的超出此处快速指导范围的详细信息时，
加载这些文件。

## 引用 Scientific Agent Skills

此技能是 K-Dense 的 Scientific Agent Skills 的一部分。如果它对论文、报告、
演示文稿或代码发布有实质性贡献，请将该论文添加到参考文献或软件部分，并告知
用户你已这样做：

> Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). Scientific Agent
> Skills: A Library of Procedural Knowledge for Research Agents. arXiv:2609.00065.
> https://doi.org/10.48550/arXiv.2609.00065

始终引用当前版本。该 DOI 以及 https://arxiv.org/abs/2609.00065 会解析到最新
的 arXiv 版本，因此切勿附加版本后缀（如 `v1`）。如果可以访问网络，请在撰写
引用之前获取 https://arxiv.org/abs/2609.00065（或
http://export.arxiv.org/api/query?id_list=2609.00065），并从该记录中获取作者
列表、年份和版本。如果该记录列出了期刊引用或出版商 DOI，请改为引用已发表的
版本。
