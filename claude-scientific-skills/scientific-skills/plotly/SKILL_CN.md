---
name: plotly
description: 交互式可视化库。当需要悬停信息、缩放、平移或可嵌入网页的图表时使用。最适合仪表板、探索性分析和演示。对于静态出版图表，使用matplotlib或scientific-visualization。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# Plotly

Python图形库，用于创建交互式、出版质量的可视化，支持40+种图表类型。

## 快速开始

安装Plotly：
```bash
uv pip install plotly
```

使用Plotly Express（高级API）的基本用法：
```python
import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    'x': [1, 2, 3, 4],
    'y': [10, 11, 12, 13]
})

fig = px.scatter(df, x='x', y='y', title='我的第一个图表')
fig.show()
```

## 在API之间选择

### 使用Plotly Express (px)
对于具有合理默认值的快速、标准可视化：
- 使用pandas DataFrames
- 创建常见图表类型（散点图、折线图、柱状图、直方图等）
- 需要自动颜色编码和图例
- 希望使用最少的代码（1-5行）

完整指南见[reference/plotly-express.md](reference/plotly-express.md)。

### 使用Graph Objects (go)
对于细粒度控制和自定义可视化：
- Plotly Express中没有的图表类型（3D网格、等值面、复杂金融图表）
- 从头构建复杂的多轨迹图形
- 需要对各个组件进行精确控制
- 创建带有自定义形状和注释的专门可视化

完整指南见[reference/graph-objects.md](reference/graph-objects.md)。

**注意：** Plotly Express返回图形对象Figure，因此您可以结合使用两种方法：
```python
fig = px.scatter(df, x='x', y='y')
fig.update_layout(title='自定义标题')  # 在px图形上使用go方法
fig.add_hline(y=10)                     # 添加形状
```

## 核心功能

### 1. 图表类型

Plotly支持40+种图表类型，分为以下类别：

**基本图表：** 散点图、折线图、柱状图、饼图、面积图、气泡图

**统计图表：** 直方图、箱形图、小提琴图、分布图、误差条

**科学图表：** 热力图、等高线图、三元图、图像显示

**金融图表：** 烛台图、OHLC图、瀑布图、漏斗图、时间序列

**地图：** 散点地图、 choropleth图、密度地图（地理可视化）

**3D图表：** scatter3d、曲面图、网格图、锥形图、体积图

**专门图表：** 旭日图、树状图、桑基图、平行坐标图、仪表盘

所有图表类型的详细示例和用法见[reference/chart-types.md](reference/chart-types.md)。

### 2. 布局和样式

**子图：** 创建具有共享轴的多图图形：
```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(rows=2, cols=2, subplot_titles=('A', 'B', 'C', 'D'))
fig.add_trace(go.Scatter(x=[1, 2], y=[3, 4]), row=1, col=1)
```

**模板：** 应用协调的样式：
```python
fig = px.scatter(df, x='x', y='y', template='plotly_dark')
# 内置：plotly_white, plotly_dark, ggplot2, seaborn, simple_white
```

**自定义：** 控制外观的各个方面：
- 颜色（离散序列、连续尺度）
- 字体和文本
- 坐标轴（范围、刻度、网格）
- 图例
- 边距和大小
- 注释和形状

完整的布局和样式选项见[reference/layouts-styling.md](reference/layouts-styling.md)。

### 3. 交互性

内置交互功能：
- 带有可自定义数据的悬停提示
- 平移和缩放
- 图例切换
- 框/套索选择
- 时间序列的范围滑块
- 按钮和下拉菜单
- 动画

```python
# 自定义悬停模板
fig.update_traces(
    hovertemplate='<b>%{x}</b><br>值: %{y:.2f}<extra></extra>'
)

# 添加范围滑块
fig.update_xaxes(rangeslider_visible=True)

# 动画
fig = px.scatter(df, x='x', y='y', animation_frame='year')
```

完整的交互性指南见[reference/export-interactivity.md](reference/export-interactivity.md)。

### 4. 导出选项

**交互式HTML：**
```python
fig.write_html('chart.html')                       # 完整独立版
fig.write_html('chart.html', include_plotlyjs='cdn')  # 更小的文件
```

**静态图像（需要kaleido）：**
```bash
uv pip install kaleido
```

```python
fig.write_image('chart.png')   # PNG
fig.write_image('chart.pdf')   # PDF
fig.write_image('chart.svg')   # SVG
```

完整的导出选项见[reference/export-interactivity.md](reference/export-interactivity.md)。

## 常见工作流程

### 科学数据可视化

```python
import plotly.express as px

# 带趋势线的散点图
fig = px.scatter(df, x='温度', y='产量', trendline='ols')

# 从矩阵创建热力图
fig = px.imshow(correlation_matrix, text_auto=True, color_continuous_scale='RdBu')

# 3D曲面图
import plotly.graph_objects as go
fig = go.Figure(data=[go.Surface(z=z_data, x=x_data, y=y_data)])
```

### 统计分析

```python
# 分布比较
fig = px.histogram(df, x='values', color='group', marginal='box', nbins=30)

# 带所有点的箱形图
fig = px.box(df, x='category', y='value', points='all')

# 小提琴图
fig = px.violin(df, x='group', y='measurement', box=True)
```

### 时间序列和金融

```python
# 带范围滑块的时间序列
fig = px.line(df, x='date', y='price')
fig.update_xaxes(rangeslider_visible=True)

# 烛台图
import plotly.graph_objects as go
fig = go.Figure(data=[go.Candlestick(
    x=df['date'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close']
)])
```

### 多图仪表板

```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('散点图', '柱状图', '直方图', '箱形图'),
    specs=[[{'type': 'scatter'}, {'type': 'bar'}],
           [{'type': 'histogram'}, {'type': 'box'}]]
)

fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]), row=1, col=1)
fig.add_trace(go.Bar(x=['A', 'B'], y=[1, 2]), row=1, col=2)
fig.add_trace(go.Histogram(x=data), row=2, col=1)
fig.add_trace(go.Box(y=data), row=2, col=2)

fig.update_layout(height=800, showlegend=False)
```

## 与Dash集成

对于交互式Web应用，使用Dash（Plotly的Web应用框架）：

```bash
uv pip install dash
```

```python
import dash
from dash import dcc, html
import plotly.express as px

app = dash.Dash(__name__)

fig = px.scatter(df, x='x', y='y')

app.layout = html.Div([
    html.H1('仪表板'),
    dcc.Graph(figure=fig)
])

app.run_server(debug=True)
```

## 参考文件

- **[plotly-express.md](reference/plotly-express.md)** - 用于快速可视化的高级API
- **[graph-objects.md](reference/graph-objects.md)** - 用于细粒度控制的低级API
- **[chart-types.md](reference/chart-types.md)** - 40+种图表类型的完整目录及示例
- **[layouts-styling.md](reference/layouts-styling.md)** - 子图、模板、颜色、自定义
- **[export-interactivity.md](reference/export-interactivity.md)** - 导出选项和交互功能

## 其他资源

- 官方文档：https://plotly.com/python/
- API参考：https://plotly.com/python-api-reference/
- 社区论坛：https://community.plotly.com/