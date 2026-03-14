---
name: zarr-python
description: 用于云存储的分块N维数组。压缩数组、并行I/O、S3/GCS集成、NumPy/Dask/Xarray兼容，适用于大规模科学计算管道。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# Zarr Python

## 概述

Zarr是一个Python库，用于存储带有分块和压缩的大型N维数组。应用此技能可实现高效并行I/O、云原生工作流，以及与NumPy、Dask和Xarray的无缝集成。

## 快速开始

### 安装

```bash
uv pip install zarr
```

需要Python 3.11+。对于云存储支持，安装额外的包：
```python
uv pip install s3fs  # 用于S3
uv pip install gcsfs  # 用于Google Cloud Storage
```

### 基本数组创建

```python
import zarr
import numpy as np

# 创建带有分块和压缩的2D数组
z = zarr.create_array(
    store="data/my_array.zarr",
    shape=(10000, 10000),
    chunks=(1000, 1000),
    dtype="f4"
)

# 使用NumPy风格索引写入数据
z[:, :] = np.random.random((10000, 10000))

# 读取数据
data = z[0:100, 0:100]  # 返回NumPy数组
```

## 核心操作

### 创建数组

Zarr提供多个方便的数组创建函数：

```python
# 创建空数组
z = zarr.zeros(shape=(10000, 10000), chunks=(1000, 1000), dtype='f4',
               store='data.zarr')

# 创建填充数组
z = zarr.ones((5000, 5000), chunks=(500, 500))
z = zarr.full((1000, 1000), fill_value=42, chunks=(100, 100))

# 从现有数据创建
data = np.arange(10000).reshape(100, 100)
z = zarr.array(data, chunks=(10, 10), store='data.zarr')

# 创建与另一个数组相似的数组
z2 = zarr.zeros_like(z)  # 匹配z的形状、分块和数据类型
```

### 打开现有数组

```python
# 打开数组（默认为读写模式）
z = zarr.open_array('data.zarr', mode='r+')

# 只读模式
z = zarr.open_array('data.zarr', mode='r')

# open()函数自动检测数组与组
z = zarr.open('data.zarr')  # 返回Array或Group
```

### 读写数据

Zarr数组支持NumPy风格索引：

```python
# 写入整个数组
z[:] = 42

# 写入切片
z[0, :] = np.arange(100)
z[10:20, 50:60] = np.random.random((10, 10))

# 读取数据（返回NumPy数组）
data = z[0:100, 0:100]
row = z[5, :]

# 高级索引
z.vindex[[0, 5, 10], [2, 8, 15]]  # 坐标索引
z.oindex[0:10, [5, 10, 15]]       # 正交索引
z.blocks[0, 0]                     # 块/分块索引
```

### 调整大小和追加

```python
# 调整数组大小
z.resize(15000, 15000)  # 扩展或缩小维度

# 沿轴追加数据
z.append(np.random.random((1000, 10000)), axis=0)  # 添加行
```

## 分块策略

分块对性能至关重要。根据访问模式选择分块大小和形状。

### 分块大小指南

- **最小分块大小**：推荐1 MB以获得最佳性能
- **平衡**：较大的分块 = 较少的元数据操作；较小的分块 = 更好的并行访问
- **内存考虑**：压缩期间整个分块必须适合内存

```python
# 配置分块大小（目标为每个分块~1MB）
# 对于float32数据：1MB = 262,144个元素 = 512×512数组
z = zarr.zeros(
    shape=(10000, 10000),
    chunks=(512, 512),  # ~1MB分块
    dtype='f4'
)
```

### 使分块与访问模式对齐

**关键**：分块形状根据数据访问方式显著影响性能。

```python
# 如果频繁访问行（第一维度）
z = zarr.zeros((10000, 10000), chunks=(10, 10000))  # 分块跨越列

# 如果频繁访问列（第二维度）
z = zarr.zeros((10000, 10000), chunks=(10000, 10))  # 分块跨越行

# 对于混合访问模式（平衡方法）
z = zarr.zeros((10000, 10000), chunks=(1000, 1000))  # 方形分块
```

**性能示例**：对于(200, 200, 200)数组，沿第一维度读取：
- 使用分块(1, 200, 200)：~107ms
- 使用分块(200, 200, 1)：~1.65ms（快65倍！）

### 大规模存储的分片

当数组有数百万个小分块时，使用分片将分块分组为更大的存储对象：

```python
from zarr.codecs import ShardingCodec, BytesCodec
from zarr.codecs.blosc import BloscCodec

# 创建带分片的数组
z = zarr.create_array(
    store='data.zarr',
    shape=(100000, 100000),
    chunks=(100, 100),  # 小分块用于访问
    shards=(1000, 1000),  # 每个分片组100个分块
    dtype='f4'
)
```

**好处**：
- 减少来自数百万小文件的文件系统开销
- 提高云存储性能（减少对象请求）
- 防止文件系统块大小浪费

**重要**：写入前整个分片必须适合内存。

## 压缩

Zarr按分块应用压缩以减少存储同时保持快速访问。

### 配置压缩

```python
from zarr.codecs.blosc import BloscCodec
from zarr.codecs import GzipCodec, ZstdCodec

# 默认：Blosc与Zstandard
z = zarr.zeros((1000, 1000), chunks=(100, 100))  # 使用默认压缩

# 配置Blosc编解码器
z = zarr.create_array(
    store='data.zarr',
    shape=(1000, 1000),
    chunks=(100, 100),
    dtype='f4',
    codecs=[BloscCodec(cname='zstd', clevel=5, shuffle='shuffle')]
)

# 可用的Blosc压缩器：'blosclz', 'lz4', 'lz4hc', 'snappy', 'zlib', 'zstd'

# 使用Gzip压缩
z = zarr.create_array(
    store='data.zarr',
    shape=(1000, 1000),
    chunks=(100, 100),
    dtype='f4',
    codecs=[GzipCodec(level=6)]
)

# 禁用压缩
z = zarr.create_array(
    store='data.zarr',
    shape=(1000, 1000),
    chunks=(100, 100),
    dtype='f4',
    codecs=[BytesCodec()]  # 无压缩
)
```

### 压缩性能提示

- **Blosc**（默认）：快速压缩/解压缩，适合交互式工作负载
- **Zstandard**：更好的压缩率，比LZ4稍慢
- **Gzip**：最大压缩，性能较慢
- **LZ4**：最快压缩，较低压缩率
- **Shuffle**：对数值数据启用shuffle过滤器以获得更好的压缩

```python
# 对数值科学数据最佳
codecs=[BloscCodec(cname='zstd', clevel=5, shuffle='shuffle')]

# 对速度最佳
codecs=[BloscCodec(cname='lz4', clevel=1)]

# 对压缩率最佳
codecs=[GzipCodec(level=9)]
```

## 存储后端

Zarr通过灵活的存储接口支持多种存储后端。

### 本地文件系统（默认）

```python
from zarr.storage import LocalStore

# 显式创建存储
store = LocalStore('data/my_array.zarr')
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))

# 或使用字符串路径（自动创建LocalStore）
z = zarr.open_array('data/my_array.zarr', mode='w', shape=(1000, 1000),
                    chunks=(100, 100))
```

### 内存存储

```python
from zarr.storage import MemoryStore

# 创建内存存储
store = MemoryStore()
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))

# 数据仅存在于内存中，不持久化
```

### ZIP文件存储

```python
from zarr.storage import ZipStore

# 写入ZIP文件
store = ZipStore('data.zip', mode='w')
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))
z[:] = np.random.random((1000, 1000))
store.close()  # 重要：必须关闭ZipStore

# 从ZIP文件读取
store = ZipStore('data.zip', mode='r')
z = zarr.open_array(store=store)
data = z[:]
store.close()
```

### 云存储（S3, GCS）

```python
import s3fs
import zarr

# S3存储
s3 = s3fs.S3FileSystem(anon=False)  # 使用凭证
store = s3fs.S3Map(root='my-bucket/path/to/array.zarr', s3=s3)
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))
z[:] = data

# Google Cloud Storage
import gcsfs
gcs = gcsfs.GCSFileSystem(project='my-project')
store = gcsfs.GCSMap(root='my-bucket/path/to/array.zarr', gcs=gcs)
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))
```

**云存储最佳实践**：
- 使用合并元数据减少延迟：`zarr.consolidate_metadata(store)`
- 将分块大小与云对象大小对齐（通常5-100 MB最佳）
- 使用Dask进行大规模数据的并行写入
- 考虑使用分片减少对象数量

## 组和层次结构

组以层次结构组织多个数组，类似于目录或HDF5组。

### 创建和使用组

```python
# 创建根组
root = zarr.group(store='data/hierarchy.zarr')

# 创建子组
temperature = root.create_group('temperature')
precipitation = root.create_group('precipitation')

# 在组内创建数组
temp_array = temperature.create_array(
    name='t2m',
    shape=(365, 720, 1440),
    chunks=(1, 720, 1440),
    dtype='f4'
)

precip_array = precipitation.create_array(
    name='prcp',
    shape=(365, 720, 1440),
    chunks=(1, 720, 1440),
    dtype='f4'
)

# 使用路径访问
array = root['temperature/t2m']

# 可视化层次结构
print(root.tree())
# 输出：
# /
#  ├── temperature
#  │   └── t2m (365, 720, 1440) f4
#  └── precipitation
#      └── prcp (365, 720, 1440) f4
```

### 兼容H5py的API

Zarr为熟悉HDF5的用户提供h5py兼容接口：

```python
# 使用h5py风格方法创建组
root = zarr.group('data.zarr')
dataset = root.create_dataset('my_data', shape=(1000, 1000), chunks=(100, 100),
                              dtype='f4')

# 像h5py一样访问
grp = root.require_group('subgroup')
arr = grp.require_dataset('array', shape=(500, 500), chunks=(50, 50), dtype='i4')
```

## 属性和元数据

使用属性将自定义元数据附加到数组和组：

```python
# 向数组添加属性
z = zarr.zeros((1000, 1000), chunks=(100, 100))
z.attrs['description'] = 'Temperature data in Kelvin'
z.attrs['units'] = 'K'
z.attrs['created'] = '2024-01-15'
z.attrs['processing_version'] = 2.1

# 属性以JSON形式存储
print(z.attrs['units'])  # 输出：K

# 向组添加属性
root = zarr.group('data.zarr')
root.attrs['project'] = 'Climate Analysis'
root.attrs['institution'] = 'Research Institute'

# 属性与数组/组一起持久化
z2 = zarr.open('data.zarr')
print(z2.attrs['description'])
```

**重要**：属性必须是JSON可序列化的（字符串、数字、列表、字典、布尔值、null）。

## 与NumPy、Dask和Xarray的集成

### NumPy集成

Zarr数组实现NumPy数组接口：

```python
import numpy as np
import zarr

z = zarr.zeros((1000, 1000), chunks=(100, 100))

# 直接使用NumPy函数
result = np.sum(z, axis=0)  # NumPy操作Zarr数组
mean = np.mean(z[:100, :100])

# 转换为NumPy数组
numpy_array = z[:]  # 将整个数组加载到内存
```

### Dask集成

Dask对Zarr数组提供延迟、并行计算：

```python
import dask.array as da
import zarr

# 创建大型Zarr数组
z = zarr.open('data.zarr', mode='w', shape=(100000, 100000),
              chunks=(1000, 1000), dtype='f4')

# 加载为Dask数组（延迟，无数据加载）
dask_array = da.from_zarr('data.zarr')

# 执行计算（并行，核心外）
result = dask_array.mean(axis=0).compute()  # 并行计算

# 将Dask数组写入Zarr
large_array = da.random.random((100000, 100000), chunks=(1000, 1000))
da.to_zarr(large_array, 'output.zarr')
```

**好处**：
- 处理大于内存的数据集
- 跨分块自动并行计算
- 与分块存储的高效I/O

### Xarray集成

Xarray提供带有Zarr后端的标记多维数组：

```python
import xarray as xr
import zarr

# 以Xarray Dataset形式打开Zarr存储（延迟加载）
ds = xr.open_zarr('data.zarr')

# 数据集包含坐标和元数据
print(ds)

# 访问变量
temperature = ds['temperature']

# 执行标记操作
subset = ds.sel(time='2024-01', lat=slice(30, 60))

# 将Xarray Dataset写入Zarr
ds.to_zarr('output.zarr')

# 从头创建带有坐标
ds = xr.Dataset(
    {
        'temperature': (['time', 'lat', 'lon'], data),
        'precipitation': (['time', 'lat', 'lon'], data2)
    },
    coords={
        'time': pd.date_range('2024-01-01', periods=365),
        'lat': np.arange(-90, 91, 1),
        'lon': np.arange(-180, 180, 1)
    }
)
ds.to_zarr('climate_data.zarr')
```

**好处**：
- 命名维度和坐标
- 基于标签的索引和选择
- 与pandas集成用于时间序列
- 气候/地理空间科学家熟悉的NetCDF类接口

## 并行计算和同步

### 线程安全操作

```python
from zarr import ThreadSynchronizer
import zarr

# 用于多线程写入
synchronizer = ThreadSynchronizer()
z = zarr.open_array('data.zarr', mode='r+', shape=(10000, 10000),
                    chunks=(1000, 1000), synchronizer=synchronizer)

# 可安全地从多个线程并发写入
# （当写入不跨越分块边界时）
```

### 进程安全操作

```python
from zarr import ProcessSynchronizer
import zarr

# 用于多进程写入
synchronizer = ProcessSynchronizer('sync_data.sync')
z = zarr.open_array('data.zarr', mode='r+', shape=(10000, 10000),
                    chunks=(1000, 1000), synchronizer=synchronizer)

# 可安全地从多个进程并发写入
```

**注意**：
- 并发读取不需要同步
- 仅当写入可能跨越分块边界时才需要同步
- 每个进程/线程写入单独的分块时不需要同步

## 合并元数据

对于有许多数组的层次存储，将元数据合并到单个文件中以减少I/O操作：

```python
import zarr

# 创建数组/组后
root = zarr.group('data.zarr')
# ... 创建多个数组/组 ...

# 合并元数据
zarr.consolidate_metadata('data.zarr')

# 使用合并的元数据打开（更快，尤其是在云存储上）
root = zarr.open_consolidated('data.zarr')
```

**好处**：
- 将元数据读取操作从N（每个数组一个）减少到1
- 对云存储至关重要（减少延迟）
- 加快`tree()`操作和组遍历

**注意**：
- 如果数组更新而不重新合并，元数据可能会过时
- 不适合频繁更新的数据集
- 多写入器场景可能有不一致的读取

## 性能优化

### 最佳性能清单

1. **分块大小**：目标为每个分块1-10 MB
   ```python
   # 对于float32：1MB = 262,144个元素
   chunks = (512, 512)  # 512×512×4字节 = ~1MB
   ```

2. **分块形状**：与访问模式对齐
   ```python
   # 行式访问 → 分块跨越列：(小, 大)
   # 列式访问 → 分块跨越行：(大, 小)
   # 随机访问 → 平衡：(中, 中)
   ```

3. **压缩**：根据工作负载选择
   ```python
   # 交互式/快速：BloscCodec(cname='lz4')
   # 平衡：BloscCodec(cname='zstd', clevel=5)
   # 最大压缩：GzipCodec(level=9)
   ```

4. **存储后端**：与环境匹配
   ```python
   # 本地：LocalStore（默认）
   # 云：S3Map/GCSMap带合并元数据
   # 临时：MemoryStore
   ```

5. **分片**：用于大规模数据集
   ```python
   # 当有数百万个小分块时
   shards=(10*chunk_size, 10*chunk_size)
   ```

6. **并行I/O**：大型操作使用Dask
   ```python
   import dask.array as da
   dask_array = da.from_zarr('data.zarr')
   result = dask_array.compute(scheduler='threads', num_workers=8)
   ```

### 分析和调试

```python
# 打印详细的数组信息
print(z.info)

# 输出包括：
# - 类型、形状、分块、数据类型
# - 压缩编解码器和级别
# - 存储大小（压缩与未压缩）
# - 存储位置

# 检查存储大小
print(f"压缩大小: {z.nbytes_stored / 1e6:.2f} MB")
print(f"未压缩大小: {z.nbytes / 1e6:.2f} MB")
print(f"压缩比: {z.nbytes / z.nbytes_stored:.2f}x")
```

## 常见模式和最佳实践

### 模式：时间序列数据

```python
# 以时间为第一维度存储时间序列
# 这允许有效追加新时间步
z = zarr.open('timeseries.zarr', mode='a',
              shape=(0, 720, 1440),  # 从0个时间步开始
              chunks=(1, 720, 1440),  # 每个分块一个时间步
              dtype='f4')

# 追加新时间步
new_data = np.random.random((1, 720, 1440))
z.append(new_data, axis=0)
```

### 模式：大型矩阵操作

```python
import dask.array as da

# 在Zarr中创建大型矩阵
z = zarr.open('matrix.zarr', mode='w',
              shape=(100000, 100000),
              chunks=(1000, 1000),
              dtype='f8')

# 使用Dask进行并行计算
dask_z = da.from_zarr('matrix.zarr')
result = (dask_z @ dask_z.T).compute()  # 并行矩阵乘法
```

### 模式：云原生工作流

```python
import s3fs
import zarr

# 写入S3
s3 = s3fs.S3FileSystem()
store = s3fs.S3Map(root='s3://my-bucket/data.zarr', s3=s3)

# 创建具有适合云的分块的数组
z = zarr.open_array(store=store, mode='w',
                    shape=(10000, 10000),
                    chunks=(500, 500),  # ~1MB分块
                    dtype='f4')
z[:] = data

# 合并元数据以加快读取
zarr.consolidate_metadata(store)

# 从S3读取（任何地方，任何时间）
store_read = s3fs.S3Map(root='s3://my-bucket/data.zarr', s3=s3)
z_read = zarr.open_consolidated(store_read)
subset = z_read[0:100, 0:100]
```

### 模式：格式转换

```python
# HDF5到Zarr
import h5py
import zarr

with h5py.File('data.h5', 'r') as h5:
    dataset = h5['dataset_name']
    z = zarr.array(dataset[:],
                   chunks=(1000, 1000),
                   store='data.zarr')

# NumPy到Zarr
import numpy as np
data = np.load('data.npy')
z = zarr.array(data, chunks='auto', store='data.zarr')

# Zarr到NetCDF（通过Xarray）
import xarray as xr
ds = xr.open_zarr('data.zarr')
ds.to_netcdf('data.nc')
```

## 常见问题和解决方案

### 问题：性能缓慢

**诊断**：检查分块大小和对齐
```python
print(z.chunks)  # 分块大小是否合适？
print(z.info)    # 检查压缩比
```

**解决方案**：
- 将分块大小增加到1-10 MB
- 使分块与访问模式对齐
- 尝试不同的压缩编解码器
- 使用Dask进行并行操作

### 问题：内存使用高

**原因**：将整个数组或大型分块加载到内存

**解决方案**：
```python
# 不要加载整个数组
# 错误：data = z[:]
# 正确：分块处理
for i in range(0, z.shape[0], 1000):
    chunk = z[i:i+1000, :]
    process(chunk)

# 或使用Dask进行自动分块
import dask.array as da
dask_z = da.from_zarr('data.zarr')
result = dask_z.mean().compute()  # 分块处理
```

### 问题：云存储延迟

**解决方案**：
```python
# 1. 合并元数据
zarr.consolidate_metadata(store)
z = zarr.open_consolidated(store)

# 2. 使用适当的分块大小（云为5-100 MB）
chunks = (2000, 2000)  # 云用更大的分块

# 3. 启用分片
shards = (10000, 10000)  # 组许多分块
```

### 问题：并发写入冲突

**解决方案**：使用同步器或确保非重叠写入
```python
from zarr import ProcessSynchronizer

sync = ProcessSynchronizer('sync.sync')
z = zarr.open_array('data.zarr', mode='r+', synchronizer=sync)

# 或设计工作流，使每个进程写入单独的分块
```

## 其他资源

有关详细的API文档、高级用法和最新更新：

- **官方文档**：https://zarr.readthedocs.io/
- **Zarr规范**：https://zarr-specs.readthedocs.io/
- **GitHub存储库**：https://github.com/zarr-developers/zarr-python
- **社区聊天**：https://gitter.im/zarr-developers/community

**相关库**：
- **Xarray**：https://docs.xarray.dev/（标记数组）
- **Dask**：https://docs.dask.org/（并行计算）
- **NumCodecs**：https://numcodecs.readthedocs.io/（压缩编解码器）