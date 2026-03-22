---
name: geopandas
description: 用于处理地理空间矢量数据（包括shapefiles、GeoJSON和GeoPackage文件）的Python库。用于处理地理数据以进行空间分析、几何操作、坐标转换、空间连接、叠加操作、等值线映射或任何涉及读取/写入/分析矢量地理数据的任务。支持PostGIS数据库、交互式地图以及与matplotlib/folium/cartopy集成。用于缓冲区分析、数据集之间的空间连接、边界融合、裁剪数据、计算面积/距离、重新投影坐标系统、创建地图或在不同空间文件格式之间转换。
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# GeoPandas

GeoPandas扩展pandas以启用几何类型的空间操作。它结合了pandas和shapely的功能，用于地理空间数据分析。

## 安装

```bash
uv pip install geopandas
```

### 可选依赖项

```bash
# 用于交互式地图
uv pip install folium

# 用于映射中的分类方案
uv pip install mapclassify

# 用于更快的I/O操作（2-4倍加速）
uv pip install pyarrow

# 用于PostGIS数据库支持
uv pip install psycopg2
uv pip install geoalchemy2

# 用于底图
uv pip install contextily

# 用于制图投影
uv pip install cartopy
```

## 快速开始

```python
import geopandas as gpd

# 读取空间数据
gdf = gpd.read_file("data.geojson")

# 基本探索
print(gdf.head())
print(gdf.crs)
print(gdf.geometry.geom_type)

# 简单绘图
gdf.plot()

# 重新投影到不同的CRS
gdf_projected = gdf.to_crs("EPSG:3857")

# 计算面积（使用投影的CRS以获得准确性）
gdf_projected['area'] = gdf_projected.geometry.area

# 保存到文件
gdf.to_file("output.gpkg")
```

## 核心概念

### 数据结构

- **GeoSeries**：具有空间操作的几何矢量
- **GeoDataFrame**：具有几何列的表格数据结构

参见 [data-structures.md](references/data-structures.md) 获取详细信息。

### 读取和写入数据

GeoPandas读取/写入多种格式：Shapefile、GeoJSON、GeoPackage、PostGIS、Parquet。

```python
# 带过滤的读取
gdf = gpd.read_file("data.gpkg", bbox=(xmin, ymin, xmax, ymax))

# 使用Arrow加速写入
gdf.to_file("output.gpkg", use_arrow=True)
```

参见 [data-io.md](references/data-io.md) 获取全面的I/O操作。

### 坐标参考系统

始终检查和管理CRS以进行准确的空间操作：

```python
# 检查CRS
print(gdf.crs)

# 重新投影（转换坐标）
gdf_projected = gdf.to_crs("EPSG:3857")

# 设置CRS（仅在元数据缺失时）
gdf = gdf.set_crs("EPSG:4326")
```

参见 [crs-management.md](references/crs-management.md) 获取CRS操作。

## 常见操作

### 几何操作

缓冲、简化、质心、凸包、仿射变换：

```python
# 缓冲10个单位
buffered = gdf.geometry.buffer(10)

# 使用容差简化
simplified = gdf.geometry.simplify(tolerance=5, preserve_topology=True)

# 获取质心
centroids = gdf.geometry.centroid
```

参见 [geometric-operations.md](references/geometric-operations.md) 获取所有操作。

### 空间分析

空间连接、叠加操作、融合：

```python
# 空间连接（相交）
joined = gpd.sjoin(gdf1, gdf2, predicate='intersects')

# 最近邻连接
nearest = gpd.sjoin_nearest(gdf1, gdf2, max_distance=1000)

# 叠加交集
intersection = gpd.overlay(gdf1, gdf2, how='intersection')

# 按属性融合
dissolved = gdf.dissolve(by='region', aggfunc='sum')
```

参见 [spatial-analysis.md](references/spatial-analysis.md) 获取分析操作。

### 可视化

创建静态和交互式地图：

```python
# 等值线地图
gdf.plot(column='population', cmap='YlOrRd', legend=True)

# 交互式地图
gdf.explore(column='population', legend=True).save('map.html')

# 多层地图
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
gdf1.plot(ax=ax, color='blue')
gdf2.plot(ax=ax, color='red')
```

参见 [visualization.md](references/visualization.md) 获取绘图技术。

## 详细文档

- **[数据结构](references/data-structures.md)** - GeoSeries和GeoDataFrame基础知识
- **[数据I/O](references/data-io.md)** - 读取/写入文件、PostGIS、Parquet
- **[几何操作](references/geometric-operations.md)** - 缓冲、简化、仿射变换
- **[空间分析](references/spatial-analysis.md)** - 连接、叠加、融合、裁剪
- **[可视化](references/visualization.md)** - 绘图、等值线地图、交互式地图
- **[CRS管理](references/crs-management.md)** - 坐标参考系统和投影

## 常见工作流

### 加载、转换、分析、导出

```python
# 1. 加载数据
gdf = gpd.read_file("data.shp")

# 2. 检查并转换CRS
print(gdf.crs)
gdf = gdf.to_crs("EPSG:3857")

# 3. 执行分析
gdf['area'] = gdf.geometry.area
buffered = gdf.copy()
buffered['geometry'] = gdf.geometry.buffer(100)

# 4. 导出结果
gdf.to_file("results.gpkg", layer='original')
buffered.to_file("results.gpkg", layer='buffered')
```

### 空间连接和聚合

```python
# 将点连接到多边形
points_in_polygons = gpd.sjoin(points_gdf, polygons_gdf, how='inner', predicate='within')

# 按多边形聚合
aggregated = points_in_polygons.groupby('index_right').agg({
    'value': 'sum',
    'count': 'size'
})

# 合并回多边形
result = polygons_gdf.merge(aggregated, left_index=True, right_index=True)
```

### 多源数据集成

```python
# 从不同来源读取
roads = gpd.read_file("roads.shp")
buildings = gpd.read_file("buildings.geojson")
parcels = gpd.read_postgis("SELECT * FROM parcels", con=engine, geom_col='geom')

# 确保匹配的CRS
buildings = buildings.to_crs(roads.crs)
parcels = parcels.to_crs(roads.crs)

# 执行空间操作
buildings_near_roads = buildings[buildings.geometry.distance(roads.union_all()) < 50]
```

## 性能提示

1. **使用空间索引**：GeoPandas为大多数操作自动创建空间索引
2. **读取时过滤**：使用`bbox`、`mask`或`where`参数仅加载所需数据
3. **使用Arrow进行I/O**：添加`use_arrow=True`以获得2-4倍更快的读取/写入
4. **简化几何**：当精度不重要时使用`.simplify()`减少复杂度
5. **批量操作**：向量化操作比迭代行快得多
6. **使用适当的CRS**：面积/距离使用投影的CRS，地理用于可视化

## 最佳实践

1. **始终检查CRS**在任何空间操作之前
2. **使用投影的CRS**进行面积和距离计算
3. **连接之前匹配CRS**进行空间连接或叠加
4. **验证几何**在操作之前使用`.is_valid`
5. **修改几何时使用.copy()`**以避免副作用
6. **简化时保留拓扑**用于分析
7. **使用GeoPackage格式**用于现代工作流（优于Shapefile）
8. **在sjoin_nearest中设置max_distance**以获得更好的性能
