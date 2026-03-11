---
name: histolab
description: 轻量级WSI切片提取和预处理。用于基本幻灯片处理、组织检测、切片提取、H&E图像的染色归一化。最适合简单流程、数据集准备、快速基于切片的分析。对于高级空间蛋白质组学、多重成像或深度学习流程，请使用pathml。
license: Apache-2.0 license
metadata:
    skill-author: K-Dense Inc.
---

# Histolab

## 概述

Histolab是一个用于处理数字病理学中全切片图像（WSI）的Python库。它自动化组织检测，从千兆像素图像中提取信息丰富的切片，并为深度学习流程准备数据集。该库支持多种WSI格式，实现了复杂的组织分割，并提供灵活的切片提取策略。

## 安装

```bash
uv pip install histolab
```

## 快速开始

从全切片图像提取切片的基本工作流程：

```python
from histolab.slide import Slide
from histolab.tiler import RandomTiler

# 加载切片
slide = Slide("slide.svs", processed_path="output/")

# 配置切片器
tiler = RandomTiler(
    tile_size=(512, 512),
    n_tiles=100,
    level=0,
    seed=42
)

# 预览切片位置
tiler.locate_tiles(slide, n_tiles=20)

# 提取切片
tiler.extract(slide)
```

## 核心功能

### 1. 切片管理

加载、检查和处理各种格式的全切片图像。

**常用操作：**
- 加载WSI文件（SVS、TIFF、NDPI等）
- 访问切片元数据（尺寸、放大倍数、属性）
- 生成缩略图用于可视化
- 处理金字塔图像结构
- 在特定坐标处提取区域

**关键类：** `Slide`

**参考：** `references/slide_management.md` 包含关于以下内容的综合文档：
- 切片初始化和配置
- 内置样本数据集（前列腺、卵巢、乳腺、心脏、肾脏组织）
- 访问切片属性和元数据
- 缩略图生成和可视化
- 处理金字塔级别
- 多切片处理工作流

**示例工作流程：**
```python
from histolab.slide import Slide
from histolab.data import prostate_tissue

# 加载样本数据
prostate_svs, prostate_path = prostate_tissue()

# 初始化切片
slide = Slide(prostate_path, processed_path="output/")

# 检查属性
print(f"尺寸：{slide.dimensions}")
print(f"级别：{slide.levels}")
print(f"放大倍数：{slide.properties.get('openslide.objective-power')}")

# 保存缩略图
slide.save_thumbnail()
```

### 2. 组织检测和掩膜

自动识别组织区域并过滤背景/伪影。

**常用操作：**
- 创建二进制组织掩膜
- 检测最大组织区域
- 排除背景和伪影
- 自定义组织分割
- 移除笔注释

**关键类：** `TissueMask`、`BiggestTissueBoxMask`、`BinaryMask`

**参考：** `references/tissue_masks.md` 包含关于以下内容的综合文档：
- TissueMask：使用自动过滤器分割所有组织区域
- BiggestTissueBoxMask：返回最大组织区域的边界框（默认）
- BinaryMask：自定义掩膜实现的基类
- 使用`locate_mask()`可视化掩膜
- 创建自定义矩形和注释排除掩膜
- 掩膜与切片提取的集成
- 最佳实践和故障排除

**示例工作流程：**
```python
from histolab.masks import TissueMask, BiggestTissueBoxMask

# 为所有组织区域创建组织掩膜
tissue_mask = TissueMask()

# 在切片上可视化掩膜
slide.locate_mask(tissue_mask)

# 获取掩膜数组
mask_array = tissue_mask(slide)

# 使用最大组织区域（大多数提取器的默认设置）
biggest_mask = BiggestTissueBoxMask()
```

**何时使用每种掩膜：**
- `TissueMask`：多个组织部分，综合分析
- `BiggestTissueBoxMask`：单个主要组织部分，排除伪影（默认）
- 自定义`BinaryMask`：特定感兴趣区域ROI，排除注释，自定义分割

### 3. 切片提取

使用不同策略从大型WSI中提取较小区域。

**三种提取策略：**

**RandomTiler：** 提取固定数量的随机定位切片
- 最适合：采样多样化区域、探索性分析、训练数据
- 关键参数：`n_tiles`、用于可重复性的`seed`

**GridTiler：** 以网格模式系统性地提取组织切片
- 最适合：完整覆盖、空间分析、重建
- 关键参数：用于滑动窗口的`pixel_overlap`

**ScoreTiler：** 基于评分函数提取排名靠前的切片
- 最适合：信息最丰富的区域、质量驱动选择
- 关键参数：`scorer`（NucleiScorer、CellularityScorer、自定义）

**常用参数：**
- `tile_size`：切片尺寸（例如，(512, 512)）
- `level`：提取的金字塔级别（0 = 最高分辨率）
- `check_tissue`：按组织内容过滤切片
- `tissue_percent`：最小组织覆盖率（默认80%）
- `extraction_mask`：定义提取区域的掩膜

**参考：** `references/tile_extraction.md` 包含关于以下内容的综合文档：
- 每种切片器策略的详细说明
- 可用评分器（NucleiScorer、CellularityScorer、自定义）
- 使用`locate_tiles()`进行切片预览
- 提取工作流程和报告
- 高级模式（多级别、分层提取）
- 性能优化和故障排除

**示例工作流程：**

```python
from histolab.tiler import RandomTiler, GridTiler, ScoreTiler
from histolab.scorer import NucleiScorer

# 随机采样（快速、多样化）
random_tiler = RandomTiler(
    tile_size=(512, 512),
    n_tiles=100,
    level=0,
    seed=42,
    check_tissue=True,
    tissue_percent=80.0
)
random_tiler.extract(slide)

# 网格覆盖（全面）
grid_tiler = GridTiler(
    tile_size=(512, 512),
    level=0,
    pixel_overlap=0,
    check_tissue=True
)
grid_tiler.extract(slide)

# 基于评分的选择（信息最丰富）
score_tiler = ScoreTiler(
    tile_size=(512, 512),
    n_tiles=50,
    scorer=NucleiScorer(),
    level=0
)
score_tiler.extract(slide, report_path="tiles_report.csv")
```

**提取前始终预览：**
```python
# 在缩略图上预览切片位置
tiler.locate_tiles(slide, n_tiles=20)
```

### 4. 过滤器和预处理

应用图像处理过滤器进行组织检测、质量控制和预处理。

**过滤器类别：**

**图像过滤器：** 色彩空间转换、阈值处理、对比度增强
- `RgbToGrayscale`、`RgbToHsv`、`RgbToHed`
- `OtsuThreshold`、`AdaptiveThreshold`
- `StretchContrast`、`HistogramEqualization`

**形态学过滤器：** 二进制图像上的结构操作
- `BinaryDilation`、`BinaryErosion`
- `BinaryOpening`、`BinaryClosing`
- `RemoveSmallObjects`、`RemoveSmallHoles`

**组合：** 将多个过滤器链接在一起
- `Compose`：创建过滤器流程

**参考：** `references/filters_preprocessing.md` 包含关于以下内容的综合文档：
- 每种过滤器类型的详细说明
- 过滤器组合和链接
- 常用预处理流程（组织检测、笔移除、细胞核增强）
- 将过滤器应用于切片
- 自定义掩膜过滤器
- 质量控制过滤器（模糊检测、组织覆盖率）
- 最佳实践和故障排除

**示例工作流程：**

```python
from histolab.filters.compositions import Compose
from histolab.filters.image_filters import RgbToGrayscale, OtsuThreshold
from histolab.filters.morphological_filters import (
    BinaryDilation, RemoveSmallHoles, RemoveSmallObjects
)

# 标准组织检测流程
tissue_detection = Compose([
    RgbToGrayscale(),
    OtsuThreshold(),
    BinaryDilation(disk_size=5),
    RemoveSmallHoles(area_threshold=1000),
    RemoveSmallObjects(area_threshold=500)
])

# 与自定义掩膜一起使用
from histolab.masks import TissueMask
custom_mask = TissueMask(filters=tissue_detection)

# 将过滤器应用于切片
from histolab.tile import Tile
filtered_tile = tile.apply_filters(tissue_detection)
```

### 5. 可视化

可视化切片、掩膜、切片位置和提取质量。

**常用可视化任务：**
- 显示切片缩略图
- 可视化组织掩膜
- 预览切片位置
- 评估切片质量
- 创建报告和图表

**参考：** `references/visualization.md` 包含关于以下内容的综合文档：
- 切片缩略图显示和保存
- 使用`locate_mask()`进行掩膜可视化
- 使用`locate_tiles()`进行切片位置预览
- 显示提取的切片和马赛克
- 质量评估（评分分布、顶部与底部切片）
- 多切片可视化
- 过滤器效果可视化
- 导出高分辨率图表和PDF报告
- Jupyter笔记本中的交互式可视化

**示例工作流程：**

```python
import matplotlib.pyplot as plt
from histolab.masks import TissueMask

# 显示切片缩略图
plt.figure(figsize=(10, 10))
plt.imshow(slide.thumbnail)
plt.title(f"切片：{slide.name}")
plt.axis('off')
plt.show()

# 可视化组织掩膜
tissue_mask = TissueMask()
slide.locate_mask(tissue_mask)

# 预览切片位置
tiler = RandomTiler(tile_size=(512, 512), n_tiles=50)
tiler.locate_tiles(slide, n_tiles=20)

# 以网格形式显示提取的切片
from pathlib import Path
from PIL import Image

tile_paths = list(Path("output/tiles/").glob("*.png"))[:16]
fig, axes = plt.subplots(4, 4, figsize=(12, 12))
axes = axes.ravel()

for idx, tile_path in enumerate(tile_paths):
    tile_img = Image.open(tile_path)
    axes[idx].imshow(tile_img)
    axes[idx].set_title(tile_path.stem, fontsize=8)
    axes[idx].axis('off')

plt.tight_layout()
plt.show()
```

## 典型工作流程

### 工作流程1：探索性切片提取

对多样化组织区域进行快速采样以进行初步分析。

```python
from histolab.slide import Slide
from histolab.tiler import RandomTiler
import logging

# 启用日志记录以跟踪进度
logging.basicConfig(level=logging.INFO)

# 加载切片
slide = Slide("slide.svs", processed_path="output/random_tiles/")

# 检查切片
print(f"尺寸：{slide.dimensions}")
print(f"级别：{slide.levels}")
slide.save_thumbnail()

# 配置随机切片器
random_tiler = RandomTiler(
    tile_size=(512, 512),
    n_tiles=100,
    level=0,
    seed=42,
    check_tissue=True,
    tissue_percent=80.0
)

# 预览位置
random_tiler.locate_tiles(slide, n_tiles=20)

# 提取切片
random_tiler.extract(slide)
```

### 工作流程2：全面网格提取

用于全切片分析的完整组织覆盖。

```python
from histolab.slide import Slide
from histolab.tiler import GridTiler
from histolab.masks import TissueMask

# 加载切片
slide = Slide("slide.svs", processed_path="output/grid_tiles/")

# 使用TissueMask处理所有组织部分
tissue_mask = TissueMask()
slide.locate_mask(tissue_mask)

# 配置网格切片器
grid_tiler = GridTiler(
    tile_size=(512, 512),
    level=1,  # 使用级别1进行更快的提取
    pixel_overlap=0,
    check_tissue=True,
    tissue_percent=70.0
)

# 预览网格
grid_tiler.locate_tiles(slide)

# 提取所有切片
grid_tiler.extract(slide, extraction_mask=tissue_mask)
```

### 工作流程3：质量驱动的切片选择

基于细胞核密度提取信息最丰富的切片。

```python
from histolab.slide import Slide
from histolab.tiler import ScoreTiler
from histolab.scorer import NucleiScorer
import pandas as pd
import matplotlib.pyplot as plt

# 加载切片
slide = Slide("slide.svs", processed_path="output/scored_tiles/")

# 配置评分切片器
score_tiler = ScoreTiler(
    tile_size=(512, 512),
    n_tiles=50,
    level=0,
    scorer=NucleiScorer(),
    check_tissue=True
)

# 预览顶部切片
score_tiler.locate_tiles(slide, n_tiles=15)

# 提取并生成报告
score_tiler.extract(slide, report_path="tiles_report.csv")

# 分析评分
report_df = pd.read_csv("tiles_report.csv")
plt.hist(report_df['score'], bins=20, edgecolor='black')
plt.xlabel('切片评分')
plt.ylabel('频率')
plt.title('切片评分分布')
plt.show()
```

### 工作流程4：多切片处理流程

使用一致参数处理整个切片集合。

```python
from pathlib import Path
from histolab.slide import Slide
from histolab.tiler import RandomTiler
import logging

logging.basicConfig(level=logging.INFO)

# 配置一次切片器
tiler = RandomTiler(
    tile_size=(512, 512),
    n_tiles=50,
    level=0,
    seed=42,
    check_tissue=True
)

# 处理所有切片
slide_dir = Path("slides/")
output_base = Path("output/")

for slide_path in slide_dir.glob("*.svs"):
    print(f"\n处理中：{slide_path.name}")

    # 创建切片特定的输出目录
    output_dir = output_base / slide_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    # 加载并处理切片
    slide = Slide(slide_path, processed_path=output_dir)

    # 保存缩略图以供审查
    slide.save_thumbnail()

    # 提取切片
    tiler.extract(slide)

    print(f"完成：{slide_path.name}")
```

### 工作流程5：自定义组织检测和过滤

处理带有伪影、注释或异常染色的切片。

```python
from histolab.slide import Slide
from histolab.masks import TissueMask
from histolab.tiler import RandomTiler
from histolab.filters.compositions import Compose
from histolab.filters.image_filters import RgbToGrayscale, OtsuThreshold
from histolab.filters.morphological_filters import (
    BinaryDilation, RemoveSmallObjects, RemoveSmallHoles
)

# 定义用于激进伪影移除的自定义过滤器流程
aggressive_filters = Compose([
    RgbToGrayscale(),
    OtsuThreshold(),
    BinaryDilation(disk_size=10),
    RemoveSmallHoles(area_threshold=5000),
    RemoveSmallObjects(area_threshold=3000)  # 移除更大的伪影
])

# 创建自定义掩膜
custom_mask = TissueMask(filters=aggressive_filters)

# 加载切片并可视化掩膜
slide = Slide("slide.svs", processed_path="output/")
slide.locate_mask(custom_mask)

# 使用自定义掩膜提取
tiler = RandomTiler(tile_size=(512, 512), n_tiles=100)
tiler.extract(slide, extraction_mask=custom_mask)
```

## 最佳实践

### 切片加载和检查
1. 处理前始终检查切片属性
2. 保存缩略图以供快速视觉审查
3. 检查金字塔级别和尺寸
4. 使用缩略图验证组织是否存在

### 组织检测
1. 提取前使用`locate_mask()`预览掩膜
2. 对多个部分使用`TissueMask`，对单个部分使用`BiggestTissueBoxMask`
3. 为特定染色（H&E vs IHC）自定义过滤器
4. 使用自定义掩膜处理笔注释
5. 在多样化切片上测试掩膜

### 切片提取
1. **提取前始终使用`locate_tiles()`预览**
2. 选择适当的切片器：
   - RandomTiler：采样和探索
   - GridTiler：完整覆盖
   - ScoreTiler：质量驱动选择
3. 设置适当的`tissue_percent`阈值（典型70-90%）
4. 在RandomTiler中使用种子以确保可重复性
5. 在适当的金字塔级别提取以进行分辨率分析
6. 为大型数据集启用日志记录

### 性能
1. 在较低级别（1、2）提取以加快处理速度
2. 适当时使用`BiggestTissueBoxMask`而不是`TissueMask`
3. 调整`tissue_percent`以减少无效切片尝试
4. 限制初始探索的`n_tiles`
5. 对非重叠网格使用`pixel_overlap=0`

### 质量控制
1. 验证切片质量（检查模糊、伪影、焦点）
2. 审查ScoreTiler的评分分布
3. 检查顶部和底部评分切片
4. 监控组织覆盖率统计
5. 如有需要，按其他质量指标过滤提取的切片

## 常见用例

### 训练深度学习模型
- 使用RandomTiler跨多个切片提取平衡数据集
- 使用带有NucleiScorer的ScoreTiler专注于细胞丰富的区域
- 以一致分辨率提取（级别0或级别1）
- 生成CSV报告以跟踪切片元数据

### 全切片分析
- 使用GridTiler进行完整组织覆盖
- 在多个金字塔级别提取以进行分层分析
- 使用网格位置保持空间关系
- 使用`pixel_overlap`进行滑动窗口方法

### 组织表征
- 使用RandomTiler采样多样化区域
- 使用掩膜量化组织覆盖率
- 使用HED分解提取染色特定信息
- 跨切片比较组织模式

### 质量评估
- 使用ScoreTiler识别最佳焦点区域
- 使用自定义掩膜和过滤器检测伪影
- 跨切片集合评估染色质量
- 标记有问题的切片以供手动审查

### 数据集策展
- 使用ScoreTiler优先考虑信息丰富的切片
- 按组织百分比过滤切片
- 生成包含切片评分和元数据的报告
- 跨切片和组织类型创建分层化数据集

## 故障排除

### 未提取切片
- 降低`tissue_percent`阈值
- 验证切片包含组织（检查缩略图）
- 确保extraction_mask捕获组织区域
- 检查tile_size是否适合切片分辨率

### 许多背景切片
- 启用`check_tissue=True`
- 提高`tissue_percent`阈值
- 使用适当的掩膜（TissueMask vs BiggestTissueBoxMask）
- 自定义掩膜过滤器以更好地检测组织

### 提取非常慢
- 在较低金字塔级别提取（level=1或2）
- 减少RandomTiler/ScoreTiler的`n_tiles`
- 使用RandomTiler而不是GridTiler进行采样
- 使用BiggestTissueBoxMask而不是TissueMask

### 切片有伪影
- 实现自定义注释排除掩膜
- 调整过滤器参数以进行伪影移除
- 增加小对象移除阈值
- 应用提取后质量过滤

### 跨切片结果不一致
- 为RandomTiler使用相同的种子
- 使用预处理过滤器归一化染色
- 按染色质量调整`tissue_percent`
- 实现切片特定的掩膜自定义

## 资源

此技能在`references/`目录中包含详细的参考文档：

### references/slide_management.md
加载、检查和处理全切片图像的综合指南：
- 切片初始化和配置
- 内置样本数据集
- 切片属性和元数据
- 缩略图生成和可视化
- 处理金字塔级别
- 多切片处理工作流
- 最佳实践和常见模式

### references/tissue_masks.md
组织检测和掩膜的完整文档：
- TissueMask、BiggestTissueBoxMask、BinaryMask类
- 组织检测过滤器的工作原理
- 使用过滤器链自定义掩膜
- 可视化掩膜
- 创建自定义矩形和注释排除掩膜
- 与切片提取的集成
- 最佳实践和故障排除

### references/tile_extraction.md
切片提取策略的详细说明：
- RandomTiler、GridTiler、ScoreTiler比较
- 可用评分器（NucleiScorer、CellularityScorer、自定义）
- 常用和策略特定参数
- 使用locate_tiles()进行切片预览
- 提取工作流程和CSV报告
- 高级模式（多级别、分层）
- 性能优化
- 常见问题故障排除

### references/filters_preprocessing.md
完整过滤器参考和预处理指南：
- 图像过滤器（色彩转换、阈值处理、对比度）
- 形态学过滤器（膨胀、腐蚀、开闭运算）
- 过滤器组合和链接
- 常用预处理流程
- 将过滤器应用于切片
- 自定义掩膜过滤器
- 质量控制过滤器
- 最佳实践和故障排除

### references/visualization.md
综合可视化指南：
- 切片缩略图显示和保存
- 掩膜可视化技术
- 切片位置预览
- 显示提取的切片和创建马赛克
- 质量评估可视化
- 多切片比较
- 过滤器效果可视化
- 导出高分辨率图表和PDF
- Jupyter笔记本中的交互式可视化

**使用模式：** 参考文件包含深入信息以支持此主要技能文档中描述的工作流程。根据需要加载特定的参考文件以获取详细实施指导、故障排除或高级功能。
