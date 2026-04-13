---
name: scientific-visualization
description: 用于生成可直接发表的科学图表的元技能。适用于创建需要多面板布局、显著性标注、误差条、色盲友好调色板以及特定期刊格式（Nature、Science、Cell）的期刊投稿图表。协调使用matplotlib/seaborn/plotly与发表样式。快速探索可直接使用seaborn或plotly。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# 科学可视化

## 概述

科学可视化将数据转化为清晰、准确的图表用于发表。创建具有多面板布局、误差条、显著性标记和色盲友好调色板的期刊级图表。使用matplotlib、seaborn和plotly以PDF/EPS/TIFF格式导出用于手稿。

## 何时使用此技能

当以下情况时应使用此技能：
- 为科学手稿创建图表或可视化
- 准备用于期刊投稿的图表（Nature、Science、Cell、PLOS等）
- 确保图表对色盲友好且可访问
- 制作具有一致样式的多面板图表
- 以正确的分辨率和格式导出图表
- 遵循特定的出版指南
- 改进现有图表以满足出版标准
- 创建需要在彩色和灰度下都能正常显示的图表

## 快速入门指南

### 基本出版质量图表

```python
import matplotlib.pyplot as plt
import numpy as np

# 应用出版样式（来自scripts/style_presets.py）
from style_presets import apply_publication_style
apply_publication_style('default')

# 创建适当大小的图表（单列 = 3.5英寸）
fig, ax = plt.subplots(figsize=(3.5, 2.5))

# 绘制数据
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), label='sin(x)')
ax.plot(x, np.cos(x), label='cos(x)')

# 正确标注单位
ax.set_xlabel('时间 (秒)')
ax.set_ylabel('振幅 (mV)')
ax.legend(frameon=False)

# 移除不必要的边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 以出版格式保存（来自scripts/figure_export.py）
from figure_export import save_publication_figure
save_publication_figure(fig, 'figure1', formats=['pdf', 'png'], dpi=300)
```

### 使用预配置样式

使用`assets/`中的matplotlib样式文件应用期刊特定样式：

```python
import matplotlib.pyplot as plt

# 选项1：直接使用样式文件
plt.style.use('assets/nature.mplstyle')

# 选项2：使用style_presets.py辅助函数
from style_presets import configure_for_journal
configure_for_journal('nature', figure_width='single')

# 现在创建图表 - 它们将自动匹配Nature规范
fig, ax = plt.subplots()
# ... 你的绘图代码 ...
```

### 使用Seaborn快速入门

对于统计图表，使用带有出版样式的seaborn：

```python
import seaborn as sns
import matplotlib.pyplot as plt
from style_presets import apply_publication_style

# 应用出版样式
apply_publication_style('default')
sns.set_theme(style='ticks', context='paper', font_scale=1.1)
sns.set_palette('colorblind')

# 创建统计比较图表
fig, ax = plt.subplots(figsize=(3.5, 3))
sns.boxplot(data=df, x='treatment', y='response', 
            order=['Control', 'Low', 'High'], palette='Set2', ax=ax)
sns.stripplot(data=df, x='treatment', y='response',
              order=['Control', 'Low', 'High'], 
              color='black', alpha=0.3, size=3, ax=ax)
ax.set_ylabel('响应 (μM)')
sns.despine()

# 保存图表
from figure_export import save_publication_figure
save_publication_figure(fig, 'treatment_comparison', formats=['pdf', 'png'], dpi=300)
```

## 核心原则和最佳实践

### 1. 分辨率和文件格式

**关键要求**（详见`references/publication_guidelines.md`）：
- **栅格图像**（照片、显微镜）：300-600 DPI
- **线条艺术**（图表、绘图）：600-1200 DPI或矢量格式
- **矢量格式**（首选）：PDF、EPS、SVG
- **栅格格式**：TIFF、PNG（科学数据绝不要使用JPEG）

**实现：**
```python
# 使用figure_export.py脚本获取正确设置
from figure_export import save_publication_figure

# 以适当的DPI保存为多种格式
save_publication_figure(fig, 'myfigure', formats=['pdf', 'png'], dpi=300)

# 或根据特定期刊要求保存
from figure_export import save_for_journal
save_for_journal(fig, 'figure1', journal='nature', figure_type='combination')
```

### 2. 颜色选择 - 色盲可访问性

**始终使用色盲友好的调色板**（详见`references/color_palettes.md`）：

**推荐：Okabe-Ito调色板**（所有类型的色盲都可区分）：
```python
# 选项1：使用assets/color_palettes.py
from color_palettes import OKABE_ITO_LIST, apply_palette
apply_palette('okabe_ito')

# 选项2：手动指定
okabe_ito = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
             '#0072B2', '#D55E00', '#CC79A7', '#000000']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=okabe_ito)
```

**对于热图/连续数据：**
- 使用感知均匀的颜色映射：`viridis`、`plasma`、`cividis`
- 避免红绿发散映射（改用`PuOr`、`RdBu`、`BrBG`）
- 绝不要使用`jet`或`rainbow`颜色映射

**始终在灰度下测试图表**以确保可解释性。

### 3. 排版和文本

**字体指南**（详见`references/publication_guidelines.md`）：
- 无衬线字体：Arial、Helvetica、Calibri
- **最终打印尺寸**的最小大小：
  - 轴标签：7-9 pt
  - 刻度标签：6-8 pt
  - 面板标签：8-12 pt（粗体）
- 标签使用句子大小写："Time (hours)" 而不是 "TIME (HOURS)"
- 始终在括号中包含单位

**实现：**
```python
# 全局设置字体
import matplotlib as mpl
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Arial', 'Helvetica']
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.labelsize'] = 9
mpl.rcParams['xtick.labelsize'] = 7
mpl.rcParams['ytick.labelsize'] = 7
```

### 4. 图表尺寸

**期刊特定宽度**（详见`references/journal_requirements.md`）：
- **Nature**：单列89 mm，双列183 mm
- **Science**：单列55 mm，双列175 mm
- **Cell**：单列85 mm，双列178 mm

**检查图表尺寸合规性：**
```python
from figure_export import check_figure_size

fig = plt.figure(figsize=(3.5, 3))  # Nature的89 mm
check_figure_size(fig, journal='nature')
```

### 5. 多面板图表

**最佳实践：**
- 用粗体字母标记面板：**A**、**B**、**C**（大多数期刊使用大写，Nature使用小写）
- 保持所有面板样式一致
- 尽可能沿边缘对齐面板
- 在面板之间使用足够的空白

**示例实现**（完整代码见`references/matplotlib_examples.md`）：
```python
from string import ascii_uppercase

fig = plt.figure(figsize=(7, 4))
gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.4)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
# ... 创建其他面板 ...

# 添加面板标签
for i, ax in enumerate([ax1, ax2, ...]):
    ax.text(-0.15, 1.05, ascii_uppercase[i], transform=ax.transAxes,
            fontsize=10, fontweight='bold', va='top')
```

## 常见任务

### 任务1：创建可发表的折线图

完整代码见`references/matplotlib_examples.md`示例1。

**关键步骤：**
1. 应用出版样式
2. 为目标期刊设置适当的图表大小
3. 使用色盲友好的颜色
4. 添加具有正确表示的误差条（SEM、SD或CI）
5. 为轴添加单位标签
6. 移除不必要的边框
7. 以矢量格式保存

**使用seaborn自动计算置信区间：**
```python
import seaborn as sns
fig, ax = plt.subplots(figsize=(5, 3))
sns.lineplot(data=timeseries, x='time', y='measurement',
             hue='treatment', errorbar=('ci', 95), 
             markers=True, ax=ax)
ax.set_xlabel('时间 (小时)')
ax.set_ylabel('测量值 (AU)')
sns.despine()
```

### 任务2：创建多面板图表

完整代码见`references/matplotlib_examples.md`示例2。

**关键步骤：**
1. 使用`GridSpec`进行灵活布局
2. 确保面板间样式一致
3. 添加粗体面板标签（A、B、C等）
4. 对齐相关面板
5. 验证最终尺寸下所有文本可读

### 任务3：创建具有适当颜色映射的热图

完整代码见`references/matplotlib_examples.md`示例4。

**关键步骤：**
1. 使用感知均匀的颜色映射（`viridis`、`plasma`、`cividis`）
2. 包含带标签的颜色条
3. 对于发散数据，使用色盲友好的发散映射（`RdBu_r`、`PuOr`）
4. 为发散映射设置适当的中心值
5. 测试灰度外观

**使用seaborn创建相关矩阵：**
```python
import seaborn as sns
fig, ax = plt.subplots(figsize=(5, 4))
corr = df.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f',
            cmap='RdBu_r', center=0, square=True,
            linewidths=1, cbar_kws={'shrink': 0.8}, ax=ax)
```

### 任务4：为特定期刊准备图表

**工作流程：**
1. 检查期刊要求：`references/journal_requirements.md`
2. 为期刊配置matplotlib：
   ```python
   from style_presets import configure_for_journal
   configure_for_journal('nature', figure_width='single')
   ```
3. 创建图表（将自动正确调整大小）
4. 按期刊规范导出：
   ```python
   from figure_export import save_for_journal
   save_for_journal(fig, 'figure1', journal='nature', figure_type='line_art')
   ```

### 任务5：修复现有图表以满足出版标准

**清单方法**（完整清单见`references/publication_guidelines.md`）：

1. **检查分辨率**：验证DPI是否满足期刊要求
2. **检查文件格式**：使用矢量格式绘制图表，使用TIFF/PNG格式处理图像
3. **检查颜色**：确保对色盲友好
4. **检查字体**：最终尺寸下最小6-7 pt，无衬线
5. **检查标签**：所有轴都有单位标签
6. **检查尺寸**：符合期刊列宽
7. **测试灰度**：图表在没有颜色的情况下可解释
8. **移除图表垃圾**：无不必要的网格、3D效果、阴影

### 任务6：创建色盲友好的可视化

**策略：**
1. 使用`assets/color_palettes.py`中的批准调色板
2. 添加冗余编码（线条样式、标记、图案）
3. 用色盲模拟器测试
4. 确保灰度兼容性

**示例：**
```python
from color_palettes import apply_palette
import matplotlib.pyplot as plt

apply_palette('okabe_ito')

# 添加超越颜色的冗余编码
line_styles = ['-', '--', '-.', ':']
markers = ['o', 's', '^', 'v']

for i, (data, label) in enumerate(datasets):
    plt.plot(x, data, linestyle=line_styles[i % 4],
             marker=markers[i % 4], label=label)
```

## 统计严谨性

**始终包含：**
- 误差条（SD、SEM或CI - 在说明中指定）
- 样本大小（n）在图表或说明中
- 统计显著性标记（*、**、***）
- 尽可能包含单个数据点（不仅仅是汇总统计）

**带有统计信息的示例：**
```python
# 显示单个点和汇总统计
ax.scatter(x_jittered, individual_points, alpha=0.4, s=8)
ax.errorbar(x, means, yerr=sems, fmt='o', capsize=3)

# 标记显著性
ax.text(1.5, max_y * 1.1, '***', ha='center', fontsize=8)
```

## 使用不同的绘图库

### Matplotlib
- 对出版细节的控制最多
- 最适合复杂的多面板图表
- 使用提供的样式文件保持一致的格式
- 详见`references/matplotlib_examples.md`获取丰富示例

### Seaborn

Seaborn提供了一个高级的、面向数据集的统计图形界面，构建在matplotlib之上。它擅长用最少的代码创建可发表的统计可视化，同时保持与matplotlib定制的完全兼容性。

**科学可视化的主要优势：**
- 自动统计估计和置信区间
- 内置对多面板图表的支持（分面）
- 默认使用色盲友好的调色板
- 使用pandas DataFrames的面向数据集API
- 变量到视觉属性的语义映射

#### 带出版样式的快速入门

始终先应用matplotlib出版样式，然后配置seaborn：

```python
import seaborn as sns
import matplotlib.pyplot as plt
from style_presets import apply_publication_style

# 应用出版样式
apply_publication_style('default')

# 配置seaborn用于出版
sns.set_theme(style='ticks', context='paper', font_scale=1.1)
sns.set_palette('colorblind')  # 使用色盲友好的调色板

# 创建图表
fig, ax = plt.subplots(figsize=(3.5, 2.5))
sns.scatterplot(data=df, x='time', y='response', 
                hue='treatment', style='condition', ax=ax)
sns.despine()  # 移除顶部和右侧边框
```

#### 出版物常见图表类型

**统计比较：**
```python
# 带单个点的箱线图以提高透明度
fig, ax = plt.subplots(figsize=(3.5, 3))
sns.boxplot(data=df, x='treatment', y='response', 
            order=['Control', 'Low', 'High'], palette='Set2', ax=ax)
sns.stripplot(data=df, x='treatment', y='response',
              order=['Control', 'Low', 'High'], 
              color='black', alpha=0.3, size=3, ax=ax)
ax.set_ylabel('响应 (μM)')
sns.despine()
```

**分布分析：**
```python
# 带分割比较的小提琴图
fig, ax = plt.subplots(figsize=(4, 3))
sns.violinplot(data=df, x='timepoint', y='expression',
               hue='treatment', split=True, inner='quartile', ax=ax)
ax.set_ylabel('基因表达 (AU)')
sns.despine()
```

**相关矩阵：**
```python
# 带适当颜色映射和注释的热图
fig, ax = plt.subplots(figsize=(5, 4))
corr = df.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))  # 仅显示下三角
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f',
            cmap='RdBu_r', center=0, square=True,
            linewidths=1, cbar_kws={'shrink': 0.8}, ax=ax)
plt.tight_layout()
```

**带置信带的时间序列：**
```python
# 带自动CI计算的折线图
fig, ax = plt.subplots(figsize=(5, 3))
sns.lineplot(data=timeseries, x='time', y='measurement',
             hue='treatment', style='replicate',
             errorbar=('ci', 95), markers=True, dashes=False, ax=ax)
ax.set_xlabel('时间 (小时)')
ax.set_ylabel('测量值 (AU)')
sns.despine()
```

#### 使用Seaborn创建多面板图表

**使用FacetGrid进行自动分面：**
```python
# 创建分面图
g = sns.relplot(data=df, x='dose', y='response',
                hue='treatment', col='cell_line', row='timepoint',
                kind='line', height=2.5, aspect=1.2,
                errorbar=('ci', 95), markers=True)
g.set_axis_labels('剂量 (μM)', '响应 (AU)')
g.set_titles('{row_name} | {col_name}')
sns.despine()

# 以正确的DPI保存
from figure_export import save_publication_figure
save_publication_figure(g.figure, 'figure_facets', 
                       formats=['pdf', 'png'], dpi=300)
```

**将seaborn与matplotlib子图结合：**
```python
# 创建自定义多面板布局
fig, axes = plt.subplots(2, 2, figsize=(7, 6))

# 面板A：带回归的散点图
sns.regplot(data=df, x='predictor', y='response', ax=axes[0, 0])
axes[0, 0].text(-0.15, 1.05, 'A', transform=axes[0, 0].transAxes,
                fontsize=10, fontweight='bold')

# 面板B：分布比较
sns.violinplot(data=df, x='group', y='value', ax=axes[0, 1])
axes[0, 1].text(-0.15, 1.05, 'B', transform=axes[0, 1].transAxes,
                fontsize=10, fontweight='bold')

# 面板C：热图
sns.heatmap(correlation_data, cmap='viridis', ax=axes[1, 0])
axes[1, 0].text(-0.15, 1.05, 'C', transform=axes[1, 0].transAxes,
                fontsize=10, fontweight='bold')

# 面板D：时间序列
sns.lineplot(data=timeseries, x='time', y='signal', 
             hue='condition', ax=axes[1, 1])
axes[1, 1].text(-0.15, 1.05, 'D', transform=axes[1, 1].transAxes,
                fontsize=10, fontweight='bold')

plt.tight_layout()
sns.despine()
```

#### 出版物调色板

Seaborn包含多个色盲友好的调色板：

```python
# 使用内置的色盲调色板（推荐）
sns.set_palette('colorblind')

# 或指定自定义色盲友好颜色（Okabe-Ito）
okabe_ito = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
             '#0072B2', '#D55E00', '#CC79A7', '#000000']
sns.set_palette(okabe_ito)

# 对于热图和连续数据
sns.heatmap(data, cmap='viridis')  # 感知均匀
sns.heatmap(corr, cmap='RdBu_r', center=0)  # 发散，居中
```

#### 在轴级和图级函数之间选择

**轴级函数**（例如`scatterplot`、`boxplot`、`heatmap`）：
- 构建自定义多面板布局时使用
- 接受`ax=`参数进行精确定位
- 与matplotlib子图更好集成
- 对图表组合有更多控制

```python
fig, ax = plt.subplots(figsize=(3.5, 2.5))
sns.scatterplot(data=df, x='x', y='y', hue='group', ax=ax)
```

**图级函数**（例如`relplot`、`catplot`、`displot`）：
- 用于按分类变量自动分面
- 创建具有一致样式的完整图表
- 非常适合探索性分析
- 使用`height`和`aspect`进行大小调整

```python
g = sns.relplot(data=df, x='x', y='y', col='category', kind='scatter')
```

#### 使用Seaborn的统计严谨性

Seaborn自动计算并显示不确定性：

```python
# 折线图：默认显示均值 ± 95% CI
sns.lineplot(data=df, x='time', y='value', hue='treatment',
             errorbar=('ci', 95))  # 可更改为'sd'、'se'等

# 条形图：显示均值和自举CI
sns.barplot(data=df, x='treatment', y='response',
            errorbar=('ci', 95), capsize=0.1)

# 始终在图表说明中指定误差类型：
# "误差条表示95%置信区间"
```

#### 出版就绪Seaborn图表的最佳实践

1. **始终先设置出版主题：**
   ```python
   sns.set_theme(style='ticks', context='paper', font_scale=1.1)
   ```

2. **使用色盲友好的调色板：**
   ```python
   sns.set_palette('colorblind')
   ```

3. **移除不必要的元素：**
   ```python
   sns.despine()  # 移除顶部和右侧边框
   ```

4. **适当控制图表大小：**
   ```python
   # 轴级：使用matplotlib figsize
   fig, ax = plt.subplots(figsize=(3.5, 2.5))
   
   # 图级：使用height和aspect
   g = sns.relplot(..., height=3, aspect=1.2)
   ```

5. **尽可能显示单个数据点：**
   ```python
   sns.boxplot(...)  # 汇总统计
   sns.stripplot(..., alpha=0.3)  # 单个点
   ```

6. **包含带单位的适当标签：**
   ```python
   ax.set_xlabel('时间 (小时)')
   ax.set_ylabel('表达 (AU)')
   ```

7. **以正确的分辨率导出：**
   ```python
   from figure_export import save_publication_figure
   save_publication_figure(fig, 'figure_name', 
                          formats=['pdf', 'png'], dpi=300)
   ```

#### 高级Seaborn技术

**用于探索性分析的成对关系：**
```python
# 所有关系的快速概览
g = sns.pairplot(data=df, hue='condition', 
                 vars=['gene1', 'gene2', 'gene3'],
                 corner=True, diag_kind='kde', height=2)
```

**层次聚类热图：**
```python
# 对样本和特征进行聚类
g = sns.clustermap(expression_data, method='ward', 
                   metric='euclidean', z_score=0,
                   cmap='RdBu_r', center=0, 
                   figsize=(10, 8), 
                   row_colors=condition_colors,
                   cbar_kws={'label': 'Z-score'})
```

**带边际分布的联合分布：**
```python
# 带上下文的双变量分布
g = sns.jointplot(data=df, x='gene1', y='gene2',
                  hue='treatment', kind='scatter',
                  height=6, ratio=4, marginal_kws={'kde': True})
```

#### 常见Seaborn问题和解决方案

**问题：图例超出绘图区域**
```python
g = sns.relplot(...)
g._legend.set_bbox_to_anchor((0.9, 0.5))
```

**问题：标签重叠**
```python
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
```

**问题：最终尺寸下文本太小**
```python
sns.set_context('paper', font_scale=1.2)  # 如需增加
```

#### 其他资源

有关seaborn的更多详细信息，请参阅：
- `scientific-skills/seaborn/SKILL.md` - 全面的seaborn文档
- `scientific-skills/seaborn/references/examples.md` - 实用用例
- `scientific-skills/seaborn/references/function_reference.md` - 完整API参考
- `scientific-skills/seaborn/references/objects_interface.md` - 现代声明式API

### Plotly
- 用于探索的交互式图表
- 导出静态图像用于发表
- 配置为出版质量：
```python
fig.update_layout(
    font=dict(family='Arial, sans-serif', size=10),
    plot_bgcolor='white',
    # ... 见matplotlib_examples.md示例8
)
fig.write_image('figure.png', scale=3)  # scale=3 约为300 DPI
```

## 资源

### 参考目录

**根据需要加载这些以获取详细信息：**

- **`publication_guidelines.md`**：全面的最佳实践
  - 分辨率和文件格式要求
  - 排版指南
  - 布局和构图规则
  - 统计严谨性要求
  - 完整的出版清单

- **`color_palettes.md`**：颜色使用指南
  - 色盲友好调色板规范及RGB值
  - 序列和发散颜色映射建议
  - 可访问性测试程序
  - 特定领域调色板（基因组学、显微镜）

- **`journal_requirements.md`**：期刊特定规范
  - 出版商的技术要求
  - 文件格式和DPI规范
  - 图表尺寸要求
  - 快速参考表

- **`matplotlib_examples.md`**：实用代码示例
  - 10个完整的工作示例
  - 折线图、条形图、热图、多面板图表
  - 期刊特定图表示例
  - 每个库的提示（matplotlib、seaborn、plotly）

### 脚本目录

**使用这些辅助脚本进行自动化：**

- **`figure_export.py`**：导出工具
  - `save_publication_figure()`：以正确的DPI保存为多种格式
  - `save_for_journal()`：自动使用期刊特定要求
  - `check_figure_size()`：验证尺寸是否满足期刊规范
  - 直接运行：`python scripts/figure_export.py`查看示例

- **`style_presets.py`**：预配置样式
  - `apply_publication_style()`：应用预设样式（默认、nature、science、cell）
  - `set_color_palette()`：快速调色板切换
  - `configure_for_journal()`：一键式期刊配置
  - 直接运行：`python scripts/style_presets.py`查看示例

### 资产目录

**在图表中使用这些文件：**

- **`color_palettes.py`**：可导入的颜色定义
  - 所有推荐调色板作为Python常量
  - `apply_palette()`辅助函数
  - 可直接导入到笔记本/脚本中

- **Matplotlib样式文件**：与`plt.style.use()`一起使用
  - `publication.mplstyle`：一般出版质量
  - `nature.mplstyle`：Nature期刊规范
  - `presentation.mplstyle`：用于海报/幻灯片的更大字体

## 工作流程摘要

**创建出版图表的推荐工作流程：**

1. **计划**：确定目标期刊、图表类型和内容
2. **配置**：为期刊应用适当的样式
   ```python
   from style_presets import configure_for_journal
   configure_for_journal('nature', 'single')
   ```
3. **创建**：构建具有适当标签、颜色和统计信息的图表
4. **验证**：检查尺寸、字体、颜色、可访问性
   ```python
   from figure_export import check_figure_size
   check_figure_size(fig, journal='nature')
   ```
5. **导出**：以所需格式保存
   ```python
   from figure_export import save_for_journal
   save_for_journal(fig, 'figure1', 'nature', 'combination')
   ```
6. **审查**：在 manuscript 上下文中查看最终尺寸

## 应避免的常见陷阱

1. **字体太小**：最终打印尺寸下文本不可读
2. **JPEG格式**：绝不要使用JPEG用于图表/绘图（会产生伪影）
3. **红绿颜色**：约8%的男性无法区分
4. **低分辨率**：出版物中的像素化图表
5. **缺少单位**：始终为轴添加单位标签
6. **3D效果**：扭曲感知，完全避免
7. **图表垃圾**：移除不必要的网格线、装饰
8. **截断轴**：条形图从零点开始，除非有科学依据
9. **样式不一致**：同一手稿中不同图表的字体/颜色不同
10. **无误差条**：始终显示不确定性

## 最终清单

在提交图表之前，验证：

- [ ] 分辨率满足期刊要求（300+ DPI）
- [ ] 文件格式正确（图表使用矢量格式，图像使用TIFF）
- [ ] 图表尺寸符合期刊规范
- [ ] 所有文本在最终尺寸下可读（≥6 pt）
- [ ] 颜色对色盲友好
- [ ] 图表在灰度下可工作
- [ ] 所有轴都有单位标签
- [ ] 存在误差条并在说明中定义
- [ ] 面板标签存在且一致
- [ ] 无图表垃圾或3D效果
- [ ] 所有图表字体一致
- [ ] 统计显著性标记清晰
- [ ] 图例清晰完整

使用此技能确保科学图表符合最高出版标准，同时对所有读者保持可访问性。