---
name: astropy
description: 用于需要Astropy API的天文学和天体物理学工作流的核心Python库，包括单位/量、坐标、FITS I/O、表格、时间系统、WCS和宇宙学。当使用Astropy实现或调试天文数据分析代码时使用。
license: BSD-3-Clause license
compatibility: Requires Python 3.11+ with astropy installed (uv for package installation). Some features (object name resolution, site lookups, remote FITS reads, IERS updates) need network access.
metadata: {"version": "1.2", "skill-author": "K-Dense Inc."}
---






# Astropy

## 概述

Astropy 是天文学的核心 Python 包，为天文研究和数据分析提供基本功能。使用 astropy 进行坐标变换、单位 和数量计算、FITS 文件操作、宇宙学计算、精确时间处理、表格数据操作和天文图像处理。

## 何时使用此技能

在以下任务中使用 astropy：
- 天球坐标系统之间的转换（ICRS、Galactic、FK5、AltAz 等）
- 处理物理单位和数量（将 Jy 转换为 mJy，将秒差距转换为 km 等）
- 读取、写入或操作 FITS 文件（图像或表格）
- 宇宙学计算（光度距离、回看时间、哈勃参数）
- 不同时间尺度（UTC、TAI、TT、TDB）和格式（JD、MJD、ISO）的精确时间处理
- 表格操作（读取星表、交叉匹配、过滤、连接）
- 像素坐标和世界坐标之间的 WCS 变换
- 天文常数和计算

## 快速开始

```python
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astropy.io import fits
from astropy.table import Table
from astropy.cosmology import Planck18

# 单位和数量
distance = 100 * u.pc
distance_km = distance.to(u.km)

# 坐标
coord = SkyCoord(ra=10.5*u.degree, dec=41.2*u.degree, frame='icrs')
coord_galactic = coord.galactic

# 时间
t = Time('2023-01-15 12:30:00')
jd = t.jd  # 儒略日

# FITS 文件
data = fits.getdata('image.fits')
header = fits.getheader('image.fits')

# 表格
table = Table.read('catalog.fits')

# 宇宙学
d_L = Planck18.luminosity_distance(z=1.0)
```

## 核心能力

### 1. 单位和数量（`astropy.units`）

处理带单位的物理量，执行单位转换，确保计算中的量纲一致性。

**关键操作：**
- 通过将值乘以单位来创建数量
- 使用 `.to()` 方法在单位之间转换
- 执行算术运算并自动处理单位
- 使用等效性进行特定领域的转换（光谱、多普勒、视差）
- 使用对数单位（星等、分贝）

**参见**：`references/units.md` 获取全面的文档、单位系统、等效性、性能优化和单位算术。

### 2. 坐标系统（`astropy.coordinates`）

表示天球位置并在不同的坐标框架之间变换。

**关键操作：**
- 使用 `SkyCoord` 在任何框架（ICRS、Galactic、FK5、AltAz 等）中创建坐标
- 坐标系统之间的变换
- 计算角距离和位置角
- 将坐标与星表匹配
- 包含距离以进行 3D 坐标操作
- 处理自行和视向速度
- 从在线数据库查询命名天体

**参见**：`references/coordinates.md` 获取详细的坐标框架描述、变换、依赖于观测者的框架（AltAz）、星表匹配和性能提示。

### 3. 宇宙学计算（`astropy.cosmology`）

使用标准宇宙学模型进行宇宙学计算。

**关键操作：**
- 使用内置宇宙学模型（Planck18、WMAP9 等）
- 创建自定义宇宙学模型
- 计算距离（光度距离、共动距离、角直径距离）
- 计算年龄和回看时间
- 确定任何红移处的哈勃参数
- 计算密度参数和体积
- 执行逆计算（给定距离找 z）

**参见**：`references/cosmology.md` 获取可用模型、距离计算、时间计算、密度参数和中微子效应。

### 4. FITS 文件处理（`astropy.io.fits`）

读取、写入和操作 FITS（灵活图像传输系统）文件。

**关键操作：**
- 使用上下文管理器打开 FITS 文件
- 按索引或名称访问 HDU（头数据单元）
- 读取和修改头（关键字、注释、历史）
- 处理图像数据（NumPy 数组）
- 处理表格数据（二进制和 ASCII 表格）
- 创建新的 FITS 文件（单文件或多扩展名）
- 对大文件使用内存映射
- 访问远程 FITS 文件（S3、HTTP）

**参见**：`references/fits.md` 获取全面的文件操作、头操作、图像和表格处理、多扩展名文件以及性能注意事项。

### 5. 表格操作（`astropy.table`）

处理表格数据，支持单位、元数据和各种文件格式。

**关键操作：**
- 从数组、列表或字典创建表格
- 多种格式读取/写入表格（FITS、CSV、HDF5、VOTable）
- 访问和修改列和行
- 对表格进行排序、过滤和索引
- 执行数据库式操作（连接、分组、聚合）
- 堆叠和串联表格
- 使用支持单位的列（QTable）
- 使用掩码处理缺失数据

**参见**：`references/tables.md` 获取表格创建、I/O 操作、数据操作、排序、过滤、连接、分组和性能提示。

### 6. 时间处理（`astropy.time`）

精确的时间表示和时间尺度与格式之间的转换。

**关键操作：**
- 以各种格式（ISO、JD、MJD、Unix 等）创建 Time 对象
- 时间尺度之间的转换（UTC、TAI、TT、TDB 等）
- 使用 TimeDelta 执行时间算术
- 为观测者计算恒星时
- 计算光行时间校正（地心、日心）
- 高效处理时间数组
- 处理掩码（缺失）时间

**参见**：`references/time.md` 获取时间格式、时间尺度、转换、算术、观测功能和精度处理。

### 7. 世界坐标系统（`astropy.wcs`）

在图像中的像素坐标和世界坐标之间变换。

**关键操作：**
- 从 FITS 头读取 WCS
- 将像素坐标转换为世界坐标（反之亦然）
- 计算图像足迹
- 访问 WCS 参数（参考像素、投影、比例）
- 创建自定义 WCS 对象

**参见**：`references/wcs_and_other_modules.md` 获取 WCS 操作和变换。

## 附加能力

`references/wcs_and_other_modules.md` 文件还涵盖：

### NDData 和 CCDData
用于多维数据集的容器，带有元数据、不确定性、掩码和 WCS 信息。

### 建模
用于创建和拟合天文数据数学模型的框架。

### 可视化
具有适当拉伸和缩放的天文图像显示工具。

### 常数
具有正确单位的物理和天文常数（光速、太阳质量、普朗克常数等）。

### 卷积
用于平滑和滤波的图像处理核。

### 统计
强大的统计函数，包括 sigma 剪裁和离群值拒绝。

## 安装

```bash
# 针对当前稳定版本的可重现安装
uv pip install "astropy==7.2.0"

# 推荐的绘图和常见工作流程的可选依赖
uv pip install "astropy[recommended]==7.2.0"

# 广泛天文学工作流程的完整可选依赖集
uv pip install "astropy[all]==7.2.0"
```

Astropy 7.2.0 需要 Python 3.11+ 并依赖 NumPy、PyERFA、PyYAML 和 packaging。使用隔离的虚拟环境；不要使用提升的权限安装 Astropy。

请注意，`[recommended]` 和 `[all]` extras 会引入未固定版本的传递依赖（matplotlib、scipy 等）。对于需要可复现性的生产环境，请使用锁文件固定完整依赖树（项目中用 `uv lock`，或对 requirements 文件使用 `uv pip compile`），并在部署前审查已解析的版本。

## 常见工作流程

### 坐标系统之间的转换

```python
from astropy.coordinates import SkyCoord
import astropy.units as u

# 创建坐标
c = SkyCoord(ra='05h23m34.5s', dec='-69d45m22s', frame='icrs')

# 转换为银道坐标
c_gal = c.galactic
print(f"l={c_gal.l.deg}, b={c_gal.b.deg}")

# 转换为地平坐标（需要时间和位置）
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz

observing_time = Time('2023-06-15 23:00:00')
observing_location = EarthLocation(lat=40*u.deg, lon=-120*u.deg)
aa_frame = AltAz(obstime=observing_time, location=observing_location)
c_altaz = c.transform_to(aa_frame)
print(f"Alt={c_altaz.alt.deg}, Az={c_altaz.az.deg}")
```

### 读取和分析 FITS 文件

```python
from astropy.io import fits
import numpy as np

# 打开 FITS 文件
with fits.open('observation.fits') as hdul:
    # 显示结构
    hdul.info()

    # 获取图像数据和头
    data = hdul[1].data
    header = hdul[1].header

    # 访问头值
    exptime = header['EXPTIME']
    filter_name = header['FILTER']

    # 分析数据
    mean = np.mean(data)
    median = np.median(data)
    print(f"Mean: {mean}, Median: {median}")
```

### 宇宙学距离计算

```python
from astropy.cosmology import Planck18
import astropy.units as u
import numpy as np

# 计算 z=1.5 处的距离
z = 1.5
d_L = Planck18.luminosity_distance(z)
d_A = Planck18.angular_diameter_distance(z)

print(f"Luminosity distance: {d_L}")
print(f"Angular diameter distance: {d_A}")

# 那个红移处的宇宙年龄
age = Planck18.age(z)
print(f"Age at z={z}: {age.to(u.Gyr)}")

# 回看时间
t_lookback = Planck18.lookback_time(z)
print(f"Lookback time: {t_lookback.to(u.Gyr)}")
```

### 交叉匹配星表

```python
from astropy.table import Table
from astropy.coordinates import SkyCoord, match_coordinates_sky
import astropy.units as u

# 读取星表
cat1 = Table.read('catalog1.fits')
cat2 = Table.read('catalog2.fits')

# 创建坐标对象
coords1 = SkyCoord(ra=cat1['RA']*u.degree, dec=cat1['DEC']*u.degree)
coords2 = SkyCoord(ra=cat2['RA']*u.degree, dec=cat2['DEC']*u.degree)

# 查找匹配
idx, sep, _ = coords1.match_to_catalog_sky(coords2)

# 按分离阈值过滤
max_sep = 1 * u.arcsec
matches = sep < max_sep

# 创建匹配的星表
matched_cat1 = cat1[matches]
matched_cat2 = cat2[idx[matches]]
```

## 最佳实践

1. **使用 Quantity 进行计算**：始终使用 astropy.units 进行物理计算
   ```python
   from astropy import units as u
   distance = 10 * u.pc
   flux = 1e-20 * u.erg / (u.cm**2 * u.s * u.AA)
   ```

2. **使用 SkyCoord 处理坐标**：不要手动转换坐标
   ```python
   from astropy.coordinates import SkyCoord
   coord = SkyCoord(ra=10.68*u.deg, dec=41.27*u.deg, frame='icrs')
   ```

3. **正确处理 FITS 文件**：使用 astropy.io.fits 确保一致性
   ```python
   from astropy.io import fits
   with fits.open('file.fits') as hdul:
       data = hdul[1].data
   ```

4. **使用表格的 Quantity 列**：在表格中使用带单位的列
   ```python
   from astropy import units as u
   from astropy.table import Table
   t = Table({'flux': [1, 2, 3] * u.Jy})
   ```

## 当前版本说明

- **astropy 6.x**：当前稳定版本
- **Python 要求**：Python 3.8+
- **主要更改**： cosmology 模块的重大更新，新的表格功能

## 文档和资源

- [Astropy 文档](https://docs.astropy.org/)
- [Astropy 教程](https://learn.astropy.org/)
- [Astropy API 参考](https://docs.astropy.org/en/latest/api/index.html)
- [FITS 格式文档](https://fits.gsfc.nasa.gov/)

## 参考文件

- `references/coordinates.md` - 坐标系统详细参考
- `references/cosmology.md` - 宇宙学计算参考
- `references/units.md` - 单位和物理常数参考
