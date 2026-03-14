---
name: seaborn
description: 带 pandas 集成的统计可视化。用于快速探索分布、关系和分类比较，具有吸引人的默认设置。最适用于箱线图、小提琴图、配对图、热力图。基于 matplotlib 构建。交互式图使用 plotly；出版物样式使用 scientific-visualization。
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# Seaborn 统计可视化

## 概述

Seaborn 是一个用于创建出版物质量统计图形的 Python 可视化库。使用此技能进行面向数据集的绘图、多元分析、自动统计估计和复杂的多面板图形，只需最少的代码。

## 设计理念

Seaborn 遵循以下核心原则：

1. **面向数据集**：直接处理 DataFrame 和命名变量，而非抽象坐标
2. **语义映射**：自动将数据值转换为视觉属性（颜色、大小、样式）
3. **统计感知**：内置聚合、误差估计和置信区间
4. **美学默认值**：开箱即用的出版物就绪主题和调色板
5. **Matplotlib 集成**：需要时完全兼容 matplotlib 自定义

## 快速入门

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# 加载示例数据集
df = sns.load_dataset('tips')

# 创建简单可视化
sns.scatterplot(data=df, x='total_bill', y='tip', hue='day')
plt.show()
```

## 核心绘图接口

### 函数接口（传统）

函数接口提供按可视化类型组织的专用绘图函数。每个类别都有**轴级**函数（绘制到单个轴）和**图级**函数（管理整个图形，带分面）。

**何时使用：**
- 快速探索性分析
- 单一用途可视化
- 当你需要特定的图表类型时

### 对象接口（现代）

`seaborn.objects` 接口提供类似 ggplot2 的声明式、可组合 API。通过链接方法来指定数据映射、标记、变换和尺度来构建可视化。

**何时使用：**
- 复杂的分层可视化
- 当你需要对变换进行精细控制时
- 构建自定义图表类型
- 程序化图表生成

```python
from seaborn import objects as so

# 声明式语法
(
    so.Plot(data=df, x='total_bill', y='tip')
    .add(so.Dot(), color='day')
    .add(so.Line(), so.PolyFit())
)
```

## 按类别分类的绘图函数

### 关系图（变量之间的关系）

**用途：** 探索两个或多个变量之间的关系

- `scatterplot()` - 将单个观察显示为点
- `lineplot()` - 显示趋势和变化（自动聚合并计算 CI）
- `relplot()` - 带自动分面的图级接口

**关键参数：**
- `x`, `y` - 主要变量
- `hue` - 附加分类/连续变量的颜色编码
- `size` - 点/线大小编码
- `style` - 标记/线样式编码
- `col`, `row` - 分面为多个子图（仅限图级）

```python
# 带有多个语义映射的散点图
sns.scatterplot(data=df, x='total_bill', y='tip',
                hue='time', size='size', style='sex')

# 带置信区间的线图
sns.lineplot(data=timeseries, x='date', y='value', hue='category')

# 分面关系图
sns.relplot(data=df, x='total_bill', y='tip',
            col='time', row='sex', hue='smoker', kind='scatter')
```

### 分布图（单变量和双变量分布）

**用途：** 了解数据分布、形状和概率密度

- `histplot()` - 带有灵活分箱的基于条形的频率分布
- `kdeplot()` - 使用高斯核的平滑密度估计
- `ecdfplot()` - 经验累积分布（无需调参）
- `rugplot()` - 单个观察刻度标记
- `displot()` - 用于单变量和双变量分布的图级接口
- `jointplot()` - 带边缘分布的双变量图
- `pairplot()` - 数据集中成对关系的矩阵

**关键参数：**
- `x`, `y` - 变量（单变量时 y 可选）
- `hue` - 按类别分离分布
- `stat` - 归一化："count"、"frequency"、"probability"、"density"
- `bins` / `binwidth` - 直方图分箱控制
- `bw_adjust` - KDE 带宽乘数（越高越平滑）
- `fill` - 填充曲线下方区域
- `multiple` - 如何处理 hue："layer"、"stack"、"dodge"、"fill"

```python
# 带密度归一化的直方图
sns.histplot(data=df, x='total_bill', hue='time',
             stat='density', multiple='stack')

# 带轮廓的双变量 KDE
sns.kdeplot(data=df, x='total_bill', y='tip',
            fill=True, levels=5, thresh=0.1)

# 带边缘分布的联合图
sns.jointplot(data=df, x='total_bill', y='tip',
              kind='scatter', hue='time')

# 成对关系
sns.pairplot(data=df, hue='species', corner=True)
```

### 分类图（跨类别的比较）

**用途：** 比较离散类别之间的分布或统计数据

**分类散点图：**
- `stripplot()` - 带抖动的点以显示所有观察
- `swarmplot()` - 非重叠点（蜜蜂群算法）

**分布比较：**
- `boxplot()` - 四分位数和离群值
- `violinplot()` - KDE + 四分位数信息
- `boxenplot()` - 大型数据集的增强箱线图

**统计估计：**
- `barplot()` - 带有置信区间的均值/聚合
- `pointplot()` - 带连接线的点估计
- `countplot()` - 每个类别的观察计数

**图级：**
- `catplot()` - 分面分类图（设置 `kind` 参数）

**关键参数：**
- `x`, `y` - 变量（通常一个是分类的）
- `hue` - 附加分类分组
- `order`, `hue_order` - 控制类别顺序
- `dodge` - 并排分离 hue 级别
- `orient` - "v"（垂直）或 "h"（水平）
- `kind` - catplot 的图类型："strip"、"swarm"、"box"、"violin"、"bar"、"point"

```python
# 显示所有点的 swarm 图
sns.swarmplot(data=df, x='day', y='total_bill', hue='sex')

# 带分割比较的小提琴图
sns.violinplot(data=df, x='day', y='total_bill',
               hue='sex', split=True)

# 带误差条的条形图
sns.barplot(data=df, x='day', y='total_bill',
            hue='sex', estimator='mean', errorbar='ci')

# 分面分类图
sns.catplot(data=df, x='day', y='total_bill',
            col='time', kind='box')
```

### 回归图（线性关系）

**用途：** 可视化线性回归和残差

- `regplot()` - 带散点 + 拟合线的轴级回归图
- `lmplot()` - 带分面支持的图级
- `residplot()` - 用于评估模型拟合的残差图

**关键参数：**
- `x`, `y` - 要回归的变量
- `order` - 多项式回归阶数
- `logistic` - 拟合逻辑回归
- `robust` - 使用稳健回归（对离群值不太敏感）
- `ci` - 置信区间宽度（默认 95）
- `scatter_kws`, `line_kws` - 自定义散点和线属性

```python
# 简单线性回归
sns.regplot(data=df, x='total_bill', y='tip')

# 带分面的多项式回归
sns.lmplot(data=df, x='total_bill', y='tip',
           col='time', order=2, ci=95)

# 检查残差
sns.residplot(data=df, x='total_bill', y='tip')
```

### 矩阵图（矩形数据）

**用途：** 可视化矩阵、相关性和网格结构数据

- `heatmap()` - 带注释的颜色编码矩阵
- `clustermap()` - 层次聚类热力图

**关键参数：**
- `data` - 二维矩形数据集（DataFrame 或数组）
- `annot` - 在单元格中显示值
- `fmt` - 注释的格式字符串（例如 ".2f"）
- `cmap` - 色图名称
- `center` - 色图中心的值（用于发散色图）
- `vmin`, `vmax` - 颜色尺度限制
- `square` - 强制方形单元格
- `linewidths` - 单元格之间的间隙

```python
# 相关性热力图
corr = df.corr()
sns.heatmap(corr, annot=True, fmt='.2f',
            cmap='coolwarm', center=0, square=True)

# 聚类热力图
sns.clustermap(data, cmap='viridis',
               standard_scale=1, figsize=(10, 10))
```

## 多图网格

Seaborn 提供用于创建复杂多面板图形的网格对象：

### FacetGrid

基于分类变量创建子图。最常用于通过图级函数（`relplot`、`displot`、`catplot`）调用，但也可以直接用于自定义图。

```python
g = sns.FacetGrid(df, col='time', row='sex', hue='smoker')
g.map(sns.scatterplot, 'total_bill', 'tip')
g.add_legend()
```

### PairGrid

显示数据集中所有变量之间的成对关系。

```python
g = sns.PairGrid(df, hue='species')
g.map_upper(sns.scatterplot)
g.map_lower(sns.kdeplot)
g.map_diag(sns.histplot)
g.add_legend()
```

### JointGrid

将双变量图与边缘分布结合。

```python
g = sns.JointGrid(data=df, x='total_bill', y='tip')
g.plot_joint(sns.scatterplot)
g.plot_marginals(sns.histplot)
```

## 图级与轴级函数

理解这种区别对于有效使用 seaborn 至关重要：

### 轴级函数
- 绘制到单个 matplotlib `Axes` 对象
- 易于集成到复杂的 matplotlib 图形中
- 接受 `ax=` 参数以精确定位
- 返回 `Axes` 对象
- 示例：`scatterplot`、`histplot`、`boxplot`、`regplot`、`heatmap`

**何时使用：**
- 构建自定义多图布局
- 组合不同的图类型
- 需要 matplotlib 级别的控制
- 与现有的 matplotlib 代码集成

```python
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
sns.scatterplot(data=df, x='x', y='y', ax=axes[0, 0])
sns.histplot(data=df, x='x', ax=axes[0, 1])
sns.boxplot(data=df, x='cat', y='y', ax=axes[1, 0])
sns.kdeplot(data=df, x='x', y='y', ax=axes[1, 1])
```

### 图级函数
- 管理整个图形，包括所有子图
- 通过 `col` 和 `row` 参数内置分面
- 返回 `FacetGrid`、`JointGrid` 或 `PairGrid` 对象
- 使用 `height` 和 `aspect` 进行大小调整（每子图）
- 无法放置在现有图形中
- 示例：`relplot`、`displot`、`catplot`、`lmplot`、`jointplot`、`pairplot`

**何时使用：**
- 分面可视化（小倍数）
- 快速探索性分析
- 一致的多面板布局
- 不需要与其他图类型组合

```python
# 自动分面
sns.relplot(data=df, x='x', y='y', col='category', row='group',
            hue='type', height=3, aspect=1.2)
```

## 数据结构要求

### 长格式数据（首选）

每个变量是一列，每个观察是一行。这种"整洁"格式提供最大的灵活性：

```python
# 长格式结构
   subject  condition  measurement
0        1    control         10.5
1        1  treatment         12.3
2        2    control          9.8
3        2  treatment         13.1
```

**优点：**
- 适用于所有 seaborn 函数
- 易于将变量重新映射到视觉属性
- 支持任意复杂性
- 适合 DataFrame 操作

### 宽格式数据

变量分布在列中。适用于简单的矩形数据：

```python
# 宽格式结构
   control  treatment
0     10.5       12.3
1      9.8       13.1
```

**用例：**
- 简单时间序列
- 相关矩阵
- 热力图
- 数组数据的快速绘图

**宽转长：**
```python
df_long = df.melt(var_name='condition', value_name='measurement')
```

## 调色板

Seaborn 为不同数据类型提供精心设计的调色板：

### 定性调色板（分类数据）

通过色调变化区分类别：
- `"deep"` - 默认，鲜艳的颜色
- `"muted"` - 更柔和，饱和度较低
- `"pastel"` - 浅，低饱和度
- `"bright"` - 高饱和度
- `"dark"` - 深色值
- `"colorblind"` - 对色觉缺陷安全

```python
sns.set_palette("colorblind")
sns.color_palette("Set2")
```

### 顺序调色板（有序数据）

显示从低到高值的进展：
- `"rocket"`, `"mako"` - 宽亮度范围（适合热力图）
- `"flare"`, `"crest"` - 受限亮度（适合点/线）
- `"viridis"`, `"magma"`, `"plasma"` - Matplotlib 感知均匀

```python
sns.heatmap(data, cmap='rocket')
sns.kdeplot(data=df, x='x', y='y', cmap='mako', fill=True)
```

### 发散调色板（居中数据）

强调从中点的偏差：
- `"vlag"` - 蓝到红
- `"icefire"` - 蓝到橙
- `"coolwarm"` - 冷到暖
- `"Spectral"` - 彩虹发散

```python
sns.heatmap(correlation_matrix, cmap='vlag', center=0)
```

### 自定义调色板

```python
# 创建自定义调色板
custom = sns.color_palette("husl", 8)

# 从浅到深渐变
palette = sns.light_palette("seagreen", as_cmap=True)

# 从色调创建发散调色板
palette = sns.diverging_palette(250, 10, as_cmap=True)
```

## 主题和美学

### 设置主题

`set_theme()` 控制整体外观：

```python
# 设置完整主题
sns.set_theme(style='whitegrid', palette='pastel', font='sans-serif')

# 重置为默认值
sns.set_theme()
```

### 样式

控制背景和网格外观：
- `"darkgrid"` - 灰色背景带白色网格（默认）
- `"whitegrid"` - 白色背景带灰色网格
- `"dark"` - 灰色背景，无网格
- `"white"` - 白色背景，无网格
- `"ticks"` - 白色背景带轴刻度

```python
sns.set_style("whitegrid")

# 移除边框
sns.despine(left=False, bottom=False, offset=10, trim=True)

# 临时样式
with sns.axes_style("white"):
    sns.scatterplot(data=df, x='x', y='y')
```

### 上下文

为不同用例缩放元素：
- `"paper"` - 最小（默认）
- `"notebook"` - 稍大
- `"talk"` - 演示幻灯片
- `"poster"` - 大格式

```python
sns.set_context("talk", font_scale=1.2)

# 临时上下文
with sns.plotting_context("poster"):
    sns.barplot(data=df, x='category', y='value')
```

## 最佳实践

### 1. 数据准备

始终使用结构良好的 DataFrame，带有有意义的列名：

```python
# 良好：DataFrame 中的命名列
df = pd.DataFrame({'bill': bills, 'tip': tips, 'day': days})
sns.scatterplot(data=df, x='bill', y='tip', hue='day')

# 避免：未命名数组
sns.scatterplot(x=x_array, y=y_array)  # 失去轴标签
```

### 2. 选择正确的图表类型

**连续 x，连续 y：** `scatterplot`、`lineplot`、`kdeplot`、`regplot`
**连续 x，分类 y：** `violinplot`、`boxplot`、`stripplot`、`swarmplot`
**一个连续变量：** `histplot`、`kdeplot`、`ecdfplot`
**相关性/矩阵：** `heatmap`、`clustermap`
**成对关系：** `pairplot`、`jointplot`

### 3. 使用图级函数进行分面

```python
# 替代手动子图创建
sns.relplot(data=df, x='x', y='y', col='category', col_wrap=3)

# 不：为简单分面手动创建子图
```

### 4. 利用语义映射

使用 `hue`、`size` 和 `style` 编码附加维度：

```python
sns.scatterplot(data=df, x='x', y='y',
                hue='category',      # 按类别着色
                size='importance',    # 按连续变量调整大小
                style='type')         # 按类型调整标记样式
```

### 5. 控制统计估计

许多函数自动计算统计数据。理解并自定义：

```python
# Lineplot 默认计算均值和 95% CI
sns.lineplot(data=df, x='time', y='value',
             errorbar='sd')  # 改为使用标准差

# Barplot 默认计算均值
sns.barplot(data=df, x='category', y='value',
            estimator='median',  # 改为使用中位数
            errorbar=('ci', 95))  # 自助法 CI
```

### 6. 与 Matplotlib 结合

Seaborn 与 matplotlib 无缝集成以进行微调：

```python
ax = sns.scatterplot(data=df, x='x', y='y')
ax.set(xlabel='自定义 X 标签', ylabel='自定义 Y 标签',
       title='自定义标题')
ax.axhline(y=0, color='r', linestyle='--')
plt.tight_layout()
```

### 7. 保存高质量图形

```python
fig = sns.relplot(data=df, x='x', y='y', col='group')
fig.savefig('figure.png', dpi=300, bbox_inches='tight')
fig.savefig('figure.pdf')  # 出版物的矢量格式
```

## 常见模式

### 探索性数据分析

```python
# 所有关系的快速概览
sns.pairplot(data=df, hue='target', corner=True)

# 分布探索
sns.displot(data=df, x='variable', hue='group',
            kind='kde', fill=True, col='category')

# 相关性分析
corr = df.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
```

### 出版物质量图形

```python
sns.set_theme(style='ticks', context='paper', font_scale=1.1)

g = sns.catplot(data=df, x='treatment', y='response',
                col='cell_line', kind='box', height=3, aspect=1.2)
g.set_axis_labels('治疗条件', '响应 (μM)')
g.set_titles('{col_name}')
sns.despine(trim=True)

g.savefig('figure.pdf', dpi=300, bbox_inches='tight')
```

### 复杂多面板图形

```python
# 将 matplotlib 子图与 seaborn 结合
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

sns.scatterplot(data=df, x='x1', y='y', hue='group', ax=axes[0, 0])
sns.histplot(data=df, x='x1', hue='group', ax=axes[0, 1])
sns.violinplot(data=df, x='group', y='y', ax=axes[1, 0])
sns.heatmap(df.pivot_table(values='y', index='x1', columns='x2'),
            ax=axes[1, 1], cmap='viridis')

plt.tight_layout()
```

### 带置信带的时间序列

```python
# Lineplot 自动聚合并显示 CI
sns.lineplot(data=timeseries, x='date', y='measurement',
             hue='sensor', style='location', errorbar='sd')

# 更多控制
g = sns.relplot(data=timeseries, x='date', y='measurement',
                col='location', hue='sensor', kind='line',
                height=4, aspect=1.5, errorbar=('ci', 95))
g.set_axis_labels('日期', '测量值 (单位)')
```

## 故障排除

### 问题：图例在图形区域外

图级函数默认将图例放在外面。要移到内部：

```python
g = sns.relplot(data=df, x='x', y='y', hue='category')
g._legend.set_bbox_to_anchor((0.9, 0.5))  # 调整位置
```

### 问题：标签重叠

```python
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
```

### 问题：图形太小

对于图级函数：
```python
sns.relplot(data=df, x='x', y='y', height=6, aspect=1.5)
```

对于轴级函数：
```python
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df, x='x', y='y', ax=ax)
```

### 问题：颜色不够明显

```python
# 使用不同的调色板
sns.set_palette("bright")

# 或指定颜色数量
palette = sns.color_palette("husl", n_colors=len(df['category'].unique()))
sns.scatterplot(data=df, x='x', y='y', hue='category', palette=palette)
```

### 问题：KDE 太平滑或锯齿状

```python
# 调整带宽
sns.kdeplot(data=df, x='x', bw_adjust=0.5)  # 不太平滑
sns.kdeplot(data=df, x='x', bw_adjust=2)    # 更平滑
```

## 资源

此技能包含用于深入探索的参考材料：

### references/

- `function_reference.md` - 所有 seaborn 函数的综合列表，带参数和示例
- `objects_interface.md` - 现代 seaborn.objects API 的详细指南
- `examples.md` - 不同分析场景的常见用例和代码模式

根据需要加载参考文件，获取详细的函数签名、高级参数或特定示例。