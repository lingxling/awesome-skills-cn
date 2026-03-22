---
name: datacommons-client
description: 与 Data Commons 一起工作，这是一个提供对来自全球来源的公共统计数据进行编程访问的平台。当处理人口统计数据、经济指标、健康统计、环境数据或任何可通过 Data Commons 获得的公共数据集时使用此技能。适用于查询人口统计、GDP 数据、失业率、疾病患病率、地理实体解析以及探索统计实体之间的关系。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# Data Commons Client

## 概述

提供对 Data Commons Python API v2 的全面访问，用于查询统计观测值、探索知识图谱和解析实体标识符。Data Commons 将来自人口普查局、卫生组织、环境机构和其他权威来源的数据聚合到一个统一的知识图谱中。

## 安装

安装带有 Pandas 支持的 Data Commons Python 客户端：

```bash
uv pip install "datacommons-client[Pandas]"
```

对于不带 Pandas 的基本用法：
```bash
uv pip install datacommons-client
```

## 核心能力

Data Commons API 由三个主要端点组成，每个端点在专门的参考文件中有详细说明：

### 1. Observation 端点 - 统计数据查询

查询实体的时间序列统计数据。有关综合文档，请参阅 `references/observation.md`。

**主要用例：**
- 检索人口、经济、健康或环境统计数据
- 访问历史时间序列数据以进行趋势分析
- 查询层次结构的数据（州内所有县、区域内所有国家）
- 比较多个实体的统计数据
- 按数据源过滤以确保一致性

**常见模式：**
```python
from datacommons_client import DataCommonsClient

client = DataCommonsClient()

# 获取最新人口数据
response = client.observation.fetch(
    variable_dcids=["Count_Person"],
    entity_dcids=["geoId/06"],  # 加利福尼亚
    date="latest"
)

# 获取时间序列
response = client.observation.fetch(
    variable_dcids=["UnemploymentRate_Person"],
    entity_dcids=["country/USA"],
    date="all"
)

# 按层次结构查询
response = client.observation.fetch(
    variable_dcids=["MedianIncome_Household"],
    entity_expression="geoId/06<-containedInPlace+{typeOf:County}",
    date="2020"
)
```

### 2. Node 端点 - 知识图谱探索

探索知识图谱内的实体关系和属性。有关综合文档，请参阅 `references/node.md`。

**主要用例：**
- 发现实体的可用属性
- 导航地理层次结构（父/子关系）
- 检索实体名称和元数据
- 探索实体之间的连接
- 列出图谱中的所有实体类型

**常见模式：**
```python
# 发现属性
labels = client.node.fetch_property_labels(
    node_dcids=["geoId/06"],
    out=True
)

# 导航层次结构
children = client.node.fetch_place_children(
    node_dcids=["country/USA"]
)

# 获取实体名称
names = client.node.fetch_entity_names(
    node_dcids=["geoId/06", "geoId/48"]
)
```

### 3. Resolve 端点 - 实体标识

将实体名称、坐标或外部 ID 转换为 Data Commons ID（DCID）。有关综合文档，请参阅 `references/resolve.md`。

**主要用例：**
- 将地点名称转换为 DCID 以进行查询
- 将坐标解析为地点
- 将 Wikidata ID 映射到 Data Commons 实体
- 处理歧义的实体名称

**常见模式：**
```python
# 按名称解析
response = client.resolve.fetch_dcids_by_name(
    names=["California", "Texas"],
    entity_type="State"
)

# 按坐标解析
dcid = client.resolve.fetch_dcid_by_coordinates(
    latitude=37.7749,
    longitude=-122.4194
)

# 解析 Wikidata ID
response = client.resolve.fetch_dcids_by_wikidata_id(
    wikidata_ids=["Q30", "Q99"]
)
```

## 典型工作流

大多数 Data Commons 查询遵循此模式：

1. **解析实体**（如果从名称开始）：
   ```python
   resolve_response = client.resolve.fetch_dcids_by_name(
       names=["California", "Texas"]
   )
   dcids = [r["candidates"][0]["dcid"]
            for r in resolve_response.to_dict().values()
            if r["candidates"]]
   ```

2. **发现可用变量**（可选）：
   ```python
   variables = client.observation.fetch_available_statistical_variables(
       entity_dcids=dcids
   )
   ```

3. **查询统计数据**：
   ```python
   response = client.observation.fetch(
       variable_dcids=["Count_Person", "UnemploymentRate_Person"],
       entity_dcids=dcids,
       date="latest"
   )
   ```

4. **处理结果**：
   ```python
   # 作为字典
   data = response.to_dict()

   # 作为 Pandas DataFrame
   df = response.to_observations_as_records()
   ```

## 查找统计变量

Data Commons 中的统计变量使用特定的命名模式：

**常见变量模式：**
- `Count_Person` - 总人口
- `Count_Person_Female` - 女性人口
- `UnemploymentRate_Person` - 失业率
- `Median_Income_Household` - 家庭收入中位数
- `Count_Death` - 死亡人数
- `Median_Age_Person` - 年龄中位数

**发现方法：**
```python
# 检查实体可用的变量
available = client.observation.fetch_available_statistical_variables(
    entity_dcids=["geoId/06"]
)

# 或通过 Web 界面探索
# https://datacommons.org/tools/statvar
```

## 使用 Pandas

所有观测响应都与 Pandas 集成：

```python
response = client.observation.fetch(
    variable_dcids=["Count_Person"],
    entity_dcids=["geoId/06", "geoId/48"],
    date="all"
)

# 转换为 DataFrame
df = response.to_observations_as_records()
# 列：date、entity、variable、value

# 重塑以进行分析
pivot = df.pivot_table(
    values='value',
    index='date',
    columns='entity'
)
```

## API 身份验证

**对于 datacommons.org（默认）：**
- 需要 API 密钥
- 通过环境变量设置：`export DC_API_KEY="your_key"`
- 或在初始化时传递：`client = DataCommonsClient(api_key="your_key")`
- 在以下地址请求密钥：https://apikeys.datacommons.org/

**对于自定义 Data Commons 实例：**
- 不需要 API 密钥
- 指定自定义端点：`client = DataCommonsClient(url="https://custom.datacommons.org")`

## 参考文档

`references/` 目录中提供了每个端点的综合文档：

- **`references/observation.md`**：完整的 Observation API 文档，包括所有方法、参数、响应格式和常见用例
- **`references/node.md`**：完整的 Node API 文档，用于图谱探索、属性查询和层次结构导航
- **`references/resolve.md`**：完整的 Resolve API 文档，用于实体标识和 DCID 解析
- **`references/getting_started.md`**：快速入门指南，包含端到端示例和常见模式

## 其他资源

- **官方文档**：https://docs.datacommons.org/api/python/v2/
- **统计变量探索器**：https://datacommons.org/tools/statvar
- **Data Commons 浏览器**：https://datacommons.org/browser/
- **GitHub 仓库**：https://github.com/datacommonsorg/api-python

## 有效使用技巧

1. **始终从解析开始**：在查询数据之前将名称转换为 DCID
2. **对层次结构使用关系表达式**：一次性查询所有子项，而不是单独查询
3. **首先检查数据可用性**：使用 `fetch_available_statistical_variables()` 查看可查询的内容
4. **利用 Pandas 集成**：将响应转换为 DataFrames 进行分析
5. **缓存解析结果**：如果重复查询相同的实体，存储 name→DCID 映射
6. **按方面过滤以确保一致性**：使用 `filter_facet_domains` 确保来自同一来源的数据
7. **阅读参考文档**：每个端点在 `references/` 目录中都有大量文档
