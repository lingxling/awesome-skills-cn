---
name: geomaster
description: 使用OpenAI的GPT-4o或GPT-4o-mini模型生成、编辑和分析地理空间数据。用于生成GeoJSON数据、执行空间分析、创建地图可视化、转换地理数据格式、分析地理空间模式、生成地理空间代码或任何涉及地理空间数据处理的任务。可以处理地理空间数据以进行空间分析、几何操作、坐标转换、空间连接、叠加操作、等值线映射或任何涉及读取/写入/分析矢量地理数据的任务。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# GeoMaster

GeoMaster是一个强大的地理空间AI助手，使用OpenAI的GPT-4o或GPT-4o-mini模型生成、编辑和分析地理空间数据。它提供类似GeoPandas的功能，但具有AI增强的能力，包括自然语言查询、智能数据生成和自动化分析。

## 何时使用此技能

使用GeoMaster当：

- **需要自然语言地理空间查询**：使用简单英语查询地理空间数据
- **需要AI辅助的数据生成**：生成GeoJSON、Shapefile或其他地理数据格式
- **需要智能空间分析**：执行复杂空间操作并解释结果
- **需要地图可视化**：创建美观的地图和可视化
- **需要数据转换**：在不同地理数据格式之间转换
- **需要模式识别**：识别地理空间数据中的模式和趋势
- **需要代码生成**：为地理空间任务生成Python/R代码

## 核心功能

### 1. 地理空间数据生成

```python
from geomaster import GeoMaster

# 初始化GeoMaster
geo = GeoMaster(model="gpt-4o")  # 或 "gpt-4o-mini"

# 生成GeoJSON数据
geojson_data = geo.generate_geojson(
    description="创建一个包含美国主要城市的GeoJSON数据集",
    features=["name", "population", "state"]
)

# 生成随机点数据
points = geo.generate_random_points(
    count=100,
    bounds=(-122.5, 37.7, -122.3, 37.9),  # xmin, ymin, xmax, ymax
    properties=["id", "value"]
)
```

### 2. 空间分析

```python
# 空间连接
joined = geo.spatial_join(
    points_gdf,
    polygons_gdf,
    predicate="within",
    description="将点连接到它们所在的多边形"
)

# 缓冲区分析
buffered = geo.buffer_analysis(
    gdf,
    distance=1000,
    unit="meters",
    description="创建1000米缓冲区"
)

# 最近邻分析
nearest = geo.nearest_neighbor(
    points_gdf,
    target_points_gdf,
    k=3,
    description="找到每个点的3个最近邻"
)
```

### 3. 地图可视化

```python
# 创建等值线地图
map = geo.create_choropleth(
    gdf,
    value_column="population",
    description="创建人口等值线地图",
    style="viridis"
)

# 创建交互式地图
interactive_map = geo.create_interactive_map(
    gdf,
    popup_columns=["name", "value"],
    description="创建带有弹出信息的交互式地图"
)

# 创建热力图
heatmap = geo.create_heatmap(
    points_gdf,
    weight_column="value",
    description="创建值的热力图"
)
```

### 4. 数据转换

```python
# GeoJSON转Shapefile
shapefile = geo.convert_format(
    geojson_data,
    target_format="shapefile",
    description="将GeoJSON转换为Shapefile"
)

# Shapefile转GeoPackage
geopackage = geo.convert_format(
    shapefile,
    target_format="geopackage",
    description="将Shapefile转换为GeoPackage"
)

# CSV转GeoJSON（带坐标列）
geojson = geo.convert_format(
    csv_data,
    target_format="geojson",
    lat_column="latitude",
    lon_column="longitude",
    description="将CSV转换为GeoJSON"
)
```

### 5. 自然语言查询

```python
# 自然语言查询
result = geo.query(
    "找出所有人口超过100万的城市",
    data=gdf
)

# 复杂查询
result = geo.query(
    "找出距离高速公路500米以内且人口超过50万的区域",
    data=gdf,
    roads_data=roads_gdf
)

# 统计查询
result = geo.query(
    "计算每个州的总人口和平均人口密度",
    data=gdf
)
```

### 6. 代码生成

```python
# 生成GeoPandas代码
code = geo.generate_code(
    task="加载Shapefile，计算每个多边形的面积，并按面积排序",
    library="geopandas"
)

# 生成可视化代码
code = geo.generate_code(
    task="创建带有图例和标题的等值线地图",
    library="matplotlib"
)

# 生成分析代码
code = geo.generate_code(
    task="执行空间连接并聚合数据",
    library="geopandas"
)
```

## 高级功能

### 1. 模式识别

```python
# 识别聚类
clusters = geo.identify_clusters(
    points_gdf,
    method="dbscan",
    description="识别点数据中的空间聚类"
)

# 识别异常值
outliers = geo.identify_outliers(
    gdf,
    method="isolation_forest",
    description="识别地理空间数据中的异常值"
)

# 识别趋势
trends = geo.identify_trends(
    gdf,
    value_column="population",
    description="识别人口分布的趋势"
)
```

### 2. 预测分析

```python
# 空间插值
interpolated = geo.spatial_interpolation(
    points_gdf,
    value_column="value",
    method="kriging",
    description="使用克里金法进行空间插值"
)

# 预测未来值
predicted = geo.predict_future(
    gdf,
    value_column="population",
    years=10,
    description="预测未来10年的人口"
)
```

### 3. 批量处理

```python
# 批量转换
results = geo.batch_convert(
    files=["file1.geojson", "file2.geojson", "file3.geojson"],
    target_format="shapefile",
    description="批量转换多个GeoJSON文件为Shapefile"
)

# 批量分析
results = geo.batch_analyze(
    files=["data1.shp", "data2.shp", "data3.shp"],
    analysis=["buffer", "area", "centroid"],
    description="批量分析多个Shapefile"
)
```

## 最佳实践

1. **使用描述性提示**：提供清晰的描述以获得更好的结果
2. **指定数据格式**：明确指定输入和输出格式
3. **使用适当的模型**：GPT-4o用于复杂任务，GPT-4o-mini用于简单任务
4. **验证结果**：始终验证AI生成的数据和分析结果
5. **结合传统工具**：将GeoMaster与GeoPandas、QGIS等传统工具结合使用
6. **处理大型数据集**：对于大型数据集，考虑分块处理或使用传统工具

## 限制

1. **模型限制**：受限于GPT-4o的上下文窗口和推理能力
2. **准确性**：AI生成的数据可能需要验证和调整
3. **性能**：对于大型数据集，性能可能不如传统工具
4. **成本**：使用GPT-4o API会产生费用
5. **复杂性**：对于非常复杂的空间分析，可能需要专业GIS软件

## 与其他工具集成

### 与GeoPandas集成

```python
import geopandas as gpd
from geomaster import GeoMaster

# 使用GeoMaster生成数据
geo = GeoMaster()
geojson_data = geo.generate_geojson("创建城市数据")

# 使用GeoPandas加载和处理
gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])

# 执行传统GeoPandas操作
gdf['area'] = gdf.geometry.area
```

### 与QGIS集成

```python
# 使用GeoMaster生成数据
geo = GeoMaster()
geojson_data = geo.generate_geojson("创建区域数据")

# 保存到文件以在QGIS中使用
with open("data.geojson", "w") as f:
    json.dump(geojson_data, f)

# 在QGIS中打开并进一步编辑
```

### 与PostGIS集成

```python
import sqlalchemy
from geomaster import GeoMaster

# 使用GeoMaster生成数据
geo = GeoMaster()
geojson_data = geo.generate_geojson("创建地点数据")

# 加载到PostGIS数据库
engine = sqlalchemy.create_engine("postgresql://user:password@localhost/db")
gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])
gdf.to_postgis("places", engine, if_exists="replace")
```

## 示例工作流

### 工作流1：生成和分析城市数据

```python
from geomaster import GeoMaster
import geopandas as gpd

# 1. 生成城市数据
geo = GeoMaster(model="gpt-4o")
cities = geo.generate_geojson(
    "创建包含美国50个最大城市的GeoJSON数据",
    features=["name", "population", "state", "coordinates"]
)

# 2. 转换为GeoDataFrame
gdf = gpd.GeoDataFrame.from_features(cities["features"])

# 3. 执行分析
gdf['area'] = gdf.geometry.area
gdf['density'] = gdf['population'] / gdf['area']

# 4. 创建可视化
map = geo.create_choropleth(
    gdf,
    value_column="population",
    description="创建城市人口地图"
)

# 5. 保存结果
gdf.to_file("cities.gpkg")
```

### 工作流2：空间连接和聚合

```python
from geomaster import GeoMaster
import geopandas as gpd

# 1. 加载数据
points = gpd.read_file("points.shp")
polygons = gpd.read_file("polygons.shp")

# 2. 使用GeoMaster执行空间连接
geo = GeoMaster()
joined = geo.spatial_join(
    points,
    polygons,
    predicate="within",
    description="将点连接到它们所在的多边形"
)

# 3. 聚合数据
aggregated = joined.groupby('polygon_id').agg({
    'value': 'sum',
    'count': 'size'
})

# 4. 合并回多边形
result = polygons.merge(aggregated, left_index=True, right_index=True)

# 5. 创建可视化
map = geo.create_choropleth(
    result,
    value_column="value",
    description="创建聚合值地图"
)
```

### 工作流3：批量数据处理

```python
from geomaster import GeoMaster
import glob

# 1. 初始化GeoMaster
geo = GeoMaster(model="gpt-4o-mini")

# 2. 批量转换文件
files = glob.glob("data/*.geojson")
for file in files:
    result = geo.convert_format(
        file,
        target_format="shapefile",
        description=f"转换{file}为Shapefile"
    )

# 3. 批量分析
results = geo.batch_analyze(
    files,
    analysis=["buffer", "area", "centroid"],
    description="批量分析所有文件"
)

# 4. 生成报告
report = geo.generate_report(
    results,
    description="生成分析报告"
)
```

## API 参考

### GeoMaster类

```python
class GeoMaster:
    def __init__(self, model="gpt-4o", api_key=None):
        """
        初始化GeoMaster

        参数:
            model: "gpt-4o"或"gpt-4o-mini"
            api_key: OpenAI API密钥（可选，从环境变量读取）
        """
        pass

    def generate_geojson(self, description, features=None, **kwargs):
        """
        生成GeoJSON数据

        参数:
            description: 数据的自然语言描述
            features: 要包含的属性列表
            **kwargs: 其他参数

        返回:
            GeoJSON数据字典
        """
        pass

    def spatial_join(self, left_gdf, right_gdf, predicate, description=None, **kwargs):
        """
        执行空间连接

        参数:
            left_gdf: 左GeoDataFrame
            right_gdf: 右GeoDataFrame
            predicate: 谓词（within, intersects, contains等）
            description: 操作的自然语言描述
            **kwargs: 其他参数

        返回:
            连接后的GeoDataFrame
        """
        pass

    def create_choropleth(self, gdf, value_column, description=None, **kwargs):
        """
        创建等值线地图

        参数:
            gdf: GeoDataFrame
            value_column: 要可视化的列
            description: 地图的自然语言描述
            **kwargs: 其他参数（样式、颜色等）

        返回:
            地图对象
        """
        pass

    def query(self, natural_language_query, data, **kwargs):
        """
        执行自然语言查询

        参数:
            natural_language_query: 自然语言查询字符串
            data: GeoDataFrame或数据字典
            **kwargs: 其他参数

        返回:
            查询结果
        """
        pass

    def generate_code(self, task, library="geopandas", **kwargs):
        """
        生成地理空间代码

        参数:
            task: 任务的描述
            library: 目标库（geopandas, matplotlib等）
            **kwargs: 其他参数

        返回:
            生成的代码字符串
        """
        pass
```

## 故障排除

### 常见问题

**问题：API密钥错误**
- 解决方案：确保设置了OPENAI_API_KEY环境变量或传递了api_key参数

**问题：生成数据不准确**
- 解决方案：提供更详细的描述，验证结果，必要时手动调整

**问题：性能慢**
- 解决方案：对于大型数据集使用GPT-4o-mini，考虑分块处理

**问题：上下文限制**
- 解决方案：将大型任务分解为较小的子任务，或使用传统工具

**问题：格式转换失败**
- 解决方案：检查输入数据格式，确保坐标参考系统正确

## 其他资源

- **OpenAI API文档**: https://platform.openai.com/docs/
- **GeoPandas文档**: https://geopandas.org/
- **GeoJSON规范**: https://geojson.org/
- **QGIS文档**: https://docs.qgis.org/
