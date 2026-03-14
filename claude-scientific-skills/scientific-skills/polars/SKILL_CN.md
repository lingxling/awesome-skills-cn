---
name: polars
description: 用于适合RAM的数据集的快速内存中DataFrame库。当pandas太慢但数据仍适合内存时使用。惰性评估、并行执行、Apache Arrow后端。最适合1-100GB数据集、ETL管道、更快的pandas替代品。对于大于RAM的数据，使用dask或vaex。
license: https://github.com/pola-rs/polars/blob/main/LICENSE
metadata:
    skill-author: K-Dense Inc.
---

# Polars

## 概述

Polars是一个基于Apache Arrow构建的Python和Rust的闪电快速DataFrame库。使用Polars的基于表达式的API、惰性评估框架和高性能数据操作功能，进行高效数据处理、pandas迁移和数据管道优化。

## 快速开始

### 安装和基本使用

安装Polars：
```python
uv pip install polars
```

基本DataFrame创建和操作：
```python
import polars as pl

# 创建DataFrame
df = pl.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["NY", "LA", "SF"]
})

# 选择列
df.select("name", "age")

# 过滤行
df.filter(pl.col("age") > 25)

# 添加计算列
df.with_columns(
    age_plus_10=pl.col("age") + 10
)
```

## 核心概念

### 表达式

表达式是Polars操作的基本构建块。它们描述数据的转换，可以组合、重用和优化。

**关键原则：**
- 使用`pl.col("column_name")`引用列
- 链式方法构建复杂转换
- 表达式是惰性的，只在上下文中执行（select、with_columns、filter、group_by）

**示例：**
```python
# 基于表达式的计算
df.select(
    pl.col("name"),
    (pl.col("age") * 12).alias("age_in_months")
)
```

### 惰性vs即时评估

**即时（DataFrame）：** 操作立即执行
```python
df = pl.read_csv("file.csv")  # 立即读取
result = df.filter(pl.col("age") > 25)  # 立即执行
```

**惰性（LazyFrame）：** 操作构建查询计划，执行前优化
```python
lf = pl.scan_csv("file.csv")  # 尚未读取
result = lf.filter(pl.col("age") > 25).select("name", "age")
df = result.collect()  # 现在执行优化查询
```

**何时使用惰性：**
- 处理大型数据集
- 复杂查询管道
- 只需要部分列/行
- 性能至关重要

**惰性评估的好处：**
- 自动查询优化
- 谓词下推
- 投影下推
- 并行执行

有关详细概念，请加载`references/core_concepts.md`。

## 常见操作

### Select
选择和操作列：
```python
# 选择特定列
df.select("name", "age")

# 用表达式选择
df.select(
    pl.col("name"),
    (pl.col("age") * 2).alias("double_age")
)

# 选择匹配模式的所有列
df.select(pl.col("^.*_id$"))
```

### Filter
按条件过滤行：
```python
# 单个条件
df.filter(pl.col("age") > 25)

# 多个条件（比使用&更清晰）
df.filter(
    pl.col("age") > 25,
    pl.col("city") == "NY"
)

# 复杂条件
df.filter(
    (pl.col("age") > 25) | (pl.col("city") == "LA")
)
```

### With Columns
添加或修改列，同时保留现有列：
```python
# 添加新列
df.with_columns(
    age_plus_10=pl.col("age") + 10,
    name_upper=pl.col("name").str.to_uppercase()
)

# 并行计算（所有列并行计算）
df.with_columns(
    pl.col("value") * 10,
    pl.col("value") * 100,
)
```

### Group By and Aggregations
分组数据并计算聚合：
```python
# 基本分组
df.group_by("city").agg(
    pl.col("age").mean().alias("avg_age"),
    pl.len().alias("count")
)

# 多个分组键
df.group_by("city", "department").agg(
    pl.col("salary").sum()
)

# 条件聚合
df.group_by("city").agg(
    (pl.col("age") > 30).sum().alias("over_30")
)
```

有关详细操作模式，请加载`references/operations.md`。

## 聚合和窗口函数

### 聚合函数
`group_by`上下文中的常见聚合：
- `pl.len()` - 计数行
- `pl.col("x").sum()` - 求和值
- `pl.col("x").mean()` - 平均值
- `pl.col("x").min()` / `pl.col("x").max()` - 极值
- `pl.first()` / `pl.last()` - 第一个/最后一个值

### 使用`over()`的窗口函数
应用聚合同时保留行数：
```python
# 向每行添加分组统计
df.with_columns(
    avg_age_by_city=pl.col("age").mean().over("city"),
    rank_in_city=pl.col("salary").rank().over("city")
)

# 多个分组列
df.with_columns(
    group_avg=pl.col("value").mean().over("category", "region")
)
```

**映射策略：**
- `group_to_rows`（默认）：保留原始行顺序
- `explode`：更快但将分组行放在一起
- `join`：创建列表列

## 数据I/O

### 支持的格式
Polars支持读取和写入：
- CSV、Parquet、JSON、Excel
- 数据库（通过连接器）
- 云存储（S3、Azure、GCS）
- Google BigQuery
- 多个/分区文件

### 常见I/O操作

**CSV：**
```python
# 即时
df = pl.read_csv("file.csv")
df.write_csv("output.csv")

# 惰性（大文件首选）
lf = pl.scan_csv("file.csv")
result = lf.filter(...).select(...).collect()
```

**Parquet（性能推荐）：**
```python
df = pl.read_parquet("file.parquet")
df.write_parquet("output.parquet")
```

**JSON：**
```python
df = pl.read_json("file.json")
df.write_json("output.json")
```

有关全面的I/O文档，请加载`references/io_guide.md`。

## 转换

### Joins
合并DataFrames：
```python
# 内连接
df1.join(df2, on="id", how="inner")

# 左连接
df1.join(df2, on="id", how="left")

# 不同列名连接
df1.join(df2, left_on="user_id", right_on="id")
```

### Concatenation
堆叠DataFrames：
```python
# 垂直（堆叠行）
pl.concat([df1, df2], how="vertical")

# 水平（添加列）
pl.concat([df1, df2], how="horizontal")

# 对角线（不同模式的联合）
pl.concat([df1, df2], how="diagonal")
```

### Pivot and Unpivot
重塑数据：
```python
# Pivot（宽格式）
df.pivot(values="sales", index="date", columns="product")

# Unpivot（长格式）
df.unpivot(index="id", on=["col1", "col2"])
```

有关详细转换示例，请加载`references/transformations.md`。

## Pandas迁移

Polars提供比pandas显著的性能改进，同时拥有更简洁的API。关键差异：

### 概念差异
- **无索引**：Polars仅使用整数位置
- **严格类型**：无静默类型转换
- **惰性评估**：通过LazyFrame可用
- **默认并行**：操作自动并行化

### 常见操作映射

| 操作 | Pandas | Polars |
|-----------|--------|--------|
| 选择列 | `df["col"]` | `df.select("col")` |
| 过滤 | `df[df["col"] > 10]` | `df.filter(pl.col("col") > 10)` |
| 添加列 | `df.assign(x=...)` | `df.with_columns(x=...)` |
| 分组 | `df.groupby("col").agg(...)` | `df.group_by("col").agg(...)` |
| 窗口 | `df.groupby("col").transform(...)` | `df.with_columns(...).over("col")` |

### 关键语法模式

**Pandas顺序（慢）：**
```python
df.assign(
    col_a=lambda df_: df_.value * 10,
    col_b=lambda df_: df_.value * 100
)
```

**Polars并行（快）：**
```python
df.with_columns(
    col_a=pl.col("value") * 10,
    col_b=pl.col("value") * 100,
)
```

有关全面的迁移指南，请加载`references/pandas_migration.md`。

## 最佳实践

### 性能优化

1. **对大型数据集使用惰性评估：**
   ```python
   lf = pl.scan_csv("large.csv")  # 不要使用read_csv
   result = lf.filter(...).select(...).collect()
   ```

2. **避免热路径中的Python函数：**
   - 留在表达式API内以实现并行化
   - 仅在必要时使用`.map_elements()`
   - 优先使用原生Polars操作

3. **对非常大的数据使用流式处理：**
   ```python
   lf.collect(streaming=True)
   ```

4. **尽早选择所需列：**
   ```python
   # 好：尽早选择列
   lf.select("col1", "col2").filter(...)

   # 坏：先对所有列过滤
   lf.filter(...).select("col1", "col2")
   ```

5. **使用适当的数据类型：**
   - 低基数字符串使用分类
   - 适当的整数大小（i32 vs i64）
   - 时间数据使用日期类型

### 表达式模式

**条件操作：**
```python
pl.when(condition).then(value).otherwise(other_value)
```

**跨多列的列操作：**
```python
df.select(pl.col("^.*_value$") * 2)  # 正则模式
```

**空值处理：**
```python
pl.col("x").fill_null(0)
pl.col("x").is_null()
pl.col("x").drop_nulls()
```

有关其他最佳实践和模式，请加载`references/best_practices.md`。

## 资源

此技能包括全面的参考文档：

### references/
- `core_concepts.md` - 表达式、惰性评估和类型系统的详细解释
- `operations.md` - 所有常见操作的综合指南，带有示例
- `pandas_migration.md` - 从pandas到Polars的完整迁移指南
- `io_guide.md` - 所有支持格式的数据I/O操作
- `transformations.md` - 连接、连接、透视和重塑操作
- `best_practices.md` - 性能优化技巧和常见模式

当用户需要有关特定主题的详细信息时，根据需要加载这些参考。