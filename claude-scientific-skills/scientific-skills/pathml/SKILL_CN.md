---
name: pathml
description: 功能齐全的计算病理学工具包。用于高级 WSI 分析，包括多重免疫荧光（CODEX、Vectra）、细胞核分割、组织图构建和病理学数据的 ML 模型训练。支持 160+ 幻灯片格式。对于从 H&E 幻灯片中提取简单瓦片，histolab 可能更简单。
license: GPL-2.0 license
metadata:
    skill-author: K-Dense Inc.
---

# PathML

## 概述

PathML 是一个用于计算病理学工作流程的综合 Python 工具包，旨在促进全幻灯片病理学图像的机器学习和图像分析。该框架提供模块化、可组合的工具，用于加载各种幻灯片格式、预处理图像、构建空间图、训练深度学习模型，以及分析来自 CODEX 和多重免疫荧光等技术的多参数成像数据。

## 何时使用此技能

应用此技能用于：
- 加载和处理各种专有格式的全幻灯片图像（WSI）
- 使用染色标准化预处理 H&E 染色组织图像
- 细胞核检测、分割和分类工作流程
- 构建用于空间分析的细胞和组织图
- 在病理学数据上训练或部署机器学习模型（HoVer-Net、HACTNet）
- 分析用于空间蛋白质组学的多参数成像（CODEX、Vectra、MERFISH）
- 量化来自多重免疫荧光的标记物表达
- 使用 HDF5 存储管理大规模病理学数据集
- 基于瓦片的分析和拼接操作

## 核心功能

PathML 提供六个主要功能领域，在参考文件中有详细记录：

### 1. 图像加载和格式

从 160+ 专有格式加载全幻灯片图像，包括 Aperio SVS、Hamamatsu NDPI、Leica SCN、Zeiss ZVI、DICOM 和 OME-TIFF。PathML 自动处理供应商特定格式，并提供统一的接口用于访问图像金字塔、元数据和感兴趣区域。

**请参阅：** `references/image_loading.md` 了解支持的格式、加载策略和处理不同幻灯片类型。

### 2. 预处理管道

通过组合用于图像操作、质量控制、染色标准化、组织检测和掩码操作的变换来构建模块化预处理管道。PathML 的 Pipeline 架构实现了跨大型数据集的可重现、可扩展预处理。

**关键变换：**
- `StainNormalizationHE` - Macenko/Vahadane 染色标准化
- `TissueDetectionHE`、`NucleusDetectionHE` - 组织/细胞核分割
- `MedianBlur`、`GaussianBlur` - 噪声减少
- `LabelArtifactTileHE` - 伪影的质量控制

**请参阅：** `references/preprocessing.md` 了解完整的变换目录、管道构建和预处理工作流程。

### 3. 图构建

构建表示细胞和组织级别关系的空间图。从分割对象中提取特征，创建适合图神经网络和空间分析的基于图的表示。

**请参阅：** `references/graphs.md` 了解图构建方法、特征提取和空间分析工作流程。

### 4. 机器学习

训练和部署用于细胞核检测、分割和分类的深度学习模型。PathML 集成 PyTorch，带有预构建模型（HoVer-Net、HACTNet）、自定义 DataLoaders 和用于推理的 ONNX 支持。

**关键模型：**
- **HoVer-Net** - 同时进行细胞核分割和分类
- **HACTNet** - 层次化细胞类型分类

**请参阅：** `references/machine_learning.md` 了解模型训练、评估、推理工作流程以及处理公共数据集。

### 5. 多参数成像

分析来自 CODEX、Vectra、MERFISH 和其他多重成像平台的空间蛋白质组学和基因表达数据。PathML 提供专门的幻灯片类和变换，用于处理多参数数据、使用 Mesmer 进行细胞分割和量化工作流程。

**请参阅：** `references/multiparametric.md` 了解 CODEX/Vectra 工作流程、细胞分割、标记物量化以及与 AnnData 的集成。

### 6. 数据管理

使用 HDF5 格式高效存储和管理大型病理学数据集。PathML 在为机器学习工作流程优化的统一存储结构中处理瓦片、掩码、元数据和提取的特征。

**请参阅：** `references/data_management.md` 了解 HDF5 集成、瓦片管理、数据集组织和批处理策略。

## 快速开始

### 安装

```bash
# 安装 PathML
uv pip install pathml

# 安装所有功能的可选依赖
uv pip install pathml[all]
```

### 基本工作流程示例

```python
from pathml.core import SlideData
from pathml.preprocessing import Pipeline, StainNormalizationHE, TissueDetectionHE

# 加载全幻灯片图像
wsi = SlideData.from_slide("path/to/slide.svs")

# 创建预处理管道
pipeline = Pipeline([
    TissueDetectionHE(),
    StainNormalizationHE(target='normalize', stain_estimation_method='macenko')
])

# 运行管道
pipeline.run(wsi)

# 访问处理后的瓦片
for tile in wsi.tiles:
    processed_image = tile.image
    tissue_mask = tile.masks['tissue']
```

### 常见工作流程

**H&E 图像分析：**
1. 使用适当的幻灯片类加载 WSI
2. 应用组织检测和染色标准化
3. 执行细胞核检测或训练分割模型
4. 提取特征并构建空间图
5. 进行下游分析

**多参数成像（CODEX）：**
1. 使用 `CODEXSlide` 加载 CODEX 幻灯片
2. 折叠多轮通道数据
3. 使用 Mesmer 模型分割细胞
4. 量化标记物表达
5. 导出到 AnnData 进行单细胞分析

**训练 ML 模型：**
1. 使用公共病理学数据准备数据集
2. 使用 PathML 数据集创建 PyTorch DataLoader
3. 训练 HoVer-Net 或自定义模型
4. 在保留的测试集上评估
5. 使用 ONNX 部署进行推理

## 详细文档参考

在处理特定任务时，请参考适当的参考文件以获取全面信息：

- **加载图像：** `references/image_loading.md`
- **预处理工作流程：** `references/preprocessing.md`
- **空间分析：** `references/graphs.md`
- **模型训练：** `references/machine_learning.md`
- **CODEX/多重 IF：** `references/multiparametric.md`
- **数据存储：** `references/data_management.md`

## 资源

此技能包括按功能领域组织的综合参考文档。每个参考文件包含详细的 API 信息、工作流程示例、最佳实践以及针对特定 PathML 功能的故障排除指南。

### references/

提供 PathML 功能深入覆盖的文档文件：

- `image_loading.md` - 全幻灯片图像格式、加载策略、幻灯片类
- `preprocessing.md` - 完整的变换目录、管道构建、预处理工作流程
- `graphs.md` - 图构建方法、特征提取、空间分析
- `machine_learning.md` - 模型架构、训练工作流程、评估、推理
- `multiparametric.md` - CODEX、Vectra、多重 IF 分析、细胞分割、量化
- `data_management.md` - HDF5 存储、瓦片管理、批处理、数据集组织

在处理特定计算病理学任务时，根据需要加载这些参考资料。