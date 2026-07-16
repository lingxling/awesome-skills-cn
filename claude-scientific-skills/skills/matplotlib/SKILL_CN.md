---
name: matplotlib
description: 用于完全自定义的低级绘图库。当您需要对每个绘图元素进行细粒度控制、创建新型绘图类型或与特定科学工作流集成时使用。导出为PNG/PDF/SVG用于出版。快速统计图表请使用seaborn；交互式图表请使用plotly；用于出版级多面板图表和期刊样式，请使用scientific-visualization。
allowed-tools:
  - Read
  - Write
  - Bash
license: https://github.com/matplotlib/matplotlib/tree/main/LICENSE
compatibility: 需要 Python 3.10+ 和 Matplotlib 3.10.x。在项目中使用 `uv add matplotlib` 安装；交互式 Jupyter 部件需要 `ipympl`。
metadata: {"version": "1.1", "skill-author": "K-Dense Inc."}
---

# Matplotlib

## 概述

Matplotlib 是 Python 的基础可视化库，用于创建静态、动画和交互式图表。此技能提供有效使用 matplotlib 的指导，涵盖 pyplot 接口（MATLAB 风格）和面向对象 API（Figure/Axes）两种方式，以及创建出版质量可视化图表的最佳实践。

## 何时使用此技能

此技能应在以下情况下使用：
- 创建任何类型的图表（线图、散点图、柱状图、直方图、热图、等高线图等）
- 生成科学或统计可视化图表
- 自定义图表外观（颜色、样式、标签、图例）
- 创建带有子图的多面板图表
- 将可视化图表导出为多种格式（PNG、PDF、SVG 等）
- 构建交互式图表或动画
- 处理 3D 可视化
- 将图表集成到 Jupyter notebook 或 GUI 应用程序中

## 安装设置

对于项目工作，使用 uv 安装 Matplotlib：

```bash
uv add matplotlib
```

对于 notebook 交互性：

```bash
uv add matplotlib ipympl
```

然后在 Jupyter 中使用 `%matplotlib widget` 或 `%matplotlib ipympl` 启用部件后端。

Matplotlib 3.10 需要 Python 3.10+ 和 NumPy 1.23+。非交互式文件输出通过 Agg、PDF、SVG 等后端实现。对于 GUI 窗口，Matplotlib 会自动选择可用的后端；如果在 uv 管理的 Python 中 `TkAgg` 失败，请使用 `uv self update` 和 `uv python upgrade --reinstall` 更新 uv 和 Python 构建版本，或使用 `uv add pyside6` 安装 Qt 后端。

## 核心概念

### Matplotlib 层次结构

Matplotlib 使用分层的对象结构：

1. **Figure（图形）** - 所有绘图元素的顶层容器
2. **Axes（坐标轴区域）** - 显示数据的实际绘图区域（一个 Figure 可以包含多个 Axes）
3. **Artist（画师）** - 图形上所有可见的元素（线条、文本、刻度等）
4. **Axis（轴）** - 处理刻度和标签的数轴对象（x 轴、y 轴）

### 两种接口

**1. pyplot 接口（隐式，MATLAB 风格）**
```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3, 4])
plt.ylabel('some numbers')
plt.show()
```
- 便于快速、简单的绘图
- 自动维护状态
- 适合交互式工作和简单脚本

**2. 面向对象接口（显式）**
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4])
ax.set_ylabel('some numbers')
plt.show()
```
- **推荐用于大多数场景**
- 对图形和坐标轴有更明确的控制
- 更适合有多个子图的复杂图形
- 更易于维护和调试

## 常见工作流

### 1. 基本绘图创建

**单个图表工作流：**
```python
import matplotlib.pyplot as plt
import numpy as np

# 创建图形和坐标轴（面向对象接口 - 推荐）
fig, ax = plt.subplots(figsize=(10, 6))

# 生成并绘制数据
x = np.linspace(0, 2*np.pi, 100)
ax.plot(x, np.sin(x), label='sin(x)')
ax.plot(x, np.cos(x), label='cos(x)')

# 自定义
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Trigonometric Functions')
ax.legend()
ax.grid(True, alpha=0.3)

# 保存和/或显示
fig.savefig('plot.png', dpi=300, bbox_inches='tight')
plt.show()
```

### 2. 多个子图

**创建子图布局：**
```python
# 方法1：常规网格
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes[0, 0].plot(x, y1)
axes[0, 1].scatter(x, y2)
axes[1, 0].bar(categories, values)
axes[1, 1].hist(data, bins=30)

# 方法2：马赛克布局（更灵活）
fig, axes = plt.subplot_mosaic([['left', 'right_top'],
                                 ['left', 'right_bottom']],
                                figsize=(10, 8))
axes['left'].plot(x, y)
axes['right_top'].scatter(x, y)
axes['right_bottom'].hist(data)

# 方法3：GridSpec（最大控制权）
from matplotlib.gridspec import GridSpec
fig = plt.figure(figsize=(12, 8))
gs = GridSpec(3, 3, figure=fig)
ax1 = fig.add_subplot(gs[0, :])  # 顶行，所有列
ax2 = fig.add_subplot(gs[1:, 0])  # 底部两行，第一列
ax3 = fig.add_subplot(gs[1:, 1:])  # 底部两行，最后两列
```

### 3. 图表类型和使用场景

**线图** - 时间序列、连续数据、趋势
```python
ax.plot(x, y, linewidth=2, linestyle='--', marker='o', color='blue')
```

**散点图** - 变量之间的关系、相关性
```python
ax.scatter(x, y, s=sizes, c=colors, alpha=0.6, cmap='viridis')
```

**柱状图** - 分类比较
```python
ax.bar(categories, values, color='steelblue', edgecolor='black')
# 水平柱状图：
ax.barh(categories, values)
```

**直方图** - 分布
```python
ax.hist(data, bins=30, edgecolor='black', alpha=0.7)
```

**热图** - 矩阵数据、相关性
```python
im = ax.imshow(matrix, cmap='coolwarm', aspect='auto')
plt.colorbar(im, ax=ax)
```

**等高线图** - 二维平面上的三维数据
```python
contour = ax.contour(X, Y, Z, levels=10)
ax.clabel(contour, inline=True, fontsize=8)
```

**箱线图** - 统计分布
```python
ax.boxplot([data1, data2, data3], tick_labels=['A', 'B', 'C'])
```

**小提琴图** - 分布密度
```python
ax.violinplot([data1, data2, data3], positions=[1, 2, 3])
```

有关全面的图表类型示例和变体，请参阅 `references/plot_types.md`。

### 4. 样式和自定义

**颜色指定方法：**
- 命名颜色：`'red'`、`'blue'`、`'steelblue'`
- 十六进制代码：`'#FF5733'`
- RGB 元组：`(0.1, 0.2, 0.3)`
- 颜色映射：`cmap='viridis'`、`cmap='plasma'`、`cmap='coolwarm'`

**使用样式表：**
```python
plt.style.use('seaborn-v0_8-darkgrid')  # 应用预定义样式
# 可用样式：'ggplot'、'bmh'、'fivethirtyeight' 等
print(plt.style.available)  # 列出所有可用样式
```

**使用 rcParams 自定义：**
```python
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['figure.titlesize'] = 18
```

**文本和注释：**
```python
ax.text(x, y, 'annotation', fontsize=12, ha='center')
ax.annotate('important point', xy=(x, y), xytext=(x+1, y+1),
            arrowprops=dict(arrowstyle='->', color='red'))
```

有关详细的样式选项和颜色映射指南，请参阅 `references/styling_guide.md`。

### 5. 保存图形

**导出为多种格式：**
```python
# 用于演示/论文的高分辨率 PNG
fig.savefig('figure.png', dpi=300, bbox_inches='tight', facecolor='white')

# 用于出版的矢量格式（可缩放）
fig.savefig('figure.pdf', bbox_inches='tight')
fig.savefig('figure.svg', bbox_inches='tight')

# 透明背景
fig.savefig('figure.png', dpi=300, bbox_inches='tight', transparent=True)
```

**重要参数：**
- `dpi`：分辨率（出版物用 300，网页用 150，屏幕用 72）
- `bbox_inches='tight'`：移除多余空白
- `facecolor='white'`：确保白色背景（对透明主题有用）
- `transparent=True`：透明背景

### 6. 处理 3D 图形

```python
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 曲面图
ax.plot_surface(X, Y, Z, cmap='viridis')

# 3D 散点图
ax.scatter(x, y, z, c=colors, marker='o')

# 3D 线图
ax.plot(x, y, z, linewidth=2)

# 标签
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
```

## 最佳实践

### 1. 接口选择
- 生产代码中**使用面向对象接口**（`fig, ax = plt.subplots()`）
- 仅将 pyplot 接口保留用于快速交互式探索
- 始终显式创建图形，而不是依赖隐式状态

### 2. 图形大小和 DPI
- 在创建时设置 figsize：`fig, ax = plt.subplots(figsize=(10, 6))`
- 为输出媒介使用合适的 DPI：
  - 屏幕/notebook：72-100 dpi
  - 网页：150 dpi
  - 印刷/出版物：300 dpi

### 3. 布局管理
- 使用 `constrained_layout=True` 或 `tight_layout()` 防止元素重叠
- 推荐使用 `fig, ax = plt.subplots(constrained_layout=True)` 实现自动间距

### 4. 颜色映射选择
- **顺序型**（viridis、plasma、inferno）：具有一致渐进关系的有序数据
- **发散型**（coolwarm、RdBu）：具有有意义中心点的数据（例如零）
- **定性型**（tab10、Set3）：分类/名义数据
- 避免使用彩虹色映射（jet）——它们在感知上不均匀

### 5. 可访问性
- 使用色盲友好的颜色映射（viridis、cividis）
- 除颜色外，为柱状图添加图案/阴影线
- 确保元素之间有足够的对比度
- 包含描述性标签和图例

### 6. 性能
- 对于大型数据集，在绘图调用中使用 `rasterized=True` 以减小文件大小
- 在绘图前进行适当的数据缩减（例如对密集时间序列进行降采样）
- 对于动画，使用 blitting 以获得更好的性能

### 7. 代码组织
```python
# 良好实践：清晰的结构
def create_analysis_plot(data, title):
    """Create standardized analysis plot."""
    fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

    # 绘制数据
    ax.plot(data['x'], data['y'], linewidth=2)

    # 自定义
    ax.set_xlabel('X Axis Label', fontsize=12)
    ax.set_ylabel('Y Axis Label', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)

    return fig, ax

# 使用该函数
fig, ax = create_analysis_plot(my_data, 'My Analysis')
fig.savefig('analysis.png', dpi=300, bbox_inches='tight')
```

## 快速参考脚本

此技能在 `scripts/` 目录中包含辅助脚本：

### `plot_template.py`
展示各种图表类型及最佳实践的模板脚本。将其用作创建新可视化图表的起点。

**用法：**
```bash
uv run python scripts/plot_template.py
```

### `style_configurator.py`
用于配置 matplotlib 样式偏好并生成自定义样式表的交互式工具。

**用法：**
```bash
uv run python scripts/style_configurator.py
```

## 详细参考

有关全面的信息，请查阅参考文档：

- **`references/plot_types.md`** - 包含代码示例和使用场景的完整图表类型目录
- **`references/styling_guide.md`** - 详细的样式选项、颜色映射和自定义
- **`references/api_reference.md`** - 核心类和方法参考
- **`references/common_issues.md`** - 常见问题的故障排除指南

## 与其他工具的集成

Matplotlib 与以下工具集成良好：
- **NumPy/Pandas** - 直接从数组和 DataFrame 绘图
- **Seaborn** - 基于 matplotlib 构建的高级统计可视化
- **Jupyter** - 使用 `%matplotlib inline` 或 `%matplotlib widget` 进行交互式绘图
- **GUI 框架** - 嵌入到 Tkinter、Qt、wxPython 应用程序中

## 常见陷阱

1. **元素重叠**：使用 `constrained_layout=True` 或 `tight_layout()`
2. **状态混乱**：使用面向对象接口以避免 pyplot 状态机问题
3. **多图形导致的内存问题**：使用 `plt.close(fig)` 显式关闭图形
4. **字体警告**：安装字体或使用 `plt.rcParams['font.sans-serif']` 抑制警告
5. **DPI 混淆**：记住 figsize 的单位是英寸，而不是像素：`像素 = dpi * 英寸`

## 其他资源

- 官方文档：https://matplotlib.org/
- 图库：https://matplotlib.org/stable/gallery/index.html
- 速查表：https://matplotlib.org/cheatsheets/
- 教程：https://matplotlib.org/stable/tutorials/index.html
