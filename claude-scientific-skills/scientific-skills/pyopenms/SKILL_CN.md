---
name: pyopenms
description: 完整的质谱分析平台。用于蛋白质组学工作流程的特征检测、肽段鉴定、蛋白质定量和复杂的LC-MS/MS管线。支持广泛的文件格式和算法。最适合蛋白质组学、全面的MS数据处理。对于简单的光谱比较和代谢物ID使用matchms。
license: 3 clause BSD license
metadata:
    skill-author: K-Dense Inc.
---

# PyOpenMS

## 概述

PyOpenMS为OpenMS库提供Python绑定，用于计算质谱分析，实现蛋白质组学和代谢组学数据的分析。用于处理质谱文件格式、处理光谱数据、检测特征、鉴定肽段/蛋白质以及执行定量分析。

## 安装

使用uv安装：

```bash
uv pip install pyopenms
```

验证安装：

```python
import pyopenms
print(pyopenms.__version__)
```

## 核心功能

PyOpenMS将功能组织为以下领域：

### 1. 文件I/O和数据格式

处理质谱文件格式并在表示之间转换。

**支持的格式**：mzML, mzXML, TraML, mzTab, FASTA, pepXML, protXML, mzIdentML, featureXML, consensusXML, idXML

基本文件读取：

```python
import pyopenms as ms

# 读取mzML文件
exp = ms.MSExperiment()
ms.MzMLFile().load("data.mzML", exp)

# 访问光谱
for spectrum in exp:
    mz, intensity = spectrum.get_peaks()
    print(f"Spectrum: {len(mz)} peaks")
```

**详细文件处理**：请参见 `references/file_io.md`

### 2. 信号处理

使用平滑、过滤、中心化和归一化处理原始光谱数据。

基本光谱处理：

```python
# 使用高斯过滤器平滑光谱
gaussian = ms.GaussFilter()
params = gaussian.getParameters()
params.setValue("gaussian_width", 0.1)
gaussian.setParameters(params)
gaussian.filterExperiment(exp)
```

**算法详情**：请参见 `references/signal_processing.md`

### 3. 特征检测

检测并链接跨光谱和样本的特征以进行定量分析。

```python
# 检测特征
ff = ms.FeatureFinder()
ff.run("centroided", exp, features, params, ms.FeatureMap())
```

**完整工作流**：请参见 `references/feature_detection.md`

### 4. 肽段和蛋白质鉴定

集成搜索引擎并处理鉴定结果。

**支持的引擎**：Comet, Mascot, MSGFPlus, XTandem, OMSSA, Myrimatch

基本鉴定工作流：

```python
# 加载鉴定数据
protein_ids = []
peptide_ids = []
ms.IdXMLFile().load("identifications.idXML", protein_ids, peptide_ids)

# 应用FDR过滤
fdr = ms.FalseDiscoveryRate()
fdr.apply(peptide_ids)
```

**详细工作流**：请参见 `references/identification.md`

### 5. 代谢组学分析

执行非靶向代谢组学前处理和分析。

典型工作流：
1. 加载和处理原始数据
2. 检测特征
3. 跨样本对齐保留时间
4. 将特征链接到共识图谱
5. 使用化合物数据库进行注释

**完整代谢组学工作流**：请参见 `references/metabolomics.md`

## 数据结构

PyOpenMS使用以下主要对象：

- **MSExperiment**：光谱和色谱图的集合
- **MSSpectrum**：具有m/z和强度对的单个质谱
- **MSChromatogram**：色谱迹
- **Feature**：检测到的色谱峰，带有质量指标
- **FeatureMap**：特征的集合
- **PeptideIdentification**：肽段的搜索结果
- **ProteinIdentification**：蛋白质的搜索结果

**详细文档**：请参见 `references/data_structures.md`

## 常见工作流

### 快速开始：加载和探索数据

```python
import pyopenms as ms

# 加载mzML文件
exp = ms.MSExperiment()
ms.MzMLFile().load("sample.mzML", exp)

# 获取基本统计信息
print(f"Number of spectra: {exp.getNrSpectra()}")
print(f"Number of chromatograms: {exp.getNrChromatograms()}")

# 检查第一个光谱
spec = exp.getSpectrum(0)
print(f"MS level: {spec.getMSLevel()}")
print(f"Retention time: {spec.getRT()}")
mz, intensity = spec.get_peaks()
print(f"Peaks: {len(mz)}")
```

### 参数管理

大多数算法使用参数系统：

```python
# 获取算法参数
algo = ms.GaussFilter()
params = algo.getParameters()

# 查看可用参数
for param in params.keys():
    print(f"{param}: {params.getValue(param)}")

# 修改参数
params.setValue("gaussian_width", 0.2)
algo.setParameters(params)
```

### 导出到Pandas

将数据转换为pandas DataFrame进行分析：

```python
import pyopenms as ms
import pandas as pd

# 加载特征图谱
fm = ms.FeatureMap()
ms.FeatureXMLFile().load("features.featureXML", fm)

# 转换为DataFrame
df = fm.get_df()
print(df.head())
```

## 与其他工具集成

PyOpenMS与以下工具集成：
- **Pandas**：将数据导出到DataFrame
- **NumPy**：处理峰数组
- **Scikit-learn**：对MS数据进行机器学习
- **Matplotlib/Seaborn**：可视化
- **R**：通过rpy2桥接

## 资源

- **官方文档**：https://pyopenms.readthedocs.io
- **OpenMS文档**：https://www.openms.org
- **GitHub**：https://github.com/OpenMS/OpenMS

## 参考

- `references/file_io.md` - 综合文件格式处理
- `references/signal_processing.md` - 信号处理算法
- `references/feature_detection.md` - 特征检测和链接
- `references/identification.md` - 肽段和蛋白质鉴定
- `references/metabolomics.md` - 代谢组学特定工作流
- `references/data_structures.md` - 核心对象和数据结构