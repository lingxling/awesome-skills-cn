---
name: matplotlib
description: Python数据可视化库。创建各种图表和图形，包括线图、散点图、柱状图、饼图、直方图、箱线图、热图、3D图、极坐标图、等高线图等。支持自定义样式、图例、注释、动画和交互式图表。适用于科学计算、数据分析、机器学习结果可视化和报告生成。
license: PSF license
metadata:
    skill-author: K-Dense Inc.
---

# Matplotlib

## 概述

Matplotlib是Python的数据可视化库，用于创建各种图表和图形，包括线图、散点图、柱状图、饼图、直方图、箱线图、热图、3D图、极坐标图、等高线图等。该库支持自定义样式、图例、注释、动画和交互式图表，适用于科学计算、数据分析、机器学习结果可视化和报告生成。

## 核心能力

### 1. 基本图表

- **线图**：显示数据随时间的变化
- **散点图**：显示两个变量之间的关系
- **柱状图**：比较不同类别的数据
- **饼图**：显示数据的比例分布
- **直方图**：显示数据的分布

### 2. 统计图表

- **箱线图**：显示数据的分布和异常值
- **小提琴图**：显示数据的分布密度
- **误差条图**：显示数据的误差范围
- **Q-Q图**：比较数据分布与理论分布

### 3. 热图和等高线图

- **热图**：显示矩阵数据的热图
- **等高线图**：显示函数的等高线
- **填充等高线图**：显示填充的等高线

### 4. 3D图形

- **3D散点图**：显示三维数据
- **3D线图**：显示三维线图
- **3D曲面图**：显示三维曲面
- **3D柱状图**：显示三维柱状图

### 5. 极坐标图

- **极坐标散点图**：在极坐标系中显示数据
- **极坐标线图**：在极坐标系中显示线图
- **极坐标柱状图**：在极坐标系中显示柱状图

### 6. 自定义样式

- **样式表**：使用预定义样式表
- **自定义样式**：自定义颜色、线型、标记等
- **图例**：添加和自定义图例
- **注释**：添加文本注释和箭头

### 7. 动画

- **简单动画**：创建简单的动画
- **复杂动画**：创建复杂的动画
- **保存动画**：保存动画为视频或GIF

### 8. 交互式图表

- **交互式缩放**：交互式缩放图表
- **交互式平移**：交互式平移图表
- **交互式选择**：交互式选择数据

## 何时使用此技能

在以下情况下使用此技能：
- 创建数据可视化图表
- 可视化科学计算结果
- 可视化数据分析结果
- 可视化机器学习结果
- 生成报告和演示文稿
- 创建交互式图表
- 创建动画

## 安装

```bash
pip install matplotlib
```

## 使用示例

### 基本线图

```python
import matplotlib.pyplot as plt
import numpy as np

# 准备数据
x = np.linspace(0, 10, 100)
y = np.sin(x)

# 创建图表
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='sin(x)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('正弦函数')
plt.legend()
plt.grid(True)
plt.show()
```

### 散点图

```python
import matplotlib.pyplot as plt
import numpy as np

# 准备数据
x = np.random.randn(100)
y = np.random.randn(100)

# 创建散点图
plt.figure(figsize=(10, 6))
plt.scatter(x, y, alpha=0.5)
plt.xlabel('x')
plt.ylabel('y')
plt.title('散点图')
plt.grid(True)
plt.show()
```

### 柱状图

```python
import matplotlib.pyplot as plt
import numpy as np

# 准备数据
categories = ['A', 'B', 'C', 'D', 'E']
values = [20, 35, 30, 35, 27]

# 创建柱状图
plt.figure(figsize=(10, 6))
plt.bar(categories, values)
plt.xlabel('类别')
plt.ylabel('值')
plt.title('柱状图')
plt.grid(True)
plt.show()
```

### 饼图

```python
import matplotlib.pyplot as plt
import numpy as np

# 准备数据
labels = ['A', 'B', 'C', 'D']
sizes = [15, 30, 45, 10]

# 创建饼图
plt.figure(figsize=(10, 6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.title('饼图')
plt.show()
```

### 直方图

```python
import matplotlib.pyplot as plt
import numpy as np

# 准备数据
data = np.random.randn(1000)

# 创建直方图
plt.figure(figsize=(10, 6))
plt.hist(data, bins=30, alpha=0.7)
plt.xlabel('值')
plt.ylabel('频数')
plt.title('直方图')
plt.grid(True)
plt.show()
```

### 箱线图

```python
import matplotlib.pyplot as plt
import numpy as np

# 准备数据
data = [np.random.randn(100) for _ in range(5)]

# 创建箱线图
plt.figure(figsize=(10, 6))
plt.boxplot(data)
plt.xlabel('类别')
plt.ylabel('值')
plt.title('箱线图')
plt.grid(True)
plt.show()
```

### 热图

```python
import matplotlib.pyplot as plt
import numpy as np

# 准备数据
data = np.random.randn(10, 10)

# 创建热图
plt.figure(figsize=(10, 8))
plt.imshow(data, cmap='hot', interpolation='nearest')
plt.colorbar()
plt.title('热图')
plt.show()
```

### 3D图形

```python
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# 准备数据
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

# 创建3D曲面图
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='viridis')
fig.colorbar(surf)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('3D曲面图')
plt.show()
```

### 子图

```python
import matplotlib.pyplot as plt
import numpy as np

# 准备数据
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# 创建子图
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# 第一个子图
ax1.plot(x, y1, label='sin(x)')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_title('正弦函数')
ax1.legend()
ax1.grid(True)

# 第二个子图
ax2.plot(x, y2, label='cos(x)', color='orange')
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.set_title('余弦函数')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()
```

### 自定义样式

```python
import matplotlib.pyplot as plt
import numpy as np

# 准备数据
x = np.linspace(0, 10, 100)
y = np.sin(x)

# 使用样式
plt.style.use('seaborn')

# 创建图表
plt.figure(figsize=(10, 6))
plt.plot(x, y, linewidth=2, color='blue', label='sin(x)')
plt.xlabel('x', fontsize=12)
plt.ylabel('y', fontsize=12)
plt.title('正弦函数', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.show()
```

### 动画

```python
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# 准备数据
x = np.linspace(0, 2*np.pi, 100)

# 创建图表
fig, ax = plt.subplots(figsize=(10, 6))
line, = ax.plot([], [], lw=2)

# 初始化函数
def init():
    line.set_data([], [])
    return line,

# 更新函数
def update(frame):
    y = np.sin(x + frame/10.0)
    line.set_data(x, y)
    return line,

# 创建动画
ani = FuncAnimation(fig, update, frames=100, init_func=init, blit=True)

plt.xlabel('x')
plt.ylabel('y')
plt.title('动画')
plt.grid(True)
plt.show()
```

## 最佳实践

1. **图表选择**：选择合适的图表类型
2. **标签和标题**：添加清晰的标签和标题
3. **图例**：添加图例以解释图表
4. **样式**：使用一致的样式
5. **颜色**：使用色盲友好的颜色
6. **字体大小**：使用合适的字体大小
7. **保存图表**：保存图表为高分辨率
8. **交互性**：考虑使用交互式库

## 常见问题

**Q: 如何保存图表？**
A: 使用 `plt.savefig('filename.png', dpi=300)` 保存图表。

**Q: 如何创建子图？**
A: 使用 `plt.subplots()` 或 `plt.subplot()` 创建子图。

**Q: 如何自定义样式？**
A: 使用 `plt.style.use('style_name')` 或手动设置样式。

**Q: 如何创建动画？**
A: 使用 `FuncAnimation` 创建动画。

## 资源

- **Matplotlib文档**：https://matplotlib.org/stable/contents.html
- **Matplotlib示例**：https://matplotlib.org/stable/gallery/index.html
- **Matplotlib教程**：https://matplotlib.org/stable/tutorials/index.html
